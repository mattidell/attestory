# Bounded reader contract — statement calculation beside Schedule 1 line 21

> **Revision (2026-09-24).** Replaces the draft at
> `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/reader-contract-draft.md`.
> The draft's wording **pin role** stays withdrawn, and so does the draft's further step of a new
> `condition-wording.v1` pinned by that role. Line 21 is not retargeted. Two recommendations below:
> per-statement rows are a separate calculation view until a worksheet successor reads them, and
> the sentence lives as a field on the rule successor the subject declaration already requires.
> Draft status of this file: not accepted.

Read-only design. Branch `milestone/student-loan-circumstance-association`, HEAD `f0f1dd7630c330f5f1c6c840b8270152641eb8d2` (the draft was written at `b558da4e`; ADR 0075 is accepted at this HEAD). Sources read here: `packages/content/tax/2025/schedule1.line-21.form-field.json`, `rule.sli-worksheet.json`, `rule.sli-worksheet-line1-subtotal.json`, `packages/derivation/presentation_projection.py`, `runner.py` (`pins_for`, `dependency_pins_for_access`, `_record_blocked`), `evaluator.py` (`_link_coverage`, `EvalBlocked`), `subject_dispatch.py`, `packages/schemas/derivation/derived-finding.v2.schema.json`, `parameter-declaration.v1.schema.json`, `rule-artifact.v10.schema.json`, `packages/schemas/tax/form-field.v3.schema.json`, `packages/presentation/pages/citation-walk.v1.html`, ADR 0075, and the coverage contract's identity table. ADR 0076 is not a file at this commit. It is the binding ADR 0075 leaves open.

This document is the contract for the current reader. It does not approve wording, does not schedule a run, and does not change the derivation record.

The carrier is presentation projection. `build_presentation_model` writes what the page shows into the durable `presentation.json`. `derivation-record.v9` stays `derivation-record.v9`. No `published` array, no `value` on disposition rows, no new record code.

**Evidence marks used below.** **Production** means committed code or content at this HEAD, including the `link_coverage` operator and its committed tests. **Prior probe** means a hand-driven run already reported (P4 in `a4-bounds.md`, Question 2 in `g2-path-investigation.md`); it was not re-executed for this revision. **Contract** means a requirement of this document, not something that runs. None of the per-subject student-loan chain is production-scheduled. ADR 0075's acceptance does not authorize a statement-specific production result.

The reader case is not complete until both of these are true:

1. Each sentence the page shows was copied from the rule field in section 8, and the projector copied that field.
2. A statement-scoped responsibility rule has actually run for a bare statement under the selection in section 7 and published the finding section 9 describes.

"School unknown" is never inferred from a missing pin, from a missing link, or from a parameter pin. A row that did not pin a school has not decided that the school is unknown.

## 1. Schedule 1 line 21 stays the worksheet deduction

**Production.** `tax.us.2025.schedule1.line-21` (`form-field.v3`) binds `tax.us.2025.schedule1.line21-sli-deduction`. That symbol is what `tax.us.2025.rule.sli-worksheet` publishes. The field is not retargeted. The projector does not hang statement rows on it, and it does not rewrite `binds_symbol`.

**Production.** The figure on that symbol is not a per-statement amount. The worksheet's line 1 is `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`, published by `tax.us.2025.rule.sli-worksheet-line1-subtotal`: one `round` of the `add` of a `collect` over `tax.us.2025.f1098e.box1-student-loan-interest` in source set `tax.us.2025.f1098e.1`. That is the raw, uncapped family sum. The worksheet rule refs that symbol. It does not collect box 1 again, and it does not read a per-statement net.

**Production.** The worksheet rule's value, read from the nested `choose` at this HEAD, is:

1. If `count` of the box-1 family is 0, the value is the literal 0. No cap, no phaseout, no eligibility arithmetic.
2. Otherwise the result is `round` under `rounding.convention`, of whichever arm fires next:
   - `filing_status` equals `married_filing_separately` → block `SLI_MFS_INELIGIBLE`.
   - Any of the three return-level scope facts is not `yes`, or any current finding of the five per-statement universal witnesses is not `yes` (`collect_categorical_all_equal`) → block `SLI_UNIVERSAL_COMPONENT_VIOLATION`.
   - Any of the twelve Schedule 1 Part II absence facts is not `yes` → block `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`.
   - `not-claimed-as-dependent` or `legally-obligated-for-interest` is `no` → the literal 0.
   - Otherwise `capped − (capped × ratio)`, where `capped = line1 − max(line1 − cap, 0)` and `cap` is `tax.us.2025.parameter.sli-interest-cap`, and `ratio` is `min(1, max(0, total-income − threshold) / phase-range)` with the division floored to 3 decimal places, half up. `threshold` and `phase-range` are filing-status-keyed parameters. `total-income` is `tax.us.2025.income.total-income`.

The guard is `require_closed` on `tax.us.2025.f1098e.1`, and, when the count is greater than 0, a `conditional_dependency_set` of those eligibility refs. A closed empty family never reads them.

**Production, and the reason there is no decomposition.** Nothing in that expression is a per-statement reduction, a link, or `demo.tax.statement-facing-amount`. The prior-probe amount is box 1 minus a `link_coverage` total (the no-link parameter is 0, so a statement with no joined link publishes box 1 unchanged). That symbol is not an operand of line 21. Between a statement's box 1 and the dollar on line 21, the current worksheet sums raw box 1 across the family, caps the sum, phases the capped sum out, and rounds once, and it may replace all of that with 0 or a block. It never subtracts a per-statement reduction on the way.

**Contract. Recommendation: a separate calculation view until worksheet integration.** Do not present statement rows as terms of line 21. There is no arithmetic in the current rules that would make their sum, or any one of them, equal the line. The integration that would connect them does not exist: a worksheet successor would have to read, as its line-1 input, the sum of per-statement nets (each box 1 minus that statement's reduction total) instead of the raw collect, and line 21 would then be the same cap, phaseout, gates, and round applied to that sum. Until that successor is the rule that publishes `tax.us.2025.schedule1.line21-sli-deduction`, the page must not say the groups explain the line.

Line 21's own section stays today's projection: one `resolved` object, the worksheet disposition, the field's own `explain`, the leaf citation walk of the worksheet. **Production.** The page shows a blocked code only when it is in the field's `blocked.codes`. That list is `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_UNCLOSED`. The three `SLI_*` codes are in `RECORD_CODES` and on the disposition. They are not in the field's list, so the banner still renders and the code line says `(unspecified)`. This contract does not add them to the field.

## 2. The calculation view

`presentation-model.v1` stays the version string. This is the `provenanceGroups` precedent: an internal validator change, not a published schema, not a version bump. Existing models that lack the new key remain valid and render as they do today.

The new key is top-level `calculationView`. It is optional. It is not a section, not a `statementGroups` array on `line-sch1-21`, and not `provenanceGroups`. Unknown top-level keys other than `provenanceGroups`, `authorization`, and `calculationView` still fail. `provenanceGroups` is unchanged and is not a substitute.

The view is present only when the run published or blocked at least one row whose resolved rule's own `publishes` is the per-statement amount symbol. **Prior probe.** That symbol, in the hand-assembled chain, is `demo.tax.statement-facing-amount`, and the row's symbol is that name plus `|` plus the subject fact id. **Contract.** The view names the symbol it joined. It does not invent a content id. Until a content rule publishes the symbol, a production run has no view.

### Join

A disposition row is a member of the view when its `symbol` is `publishes` plus `|` plus a fact id, and the resolved rule's own `publishes` equals the unsuffixed amount symbol. The check reads the rule that ran (`artifact_id` in the resolved graph). It does not rewrite `publishes` on a copy. P4's synthetic member is not the join, and retargeting line 21 is not the join.

`_one_row` is unchanged and still applies to form fields. Line 21 keeps exactly one row of `tax.us.2025.schedule1.line21-sli-deduction`. Keyed amount rows are not an ambiguous join on that field, because they are not joined to it. Zero keyed rows means the view is omitted, not a failure of line 21. An unsuffixed amount row together with keyed rows is a failure. The projector does not pick one.

### What the view carries

Required keys when the object is present:

| Key | What it is |
| --- | --- |
| `integrated` | `false` until the worksheet rule's line-1 input is the per-statement net. This contract requires `false` |
| `amountSymbol` | The unsuffixed symbol the amount rule publishes |
| `groups` | One object per keyed amount row, below |

Each group:

| Key | What it is |
| --- | --- |
| `symbol` | The keyed symbol, `publishes\|fact_id` |
| `factId` | The suffix after `\|` |
| `findingId` | The row's finding id. Absent when the row is blocked and published no finding |
| `ruleId` | `artifact_id` of the rule that published or blocked it |
| `ruleVersion` | `version` of that rule in the resolved graph |
| `disposition` | The row's disposition |
| `value` | The published value, copied from the in-memory finding. Absent when the row is blocked |
| `pins` | The finding's pins, or the blocked row's pins, copied. A pin is copied with the keys it has. `origin` is copied only when the pin has it. The projector never adds `origin` |
| `nodes` | Intermediate findings the downward walk passed through and today throws away: each reduction and each status, with `findingId`, `ruleId`, `ruleVersion`, `symbol`, `value`, `pins`, and `basisOrigin` as defined in section 3. Leaves stay leaves |
| `missing` | Present on a blocked group. Entries as section 4 classifies them. Not a single "resolved finding" shape |
| `responsibilities` | Rows found by the reverse walk below. Empty is legal |
| `lineNote` | The ordinary-line sentence, present only when the favourable-conclusion rule that published for this statement declares it. Copied from that rule, not composed |

`citationSites` on the **line 21 section** stay the worksheet's leaves. They are not rebuilt from the view. The view does not contribute a number to the line. The amount's number stays inside the group.

### Reverse walk

After the downward nodes of a group are known, take every disposition that is not already one of those nodes. If one of its input pins names a finding id already in the group, including the amount finding, attach that disposition as a responsibility row. The downward walk does not find these rows. **Prior probe.** P4 showed nothing on the amount's pin list is the responsibility.

A responsibility row carries `ruleId`, `ruleVersion`, keyed `symbol`, `findingId`, categorical `value`, and its pins. It carries `wording` only by the copy in section 8. The row is not a citation site of line 21 and is not fed through the field's citation chain.

Do not attach a disposition merely because it shares a rule family, a tax year, or an absent pin.

### Validator

`validate_presentation_model` changes as follows.

- Top-level required keys are unchanged. `provenanceGroups`, `authorization`, and `calculationView` are the optional top-level keys.
- A section may not include `statementGroups`. Line 21's section shape is unchanged.
- `calculationView.integrated` must be `false` under this contract. `groups` must be non-empty when the view is present.
- Each group must have the keys in the table. `value` and `findingId` may be absent only when `disposition` is `blocked`. `missing` is required when `disposition` is `blocked` and forbidden when it is not. `responsibilities` defaults to empty. `lineNote` is omitted rather than invented.
- `basisOrigin`, when present on a node, is `assertion` or `declared_default`, and it was copied from an input pin that had that `origin`. A parameter pin with `basisOrigin` or `origin` fails.
- `missing` entries obey section 4. A finding-id entry that does not resolve fails. A marker, a parameter id, or a symbol name that was forced through finding resolution fails.
- `wording` and `lineNote` must equal the resolved rule's field after the slot rule in section 8. Any other string fails, including a string the projector built from a template it was not given.
- A group or responsibility whose rendered text says the school or programme is not known fails unless the rule that supplied the text is the bare-statement rule and section 7's guard held for that statement.
- A slot filled from a key the finding did not pin fails.
- The unsafe-string check (`</script`, `<!--`) applies to every new string.
- `provenanceGroups` is unchanged.

### What stays out of the model

- Any edit to `derivation-record.v9`, including a `value` field or a `published` array.
- A new disposition code.
- `provenanceGroups` as the carrier for this chain.
- Statement rows joined as the breakdown of line 21.
- One section per statement.
- A question, a confirmation flag, or a screen-wide warning flag.
- A school name, the word "unknown", or the case-2 sentence, unless the copied rule field or a pinned fact key supplied it.
- The categorical token rendered as a display value. `applies` is not a sentence.
- Rewriting the form field's `label`, `description`, `explain`, or `binds_symbol`.
- An `origin` on a pin whose role is not `input`.

## 3. Parameter pins and declared-default inputs

**Production.** `derived-finding.v2` gives `origin` to a pin only in one case. The pin schema requires `origin` when `role` is `input`, and forbids `origin` on every other role. The enum is `assertion` or `declared_default`. `dependency_pins_for_access` writes `origin` only inside `if role == "input"`. A parameter pin is built as `{"role": "parameter", "id", "version"}` with no `origin`, from `access.parameters` and `access.tables`.

**Production.** A favourable eligibility default is a different object. Run init, and `subject_dispatch._optional_default`, mint a `derived-finding.v2` whose `resolved_input` is `{fact_id, origin: declared_default}` and whose pins are adoption, governance, and one parameter pin. That parameter pin has no `origin`. The symbol binding handed to a consumer is `(finding_id, "v2", "input", "declared_default")`. The consumer's pin is therefore role `input`, `origin: declared_default`, and its `id` is the **default finding**, not the parameter.

**Operator, committed tests, not a production schedule.** On the no-link path `link_coverage` returns the declared parameter. The amount rule in the coverage tests publishes box 1 minus that parameter. The finding has no `resolved_input`. Its input pin is the box-1 finding, `origin: assertion` when `use_v2`. Its parameter pin is the no-link parameter id and version, role `parameter`, and it has no `origin`. A covered path pins each link and each reduction as `input` / `assertion` and does not pin the parameter. An uncovered path does not pin the parameter either.

Those two pins must stay distinct in the model and on the page.

| | No-link parameter | Declared-default eligibility |
| --- | --- | --- |
| Where it sits | On the amount finding, role `parameter` | On the consumer, role `input`, id = the default finding |
| `origin` | Absent. Assigning one is a validator failure | `declared_default`, copied from the input pin |
| `resolved_input` | Absent on the amount | Present on the default finding, not on the amount |
| What it means | The reduction total when both joined lists are empty. A quantity | The favourable input was taken from a declared default |
| Page | The pin is shown as a parameter: id and version, no basis | `basisOrigin: declared_default` on the node that pinned the default finding |
| Sentence | Does not by itself authorize the ordinary-line note | The note is copied only from the conclusion rule's own field, and only when that rule published |

`basisOrigin` on a node is the `origin` of an input pin on that finding, and nothing else. It is never computed by noticing which pins are missing, and it is never copied off a parameter pin. The sentence "taken as met because nothing you've described says otherwise" is not the no-link parameter and is not derived from `declared_default`. It appears only as `lineNote`, and only when the conclusion rule declares that field.

Citation sites stay leaves of role `input` or `choice`. A parameter is not turned into a citation site. It is visible on the group's `pins`, not only inside an embedded act.

## 4. Blocked `missing`

**Production.** A blocked disposition's `missing` is a list of strings from the evaluator or the runner. It is not a list of finding ids. The projector classifies each string. Only the finding-id class is resolved against recorded state. Forcing another class through that lookup is a projector failure.

Recognition order, first match:

1. **Diagnostic marker**, if the string is exactly one of `link-coverage-scope-unbound`, `link-coverage-keys-unavailable`, `link-coverage-unjoinable`.
2. **Parameter id**, if the blocking rule's expression names that string as a `parameter_id`, a `table_id`, or `link_coverage.empty.parameter.id`, or the string is the `id` of a resolved `parameter-declaration.v1`.
3. **Symbol or source-set name**, if the blocking rule `requires` it, refs it, collects it, counts it, or names it as a `source_set`, or it is a fact-type id in the resolved graph, and it is not a finding id in state.
4. **Finding id**, if the string is a finding id in `FindingState` or in the run's publications. This is the only lookup. Resolve to `findingId` plus the recorded fact id when state has one, otherwise the publication's symbol.
5. **Other recorded text.** The string is shown as text. It is not looked up, and it is not a projector failure. The classes below that are not 1–4 land here.

What the view shows:

| Class | Shown as | Not shown as |
| --- | --- | --- |
| Finding id | The finding id and the recorded fact id or symbol, so an uncovered link is named | A code alone |
| Diagnostic marker | The marker string, as the name of the block | A finding, a link name, or a school |
| Parameter id | The parameter id and, when the rule named a version, that version. No `origin` | A declared-default basis, a link, or a sentence |
| Symbol or source-set name | The symbol or source-set string | A finding |
| Other recorded text | The string | A finding. The projector does not parse a sentence out of it |

An uncovered link, an orphan reduction, a duplicate link map, a link with two reductions, and a non-numeric reduction are the same disposition code (`DEPENDENCY_INVALID`) and are distinguished by which finding ids are in `missing` and by the pins. **Production, coverage contract.** That is the identity table. No new record code.

### Inventory

**Production, `link_coverage` and per-subject dispatch.** These are the strings that operator can put in `missing`:

| Situation | Code | `missing` |
| --- | --- | --- |
| Name not installed in `keyed_sources` (ordinary `attempt`, not per-subject dispatch) | `DEPENDENCY_INVALID` | `link-coverage-scope-unbound` |
| Subject keys absent, or `_scope` returned `None` for either declared name | `DEPENDENCY_INVALID` | `link-coverage-keys-unavailable` |
| Present link rows share no key name with the subject, and every coverage slot is `[]` | `DEPENDENCY_INVALID` | `link-coverage-unjoinable` |
| Joined reduction's key map equals no joined link | `DEPENDENCY_INVALID` | That reduction's `finding_id`, sorted |
| Two joined links share a key map | `DEPENDENCY_INVALID` | Both links' `finding_id` values, sorted |
| One link matches two or more reductions | `DEPENDENCY_INVALID` | That link's `finding_id` |
| Matched reduction is not a number, including a boolean | `DEPENDENCY_INVALID` | That link's `finding_id` |
| A joined link has no reduction | `DEPENDENCY_INVALID` | That link's `finding_id`, sorted. Not the reduction symbol |
| Empty parameter absent | `DEPENDENCY_ABSENT` | The parameter id |
| Empty parameter version mismatch | `DEPENDENCY_INVALID` | The parameter id |
| A `requires` name with no joined source and no optional default | `DEPENDENCY_ABSENT` | The symbol name |
| More than one source joined for a required name | `DEPENDENCY_INVALID` | Each matched source's fact id, or its finding id when it has no fact id |

**Production, the rest of `evaluator.evaluate`.** The same disposition field can also carry: a `ref` name (`DEPENDENCY_ABSENT`); a `bound_sources` name (`DEPENDENCY_ABSENT`); a `collect` or `count` source-set id, or the collect name when the source set is omitted (`SOURCE_SET_UNCLOSED`); a `parameter_id` or `table_id` (`DEPENDENCY_ABSENT`); `"{parameter_id}[{key}]"` and `"no rows for key {key} in {id}"` (`LOOKUP_MISS`); `"{table_id}[{key}] @ {value}"` (`LOOKUP_MISS`); `"{name}.{field}"` (`DEPENDENCY_INVALID`); `"{left_domain} != {right_domain}"` and `"not a categorical expression: …"` (`CATEGORICAL_DOMAIN_MISMATCH`); the rejected category token (`DEPENDENCY_INVALID`); `"expected number, got boolean …"`, `"not a number: …"`, `"unknown rounding mode: …"`, `"division by zero"`, `"unknown op survived schema: …"` (`DEPENDENCY_INVALID`). A `block` op sets `missing` to `[]` and uses the rule's code (`SLI_MFS_INELIGIBLE`, `SLI_UNIVERSAL_COMPONENT_VIOLATION`, `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`, and any other code a rule declares). `conditional_dependency_set` repeats the absent members' own `missing` names.

**Production, runner rows that do not come from `EvalBlocked`.** `requires` names absent from `self.symbols`; `v9-declarative-binding-unauthorized`; `declarative-top-level-contract-invalid`; `selection-path-id-duplicate`; `selection-path-pin-contract-invalid`; `legacy-and-derived-nominee-both-present`; `tax.us.2025.interest.derived-nominee-subtotal`; a content refusal's own `missing` list; `"{part_id}:{adjustment kind}"`; pairing and nominee fact ids from those dispatchers. They are other recorded text or, when they are finding or fact ids present in state, the finding-id class. They are not markers.

The rule's own `blocked.missing` array is not this list. **Production.** The runner does not read it. The coverage rule's declared `missing: []` is not what the disposition carries.

## 5. The page

The page is `packages/presentation/pages/citation-walk.v1.html`. The walk change is also applied to `tools/presentation_harness/examples/pages/citation-walk.v1.html`, because the product page says a change to the walk belongs in both. The evaluation copy keeps its synthetic declaration. It is not the page this contract's test loads. `live_session` keeps refusing that copy.

`renderLine` stays the one render path for line 21: the worksheet amount or the block, the field's own `explain`, the leaf citation buttons, the field citation. Line 21 gains no statement rows and no new sentence. Other lines are unchanged. Nothing is added to the page header.

When `calculationView` is present, the page renders it once, next to line 21, because that is the deduction the person is examining. The view is not inside the line's value, and it is not rendered on any other line. While `integrated` is `false`, the view shows this chrome and nothing warmer: "Not Schedule 1 line 21. The worksheet does not read these figures." That sentence is page chrome, the same kind as the blocked banner. It is not a condition and not a wording field. Both page copies use that string. The page does not compute a sum of the groups and does not place a group value in line 21's value slot.

The conditions are not `role="alert"`. They do not use the blocked banner ("No value published — cannot compute.") or the remedy box. Those stay on a real blocked disposition of line 21 only. The conditions are not inputs, not checkboxes, and not questions. The explanation is a disclosure inside the calculation view: collapsed in the ordinary view, opened by a control on that view, containing only what the model copied.

Renderer-owned strings (`REASON_TEXT`, the blocked banner, the remedy sentence, `ATTACHMENT_EXPLAIN`) are not a home for the condition sentences. The page renders model text or it renders nothing.

The sentences below are the owner's candidates from stage 4, except where section 7 forbids the bare-statement claim. They are quoted so the page has a target. They are not an approval act. A1's single responsibility paragraph is not the text.

### Nine-credit

The person enrolled in the BSc and the certificate programme at Riverside in autumn 2024, nine credits, and a financing claim names the period. Line 21 shows the worksheet result only. The calculation view shows the statement amount, its leaf citations, and the status node. The nine-credit telling is an examined input of that status node, not the ground of the amount and not the ground of eligible-student.

The disclosure shows three conditions, each distinguishable from an ordinary citation button by being a responsibility row (rule id and keyed symbol), not a line-21 `citationSites` entry:

> You are responsible for these conditions: that Riverside College was an eligible institution; that the programme you were pursuing led to a recognised credential; and that your course load met Riverside's half-time standard for that programme. They apply because you claimed the student loan interest deduction for [statement] and described enrolling at Riverside College in autumn 2024.

The circumstance named is the one the finding pinned (institution, programme, period). The treatment is the statement amount the reverse walk attached, not the worksheet dollar. `basisOrigin` on the status node is shown as the default basis when an input pin has `origin: declared_default`. The case-2 note is not used. Nine credits are not stated as having met the half-time standard. The no-link parameter is not this basis.

### Financing claim, no schooling circumstance

The person said only that this loan paid tuition for the Riverside BSc in autumn 2024. Same split: line 21 is the worksheet; the view is the statement. The disclosure uses the case-1 candidate:

> You are responsible for these conditions: that Riverside College was an eligible institution; that the BSc led to a recognised credential; and that your course load met Riverside's half-time standard. They apply because you claimed the student loan interest deduction for [statement] and said this loan paid for the Riverside BSc in autumn 2024.

The because-clause must not say the person described studying or enrolling. The financing claim remains a citation of what was said. It is not labeled as enrolment and not labeled as the ground of eligible-student. The default basis is the status node's `basisOrigin`, not the case-2 note, and not a parameter pin.

### Bare statement

Nothing joined this subject to a link. Line 21 is unchanged. The calculation view shows the statement amount and this note, and no other new sentence, and only when section 7's guard held and the conclusion rule declared the note:

> Eligibility for this deduction is taken as met because nothing you've described says otherwise.

That note is the eligibility default. It is not a description of the no-link parameter. The three conditions are not in the view's ordinary text. They are in the disclosure, and only from the bare-statement rules' own fields. The stage-4 sentence that ends "nothing you've described names them" is not the text this guard supports. Section 7 says what the sentence is allowed to claim. The statement is named from the group's `factId`. No institution and no programme are named. "Not known" appears only when the copied rule field says it, and only under that guard.

### Uncovered link

The statement row in the view is blocked. Line 21 is whatever the worksheet did with raw box 1; this contract does not define that interaction, because the worksheet does not read the block. The view shows the code, and it shows each finding-id `missing` entry's recorded identity, so the link is named. Orphan, duplicate, and non-numeric do not render the same text, because their `missing` lists differ. A marker, a parameter id, or a symbol name is shown as section 4 says, not as a link. No responsibility rows are shown: a treatment that was not taken has no responsibility on it. The blocked banner is appropriate on this row and is not the condition register.

### No-link parameter

The statement amount is published. Box 1 remains a citation. The parameter pin is visible on the group as role `parameter`, id, and version, with no `origin` and no `basisOrigin`. It is not left only inside an embedded act. This is the coverage quantity (nothing joined to reduce), not the eligibility default and not the bare-statement note. When section 7's guard also holds, the note of that case is shown from the conclusion rule, not from this pin. The page does not treat "no link" as "school unknown".

## 6. Where strings come from

### What the projector may copy today

**Production.** Every string that reaches the model is one of the following. Nothing else is a governed source.

| Source | Where it lands | The page reads it |
| --- | --- | --- |
| Form-field citizen, copied whole onto `section.field` (`form-field.v2` / `v3`) | `label`, `description`, `line`, `form.*`, `citation` id and version, each disposition's `render`, `explain`, and blocked `codes` | `label`, `line`, `render`, `explain`, `codes`, field `citation`. Not `description` |
| Evidence `label` (`evidence.v1`) | `pinLabels`, via `_evidence_label` | Citation button text. Absent label falls back to `pinId@pinVersion` |
| Attachment title (`attachment-rule` `title`) | Attachment status and citation-group `title` | Yes |
| Itemization `label`, adjustment `label` | Part `heading`, citation `context` | Yes, as heading |
| Published numeric `value` | `resolved.value` | Yes, through `{value}` |
| Published categorical `value` | Compared to the field's `render`, then stored only inside `resolved.act`. The page is required not to read it | No. The instruction `render` is shown instead |
| Adjustment row `label`, `kind`, `row_sum`, and the derived finding `value` | Citation-group tie-out text and `provenanceGroups` | Tie-out text on a citation group only. The page does not read `provenanceGroups` |
| Fact-type `title`, and the unsupported finding's `value` | `unsupportedSourceFindings` | No |
| Authorization provenance | Optional top-level `authorization` | No |

Two further strings are composed by the projector, not copied from a citizen: `_reader_label_for_finding` (`{adjustment label} — {payer}` or `{adjustment label} report group`) and the tie-out templates (`Reported subtotal: {value}`, `Adjustment: -{row_sum}`, `Recorded contributing reduction {value}`). Both serve the attachment path. They are not a wording mechanism to extend.

`citation.v1` is resolved and then dropped. Its `authority.title` and `section` never reach the model. `rule-artifact` `notes` is not read. A parameter id is not a sentence. A parameter's `values` is not copied.

### Human text that exists and is not a source

| Citizen | Human text | Why it is not the condition message |
| --- | --- | --- |
| `form-field.v3` `description` and disposition `explain` | One string per line. Line 21's `explain` talks about worksheet eligibility, MAGI, and an unclosed box-1 family | One text for every return. Cannot name Riverside on one statement and a bare statement on another. The line's `explain` stays the worksheet's |
| `rule-artifact.v10` `notes` | Free developer text. The schema does not govern it as wording | The projector does not copy it. Stage 4 already rejected it |
| `citation.v1` | A locator | No message. One locator can stand for two conditions |
| `fact-type` `title` | Developer description | A fact type types an assertion. The projector copies `title` only onto `unsupportedSourceFindings` |
| `evidence.v1` `label` and `content` | The person's evidence | Not a condition. Only `label` is copied, and only onto `pinLabels` |
| `parameter-declaration.v1` `values` | An open JSON value. The evaluator's `parameter` op decimalizes it | A sentence does not survive evaluation. Section 8 |
| `entry-field.v1` | Prompts and refusals | This projector does not read it. This page must not become an entry loop |

Page constants are not content. Adding the candidates to `REASON_TEXT` or to a new frozen object in the HTML would put owner-approved tax wording in two page copies, outside content governance. The chrome sentence in section 5 is not a precedent for these sentences.

## 7. How the bare-statement case is selected

**Contract.** The bare-statement rules publish only when a count rule published 0 for that subject by the parameter path. Absence of a school pin is not the guard. A blocked count is not the guard.

The count rule is a per-statement rule. Its value is one `link_coverage` over the link type and a presence-marker symbol, with empty parameter 0. A per-link rule publishes the decimal 1 for every current link, with that link's keys, one publication per link. **Production, operator.** `link_coverage` returns a decimal or blocks. It returns the parameter only when the subject's scope is bound, the subject's own keys are present, both joined lists are empty, and no present link row is unjoinable. It returns the sum only when every joined link has exactly one numeric match and every match has a link. Every other case blocks, and none of them fall through to the parameter.

If every marker is the decimal 1, the sum equals the number of joined links. The published value is 0 only on the parameter path. A marker of 0 would make a sum of 0 while a link exists, so the guard is not the value alone. The guard is all three:

- the count finding is published and its value is 0,
- that finding has a parameter pin for the empty parameter, and
- that finding has no input pin of a link or a marker.

**Production, and why the blocks are not a bare statement.** Unjoinable (`link-coverage-unjoinable`) is raised by dispatch before `value`, only when present link rows share no key name and every coverage slot is `[]`. Keys unavailable (`link-coverage-keys-unavailable`) is the sentinel, including a subject whose own keys are absent; that subject never takes the parameter. Scope unbound (`link-coverage-scope-unbound`) is ordinary `attempt`, which never installs the slot. An orphan marker, a duplicate link map, two markers for one link, a non-numeric marker, and a link whose marker did not publish all block with finding ids. The count symbol is then not published. The bare-statement rule `requires` the count symbol and compares the published finding as above. A missing count is `DEPENDENCY_ABSENT` of that symbol, not a 0, and the rule must not declare an `optional_default` for it. Those blocks show in the view as section 4. They do not show the bare-statement sentence.

**The condition this selects is "no link joined to this dispatch subject."** It is not "no schooling information in the workspace." An enrolment or a financing claim can sit in the workspace with no link to this subject; the count rule does not read those fact types, and the parameter path still returns 0. A link that shares a key name but not the value is also this path: **production, ADR 0075,** a shared name whose values disagree is a join of nothing, and the parameter is returned. Zero link rows are this path too, and joinability of a type with no rows is not observable. The operator also does not prove the joined list is this statement's; a shared key name such as tax year can join one link to two statements. That proof is ADR 0076. Until it is accepted, a 0 is not a statement-specific claim, and the page must not present the sentence as one. The view may show the count rule's id, version, value, and pins.

**What the wording must claim.** The sentence may claim that no current link joined to this subject. It must not claim "nothing you've described names them," because a description can be present and unlinked, and because a key-name mismatch is not a description of nothing. "Nothing connects these loans to a school" is still stronger than the operator: "these loans" and "this statement" wait on ADR 0076, and "a school" is not what the count reads. The words are the owner's. The rule field must be written to the claim the guard actually establishes, not to the stage-4 sentence, unless the owner accepts that overclaim in those words.

When the count is not the parameter path, the bare-statement rules do not publish, so their text cannot appear. That is what keeps "school not known" off a statement that has a joined link. Schooling that is present and not linked does not suppress the sentence. The sentence is not allowed to pretend it did.

Situation-scoped rules, for the nine-credit case and the financing-claim case, publish from the circumstance they pin. They do not publish on the parameter path. They are not selected by a missing school pin either.

## 8. The wording home

The wording **pin role** is withdrawn everywhere. `derived-finding.v2` and `derivation-record.v9` do not gain it. Findings do not pin a wording citizen. The projector does not look for a pin of role `wording`.

If the sentence is declared on a rule, this is how it reaches the projector. No pin carries it.

- The case is which rule published. The bare-statement rule, the financing-claim rule, and the described-enrolment rule are different rules. Each declares one sentence. The projector does not choose among sentences.
- The disposition row's `artifact_id` is the rule id. `build_presentation_model` already indexes the resolved graph by id. The projector reads that rule object, the rule that ran, not a copy with a rewritten `publishes`.
- The content version is that rule's `version`. The group stores it as `ruleVersion`. A sentence change is a new version of that rule.
- The field name on the rule successor is `wording` (the condition sentence) or `lineNote` (the ordinary-line note on the favourable-conclusion rule only). Both are strings. `notes` is not read. A rule with neither field contributes identity only: rule id, version, symbol, and no sentence.
- Slot rule. The projector replaces `{statement}`, `{institution}`, `{programme}`, or `{period}` only with a key on a fact an input pin of that finding names, or, for `{statement}` only, with the keyed symbol's fact-id suffix. A missing key fails the projection. It does not become "unknown", an empty string, or a placeholder. A bare-statement field has no institution, programme, or period slot.

### Compared

**(a) A `parameter-declaration.v1` whose `values` is the sentence, pinned with role `parameter`.** **Production.** `values` is open, so a string is schema-valid. The only way a parameter reaches a finding's pins is a successful `parameter` read: `access.parameters`, then `pins_for`. That read calls `_as_decimal`. A sentence blocks `DEPENDENCY_INVALID` with `missing` `not a number: …`. The pin is then never written. The hypothesis that this "reaches the finding's pins today" is false for prose. What is right about it: no new citizen kind, and a numeric parameter's id and version are already a pin. What is wrong: the evaluator treats `values` as a quantity; this would put prose in the same role as the no-link parameter, which section 3 forbids dressing as eligibility; one parameter is one value, not a case chosen by a guard; the projector does not copy `values` today. Not the home.

**(b) A form-field successor carrying per-case text.** **Production.** `form-field.v3` has one `description` and one `explain` per disposition, `additionalProperties: false`. A successor could add a map without editing v3. The grain is still one field per form line. The case is a per-statement derivation result. The field would hold every sentence and the projector would pick one, which is composition, not a copy. The line's `explain` would still be the wrong surface for a sentence that must not sit on every return. Not the home.

**(c) A new wording citizen referenced from a rule-schema successor.** This works. The rule successor holds `{id, version}`, the projector loads that citizen from the rule it already resolved, and the sentence can version without a new rule version. The cost is a new published schema plus the reference field. These sentences are not shared. Each case is its own rule, and that rule's version is already the content version. A second version axis is not earned. Not this contract. Do not publish `condition-wording.v1`.

**(d) The consumer.** The page or the projector holds the sentences, keyed by rule id. No schema. It fails the projector's copy rule and the page's zero-authority rule. The sentence would live in two HTML copies. A model with no declaration could still show it. Not the home.

**Contract. Recommendation: the rule field in the first half of this section.** The rule successor is the one ADR 0076 already requires for `subject`. Adding `wording` and `lineNote` there does not force a further rule version and does not force a new citizen. `rule-artifact.v10` has `additionalProperties: false` and cannot gain the fields. Until the successor exists, the view carries identity and no sentence. That state is not a completed reader case.

## 9. The statement-scoped responsibility rule

Three rules, one per condition, for the bare-statement case only. The probe rule `demo.rule.responsibility-eligible-institution` is not this rule. **Prior probe.** That rule publishes when status is `not-adverse`, its subject in P4 was the financing claim, and with subject box 1 it blocked `DEPENDENCY_ABSENT` because it requires status. Status sources are keyed to financing claims. Requiring status is what makes the bare statement unable to publish.

### Subject

The subject is the statement fact type `tax.us.2025.f1098e.box1-student-loan-interest` (identity keys lender, statement, tax-year). Not a financing claim, not an enrolment, not a run-wide box-1 scalar. The subject declaration is ADR 0076. Until that binding is accepted, section 7's sentence is not shown as a claim about this statement.

### What it reads

- The count finding of section 7, and it publishes only when that finding is the parameter path. That is the guard.
- The current box-1 finding for that statement. That is the asserted input that establishes the subject. Origin `assertion` on that input pin.
- The published per-statement amount finding for that same statement. That is the treatment. The amount rule does not read the responsibility. The responsibility is not an input of the amount. The worksheet does not read either of them.
- Its own citations, this condition's authorities only.

It does not read enrolment, a financing claim, a school, a programme, a period, or a status finding. It does not read the absence of any of those. It does not read the no-link parameter as an eligibility input.

### What it publishes

One categorical finding per statement, and only when the guard holds. Symbol is the unsuffixed condition symbol plus `|` plus the statement fact id. The value is a declared applicability token, not the prose. The rule's `wording` field is the sentence section 7 allows. A value of `applies` with no `wording` field does not say the school is unknown, and the projector must not complete the sentence.

Nothing consumes the finding. It lapses when the favourable treatment it rests on is not published.

### What it pins

- The statement's box-1 finding, role `input`, origin `assertion`.
- The count finding, role `input`, origin `assertion`.
- The per-statement amount finding, role `input`, so the reverse walk attaches the responsibility to that statement's group.
- Citation pins for this condition only.

It does not pin an institution, a programme, a period, a financing claim, or an enrolment. It does not pin a wording citizen. It does not pin the no-link parameter, and it does not put `origin` on a parameter pin. It does not pin a sentinel that means "unknown" by being absent.

The ordinary-line note is not this rule's field. The statement-keyed favourable conclusion declares `lineNote`. The conclusion's input is the statement's box-1 finding, so the conclusion has an asserted input. Its `basisOrigin` is `declared_default` only when one of its input pins has that origin. The no-link parameter never supplies it.

### Which scheduling it needs

ADR 0076, the subject declaration on the rule successor. Not a package-level map, and not a Python id list. The same successor admits `wording` and `lineNote`. It does not admit a pin role `wording`.

What that scheduling has to provide for this rule:

- A required `subject` on the rule successor, an exact fact-type pin to `tax.us.2025.f1098e.box1-student-loan-interest`.
- The package successor that admits that rule schema.
- Eligibility waits on predecessor **rule resolution**, not on the unsuffixed symbol appearing in `self.symbols`. The predecessor of the responsibility rule is the count rule and the per-statement amount rule. It is not the schooling-status rule, and it is not the worksheet. Keyed publication never inserts the unsuffixed name, so a `requires` entry of that name stays ineligible and `finalize_unreached` would then evaluate the rule once, unsuffixed.
- The intercept is on `attempt` and on `finalize_unreached`, so `runner._execute` and `reference_runner.run_reference` share it.
- One dispatch publishes per statement. The rule id resolving once must not collapse the three statements into one unsuffixed finding, and must not block every statement because one amount was blocked. A statement whose amount is blocked, or whose count is blocked, gets no responsibility finding. The other statements still publish.
- The count rule and the amount rule are `link_coverage` rules. The responsibility rules are not. They do not join links. ADR 0076's link-binding half still gates any sentence that says "this statement": until a joined link is this statement's, a coverage result is not a statement-specific claim. The rule's own grain does not depend on a shared key name with a link type.

Situation-scoped responsibility rules stay per schooling situation. Their subject is that situation, and their pins name the institution, programme, and period. They are not this bare-statement rule. They carry their own `wording` field, the named-circumstance sentence, and the same reverse walk. They do not publish when section 7's guard holds.

## 10. The demonstration standard

P4 inspected `build_presentation_model`'s return value while the run object was still in hand, and it did not load the page. That does not satisfy this contract. **Prior probe.**

The test does all of the following.

1. Run the bare-statement case, the nine-credit case, the financing-claim case, an uncovered link, and a no-link parameter through the real writers. The live path already writes `outputs/<stem>.presentation.json` from `build_presentation_model` before it returns. The runs are hand-assembled. They are not a production schedule, and the test says so.
2. Discard the run result, the publications, the dispositions, and any in-memory model. The rest of the test may hold the path of the presentation file and nothing else from the run.
3. Read that file back from disk. `validate_presentation_model` on the reloaded JSON is allowed. It is not the page proof.
4. Load the product page. Read `packages/presentation/pages/citation-walk.v1.html`. Replace `__MODEL_JSON__` with the file bytes, which is the splice `live_session` performs (`const MODEL = Object.freeze(__MODEL_JSON__);`). Serve that one document on the harness loopback and open it in a fresh Chrome target, the way `tools/presentation_harness/lib/executor.mjs` loads a candidate.
5. The harness server today splices only `__FIXTURE_JSON__`, and only into the evaluation page. The test must splice the product page's token. The fixture bytes are the re-read presentation file, not a hand-written golden and not the evaluation copy.
6. Assert with the harness check `dom-text-present`. Line 21's value is the worksheet figure when the worksheet ran, and it is never a statement group's value. The calculation view's text includes the sentence the case requires and excludes the sentences this document forbids, including "nothing you've described names them" unless the owner has put that sentence in the rule field despite section 7. Assert the disclosure control is inside the calculation view and that no form line contains the note or the conditions. Assert the conditions have no `role="alert"` and no input control. Assert an uncovered link's text names that link and differs from the other three invalid shapes. Assert a marker, a parameter id, and a symbol name are shown as themselves and are not presented as findings. Assert a model with no `wording` field does not contain the sentence. Assert a model whose finding pinned no school does not contain "not known" or "unknown" unless the bare-statement guard held and the copied field says it. Assert the no-link parameter pin has no `origin` and no `basisOrigin`, and that the eligibility note is absent when the only pin of that kind is the parameter. Assert `integrated` is false and the chrome sentence is present. Assert line 21's section has no statement rows.

A passing structural check on the Python object, or a passing check on the evaluation page, is not this demonstration.

Out of scope for the demonstration: the full `pytest` suite as a substitute for the page load; a second derivation from the closing record; `explain()`; personal or live workspace data; approving the candidate sentences; a production schedule of the per-subject chain.

## 11. Limitations and completion

`derivation-record.v9` does not retain intermediate values. **Production.** A closing record written with `use_v2=True` stores pins and dispositions. It does not store `published`, `blocked`, or `value`. `out.json` stores dispositions and no findings. The values this page shows — the worksheet amount, a statement amount, a reduction, a status, the applicability token — are in `presentation.json` only because the projector copied them from memory while it built that file. A reader that ignores `presentation.json` and reads the record cannot show them. Identity joins (which link, which status, which responsibility, whether an input pin is `declared_default`, whether a pin is a parameter) remain on the record. This contract does not add a record version to move the values. The demonstration is void if the page was explained by re-reading the run object.

The presentation file is not a reconstruction. If it is deleted, the page is not rebuilt from the record under this contract. Deleting it also loses the copied sentences: they are not on the record.

**Production, restated.** None of the per-subject chain is production-scheduled. A green demonstration is evidence about the writers and the page, not evidence that a production run publishes these rows.

Completion. All of these are required. Any one missing means the reader case is not complete.

1. Line 21 still binds `tax.us.2025.schedule1.line21-sli-deduction`. The calculation view is present for the per-statement chain, `integrated` is false, and the page does not present the groups as the line.
2. The no-link parameter is shown as a parameter pin with no `origin`. A declared-default eligibility input is shown only where an input pin has that origin. The page never assigns the parameter that origin.
3. Blocked `missing` entries are classified as section 4. Only finding ids are resolved. The four invalid link shapes do not render as the same text.
4. The bare-statement rules have run under section 7's guard, published keyed findings, carried the sentence on the rule rather than on a pin, and not pinned a school. The sentence claims no more than the guard establishes.
5. The reloaded `presentation.json` contains the calculation view, the kept intermediate nodes, classified `missing`, `basisOrigin` only from input pins, and the responsibility rows from the reverse walk.
6. The product citation-walk page, loaded from that file after the run object was discarded, shows line 21 as the worksheet and the five cases of section 5 in the calculation view.
7. A projection that sees a missing school pin, a missing link, or a parameter pin, and does not have the bare-statement rule's field under section 7's guard, does not render the school as unknown.

Not this contract: ADR 0076's full link-binding decision, the worksheet successor that would set `integrated` true, the legal-obligation consumer, the partial-reduction remainder, entry-loop questions, a change to the incumbent eligibility witnesses, `condition-wording.v1`, a wording pin role, and any edit to an existing published schema file.
