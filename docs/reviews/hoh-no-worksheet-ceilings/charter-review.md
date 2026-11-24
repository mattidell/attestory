# Charter: fresh review of a refused head of household status does not set the worksheet ceilings

Role: Reviewer, fresh context. Source HEAD on
milestone/hoh-no-worksheet-ceilings-2025. Plan:
docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md (read it
whole; Decisions 1-4). Evidence: hoh-no-worksheet-ceilings-evidence/p0.md,
track1.md, scripts and JSON. Range: `github/main..HEAD`. Do not read
governance.

## Questions

1. **The sources.** Fetch the 2025 Form 1040 instructions (filing status,
   head of household and qualifying surviving spouse tests, Qualified
   Dividends and Capital Gain Tax Worksheet lines 6 and 13) into ignored
   temp/. Is a block, rather than another status's ceiling, right for a
   refused or unanswered status? Are the published ceilings the 2025
   amounts for every status?
2. **Each successor.** Does each read exactly what standard-deduction line
   3 reads for the same refusal? Can a single, joint or separate filer, or a
   head of household or surviving spouse who answered "yes", now compute or
   be asked differently from v103? Is a filer newly asked anything?
3. **Downstream.** What do the lines that read 6 and 13 (7, 8, 14 onward,
   and the tax on line 16) show for a refused status, and is the page
   explanation still the status question rather than a raw ceiling?
4. **Nothing else moved.** Replay 0 unexpected; do declared expectations
   hide a value change? Only new files under packages/content and the
   release; no published file modified; loader v104 entries carry v103's;
   the fast size guard covers the two successors.
5. **Tests.** Do they fail on each mutant (refused status publishes its
   ceiling; falls back to the single ceiling; a control status blocks)?
   Mutate scratch copies; do not commit.

## Output

docs/reviews/hoh-no-worksheet-ceilings/review.md: a verdict (READY, READY
with notes, or NOT READY), numbered findings (HNW-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you ran.
Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock` with
separate simple commands (mkdir lock; git add that one path; git commit -F
file; rmdir lock). Bound every command that can hang; never `rm -rf`. No
code edits, no push, no spawn. Synthetic demo.* only; no absolute paths in
committed files.
