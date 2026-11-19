"""Gains and exact break-even sales reach Form 8949 and Schedule D, on published core v96.

A 27-return subset of the gain-break-even P0 returns (docs/phases/engine-breadth/
milestones/gain-break-even-evidence) runs through the real live_coordinate_run and
the saved page: 22 single-filer returns (a gain and a break-even on covered with
basis reported as the control, code W, code B, noncovered and no Form 1099-B, short
and long term, plus the code W proceeds-equal-basis return, both terms), one joint
long-term gain (all gain at the 0% rate), the three mixed returns netting to a
gain, and one code W gain probe. Each ordinary return is asserted against the P0
hand values (hand.py, from the 2025 Form 8949, Schedule D and Form 1040
instructions), never against output captured now: Form 8949 part totals and
whether it is required, Schedule D lines 1a-16, Form 1040 lines 7a, 15 and 16, the
preferential base and, where lines 15 and 16 are both gains, the Qualified
Dividends and Capital Gain Tax Worksheet lines.

The probe is the one bound: a code W row with a positive box 1g amount on a gain
blocks (ADR-0062 Decision 2, mechanism ADR-0066) and publishes no line 16 amount.

Every test is one return, so a return runs once; there is no shared memo to lose
across workers. Measured cost: each run with page rendering costs several seconds,
above the fast-lane budget, hence the live marker. The subset is 27 coordinator
runs under `-n auto`.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/gain-break-even-evidence"

PATHS = ("covered", "w", "codeb", "noncovered", "no1099b")
# 20 single returns: every path, both terms, a gain and a break-even; the w even
# shape is a loss of 500 fully disallowed, so (h) is 0.
SINGLE = [f"{p}/{t}/{s}/single" for p in PATHS for t in ("st", "lt") for s in ("gain", "even")]
# Code W proceeds equal basis with box 1g 0 (the plain break-even): 2 more, 22 in all.
SINGLE += [f"w/{t}/even-plain/single" for t in ("st", "lt")]
JOINT = ["noncovered/lt/gain/married_filing_jointly"]
MIXED = [f"mixed/{m}/single" for m in ("lt-gain", "st-gain", "three")]
ORDINARY = SINGLE + JOINT + MIXED
PROBE = "w/st/probe-gain/single"

PAGE_LINES = tuple(f"schedule-d.line-{n}" for n in ("1a", "1b", "2", "3", "6", "7", "8a", "8b", "9", "10", "13", "14",
                                                   "15", "16")) + ("form1040.line-7a", "form1040.line-15",
                                                                   "form1040.line-16")
PUBLISHED_OK = ("published_value", "computed_zero", "closure_backed_zero")
WORKSHEET = {"line-5": "qdcg-worksheet.line-5", "line-9": "qdcg-worksheet.line-9",
             "line-17": "qdcg-worksheet.line-17", "line-18": "qdcg-worksheet.line-18",
             "line-22": "qdcg-worksheet.line-22", "line-24": "qdcg-worksheet.line-24"}


@lru_cache(maxsize=1)
def _cases() -> Any:
    evidence_loader.load(EVIDENCE / "hand.py", "gbe_t1_hand")
    return evidence_loader.load(EVIDENCE / "cases.py", "gbe_t1_cases")


@lru_cache(maxsize=1)
def _hand() -> Any:
    _cases()
    return evidence_loader.load(EVIDENCE / "hand.py", "gbe_t1_hand")


@lru_cache(maxsize=None)
def _run(key: str) -> dict[str, Any]:
    run: dict[str, Any] = _cases().observe(key)
    assert "refusal" not in run and "error" not in run, (key, run)
    return run


def test_subset_is_27_returns() -> None:
    assert (len(SINGLE), len(JOINT), len(MIXED), 1) == (22, 1, 3, 1)
    assert len(set(ORDINARY + [PROBE])) == 27
    # The never-run cell: no Form 1099-B, long-term, break-even.
    assert "no1099b/lt/even/single" in SINGLE


@pytest.mark.parametrize("key", ORDINARY)
def test_return_matches_hand_values(key: str) -> None:
    run = _run(key)
    status = key.split("/")[-1]
    want = _hand().values(_cases().case_sales(key), status)
    assert run["stop"] == "saturated" and not run["blocked_rules"] and not run["questions"], key
    for line in PAGE_LINES:
        got = run["lines"][line]
        assert got["value"] == want[line], (key, line)
        assert got["disposition"] in PUBLISHED_OK, (key, line)
    # A covered-only return publishes no Form 8949 itemisation at all.
    f8949 = run["attachment_parts"].get("form8949") or {}
    assert (f8949.get("parts") or {}) == want["form8949_parts"], key
    assert bool(f8949.get("required")) is want["form8949_required"], key
    # Form 8949 is not an attachment when every sale is covered with basis reported.
    assert run["attachments"]["f8949"] == ("published" if want["form8949_required"] else "guard_inapplicable"), key
    # A break-even sale still files Schedule D (line 16 of 0).
    assert run["attachments"]["schedule-d"] == "published", key
    line15, line16 = want["schedule-d.line-15"], want["schedule-d.line-16"]
    assert run["published"]["capital-gains.selected-preferential-base"] == (min(line15, line16) if line15 > 0 else 0), key
    if "qdcg" in want:
        for name, symbol in WORKSHEET.items():
            assert abs(float(run["published"][symbol]) - float(want["qdcg"][name])) < 0.005, (key, name)


def test_code_w_gain_probe_blocks() -> None:
    """ADR-0062 Decision 2 via ADR-0066: box 1g above 0 on a gain row blocks; no line 16 amount."""
    run = _run(PROBE)
    assert ["tax.us.2025.f1099b.covered-w-st.member-validation.synthesized", "DEPENDENCY_INVALID"] in run["blocked_rules"]
    for line in ("schedule-d.line-16", "form1040.line-7a", "form1040.line-16"):
        assert run["lines"][line] == {"disposition": "blocked", "value": None}, line
    assert "schedule-d.line-16" not in run["published"]
    assert run["questions"] == []
    assert run["attachments"]["schedule-d"] == "blocked"
    # The block's code is declared on the family content (read only; the page names it).
    family = (REPO / "packages/content/tax/2025/family.f1099b-covered-w-st.v2.json")
    assert "CODE_W_ON_GAIN" in family.read_text(encoding="utf-8")
