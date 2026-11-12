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
