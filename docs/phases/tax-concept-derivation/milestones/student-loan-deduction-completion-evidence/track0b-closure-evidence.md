# Track 0b — adversarial-closure evidence for the deduction route

> **Curation note.** The disposable probe this report ran was removed when the milestone was prepared for publication. The commands below are kept as a record; the results recorded here are the evidence.

Scope is the six artifacts for the settled deduction route, on paper and in disposable runs. The ceiling is those artifacts plus executed models. No production change. Stop if the settled design is wrong in a way that changes what a person is asked or what the deduction shows, or if a line 21 model cannot reach the real presentation consumer without a production change.

Read on the milestone branch at the start of Track 0b. Command, from the repo root, exit 0:

```text
PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0b_probe.py
```

That writes `temp/track0b/probe-output.json`. Live cases use `execute` from `tests/test_f1098e_student_loan_interest_agi_track6.py`, which calls `live_coordinate_run`. The adopted package on that path is `tax.us.2025.package.core-calculations` v33, checksum `34903375cd609b2e89cd1ca62119746a6306524922f591722d9eec87de15afeb`, release `demo.release.2025` v26. `rule.sli-worksheet` v1 is a member of both v33 and v38. v38's schema is `artifact-package.v30`. The worksheet bytes are the one file `packages/content/tax/2025/rule.sli-worksheet.json`. Disposable subject rules go through `validate_package`, `_resolved_run_material`, `marshal_run_context`, and `_Run.evaluate_subject_scoped_rule`. Candidate worksheets go through the track 3 fixture's `run` and then `build_presentation_model` with the real form field `tax.us.2025.schedule1.line-21` v1 and the real citation `tax.us.2025.citation.schedule1.line-21` v1.

A one-case `execute` of the closed-empty acts wrote `temp/track0b/closed-empty-pins.json`. The suite JSON stores disposition code and symbol. Input pin ids were read from that one-case disposition. The probe now copies input and choice pin ids onto `line21_rows` for a later rerun; the suite JSON from this session was written before that field.

Identity-key names below were read by the probe from `sli-relationship-source.bundle.json` and `f1098e.bundle.json`.

| Fact | Identity keys |
| --- | --- |
| `tax.us.2025.f1098e.box1-student-loan-interest` | lender, statement, tax-year |
| `tax.us.2025.sli.statement-inclusion-relationship` | lender, statement, tax-year, borrowing |
| `tax.us.2025.sli.financing-relationship` | borrowing, period, institution, programme |
| `tax.us.2025.sli.schooling-situation` | period, institution, programme |
| `tax.us.2025.f1098e.no-related-person-interest` and the other four statement witnesses | lender, statement, tax-year |
| `tax.us.2025.f1098e.1.source-closure` | family-horizon, tax-year |

No `family*.json` under `packages/content/tax/2025/` names the inclusion, the financing link, or the schooling situation. `current_claim_applicability` is defined in `packages/tax/sli_relationship_recording.py`. `packages/derivation` does not call it. A stale link target (link current, schooling or box 1 not current) was not executed.

The runnable copies inside the probe use literal key kinds so the kernel lattice can bind `demo-*` values. The payload instances below use the published entity kinds. Those copies are not the published citizens.

## Chosen keys for the two new answers

`tax.us.2025.sli.loan-paid-only-school-costs` keys `borrowing` only, entity kind `tax.us.student-loan-borrowing-reference`, the same kind financing already uses. Values `yes`, `no`, `cannot-tell`. Only `yes` supports. The sentence is about that loan. A period key would ask about a period the design already refuses when two financings are current. Supersession policy `free`. Nature `determinable`. No default.

`tax.us.2025.sli.enrolled-at-least-half-time` keys `period`, `institution`, `programme`, the same entity kinds as schooling-situation. Values `yes`, `no`, `cannot-tell`. Only `yes` supports. The sentence says "during that schooling." Two loans that finance one schooling would share one enrollment fact. That two-loan case was not run.

Measured join, plain case `demo-stmt` / `demo-lender` / `2025`, one inclusion of `demo-loan`, one financing to `demo-2022` / `demo-college` / `demo-programme`, both answers `yes`. Those six fact types were marshalled sources (`source_names` in the suite JSON).

- A box-1 subject rule that `requires` both answers, with no `joined`, validates (`validation_box_reader` empty) and blocks `DEPENDENCY_ABSENT` naming both answer ids. The findings are current sources. The miss is the join: box 1 keys share no name with either answer.
- A financing-subject rule, `joined` the enrollment fact, direction `subject_contains_joined`, `requires` the financing type, the enrollment fact, and the loan-cost fact, validates (`validation_financing_reader` empty). It publishes `answers-affirmative` and pins `demo.finding.enroll.demo-2022`, `demo.finding.financing.demo-loan.demo-2022`, and `demo.finding.loan-answer.demo-loan`. Enrollment is the declared containment. The loan-cost fact joins through the shared name `borrowing`.
- `shared_key_count` is rejected by `rule-artifact.v12` (`SchemaValidationError` on that op). A hand-called `link_count` of financing from an inclusion subject, with no declared `joined`, returns 1, and package validation of that rule returns `LINK_COUNT_RELATIONSHIP_INVALID`. That call is the real dispatcher on a rule the package does not admit. It is not the proposed operator.

So the two answers are readable from the financing subject. They are not readable from the box-1 subject. `link_count` of inclusions plus a shared-key count of financings returns numbers. Neither returns the answer category. Carrying the financing subject's category onto the statement was not executed as a further rule.

## Payload instances

`SchemaRegistry()` validated each document below. Every check is `valid`. The finding shape stops at the already-published `finding.v1` contract. A committed positive instance of that contract is `packages/sample_data/kernel/demo_workspace/expected/current-state.json`, finding id `finding-new`, fact id `demo.counterparty-payment|counterparty=demo-corp-a,period=2025`, value `1300`, basis and evidence fields as stored there. These instances add no field that contract does not already require. No referenced type demanded a value these facts cannot supply. No field was filled by inventing a reserved doctrine.

```json
{
  "schema": "fact-type.v2",
  "id": "tax.us.2025.sli.loan-paid-only-school-costs",
  "version": "v1",
  "title": "The identified borrowing paid only for school costs",
  "nature": "determinable",
  "identity_keys": [
    {"name": "borrowing", "kind": "entity", "entity_kind": "tax.us.student-loan-borrowing-reference"}
  ],
  "value_schema": {"type": "string", "enum": ["yes", "no", "cannot-tell"]},
  "supersession": {"policy": "free"}
}
```

```json
{
  "schema": "evidence.v1",
  "id": "demo.evidence.track0b.loan-paid-only-school-costs",
  "kind": "demo.sli.ordinary-answer",
  "label": "Synthetic answer that demo-loan paid only for school costs",
  "content": {"answer": "yes"}
}
```

```json
{
  "schema": "finding.v1",
  "id": "demo.finding.track0b.loan-paid-only-school-costs",
  "fact_id": "tax.us.2025.sli.loan-paid-only-school-costs|borrowing=demo-loan",
  "value": "yes",
  "basis": "attested",
  "evidence_ids": ["demo.evidence.track0b.loan-paid-only-school-costs"]
}
```

```json
{
  "schema": "fact-type.v2",
  "id": "tax.us.2025.sli.enrolled-at-least-half-time",
  "version": "v1",
  "title": "The student was enrolled at least half-time in a degree or certificate program during the identified schooling",
  "nature": "determinable",
  "identity_keys": [
    {"name": "period", "kind": "entity", "entity_kind": "tax.us.educational-period"},
    {"name": "institution", "kind": "entity", "entity_kind": "tax.us.educational-institution"},
    {"name": "programme", "kind": "entity", "entity_kind": "tax.us.educational-programme"}
  ],
  "value_schema": {"type": "string", "enum": ["yes", "no", "cannot-tell"]},
  "supersession": {"policy": "free"}
}
```

```json
{
  "schema": "evidence.v1",
  "id": "demo.evidence.track0b.enrolled-at-least-half-time",
  "kind": "demo.sli.ordinary-answer",
  "label": "Synthetic answer that demo-2022 at demo-college demo-programme was at least half-time",
  "content": {"answer": "yes"}
}
```

```json
{
  "schema": "finding.v1",
  "id": "demo.finding.track0b.enrolled-at-least-half-time",
  "fact_id": "tax.us.2025.sli.enrolled-at-least-half-time|period=demo-2022,institution=demo-college,programme=demo-programme",
  "value": "yes",
  "basis": "attested",
  "evidence_ids": ["demo.evidence.track0b.enrolled-at-least-half-time"]
}
```

## 1. Authority lifecycle

Titles of the published facts are the `title` strings in the two bundles. The new facts' titles are the payload instances. The count and the conclusion are not published citizens yet.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| Box 1 `tax.us.2025.f1098e.box1-student-loan-interest` | The interest amount reported in box 1 of one logical Form 1098-E for 2025. Nonnegative source amount. A corrected copy of the same statement supersedes. A VOID copy is not admitted. | One lender, one statement, tax year 2025. | The statement finding and its evidence. Not the five witnesses, not the links, not the new answers. | Withdrawal, supersession by a correction, or a VOID copy that never enters. A later statement is a different member, not an edit of this one. |
| Inclusion `tax.us.2025.sli.statement-inclusion-relationship` | The person's affirmative claim that the named statement includes interest on the identified borrowing. The bundle title excludes portion, exclusivity, and a whole-statement assertion. Value only `sli.statement-inclusion.affirmed`. | One statement plus one borrowing. | The statement identity and the borrowing identity. It does not depend on schooling or on either new answer. | The finding stops being current. Zero current inclusions on a statement is a count of 0, measured below. A second current inclusion is a second row. |
| Financing `tax.us.2025.sli.financing-relationship` | The person's affirmative claim that the borrowing financed the identified schooling. The bundle title excludes sole-use, expense-qualification, and any amount. Value only `sli.financing.affirmed`. | One borrowing plus one period, institution, and programme. | Those four identities. Not a family closure. No family names this type. | The finding stops being current. The hand count then drops, measured below. There is no close step to re-attest. |
| Schooling `tax.us.2025.sli.schooling-situation` | A person-described schooling situation. Descriptions do not define identity. | Period, institution, programme. | The person's description of that situation. | The finding stops being current. Whether a still-current financing link then fails a target check is unverified: the derivation runner does not call `current_claim_applicability`, and that case was not run. |
| Loan-cost answer | The identified borrowing paid only for school costs. `yes` supports. `no` and `cannot-tell` do not. | The borrowing only. | An attested answer for that borrowing. One current finding per borrowing under this key. | Supersession (`free`) or withdrawal. A financing-subject reader then publishes `answers-not-affirmative`, measured for `no` and for a corrected finding id. |
| Enrollment answer | The student was enrolled at least half-time in a degree or certificate program during that schooling. `yes` supports. `no` and `cannot-tell` do not. | The schooling situation. | An attested answer for that period, institution, and programme. | Supersession or withdrawal. `cannot-tell` on `demo-2022` publishes `answers-not-affirmative` and pins that enrollment finding. |
| Inclusion count | How many current affirmed inclusions this box 1 statement has. The design wants exactly one. | The one statement. | Current inclusion rows whose keys contain the statement's keys. The admitted rule declares `joined` inclusion, direction `joined_contains_subject`. | A change in the current inclusion set. Measured: one inclusion publishes `1` and pins the inclusion; zero inclusions publishes `0` and pins only the box 1 finding. |
| Financing count | How many current affirmed financings share `borrowing` with that inclusion. The design wants exactly one, from the proposed shared-key count. | The one inclusion's borrowing. | Current financing rows with that borrowing. | A second financing, or withdrawal of the financing. `shared_key_count` is not a legal v12 op. The undeclared hand `link_count` returned 1, then 2, then 0. Those numbers are the dispatcher's, on a rule validation rejects. |
| Qualified-loan conclusion | This statement's interest is supported as one current loan, one current financing, both link targets current, and both new answers affirmative. Every other statement gets `not-supported`. | One box 1 statement. | The two counts, target currentness, and both answers. It does not read the five old facts. | Any count other than 1, a target that is not current, or an answer other than `yes`. The box-1 subject rule cannot read the answers today, so this conclusion cannot be published by that rule alone. The financing-subject reader can see the answers. The carry back to the statement was not run. |
| Five old statement facts | Each `yes` says the named excluded class is absent from this statement's box 1. `no` says it is present. Domain `{yes, no}`, no default. The replaced one, `no-non-qualified-loan-component`, is the bundle's single stand-in for student status, qualified education expenses, and a reasonable period. | The same statement as box 1. | An answer on that statement. Old-path only. The new-path rule does not read them. | `no` blocks the whole route. A missing row on the only statement blocks `DEPENDENCY_ABSENT`. A missing row on one of two statements does not, measured below. |
| Family closure `tax.us.2025.f1098e.1` | Every furnished 2025 box 1 amount is recorded as of the keyed horizon. The claim covers box 1 and its box 2 companion only. It says nothing about the twelve eligibility components. Closed with members authorizes the multi-lender sum. Closed-empty authorizes subtotal 0. Authorizes `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`. | The box 1 family at one horizon. | The closure finding for that horizon. | A later member displaces the closure. The prior horizon's closure stops authorizing the sum until a closure is attested on the successor horizon. Measured in the live late-member cases. |

## 2. Empty and nonempty

The ineligible nonempty result used here is a block, or a `not-supported` row that the worksheet treats as a block. It is not a published 0. The closed-empty return is the one case that publishes 0.

| Population | State | What ran | Result |
| --- | --- | --- | --- |
| Box 1 family | Closed, no statements, closure attested | Live `closed-empty`. Wages 50000. | Presentation `line-sch1-21` is `closure_backed_zero` 0. Line 26 published. Line 10 is `computed_zero` 0. Lines 11a and 11b are `published_value` 50000. The Schedule 1 attachment is `guard_inapplicable`. |
| Box 1 family | Same return, closure not attested | Live `unclosed-empty`. | Line 21 blocked `DEPENDENCY_ABSENT`. Line 26 blocked `DEPENDENCY_ABSENT`, missing `tax.us.2025.schedule1.line21-sli-deduction`. Lines 10, 11a, 11b blocked `DEPENDENCY_ABSENT`. |
| Box 1 family | Closed, one statement, old answers `yes`, box 1 `3000`, wages `50000` | Live `old-deduction` and the unmodified-worksheet candidate. | `published_value` 2500. Line 10 is 2500. Lines 11a and 11b are 47500. Attachment `published`. |
| Box 1 family | Closed, one statement, one witness `no` | Live `old-block`. | Line 21 blocked. Active code `SLI_UNIVERSAL_COMPONENT_VIOLATION`. No number. Line 26 blocked missing line 21. |
| Box 1 family | Closed, one statement, the old component fact omitted | Live `old-fact-absent`. | Line 21 blocked `DEPENDENCY_ABSENT`. The disposition row names `tax.us.2025.f1098e.no-non-qualified-loan-component`. |
| Box 1 family | Closed, two statements, the second statement's related-person answer omitted | Live `fail-open-second-witness-absent`. Amounts 1000 and 500. | Line 21 `published_value` 1500. The missing second answer did not block. |
| Box 1 family | Statements present, family not closed | Live `unclosed-nonempty`. | Line 21 blocked `SOURCE_SET_UNCLOSED`. |
| Inclusions | One current inclusion | Admitted `link_count`, hand-called on the plain world. | Publishes `1`. Pins the box 1 finding and `demo.finding.inclusion.demo-stmt.demo-loan`. |
| Inclusions | No inclusion row | Same rule, inclusion row omitted. | Publishes `0`. Pins only the box 1 finding. |
| Financings | One / two / withdrawn | Undeclared hand `link_count` from the inclusion. | `1`, then `2`, then `0`. Validation of that rule is `LINK_COUNT_RELATIONSHIP_INVALID`. |
| New answers | Both `yes` | Financing-subject reader. | `answers-affirmative`. |
| New answers | Loan answer `no`, or enrollment `cannot-tell` | Same reader, fresh worlds. | `answers-not-affirmative`. |
| New answers | Absent from the box-1 subject | Box-1 reader. | `DEPENDENCY_ABSENT` on both answer ids. |

Closed-empty input pins, from the one-case disposition: adoption `tax.us.2025.package.core-calculations`, citations `tax.us.2025.citation.form1040.sli-worksheet` and `tax.us.2025.citation.schedule1.line-21`, input `demo.f1098e.closure`, package pins `tax.us.2025.closure-mapping.f1098e.1` and `tax.us.2025.f1098e.1`. None of the five old fact ids is a pin. The worksheet's taken branch for that case, read in `rule.sli-worksheet.json`, is the literal `0`. The five ids are also absent from the suite JSON's stored line 21 disposition text for `closed-empty`.

Line 15 is `blocked` `DEPENDENCY_ABSENT` on the closed-empty return and on the 2500 deduction alike. The line 15 rule requires `tax.us.2025.income.agi` and `tax.us.2025.deductions.line-14`. The probe did not record which of those the live block named.

The phase-out amount was not re-run. The cap case, 3000 of interest at 50000 of wages, published 2500 on both the live path and the candidate path. The new-path candidate edits only the old-fact collect node (`replacement_removed_old_fact` true) and still publishes 2500 from box 1 of 3000.

## 3. Late members

### A second statement after a deduction

Live path, horizons `demo.f1098e.t0b.hi.0` and `.1`, through `live_coordinate_run`.

| Step | Line 21 | What stops being usable |
| --- | --- | --- |
| Attest one statement box 1 `1000`, close, compute (`late-base`) | `published_value` 1000. Line 10 is 1000. Lines 11a and 11b are 49000. | The closure on horizon `.0` authorizes that sum. |
| Add a second statement box 1 `500` and do not reclose (`late-added-unclosed`) | Blocked `SOURCE_SET_UNCLOSED`. Line 26 blocked missing line 21. | The horizon `.0` closure no longer authorizes the family. The previous 1000 is not the current line 21. |
| Reclose on horizon `.1` and recompute (`late-reclosed`) | `published_value` 1500. Line 10 is 1500. Lines 11a and 11b are 48500. | The successor closure is the one that authorizes the sum. |

### A second financing link

No family contains the financing type, so there is no close and no reclose. Each row is a fresh `marshal_run_context`, not a displacement inside one horizon. The previous derived count is not carried forward and then invalidated by the kernel. What the new run pins is the whole current set.

| Current financings | Hand count | Pins |
| --- | --- | --- |
| `demo-2022` only | `1` | That financing finding and the inclusion. |
| `demo-2022` and `demo-2023` | `2` | Both financing findings and the inclusion. |

The financing-subject reader on the two-period world publishes two rows, both `answers-affirmative`, each pinning its own enrollment finding (`demo.finding.enroll.demo-2022` and `demo.finding.enroll.demo-2023`) and the same loan-cost finding. The count is 2 while each answer row is affirmative. The design's `qualified` conclusion needs the count to be 1. A single rule that both counts and publishes `qualified` was not executed.

### A link withdrawn

The financing finding `demo.finding.financing.demo-loan.demo-2022` stays in the finding dict and is omitted from currency. Hand count publishes `0` and pins only the inclusion. The financing-subject reader publishes nothing and blocks nothing: no financing subject remains. The withdrawn finding is not an input pin. It has stopped being a counted row and has stopped being a subject. Schooling and the enrollment answer were still in the world. They did not keep a financing subject alive.

### An answer corrected from yes to no

Fresh currency. The original yes finding `demo.finding.loan-answer.demo-loan` is omitted. The current finding is `demo.finding.loan-answer.demo-loan.corrected` with value `no`. The reader publishes `answers-not-affirmative` and pins the corrected id, not the yes id. This was not kernel supersession inside one horizon. The yes finding is not current in that run, and the affirmative publication is not the result of it. `cannot-tell` on the enrollment fact, with the yes loan-cost finding still current, also publishes `answers-not-affirmative` and does pin the enrollment finding.

## 4. Claim reuse

The design uses the published inclusion and financing citizens. The probe read their identity-key names from `sli-relationship-source.bundle.json`. Those names are the ones in the table at the top. The bundle titles, read from that file, are the propositions:

- Inclusion: the person's affirmative ordinary-language claim that a named Form 1098-E statement includes interest on an identified borrowing. No portion, exclusivity, or whole-statement assertion.
- Financing: the person's affirmative ordinary-language claim that an identified borrowing financed an identified schooling situation. No sole-use, expense-qualification, or amount assertion.

Values remain the single affirmed category each bundle declares. Keys, titles, and value enums were not edited. No family adopts either type, so their lifecycle is the finding's own currency. There is no closure claim on them, before or after. Their authority scope stays the identities in those keys. Matching the storage shape is what the file already is. The proposition, the identity, and the lifecycle are that same file.

The conclusion is a new claim. It does not mean what `tax.us.2025.f1098e.no-non-qualified-loan-component` means. That old fact's bundle title says one answer stands in for student status, qualified education expenses, and a reasonable period, and that `yes` means that excluded class is absent from box 1. The conclusion means this statement's interest is supported as one current inclusion, one current financing of that borrowing, both targets current, and both new answers `yes`. It publishes `qualified` or `not-supported` for that statement.

The conclusion does not claim student status beyond the enrollment answer, qualified expenses beyond the loan-cost answer, a reasonable period, sole use of a loan the person never recorded, a portion of box 1, or exclusivity beyond exactly one current affirmed inclusion. The old fact's `yes` and `no` stay a different proposition, read on the old path only. The new-path worksheet clone removes that fact from the value (`replacement_removed_old_fact` true). The old-path live run still reads it: omitting it on the only statement blocks `DEPENDENCY_ABSENT` and names that fact id.

## 5. Neighbor dependencies

Read by the probe from the rule files. "Before" is that file today. "After" is the settled design, which does not add a `requires` entry on these rules. No neighbor file was edited.

| Neighbor | Before | After | No Form 1098-E, measured |
| --- | --- | --- | --- |
| Schedule 1 line 26 `rule.schedule1-line26` v1 | Requires line 21 and the twelve `schedule1-adjustments-scope.no-line*` facts. Refs are those same names. | Still requires line 21. Does not require either link, either new answer, or the five old facts. | Closed-empty: line 26 published. Unclosed-empty and old-block: line 26 blocked `DEPENDENCY_ABSENT`, missing line 21. |
| Form 1040 line 10 `rule.form1040-line10` v1 | Requires `tax.us.2025.schedule1.line26-total-adjustments` only. | Same. Line 21 is not a direct require. | Closed-empty: `computed_zero` 0. Old deduction: `published_value` 2500. Old block: blocked `DEPENDENCY_ABSENT`. |
| Form 1040 lines 11a and 11b `rule.form1040-line11` v2 | Requires total income and line 26. Both form fields bind the AGI this rule publishes. | Same. They do not read line 21 directly. | Closed-empty: both `published_value` 50000. Old deduction: both 47500. Old block: both blocked `DEPENDENCY_ABSENT`. |
| Form 1040 line 15 `rule.form1040-line15` v2 | Requires `tax.us.2025.income.agi` and `tax.us.2025.deductions.line-14`. | Same. Line 21 is not a require. | Blocked `DEPENDENCY_ABSENT` on the closed-empty return and on the 2500 deduction. The block is present when line 21 is a number, so it is not a new line 21 prerequisite. Which of the two requires the live row named was not stored. |
| Schedule 1 attachment `rule.attachment.schedule-1` v2 | `requirement.subtotals` lists the unemployment box-1 subtotal and line 21. The probe's ref walk is empty because those names sit in `requirement`, not in an `op: ref` node. | Same two subtotals. The itemization tie-out stays on the raw box 1 subtotal. The subtotal rule's note says the tie-out is that raw sum, and the cap lives in the worksheet. The note is the only place `line21-sli-deduction` appears in the subtotal file. | Closed-empty: attachment `guard_inapplicable`. Old deduction and the reclosed two-statement return: `published`. Blocked line 21: attachment `blocked`. |

A return with no Form 1098-E keeps publishing line 21 as a closure-backed 0 without the five facts, and lines 10, 11a, and 11b stay computable from that 0 and the wages. The design leaves those requires as they are. Each neighbor's own meaning is the adjustment total, AGI, taxable income, or the Schedule 1 attachment's subtotal list. None of those meanings is a per-loan answer or a link count. The new facts are inputs of the line 21 producer. They are not new prerequisites of these neighbors.

The worksheet producer, which is not one of those neighbors, is the rule that changes. Today it requires filing status, rounding, total income, and the line 1 subtotal, and its value refs the five statement facts. On the new path the qualified-row collect replaces the old component fact. On the old path the five collects stay, and a statement with no row of its own must block. Old and new inputs together block. Those are producer changes. They do not appear in the neighbor `requires` lists above.

## 6. Integration surface

Symbol `tax.us.2025.schedule1.line21-sli-deduction`. The probe scanned every JSON file under `packages/content/tax/2025/`.

| Binding | Where | Cardinality it expects |
| --- | --- | --- |
| Form field `tax.us.2025.schedule1.line-21` v1 | `binds_symbol`. In package v38. | Exactly one disposition row. `build_presentation_model` calls `_one_row`. A count other than 1 raises `PresentationModelError` (`missing or ambiguous disposition join`). Every live case in this run had `line21_section_count` 1, including the blocks. |
| Producer `tax.us.2025.rule.sli-worksheet` v1 | `publishes`. In v33 and v38. | One rule, not subject-scoped, so one disposition for the symbol. A block is one blocked row. The live rows are one per case. |
| Consumer `tax.us.2025.rule.schedule1-line26` v1 | `requires` and `ref`. In v38. | One symbol. When line 21 is blocked, line 26 is `DEPENDENCY_ABSENT` and names this symbol. Measured on `old-block` and `unclosed-empty`. |
| Attachment `tax.us.2025.rule.attachment.schedule-1` v2 | One entry in `requirement.subtotals`. In v38. | One symbol in that list, beside the unemployment subtotal. |
| `rule.sli-worksheet-line1-subtotal` v1 | The symbol occurs in a note, not in `requires`, `publishes`, or `binds_symbol`. | No binding. |

The form field's blocked-code list is `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_UNCLOSED`. The projector copies `row["code"]` into `activeCodes` without checking that list. Live `old-block` presentation `activeCodes` is `SLI_UNIVERSAL_COMPONENT_VIOLATION`, which is not on the list. The field's blocked explain text is the generic sentence about incomplete authority, an excluded class, married filing separately, or an unclosed family.

Candidate models pass the real form field, the real citation, and a clone of the real worksheet into `build_presentation_model`. The worksheet has no `reader_role`, so those candidate runs do not build the calculation view. The live runs do: their presentation includes line 10, lines 11a and 11b, and line 21. The form-field join is the consumer in both.

| Outcome | How it ran | Presentation | Hand-built |
| --- | --- | --- | --- |
| New-path deduction | Candidate. Collect of `demo.tax.track0b.qualified-loan-for-statement` expects `qualified`. Box 1 is 3000. One source row valued `qualified`. | `published_value` 2500. Schema `presentation-model.v1`. One section. | The qualified source row. The arithmetic and the field are the worksheet file and the form field. This run does not show a box-1 rule reading the two answers. |
| New-path refusal | Same clone. Source value `not-supported`. | `blocked`. Active code `SLI_UNIVERSAL_COMPONENT_VIOLATION`. No number. | The `not-supported` source row. |
| Old-path deduction | Live `old-deduction`, and a candidate that keeps the unmodified worksheet with every conditional answer `yes`. | Both `published_value` 2500. | Live acts are the track 6 synthetic statements. The candidate uses the fixture's inputs. |
| Old-path block | Live `old-block`, witness `no-related-person-interest` = `no`. Candidate sets that same answer to `no`. | Both `blocked`, active code `SLI_UNIVERSAL_COMPONENT_VIOLATION`. | The `no` answer is the synthetic witness. |
| Both-present block | Candidate. A `choose` in front of the worksheet blocks with code `SLI_OLD_AND_NEW_BOTH_PRESENT` when any old-fact row is `yes`, and the world also has a `qualified` row. | `blocked`. The evaluator's blocked entry keeps `SLI_OLD_AND_NEW_BOTH_PRESENT`. The recorded disposition code and the presentation `activeCodes` are `DEPENDENCY_INVALID`. | The gate and both source rows, on a clone of the real worksheet. |
| Closed-empty zero | Live `closed-empty`, and a candidate with no box 1 source and no witness inputs, closure closed. | Both `closure_backed_zero` 0. | Live: `statements=[]`, `close=True`. Candidate: the same closure authority helper, no amount source. |
| Old-path missing-answer block after the fix | One `_Run`. A box-1 `link_count` of `no-related-person-interest` publishes `1` for `demo-stmt` (pins the witness) and `0` for `demo-stmt-b` (pins only the box 1 finding). A second subject rule on that same run refs the count and publishes `answered` and `missing`. Those two publications are the worksheet's sources. The clone collects `demo.tax.track0b.witness-status` expecting `answered`. | `blocked`. Active code `SLI_UNIVERSAL_COMPONENT_VIOLATION`. `missing_answer_sources_hand_built` is false. | The collect node in the clone. The status rows are the dispatcher's publications. |

The same clone, with the `missing` row left out and the `answered` row kept, publishes 2500. `collect_categorical_all_equal` does not compare its row count to the box 1 count. The fix holds when the per-statement publisher emits the row. A blocked subject that emits no row leaves the deduction in place. The count rule is a legal v12 rule (`validation_ok` true, issues empty): `joined` is the witness, direction `joined_contains_subject`, and `link_count` is the only value node. The mapper is a second rule because `link_count` may not appear in `when`.

## What the evidence leaves open

The stop condition was not hit. The two questions stay an ordinary loan-cost answer keyed by borrowing and an ordinary enrollment answer keyed by the schooling situation. The cap case still shows 2500 from box 1 of 3000. All seven line 21 outcomes reached `build_presentation_model` with the real form field and no edit under `packages/`.

Three measured gaps sit in front of the build:

- A box-1 subject rule blocks `DEPENDENCY_ABSENT` on both new answers while those findings are current sources. A financing-subject rule publishes `answers-affirmative` from the same world. `link_count` and the rejected `shared_key_count` return numbers, not the answer category. The plain case does not publish `qualified` from those two operators alone. The smallest case is `demo-stmt` / `demo-lender` / `2025`, one inclusion of `demo-loan`, one financing, both answers `yes`, and the box-1 read empty.
- Declaring `shared_key_count` fails `rule-artifact.v12` validation. Declaring the hand `link_count` of financing from an inclusion subject fails with `LINK_COUNT_RELATIONSHIP_INVALID`. The hand call still returned 1, 2, and 0.
- `SLI_OLD_AND_NEW_BOTH_PRESENT` is kept on the evaluator's blocked entry and stored as `DEPENDENCY_INVALID` on the disposition the presentation consumer reads. The line is blocked, and the active code is not a sentence about both inputs. The form field's explain text does not name that situation.

`collect_categorical_all_equal` still publishes 2500 when one of two statements has no status row. The executed fix is the publisher that emits `missing` for that statement. The worksheet then blocks.

One choice is not settled by a prior owner decision and changes the words on a blocked line: whether the both-present reason has to be a new derivation-record version before Track 1, or whether blocking under an existing code is acceptable until that schema track. This track did not add a schema version.

Unverified, and not run: kernel supersession of the corrected answer inside one horizon; `current_claim_applicability` on a financing whose schooling or box 1 is no longer current; the phase-out dollar amount; a live production run that adopts the relationship bundle next to the old answers; two loans sharing one enrollment fact; a third rule that carries the financing subject's category back onto the box 1 statement.
