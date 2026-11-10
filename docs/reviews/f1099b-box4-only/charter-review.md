# Charter: fresh-reader review of Form 1099-B backup withholding without a sale

Role: Reviewer. Source HEAD on milestone/f1099b-box4-only-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/f1099b-box4-only.md (read it whole).
You have not seen the build, so judge from the committed content, tests
and evidence, not from summaries. Do not read governance.

## Questions

1. **Tax correctness, computed by hand.** Work independently from the
   2025 Form 1099-B instructions (box 4, short sales open at year end) and
   the Form 1040 line 25b instruction (public IRS sources). Compute these
   cases on a single filer with $50,000 wages and $4,500 withholding:
   - no Form 1099-B, the yes/no answered no;
   - one Form 1099-B with $150 box 4 and no closed sale, answered at
     return level;
   - that statement beside a sale statement with $200 box 4;
   - the yes/no unanswered on a return that computed on v84;
   - yes with the amount unanswered;
   - a no-sale statement that later gets a sale.

   Run each through the real coordinator on core v85 with synthetic
   `demo.*` findings. Compare Form 1040 lines 25a-25d, 33, 34 and 37. Say
   whether any expected value in
   tests/fixtures/f1099b_box4_only_v85/expected.json (or the module's
   fixture, whatever its name) is wrong.
2. **Admission.** Can any combination of honest answers publish line 25b
   short of withholding the filer received, or count one dollar twice?
   Try at least: a per-statement amount on a no-sale statement plus the
   return-level answer; a sale added and removed; the yes/no superseded;
   a return-level amount of zero. Does any v84 answer change meaning?
3. **What the filer sees.** Are the two new questions plain, true, and
   enough for a filer to answer once without double counting? Is the line
   25b field explanation true of its rule's `when`? Is the new question
   asked of returns where it cannot help, and is that cost justified?
4. **Design weight.** Is a return-level yes/no plus amount the smallest
   shape that closes the gap without a recording change?
5. **Immutability.** Is registry v83 add-only, every new citizen
   byte-identical to prototype.py's decided build, and the loader change
   limited to the v85 entries? Is `git diff github/main --stat` over
   packages/schemas, packages/kernel and packages/derivation empty?
6. **CI cost.** Name live runs that test nothing a sibling does not, and
   say how far the module can shrink without losing a Track 0 row's
   witness or the 298-run claim.
7. **Test isolation.** Do the new modules assign any other evidence
   module's globals?
8. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Write no
   absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/f1099b-box4-only/review.md, committed (explicit path, under
the collaboration-commit lock; retry with backoff if held). For each
finding give: file:line; a reproduction; a severity (blocking, should-fix
or note); the fix you would make. End with a verdict: ready, or the
blocking list. Make no other edits.
