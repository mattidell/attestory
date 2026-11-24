# Charter: fresh review of a child without a valid SSN routes the earned income credit correctly

Role: Reviewer, fresh context. Source HEAD on
milestone/eic-no-ssn-child-2025. Plan:
docs/phases/engine-breadth/milestones/eic-no-ssn-child.md (read it whole;
Decisions 1-4). Evidence: eic-no-ssn-child-evidence/p0.md, track1.md,
scripts and JSON. Range: `github/main..HEAD`. Do not read governance.

## Questions

1. **The sources, adversarially.** Fetch the 2025 Form 1040 instructions
   (line 27a, Steps 1-6, Worksheet A/B), Schedule EIC and its instructions,
   and Publication 596 into ignored temp/. Is the widened reading right: a
   filer whose qualifying children all lack a valid SSN skips Step 4 (age
   25-64, main home, not claimable as a dependent) and takes the self-only
   column, for every filing status? Read whole sections, including
   exceptions; look for any sentence that sends such a filer to Step 4 or
   chapter 3, or that keeps a Step 4 test for them. Is "could be a
   qualifying child of another person" (Step 3 question 6) still asked on
   that path? Does a married filer still need the separated-spouse test?
2. **Each successor.** For every new or changed rule, is its condition
   exactly the source condition? Can a filer with a counted (valid-SSN)
   child, or with no qualifying child at all, now compute differently
   from v101? Can a filer be newly asked something they were not required
   to answer on v101, or no longer asked something the sources require?
3. **Amounts.** Re-derive by hand from the 2025 EIC table several cases
   at other incomes (phase-in, plateau, phase-out; joint and non-joint),
   including a filer with one valid-SSN child and one without.
4. **Nothing else moved.** Replay: 0 unexpected, and do the declared
   expectations hide a value change? Only new files under packages/content
   and the release; no published file modified; loader v102 entries carry
   v101's.
5. **Tests.** Do they fail if the SSN test moves between `counts` and
   `qualifies`, if Step 4 is applied to a no-SSN-child filer, or if the
   separated-spouse test is skipped for a married filer? Mutate in a
   scratch copy; do not commit mutations.

## Output

docs/reviews/eic-no-ssn-child/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (ENS-R1 …) each with file:line, a
concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` with
separate simple commands (mkdir lock; git add that one path; git commit
-F file; rmdir lock). Bound every command that can hang; never `rm -rf`.
No code edits, no push, no spawn. Synthetic demo.* only; no absolute
paths in committed files.
