# Charter: fresh-reader review of Form 1099-B box 7 beside a loss

Role: Reviewer. Source HEAD on milestone/f1099b-box7-loss-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/f1099b-box7-loss.md (read it whole).
You have not seen the build, so judge from the committed content, tests
and evidence, not from summaries. Do not read governance.

## Questions

1. **Tax correctness, computed by hand.** Work independently from the
   2025 Form 1099-B (box 7, recipient instructions), Form 8949 and
   Schedule D instructions (public IRS sources). Compute these cases on a
   single filer with $50,000 wages and $4,500 withholding:
   - box 7 yes, one covered short-term gain;
   - box 7 yes, one long-term loss (must not publish a loss);
   - box 7 yes, a code W sale whose wash brings column (h) to zero;
   - box 7 yes on a gain statement, box 7 no on a loss statement;
   - box 7 yes, a gain and a loss on one statement;
   - box 7 unanswered beside a gain.

   Run each through the real coordinator on core v84 with synthetic
   `demo.*` findings. Compare Schedule D lines 1a-16 and 21 and Form 1040
   lines 7a, 15, 16, 24, 33, 34 and 37. Say whether any expected value in
   tests/fixtures/f1099b_box7_loss_v84/expected.json is wrong.
2. **Admission.** Can any combination of answers publish a loss from a
   box 7 "yes" statement, or a number while a box 7 answer is unread? Try
   at least: a loss sale moved between statements; a box 7 answer keyed
   to a statement with no sale; a "yes" changed to "no" and back; a
   basis correction that turns a gain into a loss; each of the eight sale
   families. Does any v83 answer change meaning?
3. **What the filer sees.** For a box 7 loss refusal: is the reason
   non-empty, true and actionable? Is the line 16 field explanation true
   of its rule's `when`? Is anything asked that cannot help?
4. **Design weight.** Line 16 v4 requires 16 symbols it does not read
   (`tools/required_versus_read_allowlist.json`). Is each a true guard? Is
   the 16-rule shape (eight verdicts, eight checks) the smallest that
   works, or is there a smaller content shape?
5. **Immutability.** Is registry v82 add-only, every new citizen
   byte-identical to prototype.py's decided build, and the loader change
   limited to the v84 entries? Is `git diff github/main --stat` over
   packages/schemas empty?
6. **The audit test.** Does the extended sale-fact audit fail if the box
   7 answer loses its value-side reader? Mutate in memory to show it.
7. **CI cost.** The live module reruns the 298 recorded v83 runs on v84
   (about 450 s of pytest time) beside 89 Track 0 runs. Name runs that
   test nothing a sibling does not, and say how far it can shrink without
   losing a Track 0 row's witness or the v83-identity claim.
8. **Test isolation.** Do the new modules assign any other evidence
   module's globals?
9. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Write no
   absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/f1099b-box7-loss/review.md, committed (explicit path, under
the collaboration-commit lock; retry with backoff if held). For each
finding give: file:line; a reproduction; a severity (blocking, should-fix
or note); the fix you would make. End with a verdict: ready, or the
blocking list. Make no other edits.
