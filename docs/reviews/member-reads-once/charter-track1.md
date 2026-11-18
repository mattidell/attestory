# Charter: Track 1 of member files are read once

Role: Builder. Source HEAD on milestone/member-reads-once-2025.
Plan: docs/phases/engine-breadth/milestones/member-reads-once.md (read
it whole, especially Decision 1). Evidence to reuse:
docs/phases/engine-breadth/milestones/rust-kernel-experiment-evidence/
(track1.md; track1_dump.py, the identity dump; track1_timing.py and
track1_profile.py; track1-summary-baseline.json with per_list_digest
3def5f6f845f2c0bee7500a17f6cdda0f0577a84de0331144b10a26f5356cab1).
Do not read governance.

## Scope

1. **Measure where the reads happen.** Count how many times per recorded
   list `_json_candidates` (packages/derivation/production_resolver.py)
   and any other reader parse or checksum each member file, and from
   which callers. Record it before changing anything.
2. **Cache.** Make each distinct member file parse and checksum at most
   once per process. Decision 1 governs the key: prefer keying on the
   bytes read (read, hash bytes, reuse the parse and checksum for
   identical bytes); measure what that saves versus a stat-based key and
   report both. The cache must be bounded or its size justified, must
   not let a caller mutate a shared parse (return copies or immutable
   views; measure the copy cost), and must expose a clear function as
   the existing validation memo does.
3. **Prove.** Rerun the identity dump on all 775 lists: per-list digest
   equal to the baseline above. Add focused tests: a file whose bytes
   change between calls is re-parsed, a caller mutating a returned body
   cannot affect a later call, and the cache path equals the uncached
   path on a synthetic member directory.
4. **Measure.** Re-time all 775 lists and re-profile the median, slowest
   and K13 workloads as rust-kernel-experiment did; report the new
   layer table and what now dominates.

No edit under packages/kernel/, packages/content/ or packages/schemas/.
Stop and report if the saving is under 10 % of a median replay, or if
any output changes.

## Deliverables

Code in packages/derivation/, tests under tests/, and in
docs/phases/engine-breadth/milestones/member-reads-once-evidence/:
track1.md (read counts, design and key choice, identity proof, timing
and layer tables), scripts (load sibling evidence scripts by path under
a unique name) and small JSON summaries. This is substrate work: run
the full suite (`pytest`) and `python3 -m mypy` before you finish and
report both lines.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks, so a usage limit
  does not lose it; update it when the checks finish.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
