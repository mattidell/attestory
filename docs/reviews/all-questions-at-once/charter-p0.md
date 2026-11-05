# P0: how many rounds of questions a return takes, and why

Role: Builder. Source HEAD on milestone/all-questions-at-once-2025.
Plan: docs/phases/engine-breadth/milestones/all-questions-at-once.md.
Read the plan, `_closure_question_reasons` in
packages/derivation/presentation_projection.py, how the runner records
`requires` and `when` blocks (packages/derivation/runner.py), the
scope-answer-questions and closure-question-coverage tests for harnesses
(tests/test_scope_answer_questions.py, tests/test_closure_question_coverage.py,
tests/helpers/current_core_returns.py). Do not read governance or unrelated
proposals.

Assigned evidence only:
docs/phases/engine-breadth/milestones/all-questions-at-once-evidence/
(p0-rounds-and-design.md, probe scripts and their outputs).

1. Build a round loop on core v75: run `live_coordinate_run`, collect every
   question sentence on every blocked line, answer exactly those (scope
   answers with the value a typical filer gives, amounts with a synthetic
   value, closures confirmed), and run again, until no line is blocked on a
   filer question or nothing new appears. Record each round's questions.
2. Run it from at least: every scope answer withheld; every amount answer
   withheld with families open; a mortgage, a Form 1099-B, a dependent and
   a foreign-tax return, each from empty. Count rounds.
3. For every question first shown after round one: the rule that hid it,
   the mechanism (a static `requires` checked after another, a raised `ref`
   inside an expression, a `choose` branch, a guard), and whether it was
   knowable in round one (does not depend on an earlier answer). Classify
   knowable versus truly conditional.
4. Design the smallest change that shows the knowable ones in round one:
   content (successor rules), runner (record every missing `requires`), or
   evaluator. Prototype on a scratch copy outside the repo or behind a
   local flag you do not commit; count rounds before and after, and confirm
   complete returns compute the same amounts.
5. Say what a truly conditional question looks like to the filer and
   leave it.

No production, test, content or schema edits. Stop after measurement and
design if the change needs a schema, expression-operation, runner,
evaluator or projection change, and report. Synthetic demo.* only; no
absolute paths in committed files. Commit evidence incrementally with
explicit paths under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir; if held, retry every 10 s up to 5 min, never remove
another holder's lock); never --no-verify; never bare git stash.
Foreground commands only; no `pgrep` or sleep waiters. No push or spawn.
Report the rounds table, the hidden-question list with mechanism and
classification, the design, the counts and limitations.
