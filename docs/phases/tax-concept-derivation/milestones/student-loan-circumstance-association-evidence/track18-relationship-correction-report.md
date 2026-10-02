# Track 18 — integrated relationship correction report

## Delivered capability

`apply_statement_correction_review` records correction scope and the corrected
box-1 source through one review-bound route and ordinary durable admission:

- **Amount only:** saves that included borrowings did not change before
  appending the corrected source. The corrected source finding cites that
  reviewed scope evidence, so the scope is in its support chain. A fresh
  recovery between those appends sees the scope evidence and old current
  amount; after source admission the guarded consumer follows the new finding
  without another inclusion answer.
- **Inclusion added:** saves the named scope first, admits the corrected source
  citing that evidence, then records the affirmative relationship against the
  corrected source. The saved intermediate state cannot publish the added
  pair against the prior composition.
- **Inclusion removed:** records `no` for the identified pair, ends that
  finding's current support, and preserves its finding and answer history
  before appending the corrected source.
- **Inclusion uncertain:** records `cannot-tell` for the identified pair,
  ends its current support before appending the corrected source, and creates a
  separately admitted unresolved status for that exact pair.

The statement and borrowing must appear in the prepared review. A stale review
is refused before the first write. Other borrowings on that statement, the
separate second statement, financing, and unknown interest portion remain
independent. A later affirmative correction uses the existing reviewed
correction route and creates a new finding with current answer provenance.
After `cannot-tell`, a later reviewed `yes` retracts that pair's current
unresolved status, preserves its history and answer support, then admits a new
affirmative finding. A later reviewed `no` also saves the answer and retracts
the exact pair's unresolved status; prior yes and cannot-tell evidence remain
historical, and neither affirmative nor unresolved output remains for that
pair. Neither answer derives a tax negative.

An unidentifiable replacement statement is refused when its subject was not
among the review's current source choices. The person must identify it; the
route does not match by amount, label, order, or handle.

For `no` and `cannot-tell`, the recorder validates the full answer, appends the
finding retraction first, then appends the answer against the revision created
by that retraction. If the answer append fails, the method raises “prior
affirmation support is ended; the new answer was not saved”; it returns no
saved-answer result. A later failure to admit unresolved status raises a
distinct error stating that the cannot-tell answer was saved but its consumer
status was not. The append-only log does not make these acts atomic, so a
partial failure requires a fresh review.

## Integrated demonstration

`tests/test_sli_track18_relationship_correction.py` uses two borrowings on the
first statement and an independent second statement. It proves the old defect:
an ordinary `no` submission is saved while the previous affirmative finding
remains current and the consumer still publishes it.

The integrated route then demonstrates a stale review refusal; amount-only
scope saved before source admission and inspected in the intermediate ActLog
state; an explicit removal affecting only its named pair; and an uncertain
correction that holds its pair before source admission. The same previously
affirmed pair is exercised in two recovered workspaces: `no` has no inclusion
observation or unresolved status, while `cannot-tell` produces a neutral
unresolved observation keyed to that pair. The unresolved finding carries the
answer evidence, and the consumer pins it and the current statement source.
The corrected source cites the scope answer in its evidence lineage. The other
borrowing and second statement retain their identities and full pins. Both an
explicit addition (source first) and a later `yes` after uncertainty are
demonstrated; that `yes` withdraws current unresolved output while retaining
the unresolved finding and answer in history. A replacement not represented
among current review choices is refused. A later `no` after uncertainty is
also demonstrated through a separate recovered workspace: its answer is saved,
the unresolved status is historical, neither output remains for that pair, and
the independent pair remains observable. Forward and reference runners agree
after each saved recovery. Forced second-append failures for cannot-tell and
no-after-uncertain prove that retraction-only partial writes raise without
reporting either answer as saved. In both cases the affected current support
is ended, historical evidence remains inspectable, and fresh recovery yields
no usable output for that pair.

The test selects package v4 by exact v36 release and registry resolution,
validates package admission, then runs both consumers through
`_run_v36`. V36 adds a separate unresolved vocabulary and one neutral rule.
The v35 package, registry, release and previously published schemas remain
unchanged.

This safety claim applies only when a statement correction uses the reviewed
`apply_statement_correction_review` route. An uncoordinated direct source
append bypasses correction scope; v36 can continue publishing an old inclusion
against the newly current same-identity statement because no action says the
composition changed. Direct source writes therefore do not establish a safe
correction workflow.

## Evidence and remaining boundary

Implemented behavior is the reviewed correction route, fail-closed relationship
standing transition, and saved unresolved status for `cannot-tell`. Demonstrated
behavior is the synthetic workflow through fresh ActLog recovery and both
admitted neutral runners. The software can consume current affirmative support
against the exact current source, or expose a saved cannot-tell state without
presenting it as inclusion or denial. Neither result supplies interest
allocation or tax treatment.

G2 and G3 remain unpassed; ADR 0076 Part 3 and worksheet integration remain
deferred. This track does not close the milestone and leaves the owner-approved
partial-result disposition open.

## Verification

- Track 18 plus Tracks 14–17 focused tests: **32 passed**.
- Fixture and envelope safety checks: **14 passed, 5 subtests passed**.
- Targeted mypy on both relationship modules and the new test: clean.
- Governance lint: **conformant**.
- Captured full suite: `pytest -n auto`, one run, **2,420 passed, 20 skipped,
  exit 0**, in 349.30s; 10 workers, 2,440 test items. Local socket permission
  was granted from process start as required by the charter. The durable,
  ignored log is `temp/track18/full-pytest.log`; process session **49731**;
  exact exit record is `temp/track18/full-pytest-status.txt` (`FULL_PYTEST_EXIT=0`).
- Executable hashes for the captured run: Python 3.14.3
  `83177d8351dbd470c6072025c5d4a56162437b12110e56f2a798564e64e012e5`;
  pytest `ff99a092615ea26925d2cab494fa7504439b7a46fe2b8e8cfb599d43bb73de1a`.
- No commit or push was made; handoff is for Foreman review.
