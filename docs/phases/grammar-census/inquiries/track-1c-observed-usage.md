# Track 1c — Observed usage (content and tests)

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 1c — observed usage
- Role: Builder
- Status of every construct record below: `pending-reconciliation`
- Source ref read: `HEAD` on `milestone/grammar-census-engine-language-map`
- Bound corpus: Track 0
  `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`
  (complete at `4f66bc83`; this reading did not re-derive the corpus)

This file is the **observed-usage** construct set. It records what committed
content actually contains and what the test suite actually demonstrates. It
does not claim that a construct is unused, unreachable, undeclared, or
unimplemented, and it does not compare this layer against any schema or any
runtime module. Set-difference claims belong to Track 2.

Where this layer is silent, the record says so. Inferences are labelled as
inferences and name what would falsify them.

## Method

1. Load every `packages/content/tax/2025/*.json` file, parse JSON, and
   classify by the top-level `schema` field. Filename prefixes were not used
   as family identity (Track 0 gap 6; re-confirmed below).
2. Walk every `when` / `value` tree in the 134 `rule-artifact.*` files and
   count `{ "op": ... }` nodes. Repeat for `attachment-rule`,
   `source-family`, `artifact-package`, `form-field`, and the other
   Layer 4 families Track 0 listed.
3. Treat `packages/sample_data/**` as a **secondary, synthetic** corpus and
   name it as such in every citation.
4. Search `tests/` (127 `.py` files) and `tools/generate_*.py` (31 files)
   for the same construct names. Classify a test as **asserting a behavior**
   when it checks a result, disposition, block code, or pin set; classify it
   as **exercising a path** when it only validates that a shape is
   schema-accepted or that a call does not raise.
5. Run existing tests and a small `evaluate()` / `EvalBlocked` synthetic
   execution on shapes copied from committed content. Those runs are shown
   under `#Synthetic executions`.

Layer numbering follows the Track 0 boundary map (`#Term boundary` surfaces
1–8, including the eighth store-side surface Track 0 added).

## Record shape

Every construct record below carries these fields, matching the plan's
`#Census unit` plus the frequency context this track is required to add:

| Field | What this layer fills with |
| --- | --- |
| `name` | Construct or construct-family name as it appears in content/tests |
| `layer` | Track 0 surface number |
| `observed_syntax` | Shape actually present (keys, literals, host `schema` versions) |
| `frequency` | File count and occurrence count in the primary corpus, or test-module count |
| `representative_citations` | Path:line, not paraphrase |
| `source_of_authority_this_layer` | The committed artifact that *uses* it (its `schema` field). This layer does not name an ADR or a schema `$defs` as authority. |
| `runtime_consumer` | Silent, unless a test this track ran or read actually calls a named consumer |
| `semantic_effect` | Silent, unless a test or synthetic execution demonstrated it |
| `input_output_observed` | Operand keys and literal domains seen in content |
| `evaluation_blocking_nonpublication` | Silent, except (a) the `blocked` object written into rule-artifacts, (b) form-field `dispositions`, (c) demonstrated test/synthetic results |
| `separately_versioned` | Host schema versions in which the construct was observed |
| `status` | Always `pending-reconciliation` |
| `provenance` | Pins, npe-walk / derivation-record fixtures, and test-demonstrated pin roles |
| `this_layer_does_not_support` | Nearby inferences this evidence does not license |

**84 construct records** follow. Searches that returned no hit are listed
after the records; they are observations about the search, not absence
claims about the language.

---

## Corpus re-verification (Track 0 Layer 4 and Layer 5)

Re-ran Track 0's method: parse each of 538 `packages/content/tax/2025/*.json`
files and read `schema`. Counts match Track 0:

| Parsed `schema` family | Files | Track 0 said |
| --- | ---: | ---: |
| `rule-artifact.*` | 134 | 134 |
| `attachment-rule.*` | 15 | 15 |
| `source-family.*` | 48 | 48 |
| `form-field.*` | 50 | 50 |
| `artifact-package.*` | 35 | 35 |
| `citation.v1` | 74 | 74 |
| `bundle.v2` | 53 | 53 |
| `source-closure-mapping.v2` | 49 | 49 |
| `parameter-declaration.v1` | 18 | 18 |
| `quantity-vocabulary.*` | 23 | 23 |
| `dividend-universe.*` | 4 | 4 |
| `taxable-interest-composition.v1` | 4 | 4 |
| `role-canon.v1` | 1 | 1 |
| `checked-conclusion-binding.v1` | 1 | 1 |
| `migration-artifact.v1` | 1 | 1 |
| no top-level `schema` | 28 | 28 (all `published-packages*.json`) |
| **total** | **538** | **538** |

Rule-artifact host schema versions in content (not a current-selection claim):

| `schema` | files |
| --- | ---: |
| `rule-artifact.v3` | 69 |
| `rule-artifact.v2` | 35 |
| `rule-artifact.v4` | 19 |
| `rule-artifact.v5` | 8 |
| `rule-artifact.v6` | 2 |
| `rule-artifact.v1` | 1 |

Attachment-rule host schema versions in content (no v5, no v7):
`v4`×7, `v6`×2, `v8`×2, `v2`×2, `v3`×1, `v1`×1.

The glob `packages/content/tax/2025/rule.*.json` still spans two families:
134 `rule-artifact` + 6 `attachment-rule` named `rule.attachment.*`. The
other 9 attachment-rule files are named `attachment.*`. Only the parsed
`schema` field identifies the family. Track 0 gap 6 holds.

`package.core-calculations.json` declares `"version": "v1"` and
`"schema": "artifact-package.v2"` (`packages/content/tax/2025/package.core-calculations.json:4`
and the `schema` field in the same object). It is the oldest core-calculations
instance under a bare filename, not a current alias. Highest-numbered
package file: `package.core-calculations.v33.json` (`"version": "v33"`,
`"schema": "artifact-package.v25"` at `:2862`). Cited as highest-numbered,
not claimed current.

Layer 5 re-check: `tests/` has 5 top-level subdirectories
(`conformance`, `derivation`, `helpers`, `source_completeness`, `tax`),
76 top-level `test_*.py`, 127 `.py` files recursively, 1508 `def test_`
functions (any indent). `tests/helpers/` exists and contains 0 `.py`
files. `tools/generate_*.py`: 31 files. Matches Track 0.

`packages/sample_data/`: 32 top-level scenario directories, 320 `.json`
files. Secondary corpus.

Live-lane note (not a construct): `tests/conftest.py` derives the `live`
marker from source tokens `live_coordinate_run` / `live_workspace` /
`LiveWorkspace` / `subprocess`. 50 `test_*.py` modules contain at least
one of those tokens; 70 do not. Only `tests/conftest.py` writes
`pytest.mark.live` in source.

---

## Surface 1 — Core clause / expression language

### C01 — `rule-artifact` citizen envelope

- **layer:** 1 (also carries surface-2 fields)
- **observed_syntax:** every one of the 134 files has top-level keys
  `schema`, `id`, `version`, `scope`, `role`, `requires`, `when`, `value`,
  `publishes`, `blocked`. `pins` in 133/134; `notes` in 132/134;
  `citations` in 90/134; `composition` in 15/134; `accounts_for` in 8/134.
- **frequency:** 134 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.wages-line1a.json:2` (`"schema": "rule-artifact.v1"`;
  the only file without `pins`);
  `packages/content/tax/2025/rule.sli-worksheet.json:204` (`"schema": "rule-artifact.v6"`).
- **source_of_authority_this_layer:** the files' own `schema` field.
- **runtime_consumer:** silent in content. Tests call `packages.derivation.runner.run`
  and `packages.derivation.evaluator.evaluate` on this shape.
- **semantic_effect:** silent as a whole-citizen claim.
- **input_output_observed:** `publishes` is a string in all 134 (a symbol id).
  `requires` is a list of strings in all 134 (length 0..33; 20 files have `[]`).
- **evaluation_blocking_nonpublication:** see C33–C35 (`blocked` object).
- **separately_versioned:** host schemas v1–v6 all appear in content.
  Content `version` field is a second axis (90 files `"v1"`, then v2–v7);
  Track 0's two-axis warning applies.
- **status:** pending-reconciliation
- **provenance:** `pins` (C36). One file, `rule.wages-line1a.json` (v1),
  has no `pins` key at all.
- **this_layer_does_not_support:** that highest host schema is current;
  that `requires` is evaluated as a guard (content writes the list; this
  layer does not show what the runner does with it).

### C02 — `role: computation`

- **layer:** 2
- **observed_syntax:** `"role": "computation"`
- **frequency:** 132 / 134 rule-artifact files.
- **representative_citations:** any of the 132; e.g. the envelope of
  `rule.sli-worksheet.json` (role sits with the other top-level keys).
- **source_of_authority_this_layer:** the rule-artifact files.
- **runtime_consumer / semantic_effect:** silent.
- **separately_versioned:** observed under rule-artifact v2–v6.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that `computation` is the only legal
  non-mapping role — see C03 and C74.

### C03 — `role: field-mapping`

- **layer:** 2
- **observed_syntax:** `"role": "field-mapping"`
- **frequency:** 2 files, both the same `id`
  `tax.us.2025.rule.w2-box1-to-line1a`.
- **representative_citations:**
  `packages/content/tax/2025/rule.wages-line1a.json:6`;
  `packages/content/tax/2025/rule.wages-line1a.v2.json` (same role, host
  schema `rule-artifact.v2`).
- **source_of_authority_this_layer:** those two files.
- **runtime_consumer:** a runner test asserts published findings pin the
  firing rule under role `field-mapping`
  (`tests/derivation/test_runner.py:153-154`, asserting behavior).
- **semantic_effect:** silent in content.
- **separately_versioned:** host v1 and v2.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that `applicability` or
  `cross-form-bridge` also appear as rule-artifact roles. Search for those
  two strings as `role` values in the 134 files found neither; they do
  appear in `role-canon.v1` (C74).

### C04 — `when` literal `true`

- **layer:** 2 (guard)
- **observed_syntax:** `"when": true` (JSON boolean).
- **frequency:** 77 / 134 files. Host-schema spread: v3×33, v2×32, v5×6,
  v4×4, v6×1, v1×1.
- **representative_citations:** `rule.wages-line1a.json` (v1 field-mapping;
  `when` is true in that file's envelope).
- **source_of_authority_this_layer:** the rule-artifact files.
- **runtime_consumer / semantic_effect:** silent in content. Tests
  demonstrate a *false* guard becoming `inapplicable` (C78); they do not
  by themselves explain literal-`true` guards.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that literal `true` is equivalent to
  omitting `when` — every file has a `when` key.

### C05 — `when` as an expression tree

- **layer:** 2
- **observed_syntax:** top-level `when.op` in the remaining 57 files:
  `all`×35, `categorical_compare`×11, `require_closed`×8, `choose`×2,
  `conditional_dependency_set`×1. No file has `"when": false`.
- **frequency:** 57 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099r-ira-fully-taxable-subtotal.json:56`
  (`"when": {"op": "require_closed", ...}`);
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json:25`
  (top-level `choose`).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** a closed list of legal guard ops —
  this is the observed top-level set, not a claim about the language.

### C06 — `value` as an expression tree

- **layer:** 1
- **observed_syntax:** `value` is `{ "op": ... }` in 120 / 134 files.
  Top-level value ops: `add`×44, `round`×28, `choose`×19, `ref`×17,
  `subtract`×8, `max`×4.
- **frequency:** 120 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099b-covered-lt-basis-subtotal.json:29`
  (`"op": "add"` wrapping a `collect`).
- **status:** pending-reconciliation

### C07 — `value` as a JSON literal

- **layer:** 1
- **observed_syntax:** `value` is not an `{op}` node: `bool true`×7,
  `str`×4 (`"not_elected"`, `"not_checked"`, `"checked"`×2), `int` 0×3.
- **frequency:** 14 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.form1040-line6d-not-checked.json` (`"not_checked"`);
  `packages/content/tax/2025/rule.schedule-a-total-closed-empty.json` (`0`);
  `packages/content/tax/2025/rule.schedule-a-boundary-no-medical.json` (`true`).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that a literal `value` is a different
  op. It is an observed alternative to an expression tree.

### C08 — op `ref`

- **layer:** 1
- **observed_syntax:** `{ "op": "ref", "name": <string> }` only. 1333
  occurrences, one keyset.
- **frequency:** 1333 occurrences in 115 / 134 files. 216 distinct `name`
  strings. 405 of the 1333 sit under `when`, 928 under `value`.
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`
  (first `ref` nodes name
  `tax.us.2025.prior-return.form1040.line-15` etc.).
- **source_of_authority_this_layer:** rule-artifact content.
- **runtime_consumer:** `evaluate()` in unit tests; `run()` in runner tests.
- **input_output_observed:** `name` is a symbol string. This layer does
  not show whether the name is a fact, a finding, or a parameter.
- **status:** pending-reconciliation
- **provenance:** tests of `run()` pin evaluated refs as `role: input`
  (`tests/derivation/test_conditional_multi_dependency.py:103-112`,
  asserting behavior).
- **this_layer_does_not_support:** typing of `name` targets (Track 0
  surface 8). The names are data this layer can list; their store kind
  is another layer's question.

### C09 — op `collect`

- **layer:** 1
- **observed_syntax:** `{ "op": "collect", "name": <string>, "source_set": <string> }`
  only. Never appears under `when` (0 when / 44 value).
- **frequency:** 44 occurrences in 43 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099div-1a-subtotal.json:23`;
  `packages/content/tax/2025/rule.f1099b-covered-lt-basis-subtotal.json`
  (`name` + `source_set` on the `collect` inside an `add`).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that `collect` and attachment-rule
  `collect_members` (C46) are the same op. They have different names
  and different keysets in content.

### C10 — op `count`

- **layer:** 1
- **observed_syntax:** same keyset as `collect`: `{ "op": "count", "name", "source_set" }`.
- **frequency:** 15 occurrences in 7 files (9 when / 6 value).
- **representative_citations:**
  `packages/content/tax/2025/rule.form1040-line12e.json:31`;
  also `rule.schedule-a-line8a.json`, `rule.schedule-a-total.json`,
  `rule.sli-worksheet.json`, `rule.ss-benefits-worksheet.v2.json`,
  `rule.ss-benefits-worksheet.v3.json`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** the numeric meaning of `count`. Content
  writes the node; no unit test file in `tests/` contains `"op": "count"`.

### C11 — op `add`

- **layer:** 1
- **observed_syntax:** `{ "op": "add", "args": [ ... ] }`. Observed arities:
  1×44, 2×43, 3×36, 4×4, 5×3, 6×1, 7×35.
- **frequency:** 166 occurrences in 79 files (2 when / 164 value).
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099b-covered-lt-basis-subtotal.json:29`
  (arity-1: `args` is a single `collect`);
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`
  (nested arity-2).
- **semantic_effect:** synthetic execution of `{op:add, args:[3]}`
  returned `3` (see `#Synthetic executions`). Tests of schema validity
  accept `{op:add, args:[1]}`
  (`tests/derivation/test_language_schemas.py:151`, path-exercise of
  schema, not arithmetic).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that arity-1 `add` is an identity
  wrapper around `collect` — that is an inference from shape. Falsified
  if another layer shows arity-1 `add` has different rounding or
  blocking than a bare `collect`.

### C12 — op `subtract`

- **layer:** 1
- **observed_syntax:** `{ "op": "subtract", "left": ..., "right": ... }`
  only. Never under `when`.
- **frequency:** 119 occurrences in 29 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`
  (`left: 0` minus a `ref`, used as a unary negation shape).
- **status:** pending-reconciliation

### C13 — op `multiply`

- **layer:** 1
- **observed_syntax:** `{ "op": "multiply", "left": ..., "right": ... }`.
- **frequency:** 1 occurrence in 1 primary-corpus file.
- **representative_citations:**
  `packages/content/tax/2025/rule.sli-worksheet.json:272`.
  Secondary: `packages/sample_data/derivation/examples/rule-artifact.v6.sli-ratio.json:11`.
- **runtime_consumer:** `packages.derivation.evaluator.evaluate`.
- **semantic_effect:** asserting tests
  `tests/derivation/test_multiply_divide.py:36-47` (`1500.00 * 0.674`,
  refs, zero operand). Synthetic 1: `multiply` of `"1500"` and `"0.133"`
  returned `Decimal('199.500')`. Ran
  `pytest tests/derivation/test_multiply_divide.py` — passed.
- **separately_versioned:** observed in host `rule-artifact.v6`.
- **status:** pending-reconciliation

### C14 — op `divide`

- **layer:** 1
- **observed_syntax:** `{ "op": "divide", "left", "right", "min_decimal_places": 3, "rounding": "half_up" }`.
  Both occurrences use this four-key set.
- **frequency:** 2 occurrences in 1 file (`rule.sli-worksheet.json`).
- **representative_citations:**
  `packages/content/tax/2025/rule.sli-worksheet.json:301` (op) and `:310`
  (`"rounding": "half_up"`).
- **runtime_consumer:** `evaluate()`.
- **semantic_effect:** asserting tests
  `tests/derivation/test_multiply_divide.py:50-118`:
  `10/4` with `min_decimal_places=2, rounding=half_up` → `2.50`;
  MAGI-excess `2000/15000` to 3 places → `0.133`;
  zero divisor raises `EvalBlocked` with category `DEPENDENCY_INVALID`;
  `half_even` on `0.125/1` to 2 places → `0.12`;
  unknown rounding `"banker"` blocks `DEPENDENCY_INVALID`.
  Synthetic 2: same 2000/15000 shape → `0.133`.
  Synthetic 3: zero divisor → `EvalBlocked category=DEPENDENCY_INVALID`
  `missing=['division by zero']`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that production content uses
  `rounding: half_even` on `divide`. That value is demonstrated by a
  unit test, not by the 134 files. Search for `half_even` in
  `packages/content/tax/2025` returned 0 files.

### C15 — op `max`

- **layer:** 1
- **observed_syntax:** `{ "op": "max", "args": [a, b] }`. All 88
  occurrences have arity 2.
- **frequency:** 88 occurrences in 14 files, all under `value`.
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`
  (`max` of a `ref` and `0`).
- **status:** pending-reconciliation

### C16 — op `compare`

- **layer:** 1
- **observed_syntax:** `{ "op": "compare", "cmp": <rel>, "left", "right" }`.
  Observed `cmp` values: `gt`×77, `lte`×28, `eq`×26, `ne`×14, `lt`×13,
  `gte`×4.
- **frequency:** 162 occurrences in 24 files (79 when / 83 value).
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json:99`.
- **semantic_effect:** synthetic 6: `choose` over `compare cmp=gt`
  selected `then` when 2>1 and `else` when 1>2.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that this `cmp` vocabulary is the same
  as source-family predicate `comparison` (C57), which uses `gt`/`ge`
  under a different field name.

### C17 — op `all`

- **layer:** 1
- **observed_syntax:** `{ "op": "all", "args": [ ... ] }`. Observed
  arities 1..24.
- **frequency:** 68 occurrences in 40 files (54 when / 14 value).
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`
  (nested `all` under `value.else.when`).
- **status:** pending-reconciliation

### C18 — op `any`

- **layer:** 1
- **observed_syntax:** `{ "op": "any", "args": [ ... ] }`. Arities 2, 3, 4, 6.
- **frequency:** 32 occurrences in 16 files (21 when / 11 value).
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`
  (`any` of an `all` and a `compare`).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that source-family predicates also use
  `any`. Search for `"op": "any"` in the 48 source-family files returned
  0 hits (see `#Searches that returned no hit`).

### C19 — op `not`

- **layer:** 1
- **observed_syntax:** `{ "op": "not", "value": <node> }`.
- **frequency:** 3 occurrences in 2 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.selected-preferential-base.v4.json:187`;
  `packages/content/tax/2025/rule.sli-worksheet.json` (negating an `all`
  of `categorical_compare`s).
- **status:** pending-reconciliation

### C20 — op `choose`

- **layer:** 1
- **observed_syntax:** `{ "op": "choose", "when", "then", "else" }` only
  (211 occurrences, one keyset). Nested `choose` is common (`then` or
  `else` is another `choose` in 69+23 cases). `then`/`else` may be a
  nested op, a JSON number, a boolean, or a string.
- **frequency:** 211 occurrences in 25 files (22 when / 189 value).
  Top-level `when` is `choose` in exactly 2 files:
  `rule.capital-loss-carryover.long-term.json`,
  `rule.capital-loss-carryover.short-term.json`.
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json:25`.
- **semantic_effect:** synthetic 6 (see C16). Schema path-exercise:
  `tests/derivation/test_language_schemas.py:157`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** a `branches` / `cases` array form —
  that keyset was not observed.

### C21 — op `round`

- **layer:** 1 and 6iii
- **observed_syntax:** `{ "op": "round", "value": <node>, "mode": <node> }`
  in 58 occurrences; one extra file also carries `"stage": "after_aggregate"`
  (C22).
- **frequency:** 59 occurrences in 35 files, all under `value`.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099div-1a-subtotal.json:18`.
- **status:** pending-reconciliation

### C22 — `round.stage: after_aggregate`

- **layer:** 1 / 6iii
- **observed_syntax:** extra key on the v1 wages rule's `round` node.
- **frequency:** 1 occurrence in 1 file.
- **representative_citations:**
  `packages/content/tax/2025/rule.wages-line1a.json:18`.
  The v2 successor `rule.wages-line1a.v2.json` has `round` without `stage`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** the meaning of `stage`. Content writes
  the key once. Schema tests include `"stage": "final"` in a minimal
  `round` node (`tests/derivation/test_language_schemas.py:160`) — that
  is a schema-accepts-shape assertion, not a semantic execution, and
  `"final"` was not observed in the 134 files.

### C23 — `round.mode` as `ref rounding.convention`

- **layer:** 3 / 6iii
- **observed_syntax:** in all 59 `round` nodes, `mode` is
  `{ "op": "ref", "name": "rounding.convention" }`, not a string enum.
- **frequency:** 59/59 round occurrences; 35 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099div-1a-subtotal.json` (`mode` is
  the nested ref next to the `round` op at `:18`).
- **related content:** `packages/content/tax/2025/core_calculations.bundle.v2.json:191`
  lists `"half_up"` as the only entry in a `rounding.convention`
  `value_schema.enum`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that production `round` nodes select
  `half_up` / `half_even` / `down` / `up` by writing those strings on
  `mode`. Search for those four strings as `round.mode` in the 134 files
  found none. `half_up` does appear as `divide.rounding` (C14) and as
  the bundle enum above. Tests pass `"mode": "half_up"` to schema
  validation (`test_language_schemas.py:160`) and pass `half_up` as an
  *input finding value* for `rounding.convention`
  (`tests/derivation/test_runner.py:108`).

### C24 — op `parameter`

- **layer:** 1
- **observed_syntax:** two keysets:
  `{ "op": "parameter", "parameter_id", "key": <node> }` ×72;
  `{ "op": "parameter", "parameter_id" }` ×2 (no `key`).
- **frequency:** 74 occurrences in 7 files, all under `value`.
- **representative_citations:**
  `packages/content/tax/2025/rule.form1040-standard-deduction.json:19`
  (`parameter_id` + `key` ref `filing_status`);
  `packages/content/tax/2025/rule.sli-worksheet.json` (the two no-`key`
  nodes, `parameter_id` `tax.us.2025.parameter.sli-interest-cap`).
- **input_output_observed:** nine distinct `parameter_id`s, mix of
  `demo.parameter.*` and `tax.us.2025.parameter.*`.
- **status:** pending-reconciliation
- **see also:** C70 (the parameter-declaration citizens those ids name).

### C25 — op `bracket_fold`

- **layer:** 1
- **observed_syntax:** `{ "op": "bracket_fold", "table_id", "key", "value" }`.
- **frequency:** 95 occurrences in 8 files, all under `value`.
- **representative_citations:**
  `packages/content/tax/2025/rule.form1040-line16.json:17`.
  Files: `rule.form1040-line16.json` and `.v2`–`.v5`;
  `rule.ss-benefits-worksheet.json` and `.v2`–`.v3`.
- **input_output_observed:** `table_id` values and occurrence counts:
  `demo.parameter.ss-benefits-half-rate.2025` ×54,
  `demo.parameter.tax-brackets.2025` ×21,
  `demo.parameter.ss-benefits-85-rate.2025` ×12,
  `demo.parameter.qdcg-preferential-brackets.2025` ×8.
  `key` is a `ref` to `filing_status` in the line-16 citation.
- **runtime_consumer:** silent in this layer (no `evaluate()` unit test
  for `bracket_fold` was found). Schema path-exercise:
  `tests/derivation/test_language_schemas.py:159`.
  `tools/generate_dsbs_t3_content.py` mentions the name.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** the fold algorithm. Content writes
  `table_id`/`key`/`value`; this layer did not execute a bracket table.

### C26 — op `range_lookup`

- **layer:** 1
- **observed_syntax (secondary corpus only):**
  `{ "op": "range_lookup", "table_id", "key", "value" }`.
- **frequency:** 0 occurrences in the 134 primary rule-artifact files
  (search for `range_lookup` in `packages/content/tax/2025` returned 0
  files). 2 JSON files under `packages/sample_data/` contain the op,
  plus a third (`expected/report.json`) that mentions the string.
- **representative_citations:**
  `packages/sample_data/derivation/examples/rule-artifact.tax-table-line16.json:17`;
  `packages/sample_data/derivation/scenarios/first_slice/scenario.json`
  (same shape on `.rules[2].value.value`).
- **runtime_consumer:** schema tests require `table_id`+`key`+`value`
  (`tests/derivation/test_language_schemas.py:130-134`,
  asserting schema rejection of a missing `value` — not lookup
  semantics). `tests/derivation/test_package_validation.py` also
  mentions the name.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** any claim that `range_lookup` is
  unused. The observation is: this search of the Track 0 primary
  content corpus found 0 hits; the secondary sample_data corpus has
  the shape above.

### C27 — op `block`

- **layer:** 2
- **observed_syntax:** `{ "op": "block", "code": <STRING> }` only.
- **frequency:** 6 occurrences in 3 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.form1040-line12e.json:58`
  (`F1098_SCOPE_CONTRADICTION`);
  `packages/content/tax/2025/rule.schedule-a-line8a.json:56`
  (`MULTIPLE_F1098_OUT_OF_SCOPE`); also `VALUE_INVALID` in that file's
  `value` tree;
  `packages/content/tax/2025/rule.sli-worksheet.json`
  (`SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`, `SLI_UNIVERSAL_COMPONENT_VIOLATION`,
  `SLI_MFS_INELIGIBLE`).
- **evaluation_blocking_nonpublication:** content writes the code string
  as the `block` node's only payload. Tests that **assert** those codes
  include `tests/test_f1098_mortgage_interest_line12e_track2.py`
  (`F1098_SCOPE_CONTRADICTION`, `MULTIPLE_F1098_*`) and
  `tests/test_sli_worksheet_line21_track3.py` (`SLI_*`).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that these codes are in the same
  vocabulary as `blocked.code` on the citizen envelope (C33–C35). They
  are different strings in different places.

### C28 — op `require_closed`

- **layer:** 2 / 4
- **observed_syntax:** `{ "op": "require_closed", "source_set": <string> }`.
  Always under `when` (71 when / 0 value).
- **frequency:** 71 occurrences in 29 files; 32 distinct `source_set` ids.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099r-ira-fully-taxable-subtotal.json:56`.
- **runtime_consumer:** `evaluate()`.
- **semantic_effect:** synthetic 5: unclosed set raises `EvalBlocked`
  `category=SOURCE_SET_UNCLOSED`; closed set returns `True`.
  Asserting runner test:
  `tests/derivation/test_runner.py:119-122`
  (`test_unclosed_empty_source_blocks_with_closure_code`, code
  `BLOCK_CLOSURE` which the test imports from the evaluator; the
  synthetic run printed `BLOCK_CLOSURE=SOURCE_SET_UNCLOSED`).
- **status:** pending-reconciliation

### C29 — op `categorical_compare`

- **layer:** 1
- **observed_syntax:** `{ "op": "categorical_compare", "cmp", "left", "right" }`.
  All 368 occurrences use `"cmp": "eq"`.
- **frequency:** 368 occurrences in 39 files (216 when / 152 value).
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json:233`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** other `cmp` values on this op. Only
  `eq` was observed.

### C30 — op `category_literal`

- **layer:** 1
- **observed_syntax:** `{ "op": "category_literal", "fact_type": {"id","version"}, "value": <string> }`.
- **frequency:** 373 occurrences in 39 files (the same 39 as C29, plus
  extras feeding `collect_categorical_all_equal`).
- **input_output_observed:** `value` counts: `yes`×280, `married_filing_separately`×70,
  `no`×18, `married_filing_jointly`×3, `qualifying_surviving_spouse`×2.
- **representative_citations:** paired with C29 in
  `rule.capital-loss-carryover.long-term.json:233` (right-hand
  `category_literal` `value: "yes"`).
- **status:** pending-reconciliation

### C31 — op `collect_categorical_all_equal`

- **layer:** 1
- **observed_syntax:** `{ "op": "collect_categorical_all_equal", "name": <fact type>, "value": <category_literal> }`.
- **frequency:** 5 occurrences in 1 file.
- **representative_citations:**
  `packages/content/tax/2025/rule.sli-worksheet.json:669`
  (`tax.us.2025.f1098e.no-related-person-interest`); four sibling
  names in the same file:
  `no-qualified-employer-plan-interest`,
  `no-non-qualified-loan-component`,
  `no-employer-educational-assistance-interest`,
  `no-qtp-earnings-used`.
- **runtime_consumer:** `evaluate()`.
- **semantic_effect:** asserting tests
  `tests/derivation/test_collect_categorical_all_equal.py:56-91`:
  all-yes → `True`; one `no` anywhere in the row list → `False`
  (order-independent); absent source → `EvalBlocked` `DEPENDENCY_ABSENT`;
  out-of-domain row → `DEPENDENCY_INVALID`; access log records a collect,
  not a ref. Synthetic 4 reproduced all-yes / one-no / absent.
  Ran `pytest tests/derivation/test_collect_categorical_all_equal.py`
  — passed.
- **separately_versioned:** host `rule-artifact.v6`.
- **status:** pending-reconciliation

### C32 — op `conditional_dependency_set`

- **layer:** 2
- **observed_syntax:** `{ "op": "conditional_dependency_set", "condition": <bool or node>, "members": [<ref>, ...] }`.
- **frequency:** 20 occurrences in 17 files, all under `when`.
  `condition` shapes: `categorical_compare`×6, literal `true`×5,
  `compare`×5, `any`×3, `all`×1. Member-list lengths: 1, 2, 4, 5, 7, 17, 22.
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json:270`
  (`condition: true`, 5 `ref` members). Host schemas: v3, v4, v6.
- **runtime_consumer:** `run()`.
- **semantic_effect:** asserting tests in
  `tests/derivation/test_conditional_multi_dependency.py`:
  inactive condition (`condition=False`) publishes and does not treat
  members as missing (`:96-101`); active condition pins every evaluated
  member ref (`:103-112`); partial absence reports `DEPENDENCY_ABSENT`
  with members in declared order (`:114-126`); blocked dispositions pin
  present reads and do not invent pins for absent members (`:128-133`).
  Ran the matching `-k` slice — passed.
- **provenance:** see the pin assertions just cited.
- **status:** pending-reconciliation

---

## Surface 2 — Dependency, guard, publication, blocking (envelope)

### C33 — `blocked.code: DEPENDENCY_ABSENT`

- **layer:** 2
- **observed_syntax:** every rule-artifact has
  `"blocked": { "code": <string>, "missing": [<string>, ...] }`.
  `DEPENDENCY_ABSENT` is the most common `code`.
- **frequency:** 81 / 134 files. `missing` is always a list (lengths 0–33).
- **representative_citations:**
  `packages/content/tax/2025/rule.capital-loss-carryover.long-term.json`
  (`code` + `missing` of the boundary fact);
  `packages/content/tax/2025/rule.form1040-line16.v5.json:3`.
- **evaluation_blocking_nonpublication:** this is a **declared blocked
  object on the citizen**, not an execution trace. Runner tests assert
  the same code string on actual blocked results
  (`tests/derivation/test_runner.py:100-104`;
  `test_conditional_multi_dependency.py:122-126`).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that this object is what the runner
  emits. Content writes it; tests of `run()` also use the string.

### C34 — `blocked.code: OPEN_DEPENDENCY`

- **layer:** 2
- **observed_syntax:** same `blocked` object, different `code`.
- **frequency:** 33 / 134 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099div-1a-subtotal.json:32`
  (`missing: ["rounding.convention"]`);
  `packages/content/tax/2025/rule.f1099div-12-subtotal.json:3`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** the relationship between
  `OPEN_DEPENDENCY` and `DEPENDENCY_ABSENT`. Both appear as
  `blocked.code` in content. Tests mentioning `OPEN_DEPENDENCY`:
  `tests/test_dsbs_t1_schema_citizens.py`,
  `tests/source_completeness/test_track3_authority_dispatch.py`.

### C35 — `blocked.code: SOURCE_SET_UNCLOSED`

- **layer:** 2
- **observed_syntax:** same `blocked` object.
- **frequency:** 20 / 134 files.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099b-covered-lt-basis-subtotal.json:3`.
- **semantic_effect:** synthetic 5 and
  `tests/derivation/test_runner.py:119-122` demonstrate a run-time
  closure block whose evaluator category constant equals
  `SOURCE_SET_UNCLOSED`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that this envelope field is how
  `require_closed` (C28) reports failure. They share a string; whether
  they share a mechanism is another layer's question.

### C36 — `pins` on the rule-artifact

- **layer:** 7
- **observed_syntax:** list of `{id, origin, role, version}` (377 pins)
  or `{id, role, version}` (16 pins, all `role: parameter`).
  Observed pin `role` values in content: `input`×377, `parameter`×16.
  Observed `origin`: `assertion`×377, absent on the 16 parameter pins.
- **frequency:** 133 files have a `pins` key; 48 of those have `[]`;
  1 file (`rule.wages-line1a.json`) has no `pins` key.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099div-12-subtotal.json:16-22`
  (`role: input`, `origin: assertion`, `id: rounding.convention`);
  parameter pins e.g. `rule.sli-worksheet.json` (`role: parameter`,
  no `origin`).
- **provenance:** content declares intended pins. Tests of `run()` show
  **additional** roles on *published findings* that do not appear in
  this content field (C80).
- **status:** pending-reconciliation

### C37 — `composition` on a rule-artifact

- **layer:** 4
- **observed_syntax:** `{ "id": <composition id>, "version": <vN> }`.
- **frequency:** 15 files. Two composition ids:
  `tax.us.2025.interest-composition` (line-2b series +
  `rule.interest-positive-total.json`) and
  `tax.us.2025.schedule-a` (the Schedule A boundary/total rules).
- **representative_citations:**
  `packages/content/tax/2025/rule.form1040-line2b.json:43`.
- **status:** pending-reconciliation
- **see also:** C72.

### C38 — `accounts_for`

- **layer:** 4 / 5a
- **observed_syntax:** list of
  `{ "relationship": "itemizes_members"|"reads_subtotal", "family": {"id","version"} }`.
- **frequency:** 8 rule-artifact files (all host `rule-artifact.v5`, the
  covered-W subtotal / Schedule D 1b/8b v2 rules): `itemizes_members`×8
  + `reads_subtotal`×2. Also 2 attachment-rule files (C82).
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099b-covered-w-lt-adjustment-subtotal.v2.json:32`.
- **status:** pending-reconciliation

### C39 — `citations`

- **layer:** 7 (as a content field; not the walk)
- **observed_syntax:** list of `{id, version}` citation pins, length 0–6.
- **frequency:** present in 90 / 134; absent key in 44.
- **status:** pending-reconciliation

### C40 — `scope`

- **layer:** 1 (envelope)
- **observed_syntax:** two shapes:
  `{family, jurisdiction, tax_year}` ×112;
  those plus `"effective_from": "2025-01-01"` ×22.
- **representative_citations:**
  `packages/content/tax/2025/rule.f1099b-covered-lt-basis-subtotal.json`
  (the `effective_from` shape).
- **status:** pending-reconciliation

---

## Surface 5a — attachment-rule and form-field

### C41 — attachment `requirement` threshold shape

- **layer:** 5a
- **observed_syntax:**
  `{ citation, comparison: "strictly_greater_than", subtotals: [<symbol>], threshold_parameter: {id, version} }`.
- **frequency:** 13 / 15 attachment-rule files.
- **representative_citations:**
  `packages/content/tax/2025/rule.attachment.schedule-b.json` (v1;
  subtotals interest+dividends, threshold
  `tax.us.2025.parameter.schedule-b-threshold`);
  `packages/content/tax/2025/attachment.f8949.json` (v6).
- **separately_versioned:** observed under attachment-rule v1, v2, v4, v6, v8.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** other `comparison` values. Only
  `strictly_greater_than` was observed.

### C42 — attachment `requirement.kind: family_nonempty`

- **layer:** 5a
- **observed_syntax:** `{ citation, kind: "family_nonempty", source_family: {id, version} }`.
- **frequency:** 2 / 15 files.
- **representative_citations:**
  `packages/content/tax/2025/attachment.schedule-d.json:167` (host v3);
  `packages/content/tax/2025/attachment.schedule-d.v2.json` (host v4,
  same kind). Later schedule-d versions (v3–v6 of the *content*
  version axis) use the threshold shape (C41) instead.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that later schedule-d files still
  carry `family_nonempty`. Search of those later files did not find the
  string; they use C41.

### C43 — completeness `check: "presence"`

- **layer:** 5a
- **observed_syntax:** `completeness.required_answers[]` item
  `{ check: "presence", fact_type: {id, version}, symbol }`.
- **frequency:** 26 such answer objects across the 15 files (every
  attachment-rule file has `completeness`).
- **representative_citations:**
  `packages/content/tax/2025/attachment.f8949.json` (`required_answers`
  with `check: "presence"`).
- **status:** pending-reconciliation

### C44 — completeness `check: "value"`

- **layer:** 5a
- **observed_syntax:** `{ check: "value", equals: "yes", fact_type, symbol }`.
  All 46 `value` checks observed use `equals: "yes"`.
- **frequency:** 46 answer objects. Present in e.g.
  `packages/content/tax/2025/attachment.schedule-a.json:80`.
- **status:** pending-reconciliation
- **tests:** `tests/test_attachment_rule_v4_completeness_value.py`
  names the construct (and also names `attempt_attachment` — see
  `#Searches that returned no hit`).

### C45 — `completeness.branch_requirements`

- **layer:** 5a
- **observed_syntax:** list of
  `{ when_answer: {symbol, equals}, adds_required: [...], names_obligations?: [...] }`.
- **frequency:** 6 / 15 files
  (`attachment.schedule-d.v5.json`, `.v6.json`;
  `rule.attachment.schedule-b.json` and `.v2`–`.v4`).
- **representative_citations:**
  `packages/content/tax/2025/attachment.schedule-d.v5.json:54`.
- **status:** pending-reconciliation

### C46 — op `collect_members` (inside attachment itemizations)

- **layer:** 5a
- **observed_syntax:** `{ "op": "collect_members", "member_fact_type": {id, version}, "source_family": {id, version} }`.
- **frequency:** 69 occurrences; present in all 15 attachment-rule files.
  Itemization wrappers vary: v1 schedule-b uses `rows` (not `row_sets`);
  later files use `row_sets` + `authority` + `tie_out`; v6/v8 add
  `adjustment_rows`.
- **representative_citations:**
  `packages/content/tax/2025/rule.attachment.schedule-b.json:20`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that this is evaluator op `collect`
  (C09). Different name, different keys, different host citizen.

### C47 — `names_obligations` / `FINCEN_114_NAMED`

- **layer:** 5a
- **observed_syntax:** `branch_requirements[].names_obligations[]`
  `{ code: "FINCEN_114_NAMED", label: <string> }`.
- **frequency:** the four schedule-b attachment-rule files.
- **representative_citations:**
  `packages/content/tax/2025/rule.attachment.schedule-b.json:48`.
- **status:** pending-reconciliation

### C48 — form-field `dispositions`

- **layer:** 7 / 5a
- **observed_syntax:** every one of 50 form-field files has
  `dispositions` with keys
  `blocked`, `closure_backed_zero`, `computed_zero`,
  `guard_inapplicable`, `published_value`. Host schemas: v3×43, v2×7.
  `blocked.codes` observed across the 50 files:
  `DEPENDENCY_ABSENT`×49, `SOURCE_SET_UNCLOSED`×41,
  `DEPENDENCY_INVALID`×39, `CATEGORICAL_DOMAIN_MISMATCH`×31,
  `SOURCE_SET_OPEN`×1.
- **frequency:** 50 files.
- **representative_citations:**
  `packages/content/tax/2025/form1040.line-10.form-field.json:27`
  (`guard_inapplicable`);
  `packages/content/tax/2025/form1040.line-2b.form-field.json:32`
  (`SOURCE_SET_OPEN` — the only form-field using that code).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that `SOURCE_SET_OPEN` and
  `SOURCE_SET_UNCLOSED` are the same code. Both appear in form-field
  `blocked.codes`; only `SOURCE_SET_UNCLOSED` appears as a
  rule-artifact `blocked.code` (C35).

### C82 — attachment-rule `accounts_for`

- **layer:** 5a
- **observed_syntax:** same relationship vocabulary as C38.
- **frequency:** 2 files:
  `attachment.f8949.v2.json` (host v8),
  `attachment.schedule-d.v6.json` (host v8).
- **status:** pending-reconciliation

---

## Surface 5b-i — source-family term / predicate language

Track 0 placed this vocabulary in `source-family.v2`, not in
attachment-rule. Observed in content: 8 files carry `source-family.v2`;
2 of those 8 carry `member_constraints` and `identity_exclusivity`
(the two covered-W families). The other 40 source-family files are
host `source-family.v1` and have neither field.

### C49 — `member_predicate`

- **layer:** 5b-i (membership, not the nested predicate language)
- **observed_syntax:** `{ "fact_type": <string> }` in all 48 files.
  No `op` key.
- **representative_citations:**
  `packages/content/tax/2025/family.f1098.json:5`.
- **status:** pending-reconciliation

### C50 — `member_constraints`

- **layer:** 5b-i
- **observed_syntax:** list of
  `{ id, block_code, meaning, violated_when: <predicate> }`.
- **frequency:** 8 constraint objects in 2 files (4 each).
- **representative_citations:**
  `packages/content/tax/2025/family.f1099b-covered-w-lt.v2.json:25`
  (`field_equals` inside `violated_when`);
  twin file `family.f1099b-covered-w-st.v2.json`.
- **evaluation_blocking_nonpublication:** `block_code` values observed:
  `BOX_1G_FLAG_WITHOUT_AMOUNT`, `BOX_1G_AMOUNT_WITHOUT_FLAG`,
  `CODE_W_ON_GAIN`, `ADJUSTMENT_EXCEEDS_LOSS` (each in both files).
- **tests asserting behavior:**
  `tests/derivation/test_declarative_validation_runtime.py:125-140`
  (invalid member blocks the family and names the constraint);
  `tests/test_declarative_validation_2025_migration.py` and
  `tests/test_schedule_d_form8949_covered_wash_sale_t1.py` mention the
  four `block_code`s.
- **status:** pending-reconciliation

### C51 — `identity_exclusivity`

- **layer:** 5b-i
- **observed_syntax:**
  `{ id, incompatible_family: {id, version}, components: [{fact_id_bound_key}, ...] }`.
  Components are **not** term/predicate nodes.
- **frequency:** 1 object in each of the same 2 files. Each has 4
  components: `broker`, `statement`, `transaction`, `tax-year`.
- **representative_citations:**
  `packages/content/tax/2025/family.f1099b-covered-w-lt.v2.json:119`.
- **tests:** `tests/derivation/test_declarative_validation_runtime.py:285-320`
  (cross-family identity unique / collision / missing component).
- **status:** pending-reconciliation

### C52 — term op `field`

- **layer:** 5b-i
- **observed_syntax:** `{ "op": "field", "field": <name> }` ×8;
  `{ "op": "field", "field": <name>, "default": 0 }` ×4.
- **frequency:** inside the 8 `violated_when` trees (2 files).
- **representative_citations:**
  `family.f1099b-covered-w-lt.v2.json` (`field` with `default: 0` on
  `box_1g_wash_sale_disallowed_amount`).
- **status:** pending-reconciliation

### C53 — term op `literal`

- **layer:** 5b-i
- **observed_syntax:** `{ "op": "literal", "arg": 0 }`.
- **frequency:** 2 occurrences (one per covered-W family), inside
  `CODE_W_ON_GAIN`.
- **status:** pending-reconciliation

### C54 — term op `subtract`

- **layer:** 5b-i
- **observed_syntax:** `{ "op": "subtract", "left": {op:field, field:basis}, "right": {op:field, field:proceeds} }`.
- **frequency:** 2 occurrences (one per family), inside
  `ADJUSTMENT_EXCEEDS_LOSS`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** treating this as rule-artifact
  `subtract` (C12). Same op string, different host language.

### C55 — term op `floor_zero`

- **layer:** 5b-i
- **observed_syntax:** `{ "op": "floor_zero", "value": <term> }`.
- **frequency:** 2 occurrences.
- **representative_citations:**
  `packages/content/tax/2025/family.f1099b-covered-w-lt.v2.json:103`.
- **status:** pending-reconciliation

### C56 — predicate op `all` (source-family)

- **layer:** 5b-i
- **observed_syntax:** `{ "op": "all", "args": [ ... ] }` wrapping other
  predicates.
- **frequency:** 6 occurrences (3 constraints × 2 files). Two
  constraints (`ADJUSTMENT_EXCEEDS_LOSS`) are a bare `compare`, not
  wrapped in `all`.
- **representative_citations:**
  `packages/content/tax/2025/family.f1099b-covered-w-lt.v2.json:22`.
- **status:** pending-reconciliation

### C57 — predicate op `compare` (field `comparison`)

- **layer:** 5b-i
- **observed_syntax:** `{ "op": "compare", "comparison": "gt"|"ge", "left", "right" }`.
  Observed `comparison`: `gt` and `ge` only.
- **frequency:** 6 occurrences.
- **representative_citations:**
  `packages/content/tax/2025/family.f1099b-covered-w-lt.v2.json:64`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that this is rule-artifact `compare`
  (C16). The relation field is `comparison` here and `cmp` there.

### C58–C61 — predicate ops `field_equals`, `field_absent`, `field_present`, `field_not_equals`

- **layer:** 5b-i
- **observed_syntax:**
  `field_equals`: `{op, field, arg}` ×2;
  `field_absent`: `{op, field}` ×2;
  `field_present`: `{op, field}` ×2;
  `field_not_equals`: `{op, field, arg}` ×2.
- **frequency:** each appears in both covered-W families (the flag /
  amount pair of constraints).
- **representative_citations:**
  `packages/content/tax/2025/family.f1099b-covered-w-lt.v2.json:25`
  (`field_equals`).
- **tests:** contract tests name these ops in
  `tests/derivation/test_declarative_validation_contract.py`.
- **status:** pending-reconciliation

### C83 — `projects_from`

- **layer:** 5b-i / 4
- **observed_syntax:** `{ id, version }` pointing at a parent family.
- **frequency:** 6 / 48 source-family files (the six covered-W
  proceeds/basis/adjustment projection families, host v2).
- **status:** pending-reconciliation

### C62 — observed predicate depth

- **layer:** 5b-ii
- **observed_syntax:** nesting of predicate `all`/`compare`/leaf ops
  inside `violated_when`. Measured depth in the 8 committed constraints:
  depth 2 ×6, depth 1 ×2. Maximum observed in primary content: **2**.
- **frequency:** 8 constraints, 2 files.
- **tests asserting behavior:**
  `tests/derivation/test_declarative_validation_runtime.py:243-272`
  (`test_deeply_nested_term_blocks_not_raises`) builds an `add` term
  chain of depth 8 under a `compare` and asserts evaluation failure
  (not a raise). That test is about a **term** tree under `compare`,
  and its comment says package validation's depth walk does not recurse
  into `left`/`right` terms. Ran that test in the `-k deeply_nested_term`
  slice — passed.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** any claim about the number 6. Content
  observed max depth 2. The test constructs a deeper tree in a demo
  family under `packages/sample_data/declarative_validation_contract/`.

---

## Surface 4 — Package selection / binding / closure

### C63 — `artifact-package` members and roles

- **layer:** 4
- **observed_syntax:** `members[]` of `{id, role, schema, version}`.
- **frequency:** 35 package files; 3 package ids:
  `tax.us.2025.package.core-calculations` ×33,
  `tax.us.2025.package.first-tax-slice` ×1,
  `tax.us.2025.package.interest-slice` ×1.
- **representative_citations:** highest-numbered (not claimed current):
  `packages/content/tax/2025/package.core-calculations.v33.json`
  (`members` length 363). Member `role` counts in that file:
  `computation` 86, `citation` 72, `fact-type-bundle` 43, `form-field` 42,
  `parameter` 38, `source-closure-mapping` 36, `source-family` 36,
  `attachment-rule` 5, and 1 each of `dividend-universe`, `composition`,
  `field-mapping`, `checked-conclusion-binding`, `migration-artifact`.
- **status:** pending-reconciliation

### C64 — `admitted_schemas`

- **layer:** 4
- **observed_syntax:** list of schema-version strings.
- **frequency:** 34 / 35 package files (absent on
  `package.first-tax-slice.json`, host `artifact-package.v1`).
- **representative_citations:** v33 lists 39 strings including
  `rule-artifact.v2`–`v6`, `attachment-rule.v1,v2,v4,v6,v8`,
  `source-family.v1` and `.v2`. It does **not** list `rule-artifact.v1`
  or `attachment-rule.v3` or `attachment-rule.v5`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that omitted versions cannot execute.
  This is a list written in a package instance.

### C65 — `input_bindings` `required` / `optional_default`

- **layer:** 4
- **observed_syntax:** `{ fact_type: {id, version}, mode, symbol }`.
- **frequency:** 34 / 35 package files. v33 has 7 bindings: `required`×2
  (`filing_status`, `rounding.convention`), `optional_default`×5
  (blind/over-65/itemized).
- **representative_citations:**
  `packages/content/tax/2025/package.core-calculations.v33.json:645`
  (`"mode": "optional_default"`).
- **tests:** `optional_default` appears in four test modules (content /
  citizen checks), e.g.
  `tests/test_capital_gain_distributions_line7a_t1_citizens.py`.
- **status:** pending-reconciliation

### C66 — `entrypoints`

- **layer:** 4
- **observed_syntax:** list of `{id, version}`.
- **frequency:** 34 / 35 files; v33 has 141.
- **status:** pending-reconciliation

### C67 — `composition_obligations`

- **layer:** 4
- **observed_syntax:** list of symbol strings. v33:
  `tax.us.2025.interest.positive-total`,
  `tax.us.2025.interest.taxable-total`.
- **frequency:** 34 / 35 files.
- **status:** pending-reconciliation

### C68 — `conflict_semantics`

- **layer:** 4
- **observed_syntax:**
  `[{ selected_producer: {id, version}, symbol }]`.
- **frequency:** 5 files, all core-calculations v29–v33 (host
  `artifact-package.v22`–`v25`). Same payload in each:
  producer `tax.us.2025.rule.schedule-a-total` v1, symbol
  `tax.us.2025.schedule-a.total`.
- **representative_citations:**
  `packages/content/tax/2025/package.core-calculations.v33.json:47`.
- **tests:** `tests/derivation/test_package_validation.py` and two
  content tests mention the field.
- **status:** pending-reconciliation

### C84 — three named package lineages

- **layer:** 4
- **observed_syntax:** package `id` is not only `core-calculations`.
- **frequency:** `package.first-tax-slice.json` (`artifact-package.v1`),
  `package.interest-slice.json` (`artifact-package.v2`), plus the
  33-file core-calculations series.
- **status:** pending-reconciliation

### C69 — `source-closure-mapping`

- **layer:** 4 / 8 (maps families onto the store)
- **observed_syntax:** 49 files, all host `source-closure-mapping.v2`,
  keys `admission`, `admits_symbol`, `closure_fact_type`,
  `closure_horizon_key`, `family`, `id`, `member_fact_type`, `schema`,
  `version`. `admission` is `{ "condition": "current-literal-true" }`
  in all 49.
- **representative_citations:**
  `packages/content/tax/2025/closure-mapping.f1098.json:3`.
- **secondary corpus:** `source-closure-mapping.v1` also appears under
  `packages/sample_data/` (4 files).
- **status:** pending-reconciliation

---

## Surface 3 / parameters / composition citizens

### C70 — `parameter-declaration`

- **layer:** 3 (tables consumed by `parameter` / `bracket_fold`)
- **observed_syntax:** 18 files, all `parameter-declaration.v1`.
  `values` shapes: filing-status keyed scalars (standard deduction,
  capital-loss limit, SLI MAGI, …); filing-status keyed **bracket
  lists** `{lower, upper, rate}` (tax-brackets, qdcg preferential,
  ss-benefits half/85 rates); unkeyed scalars (`default-zero` = 0,
  `default-false` = false, `schedule-b-threshold` = 1500,
  `sli-interest-cap` = 2500).
- **representative_citations:**
  `packages/content/tax/2025/parameter.tax-brackets.json:13`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that bracket lists are a distinct
  schema type. They are a `values` shape inside the same citizen.

### C71 — `dividend-universe`

- **layer:** 4 (composition-adjacent declared content)
- **observed_syntax:** 4 files, schemas v1–v4 of the same id
  `tax.us.2025.dividend-universe`. Fields: `composable_boxes`,
  `recorded_non_composable_boxes`, `recorded_boxes_fact_type`,
  `capital_gain_signal`. Composable-box list length grows 2→3→4→5
  across v1–v4.
- **representative_citations:**
  `packages/content/tax/2025/dividend-universe.v4.json:7`.
- **status:** pending-reconciliation

### C72 — `taxable-interest-composition`

- **layer:** 4
- **observed_syntax:** 4 files, all host
  `taxable-interest-composition.v1`, content versions v1–v4.
  `coextensiveness: "slot-bijection"` in all four. `publishes` is
  `tax.us.2025.interest.taxable-total` on v1–v3 and
  `tax.us.2025.interest.positive-total` on v4. Constituent-list
  length 4→5→7→7.
- **representative_citations:**
  `packages/content/tax/2025/interest-composition.v4.json:2`.
- **status:** pending-reconciliation

### C73 — `checked-conclusion-binding` truth table

- **layer:** 2 / 7
- **observed_syntax:** one file,
  `checked-conclusion-binding.v1`, with `components[]` (aliases C1–C4)
  and `truth_table` rows
  `all_present_all_yes` → conclusion `"no"`, `direct_route: "eligible"`;
  `all_present_any_no` → `"yes"`, `direct_route: "guard_inapplicable"`;
  `any_missing` → `"unpublished"`, `disposition: "blocked"`,
  `code: "DEPENDENCY_ABSENT"`.
- **frequency:** 1 file.
- **representative_citations:**
  `packages/content/tax/2025/schedule-d-required.conclusion-binding.json:50`.
- **status:** pending-reconciliation

### C74 — `role-canon`

- **layer:** 2
- **observed_syntax:** `{ id, roles: { <role>: <kind> }, schema, version }`.
  Includes `applicability: "rule"`, `computation: "rule"`,
  `cross-form-bridge: "rule"`, `field-mapping: "rule"`,
  `operation-semantics: "operation"`, plus many non-rule roles.
- **frequency:** 1 file.
- **representative_citations:**
  `packages/content/tax/2025/role-canon.v1.json:10`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that every listed role appears on a
  rule-artifact. Observed rule-artifact `role` values are only
  `computation` and `field-mapping` (C02, C03).

### C75 — `migration-artifact`

- **layer:** 8-adjacent (succession of facts; Track 0 surface 8 is the
  store)
- **observed_syntax:** `{ schema: migration-artifact.v1, id, version, title, pairs, finding_mapping }`.
- **frequency:** 1 file:
  `packages/content/tax/2025/schedule1-adjustments-scope.succession.json`
  (13 pairs).
- **status:** pending-reconciliation

### C81 — `rounding.convention` bundle enum `half_up`

- **layer:** 6iii
- **observed_syntax:** a fact-type bundle entry whose `value_schema.enum`
  is the single string `"half_up"`.
- **frequency:** at least the one bundle file cited.
- **representative_citations:**
  `packages/content/tax/2025/core_calculations.bundle.v2.json:191`.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that the engine's rounding-mode set
  is `{half_up}` only. This is what that bundle entry lists.

---

## Surface 7 — Provenance / disposition / explanation records

### C76 — `npe-walk`

- **layer:** 7
- **observed_syntax:** no npe-walk citizen in
  `packages/content/tax/2025`. Secondary corpus carries
  `npe-walk.v1` and `npe-walk.v2` fixtures.
- **frequency:** sample_data examples + negatives under `dsbs_t1` and
  `core_tax_conditions`.
- **representative_citations:**
  `packages/sample_data/dsbs_t1/examples/npe-walk.v2.json:1`.
- **runtime_consumer:** `walk_npe` in
  `tests/derivation/test_npe_walk.py`.
- **semantic_effect:** asserting tests:
  published walk emits `schema: npe-walk.v3` with `node_kind: published`
  and children (`:29-78`); blocked walk carries `code: DEPENDENCY_ABSENT`
  and `unmet_references` (`:79-105`); inapplicable walk uses
  `guard_result: False` (`:107-118`). Ran that slice — passed.
- **status:** pending-reconciliation
- **this_layer_does_not_support:** that production tax content authors
  npe-walk documents. Observed production of the walk is in tests and
  sample_data fixtures.

### C77 — `derivation-record`

- **layer:** 7
- **observed_syntax:** not in `packages/content/tax/2025`. Secondary
  corpus: `derivation-record.v1`, `.v2`, `.v3` fixtures
  (started/completed, negatives).
- **representative_citations:**
  `packages/sample_data/dsbs_t1/examples/derivation-record.v3.json:1`.
- **tests:** `tests/derivation/test_records.py` (9 tests);
  `tests/derivation/test_track5_ledger.py`.
- **status:** pending-reconciliation

### C78 — `guard_result` / disposition `inapplicable`

- **layer:** 2 / 7
- **observed_syntax:** the string `inapplicable` appears in 63
  `packages/content/tax/2025` files (form-field `guard_inapplicable`
  explain-text and related). The field name `guard_result` appears in
  **0** content files (search returned 0).
- **tests asserting behavior:**
  `tests/derivation/test_runner.py:106-115`
  (`test_false_guard_is_inapplicable_not_blocked`: disposition
  `inapplicable`, `guard_result` is JSON `false`);
  `tests/derivation/test_npe_walk.py:107-118`.
  10 test modules mention `guard_result`; 20 mention
  `guard_inapplicable`.
- **status:** pending-reconciliation

### C79 — `BLOCK_LOOKUP_MISS` / out-of-domain categorical

- **layer:** 2
- **observed_syntax:** the strings `BLOCK_LOOKUP_MISS` and
  `BLOCK_CATEGORICAL_DOMAIN_MISMATCH` appear in **0** content files.
  Form-fields list `CATEGORICAL_DOMAIN_MISMATCH` (no `BLOCK_` prefix)
  in 31 files (C48).
- **tests asserting behavior:**
  `tests/derivation/test_runner.py:133-145`
  (`filing_status: "martian"` → blocked code `BLOCK_LOOKUP_MISS`,
  missing text contains no traceback).
  `tests/tax/test_track3_core_conditions.py` and
  `tests/test_f1098_mortgage_interest_lifecycle.py` mention
  `CATEGORICAL_DOMAIN_MISMATCH`.
- **status:** pending-reconciliation

### C80 — publication pin roles demonstrated by tests, not by content `pins`

- **layer:** 7
- **observed_syntax:** `tests/derivation/test_runner.py:148-158`
  asserts a published finding's pins include roles
  `field-mapping`, `input`, `operation-semantics`, `adoption`,
  `governance`. Content `pins` (C36) only write `input` and
  `parameter`.
- **frequency:** that asserting test (plus CDS pin tests, C32).
- **status:** pending-reconciliation
- **this_layer_does_not_support:** treating content `pins` as the
  complete pin set that survives execution.

---

## Searches that returned no hit

These are observations about **this search**, not claims that the
construct is absent from the language.

| What was searched | Where | How | Files hit |
| --- | --- | --- | ---: |
| `range_lookup` | `packages/content/tax/2025/*.json` | substring | 0 |
| `"op": "any"` as a source-family predicate | 48 source-family files | JSON walk of `op` | 0 |
| term op `add` in source-family | 48 source-family files | JSON walk of `op==add` | 0 |
| `attempt_attachment` | 15 attachment-rule files | substring | 0 |
| `half_even`, `down`, `up` as `round.mode` | 134 rule-artifact files | JSON walk of `round` nodes | 0 (`mode` is always a `ref`) |
| `half_even` anywhere in content | `packages/content/tax/2025` | substring | 0 |
| `guard_result` | `packages/content/tax/2025` | substring | 0 |
| `BLOCK_ABSENT`, `BLOCK_CLOSURE`, `BLOCK_LOOKUP_MISS`, `BLOCK_INVALID`, `BLOCK_CATEGORICAL_DOMAIN_MISMATCH` | `packages/content/tax/2025` | substring | 0 |
| rule-artifact `"role": "applicability"` or `"cross-form-bridge"` | 134 files | parsed `role` field | 0 (both strings live in `role-canon.v1` only) |
| `"when": false` | 134 files | parsed `when` | 0 |
| attachment-rule host `v5` or `v7` | 15 files | parsed `schema` | 0 (v7 is also absent as a published schema, Track 0) |
| `family_nonempty` | 15 attachment-rule files | substring | 2 (C42), not the later schedule-d versions |
| `"op": "count"` | `tests/` | substring | 0 |
| `"op": "block"` | `tests/` | substring | 0 |
| `MEMBER_CONSTRAINT_TOO_DEEP` | `tests/` | substring | 0 (`MemberConstraintTooDeep` ×2 modules) |
| `family_nonempty` | `tests/` | substring | 0 |

`attempt_attachment` **does** appear in four test modules
(`tests/test_attachment_rule_v4_completeness_value.py`,
`tests/test_dsbs_t2_schedule_b.py`,
`tests/test_schedule_d_form8949_covered_wash_sale_t1.py`,
`tests/derivation/test_portability.py`). The content search above is
the attachment-rule corpus only.

`form-field.v1` appears in `packages/sample_data/` (8 files) and not in
`packages/content/tax/2025` (content is v2/v3).

---

## Test evidence classification

Counts are **test modules** (files), not test functions, unless a
function is named.

### Asserting a behavior (result, disposition, code, or pins)

| Construct | Test | What it asserts |
| --- | --- | --- |
| `multiply` / `divide` | `tests/derivation/test_multiply_divide.py` | arithmetic values, `DEPENDENCY_INVALID` on zero divisor and unknown rounding, `half_even` rounding |
| `collect_categorical_all_equal` | `tests/derivation/test_collect_categorical_all_equal.py` | True/False, `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, access-log collect vs ref |
| false `when` | `tests/derivation/test_runner.py:106-115` | disposition `inapplicable`, `guard_result` false, not blocked |
| unclosed collect | `tests/derivation/test_runner.py:119-122` | blocked with closure code |
| out-of-domain `parameter`/`range` key | `tests/derivation/test_runner.py:133-145` | `BLOCK_LOOKUP_MISS`, no traceback leak |
| publication pins | `tests/derivation/test_runner.py:148-158` | roles `field-mapping`, `input`, `operation-semantics`, `adoption`, `governance` |
| `conditional_dependency_set` | `tests/derivation/test_conditional_multi_dependency.py:96-133` | inactive members not missing; active pins every ref; ordered `DEPENDENCY_ABSENT`; no invented pins |
| npe-walk | `tests/derivation/test_npe_walk.py:29-118` | published / blocked / inapplicable walks, schema `npe-walk.v3` |
| member_constraints evaluation | `tests/derivation/test_declarative_validation_runtime.py:125-272` | invalid member blocks family; deep term fails closed |
| identity_exclusivity | `tests/derivation/test_declarative_validation_runtime.py:285-320` | collision blocks; unique publishes |

### Exercising a path (schema-accepts, does-not-raise, or name mention)

| Construct | Test | Why this is path-exercise |
| --- | --- | --- |
| many ops including `range_lookup`, `bracket_fold`, `round` with `mode: half_up` and `stage: final` | `tests/derivation/test_language_schemas.py:130-163` | `schemas.validate` / `assert_rejected` on shapes; no evaluation |
| `range_lookup` | `tests/derivation/test_package_validation.py` | name in a package-validation module |
| `bracket_fold` | `tools/generate_dsbs_t3_content.py` | generator, not a test assertion |
| live coordinator runs | 50 modules containing `live_coordinate_run` / `live_workspace` / `subprocess` | end-to-end execution of packages; they demonstrate that *some* path runs, but they are not cited here as the definition of any one op unless the test also asserts a named construct (several SLI / F1098 tests do assert C27 codes) |

Live-lane modules that **do** assert named construct codes (still live
integration, but the assertion is about a construct):

- `tests/test_sli_worksheet_line21_track3.py` — `SLI_*` block codes, `collect_categorical_all_equal`
- `tests/test_f1098_mortgage_interest_line12e_track2.py` — `F1098_SCOPE_CONTRADICTION`, `MULTIPLE_F1098_*`
- `tests/test_schedule_d_form8949_covered_wash_sale_t1.py` — the four member-constraint `block_code`s

---

## Synthetic executions

Ran 2026-08-20 against this worktree. Consumer:
`packages.derivation.evaluator.evaluate` (and `EvalBlocked`). Shapes
copied from committed content; literals substituted for nested refs
where the point is the op, not the tax figure.

### S1 — `multiply` (shape of `rule.sli-worksheet.json:272`)

Input: `{"op":"multiply","left":"1500","right":"0.133"}`
Result: `Decimal('199.500')`

### S2 — `divide` (shape of `rule.sli-worksheet.json:301-310`)

Input: `{"op":"divide","left":"2000","right":"15000","min_decimal_places":3,"rounding":"half_up"}`
Result: `Decimal('0.133')`

### S3 — `divide` by zero (same shape)

Result: `EvalBlocked category=DEPENDENCY_INVALID missing=['division by zero']`
(`BLOCK_INVALID` constant printed as `DEPENDENCY_INVALID`)

### S4 — `collect_categorical_all_equal` (shape of `rule.sli-worksheet.json:669`)

All-yes rows → `True`. One `no` → `False`. Empty sources →
`EvalBlocked category=DEPENDENCY_ABSENT missing=['tax.us.2025.f1098e.no-related-person-interest']`.

### S5 — `require_closed` (shape of `rule.f1099r-ira-fully-taxable-subtotal.json:56`)

Unclosed → `EvalBlocked category=SOURCE_SET_UNCLOSED`.
Closed set containing that id → `True`.

### S6 — `choose` + `compare`

`when: {op:compare, cmp:gt, left:2, right:1}` → `then` value `10`.
`left:1, right:2` → `else` value `0`.

### S7 — arity-1 `add` (shape of covered-lt-basis-subtotal)

`{"op":"add","args":[Decimal("3")]}` → `3`.

Existing-test runs (inner loop, not the full suite):

```
pytest tests/derivation/test_multiply_divide.py \
       tests/derivation/test_collect_categorical_all_equal.py \
       tests/derivation/test_runner.py -k "false_guard or lookup or unclosed_empty or multiplies_two or divides_two or zero_divisor or min_decimal_places_worksheet or rounding_mode_half_even or single_member_all_yes or one_member_no or absent_source"
# 10 passed

pytest tests/derivation/test_npe_walk.py \
       tests/derivation/test_conditional_multi_dependency.py \
       tests/derivation/test_declarative_validation_runtime.py \
       -k "walk_npe_published or walk_npe_blocked or walk_npe_inapplicable or inactive_members or active_members_publish or active_multi_and_partial or deeply_nested_term or invalid_member_blocks"
# 8 passed, 2 subtests passed
```

---

## Open questions only another layer can answer

1. Are `OPEN_DEPENDENCY` (C34) and `DEPENDENCY_ABSENT` (C33) two names
   for one blocking condition, or two conditions? Content writes both
   as `blocked.code`.
2. Are `SOURCE_SET_OPEN` (one form-field) and `SOURCE_SET_UNCLOSED`
   (20 rules + 41 form-fields) the same code on different layers?
3. What consumer interprets arity-1 `add` wrapping `collect` (C11)?
   Is it identity, a rounding stage, or something else?
4. `round.mode` in production content is always a `ref` to
   `rounding.convention`, and the committed bundle enum lists only
   `half_up`. Tests and the divide op also speak `half_even`. How do
   those facts sit on declared vs implemented?
5. `range_lookup` is in sample_data and in schema tests, not in the
   134 primary rule-artifacts. Track 2 has both the declared set and
   this search result.
6. Term op `add` and predicate op `any` are named by Track 0 as part
   of the closed 5b-i vocabularies. This search of committed
   source-family content did not find them. Declared/implemented
   presence is not this layer's to assert.
7. `attempt_attachment` is named by tests and not by the 15
   attachment-rule files. Same caveat.
8. Content `pins` (C36) vs publication pins (C80): who adds
   `operation-semantics` / `adoption` / `governance` / `field-mapping`?
9. Does `require_closed` (C28) write `blocked.code: SOURCE_SET_UNCLOSED`
   (C35), or is the envelope field independently authored?
10. `role-canon` lists `applicability` and `cross-form-bridge` as rule
    roles; the 134 files' `role` field does not use them. Declared vs
    used is Track 2.
11. `checked-conclusion-binding` `direct_route: "guard_inapplicable"`
    (C73) vs form-field `guard_inapplicable` (C48) vs runner
    disposition `inapplicable` (C78): one mechanism or three?
12. Input/output types of `ref`/`collect` `name` targets against the
    store (Track 0 surface 8) — this layer can list the strings, not
    classify them.
13. `MAX_PREDICATE_DEPTH = 6` vs observed content depth 2 vs a test
    that nests **terms** (not predicates) to depth 8. Which bound
    applies to which tree, and is it declared, implemented, or both?

---

## Track 0 or plan problems this reading surfaced

Nothing in the Track 0 corpus definition was unworkable. Counts
reproduced. Filename-vs-schema and the two version axes behaved as
Track 0 said.

Recorded, not worked around:

1. **Plan `#Census unit` vs this layer's silence.** The unit asks for
   runtime consumer, semantic effect, evaluation/blocking, and
   surviving provenance on every construct. For most content-only
   observations those fields are silent here on purpose. That is not
   a plan defect if Track 2 is prepared to fill them from 1a/1b; it
   is a mismatch if Track 2 expects 1c to have populated them.
2. **`tests/helpers/` is empty of `.py` files.** Track 0 correctly
   lists it as one of five subdirectories. A reader who globs
   `tests/helpers/*.py` will see nothing; that is not a Track 0
   counting error.
3. **Layer 5 "what counts as a test" includes live modules that
   mention a construct without asserting it.** Track 0 left
   file-by-file classification to 1c; the asserting-vs-exercising
   table above is that classification. No Track 0 citation was found
   wrong while doing it.
4. **Charter vs plan on Track 1c:** they agree (observation only; no
   set-difference claims). No conflict to record.
5. **Track 0 surface 5b-i discoverability note holds.** The
   term/predicate trees are in two `source-family.v2` files, not in
   any attachment-rule file. Searching attachment-rule for
   `field_equals` would miss them.

No governance text was interpreted. No sibling deliverable was read
(the inquiries directory contained only Track 0 when this file was
written).
