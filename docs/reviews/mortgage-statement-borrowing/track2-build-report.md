# Track 2 build report

## Current checkpoint

The first checkpoint, `c31fb9ce`, adds the canonical mortgage-borrowing
calculation vocabulary, five local/shared effective-answer mappings, the v54
core successor, and the additive v52 registry/release successor. It preserves
the complete v51 registry entries and the v53 core's 580 members and 26 input
bindings. The new mortgage-borrowing bundle was absent from v53; the existing
F1098 vocabulary v1 and successor vocabulary v2 were already present.

The current uncommitted increment adds a narrowly gated saved projection for
current Box 1 reports, current relationship outcomes (including separate
orphans), recorded account claims, actual effective-answer values and pins,
consumed input/choice finding IDs, and the exact line8a disposition. It does not
calculate tax or reread the workspace. Tests use the real Track 1 borrowing
and F1098 answer recorders and the normal coordinator, then inspect the saved
report/model. The third unlinked current-report case is represented once and
does not crash projection.

## Evidence and limits

Verified so far:

- v54 validates against the current content corpus and retains the v53 input
  bindings and member set as a subset.
- v52 retains all v51 package and citizen entries and the release pins the exact
  v52 registry bytes.
- The real coordinator publishes the five mapping dispositions with exact
  report/borrowing keys and expected local/shared input pins. A current shared
  `cannot-tell` beside a favorable local answer blocks that effective answer.
- The durable projection records actual Box 1 values, current relationship
  claims, effective values/pins, annual ceiling (separate from Box 2), and an
  exact line8a producer disposition. The fixture has
  `AUTHORIZATION_ABSENT`; it is not evidence of return authorization or a
  complete return.
- The extra unlinked third current report appears once and has no relationship;
  only the two explicitly linked reports are in the borrowing's report keys.
- The new-package/no-borrowing-activity observation is only a blocked v54
  candidate observation. It has not been compared with v53 and does not prove
  incumbent singleton behavior.

This is not a completed production calculation. The current v54 candidate still
uses the line8a v2 rule and has no executable successor chain for connected
reason/readiness, the single supported full-interest collector, or the required
line12e/attachment successors. Accordingly the tested amount is only the
existing producer's blocked disposition; no connected deductible amount,
Schedule A total, or attachment result is claimed. Outstanding Track 2 work is
to add and validate that successor chain, preserve true-empty and legacy
singleton routing, and run the chartered positive and independent refusal
cases through the coordinator and reloaded saved model.

## Focused commands

- `pytest tests/test_mortgage_borrowing_calculation.py` — 5 passed.
- `python3 -m mypy --cache-dir=<temporary-cache-dir> packages/derivation/presentation_projection.py tests/test_mortgage_borrowing_calculation.py` — no issues.

The test run emitted a sandbox pytest-cache permission warning; it did not
affect the test result. Full CI remains the gate of record, particularly
because the projector is under `packages/derivation/`.
