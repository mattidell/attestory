# Charter: Track 1 of recorded returns replaying in parallel

Role: Builder. Source HEAD on milestone/parallel-replay-2025.
Plan: docs/phases/engine-breadth/milestones/parallel-replay.md (read it
whole). Source to read: question-wording-evidence/track0.py
(`neighbour_tasks`, the neighbour replay and its classification) and its
committed track0-neighbour.json. Do not read governance.

## Build

1. **Tool.** `tools/recorded_replay.py`, importable and runnable:
   - `recorded_lists()` returns the same (key, acts) list, in the same
     order, as question-wording's `neighbour_tasks()`. Move the gathering
     logic into the tool rather than importing the evidence script, and
     leave the evidence script unchanged.
   - `replay(lists, cores, per_list, workers, part)` runs a caller-supplied
     per-list function over every list in a `concurrent.futures`
     process pool (default workers: CPU count minus one; a `--workers`
     option). It writes a resumable part file as results arrive, skips
     keys already present, and returns results keyed and sorted by list
     key, so the output does not depend on worker count or finish order.
   - A command line: `python3 tools/recorded_replay.py neighbour
     <core-a> <core-b> --workers N --part <file> --out <file>` that
     produces the same classification rows as question-wording's
     neighbour step for those two cores.
2. **Equivalence proof.** Run the command line for the two cores
   question-wording's track0-neighbour.json used, with `--workers 4` (two
   other milestones are using this machine). Compare to the committed
   track0-neighbour.json: every list key and every row equal. Commit the
   comparison script and a small JSON result (counts, wall time, workers,
   mismatches: expected none) under
   docs/phases/engine-breadth/milestones/parallel-replay-evidence/. Also
   record the single-process wall time from question-wording's evidence if
   it is stated, else measure 20 lists single-process and extrapolate,
   saying so.
3. **Tests.** `tests/test_recorded_replay.py`, fast lane (under 3.0 s
   each): `recorded_lists()` returns 775 keys equal to the committed
   track0-neighbour.json key set; ordering and output are independent of
   worker count and finish order (use a cheap fake per-list function, two
   worker counts); resume skips keys in the part file; no absolute path
   in any written file.
4. **Plan.** Fill a "Track 1 result" section: the equivalence result, wall
   time against the single-process time, the test counts, and a short
   "How a milestone uses it" paragraph (P0 rerun and Track 0 neighbour
   from one replay).

Checks: `pytest tests/test_recorded_replay.py`, `pytest -m "not live"`,
`python3 -m mypy`, `python3 tools/envelope_scan.py --range
github/main..HEAD`.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included (use a scratch directory outside the repo for part
  files).
- Do not edit packages/, tests/fixtures/, or any committed evidence of
  another milestone. Do not read docs/governance/.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push, no spawn.
- The equivalence check is the acceptance gate: report any mismatch as
  it is; do not adjust the classification to make it match.
