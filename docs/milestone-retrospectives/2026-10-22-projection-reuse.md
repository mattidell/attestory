# Retrospective — Fold Once: Less Replaying of the Same History

## Result

- **One projection per operation.** Recording, review and correction no longer
  re-project the same act history in their helpers. On the long synthetic
  history, save, correct and withdraw fold the log once instead of three or
  four times, and their CPU fell 60–72% (save 0.91s to 0.36s, correct 0.79s to
  0.22s, withdraw 0.57s to 0.22s); record and remove fold twice instead of four
  times. Reuse ends when the call returns; public functions still project
  freshly on their own; historical-prefix reads are unchanged.
- **Fast-lane warm-up.** A once-per-worker warm-up in test setup, only for
  fast-lane runs, absorbs the cold first-use cost (2.4s on a worker's first
  derivation call, 0.03s afterwards). Six classes (19 tests) returned to the
  fast lane; on the CI runner `quick` ran 1,528 tests in 23s, against 1,509 in
  30s before.
- **Suite.** A local full run passed (3,171 tests, 5,249 subtests) using 3,125s
  of CPU and 403s of wall time, against 3,488s and 426s for the previous
  milestone's comparable run. Single local runs, not a controlled comparison.
- **Not done.** The save-path incremental fold (Track 1) was skipped: P0 put it
  under 5% of folded acts, and its exact-refusal requirement made it the
  riskiest change for the smallest gain.

## What the evidence changed

The plan expected the save path and the helpers to share the cost. P0 found
helpers re-projecting within one operation were about 91% of folded acts; the
save path checked nothing on answer, correction and withdrawal saves. Measuring
before choosing moved the work to the right place again.

## Material dissent and repairs

Independent review of Track 2 found one overstated claim: the design note
called a `revision == len(staged)` check in `_commit` concurrency protection,
but `append_batch` has already refused any stale or concurrent save by then.
The note was corrected; the code was sound.

## Lessons

- Reusing a state inside one call exposes helpers that never advanced their own
  local state because a fresh projection always followed. Two such helpers had
  to be fixed before their state could be reused; look for that pattern first.
- A warm-up only helps tests that share what it warms: classes validating a
  different package kept their marks. Measure warm call times per class before
  returning a test to the fast lane, with a margin for the CI runner.

## Follow-ups

- The save-path incremental fold, if a later ranking shows it matters, with
  today's exact refusal timing preserved by differential tests.
- Remaining helper re-projections not in Track 2's named sites
  (`_stage_enrollment_follows_schooling` inside `_commit_save`,
  `_scan_displayed_answers`, `_attribute_borrowing_labels`).
- A cross-call prefix memo, only if projection still dominates a new ranking.
- Current-lattice rebuilds after the fact state changes.
