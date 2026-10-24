"""Write the 2025 no-child EIC Table parameter from the P0 probe.

The rows are the printed 0-child columns. Bands are at least `lower` and
less than `upper`, the same boundary `range_lookup` uses. The probe's
`table_credit` supplies each cell, including the starred band's footnote.
This generator does not read the ignored instruction text. The derived
numbers land in the parameter file.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/earned-income-credit-evidence/generate_eic_table_2025.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import probe

REPO = Path(__file__).resolve().parents[5]
OUT = REPO / "packages" / "content" / "tax" / "2025" / "parameter.eic-table-2025.json"

# Parameter column key, then the probe's status name. "joint" is the printed
# married-filing-jointly column. The probe calls that status "mfj".
COLUMNS = (("other", "other"), ("joint", "mfj"))

# Hand-checked cells already pinned by the no-child credit cases.
CHECKS = {
    ("other", 12000): 542,
    ("other", 14000): 389,
    ("other", 15000): 312,
    ("other", 19100): 0,
    ("other", 19103): 0,
    ("joint", 8000): 614,
    ("joint", 16000): 649,
    ("joint", 20000): 473,
    ("joint", 26200): 1,
    ("joint", 26213): 1,
}


def column_rows(probe_status: str) -> list[dict[str, str | None]]:
    """Printed rows for one 0-child column, then the completed-amount row.

    `range_lookup` misses by blocking, and it does not return 0. Worksheet A
    still looks up amounts at and above the completed phaseout, so the last
    row is that amount with an open upper and credit 0. Amounts below 1 are
    not a printed row; line 2 returns 0 before the lookup.
    """
    completed = int(probe.LIMITS[probe_status][0][3])
    rows: list[dict[str, str | None]] = []

    def add(lower: int, upper: int | None, sample: int) -> None:
        credit = probe.table_credit(sample, 0, probe_status)
        rows.append(
            {
                "lower": str(lower),
                "upper": None if upper is None else str(upper),
                "value": str(credit),
            }
        )

    add(1, 50, 1)
    low = 50
    while low + 50 <= completed:
        add(low, low + 50, low)
        low += 50
    if low < completed:
        add(low, completed, low)
    if probe.table_credit(completed, 0, probe_status) != 0:
        raise SystemExit(f"{probe_status} credit at {completed} is not 0")
    rows.append({"lower": str(completed), "upper": None, "value": "0"})
    return rows


def _check(probe_status: str, rows: list[dict[str, str | None]]) -> None:
    completed = int(probe.LIMITS[probe_status][0][3])
    if rows[-1]["upper"] is not None or int(str(rows[-1]["lower"])) != completed:
        raise SystemExit(f"{probe_status} final row is not [{completed}, none)")
    if rows[-1]["value"] != "0":
        raise SystemExit(f"{probe_status} final row credit is not 0")
    cursor = 1
    for row in rows[:-1]:
        lower = int(str(row["lower"]))
        upper = int(str(row["upper"]))
        value = int(str(row["value"]))
        if lower != cursor or lower >= upper:
            raise SystemExit(f"{probe_status} band gap at {lower}")
        for amount in (lower, upper - 1):
            got = probe.table_credit(amount, 0, probe_status)
            if got != value:
                raise SystemExit(f"{probe_status} {amount}: row {value} probe {got}")
        cursor = upper
    if cursor != completed:
        raise SystemExit(f"{probe_status} printed rows end at {cursor}, not {completed}")
    starred = rows[-2]
    if int(str(starred["value"])) != probe.FOOTNOTES[(probe_status, 0)]:
        raise SystemExit(f"{probe_status} starred band is not the footnote")


def parameter() -> dict[str, object]:
    values: dict[str, list[dict[str, str | None]]] = {}
    for column, probe_status in COLUMNS:
        rows = column_rows(probe_status)
        _check(probe_status, rows)
        values[column] = rows
    for (column, amount), expected in CHECKS.items():
        probe_status = dict(COLUMNS)[column]
        got = probe.table_credit(amount, 0, probe_status)
        if got != expected:
            raise SystemExit(f"check {column} {amount}: probe {got} expected {expected}")
    return {
        "schema": "parameter-declaration.v1",
        "id": "tax.us.2025.parameter.eic-table-2025",
        "version": "v1",
        "scope": {
            "tax_year": 2025,
            "jurisdiction": "US-federal",
            "family": "individual-income-tax",
            "effective_from": "2025-01-01",
        },
        "values": values,
    }


def main() -> int:
    document = parameter()
    OUT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    values = document["values"]
    if not isinstance(values, dict):
        raise SystemExit("parameter values are not a column map")
    counts = {key: len(rows) for key, rows in values.items()}
    print(f"wrote {OUT.name} rows={counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
