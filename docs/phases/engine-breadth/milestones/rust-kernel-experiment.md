<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "rust-kernel-experiment",
  "status": "P0 (profile) chartered 2026-11-18.",
  "scope": [
    "measure where the time goes when one recorded return is replayed on published core v96, by function and by layer (kernel, derivation, projection, schema validation, I/O)",
    "decide, from that measurement, whether a Rust port of a bounded kernel slice behind a Python binding is the right lever, and which slice",
    "if the owner confirms the kernel edit, port that slice and prove it byte-identical on all recorded lists before measuring speed and agent fluency"
  ],
  "non_goals": [
    "no change to any answer, refusal code, missing name, page text or published schema or citizen",
    "the Python engine stays the gate of record throughout the experiment",
    "no edit under packages/kernel/ before the owner confirms it after P0",
    "no rewrite beyond the slice P0 names; continuing layer by layer is a later owner decision"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/rust-kernel-experiment.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/rust-kernel-experiment.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/rust-kernel-experiment.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/rust-kernel-experiment.md"
    ]
  }
}
-->

# Rust Kernel Experiment

Milestone key: rust-kernel-experiment.
Branch: milestone/rust-kernel-experiment-2025.
Phase: Engine Breadth, engineering experiment. Opening plan: 2026-11-18.
Starting point: main at `7c043135` (core v96, registry v94, release v94).
Expected target: no package version change.

## What we are trying to accomplish

The owner asked whether the engine should move to Rust, for speed, for a
stricter language, and because models are expected to get better at
Rust. A whole rewrite is a large bet on an unmeasured premise. This
milestone answers the question with evidence: first where the time
actually goes, then one bounded slice ported and proven identical, then
a measurement the owner can decide on.

The 2026-10 measurement found the cost quadratic in log length: each save
re-projects the whole act log, and each replayed assertion rebuilt the
fact lattice. Some memoization has landed since (`_CurrentLatticeHolder`
in the kernel's finding model). Whether the remaining cost is
algorithmic (fixable in Python) or constant-factor (where Rust helps) is
the first thing to know.

## Stages

1. **P0, profile (no code change).** Profile recorded-return replays on
   published core v96 and name where the time goes. Separate algorithmic
   cost from constant-factor cost. Name the candidate slice for a port,
   its Python interface, what it would cost, and what an algorithmic fix
   in Python would buy instead.
2. **Owner gates.** Before any port: (a) the owner, or an advisor the
   owner calls, checks whether the Engineering Constraints say anything
   about implementation language or the kernel boundary (the foreman
   does not read governance); (b) the owner confirms the edit under
   `packages/kernel/`. If P0 shows an algorithmic fix dominates, the
   foreman recommends that first.
3. **Track 1, port.** The named slice in Rust behind a PyO3 binding,
   selectable at run time, the Python path unchanged and default.
4. **Track 2, differential check.** All recorded lists on both paths;
   byte-identical output required. Then measure wall time, test-suite
   time, build cost, and how the builder fared writing Rust.
5. **Review, closeout.** The owner decides whether to continue layer by
   layer.

The plan is updated after P0 with the decisions it needs.

## P0 result

Pending.

## Decisions

Pending.
