<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "parallel-replay",
  "status": "Open. Plan and Track 1 charter.",
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
- **Parallel replay (4 workers):** The complete 775-list replay took **3,018.37 s** (50.31 min), a ~4.5x wall-time reduction on 4 worker processes while running concurrently with other milestones on a 10-CPU machine.

### Tests

Fast-lane suite `tests/test_recorded_replay.py` contains 4 tests passing in the fast lane:
- `test_recorded_lists_returns_775_keys_equal_to_committed` (< 0.005 s call)
- `test_ordering_and_output_independent_of_workers_and_finish_order` (0.32 s call)
- `test_resume_skips_keys_in_part_file` (0.18 s call)
- `test_no_absolute_path_in_any_written_file` (0.18 s call)

### How a milestone uses it

A content milestone runs recorded return replay once using:
`python3 tools/recorded_replay.py neighbour <baseline-core> <new-core> --workers N --part <scratch>/part.json --out <scratch>/track0-neighbour.json`
Because the tool replays both the v83 P0 rerun subsets and the full neighbour
fixture grid together, a single parallel replay produces both the P0 rerun
table and the Track 0 neighbour dependency diff. The resumable part file
protects long runs against interruption without duplicate execution.
