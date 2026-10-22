# P0 fold attribution

Audience: Builder, reviewer.

Producer commit: the milestone plan commit. Python 3.14.3. CPU is `time.process_time` (user plus system). Wall is `time.perf_counter`. Every measured operation completed. Raw output stays under `temp/projection-reuse/`.

Command: `python3 temp/projection-reuse/measure_p0.py`

The counting wrapper lives only in that script. It replaces `findings.project` and rebinds every module global that is that same function, then wraps `ActLog.append` and `ActLog.append_batch`. Nine bindings were rebound: the kernel act log, the live coordinator, the correction session, both Form 1099-K modules, both student-loan modules, and two test modules that import the same function. `packages.kernel.facts.project` was left as its own function. No measured call came from a test or from the script.

Preparation stays outside the counter and the clock: copying the log, opening `ActLog`, building the shared registry, preparing the review snapshot, and opening the record stream. The measured call is the recorder, the review function, or `live_coordinate_run`. A save, correction, withdrawal, or removal still revalidates inside that call, and those folds are counted. `live_coordinate_run` is called without a schemas argument, so its own `DerivationSchemas()` construction sits inside the live-run figure.

## Short history

266 acts. The committed fixture `packages/sample_data/sli_correction_t1/workspace/acts.jsonl` is 262 acts and is copied as bytes. That file is the state-base seed the correction story already loads. One Autumn loan-cost answer is then corrected from yes to no through `prepare_borrowing_answer_review` and `correct_borrowing_answer_review`. One borrowing, `demo.borrowing.measured` ("Measured study loan"), is introduced through `introduce_borrowing_reference_durably`.

The extra borrowing is there so the measured save has an unanswered question. Autumn and Spring already have current answers for both ordinary questions. The measured save answers `enrolled-at-least-half-time` yes for `demo.borrowing.measured`. The measured correction changes the Spring loan-cost answer from yes to no. The measured withdrawal withdraws the Autumn enrollment answer. The measured read is `CorrectionRuntime.state` on the presentation from one setup `live_coordinate_run` (`core_calculations_surface`, run `demo.correction.run.initial`). That setup run produced a presentation.

This history has no Form 1099-K statement recorder and no statement removal. Those two operations are blank.

Kind counts after the correction and the introduced borrowing: assertion 129, bundle-adoption 36, contribution 23, entity-introduced 18, evidence-submitted 23, horizon-genesis 34, member-transition 1, package-adoption 2.

## Long history

307 acts. The seed is `tests.test_f1099k_personal_item_sale_track1._make_base_acts` finished by `tests.test_f1099k_saved_presentation_increment_d._finish_acts_v49`, 186 acts, committed with `append_batch` at revision 0. Three statements are then recorded with `close_family` false:

| Statement | Payer | Statement ref | Box 1a |
| --- | --- | --- | ---: |
| A | `demo.platform.a` | `demo.stmt.a` | 880 |
| B | `demo.platform.b` | `demo.stmt.b` | 460 |
| C | `demo.platform.c` | `demo.stmt.c` | 220 |

A and B receive the full circumstance answers through `record_f1099k_statement_answers_durably`. C is left unanswered so the measured save is an initial save. Three corrections go through `correct_f1099k_statement_answer_durably`: A purchase-cost to 1100, A platform-fees to 60, B agreed-item-price to 750. `close_f1099k_family_durably` moves the log from 304 acts to 307. The actor is `demo.user.filer-1`.

The measured record adds statement D (`demo.platform.d` / `demo.stmt.d`, box 1a 100, `close_family` false) on that closed family, and the recorder accepts it. The measured save writes the full answer set on C through `save_f1099k_statement_review`. The measured correction sets A purchase-cost to 1050 through `correct_f1099k_statement_review_answer`. The measured withdrawal withdraws `refund-amount` on B. The measured removal retracts C. The measured read is `review_f1099k_statement_with_saved_presentation` for statement A, using the presentation and record stream from one setup `live_coordinate_run` (`SURFACE_V47`, run `demo.f1099k.run.saved`). That setup run produced a presentation.

Kind counts: assertion 143, bundle-adoption 37, contribution 37, entity-introduced 13, evidence-submitted 37, horizon-genesis 35, member-transition 4, package-adoption 1.

## Project calls and acts folded

Acts folded means the length of the act sequence passed to `project`. The same digest means the same sequence of act ids.

| Operation | Short calls | Short acts | Long calls | Long acts |
| --- | ---: | ---: | ---: | ---: |
| Record a statement |  |  | 4 | 1238 |
| Save or answer | 7 | 1866 | 4 | 1273 |
| Correct an answer | 7 | 1866 | 4 | 1231 |
| Withdraw an answer | 2 | 533 | 3 | 923 |
| Remove a statement |  |  | 4 | 1232 |
| Read a saved presentation | 6 | 1596 | 1 | 307 |
| Live coordinate run | 1 | 266 | 1 | 307 |

Each call, in order:

| History | Operation | Acts | Caller |
| --- | --- | ---: | --- |
| Short | Save or answer | 266 | `packages/tax/sli_relationship_review.py:_prepare_borrowing_answer_review_from_contents` |
| Short | Save or answer | 266 | `packages/tax/sli_relationship_review.py:borrowing_recognition_clues` |
| Short | Save or answer | 266 | `packages/tax/sli_relationship_recording.py:_stage_relationship_v2_adoption` |
| Short | Save or answer | 266 | `packages/tax/sli_relationship_recording.py:_current` |
| Short | Save or answer | 267 | `packages/tax/sli_relationship_recording.py:_record_borrowing_answer_durably` |
| Short | Save or answer | 266 | `packages/tax/sli_relationship_recording.py:_stage_enrollment_follows_schooling` |
| Short | Save or answer | 269 | `packages/tax/sli_relationship_recording.py:_record_borrowing_answer_durably` |
| Short | Correct | 266 | `packages/tax/sli_relationship_review.py:_prepare_borrowing_answer_review_from_contents` |
| Short | Correct | 266 | `packages/tax/sli_relationship_review.py:borrowing_recognition_clues` |
| Short | Correct | 266 | `packages/tax/sli_relationship_recording.py:_stage_relationship_v2_adoption` |
| Short | Correct | 266 | `packages/tax/sli_relationship_recording.py:_current` |
| Short | Correct | 267 | `packages/tax/sli_relationship_recording.py:_record_borrowing_answer_durably` |
| Short | Correct | 266 | `packages/tax/sli_relationship_recording.py:_stage_enrollment_follows_schooling` |
| Short | Correct | 269 | `packages/tax/sli_relationship_recording.py:_record_borrowing_answer_durably` |
| Short | Withdraw | 266 | `packages/tax/sli_relationship_recording.py:withdraw_borrowing_answer_durably` |
| Short | Withdraw | 267 | `packages/tax/sli_relationship_recording.py:withdraw_borrowing_answer_durably` |
| Short | Read a saved presentation | 266 | `packages/derivation/correction_session.py:_scan_displayed_answers` |
| Short | Read a saved presentation | 266 | `packages/derivation/correction_session.py:_entity_label` |
| Short | Read a saved presentation | 266 | `packages/tax/sli_relationship_review.py:borrowing_recognition_clues` |
| Short | Read a saved presentation | 266 | `packages/derivation/correction_session.py:_entity_label` |
| Short | Read a saved presentation | 266 | `packages/tax/sli_relationship_review.py:borrowing_recognition_clues` |
| Short | Read a saved presentation | 266 | `packages/derivation/correction_session.py:_attribute_borrowing_labels` |
| Short | Live coordinate run | 266 | `packages/derivation/live.py:live_coordinate_run` |
| Long | Record a statement | 307 | `packages/tax/f1099k_statement_recording.py:_ensure_bundles` |
| Long | Record a statement | 307 | `packages/tax/f1099k_statement_recording.py:record_f1099k_statement_durably` |
| Long | Record a statement | 311 | `packages/kernel/act_log.py:append_batch` |
| Long | Record a statement | 313 | `packages/tax/f1099k_statement_recording.py:_commit` |
| Long | Save or answer | 307 | `packages/tax/f1099k_statement_review.py:prepare_f1099k_statement_review` |
| Long | Save or answer | 307 | `packages/tax/f1099k_statement_recording.py:_ensure_bundles` |
| Long | Save or answer | 307 | `packages/tax/f1099k_statement_recording.py:record_f1099k_statement_answers_durably` |
| Long | Save or answer | 352 | `packages/tax/f1099k_statement_recording.py:_commit` |
| Long | Correct | 307 | `packages/tax/f1099k_statement_review.py:prepare_f1099k_statement_review` |
| Long | Correct | 307 | `packages/tax/f1099k_statement_recording.py:_ensure_bundles` |
| Long | Correct | 307 | `packages/tax/f1099k_statement_recording.py:correct_f1099k_statement_answer_durably` |
| Long | Correct | 310 | `packages/tax/f1099k_statement_recording.py:_commit` |
| Long | Withdraw | 307 | `packages/tax/f1099k_statement_review.py:prepare_f1099k_statement_review` |
| Long | Withdraw | 307 | `packages/tax/f1099k_statement_recording.py:withdraw_f1099k_statement_answer_durably` |
| Long | Withdraw | 309 | `packages/tax/f1099k_statement_recording.py:_commit` |
| Long | Remove a statement | 307 | `packages/tax/f1099k_statement_review.py:prepare_f1099k_statement_review` |
| Long | Remove a statement | 307 | `packages/tax/f1099k_statement_recording.py:retract_f1099k_statement_durably` |
| Long | Remove a statement | 308 | `packages/kernel/act_log.py:append_batch` |
| Long | Remove a statement | 310 | `packages/tax/f1099k_statement_recording.py:_commit` |
| Long | Read a saved presentation | 307 | `packages/tax/f1099k_statement_review.py:prepare_f1099k_statement_review` |
| Long | Live coordinate run | 307 | `packages/derivation/live.py:live_coordinate_run` |

On the short log, five of the seven save folds and five of the seven correction folds are the same 266-act sequence. All six read folds are that same sequence. On the long log, the 307-act sequence repeats twice inside record, three times inside save, three times inside correct, twice inside withdraw, and twice inside remove.

## Checked projections inside each save

"Checked" is a `project` call whose immediate caller is `append_batch` or `append`. The folded lengths are the prefixes that call saw.

| Operation | History | Write | Acts written | Checked | Prefixes folded |
| --- | --- | --- | ---: | ---: | --- |
| Save or answer | Short | `append_batch` | 3 | 0 |  |
| Save or answer | Long | `append_batch` | 45 | 0 |  |
| Correct | Short | `append_batch` | 3 | 0 |  |
| Correct | Long | `append_batch` | 3 | 0 |  |
| Withdraw | Short | `append` | 1 | 0 |  |
| Withdraw | Long | `append_batch` | 2 | 0 |  |
| Record a statement | Long | `append_batch` | 6 | 1 | 311 |
| Remove a statement | Long | `append_batch` | 3 | 1 | 308 |

The read and the live run write nothing. The answer saves and corrections commit their acts with no checked projection. Record checks one of its six new acts, folding a 311-act prefix. Remove checks one of its three new acts, folding a 308-act prefix.

## Top callers

Totals across both histories.

| Caller | Calls | Acts folded |
| --- | ---: | ---: |
| `packages/tax/f1099k_statement_recording.py:_commit` | 5 | 1594 |
| `packages/tax/f1099k_statement_review.py:prepare_f1099k_statement_review` | 5 | 1535 |
| `packages/tax/sli_relationship_recording.py:_record_borrowing_answer_durably` | 4 | 1072 |
| `packages/tax/sli_relationship_review.py:borrowing_recognition_clues` | 4 | 1064 |
| `packages/tax/f1099k_statement_recording.py:_ensure_bundles` | 3 | 921 |
| `packages/kernel/act_log.py:append_batch` | 2 | 619 |
| `packages/derivation/live.py:live_coordinate_run` | 2 | 573 |
| `packages/tax/sli_relationship_recording.py:withdraw_borrowing_answer_durably` | 2 | 533 |
| `packages/tax/sli_relationship_review.py:_prepare_borrowing_answer_review_from_contents` | 2 | 532 |
| `packages/tax/sli_relationship_recording.py:_stage_relationship_v2_adoption` | 2 | 532 |
| `packages/tax/sli_relationship_recording.py:_current` | 2 | 532 |
| `packages/tax/sli_relationship_recording.py:_stage_enrollment_follows_schooling` | 2 | 532 |
| `packages/derivation/correction_session.py:_entity_label` | 2 | 532 |
| `packages/tax/f1099k_statement_recording.py:record_f1099k_statement_durably` | 1 | 307 |
| `packages/tax/f1099k_statement_recording.py:record_f1099k_statement_answers_durably` | 1 | 307 |
| `packages/tax/f1099k_statement_recording.py:correct_f1099k_statement_answer_durably` | 1 | 307 |
| `packages/tax/f1099k_statement_recording.py:withdraw_f1099k_statement_answer_durably` | 1 | 307 |
| `packages/tax/f1099k_statement_recording.py:retract_f1099k_statement_durably` | 1 | 307 |
| `packages/derivation/correction_session.py:_scan_displayed_answers` | 1 | 266 |
| `packages/derivation/correction_session.py:_attribute_borrowing_labels` | 1 | 266 |

## CPU on the long history

One in-process pass, before the wrapper was installed, after the history had already been built in that process. Order is the table order. The sum of the unrounded CPU figures is 5.301 seconds.

| Operation | CPU seconds | Wall seconds |
| --- | ---: | ---: |
| Record a statement | 1.251 | 1.256 |
| Save or answer | 0.913 | 0.915 |
| Correct an answer | 0.764 | 0.765 |
| Withdraw an answer | 0.587 | 0.588 |
| Remove a statement | 0.766 | 0.768 |
| Read a saved presentation | 0.196 | 0.196 |
| Live coordinate run | 0.825 | 0.829 |

Wall stays within a few milliseconds of CPU on every row, so these figures are compute.

## Cold start

One fresh process. The case is `tests.derivation.test_presence_selection_subject_reads.run_case` on `adr0077_worksheet_fixture.case_rows("old-only")`, the `TrackOneA4Cases` case. Both calls return line 21 value 2500 from the forward runner and the reference runner.

| Call | CPU seconds | Wall seconds |
| --- | ---: | ---: |
| First | 2.435 | 2.443 |
| Second | 0.027 | 0.027 |

The first call costs 2.408 seconds more CPU than the second. That gap is the per-process cold cost of this case.

## Ranking

Sources, over both histories for acts and over the long history for CPU. The CPU column splits each operation's CPU in proportion to the acts that source folded. It is a proxy for share, and it is the whole operation's CPU, including work that is outside `project`.

| Source | Acts folded | Share of acts | CPU proxy seconds | Share of long CPU |
| --- | ---: | ---: | ---: | ---: |
| Repeated helper projections | 11446 | 90.6% | 3.971 | 74.9% |
| Save-path re-projection | 619 | 4.9% | 0.506 | 9.5% |
| Coordinator's own fold | 573 | 4.5% | 0.825 | 15.6% |
| Test helpers | 0 | 0% | 0.000 | 0% |

By acts folded the order is helpers, then the save path, then the coordinator. By the CPU proxy the order is helpers, then the coordinator, then the save path. The coordinator's CPU share is larger than its act share because the live run's entire CPU, including schema construction inside the call, is assigned to its single fold.

Helpers are the repeated projections inside one recording or review call (Track 2). The save path is `append` and `append_batch` (Track 1). The coordinator row is only the immediate caller `live_coordinate_run`. On these runs that function folded the log once and no other caller folded during the live call.

A boundary that holds one projection for the rest of the call can drop the extra folds of one act-id sequence inside that call. That is 13 extra folds of the 266-act short log and 7 extra folds of the 307-act long log, 5607 acts. The same boundary can extend that state through the longer sequences in the same call — the 267-act and 269-act student-loan folds, and the Form 1099-K folds of 308 to 352 acts — instead of starting again at the first act.

The first full-log fold of each operation remains. Twelve operations each start with one: five on the short log and seven on the long log, 3479 acts. Sharing those across calls is a projected prefix kept after the call returns, which this milestone leaves out of scope.

Inside one batch, a running fold removes a second and later check. The answer batches checked nothing. Record and remove each checked once, so those two batches have no second check to remove. The single check still replays a prefix the helpers in the same call have already folded (311 acts on record, 308 on remove).

## Limits

- The suite was not run. These figures are the twelve measured operations plus one cold-start case. They are not a share of suite CPU.
- The CPU proxy follows acts folded. Equal act-id sequences are the same folded history, which says nothing about their individual CPU.
- The short history leaves record and remove blank.
- Long-history CPU is one warm pass in one process. Package resolution and schema memos are already warm from building the history, and a later operation can reuse memos an earlier operation filled. The cold-start section is the fresh-process measurement.
- The wrapper was installed after the CPU pass.
- Copying the log, opening it, building the registry, preparing the review the page would have shown, and opening the record stream are outside both the count and the clock.
- This unit chooses no production change.
