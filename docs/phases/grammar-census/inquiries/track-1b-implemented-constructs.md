# Track 1b — Implemented construct set

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 1b — Runtime
- Status: complete for this stream (`status` on every construct record is `pending-reconciliation`)
- Source ref verified: `HEAD` `765dcadf136d0954707b1a0e8bc8b754a5a62f39` on `milestone/grammar-census-engine-language-map`
- Track 0 corpus pin for Layer 3: `0f8e078e37781a6d2a532b6cc638d0034b248b02` (re-checked: `git diff --name-only 0f8e078e..HEAD -- packages/ tests/ tools/` is empty)

This is the **implemented** construct set: what the running code in Track 0 Layer 3 actually interprets. It is not a declared-versus-implemented comparison. Every `status` field is `pending-reconciliation`. Set-difference claims belong to Track 2.

## Method

1. Read the Track 0 Layer 3 file list as the bounded corpus. Did not wildcard `packages/derivation/`.
2. Enumerated interpreter dispatch from control flow, not from comments or from `loader.OPERATION_VOCABULARY`.
3. Every path, line, version, and count below was produced by `grep`/`python3` against the tree at the source ref, or by a synthetic execution shown in `#Synthetic executions`.
4. Schema files were opened only as a *search* for a shape matching a runtime behavior already found in code. A construct is in this set because code interprets it, not because a schema names it. Where a search found no schema, that is recorded as a schema-search observation, not as a "undeclared" claim.
5. Did not read `track-1a-declared-constructs.md` or `track-1c-observed-usage.md`. At start of work the inquiries directory contained only Track 0.

## Record shape

Each record carries:

- `id` — stable handle `R<n>`
- `name`
- `layer` — Track 0 surface number (1–8)
- `interpreted_forms` — the shapes the runtime actually consumes
- `runtime_consumer` — module and function
- `semantic_effect`
- `input_output`
- `evaluation_blocking_invalidity_nonpublication`
- `separately_versioned` — what the *runtime* does with version, not what a schema might say
- `provenance_surviving`
- `schema_search` — whether a schema file was located for this runtime behavior, and how
- `citations` — committed code (and, where run, a synthetic execution)
- `status` — always `pending-reconciliation`
- `nearby_inferences_not_supported`

## Corpus actually read (Layer 3)

`packages/derivation/evaluator.py`, `declarative_validation.py`, `package_validation.py`, `production_resolver.py`, `production_executor.py`, `marshal.py`, `runner.py`, `reference_runner.py`, `loader.py`, `source_authority.py`, `projection.py`, `presentation_projection.py`, `surface_resolver.py`, `explanation.py`, `records.py`, `entry_loop.py`, `live.py`, `live_session.py`, `live_viewing.py`, `live_workspace.py`, `runners/derive.py`, `runners/entry_loop_evaluation.py`; `packages/kernel/act_log.py`, `contribution.py`, `currency.py`, `facts.py`, `findings.py`, `horizons.py`, `read_models.py`, `schema_registry.py`, `runners/inspect_workspace.py`.

`entry_loop.py`, `live_session.py`, `live_viewing.py`, `live_workspace.py`, `act_log.py`, `contribution.py`, `read_models.py`, and `inspect_workspace.py` were searched for expression dispatch (`op ==`, `evaluate(`). They contain no interpreter of the clause language. Track 0's note that they are thinner consumers of grammar *effects* matches what the control flow shows.

---

# Surface 1 — Core clause / expression language

## R1. `evaluate` dispatch

- **layer:** 1
- **interpreted_forms:** any JSON value. Non-`dict` is a scalar literal. A `dict` is an operation node keyed on `expr["op"]`.
- **runtime_consumer:** `packages/derivation/evaluator.py:101-267` `evaluate`
- **semantic_effect:** closed if-chain of 23 ops; anything else is `EvalBlocked(DEPENDENCY_INVALID, ["unknown op survived schema: …"])` at `:267`.
- **input_output:** `(expr, Environment, AccessLog) -> Any` or `EvalBlocked`
- **evaluation_blocking_invalidity_nonpublication:** unknown op is a contained block, not a crash. `KeyError` on a missing required field of a known op is not converted to `EvalBlocked` (inferred from the `expr["op"]` / `expr["name"]` subscripting; would be falsified by a `expr.get` wrapper, which is not present).
- **separately_versioned:** the dispatch itself is one unversioned function. It does not branch on `rule-artifact.vN`. Version filtering happens upstream in `package_validation._SUPPORTED_SEMANTIC_SCHEMAS` and in `runner._Run.use_v2`.
- **provenance_surviving:** per-op via `AccessLog` (R27).
- **schema_search:** not used to decide this construct. The dispatch is the code.
- **citations:** `evaluator.py:101-107,267`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** `loader.OPERATION_VOCABULARY` (`loader.py:86-103`) lists 14 of the 23 ops. That frozenset is **not** the dispatch table. A reader of `loader.py` alone would miss `count`, `block`, `multiply`, `divide`, `require_closed`, `categorical_compare`, `category_literal`, `collect_categorical_all_equal`, `conditional_dependency_set`. Whether that constant is supposed to match the evaluator is a Track 2 question.

## R2. `ref`

- **layer:** 1
- **interpreted_forms:** `{"op":"ref","name": <str>}`
- **runtime_consumer:** `evaluator.py:108-116`
- **semantic_effect:** records `name` in `access.refs`; returns `env.symbols[name]`. If `name` is in `env.symbol_fact_types` and that fact type has a categorical domain, the stringified value must be in the domain or the op blocks `DEPENDENCY_INVALID`.
- **input_output:** symbol name -> stored value (any type)
- **evaluation_blocking_invalidity_nonpublication:** missing symbol -> `DEPENDENCY_ABSENT` with `[name]`. Categorical miss -> `DEPENDENCY_INVALID` with `[val]`.
- **separately_versioned:** no
- **provenance_surviving:** the ref name is in `AccessLog.refs`; the runner turns a present ref into a pin (`runner.py:301-313`) and skips absent refs (no finding identity to pin).
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:108-116`; `runner.py:301-313`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `requires` is the complete set of refs a rule may read. `marshal._rule_required_symbols` and `package_validation` inbound reachability both also walk nested `ref` names in `when`/`value` for `rule-artifact.v3..v6`.

## R3. `collect`

- **layer:** 1
- **interpreted_forms:** `{"op":"collect","name": <str>, "source_set": <str>?}`
- **runtime_consumer:** `evaluator.py:118-131`
- **semantic_effect:** reads `env.sources.get(name, [])`. Non-empty: returns `[Decimal(row) for row in rows]`, does **not** consult `closed_sets`. Empty: zero (`[]`) only if `source_set` is present **and** in `env.closed_sets`; otherwise `SOURCE_SET_UNCLOSED` with `[source_set or name]`.
- **input_output:** collectable name -> `list[Decimal]` or block
- **evaluation_blocking_invalidity_nonpublication:** empty + unclosed -> `SOURCE_SET_UNCLOSED`. Non-empty unclosed **succeeds**. Coercion of a non-numeric row -> `DEPENDENCY_INVALID`.
- **separately_versioned:** no
- **provenance_surviving:** `access.collects`; empty closed path also `access.closure_reads`. Runner pins every collected finding id (`runner.py:314-321`) and, on a closure-backed zero, the mapping, declaration, and closure finding (`:372-386`).
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:118-131`. Synthetic: empty unclosed -> `SOURCE_SET_UNCLOSED ['x']`; empty closed -> `[]` with `closure_reads={'fam'}`; nonempty unclosed -> `[Decimal('1'), Decimal('2')]` with empty `closure_reads`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `collect` and `count` share closure semantics. They do not (see R4).

## R4. `count`

- **layer:** 1
- **interpreted_forms:** `{"op":"count","name": <str>, "source_set": <str>}` (`source_set` is a required subscript, not `.get`)
- **runtime_consumer:** `evaluator.py:133-141`
- **semantic_effect:** `len(rows)` of `env.sources.get(name, [])`, but **always** requires `source_set in env.closed_sets`, even when rows are present. Always records `closure_reads`.
- **input_output:** name + family id -> `int`
- **evaluation_blocking_invalidity_nonpublication:** unclosed -> `SOURCE_SET_UNCLOSED` with `[source_set]`, including when members exist.
- **separately_versioned:** no
- **provenance_surviving:** `access.collects` and `access.closure_reads`
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:133-141`. Synthetic: nonempty unclosed -> `SOURCE_SET_UNCLOSED ['fam']`; nonempty closed -> `2` with `closure_reads={'fam'}`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that an empty `count` is `DEPENDENCY_ABSENT`. Empty closed count returns `0`.

## R5. `block`

- **layer:** 1
- **interpreted_forms:** `{"op":"block","code": <str>}`
- **runtime_consumer:** `evaluator.py:143-144`
- **semantic_effect:** `raise EvalBlocked(expr["code"], [])` — the code string is taken from the expression, not from the evaluator's five constants.
- **input_output:** code -> contained block
- **evaluation_blocking_invalidity_nonpublication:** whatever string `code` holds. On the v2 ledger path, unknown codes are remapped (R35).
- **separately_versioned:** no
- **provenance_surviving:** the blocked disposition carries the (possibly remapped) code; `missing` is empty
- **schema_search:** searched published `*.schema.json` for several codes the runner emits; `LOOKUP_MISS` and `FAMILY_VALIDATION_BLOCKED` were not found as enum members. That is a search observation, not a completeness claim over every schema.
- **citations:** `evaluator.py:143-144`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `code` is restricted to the five `BLOCK_*` constants. The raise uses `expr["code"]` directly.

## R6. `parameter`

- **layer:** 1
- **interpreted_forms:** `{"op":"parameter","parameter_id": <str>, "key": <expr>?}`
- **runtime_consumer:** `evaluator.py:146-157`
- **semantic_effect:** looks up `env.parameters[parameter_id]`. With `key`, evaluates the key and indexes `values` as a dict; without `key`, returns the whole `values` as a Decimal.
- **input_output:** parameter id (+ optional key expr) -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** missing parameter -> `DEPENDENCY_ABSENT`. Missing key in dict -> `LOOKUP_MISS`.
- **separately_versioned:** pins the parameter citizen's `version` at `runner.py:370-371`
- **provenance_surviving:** `access.parameters`
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:146-157`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none beyond the control flow

## R7. `add`

- **layer:** 1
- **interpreted_forms:** `{"op":"add","args": [<expr>, …]}`
- **runtime_consumer:** `evaluator.py:159-160` plus `_flatten` `:274-282`
- **semantic_effect:** evaluates every arg, flattens lists (so a nested `collect` becomes addends), sums as `Decimal`, empty sum is `Decimal(0)`.
- **input_output:** args -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** non-numeric / bool addend -> `DEPENDENCY_INVALID`. Empty args publish zero, not a block.
- **separately_versioned:** no
- **provenance_surviving:** whatever nested ops record
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:159-160,274-282`. Synthetic: `add` of `[]` -> `Decimal(0)`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that empty `add` is invalid

## R8. `subtract`

- **layer:** 1
- **interpreted_forms:** `{"op":"subtract","left": <expr>, "right": <expr>}`
- **runtime_consumer:** `evaluator.py:162-163`
- **semantic_effect:** Decimal subtraction of two scalars (not flattened lists)
- **input_output:** two values -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** non-numeric -> `DEPENDENCY_INVALID`
- **separately_versioned:** no
- **provenance_surviving:** nested reads
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:162-163`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `subtract` folds a list the way `add` does. It does not call `_flatten`.

## R9. `multiply`

- **layer:** 1
- **interpreted_forms:** `{"op":"multiply","left": <expr>, "right": <expr>}`
- **runtime_consumer:** `evaluator.py:165-166`
- **semantic_effect:** Decimal product of two scalars
- **input_output:** two values -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** non-numeric -> `DEPENDENCY_INVALID`
- **separately_versioned:** **not** in `loader.CANON_OPERATIONS`. Runtime does not consult `env.canon` for this op.
- **provenance_surviving:** nested reads; not recorded in `access.operations`
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:165-166`; `loader.py:104`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that multiply's meaning is pinned as operation-semantics. The evaluator never reads canon for it.

## R10. `divide`

- **layer:** 1
- **interpreted_forms:** `{"op":"divide","left": <expr>, "right": <expr>, "rounding": <str>, "min_decimal_places": <int>}`
- **runtime_consumer:** `evaluator.py:168-169,306-325`
- **semantic_effect:** `left/right` quantized to `10**(-min_decimal_places)` with a mode from `_ROUND_MODES`. Zero divisor -> `DEPENDENCY_INVALID ["division by zero"]`. Mode not in `_ROUND_MODES` -> `DEPENDENCY_INVALID`. **Does not read `env.canon`.**
- **input_output:** two numbers + mode + places -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** zero divisor and unknown mode are contained blocks, not `ZeroDivisionError`
- **separately_versioned:** not in `CANON_OPERATIONS`; rounding lives on the expression, not a canon citizen
- **provenance_surviving:** nested reads; not in `access.operations`
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:306-325`. Synthetic: `1/0` -> `DEPENDENCY_INVALID ['division by zero']`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `divide` shares `round`'s whole-dollar `canon["unit"]`. The docstring at `:307-314` states the distinction; the control flow matches the docstring here.

## R11. `max`

- **layer:** 1
- **interpreted_forms:** `{"op":"max","args": [<expr>, …]}`
- **runtime_consumer:** `evaluator.py:171-172`
- **semantic_effect:** `max` of flattened Decimal args
- **input_output:** args -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** empty args raise **`ValueError`**, not `EvalBlocked`. Synthetic confirmed: `max() iterable argument is empty`.
- **separately_versioned:** no
- **provenance_surviving:** nested reads if any args ran
- **schema_search:** no schema located for the empty-max crash (searched by reading the control flow; there is no `EvalBlocked` wrapper)
- **citations:** `evaluator.py:171-172`. Synthetic: empty `max` -> `ValueError`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that every evaluator failure is a contained `EvalBlocked`

## R12. `compare`

- **layer:** 1
- **interpreted_forms:** `{"op":"compare","left": <expr>, "right": <expr>, "cmp": "eq"|"ne"|"gt"|"gte"|"lt"|"lte"}`
- **runtime_consumer:** `evaluator.py:174-177,285-293`
- **semantic_effect:** Decimal comparison. Unknown `cmp` is a Python `KeyError` on the dict at `:286-293`, not `EvalBlocked`.
- **input_output:** two numbers + cmp -> `bool`
- **evaluation_blocking_invalidity_nonpublication:** non-numeric -> `DEPENDENCY_INVALID`; unknown cmp -> uncontained `KeyError`
- **separately_versioned:** no
- **provenance_surviving:** nested reads
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:174-177,285-293`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that unknown `cmp` is a contained block

## R13. `all`

- **layer:** 1
- **interpreted_forms:** `{"op":"all","args": [<expr>, …]}`
- **runtime_consumer:** `evaluator.py:179-180`
- **semantic_effect:** Python `all(bool(evaluate(a, …)) for a in args)` — **short-circuits**. A later `ref` is not read, not pinned, and cannot block, once an earlier arg is false.
- **input_output:** args -> `bool`
- **evaluation_blocking_invalidity_nonpublication:** a false prefix suppresses subsequent blocks
- **separately_versioned:** no
- **provenance_surviving:** only the args that actually ran
- **schema_search:** no schema located for short-circuit; it is Python `all`
- **citations:** `evaluator.py:179-180`. Synthetic: `all([False, ref missing])` -> `False` with empty `access.refs`; `all([True, ref missing])` -> `DEPENDENCY_ABSENT ['missing']`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that every declared dependency in an `all` is always named on a block

## R14. `any`

- **layer:** 1
- **interpreted_forms:** `{"op":"any","args": [<expr>, …]}`
- **runtime_consumer:** `evaluator.py:182-183`
- **semantic_effect:** Python `any(...)` — short-circuits on the first true arg
- **input_output:** args -> `bool`
- **evaluation_blocking_invalidity_nonpublication:** a true prefix suppresses subsequent blocks
- **separately_versioned:** no
- **provenance_surviving:** only args that ran
- **schema_search:** no schema located for short-circuit
- **citations:** `evaluator.py:182-183`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** same as R13

## R15. `not`

- **layer:** 1
- **interpreted_forms:** `{"op":"not","value": <expr>}`
- **runtime_consumer:** `evaluator.py:185-186`
- **semantic_effect:** `not bool(evaluate(value))`
- **input_output:** any -> `bool`
- **evaluation_blocking_invalidity_nonpublication:** propagates inner blocks
- **separately_versioned:** no
- **provenance_surviving:** inner reads
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:185-186`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R16. `choose`

- **layer:** 1
- **interpreted_forms:** `{"op":"choose","when": <expr>, "then": <expr>, "else": <expr>}`
- **runtime_consumer:** `evaluator.py:188-190`
- **semantic_effect:** evaluates `when`, then **only** the taken branch
- **input_output:** three exprs -> the taken branch's value
- **evaluation_blocking_invalidity_nonpublication:** the untaken branch cannot block and is not pinned
- **separately_versioned:** no
- **provenance_surviving:** `when` plus the taken branch
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:188-190`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that both branches are evaluated for well-formedness at runtime. Only the taken branch runs.

## R17. `round`

- **layer:** 1 / 3 / 6iii
- **interpreted_forms:** `{"op":"round","mode": <expr>, "value": <expr>}`
- **runtime_consumer:** `evaluator.py:192-194,296-303`
- **semantic_effect:** reads `env.canon["round"]["spec"]`. Mode must be in **both** `_ROUND_MODES` **and** `canon["modes"]`. Value is quantized to `canon["unit"]` using the mapped `decimal` rounding constant.
- **input_output:** mode + value -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** unknown mode (either table) -> `DEPENDENCY_INVALID`. Missing canon key -> uncontained `KeyError`.
- **separately_versioned:** yes, via `env.canon["round"]` and a pin `role=operation-semantics` (`runner.py:387-388`)
- **provenance_surviving:** `access.operations` adds `"round"`
- **schema_search:** Track 0 already points at `operation-semantics.v1` for the mode names; this stream records the runtime dual gate, not the schema enum.
- **citations:** `evaluator.py:29-35,296-303`. Synthetic: mode `half_up` with canon modes `{half_up}` and unit `1` on `1.5` -> `Decimal(2)`; mode `down` against that canon -> `unknown rounding mode: 'down'`; mode `weird` in canon but not `_ROUND_MODES` -> same invalid block.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that the Python `_ROUND_MODES` dict is an independent vocabulary. It is a mapping the runtime also intersects with canon.

## R18. `range_lookup`

- **layer:** 1 / 3
- **interpreted_forms:** `{"op":"range_lookup","table_id": <str>, "key": <expr>, "value": <expr>}`
- **runtime_consumer:** `evaluator.py:196-199,328-342`
- **semantic_effect:** table is a parameter citizen. Rows selected by evaluated `key`. First row whose band contains `value` under `canon["boundary"]` wins. On miss: `canon["on_miss"]=="zero"` returns `Decimal(0)`, else `LOOKUP_MISS`.
- **input_output:** table + key + value -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** missing table -> `DEPENDENCY_ABSENT`; miss-and-not-zero -> `LOOKUP_MISS`
- **separately_versioned:** yes, via canon and parameter version pins
- **provenance_surviving:** `access.operations` + `access.tables`
- **schema_search:** `LOOKUP_MISS` as an evaluator category is a Python constant (`evaluator.py:27`). A grep of `packages/schemas/**/*.schema.json` for `LOOKUP_MISS` returned no hits. `derivation-record.v7` enumerates other blocked codes but not this string (checked).
- **citations:** `evaluator.py:328-342`. Synthetic: miss with `on_miss=zero` -> `0`; miss with `on_miss=block` -> `LOOKUP_MISS`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `LOOKUP_MISS` survives onto a v2 derivation-record disposition. R35 remaps codes not in `record_codes`.

## R19. `bracket_fold`

- **layer:** 1 / 3
- **interpreted_forms:** `{"op":"bracket_fold","table_id": <str>, "key": <expr>, "value": <expr>}`
- **runtime_consumer:** `evaluator.py:201-204,345-360`
- **semantic_effect:** loads `env.canon["bracket_fold"]["spec"]` into a local `canon` and **never reads it**. Folds `(min(value, upper) - lower) * rate` over rows with `value > lower`. Missing upper is open-ended.
- **input_output:** table + key + value -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** missing table -> `DEPENDENCY_ABSENT`. Missing canon key -> `KeyError` before the fold. No on-miss path; a value below every lower yields `0`.
- **separately_versioned:** a canon citizen is required to be present (load fails closed if the key is absent) but its `spec` fields do not change the fold
- **provenance_surviving:** `access.operations` + `access.tables`; pin `role=operation-semantics`
- **schema_search:** the fold algorithm is in Python. Whether a schema describes the same fold is Track 1a's layer.
- **citations:** `evaluator.py:345-360`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `bracket_fold` consults canon `boundary` / `on_miss` the way `range_lookup` does. It does not.

## R20. `require_closed`

- **layer:** 1 / 2
- **interpreted_forms:** `{"op":"require_closed","source_set": <str>}`
- **runtime_consumer:** `evaluator.py:206-211`
- **semantic_effect:** if `source_set` is in `env.closed_sets`, records `closure_reads` and returns `True`; else `SOURCE_SET_UNCLOSED`
- **input_output:** family id -> `True` or block
- **evaluation_blocking_invalidity_nonpublication:** unclosed -> `SOURCE_SET_UNCLOSED`
- **separately_versioned:** no
- **provenance_surviving:** `access.closure_reads` -> mapping/declaration/closure-finding pins
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:206-211`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R21. `categorical_compare`

- **layer:** 1
- **interpreted_forms:** `{"op":"categorical_compare","left": <expr>, "right": <expr>, "cmp": "eq"|"ne"}`
- **runtime_consumer:** `evaluator.py:213-218,363-379`
- **semantic_effect:** each operand must be `category_literal` or `ref`. Domains (fact-type ids) must be equal or `CATEGORICAL_DOMAIN_MISMATCH`. Then string equality / inequality.
- **input_output:** two categorical exprs -> `bool`
- **evaluation_blocking_invalidity_nonpublication:** non-categorical operand or domain mismatch -> `CATEGORICAL_DOMAIN_MISMATCH`; value not in `env.categorical_domains` -> `DEPENDENCY_INVALID`
- **separately_versioned:** domains come from fact-type `value_schema.enum` loaded in `runner.py:196-199`
- **provenance_surviving:** refs recorded as ordinary refs
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:213-218,363-385`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a `ref` operand's domain is always the bound fact type. If `symbol_fact_types` lacks the name, `_eval_categorical_operand` uses `str(name)` as the domain (`:376`).

## R22. `category_literal`

- **layer:** 1
- **interpreted_forms:** `{"op":"category_literal","fact_type": <id or {id,version}>, "value": <str>}`
- **runtime_consumer:** `evaluator.py:220-221` (bare return of `expr["value"]`) and `:367-372` when used as a categorical operand
- **semantic_effect:** as a top-level op, returns `value` with **no domain check**. As a categorical operand, validates against `env.categorical_domains`.
- **input_output:** literal -> `str`
- **evaluation_blocking_invalidity_nonpublication:** top-level: none. Operand path: `DEPENDENCY_INVALID` on domain miss.
- **separately_versioned:** package admission also checks the exact `(id, version)` pin (`CATEGORY_LITERAL_PIN_STALE`, `package_validation.py:1998-2018`)
- **provenance_surviving:** none of its own
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:220-221,367-372`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a top-level `category_literal` is domain-checked. Only the operand helper checks.

## R23. `collect_categorical_all_equal`

- **layer:** 1
- **interpreted_forms:** `{"op":"collect_categorical_all_equal","name": <str>, "value": <categorical expr>}`
- **runtime_consumer:** `evaluator.py:223-244`; source-name registration in `live.py:67-86,132-142`
- **semantic_effect:** reads `env.sources[name]` as **strings**, not Decimals. Empty -> `DEPENDENCY_ABSENT` (not closure). Each row is domain-checked against the expected fact type. Returns whether every row equals the expected category.
- **input_output:** collectable name + expected category -> `bool`
- **evaluation_blocking_invalidity_nonpublication:** empty -> `DEPENDENCY_ABSENT`; domain miss -> `DEPENDENCY_INVALID`. **No `source_set` / closure check.**
- **separately_versioned:** no
- **provenance_surviving:** `access.collects` (not `closure_reads`)
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:223-244`. Synthetic: empty -> `DEPENDENCY_ABSENT ['w']`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that this op is a `collect` variant with the two-layer closure rule. Empty is absence, not `SOURCE_SET_UNCLOSED`.

## R24. `conditional_dependency_set`

- **layer:** 1 / 2
- **interpreted_forms:** `{"op":"conditional_dependency_set","condition": <expr>, "members": [<expr>, …]}`
- **runtime_consumer:** `evaluator.py:246-265`
- **semantic_effect:** if condition is false, returns `True` and **does not evaluate members**. If true, evaluates every member; `DEPENDENCY_ABSENT` missing names are accumulated; any other `EvalBlocked` is re-raised immediately; if any absences remain, one `DEPENDENCY_ABSENT` names the complete list.
- **input_output:** condition + members -> `True` or block
- **evaluation_blocking_invalidity_nonpublication:** inactive members cannot block and are not pinned
- **separately_versioned:** walker in `package_validation._iter_cds_member_names` is applied only to `rule-artifact.v3..v6` (`:1974-1975`)
- **provenance_surviving:** condition reads always; member reads only when active
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:246-265`. Synthetic: false condition with missing ref -> `True`, empty `refs`; true condition with two missing refs -> `DEPENDENCY_ABSENT ['a','b']`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that inactive members appear on a block's `missing` list. They do not.

## R25. Scalar literals

- **layer:** 1
- **interpreted_forms:** any non-dict `expr` (string, number, bool, null)
- **runtime_consumer:** `evaluator.py:103-104`
- **semantic_effect:** returned as-is. A bool later fed to `_as_decimal` is rejected (R28). A bool fed to `all`/`any`/`choose`/`not` is used as a boolean.
- **input_output:** scalar -> same scalar
- **evaluation_blocking_invalidity_nonpublication:** none at this node
- **separately_versioned:** no
- **provenance_surviving:** none
- **schema_search:** not consulted for existence
- **citations:** `evaluator.py:103-104`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a JSON `true` guard is invalid. `choose`/`when` coerce with `bool(...)`.

## R26. Unknown-op invalid

- **layer:** 1
- **interpreted_forms:** `{"op": <anything not in the 23>}`
- **runtime_consumer:** `evaluator.py:267`
- **semantic_effect:** `EvalBlocked(DEPENDENCY_INVALID, ["unknown op survived schema: …"])`
- **input_output:** unknown node -> block
- **evaluation_blocking_invalidity_nonpublication:** contained invalid, not a crash
- **separately_versioned:** no
- **provenance_surviving:** none unless earlier nested ops ran (they cannot: the unknown op is the current node)
- **schema_search:** the error string claims the unknown op "survived schema". That is a comment on a prior gate, not proof a schema was consulted here.
- **citations:** `evaluator.py:267`. Synthetic: `{"op":"nope"}` -> `DEPENDENCY_INVALID ['unknown op survived schema: nope']`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that this line is itself a schema check. It is the evaluator default.

## R27. `AccessLog`

- **layer:** 7
- **interpreted_forms:** sets `refs`, `collects`, `parameters`, `tables`, `operations`, `closure_reads`
- **runtime_consumer:** `evaluator.py:47-59`; consumed by `runner._Run.pins_for` `:297-400`
- **semantic_effect:** the only channel from evaluation to publication pins. `closure_reads` is populated only on the empty-closed `collect` path, on `count`, and on `require_closed`.
- **input_output:** mutation during evaluate -> pin list
- **evaluation_blocking_invalidity_nonpublication:** a blocked eval can still have a partial log; `pins_for` skips refs with no `symbol_pin`
- **separately_versioned:** v2 input pins gain `origin`
- **provenance_surviving:** this *is* the surviving provenance of an evaluation
- **schema_search:** `AccessLog` is a Python dataclass. No schema located for it.
- **citations:** `evaluator.py:47-59`; `runner.py:297-400`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that every declared `requires` entry is pinned. Only actually-read present refs are.

## R28. Numeric coercion / bool refusal

- **layer:** 1
- **interpreted_forms:** any value passed to `_as_decimal`
- **runtime_consumer:** `evaluator.py:75-83`
- **semantic_effect:** `Decimal` passes through; `bool` is refused (`True == 1` is the stated reason in the comment; the `isinstance(value, bool)` guard is what the control flow does); other values `Decimal(str(value))` or `DEPENDENCY_INVALID`
- **input_output:** Any -> `Decimal` or block
- **evaluation_blocking_invalidity_nonpublication:** bool and unparseable -> `DEPENDENCY_INVALID`
- **separately_versioned:** no
- **provenance_surviving:** none
- **schema_search:** no schema located for the bool refusal
- **citations:** `evaluator.py:75-83`. Synthetic: `add` of `True` -> `expected number, got boolean True`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R29. `all` / `any` short-circuit

- **layer:** 1
- **interpreted_forms:** the Python generators at `evaluator.py:179-183`
- **runtime_consumer:** same
- **semantic_effect:** see R13/R14. Recorded separately because the short-circuit is a semantic-weight behavior with no field on the op node.
- **input_output:** as R13/R14
- **evaluation_blocking_invalidity_nonpublication:** as R13/R14
- **separately_versioned:** no
- **provenance_surviving:** partial
- **schema_search:** no schema located
- **citations:** `evaluator.py:179-183` plus the synthetic in R13
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `conditional_dependency_set` short-circuits member evaluation on first absence. It does not: it accumulates every `DEPENDENCY_ABSENT`.

## R30. Empty `max` uncontained error

- **layer:** 1
- **interpreted_forms:** `{"op":"max","args":[]}` (or all-empty after flatten)
- **runtime_consumer:** `evaluator.py:172`
- **semantic_effect:** Python `max()` over an empty generator raises `ValueError`, which `_execute` does not catch
- **input_output:** empty -> crash
- **evaluation_blocking_invalidity_nonpublication:** not a recorded block
- **separately_versioned:** no
- **provenance_surviving:** none
- **schema_search:** no schema located
- **citations:** synthetic in R11
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that the run will still saturate other rules after this. An uncaught `ValueError` leaves `_execute`.

---

# Surface 2 — Guard, eligibility, publication, blocking

## R31. `when` guard

- **layer:** 2
- **interpreted_forms:** `rule["when"]` as an expression tree (or a scalar; `True` is what `compile_validation_graph` writes on synthesized producers)
- **runtime_consumer:** `runner._Run.attempt` `:486-501`; `finalize_unreached` `:1218-1231`
- **semantic_effect:** evaluate `when`. `EvalBlocked` -> blocked disposition. False -> `inapplicable` with `guard_result: False`. True -> evaluate `value`.
- **input_output:** expr -> bool-ish, then a disposition
- **evaluation_blocking_invalidity_nonpublication:** false guard is inapplicable, not blocked, even if `value` would fail (value is not run)
- **separately_versioned:** same evaluate() for all accepted rule-artifact versions
- **provenance_surviving:** `ledger_pins_for` of the guard's AccessLog
- **schema_search:** not consulted for existence
- **citations:** `runner.py:486-501,1218-1231`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a false guard is skipped when later numeric `requires` are absent. `finalize_unreached` preflights the guard first and records inapplicable if it proves false (`:1212-1231`).

## R32. `requires` eligibility

- **layer:** 2
- **interpreted_forms:** `rule["requires"]` list of symbols. Attachment rules have no schema field `requires`; `_requires` synthesizes eligibility from requirement subtotals, itemization symbols, and compiled `.member-validation` suffixes (`runner.py:409-444`).
- **runtime_consumer:** `is_eligible` `:446-447`; saturate loop `:1347-1356`
- **semantic_effect:** a rule is attempted only when every eligibility symbol is already in `self.symbols`. Absence at attempt time still re-checks `rule["requires"]` (not `_requires`) at `:465-468` — so an attachment whose compiled `.member-validation` is missing is *not* caught by `attempt`'s step 1 (attachments go through `attempt_attachment`). The saturate loop uses `_requires` for eligibility, then `attempt_attachment`.
- **input_output:** symbol presence -> bool
- **evaluation_blocking_invalidity_nonpublication:** never-eligible ordinary rules fall through to `finalize_unreached`, which blocks `DEPENDENCY_ABSENT` on remaining `requires` unless a false guard preflight wins
- **separately_versioned:** attachment `_requires` grows with schema: v1 subtotals only; v2+ itemization symbols; v6/v8 adjustment and signed tie-out symbols
- **provenance_surviving:** missing list on the blocked row
- **schema_search:** compiled `requires` on attachment citizens is a post-compile in-memory field (`runner.py:432-442` comment). No attachment-rule schema was searched to confirm absence of that field — the comment is not treated as evidence; the control flow reads `rule.get("requires", [])` regardless.
- **citations:** `runner.py:409-447,1347-1356`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `attempt` step 1 and `is_eligible` consult the same symbol list for attachments. They do not.

## R33. Dispositions `published` / `inapplicable` / `blocked`

- **layer:** 2 / 7
- **interpreted_forms:** disposition rows on `RunResult.dispositions`
- **runtime_consumer:** `runner._Run.attempt` / `attempt_attachment` / `_record_blocked`
- **semantic_effect:** three atomic outcomes. False guard and first-publisher-loser are both `inapplicable`; only the guard case sets `guard_result: False`. Presentation treats inapplicable without that flag as an error (`presentation_projection.py:225-228,331-333`).
- **input_output:** per-rule step -> one row
- **evaluation_blocking_invalidity_nonpublication:** this *is* that behavior
- **separately_versioned:** v2 rows add `finding_id`, `act_id`, `symbol`, `code`, `missing`, `superseded_by`
- **provenance_surviving:** `pins` on the row; v2 ledger pins drop rule roles (R90)
- **schema_search:** `derivation-record.v7` (and earlier v2+) enumerates the three disposition strings. This stream records what the runner writes.
- **citations:** `runner.py:473-554,1156-1186`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that every inapplicable row is a false guard. Conflict-losers are inapplicable with empty pins and no `guard_result`.

## R34. First-publisher-wins

- **layer:** 2 / 4
- **interpreted_forms:** `if symbol in self.symbols` at `attempt` `:471-484` and `finalize_unreached` `:1249-1263`
- **runtime_consumer:** `runner._Run`
- **semantic_effect:** once a symbol is in `self.symbols`, a later eligible producer of the same symbol is `inapplicable`, optionally with `superseded_by` pointing at the winner's rule pin. **`conflict_semantics` / `selected_producer` are never read by `runner.py` (count of `conflict_semantics` in that file: 0).** They are read only by `package_validation` (R50).
- **input_output:** already-published symbol -> inapplicable
- **evaluation_blocking_invalidity_nonpublication:** inapplicable, not blocked
- **separately_versioned:** no
- **provenance_surviving:** empty pins on the loser; winner already published
- **schema_search:** `conflict_semantics.selected_producer` exists on multiple `artifact-package.vN` schemas (grep). The runtime scheduler does not consult that field. Not a set-difference claim — a statement about this layer's control flow.
- **citations:** `runner.py:471-484`; `package_validation.py:1076-1080,2020-2026`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that saturate order is irrelevant because ids are content-addressed. Content-addressed ids make a *given* finding byte-stable; *which* producer wins still follows eligibility order in `_execute`.

## R35. Blocking-code vocabulary and ledger remapping

- **layer:** 2 / 7
- **interpreted_forms:** evaluator constants plus runner-local codes
- **runtime_consumer:** `evaluator.py:24-28`; `runner.py:143-147,1164-1183`
- **semantic_effect:** evaluator emits `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `SOURCE_SET_UNCLOSED`, `LOOKUP_MISS`, `CATEGORICAL_DOMAIN_MISMATCH`. Runner also emits `ITEMIZATION_TIE_OUT_VIOLATION`, `COMPLETENESS_VALUE_VIOLATION`, `FAMILY_VALIDATION_BLOCKED`, plus member-level codes inside family validation. On `use_v2`, `_record_blocked` writes the original code to `self.blocked` but writes the disposition `code` only if it is in `record_codes`; otherwise **`DEPENDENCY_INVALID`**. `record_codes` includes `VALUE_INVALID` and several tax-named codes (`MULTIPLE_F1098_*`, `SLI_*`) that this evaluator never assigns. It does **not** include `LOOKUP_MISS` or `FAMILY_VALIDATION_BLOCKED`.
- **input_output:** internal code -> ledger code
- **evaluation_blocking_invalidity_nonpublication:** the remap is a v2-only ledger filter
- **separately_versioned:** `CURRENT_RECORD_SCHEMA = derivation-record.v7` (`records.py:40`); v1 path does not put `code` on the disposition row
- **provenance_surviving:** `self.blocked` keeps the internal code; the disposition may not
- **schema_search:** `derivation-record.v7.schema.json` lists `VALUE_INVALID` and the `SLI_*` codes; a grep of that file for `LOOKUP_MISS` did not hit. `FAMILY_VALIDATION_BLOCKED` was not found in any `*.schema.json` (repo grep).
- **citations:** `evaluator.py:24-28`; `runner.py:1164-1183`; `records.py:32-40`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that the evaluator's five categories are the ledger vocabulary

## R36. `optional_default` input binding

- **layer:** 2
- **interpreted_forms:** package `input_bindings[]` with `mode == "optional_default"` plus fact-type `optional_default.parameter`
- **runtime_consumer:** `runner._Run.__init__` `:218-264`; admission checks in `package_validation.py:1058-1067`
- **semantic_effect:** only when `use_v2` and the symbol is not already bound. Publishes a `derived-finding.v2` with `resolved_input.origin = "declared_default"` and pins the parameter. Stores the parameter's `values` in `self.symbols`.
- **input_output:** absent input -> published default finding
- **evaluation_blocking_invalidity_nonpublication:** if the parameter is missing from `ctx.parameters`, the branch is skipped (no default, no block here)
- **separately_versioned:** gated on `use_v2`; finding schema `derived-finding.v2`
- **provenance_surviving:** pin `origin=declared_default`; downstream refs copy that origin as provenance (`runner.py:512-516,550-552`)
- **schema_search:** not used to decide the construct
- **citations:** `runner.py:218-264`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a missing default parameter is a hard run error. The `if param_val is not None` guard silently skips.

## R37. Rule roles

- **layer:** 2
- **interpreted_forms:** `computation`, `applicability`, `field-mapping`, `cross-form-bridge` on a rule; pin `role` copied from `rule["role"]`
- **runtime_consumer:** `_RULE_ROLES` in `package_validation.py:191` (admission) and `explanation.py:16` / `runner.py:128-130` (ledger exclusion)
- **semantic_effect:** admission requires package pin role to match the rule citizen's role (`ROLE_MISMATCH`). Evaluation does not branch on role. Explanation treats these four as `produced_by`. Ledger pins drop them on v2 (`_LEDGER_EXCLUDED_PIN_ROLES`).
- **input_output:** role string -> pin / explanation kind
- **evaluation_blocking_invalidity_nonpublication:** role mismatch is a package issue, not a run block
- **separately_versioned:** `loader.ROLE_VOCABULARY` (`loader.py:55-82`) is a larger set used by `role_vocabulary_report`, not by `evaluate`
- **provenance_surviving:** the producing-rule pin uses the rule's role; v2 ledger then strips it
- **schema_search:** not used to decide the construct
- **citations:** `package_validation.py:191,919-922`; `runner.py:128-130,298-300,402-407`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that role changes arithmetic. It does not.

## R38. `finalize_unreached` guard preflight

- **layer:** 2
- **interpreted_forms:** unreached ordinary rules after saturate
- **runtime_consumer:** `runner.py:1188-1330`
- **semantic_effect:** attachments: honor compiled `.member-validation` requires, else `attempt_attachment`. Ordinary rules: try `when`; if it evaluates to `False`, inapplicable even when `requires` are missing; if the preflight blocks or is true, fall through to missing-requires / conflict / evaluate.
- **input_output:** leftover rules -> dispositions
- **evaluation_blocking_invalidity_nonpublication:** false guard beats missing requires
- **separately_versioned:** no
- **provenance_surviving:** guard-preflight pins if inapplicable
- **schema_search:** no schema located for this precedence. It is runner control flow.
- **citations:** `runner.py:1188-1247`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that saturate and finalize use identical precedence. Saturate never attempts an ineligible rule, so it never sees this preflight.

## R39. `use_v2` schema switch

- **layer:** 7
- **interpreted_forms:** `self.use_v2` is true if any rule is `rule-artifact.v2..v6` **or** any attachment schema is present (`runner.py:185-191`)
- **runtime_consumer:** `_Run.__init__`, `pins_for`, `run_and_record`
- **semantic_effect:** switches derived-finding `v1`/`v2`, pin `origin`, disposition extra fields, optional_default, and — via `records.started_record` — `derivation-record.v1` vs `CURRENT_RECORD_SCHEMA` (`derivation-record.v7`). The flag is named `use_v2` and selects v7.
- **input_output:** rule schema set -> record/finding schema
- **evaluation_blocking_invalidity_nonpublication:** v1 findings are validated against `act-derived-publication.v1` as well as the finding schema; v2 findings only `validate_declared` (`runner.py:530-534`)
- **separately_versioned:** this *is* the version switch
- **provenance_surviving:** `origin` only on v2 input pins
- **schema_search:** `records.py:178` `CURRENT_RECORD_SCHEMA if use_v2 else "derivation-record.v1"`
- **citations:** `runner.py:185-191,1412-1418`; `records.py:40,168-186,204-205`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `use_v2=True` emits `derivation-record.v2`. Synthetic: `started_record(..., use_v2=True)["schema"] == "derivation-record.v7"`.

## R40. Saturate-to-fixpoint scheduler

- **layer:** 2
- **interpreted_forms:** `while progress: for rule in ctx.rules: if eligible and not resolved: attempt`
- **runtime_consumer:** `runner._execute` `:1343-1358`
- **semantic_effect:** data-driven forward chaining in package member order. Attachments use `attempt_attachment`; synthesized `*.member-validation.synthesized` ids use `_evaluate_family_validation` inside `attempt`.
- **input_output:** `RunContext` -> `RunResult` with `stop_reason="saturated"`
- **evaluation_blocking_invalidity_nonpublication:** contained per rule; the loop continues
- **separately_versioned:** no
- **provenance_surviving:** publications + dispositions + blocked
- **schema_search:** no schema located for the scheduler
- **citations:** `runner.py:1343-1358`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R41. Demand-driven reference runner

- **layer:** 2
- **interpreted_forms:** same `_Run.attempt` / `attempt_attachment`, different traversal
- **runtime_consumer:** `reference_runner.py:27-66`
- **semantic_effect:** recursively resolve `requires` of each producer, then fire. Cycles in demand return without firing (`resolving` set). A second while-loop catches late eligibility.
- **input_output:** same `RunResult` shape
- **evaluation_blocking_invalidity_nonpublication:** same per-rule step
- **separately_versioned:** no
- **provenance_surviving:** same pin assembly
- **schema_search:** no schema located
- **citations:** `reference_runner.py:27-66`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a cyclic demand is a recorded block. It is a silent return; finalize still runs.

---

# Surface 3 — Operation-semantics canon

## R42. Canon load and `env.canon`

- **layer:** 3
- **interpreted_forms:** JSON citizens in `packages/canon/derivation/*.json`, keyed by `operation`
- **runtime_consumer:** `loader.load_canon` `:136-162`; `Environment.canon` `evaluator.py:70`
- **semantic_effect:** every `CANON_OPERATIONS` member (`round`, `range_lookup`, `bracket_fold`) must be present exactly once or `SchemaValidationError`. Duplicate operation is a canon defect. Loaded canon is passed into every evaluation.
- **input_output:** directory -> `{op: citizen}`
- **evaluation_blocking_invalidity_nonpublication:** load-time error, not a per-rule block
- **separately_versioned:** each citizen has its own `version`; pins use that (`runner.py:387-388`)
- **provenance_surviving:** operation-semantics pins only for ops that set `access.operations` (round / range_lookup / bracket_fold), not multiply/divide
- **schema_search:** `loader.OPERATION_SEMANTICS_SCHEMA = "operation-semantics.v1"` (`:51`) is the constant name used in error strings; `validate_declared` uses whatever `schema` the citizen itself names (v1 or v2).
- **citations:** `loader.py:84-104,136-162`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `OPERATION_VOCABULARY` is the executable op set (see R1)

## R43. `_ROUND_MODES`

- **layer:** 3 / 6iii
- **interpreted_forms:** `half_up|half_even|down|up` -> `decimal.ROUND_*`
- **runtime_consumer:** `evaluator.py:30-35`, used by `_round` and `_divide`
- **semantic_effect:** the only rounding modes the process can apply. Canon may name a subset (R17); divide uses this table alone.
- **input_output:** mode string -> decimal rounding constant
- **evaluation_blocking_invalidity_nonpublication:** unknown -> `DEPENDENCY_INVALID`
- **separately_versioned:** the dict is unversioned Python
- **provenance_surviving:** none of its own
- **schema_search:** Track 0 classified this as grammar proper because of `operation-semantics.v1`. This stream records the Python mapping as the runtime behavior.
- **citations:** `evaluator.py:30-35,299,321`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R44. `range_lookup` boundary default

- **layer:** 3
- **interpreted_forms:** `canon["boundary"]` string
- **runtime_consumer:** `evaluator.py:95-98,338`
- **semantic_effect:** only `"lower_inclusive_upper_exclusive"` is special-cased. **Any other string**, including a missing-but-present unexpected value, takes the `else` branch: lower exclusive, upper inclusive. Synthetic: at the lower bound, LIE is true and `"anything_else"` is false; at the upper bound, LIE is false and `"anything_else"` is true.
- **input_output:** boundary name + x,lower,upper -> bool
- **evaluation_blocking_invalidity_nonpublication:** unknown boundary is not a block; it is the other convention
- **separately_versioned:** via canon
- **provenance_surviving:** none
- **schema_search:** not used to decide the construct; the `else` is Python
- **citations:** `evaluator.py:95-98`. Synthetic shown in `#Synthetic executions`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that an unknown boundary string is invalid

---

# Surface 4 — Package selection, binding, closure

## R45. `validate_package`

- **layer:** 4
- **interpreted_forms:** an `artifact-package.vN` instance plus a `(id, version) -> citizen` corpus
- **runtime_consumer:** `package_validation.validate_package` `:727-2081`; hard-gated by `production_resolver.resolve_production_package` `:363-371`
- **semantic_effect:** never raises for citizen defects; records `MemberIssue`s; `ok` is `not issues`. Production refuses unless `ok`.
- **input_output:** package + corpus -> `PackageValidation`
- **evaluation_blocking_invalidity_nonpublication:** a failed package never executes
- **separately_versioned:** checks branch on `package["schema"]` and on each member's `schema`
- **provenance_surviving:** issues are data; citation_resolutions list statically resolved citations
- **schema_search:** the function also calls `schemas.validate_declared` on the package and each member
- **citations:** `package_validation.py:727-752,2071-2081`; `production_resolver.py:363-371`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `ok` authorizes a subset. The resolver returns `HARD_GATE_REFUSED` for any issue.

## R46. `_SUPPORTED_SEMANTIC_SCHEMAS`

- **layer:** 4
- **interpreted_forms:** a frozenset of schema ids (`package_validation.py:246-293`) including `attachment-rule.v1..v6,v8` (no v7), `rule-artifact.v1..v6`, `source-family.v1` and `.v2`, `operation-semantics.v1` and `.v2`, `fact-type.v2` (not v1), `form-field.v1..v3`, `quantity-vocabulary.v1..v12`, plus `_NON_INPUT_SCHEMAS` which are listed so they can be rejected as `E14_2_FORBIDDEN_DEPENDENCY` rather than `MEMBER_SCHEMA_UNSUPPORTED`
- **runtime_consumer:** `validate_package` `:770-778`
- **semantic_effect:** a registry-valid member whose schema is absent here is `MEMBER_SCHEMA_UNSUPPORTED` and is **not** added to `resolved`, so later checks never see it.
- **input_output:** schema id -> admit or issue
- **evaluation_blocking_invalidity_nonpublication:** admission refusal
- **separately_versioned:** this *is* the runtime's accepted-schema set. Track 0's reading that "relevant = accepted by the runtime's literal sets" matches this constant.
- **provenance_surviving:** the issue row
- **schema_search:** the set is Python. `fact-type.v1` and `source-closure-mapping.v1` are named in the comment at `:244-245` as intentionally excluded.
- **citations:** `package_validation.py:238-293,770-778`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that every schema in this set has a dedicated semantic handler. Several are admitted then only role-checked.

## R47. Synthesized `<family>.member-validation`

- **layer:** 4 / 5b
- **interpreted_forms:** a compiled `rule-artifact.v5` producer with `id` `{family}.member-validation.synthesized`, `when: True`, `value: True`, `blocked.code: FAMILY_VALIDATION_BLOCKED`, plus a `requires` entry `{family}.member-validation` appended onto every structurally reaching consumer
- **runtime_consumer:** `compile_validation_graph` `:574-639`; executed by `attempt` `:461-462` -> `_evaluate_family_validation` `:628-856`
- **semantic_effect:** reachability, not authoring, creates the edge. Execution evaluates `member_constraints` and `identity_exclusivity` over current members. Success publishes `"true"` and inserts the symbol so downstream eligibility can see it. Failure blocks `FAMILY_VALIDATION_BLOCKED` (then remapped on the v2 ledger, R35).
- **input_output:** constrained families -> extra compiled rules
- **evaluation_blocking_invalidity_nonpublication:** see R74
- **separately_versioned:** producer is always emitted as `rule-artifact.v5` (`:617`)
- **provenance_surviving:** per-member findings plus a family-level true finding; pins include mapping, declaration, closure finding, horizon, and composition pins of member results
- **schema_search:** `FAMILY_VALIDATION_BLOCKED` was not found in `*.schema.json`. The synthesized citizen is validated against `rule-artifact.v5` when `schemas` is supplied (`:636-637`).
- **citations:** `package_validation.py:574-639`; `runner.py:461-462,628-856`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a family without `member_constraints` / `identity_exclusivity` / `itemizations` / `completeness` gets a producer. `_is_constrained` (`:91-97`) is the gate.

## R48. Universe guard (`COLLECT_TARGET_NOT_FAMILY`)

- **layer:** 4
- **interpreted_forms:** every `collect` node's `name` and `source_set` on a rule-artifact, when `package["schema"]` is in `artifact-package.v3`–`v17` inclusive (15 versions; v7 is in this set). **Not** v18–v25.
- **runtime_consumer:** `package_validation.py:1533-1549,1663-1681`
- **semantic_effect:** `source_set` must name a **`source-family.v1`** member (the dict `source_family_members` is built only from `schema == "source-family.v1"` at `:1550-1554`). The collect `name` must equal that family's `member_predicate.fact_type`. Failure: `COLLECT_TARGET_NOT_FAMILY`. Also forbids consuming `recorded_non_composable` fact types (`RECORDED_NON_COMPOSABLE_INPUT`) regardless of the universe-guard version gate.
- **input_output:** collect nodes -> issues or not
- **evaluation_blocking_invalidity_nonpublication:** admission
- **separately_versioned:** yes — a hard-coded schema-id set, not "latest"
- **provenance_surviving:** issue rows
- **schema_search:** no feature-matrix citizen was located (Track 0 gap 1). The set is the runtime.
- **citations:** `package_validation.py:1533-1549,1550-1554,1663-1681`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `source-family.v2` participates in this collect-target check. It is not in `source_family_members`. Whether a v2-only family would fail or skip is a Track 2 question about content; the dict construction is v1-only.

## R49. Inbound reachability

- **layer:** 4
- **interpreted_forms:** `package["entrypoints"]` plus every `form-field.v1..v3` as extra roots; edges from requires/refs/collects/parameters/compositions/citations/bundles
- **runtime_consumer:** `package_validation.py:1307-1523`
- **semantic_effect:** BFS from roots. Unvisited members -> `MEMBER_UNREACHABLE`. Exact entrypoint `(id, version)` matching is applied only for `artifact-package.v20`–`v25` (`:1319-1354`); older packages keep version-inexact roots. `closed_v2_surface` is `package version != "v1"` (`:1361`) — that is the **package instance** version axis, not the schema axis (Track 0's two-axes warning).
- **input_output:** graph -> issues
- **evaluation_blocking_invalidity_nonpublication:** admission
- **separately_versioned:** two different version axes are mixed in this function; recorded rather than normalized
- **provenance_surviving:** issue rows
- **schema_search:** not used to decide the construct
- **citations:** `package_validation.py:1307-1523`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that "v1" here means `artifact-package.v1`. The test is `str(package.get("version")) != "v1"`.

## R50. `conflict_semantics` at admission

- **layer:** 4
- **interpreted_forms:** `package["conflict_semantics"]` list of `{symbol, selected_producer}`
- **runtime_consumer:** `package_validation.py:1076-1080,2020-2026`
- **semantic_effect:** (1) a form-field whose symbol has multiple producers needs a `selected_producer` pin in the package (`FORM_FIELD_PRODUCER_CONFLICT`); (2) unique output ownership: two publishers of one symbol are `OUTPUT_OWNERSHIP_CONFLICT` unless the symbol is in `declared_conflicts`. The selected producer is **not** consulted at evaluation (R34).
- **input_output:** package field -> issues
- **evaluation_blocking_invalidity_nonpublication:** admission only
- **separately_versioned:** present on many artifact-package schema versions (grep); runtime meaning is this check
- **provenance_surviving:** issue rows
- **schema_search:** schema files name `selected_producer`; runner does not read it
- **citations:** `package_validation.py:2020-2026`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that admission's selected producer is the runtime winner

## R51. Composition obligations

- **layer:** 4
- **interpreted_forms:** `package["composition_obligations"]` plus `taxable-interest-composition.v1` members
- **runtime_consumer:** `package_validation.py:1134-1272`
- **semantic_effect:** each obligated symbol must have a composition member and a producing rule whose `composition` pin, `requires`, value-`ref`s, `require_closed` reads, and input pins bijection-match the constituents. Special case: `form1040-line2b@v4` publishing `interest.taxable-total` may resolve composition through the positive-total citizen and `_V11_ADJUSTMENT_SLOTS` (`:211-221,1214-1259`).
- **input_output:** obligation list -> issues
- **evaluation_blocking_invalidity_nonpublication:** admission
- **separately_versioned:** the v11 adjustment route is keyed on a content id/version, not a schema version
- **provenance_surviving:** issue rows
- **schema_search:** `_V11_ADJUSTMENT_SLOTS` and `_V3_ADJUSTMENT_BINDINGS` are Python literals (`:211-221`). No schema located for those three-class tuples.
- **citations:** `package_validation.py:211-221,1154-1272`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that composition checks are schema-family-generic. Several branches name specific tax ids.

## R52. `input_bindings`

- **layer:** 4 / 2
- **interpreted_forms:** `package["input_bindings"]` `{symbol, fact_type{id,version}, mode}`
- **runtime_consumer:** admission `package_validation.py:1049-1067`; marshalling `marshal.py:252-301`; optional_default R36
- **semantic_effect:** binds a run symbol to a fact type. `mode` is not used during marshalling (`marshal.py:261-262` comment matches the `continue` on absence). Disagreement among multiple current findings for a non-collect symbol leaves the symbol unbound (`_agreeing_values`, `:125-140,267-291`).
- **input_output:** bindings + current findings -> `InputFinding`s
- **evaluation_blocking_invalidity_nonpublication:** unbound -> later `DEPENDENCY_ABSENT`, not a marshal crash
- **separately_versioned:** `rounding.convention` is a hardcoded exemption from fact-surface membership (`:1055`)
- **provenance_surviving:** finding id + role `input` or `choice` (`_input_role` uses `finding.basis == "elective"`)
- **schema_search:** not used to decide the construct
- **citations:** `marshal.py:125-140,252-301`; `package_validation.py:1049-1067`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that multiple agreeing findings are ambiguous. They bind using `matches[0]` after the agreement check.

## R53. Production resolver

- **layer:** 4
- **interpreted_forms:** `act.v1` kind `package-adoption` with payload `act-package-adoption.v1`
- **runtime_consumer:** `production_resolver.select_current_adoption` `:134-204`; `resolve_production_package` `:297-377`
- **semantic_effect:** current user adoption (unique max revision, supersession) -> verified release bytes -> verified registry -> verified package checksum -> exclusive member corpus by digest -> `validate_package` hard gate. Failures are `Refusal` values, not exceptions.
- **input_output:** adoption acts + `PublicationSurface` -> `ResolvedGraph` or `Refusal`
- **evaluation_blocking_invalidity_nonpublication:** refusal reasons include `ADOPTION_NONE_CURRENT`, `ADOPTION_AMBIGUOUS`, `RELEASE_ABSENT_OR_MISMATCH`, `HARD_GATE_REFUSED`, …
- **separately_versioned:** payload schema is v1; package schema is whatever the instance names
- **provenance_surviving:** `adoption_act_id` and `release_id` on the graph; runner pins the adoption pin from context
- **schema_search:** `ADOPTION_SCHEMA = "act-package-adoption.v1"`; `RELEASE_SCHEMA = "release-registry.v1"`
- **citations:** `production_resolver.py:38-39,134-204,297-377`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a caller-supplied package path can authorize execution. The module docstring and the function signatures take acts + surface only.

## R54. Closure admission

- **layer:** 4 / 2
- **interpreted_forms:** adopted `source-closure-mapping.v2` + `source-family.v*` + current closure findings + current horizons
- **runtime_consumer:** `source_authority.resolve_closure_admissions` `:100-166`; `validate_mapping_against_family` `:29-62`; `audit_collect_authority` `:183-211`
- **semantic_effect:** content defects (fabricated mapping, pin mismatch, claim/predicate mismatch, narrow-subtotal substitution, duplicate mapping, duplicate declaration) **raise**. Finding-level defects (no horizon, 0 or >1 candidate, value not Python `True`) **omit** the family — so `collect` of an empty set blocks rather than zeroes. `env.closed_sets` is `frozenset(self.admissions)` (`runner.py:290`).
- **input_output:** mappings + declarations + findings + horizons -> `{family_id: ClosureAdmission}`
- **evaluation_blocking_invalidity_nonpublication:** quiet non-admission is the empty-collect block
- **separately_versioned:** mapping and declaration versions are pinned on a closure-backed zero
- **provenance_surviving:** `ClosureAdmission` fields; pins in `pins_for` `:372-386`
- **schema_search:** not used to decide the construct
- **citations:** `source_authority.py:100-166`; `runner.py:175-183,286-290`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a truthy non-bool (e.g. `"true"`) admits. The check is `isinstance(value, bool) and value is True` (`:155-156`).

## R55. Marshal from current findings

- **layer:** 4 / 8
- **interpreted_forms:** `FindingState` + `CurrencyView` + rules/bindings/families
- **runtime_consumer:** `marshal.marshal_run_context` `:210-402`; live fence `marshal_live_run_context` + `production_executor.execute_marshaled`
- **semantic_effect:** only `currency.current_finding_ids`. Collect sources: object values JSON-serialized (`:315`), scalars `str`. Fallback path: unbound current findings whose fact-type id is required by some rule, excluding collect names, with the same agreement guard. Attachment required symbols include requirement subtotals, completeness answers, and branch extras (`:_rule_required_symbols` `:75-108`).
- **input_output:** record state -> `RunContext`
- **evaluation_blocking_invalidity_nonpublication:** disagreement -> leave unbound
- **separately_versioned:** attachment schema list in marshal is the same seven ids as runner (no v7)
- **provenance_surviving:** finding ids on `InputFinding` / `SourceFact`
- **schema_search:** `MarshalledRunContext` seal is Python (`:_MARSHAL_SEAL`)
- **citations:** `marshal.py:29-48,75-108,210-402`; `production_executor.py:11-20`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that live execution can still call `runner.run`. `execute_marshaled` type-checks the seal.

## R56. Collect source-name assembly

- **layer:** 4
- **interpreted_forms:** family member predicates + companion types + `collect_categorical_all_equal` names
- **runtime_consumer:** `live._resolved_run_material` `:88-143`
- **semantic_effect:** `collect_names` starts as every adopted family's `member_predicate.fact_type` (v1 and v2). Companion types from `domain_companion_presence_pairs()` are appended if the subordinate is already a collect name. Then every `collect_categorical_all_equal` `name` in any rule `when`/`value` is appended. Those names are what marshal uses to fill `env.sources`.
- **input_output:** resolved graph -> `collect_source_names`
- **evaluation_blocking_invalidity_nonpublication:** a non-dict pairs return raises `LiveRunError` (`:114-117`)
- **separately_versioned:** no
- **provenance_surviving:** none of its own
- **schema_search:** companion pairs are populated by `packages/tax/loader.py`, which is **outside** Track 0 Layer 3. This stream records that `live.py:112-113` imports that function as the pair source. The kernel enforcement of the pairs is in Layer 3 (`findings.py`).
- **citations:** `live.py:67-86,88-143`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `evaluator.collect` discovers its source names from the expression alone. Marshal must have registered the name first.

## R57. Package admission issue-code family

- **layer:** 4
- **interpreted_forms:** `MemberIssue.code` strings
- **runtime_consumer:** `package_validation.py` (AST enumeration of `MemberIssue` constructors plus the three loop-variable codes and two successor-graph codes)
- **semantic_effect:** 83 distinct issue codes. Full list (verified by `ast` walk plus the `code` loop at `:1263-1267` and `_successor_graphs` at `:1281-1293`):
  `ATTACHMENT_ADJUSTMENT_AUTHORITY_MISMATCH`, `ATTACHMENT_ADJUSTMENT_CLASS_SURFACE_MISMATCH`, `ATTACHMENT_ADJUSTMENT_FAMILY_ABSENT`, `ATTACHMENT_ADJUSTMENT_LABEL_MISMATCH`, `ATTACHMENT_ADJUSTMENT_MEMBER_MISMATCH`, `ATTACHMENT_ADJUSTMENT_SUBTOTAL_MISMATCH`, `ATTACHMENT_ANSWER_EQUALS_NOT_IN_DOMAIN`, `ATTACHMENT_ANSWER_FACT_TYPE_ABSENT`, `ATTACHMENT_ANSWER_NOT_CATEGORICAL`, `ATTACHMENT_COMPOSITION_ABSENT`, `ATTACHMENT_COMPOSITION_BIJECTION_MISMATCH`, `ATTACHMENT_LINE_AUTHORITY_MISMATCH`, `ATTACHMENT_ROW_FAMILY_ABSENT`, `ATTACHMENT_ROW_MEMBER_MISMATCH`, `ATTACHMENT_ROW_SUBTOTAL_MISMATCH`, `ATTACHMENT_SINGLE_FAMILY_BIJECTION_MISMATCH`, `ATTACHMENT_TIE_OUT_OPERATION_INVALID`, `ATTACHMENT_TIE_OUT_SURFACE_MISMATCH`, `BINDING_DEFAULT_ABSENT`, `BINDING_DEFAULT_MISSING`, `BINDING_FACT_TYPE_NOT_ADMITTED`, `CATEGORY_LITERAL_PIN_STALE`, `CITATION_ABSENT`, `CLOSURE_MISSING_PARAMETER`, `COLLECT_TARGET_NOT_FAMILY`, `COMPOSITION_CLOSURE_READS_MISMATCH`, `COMPOSITION_FAMILY_ABSENT`, `COMPOSITION_FAMILY_SUBTOTAL_MISMATCH`, `COMPOSITION_INPUT_PINS_MISMATCH`, `COMPOSITION_MEMBER_MISSING`, `COMPOSITION_PIN_MISMATCH`, `COMPOSITION_PIN_MISSING`, `COMPOSITION_PRODUCER_MISSING`, `COMPOSITION_SLOT_BIJECTION_MISMATCH`, `COMPOSITION_SLOT_DUPLICATE`, `COMPOSITION_VALUE_REFS_MISMATCH`, `CONDITIONAL_DEPENDENCY_MEMBER_FACT_TYPE_ABSENT`, `CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO`, `E14_2_FORBIDDEN_DEPENDENCY`, `ENTRYPOINT_DANGLING`, `ENTRYPOINT_MALFORMED`, `ENTRYPOINT_VERSION_MISMATCH`, `EXCLUSIVITY_COUNTERPART_ABSENT`, `FAMILY_ACCOUNTING_NOT_DECLARED`, `FAMILY_ACCOUNTING_UNREACHED`, `FORCE_DECLARE_COMPOSITION_MISSING`, `FORM_FIELD_BINDING_MISSING`, `FORM_FIELD_PRODUCER_CONFLICT`, `K1_SUCCESSOR_GRAPH_MIXED`, `LINE_1A_8A_PINS_COVERED_W`, `MAPPING_FACT_TYPE_NOT_ADMITTED`, `MD_SUCCESSOR_GRAPH_MIXED`, `MEMBER_ABSENT`, `MEMBER_CHECKSUM_MISMATCH`, `MEMBER_CONSTRAINT_TOO_DEEP`, `MEMBER_SCHEMA_INVALID`, `MEMBER_SCHEMA_UNSUPPORTED`, `MEMBER_UNPUBLISHED`, `MEMBER_UNREACHABLE`, `MIGRATION_FORBIDDEN_PREDECESSOR`, `MIGRATION_PREDECESSOR_SET_INVALID`, `MIGRATION_SUCCESSOR_NOT_ADMITTED`, `MIXED_BOX12_GRAPH`, `MIXED_BOX2A_GRAPH`, `MIXED_BOX7_GRAPH`, `MIXED_LINE2A_GRAPH`, `OUTPUT_OWNERSHIP_CONFLICT`, `PACKAGE_SCHEMA_INVALID`, `QUANTITY_NOT_IN_VOCABULARY`, `QUANTITY_TAG_MISSING`, `QUANTITY_VOCABULARY_ABSENT`, `RAW_BOX12_DOWNSTREAM_READ`, `RAW_BOX2A_DOWNSTREAM_READ`, `RAW_BOX7_DOWNSTREAM_READ`, `RAW_BOX8_DOWNSTREAM_READ`, `RECORDED_NON_COMPOSABLE_INPUT`, `ROLE_MISMATCH`, `SCHEMA_NOT_ADMITTED`, `SCOPE_MISMATCH`, `SUCCESSION_PACKAGE_INCOMPLETE`, `SYNTHESIZED_PREREQUISITE_OMITTED`, `VALIDATION_PRODUCER_AMBIGUOUS`, `VALIDATION_PRODUCER_MISSING`.
- **input_output:** defect -> coded issue
- **evaluation_blocking_invalidity_nonpublication:** any code makes `ok=False`
- **separately_versioned:** codes are unversioned strings
- **provenance_surviving:** `MemberIssue` tuples
- **schema_search:** these codes live in Python. No single schema enum enumerating all 83 was located (searched by not finding `MEMBER_CONSTRAINT_TOO_DEEP` / `FAMILY_VALIDATION_BLOCKED` in schema files; not a proof about every code).
- **citations:** `package_validation.py` as enumerated
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that 83 is a schema-declared closed set

## R58. Tax-hardcoded package kill-tests

- **layer:** 4 / 6
- **interpreted_forms:** Python frozensets and dicts of specific citizen ids
- **runtime_consumer:** `package_validation.py:197-221,826-901,1281-1305,1635-1662,1688-1722`
- **semantic_effect:** examples: `_LINE_1A_8A_NON_CONFUSION_IDS` rejects `covered-w` symbols on two Schedule D rules; mixed historical/successor box graphs (`MIXED_BOX2A_GRAPH` etc.); per-package-version successor-graph tuples for core-calculations `v9`/`v10`; raw box-2a/12/8/7 downstream reads on `income.total-income` / `tax.total-tax`; Schedule 1 succession completeness via imported `MIGRATION_ID` / `PREDECESSOR_IDS` from `packages.tax.schedule1_adjustments_succession` (that module is outside Layer 3; the *call* is in Layer 3).
- **input_output:** resolved members -> issues
- **evaluation_blocking_invalidity_nonpublication:** admission
- **separately_versioned:** keyed on content ids and package instance versions
- **provenance_surviving:** issue rows
- **schema_search:** no schema located for these id lists
- **citations:** `package_validation.py:197-206,1635-1662`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that these are generic package-language rules. The control flow names tax citizen ids.

## R59. Quantity-vocabulary check vs supported set

- **layer:** 4
- **interpreted_forms:** fact-type `quantity` pins vs package quantity-vocabulary members
- **runtime_consumer:** `package_validation.py:1082-1132`
- **semantic_effect:** the quantity-vocabulary **index** is built only from `quantity-vocabulary.v1`, `.v2`, `.v3` (`:1085-1090`). `_SUPPORTED_SEMANTIC_SCHEMAS` also lists `.v4`–`.v12`. A v4+ vocabulary member is admitted (role-checked as `parameter` only if schema is v1–v3 at `:942-951` — v4+ fall through the role if-ladder without a quantity-vocabulary role check).
- **input_output:** fact quantities -> issues
- **evaluation_blocking_invalidity_nonpublication:** admission
- **separately_versioned:** yes, and the two version lists differ
- **provenance_surviving:** issue rows
- **schema_search:** not used to decide the construct
- **citations:** `package_validation.py:246-282,942-951,1085-1104`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that v4–v12 vocabularies are quantity-checked. The index loop does not include them.

---

# Surface 5a — Attachment-rule / form-field

## R60. Attachment threshold requirement

- **layer:** 5a
- **interpreted_forms:** `requirement` without `kind == "family_nonempty"`: `subtotals[]`, `threshold_parameter`, `citation`
- **runtime_consumer:** `runner.attempt_attachment` `:883-923`
- **semantic_effect:** missing subtotal or parameter -> `DEPENDENCY_ABSENT`. Required iff **any** subtotal `> threshold` (strict `>`). Each trigger is recorded `{subtotal, value, over}`. Not required -> `inapplicable` with `guard_result: False`.
- **input_output:** symbols + parameter -> required bool
- **evaluation_blocking_invalidity_nonpublication:** not-required is inapplicable, not blocked
- **separately_versioned:** shared across attachment-rule.v1..v6,v8
- **provenance_surviving:** base pins of subtotals, parameter, citation, adoption, governance
- **schema_search:** not used to decide the construct
- **citations:** `runner.py:883-923`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that equality with the threshold is required. The test is `>`.

## R61. Attachment `family_nonempty` requirement

- **layer:** 5a
- **interpreted_forms:** `requirement.kind == "family_nonempty"` with `source_family.id` and `citation`
- **runtime_consumer:** `runner._attachment_family_nonempty_trigger` `:574-626`
- **semantic_effect:** unadmitted family -> `DEPENDENCY_ABSENT` (blocked, not a silent default). Admitted: required iff `len(member_values) > 0`. Closed-empty is not-required (inapplicable).
- **input_output:** family id -> required bool
- **evaluation_blocking_invalidity_nonpublication:** unclosed/unadmitted -> blocked
- **separately_versioned:** comment names ADR-0053; control flow is schema-agnostic once `kind` matches
- **provenance_surviving:** mapping, declaration, closure finding, citation, adoption, governance
- **schema_search:** not used to decide the construct
- **citations:** `runner.py:574-626,877-882`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R62. Completeness: presence then value

- **layer:** 5a
- **interpreted_forms:** `completeness.required_answers[]` with optional `check: "value"` and `equals`
- **runtime_consumer:** `runner.attempt_attachment` `:951-1011`
- **semantic_effect:** every required (and triggered extra) symbol is presence-checked first, independently. Missing -> `DEPENDENCY_ABSENT` naming every missing symbol. Then, for `check == "value"`, `_value_str(symbol) != equals` -> `COMPLETENESS_VALUE_VIOLATION` naming `symbol=actual` strings. One pass names every currently violated answer.
- **input_output:** answer specs -> complete or block
- **evaluation_blocking_invalidity_nonpublication:** presence and value are distinct codes
- **separately_versioned:** `COMPLETENESS_VALUE_VIOLATION` is a runner constant (`:147`)
- **provenance_surviving:** pins of present answers even on a presence-block
- **schema_search:** `COMPLETENESS_VALUE_VIOLATION` appears in `derivation-record.v4` and later, and in `npe-walk.v3` (grep)
- **citations:** `runner.py:951-1011`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a value mismatch is `DEPENDENCY_ABSENT`

## R63. `branch_requirements`

- **layer:** 5a
- **interpreted_forms:** `completeness.branch_requirements[]` with `when_answer.{symbol,equals}`, `adds_required`, `names_obligations`
- **runtime_consumer:** `runner.py:957-980`
- **semantic_effect:** if the trigger symbol is absent, the branch is skipped (the trigger is already in `missing_answers` if it was required). If present and `str(value) == equals`, extra answers become required and obligations are recorded onto the published value as `named_obligations`.
- **input_output:** branches -> extra required symbols + obligation list
- **evaluation_blocking_invalidity_nonpublication:** a skipped branch cannot invent extra missing answers
- **separately_versioned:** `.get("branch_requirements", [])` — absent field is empty
- **provenance_surviving:** `named_obligations` on the published attachment value (`:1121-1127`)
- **schema_search:** not used to decide the construct
- **citations:** `runner.py:957-980,1121-1127`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a false trigger still adds extras

## R64. Itemization and tie-out

- **layer:** 5a
- **interpreted_forms:** `itemizations[].row_sets[].rows.{member_fact_type, source_family}` + `tie_out.line_symbol`; v1 uses `part["rows"]` instead of `row_sets`
- **runtime_consumer:** `runner.attempt_attachment` `:1022-1119`; admission joins in `package_validation.py:1764-1828`
- **semantic_effect:** rows are `env.sources` / `source_fids` for the member fact type. `row_sum` must equal the named subtotal symbol; `part_sum` must equal the line symbol. Mismatch -> `ITEMIZATION_TIE_OUT_VIOLATION` with `part:family:symbol` / `part:line` strings. v1 emits a legacy itemization shape; v2+ emits `row_sets`.
- **input_output:** parts -> value + pins or block
- **evaluation_blocking_invalidity_nonpublication:** tie-out is checked only after completeness holds (control-flow order in `attempt_attachment`)
- **separately_versioned:** v1 vs v2+ shapes
- **provenance_surviving:** row pins `role=input` with v2 `origin=assertion`
- **schema_search:** `ITEMIZATION_TIE_OUT_VIOLATION` is in derivation-record enums (grep)
- **citations:** `runner.py:1022-1119`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R65. v6/v8 `adjustment_rows`

- **layer:** 5a
- **interpreted_forms:** `adjustment_rows[]` with `kind`, `label`, `sign`, `rows`, `subtotal_symbol`; tie-out `positive_subtotals`, `adjustment_subtotals`, `operation`
- **runtime_consumer:** `runner.py:1052-1092`; admission `package_validation.py:1830-1944`
- **semantic_effect:** each adjustment row-sum is subtracted from `part_sum` (`:1089`). Negative member values or row-sum ≠ subtotal -> tie-out violation. Admission requires `operation == "subtract"`, surface lists to match, and for known kinds in `_V3_ADJUSTMENT_BINDINGS` a label/family-token match. One subtractive-positive-basis exception allows line symbol `interest.taxable-total` against composition `interest.positive-total` (`:1819-1827`). The v8 copy of that exception at `:1935-1941` checks `citizen["schema"] == "attachment-rule.v6"` only — **v8 does not take that exception in the 10c loop**.
- **input_output:** adjustment rows -> signed sums in the published value
- **evaluation_blocking_invalidity_nonpublication:** admission + runtime tie-out
- **separately_versioned:** `_V6_SHAPE_ATTACHMENT_SCHEMAS = {v6, v8}` (`runner.py:142`)
- **provenance_surviving:** adjustment row finding ids
- **schema_search:** not used to decide the construct
- **citations:** `runner.py:142,1052-1092`; `package_validation.py:1819-1827,1934-1944`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that the 10b and 10c subtractive exceptions treat v8 identically. 10b includes v8 (`:1820`); 10c's exception is v6-only (`:1936`).

## R66. Form-field bind and presentation join

- **layer:** 5a / 7
- **interpreted_forms:** `form-field.vN` `binds_symbol` + `dispositions.published_value.render`
- **runtime_consumer:** admission `package_validation.py:1069-1080`; presentation `presentation_projection.py:37,211-264,448-466`
- **semantic_effect:** admission: `binds_symbol` must be produced or input-bound. Presentation: only `form-field.v2` and `.v3` are `FIELD_SCHEMAS`. A field row joins the unique disposition for that symbol. `render == "{value}"` is numeric (R83); any other render string must **equal** the finding value and becomes `published_categorical` with the source value **not** copied to the model (`:242-246`).
- **input_output:** field citizen + dispositions -> section row
- **evaluation_blocking_invalidity_nonpublication:** unknown / ambiguous join raises `PresentationModelError` (fail closed), not a derivation block
- **separately_versioned:** v1 is in `_SUPPORTED_SEMANTIC_SCHEMAS` and in admission form-field role checks; it is not in `FIELD_SCHEMAS`
- **provenance_surviving:** citation sites from dependency pins
- **schema_search:** `PRESENTATION_MODEL_VERSION = "presentation-model.v1"` (`presentation_projection.py:30`). Grep of `*.schema.json` for `presentation-model` returned no hits.
- **citations:** `presentation_projection.py:30-48,211-264`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that presentation invents a display value. Numeric values are parsed from the published finding; categorical values are replaced by the field's declared instruction.

## R67. Attachment compiled `.member-validation` gate

- **layer:** 5a / 4
- **interpreted_forms:** `requires` entries ending in `.member-validation` on an attachment citizen after compile
- **runtime_consumer:** `runner._requires` `:440-442`; `finalize_unreached` `:1194-1208`
- **semantic_effect:** those symbols gate attachment eligibility the same as ordinary requires, even though `attempt_attachment` itself never reads `requires`.
- **input_output:** compiled requires -> eligibility
- **evaluation_blocking_invalidity_nonpublication:** missing compiled prereq in finalize -> `_attachment_block(DEPENDENCY_ABSENT)`
- **separately_versioned:** post-compile, not a schema field
- **provenance_surviving:** missing list
- **schema_search:** the runner comment at `:432-439` says the attachment-rule schema does not declare `requires`. This stream treats that as a comment; the control flow reads `rule.get("requires", [])`.
- **citations:** `runner.py:440-442,1194-1208`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

---

# Surface 5b — Term / predicate language and depth bound

## R68. Term language

- **layer:** 5b-i
- **interpreted_forms:** `TERM_OPS = {field, literal, add, subtract, floor_zero}` (`declarative_validation.py:6`)
- **runtime_consumer:** `Evaluator.evaluate_term` `:61-84`
- **semantic_effect:**
  - `literal`: `_dec(arg)`
  - `field`: `member[field]`, or `default` if absent, else `GrammarError`
  - `add` / `subtract`: recurse `depth+1` on left/right
  - `floor_zero`: `max(inner, 0)`
  - unknown op: `GrammarError` ("the grammar is closed")
  - bool numeric: `GrammarError` (not `EvalBlocked`)
  - `float` is accepted by `_dec` (`:43-44`) unlike evaluator `_as_decimal`'s bool-only special case
- **input_output:** term + member -> `Decimal`
- **evaluation_blocking_invalidity_nonpublication:** `GrammarError` / `MemberConstraintTooDeep` become `CONSTRAINT_EVALUATION_FAILED` at `runner.py:696-702`
- **separately_versioned:** no runtime version switch; Track 0 places the schema in `source-family.v2`
- **provenance_surviving:** family-validation member findings list violations
- **schema_search:** Track 0 locates `$defs/term` on `source-family.v2`. This stream did not re-read that schema to decide the construct exists; the ops are the Python frozenset.
- **citations:** `declarative_validation.py:6,36-84`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that this is the same `add` as evaluator R7. Different module, different depth, different error type, no `_flatten`.

## R69. Predicate language

- **layer:** 5b-i
- **interpreted_forms:** `PREDICATE_OPS = {field_present, field_absent, field_equals, field_not_equals, compare, all, any}` (`:7-10`); `COMPARISONS` gt/ge/lt/le/eq/ne (`:11-18`)
- **runtime_consumer:** `Evaluator.evaluate_predicate` `:86-113`; `evaluate_member` `:115-122`
- **semantic_effect:**
  - `field_present` / `field_absent`: key in / not in member
  - `field_equals`: `_value_equals(member.get(field, _ABSENT), arg)` — absent field is not equal (unless arg were `_ABSENT`, which it is not)
  - `field_not_equals`: absent field is **False** (does not fire). Present and unequal is True.
  - `compare`: unknown comparison -> `GrammarError`; otherwise term compare at `depth+1`
  - `all` / `any`: Python `all`/`any` over args at `depth+1` (short-circuit, same as R13)
  - a constraint fires when `violated_when` is **true**
- **input_output:** predicate + member -> `bool`; constraints -> `list[Violation]`
- **evaluation_blocking_invalidity_nonpublication:** fired constraints contribute `block_code` strings to `FAMILY_VALIDATION_BLOCKED`'s missing list
- **separately_versioned:** no
- **provenance_surviving:** `Violation(constraint_id, block_code, meaning)`
- **schema_search:** Track 0 locates `$defs/predicate` on `source-family.v2`. Ops taken from the Python frozenset.
- **citations:** `declarative_validation.py:7-18,47-59,86-122`. Synthetic: `field_equals` on absent -> `False`; `field_not_equals` on absent -> `False`; `field` with `default: 7` -> `Decimal(7)`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `field_not_equals` is true when the field is missing. It is false.

## R70. `MAX_PREDICATE_DEPTH = 6` (two literals, two algorithms)

- **layer:** 5b-ii
- **interpreted_forms:** integer `6` in two modules; evaluator raises `MemberConstraintTooDeep`; admission emits `MEMBER_CONSTRAINT_TOO_DEEP`
- **runtime_consumer:** `declarative_validation.py:20,62,87`; `package_validation.py:182-188,2037,2050-2056`
- **semantic_effect:** **The two depth functions are not the same.**
  - Evaluator: every nested `add`/`subtract`/`floor_zero`/`compare`/`all`/`any` increments `depth`. Starting depth is 1. A `compare` of a chain of 5 `add`s is too deep (`n_adds=5` -> `TOO_DEEP`).
  - Admission `_predicate_depth`: `1 + max(depth(args))` if `args` is a nonempty list, else `1`. It does **not** walk `left`/`right`/`value`. The same `compare(add^n)` tree has admission depth **1** for every `n`.
- **input_output:** tree -> accept or reject
- **evaluation_blocking_invalidity_nonpublication:** a package can admit a constraint the evaluator then refuses at run with `CONSTRAINT_EVALUATION_FAILED` / `MemberConstraintTooDeep`
- **separately_versioned:** two independent literals; nothing ties them (Track 0 gap 8)
- **provenance_surviving:** admission issue vs run block
- **schema_search:** Track 0 already recorded that JSON Schema is not claimed to enforce recursive depth. Confirmed: no schema hit for `MAX_PREDICATE_DEPTH` / `MEMBER_CONSTRAINT_TOO_DEEP`.
- **citations:** `declarative_validation.py:20,62,87`; `package_validation.py:182-188,2037-2056`. Synthetic: `n_adds=0..4` eval ok, admission_depth=1; `n_adds>=5` eval `TOO_DEEP`, admission_depth still 1.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that admission and evaluation enforce the same trees. They do not.

## R71. Identity exclusivity

- **layer:** 5b
- **interpreted_forms:** `identity_exclusivity[]` with `incompatible_family.id` and `components[]` of `fact_id_bound_key` or `member_field`
- **runtime_consumer:** `declarative_validation.identity_tuple` `:164-173`; `runner._evaluate_family_validation` `:738-792`; admission counterpart check `:2057-2064`
- **semantic_effect:** collision only across this family's current members and the named incompatible family's current members (not within one family). Missing component -> `IDENTITY_COMPONENT_MISSING`. Collision -> `IDENTITY_EXCLUSIVITY_COLLISION`. Absent counterpart declaration -> `IDENTITY_EXCLUSIVITY_FAMILY_ABSENT`. `extract_bound_keys` parses `fact_id` suffix after `|` as `k=v` pairs (`:128-139`), the same rendering `facts._fact_id` writes (`facts.py:235-237`).
- **input_output:** two member sets + components -> codes
- **evaluation_blocking_invalidity_nonpublication:** any such code contributes to `FAMILY_VALIDATION_BLOCKED`
- **separately_versioned:** no
- **provenance_surviving:** codes on the family-validation block
- **schema_search:** not used to decide the construct
- **citations:** `declarative_validation.py:128-173`; `runner.py:738-792`. Synthetic: `type|payer=p1,year=2025` + `{box:1}` with components payer + box -> `('p1','1')`.
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a malformed `k=v` part with no `=` errors. `extract_bound_keys` skips such parts (`:135-136`).

---

# Surface 6 — Runtime behaviors adjacent to grammar

## R72. Subset invariants

- **layer:** 6i
- **interpreted_forms:** `registry.subset_invariant_pairs: dict[str,str]` empty by default
- **runtime_consumer:** `schema_registry.py:91-96`; `findings._enforce_subset_invariants` `:221-275`; applied on assertion and member-transition
- **semantic_effect:** for each touched fact, if its type is subordinate or dominant in a pair, compare current values sharing the `|suffix`. Subordinate current and dominant absent -> `FindingModelError`. Subordinate `>` dominant -> `FindingModelError`. Enforcement is generic over the suffix; the registry is populated by a tax-layer loader (outside Layer 3).
- **input_output:** finding admission -> accept or raise (never recorded)
- **evaluation_blocking_invalidity_nonpublication:** reject-not-record at kernel admission, not a derivation block
- **separately_versioned:** no citizen; Python attributes
- **provenance_surviving:** none — the violating finding never enters state
- **schema_search:** no schema located for the pair map (Track 0 already classified 6i adjacent on this ground)
- **citations:** `schema_registry.py:91-96`; `findings.py:221-275,620-624`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that the kernel names box 1b/1a. The example is in a comment; the code compares whatever pairs the registry holds.

## R73. Companion presence, value domains, equality

- **layer:** 6i
- **interpreted_forms:** `companion_presence_pairs`, `companion_value_domains`, `companion_equality_pairs`
- **runtime_consumer:** `findings.py:296-405`; runner pin matching `runner.py:322-369`; live collect-name extras `live.py:108-131`
- **semantic_effect:** presence: current subordinate without current companion -> `FindingModelError`; optional value-domain restriction on the companion. Equality: both current and unequal -> `FindingModelError`; one missing is left to presence. Runner: collecting a subordinate with a declared companion **requires** a same-suffix companion source to pin, else `SourceAuthorityError` (run stop, not a contained rule block).
- **input_output:** admission / pin assembly
- **evaluation_blocking_invalidity_nonpublication:** kernel reject-not-record; runner fail-closed on missing companion pin
- **separately_versioned:** no
- **provenance_surviving:** companion input pins on the derived finding (displacement edges, R81)
- **schema_search:** no schema located for the maps
- **citations:** `findings.py:296-405`; `runner.py:322-369`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that companion equality is a derivation pin concern. The findings docstring says it is a source-admission invariant (`:367-371`); the runner separately pins companions for displacement.

## R74. Declaration/signal contradictions

- **layer:** 6i
- **interpreted_forms:** `registry.declaration_signal_contradictions` list of dicts
- **runtime_consumer:** `findings._enforce_declaration_signal_contradictions` `:433-487`
- **semantic_effect:** if the declaration fact type currently holds `declaration_value` and any current signal finding raises the signal (named field non-null, or, if `signal_field` is absent, any non-null amount), raise `FindingModelError`. Bidirectional in the sense that touching either type rechecks.
- **input_output:** admission -> reject or accept
- **evaluation_blocking_invalidity_nonpublication:** reject-not-record
- **separately_versioned:** no
- **provenance_surviving:** none
- **schema_search:** no schema located for the rule list
- **citations:** `findings.py:433-487`; `schema_registry.py:97-106`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R75. Displacement closure

- **layer:** 6ii
- **interpreted_forms:** `DECLARED_EDGE_KINDS = frozenset({"derivation","individuation"})` (`currency.py:16`)
- **runtime_consumer:** `currency.displacement_closure` `:45-67`; `compute_currency` `:168-210`; derivation fold `projection.py:66-80`
- **semantic_effect:** walk only those two edge kinds from roots. Roots themselves include correction, withdrawal, migration supersession, and superseded entities — reason kinds `correction` / `withdrawal` / `supersession` are **not** edge kinds. Derived findings: `projection.derivation_edges` builds `derivation` edges from pins with role `input` or `choice` only (`projection.py:32,44-57`). Parameter / operation-semantics / adoption / governance pins are not displacement edges.
- **input_output:** state -> `CurrencyView`
- **evaluation_blocking_invalidity_nonpublication:** displaced findings are omitted by marshal (indistinguishable from absent)
- **separately_versioned:** no
- **provenance_surviving:** `DisplacementReason` tuples
- **schema_search:** no schema located for `DECLARED_EDGE_KINDS` (Track 0 already said this)
- **citations:** `currency.py:16,45-67,168-210`; `projection.py:32-80`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a stored `current` flag is authority. `compute_currency` recomputes; `assert_materialization_matches` exists to catch stale flags (`currency.py:213-234`).

## R76. Presentation numeric kinds

- **layer:** 6 / 7
- **interpreted_forms:** `published_value` / `computed_zero` / `closure_backed_zero`
- **runtime_consumer:** `presentation_projection._classify_numeric` `:177-188`
- **semantic_effect:** nonzero -> `published_value` citing source leaves. Zero with source leaves -> `computed_zero`. Zero with only closure leaves -> `closure_backed_zero` and **drops citation leaves**. Zero with neither -> `PresentationModelError`. Closure findings are detected by `".source-closure"` in the finding id (`:_CLOSURE_FACT_MARKER` `:50,122-123`).
- **input_output:** value + leaves -> kind
- **evaluation_blocking_invalidity_nonpublication:** construction error, not a derivation block
- **separately_versioned:** `presentation-model.v1` (R77)
- **provenance_surviving:** citation sites except on closure-backed zero
- **schema_search:** kinds are Python frozensets (`:42-48`)
- **citations:** `presentation_projection.py:42-50,177-188`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that a closure-backed zero still cites the closure finding. Citation leaves are `set()`.

## R77. `presentation-model.v1` (no published schema located)

- **layer:** 7
- **interpreted_forms:** the dict `build_presentation_model` returns; validated by `validate_presentation_model` in the same file
- **runtime_consumer:** `presentation_projection.py:30,448+,598+`
- **semantic_effect:** internal projector shape. Module docstring states it is not a published schema or caller-facing contract. Attachments always emit a status entry for blocked / guard_inapplicable / published (`_resolve_attachment`).
- **input_output:** run artifacts -> model dict
- **evaluation_blocking_invalidity_nonpublication:** fail closed on join errors
- **separately_versioned:** a Python string `"presentation-model.v1"`
- **provenance_surviving:** citation groups + attachment statuses
- **schema_search:** grep of `*.schema.json` for `presentation-model` returned no matches.
- **citations:** `presentation_projection.py:1-19,30,309-445`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that this model is a grammar-proper citizen. Track 0 told this stream to expect thinner grammar here; the control flow consumes dispositions, it does not evaluate expressions.

---

# Surface 7 — Provenance, disposition, explanation records

## R78. `npe-walk.v3` walker

- **layer:** 7
- **interpreted_forms:** walk payload with `node_kind` in `{published, blocked, guard_inapplicable, no_disposition_recorded}`
- **runtime_consumer:** `explanation.walk_npe` `:152-337`; `explain` `:49-120`
- **semantic_effect:** hardcodes `"schema": "npe-walk.v3"` at `:332`. Prefers a published ledger row, else a derived-publication act, else blocked/inapplicable ledger rows, else `no_disposition_recorded` with `closing_phase`. Blocked code is the first row/blocked-entry code found — after R35 remapping. Cycles raise `CyclicDependencyError`. `explain` treats rule roles as `produced_by` and `input`/`choice` as recursive children.
- **input_output:** run_id + symbol + records -> walk dict
- **evaluation_blocking_invalidity_nonpublication:** this records them; it does not re-evaluate
- **separately_versioned:** target schema is a hardcoded v3, not `validate_declared` of whatever is current
- **provenance_surviving:** the walk *is* the explanation record
- **schema_search:** `npe-walk.v3.schema.json` exists (Track 0 corpus). The walker does not call `validate_declared` on its result in the code that was read.
- **citations:** `explanation.py:152-337`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that the walker emits `LOOKUP_MISS`. After R35, a lookup miss on v2 is ledger `DEPENDENCY_INVALID`.

## R79. Derivation-record pairing and current schema

- **layer:** 7
- **interpreted_forms:** `started` then one of `completed` / `interrupted` / `failed`; `CURRENT_RECORD_SCHEMA = "derivation-record.v7"`
- **runtime_consumer:** `records.py:40-50,121-135,168-218,221-248`
- **semantic_effect:** append-only JSONL, newline is commit, pairing is checked. Adoption gate: `adoption_pin["id"]` must be in `adopted_packages` or `AdoptionError` before start is written. `use_v2=False` writes `derivation-record.v1` and includes `published`/`blocked` arrays; `use_v2=True` writes v7 and omits those arrays (`:215-217`).
- **input_output:** records -> stream
- **evaluation_blocking_invalidity_nonpublication:** a mis-paired committed line is `RecordStreamCorruption` (read halt)
- **separately_versioned:** v1 vs v7 selected by a misnamed flag; `_VERSIONED_RECORD_SCHEMAS` is v2–v7 for recovery (`:41-50`)
- **provenance_surviving:** the stream
- **schema_search:** `CURRENT_RECORD_SCHEMA` is the one place Track 0 accepted as a real current-version designation. Confirmed at `records.py:40`.
- **citations:** `records.py:32-50,168-218`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that v2 in the flag name is v2 of the schema

## R80. Pin construction

- **layer:** 7
- **interpreted_forms:** `{role, id, version}` plus optional `origin`
- **runtime_consumer:** `runner.pins_for` `:297-400`
- **semantic_effect:** producing rule pin; present refs; collected inputs; companion inputs (fail closed); parameters/tables; closure-backed-zero mapping/declaration/closure-finding; operation-semantics for `access.operations`; `rule["citations"]`; adoption; governance. Deduped by `(role,id,version)` sort key.
- **input_output:** AccessLog + rule -> pin list
- **evaluation_blocking_invalidity_nonpublication:** missing companion -> `SourceAuthorityError` (run abort)
- **separately_versioned:** `origin` only if `use_v2`
- **provenance_surviving:** copied onto the derived finding
- **schema_search:** pin shape is written by this function; finding schemas are validated after assembly
- **citations:** `runner.py:297-400`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that citation pins come from the AccessLog. They come from `rule.get("citations", [])`.

## R81. Content-addressed ids

- **layer:** 7
- **interpreted_forms:** `prefix + sha256(canonical JSON)[:24]`
- **runtime_consumer:** `runner._content_id` `:157-158`
- **semantic_effect:** finding ids and publication act ids are functions of canonical payload. Re-run with the same pins/value yields the same ids. Scheduler order that *changes which producer wins* still changes the payload.
- **input_output:** payload -> id
- **evaluation_blocking_invalidity_nonpublication:** none
- **separately_versioned:** no
- **provenance_surviving:** the id
- **schema_search:** no schema located for the hash prefix convention
- **citations:** `runner.py:153-158,520-528`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R82. Ledger pin exclusion

- **layer:** 7
- **interpreted_forms:** v2 disposition `pins` minus roles in `{computation, applicability, field-mapping, cross-form-bridge}`
- **runtime_consumer:** `runner.ledger_pins_for` `:402-407`
- **semantic_effect:** the finding still carries the producing-rule pin; the derivation-record disposition does not.
- **input_output:** full pins -> filtered pins
- **evaluation_blocking_invalidity_nonpublication:** none
- **separately_versioned:** v2 only
- **provenance_surviving:** split across finding vs ledger
- **schema_search:** not used to decide the construct
- **citations:** `runner.py:128-130,402-407`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that explanation walking uses ledger pins. `explain` walks the **finding's** pins.

---

# Surface 8 — Kernel act / fact / entity / horizon substrate (grammar-adjacent; required to answer input/output domains)

## R83. Fact-id rendering

- **layer:** 8
- **interpreted_forms:** `{fact_type_id}|{k=v,k=v,…}`
- **runtime_consumer:** `facts._fact_id` `:235-237`; parsed by `marshal._fact_keys`, `declarative_validation.extract_bound_keys`, `findings` suffix logic
- **semantic_effect:** identity of a fact. Marshal matches collect sources by type prefix. Subset/companion invariants treat the suffix as "the same statement".
- **input_output:** type + keys -> id string
- **evaluation_blocking_invalidity_nonpublication:** a collectable without `|` cannot satisfy companion pin matching (`runner.py:337-341`)
- **separately_versioned:** no
- **provenance_surviving:** `SourceFact.fact_id`
- **schema_search:** the renderer is Python; fact-type identity_keys are schema-typed citizens
- **citations:** `facts.py:235-248`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R84. Family-horizon succession

- **layer:** 8 / 4
- **interpreted_forms:** `family-horizon.v1`; entity kind `kernel.family-horizon`
- **runtime_consumer:** `horizons.py`; `findings.apply_horizon_genesis` / `apply_member_transition`; marshal `current_horizons`
- **semantic_effect:** one current horizon per `(family id, family version, scope)`. Marshal errors if a family has chains in multiple scopes (`marshal.py:201-205`). Closure admission requires the closure finding's horizon to be that current id.
- **input_output:** horizon acts -> `current_by_chain`
- **evaluation_blocking_invalidity_nonpublication:** a finding keyed on a superseded horizon is not admitted (quiet)
- **separately_versioned:** horizon citizen is v1; family version is a chain-key component
- **provenance_surviving:** horizon id on `ClosureAdmission`; a v2 family-validation success also pins the horizon as `role=input` (`runner.py:803-808`)
- **schema_search:** `HORIZON_SCHEMA = "family-horizon.v1"`
- **citations:** `horizons.py:25-67`; `marshal.py:197-207`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R85. Member-transition vs assertion routing

- **layer:** 8
- **interpreted_forms:** act kinds `assertion` vs `member-transition`
- **runtime_consumer:** `findings.apply_assertion` `:595-615`; `apply_member_transition` `:707-774`
- **semantic_effect:** a fact type in `registry.family_member_predicates` cannot be newly asserted; it must enter via member-transition (SC-R1). A member-transition asserting a fact already in the family is rejected (SC-R2); same-member correction belongs on assertion. `family_member_predicates` is an empty set on `SchemaRegistry` unless a loader fills it (`schema_registry.py:90`).
- **input_output:** act -> state or `FindingModelError`
- **evaluation_blocking_invalidity_nonpublication:** reject-not-record
- **separately_versioned:** no
- **provenance_surviving:** none on rejection
- **schema_search:** no schema located for `family_member_predicates`
- **citations:** `findings.py:595-615,730-741`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R86. Supersession policy

- **layer:** 8
- **interpreted_forms:** fact-type `supersession.policy` in `{free, locked, closed-on-attestation}` as interpreted by `_validate_finding`
- **runtime_consumer:** `findings.py:560-580,164-218`
- **semantic_effect:** if a fact already has any finding: `free` allows correction; `locked` rejects; `closed-on-attestation` rejects only when the projected gate fact is currently `True`. Gate identity keys must all be present on the gated fact or the configuration itself is a `FindingModelError`.
- **input_output:** finding + fact type -> accept or reject
- **evaluation_blocking_invalidity_nonpublication:** reject-not-record
- **separately_versioned:** policy lives on the fact-type citizen
- **provenance_surviving:** none on rejection
- **schema_search:** not used to decide the construct
- **citations:** `findings.py:164-218,560-580`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that `closed-on-attestation` reads the gate as a derivation symbol. It projects a fact id and uses `_current_value_for_fact`.

## R87. `SchemaRegistry.validate_declared`

- **layer:** 4 / 7 / 8
- **interpreted_forms:** instance field `schema` selects the validator
- **runtime_consumer:** `schema_registry.py:234-244`; used by loader, package validation, runner finding assembly, record append
- **semantic_effect:** no declared schema -> `SchemaValidationError("<undeclared>")`. Validation is strict, no coercion. Checksum manifest makes a mutated published file a registry defect.
- **input_output:** instance -> schema id or error
- **evaluation_blocking_invalidity_nonpublication:** invalid instance does not run / does not append
- **separately_versioned:** the instance names the version; there is no registry-level "current" (Track 0)
- **provenance_surviving:** none of its own
- **schema_search:** this *is* the schema gate
- **citations:** `schema_registry.py:128-151,190-244`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that dropping `$id` in the in-memory validator (`:172-175`) changes published bytes. Published bytes are checksummed before that drop.

## R88. Migration-artifact retirement

- **layer:** 8 / 4
- **interpreted_forms:** `migration-artifact.v1` adopted as act kind `migration-adoption`
- **runtime_consumer:** `facts.apply_migration_adoption` `:165-224`; `findings.apply_migration_adoption` `:817-831`; package succession checks `:826-901`
- **semantic_effect:** named predecessor fact types leave `fact_types` and become `retired_fact_type_ids`; currency treats findings of those types as supersession roots (`currency.py:137-166`). Presented successor claims are built, not written as findings. Package validation additionally hard-codes one succession triple for Schedule 1.
- **input_output:** migration citizen -> retired types + claims
- **evaluation_blocking_invalidity_nonpublication:** duplicate adopt / overlap / missing successor -> `FactModelError`
- **separately_versioned:** citizen `migration-artifact.v1`
- **provenance_surviving:** `retired_by` tuples; presented claims
- **schema_search:** `validate_declared` on the migration citizen
- **citations:** `facts.py:165-224`; `currency.py:137-166`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R89. Kernel compose-over of act kinds

- **layer:** 8
- **interpreted_forms:** `KERNEL_ACT_KINDS`; other kinds (including `derived-publication`) are passed over
- **runtime_consumer:** `findings.apply_act` `:855-867`; `projection.derived_findings_from_acts` reads `kind == "derived-publication"`
- **semantic_effect:** one act log, two projectors. Kernel does not interpret derived findings; derivation currency folds them separately.
- **input_output:** acts -> `FindingState` (kernel) plus derived index
- **evaluation_blocking_invalidity_nonpublication:** unknown-to-kernel kind is not an error
- **separately_versioned:** no
- **provenance_surviving:** both projections
- **schema_search:** act envelopes are `act.v1`
- **citations:** `findings.py:846-867`; `projection.py:35-41`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** none

## R90. Surface artifact resolver (non-interpreter)

- **layer:** 4 (effects)
- **interpreted_forms:** `surface-adoption` acts; `surface-artifact.v1` manifest `entries` checked by SHA-256
- **runtime_consumer:** `surface_resolver.resolve_surface_artifact` `:83+`
- **semantic_effect:** reuses `select_current_adoption` with `expected_kind="surface-adoption"` so surface and package adoptions cannot tie. Entries are never parsed as grammar.
- **input_output:** acts + surface -> `ResolvedSurface` or `Refusal`
- **evaluation_blocking_invalidity_nonpublication:** refusal
- **separately_versioned:** `SURFACE_SCHEMA = "surface-artifact.v1"`
- **provenance_surviving:** adoption act id
- **schema_search:** entries are raw files; no grammar schema
- **citations:** `surface_resolver.py:55-56,83-100`
- **status:** pending-reconciliation
- **nearby_inferences_not_supported:** that this resolver interprets rule-artifact expressions. It does not.

---

# Synthetic executions

All run against the source-ref tree with `python3` importing the modules named. No personal data. No absolute paths in the outputs below.

### Evaluator dispatch (23 ops)

`inspect.getsource(evaluate)` if-op chain, in order:

`ref, collect, count, block, parameter, add, subtract, multiply, divide, max, compare, all, any, not, choose, round, range_lookup, bracket_fold, require_closed, categorical_compare, category_literal, collect_categorical_all_equal, conditional_dependency_set`

`loader.OPERATION_VOCABULARY` is the 14-name set without the nine extra ops listed in R1.

### Collect vs count vs categorical-collect (R3, R4, R23)

```
collect empty unclosed     -> SOURCE_SET_UNCLOSED missing ['x'] closure_reads set()
collect empty closed       -> [] closure_reads {'fam'}
collect nonempty unclosed  -> [Decimal('1'), Decimal('2')] closure_reads set()
count nonempty unclosed    -> SOURCE_SET_UNCLOSED missing ['fam']
count nonempty closed      -> 2 closure_reads {'fam'}
collect_categorical empty  -> DEPENDENCY_ABSENT missing ['w']
```

### Divide, unknown op, bool, empty add/max (R10, R26, R28, R7, R11)

```
divide 1/0                 -> DEPENDENCY_INVALID ['division by zero']
{"op":"nope"}              -> DEPENDENCY_INVALID ['unknown op survived schema: nope']
add of True                -> DEPENDENCY_INVALID ['expected number, got boolean True']
add of []                  -> Decimal('0')
max of []                  -> ValueError: max() iterable argument is empty
```

### `all` short-circuit and CDS (R13, R24)

```
all([False, ref missing])  -> False, refs set()
all([True, ref missing])   -> DEPENDENCY_ABSENT ['missing'], refs {'missing'}
CDS condition False        -> True, refs set()
CDS condition True, two missing refs -> DEPENDENCY_ABSENT ['a','b']
```

### Predicate depth: admission vs evaluation (R70)

`compare(add^n(field, 1), 0)` against member `{x: 1}`:

| n_adds | admission `_predicate_depth` | evaluator |
| --- | --- | --- |
| 0–4 | 1 | ok |
| ≥5 | 1 | `MemberConstraintTooDeep` |

### Round dual gate and range_lookup on_miss (R17, R18, R44)

```
round 1.5 half_up unit 1, canon modes {half_up} -> Decimal('2')
round mode down vs that canon                   -> unknown rounding mode: 'down'
round mode weird in canon only                  -> unknown rounding mode: 'weird'
range_lookup miss on_miss=zero                  -> Decimal('0')
range_lookup miss on_miss=block                 -> LOOKUP_MISS
_in_band 10 in [10,20) LIE                      -> True
_in_band 10 in [10,20] anything_else            -> False
_in_band 20 in [10,20) LIE                      -> False
_in_band 20 in [10,20] anything_else            -> True
```

### Records `use_v2` (R39)

```
started_record(use_v2=False)["schema"] -> derivation-record.v1
started_record(use_v2=True)["schema"]  -> derivation-record.v7
CURRENT_RECORD_SCHEMA                  -> derivation-record.v7
```

### Universe-guard version set (R48)

Parsed from `universe_guard_active` at `package_validation.py:1533`: artifact-package **v3–v17 inclusive** (15 versions, including v7).

`conflict_semantics` count in `runner.py`: **0**.

---

# Open questions only another layer can answer

1. Does any contract require `selected_producer` to be the runtime winner, or is first-eligible-wins the intended evaluation rule?
2. Is `LOOKUP_MISS` supposed to appear on derivation-record / npe-walk, or is remapping to `DEPENDENCY_INVALID` intended?
3. Is `loader.OPERATION_VOCABULARY` a leftover, a schema-report helper, or a gate this stream missed because it is not on the evaluate path?
4. Should admission `_predicate_depth` walk `left`/`right` the way the evaluator does, or should the evaluator only count `args`?
5. Is empty `max` supposed to be a contained block?
6. Are the tax-id kill-tests in `package_validation.py` (R58) package-language or content? Track 0 put generic package rules on surface 4 and domain axioms on 6i; this file sits on both.
7. Does `source-family.v2` participate in collect-target universe-guard, or only v1 by design?
8. What does Track 1a say `divide` / `multiply` / `count` / `block` / `require_closed` / categorical ops are, relative to `CANON_OPERATIONS`?
9. Is `use_v2` selecting `derivation-record.v7` a contract, or a flag that drifted?
10. Form-field.v1 is admitted by `_SUPPORTED_SEMANTIC_SCHEMAS` and ignored by `FIELD_SCHEMAS` — what does the declared layer say that v1 is for?
11. `bracket_fold` loads canon and ignores `spec` — does the declared canon still constrain the fold?
12. `npe-walk.v3` is hardcoded; `CURRENT_RECORD_SCHEMA` is v7. Is that pairing declared?

---

# Track 0 or plan problems (plainly)

1. **Plan vs Track 0 on surface count.** The plan's `#Term boundary` names seven surfaces. Track 0 adds an eighth (kernel substrate) and tells Track 1 streams to cite it. This stream followed Track 0, per the charter ("the milestone plan controls if it and the charter disagree" — here the disagreement is plan vs Track 0, which the charter says to record, not resolve).
2. **Track 0 citation drift (line numbers).** Re-checked against the unchanged Layer 3 pin:
   - Blocking constants are `evaluator.py:24-28`, not `:22-27` (Track 0 surface 2). `CATEGORICAL_DOMAIN_MISMATCH` is `:28`.
   - `_ROUND_MODES` is `evaluator.py:30-35`, not `:29-34` (Track 0 6iii).
   - `universe_guard_active` is `package_validation.py:1533-1549`, not `:1527-1548` (Track 0 Layer 2 / gap 1). The comment starts at `:1525`.
   - Evaluator op if-chain including `conditional_dependency_set` is `:108-265`, not `:108-246`. Line 246 is the `if op ==` for that op; the body runs to `:265`.
3. **Track 0 gap 8 is necessary but incomplete.** Dual `MAX_PREDICATE_DEPTH = 6` literals are real. Independently, the **depth algorithms differ** (R70). A census that only records the duplicated literal will miss packages that admit trees the evaluator rejects.
4. **Track 0 did not name `loader.OPERATION_VOCABULARY` as a stale 14-op subset of the 23-op dispatcher.** Surface 1's op list was taken from `evaluate` (correct) but a downstream reader of `loader.py` would get a different language.
5. **Universe-guard family table is v1-only** (`source_family_members` filters `source-family.v1`). Track 0 said 5b-i lives on `source-family.v2`. The collect-target guard therefore does not obviously apply to the citizen that holds the term/predicate vocabulary. Recorded, not worked around.
6. **Plan `#Census unit` "representative committed uses"** for this stream are code citations and synthetic executions, not `packages/content/` paths. Content use is Track 1c. This stream did not glob content.
7. Nothing else in the plan's read sections appeared unworkable. The Layer 3 file list was sufficient. `live.py`'s import of `packages.tax.loader.domain_companion_presence_pairs` is a real extra edge off the Layer 3 list; the kernel half of those pairs is still in Layer 3.

---

# Counts

- Construct records in this file: **90** (`R1`–`R90`).
- Evaluator ops actually dispatched: **23**.
- Package-admission issue codes: **83**.
- Attachment schemas the runner interprets: **7** (`v1–v6,v8`; no v7).
- Universe-guard package **schema** versions: **15** (`v3`–`v17`).
