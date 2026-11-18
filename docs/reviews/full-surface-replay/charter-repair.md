# Charter: repair of the full-surface replay review notes

Role: Builder. Source HEAD on milestone/full-surface-replay-2025.
Plan: docs/phases/engine-breadth/milestones/full-surface-replay.md
(Decision 2). Review: docs/reviews/full-surface-replay/review.md (read
FSR-R1 to FSR-R5 in full). Do not read governance.

## Scope

1. **FSR-R1.** Correct track1.md: the `notes` texts are saved (in
   `mortgageBorrowingExplanation.calculationChain.resolvedContent`).
   State plainly which optional model blocks no recorded list produces
   and that the full-surface claim covers only what the corpus reaches.
   Add one synthetic case (demo.* data) that produces at least the
   mortgage explanation block, and show the snapshot holds it and a
   control changing a `notes` text there fails unless expected.
2. **FSR-R2.** `run_full` (and the `full` CLI) report every unused
   expectation by identity in its summary; add a test.
3. **FSR-R3.** Add controls or tests that fail when the snapshot stops
   comparing the explanation graph, the other model keys, or compares
   values with plain `==` instead of by type (for example 1 against
   1.0 or True). Show in track1.md that each fails against an in-memory
   mutation of the tool (do not commit mutations).
4. **FSR-R4, FSR-R5.** Document as named blind spots in track1.md and
   the tool docstring: hash-keyed edge and pin order; dictionary key
   order (shown on the page only in `recordedApplicableClaims`); path
   masking over every saved string. Fix any of them cheaply if you can
   without weakening a comparison; say which you fixed.
5. **Prove.** Rerun v95 against v96 over all 775 lists: still 775 pass
   and 0 unexpected, with unused expectations listed. Run both replay
   test modules, `pytest -m "not live"` and `python3 -m mypy`; report
   the lines.

No edits under packages/.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
