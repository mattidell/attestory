# Bounded reader contract — statement calculation beside Schedule 1 line 21

> **Revision (2026-09-24).** Replaces the draft at
> `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/reader-contract-draft.md`.
> The draft's wording **pin role** stays withdrawn, and so does the draft's further step of a new
> `condition-wording.v1` pinned by that role. Line 21 is not retargeted. Two recommendations below:
> per-statement rows are a separate calculation view until a worksheet successor reads them, and
> the sentence lives as a field on the **second** rule successor (see ADR 0076's publication plan):
> the first successor carries `subject`, `joined` and `direction` only.
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
| `factId` | The suffix after `\|`. An **identifier** for joining rows, never displayed as the statement's name and never parsed |
| `statementLabel` | The statement's user-facing name, from **structured recorded information** only — see "The statement label" below. Absent when no label is recorded |
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
| `statementOutcome` | This statement's own `route`, `statementScope` and `conclusion` interpretations (section 9), each retaining its producer's rule id, original disposition and available finding/pins or classified `missing`. No row means `not-computed`, not an invented block. `statementScope` retains the examined claims and any recorded classifications, with a label only where recorded. `responsibilityFailures` is an array of the residual producer diagnostics described below, empty when none apply |

`citationSites` on the **line 21 section** stay the worksheet's leaves. They are not rebuilt from the view. The view does not contribute a number to the line. The amount's number stays inside the group.

### Reverse walk

After the downward nodes of a group are known, consider only **published findings of rules that declare
`reader_role: responsibility`** (section 8, "Which producers the reader explains"). Attach one when its
input pin names the group's amount finding or an intermediate derived finding in that amount's dependency
chain. Sharing an ordinary source leaf, such as box 1, is not sufficient. Do not repeat the walk outward
through newly attached responsibilities.

Pin reach associates a declared responsibility with the calculation; it does not define which rules are
responsibility producers. The probe's count and whole-disqualifier count share box 1 with the amount; its
extra-consumer test also executes an amount-reading rule with no responsibility declaration. Neither
relationship alone selects an intended responsibility; the declared `reader_role` does. `wording` supplies the
sentence and is not what identifies the producer: a responsibility rule without `wording` is still a
responsibility, and shows its identity with no sentence. The downward walk alone does not find the
responsibility findings. **Prior probe.** P4 showed nothing on the amount's pin list is the responsibility.

A responsibility row carries `ruleId`, `ruleVersion`, keyed `symbol`, `findingId`, categorical `value`, and its pins. It carries `wording` only by the copy in section 8. The row is not a citation site of line 21 and is not fed through the field's citation chain.

Blocked or inapplicable producers supply no responsibility finding, categorical value, or condition sentence.
**Every** blocked responsibility disposition for this statement is kept in
`statementOutcome.responsibilityFailures` — rule id, keyed symbol, code and classified `missing`, as recorded.
Each entry also carries `explainedBy`: for each `missing` symbol, the outcome-line entry that displays that
symbol's own producer outcome **for this statement** (section 9), or nothing. An entry is **displayed** unless
every one of its `missing` symbols has an `explainedBy` entry that is itself displayed; only then is it
redundant, and it is still in the model. A code other than `DEPENDENCY_ABSENT`, a `missing` entry that is not a
symbol, or a symbol whose producer's outcome is not on this statement's line is never suppressed. Do not
attach a disposition merely because it shares a rule family, a tax year, or an absent pin.

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
- `statementOutcome` is required on every group. Each axis carries its producer's rule id, declared
  `reader_role`, original disposition and evidence, alongside the interpretation in section 9. `missing`
  belongs only to a blocked row; an inapplicable row retains its pins but has no finding id. `not-computed`
  means there is no row. `conclusion: published` requires `route: bare` and `statementScope:
  no-whole-amount-disqualifier`. Non-empty bare-statement `responsibilities` or a `lineNote` require
  `conclusion: published`. `responsibilityFailures` contains diagnostics, never applicability findings or
  condition text; an entry marked redundant must name, for every `missing` symbol, a displayed outcome entry.

**What the validator can and cannot establish.** `validate_presentation_model` sees one model and nothing else.
It checks **shape and internal consistency** — the rules above. It cannot check that an axis equals what the
run recorded, that a finding id is the run's, that no disposition was left out, or that a value was copied
rather than computed. Those are **projection-fidelity** obligations, tested separately with the run in hand
(section 10, "Projection fidelity"). A model that passes the validator is well-formed, not faithful.
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

Those two pins must stay distinct in the model and on the page. This contract's bare-statement path declares
no `optional_default` (section 9); the right-hand column describes production behaviour the page must still
classify correctly wherever such a pin appears, not an input this contract relies on.

| | No-link parameter | Declared-default eligibility |
| --- | --- | --- |
| Where it sits | On the amount finding, role `parameter` | On the consumer, role `input`, id = the default finding |
| `origin` | Absent. Assigning one is a validator failure | `declared_default`, copied from the input pin |
| `resolved_input` | Absent on the amount | Present on the default finding, not on the amount |
| What it means | The reduction total when both joined lists are empty. A quantity | The favourable input was taken from a declared default |
| Page | The pin is shown as a parameter: id and version, no basis | `basisOrigin: declared_default` on the node that pinned the default finding |
| Sentence | Does not by itself authorize the ordinary-line note | The note is copied only from the conclusion rule's own field, and only when that rule published |

`basisOrigin` on a node is the `origin` of an input pin on that finding, and nothing else. It is never computed by noticing which pins are missing, and it is never copied off a parameter pin. The eligibility note (section 5) is not the no-link parameter and is not composed from `declared_default`. It appears only as `lineNote`, copied from the named conclusion's rule, and only when a published responsibility finding for that statement pins that conclusion (section 9). The note's default basis is the conclusion's identity; the conclusion's own `basisOrigin` is `assertion`, meaning only "not reached through a declared default".

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

An uncovered link, an orphan reduction, a duplicate link map, a link with two reductions, and a non-numeric
reduction share `DEPENDENCY_INVALID`. The identity table below identifies the affected rows, not a unique
reason for failure. In particular, duplicate reductions and a non-numeric reduction for the same link emit
identical code, `missing` **and pins**. The reader may name the affected link and report an unresolved
calculation; it cannot infer which of those defects occurred. `packages/derivation/evaluator.py`'s
`_link_coverage` reads key maps, finding ids and reduction values; `subject_dispatch._assemble_pins` carries
the access log and subject into the blocked result. The injected-source cases in
`test_duplicate_and_nonnumeric_classifications_have_identical_block_evidence` execute these consumers.
No new record code or diagnostic carrier is selected here.

### Inventory

**Production, `link_coverage` and per-subject dispatch.** These are the strings that operator can put in `missing`:

| Situation | Code | `missing` |
| --- | --- | --- |
| Name not installed in `keyed_sources` (ordinary `attempt`, not per-subject dispatch) | `DEPENDENCY_INVALID` | `link-coverage-scope-unbound` |
| Subject keys absent, or `_scope` returned `None` for either declared name — **only on the path that reaches `value`**; if the `requires` walk blocks first (a required name `None` → `DEPENDENCY_INVALID` naming it; a required name with no joined source → `DEPENDENCY_ABSENT` of that symbol, even when the subject's keys are absent), the marker is not emitted | `DEPENDENCY_INVALID` | `link-coverage-keys-unavailable` |
| Present link rows share no key name with the subject, and every coverage slot is `[]` | `DEPENDENCY_INVALID` | `link-coverage-unjoinable` |
| Joined reduction's key map equals no joined link | `DEPENDENCY_INVALID` | That reduction's `finding_id`, sorted |
| Two joined links share a key map | `DEPENDENCY_INVALID` | Both links' `finding_id` values, sorted |
| One link matches two or more reductions | `DEPENDENCY_INVALID` | That link's `finding_id` |
| Matched reduction is not a number, including a boolean | `DEPENDENCY_INVALID` | That link's `finding_id` |
| A joined link has no reduction | `DEPENDENCY_INVALID` | That link's `finding_id`, sorted. Not the reduction symbol |
| Empty parameter absent | `DEPENDENCY_ABSENT` | The parameter id |
| Empty parameter version mismatch | `DEPENDENCY_INVALID` | The parameter id |
| A `requires` name with no joined source and no optional default | `DEPENDENCY_ABSENT` | The symbol name |
| More than one source joined for a required name, **with disagreeing values** | `DEPENDENCY_INVALID` | Each matched source's fact id, or its finding id when it has no fact id |
| More than one source joined for a required name, **with agreeing values** | — not a block | `_one_source` publishes with the sort-first source (by finding id); neither id is in `missing` (`test_two_statuses_for_one_borrowing_agree_and_sort_first_publishes`) |

**Production, the rest of `evaluator.evaluate`.** The same disposition field can also carry: a `ref` name (`DEPENDENCY_ABSENT`); a `bound_sources` name (`DEPENDENCY_ABSENT`); a `collect` or `count` source-set id, or the collect name when the source set is omitted (`SOURCE_SET_UNCLOSED`); a `parameter_id` or `table_id` (`DEPENDENCY_ABSENT`); `f"{parameter_id}[{key!r}]"` and `f"no rows for key {key!r} in {id}"`, and `f"{table_id}[{key}] @ {value}"` — evaluator category `LOOKUP_MISS`, which is **not** in `RECORD_CODES` or the `derivation-record.v9` code enum, so the **disposition code is `DEPENDENCY_INVALID`** with the string kept in `missing` (a key `single` appears as `some.parameter['single']`); `"{name}.{field}"` (`DEPENDENCY_INVALID`); `"{left_domain} != {right_domain}"` and `"not a categorical expression: …"` (`CATEGORICAL_DOMAIN_MISMATCH`); the rejected category token (`DEPENDENCY_INVALID`); `"expected number, got boolean …"`, `"not a number: …"`, `"unknown rounding mode: …"`, `"division by zero"`, `"unknown op survived schema: …"` (`DEPENDENCY_INVALID`). A `block` op sets `missing` to `[]` and uses the rule's code (`SLI_MFS_INELIGIBLE`, `SLI_UNIVERSAL_COMPONENT_VIOLATION`, `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`, and any other code a rule declares). `conditional_dependency_set` repeats the absent members' own `missing` names.

**Production, runner rows that do not come from `EvalBlocked`.** `requires` names absent from `self.symbols`; `v9-declarative-binding-unauthorized`; `declarative-top-level-contract-invalid`; `selection-path-id-duplicate`; `selection-path-pin-contract-invalid`; `legacy-and-derived-nominee-both-present`; `tax.us.2025.interest.derived-nominee-subtotal`; a content refusal's own `missing` list; `"{part_id}:{adjustment kind}"`; pairing and nominee fact ids from those dispatchers. They are other recorded text or, when they are finding or fact ids present in state, the finding-id class. They are not markers.

The rule's own `blocked.missing` array is not this list. **Production.** The runner does not read it. The coverage rule's declared `missing: []` is not what the disposition carries.

### The statement label

The Form 1098-E statement fact is keyed on two **entity** keys and a literal: `lender` (entity kind
`tax.us.student-loan-lender`), `statement` (entity kind `tax.us.1098e-statement`), and `tax-year`
(`f1098e.bundle.json`). Entities are recorded with a `label` (`entity.v1`: `id`, `kind`, `label`), introduced
by an `entity-introduced` act. **Production, kernel.**

The projector builds `statementLabel` from those records:

1. Take the statement subject's box-1 fact from recorded state and read its **structured identity keys**
   from the kernel lattice — the entity ids for `lender` and `statement`, and the `tax-year` value. Never
   split, parse or display the rendered fact id or the symbol suffix to get them.
2. Look up each entity id in recorded entity state and copy its `label`. `statementLabel` is the three
   structured parts — `{lender: <label>, statement: <label>, taxYear: <value>}` — and the page renders them
   as fields, not as a sentence the projector composes.
3. If an entity has no recorded label, or a superseded entity is all that remains, that part is **absent**.
   The page shows its own chrome ("statement name not recorded") for the missing part. It does not fall back
   to the fact id, the entity id, or the evidence label's free text.
4. The box-1 finding's evidence `label` stays a **citation** label, as today. It is not the statement's name.

**Proposed contract.** Whether the lender and statement entities for real 1098-E statements carry labels
worth showing depends on the entity-introduction path (`report_statement_identity` and the entry loop); this
contract requires the projector to use them, and records "not recorded" honestly where they are absent.

## 5. The page

**The product page is unchanged.** `packages/presentation/pages/citation-walk.v1.html` and its evaluation copy
are not edited by this contract. The product page reads only `MODEL.sections`, `citationGroups`, `pinLabels`,
`attachments`, and `diagnostics`, so a model that carries `calculationView` renders on it exactly as before,
with no view. `live_session` serves only that fixed path (`PAGE_RELATIVE_PATH`), so a person on the real
return never sees the view.

**The experimental surface** is a new page beside the evaluation copy,
`tools/presentation_harness/examples/pages/statement-calculation.experimental.v1.html` (name proposed). It
reads its model from `__FIXTURE_JSON__`, which the harness server already splices, so no server change. It
declares itself synthetic with the marker `live_session` refuses on (`synthetic demo-*`), so it cannot be
served live even if the path constant were pointed at it. It shows line 21's section read-only from the same
model (the worksheet amount or the block, no statement rows, no new sentence) and, separately, the calculation
view.

**Where the view is shown: the owner chose B (experimental reader surface only)** (see "Owner choice: where
the unintegrated calculation is shown" below). Whichever surface is chosen: the view is not inside line 21's
value, is not rendered on any other line, does not sum the groups, does not put a group value in line 21's
value slot, and while `integrated` is `false` carries the chrome "Not Schedule 1 line 21. The worksheet does
not read these figures." — page chrome, not a condition and not a wording field.

### Owner choice: where the unintegrated calculation is shown

- **A — on the product page now, beside the real Schedule 1 line 21, labelled as not used by the worksheet.**
  The person examining their deduction sees the per-statement explanation in context. Risk: a figure that
  looks like a deduction sits next to the real one while the worksheet does not use it, the chain is not
  production-scheduled, and ADR 0076's binding is not accepted — so the figure is not yet a
  statement-specific claim. The label has to carry all of that.
- **B — only on an experimental reader surface until worksheet integration.** The product page is unchanged;
  the view is demonstrated on a separate surface. Nothing a person reads on the real return shows an
  unintegrated figure. Cost: the owner's demonstration standard ("the actual citation-walk page") is met on
  the experimental surface for now, and on the product page only after integration.

**Owner's choice: B (2026-09-24).** The per-statement calculation is shown only on an experimental reader
surface until worksheet integration; the product citation-walk page is unchanged by this contract, and the
demonstration standard is met on the experimental surface. Reasoning at the time of the choice: the figure is not yet something the product stands behind
(unscheduled, unbound, unintegrated), and a label is a weak guard beside a real tax line. The demonstration
standard applies unchanged to whichever surface is chosen: reload the durable file after the run is gone,
splice it into that page, load it through the harness.

The conditions are not `role="alert"`. They do not use the blocked banner ("No value published — cannot compute.") or the remedy box. Those stay on a real blocked disposition of line 21 only. The conditions are not inputs, not checkboxes, and not questions. The explanation is a disclosure inside the calculation view: collapsed in the ordinary view, opened by a control on that view, containing only what the model copied.

Renderer-owned strings (`REASON_TEXT`, the blocked banner, the remedy sentence, `ATTACHMENT_EXPLAIN`) are not a home for the condition sentences. The page renders model text or it renders nothing.

The sentences below are the owner's candidates from stage 4, revised where they claimed more than the view establishes. They are quoted so the page has a target. They are not an approval act. A1's single responsibility paragraph is not the text.

**What the view establishes, and so what a sentence may say.** It establishes that this calculation computed a
per-statement amount, and which circumstance or default the amount's findings pinned. It does not establish
that the person claimed the deduction, that anything was filed, or that a condition was checked: line 21 is
the worksheet's, the view is read-only and unintegrated, and nothing verifies a condition. So no sentence says
"you claimed", "you filed", "verified", or "confirmed". The because-clause names the treatment as "this
calculation treats the interest on [statement] as deductible". Each responsibility message keeps its read-only
form and ends "This view does not check them." For the two linked cases below, a production per-statement
amount waits on ADR 0076 Part 3 (section 11); their sentences are targets for the hand-assembled
demonstration only.

### Nine-credit

The person enrolled in the BSc and the certificate programme at Riverside in autumn 2024, nine credits, and a financing claim names the period. Line 21 shows the worksheet result only. The calculation view shows the statement amount, its leaf citations, the status node, and the **named period conclusion** the status pins — A5 stage 3's *no enumerated adverse schooling circumstance is supported for the filer, autumn 2024*. The nine-credit telling is an examined input of that conclusion, not the ground of the amount and not the ground of eligible-student.

The disclosure shows three conditions, each distinguishable from an ordinary citation button by being a responsibility row (rule id and keyed symbol), not a line-21 `citationSites` entry:

> You are responsible for these conditions: that Riverside College was an eligible institution; that the programme you were pursuing led to a recognised credential; and that your course load met Riverside's half-time standard for that programme. They apply because this calculation treats the interest on [statement] as deductible and you described enrolling at Riverside College in autumn 2024. This view does not check them.

The circumstance named is the one the finding pinned (institution, programme, period). The treatment is the statement amount the reverse walk attached, not the worksheet dollar. **The default basis is recovered from the named period conclusion**, identified by its declared `reader_role: period-conclusion` (section 8) and reached through the status node's input pin — not from `basisOrigin`. That conclusion is pinned `origin: assertion` (a same-run source; section 9), which means only "not reached through a declared default"; no `declared_default` pin is expected or read. The view shows the conclusion's rule, symbol and the inputs it examined. The case-2 note is not used. Nine credits are not stated as having met the half-time standard. The no-link parameter is not this basis. *Prerequisite, not built:* the hand-dispatched linked chain's status rule reads the enrolment value directly (`tests/test_sli_g2_binding_probe.py`, `_status_rule`) and publishes no period conclusion; a status rule that pins that conclusion is required for this case, and its production path waits on ADR 0076 Part 3.

### Financing claim, no schooling circumstance

The person said only that this loan paid tuition for the Riverside BSc in autumn 2024. Same split: line 21 is the worksheet; the view is the statement. The disclosure uses the case-1 candidate:

> You are responsible for these conditions: that Riverside College was an eligible institution; that the BSc led to a recognised credential; and that your course load met Riverside's half-time standard. They apply because this calculation treats the interest on [statement] as deductible and you said this loan paid for the Riverside BSc in autumn 2024. This view does not check them.

The because-clause must not say the person described studying or enrolling. The financing claim remains a citation of what was said, and is the examined input of the named period conclusion (A5 stage 3, case 1). It is not labeled as enrolment and not labeled as the ground of eligible-student. The default basis is that conclusion, recovered as in the nine-credit case — not `basisOrigin`, not the case-2 note, and not a parameter pin. Same prerequisite as the nine-credit case.

### Bare statement

No borrowing link joined this statement. Line 21 is unchanged. The calculation view shows the statement amount and two sentences, each from its own rule and each only when that rule published.

The bare-statement responsibility rules' `wording` (the named conclusion published and the amount is above 0, section 9), leading the disclosure:

> No borrowing is currently linked to [statement]. You are responsible for these conditions: [the conditions]. They apply because this calculation treats the interest on [statement] as deductible. This view does not check them.

The named conclusion's `lineNote`, displayed through a published responsibility finding that pins the conclusion (section 9):

> Eligibility is taken as met for the interest on [statement]: nothing said about this statement as a whole matches a disqualifying circumstance this calculation checks.

That is what the executed producer establishes, and no more: no statement-wide claim joined this statement (the owner's default-case posture — a calculation posture, not a finding that no contrary circumstance exists), or every one that joined was classified as known not to trigger the whole-amount disqualifier this classifier checks. "Known not to trigger" is not a finding of general eligibility. It does not say nothing was recorded — a borrowing-level description can exist without a link — and it does not say every disqualifier was checked. The note states the conclusion's default basis. It does not mention links, and the link sentence does not mention eligibility: a zero count is the guard, not the support. It is not a description of the no-link parameter. The three conditions are not in the view's ordinary text. They are in the disclosure, and only from the bare-statement rules' own fields. The stage-4 sentences that end "nothing you've described names them" and "nothing you've described says otherwise" are not the text: a description can exist without joining this statement. Section 7 says what the link sentence is allowed to claim. With a whole-amount-disqualifier claim or an unresolved claim joined, neither sentence appears (section 9). The statement is named from the group's `statementLabel` (below), never from `factId`. No institution and no programme are named. "Not known" appears only when the copied rule field says it, and only under that guard.

### A statement without the conclusion — the outcome line

No **bare-statement** responsibility rows or bare-statement note. A linked-case responsibility remains governed
by its own producer and dependency chain; the absence of the bare conclusion must not suppress it. The
statement outcome line (section 9) shows each non-neutral axis. These
are renderer-owned status texts, like the blocked banner — not condition sentences — and every name in them
comes from the model (a claim's or link's recorded label, a rule id), never from a template slot the model did
not fill:

- `statementScope: whole-amount-disqualifier` — "A claim about this statement as a whole, [claim label],
  describes a circumstance this calculation classifies as disqualifying the whole amount ([classifier rule
  id])." One line per claim classified 1. "Classifies", not "treats": the experimental amount does not yet read
  the classification (section 9, amount decision).
- `statementScope: unresolved` — "The calculation could not resolve the statement-wide circumstances."
  Show the count producer's original disposition and the affected entries classified by section 4, and, for
  each affected claim, the classifier's own disposition for that claim if it has one (a classifier block is
  an effect this classifier does not treat). A claim id names an affected claim; it does not prove its
  classification was absent rather than unhandled, duplicated or invalid.
- `route: linked` — "This statement's interest follows its linked borrowings." Nothing favourable or
  unfavourable is said; the group's amount row shows the link path, covered or uncovered.
- `route: unresolved` — "The calculation could not determine this statement's borrowing-link count."
  Show the original disposition and available diagnostic entries per section 4, not all as link names.
- `route` or `statementScope: not-computed`, or a conclusion `not-computed` — "Not computed: [rule id] has no
  result for this statement."
- A blocked conclusion or a residual responsibility failure — show its code and classified `missing`, even
  beside a linked route. An inapplicable conclusion is explained by the linked or disqualifier axes when they apply;
  otherwise show that the conclusion rule did not apply. Do not silently substitute a guessed cause.

None of these says the interest is or is not deductible. Until the amount change the owner chose in principle
is built (section 9), a line for `whole-amount-disqualifier` or `unresolved` also carries "The statement amount
above does not account for this."

### Uncovered link

The statement row in the view is blocked. Line 21 is whatever the worksheet did with raw box 1; this contract does not define that interaction, because the worksheet does not read the block. The view shows the code, and it shows each finding-id `missing` entry's recorded identity, so the affected link is named. It distinguishes different recorded identities and markers, not reasons the record does not distinguish (section 4). A marker, a parameter id, or a symbol name is shown as itself, not as a link. No responsibility rows are shown: a treatment that was not taken has no responsibility on it. The blocked banner is appropriate on this row and is not the condition register.

### No-link parameter

The statement amount is published. Box 1 remains a citation. The parameter pin is visible on the group as role `parameter`, id, and version, with no `origin` and no `basisOrigin`. It is not left only inside an embedded act. This is the coverage quantity (nothing joined to reduce), not the eligibility default and not the bare-statement note. When the named conclusion also published for this statement, its note is shown from that rule through a responsibility finding (section 9), not from this pin. The page does not treat "no link" as "school unknown".

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

**Hand-dispatched probe (`tests/test_sli_bare_statement_selection_probe.py`,
[`bare-statement-selection-probe.md`](bare-statement-selection-probe.md)).** A guard of "the link count is 0",
with the count computed by `link_coverage` over per-link presence markers, is **not sound under
`rule-artifact.v10`**. A rule reads only the count's value; no rule operation can inspect the count finding's
parameter or input pins. Two packages that pass `validate_package` publish the bare-statement token on a sum of
zero while a link exists: a marker whose value is 0, and markers of 1 and −1. Six other cases fail safely: no
link publishes (correct); one counted link, a blocked marker, a missing marker, an unjoinable link, a subject with
absent keys, and a count that never ran all withhold the token.

**Contract: no bare-statement rule may be selected by `count == 0` under v10.** Pin inspection stays a
presentation/provenance check, not a guard.

**The mechanism this requires.** A `link_count` expression: over the joined current links for this subject only
(no markers, no reductions), returning the number of joined links; blocking exactly as `link_coverage` does on an
unbound scope, absent subject keys, missing row keys, or present unjoinable rows; returning 0 only when no link is
joined. Zero then means one thing, and no marker content can forge it. It is a new expression alternative, so it
belongs to the **second rule successor**, authorized by this contract's acceptance (ADR 0076 publication plan).
Rejected alternatives: constraining the marker publisher to the literal 1 in validation — it would apply to every
`link_coverage` reductions publisher, including amounts, unless a count mode were declared, which is itself a
successor; a parameter sentinel — any marker can equal it; a flag exposing whether `link_coverage` took the
parameter path — works, but is a larger change than counting links directly.

**The one executable guard (proposed; `link_count` is not built).** A per-statement **count rule** (subject:
the statement's box-1 fact) publishes `link_count(links)`. Its pins: the statement's box-1 finding (`input`,
`origin: assertion`) and every joined link finding (`input`, `assertion`); **no parameter pin** — `link_count`
has no parameter. At 0 it pins only box 1. The named conclusion (section 9) is the one rule that
reads the count: it `requires` the count rule's published symbol and its guard includes
`compare eq (ref count) 0`. The responsibility rules reach the bare-statement case only through that
conclusion. Nothing reads a pin. A blocked or absent count
is `DEPENDENCY_ABSENT` of that symbol (no `optional_default` may be declared for it), so the case is not selected.

**The condition this selects is "no link joined to this dispatch subject."** It is not "no schooling
information in the workspace": an enrolment or financing claim can exist unlinked. A shared key name whose
values disagree is a join of nothing; zero rows of a type are not observably joinable. The operator does not
prove the joined list is this statement's — that is ADR 0076 Part 2. Until Part 2 is accepted and implemented, a
0 is not a statement-specific claim.

**What the wording must claim.** Only that no current borrowing link joined this statement. Candidate (the
owner's to approve): "No borrowing is currently linked to [statement]." Not "nothing you've described names
them" (a description can be present and unlinked), not "nothing connects these loans to a school" (the count
says nothing about schools), and not anything about eligibility (the count is not eligibility support,
section 9).

When the count is not 0 or does not publish, the conclusion does not publish, so neither the responsibility
text nor the note can appear. A count of 0 is necessary, not sufficient: a whole-amount-disqualifier claim or an unresolved one also
stops the conclusion (section 9). Schooling that is present but not linked does not suppress the sentence, and the sentence must not
pretend it did. Situation-scoped rules for the nine-credit and financing-claim cases publish from the
circumstance they pin, not from a count.

## 8. The wording home

The wording **pin role** is withdrawn everywhere. `derived-finding.v2` and `derivation-record.v9` do not gain it. Findings do not pin a wording citizen. The projector does not look for a pin of role `wording`.

If the sentence is declared on a rule, this is how it reaches the projector. No pin carries it.

- The case is which rule published. The bare-statement rule, the financing-claim rule, and the described-enrolment rule are different rules. Each declares one sentence. The projector does not choose among sentences.
- The disposition row's `artifact_id` is the rule id. `build_presentation_model` already indexes the resolved graph by id. The projector reads that rule object, the rule that ran, not a copy with a rewritten `publishes`.
- The content version is that rule's `version`. The group stores it as `ruleVersion`. A sentence change is a new version of that rule.
- The field name on the rule successor is `wording` (the condition sentence) or `lineNote` (the ordinary-line note on a conclusion rule only). Both are optional strings. `notes` is not read. Neither identifies what a rule is: a rule is a responsibility producer or a conclusion because it declares `reader_role` (below), not because it carries text.
- Slot rule. The projector replaces `{statement}`, `{institution}`, `{programme}`, or `{period}` only with a key on a fact an input pin of that finding names, or, for `{statement}` only, with the group's `statementLabel`. The fact-id suffix is never a slot value. A missing key fails the projection. It does not become "unknown", an empty string, or a placeholder. A bare-statement field has no institution, programme, or period slot.

### Which producers the reader explains — `reader_role`

The bounded reader explains a fixed set of producers. Each declares what it is, on the second rule successor,
as `reader_role` — one value from a closed enum. Optional text never identifies a producer, and neither does a
name convention, a shared pin, or a position in `requires`.

| `reader_role` | What the rule is | Package validation (second package successor) |
| --- | --- | --- |
| `statement-amount` | The per-statement amount (subject: box 1) | At most one per subject type in the package |
| `link-count` | The statement's borrowing-link count (`link_count`) | At most one per subject type; its value is a `link_count` node |
| `statement-scope-classifier` | Classifies one statement-wide claim (subject: the claim type) | Its value's outcomes are 1, 0, or a block, with no other literal result |
| `statement-scope-disqualifier-count` | Counts whole-amount disqualifiers among the statement's claims | At most one per subject type; a `link_coverage` whose `reductions` is a `statement-scope-classifier`'s `publishes` |
| `bare-statement-conclusion` | A5 stage 4's statement conclusion | `requires` contains exactly one `link-count` symbol and exactly one `statement-scope-disqualifier-count` symbol |
| `period-conclusion` | A5 stage 3's period conclusion (linked cases) | Published by a rule a status rule reads |
| `responsibility` | A condition left to the filer | `requires` contains exactly one conclusion symbol (`bare-statement-conclusion` or `period-conclusion`) and exactly one `statement-amount` symbol |

The projector finds a group's producers only through these declarations and the declared `requires` between
them. A package where a role's constraint fails is rejected; there is no fallback to inference. A rule with no
`reader_role` can still be an ordinary calculation node and provenance, and is never an axis, a conclusion or
a responsibility. `reader_role` belongs to the second rule successor with `wording`, `lineNote` and
`link_count` (ADR 0076 publication plan: its authorizing decision is this contract's acceptance), and is
never added to the first successor.

### Compared

**(a) A `parameter-declaration.v1` whose `values` is the sentence, pinned with role `parameter`.** **Production.** `values` is open, so a string is schema-valid. The parameter op records the read in `access.parameters` **before** `_as_decimal`. A sentence therefore blocks `DEPENDENCY_INVALID` with `missing` `not a number: …`, and **no derived finding is published** — so the prose never becomes a finding value. The **blocked disposition still pins the parameter id and version**, role `parameter`, no `origin` (`_record_blocked` and per-subject `_assemble_pins` build pins from that access log). Section 3's rule applies to that pin: it is a parameter, not an eligibility basis. The hypothesis that this "reaches the finding's pins today" is false for prose. What is right about it: no new citizen kind, and a numeric parameter's id and version are already a pin. What is wrong: the evaluator treats `values` as a quantity; this would put prose in the same role as the no-link parameter, which section 3 forbids dressing as eligibility; one parameter is one value, not a case chosen by a guard; the projector does not copy `values` today. Not the home.

**(b) A form-field successor carrying per-case text.** **Production.** `form-field.v3` has one `description` and one `explain` per disposition, `additionalProperties: false`. A successor could add a map without editing v3. The grain is still one field per form line. The case is a per-statement derivation result. The field would hold every sentence and the projector would pick one, which is composition, not a copy. The line's `explain` would still be the wrong surface for a sentence that must not sit on every return. Not the home.

**(c) A new wording citizen referenced from a rule-schema successor.** This works. The rule successor holds `{id, version}`, the projector loads that citizen from the rule it already resolved, and the sentence can version without a new rule version. The cost is a new published schema plus the reference field. These sentences are not shared. Each case is its own rule, and that rule's version is already the content version. A second version axis is not earned. Not this contract. Do not publish `condition-wording.v1`.

**(d) The consumer.** The page or the projector holds the sentences, keyed by rule id. No schema. It fails the projector's copy rule and the page's zero-authority rule. The sentence would live in two HTML copies. A model with no declaration could still show it. Not the home.

**Contract. Recommendation: the rule field in the first half of this section, on the second rule successor.** Per ADR 0076's publication plan, the first successor carries `subject`, `joined` and `direction` and is published once ADR 0076 Parts 1 and 2 are accepted; `wording` and `lineNote` are **not** in it. They arrive in the next rule version, authorized by this contract's acceptance and the owner's approval of the sentences, and are never added to the first successor after publication. No new citizen kind. `rule-artifact.v10` has `additionalProperties: false` and cannot gain the fields. Until the successor exists, the view carries identity and no sentence. That state is not a completed reader case.

## 9. The statement-scoped responsibility rule

Three rules, one per condition, for the bare-statement case only. The probe rule `demo.rule.responsibility-eligible-institution` is not this rule. **Prior probe.** That rule publishes when status is `not-adverse`, its subject in P4 was the financing claim, and with subject box 1 it blocked `DEPENDENCY_ABSENT` because it requires status. Status sources are keyed to financing claims. Requiring status is what makes the bare statement unable to publish.

### Subject

The subject is the statement fact type `tax.us.2025.f1098e.box1-student-loan-interest` (identity keys lender, statement, tax-year). Not a financing claim, not an enrolment, not a run-wide box-1 scalar. The subject declaration is ADR 0076. Until that binding is accepted, section 7's sentence is not shown as a claim about this statement.

### The chain, traced

Executed by hand in `tests/test_sli_bare_statement_chain_probe.py` (**hand-dispatched, production dispatch
code, not a production schedule**; synthetic ids; package accepted by `validate_package` first). Per statement,
subject its box-1 fact, in this order:

1. **Box 1.** The current box-1 finding is the subject of the per-statement rules below; those rules pin it
   `input` / `assertion`. The per-claim classifier and per-link rules instead pin their own subjects.
2. **Count.** `link_count` (proposed, section 7) over statement-to-borrowing links: 0 when no borrowing link
   joined this statement. The probe stands in `link_coverage` with a presence marker, as the selection probe did.
3. **Statement-scope claims and their classification.** A claim about the statement as a whole ("the loans
   on this statement paid for …", A5 stage 4 route (a)) is keyed on the statement identity plus the applied
   circumstance. The claim stays descriptive — what the person said. Its own rule (subject: the claim;
   `reader_role: statement-scope-classifier`) decides one particular consequence, explicitly, three ways:
   - **1 — a supported whole-amount disqualifier.** Today only `vehicle`: a use other than qualified higher
     education expenses. The reading (owner's A in principle, below) is § 221(d)(1)'s "solely" as 26 CFR
     1.221-1(e)(4) Example 6 applies it to a mixed-use loan, carried to every borrowing the claim reaches.
   - **0 — known not to trigger that disqualifier.** Today only `tuition`. This is not a finding of general
     eligibility, and not evidence about any other condition.
   - **Block, `DEPENDENCY_INVALID` — an effect this classifier does not treat.** Any other value. Partial and
     period-limited effects belong here until a selected rule treats them; they are never folded into 1 or 0.

   The vocabulary today is exactly `tuition` and `vehicle`, and both are handled. The catch-all is an
   **extension hazard**, not a demonstrated omission: a value later admitted without a branch would, under a
   catch-all 0, read as "does not trigger". There is no catch-all; `ClassifierExtensionHazard` widens the
   vocabulary to show both shapes (tested).
4. **Whole-disqualifier count** (`reader_role: statement-scope-disqualifier-count`).
   `link_coverage(claims, classifications, empty: no-statement-scope-claim parameter = 0)`. The empty case is
   the owner's default-case posture — no joined statement-wide claim — a calculation posture, not a finding
   that no contrary circumstance exists. A joined claim without exactly one classification, including one
   whose classifier blocked, blocks `DEPENDENCY_INVALID` (tested). Another statement's claim does not join
   (tested).
5. **The named conclusion** (`reader_role: bare-statement-conclusion`) — A5 stage 4's *no enumerated adverse
   circumstance bears on the interest this statement reports*. `requires` count and whole-disqualifier count;
   guard `all(count == 0, disqualifiers == 0)`; publishes the token `no-enumerated-adverse`. Pins: box 1, the
   count finding, the disqualifier-count finding — each `assertion`. No parameter pin; no `declared_default`
   (tested). Inapplicable when a disqualifier is counted; blocked when the count is unresolved (tested).
6. **Statement amount** (`reader_role: statement-amount`). Today: box 1 minus linked reductions, the no-link
   parameter when none. It reads neither the classification nor the conclusion, so with a whole-amount
   disqualifier it still publishes box 1 (probe: 400). The owner chose A in principle; the change is specified
   below and not built.
7. **Three responsibility rules.** Each `requires` the conclusion and the amount **and reads both in its guard**:
   the conclusion is `no-enumerated-adverse` and the amount is above 0. Pins: box 1, the conclusion, the
   amount, its citations (tested). The value is a declared applicability token; the sentence is the rule's
   `wording`.
8. **The displayed note.** `lineNote` is the conclusion rule's field. It is displayed only through a published
   responsibility finding's input pin to the conclusion — the reverse walk from the amount reaches the
   responsibility, and the responsibility names the conclusion. No published responsibility, no note.

**A correction to the previous text.** It said the amount is read "through `requires`, so that it is pinned".
That is false. `pins_for` builds input pins from the access log — what the evaluation read — and a rule whose
guard is `true` and whose value is a literal reads nothing it required. The probe's first build of the
responsibility rules pinned neither the conclusion nor the amount. The guard above is what makes them pinned.

**A second gap the probe met.** A keyed same-run publication carries no fact type to its consumers:
`subject_dispatch._fact_type_of` falls back to the symbol name, so `categorical_compare` of the conclusion
against its token blocks `CATEGORICAL_DOMAIN_MISMATCH` unless the token's fact type has the symbol's own id.
The probe uses that naming as a workaround. Production needs either that convention or the fact type carried
on keyed publications; this contract does not choose.

**How the promise "it lapses when the favourable treatment is absent" is kept.** Structurally: a
responsibility rule requires the conclusion, so where the conclusion did not publish the rule records
`DEPENDENCY_ABSENT` naming only the conclusion's symbol. The previous shape (requires count and amount, guard
count == 0) publishes on zero links alone even with a whole-amount-disqualifier claim; the probe keeps it to show that (tested).

### Why the conclusion is absent — traced upstream, per statement

The downstream result cannot say why. Four different causes give every responsibility rule the identical
`DEPENDENCY_ABSENT` with `missing` = the conclusion's symbol, and in all four the statement amount is still
published (tested, `WhyTheConclusionIsAbsent`):

| Cause | Count for this statement | Whole-disqualifier count for this statement | Conclusion for this statement |
| --- | --- | --- | --- |
| Whole-amount disqualifier established | published, 0 | published, above 0; pins the claim, whose classification is 1 | inapplicable |
| Classification unresolved (no classification, or the classifier blocked on an untreated value) | published, 0 | blocked `DEPENDENCY_INVALID`, `missing` names the claim | blocked `DEPENDENCY_ABSENT` [whole-disqualifier count symbol] |
| Required producer did not run | no result at all | published, 0 | blocked `DEPENDENCY_ABSENT` [link-count symbol] |
| Linked route | published, above 0; the amount pins its links | published, 0 | inapplicable |

So the experimental reader never reads the responsibility block for a cause. It looks up **this statement's
own** result for three symbols, `<publishes>|<statement fact id>` — the conclusion (found from the
responsibility rules' `requires`), and the two symbols the conclusion rule `requires`: the one a `link_count`
rule produces (**route**) and the one the statement-scope `link_coverage` rule produces (**statement scope**).
It records them as `statementOutcome` (section 2). **Discovery is by declaration:** the conclusion is the
responsibility's required symbol whose producer declares a conclusion `reader_role`; route and statement scope
are the conclusion's required symbols whose producers declare `link-count` and
`statement-scope-disqualifier-count` (section 8). Never by name, position or optional text; another
statement's rows are never read. The reference function
`_statement_outcome` in `tests/test_sli_bare_statement_chain_probe.py` is given the known probe producers and
classifies their dispatch results. It does not implement dependency discovery, projection, or page rendering.

- `route`: `bare` (count 0), `linked` (count above 0), `unresolved` (count blocked; its `missing` per section
  4), `not-computed` (no result).
- `statementScope`: `no-whole-amount-disqualifier` (count 0: none joined, or every joined claim known not
  to trigger it), `whole-amount-disqualifier` (count above 0), `unresolved` (count blocked or inapplicable),
  `not-computed` (no result). Each claim the count examined is listed with its classifier's own disposition
  for that claim — 1, 0, or blocked.
- `conclusion`: its own disposition, or `not-computed`.

An inapplicable count or total is `unresolved`, with the original `inapplicable` disposition retained: that
producer ran but supplied no numeric answer. Numeric interpretation compares values, not string spellings
(`0.0` is zero). These two producers promise non-negative integer counts; a published value outside that
domain is an unresolved producer-contract violation, never evidence of linked borrowings or disqualification.

**Where the cause is shown.** Bare-statement responsibility rows are not rendered when the conclusion is not
published — they would restate a treatment the calculation did not reach. Their blocked dispositions stay in
`responsibilityFailures`, and each is displayed unless every `missing` symbol's own outcome for this statement
is on the line (section 2, reverse walk). The cause is shown instead on a **statement
outcome line** directly under the statement amount in the calculation view — not inside the collapsed
disclosure, not a banner, not `role="alert"`. It shows every axis that is not neutral (`route: bare` and
`statementScope: no-whole-amount-disqualifier` are neutral). A blocked or not-computed conclusion remains
visible even if another axis already explains why the bare route was not selected. An inapplicable
conclusion needs a separate line only when neither the linked route nor a disqualifier explains it. Residual responsibility failures remain
visible without displaying their condition sentences. Texts are in section 5. A linked route is not an unfavourable result: it says
the bare-statement conclusion is not this statement's path, and the amount's own link path (covered or
uncovered) is what the group shows.

**What the probe cannot show.** A producer that does not run, does not run for any statement: in that case
S2 shows the same `not-computed` route. In every other case S2 is unchanged (tested).

**Discriminating case (tested).** S1 and S2 have no borrowing link. S1 has a current statement-wide claim that
its loans paid for a vehicle; S2 has none. S1: count 0, total 1, no conclusion, no responsibility, no note, the
outcome `statementScope: whole-amount-disqualifier` naming the claim, and — until the amount change below is
built — amount 400. S2: conclusion, three responsibilities, identical to a run with no claim
anywhere. Moving the claim to S2 leaves every S1 finding byte-identical (tested).

### What each responsibility rule publishes and pins

One categorical finding per statement, and only when its guard holds (section 9, chain step 7). Symbol is the
unsuffixed condition symbol plus `|` plus the statement fact id. The value is a declared applicability token,
not the prose. The rule's `wording` field is the sentence of section 5. A value of `applies` with no `wording`
field does not say the school is unknown, and the projector must not complete the sentence. Nothing consumes
the finding.

Pins: the box-1 finding (`input`, `assertion`); the named conclusion (`input`, `assertion` — the eligibility
basis, by its identity); the per-statement amount (`input`, so the reverse walk attaches the responsibility to
that statement's group); citation pins for this condition only. It does not pin the count, an institution, a
programme, a period, a financing claim, an enrolment, a wording citizen, or the no-link parameter; it puts no
`origin` on a parameter pin; it pins no sentinel that means "unknown" by being absent.

### Reconciled with the selected model

The previous revision of this section introduced a statement-keyed eligibility fact type with an
`optional_default`, so that a `declared_default` pin would drive `basisOrigin` and the note. **Withdrawn.** It
had no tax meaning of its own: it would manufacture a favourable description nobody gave, which the owner's
2026-09-20 decision names as the wrong layer ("`optional_default` is real, adopted, and the wrong layer here"),
and A5 stage 3 rejected disqualifiers-as-defaults. Its only function was the page's pin.

What stands is A5 stage 4's named conclusion, now with an executable producer (above). Its default basis is
carried by **being that conclusion** — its rule and symbol — not by `origin`. Its `basisOrigin` is `assertion`,
which A5 stage 3 fixed as meaning only "not reached through a declared default"; the page must not present it
as the filer's telling. Statement-scope information prevents the conclusion two ways, kept apart: a supported
whole-amount disqualifier makes the count above 0 (inapplicable); an effect the classifier does not treat
blocks the count, and the conclusion (unresolved).

### Owner decisions, 2026-09-24, and what they require

- **No joined statement-wide claim is the default case** (decided). The engine reads "none" from an empty
  collection only over a closed source set (`a4-bounds.md`); this producer reads it through `link_coverage`'s
  empty parameter — the posture the owner accepted for links on 2026-09-23. It is a calculation posture, not a
  finding that no contrary circumstance exists. The conclusion pins the disqualifier count; that count pins the
  claims and classifications it examined, which are the conclusion's transitive provenance.
- **The amount follows the supported tax consequence — A, in principle** (decided; **not built**). It is
  decided by the statement-scope result, never by whether the favourable conclusion published:
  - **Changes the amount: `whole-amount-disqualifier`.** A current, classified statement-wide claim joined to
    this statement is a supported whole-amount disqualifier. *Tax reading:* § 221(d)(1) makes a loan a
    qualified education loan only if incurred *solely* to pay qualified higher education expenses; Example 6
    holds a mixed-use loan is not one; a route-(a) claim reaches every borrowing the statement reports. So none
    of the statement's interest is interest on a qualified education loan. *Arithmetic:* amount = 0 when the
    whole-disqualifier count is above 0. That applies to linked statements too, because the claim reaches every
    borrowing on the statement. Only a classification of 1 does this.
  - **Withholds a result: `unresolved` or `not-computed`.** An effect the classifier does not treat, a missing
    or duplicated classification, or no count. The amount then requires and reads the count, so it blocks,
    naming the count's **symbol** at the amount; the count's own result names the claim (section 4), and
    `statementOutcome` keeps that cause. Not 0, and not box 1. A partial or period-limited effect is here until a
    selected rule treats it — it is never collapsed into whole-amount disqualification or into "does not
    trigger".
  - **Leaves the amount as it is: `no-whole-amount-disqualifier`.** Box 1 minus linked reductions, as today.
    "Does not trigger" says nothing about any other condition.
  - **Belongs to another path: `route: linked`.** Borrowing-level circumstances reach a linked statement's
    amount through link reductions and status, which wait on ADR 0076 Part 3. Apart from the statement-wide
    disqualifier above, this decision changes nothing there. A route that is `unresolved` or `not-computed`
    withholds the bare-statement conclusion; it does not change the amount rule, which keeps its own
    fail-closed link checks.
  - **Until built,** the experimental amount ignores the classification. The outcome line says "classifies as
    disqualifying" and "The statement amount above does not account for this."
- **Institutional responsibility conditions stay separate.** The three conditions are the filer's
  responsibility whatever the classification says; nothing here adds a question or requires new external
  verification.

### What the person said, what the rule concluded, what changed the amount, what the reader can recover

For one statement, per case. "Recovers" means from the durable `presentation.json` after the run is gone.

| Case | What the person said | What the rules concluded | What changed the amount (today → under A) | What the reader recovers |
| --- | --- | --- | --- | --- |
| No link, no claim | Nothing about this statement's schooling | Count 0; disqualifier count 0 by the no-claim parameter; conclusion published; three responsibilities | Nothing → nothing | Amount, the conclusion by `reader_role`, its pins (count, disqualifier count, the parameter behind it), responsibilities, note |
| No link, "paid for tuition" | The claim, as said | Classified 0 (does not trigger); count 0; conclusion published | Nothing → nothing | As above, plus the claim and its 0 — never shown as general eligibility |
| No link, "also paid for a vehicle" | The claim, as said | Classified 1; count 1; conclusion inapplicable; responsibilities lapse | Nothing (400) → 0 | The claim, its 1, the count, the inapplicable conclusion; "classifies as disqualifying" while the amount ignores it |
| No link, untreated value | The claim, as said | Classifier blocked; count blocked; conclusion blocked | Nothing (400) → amount blocked | The claim, the classifier's block, the count's block; "could not resolve" — not a cause it cannot see |
| Linked | Whatever the linked chain records | Count above 0; bare conclusion inapplicable | Linked reductions → the same | The link path on the amount row; no bare-statement text |

"Today" is the executed probe; "under A" is specified and not built. No row claims the person described
anything they did not, and no row lets a missing input stand for a described one.

### Which scheduling it needs

ADR 0076, the subject declaration on the rule successor. Not a package-level map, and not a Python id list. `wording` and `lineNote` come in the second rule successor, not the first (ADR 0076 publication plan). It does not admit a pin role `wording`.

What that scheduling has to provide for this rule:

- A required `subject` on the rule successor, an exact fact-type pin to `tax.us.2025.f1098e.box1-student-loan-interest`.
- The package successor that admits that rule schema.
- Eligibility waits on predecessor **rule resolution**, not on the unsuffixed symbol appearing in `self.symbols`. The predecessors of a responsibility rule are the named conclusion and the per-statement amount rule; the conclusion's are the count rule and the whole-disqualifier-count rule, whose predecessor is the claim classifier. None is the schooling-status rule or the worksheet. Keyed publication never inserts the unsuffixed name, so a `requires` entry of that name stays ineligible and `finalize_unreached` would then evaluate the rule once, unsuffixed.
- The intercept is on `attempt` and on `finalize_unreached`, so `runner._execute` and `reference_runner.run_reference` share it.
- One dispatch publishes per statement. The rule id resolving once must not collapse the three statements into one unsuffixed finding, and must not block every statement because one amount was blocked. A statement whose amount, count, or whole-disqualifier count is blocked gets no responsibility finding. The other statements still publish.
- The count rule is a `link_count` rule and the amount rule a `link_coverage` rule; both join links. The whole-disqualifier-count rule is a `link_coverage` rule over statement-scope claims, and its relation (claim identity contains the statement identity) is ADR 0076 Part 2's `joined_contains_subject`, the same as the link's. The responsibility rules and the named conclusion join nothing. ADR 0076's link-binding half still gates any sentence that says "this statement": until a joined link is this statement's, a coverage result is not a statement-specific claim. The rule's own grain does not depend on a shared key name with a link type.

Situation-scoped responsibility rules stay per schooling situation. Their subject is that situation, and their pins name the institution, programme, and period. They are not this bare-statement rule. They carry their own `wording` field, the named-circumstance sentence, and the same reverse walk. They do not publish when section 7's guard holds.

## 10. The demonstration standard

P4 inspected `build_presentation_model`'s return value while the run object was still in hand, and it did not load the page. That does not satisfy this contract. **Prior probe.**

Three separate obligations, none a substitute for another:

- **Model shape** — `validate_presentation_model` (section 2, Validator): well-formed and internally consistent.
- **Projection fidelity** — below, with the run in hand: the model says what the run recorded.
- **The durable-file demonstration** — the numbered steps: a reader recovers it from the file after the run is gone.

### Projection fidelity

With the run's publications, dispositions and resolved rules in hand, and for each statement group:

- Each `statementOutcome` axis equals the disposition recorded for `<publishes>|<statement fact id>` of the
  rule found through `reader_role` (section 8) — kind, code, `missing`, pins and finding id — and each examined
  claim's classification equals the classifier's disposition for that claim. No row from another statement is
  used.
- Every responsibility row is a published finding of a `reader_role: responsibility` rule for this statement;
  every published one that pins the amount or its chain is present.
- Every blocked responsibility disposition for this statement is in `responsibilityFailures`, unchanged, and
  its `explainedBy` entries name the displayed outcome of exactly the producers of its `missing` symbols.
- Every value in the model equals the value of the finding it names; nothing is recomputed.
- A package whose `reader_role` constraints fail is not projected.

These run against the hand-assembled chain now and against a production run once the prerequisites in
section 11 exist.

### The durable-file demonstration

The test does all of the following.

1. Run the bare-statement case, the nine-credit case, the financing-claim case, an uncovered link, and a no-link parameter through the real writers. The live path already writes `outputs/<stem>.presentation.json` from `build_presentation_model` before it returns. The runs are hand-assembled. They are not a production schedule, and the test says so.
2. Discard the run result, the publications, the dispositions, and any in-memory model. The rest of the test may hold the path of the presentation file and nothing else from the run.
3. Read that file back from disk. `validate_presentation_model` on the reloaded JSON is allowed. It is not the page proof.
4. Load the experimental page (section 5) through the harness as a candidate, the way `tools/presentation_harness/lib/executor.mjs` does, in a fresh Chrome target. The server splices `__FIXTURE_JSON__` with the fixture file's bytes.
5. The fixture is the re-read presentation file itself, not a hand-written golden. The server serves only manifest-declared, repository-confined paths, so the run must write `presentation.json` under a repository-relative path the manifest names (gitignored `temp/`, for example).
5a. Assert the product page is byte-identical to the milestone base and contains no `calculationView` reference. Loading the product page is not part of this demonstration.
6. Assert with the harness check `dom-text-present`. Line 21's value remains the worksheet figure, never a
   statement group's value. Check the five cases, the copied wording and note, the disclosure inside the
   calculation view, and the absence of condition inputs or alerts. Reject the unsupported phrases listed
   in section 5. No form line contains the note or conditions.
7. Run section 9's four causes for S1 beside a bare S2: whole-amount disqualifier, classification unresolved,
   count producer not run, and linked route. Show no S1 bare-statement responsibility sentence or note, but retain the
   corresponding outcome and evidence. The four outcomes differ; none asserts deductibility. The ordinary
   linked case is neither disqualified nor unresolved. Also run a tuition claim (does not trigger; the
   group never says eligible) and a claim whose value the classifier does not treat (unresolved, with the
   classifier's own block shown). S2 remains unchanged except when a producer was skipped
   for all subjects. Also test a blocked conclusion beside a linked route, and an unexpected responsibility
   failure after a published conclusion: neither diagnostic may disappear. The linked case in this probe has
   no linked-case responsibility producer; separately check the named-circumstance cases retain their own
   published responsibilities when the bare conclusion is inapplicable.
8. Run duplicate and nonnumeric classification cases against the same claim. Identical recorded diagnostics
   must not acquire different invented explanations. Name the affected claim and show the unresolved result.
   An inapplicable count is not described as a rule that never ran. A missing upstream total is named as a
   symbol at its consumer, with the total's own diagnostic retained separately.
9. Check reverse-walk selection: numerical count/total findings sharing box 1 do not become responsibilities;
   nor does an amount-dependent rule without a `wording` declaration. A blocked responsibility has no finding
   value or condition sentence. Published intended responsibilities still attach through their amount or
   intermediate-finding pins.
10. Check pin and label boundaries: distinguish finding ids, markers, parameter ids and symbol names as
    section 4 permits. No parameter acquires `origin` or `basisOrigin`; its presence alone produces no
    eligibility note. A missing `wording` declaration produces no responsibility sentence. A missing school
    pin never becomes “unknown” unless the selected bare-statement rule explicitly supplies that text.
    `integrated` remains false, the explanatory chrome is present, and line 21 has no statement rows.

A passing structural check on the Python object, or a passing check on the evaluation page, is not this demonstration.

Out of scope for the demonstration: the full `pytest` suite as a substitute for the page load; a second derivation from the closing record; `explain()`; personal or live workspace data; approving the candidate sentences; a production schedule of the per-subject chain.

## 11. Limitations and completion

`derivation-record.v9` does not retain intermediate values. **Production.** A closing record written with `use_v2=True` stores pins and dispositions. It does not store `published`, `blocked`, or `value`. `out.json` stores dispositions and no findings. The values this page shows — the worksheet amount, a statement amount, a reduction, a status, the applicability token — are in `presentation.json` only because the projector copied them from memory while it built that file. A reader that ignores `presentation.json` and reads the record cannot show them. Identity joins (which link, which status, which responsibility, whether an input pin is `declared_default`, whether a pin is a parameter) remain on the record. This contract does not add a record version to move the values. The demonstration is void if the page was explained by re-reading the run object.

The presentation file is not a reconstruction. If it is deleted, the page is not rebuilt from the record under this contract. Deleting it also loses the copied sentences: they are not on the record.

**Production prerequisites, in order.** ADR 0076 Parts 1 and 2 built and reviewed (Track 5); `link_count`
and `reader_role` on the second rule successor, with `wording` and `lineNote`; reliable categorical type
information on keyed same-run publications (section 9's second gap — a convention or the type carried, chosen
then); the amount change the owner chose in principle; and then the durable-file reader demonstration
(section 10). The linked cases additionally need a status rule that pins the named period conclusion, and
ADR 0076 Part 3.

**Production, restated.** None of the per-subject chain is production-scheduled. A green demonstration is evidence about the writers and the experimental page, not evidence that a production run publishes these rows. The nine-credit and financing-claim cases reach status through the link-to-status edge, which joins on borrowing only; until ADR 0076 Part 3 settles what a set of statuses for one borrowing means, no production per-statement amount is published through that edge, and those two cases are hand-assembled only.

Completion. All of these are required. Any one missing means the reader case is not complete.

1. Line 21 still binds `tax.us.2025.schedule1.line21-sli-deduction`. The calculation view is present for the per-statement chain, `integrated` is false, and the page does not present the groups as the line.
2. The no-link parameter is shown as a parameter pin with no `origin`. A declared-default eligibility input is shown only where an input pin has that origin. The page never assigns the parameter that origin.
3. Blocked `missing` entries are classified as section 4. Only finding ids are resolved. Distinct recorded
   subjects and diagnostic classes remain distinguishable; identical recorded failures are not assigned
   invented distinct causes.
4. The bare-statement responsibility rules require and read the named conclusion and the amount, publish keyed findings, carry the sentence on the rule rather than on a pin, and pin no school. The named conclusion requires and reads the count and the whole-disqualifier count; no `optional_default` is declared on this path. A whole-amount-disqualifier claim, or an unresolved one, on one statement stops that statement's conclusion, responsibilities and note and changes no other statement. The sentences claim no more than those findings establish.
5. The reloaded `presentation.json` contains the calculation view, the kept intermediate nodes, classified `missing`, `basisOrigin` only from input pins, and the responsibility rows from the reverse walk.
6. The experimental page (section 5), loaded from that file after the run object was discarded, shows line 21 as the worksheet and the five cases of section 5 in the calculation view. The product citation-walk page is unchanged and is not required to show the view.
7. A projection that sees a missing school pin, a missing link, or a parameter pin, and does not have the bare-statement rule's field under section 7's guard, does not render the school as unknown.
8. Every group carries `statementOutcome` from its own statement's results, found through declared `reader_role`s. Whole-amount disqualifier, classification unresolved, producer not run, and linked route render four different outcome lines. Every responsibility block is in the model; one is hidden only when each of its `missing` symbols' own outcome for this statement is displayed.
9. The statement-scope classifier has three explicit outcomes and no catch-all; a partial, period-limited or untreated effect is unresolved. Known-not-to-trigger is never presented as eligibility.
10. Projection fidelity (section 10) passes with the run in hand, separately from `validate_presentation_model`.

Not this contract: any product-page change (showing the view there waits for worksheet integration), ADR 0076 Part 3, the worksheet successor that would set `integrated` true, the legal-obligation consumer, the partial-reduction remainder, entry-loop questions, a change to the incumbent eligibility witnesses, `condition-wording.v1`, a wording pin role, and any edit to an existing published schema file.
