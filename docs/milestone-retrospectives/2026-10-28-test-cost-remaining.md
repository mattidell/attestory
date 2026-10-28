# Retrospective — Remaining Test and CI Cost

The milestone reused projections within mortgage operations, folded checked
save prefixes incrementally, and sharded the full suite under the required
`verify` check. The [plan](../phases/engineering-health/milestones/test-cost-remaining.md)
records the measurements and independent reviews. No test was removed, skipped,
moved, or given a higher fast-lane budget.

## Lessons for future work

- Rank the suite, then profile the case that explains the rank and inspect
  its callers. The mortgage module dominated worker-wall time, but review
  located the repeated projection in the tax caller, not the kernel. The
  one-case improvement does not establish a suite-wide share.
- Separate elapsed wait, process-tree CPU, runner occupancy or billing, and
  summed test worker time. The first sharded run failed after 1004s and used
  12808.57s of shard CPU; its failure is not a speedup. A later
  [run](https://github.com/mattidell/attestory/actions/runs/40628958771)
  succeeded in 1022s workflow elapsed time, before the historical-baseline
  fixes. Its CPU and billed minutes are not recorded here. Exact final-head
  `verify` remains outstanding. Different collections and host speeds prevent
  treating these numbers as a controlled comparison.
- Reuse within a call depends on the acts and registry still matching. An
  append must update the held projection or trigger a fresh fold. Incremental
  save folding also depends on the same applier as projection; its differential
  oracle repeats admission predicates, so shared mistakes remain possible.
- Every shard has a fresh checkout. Installing a hook on one job does not make
  it available to another. The required fan-in must fail for a skipped,
  cancelled, or failed dependency, including a draft that intentionally does
  not run the suite.
- A historical comparison needs an available, independent witness. Review
  found both an absent-ref pass and a self-comparison risk. The repaired guard
  fails closed and was independently reviewed with synthetic event cases; that
  does not establish GitHub event delivery. At main-ui convergence, the prior
  main-ui revision is the witness, so restoring a divergent historical file
  to main's bytes is refused without an independent prior-main witness.

## Follow-ups

None is selected: obtain final-head `verify` and separately record its wait,
CPU, and billed minutes; establish a trusted prior-main witness if the
convergence correction is needed; consider current-lattice rebuilding,
cross-call prefix memoization, and the remaining small helpers only after a
new ranking justifies them. Separate calls, single-act checked appends,
post-save reads, and Form 1098 withdrawal still project independently.
