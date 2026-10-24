# Track 1 recording build report

Implemented the bounded recording vocabulary and durable account operations.
The new mortgage borrowing bundle distinguishes an opaque mortgage reference,
borrowing/year claims, four exact report-link outcomes, the annual numeric
ceiling, the separate other-debt answer, and five explicit shared answers.
The recorder adopts that bundle on first use and records each claim through
evidence, contribution, and finding acts. Corrections retract and replace one
exact current claim in the same append batch. Clear retracts current 2025
recognition, relationship outcomes, ceiling, and shared answers while retaining
the entity, source reports, local answers, history, and other-debt answer.

The exact-source Form 1098 answer recorder now permits an answer save when
multiple reports are current, provided the selected report has exactly one
current Box 1 source. Missing or duplicate exact sources still refuse. The
review surface's single-report behavior is unchanged.

Focused synthetic recorder coverage verifies same-label opaque identities,
wrong-kind and missing-reference refusal, two exact report links, correction
isolation, finite nonnegative ceiling validation, stale revision refusal,
explicit withdrawal, and clear retention. These checks establish recording
behavior only; no calculation, package adoption, or production reader behavior
is claimed.

The five shared fact types use canonical production identifiers under
`tax.us.2025.mortgage.shared-*`; synthetic workspace identities remain
`demo.*`. Orphan recovery was exercised after a real F1098 `member-transition`
removed Box 1 while keeping the statement entities current: the exact affirmed
link could be replaced with a `withdrawn` outcome, while a new affirmation
without the source refused.

Verification results, with normal pytest parallel settings:

| Command | Result |
| --- | --- |
| `PYTEST_ADDOPTS='-p no:cacheprovider' pytest tests/test_mortgage_borrowing_recording.py tests/test_f1098_statement_recording.py` | 13 passed at that run. |
| `PYTEST_ADDOPTS='-p no:cacheprovider' pytest tests/test_mortgage_borrowing_recording.py::MortgageBorrowingRecordingTests::test_ceiling_validation_evidence_and_atomic_account_clear_preserve_other_debt tests/test_f1098_statement_recording.py::F1098StatementRecordingTests::test_two_exact_reports_keep_independent_answers_when_one_is_corrected` | 2 passed after adding the final clear and two-report isolation coverage. This was a focused changed-case run, not a final rerun of both modules. |
| `python3 -m mypy --cache-dir=/tmp/mypy-mortgage-track1 packages/tax/mortgage_borrowing_recording.py packages/tax/loader.py packages/tax/f1098_statement_recording.py` | Success: no issues in 3 source files. |
| `python3 -m mypy --cache-dir=/tmp/mypy-mortgage-track1` | Success: no issues in 383 source files. |
