"""Track 1a probe — 2025 EIC Table with 1, 2, 3+ child columns.

Parses the 2025 EIC Table out of the ignored instruction text and checks a
formula built from divide-down, add, multiply, subtract, max, and half-up
round. Also writes a v2 parameter with the full eight columns. Run from the
repository root:

    python3 docs/phases/engine-breadth/milestones/eic-qualifying-children-evidence/table_probe.py

The source text stays under the ignored temp tree. This file records no
absolute path.
"""

from __future__ import annotations

import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SOURCE = REPO / "temp" / "tax-on-taxable-income" / "sources" / "i1040gi-2025.txt"
V1_PARAM = REPO / "packages" / "content" / "tax" / "2025" / "parameter.eic-table-2025.json"
V2_PARAM = REPO / "packages" / "content" / "tax" / "2025" / "parameter.eic-table-2025.v2.json"

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


def column_rows(children: int, status: str) -> list[dict[str, str | None]]:
    """One column of the printed table as range_lookup rows.

    Rows are "at least lower but less than upper". The first printed row is
    $1-$50. Each later row is $50 wide up to the band that holds the
    completed phase-out amount; that band ends at the completed amount and
    carries the table's footnote credit. A final open row from the completed
    amount pays $0, because range_lookup blocks on a miss.
    """
    completed = int(LIMITS[status][children][3])
    rows: list[dict[str, str | None]] = [
        {"lower": "1", "upper": "50", "value": str(table_credit(1, children, status))}
    ]
    band = 50
    while band + 50 <= completed:
        rows.append({"lower": str(band), "upper": str(band + 50),
                     "value": str(table_credit(band, children, status))})
        band += 50
    if band < completed:
        rows.append({"lower": str(band), "upper": str(completed),
                     "value": str(FOOTNOTES[(status, children)])})
    rows.append({"lower": str(completed), "upper": None, "value": "0"})
    return rows


def generate_v2_rows() -> dict[str, list[dict[str, str | None]]]:
    """The eight columns of the v2 parameter, keyed other-N and joint-N."""
    values: dict[str, list[dict[str, str | None]]] = {}
    for key_status, formula_status in (("other", "other"), ("joint", "mfj")):
        for children in range(4):
            values[f"{key_status}-{children}"] = column_rows(children, formula_status)
    return values


def write_v2_parameter() -> None:
    """Write the v2 parameter file."""
    v1_data = json.loads(V1_PARAM.read_text())
    v2_data = {
        "schema": "parameter-declaration.v1",
        "id": "tax.us.2025.parameter.eic-table-2025",
        "version": "v2",
        "scope": v1_data["scope"],
        "values": generate_v2_rows()
    }
    V2_PARAM.write_text(json.dumps(v2_data, indent=2) + "\n")


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
    col_counts = {}  # Track per-column counts

    for low, high, values in rows:
        for index, status in ((0, "other"), (4, "mfj")):
            for children in range(4):
                col_key = f"{status}-{children}"
                if col_key not in col_counts:
                    col_counts[col_key] = {"bands": 0, "matches": 0}

                published = values[index + children]
                col_counts[col_key]["bands"] += 1

                if isinstance(published, str):
                    # Star footnote
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
                    else:
                        col_counts[col_key]["matches"] += 1
                    continue

                # Numeric cell
                got = table_credit(low, children, status)
                if got != published:
                    mismatches.append(
                        f"{status} c{children} {low}-{high}: table {published} formula {got}"
                    )
                    if len(mismatches) > 30:
                        break
                else:
                    col_counts[col_key]["matches"] += 1
            if len(mismatches) > 30:
                break
        if len(mismatches) > 30:
            break

    print(f"bands={len(rows)} numeric_cells={sum(1 for l, h, v in rows for val in v if not isinstance(val, str))} star_cells={sum(1 for l, h, v in rows for val in v if isinstance(val, str))}")

    # Print per-column counts
    for status in ("other", "mfj"):
        for children in range(4):
            col_key = f"{status}-{children}"
            counts = col_counts[col_key]
            print(f"{col_key}: bands_checked={counts['bands']} matches={counts['matches']}")

    print(f"first={rows[0][0]} last={rows[-1][0]}-{rows[-1][1]}")
    if mismatches:
        print(f"mismatches={len(mismatches)}")
        for line in mismatches[:10]:
            print(line)
        return 1

    print("formula matches every numeric cell and every footnote band")

    # Write v2 parameter
    try:
        write_v2_parameter()
        print("v2 parameter written")
    except Exception as e:
        print(f"failed to write v2 parameter: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
