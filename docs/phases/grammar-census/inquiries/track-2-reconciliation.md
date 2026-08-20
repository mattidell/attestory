# Track 2 — Adversarial reconciliation

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 2 — three-way reconciliation and set differences
- Role: Builder
- Status: in progress (partial: method, naming, Surfaces 1–2)
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
