# Track 1: gains and break-even sales pinned on core v96

Charter: `docs/reviews/gain-break-even/charter-track1.md`. Plan Decision 1.
Tests only; no content, schema, engine or package-version change.

## Modules

- `tests/test_gain_break_even_v96.py` (live): 28 tests, 27 coordinator runs.
  Each return is one test, so a return runs once. Hand values come from
  `hand.py`, not captured engine output.
- `tests/test_gain_break_even_hand_values.py` (fast): 17 tests, about 1 s.
  Restates the Tax Table, Form 8949 column (h), Schedule D routing and the
  Qualified Dividends and Capital Gain Tax Worksheet as literal numbers.

## The 27 returns (core v96, saved page)

- 22 single filers (`path/term/shape/single`): paths covered (control), w,
  codeb, noncovered, no1099b; terms st, lt; shapes gain, even (20 returns);
  plus `w/st/even-plain` and `w/lt/even-plain` (proceeds equal basis, box 1g 0).
  This includes `no1099b/lt/even`, the cell that never ran on any core.
- 1 joint: `noncovered/lt/gain/married_filing_jointly` (all gain in the 0% band).
- 3 mixed, single: `lt-gain`, `st-gain`, `three` (each nets to a gain).
- 1 probe: `w/st/probe-gain/single`, box 1g 500 on a gain.

26 ordinary returns are checked for: run saturated with no blocked rule and no
question; Schedule D lines 1a, 1b, 2, 3, 6, 7, 8a, 8b, 9, 10, 13, 14, 15, 16 and
Form 1040 lines 7a, 15, 16 (value and a published disposition); Form 8949 part
totals and whether it is an attachment; Schedule D attachment published; the
preferential base; worksheet lines 5, 9, 17, 18, 22, 24 on a net long-term gain
(14 of the 26 returns have lines 15 and 16 above zero). The probe must block at
`...f1099b.covered-w-st.member-validation.synthesized` (`DEPENDENCY_INVALID`),
with Schedule D line 16, 1040 lines 7a and 16 blocked with no value, no line 16
published, no question; the test also reads `CODE_W_ON_GAIN` in the family
content (the page's reason is not captured by the harness, see below).

## Counts

| Module | Tests | Runs | Wall |
| --- | --- | --- | --- |
| live | 28 (1 subset-size, 26 ordinary, 1 probe) | 27 | about 26 s on `-n auto` |
| fast | 17 (7 Tax Table, 8 values, 1 routes, 1 worksheet) | 0 | about 1 s |

## Notes

- The harness (`cases.observe`) keeps only reasons phrased as questions, so the
  probe pins the block by rule and code and by the content's `CODE_W_ON_GAIN`
  text, not by the page reason's code. Capturing the reason would mean editing
  the P0 harness; left for the foreman.
