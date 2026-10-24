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

### Fold Once: Less Replaying of the Same History

[Plan](milestones/projection-reuse.md). Recording, review and correction reuse
one projection per call (save, correct and withdraw 60–72% less CPU on a long
synthetic history); a per-worker warm-up returned 19 tests to the fast lane.
The save-path incremental fold was skipped as the smallest share.

### A Per-Subject Rule Reads Only Its Own Subject

[Plan](milestones/per-subject-binding.md). A per-subject rule (per statement
or per child) could be evaluated with another subject's answer when that
answer reached it as a run-wide input. Per-subject inputs are now recognised
by the subject's distinguishing identity keys and bind only from the
subject's own scope, or block; return-level inputs are unchanged. The shipped
Form 1098 residence-interest reason rule was exposed, contained by the
one-statement limit on line 8a; no content or golden changed.

## Current boundary and remaining work

The next milestone is unselected. Measured candidates:

1. **Remaining re-projection.** Helper sites outside the last milestone's
   named set (`_stage_enrollment_follows_schooling` inside `_commit_save`,
   `_scan_displayed_answers`, `_attribute_borrowing_labels`), and the
   save-path incremental fold, which preserves today's exact refusal timing.
   Re-rank first; the save path was under 5% of folded acts.
2. **Current-lattice rebuilds** after the fact state changes need an
   incremental-lattice design.
3. **Cross-call prefix memo**, only if projection still dominates a new
   ranking, keyed by exact act content and registry state.

Test moves below the coordinator were measured and are not worthwhile while
the recorder holds the cost. Persistent caches, partial catalogs, CI sharding,
test culling and application-module separation remain unselected. Parallel jobs
reduce waiting, not CPU; label those benefits separately.
