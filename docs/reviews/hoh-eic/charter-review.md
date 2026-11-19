# Charter: fresh review of the earned income credit for a head of household

Role: Reviewer, fresh context. Source HEAD on milestone/hoh-eic-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-eic.md (read it whole).
Evidence: hoh-eic-evidence/p0.md, track1.md, scripts and JSON. Range:
`github/main..HEAD`. Do not read governance.

## Questions

1. **Both questions, adversarially.** Are the not-married question and the
   separated-spouse question true to the 2025 Form 1040 line 27a
   instructions, Publication 596 and Publication 501? Every example and
   condition in them is a claim; check each against a source line. Build
   the cases where they would mislead: a spouse who died in 2023, an
   annulment, a decree of separate maintenance, a married filer living
   apart under no agreement, a nonresident spouse, a married filing
   separately filer with a counted child. Does each "no" say what happens?
2. **Too favourable or against the filer.** After v99, can a married head
   of household without a qualifying child reach a credit above $0? Can an
   unmarried one still be given $0? Do single, married filing jointly,
   qualifying surviving spouse and married filing separately keep every
   v98 value, and is anyone newly asked a question who was not before
   (besides the two intended cases)?
3. **The size cap.** Track 1 raised `test_rule_files_stay_under_5kb` to
   7,000 bytes for `rule.eic-gate-result.v3.json` only. Is that honest, or
   should the rule be smaller? Say which.
4. **Publication.** Only new files under packages/content and the release;
   no published file modified; package, registry and release validate; the
   loader's v99 entries carry v98's exactly; no validator successor-graph
   entry needed.
5. **Replay and tests.** Do the replay (775 pass, 0 unexpected; two
   unused expectations) and P0's two added checks support "nothing else
   changed", or could those checks hide a value change? Do the tests fail
   if a married answer gets the credit, if an unmarried one gets $0, if the
   question is asked of single, or if v99 admits another change? Mutate in
   a scratch copy; do not commit mutations.

## Output

docs/reviews/hoh-eic/review.md: a verdict (READY, READY with notes, or
NOT READY), numbered findings (EIC-R1 …) each with file:line, a concrete
failure scenario and a severity, and what you ran. Commit it under
`$(git rev-parse --git-dir)/collaboration-commit.lock` with separate
simple commands (mkdir lock; git add that one path; git commit -F file;
rmdir lock). Bound every command that can hang; never `rm -rf`. No code
edits, no push, no spawn. Synthetic demo.* only; no absolute paths in
committed files.
