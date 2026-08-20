# Track 1a — Declared constructs

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 1a — contracts and schema
- Status: complete for this stream
- Layer read: accepted ADRs in `docs/adr/` and every published schema version
  Track 0 classified grammar proper, plus the Layer 2 supporting citizens
  Track 0 named and the surface-8 domain Track 0 said this stream must not skip
- Not read: runtime modules as authority; committed rule content as usage;
  sibling Track 1b / 1c deliverables; anything under
  `docs/phases/claim-boundary-exploration/`

This file is the **declared** construct set: what contracts and schemas say
the language is. It does not claim that any construct is implemented, unused,
or used. Every `status` is `pending-reconciliation`.

## Method

Corpus is Track 0
(`docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`) as
accepted at `4f66bc83`. Surfaces labelled **grammar proper** were read in
every published version. Surface 8 (kernel act/fact/entity/horizon) is
**grammar-adjacent**; it is recorded only as the input/output domain the
census unit cannot answer without. Surfaces 6i and 6ii are adjacent and have
no schema-typed citizen; this layer records that silence.

Accepted ADRs are the INDEX status column (`docs/adr/INDEX.md` lines 35–100):
53 accepted, 7 retired, 3 superseded, 2 rejected, 1 proposed. Only accepted
ADRs are cited as present-tense authority. `rejected` / `superseded` /
`proposed` / `retired` are inert (INDEX lines 7–8, 13–18).

Every path, line, enum, and count below was produced by parsing the named
file or by `grep`-equivalent line scans. Filename prefixes were not used to
classify citizens. Version series were enumerated from directory listings;
`attachment-rule` has no v7.

Where a schema admits a construct and no accepted ADR fixes its meaning, that
silence is the finding. Implementation was not consulted to fill it.

### Record shape

Each construct uses the plan's `#Census unit` fields:

| Field | How this stream fills it |
| --- | --- |
| name | construct name |
| layer | Track 0 surface number and proper/adjacent label |
| accepted syntax | schema `$defs` / `enum` / required fields, cited by path:line |
| source of authority | ADR decision and/or schema citation |
| runtime consumer | **this layer is silent** |
| semantic effect | only where an ADR or schema description states it |
| input/output domains | only where the contract states them |
| evaluation / blocking / invalidity / nonpublication | only where the contract states them |
| separately versioned | yes/no, and which series |
| representative committed uses | **this layer is silent** |
| status | always `pending-reconciliation` |
| provenance that survives execution | only where ADR-0007 / 0009 / 0020 / the produced-record schemas state it |
| nearby inferences this evidence does not support | explicit |

Defaults that would otherwise repeat 108 times: runtime consumer, representative
uses, and (except surface 7) provenance-surviving-execution are silent on this
layer.

### Plan / charter / Track 0 wording

The milestone plan's Track 1a paragraph names "every relevant rule-artifact
and operation-semantics schema version." The charter names "every schema
version in the Track 0 corpus for the surfaces Track 0 classified grammar
proper." Track 0's Layer 2 bounded corpus additionally names
`artifact-package.v1..v25`, `derivation-record.v1..v7` (with v7 as the one
named current), `npe-walk.v1..v3`, `form-field.v1..v3`,
`attachment-rule.v1,v2,v3,v4,v5,v6,v8`, `source-family.v1..v2`, and
`quantity-vocabulary.v1..v12`, and tells this stream not to skip surface 8.
The plan is supposed to control on disagreement. This stream did not shrink
the reading to the plan paragraph's two families — Track 0's corpus is
binding — and records the wording clash rather than resolving it.

## Version-drift tables (declared forms, both ends)

### Rule-artifact expression ops

`packages/schemas/derivation/rule-artifact.vN.schema.json` `$defs/expr`.
A cell is the version that first admits the op, or a shape change.

| Op | v1 | v2 | v3 | v4 | v5 | v6 |
| --- | --- | --- | --- | --- | --- | --- |
| untyped literal (`string\|number\|boolean\|null`) | yes | yes | yes | yes | yes | yes |
| `ref` | `{op, name}` | same | extracted as `$defs/ref_expr` | same | same | same |
| `collect` | `{op, name}` required; `source_set` optional | `source_set` required | same | same | same | same |
| `parameter` | `{op, parameter_id}` + optional `key` expr | same | same | same | same | same |
| `add`/`max`/`all`/`any` | four separate oneOf arms | one arm, `op` enum of the four | same | same | same | same |
| `subtract` | `{op, left, right}` | same | same | same | same | same |
| `compare` `cmp` enum `eq,ne,gt,gte,lt,lte` | yes | yes | yes | yes | yes | yes |
| `not` / `choose` / `range_lookup` / `bracket_fold` | yes | yes | yes | yes | yes | yes |
| `round` | required `value, mode, stage`; `stage` enum `source, after_aggregate, final` | `stage` **removed**; `{op, value, mode}` | same | same | same | same |
| `categorical_compare` / `category_literal` | — | added | same | same | same | same |
| `require_closed` | — | added `{op, source_set}` | same | same | same | same |
| `conditional_dependency_set` | — | — | added; members are `ref_expr` only | same | same | same |
| `count` | — | — | — | added `{op, name, source_set}` | same | same |
| `block` | — | — | — | added `{op, code}` regex `^[A-Z][A-Z0-9_]+$` | same | same |
| `multiply` | — | — | — | — | — | `{op, left, right}` |
| `divide` | — | — | — | — | — | `{op, left, right, min_decimal_places, rounding}` with rounding enum `half_up, half_even, down, up` |
| `collect_categorical_all_equal` | — | — | — | — | — | `{op, name, value}` |
| top-level `pins` | absent (not required) | required | required | required | required | required |
| top-level `accounts_for` | — | — | — | — | added; relationships `composes_line, itemizes_members, reads_subtotal` | **removed** — v6 properties have no `accounts_for` |

Citations: v1 ops at `rule-artifact.v1.schema.json:54-185`; v2 minified
oneOf at `rule-artifact.v2.schema.json:13-26`; v3
`conditional_dependency_set` at `rule-artifact.v3.schema.json:45`; v4 `count`
`:33`, `block` `:34`; v5 `accounts_for` `:87-123` (present, not in
`required`); v6 `multiply` `:38`, `divide` `:39`,
`collect_categorical_all_equal` `:50`. v6 required list at `:22` matches v2–v4
and does not include `accounts_for`.

### Operation-semantics series — not a containment succession

`operation-semantics.v1` operation enum is `round, range_lookup, bracket_fold`
(`operation-semantics.v1.schema.json:9`).
`operation-semantics.v2` operation enum is `categorical_compare, require_closed`
(`operation-semantics.v2.schema.json:4`). v2 does not contain v1's three
operations. Highest-numbered is not a superset of earlier meaning.

v1 `round` spec modes enum `half_up, half_even, down, up` at `:26`;
`tie_break` `away_from_zero, to_even, toward_zero` at `:42`; stages
`source, after_aggregate, final`. `range_lookup` / `bracket_fold` `on_miss`
enum `block, zero` at `:59` and `:82`; boundary enum
`lower_inclusive_upper_exclusive, lower_exclusive_upper_inclusive`.
v2 `categorical_compare.spec.domain_mismatch` is const `block`;
`require_closed.spec.admission` is const `current-literal-true`.

v2's own description (`operation-semantics.v2.schema.json:3`) states
"Evaluation and dispatch are not implemented by this schema (ADR-0025
decision 5; ADR-0026 decision 5)."

### Block-code enums — three closed lists, not one

The rule-artifact `blocked.code` field and the `block` op's `code` are a
**pattern**, not an enum: `^[A-Z][A-Z0-9_]+$`
(`rule-artifact.v1.schema.json:24`; `rule-artifact.v4.schema.json:34`).
Closed named vocabularies live on produced-record citizens and drift
separately:

| Series | Codes |
| --- | --- |
| `npe-walk.v1` `$defs/node.properties.code` | `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_OPEN`, `VALUE_INVALID` |
| `npe-walk.v2` | `SOURCE_SET_OPEN` → `SOURCE_SET_UNCLOSED`; adds `ITEMIZATION_TIE_OUT_VIOLATION` |
| `npe-walk.v3` | v2 plus `COMPLETENESS_VALUE_VIOLATION` |
| `derivation-record.v2` `$defs/disposition.properties.code` | same five as npe-walk.v1 including `SOURCE_SET_OPEN` |
| `derivation-record.v3` | same rename/add as npe-walk.v2 |
| `derivation-record.v4` | plus `COMPLETENESS_VALUE_VIOLATION` (matches npe-walk.v3) |
| `derivation-record.v5` | plus `MULTIPLE_F1098_OUT_OF_SCOPE` |
| `derivation-record.v6` | plus `F1098_SCOPE_CONTRADICTION` |
| `derivation-record.v7` | plus `SLI_MFS_INELIGIBLE`, `SLI_UNIVERSAL_COMPONENT_VIOLATION`, `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` (`:124-135`) |
| `form-field.v2` `$defs/blocked_instruction.codes` items | `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_OPEN` |
| `form-field.v3` | `SOURCE_SET_OPEN` → `SOURCE_SET_UNCLOSED` only — no itemization/completeness/F1098/SLI codes |

There is no npe-walk.v4..v7 matching derivation-record.v5..v7. ADR-0020
decision 7 (`docs/adr/0020-non-publication-explanation-walking.md:51`) says
walk-payload dispositions use the ADR-0012 vocabulary "exactly" and that
"`invalid` is layered as a refinement of blocked." No `npe-walk.v1..v3`
`node_kind` enum contains `invalid`. The four kinds are `published`,
`blocked`, `guard_inapplicable`, `no_disposition_recorded`.

### Artifact-package admitted_schemas (additive except one drop)

v1 has no `admitted_schemas`. v2 introduces it. Subsequent versions add
citizen generations. The one **drop**: v10 adds `attachment-rule.v5` and
**removes** `quantity-vocabulary.v5`; v12 restores `quantity-vocabulary.v5`.

v25 `admitted_schemas.items.enum` has **42** names. It includes
`rule-artifact.v2..v6` and `operation-semantics.v2`. It does **not** include
`rule-artifact.v1` or `operation-semantics.v1`. Checked: no
`artifact-package.v1..v25` `admitted_schemas` enum contains
`rule-artifact.v1`.

Member roles grow: v4 adds `dividend-universe`, `attachment-rule`; v5 adds
`checked-conclusion-binding`; v23 adds `migration-artifact`.

### Attachment-rule series (no v7)

Published files, from `packages/schemas/tax/published.json` and the
directory: v1, v2, v3, v4, v5, v6, v8. Seven files. No v7.

| Version | `$id` / `schema` const | What the description says it adds |
| --- | --- | --- |
| v1 | `tax/attachment-rule.v1` | triad dispositions; threshold requirement; `collect_members`; presence completeness (ADR-0036) |
| v2 | `.v2` | `itemization_authority` `single_family` \| `composition`; `row_set` |
| v3 | `.v3` | `requirement` oneOf: existing threshold **or** `kind: family_nonempty` (ADR-0053) |
| v4 | `.v4` | `required_answer` oneOf: `check: presence` **or** `check: value` with `equals` (ADR-0055) |
| v5 **filename** | **`$id` is `tax/attachment-rule.v3`** (`attachment-rule.v5.schema.json:120`); `properties.schema.const` is `attachment-rule.v3` (`:229`) | typed `adjustment_row`; title "typed subtractive adjustment rows" |
| v6 | `.v6` | same title family as v5; own `$id` |
| v8 | `.v8` | adds `accounts_for` with the same three relationships as rule-artifact.v5 |

v5's bytes are **not** v3's bytes (SHA-256
`aecd3bf51c16fac9162afd06073627bd942bebd2d95c68ab78191a4017691780` vs
`5b3f219879095db24cab90e7b9bfdcf3b6555a022697299230eec94490099cab`, matching
`published.json`). Two published files therefore share `$id`
`tax/attachment-rule.v3` and instance discriminator `attachment-rule.v3`.

v3/v4 `requirement` admits `family_nonempty`. v5/v6/v8 `requirement` as
parsed is the **threshold-only** object (const `strictly_greater_than`),
not the v3 oneOf. v4's `check: value` does not appear in v5/v6/v8
`required_answer` (those are const `presence`). Later filenames are not
supersets of earlier requirement/completeness shapes.

### Source-family term/predicate (v2 only)

`source-family.v1` has no `$defs/term` or `$defs/predicate`.
`source-family.v2` adds `member_constraints` (`:66`), `identity_exclusivity`
(`:97`), `projects_from` (`:141`), and `$defs` at `:171`: `term` at `:172`,
`predicate` at `:278`. Track 0's line citations for those four anchors
reproduce.

Term ops (`const`): `field`, `literal`, `add`, `subtract`, `floor_zero`.
Predicate ops (`const`): `field_present`, `field_absent`, `field_equals`,
`field_not_equals`, `compare` (comparison enum `gt, ge, lt, le, eq, ne` —
**`ge`/`le`, not the rule-artifact `gte`/`lte`**), `all`, `any`.
No `not`. Recursive `$ref` on `term` and `predicate` is unbounded in JSON
Schema. ADR-0066 decision 2 names depth six in prose and says JSON Schema
is not claimed to enforce it
(`docs/adr/0066-declarative-structured-validation-and-consumer-closure.md:54-56`; the clause "greater than six" is on line 55).

### Quantity-vocabulary enums are not monotone

`quantity-vocabulary.v1..v12` each close an items-enum. Additions are not
the whole story: v7 **drops** `exempt-interest-dividends` while adding six
`covered-w-*` names; v8 **drops** those six and restores
`exempt-interest-dividends` plus `tax-exempt-interest`; v9 **drops**
`tax-exempt-interest` and adds `unemployment-compensation`; v11 restores
`tax-exempt-interest`. Highest-numbered is not a union of earlier enums.

v12 enum (20 names): `capital-gain-distributions`, `covered-lt-basis`,
`covered-lt-proceeds`, `covered-ltcg-basis`, `covered-ltcg-proceeds`,
`covered-st-basis`, `covered-st-proceeds`, `exempt-interest-dividends`,
`foreign-tax-paid`, `income-tax`, `ira-distributions`, `ordinary-dividends`,
`qualified-dividends`, `social-security-benefits`, `standard-deduction`,
`tax-exempt-interest`, `taxable-income`, `taxable-interest`,
`unemployment-compensation`, `wages`.

### Dividend-universe box sets

| Version | composable `box` enum | recorded-non-composable |
| --- | --- | --- |
| v1 | `1a, 1b` | `2a, 3, 5, 7, 12` |
| v2 | `1a, 1b, 2a` | `3, 5, 7, 12` |
| v3 | `1a, 1b, 2a, 12` | `3, 5, 7` |
| v4 | `1a, 1b, 2a, 12, 7` | `3, 5` |

## Census records

108 constructs. IDs are `D-001` .. `D-108`.

---

### Surface 1 — core clause / expression language (grammar proper)

#### D-001 — rule-artifact guarded clause

- **layer:** 1, proper
- **accepted syntax:** object with required `schema, id, version, scope, role, requires, when, value, publishes, blocked`. v1 at `rule-artifact.v1.schema.json:7-32`. v2+ additionally require `pins` (`rule-artifact.v2.schema.json:6`). `additionalProperties: false` on every version parsed.
- **source of authority:** ADR-0006 decision 1 (`docs/adr/0006-rule-artifact-language.md:15`); schema description at `rule-artifact.v1.schema.json:5`.
- **separately versioned:** yes — `rule-artifact.v1..v6`. No single current version is named in any schema; Track 0 records runtime acceptance of all six. This layer is silent on runtime.
- **declared evaluation / blocking / invalidity / nonpublication:** one clause publishes exactly one symbol or is blocked with a declared code and missing-symbol list (ADR-0006 d1, d8). Guard-false handling is not in this schema; see D-045.
- **semantic effect:** "All tax meaning in this system will live in rule artifacts" is ADR-0006 context, not a schema field. The schema describes one guarded single-publication clause.
- **input/output domains:** `when`/`value` are `$defs/expr`; `publishes` is a string symbol. The schema does not constrain which fact-type ids a `ref` may name (Track 0 gap 5; this reading agrees — no `fact-type` `$ref` inside `rule-artifact.vN` `$defs/expr`).
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that v6 is "the" language; that v1 is unreadable by a package (packages' `admitted_schemas` are a different citizen — D-047).

#### D-002 — `role` (rule-artifact)

- **layer:** 1 / 2, proper
- **accepted syntax:** enum `computation, applicability, field-mapping, cross-form-bridge` on every `rule-artifact.v1..v6` (`rule-artifact.v1.schema.json:12`; same four tokens in v6 `:11`).
- **source of authority:** ADR-0006 decisions 1 and 9 (`0006-rule-artifact-language.md:15,23`).
- **separately versioned:** the enum does not change across v1–v6. Package member roles (D-049) are a larger closed set.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent on per-role evaluation differences. The schema distinguishes them by token only.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that package member `role` and rule-artifact `role` are the same enum. They share four tokens and the package adds others.

#### D-003 — `requires`

- **layer:** 2, proper
- **accepted syntax:** array of unique nonempty strings (`rule-artifact.v1.schema.json:13-17`). Required field on every version.
- **source of authority:** ADR-0006 d1.
- **separately versioned:** shape unchanged v1–v6.
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0006 d8: open elective facts block with schema'd codes; distinguish dependency-absent from dependency-present-but-invalid. The `requires` field itself does not enum those codes.
- **status:** pending-reconciliation

#### D-004 — `when` (applicability guard)

- **layer:** 2, proper
- **accepted syntax:** `$ref: #/$defs/expr` (`rule-artifact.v1.schema.json:18`). Required.
- **source of authority:** ADR-0006 d1; ADR-0024 d1 (guards as the conditional mechanism).
- **separately versioned:** field identity stable; the expr vocabulary under it drifts (table above).
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0020 decision 1a step 3: a genuinely false guard yields ledger `inapplicable` with a real `guard_result`. Schema of `when` does not mention `guard_result`.
- **status:** pending-reconciliation

#### D-005 — `value` (expression tree)

- **layer:** 1, proper
- **accepted syntax:** `$ref: #/$defs/expr`. `$defs/expr` is a `oneOf` of an untyped literal plus closed op objects. v1 has 15 oneOf arms (`rule-artifact.v1.schema.json` `$defs.expr`); v6 has 21.
- **source of authority:** ADR-0006 d2 (closed schema-enumerated operation vocabulary); d3 (per-operation required-field constraints are the runtime authority). Extensions: ADR-0025, ADR-0037, ADR-0064.
- **separately versioned:** yes, per rule-artifact schema generation.
- **declared evaluation / blocking / invalidity / nonpublication:** an operation with absent operands is a validation failure, not tolerated input (`rule-artifact.v1.schema.json:5`).
- **status:** pending-reconciliation

#### D-006 — `publishes`

- **layer:** 1 / 2, proper
- **accepted syntax:** nonempty string (`rule-artifact.v1.schema.json:20`). Exactly one output symbol per clause (ADR-0006 d1).
- **source of authority:** ADR-0006 d1, d7 (unique output ownership is package-enforced).
- **separately versioned:** unchanged v1–v6.
- **declared evaluation / blocking / invalidity / nonpublication:** two members publishing the same symbol are a package contract matter (D-054), not a rule-artifact field.
- **status:** pending-reconciliation

#### D-007 — `blocked` (declared field on the clause)

- **layer:** 2, proper
- **accepted syntax:** object `{code, missing}`; `code` pattern `^[A-Z][A-Z0-9_]+$`; `missing` array of nonempty strings; both required (`rule-artifact.v1.schema.json:21-28`). Unchanged through v6.
- **source of authority:** ADR-0006 d1, d8.
- **separately versioned:** field shape is not; the closed code lists live on other families (drift table).
- **declared evaluation / blocking / invalidity / nonpublication:** this is the clause's declared block payload shape. It does not enum `DEPENDENCY_ABSENT` etc.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that a rule-artifact instance is schema-invalid if its `blocked.code` is a string absent from `derivation-record.v7`'s enum. The rule-artifact schema would accept it.

#### D-008 — `scope`

- **layer:** 1, proper
- **accepted syntax:** `$defs/scope`: required `tax_year` (integer), `jurisdiction`, `family`; optional `effective_from` date (`rule-artifact.v1.schema.json` `$defs.scope`).
- **source of authority:** ADR-0006 d6 (scope as content; year and jurisdiction never live in artifact ids).
- **separately versioned:** unchanged across rule-artifact v1–v6.
- **status:** pending-reconciliation

#### D-009 — `notes`

- **layer:** 1, proper (optional field)
- **accepted syntax:** optional string (`rule-artifact.v1.schema.json:30`). Not required.
- **source of authority:** schema only. No accepted ADR decision was found that assigns `notes` evaluation or publication meaning.
- **separately versioned:** present v1–v6.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent.
- **status:** pending-reconciliation

#### D-010 — `pins` (rule-artifact)

- **layer:** 1 / 7, proper
- **accepted syntax:** v2+ required array of `$defs/pin`. Pin: required `role, id, version`; `origin` required **iff** `role` is `input` (`rule-artifact.v2.schema.json:10`). Role enum: `parameter, input, choice, default, composition, citation, operation-semantics`. Origin enum: `assertion, declared_default`.
- **source of authority:** ADR-0007 d3 (role-bearing pins); ADR-0025 PC1 (`origin` required and copied transitively); ADR-0025 d2 (`assertion` vs `declared_default`).
- **separately versioned:** absent in v1; required v2–v6 with the same role enum.
- **declared evaluation / blocking / invalidity / nonpublication:** composition and citation pins are "provenance metadata only; only input and choice pins are derivation edges" (`rule-artifact.v2.schema.json:3`; ADR-0025 / 0026 / 0029 cited there).
- **provenance that survives execution:** pin roles are the attribution chain (ADR-0007 d3, ADR-0009 d1).
- **status:** pending-reconciliation

#### D-011 — `composition` and `citations` (rule-artifact metadata)

- **layer:** 1, proper (optional)
- **accepted syntax:** v2+ optional `composition` (`$defs/exact_pin`) and `citations` (array). Not in v1. Not required in v2–v6.
- **source of authority:** schema description at `rule-artifact.v2.schema.json:3`; ADR-0026 / 0029 as cited there.
- **separately versioned:** added in v2; still present in v6.
- **declared evaluation / blocking / invalidity / nonpublication:** declared as provenance metadata, not derivation edges.
- **status:** pending-reconciliation

#### D-012 — `accounts_for` (rule-artifact.v5 only)

- **layer:** 1 / 4, proper
- **accepted syntax:** optional array of `{relationship, family}`; relationship enum `composes_line, itemizes_members, reads_subtotal`; `family` is `$defs/exact_pin` (`rule-artifact.v5.schema.json:87-123`). **Not in `required`.** **Absent from v6 properties.**
- **source of authority:** ADR-0066 decision 5 (`0066-…md:74-79`): closed relationships; they record author intent and must agree with reachability-derived constrained-family set; they do not create or remove graph edges.
- **separately versioned:** appears in v5; not carried into v6. v6 title is the multiply/divide extension (ADR-0064), not an accounts_for continuation.
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0066 d6: missing or extra `accounts_for` is a package-validation rejection before a run can start. That sentence is about the production package boundary, not about this field's presence on a v6 rule.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that v6 rules may declare `accounts_for` (v6 `additionalProperties: false` and no such property). Whether attachment-rule.v8's `accounts_for` (D-066) is the v6 continuation is a question for another layer.

#### D-013 — untyped literal (expr arm 0)

- **layer:** 1, proper
- **accepted syntax:** `type: [string, number, boolean, null]` as the first `oneOf` of `$defs/expr` in every rule-artifact version (`rule-artifact.v1.schema.json` expr oneOf[0]).
- **source of authority:** schema only. ADR-0006 d2 talks about a closed operation vocabulary; it does not name bare literals as an op.
- **separately versioned:** unchanged.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent on coercion of literals.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that a literal `null` has a declared numeric or boolean meaning.

#### D-014 — `ref`

- **layer:** 1, proper
- **accepted syntax:** `{op: "ref", name}` both required; `additionalProperties: false`. v1 `:54-` ; v3+ `$defs/ref_expr` (`rule-artifact.v3.schema.json:28`).
- **source of authority:** schema. ADR-0006 d2 (closed ops). No accepted ADR decision was found that states what `name` binds to (symbol vs fact-type vs finding).
- **separately versioned:** shape stable; from v3 it is also the only legal member of `conditional_dependency_set.members`.
- **input/output domains:** `name` is a nonempty string. No schema link to `fact-type`.
- **status:** pending-reconciliation

#### D-015 — `collect`

- **layer:** 1, proper
- **accepted syntax:** `{op: "collect", name, source_set?}`. v1 required `[op, name]` with optional `source_set` (`rule-artifact.v1.schema.json:63-65`). v2+ required `[op, name, source_set]` (`rule-artifact.v2.schema.json:14`).
- **source of authority:** schema. ADR-0064 consequences text (`0064-…md:36-41`) describes `collect` as numeric aggregation — that paragraph is consequences of a later ADR, not a v1 decision, and it refers to evaluator coercion. This stream records the schema shape and that ADR-0064 treats `collect` as distinct from `collect_categorical_all_equal`. It does not adopt the evaluator sentence as declared evaluation.
- **separately versioned:** source_set optionality changes v1 → v2.
- **status:** pending-reconciliation

#### D-016 — `count`

- **layer:** 1, proper
- **accepted syntax:** `{op: "count", name, source_set}` all required (`rule-artifact.v4.schema.json:33`; same v5 `:285-299`, v6 `:33`).
- **source of authority:** schema only from v4. No accepted ADR decision was found that names `count` as a member of the closed operation vocabulary.
- **separately versioned:** v4+ only.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent.
- **status:** pending-reconciliation

#### D-017 — `block` (expression op)

- **layer:** 1 / 2, proper
- **accepted syntax:** `{op: "block", code}` with `code` pattern `^[A-Z][A-Z0-9_]+$` (`rule-artifact.v4.schema.json:34`).
- **source of authority:** schema only from v4. Distinct from the top-level `blocked` field (D-007). No accepted ADR decision was found that names this op.
- **separately versioned:** v4+.
- **declared evaluation / blocking / invalidity / nonpublication:** the schema admits an arbitrary matching code string. It does not say the evaluator must halt, must emit a ledger row, or must use that code as `disposition.code`.
- **status:** pending-reconciliation

#### D-018 — `parameter`

- **layer:** 1, proper
- **accepted syntax:** `{op: "parameter", parameter_id, key?}` ; required `op, parameter_id`; `key` is optional expr (`rule-artifact.v1.schema.json:73`).
- **source of authority:** ADR-0006 d5 (parameters are separate versioned citizens cited by id; policy values never inline into rules). Citizen shape: D-093.
- **separately versioned:** shape stable v1–v6.
- **status:** pending-reconciliation

#### D-019 — `add`

- **layer:** 1, proper
- **accepted syntax:** v1 `{op: "add", args}` `args` minItems 1. v2+ folded into `op` enum `add, max, all, any` with `args` (`rule-artifact.v2.schema.json:16`).
- **source of authority:** ADR-0006 d2 (closed vocabulary). No ADR states associativity, identity, or type of `args`.
- **separately versioned:** grouping change v1 → v2, not a meaning ADR.
- **status:** pending-reconciliation

#### D-020 — `max`

- **layer:** 1, proper
- **accepted syntax:** same as D-019 (v1 own arm; v2+ shared enum).
- **source of authority:** schema; ADR-0024 d3 mentions explicit `max(0, …)` for clamping at zero.
- **separately versioned:** as D-019.
- **status:** pending-reconciliation

#### D-021 — `all`

- **layer:** 1 / 2, proper
- **accepted syntax:** as D-019.
- **source of authority:** ADR-0024 d1 (`choose`/`all` control expressions); d4 (guard-order: combine eligibility with possibly-absent input by placing the guard first so left-to-right short-circuit skips absent refs). Short-circuit is stated as evaluator behavior in that decision; the schema does not encode evaluation order.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that JSON Schema requires left-to-right evaluation of `args`.

#### D-022 — `any`

- **layer:** 1, proper
- **accepted syntax:** as D-019.
- **source of authority:** schema; ADR-0024 d1 names `choose`/`all`, not `any`.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent on empty-args (schema forbids empty via minItems 1) and on whether any-true short-circuits.
- **status:** pending-reconciliation

#### D-023 — `subtract`

- **layer:** 1, proper
- **accepted syntax:** `{op: "subtract", left, right}` both expr (`rule-artifact.v1.schema.json:92`).
- **source of authority:** schema / ADR-0006 d2.
- **status:** pending-reconciliation

#### D-024 — `multiply`

- **layer:** 1, proper
- **accepted syntax:** `{op: "multiply", left, right}` (`rule-artifact.v6.schema.json:38`).
- **source of authority:** ADR-0064 decisions 1–2 (`0064-…md:15-16`). Additive to v6; not an amendment to ADR-0025.
- **separately versioned:** v6 only.
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0064 does not state divide-by-zero-style errors for multiply. This layer is silent on overflow and type.
- **status:** pending-reconciliation

#### D-025 — `divide`

- **layer:** 1, proper
- **accepted syntax:** required `op, left, right, min_decimal_places, rounding`; `min_decimal_places` integer minimum 0; `rounding` enum `half_up, half_even, down, up` (`rule-artifact.v6.schema.json:39`).
- **source of authority:** ADR-0064 d2: `divide` is categorically distinct from the whole-dollar `round` operator; `min_decimal_places` is a floor on the ratio's precision.
- **separately versioned:** v6 only. Rounding enum tokens match operation-semantics.v1 round *modes* (D-038, D-043) but live on this op, not on an operation-semantics citizen.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent on division by zero.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that `divide.rounding` is dispatched through an `operation-semantics.v1` `round` canon object. The v6 schema puts the enum on the op. operation-semantics.v1's operation enum does not include `divide`.

#### D-026 — `compare`

- **layer:** 1, proper
- **accepted syntax:** `{op: "compare", left, right, cmp}` with `cmp` enum `eq, ne, gt, gte, lt, lte` (`rule-artifact.v1.schema.json:111-114`).
- **source of authority:** schema; ADR-0025 d5: decimal `compare` remains numeric-only and gains no second interpretation.
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0025 d6: statically knowable categorical-vs-numeric comparison is rejected at package validation (`MEMBER_SCHEMA_INVALID`). That issue code is named in the ADR, not in rule-artifact schema.
- **status:** pending-reconciliation

#### D-027 — `not`

- **layer:** 1, proper
- **accepted syntax:** `{op: "not", value}` expr (`rule-artifact.v1.schema.json:140`).
- **source of authority:** schema. ADR-0066 d2 explicitly says the *predicate* language has no `not`. That sentence does not remove this rule-artifact op.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that `not` is available inside `source-family.v2` predicates (it is not; D-082).

#### D-028 — `choose`

- **layer:** 1 / 2, proper
- **accepted syntax:** `{op: "choose", when, then, else}` all expr (`rule-artifact.v1.schema.json:146-150`).
- **source of authority:** ADR-0024 d1.
- **declared evaluation / blocking / invalidity / nonpublication:** schema does not say whether `else` is evaluated when `when` is true.
- **status:** pending-reconciliation

#### D-029 — `range_lookup` (expression form)

- **layer:** 1, proper
- **accepted syntax:** `{op: "range_lookup", table_id, key, value}` (`rule-artifact.v1.schema.json:157-163`). `table_id` string; `key`/`value` expr.
- **source of authority:** ADR-0006 d4 (meaning is not the enum name; it lives in a versioned semantic specification — D-039).
- **separately versioned:** expr shape stable v1–v6; `stage` is not on this op. Semantics citizen is `operation-semantics.v1`.
- **declared evaluation / blocking / invalidity / nonpublication:** miss behavior is declared on the semantics citizen (`on_miss`: `block` or `zero`), not on the expr node.
- **status:** pending-reconciliation

#### D-030 — `bracket_fold` (expression form)

- **layer:** 1, proper
- **accepted syntax:** `{op: "bracket_fold", table_id, key, value}` (`rule-artifact.v1.schema.json:168-174`).
- **source of authority:** ADR-0006 d4; ADR-0024 d3 (canon row shape `lower/upper/rate`, lower-inclusive/upper-exclusive, clamp at zero via explicit `max`).
- **declared evaluation / blocking / invalidity / nonpublication:** as D-040.
- **status:** pending-reconciliation

#### D-031 — `round` (expression form)

- **layer:** 1 / 6iii, proper
- **accepted syntax:** v1 required `{op, value, mode, stage}` with `stage` enum `source, after_aggregate, final` (`rule-artifact.v1.schema.json:179-185`). v2+ `{op, value, mode}` only (`rule-artifact.v2.schema.json:26`) — **`stage` dropped**. `mode` is an expr, not the modes enum.
- **source of authority:** ADR-0006 d4; operation-semantics.v1 round spec (D-038, D-043).
- **separately versioned:** yes, both the expr shape and the semantics citizen.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that v2+ round still carries a declared stage. The v1 enum is gone from the expr. Stages remain in the *semantics* citizen's `spec.stages`.

#### D-032 — `categorical_compare` (expression form)

- **layer:** 1, proper
- **accepted syntax:** `{op: "categorical_compare", left, right, cmp}` with `cmp` enum `eq, ne` only (`rule-artifact.v2.schema.json:19`).
- **source of authority:** ADR-0025 d5–d6 (`0025-…md:64-80`).
- **separately versioned:** v2+ expr; semantics in `operation-semantics.v2` (D-041).
- **declared evaluation / blocking / invalidity / nonpublication:** run-time assertion outside the declared enum blocks `DEPENDENCY_INVALID`; domain mismatch blocks `CATEGORICAL_DOMAIN_MISMATCH`; no coercion, fallback, or repair (ADR-0025 d6). Semantics citizen const `domain_mismatch: "block"`.
- **status:** pending-reconciliation

#### D-033 — `category_literal`

- **layer:** 1, proper
- **accepted syntax:** `{op: "category_literal", fact_type, value}` with `fact_type` `$defs/exact_pin` and `value` nonempty string (`rule-artifact.v2.schema.json:20`).
- **source of authority:** ADR-0025 d5 (typed literal naming the fact type).
- **separately versioned:** v2+.
- **status:** pending-reconciliation

#### D-034 — `require_closed` (expression form)

- **layer:** 1 / 2, proper
- **accepted syntax:** `{op: "require_closed", source_set}` (`rule-artifact.v2.schema.json:23`).
- **source of authority:** ADR-0026 decision 5 (`docs/adr/0026-taxable-interest-composition-and-line-2b.md:23`); operation-semantics.v2 `require_closed` spec (D-042).
- **declared evaluation / blocking / invalidity / nonpublication:** semantics `subject: source_set`, `admission: current-literal-true`. ADR-0026 says a generic operation whose tax meaning comes only from the declared source set, reusing ADR-0014 current-horizon / current-literal-true admission. Block code names for an open set live on record/walk vocabularies (`SOURCE_SET_OPEN` then `SOURCE_SET_UNCLOSED`), not on this expr node.
- **status:** pending-reconciliation

#### D-035 — `conditional_dependency_set`

- **layer:** 1 / 2, proper
- **accepted syntax:** `{op: "conditional_dependency_set", condition, members}`; `members` nonempty unique array of `$defs/ref_expr` only (`rule-artifact.v3.schema.json:45`). **v3 only in the title; present v3–v6.** ADR-0037 production condition 1: members non-empty and ref-only — the schema encodes that.
- **source of authority:** ADR-0037 decisions 1–4 (`0037-…md:30-56`). Schema title on v3–v5: "Rule artifact with conditional multi-dependency eligibility."
- **separately versioned:** v3+ (the plan/charter example of v3 vs later is real: the op does not exist in v1/v2).
- **declared evaluation / blocking / invalidity / nonpublication:** evaluator reads condition first; if false, node succeeds and evaluates no member; if true, evaluates each member once and accumulates every dependency-absence; any absence stops that rule with the existing dependency-absent category and the complete ordered absent-member list; non-absence errors retain ordinary behavior; if all present, node succeeds (ADR-0037 d2). Inactive members are neither evaluated nor pinned (d3). Explanation carries all and only accumulated missing members through existing dependency-absence and missing-list surfaces; no opaque multi-missing error code (d4).
- **provenance that survives execution:** published finding pins the condition and all active members through existing derivation edges (d3).
- **status:** pending-reconciliation

#### D-036 — `collect_categorical_all_equal`

- **layer:** 1, proper
- **accepted syntax:** `{op: "collect_categorical_all_equal", name, value}` (`rule-artifact.v6.schema.json:50`).
- **source of authority:** ADR-0064 d3 (`0064-…md:17`).
- **separately versioned:** v6 only.
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0064 d3: read every current finding for a fact type from marshalled source rows and require all of them to match an expected category; order-independent. The schema does not name a block code for disagreement.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that this is a mode of `collect` (ADR-0064 explicitly rejects that).

---

### Surface 3 — operation-semantics (grammar proper) and 6iii rounding

#### D-037 — operation-semantics citizen

- **layer:** 3, proper
- **accepted syntax:** `{schema, operation, version, spec}` required; `additionalProperties: false`. Two schema generations with **disjoint** `operation` enums (drift table).
- **source of authority:** ADR-0006 d4; v1 description at `operation-semantics.v1.schema.json:5` ("the authority for evaluator behavior — the runner conforms to canon, canon does not describe the runner").
- **separately versioned:** yes, as its own family *and* each instance has a `version` field. Two independent axes, as Track 0 warned.
- **declared evaluation / blocking / invalidity / nonpublication:** v2 description disclaims that evaluation and dispatch are implemented by that schema.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that `operation-semantics.v2` supersedes or contains v1.

#### D-038 — `round` semantics spec

- **layer:** 3 / 6iii, proper
- **accepted syntax:** when `operation` const `round`, `spec` requires `modes, stages, tie_break, unit` (`operation-semantics.v1.schema.json:17-45`). `modes` items enum `half_up, half_even, down, up` (`:26`). `stages[].name` enum `source, after_aggregate, final`. `tie_break` enum `away_from_zero, to_even, toward_zero`. `unit` pattern `^[0-9]+(\.[0-9]+)?$`.
- **source of authority:** ADR-0006 d4.
- **separately versioned:** the spec lives only in `operation-semantics.v1`, not v2.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent on which Python rounding constant a mode name denotes. The schema names the tokens.
- **status:** pending-reconciliation

#### D-039 — `range_lookup` semantics spec

- **layer:** 3, proper
- **accepted syntax:** `spec` requires `boundary, on_miss, row_shape` (`operation-semantics.v1.schema.json:52-66`). `on_miss` enum `block, zero`. `row_shape` items enum `lower, upper, value`.
- **source of authority:** ADR-0006 d4.
- **declared evaluation / blocking / invalidity / nonpublication:** `on_miss: block` vs `zero` is declared here. No block-code token is named.
- **status:** pending-reconciliation

#### D-040 — `bracket_fold` semantics spec

- **layer:** 3, proper
- **accepted syntax:** `spec` requires `method, boundary, open_top, on_miss, row_shape` (`operation-semantics.v1.schema.json:73-89`). `method` enum is only `marginal`. `row_shape` items `lower, upper, rate`. `open_top` boolean. `on_miss` `block` \| `zero`.
- **source of authority:** ADR-0006 d4; ADR-0024 d3.
- **status:** pending-reconciliation

#### D-041 — `categorical_compare` semantics spec

- **layer:** 3, proper
- **accepted syntax:** `operation-semantics.v2` when operation const `categorical_compare`: `spec.operators` const `["eq","ne"]`; `spec.domain_mismatch` const `block` (`operation-semantics.v2.schema.json:6`).
- **source of authority:** ADR-0025 d5–d6.
- **separately versioned:** v2 only.
- **status:** pending-reconciliation

#### D-042 — `require_closed` semantics spec

- **layer:** 3, proper
- **accepted syntax:** `spec.subject` const `source_set`; `spec.admission` const `current-literal-true` (`operation-semantics.v2.schema.json:7`).
- **source of authority:** ADR-0026 d5; ADR-0014 admission vocabulary (D-092).
- **status:** pending-reconciliation

#### D-043 — rounding-mode tokens (`half_up` / `half_even` / `down` / `up`)

- **layer:** 6iii, proper (Track 0 reversed this row onto the same citizen as surface 3)
- **accepted syntax:** enum on `operation-semantics.v1` round `spec.modes` items (`:26`) **and** on `rule-artifact.v6` `divide.rounding` (`:39`). Two sites, same four tokens.
- **source of authority:** ADR-0006 d4 for the round canon; ADR-0064 d2 for divide's copy of the tokens.
- **separately versioned:** round modes live on operation-semantics.v1; divide's rounding lives on rule-artifact.v6. Nothing in either schema `$ref`s the other.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent on Decimal mapping.
- **status:** pending-reconciliation

---

### Surface 2 — guard / applicability / publication / blocking (remaining)

#### D-044 — ledger classification order (published / blocked / inapplicable)

- **layer:** 2 / 7, proper
- **accepted syntax:** `derivation-record.v2+` `$defs/disposition.properties.disposition` enum `published, blocked, inapplicable`. v1 instead has top-level `published` and `blocked` arrays (`derivation-record.v1.schema.json:16-29`) plus a description that inapplicable carries `guard_result` (`:5`).
- **source of authority:** ADR-0020 decisions 1 and 1a (`0020-…md:24-32`); ADR-0008 for record placement.
- **separately versioned:** v1 arrays vs v2+ ledger. Track 0 names `CURRENT_RECORD_SCHEMA = "derivation-record.v7"` at `packages/derivation/records.py:40` as the one committed current-version constant in this layer. That constant is code; the published schemas for v1–v7 all still exist.
- **declared evaluation / blocking / invalidity / nonpublication:** classification order (ADR-0020 d1a): (1) any declared dependency absent → `blocked` even if a sibling already published the symbol; (2) else if the output symbol is already published under ADR-0006 d7 conflict semantics → `inapplicable` as unselected conflict-loser with `superseded_by`, not a synthetic `guard_result`; (3) else evaluate guard/value: `published`, or `inapplicable` with real `guard_result`, or `blocked` for a value error. `guard_result` is required only for step-3 inapplicable.
- **provenance that survives execution:** the ledger is the single authoritative disposition surface (ADR-0020 d1). v2 description: any legacy blocked read model is derived by consumers and is not stored (`derivation-record.v2` title/description).
- **status:** pending-reconciliation

#### D-045 — guard-false → inapplicable / `guard_inapplicable`

- **layer:** 2 / 7, proper
- **accepted syntax:** ledger token `inapplicable`; walk-payload token `guard_inapplicable` (`npe-walk.v1` `$defs/node.properties.node_kind`). ADR-0020 vocabulary-layering (`0020-…md:13-20`) maps ledger `inapplicable` → payload `guard_inapplicable`.
- **source of authority:** ADR-0020 d7; ADR-0012 d4 class 5 (`0012-…md:61-62`); ADR-0024 d7 (itemization override makes the standard-deduction rule guard-inapplicable; downstream rules block on the missing dependency rather than inventing a zero).
- **separately versioned:** mapping is ADR-fixed; walk schema carries `guard_inapplicable` in v1–v3.
- **status:** pending-reconciliation

---

### Surface 4 — package selection / binding / closure (grammar proper)

#### D-046 — artifact-package citizen

- **layer:** 4, proper
- **accepted syntax:** v1 required `schema, id, version, scope, members` (`artifact-package.v1`). v2+ required `schema, id, version, scope, admitted_schemas, members, input_bindings, entrypoints, composition_obligations, package_checksum` (`artifact-package.v2` required list). `conflict_semantics` is a property in v1–v25 but **not** in `required`.
- **source of authority:** ADR-0006 d6–d7; ADR-0027 d1 (adopted content unit is the package, generation v2).
- **separately versioned:** `artifact-package.v1..v25` (25 files, contiguous). Independent of package *instance* `version` (Track 0 two-axes note).
- **declared evaluation / blocking / invalidity / nonpublication:** unadmitted schema generations reject at load (ADR-0027 d3). Exclusive execution projection: after adoption, derivation operates only on the resolved member graph (ADR-0027 d7).
- **status:** pending-reconciliation

#### D-047 — `admitted_schemas`

- **layer:** 4, proper
- **accepted syntax:** v2+ array whose items are a closed enum of schema identifiers. v25 enum has 42 entries (listed in the drift section).
- **source of authority:** ADR-0027 d3.
- **separately versioned:** the enum grows (and once shrinks) per package schema generation.
- **declared evaluation / blocking / invalidity / nonpublication:** unadmitted generations reject at load; no silent skip.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that every published `rule-artifact` or `operation-semantics` generation is package-admissible. v1 of each is published and is absent from every `admitted_schemas` enum parsed.

#### D-048 — `members` / member pin

- **layer:** 4, proper
- **accepted syntax:** v2 `$defs/member`: required `role, schema, id, version`. Member `schema` enum is the same closed set as `admitted_schemas` in that generation. v1 members are `$defs/pin` with a different, larger role enum including `adoption, governance, engine, package`.
- **source of authority:** ADR-0027 d2 (closed shared vocabulary; role canon).
- **separately versioned:** role and schema enums grow (drift table).
- **status:** pending-reconciliation

#### D-049 — member `role` tokens (package)

- **layer:** 4, proper
- **accepted syntax:** v25 member role enum: `parameter, computation, applicability, field-mapping, cross-form-bridge, form-field, source-family, source-closure-mapping, composition, fact-type, fact-type-bundle, citation, operation-semantics, dividend-universe, attachment-rule, checked-conclusion-binding, migration-artifact`.
- **source of authority:** ADR-0027 d2; ADR-0028 for fact-type/bundle; later ADRs add attachment-rule / dividend-universe / migration-artifact / checked-conclusion-binding as admitted kinds.
- **separately versioned:** yes, per artifact-package generation. Immutable meaning of a token is supposed to live in `role-canon.v1` (D-098).
- **status:** pending-reconciliation

#### D-050 — `input_bindings`

- **layer:** 4, proper
- **accepted syntax:** array of `{symbol, fact_type, mode}` with `mode` enum `required, optional_default` (`artifact-package.v2` `properties.input_bindings`).
- **source of authority:** ADR-0025 d4 (`0025-…md:57-60`).
- **declared evaluation / blocking / invalidity / nonpublication:** `required` blocks on absence; `optional_default` is valid only for the fact-type optional-default contract (D-102). The generic runner supplies no field-name, tax-year, or value policy (ADR-0025 d4).
- **status:** pending-reconciliation

#### D-051 — `entrypoints`

- **layer:** 4, proper
- **accepted syntax:** nonempty unique array of `$defs/member_ref`. Required v2+.
- **source of authority:** ADR-0027 d4 inbound: every member is reachable from declared entrypoints.
- **status:** pending-reconciliation

#### D-052 — `composition_obligations`

- **layer:** 4, proper
- **accepted syntax:** unique array of nonempty strings. Required v2+.
- **source of authority:** schema; ADR-0028 (composition-obligation trigger) as INDEX digest. The field itself is an array of strings; this schema does not `$ref` `taxable-interest-composition`.
- **status:** pending-reconciliation

#### D-053 — `conflict_semantics`

- **layer:** 4, proper
- **accepted syntax:** v1 `{symbol, resolution}` (resolution is a free string). v2+ `{symbol, selected_producer}` with `selected_producer` a member_ref. Optional (not in `required`) on every version parsed.
- **source of authority:** ADR-0006 d7; ADR-0027 d5 (a conflict entry that merely names a symbol without selecting a producer is rejected).
- **separately versioned:** v1 free-string `resolution` vs v2+ `selected_producer` pin.
- **status:** pending-reconciliation

#### D-054 — unique output ownership

- **layer:** 4, proper
- **accepted syntax:** not a schema field of its own. ADR-0006 d7: no two members may publish the same symbol unless the package declares conflict semantics as content. ADR-0027 d5: form-field `binds_symbol` is valid only when exactly one adopted producer is reachable or a conflict-semantics rule selects one.
- **source of authority:** those two decisions.
- **separately versioned:** no; it is ADR prose enforced (the ADR says) by package validation. This layer does not read that validator.
- **status:** pending-reconciliation

#### D-055 — `package_checksum`

- **layer:** 4, proper
- **accepted syntax:** required string on v2+.
- **source of authority:** ADR-0027 d6 (published package `(id, version)` is immutable; adoption compares offered bytes to the published package-instance checksum).
- **status:** pending-reconciliation

---

### Surface 5a — attachment-rule / form-field (grammar proper)

#### D-056 — attachment-rule citizen

- **layer:** 5a, proper
- **accepted syntax:** required `schema, id, version, title, scope, attachment, publishes, requirement, itemizations, completeness` on v1–v8 files parsed. v8 additionally has optional `accounts_for`.
- **source of authority:** ADR-0036 decisions 1–5; successors ADR-0053, ADR-0055, ADR-0066.
- **separately versioned:** seven published files, gap at v7. **Filename v5 declares `$id` / `schema` const of v3** (`attachment-rule.v5.schema.json:120,229`) with different bytes from `attachment-rule.v3.schema.json`.
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0036 d1 triad (D-057). Sibling line rules cannot reference the attachment symbol, so an attachment's block cannot propagate to a line (ADR-0036 d1).
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that `attachment-rule.v5` is a legal instance discriminator. An instance with `"schema": "attachment-rule.v5"` would fail the v5 *file*'s own `const: attachment-rule.v3`. An instance with `"schema": "attachment-rule.v3"` names a discriminator that two published files both claim.

#### D-057 — attachment triad dispositions

- **layer:** 5a / 2, proper
- **accepted syntax:** not an enum field on the attachment-rule citizen. Declared in ADR-0036 d1 and the v1 schema description (`attachment-rule.v1.schema.json` description): *not-required* publishes a walkable inapplicability disposition; *required-and-complete* publishes the whole form content pinned to every consumed fact; *required-and-incomplete* blocks naming each missing contributable fact. No embedded state field.
- **source of authority:** ADR-0036 d1 (`0036-…md:30-40`).
- **separately versioned:** the triad is ADR-fixed; later schema versions add requirement/completeness *shapes*, not a fourth atomic state.
- **status:** pending-reconciliation

#### D-058 — requirement: threshold / `strictly_greater_than`

- **layer:** 5a, proper
- **accepted syntax:** v1/v2 object: required `subtotals, threshold_parameter, comparison, citation`; `comparison` const `strictly_greater_than`. v3/v4: that object as one arm of `requirement.oneOf`. v5/v6/v8: threshold object again (no oneOf in the parsed `requirement`).
- **source of authority:** ADR-0036 d2 (`0036-…md:42-45`): strictly-greater-than the cited threshold; exactly the threshold amount is not over.
- **separately versioned:** yes; v3 widens, later files as parsed do not keep the oneOf.
- **status:** pending-reconciliation

#### D-059 — requirement: `family_nonempty`

- **layer:** 5a, proper
- **accepted syntax:** v3/v4 `requirement.oneOf[1]`: `kind` const `family_nonempty`. v3 description: required when the family is current and closed with at least one member; not required when current and closed-empty; blocked when unclosed.
- **source of authority:** ADR-0053 Decision 1 (cited in `attachment-rule.v3` title/description).
- **separately versioned:** admitted in v3 and v4 schemas; **not** in the parsed v5/v6/v8 `requirement`.
- **declared evaluation / blocking / invalidity / nonpublication:** blocked when unclosed — the description states it. No distinct block-code token is named on that arm.
- **status:** pending-reconciliation

#### D-060 — `collect_members`

- **layer:** 5a, proper
- **accepted syntax:** `$defs/collect_members`: `{op: "collect_members", member_fact_type, source_family}` both pins (`attachment-rule.v1` `$defs`). Not a rule-artifact expr op.
- **source of authority:** ADR-0036 d3 (`0036-…md:47-57`); production condition 4 names it as a new mechanism.
- **separately versioned:** shape stable across the seven files.
- **declared evaluation / blocking / invalidity / nonpublication:** rows pin member findings of the same closed family, same horizon. Tie-out violation is `ITEMIZATION_TIE_OUT_VIOLATION`: hard-fails the attachment derivation only — never publishes a divergent form, never blocks the line (ADR-0036 d3).
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that `collect_members` is in `$defs/expr` of any rule-artifact version (it is not).

#### D-061 — `itemization_authority`

- **layer:** 5a, proper
- **accepted syntax:** v2+ `$defs/itemization_authority` oneOf: `{kind: single_family, source_family}` or `{kind: composition, composition}`.
- **source of authority:** `attachment-rule.v2` description (additive successor to v1).
- **separately versioned:** added v2; present through v8.
- **status:** pending-reconciliation

#### D-062 — completeness: `check: presence`

- **layer:** 5a, proper
- **accepted syntax:** `$defs/required_answer` with `check` const `presence` (v1–v3, v5–v8) plus `symbol` and `fact_type` pin.
- **source of authority:** ADR-0036 d4: completeness is every required answer exists as a current finding; a "no" is a present answer; values are `{yes, no}`, never boolean; branch requirements read values only after presence holds.
- **declared evaluation / blocking / invalidity / nonpublication:** required-and-incomplete blocks naming each missing contributable fact (d1, d4).
- **status:** pending-reconciliation

#### D-063 — completeness: `check: value`

- **layer:** 5a, proper
- **accepted syntax:** v4 `$defs/required_answer` oneOf second arm: `check` const `value` with required `equals`.
- **source of authority:** ADR-0055 Decision 1 (cited in `attachment-rule.v4` description). Record code `COMPLETENESS_VALUE_VIOLATION` on `derivation-record.v4` / `npe-walk.v3`.
- **separately versioned:** v4 schema only, among the seven files parsed.
- **declared evaluation / blocking / invalidity / nonpublication:** present as a current finding but valued other than the declared required value — a completeness violation distinct from absence, never folded into `DEPENDENCY_ABSENT` (`derivation-record.v4` description).
- **status:** pending-reconciliation

#### D-064 — `adjustment_row`

- **layer:** 5a, proper
- **accepted syntax:** `$defs/adjustment_row` on v5/v6/v8: `kind` enum `nominee_distribution, accrued_interest, abp_adjustment`; `sign` const `negative`. Whole-part `tie_out.operation` const `subtract`.
- **source of authority:** schema titles/descriptions ("typed subtractive adjustment rows"). No accepted ADR decision was found that names those three `kind` tokens as a closed language enum (they look tax-content-shaped; the schema still closes them).
- **separately versioned:** v5 file / v6 / v8.
- **status:** pending-reconciliation

#### D-065 — `branch_requirements`

- **layer:** 5a, proper
- **accepted syntax:** `completeness.branch_requirements[]`: `when_answer: {symbol, equals}`; `anyOf` requires `adds_required` or `names_obligations`. Present from v1.
- **source of authority:** ADR-0036 d4 (foreign-account / foreign-trust examples as content instantiating the generic shape).
- **status:** pending-reconciliation

#### D-066 — `accounts_for` (attachment-rule.v8)

- **layer:** 5a / 4, proper
- **accepted syntax:** optional array; relationship enum `composes_line, itemizes_members, reads_subtotal` (`attachment-rule.v8`).
- **source of authority:** ADR-0066 d5 (same closed relationships as rule-artifact.v5).
- **separately versioned:** attachment-rule.v8 only, among the seven files.
- **status:** pending-reconciliation

#### D-067 — form-field citizen

- **layer:** 5a, proper
- **accepted syntax:** v1 required `schema, id, version, form, line, label, description, binds_symbol, citation_ref, dispositions` (`form-field.v1.schema.json:required` via properties `:8-27`). v2/v3 drop `citation_ref` from required; add optional `citation` pin; `citation_ref` is gone.
- **source of authority:** ADR-0012 d1–d3 (`0012-…md:23-50`).
- **separately versioned:** `form-field.v1..v3`. Track 0: no current designation found.
- **declared evaluation / blocking / invalidity / nonpublication:** the field is never a fact, finding, rule, or authoritative store of a rendered value (ADR-0012 d1; schema description `:5`).
- **status:** pending-reconciliation

#### D-068 — form-field disposition classes

- **layer:** 5a / 7, proper
- **accepted syntax:** `dispositions` required object with five keys `published_value, computed_zero, closure_backed_zero, blocked, guard_inapplicable` (`form-field.v1.schema.json:27-35`). v2/v3 keep the five keys; `blocked` becomes `$defs/blocked_instruction` (adds `codes`).
- **source of authority:** ADR-0012 d4 (`0012-…md:51-66`). Schema description `:29` restates: renderer never invents state.
- **declared evaluation / blocking / invalidity / nonpublication:** rendering never turns a block into zero, infers closure from an empty collection, or renders a false guard as a computed blank (ADR-0012 d5). `computed_zero` and `closure_backed_zero` may share a glyph; explanation must preserve lineage (d6).
- **status:** pending-reconciliation

#### D-069 — form-field blocked-code list

- **layer:** 5a / 2, proper
- **accepted syntax:** v2 `codes` items enum `DEPENDENCY_ABSENT, DEPENDENCY_INVALID, CATEGORICAL_DOMAIN_MISMATCH, SOURCE_SET_OPEN`. v3 replaces `SOURCE_SET_OPEN` with `SOURCE_SET_UNCLOSED`.
- **source of authority:** ADR-0025 PC2 (adds `CATEGORICAL_DOMAIN_MISMATCH`); ADR-0036 production condition 3 (the rename), cited in `form-field.v3` description.
- **separately versioned:** v2 vs v3. Does not grow with derivation-record.v4+.
- **status:** pending-reconciliation

#### D-070 — `binds_symbol`

- **layer:** 5a, proper
- **accepted syntax:** nonempty string on every form-field version (`form-field.v1.schema.json:25`).
- **source of authority:** ADR-0012 d3 (one-way presentation content); ADR-0027 d5 (exactly one reachable producer, or selected conflict).
- **status:** pending-reconciliation

---

### Surface 5b — source-family term/predicate language (grammar proper)

#### D-071 — source-family declaration

- **layer:** 5b-i, proper
- **accepted syntax:** v1 required `schema, id, version, title, scope, closure_claim, member_predicate, authorizes_subtotal`. v2 keeps those required and adds optional `member_constraints, identity_exclusivity, projects_from`.
- **source of authority:** ADR-0016 decisions 1–2, 5 (cited in both schema descriptions): exact natural-language closure claim plus canonical member predicate; the named subtotal is the only output closure may authorize.
- **separately versioned:** v1 / v2. Term/predicate exist only on v2.
- **status:** pending-reconciliation

#### D-072 — `member_constraints`

- **layer:** 5b-i, proper
- **accepted syntax:** optional array of `{id, block_code, meaning, violated_when}`; `violated_when` `$ref #/$defs/predicate`; `block_code` pattern `^[A-Z][A-Z0-9_]+$` (`source-family.v2.schema.json:66-95`).
- **source of authority:** ADR-0066 d1 (`0066-…md:35-47`).
- **declared evaluation / blocking / invalidity / nonpublication:** each constraint is evaluated against exactly one current member. Results are current, citable engine publications, content-addressed (d3). `block_code` is an open pattern here, like rule-artifact `blocked.code`.
- **status:** pending-reconciliation

#### D-073 — `identity_exclusivity`

- **layer:** 5b-i, proper
- **accepted syntax:** optional array of `{id, incompatible_family, components}`; each component is `$defs/identity_component` oneOf `fact_id_bound_key` or `member_field` (`source-family.v2.schema.json:97`; `$defs` identity_component).
- **source of authority:** ADR-0066 d4.
- **status:** pending-reconciliation

#### D-074 — `projects_from`

- **layer:** 5b-i, proper
- **accepted syntax:** optional `{id, version}` pin (`source-family.v2.schema.json:141`).
- **source of authority:** schema only; no accepted ADR decision was found that names this field.
- **status:** pending-reconciliation

#### D-075 — term `field`

- **layer:** 5b-i, proper
- **accepted syntax:** `{op: "field", field, default?}` ; `field` nonempty string; `default` `number|string|boolean|null` (`source-family.v2.schema.json:178`).
- **source of authority:** ADR-0066 d2 (`0066-…md:49-58`).
- **declared evaluation / blocking / invalidity / nonpublication:** an absent field is handled only by `field_absent` or an explicit term default; `field_not_equals` is false when the field is absent; no global closed-world negation (d2).
- **status:** pending-reconciliation

#### D-076 — term `literal`

- **layer:** 5b-i, proper
- **accepted syntax:** `{op: "literal", arg}` with `arg` `number|string|boolean|null` (`:203`).
- **source of authority:** ADR-0066 d2.
- **status:** pending-reconciliation

#### D-077 — term `add` / `subtract`

- **layer:** 5b-i, proper
- **accepted syntax:** binary `{op, left, right}` both `$ref #/$defs/term` (`:224, :244`).
- **source of authority:** ADR-0066 d2. **Not** the rule-artifact `add` (which takes `args` array / n-ary from v1).
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that a `source-family` term `add` is the same construct as rule-artifact `add` because they share a name.

#### D-078 — term `floor_zero`

- **layer:** 5b-i, proper
- **accepted syntax:** `{op: "floor_zero", value}` term (`:264`).
- **source of authority:** ADR-0066 d2. No counterpart in rule-artifact `$defs/expr`.
- **status:** pending-reconciliation

#### D-079 — predicate `field_present` / `field_absent`

- **layer:** 5b-i, proper
- **accepted syntax:** `{op: "field_present"|"field_absent", field}` (`:284, :301`).
- **source of authority:** ADR-0066 d2.
- **status:** pending-reconciliation

#### D-080 — predicate `field_equals` / `field_not_equals`

- **layer:** 5b-i, proper
- **accepted syntax:** `{op, field, arg}` (`:318, :344`).
- **source of authority:** ADR-0066 d2 (`field_not_equals` is false when the field is absent).
- **status:** pending-reconciliation

#### D-081 — predicate `compare`

- **layer:** 5b-i, proper
- **accepted syntax:** `{op: "compare", left, right, comparison}` with `comparison` enum `gt, ge, lt, le, eq, ne` (`:370-378`).
- **source of authority:** ADR-0066 d2.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that `ge`/`le` are the same tokens as rule-artifact `gte`/`lte`, or that this `compare` is numeric-only the way ADR-0025 binds rule-artifact `compare`.

#### D-082 — predicate `all` / `any`

- **layer:** 5b-i, proper
- **accepted syntax:** `{op, args}` with `args` minItems 1 of `$defs/predicate` (`:401, :421`). Recursive.
- **source of authority:** ADR-0066 d2. No `not`.
- **status:** pending-reconciliation

#### D-083 — predicate depth bound of six

- **layer:** 5b-ii, proper (Foreman ruling; Track 0 axes still show schema-typed citizen: No)
- **accepted syntax:** **none in JSON Schema.** `$defs/predicate` recursion is not `maxItems`-bounded. ADR-0066 d2: "Resolver admission rejects predicate depth greater than six; JSON Schema is not claimed to enforce recursive depth by itself" (`0066-…md:54-56`; "greater than six" at `:55`).
- **source of authority:** ADR-0066 d2 only, as a contract sentence. Track 0 records two Python literals plus this prose as untied (gap 8). This stream did not read those Python files for meaning.
- **separately versioned:** no schema generation carries the number 6.
- **declared evaluation / blocking / invalidity / nonpublication:** the ADR names resolver-admission rejection. It does not name the issue code. Track 0 names `MEMBER_CONSTRAINT_TOO_DEEP` from code; that token is **not** in this layer's schemas or in ADR-0066's decision text as an issue code (the ADR says "rejects predicate depth greater than six" without a code token).
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that a `source-family.v2` instance with depth 7 is JSON-Schema-invalid. The published schema would accept it.

---

### Surface 7 — provenance / disposition / explanation (grammar proper)

#### D-084 — derivation-record citizen

- **layer:** 7, proper
- **accepted syntax:** v2+ required `schema, record_id, run_id, phase, workspace_revision, governance_pins, adoption_pin`. `phase` enum `started, completed, interrupted, failed`. `stop_reason` enum `saturated, interrupted, validation-failed, execution-failed`. Optional `dispositions` array of `$defs/disposition`.
- **source of authority:** ADR-0008; ADR-0020 d1 (ledger as sole authoritative non-publication surface). v1 description at `derivation-record.v1.schema.json:5`.
- **separately versioned:** v1..v7. Track 0's named current is v7 via `packages/derivation/records.py:40`.
- **provenance that survives execution:** the record is outside the act log (ADR-0008 d1, v1 description). Closing record is structured data, no narrative.
- **status:** pending-reconciliation

#### D-085 — derivation-record block-code vocabulary

- **layer:** 7 / 2, proper
- **accepted syntax:** `$defs/disposition.properties.code` enum, drifting as in the table; v7 list at `derivation-record.v7.schema.json:124-135`.
- **source of authority:** ADR-0020 (base set); ADR-0036 PC1/PC3 (`SOURCE_SET_UNCLOSED`, `ITEMIZATION_TIE_OUT_VIOLATION`); ADR-0055 d2 (`COMPLETENESS_VALUE_VIOLATION`); later record descriptions name F1098 and SLI codes. ADR-0065 names `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`.
- **separately versioned:** each new code is a new derivation-record generation.
- **status:** pending-reconciliation

#### D-086 — npe-walk citizen

- **layer:** 7, proper
- **accepted syntax:** required `schema, id, run_id, workspace_revision, root`. `$defs/node` recursive via `children`. `rule_references` is an array (`npe-walk.v1` description: preserve all package producers).
- **source of authority:** ADR-0020 d2–d7. Walker is a pure projection; it never re-evaluates guards or rule ASTs (d2).
- **separately versioned:** v1..v3. No v4–v7 matching later record codes.
- **declared evaluation / blocking / invalidity / nonpublication:** sparse-ledger selection order (d4): published ledger row → run-scoped act-log publication → non-published ledger row → explicit `no_disposition_recorded`. Never infers a disposition.
- **provenance that survives execution:** payload carries `run_id` and workspace revision so consumers can detect staleness (d6). Cycle: `CYCLIC_DEPENDENCY_ERROR` (d5) — named in the ADR, not as an npe-walk `code` enum member.
- **status:** pending-reconciliation

#### D-087 — npe-walk `node_kind`

- **layer:** 7, proper
- **accepted syntax:** enum `published, blocked, guard_inapplicable, no_disposition_recorded` on v1–v3. Conditionals: `published` requires `finding_id`; `blocked` requires `code, unmet_references`; `guard_inapplicable` forbids those; `no_disposition_recorded` requires `closing_phase`.
- **source of authority:** ADR-0020 d4, d7.
- **declared evaluation / blocking / invalidity / nonpublication:** ADR-0020 d7's `invalid` refinement does not appear as a `node_kind`.
- **status:** pending-reconciliation

#### D-088 — npe-walk block-code vocabulary

- **layer:** 7 / 2, proper
- **accepted syntax:** v1 five codes including `SOURCE_SET_OPEN`; v2 rename + `ITEMIZATION_TIE_OUT_VIOLATION`; v3 + `COMPLETENESS_VALUE_VIOLATION`. Stops there.
- **source of authority:** same ADRs as D-085 through ADR-0055; later record-only codes have no npe-walk generation in this corpus.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that a v7 record code such as `SLI_MFS_INELIGIBLE` is a legal `npe-walk.v3` `code`. The v3 enum would reject it.

#### D-089 — derived-finding

- **layer:** 7, proper
- **accepted syntax:** v1 required `schema, id, symbol, value, version, pins`. v2 adds optional `resolved_input`. Pin roles in v2 include `default, composition, citation` in addition to v1's set; v2 pin `origin` enum `assertion, declared_default`.
- **source of authority:** ADR-0009 d1 (`0009-…md:69-80`); ADR-0025 d2–d3 for `resolved_input`.
- **separately versioned:** v1 / v2.
- **provenance that survives execution:** authority is the attribution chain, never a `basis` field (ADR-0009 d1). Kernel `finding.v1` is a different citizen (d3).
- **status:** pending-reconciliation

#### D-090 — `resolved_input` / declared default publication

- **layer:** 7 / 2, proper
- **accepted syntax:** optional on `derived-finding.v2`.
- **source of authority:** ADR-0025 d2 (`0025-…md:38-45`): default is published as a marked derived finding sharing the input's `fact_id`; `origin: declared_default` vs `assertion`; asserted input is never overwritten; absence without optional_default emits ordinary `DEPENDENCY_ABSENT`.
- **declared evaluation / blocking / invalidity / nonpublication:** as that decision. Displacement uses existing correction fold (d3) — no new root class.
- **status:** pending-reconciliation

#### D-091 — `act-derived-publication`

- **layer:** 7, proper (produced record of a publication act)
- **accepted syntax:** `act-derived-publication.v1` required `run_id, finding` (`packages/schemas/derivation/act-derived-publication.v1.schema.json`).
- **source of authority:** ADR-0007 d1–d4; ADR-0009 d2 (the act carries `derived-finding.v1`, not `finding.v1`).
- **declared evaluation / blocking / invalidity / nonpublication:** never an `assertion`. Attributed to the adopting actor through the adoption pin, not to the evaluator (ADR-0007 d2). Pin values originate in versioned inputs, never evaluator constants (d4).
- **status:** pending-reconciliation

---

### Neighboring Layer 2 citizens (Track 0 corpus; grammar-proper-adjacent to 1/4/5)

#### D-092 — source-closure-mapping

- **layer:** 4 / 5 (closure admission), proper as declared content a package admits
- **accepted syntax:** required `schema, id, version, family, member_fact_type, closure_fact_type, closure_horizon_key, admits_symbol, admission`. v1 `admission.condition` enum `current-literal-true`; v2 the same token as `const`. v2 fact-type fields are `$defs/pin`.
- **source of authority:** ADR-0014 d1–d2; ADR-0017 (horizon key); ADR-0028 d4 (v2 exact pins; bare fact-type identifiers structurally inexpressible).
- **separately versioned:** v1 / v2.
- **declared evaluation / blocking / invalidity / nonpublication:** closed admission vocabulary: exactly that one condition token.
- **status:** pending-reconciliation

#### D-093 — parameter-declaration

- **layer:** 1, proper (ADR-0006 d5)
- **accepted syntax:** required `schema, id, version, scope, values`. `values` is an unconstrained object (schema description: scalars, filing-status maps, and banded tables are all parameter values, distinguished by the consuming operation's semantics canon, not by this schema).
- **source of authority:** ADR-0006 d5; ADR-0024 d2.
- **separately versioned:** `parameter-declaration.v1` only in this corpus.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that `values` has a closed shape. The schema says it is deliberately open.

#### D-094 — checked-conclusion-binding

- **layer:** 4 / 2, proper as a schema-typed package-admitted citizen (artifact-package.v5+)
- **accepted syntax:** required `schema, id, version, title, scope, publishes, conclusion_fact_type, components, truth_table, direct_pin_boundary`. Components aliases const-required `C1..C4`. Truth table consts: `all_present_all_yes` → conclusion `no`, `direct_route: eligible`; `all_present_any_no` → conclusion `yes`, `direct_route: guard_inapplicable`; `any_missing` → conclusion `unpublished`, `disposition: blocked`, `code: DEPENDENCY_ABSENT`, `name_missing: every_missing_component`.
- **source of authority:** ADR-0050 Decision 1 (cited in the schema description). Description: "This citizen publishes the contract only; it does not execute the derivation."
- **separately versioned:** v1 only.
- **declared evaluation / blocking / invalidity / nonpublication:** the truth table **is** declared evaluation/blocking, in schema consts, while the description disclaims execution.
- **status:** pending-reconciliation

#### D-095 — dividend-universe

- **layer:** 4 (admitted content), not a Track 0 numbered surface of its own
- **accepted syntax:** required composable / recorded-non-composable box enums, drifting as in the table. Signal name remains in the descriptions as `CAPITAL_GAIN_DISTRIBUTION_RECORDED`.
- **source of authority:** ADR-0035 d3 (v1); ADR-0050 d2–d3 (v2).
- **separately versioned:** v1..v4.
- **status:** pending-reconciliation

#### D-096 — taxable-interest-composition

- **layer:** 4, proper as admitted content
- **accepted syntax:** required `schema, id, version, constituents, required_universe, publishes, coextensiveness`.
- **source of authority:** ADR-0026 (schema description: package validation performs exact slot/rule bijection).
- **separately versioned:** v1 only.
- **status:** pending-reconciliation

#### D-097 — citation

- **layer:** 4 / 5a (pin target), proper as admitted content
- **accepted syntax:** required `schema, id, version, authority`; `$defs/authority` is a discriminated closed family (parsed; not restated here in full).
- **source of authority:** ADR-0029 (schema description: resolution is structural/adoption-only and does not claim external legal verification).
- **separately versioned:** `citation.v1` only.
- **status:** pending-reconciliation

#### D-098 — role-canon

- **layer:** 4, proper as admitted content
- **accepted syntax:** required `schema, id, version, roles`.
- **source of authority:** ADR-0027 d2 (immutable versioned canon assigning one durable meaning to every member and pin role token).
- **separately versioned:** `role-canon.v1` only.
- **status:** pending-reconciliation

#### D-099 — quantity-vocabulary

- **layer:** Track 0 Layer 2 corpus; not a numbered term-boundary surface
- **accepted syntax:** required `schema, id, version, quantities`; `quantities` is a unique nonempty array whose items are a per-version closed enum (non-monotone; table above).
- **source of authority:** ADR-0028 decision 7 (cited in `quantity-vocabulary.v1.schema.json:5`).
- **separately versioned:** v1..v12. Track 0: no current designation.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that v12 contains every name earlier versions named (`covered-w-*` appears in v7 and is absent from v12).

---

### Surface 8 — kernel store (grammar-adjacent; domain only)

#### D-100 — fact-type

- **layer:** 8, adjacent (input domain a `ref`/`collect` reads; Track 0: do not skip)
- **accepted syntax:** v1 required `schema, id, title, nature, identity_keys, value_schema, supersession`; `nature` enum `determinable, elective`; `supersession.policy` const `free`. v2 adds `version`, optional `optional_default` (pin to a parameter-declaration), `quantity` / `source_amount`; supersession policy still const `free`. v3 (no `version` property) widens `supersession.policy` enum to `free, locked, closed-on-attestation` (ADR-0041).
- **source of authority:** ADR-0003 (no noun without a schema); ADR-0025 d1 (optional_default on determinable scalars only; elective cannot declare a default — intentional schema rejection); ADR-0041 (v3 policy vocabulary).
- **separately versioned:** v1..v3. `artifact-package` admitted_schemas from v2 onward name `fact-type.v2`, not v1 or v3.
- **declared evaluation / blocking / invalidity / nonpublication:** elective facts cannot declare `optional_default` (ADR-0025 d1).
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that rule-artifact `ref.name` is schema-constrained to a fact-type id.

#### D-101 — act / fact / entity / horizon substrate

- **layer:** 8, adjacent
- **accepted syntax:** published kernel citizens include `act.v1`, `act-assertion.v1..v2`, `act-entity-introduced.v1`, `act-entity-superseded.v1`, `act-member-transition.v1..v2`, `act-horizon-genesis.v1`, `act-package-adoption.v1`, `act-migration-adoption.v1`, `family-horizon.v1`, `finding.v1..v2`, plus contribution/bundle families. Enumerated by glob of `packages/schemas/kernel/*.schema.json`; not re-derived as grammar.
- **source of authority:** ADR-0002, ADR-0011, ADR-0017, ADR-0023, ADR-0033 (adoption acts). Track 0 moves `act-package-adoption.v1` here from surface 4.
- **separately versioned:** per kind.
- **declared evaluation / blocking / invalidity / nonpublication:** this layer is silent — these citizens are the store, not clause language.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** that adjacent means "no schema." Track 0's criterion keeps them adjacent because they are presupposed, not expressed.

#### D-102 — `optional_default` (fact-type.v2)

- **layer:** 8 / 2, adjacent citizen / proper contract
- **accepted syntax:** `{parameter: exact_pin}` on `fact-type.v2` only.
- **source of authority:** ADR-0025 d1–d4.
- **declared evaluation / blocking / invalidity / nonpublication:** see D-090.
- **status:** pending-reconciliation

---

### Cross-cutting declared publication / blocking contracts

#### D-103 — schema immutability / instance-named version

- **layer:** all schema-typed surfaces
- **accepted syntax:** every citizen `properties.schema` is a `const` equal to that file's generation (except the attachment-rule.v5 file, which consts v3).
- **source of authority:** ADR-0003 (`0003-…md:13`): published schema file is immutable; instances name their schema version; validation is strict with rejection — no tolerant readers, no repair.
- **separately versioned:** the rule *about* versioning, not a versioned construct.
- **status:** pending-reconciliation

#### D-104 — blocking discipline (dependency-absent vs invalid vs closure)

- **layer:** 2, proper
- **accepted syntax:** named codes on produced records (D-085, D-088, D-069), not on the rule-artifact field (D-007).
- **source of authority:** ADR-0006 d8; ADR-0025 d6 (`DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`); ADR-0036 rename to `SOURCE_SET_UNCLOSED`.
- **declared evaluation / blocking / invalidity / nonpublication:** open elective facts block with schema'd codes — no operative defaults; absent source is never silently an asserted zero (ADR-0006 d8).
- **status:** pending-reconciliation

#### D-105 — pin-value origin (no evaluator constants)

- **layer:** 7, proper
- **accepted syntax:** not a schema field; ADR-0007 d4.
- **source of authority:** ADR-0007 d4 (`0007-…md:16`).
- **declared evaluation / blocking / invalidity / nonpublication:** a pin whose value the evaluator invents is not lineage.
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** any claim about whether a given runtime constant violates this. That is Track 1b.

#### D-106 — unknown semantic schema versions fail loudly

- **layer:** 4, proper as ADR contract
- **accepted syntax:** not a JSON Schema enum. ADR-0066 d7: a package member whose declared schema validates in the registry but is not supported by the package resolver's semantic dispatch is rejected with an issue naming the member and schema; presentation projection rejects unknown form-field and attachment schema successors rather than filtering them into an incomplete model.
- **source of authority:** ADR-0066 d7 (`0066-…md:90-96`).
- **status:** pending-reconciliation
- **nearby inferences this evidence does not support:** what the runtime issue token is. The ADR does not name one in that paragraph.

#### D-107 — `no_disposition_recorded`

- **layer:** 7, proper
- **accepted syntax:** `npe-walk` `node_kind` const; requires `closing_phase` enum `started, interrupted, failed, completed`.
- **source of authority:** ADR-0020 d4 step 4: explicit rather than inferred (schema description of npe-walk.v1).
- **status:** pending-reconciliation

#### D-108 — two independent version axes on a content citizen

- **layer:** 4 (clearest on packages), proper as a declared fact about the language's identity
- **accepted syntax:** every content citizen parsed has both `schema` (schema-generation const) and `version` (instance `^v[0-9]+$`), except `fact-type.v1` / `fact-type.v3` which have no `version` property.
- **source of authority:** Track 0 Layer 2 two-axes note, confirmed by parsing `artifact-package` vs instance files' fields in schemas: the schema family counts to v25; the instance `version` pattern is independent. This stream did not parse `packages/content/` (Track 1c).
- **status:** pending-reconciliation

## Constructs the schema admits whose meaning no accepted ADR fixes

Recorded as silences, not as "undeclared":

1. Expression ops `count` (D-016) and `block` (D-017) — schema from rule-artifact.v4; no ADR decision names them.
2. Rule-artifact `notes` (D-009).
3. `source-family.v2` `projects_from` (D-074).
4. `adjustment_row.kind` tokens (D-064) — closed by schema, not found as an ADR language decision.
5. Predicate/term evaluation of `add`/`subtract`/`compare`/`all`/`any` beyond ADR-0066's closed-list and absent-field sentences — no operation-semantics citizen exists for that nested language.
6. `parameter-declaration.values` open shape (D-093) — deliberately; the distinguishing canon is supposed to be operation-semantics, which has no entry for most ops (`add`, `ref`, `choose`, …).
7. What `ref.name` / `collect.name` denote.
8. Division by zero, `choose` branch skipping, `all`/`any` short-circuit as schema rules (ADR-0024 d4 states short-circuit in evaluator terms).

## Open questions only another layer can answer

1. Which rule-artifact generations the running validators actually accept, given that every `artifact-package.v2..v25` `admitted_schemas` enum omits `rule-artifact.v1` and `operation-semantics.v1` while Track 0 records runtime literals that include rule-artifact v1–v6.
2. Whether `accounts_for` on rule-artifact.v5 is interpreted for v6 content via attachment-rule.v8, package validation, or not at all.
3. What `count` and expression-op `block` do at evaluation time, and which ledger code a `block` op emits.
4. Whether predicate depth > 6 is rejected at admission, at evaluation, both, or neither, and whether the two Python literals Track 0 names can diverge.
5. How `npe-walk.v3` projects a derivation-record.v7 row whose `code` is not in the walk enum.
6. How an instance with `"schema": "attachment-rule.v3"` is validated when two published files claim that `$id`.
7. Whether `collect.source_set` omitted on a v1 rule is accepted by runtime (schema allows it; v2+ does not).
8. Whether `round` without `stage` on v2+ exprs still applies operation-semantics.v1 `spec.stages`.
9. What `ref` / `collect` bind to in the store (surface 8), which this layer cannot see.
10. Whether `divide.rounding` shares runtime dispatch with `round` modes.

## Track 0 or plan problems this reading surfaced

1. **Plan Track 1a paragraph vs Track 0 corpus / charter** — recorded above; not resolved by shrinking the reading.
2. **Track 0 Layer 2 did not flag `attachment-rule.v5.schema.json`'s `$id`/`const` of v3.** The no-v7 gap is correctly recorded; this identity collision is additional and load-bearing for anyone who keys citizens by `$id` or by instance `schema`.
3. **Track 0 Layer 2 did not flag non-monotone `quantity-vocabulary` enums** (v7/v8/v9 drops) or the artifact-package.v10 drop of `quantity-vocabulary.v5`.
4. **Track 0 Layer 2 did not flag that `operation-semantics.v2` is not a superset of v1**, or that no `artifact-package` admitted_schemas enum lists `operation-semantics.v1` / `rule-artifact.v1`.
5. **Track 0 gap 4 (discoverability of term/predicate in source-family.v2) is confirmed.** The vocabulary is there, at the cited lines. This stream found it by reading `source-family.v2` because Track 0 said to, not because the citizen's name suggests an expression language.
6. **ADR-0020 d7 vs npe-walk `node_kind`:** the ADR's `invalid` refinement is not a schema token. Track 0's surface-2 blocking-code list mixed evaluator aliases (`BLOCK_ABSENT` / `DEPENDENCY_ABSENT`) from `packages/derivation/evaluator.py:22-27` with schema tokens. This stream did not treat those evaluator names as declared.
7. **`rule-artifact.v5` `accounts_for` disappearing in v6** is version drift the charter asked this stream to catch. Track 0 did not mention it.
8. **Surface 8 remains necessary** to answer input/output domains; the plan's seven-surface list still does not name it (Track 0 already said this).
9. **`checked-conclusion-binding.v1`, `dividend-universe`, `taxable-interest-composition`, `citation`, `role-canon`** sit in Track 0 Layer 2 and in `admitted_schemas` but are not numbered in `#Term boundary`. This stream recorded them rather than dropping them.

No Track 0 file-count cited above failed to reproduce when re-run (7 attachment-rule files, no v7; 6 rule-artifact files; 2 operation-semantics files; 25 artifact-package files; 7 derivation-record files; 3 npe-walk files; 3 form-field files; 2 source-family files; 12 quantity-vocabulary files; 66 ADR markdown files excluding INDEX).

## Verification notes

Commands used: Python `json.load` walks for enums/consts/`$defs`; line scans for citations; SHA-256 of the two attachment-rule files that share `$id`; `packages/schemas/tax/published.json` keys; `ls` of schema directories; `docs/adr/INDEX.md` status table tally (53 accepted).

Track 0 citations checked and found **correct**:

- `source-family.v2.schema.json` `member_constraints` at 66, `identity_exclusivity` at 97, `$defs` at 171, `term` at 172, `predicate` at 278
- `packages/derivation/records.py:40` `CURRENT_RECORD_SCHEMA = "derivation-record.v7"`
- attachment-rule published set is v1–v6 and v8, no v7
- ADR INDEX 66 rows, 53 accepted

Track 0 citations **not reused as this stream's authority** even where they point at real lines: evaluator.py blocking aliases and `MAX_PREDICATE_DEPTH` Python sites — those are implementation. ADR-0066 d2 is the declared depth bound.

No sibling deliverable was opened. At the start of this stream `docs/phases/grammar-census/inquiries/` listed no `track-1b-*` or `track-1c-*` file.
