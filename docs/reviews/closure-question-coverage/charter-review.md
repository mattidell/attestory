# Review: P0 and Track 1 of closure question coverage

Role: Reviewer, fresh reader. Source HEAD on
milestone/closure-question-coverage-2025. Plan:
docs/phases/engine-breadth/milestones/closure-question-coverage.md (P0
result, Decisions). Evidence: closure-question-coverage-evidence/
p0-survey-and-design.md and track1.md. Diff: `git diff github/main..HEAD`.
Do not read governance. Apply docs/roles/qualitative-review.md.

Judge, with your own `live_coordinate_run` cases where a claim is testable:

1. **Earlier cores.** Is every v74-and-earlier run unchanged? Look for a path
   where the switch reads the wrong pin (a run with no adoption pin, a
   non-core package, a correction or entry-loop session, a version like
   `v100`), and for any other reader of the BLOCK_ABSENT code on the
   synthesized member validation (explain, dispositions consumers, goldens,
   the entry loop) that now sees a different code on v75.
2. **Correctness on v75.** An unadmitted constrained family now records
   SOURCE_SET_UNCLOSED. Is that true in every case it fires: a family that
   is closed but whose admission failed for another reason (a member
   constraint or identity-exclusivity failure)? If such a family would now
   ask "have you recorded every …?" when the real problem is an invalid
   member, that is a wrong question (required).
3. **The Form 1099-K projection change.** Does it fire only for a
   selection line whose root is an unconfirmed family with a closure
   question, and is the output sorted, distinct and stable?
4. **Layering.** `runner.py` now imports `packages.tax.loader`. Is a
   version switch keyed by package id in the substrate acceptable against
   the existing pattern (live.py already imports it), or should the switch
   be passed in? Recommend, don't rule.
5. **The account.** Do the plan, evidence and tests say what the code does,
   with counts that hold? Published files and manifests add-only?

Write findings to closure-question-coverage-evidence/review.md: required
(wrong answer or question, data safety, published history) and
recommended, each with the case that shows it; notes separately. No
production, test or content edits. Synthetic demo.* only; no absolute
paths in committed files. Commit with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. Run
`python3 tools/envelope_scan.py --range github/main..HEAD`. No push or
spawn.
