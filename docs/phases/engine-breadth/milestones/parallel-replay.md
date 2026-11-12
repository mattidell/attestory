<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "parallel-replay",
  "status": "Closed 2026-11-12. Tool built, reviewed and repaired.",
  "retrospective": "docs/milestone-retrospectives/2026-11-12-parallel-replay.md",
  "scope": [
    "one reusable tool replays the recorded act lists earlier milestones replay, on any set of cores, in parallel worker processes",
    "its results equal the existing single-process neighbour replay exactly for the same cores",
    "a milestone's rerun and its Track 0 neighbour diff can share one replay"
  ],
  "non_goals": [
    "no package, content, schema, engine or kernel change",
    "no change to any committed evidence file of a closed milestone",
    "no change to which lists count as recorded"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/parallel-replay.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/parallel-replay.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/parallel-replay.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/parallel-replay.md"
    ]
  }
}
-->

# Recorded Returns Replay in Parallel (tooling)

Milestone key: parallel-replay.
Branch: milestone/parallel-replay-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-12.
Starting point: main at `080d2758`. Runs in parallel with
age-blindness-asked (PR #274) and blocked-names-question (PR #275); touches
no package, so no core version.

## What we are trying to accomplish

Every content milestone replays the same recorded act lists (775 distinct
lists from five committed fixtures) on the old and new core: once in P0's
rerun and again in Track 0's neighbour diff. Each script runs them one at a
time: about three hours per pass, twice per milestone, with the builder
idle while it waits. The useful outcome is one tool that runs the replay in
parallel worker processes, so a pass takes minutes and one replay feeds
both tables.

## What we know

- `question-wording-evidence/track0.py` `neighbour_tasks()` gathers the
  lists (v83, v84, v85, v82, v81 fixtures, de-duplicated by digest) and
  replays them on two cores; `track0-neighbour.json` is its committed
  output.
- `age-blindness-asked-evidence/rerun.py` (on PR #274's branch) already
  shards by index with a resumable part file, but was run as one shard.
- The machine has 10 CPUs. Two other milestones' builders run at the same
  time.

## Stages

Tooling milestone: no P0 or Track 0 (no tax decision is made). Track 1
builds and proves the tool; a fresh review; closeout.

1. **Track 1: build** (charter `docs/reviews/parallel-replay/charter-track1.md`).
2. **Review and repair.**
3. **Close.** Retrospective, roadmap, exact-head CI, merge.

## Process

Dispatch: agy Gemini 3.8 Flash for the build (owner's standing dispatch
plan, 2026-11-12), Argon for the review. The build's acceptance check is
exact equality with a committed single-process output, which the tool
cannot satisfy by construction.

## Track 1 result

Track 1 built `tools/recorded_replay.py`, providing `recorded_lists()`,
`replay()`, and the `neighbour` command line.

### Equivalence result

Replay of all 775 recorded act lists on published core v86 and published
core v87 using `--workers 4` reproduced the committed
`question-wording-evidence/track0-neighbour.json` with exact equivalence:
- 775 lists compared across all 5 fixture sets (v81: 206, v82: 170, v83: 298, v84: 58, v85: 43).
- 0 mismatches: every list key and every classification row matched identically (774 identical, 1 sentence-change row `v82/m_empty_exc1_unanswered/honest`, 83 identical refusals).
- Evidence recorded in `docs/phases/engine-breadth/milestones/parallel-replay-evidence/equivalence.json` via `compare_neighbour.py`.

### Wall time comparison

- **Single-process baseline:** 20 lists measured single-process took 349.68 s (17.48 s/list), extrapolating to **13,550.23 s** (225.8 min / 3.76 hr) for 775 lists.
- **Parallel replay (4 workers):** The complete 775-list replay took **2,559.48 s** (42.66 min), a ~5.3x wall-time reduction on 4 worker processes while running concurrently with other milestones on a 10-CPU machine.

### Tests

Suite `tests/test_recorded_replay.py` contains 7 tests (6 in the fast lane, 1 marked `@pytest.mark.live`):
- `test_recorded_lists_returns_775_keys_equal_to_committed` (live lane: full fixture extraction and core setup)
- `test_ordering_and_output_independent_of_workers_and_finish_order` (fast lane)
- `test_resume_skips_keys_in_part_file` (fast lane)
- `test_stale_part_file_for_different_cores_is_refused` (fast lane)
- `test_no_absolute_path_in_any_written_file` (fast lane)
- `test_baseline_other_than_v86_records_identical_errors` (fast lane)
- `test_summarize_rerun_from_replay_pins` (fast lane)

### How a milestone uses it

A content milestone runs recorded return replay once using:
```sh
python3 tools/recorded_replay.py neighbour <baseline-core> <new-core> --workers N --part <scratch>/part.json --out <scratch>/track0-neighbour.json
```

Because the part file stores both cores' pins per key (`row["pins"] = {core_a.version: pin_a, core_b.version: pin_b}`), the milestone can derive the P0 rerun table (`rerun-output.json`) directly from the same part file without executing any return a second time:
```sh
python3 tools/recorded_replay.py rerun --part <scratch>/part.json --baseline <baseline-core> --comparison <new-core> --out <scratch>/rerun-output.json
```

#### Core specifications

`tools.recorded_replay.resolve_core()` accepts either:
- **Published cores:** specified by version string (e.g. `"v86"`), resolving `registry` and `release_version` to `"v{N-2}"` (`"v84"`).
- **Candidate / scratch cores:** specified by path to a JSON file (e.g. `<scratch>/core.json`) containing:
  ```json
  {
    "version": "v87-dev",
    "registry": "v85",
    "release_version": "v85",
    "content": "packages/content",
    "releases": "packages/releases",
    "loader_from": null,
    "presence_pairs": []
  }
  ```

#### Custom replay tasks with public helpers

Milestones can implement custom parallel replays by defining a top-level, picklable `per_list` function using the public `pin_run` and `classify` helpers:

```python
from typing import Any
from tools.recorded_replay import pin_run, classify, replay, recorded_lists, Acts

def custom_per_list(key: str, acts: Acts, cores: tuple[Any, Any]) -> dict[str, Any]:
    core_a, core_b = cores
    run_id_a = f"demo.replay.{core_a.version}.{key}"
    run_id_b = f"demo.replay.{core_b.version}.{key}"
    pin_a = pin_run(core_a, acts, run_id_a)
    pin_b = pin_run(core_b, acts, run_id_b)
    row = classify(pin_a, pin_b, name_a=core_a.version, name_b=core_b.version)
    row["pins"] = {core_a.version: pin_a, core_b.version: pin_b}
    return row

# Executed across worker processes with resumable checkpointing:
results = replay(
    recorded_lists(),
    (core_a, core_b),
    custom_per_list,
    workers=4,
    part=part_path,
)
```

## Decisions on review

Foreman, 2026-11-12, on `docs/reviews/parallel-replay/review.md`. Every
finding is accepted.

1. **F1.** Tests that call `recorded_lists()` (about 70 s) are
   `@pytest.mark.live` with the measured reason; the fast lane keeps the
   ordering, resume and path tests on a fake list set.
2. **F2.** A part file records the identity of the cores it was run on
   (package id, version and checksum of each). Resuming refuses a part
   file for other cores, and results keep only keys in the requested list
   set.
3. **F3.** No core version is hard-coded; identical errors are recorded
   for any baseline, only when both runs carry the same error.
4. **F4.** The replay stores each list's pins once per core, and the
   classification is derived from the stored pins. The tool exposes the
   pin-run and classify helpers publicly, and the plan's "How a milestone
   uses it" shows a P0 rerun table and a Track 0 neighbour table derived
   from one replay, with a worked per-list function.
5. **S1.** The comparison checks every key's class and error identity,
   every change row, and the top-level `sets`, `distinct_lists`, `runs`
   and `counts`.
6. **S2.** Worker processes start with the `spawn` method;
   `recorded_lists()` returns a copy.
7. **N1.** The part-file writer applies the local-path check.

## Review and repair

Fresh-reader review: `docs/reviews/parallel-replay/review.md`, not ready.
Blocking: a 70 s fixture hidden from the fast-lane budget (F1); a part file
not bound to its cores (F2); a hard-coded v86 baseline for identical errors
(F3); no way to derive the P0 rerun table from the same replay (F4). All
seven findings were decided and repaired; tests for F2 and F3 fail on the
pre-repair tool. The equivalence proof was rerun under the strengthened
comparison: 775 lists, zero mismatches. The re-review was ready with no new
findings.

## Closeout

Closed 2026-11-12. Retrospective:
`docs/milestone-retrospectives/2026-11-12-parallel-replay.md`.
