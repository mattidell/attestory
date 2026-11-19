# Charter: Track 1 of every earned income credit answer has a question

Role: Builder. Source HEAD on milestone/eic-answer-questions-2025.
Plan: docs/phases/engine-breadth/milestones/eic-answer-questions.md (read
it whole, especially the P0 result and Decisions 2-4). Evidence:
eic-answer-questions-evidence/p0.md and its scripts. For how content
successors are published, follow the most recent content milestone,
hoh-eic (core v99). Do not read governance.

## Scope

1. **Publish** core v100, registry v98, release v98: the four input
   questions exactly as P0 words them, nothing else. New files only; never
   edit a file published on main. Add the loader's v100 entries (carry
   v99's) and check the validator's `_successor_graphs` table.
2. **Tests.** A live test module on v100 through the real coordinator and
   saved page, with no answer pre-filled that the test is about: for each
   of the four answers, a return where it is required and missing shows
   its question on the page and still blocks the same lines as v99; a
   return that answers it computes exactly as v99 (hand values for one
   single and one joint case). A fast package test that v100 admits exactly
   the four questions against v99. Re-pin any test that pins the current
   core version.
3. **Replay.** Full-surface replay of the 775 recorded lists, v99 against
   published v100, and P0's probe lists. Report pass/unexpected and unused
   expectations.

No engine, schema, projection, rule or page edits.

## Deliverables

Content under packages/content/tax/2025/, tests, and track1.md in the
evidence directory. Run the full suite (`pytest`), `python3 -m mypy` and
`pytest tests/test_schema_registry.py` after your last edit, and put the
result lines in track1.md.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`. Never raise
  `FAST_LANE_BUDGET_SECONDS` or a size cap; report instead.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push and no spawn.
