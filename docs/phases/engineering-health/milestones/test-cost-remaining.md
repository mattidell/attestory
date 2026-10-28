<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "test-cost-remaining",
  "status": "Closed. Mortgage recording and review reuse one projection inside the operation. A checked save folds its prefix incrementally and refuses as before. Full verify runs as four shards under the same verify job. PR #226 exact-head verify had not succeeded when this record was written. The next milestone is unselected.",
  "retrospective": "docs/milestone-retrospectives/2026-10-28-test-cost-remaining.md",
  "scope": [
    "rank current test CPU and waiting time before selecting work",
    "reuse one projection inside a mortgage recording or review operation",
    "fold a checked save incrementally, with the same admission and refusal",
    "shorten full-verify waiting by sharding, and keep the verify job as the required check"
  ],
  "non_goals": [
    "no test removal, skipping, moving, or fast-lane budget increase",
    "no content edits",
    "no edit to the parallel milestone's derivation files",
    "no suite-wide speedup claimed from one profile, and no CI speedup claimed from a failed or unfinished run"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md#Current boundary and remaining work",
      "docs/milestone-retrospectives/2026-10-22-projection-reuse.md",
      "docs/milestone-retrospectives/2026-10-21-test-and-ci-efficiency.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/test-cost-remaining.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/test-cost-remaining.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-28-test-cost-remaining.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/phases/engineering-health/milestones/test-cost-remaining.md"
    ]
  }
}
-->

# Remaining Test and CI Cost

Milestone key: `test-cost-remaining`. Branch: `milestone/test-cost-remaining`.
Phase: Engineering Health. Opened from the main line that published duration
run [40515157618](https://github.com/mattidell/attestory/actions/runs/40515157618).
Draft-to-final PR: [#226](https://github.com/mattidell/attestory/pull/226).

## What we are trying to accomplish

The full suite protects the product, and each development unit waits for it.
Recent full checks had taken 42–65 minutes, longer than the local run. The
aim was a measured reduction in a real source of that cost, with the same
tests and the same defect detection. A faster product operation also shortens
the wait on a long-lived workspace.

Elapsed waiting, processor time, and runner cost are different clocks. A
parallel job can shorten the first while leaving the second unchanged and
raising the third. One case's profile does not state a share of the suite.

## What was selected

P0 measured the unchanged local suite and the current CI runner, then stopped.
Independent review corrected one attribution and left the alternatives
decision-ready. The owner then selected three changes, in order:

1. Reuse one projection inside a mortgage recording or review operation, so
   the same acts are not folded twice in that call.
2. Fold a checked save incrementally, after equivalence with today's
   admission, refusal, and refusal timing was demonstrated.
3. Shorten CI waiting with a layout whose evidence separates waiting from
   processor time and runner cost.

Each unit was reviewed before the next began. No test was removed, skipped,
moved between lanes, or given a higher fast-lane budget. `packages/content/`
was not edited. `packages/derivation/live.py` and
`packages/derivation/subject_dispatch.py` match the ratified line.

## What the software does

**Mortgage recording and review.** An operation that already holds a
projection of the current acts and registry reuses it for the later reads in
that call. When the Form 1098 bundle helper appends an act, it applies that
act before returning, so the later reads see the longer list. Answer
validation does not fold again while it holds that projection. A mortgage
review passes its projection into the payment-comparison support read. A
comparison save reuses the projection only when adoption did not append; an
appended bundle is a different list, and support folds the pre-append acts
again. The post-save reads still fold the log that was written. A public call
that does not receive a projection folds on its own. Withdrawing a Form 1098
answer still folds its own staged list. Nothing is remembered across calls.

**Save folding.** One `append_batch` builds one fold for that call. Schema
validation, the incomplete tail, the expected revision, `committed_against`,
and duplicate ids still run before any fold. A checked act is one where the
new-write step may apply, or whose kind is horizon genesis, member transition,
or family handover. For that act the fold applies only the staged acts past
its cursor, using the same applier `project` uses. The act being admitted is
not added to the cursor on its own turn. An unchecked act is written without
that fold and is folded only when a later checked act in the same call asks
for a prefix that contains it. `append` of one act still calls `project` once
when that act is checked. A refusal writes nothing. The pending file, fsync,
size check, rename, and directory fsync are unchanged. The fold is dropped
when the call returns. Historical `project` is unchanged. This stays inside
the existing targeted pre-save scope; it is not a fold of every act kind
before the write.

**CI.** The required check on `main` and `main-ui` is still the job named
`verify`. The suite is the collection one pytest process would collect,
packed longest-first into four shards. Each shard runs with the repository's
existing xdist settings and with no marker filter and no deselection. Cheap
checks run in `precheck` and must succeed before any shard starts. Each shard
installs the envelope hooks in its own checkout before the suite starts.
`verify` always runs and exits unsuccessfully unless this is a full-gate
event and both `precheck` and every shard finished with result exactly
`success`. A draft pull request fails in that draft step and does not start
the suite. `quick` still runs the cheap checks and the fast lane, including
on drafts. The duration file used to pack shards is
[ci-node-durations.json](test-cost-remaining-evidence/ci-node-durations.json).
Its clock is junit testcase time from run 40515157618: worker wall seconds,
not CPU.

Each shard also prepares an independent historical baseline before pytest.
Pull requests use the event's base, main pushes use the prior main revision,
and main-ui pushes compare with main; preparation fails when the required
revisions or file are unavailable, inconsistent, or self-referential. When
main-ui converges on the main tip, the prior main-ui revision supplies an
independent witness. This conservatively refuses a convergence that restores
historical bytes already on main if the prior main-ui bytes differ: the event
does not supply an independent prior-main witness. Main movement during the
guard's observations can require a rerun; movement afterward is not observed.

## Measured evidence

The notes under [test-cost-remaining-evidence/](test-cost-remaining-evidence/)
keep the producer detail. Figures below are those records. Profile cumulative
time includes nested work. One local run on a busy machine is not a controlled
comparison.

### One local suite at P0, and the CI runs of that same suite

One local full run, 10 workers, exit 0. Real time 716.78s. Pytest wall
715.93s. User 5428.95s, system 317.41s, user plus system 5746.36s. Collected
3544, passed 3524, skipped 20. The 3544 junit rows sum to 6978.30s of worker
wall time, which is above CPU because a worker's clock runs while it is not
on a core. Load was already above the machine's core count. Wall time includes
that contention. User plus system is the waited process tree.

The mortgage calculation module is 1923.6s of that worker-wall sum, 66 tests,
27.6%. Its slowest case is 81.30s in the suite, 1.2% of the sum. Live-shaped
modules hold 6937.9s, 99.4% of the sum. Runner CPU on the CI jobs of this
suite was not recorded. Those jobs ran the same 3544 tests on 4 workers at
pytest walls of 2409.25s, 3298.91s, and 3843.75s. Summed worker time moved
with that wall. Queue before the job was 2–4s, and the pip cache was already
hitting. On the main-merge job, work outside pytest was about 24s and `quick`
finished in 69s with a 38s fast lane.

### One-case profiles

These are cold, single-process profiles under cProfile. They are not the
junit time of the same test on a warm worker, and they are not a suite share.

| Case | Suite junit | What changed in the profile |
| --- | ---: | --- |
| Mortgage late member | 81.30s | Real 124.54s to 98.57s. User plus system 123.89s to 98.03s. `findings.project` 270 calls / 77.503s to 194 calls / 52.353s. Three callers disappeared: the answer projection, answer validation, and comparison support (76 calls, 24.364s). The other callers kept their call counts. The module's other 65 tests were not profiled. |
| Form 1099-K review | 10.19s | Real 42.76s to 37.68s. User plus system 42.38s to 37.02s. `findings.project` 84 calls / 8.770s to 10 calls / 2.663s. `append_batch` 6.189s to 1.221s. The 74 batch projections became 74 `through` calls at 1.085s. Non-batch caller counts matched the baseline, so this drop is the save fold. |
| Form 1098 production | 52.54s | Real 108.13s to 73.05s. User plus system 107.49s to 72.36s. `findings.project` 540 calls / 57.032s to 72 calls / 19.531s. `append_batch` 31.771s to 3.607s, and 444 batch projections became 444 `through` calls at 3.121s. Twenty-four of the missing projections are the mortgage recording reuse. This wall clock mixes both changes. |

On the short student-loan profiles, the three helper sites still outside this
work (`_stage_enrollment_follows_schooling`, `_scan_displayed_answers`,
`_attribute_borrowing_labels`) were 0.13s to 2.30s inside profiles of about
47–49s. The resumption profile spends its time in the browser, not in
`findings.project`.

### Later local full runs

Membership changed, so these clocks sit beside the P0 suite. They do not
replace it as a before-and-after.

| Run | Collected | Passed | Skipped | Pytest wall | User plus system |
| --- | ---: | ---: | ---: | ---: | ---: |
| P0 baseline | 3544 | 3524 | 20 | 715.93s | 5746.36s |
| Save-fold substrate check | 3565 | 3545 | 20 | 582.43s | not recorded |
| Pre-ready candidate | 3574 | 3554 | 20 | 583.18s | 4994.57s |
| Tree combined with current main | 3612 | 3592 | 20 | 609.33s | 5149.65s |

The combined-tree run also reported repository mypy clean for 415 source
files. Its local shard assignment placed the 3612 collected ids into lists of
900, 912, 900, and 900, with no duplicate and no omission. Sixty-eight ids
are absent from the duration file and take the median fallback weight. That
assignment is not a GitHub execution.

### CI observations

One full sharded `verify` succeeded before the later historical-baseline fixes.
Exact final-head `verify` remains outstanding.

The packing model, on the 3574-test collection and the older duration file,
puts four shards at a pytest wall of 816.3s. That figure leaves out checkout,
setup, cold starts, `precheck`, the verify tail, and host-speed variation.
The same tests already moved from 2409s to 3844s of pytest wall on one
runner. The model is not a forecast and not a measurement of this suite.

Run [40618847234](https://github.com/mattidell/attestory/actions/runs/40618847234)
is the first full fan-in. It failed. Workflow elapsed time was 1004s and ended
in failure. The slowest shard's pytest process was 940.47s. The four pytest
process trees used 12808.57s of user plus system, at 370–387 percent of CPU
on 4 cores, so the xdist children were included. The sum of the seven job
walls is 3559s of runner occupancy. That sum is not the wait. The usage
payload did not report billed minutes. Every shard collected 3574 tests.
Assigned counts were 891, 902, 891, and 890. The only failure was the
envelope-hook clone check on shard 0: that checkout had not installed the
hooks. The other three shards exited 0 because the check was not assigned to
them. `verify` then exited unsuccessfully and skipped coverage. The hook
install now runs on every shard before the suite. Those repaired shard jobs
had not run when independent review closed.

Run [40609713044](https://github.com/mattidell/attestory/actions/runs/40609713044)
is a draft run of this workflow. `verify` failed in the draft step. `precheck`
and the shards did not start.

Run [40628919957](https://github.com/mattidell/attestory/actions/runs/40628919957),
on the pull-request head that precedes this curation commit, was cancelled.
Its `verify` job failed in the draft step and did not start the suite. That
is the draft gate, followed by cancellation. It is not a suite result.

Run [40628958771](https://github.com/mattidell/attestory/actions/runs/40628958771)
is the non-draft run of that pre-final head. `quick`, `precheck`, all four
shards, and `verify` succeeded. Workflow elapsed time was 1022s, from
03:51:23 to 04:08:25 UTC. It predates the historical-baseline fixes and does
not verify the final head. CPU and billed minutes for this run are not
recorded here.

## Independent review

P0 review blocked one sentence that priced the mortgage duplicate as a kernel
change. The caller partition is a second projection inside `packages/tax`.
The save path and the lattice stayed in their own alternatives. After that
correction the eight alternatives were decision-ready, and the review
selected nothing. The owner selected afterward.

Mortgage reuse was reviewed ready. Replayed answer, correction, withdrawal,
review, comparison, and refusal paths matched the parent on the acts, the
current values, and the refusal outcomes. The measured CPU change is the one
profiled case.

Save folding was reviewed ready. The differential tests compare exception
type and message, the first refused index, the revision, pending-file
presence, and the final log bytes with a fresh projection. Further synthetic
histories, including a refusal that must leave the previous bytes, matched
that fresh projection. The oracle repeats the admission predicates, so a
mistake introduced on both sides would not show up there; the cursor itself
is outside that copy. The fold calls `project`'s private applier. A later
`project` that stops using that applier would leave the save path behind.
The demonstrated equivalence is the committed tests plus the histories that
were run. It is not every act sequence.

The shard gate and hook repair were reviewed on their fail-closed paths. A
subsequent review identified that the historical comparison could silently
pass without its ref, and that a main push could compare against itself. The
guard was repaired and independently reviewed ready for the bounded repair:
synthetic unchanged convergence passes and changed bytes fail. The divergent
main-ui restoration limitation above remains. The review did not exercise a
GitHub event or a full suite, and event ancestry checks rely on GitHub's
supplied revisions.

## Limits that remain

- No suite-wide saving is inferred from the three profiles.
- The later local suite clocks are different collections from the P0 suite.
- Runner CPU is recorded for the failed fan-in only. The successful prior
  run's workflow wait is known, but its CPU and billed minutes are not here.
- The 816.3s model uses weights from before the mortgage reuse and the save
  fold. Ids missing from that file take a median of 0.040s.
- Host pace on identical tests already spanned 2409s to 3844s of pytest wall.
- Separate calls, a checked single-act `append`, and the post-save reads still
  project from scratch. Form 1098 withdrawal still folds on its own.
- Current-lattice rebuilds, a cross-call prefix memo, and the three named
  helpers were not taken.
- A divergent main-ui historical file cannot be restored to main's bytes at
  convergence without an independently established prior-main witness.
- Exact-head `verify` on PR #226 is still the merge gate.

## Contracts, fixtures, and verification

No published schema and no product ADR changed. Admission, refusal, and the
bytes left after a refusal stay on the existing save contract. The mortgage
reuse is a read of the projection the call already holds, dropped when the
call returns. Synthetic `demo.*` data only. The duration file holds test ids
and durations from a public CI run.

The mortgage behavior is pinned by `tests/test_mortgage_projection_reuse.py`.
The save behavior is pinned by `tests/test_save_fold_equivalence.py` together
with the existing batch and restoration tests. Shard assignment, the
fail-closed fan-in, and the hook install are pinned by `tests/test_ci_gate.py`
and `tests/test_ci_shard_checkout.py`; the historical baseline guard has its
own synthetic event and convergence tests. The kernel change required the full
suite and mypy; both passed on the tree combined with current main, as the
table above records. GitHub `verify` on the exact publication head remains
the gate of record.

## Execution record

| Unit | Result |
| --- | --- |
| P0 | Ranked the local suite and the CI runs of that suite. Independent review ready after the mortgage attribution was corrected. No slice selected by the review. |
| Track 1 | One projection reused inside mortgage recording and review. Independent review ready. One-case CPU drop recorded above. |
| Track 2 | Incremental fold inside one checked `append_batch`, with the same refusal behavior on the tested histories. Independent review ready. |
| Track 3 | Four-way shard of the full suite under the existing `verify` job. The first full run failed the missing hook install; a subsequent run succeeded before the independently reviewed historical-baseline guard. The guard retains the convergence limitation above. Final-head `verify` remains outstanding. |

## Outcome

The three selected changes are in the tree. Their measured effects are the
one-case profiles, the local full runs, and the sharded CI runs above.
Publication still waits on a successful `verify` of the exact head the owner
merges. The next milestone is unselected. Remaining work is in the
[retrospective](../../../milestone-retrospectives/2026-10-28-test-cost-remaining.md).
