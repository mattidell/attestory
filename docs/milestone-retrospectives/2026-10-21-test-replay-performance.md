# Retrospective — Faster Feedback, Cheaper Workspace Replay

## Durable lessons

- Trace the real end-to-end path before choosing a reuse lifetime. The measured
  correction story included save admission, a coordinator, and two deliberate
  test-side derivations; a shortcut would have measured different work.
- Object identity made a small, fold-local boundary practical: hold the
  current lattice only while the exact state object is unchanged, then rebuild
  on replacement. Lifecycle changes and readoption need successor lookups in
  the same fold to prove that invalidation works.
- Current and historical fact views are different products. Keep historical
  reads and currency fresh instead of treating the current lattice as a
  universal cache.
- Behavioral tests survive refactoring better than source-layout tests. The
  four-enforcer check now executes the real functions across public assertion,
  optimized projection, and retraction, while existing refusal tests remain.
- Keep fixed targets honest. CPU and control targets passed, while the
  full-construction target missed by 22. That small miss was not relabeled as a
  pass, nor was it used to justify an unmeasured wider mechanism.

## Result and open questions

Fold-local reuse reduced story CPU by 62.3%; full-lattice construction count
fell 79.95%, short of the fixed 80% target. The precise commands, case values,
and evidence limits are in the [measurement note](../phases/engineering-health/milestones/test-replay-performance-evidence/measured-performance.md).
The full verification run passed on the repaired implementation, as recorded
in the [CI run](https://github.com/mattidell/attestory/actions/runs/39551011772).
Independent semantic review found no material kernel issue. The reviewer did not independently rerun the
ordinary timings; that is an evidence limitation, not a correctness objection.

No material semantic dissent remains. Further work should first identify
remaining engine cost, then test whether any overlap is genuinely redundant,
and examine useful component-suite boundaries. No broader cache, partial
catalog construction, sharding, or test deletion is selected by this result.
