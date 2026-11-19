"""Hand values for the cf-loss-limit P0 cases, from the 2025 IRS sources.

Sources (local copies of the 2025 Instructions for Schedule D, i1040sd--2025,
and the 2025 Form 1040 instructions, i1040gi-2025; text line numbers refer
to a plain-text extraction of those PDFs, cited in p0.md):

- Capital losses are deductible up to gains plus $3,000 ($1,500 if married
  filing separately) — i1040sd "Capital Losses", text lines 186-195.
- Line 21: a carryover to 2026 exists when line 16 is a loss and that loss
  is more than the line 21 loss, or Form 1040 line 15 would be below zero;
  it is figured with the Capital Loss Carryover Worksheet — i1040sd
  "Line 21", text lines 1056-1068.
- Capital Loss Carryover Worksheet, lines 1-13 — i1040sd text lines
  789-822. The 2025 instructions print it for 2024 -> 2025; the same
  worksheet with 2025 amounts gives 2025 -> 2026 (the Line 21 text says
  the 2026 instructions carry it; Pub. 550 lets the filer figure it now).

Every case is one W-2 wage return (wages 50,000) plus sales; no other
Schedule D source and no inbound carryover. This module computes from the
inputs only, never from a run result.
"""
from __future__ import annotations

from typing import Any

WAGES = 50000
LIMIT = {"married_filing_separately": 1500}
# 2025 standard deduction by status (i1040gi, standard deduction chart).
STANDARD = {"single": 15750, "married_filing_separately": 15750, "married_filing_jointly": 31500,
            "qualifying_surviving_spouse": 31500, "head_of_household": 23625}


def values(status: str, st: int, lt: int) -> dict[str, Any]:
    """st / lt are the short- and long-term net gain or loss (column (h) totals)."""
    line7 = st                       # Sch D line 7: net short-term (lines 1a-6)
    line15 = lt                      # Sch D line 15: net long-term (lines 8a-14)
    line16 = line7 + line15          # Sch D line 16: combine 7 and 15
    limit = LIMIT.get(status, 3000)
    line21 = -min(-line16, limit) if line16 < 0 else None   # Sch D line 21: smaller loss
    line7a = line21 if line16 < 0 else line16                # Form 1040 line 7a
    f1040_line15 = max(WAGES + line7a - STANDARD[status], 0)
    raw_line15 = WAGES + line7a - STANDARD[status]           # before the zero floor
    # Carryover Worksheet with 2025 amounts (i1040sd lines 789-822).
    carry_st = carry_lt = 0
    if line21 is not None and (-line16 > -line21 or raw_line15 < 0):
        w1 = raw_line15
        w2 = -line21
        w3 = max(w1 + w2, 0)
        w4 = min(w2, w3)
        w5 = -line7 if line7 < 0 else 0
        w6 = max(line15, 0)
        w7 = w4 + w6
        carry_st = max(w5 - w7, 0)                           # W8
        if line15 < 0:
            w9 = -line15
            w10 = max(line7, 0)
            w11 = max(w4 - w5, 0)
            w12 = w10 + w11
            carry_lt = max(w9 - w12, 0)                      # W13
    return {"schedule-d.line-7": line7, "schedule-d.line-15": line15, "schedule-d.line-16": line16,
            "schedule-d.line-21": line21, "form1040.line-7a": line7a, "form1040.line-15": f1040_line15,
            "carryover-2026.short-term": carry_st, "carryover-2026.long-term": carry_lt}
