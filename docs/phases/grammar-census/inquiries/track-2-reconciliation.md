# Track 2 — Adversarial reconciliation

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 2 — three-way reconciliation and set differences
- Role: Builder
- Status: in progress (partial: construct table complete through surface 8)
- Source ref verified: `HEAD` `c954c4a854b1a8716ce74ed2a40fffa911528d25`
  on `milestone/grammar-census-engine-language-map`
- Assigned path: this file only
- Inputs (read in full before this file was started):
  Track 0 at `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`,
  Track 1a (108 constructs, `D-001`–`D-108`),
  Track 1b (90 constructs, `R1`–`R90`),
  Track 1c (84 constructs, `C01`–`C84`)

This is the **reconciled** construct set. It is the only track in this
milestone that makes declared-versus-implemented-versus-used set-difference
claims. Every Track 1 `status` of `pending-reconciliation` is replaced here.
None of those pending values survives.

Layer attestation in the table is `Y` when that stream recorded the construct
as its own census unit (or as an explicit alias of one), `—` when it did not.
A naming difference is not a set difference; both original names are kept in
the **aliases** column.

Final `status` values are the plan's `#Census unit` set: `active`,
`legacy-only`, `unused`, `apparently unreachable`, `uncertain`.

## Charter / plan scope (recorded, not resolved)

The plan's Track 2 section
(`docs/phases/grammar-census/milestones/engine-language-map.md`,
`#Tracks` / `### Track 2`) names three deliverables:
`track-2-reconciliation.md`, `track-2-representative-traces.md`, and
`track-2-tension-catalog.md`.

The dispatching charter
(`docs/reviews/2026-08-20-grammar-census-track-2-reconciliation-charter.md`)
covers **the reconciliation only**, assigns this one path, and says traces
and the tension catalog are chartered separately from this output.

This file produces the reconciliation. It does not write the other two
Track 2 paths. The split is recorded rather than closed: the plan still
owns Track 2 as a whole; this unit is the first of its three named
products.

## Method

1. Read Track 0 and Tracks 1a/1b/1c in full. Did not treat a Track 1 claim
   as established merely because it is committed, except the six Foreman-
   verified facts listed in the charter (attachment-rule.v5 `$id` collision;
   `selected_producer` absent from `runner.py`; `loader.OPERATION_VOCABULARY`
   is 14 names; all 59 committed `round` nodes take a `ref` to
   `rounding.convention`; `accounts_for` present in rule-artifact.v5 and
   absent in v6; Track 0 evaluator citations off by two lines).
2. Unify names where the three streams described the same form under
   different handles. Collapse is explicit in the aliases column.
3. For every consequential disagreement, go to source (schema, runtime, or
   a synthetic execution shown below) rather than adjudicating between two
   reports. The schema is not preferred because it is declarative; the
   runtime is not preferred because it executes.
4. Where all three layers agree on something load-bearing, spot-check the
   agreement against source anyway. Sample rule and results are in
   `#Three-way agreement spot-checks`.
5. CQ-1 merged artifacts on this tree under
   `docs/phases/claim-boundary-exploration/` were used once, as a bounded
   validation lens on surviving provenance pins — see `#CQ-1 lens`. They
   did not originate any census row.

Synthetic executions in this file were run against this worktree with
`python3` importing `packages.derivation.evaluator`,
`packages.derivation.declarative_validation`,
`packages.derivation.package_validation._predicate_depth`,
`packages.derivation.records`, and `packages.kernel.schema_registry`.
No personal data. No absolute workstation paths.

## Naming unification

These are the same construct under different names. They occupy **one**
reconciled row. They are not set differences.

| Unified name | Track 1a | Track 1b | Track 1c |
| --- | --- | --- | --- |
| `ref` | D-014 | R2 | C08 |
| `collect` | D-015 | R3 | C09 |
| `count` | D-016 | R4 | C10 |
| `block` (expression op) | D-017 | R5 | C27 |
| `parameter` | D-018 | R6 | C24 |
| `add` (rule-artifact) | D-019 | R7 | C11 |
| `max` | D-020 | R11 | C15 |
| `all` (rule-artifact) | D-021 | R13 | C17 |
| `any` (rule-artifact) | D-022 | R14 | C18 |
| `subtract` (rule-artifact) | D-023 | R8 | C12 |
| `multiply` | D-024 | R9 | C13 |
| `divide` | D-025 | R10 | C14 |
| `compare` (rule-artifact, field `cmp`) | D-026 | R12 | C16 |
| `not` | D-027 | R15 | C19 |
| `choose` | D-028 | R16 | C20 |
| `range_lookup` | D-029 | R18 | C26 |
| `bracket_fold` | D-030 | R19 | C25 |
| `round` (expression) | D-031 | R17 | C21 |
| `categorical_compare` | D-032 | R21 | C29 |
| `category_literal` | D-033 | R22 | C30 |
| `require_closed` | D-034 | R20 | C28 |
| `conditional_dependency_set` | D-035 | R24 | C32 |
| `collect_categorical_all_equal` | D-036 | R23 | C31 |
| untyped / scalar literal | D-013 | R25 | C07 |
| `when` | D-004 | R31 | C04, C05 |
| `blocked` (clause field) | D-007 | — | C33–C35 |
| `pins` (rule-artifact field) | D-010 | R80 | C36 |
| ledger `published` / `blocked` / `inapplicable` | D-044 | R33 | C78 |
| guard-false → inapplicable | D-045 | R31 | C78 |
| `conflict_semantics` / `selected_producer` | D-053 | R50, R34 | C68 |
| rounding-mode tokens | D-043 | R43 | C14, C23, C81 |
| attachment threshold | D-058 | R60 | C41 |
| `family_nonempty` | D-059 | R61 | C42 |
| `collect_members` | D-060 | R64 | C46 |
| completeness `presence` / `value` | D-062, D-063 | R62 | C43, C44 |
| `branch_requirements` | D-065 | R63 | C45 |
| `accounts_for` (rule-artifact.v5) | D-012 | — | C38 |
| `accounts_for` (attachment-rule.v8) | D-066 | — | C82 |
| form-field dispositions | D-068 | R66 | C48 |
| term language | D-075–D-078 | R68 | C52–C55 |
| predicate language | D-079–D-082 | R69 | C56–C61 |
| predicate depth bound of six | D-083 | R70 | C62 |
| `npe-walk` | D-086 | R78 | C76 |
| `derivation-record` | D-084 | R79 | C77 |
| `member_constraints` | D-072 | R47, R69 | C50 |
| `identity_exclusivity` | D-073 | R71 | C51 |
| `projects_from` | D-074 | — | C83 |
| `input_bindings` | D-050 | R52, R36 | C65 |
| `optional_default` | D-090, D-102 | R36 | C65 |
| source-closure-mapping | D-092 | R54 | C69 |
| parameter-declaration | D-093 | R6 | C70 |

These share an op **string** and are **not** the same construct. They keep
separate rows. Collapsing them would manufacture agreement.

| Distinct constructs that share a name | Why they are not one row |
| --- | --- |
| rule-artifact `add` vs source-family term `add` | n-ary `args` vs binary `left`/`right`; different host citizen; different error type (`EvalBlocked` vs `GrammarError`) |
| rule-artifact `subtract` vs term `subtract` | same split |
| rule-artifact `compare` (`cmp`: `gte`/`lte`) vs predicate `compare` (`comparison`: `ge`/`le`) | different field name, different enum tokens, different host |
| rule-artifact `all`/`any` vs predicate `all`/`any` | different host; predicate `all` has no `not` sibling in 5b-i |
| `collect` vs `collect_members` | different name, different keys, different host |
| `collect` vs `collect_categorical_all_equal` | ADR-0064 rejects treating the latter as a mode of the former; empty collect is closure, empty categorical-collect is `DEPENDENCY_ABSENT` |
| `block` (expression op) vs `blocked` (clause field) | op raises `EvalBlocked(expr["code"], [])`; field is authored on the citizen and is not read by `packages/derivation/runner.py` |
| `BLOCK_ABSENT` vs `DEPENDENCY_ABSENT` | Python alias and the string it holds (`evaluator.py:24`) |
| `BLOCK_LOOKUP_MISS` vs `LOOKUP_MISS` | same shape (`evaluator.py:27`) |
| `SOURCE_SET_OPEN` vs `SOURCE_SET_UNCLOSED` | rename across form-field.v2→v3 / npe-walk.v1→v2 / derivation-record.v2→v3 |
| package member `role` vs rule-artifact `role` | four shared tokens; package enum is larger |

## Reconciled construct table

One row per construct. Rec ids are `U-001` onward in this file. Citations
are the tightest source that settles the row; Track 1 handles remain in
the 1a/1b/1c columns.

### Surface 1 — core clause / expression language

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-001 | rule-artifact citizen envelope | D-001 | — | C01 | active | 134 files; required keys at `rule-artifact.v1.schema.json:7-32`; runtime accepts v1–v6 (`package_validation.py:192-194`, `:283-288`) |
| U-002 | untyped / scalar literal | D-013 | R25 | C07 | active | `evaluator.py:103-104`; 14 files with non-op `value` |
| U-003 | `ref` | D-014 | R2 | C08 | active | `evaluator.py:108-116`; 1333 occurrences / 115 files |
| U-004 | `collect` | D-015 | R3 | C09 | active | `evaluator.py:118-131`; 44 occurrences, all with `source_set`; empty unclosed → `SOURCE_SET_UNCLOSED`; nonempty unclosed succeeds |
| U-005 | `count` | D-016 | R4 | C10 | active | `evaluator.py:133-141`; always requires closure, even when rows exist; 15 occurrences / 7 files. No ADR names this op (1a silence). No `"op": "count"` in `tests/` |
| U-006 | `block` (expression op) | D-017 | R5 | C27 | active | `evaluator.py:143-144` raises `EvalBlocked(expr["code"], [])`; 6 occurrences / 3 files (`SLI_*`, `F1098_*`, `VALUE_INVALID`) |
| U-007 | `parameter` | D-018 | R6 | C24 | active | `evaluator.py:146-157`; 74 occurrences / 7 files; missing key → `LOOKUP_MISS` |
| U-008 | `add` (rule-artifact) | D-019 | R7 | C11 | active | `evaluator.py:159-160,274-282`; flattens lists so arity-1 `add` of a `collect` **sums**, it is not identity; empty `add` → `Decimal(0)`; 166 occurrences. Schema `minItems: 1` (`rule-artifact.v6.schema.json:36`) |
| U-009 | `max` | D-020 | R11, R30 | C15 | active | `evaluator.py:171-172`; 88 occurrences, all arity 2. Empty `max` raises uncontained `ValueError`. Schema `minItems: 1` makes the crash schema-gated in a validated package |
| U-010 | `all` (rule-artifact) | D-021 | R13, R29 | C17 | active | `evaluator.py:179-180` is Python `all` (short-circuits). ADR-0024 d4 states the short-circuit in evaluator terms; the schema does not encode order. 68 occurrences |
| U-011 | `any` (rule-artifact) | D-022 | R14, R29 | C18 | active | `evaluator.py:182-183`; 32 occurrences. Distinct from predicate `any` (U-123) |
| U-012 | `subtract` (rule-artifact) | D-023 | R8 | C12 | active | `evaluator.py:162-163`; no `_flatten`; 119 occurrences |
| U-013 | `multiply` | D-024 | R9 | C13 | active | `evaluator.py:165-166`; v6 only; not in `CANON_OPERATIONS`; 1 primary-corpus occurrence (`rule.sli-worksheet.json:272`) |
| U-014 | `divide` | D-025 | R10 | C14 | active | `evaluator.py:168-169,306-325`; zero divisor → `DEPENDENCY_INVALID ['division by zero']`; rounding lives on the op, not `env.canon`; 2 occurrences, both `rounding: half_up` |
| U-015 | `compare` (rule-artifact) | D-026 | R12 | C16 | active | `cmp` enum `eq,ne,gt,gte,lt,lte`; 162 occurrences. Unknown `cmp` is uncontained `KeyError`. Distinct from predicate `compare` (U-121) |
| U-016 | `not` | D-027 | R15 | C19 | active | `evaluator.py:185-186`; 3 occurrences / 2 files. ADR-0066 d2 says the *predicate* language has no `not`; this op is untouched |
| U-017 | `choose` | D-028 | R16 | C20 | active | `evaluator.py:188-190` evaluates only the taken branch; 211 occurrences |
| U-018 | `range_lookup` | D-029 | R18, R44 | C26 | unused | declared v1–v6; implemented; **0** hits in 134 primary rule-artifacts; 2 sample_data files. Miss → `LOOKUP_MISS` or zero per canon `on_miss` |
| U-019 | `bracket_fold` | D-030 | R19 | C25 | active | `evaluator.py:201-204,345-360` loads `env.canon["bracket_fold"]["spec"]` into a local and **never reads it**; 95 occurrences / 8 files |
| U-020 | `round` (expression) | D-031 | R17 | C21, C23 | active | v1 required `stage`; v2+ dropped it. Dual gate: mode must be in `_ROUND_MODES` **and** `canon["modes"]`. All 59 committed nodes take `mode` as `{op:ref, name: rounding.convention}` (Foreman-verified) |
| U-021 | `round.stage` | D-031 | — | C22 | legacy-only | required on rule-artifact.v1 (`:179-185`); absent v2+. One content file: `rule.wages-line1a.json:18` (`after_aggregate`). Successor `.v2.json` has no `stage`. Operation-semantics.v1 still enums stages on the *canon* citizen |
| U-022 | `categorical_compare` | D-032 | R21 | C29 | active | 368 occurrences, all `cmp: eq`. `ne` is declared and implemented, not observed |
| U-023 | `category_literal` | D-033 | R22 | C30 | active | 373 occurrences. Top-level op does **not** domain-check (`evaluator.py:220-221`); operand helper does |
| U-024 | `require_closed` | D-034 | R20 | C28 | active | `evaluator.py:206-211`; 71 occurrences, all under `when`; unclosed → `SOURCE_SET_UNCLOSED` |
| U-025 | `conditional_dependency_set` | D-035 | R24 | C32 | active | `evaluator.py:246-265`; false condition does not evaluate members; 20 occurrences / 17 files, host v3+ |
| U-026 | `collect_categorical_all_equal` | D-036 | R23 | C31 | active | `evaluator.py:223-244`; empty → `DEPENDENCY_ABSENT`, not closure; 5 occurrences, one v6 file |
| U-027 | evaluate dispatch / unknown-op | — | R1, R26 | — | active | 23-op if-chain `evaluator.py:108-267`; unknown → `DEPENDENCY_INVALID ['unknown op survived schema: …']`. This *is* the implemented vocabulary. `loader.OPERATION_VOCABULARY` is not |
| U-028 | `AccessLog` | — | R27 | — | active | `evaluator.py:47-59`; the only channel from evaluation to publication pins. No schema located |
| U-029 | numeric coercion / bool refusal | — | R28 | — | active | `evaluator.py:75-83`; `bool` refused because `True == 1`. No schema located |

### Surface 2 — guard, eligibility, publication, blocking

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-030 | rule-artifact `role` | D-002 | R37 | C02, C03 | active | enum `computation, applicability, field-mapping, cross-form-bridge` on every v1–v6. Observed: `computation` 132, `field-mapping` 2. `applicability` / `cross-form-bridge` live in `role-canon.v1` (U-150) and are **unused** on rule-artifact content. Evaluation does not branch on role |
| U-031 | `requires` | D-003 | R32 | C01 | active | eligibility list; saturate uses `_requires` (attachments synthesize extras). `attempt` step 1 re-reads `rule["requires"]` only |
| U-032 | `when` | D-004 | R31 | C04, C05 | active | 77 files literal `true`; 57 expression trees. False → `inapplicable` with `guard_result: False` (`runner.py:492-501`). No file has `"when": false` |
| U-033 | `value` | D-005 | — | C06, C07 | active | 120 expression trees, 14 literals |
| U-034 | `publishes` | D-006 | R34 | C01 | active | one symbol per clause; runtime first-publisher-wins (U-044) |
| U-035 | `blocked` (clause field) | D-007 | — | C33–C35 | active (authored); unused (as a runtime input) | required `{code, missing}` on every rule-artifact version. Pattern `^[A-Z][A-Z0-9_]+$`, not an enum. `packages/derivation/` contains **no** `rule["blocked"]` / `rule.get("blocked")` read. The runner emits its own codes |
| U-036 | `OPEN_DEPENDENCY` (authored `blocked.code`) | — | — | C34 | unused (as a ledger/evaluator code) | 33 / 134 files write it, often `missing: ["rounding.convention"]`. Not in `derivation-record.v7` enum. Not emitted by the evaluator. On the v2 ledger path would remap to `DEPENDENCY_INVALID` (U-045) |
| U-037 | `scope` | D-008 | — | C40 | active | `{family, jurisdiction, tax_year}` ± `effective_from` |
| U-038 | `notes` | D-009 | — | C01 | active | optional; 132 / 134 files. No ADR assigns evaluation meaning |
| U-039 | `pins` (rule-artifact field) | D-010 | R80 | C36 | active | required v2+. Content writes `input`×377 and `parameter`×16. Runtime `pins_for` adds operation-semantics / adoption / governance / collected inputs (C80) |
| U-040 | `composition` and `citations` | D-011 | R80 | C37, C39 | active | optional v2+; 15 composition, 90 citations. Citation pins come from `rule.get("citations")`, not AccessLog |
| U-041 | `accounts_for` (rule-artifact.v5) | D-012 | — | C38 | active (v5 content); unused (on v6) | optional in v5 (`rule-artifact.v5.schema.json:87-123`); **absent from v6** (Foreman-verified). 8 v5 files. ADR-0066 d5/d6. v6 `additionalProperties: false` |
| U-042 | ledger dispositions | D-044 | R33 | C78 | active | `published` / `blocked` / `inapplicable`. Conflict-losers are inapplicable with no `guard_result` |
| U-043 | guard-false → inapplicable | D-045 | R31, R38 | C78 | active | `runner.py:492-501`; `finalize_unreached` preflight prefers false guard over missing requires (`:1212-1231`). Walk payload token `guard_inapplicable` |
| U-044 | first-publisher-wins | D-054 | R34 | C68 | active (as runtime rule) | `runner.py:471-484`. `conflict_semantics` / `selected_producer` count in `runner.py`: **0** (Foreman-verified). Admission still requires `selected_producer` to *permit* two publishers (U-072) |
| U-045 | blocking-code remapping | D-085, D-104 | R35 | C79 | active | on `use_v2`, disposition `code` is kept only if it is in `record_codes` (`runner.py:1169-1183`); otherwise **`DEPENDENCY_INVALID`**. `LOOKUP_MISS` and `FAMILY_VALIDATION_BLOCKED` are not in that set. `self.blocked` keeps the internal code |
| U-046 | `LOOKUP_MISS` / `BLOCK_LOOKUP_MISS` | — | R6, R18, R35 | C79 | active (evaluator); apparently unreachable (on v2 ledger / npe-walk.v3) | `evaluator.py:27`; not in `derivation-record.v7` enum (`:124-135`); not in `npe-walk.v3` code enum. Tests assert `BLOCK_LOOKUP_MISS` (`test_runner.py:133-145`) |
| U-047 | `FAMILY_VALIDATION_BLOCKED` | — | R47, R35 | — | active (internal); apparently unreachable (on v2 ledger) | synthesized producer `blocked.code`; remapped to `DEPENDENCY_INVALID` on v2 ledger. Not found in any `*.schema.json` |
| U-048 | `optional_default` input binding | D-090, D-102 | R36 | C65 | active | `runner.py:218-264`; gated on `use_v2`. v33 has 5 `optional_default` bindings. Missing parameter silently skips |
| U-049 | `finalize_unreached` guard preflight | — | R38 | — | active | `runner.py:1188-1330`. No schema located |
| U-050 | saturate-to-fixpoint scheduler | — | R40 | — | active | `runner.py:1343-1358`. No schema located |
| U-051 | demand-driven reference runner | — | R41 | — | active | `reference_runner.py:27-66`. Cyclic demand is a silent return, not a recorded block |
| U-052 | `use_v2` schema switch | D-084 | R39 | — | active | `runner.py:185-191`; `records.py:168-186`. Flag named `use_v2` selects `derivation-record.v7` (`CURRENT_RECORD_SCHEMA` at `records.py:40`). Synthetic: `started_record(use_v2=True)["schema"] == "derivation-record.v7"`; `False` → `derivation-record.v1` |

### Surface 3 — operation-semantics and 6iii rounding

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-053 | operation-semantics citizen | D-037 | R42 | — | active | two schema generations with **disjoint** operation enums: v1 `round, range_lookup, bracket_fold`; v2 `categorical_compare, require_closed`. Highest-numbered is not a superset. Loaded from `packages/canon/derivation/` (`loader.py:136-162`), not from a package `admitted_schemas` member. v33 instance list omits both v1 and v2 |
| U-054 | `round` semantics spec | D-038 | R17 | C21 | active | `operation-semantics.v1.schema.json:17-45`; modes/stages/tie_break/unit. Runtime intersects this with `_ROUND_MODES` |
| U-055 | `range_lookup` semantics spec | D-039 | R18 | C26 | unused (in primary content) | `on_miss` `block`\|`zero`; boundary enum of two conventions. Primary corpus has 0 `range_lookup` nodes |
| U-056 | `bracket_fold` semantics spec | D-040 | R19 | C25 | active (citizen required); unused (as consulted spec) | schema requires `method, boundary, open_top, on_miss, row_shape`. Evaluator loads `spec` and ignores every field (`evaluator.py:345-360`). Missing canon **key** is still `KeyError` |
| U-057 | `categorical_compare` semantics spec | D-041 | R21 | C29 | active | `operation-semantics.v2`; `domain_mismatch` const `block` |
| U-058 | `require_closed` semantics spec | D-042 | R20 | C28 | active | `spec.admission` const `current-literal-true` |
| U-059 | rounding-mode tokens | D-043 | R43 | C14, C23, C81 | active | four tokens `half_up, half_even, down, up` on operation-semantics.v1 **and** on `divide.rounding`. Nothing `$ref`s the other. Content `round.mode` never writes those strings (always a `ref`). Content `divide.rounding` writes `half_up` only. Bundle enum lists `half_up` only (`core_calculations.bundle.v2.json:191`) |
| U-060 | `_ROUND_MODES` Python mapping | D-043 | R43 | — | active | `evaluator.py:30-35`. The process cannot apply any other mode. Divide uses this table alone; round also intersects canon |
| U-061 | `range_lookup` boundary `else` | — | R44 | — | active (as control flow); unused (no primary `range_lookup`) | `_in_band` (`evaluator.py:95-98`): only `"lower_inclusive_upper_exclusive"` is special-cased; **any other string** is lower-exclusive / upper-inclusive. Unknown boundary is not a block |
| U-062 | `rounding.convention` | — | R6, R17 | C23, C81 | active | the production `round.mode` is always a `ref` to this symbol. `_SUPPORTED` exempts it from fact-surface membership (`package_validation.py:1055`) |
| U-063 | `loader.OPERATION_VOCABULARY` | — | R1 | — | unused | 14-name frozenset (`loader.py:86-103`). Defined, never referenced elsewhere in `*.py` (only `role_vocabulary_report` is the sibling helper). Foreman-verified as a 14-element subset of the 23-op dispatcher |
| U-064 | `CANON_OPERATIONS` | D-037 | R42 | — | active | `round, range_lookup, bracket_fold` (`loader.py:104`). Multiply/divide/count/block/require_closed/categorical ops are **not** in it and do not pin operation-semantics |

### Surface 4 — package selection, binding, closure

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-065 | artifact-package citizen | D-046 | R45 | C63 | active | 35 files, three lineages (U-087). Schema family v1–v25 contiguous. Instance `version` is a second axis (v1–v33 for core-calculations). Unversioned `package.core-calculations.json` is instance v1, not current |
| U-066 | `admitted_schemas` | D-047 | R46 | C64 | active | v25 schema enum has 42 names, includes `rule-artifact.v2..v6` and `operation-semantics.v2`, **omits** `rule-artifact.v1` and `operation-semantics.v1`. v33 instance lists 39, omits `rule-artifact.v1`, `attachment-rule.v3`, `attachment-rule.v5`, `form-field.v1`, both operation-semantics |
| U-067 | `members` / member pin | D-048 | R45 | C63 | active | v33: 363 members |
| U-068 | member `role` tokens | D-049 | R37 | C63, C74 | active | v25 enum is larger than rule-artifact `role`. Observed in v33: computation 86, citation 72, …, 1 each of dividend-universe, composition, field-mapping, checked-conclusion-binding, migration-artifact |
| U-069 | `input_bindings` | D-050 | R52 | C65 | active | `required` blocks on absence (via later `DEPENDENCY_ABSENT`); `optional_default` is U-048. Marshal does not use `mode` (`marshal.py:261-262`) |
| U-070 | `entrypoints` | D-051 | R49 | C66 | active | v33 has 141. Exact `(id, version)` matching only for `artifact-package.v20`–`v25` |
| U-071 | `composition_obligations` | D-052 | R51 | C67 | active | v33 names two interest-total symbols. Several admission branches name specific tax ids (U-085) |
| U-072 | `conflict_semantics` | D-053 | R50 | C68 | active (admission); unused (as runtime selector) | v2+ `{symbol, selected_producer}`. 5 files (core-calculations v29–v33) name `tax.us.2025.rule.schedule-a-total` for `tax.us.2025.schedule-a.total`. Runner never reads the field (U-044) |
| U-073 | unique output ownership | D-054 | R50, R34 | C68 | active | ADR-0006 d7: no two members publish the same symbol unless the package declares conflict semantics. Admission: `OUTPUT_OWNERSHIP_CONFLICT` unless the symbol is in `declared_conflicts`. Runtime: first eligible producer wins regardless of `selected_producer` |
| U-074 | `package_checksum` | D-055 | R53 | — | active | ADR-0027 d6; production resolver compares bytes |
| U-075 | `validate_package` | — | R45 | — | active | `package_validation.py:727-2081`; production hard-gates on `ok` (`production_resolver.py:363-371`) |
| U-076 | `_SUPPORTED_SEMANTIC_SCHEMAS` | D-106 | R46 | — | active | `package_validation.py:246-293`; includes `rule-artifact.v1..v6`, `attachment-rule.v1..v6,v8` (no v7), `operation-semantics.v1` and `.v2`, `form-field.v1..v3`, `fact-type.v2` (not v1), `source-family.v1` and `.v2`. This is the runtime's accepted-schema set. Unlisted → `MEMBER_SCHEMA_UNSUPPORTED` |
| U-077 | synthesized `<family>.member-validation` | — | R47 | — | active | `compile_validation_graph` (`package_validation.py:574-639`) emits a compiled `rule-artifact.v5` producer. Reachability, not authoring, creates the edge |
| U-078 | universe guard (`COLLECT_TARGET_NOT_FAMILY`) | — | R48 | — | active (artifact-package.v3–v17); unused (v18–v25) | `package_validation.py:1533-1549`. Family table is built only from `source-family.v1` (`:1550-1554`). `source-family.v2` — the citizen that holds term/predicate — does not participate |
| U-079 | inbound reachability | D-051 | R49 | C66 | active | BFS from entrypoints plus form-fields. `closed_v2_surface` is package **instance** `version != "v1"` (`:1361`), not schema generation |
| U-080 | production resolver | D-101 | R53 | — | active | `production_resolver.py:134-204,297-377`. No committed adoption pins `tax.us.2025.package.core-calculations` (Track 0). Surface 8 act, not a package-shape citizen |
| U-081 | closure admission | D-092 | R54 | C69 | active | `source_authority.py:100-166`; `env.closed_sets = frozenset(self.admissions)` (`runner.py:290`). Truthy non-bool does not admit (`isinstance(value, bool) and value is True`) |
| U-082 | marshal from current findings | — | R55 | — | active | `marshal.py:210-402`; only `currency.current_finding_ids` |
| U-083 | collect source-name assembly | — | R56 | — | active | `live.py:67-143`; evaluator `collect` does not discover names from the expression alone |
| U-084 | package admission issue-code family | — | R57 | — | active | 83 distinct `MemberIssue.code` strings, unversioned, Python-only. No single schema enum enumerates them |
| U-085 | tax-hardcoded package kill-tests | — | R58 | — | active | `package_validation.py:197-221,1635-1662` names specific tax citizen ids. Surface-4 shape with surface-6i content. Track 0 put generic package rules on 4 and domain axioms on 6i; this file sits on both |
| U-086 | quantity-vocabulary check vs supported set | D-099 | R59 | — | active (v1–v3 index); apparently unreachable (v4–v12 as the quantity index) | `_SUPPORTED` lists v1–v12; the **index** is built only from v1–v3 (`package_validation.py:1085-1090`) |
| U-087 | three named package lineages | — | — | C84 | active | `core-calculations` (33 files), `first-tax-slice` (artifact-package.v1), `interest-slice` (artifact-package.v2) |

### Surface 5a — attachment-rule / form-field

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-088 | attachment-rule citizen | D-056 | R60–R65 | C41–C47 | active | seven published files, **no v7**. 15 content files. Host schemas in content: v4×7, v6×2, v8×2, v2×2, v3×1, v1×1. **No content host v5** |
| U-089 | attachment-rule.v5 `$id` / `schema` const of v3 | D-056 | R46 | — | apparently unreachable (as a named instance discriminator) | Foreman-verified: `$id` `tax/attachment-rule.v3` at `attachment-rule.v5.schema.json:120`; `properties.schema.const` is `attachment-rule.v3` (`:229`); different SHA-256 from the v3 file. Registry keys by **filename** (`schema_registry.py:152`), `validate_declared` by instance `schema` (`:234-244`). Catch-22: name `attachment-rule.v5` → v5 file → const requires v3 → fail; name v3 → v3 file → v5 bytes never run. `_SUPPORTED` still lists `attachment-rule.v5`. Finding, not a repair |
| U-090 | attachment triad dispositions | D-057 | R60, R61 | — | active | not-required / required-and-complete / required-and-incomplete (ADR-0036 d1). Not-required is `inapplicable` with `guard_result: False` |
| U-091 | requirement: threshold / `strictly_greater_than` | D-058 | R60 | C41 | active | 13 / 15 files. Test is `>` (`runner.py:883-923`). v3/v4 schema is a oneOf; v5/v6/v8 parsed `requirement` is threshold-only |
| U-092 | requirement: `family_nonempty` | D-059 | R61 | C42 | active (v3/v4 content and schema); unused (v5/v6/v8 schema) | schema admits it only in v3 and v4. Content: 2 files (`attachment.schedule-d.json` host v3, `.v2.json` host v4). Later schedule-d content versions use the threshold shape. Runtime is schema-agnostic once `kind` matches (`runner.py:574-626`) |
| U-093 | `collect_members` | D-060 | R64 | C46 | active | 69 occurrences, all 15 files. Not a rule-artifact expr op |
| U-094 | `itemization_authority` | D-061 | R64 | C46 | active | v2+ `single_family` \| `composition` |
| U-095 | completeness `check: presence` | D-062 | R62 | C43 | active | 26 answer objects. Presence is checked before value |
| U-096 | completeness `check: value` | D-063 | R62 | C44 | active (v4 schema and content); unused (v5/v6/v8 schema `required_answer` is const `presence`) | ADR-0055; code `COMPLETENESS_VALUE_VIOLATION`. 46 answer objects, all `equals: "yes"`. Present in e.g. `attachment.schedule-a.json` |
| U-097 | `adjustment_row` | D-064 | R65 | C46 | active | v5 file / v6 / v8 schemas; `_V6_SHAPE_ATTACHMENT_SCHEMAS = {v6, v8}` (`runner.py:142`). Kind tokens `nominee_distribution, accrued_interest, abp_adjustment` are schema-closed, no ADR language decision found (1a). 10c subtractive exception is v6-only (`package_validation.py:1936`); 10b includes v8 |
| U-098 | `branch_requirements` | D-065 | R63 | C45 | active | 6 / 15 files. False trigger does not add extras |
| U-099 | `names_obligations` / `FINCEN_114_NAMED` | D-065 | R63 | C47 | active | four schedule-b attachment-rule files. Published onto the attachment value as `named_obligations` (`runner.py:1121-1127`) |
| U-100 | `accounts_for` (attachment-rule.v8) | D-066 | — | C82 | active | same relationship enum as U-041. 2 files, both host v8: `attachment.f8949.v2.json`, `attachment.schedule-d.v6.json`. This is **not** a v6 continuation of rule-artifact `accounts_for` |
| U-101 | form-field citizen | D-067 | R66 | C48 | active | 50 files, host v3×43, v2×7. `form-field.v1` is in `_SUPPORTED` and not in content (sample_data only) |
| U-102 | form-field disposition classes | D-068 | R66, R76 | C48 | active | five keys `published_value, computed_zero, closure_backed_zero, blocked, guard_inapplicable` |
| U-103 | form-field blocked-code list | D-069 | R66 | C48 | active | v2 enums `SOURCE_SET_OPEN`; v3 replaces it with `SOURCE_SET_UNCLOSED`. One content file still carries `SOURCE_SET_OPEN`: `form1040.line-2b.form-field.json` (host v2) |
| U-104 | `binds_symbol` | D-070 | R66 | C48 | active | admission: must be produced or input-bound |
| U-105 | `FIELD_SCHEMAS` (presentation) | D-067 | R66 | C48 | active (v2/v3); apparently unreachable (v1 in presentation) | `presentation_projection.py:37` is `{form-field.v2, form-field.v3}` only. v1 is admitted by `_SUPPORTED` and ignored by the projector |
| U-106 | attachment compiled `.member-validation` gate | — | R67 | — | active | post-compile `requires` entries; `attempt_attachment` itself never reads `requires` |

### Surface 5b — source-family term / predicate language

Term and predicate ops are a **second, nested expression grammar**. They are
not additional rule-artifact operations. Track 0 reversed the adjacent
classification after finding `$defs/term` and `$defs/predicate` on
`source-family.v2` (not on any attachment-rule schema).

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-107 | source-family declaration | D-071 | — | C49 | active | 48 files: 40 host v1, 8 host v2. Term/predicate exist only on v2 |
| U-108 | `member_predicate` | D-071 | R56 | C49 | active | `{fact_type}` in all 48 files; no `op` key. This is membership, not the nested predicate language |
| U-109 | `member_constraints` | D-072 | R47, R69 | C50 | active | 8 constraint objects in 2 files (covered-W families). `block_code` is an open pattern. Evaluated by `declarative_validation.py`; failure contributes to `FAMILY_VALIDATION_BLOCKED` |
| U-110 | `identity_exclusivity` | D-073 | R71 | C51 | active | 1 object in each of the same 2 files; components are `fact_id_bound_key` / `member_field`, not term nodes |
| U-111 | `projects_from` | D-074 | — | C83 | active | 6 / 48 files. Schema only; no accepted ADR names the field (1a) |
| U-112 | term `field` | D-075 | R68 | C52 | active | 12 occurrences (8 bare, 4 with `default: 0`) |
| U-113 | term `literal` | D-076 | R68 | C53 | active | 2 occurrences (`arg: 0`) |
| U-114 | term `add` | D-077 | R68 | — | unused | declared and implemented; **0** hits in 48 source-family files. Binary `left`/`right`, not rule-artifact n-ary `add` |
| U-115 | term `subtract` | D-077 | R68 | C54 | active | 2 occurrences inside `ADJUSTMENT_EXCEEDS_LOSS` |
| U-116 | term `floor_zero` | D-078 | R68 | C55 | active | 2 occurrences. No rule-artifact counterpart |
| U-117 | predicate `field_present` | D-079 | R69 | C58–C61 | active | 2 occurrences |
| U-118 | predicate `field_absent` | D-079 | R69 | C58–C61 | active | 2 occurrences |
| U-119 | predicate `field_equals` | D-080 | R69 | C58–C61 | active | 2 occurrences. Absent field is not equal |
| U-120 | predicate `field_not_equals` | D-080 | R69 | C58–C61 | active | 2 occurrences. Absent field is **False** (does not fire) — 1b synthetic and ADR-0066 d2 agree |
| U-121 | predicate `compare` | D-081 | R69 | C57 | active | field `comparison` enum `gt, ge, lt, le, eq, ne`. Observed `gt` and `ge` only. Distinct from rule-artifact `cmp` |
| U-122 | predicate `all` | D-082 | R69 | C56 | active | 6 occurrences. Python `all` short-circuit |
| U-123 | predicate `any` | D-082 | R69 | — | unused | declared and implemented; **0** hits in 48 source-family files |
| U-124 | predicate depth bound of six | D-083 | R70 | C62 | active (as two independent literals); uncertain (as one bound) | **No JSON Schema max-depth.** ADR-0066 d2 names six in prose. Two Python literals, **two algorithms**: evaluator increments on nested `add`/`subtract`/`floor_zero`/`compare`/`all`/`any` (`declarative_validation.py:20,62,87`); admission `_predicate_depth` walks only `args` (`package_validation.py:182-188,2037-2056`) and does **not** walk `left`/`right`/`value`. Synthetic: `compare(add^n(field,1), 0)` has admission depth 1 for every n; evaluator `TOO_DEEP` at n≥5. Content max observed depth 2. Three-way agreement that "the bound is 6" is true of the literals and **false** of the trees they apply to — see `#Three-way agreement spot-checks` |

### Surface 6 — runtime behaviors adjacent to grammar

Track 0 classified 6i and 6ii grammar-adjacent (no schema-typed citizen /
store-side). 6iii rounding is proper and is U-059/U-060. These rows stay
in the census because `#Census unit` asks for runtime consumers that
assign behavior.

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-125 | subset invariants | — | R72 | — | active | `schema_registry.py:91-96`; `findings.py:221-275`. Kernel reject-not-record. Registry populated by a tax-layer loader outside Layer 3 |
| U-126 | companion presence / value domains / equality | — | R73 | — | active | `findings.py:296-405`; runner fail-closed on missing companion pin (`runner.py:322-369`) |
| U-127 | declaration/signal contradictions | — | R74 | — | active | `findings.py:433-487`; ADR-0038 decision 5 |
| U-128 | displacement closure | — | R75 | — | active | `DECLARED_EDGE_KINDS = {derivation, individuation}` (`currency.py:16`). Parameter / operation-semantics / adoption pins are not displacement edges |
| U-129 | presentation numeric kinds | D-068 | R76 | C48 | active | `published_value` / `computed_zero` / `closure_backed_zero`. Closure-backed zero **drops citation leaves** (`presentation_projection.py:177-188`) |
| U-130 | `presentation-model.v1` | — | R77 | — | unused (as a published citizen) | Python string, no `*.schema.json` hit. Module docstring: not a published schema. Consumes dispositions; does not evaluate expressions |

### Surface 7 — provenance, disposition, explanation

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-131 | derivation-record citizen | D-084 | R79 | C77 | active | `CURRENT_RECORD_SCHEMA = "derivation-record.v7"` (`records.py:40`) is the one committed current-version designation Track 0 accepted. `use_v2=False` writes v1. Not authored in `packages/content/tax/2025` |
| U-132 | derivation-record block-code vocabulary | D-085 | R35 | C27, C33 | active | v7 enum at `derivation-record.v7.schema.json:124-135` (12 codes). Includes `SLI_*` and `F1098_*` that the evaluator's five constants never assign; those arrive via the `block` op (U-006) |
| U-133 | npe-walk citizen | D-086 | R78 | C76 | active | walker hardcodes `"schema": "npe-walk.v3"` (`explanation.py:332`). Not authored in production tax content. Tests assert v3 (`test_npe_walk.py`) |
| U-134 | npe-walk `node_kind` | D-087 | R78 | C76 | active | enum `published, blocked, guard_inapplicable, no_disposition_recorded`. ADR-0020 d7's `invalid` refinement is **not** a `node_kind` |
| U-135 | npe-walk block-code vocabulary | D-088 | R35, R78 | C76 | active (through `COMPLETENESS_VALUE_VIOLATION`); apparently unreachable (for record-only codes) | v3 enum: `DEPENDENCY_ABSENT, DEPENDENCY_INVALID, CATEGORICAL_DOMAIN_MISMATCH, SOURCE_SET_UNCLOSED, VALUE_INVALID, ITEMIZATION_TIE_OUT_VIOLATION, COMPLETENESS_VALUE_VIOLATION`. No v4–v7 matching later record codes. `SLI_MFS_INELIGIBLE` is not a legal `npe-walk.v3` `code` |
| U-136 | derived-finding | D-089 | R39 | C80 | active | v1/v2; authority is the attribution chain (ADR-0009 d1) |
| U-137 | `resolved_input` / declared default | D-090 | R36 | C65 | active | `derived-finding.v2`; `origin: declared_default` vs `assertion` |
| U-138 | `act-derived-publication` | D-091 | R89 | — | active | ADR-0007; kernel compose-over does not interpret this kind (U-161) |
| U-139 | pin construction (runtime) | D-010, D-105 | R80 | C80 | active | `runner.py:297-400`. Content `pins` (U-039) are not the complete surviving set |
| U-140 | content-addressed ids | — | R81 | — | active | `runner.py:157-158`; prefix + sha256[:24] |
| U-141 | ledger pin exclusion | — | R82 | — | active | v2 disposition pins drop `{computation, applicability, field-mapping, cross-form-bridge}`. Explanation walking uses the **finding's** pins |
| U-142 | `no_disposition_recorded` | D-107 | R78 | — | active | ADR-0020 d4 step 4; requires `closing_phase` |
| U-143 | publication pin roles demonstrated by tests | D-010 | R80 | C80 | active | `test_runner.py:148-158` asserts `field-mapping, input, operation-semantics, adoption, governance`. Content `pins` only write `input` and `parameter` |

### Neighboring Layer 2 citizens (Track 0 corpus; not numbered in `#Term boundary`)

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-144 | source-closure-mapping | D-092 | R54 | C69 | active | 49 files, all host v2; `admission.condition` is `current-literal-true` in all 49. `_SUPPORTED` excludes v1 |
| U-145 | parameter-declaration | D-093 | R6 | C70 | active | 18 files, host v1 only. `values` is an unconstrained object (schema-deliberate) |
| U-146 | checked-conclusion-binding | D-094 | — | C73 | active | 1 file; truth table consts **are** declared evaluation while the description disclaims execution. `direct_route: guard_inapplicable` vs runner `inapplicable` vs form-field `guard_inapplicable` are three surfaces of one ADR-0020 layering, not three mechanisms — see Q11 |
| U-147 | dividend-universe | D-095 | R48 | C71 | active | v1–v4 of the same id; composable-box list grows 2→3→4→5 |
| U-148 | taxable-interest-composition | D-096 | R51 | C72 | active | 4 files, host v1; `coextensiveness: slot-bijection` |
| U-149 | citation | D-097 | R80 | C39 | active | 74 files, host v1. Resolution is structural/adoption-only (ADR-0029) |
| U-150 | role-canon | D-098 | R37 | C74 | active | 1 file. Lists `applicability` and `cross-form-bridge` as rule roles; the 134 files' `role` field does not use them |
| U-151 | quantity-vocabulary | D-099 | R59 | — | active | v1–v12, **not monotone**: v7 drops `exempt-interest-dividends` and adds `covered-w-*`; v8 drops those six and restores `exempt-interest-dividends`; v12 does not contain `covered-w-*`. Track 0 did not flag this |
| U-152 | migration-artifact | D-101 | R88 | C75 | active | 1 file, 13 pairs. Currency treats retired types as supersession roots |

### Surface 8 — kernel store (grammar-adjacent; required for input/output domains)

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-153 | fact-type | D-100 | R86 | — | active | v1–v3. `_SUPPORTED` names `fact-type.v2` only. `ref.name` is **not** schema-constrained to a fact-type id (Track 0 gap 5; confirmed) |
| U-154 | act / fact / entity / horizon substrate | D-101 | R83–R89 | — | active (as the domain `ref`/`collect` read) | Track 0 eighth surface. `act-package-adoption.v1` lives here, not on surface 4 |
| U-155 | `optional_default` on fact-type.v2 | D-102 | R36 | C65 | active | ADR-0025 d1: determinable scalars only; elective cannot declare a default |
| U-156 | fact-id rendering | — | R83 | — | active | `{fact_type_id}\|k=v,…` (`facts.py:235-237`); parsed by marshal, declarative_validation, findings |
| U-157 | family-horizon succession | D-092 | R84 | C69 | active | one current horizon per `(family id, family version, scope)` |
| U-158 | member-transition vs assertion routing | — | R85 | — | active | SC-R1/SC-R2 in `findings.py:595-615,730-741` |
| U-159 | supersession policy | D-100 | R86 | — | active | `free` / `locked` / `closed-on-attestation` (ADR-0041, fact-type.v3) |
| U-160 | `SchemaRegistry.validate_declared` | D-103 | R87 | — | active | instance `schema` selects the validator; no registry-level "current" |
| U-161 | kernel compose-over of act kinds | — | R89 | — | active | unknown-to-kernel kind is not an error; `derived-publication` is folded by derivation projection |
| U-162 | surface artifact resolver | — | R90 | — | active (as a non-interpreter) | SHA-256 entries; does not interpret rule-artifact expressions |

### Cross-cutting declared contracts

| Rec | Name (aliases) | 1a | 1b | 1c | Status | Citation |
| --- | --- | --- | --- | --- | --- | --- |
| U-163 | schema immutability / instance-named version | D-103 | R87 | C01 | active | ADR-0003. Exception: attachment-rule.v5 file consts v3 (U-089) |
| U-164 | two independent version axes | D-108 | R49 | C01, C63 | active | every content citizen parsed has both `schema` and `version` except fact-type.v1/v3. Package instance v33 sits on `artifact-package.v25` |
| U-165 | pin-value origin (no evaluator constants) | D-105 | R80 | C80 | active | ADR-0007 d4. Round modes applied via `_ROUND_MODES` are process constants; the *mode name* comes from a ref or from `divide.rounding` |
| U-166 | unknown semantic schema versions fail loudly | D-106 | R46 | — | active | ADR-0066 d7; runtime token `MEMBER_SCHEMA_UNSUPPORTED` |
