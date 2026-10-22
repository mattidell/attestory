<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "test-and-ci-efficiency",
  "status": "Closed. Draft pushes get the cheap checks and the fast lane in about a minute; verify fails on drafts and runs in full on ready PRs. Schema-check and historical-lattice reuse cut the sampled Form 1098 test's CPU by 48%; the local suite used 3,601s of CPU against 5,329s at P0. No test was moved.",
  "retrospective": "docs/milestone-retrospectives/2026-10-21-test-and-ci-efficiency.md",
  "scope": [
    "rank whole-suite CPU by module and by engine path, so the next change is chosen by its share of the suite",
    "shorten CI and local feedback without weakening the merge gate, labelled as shorter waiting rather than less work",
    "remove the largest measured repeated engine work whose authority and invalidation are simple",
    "identify expensive tests that only assert rule outcomes and could run below the live coordinator, keeping one live witness per path"
  ],
  "non_goals": [
    "no weaker merge gate: the final head still runs the full suite, mypy, governance lint and the envelope scan",
    "no test deletion or move without a named retained witness for each defect it catches",
    "no persistent or cross-run cache, partial catalog, or skipped validation of unverified bytes",
    "no product, schema, admission or currentness contract change, and no new tax coverage"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/milestone-retrospectives/2026-10-21-test-cost-and-coverage.md",
      "docs/phases/engineering-health/milestones/test-and-ci-efficiency.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/test-and-ci-efficiency.md",
      "docs/phases/engineering-health/milestones/test-cost-and-coverage-evidence/measured-applicability-reuse.md",
      "docs/phases/engineering-health/milestones/test-replay-performance-evidence/measured-performance.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/test-and-ci-efficiency.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-21-test-and-ci-efficiency.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/phases/engineering-health/milestones/test-and-ci-efficiency.md"
    ]
  }
}
-->

# Faster CI, Cheaper Suites, the Same Defects Caught

Milestone key: test-and-ci-efficiency.
Branch: milestone/test-and-ci-efficiency-rank-and-reduce.
Phase: Engineering Health. Opening plan: 2026-10-21.
Starting point: PR #213, merged at `0c620d26`.

## What we are trying to accomplish

The owner selected the test and CI changes proposed after PR #213. Each push
of a milestone branch still waits about 45 minutes for CI, and most of those
pushes change only documents. The two previous milestones made two engine
reads cheaper, but each chose its target from a single story's profile. The
suite has never been ranked by what it spends its CPU on.

This milestone does four connected things, in order:

1. **Rank the suite.** Measure CPU by module and attribute it to engine
   paths, so later choices follow the largest measured shares.
2. **Shorten feedback.** Change the CI workflow and local lanes so a draft or
   documentation push gets a quick answer, and the full gate runs where it
   decides a merge. These shorten waiting; they do not reduce CPU, and are
   labelled that way.
3. **Remove the largest measured repeated engine work** whose authority and
   invalidation are simple, chosen from the ranking.
4. **Review the most expensive tests at the component boundary.** Find cases
   that only assert a rule outcome yet drive the full recorder and live
   coordinator, and say which could run below the coordinator while one live
   case per path keeps the integration witness.

The useful outcome is a faster gate on the same evidence, a measured CPU
reduction, and a ranked, witnessed account of which expensive tests could be
moved. If the evidence does not support a change, record why and stop.

## What we know

- **CI.** `verify` runs on one `ubuntu-latest` runner with 4 xdist workers.
  Cheap checks now run first, and superseded PR runs are cancelled (PR #212).
  The test step took about 47 minutes after PR #212. Every push to an open
  PR, including documentation-only pushes and drafts, runs the full suite.
- **Suite shape** (measured 2026-10-20, before PRs #212 and #213; not a
  current ranking). About 3,141 tests and 5,246 subtests, 273 CPU-minutes on
  10 local cores. Student-loan modules took 74% of CPU; the top 20 of 238
  modules took 87%. `test_sli_track1_combined_standing` and
  `test_sli_correction_session` alone took 27%. Half the tests (1,563 in 93
  modules) drive the live coordinator.
- **Engine paths in the retained story profile** (PR #213's P0, summarized
  in its retrospective and measurement note):
  - `live_coordinate_run` resolves and fully validates the adopted package
    on every call: 22.7s cumulative across 11 returns, with no reuse beyond
    the schema-validation memo.
  - `compute_currency` builds the full historical lattice through
    `_declared_edges` on every call: 2,833 builds, 14.5s cumulative.
  - `SchemaRegistry.validate_declared` ran 47,519 times for 21.4s cumulative
    even with its content-addressed memo; whether that time is spent building
    cache keys is unknown.
  These are one story's nested diagnostics, not suite shares or savings.
- **Fast lane.** `-m "not live"` has had about 22 inherited budget failures,
  so it is not a trusted inner gate.

What we do not know: each engine path's share of whole-suite CPU, and which
expensive cases need the live coordinator to catch their defect.

## Actions the team will take

1. **P0 — rank the suite.** Run the full suite once with per-test durations
   (`--junitxml`) and aggregate CPU by module. Profile a small fixed sample of
   the top modules by share and attribute their time to package resolution
   and validation, currency and historical lattice builds, `project` folds by
   caller, fixture construction and the coordinator's own derivation. Report
   each as an estimated share of suite CPU, with the sample's limits. Record
   the producer commit for every profile. No change is chosen before this.
2. **Track 1 — CI and lane feedback.** Independent of P0, and labelled as
   feedback only:
   - drafts and documentation-only pushes run the cheap checks and the fast
     lane; the full suite runs on ready-for-review PRs and on `main`, so the
     merge head is always fully gated;
   - publish per-test durations from every run;
   - evaluate `--dist worksteal` against the long-tail live tests;
   - split a fast job (cheap checks plus fast lane) from the live job, so a
     cheap failure reports in minutes;
   - repair or honestly re-mark the fast lane's budget failures, without
     raising the budget, so `-m "not live"` can be trusted locally.
   Sharding and larger runners stay unselected; they cost runner minutes.
3. **Track 2 — measured engine reuse.** From P0's ranking, take the largest
   repeated work with a simple authority account. The leading candidates:
   - **Validated-package reuse keyed by verified content.** Published content
     is immutable and checksum-pinned (release to registry to members).
     Adoption selection and checksum verification still run on every call;
     only re-validation of byte-identical, already-verified content is
     reused. The key includes the schema-registry digest and the validator
     version; nothing is reused across different bytes or registries, and
     nothing outlives the process.
   - **Historical-lattice reuse inside currency**, keyed by exact fact-state
     object identity, the same boundary PR #212 proved for the current
     lattice. Nothing is reused across states.
   - **Schema-validation memo key cost**, if P0 shows the key, not the
     validation, is the expense.
   One connected design note, one build, one independent review of the
   connected change, and full CI. Measure the same cases before and after.
4. **Track 3 — component boundary for the expensive tests.** For the top
   modules by share, classify each case: needs recorder and coordinator, or
   asserts only a rule outcome that the derivation runner with a marshalled
   context would witness. Move a case only when its retained witness is named
   and one live case per path remains. The result may be a ranked
   recommendation rather than moves.
5. **Close.** Report the measured CPU change, the CI waiting change, and what
   remains costly. Independent publication review and exact-head CI.

## Current design state

**P0 is complete** ([suite ranking](test-and-ci-efficiency-evidence/p0-suite-ranking.md)).
The full suite took 628s wall and about 89 CPU-minutes (5329s user plus
system), down from 273 CPU-minutes before PRs #212 and #213. Live tests hold
96% of summed worker time; student-loan modules 59%. Package validation turned
out cheap after the first call in a process (the schema memo hits 95–99%), so
it is no longer a leading candidate. The estimated suite shares are:
fact-type `check_schema` during bundle adoption 11–19%, current-lattice
rebuilds when the fact state changes 11–20%, historical-lattice builds inside
currency 7–21% (30–50% of the form-route profiles), and every package-validation
or marshalling path under 4%. The correction-resumption module (9.3%) spends
its time waiting on a browser subprocess, not in the engine.

**Track 2 takes the two simplest-authority items at the top:** reuse of the
fact-type `value_schema` check keyed by the schema document's canonical
content and the validator version, and reuse of the historical lattice keyed
by exact fact-state object identity, the boundary PR #212 proved for the
current lattice. Current-lattice rebuilds after the state changes need an
incremental-lattice design and are not in this track. Track 1 used P0's fast-lane list for its marks.

**Tracks 1 and 2 are built and independently reviewed READY**, each after one
repair (a skipped `verify` satisfied branch protection; a schema-check key
treated a tuple like a list). Draft pushes now get the cheap checks and the fast
lane in about a minute; `verify` fails on a draft and runs in full on a ready
PR. Worksteal is adopted. After Track 2 the local full suite used 3,601s of CPU
against P0's 5,329s.

**Track 3 found no worthwhile test moves** ([classification](test-and-ci-efficiency-evidence/track3-component-boundary.md)).
Of 231 cases in seven expensive modules, 94 need the live coordinator, 126 are
mixed and 3 are rule-only. Moving every safe candidate below the coordinator
would recover about 50s (0.8% of suite time), because each case's time is in
its recorder projecting the log after every act, which a move keeps. The moves
would also drop the check that coordinator publications match the forward
runner. No test is moved. The remaining cost is recording and projection.

## Decisions that need evidence

- Which engine path holds the largest share of suite CPU? P0 answers this;
  Track 2 follows it.
- Does a reuse key cover everything that can change the result? Validated
  content needs the bytes, the schema registry and the validator version;
  historical lattices need the exact state.
- Which expensive cases need the live coordinator? Name the defect each catches
  before proposing a move.
- Does the draft and documentation fast path ever let an unverified head merge?
  It must not: branch protection and the ready-for-review run decide that.

## Readiness, evidence and contracts

No schema, admission, currentness, source-closure or saved-result contract
changes. Track 2 is an internal reuse whose Track 0 integration surface is N-A;
it still needs a written authority, lifetime and invalidation account and an
independent review before acceptance. Track 3 moves no test without named
retained witnesses. Raw profiles and timing output stay in ignored paths;
publish normalized evidence and its limits.

Work proceeds with one connected review per change, not a separate review of
each paper refinement. Focused lanes support each increment. Full CI on the
final head remains the gate of record.

## Execution record

| Unit | Result |
| --- | --- |
| P0 | One full run with per-test durations and eight single-process profiles ranked the suite: 89 CPU-minutes; fact-type schema checks, current-lattice rebuilds and historical-lattice builds lead; package validation is cheap after the first call. |
| Track 1 | Two CI jobs: `quick` (cheap checks and fast lane) on every push; `verify` fails on drafts and runs in full otherwise. Per-test durations published. 97 slow integration tests moved out of the fast lane by `live` marks with reasons (they still run in every full `verify`). `--dist worksteal` adopted. The resumption wait is real browser work. Independent review found a skipped `verify` satisfied branch protection and a too-broad module mark; both repaired and confirmed. |
| Track 2 | Process-local reuse of a successful fact-type schema check (strict-JSON canonical content, validator version, draft) and of the historical lattice for an exact fact-state object. Independent review found a tuple/list key collision; repaired and confirmed. |
| Track 3 | Classified 231 cases in seven expensive modules. Safe moves below the coordinator would recover about 0.8% of suite time; no test was moved. |

## Outcome

**Feedback.** A draft push gets mypy, governance lint, the data-boundary scan
and the fast lane in about a minute. The full gate runs when a PR is marked
ready and on every later push, and on pushes to the gated lines. Every full run
publishes per-test durations. These shorten waiting, not work.

**Work.** The sampled Form 1098 production test used 56s of CPU instead of 108s,
and the correction-session test 30s instead of 36s. The local full suite used
3,601s of CPU after Track 2 against 5,329s at P0; these are single local runs,
not a controlled comparison. Worksteal cut local wall time from 510s to 426s in
one paired run.

**Assurance.** No test was removed, skipped or moved below the coordinator; no
assertion or budget changed. Live marks moved 97 integration tests (they run
derivation runners, recorders, package validation or golden regeneration) out
of the fast lane, which fell from 1,609 to 1,516 tests; all of them still run in
every full `verify`. Much of their fast-lane time on the CI runner is a cold
first-use cost on each worker, so a per-worker warm-up in test setup could
return some of them to the lane.

**Remaining cost.** Recording and projection: `findings.project` folds the whole
log from the start hundreds of times per test. The retrospective lists the
follow-up order.
