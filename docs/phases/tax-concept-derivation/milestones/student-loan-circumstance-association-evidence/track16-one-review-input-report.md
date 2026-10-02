# Track 16 — one-review relationship input report

## Demonstrated data contract

The experimental object is an ordinary serializable review, not a page or a
published schema. `prepare_review` snapshots current borrowing, schooling and
1098-E source cards from the ActLog projection. Each card carries a visible
person-readable description, any available recognition clues, and the current
source support used to prepare it. Opaque addresses travel separately as
`choice_ref` action handles. Equal descriptions produce separate cards. No
candidate is preselected, including when only one card is present.

The one review offers two separate statements:

- “Some of this borrowing financed these studies.”
- “This statement includes interest on this borrowing.”

The person can explicitly select the borrowing and the relevant school or
statement, then answer either clause `yes`, `no`, `cannot-tell`, or leave it
`unanswered`. Both `yes` and `no` require the identified pair. A missing pair
cannot become a definite negative. A selected card must also be distinguishable
from the other displayed cards by information shown to the person; an opaque
choice handle cannot resolve two visually identical cards. A `cannot-tell` or
unanswered response can be saved without selecting an indistinguishable
candidate. A single save passes both responses and selections through Track
14's normal durable recorder. Affirmative clauses create their own findings
with the same submitted answer evidence; other responses remain in that
evidence without creating the opposite claim. Before save, the displayed
snapshot is re-prepared from one ActLog read; that same read supplies the
revision passed to the durable recorder. The recorder checks that revision
before staging and carries it unchanged into its first append. A stale review
is refused before any answer is appended.

A statement card shows its year, issuer as printed, and reported box-1 total.
The box-1 number remains the statement's fact. The review marks the interest
portion `not-requested`; an `unknown` portion on an affirmative inclusion is
recorded as unknown and does not change that relationship.

## Concrete review, saved action and recovery

This compact excerpt uses the exact synthetic values from the executed test.
The readable labels and answers are separated from the internal addresses and
source support saved with the answer.

```text
Shown:
  Borrowing: “Autumn study borrowing”
  Schooling: “Riverside College, BSc, autumn 2024”
  Statement: “2025 Form 1098-E” — Cedar Servicing — box 1: 1200.0
  Clause 1: “Some of this borrowing financed these studies.” → yes
  Clause 2: “This statement includes interest on this borrowing.” → yes

Saved answer evidence:
  submission_id: demo.track16.submission.both
  evidence_id: demo.evidence.track16.submission.both
  responses: {financing_response: yes, inclusion_response: yes}
  interest_portion_response: unknown
  references:
    borrowing_ref: demo.track16.borrowing.autumn
    schooling_fact_id: tax.us.2025.sli.schooling-situation|period=demo.track16.period.autumn,institution=demo.track16.institution.river,programme=demo.track16.programme.bsc
    statement_fact_id: tax.us.2025.f1098e.box1-student-loan-interest|lender=demo.track16.lender.cedar,statement=demo.track16.statement.2025,tax-year=2025
  recognition_context also stores the exact choice cards shown, their source
  support, both propositions, review id/time, selections and responses.

Recovered current claims, each supported by the same answer evidence:
  financing: finding sli.relationship.finding.43f808001ac5e38a6ded6962
    value sli.financing.affirmed; contribution sli.relationship.contribution.43f808001ac5e38a6ded6962
    fact tax.us.2025.sli.financing-relationship|borrowing=demo.track16.borrowing.autumn,period=demo.track16.period.autumn,institution=demo.track16.institution.river,programme=demo.track16.programme.bsc
  statement inclusion: finding sli.relationship.finding.fde2a64725f8195d1b9e2064
    value sli.statement-inclusion.affirmed; contribution sli.relationship.contribution.fde2a64725f8195d1b9e2064
    fact tax.us.2025.sli.statement-inclusion-relationship|lender=demo.track16.lender.cedar,statement=demo.track16.statement.2025,tax-year=2025,borrowing=demo.track16.borrowing.autumn
```

These are relationship findings, not a computed amount or eligibility result.
The statement's 1200.0 remains its reported total; the portion remains unknown.

## Executed evidence

`tests/test_sli_track16_one_review_input.py` builds current synthetic sources,
prepares the review from those sources, saves through `record_submission_durably`,
and recovers the resulting evidence and claims with a fresh `ActLog` instance.
The test verifies the exact content shown, selected action references, two
responses, reported statement total, evidence IDs, and current finding IDs.
It also exercises:

- Two equal-described borrowing choices, schooling situations, and statements.
  The cards remain separate and unselected. An explicit affirmative or
  negative selection of one member of each indistinguishable pair is refused;
  `cannot-tell` and `unanswered` are saved without selecting one. An unidentified
  `no` is refused, while `no` for an identified, distinguishable pair remains
  answer evidence without an affirmative claim.
- One affirmative clause while the other is unanswered, a missing selection
  refusal, a target withdrawal after review, and a same fact ID receiving new
  schooling and statement values after review. Both stale cases refuse without
  a partial save.
- Deterministic handoff interleavings for both durable paths: a legitimate
  same-key schooling correction after review validation but before the
  submission recorder reads is retained while the submission is refused; a
  same-key correction after review validation but before the correction
  recorder reads is retained while the correction is refused; and a separate
  correction case inserts the source change immediately before its first
  append. These cases append no attempted answer evidence or relationship
  claim, and correction leaves its predecessor unretracted and current. Each
  case checks the exact resulting ActLog revision and current source finding
  identity/value.
- Correction of financing to a separately selected schooling situation and
  withdrawal of the statement-inclusion claim. A second borrowing and its
  separate statement retain their original finding IDs, fact IDs, values,
  evidence IDs, and contribution IDs as current support.
- The reverse lifecycle in a separate case: correct statement inclusion to a
  separately selected statement, then withdraw financing. The original answer
  and correction evidence remain in the recovered evidence history.

The current positive claims are real Track 14 source findings. No synthetic
result is hand-built. Track 15's neutral consumer was optional and is not run
here. No consequence or treatment is inferred from the affirmative relations.

## Limits and handoff

The cards help a person recognize currently recorded subjects using their
available descriptions and evidence. This demonstration does not establish
that a statement's borrowing composition stayed the same after a same-key
change. It also does not make a relationship automatically unusable after a
source-target retraction; Track 14's applicability query remains opt-in. A
later consumer must account for those limits. The saved input proves what was
prepared for display and affirmed in the test action, not that a person
perceived it. Selection of which current candidates to offer and actual display
or delivery to a person are outside this data-contract test. It does not prove
source applicability, eligibility, an interest amount, a deduction, or tax
treatment. Before save, the contract compares the serialized review's fixed
propositions, default selections/responses, portion prompt and all choice
snapshots against a fresh preparation built from one authoritative ActLog
read. The revision from that read is the recorder's precondition. The
precondition is checked before staging, then used unchanged for the first
append. The tests demonstrate refusal when a source correction has already
committed before the recorder read or before the first append check. The
attempted operation appends no acts in those cases. ActLog checks the expected
revision after its own read, without a cross-writer lock around the subsequent
write; this evidence does not establish protection from arbitrary simultaneous
writers. After a successful first append, later acts still append one at a
time; this handoff does not provide atomicity against a later multi-act
interleaving.

The sentences and object layout are candidates for review, not accepted
wording or product integration. This is a data contract, with no new published
schema, general UI, worksheet connection, or reader expansion. Interest
allocation, whole-statement treatment, G2, and ADR 0076 Part 3 remain deferred.

## Verification

- `python3 -m pytest tests/test_sli_track16_one_review_input.py
  tests/test_sli_relationship_recording.py
  tests/test_sli_track15_versioned_source_consumer.py -q` — **25 passed**,
  including all three deterministic handoff interleavings.
- `python3 -m mypy packages/tax/sli_relationship_review.py
  packages/tax/sli_relationship_recording.py
  tests/test_sli_track16_one_review_input.py` — clean.
- `python3 tools/governance_lint.py` — conformant.
- `git diff --check` — clean.
- Captured full suite, `python3 -m pytest -n auto`, with local socket
  permission enabled from process start and `pipefail` — **2,413 passed, 20
  skipped, 0 failed; exit 0; 314.77 seconds**. Session handle: `6112`.
- Durable ignored output: `temp/track16-repair/full-suite.log` and
  `temp/track16-repair/full-suite-metadata.json`. Metadata records the command,
  session, counts, exit code, duration and executable hashes. Python 3.14.3
  SHA-256: `83177d8351dbd470c6072025c5d4a56162437b12110e56f2a798564e64e012e5`;
  pytest CLI SHA-256:
  `ff99a092615ea26925d2cab494fa7504439b7a46fe2b8e8cfb599d43bb73de1a`;
  pytest module SHA-256:
  `ee37885c9583f843390684dfb496907f87a0905128e7a3cf4ad227f49ff34c2d`.
- The earlier captured full-suite result above this section is historical
  pre-repair evidence; this run verifies the repaired implementation. The local
  captured run is implementation evidence. The PR's CI verification remains
  the merge gate of record.

### Historical pre-repair verification

- `python3 -m pytest tests/test_sli_track16_one_review_input.py tests/test_sli_relationship_recording.py tests/test_sli_track15_versioned_source_consumer.py -q` — **22 passed**.
- `python3 -m mypy packages/tax/sli_relationship_review.py tests/test_sli_track16_one_review_input.py` — clean.
- `python3 -m pytest tests/test_kernel_fixtures.py tests/test_envelope_hooks.py -q` — **14 passed, 5 subtests passed**.
- `python3 tools/governance_lint.py` — conformant.
- `git diff --check` — clean.
- Captured full suite, `python3 -m pytest -n auto`, with local socket
  permission enabled from process start and `pipefail` — **2,410 passed, 20
  skipped, 0 failed; exit 0; 291.01 seconds**. Session handle: `83435`.
- Durable ignored output: `temp/track16/full-suite.log` and
  `temp/track16/full-suite-metadata.json`. The metadata records the command,
  session, counts, exit code, duration and executable hashes. Python 3.14.3
  SHA-256: `83177d8351dbd470c6072025c5d4a56162437b12110e56f2a798564e64e012e5`;
  pytest 9.1.1 module entrypoint SHA-256:
  `37f8b6a3df1aef71336bce85e366db968ede153dd72ad4e60bebff79e279dc40`.
- This local captured run is implementation evidence. The PR's CI verification
  remains the merge gate of record.
