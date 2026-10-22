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

[Plan](milestones/test-cost-and-coverage.md). Published through PR #213.

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

### Faster CI, Cheaper Suites, the Same Defects Caught

[Plan](milestones/test-and-ci-efficiency.md). Ranked suite CPU first. Draft
pushes get the cheap checks and the fast lane in about a minute; the required
`verify` fails on drafts and runs in full when a PR is ready. Schema-check and
historical-lattice reuse lowered suite CPU (3,601s against 5,329s at P0, single
runs). Track 3 found no worthwhile test moves.

## Current boundary and remaining work

The next milestone is unselected. The measured candidates, from the most recent
suite ranking and its follow-up classification:

1. **Re-projection.** `findings.project` folds the whole log from the start,
   hundreds of times per test, mostly from product recording, review and the
   save path. In order: fold incrementally within one `ActLog.append_batch`
   save; share one projection through each recording or review operation; only
   then consider an in-process prefix memo keyed by exact act content and
   registry state. Start from a P0 of the recorder and save paths.
2. **Current-lattice rebuilds** after the fact state changes (11–20% of worker
   time at the last ranking) need an incremental-lattice design.
3. **Test moves** were measured and are not worthwhile while the recorder holds
   the cost: moving every safe candidate below the coordinator would recover
   under 1% of suite time. Revisit only after recording is cheaper.

Package validation proved cheap after the first call in a process. Persistent
caches, partial catalogs, CI sharding, test culling and application-module
separation remain unselected. Parallel jobs reduce waiting, not CPU; label
those benefits separately.
