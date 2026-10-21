# Measured performance — fold-local lattice reuse

## Cases and method

The unchanged synthetic correction story was
`tests/test_sli_deduction_end_to_end.py::TheDeductionFollowsWhatThePersonSays::test_the_story`;
the neighboring amount-only control was
`tests/test_sli_track5_worksheet_integration.py::LinkLifecycle::test_an_amount_only_correction_changes_the_deduction`.
The story exercises statement entry, linked answers, corrections and
restorations, withdrawal, an interrupted batch and recovery, re-answer, saved
explanations, and agreement between coordinator and reference output. Each of
its 11 returns performs three derivations: the live coordinator's saved run,
the test-side forward run, and the test-side reference run. The control has two
returns. These test-side derivations are not save-admission work.

P0 was measured before the kernel change, after the workflow-only CI unit; the
post-change ordinary and diagnostic runs used the same unchanged story and
control. No source change intervened in the baseline. Environment: macOS, Python
3.14.3 via `.venv/bin/python`, pytest 9.1.1, pytest-xdist 3.8.0, default
ordinary xdist setting of 10 workers. Ordinary tests were uninstrumented;
diagnostic profiles used single-process `-n 0`. Ordinary timing transcripts
were not retained. The reviewer inspected retained profiles and arithmetic,
but did not independently rerun the ordinary timings. Raw profile files are
ignored, not published.

## Commands and ordinary timings

Each ordinary command was run once. Values are reported as pytest duration,
wall, user, system, then user+system CPU. Diagnostic profiling is a separate
measurement and must not be compared to ordinary wall time.

```sh
/usr/bin/time -p .venv/bin/python -m pytest tests/test_sli_deduction_end_to_end.py::TheDeductionFollowsWhatThePersonSays::test_the_story
/usr/bin/time -p .venv/bin/python -m pytest tests/test_sli_track5_worksheet_integration.py::LinkLifecycle::test_an_amount_only_correction_changes_the_deduction
```

| Case | Point | Pytest | Wall | User | System | CPU |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Story | P0 | 133.99s | 134.93s | 137.72s | 2.62s | 140.34s |
| Story | After | 45.86s | 46.40s | 50.48s | 2.39s | 52.87s |
| Control | P0 | 51.58s | 52.29s | 56.50s | 2.14s | 58.64s |
| Control | After | 20.86s | 21.54s | 26.12s | 1.38s | 27.50s |

Story CPU decreased 62.3%, passing the 50% target (at most 70.17s). Control
CPU improved and stayed below its 64.50s no-regression ceiling. These two cases
do not establish a whole-suite speedup.

## Diagnostic profile and construction target

The single-process story diagnostic commands were:

```sh
/usr/bin/time -p .venv/bin/python -m cProfile -o temp/test-replay-performance/p0-story.prof -m pytest -n 0 tests/test_sli_deduction_end_to_end.py::TheDeductionFollowsWhatThePersonSays::test_the_story
/usr/bin/time -p .venv/bin/python -m cProfile -o temp/test-replay-performance/track1-story.prof -m pytest -n 0 tests/test_sli_deduction_end_to_end.py::TheDeductionFollowsWhatThePersonSays::test_the_story
```

Only the profile output filename differs in the post-change command, so the
baseline profile remains intact. The diagnostic story profile reported
99.78s pytest, 100.81s wall, 99.23s user, 0.80s system, and 100.03s CPU after
the change. At P0, `facts_of` ran 44,175 times (194.249s cumulative in the
instrumented process); after, it ran 8,857 times. This is 79.95% fewer, but
the fixed 80% target required at most 8,835: the result misses by 22
constructions. Keep the miss visible. The selected mechanism leaves that
shortfall; no further local optimization or wider reuse was evaluated to close
it.

The post-change count includes all `facts_of` calls in the process, not just
the holder: 5,462 holder-backed full constructions, 2,833 fresh currency edge
walks, 304 historical retraction reads, and other public/neighbor consumers.
The original story profile had 199 `findings.project` folds. Across the story,
the coordinator, test-side forward runner, and reference runner each ran 11
times both before and after; the optimization did not remove those
derivations. `append_batch` was 12 calls and 0.124s cumulative at P0, so this
case did not establish it as a dominant target. Profile cumulative times
overlap and are diagnostics, not additive ordinary CPU values.

## Verification and scope limits

Small synthetic tests compare optimized projection with an uncached
act-by-act fold and exercise same-ID readoption, entity changes, migration,
retraction, invalid findings, current/historical separation, refusal timing,
and project-call isolation. The execution-based four-enforcer test proves
the same four real functions execute through public assertion, optimized
projection, and retraction; existing runtime refusal tests remain unchanged.
No existing assertions, skips, or verification passes were removed. The
published schema does not admit `locked`; its narrow policy case therefore
compares the holder-backed internal assertion path with public uncached
`apply_act`, without broadening schema validation.

Full tax-story per-prefix current/historical entity and lattice sizes were not
measured. The small dimension check is not a substitute for that measurement.
Interrupted timing attempts before final candidate checks are incomplete and
not measurements. Full `verify` later succeeded in
[run 39551011772](https://github.com/mattidell/attestory/actions/runs/39551011772)
on the repaired implementation (3,150 passed, 20 skipped; test step
2,814.97s). The job ran
05:41:52–06:29:08 UTC; the test step ran 05:42:10–06:29:06 UTC (46m56s).
These are whole-suite observations, not a controlled speed comparison. The run
confirms the gate for that implementation, not the future curated publication
candidate; fresh CI and final review remain publication gates.
