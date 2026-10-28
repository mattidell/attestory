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

### Every Required Answer Is Read

[Plan](milestones/required-versus-read.md). Measured shipped content for
rules that require an input no evaluated path reads: one static hit in the
latest package, and no misleading question or correction hazard in the rows
examined. A static
check now gates CI (`tests/test_required_versus_read.py`, fast lane, with a
reasoned allowlist), and `tools/required_versus_read.py path` reports
path-dependent cases on demand; it does not gate, because it also measures
test coverage.

### Remaining Test and CI Cost

[Plan](milestones/test-cost-remaining.md).
[Retrospective](../../milestone-retrospectives/2026-10-28-test-cost-remaining.md).

P0 ranked the suite again and separated elapsed wait, CPU, and runner time.
The owner selected three changes. Mortgage recording and review reuse one
projection inside the operation. A checked save folds its prefix
incrementally and refuses as before. Full `verify` packs the same suite onto
four runners and stays red unless every shard succeeds. The historical baseline guard fails
closed when it cannot establish an independent comparison. At main-ui
convergence it cannot restore a divergent historical file to main's bytes
without an independent prior-main witness. One profiled mortgage
case fell from 123.89s to 98.03s of CPU. The two profiled form saves show the
batch fold itself: Form 1099-K `append_batch` from 6.189s to 1.221s, Form
1098 from 31.771s to 3.607s, the latter mixed with the mortgage reuse. The
first full sharded run failed. A successful exact-head `verify` was still
outstanding when the milestone record closed. No test was removed or moved.

## Current boundary and remaining work

The next milestone is unselected.

[Remaining Test and CI Cost](milestones/test-cost-remaining.md) is closed.
PR #226's exact-head `verify` is the merge gate for that candidate and had
not succeeded when the record was written.

Still open:

1. **Current-lattice rebuilds** after the fact state changes need an
   incremental-lattice design.
2. **Cross-call prefix memo**, only if a new ranking shows projection still
   dominates, keyed by exact act content and registry state.
3. **Helpers left in place.** `_stage_enrollment_follows_schooling` inside
   `_commit_save`, `_scan_displayed_answers`, and
   `_attribute_borrowing_labels`. On the short histories profiled at P0 their
   cumulative time was 0.13s to 2.30s inside profiles of about 47–49s.
4. **A green sharded verify**, with wait, process-tree CPU, and billed
   minutes recorded separately. The 816.3s figure is a packing model on older
   weights. The failed fan-in is not that measurement.
5. **A trusted prior-main witness** for main-ui convergence if a divergent
   historical file must be restored to main's bytes. The current guard
   conservatively refuses that correction.

Test moves below the coordinator were measured and are not worthwhile while
the recorder holds the cost. Persistent caches, partial catalogs, test culling,
and application-module separation remain unselected. Parallel jobs reduce
waiting and spend more runner time; label those benefits separately.
