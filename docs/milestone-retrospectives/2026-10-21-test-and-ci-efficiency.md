# Retrospective — Faster CI, Cheaper Suites, the Same Defects Caught

## Result

- **CI feedback.** A draft push now gets mypy, governance lint, the
  data-boundary scan and the fast lane (about 1,510 tests) in about a minute in
  the `quick` job. `verify` fails on a draft without running the suite and runs
  in full on a ready PR and on pushes to the gated lines. Every full run
  publishes per-test durations. These shorten waiting; they do not reduce work.
- **Engine CPU.** Track 2 reuses a successful fact-type `value_schema` check
  (keyed on strict-JSON canonical content and the validator version) and the
  historical lattice for an exact fact-state object. The Form 1098 production
  test fell from 108s to 56s of CPU and the correction-session test from 36s to
  30s. The local full suite used 3,601s of CPU after Track 2 against 5,329s at
  P0 (single runs, same machine; not a controlled comparison).
- **Scheduling.** `--dist worksteal` cut local full-suite wall time from 510s to
  426s in one paired run.
- **Fast lane.** 97 integration tests were marked live, each class or test
  with a stated reason, so the lane fell from 1,609 to 1,516 tests; they still
  run in every full `verify`. The lane passes locally; its CI result is the
  `quick` check on the final head.
- **Tests.** No test was moved or removed. Track 3 classified 231 cases in seven
  expensive modules and found that moving every safe candidate below the
  coordinator would recover about 0.8% of suite time.

## Material dissent and repairs

- Independent review found that a skipped `verify` satisfied branch
  protection, so a draft PR was reported mergeable with the full suite never
  run on its head. The repair makes `verify` fail on drafts instead.
- Independent review found that the schema-check key treated a tuple like a
  list, so a cached valid schema could admit an invalid twin. The repair keys
  only strict JSON trees.
- A module-wide live mark moved a 0.02s structural test out of the fast lane;
  class marks replaced it.
- The opening hypothesis that package validation dominated was wrong: after the
  first call in a process the schema memo hits 95–99% of the time.

## Lessons

- Rank the suite before choosing a target. Two earlier milestones each chose
  from one story's profile; a single full run with per-test durations plus a
  small fixed profile sample changed the ranking.
- A skipped job is a success. A required check must fail, not skip, when it did
  not do its work.
- A cache key built from serialized text is only as faithful as the
  serialization; require the input to be the type the text describes.
- On the CI runner, the first derivation-running test on each worker pays a
  cold first-use cost: tests at 1.2s locally took 4.2–4.3s there. Budget
  failures on CI follow that cost, not a fixed slowdown, so marking only the
  tests that failed in one run moves the failure to a sibling. Mark the classes
  whose cases do the integration work.
- Moving tests below the coordinator saves little when the recorder, not the
  coordinator, holds the cost. Measure the per-call saving before proposing
  moves.

## Follow-ups

- **Re-projection.** `findings.project` folds the whole log from the start,
  hundreds of times per test. In order: fold incrementally within one
  `ActLog.append_batch` save instead of re-projecting before each checked act;
  share one projection through each recording or review operation; only then
  consider an in-process prefix memo keyed by exact act content and registry
  state. Choose from a P0 of the recorder and save paths.
- **Current-lattice rebuilds** after the fact state changes (11–20% at P0)
  need an incremental-lattice design.
- **Correction resumption** (about 9% of worker time) is real browser work.
- **Fast-lane warm-up.** A per-worker warm-up in test setup (outside the
  budgeted call phase) could absorb the cold first-use cost and return some of
  the 97 marked tests to the fast lane.
