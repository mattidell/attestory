# Track 2 build report

## Current checkpoint

The first checkpoint, `c31fb9ce`, adds the canonical mortgage-borrowing
calculation vocabulary, five local/shared effective-answer mappings, the v54
core successor, and the additive v52 registry/release successor. It preserves
the complete v51 registry entries and the v53 core's 580 members and 26 input
bindings. The new mortgage-borrowing bundle was absent from v53; the existing
F1098 vocabulary v1 and successor vocabulary v2 were already present.

The projection increment adds a narrowly gated saved projection for
current Box 1 reports, current relationship outcomes (including separate
orphans), recorded account claims, actual effective-answer values and pins,
consumed input/choice finding IDs, and the exact line8a disposition. It does not
calculate tax or reread the workspace. Tests use the real Track 1 borrowing
and F1098 answer recorders and the normal coordinator, then inspect the saved
report/model. The third unlinked current-report case is represented once and
does not crash projection. A report's actual reason-chain finding is included
when a current reason publication pins that exact Box 1 finding; in the
two-report probe, this is present only for B, whose report-local answers are
complete, while A's missing local answers remain visibly absent.

The saved-model implementation and recorder-backed integration tests are in
`a82eec30` and `f27e82f8`. Consumer successors and the exact v55/v53 release
chain are in `20c9e9b4`.

The connected calculation increment is committed in `59c557ee`; its projector
compatibility/basis repair is `11d012a6`. The real recorder and coordinator
publish and save a supported two-report line8a finding of $25,500 (22,000 +
3,500), with both Box 1 findings pinned and qualified report-local reason
findings. A separate no-current-borrowing singleton publishes $22,000 and keeps
the legacy mortgage explanation, including its actual basis and answer record.
The v55 amount rule uses an exact v14 citizen with a route-aware declared basis:
the Box 2-as-annual-balance shortcut is explicitly singleton-only; the
connected route uses a separately recorded annual ceiling and retains the
conservative $750,000/$375,000 cap while disclosing the unmodeled higher
grandfathered limit. Categorical reader labels are resolved from exact
producing-rule joined/category references; the old missing-basis error remains
fail-loud, while numeric/date Box titles keep their established source path.

## Evidence and limits

Verified so far:

- v54 validates against the current content corpus and retains the v53 input
  bindings and member set as a subset.
- v52 retains all v51 package and citizen entries and the release pins the exact
  v52 registry bytes.
- v55 is additive over v54 except for intended line12e and attachment
  successor pins. Line12e v2 explicitly requires/pins Schedule A total;
  attachment v2 retains exactly the seven value-checked boundary declarations
  and removes only the obsolete liability/payment presence check. Registry v53
  retains all v52 entries, which in turn retains v51, and the release pins the
  exact v53 registry bytes.
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
- The no-borrowing-activity singleton path in the v55 candidate publishes its
  actual $22,000 amount and legacy explanation with basis/answers. This is
  candidate-path evidence, not a claim that v55 is ratified or a substitute for
  the full compatibility/refusal matrix.

Track 2 remains open. The first foundation amount is verified, but all five
shared-answer-to-reason paths, the chartered independent refusal cases,
Schedule A/line12e attachment behavior, and broader correction/lifecycle cases
remain unverified. This checkpoint does not claim complete Track 2 acceptance,
return authorization, or a complete return.

## Focused commands

- `pytest tests/test_mortgage_borrowing_calculation.py tests/test_f1098_circumstances_explanation.py tests/test_f1098_production_review_repair.py` — 24 passed, 25 subtests passed.
- `pytest tests/test_envelope_hooks.py` — 12 passed; the staged envelope scan and `git diff --check` were clean for the repair.
- `python3 -m mypy --cache-dir=<temporary-cache-dir> packages tests` — no issues in 332 source files.

The test run emitted a sandbox pytest-cache permission warning; it did not
affect the test result. Full CI remains the gate of record, particularly
because the projector is under `packages/derivation/`.
