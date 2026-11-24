# Charter: fresh review of the sale page observer reads question groups

Role: Reviewer, fresh context. Source HEAD on
milestone/sale-observer-question-groups-2025. Plan:
docs/phases/engine-breadth/milestones/sale-observer-question-groups.md.
Evidence: sale-observer-question-groups-evidence/track1.md. Range:
`github/main..HEAD`. Do not read governance.

## Questions

1. **Same rules as the page.** Read the page's blocked-reason rendering in
   `packages/presentation/pages/citation-walk.v1.html` yourself. Does the
   observer's expected text match it in every branch (question-group link
   and separator, which reasons a group names, member label, statement
   label, plain sentence, a malformed question-ref shape)?
2. **Still a check.** Does the observer still report a difference when the
   page shows the raw sentence where a group names the reason, the link
   where none does, the wrong label, or a missing reason? Mutate a scratch
   copy of the page or of a rendered DOM; do not commit.
3. **Tests.** Are the new unit tests fast-lane, and do they fail on each
   mutation? Do the edited opt-in tests still check what they checked?
4. **Nothing else moved.** Tools and tests only.

## Output

docs/reviews/sale-observer-question-groups/review.md: a verdict (READY,
READY with notes, or NOT READY), numbered findings (SOQ-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you ran.
Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock`
with separate simple commands (mkdir lock; git add that one path; git
commit -F file; rmdir lock). Bound every command that can hang; never
`rm -rf`; leave no Chrome process running. No code edits, no push, no
spawn.
