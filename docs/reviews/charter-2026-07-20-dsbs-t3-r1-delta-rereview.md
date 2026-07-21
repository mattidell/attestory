# Charter: Track 3 R1 Fix Delta — Final Independent Re-Review

Date: 2026-07-20. Prepared by the foreman; owner dispatches this seat
(ADR-0034). The reviewer is author-independent of the fix: it verifies the
fix commit against R1 as the delta re-review stated it, not against the
fix builder's own account.

## Object under review

The single fix commit `c1cd01f` on `track/dsbs-t3-qdcg-line16` (following
charter commit `1636110`, which is administrative — a charter file, not
implementation; do not treat it as part of the object under review, and do
not re-flag this as a scope-range issue the way R2 did — that is the exact
mistake this note exists to avoid repeating). Read against the F1 delta
re-review (`docs/reviews/2026-07-20-dsbs-t3-f1-delta-rereview.md`), Finding
R1, and the R1 remediation charter
(`docs/reviews/charter-2026-07-20-dsbs-t3-r1-remediation.md`).

## Scope

This is a **delta re-check**, not a fresh full review. Everything the F1
delta re-review already passed (checks 1, 2, 4, 6, 7) and R2 (a charter-
authoring artifact, not a code issue — already reconciled, do not re-open)
stand. Verify exactly:

1. **R1 discharged.** Both
   `tests/test_frrs_t3_resolver_bootstrap.py::ReleaseRegistrySubstitutions::test_changed_member_bytes_under_honest_registry_refuses`
   and
   `tests/test_frrs_t4_w2_live_integration.py::ResolverCounterProbes::test_member_substitution_has_exact_refusal_and_layout_is_inert`
   now target one explicit named member —
   `tax.us.2025.rule.form1040-line2b` v1 — located by its known filename
   (`rule.form1040-line2b.json`), not by scanning/iterating and breaking on
   a first match. Confirm both tests assert, before tampering: (a)
   membership of the named `(id, version)` in
   `package.interest-slice.json`'s `members` list with `role ==
   "computation"`, and (b) the loaded file's own `(id, version)` equals the
   named target exactly. Confirm both assertions would fail loudly (not
   silently substitute another file) if the named target were ever
   missing, renamed, or its role changed — read the assertion messages and
   confirm they're not vacuously true.
2. **No reintroduced first-match logic.** Confirm neither test still
   contains a residual loop that iterates candidates and breaks on the
   first match of anything — grep for `for ` / `break` / `next(` near the
   selection code in both files and confirm the old pattern is fully gone,
   not left as dead/unreachable fallback code.
3. **Membership claim is accurate.** Read
   `packages/content/tax/2025/package.interest-slice.json` yourself and
   confirm `tax.us.2025.rule.form1040-line2b` v1 is genuinely listed with
   `role: "computation"` at the line the fix report cites — don't take the
   citation on faith.
4. **Collateral scope.** `git diff --stat` of commit `c1cd01f` alone (not
   including `1636110`) touches exactly the two named test files — confirm
   this yourself. No DSBS/Track 3 content, kernel, `marshal.py`, or
   resolver implementation file changed.
5. **Original test intent still preserved.** Both tests still assert
   `Refusal` with reason `MEMBER_ABSENT_OR_MISMATCH`, tampering genuine
   bytes of the (now correctly identified) target file.
6. **Boundary and data safety.** No real value, workspace path, or
   refusal text entered the delta; `tools/scaffold_live_acts.py` and
   `workspace-seed/` untouched. Run the per-review safety scan.
7. **Battery re-run.** Full `.venv/bin/python3 -m unittest` (confirm
   541/541 or current total), `-m mypy`, `tools/governance_lint.py`, and
   `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` —
   re-run yourself.

## Verdict

Write `docs/reviews/2026-07-20-dsbs-t3-r1-delta-rereview.md` on the branch
with an explicit `ready` / `not ready` verdict for **Track 3 as a whole**
(original review + F1 fix + R1 fix), findings numbered S1…. If `ready`,
this closes Track 3's review gate entirely — the owner holds the merge
(ADR-0030). Track 4 (1099-DIV closure content and live-run integration)
opens next and closes the milestone.
