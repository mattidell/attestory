"""Synthetic authority fixture helpers for source completeness.

Provides explicit fresh v2 horizon genesis and true closure authority for
empty wash-sale families without mutating or rewriting existing historical v1 acts.
"""

from __future__ import annotations

from typing import Any

WASH_SALE_V2_EMPTY_FAMILIES = (
    (
        "tax.us.2025.f1099b.covered-w-st",
        "demo.synthetic.wst.v2.h0",
        "tax.us.2025.f1099b.covered-w-st.source-closure",
    ),
    (
        "tax.us.2025.f1099b.covered-w-st-proceeds",
        "demo.synthetic.wst-p.v2.h0",
        "tax.us.2025.f1099b.covered-w-st-proceeds.source-closure",
    ),
    (
        "tax.us.2025.f1099b.covered-w-st-basis",
        "demo.synthetic.wst-b.v2.h0",
        "tax.us.2025.f1099b.covered-w-st-basis.source-closure",
    ),
    (
        "tax.us.2025.f1099b.covered-w-st-adjustment",
        "demo.synthetic.wst-a.v2.h0",
        "tax.us.2025.f1099b.covered-w-st-adjustment.source-closure",
    ),
    (
        "tax.us.2025.f1099b.covered-w-lt",
        "demo.synthetic.wlt.v2.h0",
        "tax.us.2025.f1099b.covered-w-lt.source-closure",
    ),
    (
        "tax.us.2025.f1099b.covered-w-lt-proceeds",
        "demo.synthetic.wlt-p.v2.h0",
        "tax.us.2025.f1099b.covered-w-lt-proceeds.source-closure",
    ),
    (
        "tax.us.2025.f1099b.covered-w-lt-basis",
        "demo.synthetic.wlt-b.v2.h0",
        "tax.us.2025.f1099b.covered-w-lt-basis.source-closure",
    ),
    (
        "tax.us.2025.f1099b.covered-w-lt-adjustment",
        "demo.synthetic.wlt-a.v2.h0",
        "tax.us.2025.f1099b.covered-w-lt-adjustment.source-closure",
    ),
)


WASH_SALE_FAMILY_IDS = frozenset(fam[0] for fam in WASH_SALE_V2_EMPTY_FAMILIES)


def _is_v1_wash_sale_act(act: dict[str, Any]) -> bool:
    payload = act.get("payload")
    if not isinstance(payload, dict):
        return False
    kind = act.get("kind")
    if kind == "horizon-genesis":
        fam = payload.get("family")
        if isinstance(fam, dict):
            return fam.get("id") in WASH_SALE_FAMILY_IDS and fam.get("version") == "v1"
    elif kind == "assertion":
        finding = payload.get("finding")
        if isinstance(finding, dict):
            fact_id = str(finding.get("fact_id", ""))
            return any(fact_id.startswith(f"{fid}.source-closure|") for fid in WASH_SALE_FAMILY_IDS)
    return False


def append_wash_sale_v2_empty_authority(
    acts: list[dict[str, Any]],
    *,
    scope: dict[str, str] | None = None,
    tax_year: str = "2025",
) -> None:
    """Appends fresh v2 horizon genesis and true closure for the 8 empty wash-sale families.

    Removes any historical v1 acts for the wash-sale families from the synthetic base to
    guarantee a clean v2 authority baseline without concurrent active chains.
    """
    target_scope = {"tax-year": tax_year, "subject": "demo.primary"} if scope is None else dict(scope)

    acts[:] = [a for a in acts if not _is_v1_wash_sale_act(a)]

    for family_id, horizon_id, closure_type in WASH_SALE_V2_EMPTY_FAMILIES:
        idx = len(acts)
        acts.append(
            {
                "schema": "act.v1",
                "act_id": f"act-syn-v2-{idx:04d}",
                "kind": "horizon-genesis",
                "actor": "user",
                "at": f"2026-10-18T20:{idx % 60:02d}:00Z",
                "committed_against": idx,
                "payload": {
                    "family": {"id": family_id, "version": "v2"},
                    "scope": target_scope,
                    "horizon_id": horizon_id,
                },
            }
        )
        idx = len(acts)
        acts.append(
            {
                "schema": "act.v1",
                "act_id": f"act-syn-v2-{idx:04d}",
                "kind": "assertion",
                "actor": "user",
                "at": f"2026-10-18T20:{idx % 60:02d}:00Z",
                "committed_against": idx,
                "payload": {
                    "finding": {
                        "schema": "finding.v1",
                        "id": f"f.closure.{horizon_id}",
                        "fact_id": f"{closure_type}|family-horizon={horizon_id},tax-year={tax_year}",
                        "value": True,
                        "basis": "attested",
                        "evidence_ids": [],
                    }
                },
            }
        )
