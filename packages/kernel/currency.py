"""Derived currency and displacement closure.

Article 7 permits exactly two cascade edges: derivation and
individuation. This module computes current/displaced state from the
record projection each time; it never writes or trusts current flags.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from packages.kernel.facts import facts_of
from packages.kernel.findings import FindingState

DECLARED_EDGE_KINDS = frozenset({"derivation", "individuation"})


class CurrencyMaterializationError(Exception):
    """A materialized current/superseded view disagrees with recomputation."""


@dataclass(frozen=True)
class DisplacementReason:
    """Why a citizen is displaced from current state."""

    kind: str
    by: str


@dataclass(frozen=True)
class CurrencyView:
    """Derived current/displaced finding and evidence IDs."""

    current_finding_ids: frozenset[str]
    displaced_finding_ids: frozenset[str]
    current_evidence_ids: frozenset[str]
    displaced_evidence_ids: frozenset[str]
    reasons: dict[str, tuple[DisplacementReason, ...]] = field(default_factory=dict)


EdgeMap = Mapping[str, Mapping[str, set[str]]]


def displacement_closure(
    roots: set[str],
    edges: EdgeMap,
) -> tuple[set[str], dict[str, tuple[DisplacementReason, ...]]]:
    """Walk only declared displacement edges from root displaced IDs."""
    displaced = set(roots)
    reasons: dict[str, list[DisplacementReason]] = {}
    frontier = list(roots)
    while frontier:
        source = frontier.pop(0)
        for edge_kind in sorted(DECLARED_EDGE_KINDS):
            dependents = edges.get(edge_kind, {}).get(source, set())
            for dependent in sorted(dependents):
                reasons.setdefault(dependent, []).append(
                    DisplacementReason(kind=edge_kind, by=source)
                )
                if dependent not in displaced:
                    displaced.add(dependent)
                    frontier.append(dependent)
    return displaced, {
        citizen_id: tuple(citizen_reasons)
        for citizen_id, citizen_reasons in reasons.items()
    }


def _add_edge(
    edges: dict[str, dict[str, set[str]]],
    kind: str,
    source: str,
    dependent: str,
) -> None:
    edges.setdefault(kind, {}).setdefault(source, set()).add(dependent)


def _finding_corrections(
    state: FindingState,
) -> tuple[set[str], dict[str, list[DisplacementReason]]]:
    latest_by_fact: dict[str, str] = {}
    displaced: set[str] = set()
    reasons: dict[str, list[DisplacementReason]] = {}
    for finding_id, finding in state.findings.items():
        fact_id = finding["fact_id"]
        previous = latest_by_fact.get(fact_id)
        if previous is not None:
            displaced.add(previous)
            reasons.setdefault(previous, []).append(
                DisplacementReason(kind="correction", by=finding_id)
            )
        latest_by_fact[fact_id] = finding_id
    return displaced, reasons


def _declared_edges(
    state: FindingState,
    extra_edges: EdgeMap | None,
) -> dict[str, dict[str, set[str]]]:
    edges: dict[str, dict[str, set[str]]] = {"derivation": {}, "individuation": {}}
    for finding_id, finding in state.findings.items():
        for pinned_id in finding.get("pins", {}).get("finding_ids", []):
            _add_edge(edges, "derivation", pinned_id, finding_id)

    lattice = facts_of(state.fact_state)
    for finding_id, finding in state.findings.items():
        fact = lattice.get(finding["fact_id"])
        if fact is None:
            continue
        for citizen_id in fact.individuated_by:
            _add_edge(edges, "individuation", citizen_id, finding_id)

    if extra_edges is not None:
        for kind in DECLARED_EDGE_KINDS:
            for source, dependents in extra_edges.get(kind, {}).items():
                for dependent in dependents:
                    _add_edge(edges, kind, source, dependent)
    return edges


def compute_currency(
    state: FindingState,
    *,
    root_displacements: set[str] | None = None,
    extra_edges: EdgeMap | None = None,
) -> CurrencyView:
    """Compute currency from a projection, never from stored flags."""
    correction_roots, reason_lists = _finding_corrections(state)
    roots = set(correction_roots)
    if root_displacements is not None:
        roots.update(root_displacements)

    closure, closure_reasons = displacement_closure(roots, _declared_edges(state, extra_edges))
    for citizen_id, citizen_reasons in closure_reasons.items():
        reason_lists.setdefault(citizen_id, []).extend(citizen_reasons)

    finding_ids = set(state.findings)
    displaced_findings = finding_ids & closure
    current_findings = finding_ids - displaced_findings

    current_evidence = {
        evidence_id
        for evidence_id, lifecycle in state.evidence.items()
        if lifecycle.status == "current"
    }
    displaced_evidence = set(state.evidence) - current_evidence

    return CurrencyView(
        current_finding_ids=frozenset(current_findings),
        displaced_finding_ids=frozenset(displaced_findings),
        current_evidence_ids=frozenset(current_evidence),
        displaced_evidence_ids=frozenset(displaced_evidence),
        reasons={
            citizen_id: tuple(reasons)
            for citizen_id, reasons in reason_lists.items()
            if citizen_id in closure
        },
    )


def assert_materialization_matches(
    view: CurrencyView,
    materialized: Mapping[str, Any],
) -> None:
    """Catch stored stale flags by diffing them against recomputation."""
    findings = materialized.get("findings", {})
    if not isinstance(findings, Mapping):
        raise CurrencyMaterializationError("materialized findings must be a mapping")
    for finding_id, payload in findings.items():
        if not isinstance(finding_id, str) or not isinstance(payload, Mapping):
            raise CurrencyMaterializationError("malformed materialized finding entry")
        stored_current = payload.get("current")
        if not isinstance(stored_current, bool):
            raise CurrencyMaterializationError(
                f"materialized finding {finding_id} has no boolean current flag"
            )
        recomputed = finding_id in view.current_finding_ids
        if stored_current != recomputed:
            raise CurrencyMaterializationError(
                f"materialized finding {finding_id} current={stored_current}, "
                f"recomputed={recomputed}"
            )
