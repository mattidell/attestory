# Charter: repair of head of household needs a qualifying person

Role: Builder. Source HEAD on milestone/hoh-qualifying-person-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-qualifying-person.md
(Decision 7). Review: docs/reviews/hoh-qualifying-person/review.md
(HOH-R1 to R6). Do not read governance.

v98 is not on main, so its files are regenerated in place on this branch
(no successor version): core v98, registry v96 and release v96 keep their
version numbers, and their checksums and digests are regenerated.

## Scope

1. **Wording (R1-R4).** In `hoh-qualifying-person-evidence/design.py`, set
   `HOH_QUESTION` and `QSS_QUESTION` to exactly the two texts below, and
   correct `NOTES_V2` (R5): the preferential-rate ceilings themselves
   (Qualified Dividends and Capital Gain Tax Worksheet lines 6 and 13) read
   filing status directly and still show that status's ceiling after a
   no or no answer, but every worksheet line that combines a ceiling with
   taxable income (line 7 onward) is downstream of this rule and blocks,
   so no amount on the return uses them.
2. **Regenerate** the v98 content with P0's `build.py` (through the
   validating generator), replacing this branch's v98 question, rule,
   package, registry and release files. Confirm by diff that only the two
   question texts, the rule notes and the checksums and digests that
   depend on them changed.
3. **Tests.** Update any test that pins the question texts or digests.
   Add a live test that changes an answer from yes to no and sees line 12e
   refuse (the reviewer noted this is untested). Run the milestone's two
   test modules, `tests/test_schema_registry.py`, the v78 switch test,
   the fast lane (`pytest -m "not live"`) and `python3 -m mypy`. Run the
   full replay again only if a non-question value changed.
4. **Docs.** In track1.md, add the full-suite and mypy result lines from
   Track 1 (7288 passed, 25 skipped, 10986 subtests passed in 1828.75s;
   mypy: no issues in 524 source files) and a short Repair section. In
   p0.md and the plan's P0 result, correct the ceilings claim as in (1).

## Texts

HOH_QUESTION:

> You chose head of household. Answer yes only if all three of these apply. (1) You were unmarried on December 31, 2025, or you were married but your spouse did not live in your home at any time during the last 6 months of 2025 and your child, stepchild or foster child whom you can claim as a dependent (or could claim except that the child's other parent claims them) lived in your home for more than half of 2025. If your spouse died in 2025, you count as married for all of 2025 and cannot answer yes. (2) You paid more than half the cost of keeping up your home for 2025, or, if your qualifying person is your dependent parent, more than half the cost of your parent's main home for all of 2025. (3) A qualifying person lived with you for more than half of 2025 (a dependent parent need not live with you): your qualifying child, or a relative you can claim as a dependent who is your parent, brother, sister, half brother, half sister, stepbrother, stepsister, grandparent, aunt, uncle, niece, nephew or in-law. Someone who is your dependent only because they lived with you all year, or whom you claim only under a multiple support agreement, is not a qualifying person. If any of these does not apply, you cannot file as head of household: change your filing status (if you were married, that is usually married filing jointly or married filing separately).

QSS_QUESTION:

> You chose qualifying surviving spouse. Answer yes only if all of these apply: your spouse died in 2023 or 2024 and you did not remarry before the end of 2025; you could have filed a joint return with your spouse for the year your spouse died; you have a child or stepchild (not a foster child) whom you can claim as a dependent, or could claim except that the child had gross income of $5,200 or more, filed a joint return, or you can be claimed as someone else's dependent; that child lived in your home all of 2025, apart from temporary absences such as school (a child born or who died in 2025 counts if the child lived there for the part of the year the child was alive); and you paid more than half the cost of keeping up that home for 2025. If any of these does not apply, you cannot file as a qualifying surviving spouse: change your filing status (if your spouse died in 2025, you can file a joint return for 2025).

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Never edit a file published on main.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push and no spawn.
