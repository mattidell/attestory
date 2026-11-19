# Charter: Track 1 of gains and break-even sales reach Schedule D

Role: Builder. Source HEAD on milestone/gain-break-even-2025.
Plan: docs/phases/engine-breadth/milestones/gain-break-even.md (read it
whole, especially Decision 1). Evidence: gain-break-even-evidence/p0.md,
cases.py, hand.py, compare.py, comparison.json. Precedent for the test
shape: tests/test_cf_loss_limit_v96.py and
tests/test_cf_loss_limit_hand_values.py (and the cf-loss-limit review's
notes on run cost and counts). Do not read governance.

## Scope

1. **Pin the subset** named in Decision 1 (27 returns) through the real
   live coordinator and saved page on published core v96. Assert the
   Form 8949 part totals, Schedule D lines 7, 15, 16, Form 1040 lines
   7a, 15 and 16 against P0's hand values, not captured engine output.
   The code W gain probe must block with its code and no published
   line 16 amount. Mark the module live; share runs across assertions
   and state the per-worker run cost honestly in its docstring.
2. **Fast companion.** Tests that the hand functions (including the tax
   formula against a sample of Tax Table rows and the QDCG worksheet on
   a few synthetic numbers) follow the instructions, independent of the
   engine.
3. **Count honestly.** track1.md states the exact returns, controls and
   test counts the modules run.

No content, schema or engine edits; no package version change.

## Deliverables

tests/test_gain_break_even_v96.py and a fast companion; track1.md in
the evidence directory. Run the new modules, `pytest -m "not live"` and
`python3 -m mypy`; report the lines.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. No edits under packages/.
