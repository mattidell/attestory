<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "test-replay-performance",
  "status": "Closed. Earlier CI feedback and one-fold current-lattice reuse are delivered; measured story CPU fell 62.3%, while the fixed construction target missed by 22 builds. No wider cache or test cull is selected.",
  "retrospective": "docs/milestone-retrospectives/2026-10-21-test-replay-performance.md",
  "scope": [
    "improve CI feedback without weakening the verify gate",
    "measure and reduce repeated lattice construction on an unchanged synthetic correction story",
    "preserve admission, replay, currentness, saved results, and behavioral coverage"
  ],
  "non_goals": [
    "no new tax behavior, schema publication, or changed admission contract",
    "no test deletion, skipped coverage, loosened assertions, or raised fast-lane budget",
    "no cross-call cache, broader replay reuse, partial catalog construction, or CI sharding"
  ],
  "deep_reads": {
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/test-replay-performance.md",
      "docs/phases/engineering-health/milestones/test-replay-performance-evidence/measured-performance.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-21-test-replay-performance.md"
    ]
  }
}
-->

# Faster Feedback, Cheaper Workspace Replay

Milestone key: `test-replay-performance` · Engineering Health · closed on this
branch. A correction story should get slower because it does more useful work,
not because each save rebuilds all the facts before it. Developers should also
get cheap type and boundary feedback before waiting on the long regression
gate. This work improved both feedback and repeated lattice construction while
keeping the same behavior and evidence.

## Actions completed

1. Reviewed the plan and boundaries before selecting an optimization.
2. Moved existing cheap checks ahead of pytest and limited cancellation to
   superseded runs of the same pull request, preserving the `verify` gate.
3. Froze an unchanged synthetic correction story and neighboring amount-only
   control; measured ordinary timings separately from single-process profiles.
4. Compared repeated current-lattice construction with broader replay reuse,
   then selected only one-fold current-lattice reuse after independent review.
5. Implemented and differentially tested that boundary; retained the existing
   correction story, control, refusals, and full verification gate.
6. Reviewed the same-case result and retained the fixed construction-count
   miss rather than widening reuse without evidence.

## Track 0 adversarial closure

The independent design review closed READY for this bounded unit after
challenging its lifetime and consumer boundaries. The act log remains the
authority; the lattice is disposable derived state held only inside one
`findings.project` fold while the exact `KernelState` object remains current.
Replacement rebuilds it, including after entity lifecycle changes, migration,
or readoption. The closed-empty → member add → reclose, successor handover,
same-ID readoption, and current-before-historical lookup cases test the
dangerous transitions, including an historical read inside the same fold.

The holder does not cross project calls, workspaces, public direct appliers,
or registry/caller mutation after return. Historical `include_displaced=True`
reads and currency remain fresh. Existing validation and refusal timing are
preserved: new-write checks remain at ActLog admission, and historical replay
does not gain them. The lifecycle-only prospective fold remains bounded to
its existing act kinds; ordinary writes are not eagerly rejected. No saved
result or published contract is introduced. These boundaries are preserved by
the implementation and regression evidence, not merely by the READY verdict.

## What was done

The workflow now runs unchanged cheap checks before pytest and cancels only
superseded runs for the same pull request. The `verify` check, triggers, and
complete test command remain intact.

The selected engine change keeps one private current-lattice holder for the
duration of each `findings.project` fold. It retains the exact `KernelState`
object and rebuilds when that object changes. Public direct appliers and
historical views remain uncached; currency is recomputed. No cache survives a
project call. The act log remains authoritative and existing validation and
refusal behavior is preserved. No new ADR or schema was needed.

The synthetic differential and boundary tests cover identity replacement,
readoption, entities, migration, retraction, handover, current versus
historical reads, refusal cases, and call isolation. The four-enforcer test now
observes the real functions executing through assertion, optimized projection,
and retraction rather than depending on source layout. Existing refusals and
assertions remain; no skips or verification passes were removed.

## Measured result

On the same correction story, ordinary CPU fell from 140.34s to 52.87s (62.3%
lower), passing the 50% target. Wall time fell from 134.93s to 46.40s. The
neighboring amount-only control improved from 58.64s to 27.50s CPU, below the
64.50s regression ceiling. A separate single-process profile counted 44,175
full `facts_of` constructions at baseline and 8,857 afterward: 79.95% fewer,
but 22 above the fixed maximum of 8,835. The selected mechanism leaves that
shortfall; no further local optimization or wider reuse was evaluated to close
it. These are case-specific results, not a whole-suite speedup claim. Exact
commands, environment, derivation counts, and limitations are in the
[durable measurement note](test-replay-performance-evidence/measured-performance.md).

## Completion and remaining limits

Track 0's independent design gate closed READY. Track 1 received independent
semantic review with no material kernel finding; the bounded CI-test repair
delta also had no material finding. Full `verify` succeeded in run
[39551011772](https://github.com/mattidell/attestory/actions/runs/39551011772)
on the repaired implementation: 3,150 passed, 20 skipped, test step 2,814.97s
(46m54s), job 05:41:52–06:29:08 UTC; the test step itself ran
05:42:10–06:29:06 UTC
(46m56s). These are observed CI durations, not a controlled timing comparison.
The milestone PR carries final publication review and the curated candidate's
own CI posture; this implementation run is not a substitute for those checks.

Ordinary focused timing transcripts were not retained, and the reviewer did
not independently rerun those timings. The review inspected profiles and
arithmetic. Raw profiles remain ignored. Full tax-story per-prefix lattice
population was not measured. No proposed-but-unperformed population or
history-size experiment is represented as completed.

Further engine-cost investigation, assessment of genuinely redundant tests,
and useful component-suite boundaries remain for later planning. No mechanism
or test removal is selected here. See the
[retrospective](../../../milestone-retrospectives/2026-10-21-test-replay-performance.md)
and [Engineering Health roadmap](../engineering-health-roadmap.md).
