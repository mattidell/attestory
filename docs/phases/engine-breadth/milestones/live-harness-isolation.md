<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "live-harness-isolation",
  "status": "Open. P0 measured; Decisions 1-5; Track 1 chartered.",
  "scope": [
    "every test that loads a milestone evidence harness gets that harness without sharing mutable module state with another harness in the same CI process",
    "a test's result does not depend on which other test modules ran before it on the same worker",
    "no test asserts less than before, and no published package, schema or content changes"
  ],
  "non_goals": [
    "no change under packages/",
    "no change to what any test asserts, its fixture bytes, or the fast-lane budget",
    "no CI workflow change beyond what isolation needs"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/live-harness-isolation.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Live Evidence Harnesses Run in Isolation

Milestone key: live-harness-isolation.
Branch: milestone/live-harness-isolation-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-10.
Starting point: `github/main` at `5ac56b96` (core v85).

## What we are trying to accomplish

Many live test modules load milestone evidence harnesses (probe, prototype,
track0 scripts under docs/phases/*/milestones/*-evidence/) into the pytest
process, and several harnesses import and mutate each other's module
globals. Under `-n auto --dist worksteal` a worker can load harnesses in
any order, and #264's verify needed a harness-leak fix to go green. The
useful outcome is that each harness a test uses is isolated, so results do
not depend on test order.

## What we know

- About 27 test modules load files by path.
- Earlier milestones loaded harnesses "under unique module names" and ran
  older harnesses in a subprocess, by charter convention, not by a shared
  mechanism.
- **What we do not know.** Which harnesses still share or mutate state;
  whether a per-test-module loader with private copies is enough or a
  subprocess is needed; what isolation costs in CI wall time.

## Actions the team will take

1. **P0: measure.** Inventory every harness load and every cross-module
   global assignment. Reproduce an order-dependent failure, or show none
   exists, by running pairs of modules on one worker in both orders. Design
   one shared loader. Stop and report before any change under packages/.
2. **Decide.** The loader and the modules it covers.
3. **Track 1: build.** The loader, every covered module moved to it, a
   test that fails if a module loads a harness another way.
4. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

Track 0 adversarial closure does not apply: no tax claim or engine
contract changes. The review checks that no assertion weakened.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. The milestone publishes no package, so it does not
stack on PR #270's core v86.

## P0 result

P0 is recorded in
`docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/p0.md`.
The inventory tool is `inventory.py` in that directory. Thirty-one test
modules load a Python file by path; twenty reach an evidence harness. Four of
those twenty need a subprocess, because a harness they reach writes engine
state and does not restore it. Sixteen can take a private copy of the harness
modules. Three already load through a subprocess. Eight load a tool or another
test. One-worker runs of the code B / v80 pair and the noncovered / v80 pair
passed in both orders. Commit `bb59eebe` restores the three `cf_probe` globals
around one code B run; the shared module object and the sticky loader patches
remain. Two cold subprocesses of the measured harnesses cost about 0.17s more
than importing both in one process. No change under `packages/`.

## Decisions

Foreman, 2026-11-10, on P0. No order-dependent failure reproduced; the
work is preventive, so it must stay cheap.

1. **One loader under tests/** for every in-process evidence load. It
   gives each test module private copies keyed by the owning module and
   the resolved path, and it intercepts nested bare imports (`import
   probe`, `import_module("probe")`). `packages.*` and `tests.*` stay
   shared.
2. **Engine writes are restored, not subprocessed, by default.** For the
   four modules that reach a harness writing a `packages` attribute with
   no `finally` partner, the loader snapshots each attribute the harness
   writes and restores it when the owning test module finishes. A
   subprocess is used only where restoring cannot be made exact; Track 1
   records which and why, with the wall cost.
3. The sixteen private-copy modules and the four restore modules move to
   the loader. The three subprocess modules and the eight modules loading
   a tool or another test stay as they are.
4. **A guard test** fails if a test module loads an evidence file by path
   other than through the loader, and if a loaded evidence file writes a
   `packages` attribute the loader does not restore.
5. Evidence files are not edited. The fast-lane budget stays.
