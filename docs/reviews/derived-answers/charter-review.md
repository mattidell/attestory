# Review: P0 and Track 1 of derived answers

Role: Reviewer, fresh reader. Source HEAD on milestone/derived-answers-2025.
Plan: docs/phases/engine-breadth/milestones/derived-answers.md (P0 result,
Decisions). Evidence: derived-answers-evidence/p0-trace-and-design.md and
track1.md. Diff: `git diff github/main..HEAD`. Do not read governance.
Apply docs/roles/qualitative-review.md.

Judge, with your own `live_coordinate_run` cases where a claim is testable:

1. The basis. Does each delivered successor (line 12e v4, Schedule 3 line 1
   direct-ftc v4) derive only what the record proves? Try to make it publish
   from a record that does not prove the answer: a Form 1098 with box 1 of
   0, an unclosed family, a joint return, a Form 1099-DIV box 7 exactly at
   300 and 600, box 7 over the cap on a non-joint status that is not single.
2. Answered returns. Does every return that v73 publishes still publish the
   same amounts on v74? Look for a path the Track 1 open-family check did
   not run (other filing statuses, itemized versus standard, the
   contradiction block's other branches on line 12e).
3. The holds. Are the line 2a and other-dependent holds correct, and is the
   line 2a successor's "publishes an unclosed family" observation real?
4. Contradiction (Decision 2). What exactly is lost on line 12e: is
   `F1098_SCOPE_CONTRADICTION` gone in every case, or only some?
5. The account. Do the plan, evidence and tests say what the code does,
   with counts that hold? Are earlier cores and goldens untouched, and are
   published files and manifests add-only?

Write findings to derived-answers-evidence/review.md: required (wrong
answer, data safety, published history) and recommended, each with the
case that shows it; notes separately. No production, test or content edits.
Synthetic demo.* only; no absolute paths in committed files. Commit with
explicit paths under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir; retry every 10 s up to 5 min if held); never --no-verify;
never bare git stash. Foreground commands only; no pgrep or sleep waiters.
Run `python3 tools/envelope_scan.py --range github/main..HEAD`. No push or
spawn.
