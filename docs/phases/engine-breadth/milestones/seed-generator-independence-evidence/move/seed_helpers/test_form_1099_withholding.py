"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from typing import Any
from typing import cast
from seed_helpers.test_other_dependents_credit_track1 import JOINT_STATUS
from seed_helpers.test_other_dependents_credit_track1 import build
from seed_helpers.test_other_dependents_credit_track1 import _complete
from seed_helpers.test_refund_or_amount_owed_track1 import _act
from seed_helpers.test_refund_or_amount_owed_track1 import _attested
from seed_helpers.test_refund_or_amount_owed_track1 import _load

USER = "demo.user.filer-1"

YEAR = "2025"

SCOPE_KEY = {"tax-year": YEAR, "subject": "demo.primary"}

NO_OTHER_DEPENDENT = "tax.us.2025.ctc.no-other-dependent"

G_B4_FAMILY = "tax.us.2025.f1099g.b4"

G_B4 = "tax.us.2025.f1099g.box4-withholding"

G_B4_CLOSURE = "tax.us.2025.f1099g.b4.source-closure"

SSA_B6_FAMILY = "tax.us.2025.ssa1099.b6"

SSA_B6 = "tax.us.2025.ssa1099.box6-voluntary-withholding"

SSA_B6_CLOSURE = "tax.us.2025.ssa1099.b6.source-closure"

def _add(acts: list[dict[str, object]], kind: str, payload: dict[str, object]) -> None:
    acts.append(_act(len(acts), kind, payload))

def _close(acts: list[dict[str, object]], closure_fact: str, horizon: str, finding_id: str) -> None:
    _add(acts, "assertion", {"finding": _attested(finding_id, f"{closure_fact}|family-horizon={horizon},tax-year={YEAR}", True)})

def _unemployment_withholding(acts: list[dict[str, object]], amounts: list[float | None], *, close: bool = True) -> None:
    """Form 1099-G box 4 (core v59): one entry per recorded statement; None records no amount."""
    _add(acts, "bundle-adoption", {"bundle": _load("f1099g-box4.bundle.json")})
    head = "demo.fw.g4.h0"
    _add(acts, "horizon-genesis", {"family": {"id": G_B4_FAMILY, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": head})
    for i, amount in enumerate(amounts):
        if amount is None:
            continue
        keys = (("payer", f"demo.fw.g.payer.{i}"), ("statement", f"demo.fw.g.stmt.{i}"))
        head = _transition(acts, (G_B4_FAMILY, "v1"), head, f"demo.fw.g4.h{i + 1}", f"demo.fw.g.box4.{i}", G_B4, keys, amount)
    if close:
        _close(acts, G_B4_CLOSURE, head, "demo.fw.g.closure.box4")

def _social_security_withholding(acts: list[dict[str, object]], amounts: list[float | None], *, close: bool = True) -> None:
    """Form SSA-1099 box 6 (core v59): one entry per recorded statement; None records no amount."""
    _add(acts, "bundle-adoption", {"bundle": _load("ssa1099-box6.bundle.json")})
    head = "demo.fw.ssa6.h0"
    _add(acts, "horizon-genesis", {"family": {"id": SSA_B6_FAMILY, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": head})
    for i, amount in enumerate(amounts):
        if amount is None:
            continue
        keys = (("statement", f"demo.fw.ssa.stmt.{i}"),)
        head = _transition(acts, (SSA_B6_FAMILY, "v1"), head, f"demo.fw.ssa6.h{i + 1}", f"demo.fw.ssa.box6.{i}", SSA_B6, keys, amount)
    if close:
        _close(acts, SSA_B6_CLOSURE, head, "demo.fw.ssa.closure.box6")

def _w2_withholding(acts: list[dict[str, object]], amount: float) -> None:
    """Sets the base's one W-2 box 2 amount (the base records zero)."""
    hits = 0
    for act in acts:
        finding = cast(dict[str, Any], act["payload"]).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith("tax.us.2025.w2.box2-withholding|"):
            finding["value"] = amount
            hits += 1
    assert hits == 1, hits

def _base(*, wages: float, w2_withheld: float = 0.0, joint: bool = False) -> list[dict[str, object]]:
    status: dict[str, Any] = {"filing_status": JOINT_STATUS} if joint else {}
    acts = _complete(build(wages=wages, children={}, return_answers={NO_OTHER_DEPENDENT: "yes"}, **status))
    _w2_withholding(acts, w2_withheld)
    return acts
