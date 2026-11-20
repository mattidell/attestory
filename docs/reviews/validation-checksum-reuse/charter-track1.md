# Charter: Track 1 of validation reuses member checksums

Role: Builder. Source HEAD on milestone/validation-checksum-reuse-2025.
Plan: docs/phases/engine-breadth/milestones/validation-checksum-reuse.md
(read it whole). Precedents: the rust-kernel-experiment and
member-reads-once milestones (their evidence directories and
retrospectives: the validation memo in production_resolver.py, the member
cache `_member_candidates`, and how they proved byte identity and paired
timings), and tools/recorded_replay.py. Do not read governance.

## Scope

1. **Measure.** Profile one median and the slowest recorded list on
   published core v100. Report where citizen checksums are computed, how
   many per list, and their share of wall time. Cite file:line.
2. **Build.** Reuse checksums the member cache already holds, in the
   validation memo key and in `validate_package`, wherever the cached value
   is keyed by the exact bytes it stands for. A changed citizen must still
   change the key and still be validated. Do not edit `packages/kernel/`;
   if the lever needs it, stop and report.
3. **Prove.** All 775 recorded lists byte-identical before and after
   (run in parallel shards, one shared materialization). Add tests:
   a mutated citizen after a cached read is still caught; the memo
   key changes when any member's bytes change; and the cache is cleared
   where the existing clear hooks clear it.
4. **Time.** Paired cold and warm median and slowest-list timings, before
   and after, and the full suite's wall time if you run it.

This touches `packages/derivation/`: run the full suite (`pytest`, in
bounded chunks if one run cannot fit) and `python3 -m mypy` after your
last edit. Put results in
docs/phases/engine-breadth/milestones/validation-checksum-reuse-evidence/track1.md.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`. Never raise a
  fast-lane budget or size cap.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push and no spawn.
