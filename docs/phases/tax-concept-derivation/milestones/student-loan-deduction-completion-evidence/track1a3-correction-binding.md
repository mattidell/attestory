# Track 1a-3 — correction binding

Labels: **implemented** means code changed and tested in this unit. **Proposed** means ADR text, or a disposable probe. The kernel enforcer and the replay omission are proposed.

## Binding

One scope evidence authorizes one admitted finding. The three sides are the box 1 finding the review saw (`reviewed_statement_finding_id`), the intended correction (`corrected_box1_total` and `source_correction_id`), and the resulting finding (that amount, that correction identity on its corrected-statement evidence, and that finding as its predecessor). The evidence kind is `tax.student-loan.relationship-answer`. Statement identity, an allowed scope, and a refresh flag are not enough. A missing field fails closed. The fields sit on open `evidence.v1` content. No published schema changes.

The recorder (`_append_statement_source_correction_durably`) and the read-side check (`_reviewed_correction_refreshes`) use that binding. Part 5 states the same rule for `apply_assertion`.

## Counterexamples

Owner reuse, before the fix. The failing test was committed before the fix. Command: `python3 -m pytest tests/test_sli_correction_entry_enforcement.py::CorrectionEntryEnforcement::test_unreviewed_2900_citing_reviewed_1775_scope_evidence_is_not_current -q --tb=short`. Result: 1 failed, `AssertionError: 'current' != 'unresolved-applicability'`. A reviewed 1775 was followed by an unreviewed 2900 citing `demo.evidence.track6.reviewed-1775`, and the read-side reported the inclusion current. Label: the defect, recorded before the fix.

Same reuse, after the fix. **Implemented.** `test_unreviewed_2900_citing_reviewed_1775_scope_evidence_is_not_current`. The recorder raises `RelationshipRecordingRefused` before any append. The revision is unchanged. 1775 stays current. The inclusion stays current. `demo.finding.track1a3.smuggle-2900` is absent. A kernel-admitted smuggle of the same citation is then in the log. `project` admits it. The read-side reports `unresolved-applicability`. **Proposed:** `apply_assertion` would refuse that smuggle.

Same amount. **Implemented.** `test_same_amount_reuse_of_scope_evidence_is_refused`. A second update of 1775 citing `demo.evidence.track6.same-amount` is refused. The revision is unchanged. The inclusion stays current.

Changed box 1. **Implemented.** `test_reviewed_correction_against_a_changed_box1_is_refused`. The review is prepared, box 1 is appended at 1640, and `apply_statement_correction_review` refuses. The revision is unchanged. 1775 is not in the log. Applicability is `unresolved-applicability`.

Different predecessor. **Implemented.** `test_scope_evidence_for_a_different_predecessor_does_not_refresh`. One citation whose `reviewed_statement_finding_id` is not the predecessor stays `unresolved-applicability`. An evidence-id-only check would report current.

Wrong kind. **Implemented.** `test_wrong_kind_scope_evidence_does_not_refresh`. The recorder refuses. A smuggled finding on kind `tax.other-answer` stays `unresolved-applicability`.

Ordinary routes. **Implemented.** `test_case_1_reviewed_amount_only_keeps_inclusion_and_both_amounts` and `test_case_2_reviewed_removal_drops_applicability_and_keeps_affirmation` still pass. Case 1 stores the binding and stays current. Case 2 answers the inclusion before the source append.

Command after the fix: `python3 -m pytest tests/test_sli_correction_entry_enforcement.py tests/test_sli_relationship_recording.py -q --tb=line`. Result: 23 passed, 1 failed. The failure is `OrdinaryRelationshipRecording.test_statement_inclusion_correction_and_withdrawal_are_independent`, `unresolved-applicability` != `current`. It is the pre-existing Track 6 expectation on a direct unscoped append. This unit did not edit that test. `python3 -m mypy`: `Success: no issues found in 307 source files`.

## Boundary

`ActLog.append` persists a schema-valid act. It does not admit. `project` admits through `apply_assertion`, which does not know Part 5, so the smuggle projects. The boundary that refuses a new correction before it is persisted is `_append_statement_source_correction_durably`: the 2900 write leaves no assertion. **Implemented.**

No single boundary covers every write. Other appenders (`record_submission_durably`, `correct_relationship_claim_durably`, the unresolved-inclusion and borrowing writers, nominee allocation, `entry_loop`, `runner`) do not know this binding. Part 5 binds the proposed rule at `apply_assertion`, the function replay and `apply_contribution_batch` both reach. **Proposed.** This unit does not edit `packages/kernel` or `packages/derivation`.

## Replay

**Proposed.** Replay the acts unchanged. `project` does not raise, so the history stays readable. Refusing to project would make the workspace unreadable. A version gate alone would still replay the inclusion and the unbound box 1 as current, and the chain would still deduct.

The chain does not call `current_claim_applicability`. `marshal_run_context` builds sources from `current_finding_ids`. Today the smuggled 2900 and the old inclusion are both current, so the identity join supports the deduction. The choice omits that inclusion from the subject set when the read-side binding is not `current`. The box 1 finding stays. Track 0f item 1: a statement missing its inclusion publishes no conclusion, and the worksheet blocks `DEPENDENCY_ABSENT` rather than deducting. A workspace with no inclusion has nothing to omit.

Probe, not installed: `PYTHONPATH=. python3 temp/track1a3/replay_probe.py`. Output:

```
recorder_refused=True
revision_unchanged=True
project_raises=false
history_readable=true acts=24
chain_today_box1=[2900.0]
chain_today_inclusion_current=True
read_side=unresolved-applicability
chain_proposed_inclusion_ids=[]
no_claim_box1_before=[1250.0]
no_claim_box1_after=[1410.0]
no_claim_inclusions=[]
no_claim_proposed_omits=[]
no_claim_applicability=[]
```

## What is which

Implemented: the recorder refusal, the read-side binding, including evidence kind, and the tests above.

Proposed: Part 5's `apply_assertion` rule with the same binding, and the replay omission. The probe shows the omission. It is not installed.
