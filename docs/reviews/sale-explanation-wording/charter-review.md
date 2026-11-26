# Charter: fresh review of the sale block explanations read plainly

Role: Reviewer. Source HEAD on milestone/sale-explanation-wording-2025.
Plan: docs/phases/engine-breadth/milestones/sale-explanation-wording.md
(read it whole, including "Track 1 result"). Do not read governance.

## Questions

1. **Wording bar.** Read every one of the 30 v2 explanations and 8 v2
   questions. Does each meet the plan's bar? Is each true to the 2025
   Form 8949 and Schedule D instructions and the Form 1099-B box numbers
   it names (box 1d, 1e, 1g, 2, 12; columns (b)-(g))? Does any tell the
   filer to do something wrong or impossible on this product's entry
   surface? Name each sentence you would change and give the change.
2. **Only words moved.** Is the replay method sound (Track 1 open question:
   reasons re-sort by sentence; the replay substitutes the new sentences
   into the v106 output, re-sorts and requires an exact match)? Do the
   controls show it can fail? Any number, disposition or block-code move?
3. **Publication.** New files only; no published file edited; loader v107
   entries carry v106; size guard; registry and release only advance core.
4. **Tests.** Do the new tests fail if a sentence regresses to engine text
   or a link is lost? Is the mechanical bar check sensitive?

Run `python3 tools/envelope_scan.py --range github/main..HEAD`. Run pytest
only to confirm a specific failing claim.

## Output

Final message: verdict READY or NOT READY, findings (id, severity, file:line,
one line, proposed fix), and what you ran. Write nothing to the repo. No
push, no spawn.
