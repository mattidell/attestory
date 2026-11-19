"""Hand values for the gain-break-even P0 cases, from the 2025 IRS sources.

Sources (local copies of the 2025 Instructions for Form 8949, i8949--2025;
Instructions for Schedule D, i1040sd--2025; and Instructions for Form 1040,
i1040gi-2025; text line numbers are of a plain-text extraction of those PDFs,
cited in p0.md):

- Form 8949 column (h) = (d) - (e), then the column (g) adjustment
  (i8949 "Column (h)", text lines 717-735). Code B: (e) is the basis the
  Form 1099-B shows and (g) is reported minus correct basis (i8949 Example 4,
  lines 736-747). Code W: (g) is the disallowed wash-sale loss.
- Box A/D with an adjustment -> Schedule D line 1b/8b; box B/E -> 2/9; box
  C/F -> 3/10; covered, basis reported, no adjustment -> 1a/8a (i1040sd
  "Lines 1a and 8a" and "Lines 1b, 2, 3, 8b, 9, and 10", text lines 835-880).
- Schedule D line 7 = lines 1a-6, line 15 = lines 8a-14, line 16 = 7 + 15;
  a gain or zero on line 16 goes to Form 1040 line 7a (Schedule D Part III).
- Form 1040 line 16: the Qualified Dividends and Capital Gain Tax Worksheet
  when Schedule D lines 15 and 16 are both more than zero (i1040gi "Line 16",
  text lines 2375-2385; worksheet text lines 2455-2510); otherwise the Tax
  Table (i1040gi 2025 Tax Table, text lines 4690-5700). tax_table() taxes a
  $50 band at its midpoint by the 2025 rate brackets and rounds to the
  dollar; checked against every Tax Table row from 3,000 to 99,950, single
  and married filing jointly (1,940 rows, no difference).

Every case is the harness wage return (wages 50,000, standard deduction, no
qualified dividends, no other Schedule D source). This module computes from
the inputs only, never from a run result.
"""
from __future__ import annotations

import math
from typing import Any

WAGES = 50000
STANDARD = {"single": 15750, "married_filing_jointly": 31500}
# 2025 rate brackets (i1040gi Tax Computation Worksheet, text lines 5754-5815); enough for these cases.
BRACKETS = {
    "single": ((11925, 0.10), (48475, 0.12), (103350, 0.22), (197300, 0.24)),
    "married_filing_jointly": ((23850, 0.10), (96950, 0.12), (206700, 0.22), (394600, 0.24)),
}
QDCG_LINE6 = {"single": 48350, "married_filing_jointly": 96700}
QDCG_LINE13 = {"single": 533400, "married_filing_jointly": 600050}

# (Form 8949 box for st, for lt, Schedule D line for st, for lt). Covered = no Form 8949.
ROUTE = {
    "covered": (None, None, "1a", "8a"),
    "w": ("a", "d", "1b", "8b"),
    "codeb": ("a-code-b", "d-code-b", "1b", "8b"),
    "noncovered": ("b", "e", "2", "9"),
    "no1099b": ("c", "f", "3", "10"),
}
ST_LINES = ("1a", "1b", "2", "3")
LT_LINES = ("8a", "8b", "9", "10")


def schedule_tax(income: float, status: str) -> float:
    tax, low = 0.0, 0.0
    for top, rate in BRACKETS[status]:
        if income <= low:
            break
        tax += (min(income, top) - low) * rate
        low = top
    return tax


def tax_table(income: int, status: str) -> int:
    """Tax Table for 3,000 <= income < 100,000: the $50 band's midpoint, rounded half up."""
    assert 3000 <= income < 100000, income
    mid = math.floor(income / 50) * 50 + 25
    return int(math.floor(schedule_tax(mid, status) + 0.5))


def row(path: str, spec: dict[str, Any]) -> dict[str, float]:
    d, e = spec["proceeds"], spec["basis"]
    if path == "codeb":
        g = spec["basis"] - spec["corrected"] + spec.get("wash", 0.0)
    else:
        g = spec.get("wash", 0.0)
    return {"d": d, "e": e, "g": g, "h": d - e + g}


def values(sales: list[tuple[str, str, dict[str, Any]]], status: str) -> dict[str, Any]:
    lines = {n: 0 for n in ST_LINES + LT_LINES}
    parts: dict[str, float] = {}
    for path, term, spec in sales:
        r = row(path, spec)
        box_st, box_lt, line_st, line_lt = ROUTE[path]
        box, line = (box_st, line_st) if term == "st" else (box_lt, line_lt)
        lines[line] += r["h"]
        if box is not None:
            for col, part in (("d", "proceeds"), ("e", "basis"), ("g", "adjustment")):
                key = f"box-{box}-{part}"
                parts[key] = parts.get(key, 0) + r[col]
    out: dict[str, Any] = {f"schedule-d.line-{n}": int(v) for n, v in lines.items()}
    out["schedule-d.line-6"] = out["schedule-d.line-13"] = out["schedule-d.line-14"] = 0
    line7 = sum(lines[n] for n in ST_LINES)
    line15 = sum(lines[n] for n in LT_LINES)
    line16 = line7 + line15
    assert line16 >= 0, "these cases are gains or break-even overall"
    out.update({"schedule-d.line-7": int(line7), "schedule-d.line-15": int(line15), "schedule-d.line-16": int(line16),
                "form1040.line-7a": int(line16)})
    taxable = max(WAGES + int(line16) - STANDARD[status], 0)
    out["form1040.line-15"] = taxable
    table = tax_table(taxable, status)
    if line15 > 0 and line16 > 0:
        w1 = taxable
        w3 = int(min(line15, line16))
        w4 = w3                                   # line 2 (qualified dividends) is 0
        w5 = max(w1 - w4, 0)
        w7 = min(w1, QDCG_LINE6[status])
        w8 = min(w5, w7)
        w9 = w7 - w8
        w10 = min(w1, w4)
        w12 = w10 - w9
        w14 = min(w1, QDCG_LINE13[status])
        w15 = w5 + w9
        w16 = max(w14 - w15, 0)
        w17 = min(w12, w16)
        w18 = w17 * 0.15
        w20 = w10 - (w9 + w17)
        w21 = w20 * 0.20
        w22 = tax_table(w5, status)
        w23 = w18 + w21 + w22
        w24 = table
        out["qdcg"] = {"line-3": w3, "line-5": w5, "line-9": w9, "line-17": w17, "line-18": w18, "line-22": w22,
                       "line-24": w24}
        out["form1040.line-16"] = int(round(min(w23, w24)))
        out["tax_path"] = "qdcg-worksheet"
    else:
        out["form1040.line-16"] = table
        out["tax_path"] = "tax-table"
    out["form8949_parts"] = {k: int(v) for k, v in parts.items() if v}
    out["form8949_required"] = bool(parts)
    return out
