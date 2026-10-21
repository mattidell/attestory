# Engineering Health Roadmap

## Completed milestones

### Faster Feedback, Cheaper Workspace Replay

[Plan](milestones/test-replay-performance.md).

The CI workflow runs cheap checks before the full suite and cancels only
superseded runs of the same PR. Fold-local current-lattice reuse made the
unchanged correction story cheaper without skipping admission or historical
checks. Story CPU fell 62.3%; the fixed lattice-construction target missed by
22 builds. The [measurement note](milestones/test-replay-performance-evidence/measured-performance.md)
keeps those outcomes and limits separate from CI acceptance. Published through
PR #212.

### Less Repeated Work, the Same Defects Caught

[Plan](milestones/test-cost-and-coverage.md). Closed on this branch; PR #213
holds publication review and exact-head CI.

The live return now reuses its already-projected current state to read claim
applicability, rather than replaying the full history again for that purpose.
Public cold reads remain fresh and historical correction checks still read
their actual earlier states. No test, parity check or saved-output assertion
was removed. The [measurement note](milestones/test-cost-and-coverage-evidence/measured-applicability-reuse.md)
records the unchanged story/control observations and diagnostic counts; these
are not whole-suite speedup claims.

The source investigation separated costly product reads from cheap test-side
derivations. Its sampled tests protected distinct defects, so it justified no
test cull or application split. The completed boundary is one invocation,
not a persistent cache or a new source-use contract. No tax coverage changes.

## Current boundary and remaining work

The next milestone is unselected. Further work should compare these candidates
before selecting another mechanism:

1. **Package-validation cost.** The retained story profile attributes about
   22.7s cumulative to validation across 11 returns. Schema checks already
   have content-addressed memoization. Identify the remaining expensive
   substeps, actual misses and authority-preserving boundary before proposing
   another cache, partial catalog or skipped work.
2. **Current and historical lattice reads.** Establish whether repeated
   construction uses the same exact state and which lifecycle changes require
   rebuilding. A current view cannot substitute for historical authority.
3. **Test design.** Remove or shorten a story only after retained witnesses
   demonstrably catch its distinct correction, recovery, refusal and saved
   result defects. The bounded sample did not establish redundancy or a
   current slow-module ranking.
4. **Useful component commands.** Focused suites can shorten local feedback
   without separately deployable applications. Shared kernel/derivation and
   dynamic package changes still need integration coverage and full CI.

Broader replay caches, partial catalogs, CI sharding, test culling and
application-module separation remain unselected. Parallel jobs can reduce
waiting without reducing total CPU; label those benefits separately. Existing
tax-product limitations remain with their product phases, not silently solved
by engineering-health work.
