# P0 suite ranking

Audience: Foreman, Track 1, Track 2.

This unit ranks suite CPU. It changes no production code and no tests, and it chooses no fix.

## Commits and commands

The full suite was already recorded and was not rerun.

| Record | Commit | Result |
| --- | --- | --- |
| Suite durations, console, `/usr/bin/time` | the milestone plan commit | 3153 passed, 20 skipped, 5249 subtests, pytest 628.00s |
| Profiles and the fast lane | the first Track 1 workflow commit | descendant of the suite commit; `packages/` and `tests/` are identical between the two |

`/usr/bin/time` on the suite: real 628.92, user 5102.38, sys 226.60. User plus system is 5328.98s. The junit `testsuite` wall attribute is 627.972s.

Each profile was one single-process run, after the reason for that test had been written to `temp/test-and-ci-efficiency/sample-selection.txt`:

```sh
python3 -m cProfile -o temp/test-and-ci-efficiency/<name>.prof -m pytest -n 0 -q "<node id>"
```

No profile exceeded 10 minutes. The fast lane was one run after the profiles:

```sh
python3 -m pytest -m "not live" -q
```

Raw profiles, pytest logs, and the fast-lane log stay under `temp/test-and-ci-efficiency/`.

## How the sums should be read

Junit gives one duration per testcase. That duration is worker wall time, including any subtests inside the testcase. The 3173 testcases sum to **6113.67s**. With xdist that sum approximates CPU, because workers run at once. It is 14.7% above measured user+system (6113.67 / 5328.98). Worker wall includes time a worker was not on CPU. Shares below use 6113.67s as the denominator because that is the sum that splits by test. The wall clock of the suite was 628.92s, about 8.5 times less than user+system, which matches a run spread across the machine's workers (`pytest.ini` uses `-n auto`).

The junit `tests` attribute is 8422, which is 3173 testcases plus the 5249 subtests reported on the console. Subtests are not separate timed rows. A module's seconds already include its subtests.

The `live` mark is the one pytest applies. `tests/conftest.py` marks a module when its source contains `live_coordinate_run`, `live_workspace`, `LiveWorkspace`, or `subprocess`. Two modules carry an explicit `@pytest.mark.live` and do not contain those tokens, so the fast lane excludes them too: `tests/test_f1098_statement_recording.py` (49.48s) and `tests/test_f1099k_statement_recording.py` (1.64s). Each file has a single test class and the mark is on that class.

Family is by path: `test_sli*` and paths containing `student_loan` are student loan, including the Form 1098-E student-loan files (74.76s). Other `1098` paths are Form 1098. Paths containing `1099k`, `1099_k`, or `1099-k` are Form 1099-K.

## Module ranking

241 modules, 3173 testcases.

| Population | Worker seconds | Share | Tests | Modules |
| --- | ---: | ---: | ---: | ---: |
| Live | 5849.89 | 95.69% | 1564 | 102 |
| Fast lane | 263.78 | 4.31% | 1609 | 139 |
| Student loan | 3610.32 | 59.05% | 583 | 41 |
| Form 1099-K | 638.31 | 10.44% | 98 | 8 |
| Form 1098 | 637.20 | 10.42% | 104 | 11 |
| Other | 1227.84 | 20.08% | 2388 | 181 |

The top 25 modules are 5030.34s, 82.3% of the summed worker time.

| Rank | Module | Family | Tests | Seconds | Share | Cumulative | Live |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `tests/test_sli_correction_session.py` | student loan | 70 | 697.69 | 11.41% | 11.41% | yes |
| 2 | `tests/test_sli_correction_resumption.py` | student loan | 17 | 568.38 | 9.30% | 20.71% | yes |
| 3 | `tests/test_sli_track1_combined_standing.py` | student loan | 57 | 552.27 | 9.03% | 29.74% | yes |
| 4 | `tests/test_sli_track5_worksheet_integration.py` | student loan | 39 | 356.27 | 5.83% | 35.57% | yes |
| 5 | `tests/test_f1099k_statement_review.py` | Form 1099-K | 25 | 341.35 | 5.58% | 41.15% | yes |
| 6 | `tests/test_f1098_production_review_repair.py` | Form 1098 | 7 | 258.52 | 4.23% | 45.38% | yes |
| 7 | `tests/test_multiple_statement_sale_acceptance.py` | other | 13 | 226.55 | 3.71% | 49.09% | yes |
| 8 | `tests/test_sli_track7_interruption_safety.py` | student loan | 20 | 201.39 | 3.29% | 52.38% | yes |
| 9 | `tests/test_multiple_statement_candidate_repairs.py` | other | 10 | 194.12 | 3.18% | 55.56% | yes |
| 10 | `tests/test_sli_line21_explanation_data.py` | student loan | 20 | 188.11 | 3.08% | 58.63% | yes |
| 11 | `tests/test_f1098_statement_review.py` | Form 1098 | 10 | 172.93 | 2.83% | 61.46% | yes |
| 12 | `tests/test_sli_track2_explanation.py` | student loan | 12 | 171.94 | 2.81% | 64.27% | yes |
| 13 | `tests/test_ssa_no_activity_line6b_track1.py` | other | 28 | 127.35 | 2.08% | 66.36% | yes |
| 14 | `tests/test_f1099k_computation_rules.py` | Form 1099-K | 9 | 121.61 | 1.99% | 68.35% | yes |
| 15 | `tests/test_sli_enrollment_follows_schooling.py` | student loan | 6 | 108.69 | 1.78% | 70.12% | yes |
| 16 | `tests/test_ssa1099_benefits_line6_track2.py` | other | 48 | 101.16 | 1.65% | 71.78% | yes |
| 17 | `tests/test_sli_track11_collection_declarations.py` | student loan | 3 | 90.33 | 1.48% | 73.26% | yes |
| 18 | `tests/test_sli_track10_saved_account_evidence.py` | student loan | 7 | 80.19 | 1.31% | 74.57% | yes |
| 19 | `tests/test_f1099k_saved_presentation_increment_d.py` | Form 1099-K | 5 | 76.08 | 1.24% | 75.81% | yes |
| 20 | `tests/test_sli_track2_repair.py` | student loan | 5 | 74.86 | 1.22% | 77.04% | yes |
| 21 | `tests/test_f1098_circumstances_calculation.py` | Form 1098 | 13 | 71.71 | 1.17% | 78.21% | yes |
| 22 | `tests/test_sli_line21_explanation_page.py` | student loan | 7 | 69.69 | 1.14% | 79.35% | yes |
| 23 | `tests/test_sli_track13_explicit_relationship_recording.py` | student loan | 5 | 63.92 | 1.05% | 80.40% | no |
| 24 | `tests/test_sli_bounded_method_transfer_p1.py` | student loan | 36 | 63.10 | 1.03% | 81.43% | yes |
| 25 | `tests/test_sli_track12_account_reference_boundary.py` | student loan | 4 | 52.11 | 0.85% | 82.28% | yes |

Subtests do not explain the top of this table. The console total is 5249, and 85 modules that contain a `self.subTest(` site account for 2997.04s (49.0%). Site count is not a runtime count. Several of the largest modules contain no `self.subTest(` at all (`test_sli_track1_combined_standing.py` at 552.27s, `test_f1099k_statement_review.py` at 341.35s). Among the top 25, the modules that do contain sites are correction session (8), correction resumption (1), track 5 worksheet (4), Form 1098 production review (6), track 7 interruption (2), Form 1098 statement review (1), SSA line 6b (2), enrollment (2), SSA line 6 (4), and bounded method transfer (2). Their junit time is still the whole testcase.

## Sample

Eight tests, the planned cap. Reasons were fixed before any profile started.

1. `tests/test_sli_correction_session.py::Correction4AttributionByIdentity::test_d1_each_answer_carries_its_own_borrowing_before_and_after_correcting_autumn` (junit 37.18s). Slowest test in the highest-share module.
2. `tests/test_sli_correction_resumption.py::SavedAccountResumption::test_reopened_page_shows_the_correction_and_drops_an_old_token` (junit 72.89s). Slowest test in the second module, and the slowest student-loan test.
3. `tests/test_sli_track1_combined_standing.py::CoverDetail::test_case_K7_phaseout` (junit 17.83s). Slowest test in the third module. That module's 552.27s is spread across 57 tests; this case is the peak, at 17.83s.
4. `tests/test_sli_track5_worksheet_integration.py::WorksheetSelection::test_a_missing_retained_answer_cannot_be_bypassed_on_the_new_path` (junit 28.41s). Slowest test in the fourth module.
5. `tests/test_f1099k_statement_review.py::F1099KStatementReviewLiveDerivationTests::test_owner_regression_platform_pass_through_additional_shipping` (junit 26.45s). Slowest test in the highest-share Form 1099-K module (rank 5). The class is the live statement-review route.
6. `tests/test_f1098_production_review_repair.py::F1098ProductionReviewRepairTests::test_named_outside_cases_and_three_justified_zeros_keep_their_dispositions` (junit 126.81s). Slowest test in the highest-share Form 1098 module (rank 6), the production review and repair route, and the slowest test in the suite.
7. `tests/test_f1098_statement_review.py::F1098SavedRunAssociationTests::test_actual_v44_live_run_is_associated_only_at_its_recorded_revision` (junit 51.66s). Slowest test in the next Form 1098 module (rank 11), so Form 1098 is not only the production-repair route. This case is the saved-run association route.
8. `tests/test_f1099k_computation_rules.py::Form1099KComputationRulesTests::test_not_computed_paths` (junit 21.76s). Slowest test in the next Form 1099-K module (rank 14), so Form 1099-K is not only statement review. This case is the computation-rules route.

Profile files: `sli-correction-session-d1`, `sli-correction-resumption-reopened`, `sli-track1-k7-phaseout`, `sli-track5-missing-retained`, `f1099k-review-owner-regression`, `f1098-production-named-outside`, `f1098-review-v44-association`, `f1099k-computation-not-computed`. All eight exited 0. Wall times were 67.6s, 60.0s, 53.5s, 76.7s, 66.5s, 215.5s, 104.6s, and 62.1s.

## Attribution

Cumulative times overlap. A figure in this section is profiled time inside one fresh process, which is slower than the junit worker time wherever the path makes many Python calls. Flat costs look large in a short profile because the process pays them once. Call counts are the evidence for what repeats.

The resumption profile contains no calls to the engine functions below. Its exclusive time is 35.81s in `select.poll`, 13.33s in lock acquire, and 9.80s in socket `recv_into`, and `time.sleep`'s cumulative time is 58.99s. The test drives a browser subprocess. The child process is outside this profile, so this row does not attribute engine paths. The module is 9.30% of summed worker time and stays unattributed.

| Path | Session | Track 1 K7 | Track 5 | 1099-K review | 1098 production | 1098 review | 1099-K rules |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Profiled total | 64.65 | 51.48 | 73.17 | 62.85 | 197.32 | 96.39 | 58.50 |
| Junit worker | 37.18 | 17.83 | 28.41 | 26.45 | 126.81 | 51.66 | 21.76 |
| `live_coordinate_run` calls / cumulative s | 2 / 24.12 | 1 / 21.56 | 4 / 27.96 | 2 / 5.04 | 12 / 52.23 | 7 / 37.86 | 2 / 5.11 |
| `resolve_production_package` calls / s | 2 / 20.23 | 1 / 19.55 | 4 / 21.70 | 4 / 24.65 | 12 / 27.62 | 7 / 23.79 | 3 / 22.89 |
| `validate_package` calls / s | 2 / 19.69 | 1 / 19.28 | 4 / 20.61 | 4 / 23.82 | 12 / 24.62 | 7 / 22.26 | 3 / 22.22 |
| Schema misses (`sorted` of `iter_errors` from `SchemaRegistry.validate`) calls / s | 1612 / 19.53 | 1572 / 19.35 | 1409 / 19.96 | 1735 / 22.64 | 1591 / 21.32 | 1576 / 20.65 | 1495 / 21.38 |
| Key `json.dumps` from `SchemaRegistry.validate` calls / s | 258001 / 2.42 | 151145 / 1.44 | 200651 / 1.94 | 36620 / 0.41 | 169210 / 1.86 | 70905 / 0.76 | 34228 / 0.37 |
| `findings.project` calls / s | 187 / 33.54 | 124 / 22.81 | 196 / 40.05 | 94 / 32.30 | 540 / 162.63 | 97 / 65.63 | 63 / 29.64 |
| Historical lattice `_declared_edges` calls / s | 508 / 2.77 | 182 / 1.03 | 577 / 2.95 | 5634 / 18.91 | 26356 / 98.37 | 9638 / 46.35 | 4887 / 18.43 |
| `compute_currency` calls / s | 508 / 2.83 | 182 / 1.06 | 577 / 3.01 | 5634 / 19.36 | 26356 / 100.74 | 9638 / 47.44 | 4887 / 18.87 |
| Current lattice `facts_of` from `for_state` calls / s | 4388 / 14.32 | 3137 / 10.42 | 5369 / 18.19 | 1550 / 4.90 | 8424 / 24.55 | 2417 / 8.32 | 1287 / 4.42 |
| Fact-type `check_schema` from `_validate_fact_type` s | 14.5 | 10.2 | 17.1 | 7.5 | 34.5 | 8.7 | 5.8 |
| Marshal + `execute_and_record_marshaled` s | 1.61 | 0.88 | 2.39 | 1.70 | 9.91 | 5.49 | 1.62 |

### Package resolution and validation

Every `validate_package` call in these profiles is from `resolve_production_package`. Resolution's own remainder, after `validate_package`, is about 0.5s to 3s. `validate_package`'s cumulative time is almost all `loader.validate_declared`. On the one-call Track 1 profile, that is 423 calls and 18.92s of the 19.28s. Those loader calls are the cold `SchemaRegistry.validate` misses: miss counts stay between 1409 and 1735 and miss time stays between 19.35s and 22.64s while `validate` calls range from 34,228 to 258,001 and `validate_package` calls range from 1 to 12.

The calls after the first are cheap. One validation in the Track 1 profile is 19.28s. Twelve validations in the Form 1098 production profile are 24.62s. The tests differ, so this is a cross-profile comparison: the eleven extra calls add about 5 profiled seconds, about half a second each. Cache hits on `SchemaRegistry.validate` are 95.3% to 99.4% of calls. Hit bookkeeping (`OrderedDict.move_to_end`) is under 0.05s.

`SchemaRegistry.validate_declared` is the main caller of `SchemaRegistry.validate` (20.03s of 22.31s in the session profile, and a similar fraction in the others). Of `validate`'s cumulative time, key construction is the `json.dumps` column (0.37s to 2.42s) and validation is the miss column (about 19s to 23s). The key is built on every call, including hits. The misses are the expense. `iter_errors` is invoked through `sorted`, so its caller in the profile is `sorted`, not `validate`.

Registry load (`SchemaRegistry._load` / `_load_directory`, including `check_schema` of published schemas) is an additional flat cost, 4.79s to 5.25s in every profile, including the profile that constructs the registry 48 times. The compiled-schema memo absorbs the repeats.

These flat costs are paid once per process. In the suite they fall on each xdist worker, not on each test. The suite's user+system was about 8.5 times its wall clock, so about ten workers. About ten cold starts, at the profiled cost, are a few percent of user+system. cProfile inflates the jsonschema portion, so the real per-worker cost is smaller.

### Currency and the historical lattice

`compute_currency` calls and `_declared_edges` calls match in every in-process profile, and `facts_of` calls from `_declared_edges` match those too. Each currency computation builds the historical lattice once, through `facts_of(state.fact_state, include_displaced=True)`. The rest of `compute_currency`, after `_declared_edges`, is 0.02s to 2.37s. The currency path's time is the historical build.

`facts_of` has no memo. The current-lattice holder in `findings.py` reuses `facts_of(fact_state)` when the fact-state object is the same object. The historical call does not.

The profile records call counts, not argument identities. Fact states are created by `facts.initial_state` and `facts.apply_act` (`KernelState` is constructed only in `initial_state`; later states come from `replace`). Historical builds compared with states created:

| Sample | Historical builds | Fact states created | Builds per state |
| --- | ---: | ---: | ---: |
| Session | 508 | 8248 | 0.06 |
| Track 1 K7 | 182 | 5754 | 0.03 |
| Track 5 | 577 | 9642 | 0.06 |
| 1099-K review | 5634 | 3296 | 1.71 |
| 1098 production | 26356 | 17616 | 1.50 |
| 1098 review | 9638 | 4015 | 2.40 |
| 1099-K rules | 4887 | 2400 | 2.04 |

On the Form 1098 and Form 1099-K samples, builds exceed states created, so some fact-state object is passed to more than one historical build. That matches the source: `fact_state` stays the same object across finding acts that do not apply a fact act, and `_compute_view` calls `compute_currency` on the admission state. On the student-loan samples, builds are fewer than states created, so the counts do not require a repeated object. The dominant currency caller in every in-process profile is `_compute_view`.

The current-lattice column is the other `facts_of` path, the holder's `for_state` rebuilds when the fact-state object changes. It is 10s to 18s on the student-loan samples and 4s to 25s on the form samples.

### `findings.project` by caller

Cumulative project time includes the lattice builds and the fact-type checks. It mostly does not include package validation: package validation sits under `live_coordinate_run` → `resolve_production_package`, and only the coordinator's own project calls sit in both. Those coordinator project calls are 3.8% to 10.6% of project cumulative time.

| Caller class | Session | Track 1 K7 | Track 5 | 1099-K review | 1098 production | 1098 review | 1099-K rules |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Product recording/review | 53.0% | 68.3% | 76.0% | 39.3% | 47.3% | 76.9% | 63.6% |
| Act-log append | 19.4% | 14.5% | 7.7% | 55.8% | 45.4% | 9.5% | 30.7% |
| Test helper | 15.4% | 13.4% | 8.6% | 0 | 0 | 2.9% | 0 |
| Coordinator | 5.4% | 3.8% | 7.7% | 4.9% | 7.3% | 10.6% | 5.7% |
| Other product | 6.8% | 0 | 0 | 0 | 0 | 0 | 0 |

Product recording and review is `packages/tax/` (statement recording, statement review, relationship recording). Act-log append is `append` / `append_batch` projecting the log. Test helpers are under `tests/`. The coordinator column is `live_coordinate_run`.

Fact-type `check_schema` from `_validate_fact_type` runs inside `apply_bundle_adoption` during the fold. It scales with the test (5.8s to 34.5s) and is separate from the cold package-validation misses.

### Coordinator derivation, and time outside product calls

`marshal_live_run_context` plus `execute_and_record_marshaled` (which calls `runner._execute`) is 0.88s to 9.91s, 1.7% to 5.7% of profiled time. Test-side `runner.run` is 0 calls in five profiles and one to four calls in the other two, at 0.09s and 0.18s.

Exclusive time inside `tests/` is about 0.1% of the in-process profiles. Fixture construction in the test modules is not where those profiles spend time. The resumption module is the outside-product block in this sample: its slowest test waits on a browser.

### What repeats on every sampled in-process route

All seven in-process tests call `live_coordinate_run`, `validate_package`, `SchemaRegistry.validate`, `findings.project`, and `compute_currency`. Cold package validation and registry load are flat per process. Historical-lattice builds, current-lattice rebuilds, and fact-type `check_schema` scale with the test and are much larger on the form routes (historical) or on the student-loan routes (current lattice and fact-type checks) as the table shows. The resumption test shows that a live-marked module can spend its worker time outside the process entirely.

## Suite estimate

Apply each in-process path's share of profiled time to the worker seconds of its family. The low end uses the sampled modules only, at the lower share seen in that family. The high end uses the whole family at the higher share. Student-loan shares exclude the unattributed resumption module (568.38s) from the base. The other family (1227.84s, 20.1%) was not sampled; its low is zero and its high applies the highest share seen in any sample. Cumulative paths that contain these rows are not given a separate suite share.

| Path | Named-family range | With the unsampled other family | Where it runs |
| --- | ---: | ---: | --- |
| Fact-type `check_schema` during bundle adoption | 11–15% | 11–19% | Every in-process sample, inside the fold. Scales with bundle adoption. |
| Current-lattice rebuilds (`for_state`) | 11–15% | 11–20% | Every in-process sample. Larger on the student-loan profiles (20–25% of profiled time) than on the form profiles (8–12%). |
| Historical lattice (`_declared_edges` → `facts_of(..., include_displaced=True)`) | 7–11% | 7–21% | Every in-process sample. About 2–4% of the student-loan profiles and 30–50% of the form profiles. |
| Cold package validation plus registry load | 1–4% of suite CPU | same | Once per worker, not once per test. The same ~19–23 profiled seconds of misses appears in every profile. |
| Schema memo key (`json.dumps` inside `SchemaRegistry.validate`) | 1–3% | 1–4% | Every `validate` call, including cache hits. Smaller than the miss time in every profile. |
| Coordinator marshal and execute | 1–3% | 1–4% | Every `live_coordinate_run` in the in-process sample. |
| Repeated `validate_package` after the first call in the process | under the cold cost | same | Visible as ~0.5 profiled seconds per extra call in the 1-call versus 12-call comparison. |

The two lattice rows and the fact-type checks are additive with each other. They sit inside `findings.project` and must not be added to project time. Cold package validation sits beside the fold, under resolution, except for the coordinator's own project call.

## Track 2 ranking

Ranked by the estimated suite share above. The range on the unsampled other family can swap the first three. None of these is a chosen design.

1. **Fact-type schema checks during bundle adoption.** Largest share if student-loan profiles represent that family: on the order of 11–19% of summed worker time. A reuse would have to key on the fact-type document bytes and the validator version. A different document, or a different validator, has to be checked again.
2. **Current-lattice rebuilds when the fact-state object changes.** About 11–20%. The holder already returns the previous lattice when the fact-state object is the same object. The remaining time is rebuilds after the object changes. A further reuse would have to key on the exact fact state, and a different state would need a new lattice.
3. **Historical-lattice rebuilds inside currency.** About 7–21%, and the top of that range is the unsampled other family behaving like Form 1098. On the form samples the same fact-state object is rebuilt (builds per created state are 1.50 to 2.40). A reuse would have to key on that exact fact-state object. A different state would need a new historical lattice. Nothing in the profile supports reusing a lattice across states.
4. **Cold validation of an already verified package, once per process.** About 1–4% of suite CPU after it is amortized across a worker. A reuse would have to key on the verified bytes, the schema-registry digest, and the validator version. Repeats inside one process are already cheap because the schema memo hits.
5. **Schema-memo key construction.** About 1–4%. The key is built on every `SchemaRegistry.validate` call and costs 0.37s to 2.42s in these profiles, against about 20s of cold misses. The key is the smaller part of this path.
6. **Coordinator marshalling and execution.** About 1–4%. A reuse would have to key on the marshalled inputs the run actually consumes: rules, parameters, projected state, and currency. This share is smaller than the fold paths that feed it.
7. **Repeated package validation after the first call in the process.** The strongest case in the sample, twelve calls against one, adds about five profiled seconds. Same key as the cold validation. Smaller than the lattice paths inside that same long test.

## Fast lane

`python3 -m pytest -m "not live" -q` exited 1. Pytest reported 16 failed, 1585 passed, 8 skipped, 3272 subtests passed in 69.95s. All 16 failures are budget failures (`FAST_LANE_BUDGET_SECONDS` is 3.0). Durations are the one-decimal figures in the failure text.

| Duration | Test |
| ---: | --- |
| 38.2s | `tests/test_sli_track13_explicit_relationship_recording.py::ExplicitRelationshipRecording::test_two_statement_claim_lifecycles_keep_exact_consumer_support` |
| 24.0s | `tests/test_declarative_validation_2025_migration.py::PackagePublication::test_historical_v31_and_v26_byte_identity` |
| 19.6s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_mixed_scope_beside_an_unrelated_statement` |
| 11.2s | `tests/test_f1098e_student_loan_interest_track8_presentation.py::ProductionShapedGoldens::test_every_model_binds_all_four_form_field_symbols_exactly_once` |
| 10.2s | `tests/test_f1099k_content_successors_increment_a.py::F1099KContentSuccessorsIncrementATests::test_f1099k_family_version_for_workspace_and_recording` |
| 9.4s | `tests/test_sli_track13_explicit_relationship_recording.py::ExplicitRelationshipRecording::test_active_claim_and_evidence_addresses_cannot_be_reused` |
| 9.0s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_a_stale_schooling_blocks_the_statement_and_leaves_the_sibling` |
| 8.5s | `tests/test_sli_track13_explicit_relationship_recording.py::ExplicitRelationshipRecording::test_explicit_claims_are_admitted_and_reopened_through_real_consumers` |
| 8.4s | `tests/test_later_year_basis_reuse_track0.py::C8bCandidateAgainstCurrentPackageValidation::test_current_production_package_validation_accepts_the_invented_source_set` |
| 8.4s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_a_stale_statement_publishes_nothing_for_it_and_leaves_the_sibling` |
| 8.4s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_every_current_statement_gets_a_result` |
| 8.2s | `tests/test_declarative_validation_2025_migration.py::PackagePublication::test_consumer_class_accounting_and_compiled_edge_mutants` |
| 7.3s | `tests/derivation/test_schema_version_dispatch_boundaries.py::CorePackageSupportedSchemas::test_selected_core_package_has_no_unsupported_members` |
| 6.3s | `tests/test_f1098_circumstances_vocabulary.py::CircumstanceVocabulary::test_every_bundle_type_and_selected_value_is_durably_admitted` |
| 5.9s | `tests/test_f1098e_student_loan_interest_track8_presentation.py::ProductionShapedGoldens::test_regeneration_is_deterministic_and_matches_committed_goldens` |
| 3.5s | `tests/test_sli_track15_versioned_source_consumer.py::VersionedSourceConsumer::test_actlog_recovery_both_runners_and_independent_claim_lifecycles` |

No test was changed.

## Limits that weaken the ranking

- The resumption module is 9.30% of summed worker time, and its sampled test does not show engine time. The other sixteen tests in that module were not profiled.
- The other family is 20.1% of summed worker time and has no profile. It is large enough to reorder the first three Track 2 rows.
- One test stands for its module, and the module's slowest test stands for its family. Track 1's 552.27s is spread across 57 tests whose slowest case is 17.83s.
- Profiled seconds are not junit seconds. Call-heavy paths are inflated, so the suite percentages for those paths are high relative to real CPU. The order among call-heavy paths is the comparison the profiles support. The cold package cost and the browser wait are different kinds of time.
- Historical-lattice identity is inferred from call counts plus the source. The profile does not record object ids.
- The 1-call versus 12-call package-validation comparison uses two different tests.
- Junit subtests are not itemized, so subtest counts cannot be tied to individual seconds beyond the static `self.subTest(` sites.
