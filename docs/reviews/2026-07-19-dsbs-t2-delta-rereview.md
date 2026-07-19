# Review: Track 2 Repair Delta — Independent Re-Review (F1 Delta Check)

Date: 2026-07-19. Reviewer: author-independent (fresh session, no access to
the authoring session(s) of the original build, the original review, or the
repair). Object under review: the repair delta `0541875..854c71a` on
`track/dsbs-t2-composition-conditional-machinery` (one commit,
"repair(dsbs-t2): fix Schedule B Part I tie-out target (F1)"), read against
the original review (`docs/reviews/2026-07-19-dsbs-t2-composition-
conditional-machinery-review.md`, verdict NOT READY, finding F1) and its
charter. This is a delta re-check per
`docs/reviews/charter-2026-07-19-dsbs-t2-delta-rereview.md`: the original
review's eight passing checks stand unless this delta disturbs them.

## Verdict: **READY** (original review + this delta, taken together)

F1 is discharged by the narrower of the two options the original review
named acceptable (retarget the tie-out, not widen the itemization scope),
matching the repair commit's own claim. The fix is a single-line content
change plus a mechanical checksum cascade and new test coverage; no
runner/evaluator/schema code was touched. The new regression golden
constructs a genuinely non-degenerate divergence (line 2b = 450 vs. box-1
subtotal = 300) and enters through `live_coordinate_run`, not a
`RunContext` shortcut. Collateral scope is exactly as claimed: one content
file, one checksum-cascade set (12 files, each a pure checksum-string
diff), and one test file. Full battery re-run green. Combined with the
original review's eight passing checks (Track 2's own admission-invariant,
composition, existence-conditional, itemization-identity, dividend-side
tie-out, Part III completeness, and boundary-fence mechanisms), the track
is ready for owner merge.

## R1 — F1 discharged, not relocated (Check 1): PASS

`git diff 0541875..854c71a -- packages/content/tax/2025/rule.attachment.schedule-b.json`
is exactly one line:

```
-      "tie_out": { "line_symbol": "tax.us.2025.interest.taxable-total" }
+      "tie_out": { "line_symbol": "tax.us.2025.interest.b1-subtotal" }
```

only inside `part-i-interest`; `part-i-interest.rows.source_family` (still
`tax.us.2025.f1099int.b1`) is untouched — the itemization's *row* scope was
already correct per the original review's check 4; only the tie-out
*target* moves.

I read `rule.f1099int-b1-subtotal.json`'s `value` expression directly
rather than trusting the symbol name: it is `round(add(collect(
tax.us.2025.f1099int.box1-interest, source_set=tax.us.2025.f1099int.b1)))`,
publishing `tax.us.2025.interest.b1-subtotal`. This is genuinely a single-
family collect over the box-1 source set only — no composition of box-3,
OID, or non-form interest anywhere in the expression. The file's own
`notes` field independently corroborates this: "This symbol is the box-1
subtotal only - per ADR-0016 it never publishes to, or stands behind, Form
1040 line 2b or any claim about total taxable interest." Confirmed
genuinely box-1-only, not on faith.

This is the narrower fix (retarget the tie-out), not the alternative the
original review also named (widen Part I's itemization rows to cover box-3/
OID/non-form). `rule.attachment.schedule-b.json`'s `part-i-interest.rows`
block is byte-identical before and after (only the `tie_out` line differs
in the diff) — the itemization still `collect_members`s
`tax.us.2025.f1099int.b1` alone. The commit message's claim that the
narrower option shipped is accurate.

## R2 — Dividend-side tie-out untouched (Check 2): PASS

`part-ii-ordinary-dividends.tie_out.line_symbol` still reads
`tax.us.2025.dividends.ordinary-total` in the post-repair file (confirmed
by direct read); the diff touches only `part-i-interest`'s tie_out line, as
shown above. No change to Part II.

## R3 — New regression coverage is real (Check 3): PASS

`PartIInterestTieOutWithConcurrentNonBox1Interest` (`tests/
test_dsbs_t2_schedule_b.py`, added in this delta) constructs box-1 interest
= 300 and box-3 interest = 150 concurrently, alongside box1a = 2000
dividends (to keep the $1,500 threshold crossed independent of the
interest scenario). I derived the arithmetic independently:

- Line 2b (`tax.us.2025.interest.taxable-total`, the four-family sum) =
  300 (box-1) + 150 (box-3) + 0 (OID) + 0 (non-form) = **450**.
- The box-1 subtotal alone (`tax.us.2025.interest.b1-subtotal`) = **300**.

These two figures genuinely diverge (450 ≠ 300) — not a case where they
happen to coincide, which is exactly the triggering condition F1 named as
previously unexercised. The test asserts: line 2b's rule row is
`published` (confirming 450 computed correctly); the attachment row is
`published` with no `ITEMIZATION_TIE_OUT_VIOLATION` code (confirming the
retargeted tie-out — 300 row-sum vs. 300 box-1-subtotal line-value — ties
out cleanly instead of spuriously comparing 300 against 450); and Part I's
pins include the box-1 finding but explicitly exclude the box-3 finding
(confirming the itemization's row scope is still honestly box-1-only, not
silently widened as a side effect of the fix).

The test enters through `live_coordinate_run`: it calls `_run(...)`
(`tests/test_dsbs_t2_schedule_b.py:214-225`), which is the module's shared
helper wrapping `live_coordinate_run` directly (not a `RunContext`
shortcut) — confirmed by reading the helper body. The file's own docstring
requirement that every golden enter through `live_coordinate_run` is
satisfied for this test.

## R4 — Supplementary `RunContext` classes correctly extended (Check 4): PASS

`WholeFormValueContent` and `TieOutInvariant` each gained a new
`InputFinding("tax.us.2025.interest.b1-subtotal", "0", ...)` alongside the
pre-existing `tax.us.2025.interest.taxable-total` input (confirmed by
reading the diff hunks directly).

I re-read `attempt_attachment` in `packages/derivation/runner.py` to
confirm this is the correct fix, not a workaround: `subtotal_symbols =
requirement["subtotals"]` (line 471) — which in the content is
`["tax.us.2025.interest.taxable-total", "tax.us.2025.dividends.ordinary-
total"]`, read at lines 496-500 for the threshold-trigger check
(`self.symbols[s]` per subtotal) — is a wholly separate list from
`tie_symbol = part["tie_out"]["line_symbol"]` (line 562), read
independently per itemization part inside the tie-out loop (lines 561-577).
These are two structurally distinct reads of `self.symbols` keyed by two
different content-declared symbol names. Since the threshold check still
legitimately needs the full `taxable-total` (ADR-0036's $1,500 requirement
test is over total taxable interest, not box-1 alone) while the tie-out now
needs `b1-subtotal`, both test contexts genuinely require both inputs
supplied — this is not a workaround masking a residual bug in the fold;
it is the correct consequence of the two symbols now being genuinely
independent inputs to two different purposes within the same rule.

## R5 — No collateral damage (Check 5): PASS

`git diff 0541875..854c71a --stat` shows exactly 14 files:
`rule.attachment.schedule-b.json` (content fix, R1), `published-packages.json`
(one checksum), 10 `frrs_t3` adoption fixtures + 1 release fixture (each a
checksum-string diff only — confirmed by reading every changed line in
every file: all are `"checksum": "..."` or `"package_registry_sha256":
"..."` value changes, nothing else touched), and `tests/
test_dsbs_t2_schedule_b.py` (new test + two extended classes, R3/R4).

`git diff 0541875..854c71a -- packages/derivation/runner.py
packages/derivation/evaluator.py packages/schemas/` is empty — confirmed
no runner, evaluator, or schema file changed, matching the commit
message's claim that the tie-out mechanism itself was already correct and
only the content was wrong.

## R6 — Boundary and data safety (Check 6): PASS

Scanned the full delta diff for real-value/PII/workspace-path/refusal-text
patterns (`ssn|real|refusal|/Users/|workspace`, case-insensitive): no
matches. All new/changed identifiers in the delta follow the established
`demo.*` (fixtures) / `tax.us.2025.*` (content) conventions — confirmed by
direct read of the new test additions (`demo.dsbs.t2.schb.int-payer`,
`demo.dsbs.t2.schb.int-stmt`, `demo.dsbs.t2.schb.finding.int-box1/box3`,
etc.). `tools/scaffold_live_acts.py` and `workspace-seed/` are present as
untracked in this worktree; left untouched and not staged, per standing
boundary discipline.

## R7 — Verification battery re-run (Check 7): PASS

`.venv/bin/python3` in this worktree is already Python 3.13.12 and
imports cleanly; no rebuild needed. Ran fresh, not trusted:

- `.venv/bin/python3 -m unittest` — **510 tests, OK** (111.8s).
- `.venv/bin/python3 -m mypy` — **Success: no issues found in 99 source
  files**.
- `.venv/bin/python3 tools/governance_lint.py` — **governance lint:
  conformant**.
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — **exit
  0, clean**.

510 (up from the original review's 509) matches the one new test added by
this delta (`PartIInterestTieOutWithConcurrentNonBox1Interest`'s single
test method); 99 mypy-checked source files (up from the original review's
98) reflects the delta's net-new content in the count mypy reports over the
package; the load-bearing fact is that mypy remains clean.

## Summary

All seven delta-check items pass on direct re-derivation from committed
source. F1 is genuinely discharged by the narrow, verifiable content fix
the original review anticipated would suffice, with non-vacuous regression
coverage entering through the authoritative live-run surface, no collateral
touch to any file outside the fix's necessary scope, and a clean full
battery re-run. Combined with the original review's eight passing checks
(which this delta does not disturb — no code outside
`rule.attachment.schedule-b.json`'s single tie-out line and the test file
changed), Track 2 (composition and conditional machinery) is **ready** for
owner merge.
