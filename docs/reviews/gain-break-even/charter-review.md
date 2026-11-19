# Charter: fresh review of gains and break-even sales reach Schedule D

Role: Reviewer, fresh context. Source HEAD on
milestone/gain-break-even-2025. Plan:
docs/phases/engine-breadth/milestones/gain-break-even.md (read it
whole). Evidence: gain-break-even-evidence/p0.md, track1.md, scripts
and JSON. Range: `github/main..HEAD`. Do not read governance.

## Questions

1. **Hand values.** Are P0's hand values right by the 2025 Form 8949,
   Schedule D and Form 1040 instructions in the local sources (part
   totals, Schedule D lines 7, 15, 16, Form 1040 lines 7a, 15, 16, the
   qualified-dividends-and-capital-gain worksheet), including the joint
   0 % band case and the mixed returns? Are they independent of engine
   output?
2. **Census.** Is the claim that no v96 test runs a gain or break-even,
   and that the long-term no-Form-1099-B break-even never ran, sound?
3. **Tests.** Do the tests fail if a gain path stopped reaching
   Schedule D, if a break-even published a nonzero line, if the QDCG
   path were skipped, or if the code W gain stopped blocking? Mutate in
   memory or in a scratch copy; do not commit mutations. Is the code W
   probe's assertion (rule plus `DEPENDENCY_INVALID`, not the reason
   code) strong enough?
4. **Decisions and bounds.** Are Decision 2's bounds (break-even files
   Schedule D despite Exception 1 yes; worksheet intermediates) correct
   by the instructions?
5. **Cost and counts.** Are run cost and counts stated honestly?

## Output

docs/reviews/gain-break-even/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (GBE-R1 …) each with file:line,
a concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir …
rmdir), staging that one path. No code edits, no push, no spawn.
Synthetic demo.* only; no absolute paths in committed files.
