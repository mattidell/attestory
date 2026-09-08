"""Nominee-Allocation Assertion Recording, Track 2: recovery and read integration.

Milestone ``docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md``.
Track 1 owns the production acceptance boundary
(``packages.tax.nominee_allocation_recording``): it rebuilds from the log,
validates, appends at exact successive revisions, and returns only after the
durable log reprojects. This module does not rebuild that boundary, wrap it,
or re-prove that it persists.

Given a workspace that already contains allocations, this module rebuilds
from a **committed act log only** — never from in-memory state handed over
as authoritative — and exposes:

- the current allocations (amount, recipient display label, contribution
  and evidence provenance) at each
  ``(payer, statement, tax-year, recipient)`` identity;
- recoverable attribution for a current allocation (assertion act, actor,
  time) and, for a retracted one, what was said, who said it, and who
  later ended current support (via the ``("retraction", <act id>)``
  displacement reason) -- never that the original actor recanted;
- the report join, with deterministic ``report_fact_id`` always present and
  ``current_report_finding_id`` possibly absent.

``packages.kernel.read_models.build_read_model`` does not expose entity
labels, actor/time, or ``CurrencyView.reasons``. A tax-specific recovery
view is therefore the expected consumer of those. It composes
``findings.project``, ``currency.compute_currency``, and the fact/entity
lattice, and indexes the original acts for attribution.

**The one invariant:** ``compute_currency`` remains the sole definition of
current standing. This module consults that view; it does not re-derive
what is current by any other rule, and it does not cache standing into a
second source of truth. ``packages/kernel/`` is unchanged.

**What a reader of this view may say.** An allocation is recorded, by whom
and when. One was removed from current use, by whom and when.

**What a reader of this view may not say.** That the original actor
recanted. That no allocation exists in the world. That absence of an
allocation means the taxpayer owns the full amount. Actor is opaque
provenance; admission never consults actor identity and no permission is
enforced here.

**Remaining coordinator work (Track 2 deliverable 4): none.** Track 1
answered the carried production/coordinator question by building directly
on ``apply_contribution_batch`` and a separate bounded retraction helper.
This module is a read of a committed log. It admits nothing, appends
nothing, and adds no coordinator layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from packages.kernel.currency import CurrencyView, compute_currency
from packages.kernel.facts import Fact, fact_id_for, facts_of
from packages.kernel.findings import FindingState, project
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.nominee_allocation_recording import (
    ALLOCATION_FACT_TYPE_ID,
    RECIPIENT_ENTITY_KIND,
)
from packages.tax.report_statement_identity import REPORT_FACT_TYPE


class NomineeAllocationRecoveryError(ValueError):
    """Recovery cannot be completed from the committed log."""


class NomineeAllocationInvariantError(NomineeAllocationRecoveryError):
    """A kernel invariant this reader refuses to paper over.

    The required case: more than one current finding for one box-1 fact
    identity. This reader does not pick one.
    """


@dataclass(frozen=True)
class CurrentNomineeAllocation:
    """One currently-standing allocation recovered from the committed log.

    ``report_fact_id`` is the deterministic box-1 fact id the allocation's
    identity components resolve to; it is always present, including when no
    current box-1 finding stands. ``current_report_finding_id`` is the
    current box-1 finding for that fact, or ``None`` when none stands.
    This record carries no report value: a missing current finding is not
    filled from history and is not reported as a successful current-value
    join.
    """

    fact_id: str
    payer_id: str
    statement_id: str
    tax_year: str
    recipient_id: str
    recipient_display_label: str
    amount: Any
    current_finding_id: str
    assertion_act_id: str
    assertion_actor: str
    assertion_at: str
    contribution_id: str | None
    evidence_ids: tuple[str, ...]
    report_fact_id: str
    current_report_finding_id: str | None


@dataclass(frozen=True)
class RetractedNomineeAllocation:
    """One allocation finding whose current support was ended.

    Recovers what was said, who said it, and who later ended current
    support. It does not record that the original asserting actor recanted,
    that the allocation no longer exists in the world, or that the taxpayer
    owns the amount. Report-join cardinality matches current records:
    ``report_fact_id`` is always present; ``current_report_finding_id`` may
    be absent; more than one current box-1 finding is refused, not picked.
    """

    fact_id: str
    payer_id: str
    statement_id: str
    tax_year: str
    recipient_id: str
    recipient_display_label: str
    amount: Any
    finding_id: str
    assertion_act_id: str
    assertion_actor: str
    assertion_at: str
    contribution_id: str | None
    evidence_ids: tuple[str, ...]
    retraction_act_id: str
    retraction_actor: str
    retraction_at: str
    report_fact_id: str
    current_report_finding_id: str | None


@dataclass(frozen=True)
class NomineeAllocationRecoveryView:
    """Discardable recovery of nominee-allocation records and provenance.

    Rebuilding from the same committed acts must produce the same records.
    This is not an authority source and not a second definition of current
    standing.
    """

    current: tuple[CurrentNomineeAllocation, ...]
    retracted: tuple[RetractedNomineeAllocation, ...]


def unique_current_finding_id(
    fact_id: str,
    state: FindingState,
    currency: CurrencyView,
) -> str | None:
    """The unique current finding for ``fact_id``, or ``None`` if none stands.

    Standing comes from ``currency`` — a ``compute_currency`` view of
    ``state``, never an independently recomputed set. Zero current findings
    is a legitimate absence (an allocation may stand while no current box-1
    finding does). More than one is an invariant failure: this function
    refuses rather than picking one.
    """
    matching = sorted(
        finding_id
        for finding_id in currency.current_finding_ids
        if state.findings.get(finding_id, {}).get("fact_id") == fact_id
    )
    if len(matching) > 1:
        raise NomineeAllocationInvariantError(
            f"more than one current finding for fact {fact_id}: "
            f"{matching}; refusing rather than picking one"
        )
    if not matching:
        return None
    return matching[0]


def report_fact_id_for_allocation(fact: Fact) -> str:
    """The deterministic box-1 fact id the allocation's identity resolves to.

    Always defined from the allocation's payer, statement, and tax-year
    keys. Does not require a current box-1 finding, and does not read any
    finding value.
    """
    keys = dict(fact.keys)
    return fact_id_for(
        REPORT_FACT_TYPE,
        (
            ("payer", keys["payer"]),
            ("statement", keys["statement"]),
            ("tax-year", keys["tax-year"]),
        ),
    )


def recover_nominee_allocations(
    acts: Sequence[Mapping[str, Any]],
    registry: SchemaRegistry,
) -> NomineeAllocationRecoveryView:
    """Rebuild current allocations, attribution, and report join from the log.

    ``acts`` is the committed act sequence (``ActLog.read().acts``). This
    function projects, consults ``compute_currency`` once, and indexes the
    original acts. It does not append, admit, or consult a caller-supplied
    in-memory fold as standing.
    """
    committed = tuple(dict(act) for act in acts)
    state = project(committed, registry)
    currency = compute_currency(state)
    return _recover_from_projection(committed, state, currency)


def _recover_from_projection(
    acts: tuple[dict[str, Any], ...],
    state: FindingState,
    currency: CurrencyView,
) -> NomineeAllocationRecoveryView:
    lattice = facts_of(state.fact_state)
    acts_by_id = {act["act_id"]: act for act in acts}
    assertion_by_finding_id = _index_assertion_acts(acts)

    current_records: list[CurrentNomineeAllocation] = []
    for finding_id in sorted(currency.current_finding_ids):
        finding = state.findings.get(finding_id)
        if finding is None:
            raise NomineeAllocationInvariantError(
                f"currency names current finding {finding_id} that is absent "
                "from the projected state"
            )
        fact_id = finding["fact_id"]
        if _fact_type_id(fact_id) != ALLOCATION_FACT_TYPE_ID:
            continue
        fact = lattice.get(fact_id)
        if fact is None:
            raise NomineeAllocationInvariantError(
                f"current allocation finding {finding_id} answers fact "
                f"{fact_id}, which is absent from the current lattice"
            )
        assertion_act = assertion_by_finding_id.get(finding_id)
        if assertion_act is None:
            raise NomineeAllocationInvariantError(
                f"current allocation finding {finding_id} has no assertion act "
                "in the committed log"
            )
        identity = _allocation_identity(state, fact, currency)
        current_records.append(
            CurrentNomineeAllocation(
                fact_id=fact_id,
                payer_id=identity["payer_id"],
                statement_id=identity["statement_id"],
                tax_year=identity["tax_year"],
                recipient_id=identity["recipient_id"],
                recipient_display_label=identity["recipient_display_label"],
                amount=finding["value"],
                current_finding_id=finding_id,
                assertion_act_id=assertion_act["act_id"],
                assertion_actor=assertion_act["actor"],
                assertion_at=assertion_act["at"],
                contribution_id=_contribution_id(finding),
                evidence_ids=_evidence_ids(finding),
                report_fact_id=identity["report_fact_id"],
                current_report_finding_id=identity["current_report_finding_id"],
            )
        )

    retracted_records: list[RetractedNomineeAllocation] = []
    for finding_id, reasons in currency.reasons.items():
        finding = state.findings.get(finding_id)
        if finding is None:
            continue
        if _fact_type_id(finding["fact_id"]) != ALLOCATION_FACT_TYPE_ID:
            continue
        retraction_bys = [reason.by for reason in reasons if reason.kind == "retraction"]
        if not retraction_bys:
            continue
        if len(set(retraction_bys)) > 1:
            raise NomineeAllocationInvariantError(
                f"allocation finding {finding_id} names more than one "
                f"retraction act {sorted(set(retraction_bys))}; refusing "
                "rather than picking one"
            )
        retraction_act_id = retraction_bys[0]
        retraction_act = acts_by_id.get(retraction_act_id)
        if retraction_act is None:
            raise NomineeAllocationInvariantError(
                f"retraction displacement of {finding_id} names act "
                f"{retraction_act_id}, which is absent from the committed log"
            )
        fact_id = finding["fact_id"]
        fact = lattice.get(fact_id)
        if fact is None:
            raise NomineeAllocationInvariantError(
                f"retracted allocation finding {finding_id} answers fact "
                f"{fact_id}, which is absent from the current lattice"
            )
        assertion_act = assertion_by_finding_id.get(finding_id)
        if assertion_act is None:
            raise NomineeAllocationInvariantError(
                f"retracted allocation finding {finding_id} has no assertion "
                "act in the committed log"
            )
        identity = _allocation_identity(state, fact, currency)
        retracted_records.append(
            RetractedNomineeAllocation(
                fact_id=fact_id,
                payer_id=identity["payer_id"],
                statement_id=identity["statement_id"],
                tax_year=identity["tax_year"],
                recipient_id=identity["recipient_id"],
                recipient_display_label=identity["recipient_display_label"],
                amount=finding["value"],
                finding_id=finding_id,
                assertion_act_id=assertion_act["act_id"],
                assertion_actor=assertion_act["actor"],
                assertion_at=assertion_act["at"],
                contribution_id=_contribution_id(finding),
                evidence_ids=_evidence_ids(finding),
                retraction_act_id=retraction_act_id,
                retraction_actor=retraction_act["actor"],
                retraction_at=retraction_act["at"],
                report_fact_id=identity["report_fact_id"],
                current_report_finding_id=identity["current_report_finding_id"],
            )
        )

    return NomineeAllocationRecoveryView(
        current=tuple(current_records),
        retracted=tuple(
            sorted(retracted_records, key=lambda record: record.finding_id)
        ),
    )


def _fact_type_id(fact_id: str) -> str:
    return fact_id.split("|", 1)[0]


def _contribution_id(finding: Mapping[str, Any]) -> str | None:
    value = finding.get("contribution_id")
    return value if isinstance(value, str) else None


def _evidence_ids(finding: Mapping[str, Any]) -> tuple[str, ...]:
    raw = finding.get("evidence_ids")
    if not isinstance(raw, list):
        return ()
    return tuple(item for item in raw if isinstance(item, str))


def _allocation_identity(
    state: FindingState,
    fact: Fact,
    currency: CurrencyView,
) -> dict[str, Any]:
    keys = dict(fact.keys)
    recipient_id = keys["recipient"]
    report_fact_id = report_fact_id_for_allocation(fact)
    return {
        "payer_id": keys["payer"],
        "statement_id": keys["statement"],
        "tax_year": keys["tax-year"],
        "recipient_id": recipient_id,
        "recipient_display_label": _recipient_display_label(state, recipient_id),
        "report_fact_id": report_fact_id,
        "current_report_finding_id": unique_current_finding_id(
            report_fact_id, state, currency
        ),
    }


def _index_assertion_acts(
    acts: tuple[dict[str, Any], ...],
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for act in acts:
        if act.get("kind") != "assertion":
            continue
        finding = act.get("payload", {}).get("finding")
        if not isinstance(finding, dict):
            continue
        finding_id = finding.get("id")
        if isinstance(finding_id, str):
            indexed[finding_id] = act
    return indexed


def _recipient_display_label(state: FindingState, recipient_id: str) -> str:
    lifecycle = state.fact_state.entities.get(recipient_id)
    if lifecycle is None:
        raise NomineeAllocationInvariantError(
            f"allocation recipient {recipient_id} is absent from the entity lattice"
        )
    entity = lifecycle.entity
    if entity.get("kind") != RECIPIENT_ENTITY_KIND:
        raise NomineeAllocationInvariantError(
            f"allocation recipient {recipient_id} is kind "
            f"{entity.get('kind')!r}, not {RECIPIENT_ENTITY_KIND!r}"
        )
    label = entity.get("label")
    if not isinstance(label, str) or not label:
        raise NomineeAllocationInvariantError(
            f"allocation recipient {recipient_id} has no display label"
        )
    return label
