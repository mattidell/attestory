<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "projection-reuse",
  "status": "Closed. Recording, review and correction reuse one projection per call: save, correct and withdraw fold the log once instead of three or four times (60-72% less CPU on the long history). A per-worker fast-lane warm-up returned 19 tests to the lane. The save-path incremental fold was skipped as the smallest share.",
  "retrospective": "docs/milestone-retrospectives/2026-10-22-projection-reuse.md",
  "scope": [
    "attribute the repeated whole-log projections to the recording, review and save operations that cause them",
    "fold incrementally within one ActLog save, preserving today's exact admission and refusal behavior",
    "share one projection through each recording or review operation instead of re-projecting in its helpers",
    "absorb the CI worker's cold first-use cost outside the budgeted test call, and return marked tests to the fast lane only where they then fit"
  ],
  "non_goals": [
    "no change to what a save admits or refuses: a stricter full pre-save fold is ADR 0079's not-decided item and returns to the owner as a contract choice",
    "no reuse across calls or processes: a projected-prefix memo stays a named candidate, not in scope",
    "no weaker merge gate, no test deletion, skip, assertion change or raised fast-lane budget",
    "no product, schema, currentness or saved-result change, and no new tax coverage"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/milestone-retrospectives/2026-10-21-test-and-ci-efficiency.md",
      "docs/phases/engineering-health/milestones/projection-reuse.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/projection-reuse.md",
      "docs/phases/engineering-health/milestones/test-and-ci-efficiency-evidence/p0-suite-ranking.md",
      "docs/adr/0079-family-version-handover-and-containment.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/projection-reuse.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-22-projection-reuse.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md",
      "docs/phases/engineering-health/milestones/projection-reuse.md"
    ]
  }
}
-->

# Fold Once: Less Replaying of the Same History

Milestone key: projection-reuse.
Branch: milestone/projection-reuse-fold-once.
Phase: Engineering Health. Opening plan: 2026-10-21.
Starting point: PR #214, merged at `b475de37`.

## What we are trying to accomplish

The owner selected the re-projection fixes proposed at the close of PR #214.
`findings.project` folds a workspace's whole act history from the start. The
last suite ranking found it called hundreds of times per test: 94 to 540 times
in the sampled tests, mostly from product recording and review (39–77% of its
time) and from the save path (8–56%). A real workspace with a long history pays
the same cost on every save and review, so this is product work as well as test
cost.

The fixes, cheapest and safest first:

1. **Fold incrementally within one save.** `ActLog.append_batch` re-projects the
   whole log plus the staged acts before each lifecycle or new-write act it
   checks, then discards that projection. Because the fold is pure, it can
   project the committed log once and advance a running state act by act.
2. **Share one projection per operation.** One recording or review call
   projects in the recorder, in helpers such as `_current` and
   `borrowing_recognition_clues`, and again in review. Passing one state through
   the operation removes the repeats, the same one-invocation boundary PR #213
   used.
3. **Warm the fast lane per worker.** On the CI runner, the first
   derivation-running test on each worker pays a cold first-use cost (1.2s
   locally became 4.2–4.3s). PR #214 marked 97 integration tests live, partly
   for that reason. A per-worker warm-up outside the budgeted test call could let
   some return to the fast lane.

The useful outcome is fewer whole-log folds per save and per operation, a
measured CPU reduction on the same cases, and an honest fast-lane result. If a
fix would change what a save admits or refuses, stop and bring it back.

## What we know

- The full suite used about 3,600s of CPU locally after PR #214's reuse, against
  5,329s at the previous milestone's P0. The CI `verify` on PR #214's merge is
  the current whole-suite observation.
- `project` is a pure left fold over acts (`packages/kernel/findings.py`,
  `project`). `ActLog.append` projects the committed log for its checks;
  `append_batch` re-projects `staged` before each checked act
  (`packages/kernel/act_log.py`, `append_batch`). Today only lifecycle acts
  (`horizon-genesis`, `member-transition`, `family-handover`) and acts subject to
  the ADR-0077 new-write step are checked before saving.
- ADR 0079 lists a full pre-save fold of every act kind as **not decided**. An
  act the fold would reject but that is not checked today is saved, and then
  fails the next `project`.
- What we do not know: how many whole-log folds each recording, review and save
  operation performs, by caller, on long and short histories; and how much of
  the fast lane's CI time is cold start.

## Actions the team will take

1. **P0 — attribute the folds.** Profile a fixed sample of operations through
   the real recorders and save path, on a short and a long synthetic history:
   record a statement, save answers, correct, withdraw, remove, and review. For
   each, count `project` calls and their callers, the acts folded per call, and
   `append_batch` checks per batch. Report folds per operation and estimated
   share of suite CPU, with limits. Record the producer commit. No change is
   chosen before this.
2. **Track 1 — incremental fold in one save.** Project the committed log once
   per `append` or `append_batch` call and advance a running state through the
   staged acts. **Preserve today's exact admission and refusal behavior**,
   including when a refusal is raised and which acts are checked. If an
   unchecked act fails to fold, today's behavior is that a later checked act's
   projection raises; the running state must reproduce that, not refuse earlier
   or later. Differential tests compare every refusal and every admitted log
   with the current implementation on the same batches.
3. **Track 2 — one projection per operation.** From P0's callers, pass one state
   through each recording or review operation where helpers re-project the same
   acts. Public cold readers keep projecting freshly; historical-prefix reads
   keep reading their own prefixes. Nothing is retained after the call.
4. **Track 3 — fast-lane warm-up.** Add a per-worker warm-up in test setup,
   outside the budgeted call phase, that pays the cold first-use cost once.
   Measure the marked tests' call times on the CI runner. Return a test to the
   fast lane only where it then fits the unchanged 3-second budget with margin.
   The budget, assertions and live/fast meaning stay the same.
5. **Close.** Measure the same cases before and after; report folds per
   operation and CPU separately from waiting. Independent review of each
   engine change and exact-head CI.

## Current design state

**P0 is complete** ([fold attribution](projection-reuse-evidence/p0-fold-attribution.md)).
Across record, answer, correct, withdraw, remove, review and one coordinator
run on a short (266-act) and a long (307-act) synthetic history, repeated
helper projections inside one operation were 90.6% of acts folded and about
75% of the CPU proxy. The save path's checked re-projections were 4.9% (answer,
correction and withdrawal saves checked nothing; record and remove checked
once each), and the coordinator's own fold 4.5%. The leading re-projectors are
`f1099k_statement_recording._commit` and `_ensure_bundles`,
`prepare_f1099k_statement_review`, `_record_borrowing_answer_durably` and
`borrowing_recognition_clues`. A fresh process paid 2.4s of CPU on its first
derivation call and 0.03s on the second.

**Order changed:** Track 2 (one projection per operation) went first, then
Track 3 (warm-up). Track 1 (the save path) was skipped as the smallest share
with the strictest behaviour-preservation requirement; it is a follow-up.

## Decisions that need evidence

- Which operations cause most whole-log folds, and which callers? P0 answers.
- Does the incremental fold reproduce every current refusal and admitted log?
  Differential tests answer; if not, stop.
- Is a stricter pre-save fold wanted? That is an owner contract choice under
  ADR 0079, not part of this milestone.
- After Tracks 1 and 2, is projection still dominant enough to justify a
  cross-call prefix memo? Only then does it return as a candidate, with its own
  authority account (exact act content and registry state).

## Readiness, evidence and contracts

No admission, currentness, schema, source-closure or saved-result contract
changes. Track 1 and Track 2 are internal reuse inside one call; each needs a
short design note (what is reused, its key and lifetime, what still runs, how a
failure surfaces) and one independent review of the connected change. Track 3
changes test infrastructure only. Raw profiles and timings stay under `temp/`.

Implementation uses the targeted lanes and `python -m mypy`; full CI on the
ready head is the gate of record. One connected review per change.

## Execution record

| Unit | Result |
| --- | --- |
| P0 | Counted whole-log folds per operation on a short and a long synthetic history: helper re-projection within one operation was about 91% of acts folded; the save path under 5%; a worker's first derivation call cost 2.4s of CPU, the second 0.03s. |
| Track 2 | One projection per recording, review or correction call in the Form 1099-K recorder and review, the student-loan answer recorder and recognition clues, and the correction session. Two helpers were fixed to advance their own state. Independent review READY after one design-note correction. |
| Track 3 | Per-worker fast-lane warm-up in test setup; six classes (19 tests) returned to the fast lane; `quick` green on the CI runner with 1,528 tests in 23s. |
| Track 1 | Skipped: under 5% of folded acts, with the strictest refusal-preservation requirement. |

## Outcome

**Work.** On the long synthetic history, save, correct and withdraw fold the
log once instead of three or four times, with 60–72% less CPU; record and
remove fold twice instead of four times. A local full run used 3,125s of CPU
and 403s of wall time against 3,488s and 426s for the previous milestone's
comparable run (single runs, not a controlled comparison).

**Feedback.** The fast lane runs 1,528 tests in about 23s on the CI runner, 19
more than before, with the cold first-use cost paid once per worker in setup.

**Assurance.** No result, refusal, saved act or saved output changed; Track 2's
regressions compare each operation's state with a fresh fold of the committed
log. No test was removed, skipped or weakened, and the fast-lane budget is
unchanged.

**Remaining.** The save-path fold, the remaining helper re-projections outside
Track 2's sites, and current-lattice rebuilds; see the retrospective.
