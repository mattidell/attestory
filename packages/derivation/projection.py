"""Derivation currency: displacement folded over derived findings.

ADR-0010 decision 3 (compose-over): the kernel `currency.py` keeps folding
kernel findings and stays unaware of the derivation family. This layer reads
derived findings from the act log, turns their `input`/`choice` pins into
derivation edges, and runs the kernel's own `displacement_closure` from the
kernel's displaced set. So superseding an input finding displaces every derived
finding that stood on it — the correction cascade, as a consequence of the
record (Article 7), chaining through derived-on-derived.

Derived findings are displacement *targets, never roots* (decision 5): they
carry a `symbol`, not a `fact_id`, and never enter the kernel's correction-root
detection. A stale derived value leaves current state by displacement along the
edge, not by same-fact correction; producing its replacement is re-derivation,
which is out of scope (decision 6).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.kernel.currency import (
    CurrencyView,
    DisplacementReason,
    compute_currency,
    displacement_closure,
)
from packages.kernel.findings import project
from packages.kernel.schema_registry import SchemaRegistry

_DEPENDENCY_ROLES = frozenset({"input", "choice"})


def derived_findings_from_acts(acts: tuple[dict[str, Any], ...]) -> dict[str, dict[str, Any]]:
    """Index the derived findings carried by derived-publication acts."""
    return {
        act["payload"]["finding"]["id"]: act["payload"]["finding"]
        for act in acts
        if act["kind"] == "derived-publication"
    }


def derivation_edges(derived: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    """Edges pinned_finding -> derived_finding, from dependency pins only.

    Parameter / operation-semantics / adoption / governance pins are provenance,
    never displacement edges: changing a parameter version is a re-adoption, not
    a correction of a finding this derived value stood on.
    """
    edges: dict[str, set[str]] = {}
    for finding_id, finding in derived.items():
        for pin in finding["pins"]:
            if pin["role"] in _DEPENDENCY_ROLES:
                edges.setdefault(pin["id"], set()).add(finding_id)
    return edges


@dataclass(frozen=True)
class DerivationCurrencyView:
    current_derived_ids: frozenset[str]
    displaced_derived_ids: frozenset[str]
    reasons: dict[str, tuple[DisplacementReason, ...]]


def compute_derivation_currency(
    kernel_currency: CurrencyView,
    derived: dict[str, dict[str, Any]],
) -> DerivationCurrencyView:
    """Propagate the kernel's displacement into derived findings."""
    edges = derivation_edges(derived)
    roots = set(kernel_currency.displaced_finding_ids)
    closure, reasons = displacement_closure(roots, {"derivation": edges})
    derived_ids = set(derived)
    displaced = derived_ids & closure
    return DerivationCurrencyView(
        current_derived_ids=frozenset(derived_ids - displaced),
        displaced_derived_ids=frozenset(displaced),
        reasons={finding_id: reasons.get(finding_id, ()) for finding_id in sorted(displaced)},
    )


def workspace_currency(
    acts: tuple[dict[str, Any], ...],
    registry: SchemaRegistry,
) -> tuple[CurrencyView, DerivationCurrencyView]:
    """Both currency views over one act log: kernel findings and derived findings."""
    kernel_currency = compute_currency(project(acts, registry))
    derived = derived_findings_from_acts(acts)
    return kernel_currency, compute_derivation_currency(kernel_currency, derived)
