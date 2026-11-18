<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "rust-kernel-experiment",
  "status": "Review READY with notes; repair chartered 2026-11-18. Rust port parked behind owner gates.",
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

Evidence: `rust-kernel-experiment-evidence/p0.md` and the JSON beside it.
All 775 recorded lists were timed on core v96 (787 s wall on 9 workers;
median list 7.8 s, a narrow tail of 28 lists above 10 s). Profiled in one
process: the median list (6.6 s), the slowest (39 s) and test K13
(5.2 s), with cProfile, a stack sampler and no-profiler cost centres.

- The kernel is not where replays spend time: about 6 % of the median
  list and 1 % of the slowest. The actual rule evaluation is about 2 %.
- The dominant costs are algorithmic, in `packages/derivation/`:
  `validate_package` loops members inside members for every source
  family (about 49 M steps, half of the median list) and runs twice per
  replay on the same package; the presentation closure-question walk
  re-walks the blocked-row graph once per path and rescans every
  resolved member per step (84 % of the slowest list).
- Growth: replay time is flat in log length and jumps with the shape of
  the blocked-row graph. One kernel projection is mildly superlinear
  (lattice metadata rebuilt per assertion, 0.2 s at 350 acts); recorder
  stories re-project the whole log on every save, which is why K13
  spends 52 % in kernel projection.
- Python fixes (validation index and memo, file-load memo, closure-walk
  memo, marshal precompute) are estimated to take the median replay from
  6.6 s to about 1.5 s and the slowest from 39 s to about 2 s.
- Port candidate if the owner continues: the kernel replay fold
  (`findings.project` and the `facts.py` lattice). Upside today is under
  6 % per replay; the binding must call back into Python for schema
  validation per assertion, and the state it returns is read as Python
  objects throughout derivation.

Recommendation: fix the algorithms in Python first and re-measure; the
decisions this needs are listed at the end of `p0.md`.

## Decisions

1. **Fix the algorithms first (2026-11-18, foreman, on P0's
   recommendation; the owner may redirect).** The kernel is about 6 % of
   a median replay and 1 % of the slowest, so a Rust port of it cannot
   pay for itself in speed today. Track 1 makes the four derivation-side
   fixes P0 names in Python, plus the harness memo, and proves every
   recorded list byte-identical. No edit under `packages/kernel/`.
2. **The Rust port stays open, not dropped.** After Track 1 the foreman
   re-profiles. If the kernel then dominates, or the owner wants the
   language and agent-fluency evidence regardless, the port resumes at
   the slice P0 named (kernel replay fold), behind gates 2a and 2b
   unchanged. The kernel algorithmic fix (incremental re-projection,
   lattice metadata) waits on the same kernel-edit confirmation.
3. **Byte-identical is the contract.** Every recorded list's result,
   page and error (class and message) must match the pre-change code
   exactly; any difference stops the track. Package validation must
   report the same errors always, in the same order under any fixed
   hash seed (Decision 5).
4. **Keep the projection change local.** The blocked-sale-pages
   milestone (another foreman) will touch the page and renderer; the
   closure-walk memo stays inside the walk functions so a later rebase
   is small.
5. **Repair the review notes (2026-11-18).** The fresh review
   (`docs/reviews/rust-kernel-experiment/review.md`) is READY with three
   low notes. RKE-R1: add a deterministic closure-walk case that fails
   when either cycle guard is dropped. RKE-R2: put the member corpus in
   the validation memo key (or verify it against the checksums inside
   `_validate_once`), and add a unit test for the marshal precompute.
   RKE-R3: Decision 3's order contract is "the same errors always, in
   the same order under any fixed hash seed", because the pristine
   validator already iterates a set; and align track1.md's
   finding-model row with its samples.
