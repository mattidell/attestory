# Charter: fresh review — every line speaking plainly (core v96)

Role: Reviewer, fresh context. Source HEAD on
milestone/plain-line-texts-2025, against github/main (core v95).
Plan: docs/phases/engine-breadth/milestones/plain-line-texts.md (read it
whole). Read docs/roles/reviewer.md and docs/roles/qualitative-review.md.
Do not read governance. You did not build this; review the artifact, not
the reports.

## Questions

1. **Truth to the filer.** Read every one of the 57 published sentences
   (track0-wording.json) in at least one drawn state you build yourself
   through the real live coordinate run and saved page, choosing the
   states most likely to make it false (absence versus rounding, spouse
   records, a corrected answer, a guard that does not apply). Report any
   sentence that claims something the return does not have, or drops the
   basis the old sentence gave.
2. **Only words changed.** Confirm each of the 50 content successors
   differs from its predecessor only in the manifest's properties (and
   the version), and the package replaces exactly those 50 members. Confirm
   the validator change is exactly Decision 5 and the three re-pinned
   tests pin what this build publishes rather than loosening a check.
3. **Replay claim.** Recompute the classification from the committed
   track1 evidence, and re-run the strict classifier on a sample of at
   least 40 recorded lists live on published v95 and v96 yourself.
4. **Tests.** Do the new tests fail if a sentence reverts, a value
   changes, or the v96 entry is removed? Mutate and run them to show it.
5. **Scope and debt.** Anything parked that should not be, any rule or
   definition now written twice, any absolute path or non-demo data.

Run `pytest` only on specific modules to confirm a specific claim; CI
`verify` is the full-suite gate. Write findings with severity (blocking,
should-fix, note) and a verdict READY or NOT READY in
docs/reviews/plain-line-texts/review.md and commit it, staging explicit
paths, under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir). Do not edit anything else. No push, no spawn, no
--no-verify, no bare git stash. Foreground commands only.
