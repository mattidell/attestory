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

### Package Successor Generator

[Plan](milestones/package-successor-generator.md).
[Retrospective](../../milestone-retrospectives/2026-10-28-package-successor-generator.md).
The generator constructs and validates candidate package, registry and release
chains from explicit changes. It reproduces three chains through core v60:
v57/v55/v55 to v58/v56/v56, v58/v56/v56 to v59/v57/v57, and v59/v57/v57 to
v60/v58/v58, all byte for byte. Structural replacement checks
do not establish tax meaning; companion declarations and live release evidence
remain separate publication duties.

### Explain a Shared Input Once

[Plan](milestones/explanation-sharing.md).
[Retrospective](../../milestone-retrospectives/2026-10-28-explanation-sharing.md).

Normal explanations, CLI and NPE output, and new saved presentations retain one
shared graph with every recorded use and its pin metadata. A reader can follow
a saved line to its source and navigate reuse without the originating run.
Historical presentation bytes stay unchanged. The reproduced line 27a graphs
are about 154–155 KB rather than 1.6 MB expanded trees; whole saved files grow
because they newly preserve complete lineage. No runtime speedup or new tax
coverage is claimed. Ordinary correction tests also reuse isolated browser
contexts; fresh recovery/lifecycle paths remain, and startup is coordinated
across workers. Direct CLI rendering is conservatively serialized. Fewer
launches were demonstrated, not a full-suite speedup or the earlier startup
failure's cause. PR #229's exact-head `verify` is the publication gate.

### Replay a Log in One Pass

[Plan](milestones/lattice-rebuild.md).
[Retrospective](../../milestone-retrospectives/2026-11-05-lattice-rebuild.md).
[Measurements](milestones/lattice-rebuild-evidence/measured-performance.md).

One kernel projection incrementally maintains current and historical lattice
combinations. Public dictionary ownership, historical first-read snapshots,
ordering and refusals remain compatible with full rebuild. The owner selected
this bounded optimization after P0 found a narrower opportunity than October's
ranking implied. The integrated core-v76 pair saved 16.4% process-tree CPU on
two cases; whole replay is not established as linear, active-index memory can
increase, and no net-suite saving is claimed. Every fixture-prefix observation
is retained with a cheaper differential execution strategy and explicit cold
checkpoints; the permanent tests and final repaired-head cost are documented.
Exact-head green `verify` on PR #258 remains the publication gate. The
owner-requested browser-resource instrumentation is also delivered: CI
retained bounded progress and Linux process samples on the exact launch path,
with upload-on-failure and no deadline increase. A passing instrumented run
does not explain the earlier 20-second startup.

## Current boundary and remaining work

[Remaining Test and CI Cost](milestones/test-cost-remaining.md) is closed.
PR #226's exact-head `verify` is the merge gate for that candidate and had
not succeeded when the record was written.

Still open:

1. **Package resolution and remaining replay scans.** Current-lattice delta
   maintenance is delivered by lattice-rebuild, but metadata scans, ordered
   output and finding/currency work still grow. P0 found package resolution
   dominant in other leading sampled cases. Profile it before selecting the
   next slice; no resolver optimization is selected here. Establish a same-base
   net-suite comparison including the added differential-test cost.
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
6. **Partial port and torn browser path.** The lifecycle milestone closed
   the fake-marker race and the harness's whole-decimal port line only.
   `packages/derivation/live_viewing.py` `_wait_for_devtools` still accepts
   a digit-only `DevToolsActivePort` buffer with no newline. That reader
   and `waitForDevToolsActivePort` still accept a torn path such as
   `12345\n/devtools/bro`. Neither reader was brought under the stricter
   rule.
7. **Chrome lifecycle observation under load.** The lattice-rebuild full run
   failed the stuck-positive-port test's observation of a malformed file within
   its existing deadline; the unchanged test passed alone. Cause and repair
   remain unestablished. This is not grounds to exempt the check or call it
   infrastructure; diagnose separately if it recurs in exact-head CI.

Test moves below the coordinator were measured and are not worthwhile while
the recorder holds the cost. Persistent caches, partial catalogs, test culling,
and application-module separation remain unselected. Parallel jobs reduce
waiting and spend more runner time; label those benefits separately.

## Process changes

### Retire Phase State

[Plan](milestones/retire-phase-state.md).
[Retrospective](../../milestone-retrospectives/2026-10-29-retire-phase-state.md).
`docs/phase-state.md` is retired. The foreman capsule reads the plan from the
branch name and derives open or closed from it; orientation takes the role
and charter explicitly. Parked work moved to the Engine Breadth roadmap.

### Chrome Starts Before the Gate Gives Up

[Plan](milestones/chrome-startup-flake.md).
[Retrospective](../../milestone-retrospectives/2026-10-31-chrome-startup-flake.md).

Seven required runs failed in two days on one Chrome startup timeout. The
one traced failure was a cold first launch ready at 11.2 seconds against a
ten-second allowance. The allowance is now 45 seconds inside the startup
slot, the owner waits longer than the worst case, and slow launches are
reported. No full-suite speedup or cause beyond disk-wait at first launch is
claimed.

### The Chrome Lifecycle Test Waits for Its Marker

[Plan](milestones/chrome-lifecycle-race.md).
[Retrospective](../../milestone-retrospectives/2026-11-04-chrome-lifecycle-race.md).

The lifecycle fake publishes its marker by renaming a complete document and
waits for usable JSON. The launch assertion is observed immediately, and
cancellation and drain still run when that wait fails. A DevTools port is
ready only as a whole decimal line. Deadlines, `browserPath` as the trimmed
second field, and the profile-absent and `ESRCH` assertions stay. An injected
empty marker failed 10 of 10 counted runs before the repair and passed 10 of
10 after. Unmodified runs passed 46 of 46 on both sides. The Python live
viewer still accepts a digit-only port buffer with no newline, and both that
reader and the harness still accept a torn browser path. Those two readers
are outside this result. Exact-head `verify` on the curated tree remains the
publication gate.

### Complete Current-Core Returns for Tests

[Plan](milestones/current-core-harnesses.md).
[Retrospective](../../milestone-retrospectives/2026-10-31-current-core-harnesses.md).

`tests/helpers/current_core_returns.py` builds complete returns on the latest
core reaching line 2a, Schedule 8812 line 21 and Schedule 1 line 21. The
checks the cents and correction milestones left structural now run live; no
product defect was found.

### The Remaining Closure Entries, Confirmed Live

[Plan](milestones/closure-live-confirmation.md).
[Retrospective](../../milestone-retrospectives/2026-10-31-closure-live-confirmation.md).

Form 1099-INT box 8, Form 1099-DIV box 7 and Form 1098-E, allowed in the
closure regression test on a static reading, hold live on core v66; so does
box 8's attachment path. No gap was found.

