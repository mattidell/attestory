# Charter: Track 3 F1 Fix Delta — Independent Re-Review

Date: 2026-07-20. Prepared by the foreman; owner dispatches this seat
(ADR-0034). The reviewer is author-independent of the fix: it verifies the
fix commit against F1 as the original review stated it, not against the
fix builder's own account.

## Object under review

The fix delta `c0731f4..1247b89` on `track/dsbs-t3-qdcg-line16` (one
commit fixing the two test-selection sites), read against the original
review (`docs/reviews/2026-07-20-dsbs-t3-qdcg-line16-review.md`, Finding
F1) and its charter
(`docs/reviews/charter-2026-07-20-dsbs-t3-qdcg-line16-review.md`), plus the
fix's own charter
(`docs/reviews/charter-2026-07-20-dsbs-t3-f1-remediation.md`).

## Scope

This is a **delta re-check**, not a fresh full ten-check review. The
original review's nine passing checks (1–9) stand unless this delta itself
disturbs them (it should not — the fix charter forbids touching any
DSBS/Track 3 content, schema, or kernel file). Verify exactly:

1. **F1 discharged, not relocated.** In both
   `tests/test_frrs_t3_resolver_bootstrap.py::test_changed_member_bytes_under_honest_registry_refuses`
   and
   `tests/test_frrs_t4_w2_live_integration.py::ResolverCounterProbes::test_member_substitution_has_exact_refusal_and_layout_is_inert`,
   confirm the target-file selection is now genuinely deterministic against
   that test's own resolved package/release surface — not directory or
   glob order. Read the fix and confirm it selects a rule file by checking
   membership (`(id, version)`) against the specific package
   (`tax.us.2025.package.interest-slice` v1, per the fix report) the test's
   own `_surface(...)`/adoption act actually resolves — not by re-adding a
   different accidental first-match. Confirm the match key used
   (`body["id"]`/`body.get("version","v1")` against `package["members"]`)
   is actually how `packages/derivation/production_resolver.py`'s
   `_resolve_member_corpus` (or equivalent) matches candidates — read that
   function yourself, don't take the fix's stated mechanism on faith.
2. **The new selection genuinely excludes Track 3's file.** Confirm
   `rule.form1040-line16.v2.json` is not a member of
   `package.interest-slice.json` (read that package's member list
   directly) and would be skipped by the new selection logic even though
   it still sorts first lexicographically — construct or reason through why
   the old code picked it and the new code does not.
3. **No collateral damage.** The delta touches only the two named test
   files. Confirm no DSBS/Track 3 content file
   (`rule.form1040-line16.v2.json`, `qdcg.bundle.json`,
   `package.core-calculations.v6.json`, etc.), no kernel file
   (`findings.py`, `schema_registry.py`), no `marshal.py`, and no resolver
   implementation file changed in this delta — `git diff --stat
   c0731f4..1247b89` should show exactly the two test files (confirm this
   yourself, don't trust the fix report's file list).
4. **Both tests' original intent is preserved.** Each still asserts a
   `Refusal` with the same `reason` string as before the fix — confirm the
   assertions were not weakened or the scenario narrowed to make the test
   pass trivially (e.g. confirm the tampered file is still genuinely a
   different byte-sequence than the original, and the resolver's rejection
   path is still the one being exercised, not some other early-exit).
5. **No new fragility introduced.** If the new selection logic itself
   depends on iteration order across multiple qualifying members (i.e. more
   than one file in `package.interest-slice.json`'s member set could match),
   confirm the result is still deterministic — either only one member
   qualifies, or the tie-break is itself principled (not another silent
   "first" assumption that could break again later).
6. **Boundary and data safety hold.** No real value, workspace path, or
   refusal text entered the delta; `tools/scaffold_live_acts.py` and
   `workspace-seed/` remain untouched. Run the per-review safety scan.
7. **Battery re-run.** Full `.venv/bin/python3 -m unittest` (confirm the
   full 541-test count, not just the two previously-failing tests, and that
   the count matches or exceeds the original review's baseline), `-m
   mypy`, `tools/governance_lint.py`, and `.venv/bin/python3
   tools/envelope_scan.py --range main..HEAD` — re-run yourself, not
   trusted.

## Verdict

Append a dated delta-re-review file
(`docs/reviews/2026-07-20-dsbs-t3-f1-delta-rereview.md`) with an explicit
`ready` / `not ready` verdict for Track 3 as a whole (original review + this
delta), findings numbered R1…. If ready, this closes Track 3's review gate
— the owner holds the merge (ADR-0030). Track 4 (1099-DIV closure content
and live-run integration) opens next and closes the milestone.
