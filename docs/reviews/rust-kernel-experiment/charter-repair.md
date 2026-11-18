# Charter: repair of the Rust kernel experiment review notes

Role: Builder. Source HEAD on milestone/rust-kernel-experiment-2025.
Plan: docs/phases/engine-breadth/milestones/rust-kernel-experiment.md
(Decision 5). Review: docs/reviews/rust-kernel-experiment/review.md
(RKE-R1 to RKE-R3; read each in full). Do not read governance.

## Scope

1. **RKE-R1.** Add a deterministic `ClosureWalkMemo` test with the
   review's two-path synthesized-meaning graph. Show in track1.md that
   it fails when `frame.hits.isdisjoint(seen)` is removed and when
   `seen.isdisjoint(known.examined)` is removed (mutate in memory or in
   a scratch copy; do not commit the mutation).
2. **RKE-R2.** Make the validation memo safe for any caller: include a
   digest of the corpus actually validated in the key, or verify inside
   `_validate_once` that the corpus matches `citizen_checksums` before a
   lookup. Choose the cheaper one that keeps Track 1's speed; report
   the cost. Add a test where the same checksums with a different
   corpus miss the memo, and a small synthetic unit test for the marshal
   precompute (`required_by_any_rule`) matching the per-rule path.
3. **RKE-R3.** Align track1.md's `kernel: finding model` row with
   `track1-sample-*.json`. (The plan's Decision 3 wording is the
   foreman's; leave the plan alone.)
4. **Prove.** Rerun the identity dump on all 775 lists against the
   committed baseline: per-list digest unchanged. Run the full suite
   and `python3 -m mypy`; report both lines.

No edit under packages/kernel/, packages/content/ or packages/schemas/.
Stop and report if a fix changes any output.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
