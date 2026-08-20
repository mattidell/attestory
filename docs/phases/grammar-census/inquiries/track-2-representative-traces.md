# Track 2b-i — Representative traces

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 2b-i — representative traces
- Role: Builder
- Status: in progress
- Source ref verified: `HEAD` `c889f7ca918cd39ed6fa1c5a1303a929979e1592`
  on `milestone/grammar-census-engine-language-map`
- Assigned path: this file only
- Primary input: `docs/phases/grammar-census/inquiries/track-2-reconciliation.md`
  (166 constructs, accepted at `f276cc5b`)
- Charter: `docs/reviews/2026-08-20-grammar-census-track-2b-traces-and-tensions-charter.md`

This is a **small set of semantically contrastive traces**, not a tax-coverage
census and not the tension catalog. Every material claim cites a committed
path (with schema version where the artifact is versioned), a reconciled
construct id (`U-###`), or an execution shown below. Traces cite the
reconciliation; they do not cite the sibling tension-catalog stream.

## Evidence convention

Every step is tagged **Executed** or **Inferred**. A step that mixes the two
is a defect in this file.

- **Executed.** A command this builder ran, or an existing test this builder
  re-ran, with the invocation and the result. Schema validation of named
  files via `DerivationSchemas.validate_declared` is executed.
- **Inferred.** A conclusion from reading committed code or content. Each
  inferred step names what would falsify it.

Synthetic executions import `packages.derivation.evaluator`,
`packages.derivation.declarative_validation`,
`packages.derivation.package_validation._predicate_depth`, and
`packages.derivation.loader.DerivationSchemas`. No personal data. No
absolute workstation paths.

Content is classified by the instance `schema` field, never by filename.

## Selection

The plan's starter contrasts are arithmetic composition, conditional
applicability, source-set closure and blocking, categorical reasoning, and
a worksheet-like computation. That is a starting set, not a quota. A sixth
trace is included because the reconciled census has a **second, nested
expression grammar** on `source-family.v2` (U-112–U-124) that none of those
five exhibits.

| Trace | Contrast | Construct no other trace in this set is for | Ends in |
| --- | --- | --- | --- |
| 1 | arithmetic composition | U-008 `add` flattening a U-004 `collect` (the common sum-of-members path) | published finding |
| 2 | conditional applicability | U-032 / U-043 false `when` → ledger `inapplicable` with a real `guard_result` | inapplicable (not a block) |
| 3 | source-set closure | U-024 `require_closed` and the empty/unclosed vs nonempty-unclosed split of U-004 / U-005 | `SOURCE_SET_UNCLOSED` block, and the closed-empty zero |
| 4 | categorical reasoning | U-022 `categorical_compare` + U-023 `category_literal` (368/373 primary occurrences; all observed `cmp` is `eq`) | boolean used as a `choose` / `when` discriminator; out-of-domain is `DEPENDENCY_INVALID` |
| 5 | worksheet-like computation | U-013 `multiply`, U-014 `divide`, U-017 `choose`, U-006 `block`, U-025 `conditional_dependency_set`, U-026 `collect_categorical_all_equal` composed as one citizen | published dollar amount, or `SLI_*` / `DEPENDENCY_ABSENT` |
| 6 | nested term/predicate grammar | U-109 `member_constraints` evaluated by `declarative_validation.py`, not by `evaluator.evaluate` | `FAMILY_VALIDATION_BLOCKED` (internal); v2 ledger remaps |

Stop rule: a seventh trace would repeat a construct already in this table
(attachment completeness is another "evaluate then block" on a different
citizen; `bracket_fold` is 95 uses of an unread spec; `range_lookup` is
unused in the primary corpus). Those are catalog material, not additional
traces.

**Content vs synthetic.** Traces 1, 3, 4, 5, and 6 start from 2025 primary
content. Trace 2 starts from committed sample_data: no primary rule-artifact
has `"when": false`, and no primary file's top-level `when` is a numeric
`compare` (Track 1c C05: top-level `when.op` is `all` × 35,
`categorical_compare` × 11, `require_closed` × 8, `choose` × 2,
`conditional_dependency_set` × 1). The asserting runner test for false-guard
→ inapplicable is the demo tax-table rule. Production `when` trees that go
false do so through constructs traces 3–5 already cover.

## Trace 1 — Arithmetic composition: `add` of `collect`

### Why this trace

U-008 is the most common value-tree op in primary content (166 occurrences;
Track 1c C06: top-level `value.op` is `add` × 44). The load-bearing behaviour
is not "add numbers": `_flatten` makes arity-1 `add` of a `collect` a **sum
of members**, not identity (reconciliation V10 / D8). No other trace is
about that fold.

### Declared content

Primary citizen (schema field, not filename):

`packages/content/tax/2025/rule.f1099b-covered-lt-basis-subtotal.json`

- `schema`: `rule-artifact.v2` (U-001)
- `id`: `tax.us.2025.rule.f1099b-covered-lt-basis-subtotal`
- `version`: `v1` (U-164: instance version is a second axis)
- `role`: `computation` (U-030)
- `when`: JSON `true` (U-032; 77 / 134 files)
- `publishes`: `tax.us.2025.f1099b.covered-lt-basis-subtotal` (U-034)
- `value`: `{ "op": "add", "args": [{ "op": "collect", "name": "tax.us.2025.f1099b.covered-lt-txn.basis", "source_set": "tax.us.2025.f1099b.covered-lt-basis" }] }`
- authored `blocked.code`: `SOURCE_SET_UNCLOSED` (U-035 — unread by the runner; coincidence of vocabulary with the evaluator code, not a mechanism; 1c Q9 / Track 2 resolved Q27)

Same construct in committed sample_data, with an extra `round` wrapper the
primary file does not have:

`packages/sample_data/derivation/examples/rule-artifact.wages-line1a.json`
(`schema`: `rule-artifact.v1`; `value` is `round` of `add` of `collect`
`demo.w2.box1` / `source_set` `demo.w2`).

### Validation

**Executed.** `DerivationSchemas.validate_declared` on both files:
`rule-artifact.v2` and `rule-artifact.v1` respectively. Both accepted.

**Inferred.** A package that admits this v2 rule does so because
`_SUPPORTED_SEMANTIC_SCHEMAS` includes `rule-artifact.v2` (U-076,
`package_validation.py:246-293`). `artifact-package.v25` `admitted_schemas`
also lists `rule-artifact.v2`. Falsified if a production package of this
rule reported `MEMBER_SCHEMA_UNSUPPORTED`.

### Evaluation

Evaluator (`packages/derivation/evaluator.py`):

- `collect` (`:118-131`, U-004): `env.sources.get(name, [])`. Nonempty → list
  of Decimals, **even if `source_set` is not in `closed_sets`**. Empty +
  missing-or-unclosed `source_set` → `EvalBlocked(SOURCE_SET_UNCLOSED, …)`.
  Empty + closed → `[]` and records `access.closure_reads`.
- `add` (`:159-160` plus `_flatten` `:274-282`, U-008): sums the flattened
  list; empty flatten → `Decimal(0)`.

**Executed.** Same `collect` / `add` tree as the primary file, consumer
`packages.derivation.evaluator.evaluate`:

```
nonempty unclosed collect  -> [Decimal('100'), Decimal('50')]
nonempty unclosed add      -> Decimal('150')
empty unclosed collect     -> SOURCE_SET_UNCLOSED missing ['tax.us.2025.f1099b.covered-lt-basis']
empty closed collect       -> []
empty closed add           -> Decimal('0')
arity-1 add of [100, 50]   -> Decimal('150')
```

The nonempty-unclosed success is the S4 surprise: "collect requires closure"
is false for a nonempty source. Closure is required to treat empty as zero.

**Executed.** Existing runner test, re-run:

```
pytest tests/derivation/test_runner.py -k chain_computes_to_fixpoint
```

`test_chain_computes_to_fixpoint` (`tests/derivation/test_runner.py:84-95`)
runs the demo wages rule over two `demo.w2.box1` facts `40000` and `2000`
plus `rounding.convention` `half_up`. Published
`demo.form1040.line1a` = `"42000"`. That is `add` of `collect` then `round`
(U-020). Passed.

### Consequence

**Executed.** Same module, `test_published_finding_pins_carry_roles`
(`test_runner.py:149-160`): the published finding's pins include
`field-mapping`, `input`, `operation-semantics`, `adoption`, `governance`.
Content `pins` on the primary file are `[]` (U-039 writes `input`/`parameter`
when authors fill them; U-139 `runner.pins_for` is the surviving set).

**Inferred.** `npe-walk.v3` of a published symbol has `node_kind: published`
(`tests/derivation/test_npe_walk.py:29-78`, re-run under
`-k walk_npe_published`; U-133 / U-134). Falsified if a successful
`add`/`collect` publication walked as `blocked`.

**Inferred.** The primary file's authored `blocked` field is not consulted
on the success path or the unclosed path: `packages/derivation/runner.py`
has no `rule["blocked"]` read (U-035). The evaluator raises
`SOURCE_SET_UNCLOSED` on empty-unclosed collect regardless of what the
citizen wrote. Falsified by a `rule.get("blocked")` in
`packages/derivation/`.

### Nearby inferences this evidence does not support

- That every `add` wraps a `collect`. 166 `add` nodes; the arity-1 wrap is
  the observed subtotal pattern, not the only shape.
- That nonempty `collect` requires closure. It does not (executed above).
- That `count` shares this empty/unclosed rule. It does not (Trace 3).
- That the authored `blocked.code` is what the ledger records.

## Trace 2 — Conditional applicability: false `when` is inapplicable

### Why this trace

U-043 is the only path from a successfully evaluated false guard to a
ledger row. It is not a block, not a missing `requires`, and not a
conflict-loser (those are `inapplicable` with **no** `guard_result`,
U-042 / `runner.py:471-484`). A trace set that only published findings
would describe a different engine. This is the required non-success
ending that is *applicability*, not invalidity.

### Declared content

No primary 2025 rule-artifact writes `"when": false` (Track 1c C05). The
asserting fixture is committed sample_data:

`packages/sample_data/derivation/examples/rule-artifact.tax-table-line16.json`

- `schema`: `rule-artifact.v1`
- `id`: `demo.rule.tax-table-line16`
- `when`: `{ "op": "compare", "cmp": "lt", "left": { "op": "ref", "name": "demo.form1040.line15" }, "right": { "op": "parameter", "parameter_id": "demo.parameter.regular-tax-split.2025" } }` (U-015, U-003, U-007)
- `requires`: `demo.form1040.line15`, `filing_status`, `rounding.convention` (U-031)
- `publishes`: `demo.form1040.line16`
- authored `blocked.code`: `OPEN_TAX_TABLE_ROW` (U-035 unread)

Companion parameter
`packages/sample_data/derivation/examples/parameter.regular-tax-split.json`
(`schema`: `parameter-declaration.v1`, U-145) has `"values": "100000"`.

Production analog (not this trace's executed fixture): a `when` tree of
`categorical_compare` or `require_closed` can also evaluate false or
raise. Those constructs are Traces 3–4.

### Validation

**Executed.** `validate_declared` accepted the tax-table rule as
`rule-artifact.v1` and the split parameter as `parameter-declaration.v1`.

**Inferred.** `rule-artifact.v1` is in `_SUPPORTED` and omitted from every
`artifact-package.v2..v25` `admitted_schemas` enum (U-066 / D15). This
demo file is executable in isolation via the test runner, which does not
go through production package admission. Falsified if this test constructed
its rules through `validate_package` of an `artifact-package.v25` instance
that listed `rule-artifact.v1`.

### Evaluation

Runner (`packages/derivation/runner.py:486-501`, U-043):

1. Missing `requires` → `DEPENDENCY_ABSENT` **before** the guard
   (`:464-468`, U-031).
2. `evaluate(rule["when"])` catching `EvalBlocked` → record blocked with
   the evaluator code (`:487-491`).
3. Truthy guard → evaluate `value`.
4. Falsy guard → disposition `inapplicable` with `guard_result: False`.

**Executed.** Evaluator on the declared `when` tree:

```
line15 14950 < 100000  -> True   (refs=['demo.form1040.line15'])
line15 200000 < 100000 -> False  (refs=['demo.form1040.line15'])
when true literal      -> True
when missing ref       -> DEPENDENCY_ABSENT missing ['demo.form1040.line15']
```

A false compare is an ordinary boolean. A missing `ref` inside `when` is
a block, not inapplicable. Those are different runner steps.

**Executed.** Existing runner test, re-run:

```
pytest tests/derivation/test_runner.py -k false_guard
```

`test_false_guard_is_inapplicable_not_blocked` (`test_runner.py:106-115`)
feeds `demo.form1040.line15` = `200000` (at or above the split). Disposition
of `demo.rule.tax-table-line16` is `inapplicable` with `guard_result` false.
Not present in `result.blocked`. Passed.

### Consequence

**Executed.** `tests/derivation/test_npe_walk.py:107-131`
(`test_walk_npe_inapplicable`, re-run under `-k walk_npe_inapplicable`):
a ledger row `disposition: inapplicable` + `guard_result: False` walks as
`node_kind: guard_inapplicable` (U-134). Schema of the walk is
`npe-walk.v3` (hardcoded at `explanation.py:332`, U-133). Passed.

**Inferred.** Conflict-loser `inapplicable` rows have no `guard_result`
(`runner.py:474-484`). Walking those is a different `node_kind` path
(`test_walk_npe_conflict_loser`). This trace is only the false-guard
case. Falsified if `_record_blocked` were called for a false `when`.

### Nearby inferences this evidence does not support

- That production content contains a numeric `compare` as top-level `when`.
  It does not (C05).
- That a failed `requires` check is inapplicable. It is
  `DEPENDENCY_ABSENT` (executed by
  `test_ineligible_rule_finalizes_blocked_on_missing_dependency`,
  `test_runner.py:97-104`).
- That authored `OPEN_TAX_TABLE_ROW` is the ledger code for a false guard.
  The false-guard path never reads that field.

## Trace 3 — Source-set closure: `SOURCE_SET_UNCLOSED` and the closed zero

### Why this trace

Three ops talk about source-set closure and do not share a rule (D8):

- U-004 `collect`: empty unclosed blocks; nonempty unclosed **succeeds**;
  empty closed is `[]` (Trace 1 executed this).
- U-005 `count`: **always** requires `source_set in closed_sets`, even
  when rows exist. No ADR names this op (Track 2 U-005).
- U-024 `require_closed`: always under `when` in primary content (71
  occurrences / 29 files). Unclosed raises `SOURCE_SET_UNCLOSED`; closed
  returns `True`. Because it sits in `when`, an unclosed set is a **block
  during guard evaluation**, not Trace 2's inapplicable.

The semantic contrast is "absence of closure is a first-class block, and
recorded completeness is what licenses zero." ADR-0011: zero is never
assumed.

### Declared content

`require_closed` in production `when`:

`packages/content/tax/2025/rule.f1099r-ira-fully-taxable-subtotal.json`

- `schema`: `rule-artifact.v3`
- `id`: `tax.us.2025.rule.f1099r-ira-fully-taxable-subtotal`
- `when`: `{ "op": "require_closed", "source_set": "tax.us.2025.f1099r.ira-fully-taxable" }`
- `value`: `round` of `add` of `collect`
  `tax.us.2025.f1099r.ira-box1-taxable-distribution` /
  `source_set` `tax.us.2025.f1099r.ira-fully-taxable`
- authored `blocked.code`: `OPEN_DEPENDENCY` (U-036; unread; would remap
  to `DEPENDENCY_INVALID` on a v2 ledger if it were ever the disposition
  code — V7)

`count` in production `when` / `value` (worksheet; reused here only for
the closure rule of `count`):

`packages/content/tax/2025/rule.sli-worksheet.json` (`schema`:
`rule-artifact.v6`) has `require_closed` on `tax.us.2025.f1098e.1` in
`when`, and `{ "op": "count", "name": "tax.us.2025.f1098e.box1-student-loan-interest", "source_set": "tax.us.2025.f1098e.1" }`
compared to 0 to take the closed-empty shortcut (U-005).

Demo wages (Trace 1) is the executed empty-unclosed `collect` in a runner.

### Validation

**Executed.** `validate_declared` accepted the IRA rule as
`rule-artifact.v3` and the SLI worksheet as `rule-artifact.v6`.

**Inferred.** `require_closed` is declared from rule-artifact.v1 through
v6 (`$defs/expr`) and has a separately versioned operation-semantics.v2
spec with `spec.admission` const `current-literal-true` (U-058). The
evaluator does not read that spec; it tests `env.closed_sets`
(`evaluator.py:206-211`). Falsified if `_require_closed` indexed
`env.canon["require_closed"]`.

### Evaluation

**Executed.** Evaluator:

```
require_closed unclosed           -> SOURCE_SET_UNCLOSED missing ['tax.us.2025.f1099r.ira-fully-taxable']
require_closed closed             -> True  (closure_reads=['tax.us.2025.f1099r.ira-fully-taxable'])
count nonempty unclosed           -> SOURCE_SET_UNCLOSED missing ['tax.us.2025.f1098e.1']
count nonempty closed             -> 1
count empty closed                -> 0
```

Compared with Trace 1: nonempty unclosed **collect** succeeded. Nonempty
unclosed **count** blocked. Same string `source_set`, different ops.

**Executed.** Existing runner tests, re-run:

```
pytest tests/derivation/test_runner.py -k "unclosed_empty_source or closure_authority_empty"
pytest tests/test_sli_worksheet_line21_track3.py -k "unclosed_family_blocks_on_closure or closed_empty_family_computes_zero"
```

- `test_unclosed_empty_source_blocks_with_closure_code`
  (`test_runner.py:119-122`): demo wages, `sources=[]`, no closed set →
  blocked with `BLOCK_CLOSURE` (`SOURCE_SET_UNCLOSED`). Passed.
- `test_closure_authority_empty_source_publishes_zero`
  (`test_runner.py:124-131`): same collect, empty sources, but
  `demo_closure_authority()` admits the set → published
  `demo.form1040.line1a` = `"0"`. Passed.
- `test_unclosed_family_blocks_on_closure`
  (`tests/test_sli_worksheet_line21_track3.py:224-234`): production SLI
  worksheet, nonempty box-1 source, closure not admitted → blocked
  `SOURCE_SET_UNCLOSED`, no published Schedule 1 line 21. Passed.
- `test_closed_empty_family_computes_zero` (`:218-222`): closed empty →
  published `"0"`, not blocked. Passed.

Runner mapping: `evaluate(when)` raising `EvalBlocked` becomes
`_record_blocked` (`runner.py:487-491`). `SOURCE_SET_UNCLOSED` is in
`record_codes` (`:1169-1182`, U-045), so the v2 ledger keeps it. It is
also in `npe-walk.v3`'s code enum (U-135).

### Consequence

**Executed.** `test_walk_npe_blocked` (`test_npe_walk.py:79-105`, re-run
under `-k walk_npe_blocked`): a blocked disposition walks as
`node_kind: blocked` with `code` and `unmet_references`. Passed. The
fixture uses `DEPENDENCY_ABSENT`; **Inferred** the same walker emits
`SOURCE_SET_UNCLOSED` when that is the disposition code, because it
copies the row's `code` after remap (`explanation.py`). Falsified if the
walker rewrote closure codes to `DEPENDENCY_ABSENT`.

**Inferred.** Authored `OPEN_DEPENDENCY` on the IRA file is not the
unclosed-set code. Evaluator constant `BLOCK_CLOSURE` is
`SOURCE_SET_UNCLOSED` (`evaluator.py:26`). One leftover form-field still
lists `SOURCE_SET_OPEN` (`form1040.line-2b.form-field.json`, host
`form-field.v2`, D7 / U-103). Falsified if `evaluate` still emitted
`SOURCE_SET_OPEN`.

### Nearby inferences this evidence does not support

- That closed-empty and unclosed-empty are the same user outcome. They
  are published zero vs blocked.
- That `collect_categorical_all_equal` empty is a closure block. Empty
  categorical-collect is `DEPENDENCY_ABSENT` (Trace 5 executed).
- That `require_closed` in `when` yields Trace 2 inapplicable. It yields
  a block, because the op raises rather than returning false.

## Trace 4 — Categorical reasoning: `categorical_compare` and `category_literal`

### Why this trace

U-022 / U-023 are the most frequent expression ops after `ref` (368 and
373 occurrences). Every observed `categorical_compare` uses `cmp: eq`;
`ne` is declared and implemented, not observed (U-022). This is not
numeric `compare` (U-015, field `cmp`, tokens `gte`/`lte`). Domain
mismatch is `CATEGORICAL_DOMAIN_MISMATCH`; an out-of-domain value is
`DEPENDENCY_INVALID`. No other trace is about that domain-checked
equality.

### Declared content

`packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`

- `schema`: `rule-artifact.v3`
- `id`: `tax.us.2025.rule.capital-loss-carryover.long-term`
- `publishes`: `tax.us.2025.capital-loss-carryover.long-term`
- Path A short-circuit in `value` (Track 1c C29 representative citation,
  around line 233): `choose` whose `when` is
  `{ "op": "categorical_compare", "cmp": "eq", "left": { "op": "ref", "name": "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers" }, "right": { "op": "category_literal", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers", "version": "v1" }, "value": "yes" } }`
  and whose `then` is literal `0`.

The same pair appears in 39 files. SLI's MFS check (Trace 5) is the
same op against `filing_status` / `married_filing_separately`.

### Validation

**Executed.** `validate_declared` accepted the file as `rule-artifact.v3`.

**Inferred.** `category_literal.fact_type` is a `{id, version}` pair in
content. The evaluator's operand helper uses the `id` as the domain key
(`evaluator.py:367-372`). JSON Schema does not constrain `ref.name` to a
fact-type id (Track 0 gap 5 / U-153). Falsified if
`_eval_categorical_operand` required `ref.name == fact_type.id`.

### Evaluation

`categorical_compare` (`evaluator.py:213-218`, U-022): evaluate both
operands as `(domain, value)`; unequal domains →
`CATEGORICAL_DOMAIN_MISMATCH`; `eq` is Python `==` on the values.
Top-level `category_literal` does **not** domain-check
(`evaluator.py:220-221`, U-023); the operand helper does
(`:367-372, 382-385`).

**Executed.** Shape of the Path A `when`, consumer `evaluate`:

```
eq yes vs yes        -> True   (refs the boundary symbol)
eq no vs yes         -> False
out of domain maybe  -> DEPENDENCY_INVALID missing ['maybe']
domain mismatch      -> CATEGORICAL_DOMAIN_MISMATCH
                       missing ['other.domain != tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers']
```

Environment for the first two rows: `symbol_fact_types` maps the ref
name to that same fact-type id; `categorical_domains` is `{yes, no}`.
Out-of-domain used `"maybe"` against that set. Domain mismatch bound
the ref to `other.domain`.

**Inferred.** `choose` then evaluates only the taken branch
(`evaluator.py:188-190`, U-017). Path A `yes` therefore never reads the
prior-return refs under the `else`. Falsified if `choose` evaluated both
branches and unioned their `AccessLog`. (Trace 5 executes `choose`
directly.)

### Consequence

**Inferred.** Path A `yes` publishes `0` as an ordinary finding, not
`inapplicable`. The rule's `when` is a `choose` wrapping
`conditional_dependency_set` (U-025), not this categorical node — the
categorical node is inside `value`. A `no` on the boundary fact takes
the `else` (worksheet arithmetic) rather than skipping the citizen.
Falsified if a `yes` on that fact produced disposition `inapplicable`
for this rule.

Existing live test `tests/test_schedule_d_inbound_loss_carryovers_t1.py`
drives Path A (`BOUNDARY_PATH_A` sets the declaration to `"yes"`) through
`live_coordinate_run`. **Not re-run here** (live lane). Named as the
committed end-to-end of this content; the evaluator rows above are the
executed evidence for the op.

**Executed.** Out-of-domain elective on a *parameter* key (different op,
same invalidity family): `test_out_of_domain_elective_blocks_invalid_without_leaking_exceptions`
(`test_runner.py:133-145`, re-run under `-k lookup`) asserts
`BLOCK_LOOKUP_MISS` (`LOOKUP_MISS`) and no traceback in `missing`.
Passed. On a v2 ledger that code remaps to `DEPENDENCY_INVALID` (V7 /
U-046), which is walk-legal; `LOOKUP_MISS` itself is not in
`npe-walk.v3` or `derivation-record.v7`. Categorical out-of-domain
already emits `DEPENDENCY_INVALID` (`BLOCK_INVALID`), so it does not
need that remap.

### Nearby inferences this evidence does not support

- That `cmp: ne` is unused because it is unimplemented. It is
  implemented (`evaluator.py:218`).
- That top-level `category_literal` domain-checks. It returns
  `expr["value"]` unchecked.
- That this is the same construct as predicate `compare` (U-121, field
  `comparison`, tokens `ge`/`le`). Collapsing them manufactures
  agreement (reconciliation naming table).

## Trace 5 — Worksheet-like computation: SLI Schedule 1 line 21

### Why this trace

One citizen composes staged arithmetic, branching, a conditional
dependency set, a categorical universal over a family, and explicit
`block` ops with tax-shaped codes. That *composition* is the construct:
a worksheet as declared content, not a Python procedure. Unique in this
set: U-013 `multiply` (1 primary file), U-014 `divide` (2 occurrences,
both `rounding: half_up`), U-006 `block` (content codes `SLI_*`),
U-025 `conditional_dependency_set`, U-026 `collect_categorical_all_equal`
(5 occurrences, all this file). `choose` (U-017) is the spine.

### Declared content

`packages/content/tax/2025/rule.sli-worksheet.json`

- `schema`: `rule-artifact.v6` (multiply / divide / collect_categorical
  live here; U-013, U-014, U-026)
- `id`: `tax.us.2025.rule.sli-worksheet`
- `publishes`: `tax.us.2025.schedule1.line21-sli-deduction`
- `when`: `all` of `require_closed` on `tax.us.2025.f1098e.1` and a
  `conditional_dependency_set` whose condition is `count > 0` and whose
  members are refs to eligibility facts (U-010, U-024, U-025, U-005)
- `value` (outer `choose`):
  - `when` `count == 0` → literal `0` (closed-empty shortcut; Trace 3)
  - `else` → `choose` MFS `categorical_compare` → `block`
    `SLI_MFS_INELIGIBLE`
  - further `choose`s: universal-component `not`/`all` of
    `categorical_compare` plus five `collect_categorical_all_equal`
    nodes → `block` `SLI_UNIVERSAL_COMPONENT_VIOLATION`; Part II
    activity → `block` `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`; else the
    nine-line arithmetic (`divide` with `min_decimal_places: 3` and
    `rounding: half_up`, `multiply`, `max`, `subtract`, outer `round`
    of a `ref` to `rounding.convention`)

### Validation

**Executed.** `validate_declared` accepted the file as `rule-artifact.v6`.

**Inferred.** `multiply` / `divide` / `collect_categorical_all_equal` /
`conditional_dependency_set` are **not** in `loader.OPERATION_VOCABULARY`
(14 names, U-063, never referenced from another `*.py` file) and **are**
in the 23-op dispatcher (U-027, V1). Schema v6 `$defs/expr` oneOf
includes them. Falsified if `evaluate` rejected `"op": "multiply"` as
`unknown op survived schema`.

### Evaluation

**Executed.** Isolated ops, shapes taken from this file:

```
multiply 2000 * 0.333                          -> Decimal('666.000')
divide 5000/15000 half_up 3dp                  -> Decimal('0.333')
divide 1/0                                     -> DEPENDENCY_INVALID ['division by zero']
choose then (when true)                        -> 0
choose else (when false)                       -> 99
block SLI_MFS_INELIGIBLE                       -> category SLI_MFS_INELIGIBLE missing []
CDS condition False, member ref missing        -> True  (refs set empty)
CDS condition True, member ref missing         -> DEPENDENCY_ABSENT ['missing.symbol']
collect_categorical_all_equal all yes          -> True
collect_categorical_all_equal one no           -> False
collect_categorical_all_equal empty            -> DEPENDENCY_ABSENT [the name]
```

`choose` evaluates only the taken branch: the false-`when` row did not
need the `then` value to exist as a successful eval. CDS false does not
read members (U-025; ADR-0037). Empty categorical-collect is
`DEPENDENCY_ABSENT`, not `SOURCE_SET_UNCLOSED` (D8).

**Executed.** Existing tests, re-run:

```
pytest tests/derivation/test_multiply_divide.py \
       tests/derivation/test_collect_categorical_all_equal.py \
       tests/derivation/test_conditional_multi_dependency.py \
       tests/test_sli_worksheet_line21_track3.py \
       -k "multiplies_two or divides_two or zero_divisor or min_decimal_places_worksheet or rounding_mode_half_even or single_member_all_yes or one_member_no or absent_source or inactive_members or active_members_publish or active_multi_and_partial or single_statement_in_phaseout_band or mfs_filing_status or closed_empty_family_computes_zero"
```

Passed. Load-bearing assertions:

- `test_single_statement_in_phaseout_band_reduces_the_deduction`
  (`tests/test_sli_worksheet_line21_track3.py:251-265`): box-1 `2000`,
  MAGI `90000`, single, closed family, eligibility yes → published
  Schedule 1 line 21 `"1334"`. Comment in the test: line7 = `5000/15000`
  = `0.333` half_up 3dp; line8 = `2000*0.333` = `666.000`; line9 =
  `2000 - 666.000` = `1334`. Matches the isolated multiply/divide rows.
- `test_mfs_filing_status_blocks_the_whole_route` (`:318-329`):
  `filing_status` `married_filing_separately` → blocked
  `SLI_MFS_INELIGIBLE`, no published line 21. That is U-006 `block`
  after U-022, **not** Trace 2 inapplicable: the citizen's `when` passed
  (`require_closed` + CDS members present); `value` raised.
- `test_collect_categorical_all_equal.py`: all-yes True; one `no` False
  order-independently; absent source `DEPENDENCY_ABSENT`.
- `test_conditional_multi_dependency.py:96-133`: inactive CDS members
  are not missing; active pins every ref; partial active set is ordered
  `DEPENDENCY_ABSENT`.

### Consequence

**Executed.** `SLI_MFS_INELIGIBLE` is in `record_codes`
(`runner.py:1179`), so the v2 ledger **keeps** it (V7). It is **not** in
`npe-walk.v3`'s code enum (U-135). **Inferred.** A walk of this block
would emit a `code` the walk schema does not list; the walker does not
`validate_declared` its result in the code that was read (Track 2
resolved Q5). Falsified if `walk_npe` called `validate_declared` on the
walk document for this code.

**Inferred.** Universal-component violation uses the same `block` op with
`SLI_UNIVERSAL_COMPONENT_VIOLATION` (`test_universal_component_violation_blocks_the_whole_route`,
not re-run in the `-k` set above; named, not executed this turn). Empty
categorical-collect on a nonempty-family route would `DEPENDENCY_ABSENT`
the witness name (executed isolated) rather than treating "no rows" as
"all equal".

### Nearby inferences this evidence does not support

- That `divide.rounding` reads operation-semantics canon. Divide indexes
  `_ROUND_MODES` only (U-060 / D9). Round also intersects `canon["modes"]`.
- That `half_even` appears in 2025 content. Bundle enum is `{half_up}`;
  content `divide.rounding` is `half_up`; `half_even` is a test-only
  rounding token on divide.
- That CDS is `all` with extra reporting. `all` short-circuits
  (`evaluator.py:179-180`); CDS on a true condition evaluates every
  member and unions `DEPENDENCY_ABSENT` names.


