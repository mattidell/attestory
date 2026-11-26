# Charter: Track 1 of evidence probes find questions by structure

Role: Builder. Source HEAD on milestone/question-filter-2025. Plan:
docs/phases/engine-breadth/milestones/question-filter.md (read whole;
Decisions 1-2 govern). Do not read governance.

## Scope

1. Replace the "?" filters in
   `docs/phases/engine-breadth/milestones/blocked-names-question-evidence/common.py`
   and `preferential-base-reason-evidence/probe.py` with one shared rule
   (Decision 1). Prefer a small helper both import, in the
   blocked-names-question evidence directory, over two copies.
2. Run every test that loads these probes:
   tests/test_blocked_names_question_v89.py,
   tests/test_blocked_names_question_v89_package.py,
   tests/test_preferential_base_reason_v91.py,
   tests/test_preferential_base_reason_v91_package.py,
   tests/test_line16_names_v95.py, tests/test_plain_line_texts_v96.py,
   plus any other `grep -rl` finds. Re-pin only what Decision 2 allows.
3. A unit test (fast lane) of the helper: a v3 model with an imperative
   linked question, a "?" sentence that is not linked, and a pre-v3 model.
4. `docs/phases/engine-breadth/milestones/question-filter-evidence/track1.md`:
   the field used and why, every changed count or output with the sentence
   that moved, and test results. A "Track 1 result" section in the plan.
5. Checks: the tests above, fast lane (`pytest -m "not live"`), mypy on
   touched test modules, governance_lint, envelope_scan over
   github/main..HEAD. No full suite (no packages/ change); if you find you
   must touch packages/, stop and report.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/, any published file, or any schema.
- Commit in steps with separate simple commands (mkdir lock; git add
  <paths>; git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf` (not even
  __pycache__). Never --no-verify or a bare git stash. Foreground commands
  only. No push and no spawn.

Final message: DONE or STOPPED, commits, every changed count, test results.
