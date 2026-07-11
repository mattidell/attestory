# Round 2 — Fresh-Reader Legibility Recovery (it2 rival artifacts)

Reviewer: context-starved legibility seat (owner-launched, fresh session).
Method: I read only my role file, the round-2 "Legibility scope" section, and the
four artifact files it names (`package.json`, `rules.json`, `parameters.json`,
`schemas/prototype.schema.json`, all from branch `prototypes/rule-language/it2`).
No governance docs, no examination, no charter, no it1 materials, no tests, no
evaluator source, no git history. Every claim below is recovered from the four
artifacts alone. Where I had to import outside knowledge (tax semantics, evaluator
behavior) to make a span mean anything, I mark it as an **assumed-knowledge finding**
rather than pretending I recovered it.

Confidence scale: **certain** / **probable** / **guessing**.

---

## A. The expression language (recovered from the schema + observed usage)

The schema closes the operator set. An `expr` is either a JSON scalar
(`string`/`number`/`boolean`/`null`) used as a literal, or an object with a
required `op` drawn from this fixed enum:

```
ref, collect, parameter, add, subtract, max, compare, all, any, not,
choose, range_lookup, bracket_fold, round
```

Recovered meaning of each op (from how rules use them; **certain** unless noted):

- `ref {name}` — read a previously **published symbol** by name (e.g. `interest.gross`).
- `collect {name}` — gather every instance of a raw input field (e.g. `w2.box1`
  across all W-2s). **Probable**: I infer "gather all occurrences" because `collect`
  is always wrapped in `add`, which implies a multiset being summed. The artifact
  never defines `collect`, so the many-instances semantics is an inference, not a
  recovery. *(finding L-1)*
- `add {args:[...]}` — n-ary sum of its argument expressions.
- `subtract {left,right}` — `left - right`.
- `max {args:[...]}` — maximum of the arguments (used only as `max(0, …)`, i.e. a floor).
- `compare {left,right,cmp}` — boolean; `cmp ∈ {eq,ne,gt,gte,lt,lte}`.
- `parameter {parameter_id, key?}` — look up a declared parameter; optional `key`
  selects a sub-entry (used with `key = ref filing_status` for the standard-deduction table).
- `range_lookup {table_id, key, value}` — find the row in `table_id`'s `key`
  sub-table whose `[lower,upper]` band contains `value`, and return that row's
  `value` field. **Probable** — see L-6.
- `bracket_fold {table_id, key, value}` — compute progressive tax by folding `value`
  across the bracket rows of `table_id`'s `key` sub-table (per-band `rate`). **Probable/guessing**
  — the *fold arithmetic* is not stated anywhere; I infer standard marginal-bracket
  accumulation. *(finding L-7)*
- `round {args:[expr], mode, stage}` — round the (single) argument; `mode` is an
  expression (always `ref rounding.convention`); `stage ∈ {source, after_aggregate, final}`.
  **Guessing** on what `stage` changes operationally — see L-2.
- `all`, `any`, `not`, `choose {when,then,else}` — declared in the grammar but
  **never used** by any rule in `rules.json`. I can only recover their intended
  shape (boolean AND/OR/NOT; a conditional select), not confirm behavior. *(finding L-3)*

**Structural finding L-4 (schema does not constrain ops per-shape):** the `expr`
object lists all keys (`name`, `args`, `left`, `right`, `cmp`, `when`, `then`,
`else`, `value`, `table_id`, `mode`, `stage`, `key`, `parameter_id`) as optional
with `additionalProperties:false`, but nothing ties a given `op` to *which* keys
are mandatory. The schema would accept a `round` with no `mode`, a `compare` with
no `cmp`, or an `add` with a stray `left`. So the grammar is enumerated but not
tight: an artifact can be schema-valid yet semantically malformed. This weakens the
"meaning recoverable from the artifact" claim only slightly (the used rules are all
well-formed), but a fresh reader cannot rely on the schema to reject nonsense exprs.

---

## B. Parameters (`parameters.json`)

All five are `parameter-declaration` citizens scoped to tax_year 2025,
US-federal, individual-income-tax, effective 2025-01-01. **All monetary values are
JSON strings**, not numbers — I read this as a deliberate decimal-as-string choice
to avoid binary float (**probable**; the artifact doesn't say why, but the pattern
is unambiguous). Recovery:

| parameter_id | shape | recovered meaning | conf. |
|---|---|---|---|
| `standard-deduction.2025` | map keyed by filing status | Standard deduction: single 15000, MFJ 30000, MFS 15000, HoH 22500, QSS 30000. | certain |
| `schedule-b-threshold.2025` | scalar `"1500"` | The 1500 threshold that routes taxable interest onto Schedule B vs. directly to the 1040. | certain (mechanism); the *number's* legal meaning is assumed-knowledge |
| `regular-tax-split.2025` | scalar `"100000"` | The 100000 cutoff that selects tax-table lookup (below) vs. bracket-fold worksheet (at/above). | certain (mechanism) |
| `tax-table-sample.2025` | map: filing status → list of `{lower,upper,value}` | A **sparse** precomputed tax table: for a taxable-income band `[lower,upper]`, the tax is `value`. Only a handful of bands per status (single has 3, MFJ 2, HoH 1). | certain (structure) |
| `tax-brackets.2025` | map: filing status → list of `{lower,upper,rate}` | Progressive marginal brackets (10%/12%/22%/24%/32%/35%/37%), top band has `upper: null` (open-ended). single, MFJ, HoH only. | certain (structure) |

Findings from the parameters:

- **L-5 (missing filing statuses in tables):** `standard-deduction` covers five
  filing statuses, but both `tax-table-sample` and `tax-brackets` cover only
  `single`, `married_filing_jointly`, `head_of_household`. A return filed
  `married_filing_separately` or `qualifying_surviving_spouse` can obtain a standard
  deduction but has **no tax table and no brackets** — the line-16 rules would find
  no matching `key` sub-table. From the artifact alone this looks like an incomplete
  corpus; rule `f7.tax-table-line16`'s note ("Prototype corpus contains only rows
  exercised by fixtures; unrepresented rows block rather than invent a value")
  self-declares this as intentional scoping. I record it as a recovered *limit*, not
  a bug, because the artifact tells me so — a good legibility mark.

- **L-6 (band boundary convention unstated):** `tax-table-sample` bands are
  `[lower,upper]` half-open? closed? The rows are like `14950–15000`, `15000` shared
  as an `upper` of one row and never a `lower` of the next (rows are non-adjacent,
  50-wide islands). Whether a `value` exactly on a boundary lands in a row is not
  recoverable. For `tax-brackets` the bands *are* adjacent (`upper` of one == `lower`
  of next, e.g. 11925), so boundary handling matters and is **not stated**. I must
  assume the standard "lower ≤ x < upper" convention. *(assumed-knowledge)*

---

## C. Package (`package.json`)

`artifact-package` `package:first-tax-slice.2025.rival` v1, scope 2025 / US-federal /
individual-income-tax. It is a **closure manifest**: a flat `members` list, each a
*pin* of `{role, citizen_id, version}`. It pins the 5 parameters and 26 rules with a
`role` tag per member: `parameter`, `rule`, `mapping`, or `bridge`.

**Recovered purpose (certain):** the package enumerates exactly which citizen
versions constitute "the first tax slice" — a reproducible bill of materials. Every
`parameter_id` referenced by a rule (`standard-deduction`, `schedule-b-threshold`,
`regular-tax-split`, `tax-table-sample`, `tax-brackets`) is a package member, so the
package is **parameter-closed** with respect to the rules it lists. Good closure signal.

Findings:

- **L-8 (member `role` vs. rule `role` mismatch in vocabulary):** the package tags
  members with `mapping`/`bridge`, but the rule artifacts themselves carry
  `role: field-mapping` / `cross-form-bridge`. So the same rule is `"mapping"` in the
  package and `"field-mapping"` inside the artifact. A fresh reader must guess that
  `mapping`≙`field-mapping` and `bridge`≙`cross-form-bridge`. The mapping is obvious
  but not stated — a small legibility seam. Also the pin `role` enum in the schema
  (`input, choice, parameter, rule, mapping, bridge, adoption, governance, engine`)
  is a *third* vocabulary, broader than either.

- **L-9 (closure is over declared members, not over referenced symbols):** the
  package guarantees the listed citizens are present, but nothing in the package
  asserts that every symbol a rule *consumes* is produced by a member (see the
  dangling `form1040.line24` / `.line33` in §D). Package closure ≠ dataflow closure.

---

## D. Rules (`rules.json`) — the computation graph

26 rule artifacts, each `rule-artifact` v1, same scope. Common shape:
`requires` (symbolic deps), `when` (a boolean guard; `true` = unconditional),
`value` (the expression computed), `publishes` (the output symbol), `blocked`
(`{code, missing}` — recovered as: *if a required input is unavailable, halt this
rule and emit this diagnostic code naming what's missing*; **probable**). The
`f<N>` prefix in each id (`f1`, `f2`, `f11`, …) I read as a **form-step tag**
grouping rules by the worksheet step they implement (**guessing** on the exact
numbering scheme).

### Recovered dataflow (plain English)

**Wages (f1)** — `wages-to-1040-line1a`: collect every `w2.box1`, sum, round → `form1040.line1a`.

**Interest income (f2, f11)**
- `f2.interest-gross`: collect `int1099.box1` + `int1099.box3`, sum, round → `interest.gross`.
- `f11.taxable-interest-no-box3`: **when** sum(`int1099.box3`) == 0 → `interest.taxable = interest.gross`.
- `f11.taxable-interest-with-exclusion`: **when** sum(`int1099.box3`) > 0 →
  `interest.taxable = round(interest.gross − savings_bond.excludable_interest)`.
  These two partition on box3, so exactly one publishes `interest.taxable`. (**certain**
  they're mutually exclusive; the *reason* box3>0 triggers a savings-bond exclusion
  path is assumed-knowledge — box3 = US savings bond / Treasury interest. *L-10*)

**Schedule B routing (f3a)** — two complementary producers of `form1040.line2b`:
- `schedule-b-part-i-applicability`: **when** `interest.taxable` **>** threshold(1500)
  → `schedule_b.part_i.applicable = true`.
- `f2.interest-to-schedule-b-line1`: `schedule_b.line1 = interest.gross` (requires
  `schedule_b.part_i.applicable`, so effectively only when applicable).
- `f11.exclusion-to-schedule-b-line3`: `schedule_b.line3 = interest.gross − interest.taxable`
  (the excluded amount).
- `f2.schedule-b-line4`: `line4 = line1 − line3`.
- `f2.schedule-b-to-1040-line2b` (bridge): `form1040.line2b = schedule_b.line4`.
- `f3a.direct-interest-to-1040-line2b`: **when** `interest.taxable` **≤** threshold
  → `form1040.line2b = interest.taxable` (bypass Schedule B).
  The `>`/`≤` guards make the Schedule-B path and the direct path mutually exclusive,
  so `form1040.line2b` has a single producer for any given return. **certain** (this is
  a clean guarded-exclusivity pattern; I note it because duplicate-output ordering is
  exactly the kind of thing this design seems built to prevent).

**Schedule B Part III / foreign accounts (f3b)**
- `part-iii-applicability`: **when** `foreign_account.exists` == true → `schedule_b.part_iii.applicable`.
- `part-iii-questions`: → publishes the literal string `"schedule_b.part_iii.questions.7a_7b_8"`.
  This is an **opaque token** — I recover that Part III asks questions "7a, 7b, 8" but
  what those questions *are* is not carried by the artifact. *(assumed-knowledge, L-11)*

**Withholding (f4)**
- `w2-withholding-to-line25a`: collect `w2.box2`, round → `form1040.line25a`.
- `interest-withholding-to-line25b`: collect `int1099.box4`, round → `form1040.line25b`.
- `withholding-components-to-line25d`: `line25d = line25a + line25b`.

**Standard deduction (f5)** — `standard-deduction`: look up
`parameter:standard-deduction.2025` keyed by `filing_status`, round → `form1040.line12`.

**Totals / AGI (f12, f6)**
- `f12.total-income-line9`: `line9 = line1a + line2b`. (**L-12**: total income here is
  *only* wages + taxable interest; no other income types — recovered as the slice's
  deliberately narrow scope.)
- `f12.penalty-to-schedule1-line26`: collect `int1099.box2`, round → `schedule1.line26`.
  (box2 = early-withdrawal penalty — assumed-knowledge, *L-10*.)
- `f12.schedule1-to-1040-line10` (bridge): `form1040.line10 = schedule1.line26`.
- `f12.agi-line11`: `line11 = line9 − line10`.
- `f6.taxable-income-floor`: `line15 = max(0, line11 − line12)`. (Floors taxable income
  at zero; standard deduction can't create a negative. **certain**.)

**Tax (f7)** — two complementary producers of `form1040.line16`, split on `line15`
vs `regular-tax-split` (100000):
- `tax-table-line16`: **when** `line15` **<** 100000 → `range_lookup` the sparse
  `tax-table-sample` by `filing_status`, round → `form1040.line16`.
- `worksheet-line16`: **when** `line15` **≥** 100000 → `bracket_fold` the
  `tax-brackets` by `filing_status`, round → `form1040.line16`.
  Guards are exclusive → single producer. **certain** on routing; **probable** on
  `range_lookup` semantics, **guessing** on `bracket_fold` arithmetic (L-7).

**Refund / balance due (f8)** — two complementary producers, split on line33 vs line24:
- `overpayment-line34`: **when** `line33` **>** `line24` → `line34 = line33 − line24`.
- `amount-owed-line37`: **when** `line24` **>** `line33` → `line37 = line24 − line33`.

### Dangling-reference finding (L-13, important)

`f8` consumes `form1040.line33` and `form1040.line24`, but **no rule in this package
publishes either symbol**. Tracing every `publishes` in `rules.json`, the produced
set is: line1a, line2b, line9, line10, line11, line12, line15, line16, line25a/b/d,
line34, line37, schedule1.line26, interest.*, schedule_b.*. Neither `line24` (total
tax) nor `line33` (total payments) is produced. So the refund/owed rules are
**structurally unsatisfiable within this package** — they would perpetually `blocked`
on missing dependencies. Likewise `form1040.line16` (tax) and `form1040.line25d`
(withholding) are computed but **never consumed** — the wiring from line16→line24 and
line25d→line33 is absent. From the artifact alone this reads as an **incomplete slice**:
the graph has produced leaves (16, 25d) and unproduced needs (24, 33) that the missing
"total tax" and "total payments" summation rules would bridge. I cannot tell whether
this is intentional scoping or an omission; the package does not declare its own
dataflow completeness (L-9).

### `requires` vs `collect` asymmetry (L-14)

Rules list *symbolic* dependencies in `requires`/`blocked.missing` (e.g.
`rounding.convention`, `interest.gross`, `filing_status`) but do **not** list the raw
form boxes they `collect` (e.g. `w2.box1`, `int1099.box3`). So `f1` `requires` only
`rounding.convention` though it plainly needs W-2 data. Recovered model (**probable**):
raw form inputs are treated as an ambient fact source that's always "present" (empty
collect = 0), whereas `requires` tracks *derived* prerequisites whose absence should
*block*. A fresh reader can follow it, but the omission means `requires` is **not** a
complete input manifest — you cannot enumerate a rule's real inputs from `requires` alone.

### `stage` on `round` (L-2)

`round` carries `stage ∈ {source, after_aggregate, final}`. Observed: `after_aggregate`
on collect-then-sum rules (round the total), `final` on terminal computations
(standard deduction, taxable-interest-with-exclusion, both line16 rules). `source` is
never used. The operational difference — presumably *when* in a pipeline rounding is
applied (per-source vs post-aggregation vs end-of-chain) — is **not defined by any
artifact**. I recover the intent (rounding discipline is explicit and staged, which is
a genuine strength) but not the precise semantics. *(assumed-knowledge / guessing)*

### `blocked` codes (L-15)

Each rule's `blocked.code` is a self-describing diagnostic: `OPEN_DEPENDENCY` (generic
missing upstream), `OPEN_EXCLUSION_FACT` (savings-bond exclusion amount),
`OPEN_ELECTIVE_FACT` (filing status), `OPEN_FOREIGN_ACCOUNT_FACT`, `OPEN_TAX_TABLE_ROW`
(no matching table band). These are legible without outside help — the code names the
*category* of missing input. Good recoverability. One mismatch worth noting:
`f11.taxable-interest-with-exclusion` `requires` includes `interest.gross` and
`rounding.convention`, but its `blocked.missing` lists only `savings_bond.excludable_interest`
— so `blocked.missing` is a *curated headline* of the most salient gap, not a mirror of
`requires`. (**probable**; consistent across rules where they differ.)

---

## E. Schema-declared citizens I did *not* receive as artifacts

The schema's top-level `oneOf` admits seven citizen kinds; my scope contained only
three (`rule`, `parameters`, `package`). The other four are declared but not exercised
in the files I read — I can recover their *shape* only:

- **`adoption` (`adoption-act`)** — records an actor adopting a package into a
  workspace at a revision: `{act_id (act:adoption:…), actor_id, workspace_revision,
  package (pin), scope}`. Recovered intent: an audit act binding "who turned on which
  package, where."
- **`publication` (`derived-publication-act`)** — `{act_id (act:publication:<24 hex>),
  actor_id, workspace_revision, run_id, finding_id, claim, pins}`. Intent: an act
  asserting a derived finding from a run, with provenance pins.
- **`finding` (`derived-finding`)** — `{finding_id (finding:derived:<24 hex>), symbol,
  value, version:"v1", pins}`. Intent: one computed output value for a `symbol`, with
  the pins (citizen versions) that produced it. **This is the recovered output-ownership
  contract**: a result is inseparable from the pinned inputs that made it.
- **`record` (`derivation-record`)** — `{record_id, run_id, phase (started/completed/
  interrupted/failed), workspace_revision, governance_pins, adoption_pin, read[],
  published[], blocked[], stop_reason (started/saturated/interrupted/validation-failed/
  execution-failed)}`. Intent: a per-run ledger of what was read, what was published,
  what blocked, and why the run stopped. `saturated` I read as "fixpoint reached — no
  more rules can fire" (**guessing**).

I flag (L-16) that the `act:publication` and `finding:derived` ids require a
24-hex-char content address (`[a-f0-9]{24}`), implying content-addressed provenance,
while `act:adoption` and rule/parameter ids are human-readable slugs. Two id
disciplines coexist; the reason is inferable (machine-generated acts vs authored
citizens) but unstated.

---

## F. Assumed-knowledge findings (the core legibility measure)

These are spans where the artifact's meaning is **not** self-contained — a fresh
reader must import tax or evaluator knowledge:

1. **L-1** `collect` — many-instance-gather semantics never defined.
2. **L-2** `round.stage` (source/after_aggregate/final) — operational meaning undefined.
3. **L-6** table/bracket band boundary convention (open vs closed intervals) — undefined,
   and it *matters* for adjacent bracket bands.
4. **L-7** `bracket_fold` — the progressive-tax fold arithmetic is nowhere specified;
   recovered only by importing knowledge of marginal-rate taxation. The rule note even
   says "the evaluator only folds generic ranges," confirming the math lives in the
   evaluator, not the artifact.
5. **L-10** form-box meanings: `int1099.box2` = penalty, `box3` = savings-bond/Treasury
   interest triggering an exclusion, `box4` = withholding, `w2.box1/box2` = wages/withholding.
   The artifact uses these boxes as bare names; their meaning is imported IRS-form knowledge.
6. **L-11** `"schedule_b.part_iii.questions.7a_7b_8"` — an opaque literal; the questions
   themselves aren't carried.
7. **L-5 / L-12 / L-13** scope limits (missing filing statuses; income = wages+interest
   only; line24/line33 unproduced) — recoverable as *facts about the graph*, but whether
   each is intentional requires outside context. Two of these (L-5, tax-table row gaps)
   the artifacts self-declare via `notes`; the line24/line33 gap (L-13) they do **not**.

## G. What was strongly recoverable (positive marks)

- The **operator grammar is closed and enumerable** (schema), so a rule's space of
  possible meanings is bounded — the single biggest legibility asset here.
- **Guarded exclusivity** on the three doubled outputs (`form1040.line2b`, `.line16`,
  and the line34/line37 refund-vs-owed pair) is expressed *in the artifacts* via
  complementary `when` conditions — I could confirm single-producer behavior without
  any tie-break rule or external ordering.
- **Rounding is explicit** (every monetary aggregation names a convention and a stage),
  even though the stage *semantics* aren't (L-2).
- **Provenance is first-class**: `finding` pins its producing citizen versions, and
  `record` logs read/published/blocked per run — output ownership is legible by design.
- **`blocked` diagnostics are self-describing** — you can tell *why* a rule can't fire
  from its own code + missing list.

## H. Confidence summary

| Artifact | Overall recovery confidence |
|---|---|
| `parameters.json` | **certain** on structure; boundary/decimal conventions probable |
| `package.json` | **certain** (it's a closure manifest); role-vocab seam noted |
| `rules.json` — dataflow graph | **probable→certain** for wiring; `bracket_fold`/`stage`/`collect` semantics **guessing** |
| `prototype.schema.json` | **certain** on the grammar/citizen shapes; unexercised ops (all/any/not/choose) and un-received citizens recovered by shape only |

Net: the *skeleton* (which rule feeds which line, which guards partition which output)
is highly recoverable from the artifacts alone. The *arithmetic leaves*
(`bracket_fold`, rounding `stage`, band boundaries) and the *form-box vocabulary* are
where the artifact stops carrying its own meaning and the evaluator / IRS knowledge
takes over. The one place the graph is self-inconsistent as delivered is the dangling
`form1040.line24`/`.line33` in the f8 refund/owed rules (L-13).
