# Charter: repair of the box4-no-prompt replay classifier (review F2)

Role: Builder. Source HEAD on milestone/box4-no-prompt-2025.
Plan: docs/phases/engine-breadth/milestones/box4-no-prompt.md, "Review
disposition" (Decisions 9-10). Review: docs/reviews/box4-no-prompt/review.md,
F2. Do not read governance.

## Repair

1. **Strict classifier.** In box4-no-prompt-evidence/classify.py, before
   any expected label is assigned, compare every row of the two pins
   (all rows, including rows present on only one side) and fail the list
   as `unexpected` on any changed value, outcome, disposition, refusal
   code, or an added or removed row. The only permitted differences are:
   line 25b's (and rows that explain through it) `missing` name moving
   from `f1099b.statement-box4-withholding` to the return-level
   `no-sale-box4-present` question, and the box 4 amount sentence v1 →
   v2 text. Keep the separate counters and make them count added and
   removed rows.
2. **Mutation check.** A small evidence script (or a fast test under
   tests/ if it fits the 3.0 s budget) that feeds the classifier the
   review's three mutations (25b disposition change, 25b code change,
   a value 0 → 999 on a no-without-amount list) and an added and a
   removed row; each must be `unexpected`. The real pin pairs must keep
   their labels.
3. **Reclassify.** Rerun the classification over the saved Track 1
   775-list replay. If the saved replay does not hold full rows, rerun
   it with `python3 tools/recorded_replay.py` in parallel (CPU count
   minus one workers), part file outside the repo, and report wall time.
   Commit the new classification and update the counts in
   track1-result.md and the plan's Track 1 result if any change.
4. **Checks.** Run the touched tests, `pytest -m "not live"`,
   `python3 -m mypy` if Python under tests/ changed, and
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Add a
   "Review repair" paragraph to the plan.

Stop and report if the strict classifier finds any unexpected change.

## Rules

- No content, package, loader or production edits.
- Synthetic demo.* only; no absolute or temp-directory paths in
  committed files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s up to 5 min if held).
- Never --no-verify or a bare git stash. Foreground only: never end your
  turn while a command is running. No push, no spawn.
