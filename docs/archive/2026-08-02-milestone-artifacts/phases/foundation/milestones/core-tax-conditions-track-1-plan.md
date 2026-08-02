# Track 1 Development Plan — Contract Schemas and Payload Instances

Foreman work order, 2026-07-15. Parent: `core-tax-conditions-and-presentation-integration.md` (Track 1). Track 0 complete (ADRs 0020, 0024–0029 accepted); this track publishes the production schema surface those decisions require, so Tracks 2–5 have contracts to build content and engine against.

## Scope fence (read first)

Track 1 lands **schema definitions + payload instances (positive & negative) + schema-validation tests + registry manifests (`published.json`)** only. It does **not** implement runtime behavior.

Explicitly **out of Track 1** (do not build here):
- **Validator dispatch / cross-kind joins** — typed closed graph, entrypoint reachability, force-declare, `require_closed` execution, slot bijection, exclusive projection, package↔adoption inclusion → **Track 4**.
- **Content** — B3/OID/`unreported` interest families, standard-deduction & bracket parameter tables, line rules, form-field *instances*, composition instances → **Tracks 2/3**.
- **Runner/walker code** — ledger writing, `npe-walk` traversal, citation resolver logic → **Track 5**.
- Presentation/display formatting of citations → deferred rendering contract (ADR-0029 d6).

A schema may *encode* a constraint (e.g. `optional_default` forbidden on elective fact types; `quantity` required and non-empty) as JSON-Schema structure. Behavior that a JSON schema cannot express (graph reachability, force-declare) is Track 4 — reference it in the schema's `description`, don't fake it.

## Deliverables — new/changed schemas, in dependency order

Build in layers; each layer's citizens are referenced by the next.

### Layer A — vocabularies/canon (no deps)
| # | Schema | New/Δ | Source | Key content |
|---|---|---|---|---|
| A1 | `quantity-vocabulary.v1` | new (kernel) | 0028 d7 | Closed versioned enum of tax-quantity ids (`taxable-interest`, `wages`, …). Immutable; monotony like the role canon. |
| A2 | `role-canon.v1` | new | 0027 d2 | Versioned immutable canon: each member/pin role token → one meaning across generations. Enumerates the expanded role set (below). |

### Layer B — kernel fact surface (v2)
| # | Schema | New/Δ | Source | Key content |
|---|---|---|---|---|
| B1 | `fact-type.v2` | new gen | 0028 d1 · 0025 d1 · 0028 d7 | Add `version` `^v[0-9]+$`. Add `optional_default:{parameter:{id,version}}` — **schema-reject when `nature` is elective** (E3.1). Add `quantity:{id,version}` **required for source-amount fact types**, resolving to A1; missing/empty **rejects** (no fail-open). v1 stays valid historical, not a v2 pin target. |
| B2 | `bundle.v2` | new gen | 0028 d1–2 | Add `version`. Nested fact identities carry exact `(id, version)`. |
| B3 | `act-bundle-adoption.v2` | new gen | 0028 d3 | Wholesale body embeds `bundle.v2` with versioned nested identities (basis for Track-4 nested-set equality). |

### Layer C — derivation citizens (v2)
| # | Schema | New/Δ | Source | Key content |
|---|---|---|---|---|
| C1 | shared **pin vocabulary** (in `derived-finding.v2` + `rule-artifact.v2`) | Δ | 0025 d3 · 0026/0027 · 0029 d3 | Add roles `default` and `composition` (**provenance-only, non-edge** — only `input`/`choice` are edges). Add required `origin:"assertion"\|"declared_default"` on `input` pins. Add `citation` pin. Keep role tokens aligned to A2. |
| C2 | `derived-finding.v2` | new gen | 0025 d2 | Add closed `resolved_input` branch `{fact_id, origin:"declared_default"}` for default-resolution findings. |
| C3 | `operation-semantics.v2` | new gen | 0025 d5 · 0026 d5 | New op citizens: `categorical_compare` (operators eq/ne, exact enum-token, domain-mismatch=block); `require_closed` (source_set; reuses ADR-0014 dispatch — semantics only). |
| C4 | `rule-artifact.v2` | new gen | 0025 d5 · 0029 d3 | Closed expression forms `categorical_compare` + `category_literal{fact_type,value}`. Optional `composition:{id,version}` pin. Optional array of unique `citation` pins (metadata; must not alter when/value/publishes). |
| C5 | `source-closure-mapping.v2` | new gen | 0028 d4 | `member_fact_type` / `closure_fact_type` become exact `{id,version}` pins (not bare id strings). |
| C6 | `derivation-record` single-surface fold (`.v2`) | new gen | 0020 d1/d1a/d7 | One authoritative `dispositions[]` ledger; ledger enum `published\|blocked\|inapplicable`; row carries block code, unmet refs, and **either** `guard_result` (false guard) **or** `superseded_by` (conflict-loser). Legacy top-level `blocked[]` becomes a **derived read-model**. **Repair the self-contradictory `derivation-record.completed.json` fixture concurrently (NPE-G10).** |
| C7 | `npe-walk.v1` | new | 0020 d2–4 | Walk payload: node carries `rule_references[]` (array); run-scoped fields; `no_disposition_recorded` node; `run_id` + `workspace_revision` currency. Payload dispositions use ADR-0012 vocab (`guard_inapplicable`), mapped from ledger `inapplicable`. |

### Layer D — package, presentation, new citizens
| # | Schema | New/Δ | Source | Key content |
|---|---|---|---|---|
| D1 | `artifact-package.v2` | new gen | 0025 d4 · 0027 d2/3/4/8 · 0028 d5 | `input_bindings[]` (`mode:"required"\|"optional_default"`); `admitted_schemas[]`; member `role` enum += `form-field, source-family, source-closure-mapping, composition, fact-type-bundle, citation` (per A2); `entrypoints`; `composition_obligations[]` (published symbols); package-instance checksum field. |
| D2 | `form-field.v2` | new gen | 0029 d3 · 0025 PC2 | At most **one** `citation` pin `{id,version}`. Disposition enum += `CATEGORICAL_DOMAIN_MISMATCH`; confirm `DEPENDENCY_INVALID` covers enum-invalid (ADR-0012 vocabulary amendment — E1). |
| D3 | `taxable-interest-composition.v1` | new | 0026 d1–2 | Composition citizen: closed `constituents[]` each pinning a source-family declaration + its `authorizes_subtotal`; `required_universe.claim`; `publishes`; coextensiveness declaration. (Instances are Track 2.) |
| D4 | `citation.v1` | new | 0029 d1/d4 | Citation citizen: `id`, `version`, **discriminated** authority-family/locator (`us-code`, `irs-form`, `irs-instructions`, `irs-publication`); reject cross-family locators / soft property bags. |

### Layer E — vocabulary amendment (cross-cutting)
- **E1 (ADR-0012 disposition vocabulary):** add `CATEGORICAL_DOMAIN_MISMATCH`; confirm `DEPENDENCY_INVALID`. Applies wherever dispositions are enumerated (form-field disposition enum; ledger/walk payload vocab). Fold into D2/C6/C7 rather than a standalone file.

## Payloads, tests, registry (per schema — definition of done)

For **each** schema above:
1. **Positive instance(s)** under `packages/schemas/**/examples/` (or the repo's existing example convention) — a minimal valid citizen.
2. **Isolated negative(s)** — at minimum the schema's named reject. High-value negatives to include:
   - `fact-type.v2`: `optional_default` on an elective fact → reject; source-amount fact missing `quantity` → reject.
   - `artifact-package.v2`: unadmitted schema generation; `composition_obligations` symbol with no composition member/pin; `input_binding` to an absent fact type.
   - `derived-finding.v2`: `input` pin missing `origin` → reject.
   - `source-closure-mapping.v2`: bare-id fact field → reject.
   - `citation.v1`: cross-family locator → reject.
   - `form-field.v2`: two citation pins → reject.
3. **Schema-validation test** (positive validates, each negative fails) in `tests/…` following the existing schema-test pattern.
4. **Registry entry** in the directory `published.json` with sha256; **immutability test** (republish under same `(id,version)` with changed bytes → reject). New generations are new registry rows; v1 rows are untouched.

## Verification (Track 1 exit)
- `python3 -m unittest` (project `.venv`; system python lacks jsonschema) green.
- `python3 tools/governance_lint.py` green.
- Every new/changed schema has ≥1 positive and its named negative(s); registry immutability holds.
- No validator-dispatch or content logic introduced (scope fence).
- One Track 1 commit (per the milestone's atomic-per-track rule), or a small number of layer-ordered commits if the diff is large — foreman custody.

## Build order & handoff
A → B → C → D → E. A1/A2 first (everything references quantity + role canon); B before C4/C5 (fact identities); C1 pin vocabulary before C2/C4; D1 last in the schema set (it references the widest surface). E folds into D2/C6/C7.

Open question for the owner before a builder is launched: **who executes Track 1** — an owner-launched implementation seat (this is repo code, not a decision round, so the rival discipline does not apply), or the foreman directly under owner go. The plan is builder-agnostic; it needs a driver.
