"""Evidence and asserted findings.

Track 4 keeps Article 1's boundary explicit: evidence is source-flavor
provenance for findings, never a parent or identity source. Assertion
acts create immutable finding citizens; evidence replacement changes a
derived evidentiary-standing view without rewriting findings.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

import jsonschema

from packages.kernel import facts, horizons
from packages.kernel.schema_registry import SchemaRegistry

EVIDENCE_SCHEMA = "evidence.v1"
FINDING_SCHEMA = "finding.v1"


class FindingModelError(Exception):
    """An evidence or assertion act is semantically inadmissible."""


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
    horizon_state: horizons.HorizonState = field(default_factory=horizons.initial_state)
    # Facts whose member standing was withdrawn by a member-transition
    # remove/reclassify. Withdrawal is a displacement *root* over the
    # fact's findings (like correction), never a new edge kind.
    withdrawn_fact_ids: frozenset[str] = frozenset()


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


def _validate_finding(
    state: FindingState, finding: dict[str, Any], registry: SchemaRegistry
) -> None:
    registry.validate(FINDING_SCHEMA, finding)
    if "pins" in finding:
        raise FindingModelError("derived finding pins are not admitted in the kernel yet")
    if finding["id"] in state.findings:
        raise FindingModelError(f"finding already exists: {finding['id']}")

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
    # rules (Ontology §2, Supersession). Only the "free" policy is
    # published today, but the declaration is consulted, not decorative:
    # restricted policies arrive with rule artifacts and bind here.
    already_answered = any(
        existing["fact_id"] == finding["fact_id"]
        for existing in state.findings.values()
    )
    if already_answered:
        policy = fact_type["supersession"]["policy"]
        if policy != "free":
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
    findings = dict(state.findings)
    findings[finding["id"]] = finding
    return replace(state, findings=findings)


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
    if member["action"] in ("assert", "reclassify"):
        finding = member["finding"]
        _validate_finding(state, finding, registry)
        findings[finding["id"]] = finding
    if member["action"] in ("remove", "reclassify"):
        withdrawn = _withdraw_member_fact(state, member["fact_id"])

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

    return replace(
        state,
        horizon_state=horizon_state,
        findings=findings,
        withdrawn_fact_ids=withdrawn,
        fact_state=replace(state.fact_state, entities=entities),
    )


_APPLIERS = {
    "evidence-submitted": apply_evidence_submitted,
    "evidence-replaced": apply_evidence_replaced,
    "assertion": apply_assertion,
    "horizon-genesis": apply_horizon_genesis,
    "member-transition": apply_member_transition,
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
