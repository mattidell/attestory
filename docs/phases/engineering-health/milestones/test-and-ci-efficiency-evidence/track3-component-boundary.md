# Track 3 component boundary

Audience: Foreman, reviewer.

This unit classifies. It moves no test.

## Scope

For the eight highest-share modules in the P0 ranking, excluding the browser-bound `tests/test_sli_correction_resumption.py`, every test case is classified as live-required, rule-outcome, or mixed. For each rule-outcome or mixed case, the below-coordinator assertion, the existing helper, the retained live witness, and the junit duration are named, and candidate moves are ranked by time saved. The classified set is the seven remaining modules: correction session, track 1 combined standing, track 5 worksheet, Form 1099-K statement review, Form 1098 production review, multiple-statement sale acceptance, and track 7 interruption.

Evidence: the recorded P0 junit durations and the test sources. Uncertain cases stay live and are not candidate moves. No test or production code was changed.

## What the classes mean

A case is **live-required** when the defect it catches is in recording, saving, admission, currency, recovery, the coordinator's wiring, or the saved explanation.

A case is **rule-outcome** when its assertions are only what the rules compute from inputs the fixture could supply directly. The rule symbols are named below.

A case is **mixed** when it asserts some of each. `run_live` and `run_v42` make a case mixed even when the test method's own asserts are rule results, because those helpers also require a non-refusal, a reloaded presentation file, forward/reference agreement, and coordinator publications equal to the forward runner.

Eight track 5 cases assert published package bytes, registry checksums, or declared rule text and do not run a derivation. They are **package-bytes**. They are not one of the three classes. They are not moves. They are counted so the module total is the whole file.

## Existing helper, and why most modules stay on the coordinator

The below-coordinator helper that already exists for this worksheet family is `run_package` in `tests/test_sli_track5_worksheet_integration.py`. It validates a package file, projects the acts, computes currency, marshals with `marshal_live_run_context` (including `_statement_inclusion_applicability` and `_resolve_run_authorization`), runs `run` and `run_reference`, and builds the presentation with `build_presentation_model`. The coordinator uses that same presentation function.

`run_package` does not resolve a release, open a workspace, write the record stream, or pass `companion_presence_pairs`. It also omits the authorization provenance and workspace revision that `live_coordinate_run` passes into `build_presentation_model`. `live_coordinate_run` additionally calls `validate_projected_source_boundary` before marshalling. Those gaps are why one live case stays on each path, and why Form 1098 and Form 1099-K cases are not candidates: those modules have no helper that marshals the way their coordinator does, and their saved-review assertions are the defect.

A candidate move keeps the recorder that builds the acts and replaces only the final `run_live` or `run_v42` with `run_package`. Track 1 v42 cases would pass `package.core-calculations.v42.json`. Track 1 v41 bases and track 5 cases would pass `package.core-calculations.v41.json`. Track 1 and track 5 share `SCOPE` and `USER`.

## How time saved was estimated

Junit durations are worker seconds from `temp/test-and-ci-efficiency/suite-durations.xml`, the P0 suite at the milestone plan commit. Module totals below match the ranking. Per-test figures are those junit rows. The denominator for shares is the ranking's summed worker time, 6113.67s.

The P0 profiles were fresh processes, so each one pays a cold `validate_package` of about 19s. In the suite that cold cost is per worker, not per test. Replacing a call does not recover it.

The Track 5 profile is `test_a_missing_retained_answer_cannot_be_bypassed_on_the_new_path` (junit 28.41s, four `live_coordinate_run` calls, 73.17s profiled). Coordinator cumulative 27.96s minus `validate_package` 20.61s leaves 7.35s. The coordinator's share of `findings.project` is 7.7% of 40.05s, about 3.08s, and `run_package` still projects once. The remainder is about 4.27 profiled seconds for four calls. Deflated by 73.17/28.41, that is about 0.42 junit seconds per call.

The Track 1 K7 profile is one call (junit 17.83s, 51.48s profiled). Non-validate coordinator remainder 2.28s. Marshal plus execute is 0.88s. Deflated by 51.48/17.83, marshal plus execute is about 0.30 junit seconds and the whole non-validate remainder is about 0.79. The high end overstates, because that remainder includes the project `run_package` still does.

**Per replaced call: 0.3s to 0.8s, point 0.5s.** Call counts below come from the source (subtests and repeated `_run` / `run_live`). A heavier derivation sits toward the high end. The junit duration of the case is mostly the recorder's per-act projection, which the move keeps.

## Counts

| Module | Cases | Live-required | Rule-outcome | Mixed | Package-bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| `test_sli_correction_session.py` | 70 | 66 | 0 | 4 | 0 |
| `test_sli_track1_combined_standing.py` | 57 | 0 | 0 | 57 | 0 |
| `test_sli_track5_worksheet_integration.py` | 39 | 0 | 0 | 31 | 8 |
| `test_f1099k_statement_review.py` | 25 | 7 | 2 | 16 | 0 |
| `test_f1098_production_review_repair.py` | 7 | 2 | 0 | 5 | 0 |
| `test_multiple_statement_sale_acceptance.py` | 13 | 1 | 1 | 11 | 0 |
| `test_sli_track7_interruption_safety.py` | 20 | 18 | 0 | 2 | 0 |
| Seven modules | 231 | 94 | 3 | 126 | 8 |

231 cases. 94 + 3 + 126 + 8 = 231.

## Candidate moves and the witnesses that stay

A candidate replaces one or more `run_live` / `run_v42` calls with `run_package` and keeps the same rule assertions. Three cases stay live as the witnesses. They are not candidates.

| Path | Retained case | Junit | Defect only that live case still catches |
| --- | --- | ---: | --- |
| Track 1 v42, `run_v42` | `CoverDetail.test_case_K1` | 9.23 | The v42 coordinator writes a presentation, its publications match the forward runner, and the saved model contains `line21Explanation`. |
| Track 1 v41 base, `run_live` | `V41Base.test_base_K1` | 10.47 | The adopted v41 release still blocks with `old-and-new-sli-inputs-both-present` and the saved sentence "cannot be used together". |
| Track 5 v41 surface, `run_live` | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` | 16.99 | The coordinator's saved file names only the retracted statement, Birch's standing stays `none`, and the rendered page shows that sentence when headless Chromium is present. The sentence assertions run before the browser check, so a missing browser skips only the visible-page half. |

One further track 1 case stays live because it is uncertain, not because it is the witness: `CoverDetail.test_case_late_unclosed` (7.30s). It admits Cedar on a successor horizon and does not reclose. The blocked code is `SOURCE_SET_UNCLOSED`. `live_coordinate_run` calls `validate_projected_source_boundary` and `run_package` does not. Which of those two produces the code was not separated. Uncertain stays live.

That leaves 54 track 1 calls and 47 track 5 calls, 101 calls.

## Top ten by estimated time saved

Equal call counts are ordered by junit, as a proxy for a heavier derivation. The point estimate is 0.5s per call. The range is 0.3–0.8s per call.

| Rank | Case | Calls | Junit | Saved, point (range) | Below-coordinator assertion | Witness |
| ---: | --- | ---: | ---: | --- | --- | --- |
| 1 | `WorksheetSelection.test_a_missing_retained_answer_cannot_be_bypassed_on_the_new_path` | 4 | 28.41 | 2.0s (1.2–3.2) | Four subtests. Standing `none`. Worksheet `DEPENDENCY_INVALID` missing the statement. The skipped `tax.us.2025.rule.sli-answer-status-*` blocks `DEPENDENCY_ABSENT`. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 2 | `WorksheetSelection.test_a_negative_retained_answer_cannot_be_bypassed_on_the_new_path` | 4 | 27.17 | 2.0s (1.2–3.2) | Four subtests. Standing `none`. Worksheet code `SLI_UNIVERSAL_COMPONENT_VIOLATION`. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 3 | `WorksheetSelection.test_a_second_statement_beside_a_supported_one_needs_its_own_retained_answers` | 3 | 16.08 | 1.5s (0.9–2.4) | Three runs. Standing `none` on both, then `DEPENDENCY_INVALID` missing Birch, then `SLI_UNIVERSAL_COMPONENT_VIOLATION`, then value 2300. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 4 | `LinkLifecycle.test_correcting_a_link_away_blocks_and_restoring_it_returns_the_deduction` | 3 | 12.47 | 1.5s (0.9–2.4) | Three runs. 2500, then blocked with standing `no-loan-link`, then 2500. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 5 | `LineReasons.test_a_retained_answer_missing_or_no_on_a_second_statement` | 2 | 18.23 | 1.0s (0.6–1.6) | Two runs. Birch's missing related-person answer, then the related-person `no` sentence. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 6 | `LinkLifecycle.test_plain_case_and_phase_out` | 2 | 17.44 | 1.0s (0.6–1.6) | Values 2500 and 1334, disposition `published_value`. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 7 | `LinkLifecycle.test_an_amount_only_correction_changes_the_deduction` | 2 | 15.68 | 1.0s (0.6–1.6) | Value 2500, then 1000 after `reviewed_amount_only`. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 8 | `WorksheetSelection.test_an_unrelated_supported_statement_never_rescues_a_blocked_one` | 2 | 14.24 | 1.0s (0.6–1.6) | Two runs. Blocked with standing `none` and `enrollment-answer-missing`, then value 2300. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 9 | `LinkLifecycle.test_withdrawing_a_link_blocks_and_restoring_it_returns_the_deduction` | 2 | 11.13 | 1.0s (0.6–1.6) | Standing `inclusion-withdrawn` and blocked, then 2500. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |
| 10 | `WorksheetSelection.test_old_only_complete_workspaces_keep_their_v38_results` | 2 | 10.48 | 1.0s (0.6–1.6) | Line 21 value 2500 and 1334, disposition `published_value`, v38 publications preserved, five derived pins on the line finding. Helper: `run_package` on v41. | `LineReasons.test_retracted_statement_names_only_it_and_keeps_the_other_statement_supported` |

Top ten calls: 26. Point estimate 13.0s, range 7.8–20.8s.

The witness's defect, for every row: the track 5 coordinator's saved presentation and, when Chromium is present, the rendered line. A moved case would no longer check that the coordinator's publications match the forward runner.

## The rest of the safe candidates

Each is one call unless noted, so about 0.5s (0.3–0.8). Same helper and the witness for its path.

### Track 5, remaining

| Case | Calls | Junit | Assertion a `run_package` version keeps |
| --- | ---: | ---: | --- |
| `LineReasons.test_a_stale_schooling_names_only_its_statement` | 1 | 16.61 | Sentence names only Cedar's schooling dependency. |
| `LinkLifecycle.test_the_owners_mixed_applicability_case_blocks` | 1 | 15.12 | Blocked. Standing `applicability-unestablished`. |
| `LineReasons.test_the_owners_mixed_applicability_case` | 1 | 15.05 | Sentence: the statement this link was confirmed against changed or was removed. |
| `WorksheetSelection.test_a_stale_schooling_refuses_naming_its_statement` | 1 | 13.97 | Worksheet `DEPENDENCY_INVALID` missing Cedar. Birch standing `none`. |
| `LineReasons.test_an_unrelated_supported_statement_is_not_named` | 1 | 11.59 | Sentence names only Birch's missing enrollment answer. |
| `LineReasons.test_a_sole_retracted_statement_still_has_a_reason_without_a_current_subject` | 1 | 11.21 | Blocked. Worksheet missing is the applicability marker. Sentence is the marker refusal's declared wording. Reason `factId` is the recorded inclusion. |
| `WorksheetSelection.test_new_path_plain_case_publishes_2500_from_the_standing_and_four_answers` | 1 | 10.67 | Value 2500. `tax.us.2025.sli.statement-line21-standing` is `none`. Derived pins are the standing and the four `tax.us.2025.sli.answer-status.*` findings. Replaced-answer status is absent. |
| `LineReasons.test_neither_and_a_link_corrected_away` | 2 | 8.71 | Two runs. Sentence: no student loan is linked to this statement. |
| `WorksheetSelection.test_a_denied_link_alone_is_the_new_path` | 1 | 8.59 | Same both-present token when a denied link keeps the new path present. |
| `LineReasons.test_old_path_missing_answers_name_the_statement_and_never_read_as_no` | 1 | 8.43 | Saved line 21 sentences name Birch's two missing answers and say a missing answer is not no. |
| `LineReasons.test_a_published_line_carries_no_reasons` | 1 | 7.95 | A published line 21 has no `reasons` key. |
| `LinkLifecycle.test_a_workspace_without_relationship_bundle_v2_blocks` | 1 | 7.52 | Blocked. Standing `loan-cost-answer-missing`. |
| `LineReasons.test_a_workspace_that_cannot_record_the_answers_is_told_so` | 1 | 7.19 | Sentence: the workspace cannot record the answers yet. |
| `WorksheetSelection.test_both_present_blocks_on_the_replaced_answer` | 1 | 6.81 | Worksheet `DEPENDENCY_INVALID` missing `old-and-new-sli-inputs-both-present`. |
| `LineReasons.test_both_present` | 1 | 6.79 | Sentence: the older answer and the loan links cannot be used together. |
| `WorksheetSelection.test_old_only_with_a_statement_missing_an_answer_now_blocks` | 1 | 4.23 | `tax.us.2025.rule.sli-worksheet` blocked `DEPENDENCY_INVALID` missing Birch; `tax.us.2025.rule.sli-answer-status-no-qtp-earnings-used` blocks `DEPENDENCY_ABSENT`. The v39 comparison already uses `run_package`. |
| `WorksheetSelection.test_old_only_with_a_no_keeps_the_violation` | 1 | 2.26 | Worksheet code `SLI_UNIVERSAL_COMPONENT_VIOLATION`. |
| `WorksheetSelection.test_the_four_retained_answers_do_not_select_the_old_path` | 1 | 2.02 | Blocked. Standing `no-loan-link`. |
| `WorksheetSelection.test_nonempty_with_neither_blocks` | 1 | 1.30 | Blocked `DEPENDENCY_INVALID`. Standing `no-loan-link`. |
| `WorksheetSelection.test_closed_empty_publishes_zero` | 1 | 1.18 | Value 0, disposition `closure_backed_zero`. |

### Track 1 v42, `CoverDetail`

Every candidate asserts, through `run_package` on v42: `tax.us.2025.rule.sli-worksheet` line 21 disposition, value, and active code; `tax.us.2025.sli.statement-combined-standing` per form. The forward runner's publications supply the standing classes. Neighbors, where marked, also assert `tax.us.2025.form1040.line-1a`, `tax.us.2025.form1040.line-10`, `tax.us.2025.schedule1.line26-total-adjustments`, and `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`. Locality, where marked, asserts `tax.us.2025.sli.sum.inclusion-loan-cost-no`, `tax.us.2025.sli.flag.inclusion-loan-cost-no`, and `tax.us.2025.sli.count.statement-inclusion-denied`.

Witness for all of these: `CoverDetail.test_case_K1`.

| Case | Junit | What is specific |
| --- | ---: | --- |
| `test_case_K7_phaseout` | 17.83 | value 1668 at wages 90000 |
| `test_case_K7_below` | 16.43 | value 2500 on 2000+1000 |
| `test_case_open_loan_no` | 16.23 | combined `open-inclusion-loan-cost-no` |
| `test_case_L7` | 16.04 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_U8e` | 15.92 | combined `financing-denied-unsettled` |
| `test_case_both_contrary` | 15.75 | combined `contrary-on-unsettled-inclusion` |
| `test_case_K12` | 15.50 | missing Cedar's autumn marker |
| `test_case_K8_after` | 14.61 | combined `enrollment-no` |
| `test_case_M5` | 13.40 | combined `contradicts-enrollment-no` |
| `test_case_K13` | 12.77 | combined `applicability-unestablished` on Birch; missing Birch's spring marker |
| `test_case_K0b` | 12.64 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_K3` | 12.05 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_two_form` | 10.58 | locality: Cedar's loan-cost no does not flag Birch |
| `test_case_U8a` | 10.56 | combined `mixed-unresolved-and-lacks` |
| `test_case_L10a` | 10.22 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_M3` | 9.98 | combined `contradicts-loan-cost-no` |
| `test_case_K8_before` | 9.55 | value 2300 |
| `test_case_denied_loan_no` | 9.31 | locality: denied count on Cedar only |
| `test_case_U4` | 9.25 | combined `inclusion-cannot-tell` |
| `test_case_U10b` | 9.18 | combined `enrollment-cannot-tell` |
| `test_case_K9_before` | 9.17 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_open_enroll_no` | 9.12 | combined `open-inclusion-enrollment-no` |
| `test_case_K9_after` | 8.89 | older standing `yes` on both forms |
| `test_case_M2` | 8.79 | combined `contradicts-enrollment-no` |
| `test_case_withdrawn_enroll_no` | 8.73 | combined `withdrawn-inclusion-enrollment-no` |
| `test_case_L8b` | 8.71 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_withdrawn_loan_no` | 8.71 | combined `withdrawn-inclusion-loan-cost-no` |
| `test_case_L8d` | 8.70 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_K10` | 8.70 | combined `contradicts-loan-cost-no` |
| `test_case_shared_borrowing` | 8.56 | locality: both inclusions flag loan-cost no |
| `test_case_K2` | 8.18 | neighbors; combined `older-no`; code `DEPENDENCY_INVALID` |
| `test_case_K0a` | 8.08 | neighbors (line 1a wages, line 10, line 26, worksheet line 1) |
| `test_case_U9b` | 8.08 | combined `loan-cost-cannot-tell` |
| `test_case_K6` | 7.90 | code `SLI_UNIVERSAL_COMPONENT_VIOLATION` |
| `test_case_L8c` | 7.44 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_L9a` | 7.04 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_mix_loan_missing_enroll_cannot_tell` | 6.96 | combined `mixed-unresolved-and-lacks` |
| `test_case_M1` | 6.95 | combined `contradicts-loan-cost-no` |
| `test_case_K11` | 6.32 | missing Cedar box 1 |
| `test_case_K5` | 5.89 | published 2500, or the blocked code in the spec; combined `none` unless noted |
| `test_case_U3` | 4.14 | combined `statement-loan-cannot-tell` |
| `test_case_empty` | 4.07 | neighbors; disposition `closure_backed_zero`, value 0 |
| `test_case_mfs` | 3.82 | neighbors; code `SLI_MFS_INELIGIBLE` |

Staying live, not in the candidate sum: `test_case_K1` (9.23s) and `test_case_late_unclosed` (7.30s).

### Track 1 v41 bases

Each candidate asserts, through `run_package` on v41: line 21 blocked, worksheet code `DEPENDENCY_INVALID`, missing token `old-and-new-sli-inputs-both-present`, and a reason whose text contains "cannot be used together". Witness: `V41Base.test_base_K1`.

| Case | Junit |
| --- | ---: |
| `test_base_L7` | 13.00 |
| `test_base_denied_loan_no` | 10.43 |
| `test_base_K9_after` | 9.99 |
| `test_base_L8c` | 9.35 |
| `test_base_L8b` | 8.73 |
| `test_base_L8d` | 8.58 |
| `test_base_K3` | 8.08 |
| `test_base_K9_before` | 7.69 |
| `test_base_L10a` | 7.10 |
| `test_base_L9a` | 6.72 |
| `test_base_K5` | 4.82 |

`test_base_K1` (10.47s) stays.

## Cases that are rule-outcome or mixed and are not candidates

### Correction session, four mixed cases

A below-coordinator check of the standing string would use `run_package` on the acts after confirm. It would not remove a coordinator call. `CorrectionRuntime.confirm` is the defect, and confirm is what runs the coordinator. The case stays whole.

| Case | Junit | Both kinds |
| --- | ---: | --- |
| `BlockedNoToYesCase.test_correcting_no_to_yes_unblocks_the_form` | 11.57 | Correcting no to yes unblocks the form. Also asserts explanation-row standing `none` on both lenders after the save. |
| `BlockedNoToYesTransport.test_confirm_route_unblocks` | 8.92 | The confirm route unblocks. Also asserts explanation-row standing `none`. |
| `FirstWorkingExample.test_choose_cedar_confirm_yes_to_no` | 14.16 | Session confirm saves one answer and recalculates. Also asserts explanation-row standing `loan-cost-no` on Cedar and `none` on Birch. |
| `SharedBorrowingCase.test_one_correction_reaches_both_forms` | 7.29 | One confirm reaches both forms. Also asserts explanation-row standing `loan-cost-no` on Cedar and Birch, and one shared finding id. |

### Form 1099-K rule-outcome, no safe helper

`run_package` does not install domain companion pairs or the source-boundary check these statement rules sit next to. No helper in `tests/test_f1099k_statement_review.py` or the sale module marshals the production surface. Uncertain, so they stay live. Not ranked.

| Case | Junit | Symbols |
| --- | ---: | --- |
| `test_case2_no_form_1099k_on_schedule1_return` | 8.28 | `tax.us.2025.schedule1.top-entry` is 0 after `record_f1099k_no_statements_durably`. No saved-review assertion. |
| `test_case9_statement_recorded_after_no_1099k` | 14.67 | `tax.us.2025.schedule1.top-entry` is 0, then absent, then 880, across three coordinator runs. No saved-review assertion. |
| `test_case_12_candidate_c_closed_empty_v2` | 7.55 | Top-entry value 0 and a zero disposition (`closure_backed_zero`, `published_zero`, `published_value`, or `computed_zero`) from the saved presentation. Symbol `tax.us.2025.schedule1.top-entry`. |

### Form mixed cases

Each asserts a rule publication and a saved review, saved explanation, family handover, or atomic save. The saved half is the defect the live path exists to catch. There is no existing helper that reproduces the coordinator's companion pairs, source boundary, and saved presentation review. They stay live.

Form 1099-K statement review, mixed:

| Case | Junit | Both kinds |
| --- | ---: | --- |
| `test_owner_regression_platform_pass_through_additional_shipping` | 26.45 | Saved explanation and `tax.us.2025.f1099k.statement-loss-reason` for platform pass-through with extra shipping. |
| `test_correction_platform_pass_through_additional_shipping` | 21.06 | Same saved explanation after a correction in that workspace. |
| `test_shipping_question_to_recorded_value_discriminating_example` | 17.26 | Question to recorded value to saved loss result for seller-received shipping. |
| `test_case6_answer_cannot_tell_for_an_amount` | 14.16 | Saved can't-tell stop. |
| `test_case3_correct_cost_across_loss_gain_boundary` | 14.03 | Saved unresolved explanation across the loss/gain correction, and the history of both answers. |
| `test_case7_corrected_statement_reconciliation_stop` | 13.91 | Saved reconciliation stop after a box 1a correction. |
| `test_case13_saved_run_recalculation_needed_on_correction` | 13.47 | Saved run becomes recalculation-needed after a correction. |
| `test_case5_withdraw_an_amount` | 13.23 | Saved stop for the withdrawn amount. |
| `test_case4_withdraw_personal_use_answer` | 13.06 | Saved state `personal-use-unconfirmed` after withdrawal. |
| `test_case8_second_statement_multiple_statement_stop` | 13.03 | Saved multiple-statement stop. |
| `test_shipping_pass_through_supported_loss` | 12.31 | Platform pass-through still saves a supported loss. |
| `test_classification_actually_unresolved` | 12.05 | Saved unresolved classification, reason sentence, and income sentence. |
| `test_classification_supported_zero_admitted_statement` | 12.04 | Saved classification of an admitted $0 statement as supported zero. |
| `test_classification_missing_output` | 11.26 | Saved missing-output classification when the saved run has neither top entry nor reason. Symbols `tax.us.2025.schedule1.top-entry` and `tax.us.2025.form.f1099k.unresolved`. |
| `test_case1_record_statement_and_all_answers_for_loss` | 10.89 | Saved review `current-supported-loss` and sentence, and `tax.us.2025.schedule1.top-entry` equals box 1a (880). |
| `test_classification_closed_empty_zero` | 8.13 | Saved classification of closed-empty zero. |

Form 1098 production review, mixed:

| Case | Junit | Both kinds |
| --- | ---: | --- |
| `test_named_outside_cases_and_three_justified_zeros_keep_their_dispositions` | 126.81 | Twelve scenarios. `tax.us.2025.f1098.residence-interest-reason` and `tax.us.2025.schedule-a.line8a` / `tax.us.2025.rule.f1098-line8a`, plus the saved mortgage-interest explanation text and `calculationAssociation`. |
| `test_v2_recorder_uncertainty_correction_and_saved_statement_reasons` | 54.05 | Rule dispositions (`published` / `blocked` / `DEPENDENCY_ABSENT`) and saved statement reasons, including `savedUnresolvedExplanation`. |
| `test_v2_labels_defaults_joint_return_debt_limit_and_append_only_registry` | 19.78 | Line 8a dispositions and saved state, and the append-only registry bytes. |
| `test_personal_v1_tokens_do_not_satisfy_v2_and_v44_remains_available` | 19.36 | v1 answers do not fill v2 inputs: line 8a stays blocked missing `filing-unit-owns-home` and `shared-main-home`. The v44 surface still saves reason `qualified`. |
| `test_v2_single_answer_adopts_selected_questions_and_conflicting_save_is_atomic` | 10.38 | A conflicting save is refused and the revision is unchanged. One accepted answer adopts bundle v2. Line 8a then blocks missing `shared-main-home`. |

Multiple-statement sale, mixed:

| Case | Junit | Both kinds |
| --- | ---: | --- |
| `test_case_06_atomic_statement_removal` | 25.42 | Atomic removal leaves one statement's saved 880 result after a fresh closure. |
| `test_case_04_answer_withdrawal_on_one_statement` | 22.13 | Withdrawal on statement 2 saves `personal-use-unconfirmed` and blocks the top entry. |
| `test_case_09_v1_single_statement_workspace_upgraded_on_second_statement` | 21.80 | Family handover when a second statement arrives. Saved box 1a and the top entry after closure. |
| `test_case_05_statement_correction_with_amount_mismatch` | 21.60 | Saved reconciliation discrepancy on the corrected statement. The other statement's saved result stays. |
| `test_case_03_mixed_outcome_one_supported_loss_one_unknown_cost_basis` | 21.10 | Top entry blocked. Statement 1's saved supported loss is kept. Statement 2's saved unresolved explanation. |
| `test_case_13_gain_or_excluded_statement_beside_supported_loss` | 19.85 | Top entry blocked beside an unsupported gain. Statement 1's saved supported loss is kept. |
| `test_case_01_two_supported_personal_losses_differing_amounts` | 19.80 | Saved reviews at 880 and 460, top entry 1340, pins from `tax.us.2025.schedule1.top-entry` to the closure, `tax.us.2025.f1099k.box1a-subtotal`, and both `tax.us.2025.f1099k.statement-loss-reason` findings. Currency of both statement findings. |
| `test_case_02_two_supported_personal_losses_identical_amounts` | 19.11 | Saved supported loss on two identical 500 amounts, top entry 1000, no collision. |
| `test_case_08_v1_closed_empty_workspace_upgraded_on_first_statement` | 15.45 | Family handover from a v1 closed-empty workspace. Top entry blocked until the v2 closure, then publishes. |
| `test_case_10_untouched_v1_workspace_under_successor_package` | 12.96 | An untouched v1 workspace keeps its historical saved presentation. A new run on the successor package is unclosed. |
| `test_case_07_single_statement_f1099k_invariant` | 11.84 | Single-statement saved supported loss. The multiple-statement work must not change this shape. |

### Track 7 mixed cases

| Case | Junit | Both kinds | Why it stays |
| --- | ---: | --- | --- |
| `test_a_v1_workspace_records_its_answers_and_deducts` | 7.08 | The first borrowing answer's save is `bundle-adoption`, `evidence-submitted`, `contribution`, `assertion`, and bundle v2 is adopted once. Then line 21 value 1500 through `run_live`. | It is the only production-path witness that this recording shape deducts 1500. The act-kind assertions are the recording defect and stay with it. |
| `test_a_workspace_with_no_relationship_claims_is_unchanged` | 2.16 | Old answers append one act at a time, never a batch, and no pending file. Line 21 is published 1500 through `run_live`. | It is the only witness that old answers still append one act at a time and still publish 1500. |

The sweep tests are live-required, not mixed. `_result` caches by the act-list hash, so an interrupted recovery that correctly keeps the old acts does not call `run_live` again. Each sweep pays two live runs (before, and the completed save). The defect is torn-save recovery. They stay.

## Live-required cases

### Correction session

| Case | Junit | Defect |
| --- | ---: | --- |
| `Correction4AttributionByIdentity.test_d1_each_answer_carries_its_own_borrowing_before_and_after_correcting_autumn` | 37.18 | Saved explanation: each said item, including a displaced predecessor, carries its own borrowing by finding id. Not a rule-value move. |
| `Track2Browser.test_retry_page_recovers_the_one_saved_correction` | 30.06 | Browser page for retry, historical, withdrawn, shared, duplicate-label, blocked, and D1 states. The resumption module is the other browser path and is out of this unit. |
| `BrowserIntegration.test_dropped_confirm_recovers_the_calculated_outcome` | 28.86 | The served page shows the calculated before-and-after explanation, refuses an indistinguishable choice with nothing saved, drops a stale financing change, and recovers a dropped confirm. |
| `RecoveryPage.test_refresh_after_a_calculated_outcome_shows_it_again` | 28.10 | The page recovers a dropped saved-not-calculated outcome, states that an unknown token is unknown, and shows a calculated outcome again on refresh. |
| `Track2Browser.test_historical_page_shows_the_superseded_answer` | 26.29 | Browser page for retry, historical, withdrawn, shared, duplicate-label, blocked, and D1 states. The resumption module is the other browser path and is out of this unit. |
| `BrowserIntegration.test_indistinguishable_choice_is_refused_with_nothing_saved` | 25.38 | The served page shows the calculated before-and-after explanation, refuses an indistinguishable choice with nothing saved, drops a stale financing change, and recovers a dropped confirm. |
| `RecoveryRuntime.test_calculated_outcome_is_recovered_by_its_own_token` | 23.41 | Token recovery: calculated, saved-not-calculated, pre-save, unconfirmed, unknown, cancelled, foreign, and a superseded retry. |
| `BrowserIntegration.test_choose_confirm_calculated_shows_before_and_after_explanation` | 23.29 | The served page shows the calculated before-and-after explanation, refuses an indistinguishable choice with nothing saved, drops a stale financing change, and recovers a dropped confirm. |
| `RecoveryTransport.test_outcome_routes` | 23.19 | Outcome and retry routes recover or refuse by token. |
| `Track2Browser.test_shared_page_lists_both_forms_and_both_rows_change` | 22.99 | Browser page for retry, historical, withdrawn, shared, duplicate-label, blocked, and D1 states. The resumption module is the other browser path and is out of this unit. |
| `Track2Browser.test_blocked_page_yes_unblocks_and_shows_history` | 22.18 | Browser page for retry, historical, withdrawn, shared, duplicate-label, blocked, and D1 states. The resumption module is the other browser path and is out of this unit. |
| `RecoveryPage.test_dropped_saved_not_calculated_can_be_calculated_again` | 21.61 | The page recovers a dropped saved-not-calculated outcome, states that an unknown token is unknown, and shows a calculated outcome again on refresh. |
| `NamedStatesTransport.test_each_committed_state_serves_its_opening` | 19.75 | Each committed state serves its opening over the session transport. |
| `BrowserIntegration.test_financing_change_after_confirmation_shown_is_not_saved` | 19.12 | The served page shows the calculated before-and-after explanation, refuses an indistinguishable choice with nothing saved, drops a stale financing change, and recovers a dropped confirm. |
| `Track2Browser.test_d1_page_shows_the_denied_borrowing_without_internal_codes` | 18.36 | Browser page for retry, historical, withdrawn, shared, duplicate-label, blocked, and D1 states. The resumption module is the other browser path and is out of this unit. |
| `Track2Browser.test_duplicate_label_page_shows_clues_before_choosing` | 16.34 | Browser page for retry, historical, withdrawn, shared, duplicate-label, blocked, and D1 states. The resumption module is the other browser path and is out of this unit. |
| `Track2Browser.test_withdrawn_page_shows_nothing_to_correct` | 16.05 | Browser page for retry, historical, withdrawn, shared, duplicate-label, blocked, and D1 states. The resumption module is the other browser path and is out of this unit. |
| `RecoveryPage.test_unknown_stored_token_states_the_outcome_is_unknown` | 15.51 | The page recovers a dropped saved-not-calculated outcome, states that an unknown token is unknown, and shows a calculated outcome again on refresh. |
| `HistoricalResult.test_open_on_earlier_result_after_a_later_correction` | 13.52 | Opening an earlier result after a later correction, and a withdrawn answer, are historical session results. The runtime is not historical by default. |
| `SharedBorrowingTransport.test_confirm_route_changes_both_rows` | 13.30 | The confirm route changes both forms' rows. The defect is the session transport. |
| `RecoveryRuntime.test_retry_is_token_bound_and_a_superseded_correction_is_refused` | 12.90 | Token recovery: calculated, saved-not-calculated, pre-save, unconfirmed, unknown, cancelled, foreign, and a superseded retry. |
| `DuplicateLabelsCase.test_distinguishable_pair_shows_different_clues_per_choice` | 11.31 | A distinguishable pair shows different clues. A truly identical pair is refused and writes nothing. |
| `RetryTransport.test_retry_route_recovers_saved_not_calculated` | 10.62 | The retry route recovers saved-not-calculated. |
| `RetryAfterSavedNotCalculated.test_retry_writes_no_act_and_recovers_the_saved_correction` | 9.23 | Retry writes no act and recovers the saved correction. Retry before any correction refuses. |
| `Repair1Distinguishability.test_choose_then_confirm_refuses_an_indistinguishable_pair` | 8.99 | An indistinguishable pair is refused at confirm and nothing is saved. |
| `Correction1LabelsAsDisplayed.test_whitespace_only_label_difference_refuses` | 8.98 | Distinguishability uses the label as displayed. Whitespace-only differences refuse; case differences stay distinguishable. |
| `Repair3HonestOutcomes.test_second_confirm_on_same_token_returns_recorded_outcome` | 8.65 | A calculation refusal, a coordinator exception, or a presentation read failure reports saved-not-calculated. A second confirm returns the recorded outcome. |
| `Correction1RedactedRefusal.test_indistinguishable_choice_is_redacted` | 8.19 | Indistinguishable, stale, and forced admission refusals are redacted. |
| `Correction1LabelsAsDisplayed.test_case_difference_alone_stays_distinguishable` | 8.06 | Distinguishability uses the label as displayed. Whitespace-only differences refuse; case differences stay distinguishable. |
| `HistoricalTransport.test_choose_and_confirm_target_the_current_answer` | 7.85 | Choose and confirm target the current answer. A withdrawn choose writes nothing. |
| `DuplicateLabelsCase.test_truly_identical_pair_is_refused_without_writing` | 7.76 | A distinguishable pair shows different clues. A truly identical pair is refused and writes nothing. |
| `RecoveryTransport.test_retry_route_refuses_a_superseded_correction` | 7.57 | Outcome and retry routes recover or refuse by token. |
| `Repair2RelationshipMeaning.test_financing_withdrawal_after_prepare_is_not_saved` | 7.28 | A financing withdrawal after prepare is not saved. |
| `RecoveryRuntime.test_pre_save_not_saved_is_recovered` | 7.23 | Token recovery: calculated, saved-not-calculated, pre-save, unconfirmed, unknown, cancelled, foreign, and a superseded retry. |
| `NamedStates.test_every_committed_state_seeds_and_runs` | 6.99 | Committed correction states seed, and the catalog names each state. Not a derivation. |
| `RecoveryRuntime.test_saved_not_calculated_outcome_is_recovered` | 6.55 | Token recovery: calculated, saved-not-calculated, pre-save, unconfirmed, unknown, cancelled, foreign, and a superseded retry. |
| `RecoveryRuntime.test_unknown_cancelled_and_foreign_tokens` | 6.52 | Token recovery: calculated, saved-not-calculated, pre-save, unconfirmed, unknown, cancelled, foreign, and a superseded retry. |
| `Correction2RelationshipAttribution.test_d1_financing_and_inclusion_items_carry_their_borrowing_label` | 6.32 | Financing and inclusion items carry their borrowing label by identity, including one borrowing shared by two forms. |
| `HistoricalTransport.test_withdrawn_choose_writes_nothing` | 5.92 | Choose and confirm target the current answer. A withdrawn choose writes nothing. |
| `Correction1RedactedRefusal.test_stale_confirmation_refusal_is_redacted` | 5.54 | Indistinguishable, stale, and forced admission refusals are redacted. |
| `Repair3HonestOutcomes.test_exception_in_live_coordinate_run_reports_saved_not_calculated` | 5.50 | A calculation refusal, a coordinator exception, or a presentation read failure reports saved-not-calculated. A second confirm returns the recorded outcome. |
| `Repair3HonestOutcomes.test_calculation_refusal_reports_saved_not_calculated` | 5.48 | A calculation refusal, a coordinator exception, or a presentation read failure reports saved-not-calculated. A second confirm returns the recorded outcome. |
| `RecoveryRuntime.test_unconfirmed_token_is_not_saved_and_later_confirm_is_refused` | 5.44 | Token recovery: calculated, saved-not-calculated, pre-save, unconfirmed, unknown, cancelled, foreign, and a superseded retry. |
| `DuplicateLabelsTransport.test_identical_pair_route_refuses_and_writes_nothing` | 5.42 | The identical-pair route refuses and writes nothing. |
| `Repair3HonestOutcomes.test_presentation_read_failure_reports_saved_not_calculated` | 5.14 | A calculation refusal, a coordinator exception, or a presentation read failure reports saved-not-calculated. A second confirm returns the recorded outcome. |
| `HistoricalResult.test_withdrawn_answer_shows_nothing_to_correct_and_writes_nothing` | 4.88 | Opening an earlier result after a later correction, and a withdrawn answer, are historical session results. The runtime is not historical by default. |
| `HistoricalResult.test_runtime_not_marked_historical_by_default` | 3.75 | Opening an earlier result after a later correction, and a withdrawn answer, are historical session results. The runtime is not historical by default. |
| `RetryAfterSavedNotCalculated.test_retry_before_any_correction_refuses` | 2.80 | Retry writes no act and recovers the saved correction. Retry before any correction refuses. |
| `Correction2FreshDisplay.test_every_outcome_shows_its_own_plain_word_phrase` | 2.64 | Each relationship outcome shows its own plain-word phrase on the fresh display. |
| `Correction2StaleConfirmation.test_outcome_change_after_prepare_refuses_without_writing` | 2.05 | An outcome change after prepare refuses the token and writes nothing. |
| `Correction2SavedEvidenceCarriesOutcome.test_saved_choices_shown_carries_the_outcome_phrase` | 0.69 | Saved choices-shown evidence carries the outcome phrase. |
| `ChoicesEnumeration.test_two_distinct_borrowings_stay_two_choices` | 0.61 | Choice enumeration over a hand-built `line21Explanation`. Already does not call the coordinator. Defect: two forms that share one finding id must be one choice. |
| `ResolveOutcomes.test_superseded_names_the_current_one` | 0.55 | Currency of the displayed answer: current, superseded, withdrawn (`no-target`), or not a correction target. Already does not call the coordinator. |
| `ResolveOutcomes.test_no_target_after_withdrawal` | 0.53 | Currency of the displayed answer: current, superseded, withdrawn (`no-target`), or not a correction target. Already does not call the coordinator. |
| `Admission.test_malformed_and_unknown_token_refused_without_echo` | 0.52 | Malformed and unknown tokens are refused without echoing an act, finding, or identifier. |
| `ResolveOutcomes.test_current` | 0.43 | Currency of the displayed answer: current, superseded, withdrawn (`no-target`), or not a correction target. Already does not call the coordinator. |
| `ResolveOutcomes.test_box_witness_is_not_a_target` | 0.37 | Currency of the displayed answer: current, superseded, withdrawn (`no-target`), or not a correction target. Already does not call the coordinator. |
| `ChoicesEnumeration.test_shared_borrowing_two_forms_is_one_choice` | 0.36 | Choice enumeration over a hand-built `line21Explanation`. Already does not call the coordinator. Defect: two forms that share one finding id must be one choice. |
| `Cancel.test_cancel_leaves_log_revision_unchanged` | 0.36 | Preparing a review writes no act. Log revision stays put. |
| `Correction2RelationshipAttribution.test_shared_borrowing_across_two_forms_carries_its_label_on_both` | 0.36 | Financing and inclusion items carry their borrowing label by identity, including one borrowing shared by two forms. |
| `Correction1RedactedRefusal.test_forced_admission_refusal_is_redacted` | 0.35 | Indistinguishable, stale, and forced admission refusals are redacted. |
| `Neighbor.test_prepare_review_cards_still_carry_no_clues` | 0.34 | Ordinary review cards still carry no correction clues. |
| `SurfaceArtifact.test_resolves_and_serves_bytes_equal_to_manifest_entry` | 0.12 | Correction surface bytes equal the manifest entry the session serves. |
| `ChoicesEnumeration.test_empty_presentation_yields_no_choices` | 0.11 | Choice enumeration over a hand-built `line21Explanation`. Already does not call the coordinator. Defect: two forms that share one finding id must be one choice. |
| `NamedStates.test_every_state_including_historical_has_a_description` | 0.00 | Committed correction states seed, and the catalog names each state. Not a derivation. |
| `NamedStates.test_readme_names_each_state_command` | 0.00 | Committed correction states seed, and the catalog names each state. Not a derivation. |

### Form 1099-K, live-required

| Case | Junit | Defect |
| --- | ---: | --- |
| `test_atomic_save_interrupted_leaves_log_clean` | 19.71 | An interrupted answer save leaves the log clean. |
| `test_case12_unrelated_w2_untouched_through_changes` | 15.92 | Currency: `tax.us.2025.w2.box1-wages` stays current and 90000 through recording, correction, and withdrawal. No coordinator call. |
| `test_review_answer_and_correction_and_withdrawal` | 14.58 | Answer, correction, and withdrawal recording. |
| `test_box4_presented_as_supplied_by_person_or_none` | 13.87 | Review presents box 4 from the recorded fact, or none when the fact is absent. No coordinator. |
| `test_atomic_save_of_review_answers` | 11.01 | Saving review answers is one batch. |
| `test_tampered_review_question_or_choice_refused` | 9.19 | A tampered question or choice is refused. |
| `test_review_preparation_and_human_labels` | 7.78 | Review preparation labels for payer, year, box 1a, and box 4. No coordinator. |

### Form 1098, live-required

| Case | Junit | Defect |
| --- | ---: | --- |
| `test_v2_timing_defaults_remain_structural_and_cannot_be_submitted` | 17.70 | Timing fact types keep structural `not-asked`, and the review refuses submitting that token. Log bytes unchanged. No coordinator. |
| `test_v2_versioned_answer_metadata_never_falls_back_or_depends_on_resolution_order` | 10.46 | Saved explanation metadata: versioned answer labels do not depend on member order, and a missing v2 type fails closed. The live run only supplies the finding. |

### Sale, live-required

| `test_case_11_stale_older_version_write_refused` | 7.95 | Recording refuses a v1 write onto an active v2 chain. Revision unchanged. No coordinator. |

### Track 7, live-required

| Case | Junit | Defect |
| --- | ---: | --- |
| `test_correction_removing_a_loan` | 23.71 | Same interruption contract. Completed save publishes 1500. |
| `test_correction_with_an_uncertain_loan` | 17.52 | Same interruption contract. Completed save blocks. |
| `test_correction_adding_a_loan` | 13.89 | Same interruption contract. Completed save blocks. |
| `test_one_save_with_both_links` | 13.18 | Torn and clean interruption of one `append_batch` leaves none of the save. Completed save blocks line 21. |
| `test_first_answer_in_a_v1_workspace_adopts_bundle_v2` | 13.04 | Same interruption contract for the save that adopts relationship bundle v2. Completed save still blocks. |
| `test_amount_only_correction` | 12.22 | Same interruption contract. Completed save publishes 1000. |
| `test_v1_no_on_the_statement_link` | 11.99 | Same interruption contract on the v1 path. Completed save blocks. |
| `test_v1_history_with_an_ended_link_is_refused_with_a_reason` | 11.47 | Adopting v2 over a v1 ended link is refused. Log bytes unchanged. |
| `test_answering_a_borrowing_question` | 10.01 | Same interruption contract. Completed save publishes 1500. |
| `test_yes_after_a_withdrawn_link` | 10.00 | Same interruption contract. Completed save publishes 1500. |
| `test_withdrawing_the_statement_link` | 9.94 | Same interruption contract. Completed save blocks. |
| `test_correcting_a_borrowing_answer` | 9.73 | Same interruption contract. Completed save blocks. |
| `test_no_on_the_financing_link` | 9.45 | Same interruption contract. Completed save blocks. |
| `test_no_on_the_statement_link` | 9.21 | Same interruption contract. Completed save blocks. |
| `test_cannot_tell_on_the_statement_link` | 9.13 | Same interruption contract. Completed save blocks. |
| `test_correcting_the_only_link_beside_old_answers` | 7.39 | Same interruption contract. A partial save must not let the old path deduct. Completed save blocks. |
| `test_a_correction_refused_at_its_box1_act_writes_nothing` | 0.24 | ADR 0077 Part 5 admission: a box 1 act outside the reviewed amount writes nothing. The bound 1300 correction stays current. |
| `test_a_workspace_without_the_relationship_bundle_is_not_given_one` | 0.03 | A workspace that never adopted the relationship bundle refuses the borrowing question. Log bytes unchanged. No coordinator. |

## Package-bytes, track 5

| Case | Junit | What it checks |
| --- | ---: | --- |
| `WorksheetSelection.test_the_worksheet_arithmetic_is_v1_byte_for_byte` | 0.00 | Declared worksheet arithmetic bytes against v1. No derivation. |
| `WorksheetSelection.test_v40_validates_and_the_worksheet_is_a_v13_selection` | 0.36 | Package validation and the v13 selection paths on `tax.us.2025.rule.sli-worksheet` v3. No derivation. |
| `Publication.test_v4_gates_v3_loan_links_on_the_marker_count_and_nothing_else` | 0.00 | Declared v4 loan-link path gates v3 on the marker count. No derivation. |
| `LineReasons.test_every_track4_reason_and_the_refusal_token_have_a_sentence` | 0.00 | Every standing const and the refusal token has a declared sentence. No derivation. |
| `Publication.test_registry_v38_appends_only_and_the_release_pins_it` | 0.00 | Registry append-only and the release pins that registry's bytes. |
| `Publication.test_registry_v39_appends_only_and_the_release_pins_it` | 0.00 | Registry append-only and the v39 release pins that registry's bytes. |
| `Publication.test_v40_is_v39_with_the_worksheet_successor_and_its_inputs` | 0.00 | Package membership: v40 is v39 plus the worksheet successor. Checksum. |
| `Publication.test_v41_is_v40_with_the_marker_gate` | 0.38 | Package membership: v41 is v40 plus the marker gate. `validate_package` accepts v41. |

## Estimate

Safe candidates are 84 cases and 101 coordinator calls. Their junit sum is 863.80s (track 1 525.27s, track 5 338.53s), which is 14.1% of summed worker time. That sum is what the cases spend today. It is not the recoverable share. The recorder stays.

**Recoverable coordinator increment: 50.5s, range 30.3–80.8s.** That is 0.83% of 6113.67s, range 0.50–1.32%. Track 1's 54 single calls are 27.0s of the point estimate. Track 5's 47 calls are 23.5s. The top ten are 13.0s of that.

The seven classified modules are 2634.04s, 43.1% of summed worker time. Almost all of that stays, because it is recording, currency, and saved-review work the move does not remove.

## Limits

- The per-call range is two profiles, deflated by profiled-time over junit. cProfile inflates call-heavy paths. One Track 5 test stands for every track 5 call, and K7 stands for every track 1 call. A short closed-empty run and a phase-out run are not the same coordinator cost; the range is there for that.
- Cold package validation is excluded on purpose. It is paid once per worker. Moving calls does not remove it.
- `run_package` still projects, computes currency, marshals, and runs both runners. The ranking's lattice and fact-type shares sit in that work. This estimate does not claim any of it.
- Junit subtests are one timed row. Call counts for the four-answer loops are from the source, not from the junit file.
- `run_package` skips release resolution, workspace guards, the record stream, companion pairs, the source-boundary check, and two presentation arguments. The three retained cases are what still see those. A coordinator bug that appears only on an act shape the witness does not build — an amount-only correction, a v1 bundle, a second statement — would not be caught by the witness. The moved case would still run the rules on that act shape.
- `test_case_late_unclosed` stays because the source-boundary gap is unresolved. Other closure-backed zeros (`test_case_empty`, `test_closed_empty_publishes_zero`) are candidates. If their zero is produced by the source-boundary check rather than the worksheet, the move would drop it. That is a narrower uncertainty than the unclosed horizon, and it is called out here rather than used to hold every zero back.
- The rendered-page half of the track 5 witness skips when headless Chromium is absent. The saved-file assertions in that test still run.
- Form 1098, Form 1099-K, the sale module, track 7, and the correction session are not in the estimate. Their junit time is large and is not claimed.
- No case was re-timed. The full suite was not run. Shares use the P0 denominator only.

## What this unit did not do

No test was moved or edited. No production code was edited. No full suite was run. Nothing was pushed.
