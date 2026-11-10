# Charter: fresh-reader review of Form 1099-B backup withholding

Role: Reviewer. Source HEAD on milestone/f1099b-backup-withholding-2025,
diffed against `github/main`. Plan:
docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md (read
it whole). You have not seen the build, so judge from the committed
content, tests and evidence, not from summaries. Do not read governance.

## Questions

1. **Tax correctness, computed by hand.** Work independently from the
   2025 Form 1040 instructions for line 25b and the Form 1099-B
   instructions for box 4 (public IRS sources). Compute these cases:
   - one sale statement with $150 in box 4, wages with W-2 withholding;
   - two sale statements, box 4 on one only;
   - box 4 answered $0 on every statement (must equal core v82);
   - a box 4 amount recorded for a statement whose sales were removed;
   - box 4 unanswered on a return with sales;
   - a return with no sales (no box 4 question).

   Run each through the real coordinator on core v83 with synthetic
   `demo.*` findings. Compare Form 1040 lines 25b, 25d, 33, 34, 35a and 37.
   Say whether any expected value in
   tests/fixtures/f1099b_backup_withholding_v83/expected.json is wrong.
2. **Admission.** Can any combination of answers publish a wrong number,
   or a number while a box 4 amount is unread? Try at least: a negative or
   non-numeric amount; an amount keyed to a statement with no sale; a
   leftover v82 yes/no box 4 answer on a v83 run; a statement added after
   box 4 was answered for the others. Does any v82 answer change meaning?
3. **The question.** Is the box 4 question's wording plain, and does a
   truthful answer supply what line 25b v7 reads? Is "If box 4 is blank,
   enter $0" correct for the filer?
4. **The audit test.** Does the extended sale-fact audit
   (sale-family-audit-evidence/tables.py) fail if the box 4 amount loses
   its reader? Mutate locally to show it.
5. **Immutability.** Run `git diff github/main --stat` over
   packages/content and packages/schemas. Is registry v81 add-only? Is the
   loader change limited to the per-core v83 entries? Is every new
   citizen byte-identical to the prototype's `decided` build?
6. **What the filer sees.** For every blocked line: is the reason
   non-empty and true? Is every new `explain` sentence true of its rule's
   `when`?
7. **CI cost.** The v83 fixture is 2.0 MB and the live module runs every
   Track 0 case and 213 returns. Name runs that test nothing a sibling
   does not, and say how far it can shrink without losing a Track 0 row's
   witness. Report the module's measured wall time.
8. **Test isolation.** Do the new modules assign any other evidence
   module's globals, at import or otherwise? CI runs several modules in
   one process.
9. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`, and check
   that no committed file has an absolute or temp-directory path. Do not
   write such a path in the review either.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/f1099b-backup-withholding/review.md, committed (staging the
explicit path, under the collaboration-commit lock; if the lock is held,
retry with backoff and never remove it). For each finding give:
file:line; a reproduction; a severity (blocking, should-fix or note); the
fix you would make. End with a verdict: ready, or the blocking list.
Make no other edits.
