"""The cf-loss-limit hand-value function equals the Schedule D instruction arithmetic.

The expected values pinned by tests/test_cf_loss_limit_v96.py come from
hand.py, so they must not themselves be engine output. These synthetic cases
restate the 2025 Schedule D instructions (loss limit 3,000, or 1,500 married
filing separately; the Capital Loss Carryover Worksheet) as literal numbers.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

HAND = Path(__file__).resolve().parents[1] / ("docs/phases/engine-breadth/milestones/"
                                              "cf-loss-limit-evidence/hand.py")


def _values(status: str, st: int, lt: int) -> dict[str, Any]:
    return evidence_loader.load(HAND, "cfl_t1_hand_fast").values(status, st, lt)  # type: ignore[no-any-return]


# (status, short-term, long-term) -> (line 16, line 21 as a loss, 1040 line 15, 2026 carry ST, LT)
CASES = [
    ("single", -1500, 0, -1500, -1500, 32750, 0, 0),             # below the limit: whole loss
    ("single", 0, -3000, -3000, -3000, 31250, 0, 0),             # at the limit
    ("single", -5000, 0, -5000, -3000, 31250, 2000, 0),          # above: short-term excess carries
    ("single", 0, -5000, -5000, -3000, 31250, 0, 2000),          # above: long-term excess carries
    ("single", -2500, -2500, -5000, -3000, 31250, 0, 2000),      # split: short-term used first
    ("married_filing_separately", -750, 0, -750, -750, 33500, 0, 0),
    ("married_filing_separately", 0, -1500, -1500, -1500, 32750, 0, 0),
    ("married_filing_separately", -1750, -1750, -3500, -1500, 32750, 250, 1750),
    ("married_filing_jointly", -3500, 0, -3500, -3000, 15500, 500, 0),  # joint deduction 31,500
    ("single", 4000, -1000, 3000, None, 37250, 0, 0),           # net gain: no line 21 loss
]


@pytest.mark.parametrize("status,st,lt,l16,l21,l15,carry_st,carry_lt", CASES)
def test_hand_values_match_instruction_arithmetic(status: str, st: int, lt: int, l16: int,
                                                  l21: int | None, l15: int, carry_st: int,
                                                  carry_lt: int) -> None:
    got = _values(status, st, lt)
    assert got["schedule-d.line-7"] == st and got["schedule-d.line-15"] == lt
    assert got["schedule-d.line-16"] == l16
    assert got["schedule-d.line-21"] == l21
    assert got["form1040.line-7a"] == (l21 if l21 is not None else l16)
    assert got["form1040.line-15"] == l15
    assert (got["carryover-2026.short-term"], got["carryover-2026.long-term"]) == (carry_st, carry_lt)
