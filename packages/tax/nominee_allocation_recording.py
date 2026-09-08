"""Nominee-Allocation Assertion Recording, Track 1: producer and lifecycle.

Milestone `docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md`.
Track 0's contract (`docs/prototypes/nominee-allocation-assertion-recording/`)
selected the identity, association, and lifecycle mechanism against the
committed kernel and the committed Form 1099-INT report identity, but built
nothing production: it folded acts directly in memory. This module builds
what Track 0 did not:

- the production content bundle wiring (``packages.tax.loader``);
- an ordinary-answer producer that admits through the real
  ``packages.kernel.contribution.apply_contribution_batch`` boundary;
- recipient identity: an application-minted opaque workspace id under a
  bounded role-specific entity kind, introduced through its own named helper
  -- never derived from the typed display name, and never re-introduced for
  an existing recipient;
- a separate bounded retraction helper (``apply_contribution_batch`` cannot
  carry a ``finding-retracted`` act -- its successor kinds are exactly
  ``{"assertion", "member-transition"}``);
- real ``ActLog`` persistence: this module's own responsibility, not the
  caller's, because Track 1 owns the production acceptance boundary.

**The proposition, without its speaker.** *The amount of interest reported on
this identified Form 1099-INT that is allocated to this named other person.*
The finding supplies the current answer with ``basis: "attested"``; the
enclosing assertion act supplies who stated it and when. A later tax rule --
not this fact -- decides any nominee-interest consequence. This module
publishes no rule and no derived symbol.

**Actor and event metadata are the caller's, always.** Both cited precedents
(``packages.tax.report_statement_identity``,
``packages.tax.obligation_acquisition_mapping``) hard-code ``"actor": "user"``.
They are a guide to contribution *shape* only. Every function here takes
``actor`` and ``at`` as required parameters and copies them, unchanged, into
every act it emits. Actor is opaque provenance: never authentication, never
permission, never part of the proposition's identity, and never manufactured,
defaulted, or inferred by this module.

**No general circumstance router.** The one discriminant this module accepts
is the closed ``circumstance`` field on the ordinary answer set, required to
equal ``"nominee-allocation"``. Any other shape -- an accrued-interest
answer, an erroneous-report answer, or anything else -- fails
``validate_nominee_allocation_answers`` before any act is built. This module
does not know, and does not claim to know, where such an answer should
instead go.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Mapping

import jsonschema

from packages.kernel import facts, findings
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.findings import FindingState
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.report_statement_identity import (
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)

# Production identity -- selected by Track 0, restated here as real content,
# not the probe's demo namespace (`demo.nominee-allocation.amount`).
ALLOCATION_FACT_TYPE_ID = "tax.us.nominee-allocation.amount"

# A bounded, role-specific entity kind for an interest-allocation recipient --
# not a general natural-person model. Follows this corpus's own sibling
# convention (`tax.us.interest-payer`, `tax.us.interest-obligation`).
RECIPIENT_ENTITY_KIND = "tax.us.interest-allocation-recipient"

# The one discriminant this producer accepts. Not a general circumstance
# router: every other value, or its absence, fails validation before any act
# is built.
ALLOCATION_CIRCUMSTANCE = "nominee-allocation"

# Declared evidence.content.mode values this producer reads from the
# current evidence.v1 citizen. Product-specific: not a general evidence
# ontology and not a new schema. An allocation assertion requires a current
# ordinary-language-entry citizen whose submitted answers correspond to the
# finding being mapped. A Form 1099-INT copy is evidence of what the payer
# reported; it is not evidence that the user allocated an amount to another
# recipient.
DOCUMENT_REPORT_EVIDENCE_MODE = "document-report-entry"
ORDINARY_LANGUAGE_EVIDENCE_MODE = "ordinary-language-entry"

# Fields of the submitted ordinary-language answer that determine the
# canonical finding. recipient_display_label does not: it is a
# non-authoritative label on a new recipient entity, not part of the
# proposition.
_ALLOCATION_CORRESPONDENCE_FIELDS: tuple[str, ...] = (
    "circumstance",
    "payer_name",
    "statement_reference",
    "tax_year",
    "recipient_id",
    "amount",
)


class NomineeAllocationInputError(ValueError):
    """The allocation answer set, recipient, or retraction target is refused."""


# ---------------------------------------------------------------------------
# The structured ordinary-language input projection (closed).
# ---------------------------------------------------------------------------

NOMINEE_ALLOCATION_ANSWERS_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        # The discriminant. Any other value -- or a genuinely different
        # answer shape entirely (e.g. an accrued-interest or
        # erroneous-report answer set) -- is refused by this const check or
        # by `additionalProperties: false` below, never captured here.
        "circumstance": {"const": ALLOCATION_CIRCUMSTANCE},
        # "Who paid or reported this interest?" -- the identified Form
        # 1099-INT's own payer, as it appears on the person's own report.
        "payer_name": {"type": "string", "minLength": 1, "pattern": r"\S"},
        # "Which statement or account reference is this, exactly as it
        # appears on that report?"
        "statement_reference": {"type": "string", "minLength": 1, "pattern": r"\S"},
        # The report's own tax year (a literal identity component, shared
        # with the box-1 report; never a separately-asked classification).
        "tax_year": {"type": "integer"},
        # The application-minted opaque recipient id -- never derived from
        # typed text. Existing recipient: this names a current entity of
        # `RECIPIENT_ENTITY_KIND`. New recipient: paired with
        # `recipient_display_label` below.
        "recipient_id": {"type": "string", "minLength": 1},
        # Present only when `recipient_id` names a genuinely new recipient.
        # Non-authoritative: a display label only, never a verified
        # identity. Absent (or null) for an existing recipient -- supplying
        # one there is refused, not silently ignored, because entity labels
        # are immutable and display-name correction is deferred.
        "recipient_display_label": {"type": ["string", "null"], "minLength": 1},
        # The stated allocation amount. Strictly positive -- the fact
        # type's own `value_schema` enforces this identically; refusing a
        # non-positive amount here as well means a zero answer never
        # reaches contribution admission at all (A0).
        "amount": {"type": "number", "exclusiveMinimum": 0},
    },
    "required": [
        "circumstance",
        "payer_name",
        "statement_reference",
        "tax_year",
        "recipient_id",
        "amount",
    ],
    "additionalProperties": False,
}

# The plain-language question surface, named so a reviewer (or a test) can
# confirm no question asks for a tax classification, election, or nominee
# characterization.
NOMINEE_ALLOCATION_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("payer_name", "Who paid or reported this interest?"),
    (
        "statement_reference",
        "Which statement or account reference is this, exactly as it "
        "appears on that report?",
    ),
    ("tax_year", "What tax year does that report cover?"),
    ("recipient_id", "Which recipient record does this allocation concern?"),
    (
        "recipient_display_label",
        "What name should this new recipient record show? (only asked "
        "when the recipient is new)",
    ),
    ("amount", "How much of that reported interest belongs to them?"),
)


def _reject_non_finite_amount(answers: Mapping[str, Any]) -> None:
    """Reject ``inf``/``-inf``/``nan`` for ``amount``.

    JSON Schema's ``exclusiveMinimum`` does not by itself exclude IEEE-754
    non-finite values (see the identical guard in
    ``obligation_acquisition_mapping._reject_non_finite_numbers``). Checked
    before any finding is built, so a non-finite amount never reaches
    contribution admission.
    """
    value = answers.get("amount")
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)) and not math.isfinite(value):
        raise NomineeAllocationInputError(
            f"nominee-allocation answer set is invalid: 'amount' must be a "
            f"finite number, not {value!r} (path: ['amount'])"
        )


_VALIDATOR = jsonschema.Draft202012Validator(NOMINEE_ALLOCATION_ANSWERS_SCHEMA)


def validate_nominee_allocation_answers(answers: Mapping[str, Any]) -> None:
    """Fail closed on anything that is not a well-formed allocation answer.

    This is the whole of this module's "circumstance routing": an answer
    set naming a different circumstance (or no circumstance at all), or
    carrying any field this shape does not declare, is rejected here,
    before it can reach a canonical fact -- never routed anywhere, because
    no general router exists in this module. An accrued-interest answer
    (A9) or an erroneous-report answer (A10) both fail here: neither can
    satisfy this schema's ``circumstance`` const plus its closed field set.
    """
    _reject_non_finite_amount(answers)
    errors = sorted(_VALIDATOR.iter_errors(dict(answers)), key=lambda e: e.path)
    if errors:
        first = errors[0]
        raise NomineeAllocationInputError(
            f"nominee-allocation answer set is invalid: {first.message} "
            f"(path: {list(first.path)})"
        )


def _require_ordinary_language_allocation_evidence(
    state: FindingState, evidence_id: str, answers: Mapping[str, Any]
) -> None:
    """Require current ordinary-language evidence that matches this call.

    Positive product-specific requirement, not a general evidence schema
    or ontology. Before any act is appended, the cited evidence citizen
    must be current, its ``content.mode`` must be exactly
    ``ordinary-language-entry``, its ``content.answers`` must be a valid
    ordinary-language nominee-allocation submission, and those answers
    must correspond to the answers this call is mapping on every field
    that determines the finding. Missing, malformed, document-report, and
    unrelated modes are all refused. An arbitrary evidence citizen must
    not license a different normalized finding.

    The evidence retains the submitted representation; the finding is the
    canonical proposition derived from it. The two are not collapsed.
    """
    lifecycle = state.evidence.get(evidence_id)
    if lifecycle is None or lifecycle.status != "current":
        raise NomineeAllocationInputError(
            f"allocation evidence {evidence_id!r} is not a current evidence citizen"
        )
    content = lifecycle.evidence.get("content")
    if not isinstance(content, dict):
        raise NomineeAllocationInputError(
            f"allocation evidence {evidence_id!r} has malformed content; "
            "a nominee-allocation assertion requires a current "
            "ordinary-language-entry submission"
        )
    mode = content.get("mode")
    if mode != ORDINARY_LANGUAGE_EVIDENCE_MODE:
        extra = ""
        if mode == DOCUMENT_REPORT_EVIDENCE_MODE:
            extra = (
                "; a Form 1099-INT copy is evidence of what the payer "
                "reported, not that the user allocated an amount to another "
                "recipient"
            )
        raise NomineeAllocationInputError(
            f"allocation assertion requires ordinary-language-entry evidence "
            f"{evidence_id!r}{extra} (mode {mode!r})"
        )
    recorded = content.get("answers")
    if not isinstance(recorded, dict):
        raise NomineeAllocationInputError(
            f"allocation evidence {evidence_id!r} is not a valid "
            "ordinary-language nominee-allocation submission"
        )
    try:
        validate_nominee_allocation_answers(recorded)
    except NomineeAllocationInputError as exc:
        raise NomineeAllocationInputError(
            f"allocation evidence {evidence_id!r} is not a valid "
            f"ordinary-language nominee-allocation submission: {exc}"
        ) from exc
    mismatched = [
        field
        for field in _ALLOCATION_CORRESPONDENCE_FIELDS
        if recorded.get(field) != answers.get(field)
    ]
    if mismatched:
        raise NomineeAllocationInputError(
            f"allocation evidence {evidence_id!r} does not correspond to the "
            f"answers being mapped (differing fields: {mismatched})"
        )


# ---------------------------------------------------------------------------
# Identity.
# ---------------------------------------------------------------------------


def derive_nominee_allocation_fact_id(
    *,
    payer_name: str,
    statement_reference: str,
    tax_year: int,
    recipient_id: str,
) -> str:
    """The allocation fact id, sharing the box-1 report's own identity.

    ``payer`` and ``statement`` are derived by the committed document-side
    convention in ``packages.tax.report_statement_identity`` -- the same
    real derivation the box-1 report itself uses, not a parallel invented
    identity. ``recipient`` is the caller's application-minted opaque id,
    never derived from typed text.
    """
    return facts.fact_id_for(
        ALLOCATION_FACT_TYPE_ID,
        (
            ("payer", derive_reported_payer_entity_id(payer_name)),
            (
                "statement",
                derive_reported_statement_entity_id(
                    payer_name=payer_name, statement_reference=statement_reference
                ),
            ),
            ("tax-year", str(tax_year)),
            ("recipient", recipient_id),
        ),
    )


# ---------------------------------------------------------------------------
# Recipient introduction -- a named helper, deliberately outside the
# contribution batch (`apply_contribution_batch`'s successor kinds are
# exactly `{"assertion", "member-transition"}`; entity introduction is not
# one of them and must not be implied to be).
# ---------------------------------------------------------------------------


def build_recipient_entity_act(
    *,
    recipient_id: str,
    display_label: str,
    actor: str,
    at: str,
    act_id: str,
    committed_against: int,
) -> dict[str, Any]:
    """The ``entity-introduced`` act for a genuinely new allocation recipient.

    The typed display label is recorded as a non-authoritative label only.
    Entity labels are immutable (``packages.kernel.facts.py:122``); no path
    here or anywhere edits one in place, and display-name correction is
    deliberately deferred.
    """
    return {
        "schema": "act.v1",
        "act_id": act_id,
        "kind": "entity-introduced",
        "actor": actor,
        "at": at,
        "committed_against": committed_against,
        "payload": {
            "entity": {
                "schema": "entity.v1",
                "id": recipient_id,
                "kind": RECIPIENT_ENTITY_KIND,
                "label": display_label,
            }
        },
    }


def _current_recipient_entity(
    state: FindingState, recipient_id: str
) -> facts.EntityLifecycle | None:
    lifecycle = state.fact_state.entities.get(recipient_id)
    if lifecycle is None:
        return None
    if lifecycle.status != "current":
        return None
    if lifecycle.entity.get("kind") != RECIPIENT_ENTITY_KIND:
        return None
    return lifecycle


# ---------------------------------------------------------------------------
# Contribution batch (assertion / correction). Mirrors
# ``obligation_acquisition_mapping.build_ordinary_acquisition_contribution``
# in shape only -- attribution is never hard-coded here.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NomineeAllocationContribution:
    """The synthetic acts one allocation contribution batch produces."""

    contribution_act: dict[str, Any]
    assertion_act: dict[str, Any]
    finding: dict[str, Any]


def build_nominee_allocation_contribution(
    answers: Mapping[str, Any],
    *,
    actor: str,
    at: str,
    contribution_act_id: str,
    assertion_act_id: str,
    contribution_id: str,
    evidence_id: str,
    finding_id: str,
    committed_against: int,
    fact_id: str | None = None,
) -> NomineeAllocationContribution:
    """Build the contribution + assertion acts for one allocation answer set.

    Does not decide admissibility -- ``packages.kernel.contribution.apply_contribution_batch``
    is the real boundary that does. ``actor`` and ``at`` are the caller's,
    copied unchanged into both acts; this function never manufactures them.
    """
    validate_nominee_allocation_answers(answers)
    resolved_fact_id = fact_id or derive_nominee_allocation_fact_id(
        payer_name=answers["payer_name"],
        statement_reference=answers["statement_reference"],
        tax_year=answers["tax_year"],
        recipient_id=answers["recipient_id"],
    )
    finding = {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": resolved_fact_id,
        # basis: "attested" -- what the actor stated about this
        # circumstance, not what a document reported (the committed
        # precedent at obligation_acquisition_mapping.py:599-601).
        "value": answers["amount"],
        "basis": "attested",
        "evidence_ids": [evidence_id],
        "contribution_id": contribution_id,
    }
    contribution_act = {
        "schema": "act.v1",
        "act_id": contribution_act_id,
        "kind": "contribution",
        "actor": actor,
        "at": at,
        "committed_against": committed_against,
        "payload": {
            "contribution": {
                "schema": "contribution.v1",
                "id": contribution_id,
                "evidence_id": evidence_id,
                "content": {
                    # Mode is recorded only after the cited evidence citizen
                    # has been verified as ordinary-language-entry. This
                    # producer does not invent whether that interaction was
                    # synthetic; synthetic fixtures identify themselves on
                    # their own evidence citizens.
                    "mode": ORDINARY_LANGUAGE_EVIDENCE_MODE,
                },
            }
        },
    }
    assertion_act = {
        "schema": "act.v1",
        "act_id": assertion_act_id,
        "kind": "assertion",
        "actor": actor,
        "at": at,
        "committed_against": committed_against + 1,
        "payload": {"finding": finding},
    }
    return NomineeAllocationContribution(
        contribution_act=contribution_act, assertion_act=assertion_act, finding=finding
    )


# ---------------------------------------------------------------------------
# Persistence: this operation's own responsibility (Track 1 owns the
# production acceptance boundary). Rebuilds current state from the real
# ``ActLog``, semantically pre-applies every act it is about to write,
# appends only after every pre-check has passed, and returns only once the
# durable log can be reprojected to the accepted state.
#
# There is no atomic multi-act append: ``ActLog.append`` commits exactly one
# act per call against an expected revision. If this call is interrupted
# after the semantic pre-check but partway through the ordered appends
# below, a *prefix* of {entity, contribution, assertion} may persist; the
# log's own guarantee is that interruption can only lose an act, never
# corrupt history -- it is not a guarantee that this multi-act sequence
# completes as a unit. There is no transaction substrate and no rollback.
# Repeating ``assert_nominee_allocation`` is not idempotent and is not a
# resume: an existing prefix (the recipient already introduced, or the
# contribution already recorded) can make the retry fail. **Hard gate:** no
# user-facing production caller may rely on this operation until resumable
# or idempotent recovery of a persisted prefix is closed.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NomineeAllocationAssertionResult:
    """The durable outcome of one ``assert_nominee_allocation`` call."""

    state: FindingState
    entity_act: dict[str, Any] | None
    contribution_act: dict[str, Any]
    assertion_act: dict[str, Any]
    finding: dict[str, Any]
    revision: int


def assert_nominee_allocation(
    log: ActLog,
    registry: SchemaRegistry,
    *,
    answers: Mapping[str, Any],
    actor: str,
    at: str,
    evidence_id: str,
    contribution_id: str,
    finding_id: str,
    record_id: str,
    contribution_act_id: str,
    assertion_act_id: str,
    entity_act_id: str | None = None,
) -> NomineeAllocationAssertionResult:
    """Assert (or correct) one nominee-allocation answer, durably.

    ``answers`` must validate under ``NOMINEE_ALLOCATION_ANSWERS_SCHEMA``; a
    non-allocation answer set (A9, A10) or a non-positive amount (A0) is
    refused here, before any act is built or the log is touched.

    Recipient handling, per Track 1's deliverable 0:

    - **existing recipient** -- ``answers["recipient_id"]`` must name a
      *current* entity of ``RECIPIENT_ENTITY_KIND``. No ``entity-introduced``
      act is built or appended (re-introduction is refused by the kernel
      itself, ``packages/kernel/facts.py:122``, and this function never
      attempts it). Supplying ``recipient_display_label`` here is refused,
      not silently ignored -- entity labels are immutable, and this is not
      a display-name correction path;
    - **new recipient** -- ``answers["recipient_id"]`` must name no current
      entity at all, and ``recipient_display_label`` must be supplied. A
      named helper (``build_recipient_entity_act``) constructs the
      ``entity-introduced`` act and it is semantically admitted *before*
      the contribution batch is even built.

    Every act this call may write is pre-applied against the rebuilt
    in-memory state (``findings.apply_act`` / ``apply_contribution_batch``)
    before this call appends anything to ``log`` -- an inadmissible
    sequence never reaches the durable log. Only once every pre-check has
    passed are the acts appended, in order, each at its exact successive
    revision.
    """
    validate_nominee_allocation_answers(answers)

    contents = log.read()
    state = findings.project(contents.acts, registry)
    revision = contents.revision
    _require_ordinary_language_allocation_evidence(state, evidence_id, answers)

    recipient_id = answers["recipient_id"]
    display_label = answers.get("recipient_display_label")
    existing_lifecycle = state.fact_state.entities.get(recipient_id)
    current_recipient = _current_recipient_entity(state, recipient_id)

    entity_act: dict[str, Any] | None = None
    if current_recipient is not None:
        if display_label is not None:
            raise NomineeAllocationInputError(
                f"recipient {recipient_id!r} already exists; display-name "
                "correction is deferred and is not performed by this "
                "operation (entity labels are immutable)"
            )
    else:
        if existing_lifecycle is not None:
            # The id names something, but not a current recipient entity of
            # the selected kind -- refuse rather than reintroduce it under
            # a name it does not currently hold.
            raise NomineeAllocationInputError(
                f"recipient id {recipient_id!r} does not name a current "
                f"entity of kind {RECIPIENT_ENTITY_KIND!r}"
            )
        if not display_label:
            raise NomineeAllocationInputError(
                f"recipient {recipient_id!r} is not a current entity; a new "
                "recipient requires 'recipient_display_label'"
            )
        entity_act = build_recipient_entity_act(
            recipient_id=recipient_id,
            display_label=display_label,
            actor=actor,
            at=at,
            act_id=entity_act_id or f"{assertion_act_id}.recipient",
            committed_against=revision,
        )
        # Pre-apply semantically before this call writes anything durable.
        state = findings.apply_act(state, entity_act, registry)

    batch_committed_against = revision + (1 if entity_act is not None else 0)
    built = build_nominee_allocation_contribution(
        answers,
        actor=actor,
        at=at,
        contribution_act_id=contribution_act_id,
        assertion_act_id=assertion_act_id,
        contribution_id=contribution_id,
        evidence_id=evidence_id,
        finding_id=finding_id,
        committed_against=batch_committed_against,
    )
    # Pre-apply the whole contribution batch semantically -- this raises
    # (ContributionError) before anything is appended if it is inadmissible.
    apply_contribution_batch(
        state,
        contribution_act=built.contribution_act,
        successor_acts=[built.assertion_act],
        registry=registry,
        record_id=record_id,
        workspace_revision=batch_committed_against,
    )

    # Every pre-check passed. Append, in order, each at its exact
    # successive revision. `ActLog.append` commits exactly one act per
    # call -- there is no atomic multi-act append (see module docstring).
    if entity_act is not None:
        revision = log.append(entity_act, expected_revision=revision)
    revision = log.append(built.contribution_act, expected_revision=revision)
    revision = log.append(built.assertion_act, expected_revision=revision)

    # Return only once the durable log reprojects to the accepted state --
    # never the in-memory fold above, which is not evidence of persistence.
    contents_after = log.read()
    state_after = findings.project(contents_after.acts, registry)
    return NomineeAllocationAssertionResult(
        state=state_after,
        entity_act=entity_act,
        contribution_act=built.contribution_act,
        assertion_act=built.assertion_act,
        finding=built.finding,
        revision=revision,
    )


# ---------------------------------------------------------------------------
# Retraction -- a separate, bounded production operation.
# `apply_contribution_batch` cannot carry a retraction: its successor kinds
# are exactly {"assertion", "member-transition"}
# (`packages/kernel/contribution.py:21`), so `finding-retracted` is refused
# as a carrier. This helper is product-specific: it verifies the named
# current finding answers *this* fact type before doing anything, so it
# never becomes an unrestricted way to retract arbitrary workspace facts.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NomineeAllocationRetractionResult:
    """The durable outcome of one ``retract_nominee_allocation`` call."""

    state: FindingState
    retraction_act: dict[str, Any]
    revision: int


def retract_nominee_allocation(
    log: ActLog,
    registry: SchemaRegistry,
    *,
    finding_id: str,
    actor: str,
    at: str,
    act_id: str,
) -> NomineeAllocationRetractionResult:
    """End the current support of one identified nominee-allocation finding.

    Ends the workspace's current support for the named finding; it does not
    write a replacement value and does not assert the opposite proposition.
    The original assertion, its actor, and its time stay historical; this
    retraction carries its own actor and time. **Nothing this helper emits
    or documents claims or implies that the original actor recanted** --
    admission never consults actor identity (ADR-0073 Decision 3), so this
    records provenance, not permission, and not personal withdrawal.

    Refused, before anything is built, if the named finding does not
    currently exist or does not answer ``ALLOCATION_FACT_TYPE_ID`` -- this
    helper is not a general-purpose retraction surface. The fact's own
    lifecycle rules (currency, supersession policy, family membership,
    declared admission invariants) are enforced by the kernel's own
    ``finding-retracted`` applier when this call semantically pre-applies
    the act below; this helper adds only the fact-type guard.
    """
    contents = log.read()
    state = findings.project(contents.acts, registry)
    revision = contents.revision

    finding = state.findings.get(finding_id)
    if finding is None:
        raise NomineeAllocationInputError(
            f"cannot retract unknown finding: {finding_id}"
        )
    lattice = facts.facts_of(state.fact_state, include_displaced=True)
    fact = lattice.get(finding["fact_id"])
    fact_type_id = fact.fact_type_id if fact is not None else None
    if fact_type_id != ALLOCATION_FACT_TYPE_ID:
        raise NomineeAllocationInputError(
            f"finding {finding_id} answers fact type {fact_type_id!r}, not "
            f"{ALLOCATION_FACT_TYPE_ID!r}; this helper retracts "
            "nominee-allocation findings only"
        )

    retraction_act = {
        "schema": "act.v1",
        "act_id": act_id,
        "kind": "finding-retracted",
        "actor": actor,
        "at": at,
        "committed_against": revision,
        "payload": {"finding_id": finding_id},
    }
    # Semantically pre-apply before persistence -- an inadmissible
    # retraction (not current, locked policy, family member, admission
    # invariant) never reaches the log.
    findings.apply_act(state, retraction_act, registry)

    revision = log.append(retraction_act, expected_revision=revision)

    contents_after = log.read()
    state_after = findings.project(contents_after.acts, registry)
    return NomineeAllocationRetractionResult(
        state=state_after, retraction_act=retraction_act, revision=revision
    )
