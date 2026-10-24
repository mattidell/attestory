"""P0 probe — 2025 EIC Table as a formula (investigation only).

Parses the 2025 EIC Table out of the ignored instruction text and checks a
formula built from divide-down, add, multiply, subtract, max, and half-up
round. Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/earned-income-credit-evidence/probe.py

The source text stays under the ignored temp tree. This file records no
absolute path.
"""

from __future__ import annotations

import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SOURCE = REPO / "temp" / "tax-on-taxable-income" / "sources" / "i1040gi-2025.txt"

# Statutory percentages are not printed in Rev. Proc. 2024-40 or the Form 1040
# instructions. These are the rates that reproduce the Rev. Proc. maximum
# credits and the table. Credit rate, then phaseout rate.
RATES = {
    0: (Decimal("0.0765"), Decimal("0.0765")),
    1: (Decimal("0.34"), Decimal("0.1598")),
    2: (Decimal("0.40"), Decimal("0.2106")),
    3: (Decimal("0.45"), Decimal("0.2106")),
}

# Rev. Proc. 2024-40 §2.06. Order: earned income amount, maximum credit,
# phaseout start, completed phaseout. "other" is every status except MFJ.
LIMITS = {
    "other": {
        0: (Decimal(8490), Decimal(649), Decimal(10620), Decimal(19104)),
        1: (Decimal(12730), Decimal(4328), Decimal(23350), Decimal(50434)),
        2: (Decimal(17880), Decimal(7152), Decimal(23350), Decimal(57310)),
        3: (Decimal(17880), Decimal(8046), Decimal(23350), Decimal(61555)),
    },
    "mfj": {
        0: (Decimal(8490), Decimal(649), Decimal(17730), Decimal(26214)),
        1: (Decimal(12730), Decimal(4328), Decimal(30470), Decimal(57554)),
        2: (Decimal(17880), Decimal(7152), Decimal(30470), Decimal(64430)),
        3: (Decimal(17880), Decimal(8046), Decimal(30470), Decimal(68675)),
    },
}

# Footnote credit for the band that contains the completed phaseout, for an
# amount that is still below that amount. Keyed by (status, children) to the
# published footnote dollars. i1040gi-2025.txt lines cited in the evidence.
FOOTNOTES = {
    ("other", 0): 0,
    ("mfj", 0): 1,
    ("other", 1): 3,
    ("other", 2): 1,
    ("mfj", 1): 0,
    ("other", 3): 1,
    ("mfj", 2): 3,
    ("mfj", 3): 3,
}

NUM = r"\d{1,3}(?:,\d{3})*"
CELL = r"(?:\d{1,3}(?:,\d{3})*|\*{1,3})"
ROW = re.compile(
    rf"({NUM})\s+({NUM})\s+"
    + r"\s+".join([f"({CELL})"] * 8)
)


def money(text: str) -> int:
    return int(text.replace(",", ""))


def cell(text: str) -> int | str:
    if text.startswith("*"):
        return text
    return money(text)


def half_up(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def table_credit(amount: int, children: int, status: str) -> int:
    """Credit the 2025 EIC Table shows for this dollar amount.

    amount is the worksheet figure being looked up. status is "mfj" or "other".
    """
    earned_at, maximum, phaseout_at, completed = LIMITS[status][children]
    credit_rate, phaseout_rate = RATES[children]
    if amount < 1 or Decimal(amount) >= completed:
        return 0
    band = (Decimal(amount) // Decimal(50)) * Decimal(50)
    band_end = band + Decimal(50)
    midpoint = band + Decimal(25)
    # The published cell is the statutory credit at one point in the band.
    # That point is the $50 midpoint, except where the band crosses a corner
    # of the credit (the earned-income amount, the phaseout threshold, or the
    # completed phaseout) and the midpoint is still on the other side of it.
    if band < completed < band_end:
        point = (band + completed) / Decimal(2)
    elif band <= earned_at < band_end and midpoint < earned_at:
        point = earned_at
    elif band < phaseout_at < midpoint:
        point = phaseout_at
    else:
        point = midpoint
    if point >= earned_at:
        phased_in = int(maximum)
    else:
        phased_in = min(half_up(point * credit_rate), int(maximum))
    if point <= phaseout_at:
        return phased_in
    reduced = maximum - phaseout_rate * (point - phaseout_at)
    return max(0, half_up(reduced))


def load_rows() -> list[tuple[int, int, list[int | str]]]:
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    start = text.find("2025 Earned Income Credit (EIC) Table")
    end = text.find("credit for other dependents, or the addi", start)
    if start < 0 or end < 0:
        raise SystemExit("EIC table region not found in the instruction text")
    rows: list[tuple[int, int, list[int | str]]] = []
    for match in ROW.finditer(text[start:end]):
        low = money(match.group(1))
        high = money(match.group(2))
        # Every band is $50 wide except the first, which the table prints as
        # "at least 1 but less than 50" because a $0 lookup is not a row.
        if high - low != 50 and (low, high) != (1, 50):
            continue
        values = [cell(match.group(i)) for i in range(3, 11)]
        rows.append((low, high, values))
    rows.sort(key=lambda item: item[0])
    return rows


def main() -> int:
    rows = load_rows()
    if len(rows) < 1000:
        print(f"parsed only {len(rows)} bands; layout parse failed")
        return 1
    lows = [low for low, _, _ in rows]
    if len(lows) != len(set(lows)):
        print("duplicate bands")
        return 1
    expected = [1] + list(range(50, lows[-1] + 1, 50))
    if lows != expected:
        missing = [n for n in expected if n not in set(lows)]
        extra = [n for n in lows if n not in set(expected)]
        print(f"band gaps missing={missing[:10]} extra={extra[:10]}")
        return 1

    mismatches: list[str] = []
    numeric = 0
    stars = 0
    for low, high, values in rows:
        for index, status in ((0, "other"), (4, "mfj")):
            for children in range(4):
                published = values[index + children]
                if isinstance(published, str):
                    stars += 1
                    completed = int(LIMITS[status][children][3])
                    if not (low <= completed < high):
                        mismatches.append(
                            f"star {published} at {low}-{high} {status} c{children} "
                            f"does not contain completed {completed}"
                        )
                        continue
                    expect = FOOTNOTES[(status, children)]
                    got_low = table_credit(low, children, status)
                    got_last = table_credit(completed - 1, children, status)
                    got_end = table_credit(completed, children, status)
                    if (got_low, got_last, got_end) != (expect, expect, 0):
                        mismatches.append(
                            f"footnote {status} c{children} [{low}, {completed}) "
                            f"published {expect}, formula {got_low}/{got_last}, "
                            f"at completed {got_end}"
                        )
                    continue
                numeric += 1
                got = table_credit(low, children, status)
                if got != published:
                    mismatches.append(
                        f"{status} c{children} {low}-{high}: table {published} formula {got}"
                    )
                    if len(mismatches) > 30:
                        break
            if len(mismatches) > 30:
                break
        if len(mismatches) > 30:
            break

    print(f"bands={len(rows)} numeric_cells={numeric} star_cells={stars}")
    print(f"first={rows[0][0]} last={rows[-1][0]}-{rows[-1][1]}")
    if mismatches:
        print(f"mismatches={len(mismatches)}")
        for line in mismatches[:30]:
            print(line)
        return 1
    print("formula matches every numeric cell and every footnote band")

    # Representative rows the evidence cites: first band, a half-up .5 case,
    # the earned-income-amount band, the phaseout-start band, a phaseout row,
    # and the last nonzero band of each column.
    samples = [1, 50, 100, 2450, 8450, 8500, 10600, 10650, 12700, 15000, 17850, 19100, 23350, 26200, 50400, 57300, 57550, 61550, 64400, 68650]
    print("samples:")
    for amount in samples:
        cells = [
            table_credit(amount, children, status)
            for status in ("other", "mfj")
            for children in range(4)
        ]
        print(f"  {amount}: {cells}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
