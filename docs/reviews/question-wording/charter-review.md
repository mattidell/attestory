# Charter: fresh-reader review of question wording

Role: Reviewer. Source HEAD on milestone/question-wording-2025. This
branch is stacked on #270, so diff against
`github/milestone/selection-keyed-collect-2025` (7fb81080), not main.
Plan: docs/phases/engine-breadth/milestones/question-wording.md (read it
whole, including the Disposition and the Track 1 result). You have not
seen the build, so judge from the committed content, tests and evidence,
not from summaries. Do not read governance.

## Questions

1. **Truth of each sentence, by hand.** From the 2025 Form 1040 and
   Schedule D / Form 8949 instructions, the wash-sale rules, the Schedule
   D Exception 1 conditions, the student loan interest deduction
   worksheet and the standard deduction age and blindness rules (public
   IRS sources), say whether each new question and fact title is true of
   what its consuming rule reads, for everyone it is asked of. Compute at
   least: a covered sale with no wash sale; one with a wash-sale loss
   adjustment beside one without; a zero-net sale with Exception 1
   answered; a joint return whose spouse is claimed; a single filer
   claimed by a parent. Run each through the real coordinator on core
   v87 with synthetic `demo.*` findings and compare the lines the rule
   feeds. Say whether any hand value pinned in
   tests/test_question_wording_v87.py is wrong.
2. **Meaning change.** Does any v86 answer mean something different under
   the v87 words, so a recorded return would now be answered falsely?
   Could a truthful filer reading the new words answer in a way that
   moves a number the wrong way?
3. **What the filer sees.** Are the words plain and short enough to
   answer once? Does any word promise more than the rule does?
4. **Immutability.** Is registry v85 add-only, every new citizen
   byte-identical to prototype.py's decided build, and the loader change
   limited to v87 entries? Is the diff over packages/schemas,
   packages/kernel and packages/derivation empty?
5. **CI cost.** The live module runs 326 coordinator runs in about 334 s.
   Name runs that test nothing a sibling does not, and say how far it can
   shrink without losing a Track 0 row's witness or the 298-run claim.
6. **Test isolation.** Do the new modules load evidence only through
   tests/evidence_loader.py and assign no other module's globals?
7. **The four browser failures** the builder saw in
   tests/test_explanation_saved_browser.py under parallel shards: does
   anything in this diff touch that path?
8. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/milestone/selection-keyed-collect-2025..HEAD`.
   Write no absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/question-wording/review.md, committed (explicit path, under
the collaboration-commit lock; retry with backoff if held). For each
finding give: file:line; a reproduction; a severity (blocking, should-fix
or note); the fix you would make. End with a verdict: ready, or the
blocking list. Make no other edits.
