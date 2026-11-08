# Charter: fresh-reader review of broker basis corrections

Role: Reviewer. Source HEAD on milestone/f8949-code-b-2025, diffed
against `github/main`. Plan: docs/phases/engine-breadth/milestones/f8949-code-b.md
(read it whole). You have not seen the build, so judge from the committed
content, tests and evidence, not from summaries. Do not read governance.

## Questions

1. **Tax correctness, computed by hand.** Work independently from the
   2025 Form 8949 and Schedule D instructions (public IRS sources; the
   evidence names them and their checksums). Compute these cases:
   - a box A sale whose broker basis is too high;
   - a box D sale whose broker basis is too low;
   - a correction that turns a gain into a loss, with the line 21 limit;
   - a BW row;
   - a box B sale with a wrong reported basis;
   - a mixed return with a code B sale beside covered and noncovered
     sales.

   Run each through the real coordinator on core v81 with synthetic
   `demo.*` findings. Compare every line: Schedule D lines 1a, 1b, 2, 7,
   8a, 8b, 9, 15, 16 and 21; Form 1040 lines 7a, 15 and 16; and Form
   8949 columns (d), (e), (g) and (h). Say whether any expected value in
   tests/fixtures/code_b_sales_v81/expected.json is wrong.
2. **Admission.** Can any combination of answers do either of these?
   - Publish a return whose wrong broker basis was left uncorrected.
   - Publish a wrong number on a recorded sale.

   Try at least:
   - one transaction recorded on two families, across terms or within one
     term;
   - a column (g) row that disagrees with its worksheet;
   - a wash amount above the corrected loss;
   - zero proceeds;
   - the taxpayer-side flag.

   Does any v80 answer change meaning?
3. **The four inherited v80 fixes (Decision 6).** Is each correct and
   complete? Did they change any v80 return beyond the patterns the plan
   lists?
4. **Immutability.** Run `git diff github/main --stat` over
   packages/content and packages/schemas. Is registry v79 add-only? Is
   the loader change limited to the per-core v81 entries?
5. **What the filer sees.** For every blocked line, check:
   - Is the reason non-empty and true?
   - Is every new `explain` sentence true of its rule's `when`?
   - Are the new questions' words true of their propositions, and plain?
6. **CI cost.** Find redundant cases in the live module. The fixture is
   about 447 KB; is that size justified?
7. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`, and check
   that no committed file has an absolute or temp-directory path.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/f8949-code-b/review.md. For each finding give:
- file:line;
- a reproduction;
- a severity: blocking, should-fix or note;
- the fix you would make.

End with a verdict: ready, or the blocking list.
