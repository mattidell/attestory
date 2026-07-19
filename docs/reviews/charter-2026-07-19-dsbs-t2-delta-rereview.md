# Charter: Track 2 Repair Delta — Independent Re-Review

Date: 2026-07-19. Prepared by the foreman; dispatched under the owner's
standing authorization for this continuation. The reviewer is
author-independent of the repair: it verifies the foreman's repair commit
against the original review's finding, not against the foreman's account of
it.

## Object under review

The repair delta `0541875..854c71a` on
`track/dsbs-t2-composition-conditional-machinery` (one commit, "repair(dsbs-
t2): fix Schedule B Part I tie-out target (F1)"), read against the original
review (`docs/reviews/2026-07-19-dsbs-t2-composition-conditional-machinery-
review.md`) and its charter (`docs/reviews/charter-2026-07-19-dsbs-t2-
composition-conditional-machinery-review.md`).

## Scope

This is a **delta re-check**, not a fresh full nine-check review. The
original review's eight passing checks (1–4, and 5's dividend-side half, 6,
7, 8) stand unless the repair delta itself disturbs them. Verify exactly:

1. **F1 discharged, not relocated.** `rule.attachment.schedule-b.json`'s
   `part-i-interest.tie_out.line_symbol` now names
   `tax.us.2025.interest.b1-subtotal` (the box-1-only subtotal), not
   `tax.us.2025.interest.taxable-total` (line 2b's four-family sum).
   Confirm `tax.us.2025.interest.b1-subtotal` is genuinely the box-1-only
   figure — read `rule.f1099int-b1-subtotal.json`'s `value` expression
   yourself, don't take the symbol name on faith. Confirm no other part of
   the fix silently widened Part I's itemization *rows* to cover box-3/OID/
   non-form instead (that would be the alternative fix the original review
   also named as acceptable — verify which one actually shipped, since the
   commit message claims the narrower tie-out-retarget option).
2. **The dividend-side tie-out (Part II) is untouched and still correct.**
   `part-ii-ordinary-dividends.tie_out.line_symbol` still names
   `tax.us.2025.dividends.ordinary-total`, unchanged by this delta.
3. **New regression coverage is real, not vacuous.**
   `PartIInterestTieOutWithConcurrentNonBox1Interest` in
   `tests/test_dsbs_t2_schedule_b.py` asserts a scenario with concurrent
   non-zero box-1 *and* box-3 interest (the exact combination F1 named)
   publishes cleanly — construct the arithmetic yourself (line 2b = box-1 +
   box-3 = 300 + 150 = 450; the box-1 subtotal alone = 300) and confirm the
   test's assertions are consistent with a genuinely non-degenerate
   divergence between the two figures, not a case where they happen to
   coincide. Confirm this golden enters through `live_coordinate_run` (the
   file's own docstring says every golden must), not a `RunContext`
   shortcut newly introduced by the repair.
4. **The two supplementary `RunContext`-level classes still hold.**
   `WholeFormValueContent` and `TieOutInvariant` each needed a new
   `tax.us.2025.interest.b1-subtotal` input added alongside the pre-existing
   `tax.us.2025.interest.taxable-total` input (the repair's stated reason:
   `attempt_attachment` reads the two symbols for two different purposes —
   the existence-conditional threshold and the Part I tie-out — that
   happened to share one input value before the fix only by coincidence).
   Confirm this reasoning by reading `attempt_attachment` in
   `packages/derivation/runner.py` yourself: confirm `requirement.subtotals`
   (the threshold check) and each itemization part's `tie_out.line_symbol`
   (the tie-out check) are in fact read from independent symbols in the
   citizen's declared content, so supplying both inputs is the correct fix
   for these test contexts rather than a workaround masking a residual bug.
5. **No collateral damage.** The delta touches only:
   `rule.attachment.schedule-b.json`, `published-packages.json`, the
   `frrs_t3` adoption/release checksum fixtures (mechanical registry-
   checksum cascade — confirm each changed fixture's diff is *only* a
   checksum string, nothing else), and `tests/test_dsbs_t2_schedule_b.py`.
   No `packages/derivation/runner.py`, `evaluator.py`, or any other schema
   file changed — confirm this is genuinely a content-only fix, matching
   the commit message's claim that the tie-out mechanism itself was already
   correct.
6. **Boundary and data safety hold.** All new/changed test fixtures remain
   `demo.*` synthetic; no real value, workspace path, or refusal text
   entered the delta. Run the per-review safety scan.
7. **Battery re-run.** Full `.venv/bin/python3 -m unittest`, `-m mypy`,
   `tools/governance_lint.py`, and `.venv/bin/python3
   tools/envelope_scan.py --range main..HEAD` — re-run yourself, not
   trusted. If the venv fails to import, rebuild it (see prior charters on
   this branch for the rebuild pattern).

## Verdict

Append a dated delta-re-review section or new file
(`docs/reviews/2026-07-19-dsbs-t2-delta-rereview.md`) with an explicit
`ready` / `not ready` verdict for the track as a whole (original review +
this delta), findings numbered R1… . The owner holds the merge (ADR-0030).
