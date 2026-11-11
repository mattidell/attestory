"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

import copy
from seed_helpers.test_refund_or_amount_owed_track1 import _act
from seed_helpers.test_refund_or_amount_owed_track1 import _attested
from seed_helpers.test_refund_or_amount_owed_track1 import _load

NO21 = "tax.us.2025.schedule2-partii-scope.no-line21-additional-taxes"

NO2731 = "tax.us.2025.lines27-31-scope.no-refundable-credits-or-other-payments"

NO38 = "tax.us.2025.line38-scope.no-estimated-tax-penalty"

EST = "tax.us.2025.payments.estimated-and-prior-year-applied"

APPLIED = "tax.us.2025.payments.overpayment-applied-to-2026"

def _add_bottom_line_answers(
    acts: list[dict[str, object]], *, estimated: float = 0.0, applied_2026: float | None = None
) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("refund-or-amount-owed-questions.bundle.json")})
    add("assertion", {"finding": _attested("demo.t2.no21", f"{NO21}|tax-year=2025", "yes")})
    add("assertion", {"finding": _attested("demo.t2.no2731", f"{NO2731}|tax-year=2025", "yes")})
    add("assertion", {"finding": _attested("demo.t2.no38", f"{NO38}|tax-year=2025", "yes")})
    add("assertion", {"finding": _attested("demo.t2.estimated", f"{EST}|tax-year=2025", estimated)})
    if applied_2026 is not None:
        add("assertion", {"finding": _attested("demo.t2.applied2026", f"{APPLIED}|tax-year=2025", applied_2026)})
    return acts

def _add_box2_only(acts: list[dict[str, object]], *, employer: str, slip: str, amount: float) -> list[dict[str, object]]:
    acts = copy.deepcopy(acts)

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("w2-box2.bundle.json")})
    add("assertion", {"finding": _attested(f"demo.t2.box2.{slip}", f"tax.us.2025.w2.box2-withholding|employer={employer},w2-slip={slip},tax-year=2025", amount)})
    return acts
