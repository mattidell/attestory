# Charter: fresh-reader review of sales without a Form 1099-B

Role: Reviewer. Source HEAD on milestone/f8949-boxes-cf-2025, diff
against `github/main`. Plan: docs/phases/engine-breadth/milestones/f8949-boxes-cf.md
(read it whole). You have not seen the build, so judge from the committed
content, tests and evidence, not from summaries. Do not read governance.
Edit nothing except your review file.

## Questions

1. **Tax correctness, computed by hand.** Use the 2025 Form 8949 and
   Schedule D instructions (public IRS sources; the evidence names them
   and their checksums). Compute these independently:
   - a box F gain;
   - a box C loss, with the $3,000 limit on line 21;
   - a box C sale with a code W adjustment;
   - a mixed return with box A, B and C short-term sales and a box F
     long-term sale.

   Run each through the real coordinator on core v80, using synthetic
   `demo.*` findings. Compare every line: Schedule D lines 1a, 2, 3, 7,
   9, 10, 15, 16 and 21, Form 1040 lines 7a, 15 and 16, and the Form
   8949 attachment. Say whether any expected value in
   tests/test_no1099b_sales_v80.py is wrong.
2. **Admission.** Read the new grouped question, the new in-class answer
   and the checks on lines 2, 3, 9 and 10:
   - Can any combination of answers publish a return with a box C or F
     sale left unrecorded?
   - Can any combination publish a wrong number on a recorded sale? Try
     shared sale records, amounts that disagree, code W on a gain, and a
     missing proceeds or basis amount.
   - Does any v79 answer change meaning?
3. **Immutability.** Did any published schema, citizen or package change
   bytes? Check `git diff github/main --stat` over packages/content and
   packages/schemas. Is registry v78 add-only? Is the loader change only
   the per-core v80 entries?
4. **What the filer sees.** For every blocked line in the cases:
   - Is the page reason non-empty and true?
   - Is every new `explain` sentence true of its rule's `when`?
   - Is each question asked once?
   - Is the new question's wording plain, and true for a filer who sold
     something other than securities?
5. **CI cost.** The new live module is about 121 coordinator runs, with a
   slowest case of about 70 s. Say whether the cases are redundant and
   which ones could merge without losing a distinct disposition path.
6. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Check that
   no committed file has an absolute local path.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/f8949-boxes-cf/review.md. For each finding give:
- file:line;
- a reproduction;
- a severity: blocking, should-fix or note;
- the fix you would make.

End with a verdict: ready, or the blocking list.

Commit the review with an explicit path, under the commit lock
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
Never use --no-verify or a bare git stash. Run foreground commands only.
No push or spawn.
