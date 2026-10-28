# P0 measurement: current suite and CI cost

Audience: reviewer and owner. This unit measures. It selects no change.

Producer commit: the P0 candidate on `milestone/test-cost-remaining`. `origin/main` is `a0bc250a67449a347f609550906f229fdd872daa`. The branch is 0 behind and 2 ahead of that line. The two commits are the milestone plan and this charter. `packages/`, `tests/`, `pytest.ini`, `requirements.txt`, and `.github/` match `origin/main`.

Raw output was collected outside Git and is not a durable artifact. Nothing in this note is a measured saving. Profile times overlap and include profiler overhead. No whole-suite share is inferred from one case.

## What was measured

One local full suite, with process-tree CPU from `/usr/bin/time -l`. A separate probe of four child processes burning 0.75s each reported real 0.93s, user 3.19s, sys 0.07s, so waited children are included in user plus system.

The machine is an Apple M1 Max with 10 cores. Python 3.14.3, pytest 9.1.1, xdist 3.8.0, macOS 26.5.2. `PYTEST_ADDOPTS` was unset. `pytest.ini` supplies `-n auto --dist worksteal`, which started 10 of 10 workers.

```text
/usr/bin/time -l python3 -m pytest --junitxml=temp/test-cost-remaining/pytest.xml --durations=0
```

Started `2026-10-27T18:24:17Z`, ended `2026-10-27T18:36:14Z`. Exit 0. One-minute load was already 11.53, 17.13, 13.65 at the start and 106.87, 115.36, 84.07 at the end. The rusage block records 5,176,899 involuntary context switches. Wall time is a contended measurement. User plus system is still the suite process tree's accounted CPU.

| Quantity | Value |
| --- | ---: |
| Real time (`/usr/bin/time`) | 716.78s |
| Pytest-reported wall | 715.93s |
| User | 5428.95s |
| System | 317.41s |
| User plus system | 5746.36s |
| Collected tests | 3544 |
| Passed | 3524 |
| Failed | 0 |
| Skipped | 20 |
| Successful subtest reports | 6471 |

The terminal summary hides successful subtests at the default subtest verbosity. Pytest's junit counter records each passing call report. Its `tests` value is 10015, with 0 failures, 0 errors, and 20 skips, so 9995 passing reports. Subtracting the 3524 passing tests leaves 6471 successful subtest reports. That matches unittest calling `addSubTest` for each successful `subTest`, which pytest logs as an extra passing call. The same junit `tests` value, 10015, is on the `#216` main-merge artifact.

Twenty skips are surface tests whose Node toolchain or vendored tree is absent: 9 in `tests/test_entry_loop_t1.py`, 3 in `tests/test_surface_t1_build_and_open.py`, and 8 in `tests/test_surface_t1_resolver.py`. There were no failures and no errors.

Junit `time` on each testcase is setup plus call plus teardown (`junit_duration_report` default `total`). The 3544 rows sum to **6978.30s**. That sum is worker wall time. It is 21.4% above measured CPU (6978.30 / 5746.36) because a worker's clock runs while it is not on CPU. CPU divided by wall is 8.02 across 10 workers. Shares below use 6978.30s only as the sum that splits by test.

## Where the local worker time sits

269 modules, one per `tests/**/test_*.py` file with a row in the junit file. A module is counted live when its source contains one of the four tokens `tests/conftest.py` uses to add the live mark (`live_coordinate_run`, `live_workspace`, `LiveWorkspace`, `subprocess`) or an explicit live mark. The explicit spellings are `@pytest.mark.live` and `pytestmark = pytest.mark.live`, including a call that passes a reason. Conftest adds the mark for the four tokens. Pytest collects an explicit mark on its own, and the fast lane's `-m "not live"` excludes that module.

Two modules are explicit marks with none of the four tokens and none of the `@pytest.mark.live` spelling: `tests/test_mortgage_borrowing_review.py` (7 tests, 36.15s) and `tests/test_sli_track4_validation_repair.py` (6 tests, 3.20s). Counting those spellings puts both in the live row.

| Population | Worker seconds | Share | Tests |
| --- | ---: | ---: | ---: |
| Live modules | 6937.9 | 99.4% | 2071 |
| Other modules | 40.4 | 0.6% | 1473 |
| Student loan | 2377.6 | 34.1% | 583 |
| Mortgage | 2062.4 | 29.6% | 124 |
| Other families | 1944.0 | 27.9% | 2665 |
| Form 1098 | 300.0 | 4.3% | 74 |
| Form 1099-K | 294.3 | 4.2% | 98 |

The top 25 modules are 5337.2s, 76.5% of summed worker time.

| Rank | Module | Tests | Seconds | Share | Cumulative |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `tests/test_mortgage_borrowing_calculation.py` | 66 | 1923.6 | 27.6% | 27.6% |
| 2 | `tests/test_sli_correction_session.py` | 70 | 528.6 | 7.6% | 35.1% |
| 3 | `tests/test_sli_correction_resumption.py` | 17 | 394.3 | 5.7% | 40.8% |
| 4 | `tests/test_sli_track1_combined_standing.py` | 57 | 352.7 | 5.1% | 45.8% |
| 5 | `tests/test_other_dependents_credit_track1.py` | 44 | 308.0 | 4.4% | 50.3% |
| 6 | `tests/test_sli_track5_worksheet_integration.py` | 39 | 186.5 | 2.7% | 52.9% |
| 7 | `tests/test_sli_track7_interruption_safety.py` | 20 | 133.6 | 1.9% | 54.8% |
| 8 | `tests/test_f1099k_statement_review.py` | 25 | 130.6 | 1.9% | 56.7% |
| 9 | `tests/test_child_tax_credit_track1.py` | 32 | 120.4 | 1.7% | 58.4% |
| 10 | `tests/test_f1098_production_review_repair.py` | 7 | 108.8 | 1.6% | 60.0% |
| 11 | `tests/test_sli_line21_explanation_data.py` | 20 | 104.2 | 1.5% | 61.5% |
| 12 | `tests/test_eic_qualifying_children_track1.py` | 15 | 100.6 | 1.4% | 62.9% |
| 13 | `tests/test_earned_income_credit_track1.py` | 20 | 96.8 | 1.4% | 64.3% |
| 14 | `tests/test_multiple_statement_sale_acceptance.py` | 13 | 85.2 | 1.2% | 65.5% |
| 15 | `tests/test_ssa_no_activity_line6b_track1.py` | 28 | 81.9 | 1.2% | 66.7% |
| 16 | `tests/test_ssa1099_benefits_line6_track2.py` | 48 | 75.3 | 1.1% | 67.8% |
| 17 | `tests/test_f1099k_computation_rules.py` | 9 | 73.8 | 1.1% | 68.9% |
| 18 | `tests/test_mortgage_borrowing_recording.py` | 12 | 73.4 | 1.1% | 69.9% |
| 19 | `tests/test_refund_or_amount_owed_track2.py` | 12 | 71.5 | 1.0% | 70.9% |
| 20 | `tests/test_f1098_statement_review.py` | 12 | 70.8 | 1.0% | 71.9% |
| 21 | `tests/test_sli_track11_collection_declarations.py` | 3 | 65.2 | 0.9% | 72.9% |
| 22 | `tests/test_multiple_statement_candidate_repairs.py` | 10 | 65.0 | 0.9% | 73.8% |
| 23 | `tests/test_sli_enrollment_follows_schooling.py` | 6 | 63.5 | 0.9% | 74.7% |
| 24 | `tests/test_sli_track2_explanation.py` | 12 | 61.6 | 0.9% | 75.6% |
| 25 | `tests/test_schedule_d_form8949_covered_wash_sale_t1.py` | 47 | 61.5 | 0.9% | 76.5% |

The slowest cases are spread across the mortgage module. Its slowest case is 81.30s, 1.2% of the sum. The second case in the suite is the other-dependents omission test at 76.63s.

## CI runs

CI is GitHub-hosted `ubuntu-latest`. Every full log inspected says `created: 4/4 workers` and the setup-python cache key is Linux x64 Ubuntu 24.04, Python 3.13.16. The pip cache hit on every full run below. Install dependencies is 4–6s. Runner CPU is unmeasured: the pytest step is `pytest --junitxml=test-results/pytest.xml --durations=50`, and the logs contain no rusage. Summed junit time is worker wall time, not CPU.

Job queue, from job `created_at` to `started_at`, is 2–4s. Step times below are the Actions timestamp deltas, which are whole seconds. The pytest line from the log is the finer wall time.

| Run | Commit | Result | Verify queue | Verify wall | Pytest wall | Passed | Artifact sum |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PR #225 ready, run 40276035420 | `f8a74ace` | success | 3s | 2673s | 2642.39s | 3416 | 10476.1s |
| PR #225 draft, run 40275564178 | `f8a74ace` | verify failure | 2s | 4s | not run |  |  |
| PR #216 earlier, run 40447884142 | `577e439c` | success | 3s | 2433s | 2409.25s | 3524 | 9500.4s |
| PR #216 head, run 40483936036 | `ded369e7` | success | 4s | 3869s | 3843.75s | 3524 | 15196.0s |
| `#216` main merge, run 40515157618 | `a0bc250a` | success | 3s | 3327s | 3298.91s | 3524 | 13059.8s |

The draft failure is the "Draft PRs do not run the full gate" step. Checkout, install, and tests were skipped. A duplicate `#216` run at the same minute was cancelled by concurrency within about two seconds. `#225` main merge, run 40342691288, is the pre-mortgage suite: pytest 2018.24s, 3416 passed. It is context for the later suite, not the current baseline.

On the `#216` main merge, the verify job's non-pytest steps are about 24s: checkout 3s, setup-python 2s, install 5s, mypy 10s, and the remaining gates and the duration upload at 0–1s each. `quick` on that push finished in 69s, with the fast lane at 38s. Fast-lane wall on the other full runs was 20–36s. Those jobs run beside `verify`, so workflow wall is the verify job.

The three `#216` full runs execute the same 3544 tests on 4 workers. Pytest wall is 2409s, 3299s, and 3844s. Summed worker time scales with that wall (ratios 3.94, 3.96, and 3.95). The workers stayed busy while the runner's pace changed. Without CPU counters, host speed and steal time are both open. The local sum for the same tests is 6978.30s, and the main-merge sum is 13059.8s, ratio 1.87. Module ratios for the largest modules are mostly near 2, with correction session at 1.34 and the multiple-statement sale module at 2.70.

A minimal way to obtain runner CPU without changing which tests run or the pass/fail gate: prefix the existing pytest command with `/usr/bin/time -v` so GNU time records elapsed, user, and system for the waited process tree, and print `nproc` once. Publish those lines with the duration artifact. This unit does not change the workflow.

## Profiles

Seven tests were selected before any profile started. Each ran alone:

```text
/usr/bin/time -l python3 -m cProfile -o PROFILE -m pytest -n 0 -q NODE --tb=line
```

`-n 0` overrode xdist. No console contained a workers line. All seven exited 0. cProfile's default timer is real time inside the profiled process. `/usr/bin/time` user plus system is CPU of that process and the children it waited for. Junit seconds are the same test's time inside the full parallel run, on a warm worker. The profile pays collection and a cold process, and cProfile inflates call-heavy Python. Those three clocks are not interchangeable.

| Profile | Junit in the suite | Profile real | User + system | Pytest line |
| --- | ---: | ---: | ---: | --- |
| Mortgage late member | 81.30s | 124.54s | 123.89s | 1 passed in 123.60s |
| Other-dependents omitted | 76.63s | 162.98s | 162.32s | 1 passed, 35 subtests passed in 162.08s |
| Resumption reopened | 45.05s | 38.29s | 31.05s | 1 passed in 37.36s |
| Correction attribution | 26.64s | 47.56s | 47.06s | 1 passed in 46.71s |
| Enrollment interrupted relink | 17.18s | 49.01s | 48.51s | 1 passed, 10 subtests passed in 48.11s |
| Form 1099-K review | 10.19s | 42.76s | 42.38s | 1 passed in 41.86s |
| Form 1098 production | 52.54s | 108.13s | 107.49s | 1 passed, 12 subtests passed in 107.25s |

Profile load moved from 9.10, 58.25, 66.29 to 5.81, 14.73, 37.30. The mortgage, credit, correction, enrollment, 1099-K, and 1098 profiles are CPU-bound: user plus system is within a few seconds of real time. The resumption profile is not an engine fold.

### Resumption is the browser

Exclusive time is 22.25s in `select.poll`, 12.57s in lock acquire, and 2.35s in socket `recv_into`. `findings.project` does not appear. User plus system, 31.05s, is above the parent's poll wait, so the waited child holds CPU that this profile does not attribute. The module is 394.3s of worker time, 5.7% of the sum, and stays outside the engine paths below.

### Repeated folds, lattices, and package resolution

Cumulative times contain each other. `facts_of` contains current-lattice `for_state` and historical `_declared_edges`. Both contain `_project_fact_lattice`. `findings.project` contains those lattices. Package validation sits under `resolve_production_package` and mostly beside the fold. Adding a row to another row double-counts.

| Path | Mortgage | Other dependents | Correction | Enrollment | 1099-K review | 1098 production |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Profile real | 124.54 | 162.98 | 47.56 | 49.01 | 42.76 | 108.13 |
| `live_coordinate_run` calls / cumulative s | 2 / 35.21 | 35 / 155.46 | 2 / 22.96 | 2 / 22.95 | 2 / 4.10 | 12 / 43.41 |
| `validate_package` calls / cumulative s | 2 / 29.24 | 35 / 59.60 | 2 / 19.77 | 2 / 20.17 | 4 / 23.81 | 12 / 24.96 |
| `validate_package` exclusive s | 1.52 | 22.34 | 0.39 | 0.31 | 0.81 | 2.27 |
| `findings.project` calls / cumulative s | 270 / 77.50 | 35 / 17.16 | 158 / 13.76 | 147 / 15.51 | 84 / 8.77 | 540 / 57.03 |
| `append_batch` calls / cumulative s | 40 / 3.43 |  | 9 / 0.09 | 15 / 0.13 | 6 / 6.19 | 24 / 31.77 |
| Project calls from `append_batch` / their cumulative s | 38 / 2.91 |  |  |  | 74 / 6.05 | 444 / 31.26 |
| Findings `for_state` calls / cumulative s | 75520 / 34.68 | 11746 / 7.86 | 24936 / 11.51 | 27854 / 13.27 | 8806 / 3.79 | 51636 / 25.35 |
| `_declared_edges` calls / cumulative s | 38488 / 35.87 | 6083 / 8.05 | 500 / 0.80 | 405 / 0.87 | 4510 / 4.05 | 26356 / 26.70 |
| `_project_fact_lattice` exclusive s | 30.67 | 7.39 | 6.12 | 7.24 | 3.73 |  |
| `_validate_fact_type` cumulative s | 1.19 | 0.38 | 0.54 | 0.57 | 0.32 | 1.38 |

Empty cells were not present in that profile's recorded functions. The 1098 production row's lattice exclusive figure was not pulled separately; its `_declared_edges` cumulative time is 26.70s and its findings `for_state` cumulative time is 25.35s.

On the mortgage case, `findings.project` is 270 calls and 77.503 cumulative seconds. These twelve immediate callers are the whole partition. Rounded caller seconds sum to 77.52; the unrounded caller times sum to 77.503.

| Caller | Calls | Cumulative seconds | Tree |
| --- | ---: | ---: | --- |
| `prepare_f1098_statement_review` | 54 | 16.97 | `packages/tax` |
| `_commit` | 27 | 8.56 | `packages/tax` |
| `_ensure_bundle` | 27 | 8.54 | `packages/tax` |
| `answer_f1098_statement_answer_durably` | 27 | 8.47 | `packages/tax` |
| `_validate_answers` | 27 | 8.45 | `packages/tax` |
| `current_mortgage_payment_comparison_support` | 22 | 7.45 | `packages/tax` |
| `prepare_mortgage_borrowing_review` | 22 | 7.45 | `packages/tax` |
| `_save_claim` | 11 | 3.77 | `packages/tax` |
| `_adopt` | 11 | 3.75 | `packages/tax` |
| `append_batch` | 38 | 2.91 | `packages/kernel` |
| `live_coordinate_run` | 2 | 0.64 | `packages/derivation` |
| `introduce_mortgage_borrowing_reference_durably` | 2 | 0.56 | `packages/tax` |

`answer_f1098_statement_answer_durably` projects the staged acts and then calls `_validate_answers`, which projects those same staged acts. Nothing is appended between the two calls. Both are 27 calls on this profile. The second call is 8.447s. The same shape appears inside `prepare_mortgage_borrowing_review`: it projects the log acts and then calls `current_mortgage_payment_comparison_support` on those acts, with no write between them. Both are 22 calls here, and the second call is 7.450s. Both pairs are in `packages/tax`.

`_ensure_bundle` and `_adopt` project before they may append a bundle act. `_commit` calls `append_batch` and then projects the log read back after the save. `_save_claim` does the same read-back. `prepare_f1098_statement_review` projects once per call. `introduce_mortgage_borrowing_reference_durably` was entered once and projects twice, once before `append` and once on the read-back.

`append_batch`'s own cumulative time is 40 calls and 3.428s. `_run_connected_case` accounts for 2 of those calls and 3.015s. `_commit` accounts for 27 calls and 0.271s. `_save_claim` accounts for 11 calls and 0.142s. The 38 `project` calls charged to `append_batch` are 2.911s. The recorder entries total 0.413s, so at most 0.413s of that project time can sit there. At least 2.498s sits in `_run_connected_case`'s two direct batches. Inside `append_batch`, `project` runs for an act when a new-write invariant may apply or the act kind is a lifecycle kind. Two `live_coordinate_run` calls account for 35.21s, including one cold package resolution near 29s. `_project_fact_lattice` exclusive time on this profile is 30.67s, inside the projections.

On the other-dependents case, 35 subtests call `live_coordinate_run` 35 times. `validate_package` exclusive time is 22.34s across those 35 calls, so the cost is not a single cold start sitting only in one callee. Marshal `_iter_ref_names` exclusive time is 32.10s. `project` is 17.16s. The profile is 2.1 times the test's suite junit time, so the absolute profile seconds are inflated. The call counts are not.

On the two short student-loan saves, package resolution is about 20 cumulative seconds for 2 calls, and `project` is 13.76s and 15.51s. The named helpers are inside that smaller `project` total:

| Helper | Correction calls / cumulative s | Enrollment calls / cumulative s |
| --- | ---: | ---: |
| `_stage_enrollment_follows_schooling` | 9 / 1.30 | 15 / 2.30 |
| `_scan_displayed_answers` | 1 / 0.13 | absent |
| `_attribute_borrowing_labels` | 2 / 0.40 | absent |

`_stage_enrollment_follows_schooling` is called from `_commit_save`. `_scan_displayed_answers` is called from `_working_state`. `_attribute_borrowing_labels` is called from `_line21_view`. On the correction profile, `append` — the single-act write, not `append_batch` — is the largest `project` caller, at 74 calls and 2.80s. `append_batch` itself is 0.09s and 0.13s on these two saves.

On the Form 1099-K review, 74 of 84 `project` calls come from `append_batch` (6.05s of 8.77s). On the Form 1098 production case, 444 of 540 `project` calls come from `append_batch` (31.26s of 57.03s). That is the save-path fold on those two long form routes. It is not the mortgage case's main cost, and it is not the short student-loan saves' main cost.

Fact-type `_validate_fact_type` stays under 1.4 cumulative seconds in every profile here. The older suite-wide range for that check is not a result of this measurement.

## Alternatives

No slice is selected.

1. **A second projection of the same acts inside one tax operation.** Evidence is the caller partition above, from the one mortgage profile. Its case is the module's slowest, 81.30 junit seconds of the module's 1923.6s across 66 tests. The other 65 tests were not profiled. The 1923.6s figure ranks the module. The measured size of a repeated projection is the second call on this profile: 8.447s in `_validate_answers`, and 7.450s in `current_mortgage_payment_comparison_support`. Each pair sits in `packages/tax`. A change limited to the second call in each pair would stay in that tree. `append_batch`'s 2.911s of `project`, and the lattice's 30.67s exclusive time, stay in alternatives 3 and 5. Sharing one projection across separate calls stays alternative 6, and its key still has to include the exact act contents and registry state. Admission, refusal timing, and displaced-fact checks belong to those alternatives. No slice is selected.

2. **Many full live runs inside one credit test.** Evidence: the second-slowest case, 76.63 junit seconds, performs 35 `live_coordinate_run` calls and 35 `validate_package` calls. Exclusive profiled time is 22.34s in `validate_package` and 32.10s in marshal `_iter_ref_names`, against 17.16s in `project`. The profile wall is 162.98s, so overhead is large and the cold-versus-repeat split inside those 35 calls was not measured call by call. Benefit is unclear until a warm process separates the first resolution from the other 34. Cost could be a test change, which can drop a case the suite now executes. Risk is weaker defect detection. Verification is the same cases before and after, plus the fast lane and the full suite if the engine changed.

3. **Incremental save folding.** Evidence for a benefit is the two long form profiles: `append_batch` accounts for 444 of 540 project calls on Form 1098 production and 74 of 84 on Form 1099-K review. Evidence against a suite-wide claim is the mortgage profile, where `append_batch`'s own cumulative time is 3.428s: 3.015s in the test helper's two direct batches and 0.413s in the recorder's `_commit` and `_save_claim` calls. Of the 2.911s of `project` charged to `append_batch`, at most 0.413s can sit in the recorder calls. The short student-loan saves are about 0.1s. Exact refusal comparison, before any implementation: drive current `append_batch` and the candidate with the same synthetic batches and compare exception type, the index of the first refused act, and byte-identical log contents. The batches are a valid batch, a stale `expected_revision`, a duplicate `act_id`, a `committed_against` mismatch, a new-write or lifecycle refusal on a later act, an incomplete tail, and a log whose size changes after the pending file is written. Today the checks run before the rename, a refusal writes nothing, and a size change unlinks the pending file and leaves the log as the other writer left it. The candidate has to refuse at that same act and leave the same bytes. Success has to return the same revision.

4. **The three named helpers.** They still call `project`, from `_commit_save`, `_working_state`, and `_line21_view`. On the short histories profiled, their cumulative time is 0.13s to 2.30s inside profiles of 47–49s. That does not support a suite share. A later ranking can ignore them only after a profile of a case that actually spends its time there.

5. **Current-lattice rebuilds.** Findings `for_state` is 34.68 cumulative seconds on the mortgage profile and 25.35s on the Form 1098 profile, inside `project`, with `_project_fact_lattice` the expensive exclusive work on the mortgage case. The earlier 11–20% suite figure is not re-measured. An incremental lattice would need its own design and a check that displaced facts used by historical reads still resolve.

6. **A cross-call prefix memo.** Projection dominates the mortgage profile (77.50s of 124.54s, 270 calls) and the Form 1098 profile (57.03s of 108.13s, 540 calls). It does not dominate resumption, and on the credit test package resolution and marshal walks are larger. On the short student-loan profiles, one cold package resolution is about 20s beside 14–16s of `project`. A memo is a candidate only for repeated projections after that first resolution, and its key has to include the exact act contents and registry state. The profiles do not show that a memo would shrink the credit test or the browser module.

7. **CI sharding and job layout, as a wait reduction.** Evidence: queue is 2–4s, setup and non-pytest gates are about half a minute, and the pytest step is the verify job. Four workers stay busy. The same suite's pytest wall already moves between 2409s and 3844s. The longest main-merge case is 145.76s, while the mortgage module is 3971.1 of 13059.8 summed worker seconds. A second runner can shorten the wait and spends more runner time. It does not reduce CPU. Duplicate cold starts per worker would be paid again in each shard.

8. **Dependency caching.** The inspected runs already restore the pip cache. Install is a few seconds. Caching is not the remaining wait. A cache that skips tests would change detection and is outside this measurement.

## Limits

One local suite, on a machine that was already past its core count. One profile per named case. cProfile real time is not CPU and is not the test's time on a warm worker. The mortgage `findings.project` callers are the full immediate-caller partition. Other caller lists in this note are the callers that were recorded for that row. Historical and current lattice times overlap. Caller cumulative times contain each other. Runner CPU is unmeasured. No optimization is chosen.
