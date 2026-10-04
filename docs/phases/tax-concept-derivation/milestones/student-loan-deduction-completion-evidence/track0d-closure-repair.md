# Track 0d closure repair

> **Curation note.** The disposable probe this report ran was removed when the milestone was prepared for publication. The commands below are kept as a record; the results recorded here are the evidence.

Disposable evidence. Not production content. Conclusion words are Track 0e's:
`plain-case-supported` and `not-supported`.

Command:

```text
PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0d_probe.py evidence1
```

Exit code 0. Both runners agreed on every case below. Scratch JSON is under
ignored `temp/track0d/`.

## Stand-in

Label: executed with the runtime stand-in operator.

`shared_key_count` is not a schema token. The probe validates the
inclusion-support rule with a literal `0`, then replaces that value in the
marshalled rule and patches the evaluator. The operator counts current
financing rows that share the inclusion's `borrowing`. It does not read the
financing value, the schooling, or evidence text. A financing row with no
`borrowing` key blocks every inclusion and names that finding. Zero matches
return 0 and add no financing pin. The inclusion pin is the dispatcher's.

## Evidence 1 — carry-back

The inclusion rule publishes numeric support for every inclusion it is given.
Support is 1 only when the stand-in count is 1, both re-keyed answers are
`yes`, and the financing-scope mark is `complete` or `closed-denial`. A missing
answer takes the declared default `no` and publishes 0. The statement rule
publishes for every box 1. It publishes `plain-case-supported` only when the
inclusion `link_count` is 1, ADR 0075 `link_coverage` of those support values
is 1, and the statement-scope mark is `complete` or `closed-denial`. Otherwise
it publishes `not-supported`. Scope marks default to `complete` when no scope
row is present. That default is a declared parameter pin, origin
`declared_default`.

Label for every chain row in this section: executed with the runtime stand-in
operator. The worksheet dollar result uses the existing candidate worksheet,
with the old-fact collect swapped to the chain's conclusion symbol. The
conclusion finding id fed to that worksheet is the chain publication id, not a
hand-authored flag. Because that flag was produced by the stand-in chain, the
dollar result is labeled executed with the runtime stand-in operator. The
presentation section is labeled presentation only.

| Case | Support | Statement | Worksheet | Presentation |
| --- | --- | --- | --- | --- |
| Plain, box 1 of 3000, income 50000 | 1 | plain-case-supported | 2500 | published_value 2500 |
| Phase-out, box 1 of 2000, income 90000 | 1 | plain-case-supported | 1334 | published_value 1334 |
| Amount-only, box 1 of 1000, income 50000 | 1 | plain-case-supported | 1000 | published_value 1000 |
| Corrected back to the plain inputs | 1 | plain-case-supported | 2500 | published_value 2500 |
| Second statement with no inclusion, beside a plain statement | 1 and none | plain-case-supported and not-supported | no line 21; blocked `SLI_UNIVERSAL_COMPONENT_VIOLATION` | blocked, activeCodes that code |
| Two loans, each with its own enrollment `yes` | 1 and 1 | both plain-case-supported | 2500 | published_value 2500 |

Pins a person can follow on the plain case, from the statement publication:
the box finding, the inclusion finding, the support publication, and the
declared scope default. The support publication pins the loan-cost `yes`, the
re-keyed enrollment `yes`, the financing finding, and the same inclusion.
Both runners produced those pins.

Refused shapes at steps 1 and 2:

| Case | What published | Label |
| --- | --- | --- |
| Old yes only (a box and no new-path rows) | not-supported. The chain does not stay silent. | stand-in |
| Missing inclusion | not-supported | stand-in |
| Inclusion omitted from currency | not-supported | stand-in |
| No financing row | support 0, not-supported | stand-in |
| Inclusion cannot-tell stored as the unresolved fact type, not as an inclusion | not-supported. The chain does not read that fact. | stand-in |
| Two inclusions on one statement, each with support 1 | not-supported | stand-in |
| Two financing periods for one borrowing | support 0, not-supported | stand-in |
| Loan answer missing, or `no` | support 0, not-supported | stand-in |
| Enrollment answer missing, or `no` | support 0, not-supported | stand-in |
| Current box identity changed; the inclusion still names the previous statement | the current box is not-supported. The orphan inclusion still publishes support 1. | stand-in |
| Both old and new inputs present | the chain still publishes plain-case-supported. It does not read the old fact. | stand-in |
| Financing row still current with value `sli.financing.cannot-tell` | support 1, plain-case-supported. The stand-in counts the row and ignores the value. | stand-in |
| Schooling row omitted, financing still current | support 1, plain-case-supported. Steps 1 and 2 do not notice. | stand-in |

The both-input refusal and the stale-schooling refusal are not closed here.
The smallest both-input case is the chain above: a current old-fact `yes`
beside an otherwise plain link still publishes `plain-case-supported`.
The smallest stale-schooling case is the chain above: omitting the schooling
row leaves the statement `plain-case-supported`.

## Re-key

Enrollment is keyed by `borrowing`, same containment as the loan-cost answer.
The words of the question are unchanged. The grain is the loan.

Measured: two statements, two borrowings, one schooling period. An enrollment
`yes` on only the first borrowing publishes support 1 and 0. The statements
are `plain-case-supported` and `not-supported`. The worksheet blocks with
`SLI_UNIVERSAL_COMPONENT_VIOLATION` and publishes no line 21. The same return
with an enrollment `yes` on each borrowing publishes `plain-case-supported`
for both, and the worksheet publishes 2500. One schooling-scoped answer does
not cover both loans. Asking once per loan changes the deduction when two
loans paid for one schooling and the person answered once.

Schooling-keyed alternative, package validation only. Label: executed existing
engine. A financing subject may declare `subject_contains_joined` against an
enrollment keyed by period, institution, and programme (`ok`, no issues). An
inclusion subject may not: `RULE_RELATIONSHIP_NOT_CONTAINED`, subject keys
`borrowing`, `lender`, `statement`, `tax-year`, joined keys `institution`,
`period`, `programme`. This probe did not run that financing rule forward.
Carrying its mark onto the inclusion is not a declared containment.

## Not closed by the design chain

Evidence 6 measures mixed scope. The hand-built cannot-tell row in evidence 1
stays current and is counted as support. The recorder path below retracts
that row. Evidence 2 shows the design chain still does not notice a stale
schooling or a stale statement. Evidence 3 shows coverage once every current
box has a published row, and shows that dropping that row still deducts.
Evidence 4 shows the both-present refusal on a separate clone. The design
chain still publishes `plain-case-supported` when the old fact is also
present. Evidence 5 states the production operator from the stand-in runs.

## Evidence 6 — mixed scope through the real recorder

Command: `PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0d_probe.py evidence6`. Exit 0. Both runners agreed on every chain. No chain blocked.

Each scene starts from the durable recorder and is read back through a fresh ActLog. That recovery, the evidence responses, the current and historical counts, and `current_claim_applicability` are executed existing engine. The chain does not read the log. It reads a copy of the current relationship rows, with the recovered finding ids kept. Historical rows are not copied. The two qualification answers are disposable `yes` rows; the recorder does not store them. Supplying `yes` keeps a false support on the count, rather than on a missing answer. The scope marks are a disposable projection over the recovered log. They are not a production fact and not production code. Every chain conclusion is executed with the runtime stand-in operator. The scope-mark echo copies the projected statement mark with an existing rule and does not call the stand-in. The worksheet is the existing candidate worksheet with the old-fact collect swapped to the chain conclusion, so its dollar result is executed with the runtime stand-in operator. The box amounts are the recovered synthetic statement values `1250.0` and `1800.0`, not chain publications. Income is the harness figure `50000`. The presentation section is presentation only. Its explain sentence was absent from the section shape this probe reads, so that sentence is unverified.

Every scene includes an unrelated sibling statement (box `1800.0`, its own borrowing and schooling, both links affirmed) beside the primary statement (box `1250.0`). In the tables, the sibling is first and the primary is second.

Before the second answer or the withdrawal, two current links share the borrowing or the statement. The naive chain publishes no scope fact, so financing scope defaults to `complete`. The primary is `not-supported`. The sibling is `plain-case-supported`.

| Scene | Current financing / inclusion | Primary support | Primary conclusion |
| --- | --- | --- | --- |
| Financing cannot-tell, no, or withdrawal | 3 / 2 | 0 | not-supported |
| Inclusion cannot-tell, no, or withdrawal | 2 / 3 | 0 and 1 | not-supported |
| Financing or inclusion, second link never mentioned | 2 / 2 | 1 | plain-case-supported |

The inclusion scenes publish two supports on the primary statement before the answer. The second borrowing has an inclusion and no financing claim, because that submission left financing unanswered, so its support is 0. The first borrowing's support is 1. Statement link count is 2, so the statement is `not-supported`.

After the durable answer or withdrawal, fresh recovery leaves one current affirmative where there had been two. The naive chain then publishes support 1 and `plain-case-supported` for the primary. That is the failure a count of remaining affirmatives cannot see.

| Scene | After financing / inclusion / unresolved | Historical | Naive primary | Proposed primary support | Proposed primary conclusion | Proposed primary mark | Worksheet | Presentation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Financing cannot-tell | 2 / 2 / 0 | financing 1 | plain-case-supported | 0 | not-supported | unresolved-scope | no line 21, `SLI_UNIVERSAL_COMPONENT_VIOLATION` | blocked, that code |
| Inclusion cannot-tell | 2 / 2 / 1 | inclusion 1 | plain-case-supported | 1 | not-supported | unresolved-scope | no line 21, same code | blocked, that code |
| Financing no | 2 / 2 / 0 | financing 1 | plain-case-supported | 1 | plain-case-supported | closed-denial | 2500 | published value 2500 |
| Inclusion no | 2 / 2 / 0 | inclusion 1 | plain-case-supported | 1 | plain-case-supported | closed-denial | 2500 | published value 2500 |
| Financing withdrawal | 2 / 2 / 0 | financing 1 | plain-case-supported | 0 | not-supported | withdrawn-link | no line 21, same code | blocked, that code |
| Inclusion withdrawal | 2 / 2 / 0 | inclusion 1 | plain-case-supported | 1 | not-supported | withdrawn-link | no line 21, same code | blocked, that code |
| Financing never had a second schooling | 2 / 2 / 0 | none | plain-case-supported | 1 | plain-case-supported | complete | 2500 | published value 2500 |
| Inclusion never had a second borrowing | 2 / 2 / 0 | none | plain-case-supported | 1 | plain-case-supported | complete | 2500 | published value 2500 |

The sibling stays `plain-case-supported` with mark `complete` in every scene. It does not rescue the primary. When the primary is `not-supported`, the worksheet blocks and publishes no line 21.

Recovered pair status on the primary borrowing `demo.track14.borrowing.autumn`, after the answer:

- Financing cannot-tell. The second schooling pair is `cannot-tell`. The first schooling pair and the inclusion stay `affirmed`. Borrowing mark `unresolved-scope`. No current unresolved fact. The projection read the evidence response `cannot-tell`.
- Inclusion cannot-tell. The second borrowing's inclusion pair is `cannot-tell`. A current fact of type `demo.tax.2025.sli.statement-inclusion-unresolved` remains, value `sli.statement-inclusion.unresolved`, keyed to `demo.track0d.borrowing.second` and the primary statement. Financing of the first borrowing stays `complete`, so that inclusion's support stays 1. The statement mark is what blocks.
- Financing no. The second schooling pair is `no`. Borrowing and statement marks are `closed-denial`.
- Inclusion no. The second inclusion pair is `no`. The statement mark is `closed-denial`. Financing of the first borrowing stays `complete`.
- Financing withdrawal. The second schooling pair is `withdrawn`. The evidence list has the original `yes` and no successor response. Borrowing and statement marks are `withdrawn-link`.
- Inclusion withdrawal. The second inclusion pair is `withdrawn`. No successor response. The statement mark is `withdrawn-link`. Support on the remaining inclusion stays 1.
- Genuine absence. Only the affirmed sibling pair and the affirmed primary pair exist. Both marks are `complete`.

`current_claim_applicability` on the fresh acts returns `current` for the claims that remain. It does not name cannot-tell, no, or withdrawal.

Explicit no and genuine absence both publish worksheet 2500. The boxes are 1250.0 and 1800.0, and the candidate worksheet caps that sum at 2500. They share the dollar result because both are closed scope with one supporting link. They do not share a scope mark: no is `closed-denial`, absence is `complete`.

Inclusion cannot-tell and inclusion withdrawal keep support 1 on the remaining inclusion. Financing cannot-tell and financing withdrawal publish support 0, because the borrowing mark is not `complete` or `closed-denial`. The statement conclusion is still `not-supported` in all four, because the statement mark is not `complete` or `closed-denial`.

## Evidence 7 — what a rule can see

Command: `PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0d_probe.py evidence7`. Exit 0. This run leaves the sample unresolved vocabulary unadopted. The refusal and the recovered counts are executed existing engine. The naive conclusion below is executed with the runtime stand-in operator.

Inclusion cannot-tell refuses: `RelationshipRecordingRefused: unresolved inclusion diagnostic bundle is not adopted in this workspace`. No finding is written. With that bundle adopted, evidence 6 recorded a current fact `demo.tax.2025.sli.statement-inclusion-unresolved`, value `sli.statement-inclusion.unresolved`, keyed by the second borrowing and the primary statement. The derivation chain does not read that fact. The disposable projection did, and the statement then published `not-supported` with mark `unresolved-scope` while the remaining inclusion's support stayed 1.

Financing cannot-tell does not refuse when the bundle is absent. Fresh recovery shows current financing 2, current inclusion 2, unresolved 0, historical financing 1. The evidence response is `cannot-tell`. `current_claim_applicability` returns only `current`. There is no current unresolved fact. The naive chain publishes `plain-case-supported` for the primary. The same shape with the bundle adopted, in evidence 6, also left unresolved at 0. The only durable trace of financing cannot-tell is the evidence response plus the retracted finding.

Explicit no, measured in evidence 6, has the same hole. The response is `no`, the finding is historical, unresolved stays 0, and applicability stays `current`. Withdrawal leaves a historical finding and no successor response. Applicability does not list the retracted finding.

Production needs four current facts a subject rule can require, written by the recorder, and admitted for a real workspace rather than by adopting the sample bundle:

- Financing cannot-tell. A current unresolved fact keyed by the borrowing and the schooling identity. The probe executed that read by projecting the evidence response into a disposable scope row. Support became 0 and the statement became `not-supported` with `unresolved-scope`.
- Inclusion cannot-tell. The fact the recorder already writes, once that type is admitted without the sample bundle. The probe executed that read from the recovered current fact.
- Explicit no, for a financing pair and for an inclusion pair. A current negative claim, so the rule does not read evidence content. The probe fed `closed-denial` from the `no` response. Support stayed 1 and the statement stayed `plain-case-supported`, with that mark.
- Withdrawal. A current retracted-without-successor marker. Applicability does not provide one. The probe treated a finding that is not current, and that has no `no` or `cannot-tell` successor, as `withdrawn-link`.

The naive chain defaults a missing scope fact to `complete`. That default is why a retracted second link becomes `plain-case-supported`. A production rule must not use that default for a borrowing or a statement that has one of these facts. Genuine absence has none of them, and both the naive chain and the proposed chain left it `complete`.

## Evidence 8 — distinct consequences

The proposed chain in evidence 6 is the execution. Conclusion values are only `plain-case-supported` and `not-supported`. The distinct consequence is the pair of conclusion and scope mark. Labels are the same as evidence 6: the conclusion and the worksheet dollar are executed with the runtime stand-in operator, the mark echo is executed existing engine over a disposable projection, and the presentation section is presentation only.

| After recovery | Primary conclusion | Primary mark | Primary support | Worksheet |
| --- | --- | --- | --- | --- |
| Financing cannot-tell | not-supported | unresolved-scope | 0 | blocked, no line 21 |
| Inclusion cannot-tell | not-supported | unresolved-scope | 1 | blocked, no line 21 |
| Financing no | plain-case-supported | closed-denial | 1 | 2500 |
| Inclusion no | plain-case-supported | closed-denial | 1 | 2500 |
| Financing withdrawal | not-supported | withdrawn-link | 0 | blocked, no line 21 |
| Inclusion withdrawal | not-supported | withdrawn-link | 1 | blocked, no line 21 |
| Second schooling never mentioned | plain-case-supported | complete | 1 | 2500 |
| Second borrowing never mentioned | plain-case-supported | complete | 1 | 2500 |

Cannot-tell is `not-supported` plus `unresolved-scope` because an open second link must not be dropped, and the one remaining affirmative must not become the whole loan. The worksheet blocks. Financing and inclusion cannot-tell share that statement pair on purpose. They do not share support. Financing cannot-tell marks the borrowing `unresolved-scope`, so support is 0. Inclusion cannot-tell leaves the remaining inclusion's financing `complete`, so its support stays 1, and the statement mark is what blocks.

Explicit no is `plain-case-supported` plus `closed-denial`. A no closes that pair, and the remaining single affirmative is the whole support. Financing no and inclusion no share that pair. Both worksheets publish 2500.

Withdrawal is `not-supported` plus `withdrawn-link`. A retraction without a successor answer is not a no and not silence. The worksheet blocks. Financing and inclusion withdrawal share that statement pair. Support is 0 for the financing withdrawal and 1 for the inclusion withdrawal, for the same reason as cannot-tell: the borrowing mark gates support, and the statement mark gates the conclusion.

Genuine absence is `plain-case-supported` plus `complete`. Nothing was removed, and the single current link is the whole scope. The two absence scenes share that pair, and both worksheets publish 2500.

Explicit no and genuine absence deliberately share `plain-case-supported` and the worksheet value 2500. Both are closed scope with one supporting link, and the recovered boxes are `1250.0` and `1800.0`, which the candidate worksheet caps at 2500. They do not share a mark. No carries `closed-denial`. Absence carries `complete`.

The sibling statement is `plain-case-supported` with mark `complete` in every row. It does not change the primary pair.

Before the answer, cannot-tell, no, and withdrawal are not distinct. The second link is still affirmative, the count is 2, and the primary is `not-supported`. After recovery, the naive chain gives all three `plain-case-supported`. That shared result is the accident. The proposed marks separate them.

## Evidence 2 — stale target

Commands: `PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0d_probe.py evidence2`. Exit 0. Both runners agreed on every case.

The design chain does not notice. Label: executed with the runtime stand-in operator.

| Case | Support | Conclusion |
| --- | --- | --- |
| Schooling row absent, financing still current | 1 | plain-case-supported |
| Schooling finding present but not current | 1 | plain-case-supported |
| Statement finding present but not current | 1 | no statement conclusion |

When the statement is not current, it is not a subject, so the chain publishes no `not-supported` for it. The inclusion support still publishes 1. The stand-in count does not read schooling or the statement.

The smallest derivation check is a financing subject that requires the schooling fact, direction `subject_contains_joined`, value a ref of the schooling fact. The same shape on the inclusion requires the box 1 fact. Label: executed existing engine. No stand-in node.

| Case | Result |
| --- | --- |
| Schooling row current | publishes `demo schooling` |
| Schooling row absent | `DEPENDENCY_ABSENT`, missing `tax.us.2025.sli.schooling-situation`, subject the financing fact |
| Schooling finding not current | same `DEPENDENCY_ABSENT` |
| Statement row current | publishes `3000` |
| Statement row absent | `DEPENDENCY_ABSENT`, missing `tax.us.2025.f1098e.box1-student-loan-interest`, subject the inclusion fact |
| Statement finding not current | same `DEPENDENCY_ABSENT` |

`current_claim_applicability` notices the same gap on a fresh ActLog. With both sources current, every row is `current`. Removing the schooling source act from the recovered act list makes the financing row `unresolved-applicability` and leaves the inclusion `current`. Removing the statement source act makes the inclusion row `unresolved-applicability` and leaves the financing `current`. One act was removed in each cut. That removal is done in the probe, not by the recorder. The derivation path does not call this check. Label: executed existing engine.

The stale-target row is not closed by the design chain. The two checks above are what notice it.

## Evidence 3 — coverage

Command: the same probe with `evidence3`. Exit 0. Both runners agreed.

New path. Two boxes of `3000`, income `50000`. One box has the plain link chain. The other box has no inclusion. The chain publishes `plain-case-supported` and `not-supported`. Label for the conclusions and the worksheet dollar: executed with the runtime stand-in operator. Presentation is presentation only.

| Worksheet inputs | Line 21 | Presentation |
| --- | --- | --- |
| Both conclusions | no line 21, `SLI_UNIVERSAL_COMPONENT_VIOLATION`, missing empty | blocked, that code |
| The `not-supported` publication omitted, both box amounts kept | 2500 | published value 2500 |
| The one supported statement alone | 2500 | published value 2500 |

The collect blocks only when a published row is not `plain-case-supported`. Dropping the `not-supported` row fail-opens to the capped deduction. The publisher is what closes the row, because the chain emitted a conclusion for the box that had no inclusion.

Old path. For each of the five answers, a real `link_count` of that answer, then a mapper that publishes `missing` when the count is 0 and `answered` otherwise. Two statements, one answer present. Label: executed existing engine. The worksheet is the existing candidate with that answer's collect swapped to expect `answered`. One harness box of `3000`, income `50000`. The same three results on every answer: `no-related-person-interest`, `no-non-qualified-loan-component`, `no-qualified-employer-plan-interest`, `no-employer-educational-assistance-interest`, `no-qtp-earnings-used`.

| Inputs | Status values | Line 21 | Presentation |
| --- | --- | --- | --- |
| Both published status rows | `answered`, `missing` | no line 21, `SLI_UNIVERSAL_COMPONENT_VIOLATION`, missing empty | blocked, that code |
| The `missing` row omitted | `answered` only | 2500 | published value 2500 |
| One statement, its answer present | `answered` | 2500 | published value 2500 |

The blocked code is the worksheet's universal-component code. `blocked.missing` is empty, and the presentation does not display the word `missing`. The Track 0b fail-open clone blocks when the `missing` row is published. Omitting that row still publishes 2500. One answered statement still deducts.

## Evidence 4 — both inputs present

Command: the same probe with `evidence4`. Exit 0.

The published line 2b rule declares `selection.mode` `exclusive_presence`, `selection.conflict` `refuse`, and `selection.refusal` code `DEPENDENCY_INVALID` with missing `legacy-and-derived-nominee-both-present`. That is the declared precedent. It is not a run.

The design chain, with the old fact `yes` on the same statement as the plain link rows, still publishes `plain-case-supported`. Both runners agreed. Label: executed with the runtime stand-in operator. The chain does not read the old fact. The new-path worksheet, fed only that chain's conclusion, box `3000`, income `50000`, publishes 2500.

The both-present clone replaces the candidate worksheet's value with one `collect_categorical_all_equal` whose expected category is `clear`. The fact type enum is only `clear`. The source value is `old-and-new-sli-inputs-both-present`. Label: executed existing engine. There is no stand-in node in this clone. It blocks. No line 21 is published.

| Surface | Result |
| --- | --- |
| Blocked code | `DEPENDENCY_INVALID` |
| Blocked missing | `old-and-new-sli-inputs-both-present` |
| Disposition | `blocked`, code `DEPENDENCY_INVALID`, missing the same token |
| Presentation | presentation only: `blocked`, active codes `DEPENDENCY_INVALID`, value absent |

The token does not appear in the presentation section. The blocked explain text is the generic line 21 sentence: "Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed." A person sees `DEPENDENCY_INVALID` and that sentence, not the token. The missing list on the disposition is where the token is named.

This clone is not a presence test inside the deduction. An empty collect blocks, so one expression cannot mean both "the old rows are present" and "the old rows are absent." The new-path rule remains the one that publishes 2500. The production worksheet was not edited.

## Evidence 5 — what the production count must do

Command: the same probe with `evidence5`. Exit 0. Both runners agreed on every chain. Label for every row: executed with the runtime stand-in operator. The direct rows call the stand-in function. The chain rows run it inside the support rule. It is not production code and `shared_key_count` is not a schema token.

Direct calls, subject borrowing `demo-loan` unless noted:

| Case | Value | Pins | Blocked missing |
| --- | --- | --- | --- |
| Two financing rows, same affirmed value, two periods | 2 | both financing finding ids | none |
| One financing row | 1 | that financing finding id | none |
| No financing row | 0 | none | none |
| One row whose keys are null, plus one good row | none | the null-key finding id | that finding id |
| Subject keys null | none | none | `link-coverage-keys-unavailable` |
| Subject map has no borrowing | none | none | `link-coverage-keys-unavailable` |

The null-key row names its finding id. The subject failures name `link-coverage-keys-unavailable` and do not name the financing finding. The exception text is `DEPENDENCY_INVALID` followed by that missing entry.

Chain, same operator inside the support rule:

| Case | Support | Pins on the support publication | Conclusion |
| --- | --- | --- | --- |
| One period | 1 | the loan answer, the enrollment answer, that financing, the inclusion, and the declared scope default | plain-case-supported |
| Two periods, equal affirmed value | 0 | both financing findings and the inclusion | not-supported |
| No financing row | 0 | the inclusion only | not-supported |
| Financing finding not current | 0 | the inclusion only | not-supported |
| Two statements, two borrowings | 1 and 1 | each publication pins its own financing, not the other | both plain-case-supported |
| One financing row with no borrowing key, two inclusions | none published | both inclusions block | no conclusion |

The row with no borrowing key blocks every inclusion: `DEPENDENCY_INVALID`, missing `demo.finding.financing.no-borrowing`. It is not dropped and it is not published as 1. Each statement then blocks `DEPENDENCY_INVALID` missing its inclusion finding, because the support publication is absent.

An inclusion row that omits borrowing does not reach the subject-key failure inside the chain. The support rule blocks first with `DEPENDENCY_INVALID` missing `demo.tax.track0d.loan-paid-only-school-costs`, because that answer is not in the join. The direct call is what shows the subject-key failure.

Production shared-key count has to do these things:

- Count current financing rows that share the subject's borrowing. Equal values stay separate rows. Two periods count as 2 and pin both financing findings.
- One matching row returns 1 and pins that financing.
- No current match returns 0 and adds no financing pin. A financing finding that is not current is this case.
- A financing row with no borrowing key, or with null keys, blocks every inclusion, names that finding id in missing, and must not publish 1.
- A subject with null keys, or a subject map without borrowing, blocks with missing `link-coverage-keys-unavailable` and does not name a financing finding.
- The operator does not read the financing value, the schooling, or evidence text. A current row whose value is cannot-tell still counts. Evidence 6 is why a count of remaining affirmatives is not enough: the recorder retracts the cannot-tell row, and the scope mark has to keep that loan from becoming supported.
