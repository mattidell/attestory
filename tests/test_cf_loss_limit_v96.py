"""Box C and F capital losses are limited at Schedule D line 21, on published core v96.

A subset of the cf-loss-limit P0 returns (docs/phases/engine-breadth/milestones/
cf-loss-limit-evidence) runs through the real live_coordinate_run and the saved
page: Form 8949 box C only (short-term), box F only (long-term) and C plus F,
below, at and above the limit, for single and married filing separately, plus
the same amounts through box A/D as a control. Schedule D lines 7, 15, 16, 21
and Form 1040 lines 7a and 15 are asserted against the P0 hand values (hand.py,
from the 2025 Schedule D instructions), not against output captured now, and
each box C/F return must equal its A/D control on those lines.

Boundary (cf-loss-limit Decision 1): no 2025-to-2026 capital loss carryover is
published on any pinned return. ADR-0058 Decision 7 and ADR-0060 Decision 7
forbid publishing an amount carried into 2026; only the inbound 2024-to-2025
carryover (published as 0 here) exists.

Measured reason for the live marker: each run with page rendering costs several
seconds, above the fast-lane budget. Runs are memoised per worker process, so a
return is run once per worker that reads it; under parallel workers a return can
still run on two or three workers (review CFL-R1).
"""
from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/cf-loss-limit-evidence"

STATUSES = ("single", "married_filing_separately")
SHAPES = ("st", "lt", "both")  # box C only, box F only, box C plus F
SIZES = ("below", "at", "above")
CF_KEYS = [f"cf/{shape}/{status}/{size}" for status in STATUSES for shape in SHAPES for size in SIZES]
# One A/D control per status and shape at the over-limit size, and one at the limit.
AD_KEYS = [f"ad/{shape}/{status}/{size}" for status in STATUSES for shape in SHAPES for size in ("at", "above")]
COMPARED = ("schedule-d.line-7", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
            "form1040.line-7a", "form1040.line-15")
SIZE: dict[str, Callable[[int], int]] = {"below": lambda limit: limit // 2, "at": lambda limit: limit, "above": lambda limit: limit + 2000}
SPLIT: dict[str, Callable[[int], tuple[int, int]]] = {"st": lambda loss: (-loss, 0), "lt": lambda loss: (0, -loss),
         "both": lambda loss: (-(loss - loss // 2), -(loss // 2))}
BOX_LINES = {"cf": ("schedule-d.line-3", "schedule-d.line-10"), "ad": ("schedule-d.line-1a", "schedule-d.line-8a")}
# Symbols naming a carryover or 2026 that a return may publish: the two inbound
# 2024-to-2025 worksheets and the refund applied to 2026 tax; none is a loss carried to 2026.
ALLOWED_CARRY_SYMBOLS = {"capital-loss-carryover.short-term", "capital-loss-carryover.long-term",
                         "payments.line36-applied-to-2026"}


@lru_cache(maxsize=1)
def _cases() -> Any:
    evidence_loader.load(EVIDENCE / "hand.py", "cfl_t1_hand")
    return evidence_loader.load(EVIDENCE / "cases.py", "cfl_t1_cases")


@lru_cache(maxsize=None)
def _run(key: str) -> dict[str, Any]:
    run: dict[str, Any] = _cases().observe(key)
    assert "refusal" not in run and "error" not in run, (key, run)
    return run


def _hand(key: str) -> tuple[dict[str, Any], int, int]:
    route, shape, status, size = key.split("/")
    loss = SIZE[size](1500 if status == "married_filing_separately" else 3000)
    st, lt = SPLIT[shape](loss)
    hand = _cases().hand.values(status, st, lt)
    return hand, st, lt


@pytest.mark.parametrize("key", CF_KEYS + AD_KEYS)
def test_lines_match_hand_values(key: str) -> None:
    run = _run(key)
    hand, st, lt = _hand(key)
    route = key.split("/")[0]
    assert run["stop"] == "saturated" and not run["blocked_rules"] and not run["questions"]
    for line in COMPARED:
        got = run["lines"][line]
        # The engine publishes line 21 as the positive amount of the loss; the form shows it in parentheses.
        expected = -hand[line] if line == "schedule-d.line-21" else hand[line]
        assert got["value"] == expected, (key, line)
        assert got["disposition"] in ("published_value", "computed_zero"), (key, line)
    own_st, own_lt = BOX_LINES[route]
    other_st, other_lt = BOX_LINES["ad" if route == "cf" else "cf"]
    assert (run["lines"][own_st]["value"], run["lines"][own_lt]["value"]) == (st, lt)
    assert run["lines"][other_st]["value"] == 0 and run["lines"][other_lt]["value"] == 0


@pytest.mark.parametrize("key", [k for k in CF_KEYS if k.rsplit("/", 1)[1] != "below"])
def test_cf_equals_ad_control(key: str) -> None:
    run, control = _run(key), _run("ad/" + key.split("/", 1)[1])
    skip = {"schedule-d.line-1a", "schedule-d.line-3", "schedule-d.line-8a", "schedule-d.line-10"}
    assert {k: v for k, v in run["lines"].items() if k not in skip} == \
        {k: v for k, v in control["lines"].items() if k not in skip}
    for field in ("stop", "blocked_rules", "questions", "carryover_published"):
        assert run[field] == control[field], field
    # The only page difference is the attachment: Form 8949 for box C/F sales.
    assert run["page_attachments"]["f8949"] == "published"
    assert control["page_attachments"]["f8949"] == "guard_inapplicable"


@pytest.mark.parametrize("key", CF_KEYS + AD_KEYS)
def test_no_2026_carryover_published(key: str) -> None:
    """ADR-0058 and ADR-0060 Decision 7: nothing carried into 2026 is published, for any box."""
    run = _run(key)
    assert set(run["carry_or_2026_symbols"]) <= ALLOWED_CARRY_SYMBOLS, key
    # The inbound 2024-to-2025 carryover is "none" on these returns.
    assert run["carryover_published"] == {"capital-loss-carryover.short-term": 0,
                                          "capital-loss-carryover.long-term": 0}
    assert run["lines"]["schedule-d.line-6"]["value"] == 0 and run["lines"]["schedule-d.line-14"]["value"] == 0
