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

from packages.kernel import facts
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
    """Fold state for evidence and asserted findings."""

    fact_state: facts.KernelState = field(default_factory=facts.initial_state)
    evidence: dict[str, EvidenceLifecycle] = field(default_factory=dict)
    findings: dict[str, dict[str, Any]] = field(default_factory=dict)


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


_APPLIERS = {
    "evidence-submitted": apply_evidence_submitted,
    "evidence-replaced": apply_evidence_replaced,
    "assertion": apply_assertion,
}


def apply_act(
    state: FindingState, act: dict[str, Any], registry: SchemaRegistry
) -> FindingState:
    """Advance the evidence/finding projection by one act."""
    if act["kind"] in {"bundle-adoption", "entity-introduced", "entity-superseded"}:
        return replace(
            state,
            fact_state=facts.apply_act(state.fact_state, act, registry),
        )
    applier = _APPLIERS.get(act["kind"])
    if applier is None:
        raise FindingModelError(f"no applier for act kind: {act['kind']}")
    return applier(state, act["payload"], registry)


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
