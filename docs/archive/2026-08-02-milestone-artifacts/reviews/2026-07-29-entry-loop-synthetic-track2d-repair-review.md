# Re-review — The Entry Loop (synthetic), Track 2d repair

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track2d-repair-review.md`
- Branch: `milestone/entry-loop-synthetic`
- Repair object: `f4d31b8..8ff027f`
- Current clean pointer tip: `0b6c4bbb4f654e47eae63ff13f42261ce04c85d0`
- Status: **Advisory re-review**. This record does not issue a formal
  `READY` or `NOT READY` verdict.

## Evidence

The worktree was clean at the oriented pointer tip. The repair commit changes
only the Track 2d parser, declaration, focused tests, and regenerated surface
adoption/manifest/release/registry metadata. No criteria, contrast work,
field-contract model, real data, or Track 3 work was introduced.

The focused run `python3 -m unittest tests.test_entry_loop_t1` passed all 27
tests. `python3 tools/envelope_scan.py --range main..HEAD` and
`git diff --check f4d31b8..HEAD` exited cleanly.

Independent in-memory mutation of the loaded declaration to
`maxFractionDigits=3`, `requirePositive=false`, and `maxValue="1000.000"`
produced `1.234`, `0`, `-1`, and the exact maximum `1000`; `1.2345` and
`1000.001` were rejected. Malformed `maxFractionDigits`, `requirePositive`, and
non-numeric `maxValue` values returned `entry-format-unavailable`.

The regenerated surface metadata was recomputed independently: all 942
manifest entries matched their byte counts and SHA-256 digests; the manifest
checksum matched the registry and adoption package pin; the release registry
digest matched the registry bytes; and the adoption release checksum matched
the release bytes.

## Rechecked findings

### F1 — Partially closed: declaration-driven validation

The valid declaration controls now govern the parser. The declaration records
`maxFractionDigits`, `requirePositive`, and `maxValue` at
`packages/sample_data/entry_loop_t1/surface/content/app/src/w2-box1-format.js:9-11`.
The loader validates their types and numeric validity at
`packages/derivation/entry_loop.py:135-152`, and the parser applies them at
`packages/derivation/entry_loop.py:363-412`.

The live load path therefore refuses malformed non-positive maxima. However,
the parser itself does not reject a malformed non-positive `maxValue` after it
has been supplied in-memory. Reproduction:

```python
spec = dict(_load_w2_box1_format(repo_root), requirePositive=False, maxValue="0")
_parse_box1_with_format("0", spec)   # returns 0
_parse_box1_with_format("-1", spec)  # returns -1
```

`_parse_box1_with_format` checks only that the parsed maximum is finite and
that `amount > maximum` at `packages/derivation/entry_loop.py:407-412`; it does
not require the maximum itself to be positive. The loader's guard means this
does not bypass the live runtime, but it remains a residual against the
charter's requirement that malformed declarations fail closed. The new test
at `tests/test_entry_loop_t1.py:243-255` covers non-numeric but not non-positive
`maxValue`.

### F2 — Closed: anti-drift regression

`tests/test_entry_loop_t1.py:243-255` mutates all three numeric controls and
asserts both newly accepted values and values beyond the declared precision or
maximum are refused. A parser that stopped using any of
`maxFractionDigits`, `requirePositive`, or `maxValue` would fail this test. The
current test therefore proves the requested relationship without introducing
a generalized cross-language contract test.

## Non-findings

- The accepted grouped, prefixed, plain, signed-under-mutated-declaration,
  zero-under-mutated-declaration, precision-boundary, and maximum-boundary
  behaviors were independently exercised.
- Existing malformed-input, redaction, revision/log preservation, and
  synthetic data-safety checks remain passing.
- The JS-to-Python declaration seam remains deferred as explicitly chartered;
  it was not refactored or treated as a Track 2d residual.
