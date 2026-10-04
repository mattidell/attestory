# Track 0a — route map from recorded relationships to the deduction

Read on the milestone branch at the start of Track 0a.
Investigation only. No rule, package, schema, or test was changed.
Claims below were checked against the named files. Anything not checked is marked unverified.

Track 0e rewrote sections 2, 3, 8, and 9 to the owner's decisions of
2026-10-01 and to the basis in
[track0e-conclusion-basis.md](track0e-conclusion-basis.md). Sections 1 and
4–7 are the original investigation, except the category-name corrections
marked in sections 6 and 7.

The five eligibility facts are the per-statement yes/no witnesses in
`packages/content/tax/2025/f1098e.bundle.json` (`tax.us.2025.f1098e.vocabulary` v1).
Each is keyed by lender, statement, and tax year 2025. The only values are `yes`
and `no`. There is no default. `yes` means the named excluded amount is not in
this statement's box 1. `no` means it is. They are not boolean true/false.

| Fact | What the person is asserting |
| --- | --- |
| `tax.us.2025.f1098e.no-related-person-interest` | Box 1 does not include interest on a loan from a related person. |
| `tax.us.2025.f1098e.no-qualified-employer-plan-interest` | Box 1 does not include interest on a loan from a qualified employer plan. |
| `tax.us.2025.f1098e.no-non-qualified-loan-component` | Box 1 does not include interest on a loan that fails the qualified-student-loan test. The fact's own title says this one answer stands in for student status, qualified education expenses, and a reasonable period of time. |
| `tax.us.2025.f1098e.no-employer-educational-assistance-interest` | Box 1 does not include interest an employer paid under an educational assistance program. |
| `tax.us.2025.f1098e.no-qtp-earnings-used` | Earnings from a qualified tuition program were not used to pay this statement's interest. |

The titles cite Pub. 970. This report did not re-read Pub. 970. The legal gloss
above is the bundle's, not an independent reading of the publication.

## 1. Worksheet today

`tax.us.2025.rule.sli-worksheet-line1-subtotal` v1
(`packages/content/tax/2025/rule.sli-worksheet-line1-subtotal.json`) does not
read any of the five. It publishes
`tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`, the raw sum of
`tax.us.2025.f1098e.box1-student-loan-interest` over family
`tax.us.2025.f1098e.1`. Its guard is unconditionally true.

The family does not use the five either.
`packages/content/tax/2025/family.f1098e-1.json` says its closure claim covers
box 1 and the box 2 companion only, and says nothing about eligibility.
`packages/content/tax/2025/closure-mapping.f1098e.1.json` admits that same
subtotal from `tax.us.2025.f1098e.1.source-closure`. The bundle only defines
the five fact types. It does not compute.

`tax.us.2025.rule.sli-worksheet` v1
(`packages/content/tax/2025/rule.sli-worksheet.json`) is the only rule that
reads the five. It publishes `tax.us.2025.schedule1.line21-sli-deduction`.
Package `package.core-calculations.v38` adopts this rule at v1. The five are
declared input pins. They are not in the rule's `requires` list and they are
not in the `conditional_dependency_set` on its guard. The guard, when box 1
has at least one row, requires seventeen other facts (the three return-level
scope facts, the twelve Schedule 1 absence facts, not-claimed-as-dependent,
and legally-obligated). The five are read later, inside the amount, by
`collect_categorical_all_equal`, each compared to `yes`.

What the worksheet does with them:

- Closed family with no box 1 rows: line 21 is the literal `0`. The five are
  not read. The cap and phase-out are not applied.
- Married filing separately, and the family is not empty: block
  `SLI_MFS_INELIGIBLE`. Line 21 is not published. This is tested in
  `tests/test_sli_worksheet_line21_track3.py`.
- Any of the three return-level scope facts is not `yes`, or any current row
  of any of the five is not `yes`: block
  `SLI_UNIVERSAL_COMPONENT_VIOLATION`. Line 21 is not published. A `no` does
  not become a legal zero. Tested for
  `tax.us.2025.f1098e.no-related-person-interest` = `no` in that same test,
  in `tests/test_schedule1_line26_track4.py`, and on the saved path in
  `tests/test_f1098e_student_loan_interest_agi_track6.py`. The other four use
  the same operator and the same branch. A separate live run for each of
  those four was not executed here.
- Otherwise the twelve Schedule 1 absence facts and the two legal-zero facts
  are applied. Those are not the five. A `no` on not-claimed-as-dependent or
  legally-obligated publishes a computed `0`. A `no` on a Schedule 1 absence
  blocks `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`.
- If none of those gates fire, the existing cap and MAGI phase-out run on the
  line 1 subtotal. This milestone does not change that arithmetic.

Absent, `no`, and withdrawn:

- `no` is the value above. The whole deduction is blocked, not zeroed.
- Absent means no current finding of that fact type at all.
  `collect_categorical_all_equal` in `packages/derivation/evaluator.py` then
  raises `DEPENDENCY_ABSENT` naming the fact type. The unit test is
  `tests/derivation/test_collect_categorical_all_equal.py`. The worksheet
  rule's static `blocked` list does not name the five; the absence is raised
  while the amount is evaluated. A full worksheet run with one of the five
  omitted was not executed here.
- The operator does not match rows to box 1 statements. If one statement has
  `yes` and another statement has no row of that fact, the rows that exist
  are all `yes`, and the gate passes. The missing statement's interest is
  still in the line 1 sum. Verified by reading the operator and the rule
  tree, not by a live two-statement run.
- Withdrawn: `packages/derivation/marshal.py` feeds the operator only from
  current findings. `packages/kernel/currency.py` drops a finding that was
  retracted or whose fact was member-withdrawn. If that leaves no current
  row of the fact type, the result is the same `DEPENDENCY_ABSENT` as
  absence. If another statement's `yes` remains, the gate still passes, for
  the same reason as a missing row. No product command that withdraws these
  five facts was found. That last sentence is the limit of the search, not a
  proof that no caller exists outside the files read.

`tax.us.2025.rule.schedule1-line26` v1 reads line 21 by reference and publishes
`tax.us.2025.schedule1.line26-total-adjustments`. When line 21 is blocked,
line 26 is `DEPENDENCY_ABSENT` and names line 21
(`tests/test_schedule1_line26_track4.py`). A published `0` is a real number
and can flow through.

Consumers of the line 21 symbol in `package.core-calculations.v38`, by
searching that package's members:

- Producer, not a consumer: `tax.us.2025.rule.sli-worksheet` v1.
- `tax.us.2025.rule.schedule1-line26` v1 reads it as the amount of line 26.
- `tax.us.2025.rule.attachment.schedule-1` v2 names it in
  `requirement.subtotals`, beside the unemployment subtotal, as a reason
  Schedule 1 can be required. The line 21 itemization ties out to the raw
  box 1 subtotal, not to the deduction. What the attachment does when line
  21 is blocked was not re-run.
- `tax.us.2025.schedule1.line-21` v1 binds the symbol for the form. Its
  blocked explanation does not name `SLI_UNIVERSAL_COMPONENT_VIOLATION`.
  The presentation test
  `tests/test_f1098e_student_loan_interest_track8_presentation.py` still
  shows that code on the line. The stored explain text is the generic
  blocked sentence.

Downstream of line 26, still in v38:

- `tax.us.2025.rule.form1040-line10` v1 reads line 26 and publishes
  `tax.us.2025.income.line10-adjustments`. Form field
  `tax.us.2025.form1040.line-10` binds that symbol.
- `tax.us.2025.rule.form1040-line11` v2 reads line 26 directly, not line 10,
  and publishes `tax.us.2025.income.agi`. Form fields
  `tax.us.2025.form1040.line-11a` and `tax.us.2025.form1040.line-11b` both
  bind AGI.
- `tax.us.2025.rule.form1040-line15` v2 reads AGI and publishes
  `tax.us.2025.income.taxable-income`. Form field
  `tax.us.2025.form1040.line-15` binds it.
- `tax.us.2025.rule.form1040-line16` v5 reads taxable income.

The line 1 subtotal rule mentions line 21 only in its notes. It does not
read it. Readers of line 16 beyond that one rule were not enumerated.

## 2. Which fact the two questions replace

Superseded: the earlier text of this section recommended replacing the
non-qualified-loan question and adding no question about the student, the
expenses, or sole use. The owner decided otherwise on 2026-10-01.

The fact the new path replaces is still only
`tax.us.2025.f1098e.no-non-qualified-loan-component`. The other four
statement answers stay asked yes/no facts. The financing link and the
inclusion link do not replace that fact by themselves. Two ordinary answers
are asked with the links.

| Question | Key | Values |
| --- | --- | --- |
| The identified borrowing paid only for school costs. | `tax.us.2025.sli.loan-paid-only-school-costs`, key `borrowing` only, entity kind `tax.us.student-loan-borrowing-reference` | `yes`, `no`, `cannot-tell`. Only `yes` supports. No default. |
| The student was enrolled at least half-time in a degree or certificate program during that schooling. | `tax.us.2025.sli.enrolled-at-least-half-time`, keys `period`, `institution`, and `programme`, the same entity kinds as the schooling situation | `yes`, `no`, `cannot-tell`. Only `yes` supports. No default. |

Track 0b recorded these keys. This section does not create the fact types.

On the new path the person is no longer asked whether box 1 has no
non-qualified-loan component. They are still asked the other four statement
questions and the return-level questions the worksheet already asks. The two
links remain the relationship questions the previous milestone records.

The two answers, the two links, and the two counts do not establish every
condition of a qualified education loan. The authority and the full
classification are in
[track0e-conclusion-basis.md](track0e-conclusion-basis.md). In short, the
design supports the replaced fact as follows.

- Said: the school-costs answer, the half-time answer, the financing
  affirmation, and the inclusion affirmation.
- Derived: one current affirmed financing for that borrowing, and one current
  affirmed inclusion on that statement.
- Assumed in the person's favor, with no answer: a reasonable period; school
  costs standing in for qualified higher education expenses, including the
  required reductions; whose education, as of the time the loan was incurred;
  that the named borrowing is indebtedness the taxpayer incurred; and that
  box 1 holds no loan the person did not record.
- Left with the person, and not established: that the institution is an
  eligible educational institution, that the enrollment meets the
  institution's half-time standard, that the program leads to a recognized
  credential, and that cost of attendance is the institution's figure.
- Still asked elsewhere: related person, qualified employer plan,
  employer-paid interest, qualified-tuition-program earnings, and the legal
  obligation to pay the interest.
- Unsupported as a favorable path: a loan used only to refinance a qualified
  education loan. The plain case does not assume a refinance qualifies.

The favorable result is not named `qualified`. Section 3 is the case.
Section 8 is the value `plain-case-supported`.

## 3. The plain case

Superseded: the earlier text of this section stopped at one borrowing, one
schooling, and one statement, and left student status, qualified expenses,
and sole use unasked. The owner added the two ordinary questions and kept
the whole box 1.

The plain case is one borrowing, one schooling situation, and one 2025 Form
1098-E. Both links are currently affirmed. Both ordinary answers are `yes`.
Each count is 1. The deduction uses the whole box 1. A loan inside that
figure that the person never recorded is not detected. That limit is an
assumption stated on the result. It is not a finding that no such loan
exists.

| Condition | Where it stands |
| --- | --- |
| One current borrowing, introduced by the person under an opaque id. | Recorded (`tax.us.student-loan-borrowing-reference`). The id is not a finding that the taxpayer incurred the indebtedness. That part is an assumption on the result. |
| Exactly one current financing claim, value `sli.financing.affirmed`, pointing at one schooling situation. | Recorded when the person answers yes. The count of one is derived. |
| That schooling is one period, one institution, and one programme. | Recorded as `tax.us.2025.sli.schooling-situation`. The period key is an identifier. It is not a judgment that the period was reasonable. |
| The borrowing paid only for school costs. | `loan-paid-only-school-costs` is `yes`. This is the person's use answer. It is not a finding that the costs were qualified higher education expenses. |
| The student was enrolled at least half-time in a degree or certificate program during that schooling. | `enrolled-at-least-half-time` is `yes`. This is the person's enrollment answer. It does not establish the institution's half-time standard or that the credential is recognized. |
| Reasonable period, whose education, qualified expenses after the required reductions, and that the taxpayer incurred this debt. | Assumed in the person's favor. No question asks them. The result says so. |
| Eligible institution, the institution's half-time standard, a recognized credential, and the institution's cost of attendance. | The person's responsibility. Not established. Not a block by themselves. |
| One current box 1 for 2025 and exactly one current affirmed inclusion of that borrowing. The whole box 1 is assigned to it. | The inclusion is recorded. The count of one is derived. Assigning the unrecorded remainder of box 1 is the owner's whole-box assumption. An unknown interest portion stays as the recorder stores it and does not undo the link. |
| The other four eligibility facts are `yes`. Filing status is not married filing separately. The legal-obligation and not-claimed-as-dependent answers are `yes`. The Schedule 1 absence facts are `yes`. The family is closed. | Still asked, or already required by the worksheet. |
| The old non-qualified-loan answer is absent on every statement. | Exclusive regimes. If that old answer is current anywhere, and any inclusion or unresolved inclusion exists anywhere, the return blocks. |

A second period, a second borrowing, or a second statement is outside this
case. The deduction blocks. That refuses a mixed-period treatment rather than
deciding one. A refinance is outside the result this case publishes.

The favorable value is `plain-case-supported` on
`tax.us.2025.sli.statement-loan-support`. What that value asserts, and the
four groups its stated basis carries, are in
[track0e-conclusion-basis.md](track0e-conclusion-basis.md), section 3.

## 4. Refused cases

There is no screen copy for these yet. The sentences below are the reasons
the deduction should carry. None of them is a published zero. A missing
answer is not the old fact's `no`, and it is not the number 0. Line 21
stays unpublished, so line 26 stays `DEPENDENCY_ABSENT` as it does today
when line 21 is blocked.

A return with no Form 1098-E at all is not one of these cases. The worksheet
already publishes 0 for a closed-empty family without reading eligibility.

| Case | What is true | Reason to show |
| --- | --- | --- |
| Missing link | No current affirmed financing for the borrowing, or no current affirmed inclusion of that borrowing on the statement. This includes `unanswered`. It also includes a saved `no`: `packages/tax/sli_relationship_recording.py` stores `no` only in the answer evidence and does not create a claim finding. | "We don't have a recorded connection between this interest statement, one loan, and one schooling, so the student-loan deduction is blocked. Leaving this blank is not a no." |
| Cannot tell, statement | A current `demo.tax.2025.sli.statement-inclusion-unresolved` row for any borrowing on this statement. The recorder writes that row only when the diagnostic fact type is adopted. | "You couldn't tell whether this statement includes interest on this loan. The deduction stays blocked until you can." |
| Cannot tell, financing | The person answered `cannot-tell` on the financing. No unresolved fact type exists for financing, even in the diagnostic vocabulary. A rule cannot see it. It looks like a missing financing. | Until a production fact exists, use the missing-link sentence. Do not invent "you said you couldn't tell" from evidence the rule cannot read. |
| Withdrawn link | `withdraw_relationship_claim_durably`, or the retraction inside `answer_relationship_claim_durably`, has ended the claim and nothing current replaces it. | "That connection was withdrawn, so the deduction is blocked." |
| Corrected link outside the plain case | A reviewed correction removes the inclusion, points it at a different borrowing, or points the financing at a different schooling, and section 3 no longer holds. A correction that still meets section 3 is the plain case again, on the new current findings. An amount-only correction that keeps the same links is also the plain case; the deduction uses the new box 1. | "The corrected answer no longer describes one loan, one schooling, and one statement, so the deduction is blocked." |
| Statement changed off the checked path | A direct box 1 write leaves an old inclusion current. The Track 18 report and the capability handoff both say a direct source write can do this. The reviewed route is `apply_statement_correction_review`. This report did not re-run that bypass. | "This statement was changed without the checked correction, so the old loan link can't be used. The deduction is blocked." |
| Statement covers another loan | A second current affirmed inclusion on the same statement, or a current unresolved inclusion for another borrowing on it. A `no` about some other borrowing is not this case: it creates no finding, and it means that other borrowing is not on the statement. A loan the person never mentioned is invisible. Do not claim it is detected. | "This statement includes interest from more than one loan, or from a loan you couldn't confirm. We don't split one statement's interest, so the deduction is blocked." |
| More than one schooling | Two current financing claims for the same borrowing. That is two periods or two programmes. This is not a choice of mixed-period treatment. | "This loan is tied to more than one schooling period. This version doesn't decide what that does to the interest, so the deduction is blocked." |
| Stale target | The link finding is still current, but the schooling or the box 1 it names is not. `current_claim_applicability` returns `unresolved-applicability` in that case. It is a function the consumer must call. It does not block the engine by itself. | "The schooling or the statement this link points at is no longer the current record, so the deduction is blocked." |
| Another statement is outside the case | Any other box 1 on the return is not the plain case. The worksheet publishes one line 21 for the return. | "Another interest statement isn't in the one-loan case we can support, so the deduction is blocked rather than guessed." |

Unknown interest portion is not a refusal. The recorder accepts only
`unknown` or `unanswered` for that field, and the capability handoff says
an unknown portion does not undo the link. The other four eligibility
facts, married filing separately, the dependent and legal-obligation
answers, and the Schedule 1 absence facts keep the worksheet behavior in
section 1.

## 5. Relationship records available

Production fact types are the three in
`packages/content/tax/2025/sli-relationship-source.bundle.json`. That bundle
is not a member of `package.core-calculations.v38`.

| Fact | Keys | Only value | What it is |
| --- | --- | --- | --- |
| `tax.us.2025.sli.schooling-situation` | period, institution, programme | any non-empty string | The person's description of one schooling situation. The description does not define identity. |
| `tax.us.2025.sli.financing-relationship` | borrowing, period, institution, programme | `sli.financing.affirmed` | This borrowing financed that schooling situation. |
| `tax.us.2025.sli.statement-inclusion-relationship` | lender, statement, tax-year (`2025`), borrowing | `sli.statement-inclusion.affirmed` | This statement includes interest on this borrowing. |

`packages/tax/sli_relationship_recording.py` is the production recorder. The
standing rules it actually implements:

- Only `yes` creates a claim finding. `no`, `cannot-tell`, and `unanswered`
  are stored on the evidence content and do not become claim findings.
- A later `no` or `cannot-tell` on a current claim retracts that finding
  before the new answer is saved. The old affirmation stays in history and
  is not current.
- `cannot-tell` on an inclusion, and only on an inclusion, then admits
  `demo.tax.2025.sli.statement-inclusion-unresolved` with the same keys as
  the inclusion and the value `sli.statement-inclusion.unresolved`. That
  fact type is diagnostic. The recorder refuses to write it unless the
  workspace has adopted the diagnostic bundle.
- `current_claim_applicability` reports `current` when the schooling or the
  box 1 named by the claim is still a current finding, and
  `unresolved-applicability` otherwise. Callers have to read that list.
  Nothing in the derivation runner calls it.
- A withdrawn claim is a finding retraction. Currency then omits it.
  History remains.

The neutral consumer is the diagnostic package
`demo.tax.2025.package.sli-relationship-source-diagnostic` v4, in
`packages/sample_data/student_loan_relationship_source/package.sli-relationship-source-diagnostic.v4.json`.
Release `demo.release.sli-relationship-source.2025` v36 points at that
package's registry. The package admits the production relationship bundle,
the Form 1098-E bundle, and two sample bundles. Its rules are
`rule-artifact.v12`:

- `demo.rule.tax.2025.sli.guarded-financing-observation` v1. Subject is the
  financing claim. Joined is the schooling situation. Direction
  `subject_contains_joined`. It publishes
  `demo.tax.2025.sli.financing-observation` = `sli.financing.observed` when
  the claim is affirmed and the schooling row is readable. Otherwise it
  blocks. Its note says it is not a tax conclusion.
- `demo.rule.tax.2025.sli.guarded-statement-inclusion-observation` v1.
  Subject is the inclusion claim. Joined is box 1. Same direction. It
  publishes `demo.tax.2025.sli.statement-inclusion-observation` =
  `sli.statement-inclusion.observed` the same way.
- `demo.rule.tax.2025.sli.statement-inclusion-unresolved-observation` v1.
  Subject is the unresolved status. Joined is box 1. It publishes
  `demo.tax.2025.sli.statement-inclusion-unresolved-observation` =
  `sli.statement-inclusion.unresolved-observed`.

The observation fact types and the unresolved fact types live in
`packages/sample_data/student_loan_relationship_source/`. They are sample
vocabulary (`demo.tax.2025...`), not production content. The unguarded
observation rules in that folder are not entry points of package v4.

What a later tax rule may rely on is narrower than the diagnostic output.
It may rely on a current affirmed claim whose target is still current, and
on a current unresolved inclusion row when that diagnostic fact is adopted.
It may not treat a diagnostic observation as a qualified-loan conclusion.
The observations were not re-executed in this investigation. The shapes
above are the rule files.

## 6. Rule shape

Proposed rule, not an existing file:
`tax.us.2025.rule.sli-statement-loan-support`.
Track 0e correction: the earlier id was
`tax.us.2025.rule.sli-qualified-loan-conclusion`.

- Subject: one Form 1098-E box 1 row,
  `tax.us.2025.f1098e.box1-student-loan-interest` v1. The conclusion is per
  statement, which is the grain of the fact being replaced.
- Joined: `tax.us.2025.sli.statement-inclusion-relationship` v1.
- Direction: `joined_contains_subject`. Box 1's key names (lender,
  statement, tax-year) are contained in the inclusion's key names. That is
  the containment check in `packages/derivation/package_validation.py`.
- Operator: `link_count` once, in the value, never in the guard. Validation
  requires that shape, and it requires the counted type to be the joined
  type under `joined_contains_subject`. The operator returns the number of
  joined rows, and zero is a number, not a block
  (`packages/derivation/evaluator.py`).
- Output symbol: `tax.us.2025.sli.statement-loan-support`.
  Plain case: category `plain-case-supported`. Every other statement that
  has a box 1 row: category `not-supported`. Not the old `yes`/`no`. A `no`
  would mean the excluded class is present, which is the wrong reason for a
  missing or uncertain link. Track 0e correction: the earlier text of this
  bullet named the symbol `qualified-loan-for-statement` and the plain-case
  category `qualified`. That name claims a qualified education loan. The
  basis does not support the claim, so the value is `plain-case-supported`.
- The rule publishes a row for every box 1 subject. It does not go
  inapplicable and it does not block instead of publishing. Section 1
  showed that `collect_categorical_all_equal` passes when every row that
  happens to exist is `yes`. A missing conclusion row would let some other
  statement's `plain-case-supported` hide this statement's interest inside
  the line 1 sum. The worksheet gate has to require one conclusion row per
  box 1 row, every one of them `plain-case-supported`, before it runs the
  unchanged arithmetic. Anything else blocks line 21. Track 0e correction:
  the earlier text of this bullet required every row to be `qualified`.
- Pins: the box 1 finding; every inclusion finding `link_count` reads
  (`packages/derivation/subject_dispatch.py` adds those finding ids as
  input pins); the one financing finding; the schooling finding; the
  loan-cost answer for that borrowing; and the enrollment answer for that
  schooling. Track 0e correction: the earlier text stopped at the links and
  the schooling and called those pins the whole support a person can trace.
  The two ordinary answers are inputs too. The assumptions and the
  responsibilities are not pins. The result states them, because the rule
  never read them as findings.
- Authority: cite `tax.us.2025.citation.form1040.sli-worksheet`, the
  citation the worksheet rule already names. The citation text was not
  opened.

The inclusion count can be written with the operators we have. The
financing count cannot.

Financing's keys are borrowing, period, institution, and programme.
Inclusion's keys are lender, statement, tax-year, and borrowing. Neither
set contains the other, so financing cannot be the declared joined type.
The validator calls that `RULE_RELATIONSHIP_NOT_CONTAINED`. A statement
shares no key name with a financing row, so `_scope` joins nothing.

An inclusion subject would share the name `borrowing`. `_scope` would
match on that single name. ADR 0076 does not declare that pair: one shared
name is not containment. A required reference to the matched rows then
uses `_one_source`. Every financing value is the same category,
`sli.financing.affirmed`, so two rows agree and one is kept. Two periods
look like one period. Track 0e correction: the next paragraphs used the
category `qualified` for that false favorable result. The category is now
`plain-case-supported`. The failing case is unchanged.

ADR 0075 `link_coverage` is the wrong tool. It sums a numeric reduction
whose entire key map equals the link. These claims are categories. Box 1's
keys are not the inclusion's keys, so the box 1 amount would be an orphan
reduction and the operator would block. `count` only counts a closed
source family. These relationships are not one.

Smallest missing capability: a fail-closed count of rows that share one
named key, `borrowing`, with the statement's single inclusion, where two
rows with the same category still count as two rows.

Failing case, all synthetic: statement `demo-stmt` from lender
`demo-lender` for 2025, box 1 = 1000. Borrowing `demo-loan`. One affirmed
inclusion of `demo-loan` on that statement. Two affirmed financings of
`demo-loan`: schooling period `demo-2022` and schooling period `demo-2023`,
same institution and programme. The plain case must refuse this. A rule
that can only read the financing category sees one affirmed value and
would call the statement `plain-case-supported`. No current operator counts
the two financing rows from the statement.

Until that count exists, the rule above must not be adopted. Publishing
`plain-case-supported` without it would accept the failing case. This is an
operator gap, not a reading of governance text, and it does not require choosing
what several periods do to the interest. The answer remains "block."

The new categories need a new fact type. The old fact only allows `yes`
and `no`, and `no` already means the excluded class is present. Adding
that fact type is a later track. It has to follow the schema publication
rules. This report does not add it. The same is true of a production
successor to `demo.tax.2025.sli.statement-inclusion-unresolved`, which a
core package cannot read while it stays a sample fact. Financing has no
unresolved fact at all.

## 7. Old and new inputs together

Three ways a workspace can be arranged, and one recommendation.

**Old fact only.** The worksheet keeps reading
`tax.us.2025.f1098e.no-non-qualified-loan-component` exactly as section 1.
Relationships are ignored because there are none on the statement. Existing
results stay. This option alone does not finish the milestone.

**New conclusion only.** The worksheet stops reading the old fact. A
workspace that still has only the old `yes` has no conclusion row. Line 21
blocks instead of deducting. That is a stated refusal, not a different
number, but it changes every current synthetic deduction. The bounded
class the package already demonstrates would stop deducting.

**Both, with one regime winning by default.** If the new links are present,
ignore the old fact. If they are absent, use the old fact. Dangerous in
two directions. A stray inclusion on a statement that already has the old
`yes` would switch that statement onto the new path and could turn a
working deduction into a block, or, once the new path publishes
`plain-case-supported`, could keep the deduction for a different reason
without saying the old answer was set aside. If the old `yes` always wins
while it is present, correcting a link does not change the deduction, which
breaks the milestone's own done-when sentence. Track 0e correction: this
paragraph previously named the new path's value `qualified`.

**Recommendation: exclusive regimes. Both present blocks.** Do not compare
the answers, and do not let agreement pick a winner.

- No inclusion and no unresolved inclusion on any statement: old path, for
  the whole return, including a `no` and including a missing old fact.
- Every statement is on the new path (a conclusion row, and no current old
  fact on any statement): the worksheet reads the new conclusion and not
  the old fact.
- Any old-fact row for a statement, together with any inclusion or
  unresolved inclusion on any statement: block the return. Proposed reason:
  "This return has both the old qualification answer and a loan or
  statement link. Remove one of them. We will not choose between them."
  Proposed disposition: line 21 unpublished. Not
  `SLI_UNIVERSAL_COMPONENT_VIOLATION`, and not 0. The code is for the build
  to name. It does not exist today.

A financing that is not on a statement does not, by itself, flip the
return. The old path is about the statement fact. The new path starts when
an inclusion or an unresolved inclusion exists.

Mixed statements are the same block. One statement answered the old way
and another answered with links is "both present" for the return. Line 21
is one number. The current gate is return-wide, and splitting one
deduction across two input regimes is more than a change of source.

The precedent is `tax.us.2025.rule.form1040-line2b` v8
(`packages/content/tax/2025/rule.form1040-line2b.v8.json`): its notes say
the legacy and new paths are exclusive and that both refuses, and the rule
declares `selection.mode` `exclusive_presence` with `selection.conflict`
`refuse`. That is a precedent for the policy only. The worksheet rule is
not that schema, and this milestone should not copy the nominee machinery.
Nominee interest was not re-read beyond that rule's selection fields.

Effect on fixtures:

- `tests/test_sli_worksheet_line21_track3.py` asserts line 21 = `2500` for
  one box 1 of 3000, total income 50000, single, the family closed, and
  every conditional answer `yes`. Under this policy that run has no
  relationship rows, so it stays `2500`. The phase-out example in the same
  test (box 1 of 2000, total income 90000, result `1334`) stays too.
- `packages/sample_data/f1098e_student_loan_interest_track6/presentation/below-floor.presentation-model.v1.json`
  and `explanation/report.json` pin the five old `demo.f1098e...` findings,
  including `demo.f1098e.no-non-qualified-loan-component.0`. They are
  old-path fixtures. Their numbers should not be regenerated.
- `closed-empty.presentation-model.v1.json` binds line 21 and does not pin
  that old fact. The empty family publishes 0 without reading the five.
  It stays 0.
- `universal-violation.presentation-model.v1.json` binds line 21. Which
  witness it sets to `no` was not re-opened. It is an old-path block and
  should stay a block.
- The plan's new synthetic `demo-*` cases (plain case, outside loan,
  uncertain, withdrawn, restored, old only, both present, second statement)
  are new fixtures. They are not edits to the track 6 goldens.

No other committed golden that names
`tax.us.2025.f1098e.no-non-qualified-loan-component` was found under
`packages/sample_data/`. Tests that build the old `yes` in memory follow
the old path and do not need new expected numbers.

## 8. Case table for the build

Superseded: the earlier table published `qualified` for the plain case from
the links alone. The decided design publishes `plain-case-supported` only
when section 3 holds, including both ordinary answers at `yes`, and the
result carries the basis in
[track0e-conclusion-basis.md](track0e-conclusion-basis.md).

Line 21 is the worksheet's published symbol. "Worksheet" here means
whether the cap and phase-out run. "Line 21" means what Schedule 1 shows.
Amounts in the first two rows are the current rule's, from
`tests/test_sli_worksheet_line21_track3.py`, and they stay the amounts
only when the plain-case value and the other gates have already passed.
Refusals do not enter the arithmetic. The other four eligibility facts are
`yes` unless a row says otherwise. Filing status is single unless a row
says otherwise. The family is closed. One box 1 unless a row says otherwise.
On a new-path row, both ordinary answers are `yes` unless the row says
otherwise.

| Case | Inputs | Rule result | Worksheet | Schedule 1 line 21 |
| --- | --- | --- | --- | --- |
| Plain case | One borrowing, one schooling, one affirmed financing, one affirmed inclusion, both ordinary answers `yes`, box 1 = 3000, total income 50000, no old fact | `plain-case-supported` for that statement | Cap and phase-out run unchanged | `2500` |
| Plain case, phase-out | Same links and the same two `yes` answers, box 1 = 2000, total income 90000 | `plain-case-supported` | Unchanged arithmetic | `1334` |
| Old yes only | Today's five facts all `yes`, no inclusion and no unresolved inclusion, box 1 = 3000, total income 50000 | New rule publishes nothing | Old gate, unchanged | `2500` |
| Old `no` only | Old non-qualified-loan fact is `no`, no links | New rule publishes nothing | Does not run the arithmetic | Blocked `SLI_UNIVERSAL_COMPONENT_VIOLATION`, not 0. Line 26 then `DEPENDENCY_ABSENT` |
| Old fact missing, no links | Nonempty box 1, the old fact has no current row, no links | New rule publishes nothing | Does not run | `DEPENDENCY_ABSENT`, not 0 |
| Closed empty | No box 1, no links | New rule has no subject | Not entered | `0`, as today |
| Missing or withdrawn link, or financing cannot-tell | Box 1 present, no current affirmed pair, no old fact | `not-supported` | Does not run | Unpublished, not 0. Reason in section 4 |
| Ordinary answer is `no`, `cannot-tell`, or missing | Links would otherwise be the plain case, no old fact | `not-supported` | Does not run | Unpublished, not 0. A missing answer is not the old fact's `no` and not 0 |
| Inclusion cannot-tell | Current unresolved inclusion, no old fact | `not-supported` | Does not run | Unpublished, not 0 |
| Second inclusion, second period, or stale target | Outside section 3, no old fact | `not-supported` | Does not run | Unpublished, not 0 |
| Second statement outside the case | One plain statement and one that is not | One `plain-case-supported`, one `not-supported` | Does not run | Unpublished, not 0. Not a deduction for the plain statement alone |
| Both inputs | Old fact current on a statement, and any inclusion or unresolved inclusion on the return | Do not use `plain-case-supported` from this mix | Do not run either gate | Unpublished, not 0. Not the universal-component code |
| Corrected back to the plain case | Section 3 holds again, no old fact, box 1 = 3000, total income 50000 | `plain-case-supported` on the new current findings | Unchanged arithmetic | `2500` |
| Amount-only correction inside the plain case | Same links and the same two `yes` answers, box 1 changes from 3000 to 1000, income 50000 | `plain-case-supported` | Unchanged arithmetic | `1000`. The 1000 figure is the cap not binding on a smaller box 1; the test file shows the cap at 2500 and the below-floor path, and does not itself assert this 1000 row. Treat 1000 as following that same arithmetic, not as a separate executed test |
| Unchecked statement rewrite | Old inclusion still current after a direct box 1 write | `not-supported` | Does not run | Unpublished, not 0 |

The plain-case rows are the expected results after the count in section 6
exists and the result carries the stated basis. They are not results the
engine can produce today. `plain-case-supported` is not a finding that the
loan is a qualified education loan.

## 9. Owner decisions

Superseded: the earlier text of this section asked three open questions and
stated recommendations. The owner decided those questions on 2026-10-01, and
decided a fourth point this section had not asked. The decisions are the
design.

1. **Two ordinary questions replace the tax question.** For the plain case
   the person is asked whether the loan paid only for school costs, and
   whether the student was enrolled at least half-time in a degree or
   certificate program during that schooling. The keys are in section 2.
   The other four yes/no facts stay asked. The result is
   `plain-case-supported`, not a qualified-education-loan finding, because
   the two answers, two links, and two counts do not establish every
   condition. The assumptions and the responsibilities travel with the
   result.

2. **Old and new inputs are exclusive.** A return with the old
   non-qualified-loan answer on any statement and any inclusion or unresolved
   inclusion on any statement is blocked, even when the two would have
   agreed. Old-only returns, including the track 6 goldens, keep today's
   numbers.

3. **The plain case deducts the whole box 1.** No question hunts for a loan
   the person never mentioned. A second recorded loan on the statement still
   blocks. The unmentioned loan is an assumption on the result, not a
   detected absence.

4. **The fail-open defect is fixed on the old path.** Every box 1 statement
   must carry its own answer for each of the five facts. A statement without
   one blocks the deduction. That fix is a later track. It is recorded here
   because the owner decided it with the other three.

The missing financing count remains an operator gap. Two schooling periods
block either way. It is not an open question.
