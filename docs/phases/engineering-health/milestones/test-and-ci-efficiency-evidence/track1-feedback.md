# Track 1 feedback

This unit shortens waiting. It does not reduce engine CPU. `verify` still runs the full suite plus the cheap checks.

## Fast lane

P0 listed 16 budget failures. Marking those left other tests in the same modules over the 3-second budget: the first test of that work on a worker pays the package validation, golden regeneration, or both-runners cost, and a later run assigned that cost to a sibling. Each test below is marked `@pytest.mark.live` with a one-line comment, or covered by a module `pytestmark` that says the same thing. No assertion was removed, no test was skipped, and `FAST_LANE_BUDGET_SECONDS` is still 3.0.

| P0 duration | Test | Why it is an integration test |
| ---: | --- | --- |
| 38.2s | `tests/test_sli_track13_explicit_relationship_recording.py::ExplicitRelationshipRecording::test_two_statement_claim_lifecycles_keep_exact_consumer_support` | Two-statement claim lifecycle through real consumers and both derivation runners. |
| 24.0s | `tests/test_declarative_validation_2025_migration.py::PackagePublication::test_historical_v31_and_v26_byte_identity` | Validates the whole historical v31 package against the content corpus. |
| 19.6s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_mixed_scope_beside_an_unrelated_statement` | Eight recorded cases, each recovered and run through both derivation runners. |
| 11.2s | `tests/test_f1098e_student_loan_interest_track8_presentation.py::ProductionShapedGoldens::test_every_model_binds_all_four_form_field_symbols_exactly_once` | Regenerates the Form 1098-E presentation goldens. |
| 10.2s | `tests/test_f1099k_content_successors_increment_a.py::F1099KContentSuccessorsIncrementATests::test_f1099k_family_version_for_workspace_and_recording` | Adopts a published package and records a durable Form 1099-K statement. |
| 9.4s | `tests/test_sli_track13_explicit_relationship_recording.py::ExplicitRelationshipRecording::test_active_claim_and_evidence_addresses_cannot_be_reused` | Projects a full equal-pair case and refuses reused claim and evidence addresses. |
| 9.0s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_a_stale_schooling_blocks_the_statement_and_leaves_the_sibling` | Recovers a recorded workspace and runs both derivation runners. |
| 8.5s | `tests/test_sli_track13_explicit_relationship_recording.py::ExplicitRelationshipRecording::test_explicit_claims_are_admitted_and_reopened_through_real_consumers` | Admits claims and checks them through real consumers and both runners. |
| 8.4s | `tests/test_later_year_basis_reuse_track0.py::C8bCandidateAgainstCurrentPackageValidation::test_current_production_package_validation_accepts_the_invented_source_set` | Validates the current production package, then the same package with a candidate member. |
| 8.4s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_a_stale_statement_publishes_nothing_for_it_and_leaves_the_sibling` | Recovers a recorded workspace and runs both derivation runners. |
| 8.4s | `tests/test_sli_track4_support_chain.py::StatementSupport::test_every_current_statement_gets_a_result` | Recovers a recorded workspace and runs both derivation runners. |
| 8.2s | `tests/test_declarative_validation_2025_migration.py::PackagePublication::test_consumer_class_accounting_and_compiled_edge_mutants` | Compiles the whole v32 package validation graph and checks its mutants. |
| 7.3s | `tests/derivation/test_schema_version_dispatch_boundaries.py::CorePackageSupportedSchemas::test_selected_core_package_has_no_unsupported_members` | Validates the selected core package against the full content corpus. |
| 6.3s | `tests/test_f1098_circumstances_vocabulary.py::CircumstanceVocabulary::test_every_bundle_type_and_selected_value_is_durably_admitted` | Durably admits every Form 1098 circumstance type and value, then projects the log. |
| 5.9s | `tests/test_f1098e_student_loan_interest_track8_presentation.py::ProductionShapedGoldens::test_regeneration_is_deterministic_and_matches_committed_goldens` | Regenerates the Form 1098-E presentation goldens and compares them to the committed files. |
| 3.5s | `tests/test_sli_track15_versioned_source_consumer.py::VersionedSourceConsumer::test_actlog_recovery_both_runners_and_independent_claim_lifecycles` | Records two claim lifecycles, recovers the act log, and runs both derivation runners. |

The same runs also exceeded the budget, and were marked for the same reasons:

| Duration | Test | Why it is an integration test |
| ---: | --- | --- |
| 10.1s | `BelowFloorFullDeduction::test_full_capped_deduction_flows_through_to_agi` | Regenerates the Form 1098-E presentation goldens and checks the below-floor path. |
| 9.8s | `UniversalComponentViolationBlocks::test_related_person_interest_blocks_line21_and_downstream` | Regenerates the Form 1098-E presentation goldens and checks the blocked path. |
| 9.8s | `F1099KContentSuccessorsIncrementATests::test_package_v49_validation_and_release` | Validates the whole v49 package against the content corpus. |
| 9.4s | `ExplicitRelationshipRecording::test_nonaffirmative_and_wrong_scope_refuse_without_source_assertion` | Projects a full reference case and refuses recording without a source assertion. |
| 9.2s | `ExplicitRelationshipRecording::test_membership_needs_no_schooling_and_wrong_kind_borrowing_is_atomic_refusal` | Projects a full reference case and refuses an atomic recording. |
| 8.9s | `StatementSupport::test_the_person_cannot_tell_which_loan_the_statement_covers` | Recovers a recorded workspace and runs both derivation runners. |
| 8.8s | `ApplicabilityMarker::test_sole_omitted_link` | Covered by the support-chain class mark below. |
| 8.5s | `StatementSupport::test_missing_answers_reach_the_statement_as_missing` | Recovers a recorded workspace and runs both derivation runners. |
| 8.5s | `Publication::test_existing_package_results_are_unchanged` | Validates v38 and v39 and runs both packages over one saved workspace. |
| 8.5s | `ApplicabilityMarker::test_owners_mixed_case` | Covered by the support-chain class mark below. |
| 8.4s | `StatementSupport::test_two_loans_and_two_schoolings` | Recovers a recorded workspace and runs both derivation runners. |
| 8.2s | `StatementSupport::test_without_relationship_bundle_v2_a_claimed_statement_is_not_supported` | Covered by the support-chain class mark below. |
| 8.1s | `StatementSupport::test_plain_case_is_supported_with_its_basis_and_pins` | Recovers a recorded workspace and runs both derivation runners. |
| 8.1s | `F1099KContentSuccessorsIncrementATests::test_record_no_statements_family_version_threading` | Adopts a published package and records a durable Form 1099-K statement. |
| 8.0s | `V35EntrypointPins::test_v35_rejects_a_dangling_entrypoint` | Covered by the validation-repair module mark below. |
| 7.9s | `V39NomineeCrossChecks::test_v39_rejects_split_attachment_and_line2b_pins` | Covered by the validation-repair module mark below. |
| 7.8s | `V39NomineeCrossChecks::test_published_v39_validates` | Covered by the validation-repair module mark below. |
| 7.5s | `V39NomineeCrossChecks::test_a_later_version_is_checked_without_another_edit` | Covered by the validation-repair module mark below. |
| 7.4s | `PackagePublication::test_v32_validates_and_compiled_graph` | Validates the whole v32 package and checks its compiled member-validation graph. |
| 3.3s | `F1099KContentSuccessorsIncrementATests::test_f1099k_v48_workspace_preserves_v1` | Adopts a published package and records a durable Form 1099-K statement. |
| 1.99s | `ClosedEmptyComputedZero::test_closed_empty_family_is_closure_backed_zero` | Same golden regeneration as the tests above it; marked with them so the cold regeneration is not left in the lane. |

In `tests/test_sli_track4_support_chain.py`, the classes `InclusionSupport`, `StatementSupport` and `ApplicabilityMarker` are marked live: every case in them recovers a saved workspace and runs both derivation runners through `_run`. The `Publication` class's structural member and checksum test (0.02s) stays in the fast lane; its package-and-runner test keeps its own method mark. (Track 1 review corrected an earlier module-wide mark.) `tests/test_sli_track4_validation_repair.py` is marked at module scope: each case validates the published core-calculations package, or that package with one mutant. The other Form 1099-K tests that adopt a published package are marked even when this machine's warm run stayed under 3 seconds, because the cold adoption in the same class took about 8 seconds:

- `test_adoption_by_other_actor_preserves_v1`
- `test_adoption_by_other_scope_preserves_v1`
- `test_superseded_adoption_selects_active`
- `test_unresolvable_adoption_raises_error`

`python3 -m pytest -m "not live" -q` exited 0. Pytest reported `1551 passed, 8 skipped, 3251 subtests passed in 17.55s`.

The preceding `python3 -m pytest -m "not live" -q --durations=15` on the same tree also exited 0 (`1551 passed, 8 skipped, 3251 subtests passed in 17.20s`). These call durations are at least 1.5 seconds, within 2x of the 3-second budget. The CI runner is slower, so a later `quick` run may have to mark them the same way:

| Duration | Test |
| ---: | --- |
| 2.32s | `tests/derivation/test_presence_selection_subject_reads.py::WorksheetValidates::test_a_declared_read_needs_a_publisher_with_that_subject` |
| 1.99s | `tests/test_capital_gain_distributions_line7a_t3_presentation.py::ProductionShapedGoldens::test_regeneration_is_deterministic_and_matches_committed_goldens` |
| 1.91s | `tests/derivation/test_presence_selection_subject_reads.py::WorksheetValidates::test_path_ids_are_unique_and_neither_is_reserved` |
| 1.76s | `tests/derivation/test_presence_selection_subject_reads.py::WorksheetValidates::test_requires_are_the_refs_and_undeclared_collects` |
| 1.75s | `tests/derivation/test_presence_selection_subject_reads.py::WorksheetValidates::test_path_pins_are_one_per_requires_in_order` |

## Worksteal

Both commands ran once on the same tree (including Track 2): first with `-n auto`, then with `--dist worksteal`, before that flag was added to `pytest.ini`. `pytest-randomly` is not installed, so neither command passed `-p no:randomly`. Current `addopts` were `-n auto` (xdist's default distribution). The second command added `--dist worksteal`.

| Setting | Wall | User | System | User+system | Pytest |
| --- | ---: | ---: | ---: | ---: | --- |
| `-n auto` | 510.54s | 3373.86s | 227.61s | 3601.47s | 3157 passed, 20 skipped, 5249 subtests passed in 509.75s |
| `--dist worksteal` | 426.43s | 3265.12s | 222.61s | 3487.73s | 3157 passed, 20 skipped, 5249 subtests passed in 425.62s |

Wall fell by 84.11s (16.5%). User+system fell by 113.74s (3.2%). Both runs exited 0 with the same counts. That wall drop is large enough to adopt. `pytest.ini` now has `addopts = -n auto --dist worksteal`. This is waiting: idle workers at the end of the long tests, not less engine CPU. One pair of runs is the whole comparison.

## Quick job

`.github/workflows/ci.yml` runs `python -m pytest -m "not live"` in the `quick` job, after mypy, governance lint, and the envelope scan. `verify` is unchanged: it still runs those cheap checks and then the full suite. The Foreman pushes and reads the `quick` run. A test that exceeds the budget on that runner gets the same live mark.

## Browser waits

P0 profiled `tests/test_sli_correction_resumption.py::SavedAccountResumption::test_reopened_page_shows_the_correction_and_drops_an_old_token` at 60.0s wall. Exclusive time was 35.81s in `select.poll`, 13.33s in lock acquire, and 9.80s in socket `recv_into`. `time.sleep` cumulative time was 58.99s. The profile contains no engine calls. The child process is outside it.

The test starts the correction runner in one child, then `tests/helpers/correction_browser_client.mjs` in another. The parent waits in `Popen.communicate(timeout=...)`. On this Python, `subprocess.Popen._wait` with a timeout does not block in `waitpid`. It polls and calls `time.sleep`, doubling the delay up to 0.05s (`subprocess.py` around the POSIX `_wait`). The 59s of sleep is that poll for the same minute the browser child is running. A blocking `waitpid` would show the same wall time under a different function.

The client already waits on readiness:

- `tools/presentation_harness/lib/chrome.mjs` returns when Chrome writes `DevToolsActivePort`. The 25ms pause is only the gap between reads.
- `waitUntil` in the browser client evaluates the page and returns when the condition is true. It does not sleep out its 600s budget. The 25ms pause is the same kind of gap.
- Navigation waits on Chrome's `Page.loadEventFired` event.
- `Browser.close` and process exit use 10s and 30s only as ceilings. The wait ends when Chrome exits.
- `packages/derivation/live_viewing.py` `_wait_for_devtools` polls the same port file every 0.01s. This test launches Chrome through the Node harness, not through `LiveViewingVehicle`.
- `_Child._line` returns when the runner prints its ready line. The 1s queue timeout only bounds how long to wait before noticing a dead child.

No assertion and no page change would make that minute shorter. Nothing in the test, the helper, or the Chrome launch was edited. There is no before/after module time.

## Limits

The marks change which lane runs the test. They do not change what the test asserts, and the full suite still runs every one of them. Fast-lane durations are one parallel run's call time on this machine. A warm worker and a cold worker do not agree, which is why siblings of the P0 list were marked after they failed a later run. Worksteal is one pair of full-suite runs, not a repeated trial. The browser finding is from the P0 profile plus the current wait sites; this unit did not re-profile that test. None of this reduces engine CPU. `verify` is unchanged.

## CI runner check

The first `quick` run on the CI runner ([run 39689667980](https://github.com/mattidell/attestory/actions/runs/39689667980))
failed one fast-lane test at 3.1s against the 3.0s budget:
`tests/test_capital_gain_distributions_line7a_t3_presentation.py::ProductionShapedGoldens::test_regeneration_is_deterministic_and_matches_committed_goldens`
(1.99s locally; the runner was about 1.56 times slower). It regenerates
committed goldens, so it is marked live for the same reason as the Form 1098-E
golden tests. `tests/derivation/test_presence_selection_subject_reads.py::WorksheetValidates`
(1.7–2.3s locally per case) is marked live as a class: each case validates a
whole v35 package. No assertion or budget changed. Local fast lane afterwards:
1541 passed, 8 skipped, 3251 subtests, 10.66s.

## Gate repair after review

Track 1 review found that a skipped `verify` satisfied branch protection: a
skipped job is a success, so draft PR #214 was reported `CLEAN` with the full
suite never run on its head. `verify` no longer has a job-level condition. On a
draft PR its first step fails with a message, before any setup or suite step;
on a push or a ready PR that step is skipped and the full quartet runs. A draft
therefore shows a failed `verify`, and marking it ready runs `verify` in full on
that head.

## Publication check

The final publication review found two more fast-lane failures on the CI runner
at the curated head: `DerivedPinRecords::test_a_run_with_a_derived_entry_pin_closes_on_v10`
(4.3s) and `TrackOneA4Cases::test_both_present_blocks_on_the_named_token_and_pins_activity`
(4.2s), both about 1.2s locally. The difference is a cold first-use cost on each
CI worker that lands on whichever derivation-running test comes first. The
classes whose cases do that integration work are now marked live with reasons:
`DerivedPinRecords` (records a derivation through `run_and_record`),
`TrackOneA4Cases`, `SelectedPathEntries`, `LazyRead`, `ActivityOnlySource` and
`SelectionNeverFallsThrough` (each marshals the worksheet and runs both
derivation runners), and `LinkOutcomes` (records answers through the real
recorder and save). Counting every test the marks remove, the fast lane went
from 1,609 tests at `main` to 1,516, including four new reuse tests; the 97
removed tests still run in every full `verify`. Local fast lane afterwards:
1508 passed, 8 skipped, 3227 subtests, 9.51s.
