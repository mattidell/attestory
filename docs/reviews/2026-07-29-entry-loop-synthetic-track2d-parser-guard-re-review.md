# Re-review — The Entry Loop (synthetic), Track 2d parser guard

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track2d-parser-guard-re-review.md`
- Branch: `milestone/entry-loop-synthetic`
- Repair object: `e27847c..c4cd1fe`
- Current clean pointer tip: `004af3e773070e57c685b32d6d8b0811ad32b1fe`
- Status: **Advisory closure record**. This review does not issue a formal
  `READY` or `NOT READY` verdict.

## Rechecked residual

The remaining parser-guard finding is closed. `_parse_box1_with_format` now
rejects a supplied `maxValue` that is zero, negative, non-finite, or
non-numeric with `entry-format-unavailable` at
`packages/derivation/entry_loop.py:407-416`, independently of the loader's
validation path.

The focused regression at `tests/test_entry_loop_t1.py:257-271` covers
`0`, `-1`, `-0.01`, `NaN`, `Infinity`, `-Infinity`, and `not-a-number`, and
checks both zero and signed candidate values for the malformed ceilings.

## Measurements

With an in-memory valid declaration mutated to `maxFractionDigits=3`,
`requirePositive=false`, and `maxValue="1000.000"`:

- `1000.000` normalized to `1000`;
- `1000.001` returned `entry-value-invalid`;
- the existing focused regression continued to prove the declared precision
  and positivity controls.

`python3 -m unittest tests.test_entry_loop_t1` passed all 28 tests.
`python3 tools/envelope_scan.py --range main..HEAD` exited cleanly.

The regenerated surface metadata remains consistent: all 942 manifest entries
matched their byte counts and SHA-256 digests; the manifest checksum matched
the registry and adoption package pin; the release registry digest matched the
registry bytes; and the adoption release checksum matched the release bytes.

No criteria, contrast work, field-contract model, real data, surface metadata
edit, or JS/Python seam refactor was introduced by the reviewed repair.

## Residuals

None found within the chartered parser-guard scope.
