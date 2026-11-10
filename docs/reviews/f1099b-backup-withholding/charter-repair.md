# Charter: repair of the Form 1099-B backup withholding review

Role: Builder. Source HEAD on milestone/f1099b-backup-withholding-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md,
Decision 6. Review: docs/reviews/f1099b-backup-withholding/review.md (read
it whole; it has the reproductions). Do not read governance.

Core v83, registry v81 and release v81 and every new citizen are
unpublished on this branch: rebuild them in place (regenerate from
prototype.py, then `python3 -m tools.package_successor`); do not make
v84. Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Repairs

1. **Finding 1, blocking.** Implement Decision 6 in prototype.py's
   `decided` design: line 25b v7 adds every current box 4 amount on both
   arms. A no-sale, no-amount return must still publish line 25b
   (computed zero) and be asked nothing new. If the language cannot do
   that without a closure question, take Decision 6's fallback (block
   with a true reason while an amount exists and every sale count is
   zero) and say so in the plan. Rerun Track 0 and the 213-return
   classification; correct `trace2_sale_removed`, `alc_stmt_orphan`,
   `b4_statement_removed` to the hand values (the review's $200 return:
   line 25b 200, 25d 4,700, 33 4,700, 34 825, 35a 825, 37 0), add the
   review's $150 orphan and orphan-beside-kept-sale cases, and update
   track0-closure.md and the plan's Track 0 section. Classify every
   v82 return that changes. Fix the field description, the family
   closure claim and the loader comment at packages/tax/loader.py:514 so
   each says what the rule adds.
2. **Finding 2.** The sale-fact audit counts the amount as read only on a
   value-side read (`collect`, `ref` or sum), not a `require_paired` key.
   Add a test that removing the value `collect` fails the audit.
3. **Finding 3.** The blocked explain says line 25b is blocked while a
   recorded sale's statement has no box 4 amount (or whatever Decision 6's
   outcome makes true).
4. **Finding 4.** Drop the regenerator's temp-directory write, or write
   under an ignored local directory.
5. **Finding 5.** Add line 25d to `CHARTER_LINES` and require it on every
   success pin.

Regenerate tests/fixtures/f1099b_backup_withholding_v83/expected.json and
report its size and run count. Then run `pytest -m "not live"`, the full
`pytest` (shard if needed, sum the counts), `python3 -m mypy` and
`python3 tools/envelope_scan.py --range github/main..HEAD`, and update the
plan's "Track 1 result" with the new counts, classes and a "Repair"
paragraph.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Load evidence harnesses under unique module names; never assign another
  evidence module's globals.
- Keep every test under the 3.0 s fast-lane budget or `@pytest.mark.live`
  with a measured reason.
- Commit after each numbered repair, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry with backoff if held, never remove another holder's lock). Never
  --no-verify, never git stash, never push.
