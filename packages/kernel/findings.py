"""Evidence and asserted findings.

Track 4 keeps Article 1's boundary explicit: evidence is source-flavor
provenance for findings, never a parent or identity source. Assertion
acts create immutable finding citizens; evidence replacement changes a
derived evidentiary-standing view without rewriting findings.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from decimal import Decimal, InvalidOperation
from typing import Any

import jsonschema

from packages.kernel import facts, horizons
from packages.kernel.schema_registry import SchemaRegistry

EVIDENCE_SCHEMA = "evidence.v1"
FINDING_SCHEMA = "finding.v1"
FINDING_SCHEMA_V2 = "finding.v2"
CONTRIBUTION_SCHEMA = "contribution.v1"
ADMITTED_FINDING_SCHEMAS = frozenset({FINDING_SCHEMA, FINDING_SCHEMA_V2})


class FindingModelError(Exception):
    """An evidence or assertion act is semantically inadmissible."""


# Named refusal code for a migration artifact declaring
# ``resolution_policy.policy == "resolved-required"`` (ADR-0072 Decision 4):
# adoption refuses while any predecessor fact this migration would retire --
# live or withdrawn -- last recorded a nonzero value. The one currently
# accepted way to resolve a nonzero claim is a same-identity correction to a
# genuinely zero value (the predecessor fact type's own declared
# ``supersession.policy: "free"``); a withdrawal (however it is annotated)
# never resolves a nonzero claim on its own -- it only matters for a claim
# whose last recorded value was already zero. Generic kernel mechanism,
# opt-in per artifact -- no fact-type id is hardcoded here.
MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM = "MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM"


@dataclass(frozen=True)
class EvidenceLifecycle:
    """Derived lifecycle for one evidence citizen."""

    evidence: dict[str, Any]
    status: str
    successor_id: str | None = None


@dataclass(frozen=True)
class EvidenceReferenceStanding:
    """How one finding's evidence reference stands in current state."""

    evidence_id: str
    status: str
    successor_id: str | None = None


@dataclass(frozen=True)
class FindingStanding:
    """A finding plus derived standing of the evidence it cited."""

    finding: dict[str, Any]
    evidence: tuple[EvidenceReferenceStanding, ...]


@dataclass(frozen=True)
class FindingState:
    """Fold state for evidence, asserted findings, and horizon chains."""

    fact_state: facts.KernelState = field(default_factory=facts.initial_state)
    evidence: dict[str, EvidenceLifecycle] = field(default_factory=dict)
    findings: dict[str, dict[str, Any]] = field(default_factory=dict)
    # Contribution citizens (ADR-0032): provenance anchors, never standing edges.
    contributions: dict[str, dict[str, Any]] = field(default_factory=dict)
    horizon_state: horizons.HorizonState = field(default_factory=horizons.initial_state)
    # Facts whose member standing was withdrawn by a member-transition
    # remove/reclassify. Withdrawal is a displacement *root* over the
    # fact's findings (like correction), never a new edge kind.
    withdrawn_fact_ids: frozenset[str] = frozenset()
    # Withdrawn fact_id -> the fact_id the removing member-transition named
    # (via act-member-transition.v3's optional ``corresponds_to_fact_id``)
    # as whatever took over its computational role. Recorded for historical
    # completeness whenever a v3-shaped removal names one -- v3 remains
    # accepted, immutable published history -- but no migration-adoption
    # check consults this map for authority: a real, current correspondence
    # is not sufficient to establish that a nonzero claim's role actually
    # transferred, so a nonzero legacy claim always blocks migration
    # regardless of what this map holds.
    withdrawal_correspondence: dict[str, str] = field(default_factory=dict)
    # Presented successor claims produced by a migration-adoption act.
    # Each is an input to a later user assertion; nothing here writes a
    # successor finding (ADR-0025 decision 7, finding half only).
    presented_successor_claims: tuple[dict[str, Any], ...] = ()


def initial_state() -> FindingState:
    return FindingState()


def current_evidence_ids(state: FindingState) -> set[str]:
    """The single source of evidence currency; currency views reuse it."""
    return {
        evidence_id
        for evidence_id, lifecycle in state.evidence.items()
        if lifecycle.status == "current"
    }


def _current_evidence(state: FindingState) -> dict[str, EvidenceLifecycle]:
    return {
        evidence_id: state.evidence[evidence_id]
        for evidence_id in current_evidence_ids(state)
    }


def _validate_evidence(evidence: dict[str, Any], registry: SchemaRegistry) -> None:
    registry.validate(EVIDENCE_SCHEMA, evidence)


def apply_evidence_submitted(
    state: FindingState, payload: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    evidence = payload["evidence"]
    _validate_evidence(evidence, registry)
    evidence_id = evidence["id"]
    if evidence_id in state.evidence:
        raise FindingModelError(f"evidence already exists: {evidence_id}")
    lifecycles = dict(state.evidence)
    lifecycles[evidence_id] = EvidenceLifecycle(evidence=evidence, status="current")
    return replace(state, evidence=lifecycles)


def apply_evidence_replaced(
    state: FindingState, payload: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    evidence_id = payload["evidence_id"]
    lifecycles = dict(state.evidence)
    existing = lifecycles.get(evidence_id)
    if existing is None:
        raise FindingModelError(f"unknown evidence: {evidence_id}")
    if existing.status != "current":
        raise FindingModelError(f"evidence is not current: {evidence_id}")

    replacement = payload.get("replacement")
    successor_id: str | None = None
    if replacement is not None:
        _validate_evidence(replacement, registry)
        successor_id = replacement["id"]
        if successor_id == evidence_id:
            raise FindingModelError("replacement evidence must have a new id")
        if successor_id in lifecycles:
            raise FindingModelError(f"evidence already exists: {successor_id}")
        lifecycles[successor_id] = EvidenceLifecycle(
            evidence=replacement, status="current"
        )

    lifecycles[evidence_id] = EvidenceLifecycle(
        evidence=existing.evidence,
        status="replaced" if successor_id is not None else "withdrawn",
        successor_id=successor_id,
    )
    return replace(state, evidence=lifecycles)


def _current_value_for_fact(state: FindingState, fact_id: str) -> Any:
    """The current value answering one fact, or a sentinel if none is current.

    Mirrors ``currency.py``'s correction rule (the last-inserted finding for
    a fact id wins) without pulling in the full displacement-closure
    machinery; a withdrawn fact has no current value either.
    """
    if fact_id in state.withdrawn_fact_ids:
        return _NO_CURRENT_VALUE
    value: Any = _NO_CURRENT_VALUE
    for existing in state.findings.values():
        if existing["fact_id"] == fact_id:
            value = existing["value"]
    return value


_NO_CURRENT_VALUE = object()


def _enforce_closed_on_attestation(
    state: FindingState,
    finding: dict[str, Any],
    fact: facts.Fact,
    fact_type: dict[str, Any],
) -> None:
    """ADR-0041 Decision §4: reject correction once the named gate closure
    fact is currently attested ``true``; permit otherwise (false, absent,
    or the gate fact type carrying no current finding at all).

    The gate fact's identity is resolved by projecting the already-answered
    fact's own key bindings onto the gate fact type's declared identity-key
    names (the same scope-projection ADR-0016's family-subtotal/closure-claim
    pattern already performs) - reusing ``_current_value_for_fact``, the
    existing last-inserted-wins/withdrawal-aware current-value reader, so
    horizon succession (ADR-0017 decision 5) reopens correction exactly as
    it already reopens closure-backed derived results: a horizon successor
    projects a distinct gate fact id with no recorded finding of its own,
    which reads as absent (permitted) here without any new mechanism.

    ADR-0041 leaves the exact scope-matching algorithm "Not Decided" for
    cases where key names are not shared; this implements the narrowest
    case it does settle - the gate fact type's identity-key names must all
    be present, by name, among the already-answered fact's own keys. A gate
    fact type naming a key the gated fact type does not carry is a content
    configuration error, rejected explicitly rather than silently permitted.
    """
    gate = fact_type["supersession"]["gate"]
    gate_fact_type_id = gate["fact_type"]
    gate_fact_type = state.fact_state.fact_types.get(gate_fact_type_id)
    if gate_fact_type is None:
        raise FindingModelError(
            f"finding {finding['id']}: fact {fact.fact_id} is gated on "
            f"undeclared fact type {gate_fact_type_id!r}"
        )
    own_keys = dict(fact.keys)
    gate_keys: list[tuple[str, str]] = []
    for key in gate_fact_type["identity_keys"]:
        name = key["name"]
        if name not in own_keys:
            raise FindingModelError(
                f"finding {finding['id']}: cannot project fact {fact.fact_id} "
                f"onto gate fact type {gate_fact_type_id!r}: identity key "
                f"{name!r} is not among {fact.fact_type_id}'s own identity keys"
            )
        gate_keys.append((name, own_keys[name]))
    gate_fact_id = facts.fact_id_for(gate_fact_type_id, tuple(gate_keys))
    gate_value = _current_value_for_fact(state, gate_fact_id)
    if gate_value is True:
        raise FindingModelError(
            f"finding {finding['id']}: fact {fact.fact_id} is governed by "
            f"supersession policy 'closed-on-attestation'; gate "
            f"{gate_fact_id} is currently attested true, which does not "
            f"permit correction here"
        )


def _enforce_subset_invariants(
    state: FindingState, registry: SchemaRegistry, touched_fact_ids: tuple[str, ...]
) -> None:
    """Enforce every domain-declared subset invariant a touched fact reaches.

    A subset invariant pairs a subordinate fact type to a dominant one
    (``registry.subset_invariant_pairs``, e.g. ADR-0035 decision 4: 1099-DIV
    box 1b <= box 1a for the same statement). Both facts share every
    identity-key binding but the fact type id, so the fact id's key suffix
    (everything after the first ``|``) names "the same statement" without
    any domain knowledge here. Enforcement runs against the fully-updated
    successor state so it sees the touched act's own change plus every
    prior admission in the same fold - including same-batch ordering: a
    dominant fact admitted after its subordinate in one contribution batch
    is already recorded by the time the subordinate's check (or a later
    re-check triggered by the dominant admission) runs, because each act
    folds sequentially and this check runs on the resulting state, not a
    stale snapshot. A violating pair is never recorded: this function
    raises before the caller ever observes the successor state.
    """
    pairs = getattr(registry, "subset_invariant_pairs", None)
    if not pairs:
        return
    reverse_pairs = {dominant: subordinate for subordinate, dominant in pairs.items()}
    checked: set[tuple[str, str]] = set()
    for fact_id in touched_fact_ids:
        if "|" not in fact_id:
            continue
        fact_type_id, suffix = fact_id.split("|", 1)
        subordinate_type = fact_type_id if fact_type_id in pairs else reverse_pairs.get(fact_type_id)
        if subordinate_type is None:
            continue
        dominant_type = pairs[subordinate_type]
        key = (subordinate_type, suffix)
        if key in checked:
            continue
        checked.add(key)
        subordinate_id = f"{subordinate_type}|{suffix}"
        dominant_id = f"{dominant_type}|{suffix}"
        subordinate_value = _current_value_for_fact(state, subordinate_id)
        if subordinate_value is _NO_CURRENT_VALUE:
            continue
        dominant_value = _current_value_for_fact(state, dominant_id)
        if dominant_value is _NO_CURRENT_VALUE:
            raise FindingModelError(
                f"subset invariant violated: {subordinate_id} is current "
                f"({subordinate_value!r}) but {dominant_id} has no current value; "
                f"rejected, not recorded"
            )
        if subordinate_value > dominant_value:
            raise FindingModelError(
                f"subset invariant violated: current value of {subordinate_id} "
                f"({subordinate_value!r}) exceeds current value of {dominant_id} "
                f"({dominant_value!r}); rejected, not recorded"
            )



def _companion_list(pairs: dict[str, Any], subordinate_type: str) -> list[str]:
    """Normalize one subordinate's companion entry to a list of fact-type ids.

    Domain maps may declare a single companion string or a list of companions
    (box-7 requires both box-8 and same-statement box-1a). Empty entries are
    ignored.
    """
    raw = pairs.get(subordinate_type)
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, (list, tuple)):
        return [item for item in raw if isinstance(item, str) and item]
    return []


def _enforce_companion_presence(
    state: FindingState, registry: SchemaRegistry, touched_fact_ids: tuple[str, ...]
) -> None:
    """Enforce every domain-declared companion-presence pair a touched fact reaches.

    A companion-presence pair maps a subordinate member fact type to one or
    more companion fact types (``registry.companion_presence_pairs``). Both
    share every identity-key binding but the fact type id, so the fact id's
    key suffix names the same logical statement without domain knowledge
    here. A current subordinate without a current companion is rejected.
    Optional ``registry.companion_value_domains`` may restrict companion
    values (e.g. box-13 absence/zero); otherwise value domains are left to
    the companion fact type's ``value_schema``. Enforcement runs against the
    fully-updated successor state so same-batch ordering is visible, matching
    ``_enforce_subset_invariants``.
    """
    pairs = getattr(registry, "companion_presence_pairs", None)
    if not pairs:
        return
    value_domains = getattr(registry, "companion_value_domains", None) or {}
    reverse_pairs: dict[str, str] = {}
    for subordinate, companions in pairs.items():
        for companion in _companion_list(pairs, subordinate):
            # Last subordinate wins for reverse touch of a multi-used companion
            # type; enforcement still re-derives the full companion list from
            # the subordinate when the subordinate is current.
            reverse_pairs[companion] = subordinate
    checked: set[tuple[str, str, str]] = set()
    for fact_id in touched_fact_ids:
        if "|" not in fact_id:
            continue
        fact_type_id, suffix = fact_id.split("|", 1)
        subordinate_type = (
            fact_type_id if fact_type_id in pairs else reverse_pairs.get(fact_type_id)
        )
        if subordinate_type is None:
            continue
        companions = _companion_list(pairs, subordinate_type)
        if not companions:
            continue
        subordinate_id = f"{subordinate_type}|{suffix}"
        subordinate_value = _current_value_for_fact(state, subordinate_id)
        if subordinate_value is _NO_CURRENT_VALUE:
            # Companion alone may stand; the bounded consumer requires both.
            continue
        for companion_type in companions:
            key = (subordinate_type, companion_type, suffix)
            if key in checked:
                continue
            checked.add(key)
            companion_id = f"{companion_type}|{suffix}"
            companion_value = _current_value_for_fact(state, companion_id)
            if companion_value is _NO_CURRENT_VALUE:
                raise FindingModelError(
                    f"companion presence violated: {subordinate_id} is current "
                    f"({subordinate_value!r}) but {companion_id} has no current value; "
                    f"rejected, not recorded"
                )
            allowed = value_domains.get(companion_type)
            if allowed is not None and companion_value not in allowed:
                raise FindingModelError(
                    f"companion presence violated: {companion_id} is current with "
                    f"value {companion_value!r}; admitted domain is {sorted(allowed, key=repr)}; "
                    f"rejected, not recorded"
                )


def _enforce_companion_equalities(
    state: FindingState, registry: SchemaRegistry, touched_fact_ids: tuple[str, ...]
) -> None:
    """Enforce domain-declared same-statement numeric equality at admission.

    Equality is a source-admission invariant, not a derivation-pin concern.
    Both fact types share the identity-key suffix; a current subordinate with
    no current companion is left to the companion-presence rule, while a
    present unequal companion rejects the whole admission before execution.
    """
    pairs = getattr(registry, "companion_equality_pairs", None)
    if not pairs:
        return
    reverse_pairs = {companion: subordinate for subordinate, companion in pairs.items()}
    checked: set[tuple[str, str]] = set()
    for fact_id in touched_fact_ids:
        if "|" not in fact_id:
            continue
        fact_type_id, suffix = fact_id.split("|", 1)
        subordinate_type = fact_type_id if fact_type_id in pairs else reverse_pairs.get(fact_type_id)
        if subordinate_type is None:
            continue
        companion_type = pairs[subordinate_type]
        key = (subordinate_type, suffix)
        if key in checked:
            continue
        checked.add(key)
        subordinate_id = f"{subordinate_type}|{suffix}"
        companion_id = f"{companion_type}|{suffix}"
        subordinate_value = _current_value_for_fact(state, subordinate_id)
        companion_value = _current_value_for_fact(state, companion_id)
        if subordinate_value is _NO_CURRENT_VALUE or companion_value is _NO_CURRENT_VALUE:
            continue
        try:
            equal = subordinate_value == companion_value
        except Exception:
            equal = False
        if not equal:
            raise FindingModelError(
                f"companion equality violated: {subordinate_id} current value "
                f"{subordinate_value!r} does not equal {companion_id} current value "
                f"{companion_value!r}; rejected, not recorded"
            )


def _current_values_for_fact_type(
    state: FindingState, fact_type_id: str
) -> dict[str, Any]:
    """Every currently-held finding's value for one fact type, keyed by fact id.

    Mirrors ``_current_value_for_fact``'s last-inserted-wins rule but spans
    every distinct fact id of the given type (e.g. every 1099-DIV statement's
    own recorded-boxes finding), not one singular fact - a declaration fact
    type has exactly one fact id in practice, a per-statement recorded fact
    type may have several.
    """
    prefix = f"{fact_type_id}|"
    fact_ids = {
        finding["fact_id"]
        for finding in state.findings.values()
        if finding["fact_id"] == fact_type_id or finding["fact_id"].startswith(prefix)
    }
    values: dict[str, Any] = {}
    for fact_id in fact_ids:
        value = _current_value_for_fact(state, fact_id)
        if value is not _NO_CURRENT_VALUE:
            values[fact_id] = value
    return values


def _enforce_declaration_signal_contradictions(
    state: FindingState, registry: SchemaRegistry, touched_fact_ids: tuple[str, ...]
) -> None:
    """Reject an admission making a declared value and a contributed signal
    both current (ADR-0038 decision 5: the bidirectional admission-locus
    contradiction interlock).

    Same posture and same fold-based same-batch guarantee as
    ``_enforce_subset_invariants``: each declared rule
    (``registry.declaration_signal_contradictions``) names a categorical
    declaration fact type/value and a recorded fact type whose per-instance
    value carries a named field that, non-null on any currently-held
    instance, raises the contradicting signal. Enforcement runs against the
    fully-updated successor state, so it sees the touched act's own change
    plus every prior admission in the same fold - including same-batch
    ordering, for the identical reason ``_enforce_subset_invariants``
    documents: each act folds sequentially and this check runs on the
    resulting state, not a stale snapshot. A violating pair is never
    recorded: this function raises before the caller ever observes the
    successor state.
    """
    rules = getattr(registry, "declaration_signal_contradictions", None)
    if not rules:
        return
    touched_types = {fact_id.split("|", 1)[0] for fact_id in touched_fact_ids}
    for rule in rules:
        declaration_type = rule["declaration_fact_type"]
        signal_type = rule["signal_fact_type"]
        if declaration_type not in touched_types and signal_type not in touched_types:
            continue
        declared_values = _current_values_for_fact_type(state, declaration_type)
        if rule["declaration_value"] not in declared_values.values():
            continue
        signal_values = _current_values_for_fact_type(state, signal_type)
        signal_field = rule.get("signal_field")
        if signal_field is None:
            # ADR-0050 decision 2/4: successor signal is a current non-null
            # box-2a family member value (numeric amount), not a residual
            # recorded-boxes field. Historical null/residual content must not
            # masquerade as the signal.
            raised = any(value is not None for value in signal_values.values())
            signal_desc = "non-null amount"
        else:
            raised = any(
                isinstance(value, dict) and value.get(signal_field) is not None
                for value in signal_values.values()
            )
            signal_desc = repr(signal_field)
        if raised:
            raise FindingModelError(
                f"declaration/signal contradiction: {declaration_type} is "
                f"currently {rule['declaration_value']!r} but a current "
                f"{signal_type} finding records {signal_desc}; "
                f"rejected, not recorded"
            )


def _validate_finding(
    state: FindingState, finding: dict[str, Any], registry: SchemaRegistry
) -> None:
    declared = finding.get("schema")
    if declared not in ADMITTED_FINDING_SCHEMAS:
        raise FindingModelError(
            f"finding names no admitted schema version: {declared!r}"
        )
    registry.validate(str(declared), finding)
    if "pins" in finding:
        # Human findings carry no derivation pins. contribution_id is a
        # separate provenance field (ADR-0032 Decision 2) and must never
        # ride pins.finding_ids — the sole derivation-edge surface.
        raise FindingModelError("derived finding pins are not admitted in the kernel yet")
    if finding["id"] in state.findings:
        raise FindingModelError(f"finding already exists: {finding['id']}")

    contribution_id = finding.get("contribution_id")
    if contribution_id is not None:
        contribution = state.contributions.get(contribution_id)
        if contribution is None:
            raise FindingModelError(
                f"finding {finding['id']} references unknown contribution: "
                f"{contribution_id}"
            )
        # ADR-0032 Decision 2: contribution.evidence_id must be a member of
        # the finding's evidence_ids (Article 1 channel retained + consistent).
        if contribution["evidence_id"] not in finding["evidence_ids"]:
            raise FindingModelError(
                f"finding {finding['id']}: contribution {contribution_id} "
                f"evidence_id {contribution['evidence_id']!r} is not a member of "
                f"evidence_ids {list(finding['evidence_ids'])}"
            )

    lattice = facts.facts_of(state.fact_state)
    fact = lattice.get(finding["fact_id"])
    if fact is None:
        raise FindingModelError(f"finding references unknown fact: {finding['fact_id']}")
    fact_type = state.fact_state.fact_types[fact.fact_type_id]
    value_errors = sorted(
        jsonschema.Draft202012Validator(fact_type["value_schema"]).iter_errors(
            finding["value"]
        ),
        key=lambda e: list(e.absolute_path),
    )
    if value_errors:
        first = value_errors[0]
        raise FindingModelError(
            f"finding {finding['id']} value does not conform to "
            f"{fact_type['id']}: {first.message}"
        )

    # Elective answers are constituted by choice; determinable answers
    # report the world (Ontology §2, basis; Article 3). The fact's
    # declared nature and the finding's basis must agree in both
    # directions, or an election could be "closed" by a report and a
    # worldly fact by fiat.
    elective_fact = fact.nature == "elective"
    elective_basis = finding["basis"] == "elective"
    if elective_fact and not elective_basis:
        raise FindingModelError(
            f"finding {finding['id']}: fact {fact.fact_id} is elective; "
            f"its answer is constituted by choice, not {finding['basis']}"
        )
    if elective_basis and not elective_fact:
        raise FindingModelError(
            f"finding {finding['id']}: fact {fact.fact_id} is determinable; "
            "an elective basis cannot constitute its answer"
        )

    # Correction is governed by the fact type's declared supersession
    # rules (Ontology §2, Supersession; ADR-0041). The vocabulary is
    # closed to three values, each a state predicate over data the
    # kernel already tracks - never an identity check.
    already_answered = any(
        existing["fact_id"] == finding["fact_id"]
        for existing in state.findings.values()
    )
    if already_answered:
        policy = fact_type["supersession"]["policy"]
        if policy == "closed-on-attestation":
            _enforce_closed_on_attestation(state, finding, fact, fact_type)
        elif policy != "free":
            # "locked" (ADR-0041 Decision §3): correction forbidden
            # unconditionally once any finding for this fact_id exists -
            # identical to the already_answered test just computed, so no
            # further state read is needed.
            raise FindingModelError(
                f"finding {finding['id']}: fact {fact.fact_id} is governed by "
                f"supersession policy '{policy}', which does not permit correction here"
            )

    if finding["basis"] == "documentary" and not finding["evidence_ids"]:
        raise FindingModelError(
            f"documentary finding {finding['id']} names no evidence"
        )
    current_evidence = _current_evidence(state)
    for evidence_id in finding["evidence_ids"]:
        if evidence_id not in current_evidence:
            raise FindingModelError(
                f"finding {finding['id']} references non-current evidence: "
                f"{evidence_id}"
            )


def apply_assertion(
    state: FindingState, payload: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    finding = payload["finding"]
    _validate_finding(state, finding, registry)

    # SC-R1: A predicate-matching member fact for an adopted family must not be admittable
    # through a plain assertion unless the fact is already currently a member of the family
    # (which represents a same-member correction, not a new membership transition).
    lattice = facts.facts_of(state.fact_state)
    fact = lattice.get(finding["fact_id"])
    if fact and hasattr(registry, "family_member_predicates") and fact.fact_type_id in registry.family_member_predicates:
        fact_is_member = (
            any(f["fact_id"] == finding["fact_id"] for f in state.findings.values())
            and finding["fact_id"] not in state.withdrawn_fact_ids
        )
        if not fact_is_member:
            raise FindingModelError(
                f"cannot assert member fact {finding['fact_id']} through a plain assertion; "
                f"must use a member-transition instead"
            )

    findings = dict(state.findings)
    findings[finding["id"]] = finding
    new_state = replace(state, findings=findings)
    _enforce_subset_invariants(new_state, registry, (finding["fact_id"],))
    _enforce_declaration_signal_contradictions(new_state, registry, (finding["fact_id"],))
    _enforce_companion_presence(new_state, registry, (finding["fact_id"],))
    _enforce_companion_equalities(new_state, registry, (finding["fact_id"],))
    return new_state


def apply_contribution(
    state: FindingState, payload: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    """Admit a contribution citizen (ADR-0032 Decision 1).

    A contribution is an immutable product event: no supersession, no
    withdrawal. It anchors later findings by id; it is not a standing edge.
    """
    contribution = payload["contribution"]
    registry.validate(CONTRIBUTION_SCHEMA, contribution)
    contribution_id = contribution["id"]
    if contribution_id in state.contributions:
        raise FindingModelError(f"contribution already exists: {contribution_id}")
    evidence_id = contribution["evidence_id"]
    if evidence_id not in _current_evidence(state):
        raise FindingModelError(
            f"contribution {contribution_id} references non-current evidence: "
            f"{evidence_id}"
        )
    contributions = dict(state.contributions)
    contributions[contribution_id] = contribution
    return replace(state, contributions=contributions)


def _horizon_entity(citizen: dict[str, Any]) -> dict[str, Any]:
    """Project a horizon citizen into the fact lattice as an entity record.

    Closure fact types key on ``kernel.family-horizon`` with an ordinary
    entity key, so the lattice individuates one closure fact per horizon
    and succession displaces it through the existing individuation edge
    (ADR-0017 decision 5). The entity record is a projection of the same
    act, not a second store.
    """
    family = citizen["family"]
    return {
        "schema": facts.ENTITY_SCHEMA,
        "id": citizen["id"],
        "kind": horizons.HORIZON_ENTITY_KIND,
        "label": f"Membership horizon for {family['id']} {family['version']}",
    }


def _introduce_horizon_entity(
    entities: dict[str, facts.EntityLifecycle], citizen: dict[str, Any]
) -> None:
    if citizen["id"] in entities:
        raise FindingModelError(
            f"horizon id collides with an existing entity: {citizen['id']}"
        )
    entities[citizen["id"]] = facts.EntityLifecycle(
        entity=_horizon_entity(citizen), status="current"
    )


def apply_horizon_genesis(
    state: FindingState, payload: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    horizon_state = horizons.apply_genesis(state.horizon_state, payload, registry)
    entities = dict(state.fact_state.entities)
    citizen = horizon_state.horizons[payload["horizon_id"]].horizon
    _introduce_horizon_entity(entities, citizen)
    return replace(
        state,
        horizon_state=horizon_state,
        fact_state=replace(state.fact_state, entities=entities),
    )


def _withdraw_member_fact(state: FindingState, fact_id: str) -> frozenset[str]:
    if fact_id in state.withdrawn_fact_ids:
        raise FindingModelError(f"member fact already withdrawn: {fact_id}")
    if not any(
        finding["fact_id"] == fact_id for finding in state.findings.values()
    ):
        raise FindingModelError(
            f"member removal names a fact with no recorded finding: {fact_id}"
        )
    return state.withdrawn_fact_ids | {fact_id}


def apply_member_transition(
    state: FindingState, payload: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    """One atomic membership transition: member half plus horizon successor.

    The horizon half is validated first, so every admission negative in
    the recorded corpus (missing genesis, replayed successor, wrong or
    future predecessor) rejects before the member half is examined. Any
    rejection raises out of this pure function, leaving neither member
    state nor horizon state changed (ADR-0017 decision 3).
    """
    horizon_state, predecessor_id = horizons.apply_transition(
        state.horizon_state, payload, registry
    )

    member = payload["member"]
    findings = dict(state.findings)
    withdrawn = state.withdrawn_fact_ids
    withdrawal_correspondence = state.withdrawal_correspondence
    touched_fact_ids: list[str] = []
    if member["action"] in ("assert", "reclassify"):
        finding = member["finding"]
        _validate_finding(state, finding, registry)

        # SC-R2: A member-transition asserting a fact already in the family must be rejected.
        # Same-member value corrections belong on the ordinary assertion path instead.
        fact_id = finding["fact_id"]
        is_member = (
            any(f["fact_id"] == fact_id for f in state.findings.values())
            and fact_id not in state.withdrawn_fact_ids
        )
        if is_member:
            raise FindingModelError(
                f"transition asserting fact {fact_id} already in the family is rejected: "
                f"same-member correction belongs on the ordinary assertion path"
            )

        findings[finding["id"]] = finding
        touched_fact_ids.append(fact_id)
    if member["action"] in ("remove", "reclassify"):
        withdrawn = _withdraw_member_fact(state, member["fact_id"])
        touched_fact_ids.append(member["fact_id"])
        corresponds_to_fact_id = member.get("corresponds_to_fact_id")
        if corresponds_to_fact_id is not None:
            withdrawal_correspondence = dict(withdrawal_correspondence)
            withdrawal_correspondence[member["fact_id"]] = corresponds_to_fact_id

    entities = dict(state.fact_state.entities)
    predecessor_lifecycle = entities.get(predecessor_id)
    if predecessor_lifecycle is None:
        raise FindingModelError(
            f"horizon {predecessor_id} has no projected entity record"
        )
    successor_citizen = horizon_state.horizons[payload["successor"]["id"]].horizon
    _introduce_horizon_entity(entities, successor_citizen)
    entities[predecessor_id] = facts.EntityLifecycle(
        entity=predecessor_lifecycle.entity,
        status="superseded",
        successor_id=payload["successor"]["id"],
    )

    new_state = replace(
        state,
        horizon_state=horizon_state,
        findings=findings,
        withdrawn_fact_ids=withdrawn,
        withdrawal_correspondence=withdrawal_correspondence,
        fact_state=replace(state.fact_state, entities=entities),
    )
    _enforce_subset_invariants(new_state, registry, tuple(touched_fact_ids))
    _enforce_declaration_signal_contradictions(new_state, registry, tuple(touched_fact_ids))
    _enforce_companion_presence(new_state, registry, tuple(touched_fact_ids))
    _enforce_companion_equalities(new_state, registry, tuple(touched_fact_ids))
    return new_state


def _present_successor_claims(
    state: FindingState, migration: dict[str, Any]
) -> tuple[dict[str, Any], ...]:
    """Build presented successor claims from then-current predecessor findings.

    Only the last current finding on each predecessor fact is an input.
    Open predecessor facts produce no claim. The user asserts the
    presented value; this function does not write a successor finding.

    A predecessor finding whose fact_id is in ``state.withdrawn_fact_ids``
    is skipped entirely (see the ``if fact_id in state.withdrawn_fact_ids``
    check below): a withdrawn finding's true value is preserved unmodified
    in ``state.findings``, but it is no longer live, so no claim is built
    for it. A withdrawn predecessor's own true, last-recorded value is
    still separately checked for zero-ness by
    ``_refuse_unresolved_nonzero_withdrawals`` (``apply_migration_adoption``
    reads ``state.findings``/``state.withdrawn_fact_ids`` directly for that
    check, not this function's ``claims`` output) -- withdrawal never
    exempts a nonzero claim from that check on its own; it only ever
    matters for a claim whose value was already genuinely zero.
    """
    lattice = facts.facts_of(state.fact_state)
    claims: list[dict[str, Any]] = []
    last_by_fact: dict[str, dict[str, Any]] = {}
    for finding in state.findings.values():
        fact_id = finding["fact_id"]
        if fact_id in state.withdrawn_fact_ids:
            continue
        last_by_fact[fact_id] = finding
    successor_by_predecessor = {
        pair["predecessor"]: pair["successor"] for pair in migration["pairs"]
    }
    for fact in lattice.values():
        successor_id = successor_by_predecessor.get(fact.fact_type_id)
        if successor_id is None:
            continue
        current_finding = last_by_fact.get(fact.fact_id)
        if current_finding is None:
            continue
        claims.append(
            {
                "predecessor_finding_id": current_finding["id"],
                "predecessor_fact_id": fact.fact_id,
                "successor_fact_type_id": successor_id,
                "successor_fact_id": facts.fact_id_for(successor_id, fact.keys),
                "proposed_value": current_finding["value"],
                "migration_id": migration["id"],
            }
        )
    return tuple(claims)


def _is_zero_value(value: Any) -> bool:
    """True only for a value that unambiguously means "no live claim".

    A value this function cannot parse as a number is treated as *not*
    zero -- refusing an unresolved-looking claim is the safe default,
    never silently letting an unparseable value through. This is one of
    two independent ways a predecessor claim resolves before migration
    (the other is withdrawal, checked directly against
    ``state.withdrawn_fact_ids`` in ``_present_successor_claims`` --
    ``_is_zero_value`` never stands in for withdrawal, since a claim that
    is truly nonzero must never be asserted as zero to unblock migration;
    see ``_refuse_unresolved_nonzero_claims``).
    """
    if isinstance(value, bool):
        return value is False
    try:
        return Decimal(str(value)) == 0
    except (InvalidOperation, ValueError, TypeError):
        return False


def _refuse_unresolved_nonzero_claims(
    migration: dict[str, Any], claims: tuple[dict[str, Any], ...], registry: SchemaRegistry
) -> None:
    """Enforce an opt-in, registry-declared ``resolved-required`` resolution
    policy for this migration id (ADR-0072 Decision 4). Resolution for a
    nonzero predecessor claim is a genuinely-zero correction, or a
    withdrawal whose claim was already genuinely zero -- never a
    withdrawal alone for a claim that is still nonzero.

    Without this, adoption presents a claim for a then-current predecessor
    finding and immediately retires the predecessor type -- a real, live
    legacy value would be presented (never written) but no longer
    contribute to any computation, discarded with no refusal and no trace.

    A ``resolved-required`` migration id instead refuses adoption outright
    while any predecessor claim remains live and nonzero. ``claims`` (built
    by ``_present_successor_claims``) already omits any predecessor
    finding whose fact_id is in ``state.withdrawn_fact_ids`` -- so a claim
    reaching this function was never withdrawn; a withdrawn predecessor's
    own nonzero value is separately checked by
    ``_refuse_unresolved_nonzero_withdrawals``, which this function does
    not duplicate. The one currently accepted way to resolve a live,
    nonzero legacy claim before adoption is a same-identity correction to a
    genuinely zero value -- the fact type's own declared
    ``supersession.policy: "free"`` (as ADR-0072's amount-collision
    resolution already uses) -- valid only when the amount genuinely
    became zero (e.g. a data-entry correction), never to paper over a
    claim that is still true. A member-transition withdrawal, with or
    without a named ``corresponds_to_fact_id``, does not resolve a live,
    nonzero claim: see ``_refuse_unresolved_nonzero_withdrawals``, which
    refuses that shape unconditionally.

    The policy is declared on ``registry.migration_resolution_policies``
    (a domain loader populates the map, mirroring
    ``companion_presence_pairs`` / ``declaration_signal_contradictions``),
    never hardcoded to a migration or fact-type id in this generic kernel
    mechanism -- a migration id absent from the map keeps today's
    unconditional-adoption behavior.
    """
    if registry.migration_resolution_policies.get(migration["id"]) != "resolved-required":
        return
    unresolved = sorted(
        claim["predecessor_fact_id"]
        for claim in claims
        if not _is_zero_value(claim["proposed_value"])
    )
    if unresolved:
        raise FindingModelError(
            f"migration {migration['id']}: {MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM} -- "
            "adoption refused: unresolved legacy claim(s) would be discarded "
            "by this migration (never carried forward as a computation "
            "input). A nonzero legacy claim blocks migration; the only "
            "currently accepted resolution is a same-identity correction to "
            "a genuinely zero value via the predecessor fact type's own "
            "declared supersession policy. Withdrawing the claim does not "
            "resolve it -- it must already be zero. Never assert zero for a "
            f"claim that is still true: {', '.join(unresolved)}"
        )


def _refuse_unresolved_nonzero_withdrawals(
    state: FindingState, migration: dict[str, Any], registry: SchemaRegistry
) -> None:
    """One coherent rule for a withdrawn predecessor fact under a
    ``resolved-required`` migration: it blocks adoption if and only if its
    own true, last-recorded value is still nonzero -- regardless of
    whether the removing member-transition named a
    ``corresponds_to_fact_id`` (act-member-transition.v3), and regardless
    of whether any named correspondence is real, current, or displaced.

    A named correspondence (``corresponds_to_fact_id``) is never checked or
    consulted for a withdrawal, regardless of value: the predecessor fact
    type carries no obligation, payer, or report identity anywhere in its
    own declared identity keys for any correspondence to be checked
    against, so a real, current, but domain-wrong correspondence could
    otherwise let migration admit and publish a known-wrong result, and a
    withdrawn predecessor whose value is already genuinely zero must never
    be refused merely for omitting an irrelevant "replacement" for a
    computational role that never existed. No correspondence is required,
    checked, or consulted for any withdrawal, regardless of value. A
    nonzero withdrawn predecessor always blocks; a zero withdrawn
    predecessor never does. The only currently accepted way to resolve a
    live or withdrawn nonzero legacy claim is a same-identity correction
    to a genuinely zero value (see ``_refuse_unresolved_nonzero_claims``).
    Whether to build a genuine representation-transfer adjudication act
    remains an explicit, undecided owner question (ADR-0072, "Open and
    owner-held" in ``docs/phase-state.md``) -- not something this function
    should approximate with another structural proxy.
    """
    if registry.migration_resolution_policies.get(migration["id"]) != "resolved-required":
        return
    predecessor_types = {pair["predecessor"] for pair in migration["pairs"]}
    lattice = facts.facts_of(state.fact_state)
    last_by_fact: dict[str, dict[str, Any]] = {}
    for finding in state.findings.values():
        last_by_fact[finding["fact_id"]] = finding
    unresolved = sorted(
        fact.fact_id
        for fact in lattice.values()
        if fact.fact_type_id in predecessor_types
        and fact.fact_id in state.withdrawn_fact_ids
        and fact.fact_id in last_by_fact
        and not _is_zero_value(last_by_fact[fact.fact_id]["value"])
    )
    if unresolved:
        raise FindingModelError(
            f"migration {migration['id']}: {MIGRATION_UNRESOLVED_PREDECESSOR_CLAIM} -- "
            "adoption refused: withdrawn predecessor fact(s) still carry a "
            "true, nonzero historical value. A nonzero legacy claim blocks "
            "migration whether or not it was withdrawn, and whether or not "
            "the withdrawal named a corresponds_to_fact_id -- no accepted "
            "mechanism can check a claimed representation transfer against "
            "anything, since the predecessor fact type carries no "
            "obligation, payer, or report identity. The only currently "
            "accepted resolution is a same-identity correction to a "
            "genuinely zero value via the predecessor fact type's own "
            f"declared supersession policy: {', '.join(unresolved)}"
        )


def apply_migration_adoption(
    state: FindingState, payload: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    """Adopt a migration artifact: retire named types, present claims."""
    migration = payload["migration"]
    registry.validate_declared(migration)
    claims = _present_successor_claims(state, migration)
    _refuse_unresolved_nonzero_claims(migration, claims, registry)
    _refuse_unresolved_nonzero_withdrawals(state, migration, registry)
    new_fact_state = facts.apply_migration_adoption(
        state.fact_state, payload, registry
    )
    return replace(
        state,
        fact_state=new_fact_state,
        presented_successor_claims=state.presented_successor_claims + claims,
    )


_APPLIERS = {
    "evidence-submitted": apply_evidence_submitted,
    "evidence-replaced": apply_evidence_replaced,
    "assertion": apply_assertion,
    "horizon-genesis": apply_horizon_genesis,
    "member-transition": apply_member_transition,
    "contribution": apply_contribution,
    "migration-adoption": apply_migration_adoption,
}

_FACT_ACT_KINDS = frozenset({"bundle-adoption", "entity-introduced", "entity-superseded"})

# The act kinds the kernel projection owns. Other families (e.g. the derivation
# family's `derived-publication`) may share the workspace act log; the kernel
# projects only its own kinds and passes over the rest (ADR-0010 compose-over).
# This is safe: the act log validates every committed act against its payload
# schema at read time, so a non-kernel kind here is a known other-family act,
# never a typo.
KERNEL_ACT_KINDS = _FACT_ACT_KINDS | frozenset(_APPLIERS)


def apply_act(
    state: FindingState, act: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    """Advance the evidence/finding projection by one act."""
    kind = act["kind"]
    if kind not in KERNEL_ACT_KINDS:
        return state  # not a kernel act; another family projects it
    if kind in _FACT_ACT_KINDS:
        return replace(
            state,
            fact_state=facts.apply_act(state.fact_state, act, registry),
        )
    return _APPLIERS[kind](state, act["payload"], registry)


def project(acts: tuple[dict[str, Any], ...], registry: SchemaRegistry) -> FindingState:
    state = initial_state()
    for act in acts:
        state = apply_act(state, act, registry)
    return state


def evidentiary_standing(state: FindingState) -> dict[str, FindingStanding]:
    """Return findings with derived standing of their evidence references."""
    standing: dict[str, FindingStanding] = {}
    for finding_id, finding in state.findings.items():
        refs: list[EvidenceReferenceStanding] = []
        for evidence_id in finding["evidence_ids"]:
            lifecycle = state.evidence[evidence_id]
            refs.append(
                EvidenceReferenceStanding(
                    evidence_id=evidence_id,
                    status=lifecycle.status,
                    successor_id=lifecycle.successor_id,
                )
            )
        standing[finding_id] = FindingStanding(
            finding=finding,
            evidence=tuple(refs),
        )
    return standing
