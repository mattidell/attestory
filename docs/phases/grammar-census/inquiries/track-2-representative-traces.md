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
