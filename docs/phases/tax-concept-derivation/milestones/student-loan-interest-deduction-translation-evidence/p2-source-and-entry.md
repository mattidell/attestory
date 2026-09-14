# P2 engine observations — source, identity, and entry path

For the selected constituent, eligible-student status under § 221(d)(1)(C).

**Evidence level.** Observations of committed behavior at the source state examined during this milestone — committed artifacts, committed tests and goldens, and the code that executes them. **Later work must revalidate any specific claim against current code.** This record designs no implementation and chooses among no resolutions.

Throughout: a prepared fact that a rule can consume is not evidence that the product can obtain or preserve that fact honestly.

## Discrepancies

These do not reopen P0 or the P1 selection. Work continues against both as given.

1. **VOID exclusion is prose and omission, not an executing filter.** The box-1 fact-type title and the family `closure_claim` both say a VOID-checked copy is never admitted. `packages/kernel/` contains no `VOID` string. No fact type in `f1098e.bundle.json` has a void field on `identity_keys` or `value_schema`. `tests/test_f1098e_student_loan_interest_track2.py::KernelProjectionCases.test_n1_void_statement_never_becomes_a_member` never constructs a VOID finding; it admits only the valid statement and asserts one box-1 member exists. The executing behavior is: a VOID copy is simply not contributed.

2. **Family `closure_claim` authorizes a closed-empty numeric zero.** `family.f1098e-1.json` says "closed-empty authorizes subtotal 0." That is the family's own prose. The worksheet's `count == 0` branch in `rule.sli-worksheet.json` returns literal `0`. P0 F7 already records that this overclaims the tax result. Confirmed against the committed artifacts; not reopened.

3. **P0 F2's "identity keys dropped" is true of `Environment.sources`, not of marshalled `SourceFact`.** `marshal.py` does attach `keys` and `fact_id` to each `SourceFact`. `_Run.__init__` then folds `ctx.sources` into `self.sources: dict[str, list[str]]` by appending `fact.value` only. `collect_categorical_all_equal` reads that values-only dict. The correspondence failure is the same; the drop happens at Environment construction, not at marshalling.

---

## 1. Form 1098-E contribution and closure behavior

### 1.1 How a box-1 member is admitted

**Artifact.** `packages/content/tax/2025/f1098e.bundle.json`, fact type `tax.us.2025.f1098e.box1-student-loan-interest` (schema `fact-type.v2`, version `v1`).

**Fields read.**

| Field | Value |
| --- | --- |
| `identity_keys` | `lender` (entity `tax.us.student-loan-lender`), `statement` (entity `tax.us.1098e-statement`), `tax-year` (literal `["2025"]`) |
| `value_schema` | `{ "type": "number", "minimum": 0 }` |
| `nature` | `determinable` |
| `supersession.policy` | `free` |

Fact id form, verified by constructing and admitting one: `tax.us.2025.f1098e.box1-student-loan-interest|lender=<id>,statement=<id>,tax-year=2025`.

**Sibling fields not relied upon at box-1 admission.** The five per-statement eligibility witnesses (`no-related-person-interest`, `no-qualified-employer-plan-interest`, `no-non-qualified-loan-component`, `no-employer-educational-assistance-interest`, `no-qtp-earnings-used`); the source-closure fact; every `sli-scope.*` fact. A box-1 member was admitted with none of those present. Account number is not an identity key (bundle JSON contains neither `account-number` nor `account_number`).

**Admission path, executing code.** There is no dedicated Form 1098-E producer under `packages/tax/`. Box-1 membership is a kernel family-member fact. The live path that actually admits one is:

1. `bundle-adoption` of `tax.us.2025.f1098e.vocabulary`.
2. `entity-introduced` for the lender (`tax.us.student-loan-lender`) and the statement (`tax.us.1098e-statement`).
3. Ordinary `assertion` of the same-identity box-2 companion (required; see 1.2). Box-2 is **not** a family member.
4. `horizon-genesis` for family `tax.us.2025.f1098e.1`.
5. `member-transition` with `member.action == "assert"` carrying the box-1 finding. `packages/kernel/findings.py` `apply_assertion` (SC-R1) rejects a first-time box-1 finding on the plain assertion path: `"cannot assert member fact … through a plain assertion; must use a member-transition instead"`. Confirmed by `tests/test_f1098e_student_loan_interest_track2.py::test_n2_box1_via_plain_assertion_rejected`.

`packages/kernel/contribution.py` `apply_contribution_batch` is the generic contribution boundary: it applies a `contribution` act, then successor `assertion` / `member-transition` acts, through the same `apply_act`. Nothing in that module is Form 1098-E-specific. Production projection (`packages/derivation/live.py` `live_coordinate_run`) installs the companion-presence map onto the registry before `project(...)`, so live admission and `tax_registry()` admission use the same pair.

**Downstream consumers of a current box-1 member.**

- Family membership: `packages/content/tax/2025/family.f1098e-1.json` `member_predicate.fact_type`.
- Raw subtotal: `packages/content/tax/2025/rule.sli-worksheet-line1-subtotal.json` `collect` of `tax.us.2025.f1098e.box1-student-loan-interest` over `source_set` `tax.us.2025.f1098e.1`, publishing `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`.
- Worksheet count / closed-empty branch: `packages/content/tax/2025/rule.sli-worksheet.json` `count` of the same fact type over the same source set (the `count == 0` `when` and the nonempty `conditional_dependency_set` condition).
- Schedule 1 attachment itemization: `packages/content/tax/2025/rule.attachment.schedule-1.v2.json` `collect_members` of that family, `member_fact_type` box-1, `subtotal_symbol` / `tie_out.line_symbol` the same raw subtotal.
- Companion-presence enforcement: `packages/tax/loader.py` `domain_companion_presence_pairs` treats box-1 as the subordinate.

The five eligibility witnesses are **not** consumers of the box-1 amount. They share identity keys with it but are separate fact types.

**Prepared fact versus honest obtainment.** The kernel will admit a prepared nonnegative box-1 finding on a member-transition, given entities and a box-2 companion. No production producer constructs that finding from a Form 1098-E or from a user account. Tests and the focused check below construct acts directly.

### 1.2 Box-2 companion-presence requirement

**Artifact.** Same bundle, fact type `tax.us.2025.f1098e.box2-checked-authority`. Pair map: `packages/tax/loader.py` `domain_companion_presence_pairs` maps box-1 → box-2. Value domain: `domain_companion_value_domains` maps box-2 → `frozenset({None, False})`.

**Fields read.**

| Field | Value |
| --- | --- |
| `identity_keys` | identical to box-1 (`lender`, `statement`, `tax-year`) |
| `value_schema` | `{ "anyOf": [ {"type": "null"}, {"const": false} ] }` |
| `supersession.policy` | `free` |

**Sibling fields not relied upon.** The five eligibility witnesses; the source-closure fact; box-1's numeric value (presence of a current box-1 is what triggers the pair; the amount is not compared to box-2).

**Executing enforcement.** `packages/kernel/findings.py` `_enforce_companion_presence`, called from both `apply_assertion` and `apply_member_transition` against the fully-updated successor state. Companion identity is the same fact-id key suffix after `|`; the kernel has no Form 1098-E knowledge. A current box-1 without a current box-2 raises `FindingModelError`: `companion presence violated: <box-1 fact id> is current (…) but <box-2 fact id> has no current value; rejected, not recorded`. A current box-2 whose value is outside `{None, False}` is rejected the same way if it somehow became current; in practice `True` never becomes current because box-2's own `value_schema` rejects it first: `finding … value does not conform to tax.us.2025.f1098e.box2-checked-authority: True is not valid under any of the given schemas`.

Box-2 may stand alone (the reverse pair does not require box-1). The bounded consumer requires both. Confirmed: missing companion rejected; `True` rejected; `None` and `False` admit.

The worksheet does **not** pin or read box-2. `rule.sli-worksheet.json` notes say component 8 has no pin: a checked box is refused at admission, so a pin would fabricate an audit trail. That is consumption, not admission.

**Downstream consumers of box-2.** Kernel companion-presence only, plus marshalling as a collect source name when box-1 is a family member (`packages/derivation/live.py` `_resolved_run_material` extra companions). No rule in the v38 graph reads the box-2 value.

### 1.3 VOID handling

No VOID representation exists. Kernel code has no VOID concept. Structural identity and value schema of every fact type in the bundle contain no `void` field (verified by dumping `identity_keys` and `value_schema`). A VOID-checked copy is excluded only if it is never contributed: no entity, no box-1 finding, no box-2 finding. That is a contribution convention recorded in titles, not a filter over an admitted member.

### 1.4 Correction and supersession of a box-1 member

**Supersession policy** on box-1, box-2, the five witnesses, and the closure fact is `free` (`f1098e.bundle.json`). `packages/kernel/findings.py` `_validate_finding`: a second finding for the same `fact_id` is allowed when policy is `free`.

**New membership versus same-member correction.**

- First admission of a box-1 `fact_id` must be a `member-transition` `assert` (SC-R1).
- A `member-transition` `assert` of a `fact_id` already in the family is rejected (SC-R2): `"transition asserting fact … already in the family is rejected: same-member correction belongs on the ordinary assertion path"`.
- Same-identity value correction is an ordinary `assertion`. Both findings remain in `state.findings`. `packages/kernel/currency.py` `_finding_corrections` walks insertion order and treats the later finding for that `fact_id` as current, displacing the earlier with reason kind `correction`. Marshalling (`marshal.py`) reads only `currency.current_finding_ids`.

Focused check (synthetic `demo.sli.lender.corr` / `demo.sli.stmt.corr`): member-transition correction rejected; assertion of `125.0` over `100.0` admitted; both findings stored.

Member removal is a separate `member-transition` `remove` / `reclassify` path (`apply_member_transition`); it withdraws the fact id. That is membership lifecycle, not a same-identity value correction.

### 1.5 What the closure attests, and what it does not (P0 F7)

**Artifacts.**

- Family: `packages/content/tax/2025/family.f1098e-1.json` (`tax.us.2025.f1098e.1` v1). `member_predicate` is box-1 only. `authorizes_subtotal` is `tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal`. `closure_claim` (prose): every box-1 amount on a Form 1098-E furnished to the taxpayer for 2025 is recorded as of the keyed horizon; covers box 1 and its box-2 companion only; says nothing about the eligibility components, MAGI, Schedule 1 Part II, or Form 1040 line 10/11a/11b.
- Closure fact type: same bundle, `tax.us.2025.f1098e.1.source-closure`. Identity keys: `family-horizon` (entity `kernel.family-horizon`) and `tax-year` literal `2025`. Value schema: boolean. Title: `true` asserts every furnished 1098-E box-1 interest amount is recorded as of that horizon; covers box 1 and its box-2 companion only; never the eligibility components.
- Mapping: `packages/content/tax/2025/closure-mapping.f1098e.1.json`. `admission.condition` is `current-literal-true`. `closure_horizon_key` is `family-horizon`. `admits_symbol` equals the family's `authorizes_subtotal`. `member_fact_type` is box-1. `packages/derivation/source_authority.py` `validate_mapping_against_family` requires that exact pin/predicate/symbol match.

**Fields the dispatch actually reads.** `packages/derivation/source_authority.py` `resolve_closure_admissions`: for the mapping, the current horizon of family `tax.us.2025.f1098e.1`, and the unique current closure finding whose `fact_type` is `tax.us.2025.f1098e.1.source-closure` and whose `horizon_id` equals that current horizon. Admission requires `isinstance(value, bool) and value is True`. False, absent, duplicate, displaced, or truthy-non-boolean findings are quiet non-admissions (family stays out of `closed_sets`). Marshaling: `packages/derivation/marshal.py` `marshal_closure_authority` extracts `family-horizon` from the closure fact id and the current horizon from `state.horizon_state.current_by_chain`.

**Sibling fields not relied upon for family admission.** Box-1 member values; box-2; the five eligibility witnesses; `sli-scope.*`; any claim about which physical forms were furnished. A `True` closure on genesis horizon `demo.sli.h0` was admitted with zero box-1 members. A `False` closure is a lawful finding and does not admit the family.

**What the closure attests (executing meaning).** That the recorded box-1 amount family is complete relative to the box-1 amounts on furnished Forms 1098-E, as of the keyed horizon, because a current literal-`True` closure finding exists for that horizon. Members of the family are box-1 amount findings only.

**What it does not attest.**

- Which Forms 1098-E were furnished, or that none was (not a document inventory).
- That the taxpayer paid no deductible student loan interest, or any amount of interest paid.
- Any eligibility component, MAGI completeness, Schedule 1 Part II completeness, or Form 1040 line 10/11a/11b.
- Per-loan composition of a statement's box-1 figure.

A later membership transition introduces a successor horizon and supersedes the predecessor horizon entity (`apply_member_transition`). A closure keyed on the predecessor is then not on the current horizon and cannot admit.

**Closed-empty product consequence, as committed.** `rule.sli-worksheet.json` `when` unconditionally `require_closed` on `tax.us.2025.f1098e.1`. Its value `choose` returns literal `0` when `count` of box-1 over that family equals 0, without reading filing status, eligibility components, the line-1 subtotal, or worksheet arithmetic. That is committed behavior. P0 F7 records that this publishes a numeric deduction the closure does not support. This unit does not design the remedy.

**Downstream consumers of closure admission.** `require_closed` / empty-`collect` / `count` in `rule.sli-worksheet.json`; empty-`collect` authorization in `rule.sli-worksheet-line1-subtotal.json` (unconditional `when: true`; closure is enforced downstream by the worksheet, per that rule's notes); Schedule 1 attachment authority keyed on the same family. Presentation classification of the resulting zero is the P2 computation-and-consumers record.

### 1.6 Checks run

- `pytest tests/test_f1098e_student_loan_interest_track2.py` — 16 passed.
- Focused kernel projection (synthetic `demo.*` ids only): box-1 admits with box-2 `None` and with no eligibility witnesses; missing companion rejected with `companion presence violated`; box-2 `True` rejected on `value_schema`; same-member `member-transition` rejected; same-identity `assertion` of `125.0` over `100.0` admitted; closed-empty `True` closure admitted with zero box-1 members; `False` closure admitted as a finding.
- Artifact dump: identity keys, value schemas, supersession, mapping admission condition, companion pair and domain, VOID absent from structural fields.

---

## 2. Witness identity and the multi-statement fold

P0 F2 is **confirmed**: two box-1 statements with one witness finding between them do not block. The universal test passes and both amounts remain collectable. Track 6b removed assertion-order dependence when two witnesses *disagree*; it did not establish per-statement coverage.

### 2.1 Identity of the five per-statement witnesses

**Artifact.** `packages/content/tax/2025/f1098e.bundle.json`. The five fact types:

| Fact type | Identity keys | Value schema | Supersession |
| --- | --- | --- | --- |
| `tax.us.2025.f1098e.no-related-person-interest` | `lender` (`tax.us.student-loan-lender`), `statement` (`tax.us.1098e-statement`), `tax-year` literal `2025` | `{yes, no}` | `free` |
| `tax.us.2025.f1098e.no-qualified-employer-plan-interest` | same | `{yes, no}` | `free` |
| `tax.us.2025.f1098e.no-non-qualified-loan-component` | same | `{yes, no}` | `free` |
| `tax.us.2025.f1098e.no-employer-educational-assistance-interest` | same | `{yes, no}` | `free` |
| `tax.us.2025.f1098e.no-qtp-earnings-used` | same | `{yes, no}` | `free` |

Same identity keys as box-1 and box-2. No loan key. No academic-period key. Not family members: they enter by ordinary `assertion`, not `member-transition`. No `domain_companion_presence_pairs` entry requires a witness for each box-1 member (box-2 is the only companion).

**Fields read by the worksheet.** `packages/content/tax/2025/rule.sli-worksheet.json` reads each of the five via `collect_categorical_all_equal` with `name` equal to the fact-type id and expected `category_literal` `"yes"`. Those five nodes sit in the nonempty-route `all` conjuncts. The `choose` `then` is `block` with code `SLI_UNIVERSAL_COMPONENT_VIOLATION` when `not` of that `all` is true.

**Sibling fields not relied upon by the fold.** Box-1 amounts; box-2; statement and lender identity of each source row; whether every box-1 `fact_id` suffix has a matching witness `fact_id` suffix; the compressed predicates inside `no-non-qualified-loan-component` (chapeau, (A), (B), (C) separately).

**Downstream consumers.** Only `rule.sli-worksheet.json` (the five `collect_categorical_all_equal` nodes). `live.py` `_iter_collect_categorical_names` registers those fact-type ids as collect source names so marshal populates `ctx.sources` for them. They are not family members and do not authorize a subtotal.

### 2.2 How `collect_categorical_all_equal` reads them

**Marshal, fact-type match only.** `packages/derivation/marshal.py` `marshal_run_context`: for each name in `collect_source_names`, every current finding whose `_fact_type_id(fact_id)` equals that name (or whose fact id is prefixed by it) becomes a `SourceFact`. Selection is by fact-type id. The `SourceFact` still carries `fact_id` and lattice `keys`.

**Environment drop.** `packages/derivation/runner.py` `_Run.__init__`:

```text
self.sources: dict[str, list[str]] = {}
for fact in ctx.sources:
    self.sources.setdefault(fact.name, []).append(fact.value)
```

`Environment.sources` is therefore `dict[str, list[str]]` — values only. Parallel `source_fids` / `source_fact_ids` exist on `_Run` but are not passed to `Environment`.

**Evaluator.** `packages/derivation/evaluator.py` `collect_categorical_all_equal`:

```text
rows = env.sources.get(name, [])
if not rows:
    raise EvalBlocked(BLOCK_ABSENT, [name])
...
return all(row == expected_val for row in rows)
```

It never reads `keys`, `fact_id`, or box-1 membership. An empty row set is `DEPENDENCY_ABSENT` (P0 F2's C3). A nonempty set of `"yes"` is `True` regardless of how many box-1 members exist. A `"no"` in the set makes the `all` false, and the worksheet then blocks `SLI_UNIVERSAL_COMPONENT_VIOLATION` (Track 6b / path (j)).

### 2.3 Smallest focused evidence for the C6 coverage failure

Kernel projection of two statements (lenders `demo.sli.lender.a` / `demo.sli.lender.b`, statements `demo.sli.stmt.a` / `demo.sli.stmt.b`), box-1 amounts `1000.0` and `500.0`, box-2 companions present, family closed on the successor horizon, and **one** current `no-non-qualified-loan-component` finding on statement A only, value `"yes"`. Then `marshal_run_context` with collect names `{box-1, box-2, that witness}`, and `evaluate` of the worksheet's `collect_categorical_all_equal` node plus `collect` of box-1.

Observed:

| Surface | Result |
| --- | --- |
| Current findings | two box-1, two box-2, one witness on statement A, one `True` closure |
| Marshalled witness `SourceFact` | one row; `keys=(lender=a, statement=a, tax-year=2025)` still present |
| `env.sources[witness]` | `["yes"]` |
| `env.sources[box-1]` | `["1000.0", "500.0"]` |
| `collect_categorical_all_equal` | `True` (does not block) |
| `collect` of box-1 | `[Decimal('1000.0'), Decimal('500.0')]`, sum `1500.0` |
| Same op with no witness rows | `DEPENDENCY_ABSENT` (C3 still holds) |
| Same op with `["yes", "no"]` | `False` (disagreement still fails the universal test) |

Statement B's box-1 amount is therefore included in the line-1 collect with no witness of its own. One statement's `"yes"` covers the other. Confirms P0 F2's C6 result. Track 6b's path-(j) fixtures (`tests/test_f1098e_student_loan_interest_agi_track6.py::TestPathJMultiStatementDisagreement`) prove the *disagreeing two-witness* case now blocks in both assertion orders; they do not construct the one-witness case.

Nothing in admission requires a witness per statement. Box-2 companion presence is the only per-statement coverage mechanism on this route (P0 F6 notion 2).

The same identity gap is loan-level, not only statement-level: the keys are lender + statement + tax-year. A statement that aggregates several loans has no per-loan witness slot. That is C7's identity problem; it is not a fold bug. The fold would still see values only even if a loan key existed.

### 2.4 Checks run

- Artifact dump of the five witnesses' `identity_keys` and `value_schema`.
- Focused marshal + evaluate of the C6 shape above (synthetic `demo.sli.*` ids).
- Code read: `marshal_run_context` source loop; `_Run.__init__` source fold; `collect_categorical_all_equal`; worksheet `choose` around those five nodes.

---

## 3. Whether the promise's preconditions are representable at all

The production promise requires three objects: an identified loan, an identified academic period, and an amount of interest attributable to that loan. **None of the three exists in the committed model.** The rule can consume a prepared statement-scoped box-1 amount and a prepared statement-scoped compressed witness. It cannot obtain or preserve a loan-and-period-keyed eligible-student showing, because those keys are not there to write.

This does not design replacements. It names what exists, what does not, and the nearest committed shape for each.

### 3.1 Identified loan, distinct from lender and statement — **does not exist**

**What exists.** Every Form 1098-E fact type in `f1098e.bundle.json` except the closure is keyed `lender` (`tax.us.student-loan-lender`) + `statement` (`tax.us.1098e-statement`) + `tax-year` literal `2025`. The closure is keyed `family-horizon` + `tax-year`. The Form 1098-E vocabulary uses exactly those two entity kinds, plus `kernel.family-horizon` on the closure. The 2025 corpus as a whole declares 26 entity kinds; a targeted search of it for a student-loan or debt identity, and for identity-key names `loan` / `obligation` / `period` / `academic-period` / `term` / `school` / `institution`, returns none tied to Form 1098-E. (Corrected 2026-09-14: this sentence previously claimed the whole corpus contained only those three kinds, which is false — the conclusion below is unaffected.) There is no `tax.us.student-loan`, no `loan` identity key, and no fact type that keys a student-loan object separately from the lender and the statement.

The box-1 title itself records the aggregation: "A lender may aggregate several qualified student loans on one statement." `tests/test_f1098e_student_loan_interest_track2.py::test_p2_same_lender_two_statements_both_admitted` treats two statements from one lender as "e.g. two loans" — a statement used as a loan proxy, not a loan identity.

**Nearest existing shape (other domains, not this deduction).**

- `tax.us.interest-obligation`, used only by `packages/content/tax/2025/obligation-acquisition.bundle.json` as the `obligation` key of `tax.us.obligation-acquisition-circumstance`, together with `tax.us.interest-payer` and `acquisition-year`. That is a debt-like entity distinct from payer and from a Form 1099-INT/OID statement. It is the accrued-interest / bond domain (ADR-0068). It is not a student loan and is not referenced from any 1098-E fact type.
- `tax.us.f1099b-transaction`, a sub-statement object under broker + statement, used for Form 1099-B covered transactions. Same pattern (object below a statement), different domain.
- `tax.us.acquisition-report-pairing`, a pairing record that associates one obligation with one report. Again ADR-0068; not wired to Form 1098-E.

Using the 1098-E statement as the loan would collapse mixed loans on one statement into one identity. That is the compression C7 forbids. This unit does not choose a substitute.

### 3.2 Academic period — **does not exist**

A scan of `packages/content/tax/2025/*.json` for `academic`, `enroll`, `half-time`, `course load`, and `eligible student` returned no files. No entity kind is a school, institution, term, or academic period. No fact type carries enrollment, program, or workload.

**Nearest existing shape.**

- The `tax-year` literal `2025` on every 1098-E fact. P1 already states that the tax year and the academic period are different objects, and that enrollment during 2025 is irrelevant except where 2025 is the period the loan financed.
- `acquisition_date` / `acquisition-year` on `tax.us.obligation-acquisition-circumstance` — a calendar date of bond purchase, not an academic period.

The compressed witness `no-non-qualified-loan-component` is a `{yes, no}` about the statement's box-1 figure. It has no period key and does not ask about enrollment or workload (the P1 loan-qualification record constituent 4, current representation). A prepared `"yes"` on that witness is something a rule can consume; it is not an academic-period fact.

### 3.3 Interest attributable to one loan on an aggregating statement — **does not exist**

**What exists.** Box-1 is one nonnegative number per statement. Family `tax.us.2025.f1098e.1` collects those statement amounts. The authorized subtotal is their raw sum. There is no per-loan amount field, no allocation fact type on a 1098-E identity, and no member below the statement.

Box-2 is an amount-composition qualifier for origination fees / capitalized interest on a pre-9/1/2004 loan. It is not a split of box-1 across loans. Its domain is `{null, false}`.

**Nearest existing shape (other domains).**

- `tax.us.nominee-allocation.amount` (`nominee-allocation.bundle.json`): a positive amount allocated from one identified Form 1099-INT to one named recipient. Identity is payer + statement + tax-year + `tax.us.interest-allocation-recipient`. That is a statement-amount split by *recipient*, produced by `packages/tax/nominee_allocation_recording.py`. It is not a split of Form 1098-E box-1 by loan.
- Pairing-scoped `tax.us.2025.interest.current-year-adjustment.pairing-scoped`: a per-pairing amount, not a per-student-loan amount, and not a 1098-E consumer.
- Form 1099-B covered-transaction scalar companions (proceeds / basis) at transaction identity under a statement — sub-statement amounts in a different family.

Without a per-loan amount, a statement that aggregates several loans has no representable "interest attributable to that loan." The collect of box-1 can only sum statement totals.

### 3.4 Plain result

| Promise precondition | Representable today? | Nearest committed shape |
| --- | --- | --- |
| Identified loan, distinct from lender and statement | No | `tax.us.interest-obligation` (bond/accrued-interest domain); 1098-E `statement` as a too-coarse proxy |
| Academic period | No | `tax-year` literal `2025` (a different object); no school/term/enrollment fact |
| Interest attributable to one loan on an aggregating statement | No | Statement-level box-1; nominee allocation splits a *1099-INT* by recipient, not a 1098-E by loan |

The three preconditions are therefore not representable as a set. A producer for the selected constituent would have nowhere in the committed 1098-E vocabulary to hang a loan key, a period key, or a per-loan amount. Item 6 records what each C7 resolution would require of that gap. This item does not choose among them.

### 3.5 Checks run

- Python walk of every `entity_kind` and of identity-key names `loan` / `obligation` / `period` / `academic-period` / `term` / `school` / `institution` under `packages/content/tax/2025/`.
- Text scan of that directory for `academic`, `enroll`, `half-time`, `course load`, `eligible student`: no hits.
- Direct read of `f1098e.bundle.json` identity keys, `obligation-acquisition.bundle.json`, `nominee-allocation.bundle.json`, `pairing-scoped-consequences.bundle.json`.

---

## 4. Lifecycle through the real path

A per-statement categorical witness (illustrated with `tax.us.2025.f1098e.no-non-qualified-loan-component`; the other four share the same identity, supersession, and admission path) can be corrected, retracted, and reasserted **as a prepared kernel fact**. The product has no producer that obtains that fact from an ordinary account, and `apply_contribution_batch` is not a retraction carrier.

### 4.1 What `contribution.py` will carry

**Artifact.** `packages/kernel/contribution.py` `apply_contribution_batch`. Successor kinds are exactly `{"assertion", "member-transition"}` (`_SUCCESSOR_KINDS`). Order: started contribution-record → apply the `contribution` act → apply each successor → terminal record listing asserted facts. Each successor finding must carry `contribution_id` matching the batch and must not put the contribution pin in `finding.pins` (provenance only, never a derivation edge).

The kernel will admit a prepared witness assertion through that batch: the five witnesses are not family members, so they use `assertion`, not `member-transition`. Confirmed: a synthetic ordinary-language-entry contribution of `"yes"` on `no-non-qualified-loan-component` for `demo.sli.lender.life` / `demo.sli.stmt.life` completed, with `contribution_id` stored on the finding.

A `finding-retracted` successor is refused before any act is applied: `successor act kind 'finding-retracted' is not a contribution carrier (expected assertion or member-transition)`.

`apply_contribution_batch` folds in-memory state. It does not open an `ActLog`. Persistence is the caller's problem unless a producer owns it.

### 4.2 Correction

Supersession policy on every 1098-E witness is `free`. A second contribution batch with a new `assertion` for the same `fact_id` and a new finding id is the correction path. Both findings remain in `state.findings`. `compute_currency` `_finding_corrections` displaces the earlier with reason kind `correction`. Marshalling reads only current finding ids.

Confirmed: `"yes"` (`demo.sli.life.wit.1`) then `"no"` (`demo.sli.life.wit.2`) on the same witness `fact_id`; current value `"no"`; original displaced `correction by demo.sli.life.wit.2`. No horizon advance (witnesses are not family members).

### 4.3 Retraction

Kernel path: act kind `finding-retracted`, payload `{ "finding_id": ... }`, applier `packages/kernel/findings.py` `apply_finding_retracted` (needs the envelope `act_id`). Six refusals: unknown finding; not current under `compute_currency`; `locked` policy; `closed-on-attestation` while the gate is true; currently a source-family member; prospective state violates an admission invariant (companion presence among them). Actor is recorded and never consulted.

Witnesses are not family members and are `free`, so retraction of a current witness finding is admitted. It ends current support. It writes no replacement value and no opposite claim. Historical assertions remain in the log.

Confirmed: retracting `demo.sli.life.wit.2` left no current witness finding; `retracted_finding_ids` contained that id; displacement reason `retraction by demo.sli.life.act.009`.

Box-1 **cannot** take this path. It is the family member predicate. Confirmed: `cannot retract finding demo.sli.life.box1: fact … is currently a source-family member; use a member-transition removal instead`. Membership removal is `member-transition` `remove`, which `apply_contribution_batch` *can* carry, and which advances the horizon.

### 4.4 Reassertion

A new contribution batch with a new assertion for the same `fact_id` after retraction is admitted. The retracted finding stays stored and non-current. The new finding is current.

Confirmed: `demo.sli.life.wit.3` value `"yes"` current; historical ids `wit.1`, `wit.2`, `wit.3` all still in `state.findings`.

Prepared-fact versus honest obtainment: the kernel preserves correction, retraction, and reassertion of a witness that someone already constructed. Nothing in this path asks a user about enrollment, program, or workload, or keys the answer on a loan or academic period.

### 4.5 What `nominee_allocation_recording.py` does that no Form 1098-E fact has a counterpart for

**Artifact.** `packages/tax/nominee_allocation_recording.py`. Contrast, not a design for this deduction.

| Capability | Nominee allocation | Form 1098-E (box-1, box-2, five witnesses, closure) |
| --- | --- | --- |
| Ordinary-answer producer | `assert_nominee_allocation`: closed `NOMINEE_ALLOCATION_ANSWERS_SCHEMA` (`circumstance` const `"nominee-allocation"`, payer name, statement reference, tax year, recipient id, amount) | None. Tests and this unit construct kernel acts directly. |
| Fact-id derivation from ordinary fields | `derive_nominee_allocation_fact_id` via `packages/tax/report_statement_identity.py` (payer + statement + tax-year + recipient) | None. Caller must already know the canonical `fact_id`. |
| Application-minted entity | `build_recipient_entity_act` for `tax.us.interest-allocation-recipient`; opaque id, never derived from typed display name; existing current recipient is reused, not re-introduced | Lender and statement entities are introduced in tests by hand. No minting helper. |
| Evidence-mode correspondence | Requires current `ordinary-language-entry` evidence whose submitted answers correspond to the mapped finding (`_require_ordinary_language_allocation_evidence`). A Form 1099-INT copy is not that evidence. | No 1098-E producer checks evidence mode or answer correspondence. |
| Durable `ActLog` ownership | Reads the log, semantically pre-applies every act, appends only after pre-checks, returns only a reprojection from the durable log | No 1098-E module appends to an `ActLog`. |
| Retraction helper | `retract_nominee_allocation`: product-specific, fact-type-guarded `finding-retracted` writer, because the contribution batch cannot carry that kind | No 1098-E retraction helper. Kernel `apply_act` works if a caller builds the act. |
| Correction as the same producer | `assert_nominee_allocation` is also the correction path (same `fact_id`, new finding) | Generic `apply_contribution_batch` can correct a prepared witness; nothing produces the correction from an ordinary account. |

The nominee module publishes no rule and no derived symbol. A later adopted rule decides tax consequence. That split is the pattern P0 F1 names as the missing entry path for this deduction's ten eligibility and scope answers.

### 4.6 Checks run

- Focused contribution-batch lifecycle on `no-non-qualified-loan-component` (assert → correct → batch-refuses-retraction → `apply_act` retraction → reassert).
- Box-1 `finding-retracted` refused as a family member.
- Direct read of `apply_contribution_batch`, `apply_finding_retracted`, `assert_nominee_allocation`, `retract_nominee_allocation`.

---

## 5. Entry and mapping path (P0 F1)

P0 F1's three observations are **confirmed**, and they stay separated. The selected constituent does not yet have an entry path. Generic admission of the *compressed* witness is not an entry path for eligible-student status.

The ten answers F1 names:

- per-statement: `no-related-person-interest`, `no-qualified-employer-plan-interest`, `no-non-qualified-loan-component`, `no-employer-educational-assistance-interest`, `no-qtp-earnings-used`
- filer-level: `sli-scope.no-form-2555`, `sli-scope.no-form-4563`, `sli-scope.no-puerto-rico-or-samoa-income`, `sli-scope.not-claimed-as-dependent`, `sli-scope.legally-obligated-for-interest`

### 5.1 Producer search — confirmed

Grep of `packages/**/*.py` for those ten fact-type ids: no hits. `packages/tax/` in particular has no 1098-E producer. The contrast named by P0, `packages/tax/nominee_allocation_recording.py`, exists and is unused by this deduction (item 4).

Outside production code, two non-producers construct or mention them:

- `tests/` (including `tests/test_f1098e_student_loan_interest_agi_track6.py` `_f1098e_acts`) builds kernel acts in memory for fixtures.
- `tools/generate_f1098e_track8_presentation_goldens.py` reuses that Track 6 choreography, including a `no-related-person-interest: "no"` statement, to regenerate presentation goldens.

`tools/generate_f1098e_track6_content.py` lists `sli-scope.bundle.json` as a package member. It does not contribute an answer.

No module turns a user's ordinary account into any of the ten.

### 5.2 `input_bindings` absence is marshalling evidence only — confirmed

**Artifact.** `packages/content/tax/2025/package.core-calculations.v38.json` `input_bindings`: seven entries (`filing_status`, `rounding.convention`, `spouse_blind`, `spouse_over_65`, `tax.us.2025.deductions.itemized`, `taxpayer_blind`, `taxpayer_over_65`). None of the ten.

How a *prepared* current finding of one of the ten reaches a run:

- **Per-statement five.** `live.py` `_resolved_run_material` walks `rule.sli-worksheet.json` `when`/`value` for `collect_categorical_all_equal` names and appends those fact-type ids to `collect_source_names`. `marshal.py` then emits one `SourceFact` per current finding of that type into `ctx.sources`. The evaluator reads `env.sources` (item 2). Not an `input_bindings` path.
- **Filer-level five.** Read by unkeyed `ref` inside the worksheet's `conditional_dependency_set` / `categorical_compare`. They are not collect source names and are not in `input_bindings`. `marshal.py`'s unbound-symbol fallback binds a type id that some rule requires, when current findings for that type agree. Disagreement leaves the symbol unbound (`DEPENDENCY_ABSENT`). Filer-level facts are keyed by `tax-year` alone, so one current finding is the expected cardinality.

Absence of `input_bindings` does not prove a finding cannot be created. Item 4 created one through `apply_contribution_batch`.

### 5.3 Generic admission is available — confirmed

`apply_contribution_batch` admits a prepared `assertion` for any of these declared fact types. Item 4 admitted, corrected, and reasserted `no-non-qualified-loan-component` that way. Nothing in the fact types prevents admission. What is absent is the producer that would turn a user's account into such an assertion.

Admitting the compressed `no-non-qualified-loan-component` `{yes, no}` is **not** an entry path for the selected constituent. That fact asks whether a non-qualified-loan component is absent from box 1. It does not ask about enrollment, program, or workload, and it is not keyed on a loan or academic period (the P1 loan-qualification record constituent 4, current representation).

### 5.4 What a producer for the selected constituent would have to accept

Without designing it. Given P1's production promise, item 3's missing identities, and item 4's lifecycle path:

- **Ordinary inputs, not the tax conclusion.** School, program, the academic period the borrowed money paid for, and course load. Not "were you an eligible student" and not the compressed `{yes, no}` on `no-non-qualified-loan-component`.
- **Institutional and public-authority inputs the application cannot push onto the user:** program candidacy; institutional eligibility by § 25A(b)(3)(A) → HEA § 484(a)(1) → HEA § 1094 (not the chapeau's § 25A(f)(2) → HEA § 481 route); the institution-defined half-time threshold for that period. Where those cannot be established, the route stays unresolved, never favorable.
- **The three promise objects.** An identified loan distinct from lender and statement; an identified academic period distinct from tax year; an amount of interest attributable to that loan. None of those is representable today (item 3). A producer that accepted only a Form 1098-E statement identity would be accepting the wrong object.
- **Unknown or mixed composition as unresolved.** A statement that aggregates several loans, or a loan that financed several periods, must not be treated as uniform. The producer cannot honestly emit a single statement-scoped `{yes, no}` as the (C) answer in those cases.
- **Contribution boundary and lifecycle.** Assertion (and correction / reassertion) through `apply_contribution_batch`; retraction through a `finding-retracted` path the batch cannot carry, as the nominee producer already does for a different fact. Historical assertions remain provenance.

This milestone, per P0 F1's consequence, builds the first such producer for this deduction rather than displacing a question the product asks today. This item does not design that producer.

### 5.5 Checks run

- Grep of `packages/**/*.py` and `packages/tax/**/*.py` for the ten fact-type ids: no production hits.
- Grep of `tools/**/*.py`: Track 8 golden generator and Track 6 content packager only.
- Dump of v38 `input_bindings` (seven symbols; none of the ten).
- Item 4's contribution-batch admission of a prepared per-statement witness.

---

## 6. C7 representability

C7 is one statement aggregating more than one loan. The selected constituent is debt- and period-scoped, so the statement- or debt-scoped branch of C7 applies: the plan must carry honest identity for the indebtedness or explicitly refuse the class. P1 requires the milestone to deliver exactly one of three resolutions. This item does not choose. It says what the committed model can support today, and what each resolution would require, given items 3 and 4.

**None of the three is delivered by the committed model.** The C6 one-witness fold (item 2) passes both statement amounts. Box-1 is a statement total. There is no loan key, no period key, and no per-loan amount (item 3). The compressed witness is not (C).

### 6.1 Supportable single-loan single-period association — **not supportable today**

Would require, at minimum:

- A representable **loan** distinct from `lender` and `statement` (item 3.1). Using `tax.us.1098e-statement` as the loan pretends every aggregated loan is the same object.
- A representable **academic period** distinct from `tax-year` (item 3.2). Using 2025 as the period pretends enrollment-year equals financed period. One loan can still mix periods.
- An association, at that loan-and-period identity, that this statement's box-1 is entirely interest on that one loan for that one period — a proposition that can be corrected, retracted, and reasserted (item 4) without silently establishing the chapeau, (A), or (B).
- A way to keep mixed or unknown composition off this path. The committed fold will not do that: one `"yes"` covers every statement amount.

The nearest existing association shape is ADR-0068's acquisition-to-report pairing (`tax.us.acquisition-report-pairing` / `tax.us.interest-obligation`). It is not wired to Form 1098-E, and it does not encode an academic period. This unit does not adopt it.

### 6.2 Honest per-loan allocation — **not supportable today**

Would require, at minimum:

- Identified loans (item 3.1) for every loan the statement aggregates.
- A **per-loan amount** whose relationship to the statement's box-1 is honest (item 3.3). No such amount exists. `collect` of box-1 can only sum statement totals.
- Academic-period identity per loan, because (C) can hold for one period a loan financed and fail for another.
- Lifecycle of those amounts: contribution-batch assertion/correction/reassertion, and a `finding-retracted` path the batch cannot carry (item 4).

The nearest existing split is `tax.us.nominee-allocation.amount`: a positive amount taken from one Form 1099-INT for one recipient, produced by `nominee_allocation_recording.py`. It is the wrong statement family, the wrong extra key (recipient, not loan), and it is not a 1098-E producer. Reusing it as a student-loan allocation would be a different proposition. This unit does not design a counterpart.

Without per-loan amounts, "remove interest attributable to a disqualified loan from worksheet line 1" has no input.

### 6.3 Refusal on unknown composition — **not delivered today; does not require loan identity**

This is the only of the three that does not need a loan or period key in order to be *honest*. Unknown composition is the current state of every 1098-E statement: the form omits which loans box-1 aggregates and in what proportion (P0.1).

What the committed model does instead:

- Nonempty family, missing witness: `DEPENDENCY_ABSENT` (C3). That is absence of the compressed answer, not a named unknown-composition refusal.
- Nonempty family, one `"yes"` witness, several statements: the universal test **passes** and both amounts collect (item 2). Unknown composition is treated as covered.
- Adverse compressed `"no"`: `SLI_UNIVERSAL_COMPONENT_VIOLATION`. That code does not name composition, enrollment, or (C) (P0 F3).
- Closed-empty: literal `0` (item 1 / P0 F7), a numeric deduction, not a refusal.

So a refusal-on-unknown-composition resolution could use existing block/unavailable *machinery* without inventing a loan entity, but it is not what the committed rules do, and no committed block code names unknown composition. It would still require:

- A condition that composition is unknown (today that is always true of box-1; a later association or allocation path would have to turn the condition off when composition is actually known).
- A product disposition that is a refusal, not a box-1 pass-through and not a closure-backed zero.
- A reader-facing reason that names unknown composition rather than `SLI_UNIVERSAL_COMPONENT_VIOLATION` or `DEPENDENCY_ABSENT`.
- The same lifecycle honesty as C5: retracting a later composition-known assertion must return the route to refusal, not revive a prior compressed `"yes"`.

### 6.4 Plain result

| C7 resolution | Committed model today | What it would require |
| --- | --- | --- |
| Single-loan single-period association | Cannot support honestly | Loan identity, period identity, an association at that pair, and mixed/unknown kept off the path |
| Honest per-loan allocation | Cannot support | Loan identity, per-loan amounts related to box-1, period identity per loan, allocation lifecycle |
| Refusal on unknown composition | Not delivered; coverage failure currently *passes* | A named refusal when composition is unknown; does not itself require a loan key |

Which resolution a resumed milestone delivers is not chosen here.

### 6.5 Checks run

- Items 2–5's executing checks (C6 fold; entity-kind dump; contribution/retraction lifecycle; producer search).
- Plan text: P1 selection's three C7 resolutions; *Fixed cases* C7 statement- or debt-scoped branch.
