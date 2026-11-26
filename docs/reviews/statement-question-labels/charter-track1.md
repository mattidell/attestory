# Charter: Track 1 of a per-statement question names the statement

Role: Builder. Source HEAD on milestone/statement-question-labels-2025.
Contract: ADR 0089 (accepted 2026-11-26), Decisions 1-6, which govern.
Plan: docs/phases/engine-breadth/milestones/statement-question-labels.md
(P0 result and Decisions). Evidence: statement-question-labels-evidence/
(p0.md, design.py, replay.py). Do not read governance.

The branch is rebased onto main at core v108 (P0 ran on v106/v107).

## Scope

1. In `packages/derivation/presentation_projection.py`, implement ADR 0089
   in `_closure_question_reasons` and its walk frame: attribute a Form
   1099-B box 4 amount or box 7 question to the unanswered statements by
   calling the evaluator's own `require_paired` test (Decision 4; extract a
   shared helper from the evaluator if needed, without changing its
   behavior), narrow box 4 by the need table (Decision 2), emit one reason
   per statement with `statementLabel` (Decision 3), fail closed
   (Decision 6). No schema, content, number, code or report change.
2. The need table in `packages/tax`, gated to core v106 or later (every
   core that publishes the per-sale `box4-amount-needed` results).
3. Tests: unit tests in the style of `tests/test_same_label_members_walk.py`
   (two and three statements, one statement, duplicate labels, a box 4
   "no" statement not named, fail-closed cases, a pre-v106 core) and a live
   test over a subset of the P0 cases with the page DOM checker
   (`page-plain-words-evidence/check_page_dom.mjs`).
4. Full-surface replay on the built code against the pre-Track-1
   projection, on core v108, one shared run with parallel workers over all
   775 recorded lists plus the P0 cases. Expect only question-reason
   changes on the lists P0 found (141 on v106; report the v108 count and
   explain any difference), 0 unexpected.
5. Checks: this touches packages/derivation, so run the full suite once
   before handing off (in foreground batches of test files if one run hits
   the command time limit); mypy on touched modules; governance_lint;
   envelope_scan over github/main..HEAD.

## Deliverables

Code, tests, `statement-question-labels-evidence/track1.md` (with replay
totals and the full-suite result), a "Track 1 result" section in the plan.
Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/, any published file, or any schema.
- Commit with separate simple commands (mkdir lock; git add <paths>; git
  commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf` (not even
  __pycache__). Never --no-verify or a bare git stash. Foreground commands
  only. No push and no spawn.

Final message: DONE or STOPPED, commits, replay totals, full-suite result,
tests.
