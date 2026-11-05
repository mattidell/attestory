# Review: P0 and Track 1 of all questions at once

Role: Reviewer, fresh reader. Source HEAD on
milestone/all-questions-at-once-2025. Plan:
docs/phases/engine-breadth/milestones/all-questions-at-once.md (P0
result, Decisions). Evidence: all-questions-at-once-evidence/
p0-rounds-and-design.md and track1.md. Diff: `git diff github/main..HEAD`.
Do not read governance. Apply docs/roles/qualitative-review.md.

Judge, with your own `live_coordinate_run` cases where a claim is testable:

1. **Earlier cores.** Is every v75-and-earlier run byte-identical? Look for
   a path where `record_later_any_refs` or the closure-check witness
   preference turns on without the v76 pin (no adoption pin, a non-core
   package, a correction or entry-loop session, a version like `v100`), and
   for any Environment built outside `_Run.env()` that could differ.
2. **Presence, never absence.** A later-arm ref is recorded only while a
   count is blocked and a compared set already has a member. Find a case
   where v76 asks for an amount the return has no statement for (a return
   with no W-2 asked for box 2; a Form 1099-DIV box 4 asked with no
   Form 1099-DIV), or asks a conditional question before the answer it
   depends on (`choose`, `conditional_dependency_set`, nested `any` or
   `all`). Either is a wrong question (required).
3. **Values.** Does any v76 return publish an amount different from v75 on
   the same inputs, or does a complete return differ in anything but the
   adopted package? Does the witness preference change a published
   disposition code a consumer reads (explain, the entry loop, goldens)?
4. **The evaluator change.** `any` under the switch must return what the
   short-circuiting `any` returns, and raise only where it raised before.
   Check the merged `missing` list: distinct, ordered, and does
   `later_refs` leak onto a row whose block was not a count?
5. **The account.** Do the plan, evidence and tests say what the code does,
   with round counts that hold (amounts 4→2, mortgage 4→2, Form 1099-B
   4→3, dependent 6→5, foreign tax 6→5)? Is the foreign-tax deviation from
   the prototype (6) explained correctly? Published files and manifests
   add-only? The allowlist additions justified?

Write findings to all-questions-at-once-evidence/review.md: required
(wrong answer or question, data safety, published history) and
recommended, each with the case that shows it; notes separately. No
production, test or content edits. Synthetic demo.* only; no absolute
paths in committed files. Commit with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. Run
`python3 tools/envelope_scan.py --range github/main..HEAD`. No push or
spawn.
