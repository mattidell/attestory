"""P0 case table: Schedule 8812 worked through for the plan's cases.

Pure arithmetic over the lines of Schedule 8812 (2025) as printed in the
downloaded form and instructions. Every line number below is the form's own
line. Case inputs (tax, earned income, AGI, child counts) are synthetic and are
not source figures. Run from anywhere:

    python3 docs/phases/engine-breadth/milestones/child-tax-credit-evidence/ctc_case_table.py
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


CTC_PER_CHILD = 2200  # Sch 8812 line 5 (text line 18: "Multiply line 4 by $2,200")
ODC_PER_DEPENDENT = 500  # Sch 8812 line 7 (text line 23)
ACTC_PER_CHILD = 1700  # Sch 8812 line 16b (text line 51)
EARNED_THRESHOLD = 2500  # Sch 8812 line 19 (text line 59)
ACTC_RATE = 0.15  # Sch 8812 line 20 (text line 60)
PHASE_OUT_SINGLE = 200_000  # Sch 8812 line 9 (text lines 25-27)
PHASE_OUT_MFJ = 400_000  # Sch 8812 line 9 (text line 26)
PHASE_RATE = 0.05  # Sch 8812 line 11 (text line 35)


@dataclass
class Case:
    label: str
    joint: bool
    agi: int  # Sch 8812 line 1 = Form 1040 line 11a; line 3 = line 1 (no 2a-2c)
    tax: int  # Form 1040 line 16 = line 18 (no line 17); Credit Limit Worksheet A line 1
    earned: int  # Sch 8812 line 18a (earned income, no combat pay)
    under17: int  # qualifying children under 17 with a valid SSN (line 4)
    other_dependents: int = 0  # line 6 (ODC) -- outside the slice when > 0
    no_ssn_children: int = 0  # children who would be ODC only -- outside the slice


def half_up(value: float) -> int:
    """Whole dollars, halves up, as the engine's rounding convention does."""
    return int(Decimal(str(value)).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def phase_out_line10(agi: int, joint: bool) -> int:
    """Line 10: AGI above the threshold, rounded up to the next $1,000 (text lines 32-34)."""
    threshold = PHASE_OUT_MFJ if joint else PHASE_OUT_SINGLE
    excess = agi - threshold
    if excess <= 0:
        return 0
    if excess % 1000 == 0:
        return excess
    return (excess // 1000 + 1) * 1000


def compute(c: Case) -> dict[str, object]:
    out: dict[str, object] = {"label": c.label}
    if c.other_dependents or c.no_ssn_children:
        out["status"] = "REFUSED: other dependent (ODC) outside the slice"
        return out
    if c.under17 == 0:
        out["status"] = "no CTC children; line 19 and 28 are $0"
        out.update(line19=0, line28=0, total=0)
        return out
    l8 = CTC_PER_CHILD * c.under17  # line 5 + line 7 (line 7 = 0)
    l10 = phase_out_line10(c.agi, c.joint)
    l11 = half_up(l10 * PHASE_RATE)
    if l8 <= l11:
        out["status"] = "line 12 No: no CTC, ODC or ACTC"
        out.update(line8=l8, line11=l11, line19=0, line28=0, total=0)
        return out
    l12 = l8 - l11
    l13 = c.tax  # Credit Limit Worksheet A: line 1 = tax; lines 2-5 = tax (no Sch 3 credits)
    l14 = min(l12, l13)
    out.update(line8=l8, line10=l10, line11=l11, line12=l12, line13=l13, line14=l14, line19=l14)
    l16a = l12 - l14
    if l16a == 0:
        out.update(line16a=0, line28=0, total=l14, status="no ACTC: line 16a is zero")
        return out
    l16b = ACTC_PER_CHILD * c.under17
    l17 = min(l16a, l16b)
    l19 = max(c.earned - EARNED_THRESHOLD, 0)
    l20 = half_up(l19 * ACTC_RATE)
    out.update(line16a=l16a, line16b=l16b, line17=l17, line19_earned=l19, line20=l20)
    if c.under17 >= 3 and l20 < l17:
        out["status"] = "REFUSED: Part II-B needs Sch 8812 lines 21-24 (W-2 boxes 4 and 6), not recorded"
        out.update(line28=None, total=None)
        return out
    l28 = min(l17, l20)
    out.update(line28=l28, total=l14 + l28, status="computed")
    return out


CASES = [
    Case("C1 single, 1 child, tax above credit", False, 60_000, 3_000, 30_000, 1),
    Case("C2 single, 1 child, tax below credit, ACTC ramp", False, 60_000, 500, 10_000, 1),
    Case("C3 single, 2 children, tax 1,000, earned 20,000", False, 60_000, 1_000, 20_000, 2),
    Case("C4 single, 1 child, earned 2,000 (no ACTC)", False, 30_000, 500, 2_000, 1),
    Case("C5 single, 1 child, earned exactly 2,500", False, 30_000, 500, 2_500, 1),
    Case("C6 single, AGI 210,000, 2 children (phase-out)", False, 210_000, 9_000, 60_000, 2),
    Case("C7 single, AGI 200,500 (rounds to 201,000)", False, 200_500, 9_000, 60_000, 1),
    Case("C8 MFJ, AGI 401,000, 1 child", True, 401_000, 9_000, 60_000, 1),
    Case("C9 MFJ, AGI 410,000, 1 child (partly phased)", True, 410_000, 9_000, 60_000, 1),
    Case("C10 MFJ, 3 children, tax 0, earned 20,000 (II-B)", True, 60_000, 0, 20_000, 3),
    Case("C11 MFJ, 3 children, tax 2,000, earned 30,000 (II-B)", True, 60_000, 2_000, 30_000, 3),
    Case("C12 MFJ, 3 children, tax 2,000, earned 40,000 (line 20 >= 17)", True, 60_000, 2_000, 40_000, 3),
    Case("C13 MFJ, 3 children, tax 0, earned 60,000 (line 20 above line 17)", True, 60_000, 0, 60_000, 3),
    Case("C14 single, 1 child claimed, aged 17 (ODC, refused)", False, 60_000, 3_000, 30_000, 0, other_dependents=1),
    Case("C15 single, 1 child, no SSN (ODC, refused)", False, 60_000, 3_000, 30_000, 1, no_ssn_children=1),
]


def main() -> int:
    for c in CASES:
        r = compute(c)
        print(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
