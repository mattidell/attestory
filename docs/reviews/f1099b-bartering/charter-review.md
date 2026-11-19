# Charter: fresh review of a Form 1099-B bartering amount is not lost

Role: Reviewer, fresh context. Source HEAD on
milestone/f1099b-bartering-2025. Plan:
docs/phases/engine-breadth/milestones/f1099b-bartering.md (read it
whole). Evidence: f1099b-bartering-evidence/p0.md, track1.md, scripts
and JSON. Range: `github/main..HEAD`. Do not read governance.

## Questions

1. **The sentence, adversarially.** Is the added sentence true and
   sensible wherever a filer sees it (each of the five questions, on
   the saved page, in every state the page draws them)? Build the
   states where it would mislead: a filer with a barter amount who is
   not in business, a box 13 of 0, a Form 1099-B with box 13 and a
   sale, a filer who received bartering not on a Form 1099-B. Is
   refusing through the business answer honest, and does the page then
   tell the filer why the return stopped?
2. **Silently wrong.** After v97, can a filer with a box 13 amount who
   reads the questions still reach a computed return that leaves the
   income out? Is the remaining gap (box 13 cannot be recorded) stated
   plainly in the plan and parked list?
3. **Publication.** Only new files under packages/content and the
   release; no published file modified; package, registry and release
   validate; `packages/tax/loader.py` v97 entries carry v96's exactly.
   Is no validator successor-graph entry truly needed?
4. **Replay and tests.** Does the full-surface replay (775 pass, 0
   unexpected; six unused expectations) support "nothing else
   changed"? Do the tests fail if the sentence is dropped from one of
   the five questions, if the yes answer stops refusing, or if v97
   admits another change? Mutate in memory or in a scratch copy; do not
   commit mutations.

## Output

docs/reviews/f1099b-bartering/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (BART-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you
ran. Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir), staging that one path. No code edits, no push, no
spawn. Synthetic demo.* only; no absolute paths in committed files.
