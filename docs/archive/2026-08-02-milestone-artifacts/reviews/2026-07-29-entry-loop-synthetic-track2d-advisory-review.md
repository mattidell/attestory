# Advisory Review — The Entry Loop (synthetic), Track 2d

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track2d-advisory-review.md`
- Branch: `milestone/entry-loop-synthetic`
- Review object: `95225ea..fe883df`
- Current clean pointer tip: `9cc7f757be3fa81ff1e5302b4d3fb0287d7344ef`
- Status: **Advisory findings only**. This record does not issue a formal
  `READY` or `NOT READY` verdict.

## Scope and evidence

The implementation object contains only the Track 2d changes to the W-2 Box 1
format declaration, parser, surface metadata, and focused tests. The later
pointer and documentation commits through `9cc7f75` are administrative context
named by the review charter, not additional product scope.

The worktree was clean at the reviewed pointer tip. The focused test run
`python3 -m unittest tests.test_entry_loop_t1` passed all 26 tests. The reviewer
ran `python3 tools/envelope_scan.py --range main..HEAD` and
`git diff --check 95225ea..HEAD`; both exited cleanly.

Independent runtime checks confirmed that `90000`, `90000.50`, `90,000`,
`$90000`, and `$90,000.50` normalize to the expected numeric values. The
malformed values `9,0,0`, `$$90000`, `90,00.5`, `1.234`, `0`, `-1`,
`1000000000`, and `999999999.999` were rejected. HTTP rejection checks returned
422, did not echo the submitted value, and left both revision and act-log count
unchanged.

The surface metadata was independently recomputed: all 942 manifest entry
byte counts and SHA-256 digests matched; the manifest package checksum matched
the registry and adoption pins; the release registry digest matched the
registry bytes; and the adoption release checksum matched the release bytes.

The implementation range contains no criteria document, contrast change,
field-contract model, real data, or unrelated product file.

## Findings

### F1 — High: the declaration does not fully govern validation

`packages/sample_data/entry_loop_t1/surface/content/app/src/w2-box1-format.js:9-10`
declares `maxFractionDigits: 2` and `requirePositive: true`, but
`packages/derivation/entry_loop.py:340-360` hard-codes the two-decimal regex,
the `exponent < -2` check, unconditional positivity, and the maximum numeric
value. `_load_w2_box1_format` validates only the comma and currency-prefix
flags at `packages/derivation/entry_loop.py:128-133`.

Reproduction:

- Change the declaration's `maxFractionDigits` to `3`. The rejection message
  uses that declaration value at `packages/derivation/entry_loop.py:169-179`,
  but the validator still rejects `1.234` through the regex and exponent
  checks.
- Change `requirePositive` to `false`. The validator still rejects `0` at
  `packages/derivation/entry_loop.py:354`.

The current declaration and current validator agree by coincidence on these
values, but a declaration-only change can make the user-facing guidance
promise a form the validator refuses. This violates the single-source and
anti-drift requirements even though the current accepted set behaves as
intended.

### F2 — Medium: the anti-drift regression asserts configuration, not the relationship

`tests/test_entry_loop_t1.py:224-236` asserts that the current comma and
currency flags equal `accepted`, then exercises one grouped value and one
prefixed grouped value. It does not vary or exercise `maxFractionDigits` or
`requirePositive`, and it does not assert that the validator's accepted set is
derived from every declaration control.

The test would remain green if `maxFractionDigits` changed from `2` to `3` or
`requirePositive` changed from `true` to `false`, while the validator remained
unchanged. The adversarial regression at
`tests/test_entry_loop_t1.py:378-386` covers malformed grouping and currency
symbols, but not those declaration-driven precision and positivity controls.

## Non-findings

- Current comma grouping, optional leading `$`, canonical numeric conversion,
  malformed grouping, repeated or misplaced symbols, excess precision,
  non-positive values, oversized values, redaction, and state preservation
  were independently exercised as described above.
- The changed adoption, manifest, release, and registry files are internally
  consistent and synthetic.
- No formal usability score or gate verdict was issued.
