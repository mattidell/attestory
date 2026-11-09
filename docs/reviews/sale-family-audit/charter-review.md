# Charter: fresh-reader review of the sale family audit

Role: Reviewer. Source HEAD on milestone/sale-family-audit-2025, diffed
against `github/main`. Plan: docs/phases/engine-breadth/milestones/sale-family-audit.md
(read it whole). You have not seen the build, so judge from the committed
content, tests and evidence, not from summaries. Do not read governance.

## Questions

1. **Tax correctness, computed by hand.** Work independently from the
   2025 Form 1040, Form 8949 and Schedule D instructions and the Qualified
   Dividends and Capital Gain Tax Worksheet (public IRS sources; the
   evidence names them). Compute these cases:
   - wages plus one box E sale, Exception 1 answered truthfully (D1);
   - a sale netting to zero beside a $1,000 box 2a distribution (D2);
   - a box C sale with zero proceeds and zero basis (D3);
   - a direct line 8a sale with a box 1g wash amount (D4);
   - a covered long-term sale (D5);
   - box 4 withholding on one statement, a second sale on a new statement;
   - a box 7 loss.

   Run each through the real coordinator on core v82 with synthetic
   `demo.*` findings. Compare Schedule D lines 1a-16, Form 1040 lines 7a,
   15, 16, 24, 25b, 33, 34 and 37. Say whether any expected value in
   tests/fixtures/sale_family_audit_v82/expected.json is wrong.
2. **Admission.** Can any combination of answers publish a wrong number,
   or a number while a sale fact is unread? Try at least: rows on a
   different transaction; a box 4 or box 7 answer left over after a new
   statement; an Exception 1 answer beside a recorded sale; a removed sale.
   Does any v81 answer change meaning?
3. **The audit test.** Does the committed fact-field/consumer audit fail
   if a sale fact field loses its last reader? Mutate one locally to show
   it. Is every allowlisted unread field's reason true?
4. **Immutability.** Run `git diff github/main --stat` over
   packages/content and packages/schemas. Is registry v80 add-only? Is the
   loader change limited to the per-core v82 entries?
5. **What the filer sees.** For every blocked line: is the reason
   non-empty and true? Is every new or reworded question's "yes" the
   fact's "yes", and plain? Is every new `explain` sentence true of its
   rule's `when`?
6. **CI cost.** The live module makes about 694 coordinator runs (about
   11 minutes on 10 workers) and its fixture is 1.8 MB. Name redundant
   cases or runs that test nothing a sibling does not, and say how far it
   can shrink without losing a Track 0 row's witness.
7. **Test isolation.** Do the new modules assign any other evidence
   module's globals, at import or otherwise? CI runs several modules in
   one process.
8. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`, and check
   that no committed file has an absolute or temp-directory path. Do not
   write such a path in the review either.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/sale-family-audit/review.md, committed (staging the explicit
path, under the collaboration-commit lock). For each finding give:
file:line; a reproduction; a severity (blocking, should-fix or note); the
fix you would make. End with a verdict: ready, or the blocking list.
