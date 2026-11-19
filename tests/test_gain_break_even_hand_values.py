"""The gain-break-even hand-value function follows the 2025 instructions.

tests/test_gain_break_even_v96.py pins engine output to hand.py, so hand.py must
not itself be engine output. These synthetic cases restate the 2025 Tax Table,
the Form 8949 column (h) rule, the Schedule D routing and the Qualified Dividends
and Capital Gain Tax Worksheet as literal numbers worked by hand from the
instructions, independent of the engine.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

HAND = Path(__file__).resolve().parents[1] / ("docs/phases/engine-breadth/milestones/"
                                              "gain-break-even-evidence/hand.py")


def _hand() -> Any:
    return evidence_loader.load(HAND, "gbe_t1_hand_fast")


# (status, taxable income, Tax Table amount). Worked: the $50 row's midpoint taxed by
# the 2025 brackets, rounded to the dollar, e.g. single 5,000 row: 5,025 x 10% = 502.5 -> 503.
TABLE = [
    ("single", 5000, 503),
    ("single", 34250, 3875),    # 1,192.50 + (34,275 - 11,925) x 12% = 3,874.50 -> 3,875
    ("single", 51750, 6305),
    ("single", 54250, 6855),
    ("married_filing_jointly", 18500, 1853),   # 18,525 x 10%
    ("married_filing_jointly", 36000, 3846),
    ("married_filing_jointly", 38500, 4146),
]


@pytest.mark.parametrize("status,income,expected", TABLE)
def test_tax_table_rows(status: str, income: int, expected: int) -> None:
    assert _hand().tax_table(income, status) == expected


def _sale(path: str, term: str, **spec: float) -> tuple[str, str, dict[str, float]]:
    return (path, term, spec)


# (sales, status) -> (line 7, 15, 16, 1040 line 15, 1040 line 16, Form 8949 required)
CASES = [
    # short-term gain, wages 50,000, single: 70,000 - 15,750 = 54,250, Tax Table (line 7 > 0, 15 = 0)
    ([_sale("noncovered", "st", proceeds=25000, basis=5000)], "single", (20000, 0, 20000, 54250, 6855, True)),
    # long-term gain, single: worksheet, 4,760 (885 at 15% plus 3,875 on 34,250)
    ([_sale("covered", "lt", proceeds=25000, basis=5000)], "single", (0, 20000, 20000, 54250, 4760, False)),
    # long-term gain, joint: all 20,000 sits in the 0% band
    ([_sale("noncovered", "lt", proceeds=25000, basis=5000)], "married_filing_jointly",
     (0, 20000, 20000, 38500, 1853, True)),
    # break-even: line 16 of 0, wages only 34,250 taxable
    ([_sale("no1099b", "lt", proceeds=8000, basis=8000)], "single", (0, 0, 0, 34250, 3875, True)),
    # code B: reported basis 6,000 corrected to 5,000 -> (g) 1,000, (h) = 25,000 - 6,000 + 1,000
    ([_sale("codeb", "st", proceeds=25000, basis=6000, corrected=5000)], "single", (20000, 0, 20000, 54250, 6855, True)),
    # code W full disallowance: loss 500, (g) 500, (h) 0
    ([_sale("w", "st", proceeds=1000, basis=1500, wash=500)], "single", (0, 0, 0, 34250, 3875, True)),
    # mixed: lt gain 20,000 (box E) less st loss 3,000 (box C): worksheet on 17,000
    ([_sale("noncovered", "lt", proceeds=25000, basis=5000), _sale("no1099b", "st", proceeds=1000, basis=4000)],
     "single", (-3000, 20000, 17000, 51250, 4310, True)),
    # mixed: line 15 a loss -> Tax Table on line 15
    ([_sale("codeb", "st", proceeds=25000, basis=6000, corrected=5000), _sale("w", "lt", proceeds=1000, basis=4000, wash=500)],
     "single", (20000, -2500, 17500, 51750, 6305, True)),
]


@pytest.mark.parametrize("sales,status,expected", CASES)
def test_values_follow_instructions(sales: list[tuple[str, str, dict[str, float]]], status: str,
                                    expected: tuple[int, int, int, int, int, bool]) -> None:
    got = _hand().values(sales, status)
    l7, l15, l16, f15, f16, required = expected
    assert (got["schedule-d.line-7"], got["schedule-d.line-15"], got["schedule-d.line-16"]) == (l7, l15, l16)
    assert got["form1040.line-7a"] == l16 and got["form1040.line-15"] == f15 and got["form1040.line-16"] == f16
    assert got["form8949_required"] is required


def test_form_8949_parts_and_routes() -> None:
    hand = _hand()
    codeb = hand.values([_sale("codeb", "st", proceeds=25000, basis=6000, corrected=5000)], "single")
    assert codeb["form8949_parts"] == {"box-a-code-b-proceeds": 25000, "box-a-code-b-basis": 6000,
                                      "box-a-code-b-adjustment": 1000}
    assert codeb["schedule-d.line-1b"] == 20000
    wash = hand.values([_sale("w", "st", proceeds=1000, basis=1500, wash=500)], "single")
    assert wash["form8949_parts"] == {"box-a-proceeds": 1000, "box-a-basis": 1500, "box-a-adjustment": 500}
    assert wash["schedule-d.line-1b"] == 0
    # Box B/E -> 2/9, box C/F -> 3/10, covered with basis reported -> 1a/8a with no Form 8949.
    assert hand.values([_sale("noncovered", "st", proceeds=9, basis=4)], "single")["schedule-d.line-2"] == 5
    assert hand.values([_sale("no1099b", "lt", proceeds=9, basis=4)], "single")["schedule-d.line-10"] == 5
    covered = hand.values([_sale("covered", "lt", proceeds=9, basis=4)], "single")
    assert covered["schedule-d.line-8a"] == 5 and covered["form8949_parts"] == {}


def test_qdcg_worksheet_lines() -> None:
    hand = _hand()
    single = hand.values([_sale("covered", "lt", proceeds=25000, basis=5000)], "single")["qdcg"]
    # taxable 54,250, gain 20,000: line 5 = 34,250; line 9 = 48,350 - 34,250 = 14,100;
    # line 17 = 5,900 (20,000 - 14,100); line 18 = 15% = 885; line 22 = Tax Table(34,250); line 24 = Tax Table(54,250).
    assert (single["line-5"], single["line-9"], single["line-17"], single["line-18"], single["line-22"],
            single["line-24"]) == (34250, 14100, 5900, 885, 3875, 6855)
    # joint: taxable 38,500, line 5 = 18,500; line 9 = 20,000 (all gain at 0%); lines 17, 18 = 0.
    joint = hand.values([_sale("covered", "lt", proceeds=25000, basis=5000)], "married_filing_jointly")["qdcg"]
    assert (joint["line-5"], joint["line-9"], joint["line-17"], joint["line-18"], joint["line-22"]) == \
        (18500, 20000, 0, 0, 1853)
    # 17,000 net gain: taxable 51,250; line 9 = 14,100; line 17 = 2,900; 15% = 435; total 435 + 3,875 = 4,310.
    mixed = hand.values([_sale("noncovered", "lt", proceeds=25000, basis=5000),
                         _sale("no1099b", "st", proceeds=1000, basis=4000)], "single")
    assert (mixed["qdcg"]["line-17"], mixed["qdcg"]["line-18"], mixed["form1040.line-16"]) == (2900, 435, 4310)
    # No worksheet when line 15 or 16 is zero or less (short-term gain, break-even).
    assert "qdcg" not in hand.values([_sale("noncovered", "st", proceeds=9, basis=4)], "single")
    assert "qdcg" not in hand.values([_sale("noncovered", "lt", proceeds=9, basis=9)], "single")
