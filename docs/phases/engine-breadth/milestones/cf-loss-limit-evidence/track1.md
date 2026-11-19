# Track 1: box C and F loss limit pinned

Charter: `docs/reviews/cf-loss-limit/charter-track1.md`. Tests only; no content,
schema, engine or package change.

## Subset chosen and why

`tests/test_cf_loss_limit_v96.py` runs 24 of P0's 90 returns on published core
v96 through `live_coordinate_run` and the saved page (P0's `cases.py` builds
and observes them):

- 18 box C/F returns: `cf/{st,lt,both}` (box C only, box F only, C plus F)
  for single and married filing separately, at `below`, `at` and `above` the
  limit (3,000; 1,500 separately). These are the two statuses whose limit
  differs, and the three sizes straddle the cap.
- 6 A/D controls: `ad/{st,lt,both}` for each status at `at` and `above`. Every
  C/F return at or over the limit is compared with its own control; below the
  limit nothing is capped, so no control is run there.

Assertions per return: Schedule D lines 7, 15, 16, 21 and Form 1040 lines 7a
and 15 equal P0's `hand.py` values (line 21 as the positive loss amount, the
form's parentheses); the sale lands on its own box line; stop `saturated`, no
blocked rule, no question. Each C/F return equals its control on every
non-box line, disposition, question and inbound carryover; only Form 8949
differs (`published` against `guard_inapplicable`).

The fast companion `tests/test_cf_loss_limit_hand_values.py` checks
`hand.values` against literal Schedule D instruction arithmetic (limit,
worksheet order, joint deduction, net gain) on 10 synthetic cases, so the
expected values are not engine output.

## Run time

Live module: 72 tests in about 40 s wall on `-n auto` (each worker memoises
its runs). Fast companion: 10 tests, about 1 s.

## Boundary

`test_no_2026_carryover_published` runs on all 24 returns: the only published
symbols naming a carryover or 2026 are the two inbound 2024-to-2025 carryover
symbols (published 0 here) and `payments.line36-applied-to-2026` (refund
applied to 2026 tax); none is a loss carried to 2026. This is the boundary of
ADR-0058 Decision 7 and ADR-0060 Decision 7, named in the test's docstring.
