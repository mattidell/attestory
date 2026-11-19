# Charter: fresh review of box C and F losses are limited and carried

Role: Reviewer, fresh context. Source HEAD on
milestone/cf-loss-limit-2025. Plan:
docs/phases/engine-breadth/milestones/cf-loss-limit.md (read it whole).
Evidence: cf-loss-limit-evidence/p0.md, track1.md, scripts and JSON.
Range: `github/main..HEAD`. Do not read governance.

## Questions

1. **Hand values.** Are P0's hand values right by the 2025 Schedule D
   instructions in the local sources (lines 7, 15, 16, 21; Form 1040
   lines 7a and 15), for every filing status, including married filing
   separately at and above $1,500 and a split short/long-term loss? Are
   they computed independently of engine output?
2. **Tests.** Do the tests assert hand values rather than captured
   engine output? Would they fail if box C/F stopped reaching line 21,
   if the separate-return limit became $3,000, or if a 2026 carryover
   were published? Mutate in memory or in a scratch copy to check; do
   not commit mutations. Is the dependency of tests on evidence-dir
   scripts (cases.py, hand.py) sound and isolated?
3. **Decisions.** Is narrowing to the limit (Decision 1) supported by
   P0, and are the parked carryover and wording questions stated
   accurately?
4. **Cost.** Is the live module's run cost honest and proportionate?

## Output

docs/reviews/cf-loss-limit/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (CFL-R1 …) each with file:line,
a concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir …
rmdir), staging that one path. No code edits, no push, no spawn.
Synthetic demo.* only; no absolute paths in committed files.
