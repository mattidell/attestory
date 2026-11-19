# Charter: fresh review of head of household needs a qualifying person

Role: Reviewer, fresh context. Source HEAD on
milestone/hoh-qualifying-person-2025. Plan:
docs/phases/engine-breadth/milestones/hoh-qualifying-person.md (read it
whole). Evidence: hoh-qualifying-person-evidence/p0.md, track1.md,
scripts and JSON. Range: `github/main..HEAD`. Do not read governance.

## Questions

1. **The questions, adversarially.** Are the two question sentences
   true to the 2025 Form 1040 instructions and Publication 501, and
   sensible wherever a filer sees them on the saved page? Build the
   cases where they would mislead: a filer who is considered unmarried,
   a dependent parent who lives elsewhere, a qualifying person who is not
   a dependent (for example a qualifying child claimed by the other
   parent), a spouse who died in 2025, a foster child for the surviving
   spouse status. Does a "no" tell the filer what to do next?
2. **Silently wrong.** After v98, can a filer reach head of household or
   qualifying surviving spouse amounts anywhere (standard deduction,
   Tax Table column, preferential ceilings, credits, itemizing routes)
   without answering yes? Does any other rule read filing status for a
   larger amount without passing through
   `rule.dependents-worksheet-line-3`?
3. **Nothing else moved.** Do single, married filing jointly and married
   filing separately read nothing new? Does a yes keep every v97 value?
   Is the parked earned-income-credit finding (Decision 5) stated
   accurately?
4. **Publication.** Only new files under packages/content and the
   release; no published file modified; package, registry and release
   validate; `packages/tax/loader.py` v98 entries carry v97's exactly;
   no validator successor-graph entry is needed.
5. **Replay and tests.** Does the replay (775 pass, 0 unexpected, two
   unused question expectations) support "nothing else changed"? Do the
   tests fail if a "no" stops refusing, if a yes changes a value, if the
   rule reads the answer for single, or if v98 admits another change?
   Mutate in a scratch copy; do not commit mutations.

## Output

docs/reviews/hoh-qualifying-person/review.md: a verdict (READY, READY
with notes, or NOT READY), numbered findings (HOH-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you ran.
Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock`
with separate simple commands (mkdir lock; git add that one path; git
commit -F file; rmdir lock). Bound every command that can hang; never
`rm -rf`. No code edits, no push, no spawn. Synthetic demo.* only; no
absolute paths in committed files.
