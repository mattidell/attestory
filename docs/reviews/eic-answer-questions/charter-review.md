# Charter: fresh review of every earned income credit answer has a question

Role: Reviewer, fresh context. Source HEAD on
milestone/eic-answer-questions-2025. Plan:
docs/phases/engine-breadth/milestones/eic-answer-questions.md (read it
whole). Evidence: eic-answer-questions-evidence/p0.md, track1.md,
scripts and JSON. Range: `github/main..HEAD`. Do not read governance.

## Questions

1. **The four questions, adversarially.** Is each true to the 2025 Form
   1040 line 27a instructions and Publication 596? Every condition and
   example is a claim; check each against a source line. Build the cases
   where one misleads: a filer born January 1, 1961; a spouse who died in
   2025 at 64; a joint return where only one spouse meets the age test; a
   military member abroad; a filer someone could claim but who files only
   for a refund; a spouse with an ITIN or a "Valid for Work Only With DHS
   Authorization" card. Is the dependent question's yes/no polarity
   recorded correctly (a yes must stop the credit)?
2. **Census.** Is P0's census complete: after v100, does any credit
   answer the engine requires still lack a question, other than the
   parked counted-child answers? Is anyone newly asked something they were
   not required to answer on v99?
3. **Nothing else moved.** Does every answered return compute as on v99?
   Does any recorded or probe return newly block or change a number?
4. **Publication.** Only new files under packages/content and the
   release; no published file modified; the loader's v100 entries carry
   v99's exactly; no validator successor-graph entry needed.
5. **Tests.** Do the tests fail if a question is dropped from v100, if
   the dependent polarity is reversed, or if a question names the wrong
   fact? Mutate in a scratch copy; do not commit mutations.

## Output

docs/reviews/eic-answer-questions/review.md: a verdict (READY, READY
with notes, or NOT READY), numbered findings (EAQ-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you ran.
Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock`
with separate simple commands (mkdir lock; git add that one path; git
commit -F file; rmdir lock). Bound every command that can hang; never
`rm -rf`. No code edits, no push, no spawn. Synthetic demo.* only; no
absolute paths in committed files.
