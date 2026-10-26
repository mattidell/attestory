"""P0 case table: Schedule 8812 lines 1-14 and line 19 for the other-dependent cases.

Synthetic inputs (``demo-*`` labels are the people; amounts are invented). The
arithmetic is the form's, not a rounding policy: line 10 rounds up to the next
$1,000 when it is more than zero and not a multiple of $1,000
(``f1040s8.txt:30-33``); line 11 is 5% of line 10 (exact, so no rounding applies).
Half-up rounding is used only where a percentage can leave a remainder. The
Schedule 3 credits on Worksheet A line 2 are absent by answer and enter as zero.

Run from any directory:

    python3 docs/phases/engine-breadth/milestones/other-dependents-credit-evidence/odc_case_table.py
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

CTC_PER_CHILD = 2200  # Schedule 8812 line 5 (f1040s8.txt:17-18)
ODC_PER_DEPENDENT = 500  # line 7 (f1040s8.txt:23)
THRESHOLD = {"joint": 400_000, "other": 200_000}  # line 9 (f1040s8.txt:25-27)


def half_up(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class Case:
    label: str
    status: str  # "joint" or "other"
    agi: int  # line 3 (line 1 plus 2a-2d, all zero here)
    tax: int  # Form 1040 line 18, used as Worksheet A line 1
    under17_ssn: int  # line 4
    odc: int  # line 6 (other dependents, including children who fail a test)


def compute(c: Case) -> dict[str, Optional[int]]:
    line5 = CTC_PER_CHILD * c.under17_ssn
    line7 = ODC_PER_DEPENDENT * c.odc
    line8 = line5 + line7
    excess = c.agi - THRESHOLD[c.status]
    if excess > 0 and excess % 1000:
        excess = (excess // 1000 + 1) * 1000  # line 10: next multiple of $1,000
    line10 = max(0, excess)
    line11 = half_up(Decimal(line10) * Decimal("0.05"))
    if line8 <= line11:
        return {"l5": line5, "l7": line7, "l8": line8, "l10": line10, "l11": line11,
                "l12": 0, "l13": c.tax, "l19": 0}
    line12 = line8 - line11
    line13 = c.tax  # Worksheet A line 5 with Schedule 3 credits absent (zero)
    return {"l5": line5, "l7": line7, "l8": line8, "l10": line10, "l11": line11,
            "l12": line12, "l13": line13, "l19": min(line12, line13)}


CASES: tuple[Case, ...] = (
    Case("K1 MFJ, one 17-year-old with SSN (ODC only)", "joint", 60_000, 3_000, 0, 1),
    Case("K2 single, 17-year-old with SSN and one child under 17", "other", 60_000, 3_000, 1, 1),
    Case("K3 single, child with ITIN only (ODC only)", "other", 60_000, 3_000, 0, 1),
    Case("K4 single, parent as qualifying relative only", "other", 60_000, 3_000, 0, 1),
    Case("K5 single, child under 17 and parent (cap at tax)", "other", 60_000, 2_000, 1, 1),
    Case("K6 single, two under 17 and one ODC (cap at tax)", "other", 60_000, 1_200, 2, 1),
    Case("K7 single, phase-out 210,000 (line 10 10,000)", "other", 210_000, 9_000, 2, 1),
    Case("K8 MFJ, phase-out 401,000 (line 10 1,000)", "joint", 401_000, 9_000, 1, 1),
    Case("K9 MFJ, phase-out 401,001 (line 10 2,000)", "joint", 401_001, 9_000, 1, 1),
    Case("K10 single, phase-out 300,000 (line 8 below line 11)", "other", 300_000, 9_000, 0, 1),
    Case("K11 single, AGI exactly 200,000 (no excess)", "other", 200_000, 9_000, 0, 1),
    Case("K12 single, two ODC dependents, no children", "other", 60_000, 3_000, 0, 2),
)


def main() -> None:
    print("| Case | Line 5 | Line 7 | Line 8 | Line 10 | Line 11 | Line 12 | Line 13 | Line 19 |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for c in CASES:
        r = compute(c)
        print(f"| {c.label} | {r['l5']:,} | {r['l7']:,} | {r['l8']:,} | {r['l10']:,} | "
              f"{r['l11']:,} | {r['l12']:,} | {c.tax:,} | {r['l19']:,} |")
    print()
    print("Refused, with no amount: a relative with gross income at or above $5,200; "
          "a dependent who is not a U.S. citizen, national or resident alien; a child "
          "aged 17 checked for the child tax credit (the box is wrong); a claimed "
          "dependent with no TIN answer (asked for every child).")


if __name__ == "__main__":
    main()
