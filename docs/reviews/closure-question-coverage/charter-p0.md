# P0: which unconfirmed families do not ask their question

Role: Builder. Source HEAD on milestone/closure-question-coverage-2025.
Plan: docs/phases/engine-breadth/milestones/closure-question-coverage.md.
Read the plan, `_closure_question_reasons` and its callers in
packages/derivation/presentation_projection.py and packages/derivation/live.py,
tests/test_scope_answer_questions.py and tests/test_input_questions.py for
the existing harness, and the closure mappings and rules of the families
you find failing. Do not read governance or unrelated proposals.

Assigned evidence only:
docs/phases/engine-breadth/milestones/closure-question-coverage-evidence/
(p0-survey-and-design.md, probe scripts and their outputs).

1. List every source family core v74 reads that has a closure (from the
   package's closure mappings). For each, on a v74 return that publishes
   and records that family (add members where the family needs them to be
   read), remove only its closure assertion and run `live_coordinate_run`.
   Record: lines blocked, each line's root codes, and whether the line
   names the family's completeness question. Also run with no members.
2. For each family that does not name its question, trace why: which rule
   reports the code, and what it reads. Start with
   `f1099b.covered-w-st-txn` and `f1099b.covered-w-lt-txn`.
3. Design the smallest fix: a successor rule or mapping, or a declared
   question. Prototype it on a scratch v75 outside the repo: the failing
   cases now name the question; every confirmed return and every other
   case is byte-identical to v74. Count lines that gain the question and
   any committed fixture or golden that moves.
4. Families whose question wording is missing or misleading: list them and
   stop short of rewording.

No production, test, content or schema edits. Stop if the fix needs a
schema, expression-operation, projection or engine change, and report.
Synthetic demo.* only; no absolute paths in committed files. Commit
evidence incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
if held, retry every 10 s up to 5 min, never remove another holder's lock);
never --no-verify; never bare git stash. Foreground commands only; no
`pgrep` or sleep waiters. No push or spawn. Report the table, the causes,
the design, the counts and limitations.
