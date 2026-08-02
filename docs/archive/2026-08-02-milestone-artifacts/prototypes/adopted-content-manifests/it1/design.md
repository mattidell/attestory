# Incumbent design — adopted-content membership surface, iteration 1

Date: 2026-07-14. Builder: High-tier incumbent (owner-launched). Charter:
`charter-it1.md`. Evidence: Rung 2 (paper schema/canon diffs + static probes
against committed `artifact-package.v1` / `package_validation.py` / tax content
at HEAD). No repository schema, package, or validator edits. All ids, amounts,
and paths synthetic except committed reference shapes named as such.

## Boundary

- **Propositions:** ACM-P1 (membership surface; extend vs succeed ADR-0006) and
  ACM-P2 (cross-kind binding integrity + schema-generation coexistence).
- **Prior art:** inert spike + proposed ADR-0022 are **superseded, not
  inherited**. Their path-based `manifest.json` and file-existence “closure”
  are rejected (they fork ADR-0006’s pin-versioned package and omit form-fields,
  source-authority, ELX bindings, and composition).
- **Not this design:** UI packaging, multi-package dependency graphs, citation
  resolver membership (Track 0.c), runner tax arithmetic, schema *publication*
  checksums (ADR-0003 `published.json` stays), directory layout under
  `packages/content/`.

### Committed gaps (static probes at HEAD)

| Probe | Observation |
| --- | --- |
| P1 | `artifact-package.v1` member `role` enum admits rules/parameters/lineage pins only — **not** `form-field`, `source-family`, `source-closure-mapping`, `composition`, `fact-type`. No `input_bindings`, no admitted-schema list. |
| P2 | `package_validation.py` checks schema, pin resolution, role agreement (rules/parameters), scope, parameter/table expression refs, output ownership — **not** `binds_symbol`, source-family/`source_set`, mapping↔family, composition, or ELX bindings. |
| P3 | Committed `package.first-tax-slice` @v1 pins only the line-1a rule; co-located `form1040.line-1a.form-field` (binds the rule’s `publishes`) is **outside** membership. Validator cannot reject a dangling form-field. |
| P4 | Committed `package.interest-slice` @v1 pins only the B1 subtotal rule; co-located family + mapping are **outside** membership. |
| P5 | `loader.ROLE_VOCABULARY` lacks `form-field`, `source-family`, `source-closure-mapping`, `composition` (required by ADR-0026 for pins), and `default` (ADR-0025). |

These are the real gaps this design closes — not a blank slate.

---

## ACM-P1 — membership surface: **extend** ADR-0006

### Claim

A **closed content unit** is an `artifact-package` under ADR-0006 decisions 6–7
and 9: exact member versions (`id`+`version` pins), bidirectional reference
closure, scope-as-content, unique output ownership, and **one shared role
vocabulary** across artifact / package member / finding pin. This design
**extends** that unit via a versioned successor schema
(`artifact-package.v2`), it does **not** invent a second membership authority
(path inventory, parallel manifest citizen, or filesystem graph).

**Extend, not succeed-as-replacement.** Succession would only be justified if
the package *stopped* being the closed pin manifest. The production substrate
already is that manifest for rules and parameters. Post-0006 citizen kinds
(form-fields, source-family/mapping, fact types, composition, ELX package
bindings) must enter **the same pin table**, with the same immutability and
contained-validation discipline (decision 3; Article 9 / ADR-0003).

`artifact-package.v1` remains valid **historical** content (ADR-0025 posture).
New units that close over post-0006 kinds declare `schema: "artifact-package.v2"`.

### Member kinds (pin surface)

Every member is a pin `{role, id, version}`. The role token is drawn from the
**single** shared vocabulary (decision 9). New tokens added once; never given a
second meaning across schema generations.

| Role token | Citizen schema (admissible generations) | Pin meaning (one token, one meaning) |
| --- | --- | --- |
| `computation` / `applicability` / `field-mapping` / `cross-form-bridge` | `rule-artifact.v1` (+ `.v2` when admitted) | Rule member; role must equal the artifact’s own `role` |
| `parameter` | `parameter-declaration.v1` | Parameter / table citizen |
| `operation-semantics` | `operation-semantics.v1` (+ `.v2` for ELX ops) | Versioned op canon the unit relies on beyond global engine canon |
| `form-field` | `form-field.v1` | Presentation citizen (ADR-0012); **not** a derivation edge |
| `source-family` | `source-family.v1` | Family claim/predicate authority (ADR-0016) |
| `source-closure-mapping` | `source-closure-mapping.v1` | Closure→calculation mapping (ADR-0014) |
| `composition` | `taxable-interest-composition.v1` (and later composition schemas) | Composition citizen (ADR-0026). Same token as the **provenance-only** finding/rule pin role: names a composition; **never** an `input`/`choice` edge (ADR-0010) |
| `fact-type` | `fact-type.v1` (+ `.v2` for `optional_default`) | Fact-type surface the unit’s rules/bindings close over (bundles may be authoring convenience; **pins version-lock individual fact types**) |

Kernel **bundle adoption** remains how fact-type vocabulary enters a workspace
(act-bundle-adoption). Package membership **pins which versions this unit
closes over** for validation — it does not re-implement kernel adoption.

### Package-level fields on `artifact-package.v2`

Retained from v1: `id`, `version` (`^v[0-9]+$`), `scope`, `members`,
`conflict_semantics`.

**Added:**

1. **`admitted_schemas`** (array of schema ids, minItems 1) — the schema
   generations this unit may load. Example for a wages unit that is still
   v1-only on rules:

   ```json
   "admitted_schemas": [
     "rule-artifact.v1",
     "form-field.v1",
     "fact-type.v1",
     "parameter-declaration.v1",
     "operation-semantics.v1"
   ]
   ```

2. **`input_bindings`** (ADR-0025) — zero or more
   `{symbol, fact_type, mode}` with `mode ∈ {"required","optional_default"}`.

Rules that publish a composition-gated symbol (ADR-0026 line-2b pattern) carry a
required **`composition: {id, version}`** field on `rule-artifact.v2` (paper
diff owned by Track 1 under ADR-0026; this design only requires package
validation to enforce the pin non-vacuously against a package member).

### Bidirectional closure (membership graph)

Let `M` be the set of pinned `(id, version)` keys. Let `corpus[m]` be the
citizen. Validation walks **all** members and records **contained**
`MemberIssue`s (never aborts the walk — ADR-0006 decision 3).

**Outbound (every reference lands on a pin):**

| Edge | Must resolve to |
| --- | --- |
| Rule expression `parameter` / `table_id` | `parameter` member in `M` (existing) |
| Rule `collect.source_set` / family name | `source-family` member whose `id` equals the set (version from co-pinned family used by mapping) |
| Rule `composition` pin | `composition` member exact `(id,version)` |
| Mapping `family` pin | `source-family` member exact match |
| Form-field `binds_symbol` | Symbol in package `output_owners` (or `conflict_semantics`) |
| `input_bindings[].fact_type` | `fact-type` member |
| `optional_default` parameter (on fact-type.v2) | `parameter` member |
| Composition slot `family` + subtotal | Pinned family + a rule member that `publishes` that family’s `authorizes_subtotal` |

**Inbound / integrity (no vacuous claim):**

- Unique output ownership (existing decision 7).
- Mapping `admits_symbol` = pinned family’s `authorizes_subtotal` (existing
  `source_authority.validate_mapping_against_family`, now **gated at package
  load** when both are members).
- Composition slot set is a **bijection** with the publishing rule’s
  constituents (ADR-0026 decisions 2/4) — not mere file presence.
- A rule that declares `composition` must resolve; a rule publishing a symbol
  that a composition citizen `publishes` **must** carry that pin (mandatory
  licensed binding — defeats vacuous no-op).

**Not standing-affecting:** membership pins and the `composition` role create
**no** new derivation edges. Displacement remains `input`/`choice` only
(ADR-0010).

### Scope and immutability

- Member scope must match package scope (existing). Form-fields carry form-year
  / jurisdiction on `form`; validator requires
  `form.tax_year` / `form.jurisdiction` agree with package scope where those
  fields exist (presentation citizens without full `scope` object).
- Package `(id, version)` content is immutable once published (Article 9). A
  new member set is a **new package version**, never an in-place edit of `vN`.

---

## ACM-P2 — binding integrity and schema-generation coexistence

### Binding rejects at load (contained issues)

| Defect | Issue code (proposed; exact strings triage-deferred) |
| --- | --- |
| Form-field `binds_symbol` not published by any member / conflict rule | `FORM_FIELD_DANGLING_BINDING` |
| Line rule lacks required `composition` pin, or pin absent from `M` | `COMPOSITION_BINDING_MISSING` |
| Composition pin resolves but `publishes` ≠ rule’s `publishes` | `COMPOSITION_PUBLISHES_MISMATCH` |
| Composition slots ↛ bijection with rule constituents / family predicates | `COMPOSITION_SLOT_BIJECTION` |
| Mapping/family/subtotal peer referenced but not pinned at version | `CLOSURE_MISSING_PEER` |
| `input_bindings` fact type or default parameter absent from `M` | `ELX_BINDING_ABSENT` |
| Elective fact type carries `optional_default` | `ELX_ELECTIVE_DEFAULT` (schema-level reject preferred) |
| Member’s `schema` ∉ package `admitted_schemas` | `MEMBER_SCHEMA_UNADMITTED` |
| Pin `role` ∉ shared vocabulary, or role token reused with new meaning | `PIN_ROLE_UNKNOWN` / schema reject |
| Existing codes retained | `PACKAGE_SCHEMA_INVALID`, `MEMBER_ABSENT`, `MEMBER_SCHEMA_INVALID`, `ROLE_MISMATCH`, `SCOPE_MISMATCH`, `CLOSURE_MISSING_PARAMETER`, `OUTPUT_OWNERSHIP_CONFLICT` |

All are **per-member (or per-package) recorded issues**. An ELX hole on one
binding does not abort validation of unrelated members (decision 3).

### Schema-generation coexistence

1. Package lists every schema generation it closes over in `admitted_schemas`.
2. Historical `*.v1` content remains loadable when listed; `*.v2` (ELX rule /
   fact-type / package / finding shapes; composition citizen; `composition`
   role) loads only when listed.
3. **No silent partial load:** a member whose schema is unadmitted is
   `MEMBER_SCHEMA_UNADMITTED`, not skipped.
4. **No dual-meaning pin roles:** vocabulary extension is additive. The token
   `composition` means “names a composition citizen / provenance pin” at every
   generation that admits it. A generation that needs a different concept uses
   a **new** token (or a governed migration), never overloads `input` /
   `parameter` / `composition`.

### Claim → contract change → validator behavior

| Claim | Paper schema/canon change | Validator |
| --- | --- | --- |
| Unit is extended package | `artifact-package.v2` (+ `admitted_schemas`, `input_bindings`; extended role enum) | Validate package against v1 or v2 by declared `schema` |
| Shared vocabulary grows | `loader.ROLE_VOCABULARY` + all role enums gain new tokens as subsets | `role_vocabulary_report` still proves subset |
| Form-field / family / mapping / composition / fact-type members | Role→schema dispatch table in validator | Resolve pin; `validate_declared`; kind-specific edges |
| Binding integrity | No new standing edge; pure load checks | Codes above; `ok = not issues` |
| Composition mandatory | `rule-artifact.v2` `composition` pin field (Track 1 / ADR-0026) | Non-vacuous resolve + bijection |
| ELX package bindings | As ADR-0025; enforced here at membership | `input_bindings` + fact-type.v2 cross-check |

---

## Gate-2 cases (synthetic)

### Case 1 — Positive: minimal closed wages unit

**Unit** `U-wages@v1` (`artifact-package.v2`):

| Pin role | id @ version |
| --- | --- |
| `field-mapping` | `tax.us.2025.rule.w2-box1-to-line1a@v1` (shape: committed rule) |
| `form-field` | `tax.us.2025.form1040.line-1a@v1` (`binds_symbol` = rule `publishes`) |
| `fact-type` | `tax.us.2025.w2.box1-wages@v1`, `tax.us.2025.w2.source-closure@v1` |
| `parameter` | `rounding.convention@v1` (rule `requires` / expression refs) |

`admitted_schemas`: `rule-artifact.v1`, `form-field.v1`, `fact-type.v1`,
`parameter-declaration.v1`.

**Trace (producer → authority → consumer → failure map):**

- **Producers:** content authors of rule, form-field, fact types, parameter.
- **Authority:** package validator + published schemas (ADR-0006 decision 3);
  adoption act pins `U-wages@v1` for any run.
- **Consumers:** saturation runner (rules/parameters); renderer (form-field
  dispositions only — never invents values).
- **Failure map:** missing parameter → `CLOSURE_MISSING_PARAMETER`; bad
  form-field bind → `FORM_FIELD_DANGLING_BINDING`; unadmitted schema →
  `MEMBER_SCHEMA_UNADMITTED`; one bad member leaves others checked.

**Outcome:** validates (`ok: true`); `output_owners` includes
`tax.us.2025.wages.total-w2-box1`.

### Case 2 — Positive: composition-bearing line-2b unit

**Unit** `U-2b@v1` pins (paper shapes; OID-inclusive per ADR-0026):

- Composition citizen `C-2b@v1` (`taxable-interest-composition.v1`) publishing
  `tax.us.2025.form1040.line2b.taxable-interest` with slots
  `{int_box1, int_box3, taxable_oid, unreported_taxable_interest}`.
- Four `source-family` + four `source-closure-mapping` + four subtotal
  `computation` rules + line-2b `computation` rule with mandatory
  `composition: {id: C-2b, version: v1}` + line-2b `form-field`.
- Fact types and parameters each slot needs; `admitted_schemas` includes
  composition + rule-artifact.v2 (composition pin field).

**`composition` in shared vocabulary:** added once as package-member role and
as provenance pin role on findings/rules. Runner records the pin; currency
extracts edges only from `input`/`choice` (ADR-0010) — composition never
displaces.

**Outcome:** validates when slot bijection holds and every family/mapping/
subtotal/form-field edge closes.

### Case 3 — Negative: dangling form-field (mandatory)

Package pins form-field F with `binds_symbol: "tax.us.2025.missing.symbol"` and
no rule publishes it / no `conflict_semantics` entry.

**Outcome:** `FORM_FIELD_DANGLING_BINDING` on F; `ok: false`. Other members
still receive their checks.

### Case 4 — Negative: unlicensed / incomplete composition (mandatory)

Three sub-cases (any one sufficient; all paper-cheap):

| Sub | Defect | Code |
| --- | --- | --- |
| 4a | Line-2b rule ships **without** `composition` pin | `COMPOSITION_BINDING_MISSING` |
| 4b | Pin present but no composition member / wrong version | `COMPOSITION_BINDING_MISSING` or `MEMBER_ABSENT` |
| 4c | Composition present; slot set omits OID (not a bijection) | `COMPOSITION_SLOT_BIJECTION` |

Defeats “file exists” vacuity: a co-located composition document that is not
pinned, or is pinned without bijection, does not license publication.

### Case 5 — Negative: ELX binding hole

Package declares
`input_bindings: [{symbol: "taxpayer_age65", fact_type: "tax.us.2025.taxpayer-age65", mode: "optional_default"}]`
but either (a) fact-type not in `M`, or (b) fact-type.v2 `optional_default`
parameter not in `M`, or (c) fact-type is `nature: "elective"`.

**Outcome:** (a)(b) `ELX_BINDING_ABSENT`; (c) `ELX_ELECTIVE_DEFAULT` /
schema reject. Issue is **contained** — unrelated wage members still validated.

### Case 6 — Negative: partial / version-skew load

Strongest single negative this surface owns:

- Package `admitted_schemas` lists only `rule-artifact.v1`.
- A member declares `schema: "rule-artifact.v2"` (e.g. carries `composition`
  pin field / categorical ops).

**Outcome:** `MEMBER_SCHEMA_UNADMITTED`. (Also covered: rule refs a
source-family id not in `M` → `CLOSURE_MISSING_PEER`; two generations must not
redefine `composition` — prevented by vocabulary monotony + schema review.)

### Case 7 — Lifecycle (mandatory)

| Step | Package | Members (abbrev.) | Result |
| --- | --- | --- | --- |
| 1 | `U@v1` | wages rule + form-field line-1a + fact types + parameter | validates; adoptable |
| 2 | Publish **new** `U@v2` | `U@v1` members **plus** form-field line-2b + composition stack | validates as successor unit |
| 3 | Historical | `U@v1` content bytes unchanged | remains closed historical; still validates against the same corpus of its pins |
| 4 | Illegal partial upgrade | Document claiming `id=U, version=v1` but member set of step 2 | **reject**: published `(id,version)` immutability (Article 9 / ADR-0003). Store/registry: content hash / prior publish mismatch — not an in-place edit. If presented only to validator without registry, treat as a **different** unpublished instance; adoption of two divergent bodies under one version is forbidden at the adoption boundary |
| 5 | Re-adoption | Adoption act pins `U@v2` | validates; runs use v2 membership |

**Named versions / pins / codes in the illegal step:** package
`tax.example.unit.U` versions `v1`→`v2`; members e.g.
`rule.wages@v1`, `form.line-1a@v1`, then add `form.line-2b@v1`,
`composition.2b@v1`, families/mappings/subtotals `@v1`. Illegal partial:
`PACKAGE_SCHEMA_INVALID` or adoption-time `PACKAGE_VERSION_CONFLICT` (production
condition: registry enforces hash of published package citizen). No silent
in-place edit.

---

## Producer → authority → consumer (unit-level)

| Role | Actor |
| --- | --- |
| Producer | Content authors of every pinned citizen + the package document |
| Authority | Published schemas + package validator (contained issues) + adoption act |
| Consumer | Runner (derivation members only); renderer (form-fields); coverage (families/composition claims) |
| Failure | Recorded issues / blocked runs — never tolerant repair (E9.1) |

---

## Explicit unresolved authority

1. **Exact issue-code strings and registry hash mechanics** for package
   immutability are production/Track-4 details (Gate 5 defers exact strings).
2. Whether **unused** pin members (unreferenced parameters) are rejected by
   reverse-reachability is not required for the floor; this design only
   mandates outbound reference + binding integrity.
3. **Multi-package** composition (unit A depends on unit B) is out of scope.
4. Citation-resolver membership for `citation_ref` remains Track 0.c.
5. Runtime environment here could not import `jsonschema` (host venv path);
   probes are static contract reads of committed JSON/Python at HEAD — enough
   to show membership gaps; full throwaway `validate_package` execution is a
   production-condition re-run, not a paper blocker.

## Floor check (Gate 6)

- No second authority alongside ADR-0006 → **extend via v2**.
- Closes over form-fields **and** source-family/mapping **and** composition.
- Rejects case 3 and cases 4–5; lifecycle case 7 named.
- ACM-P2 settled at static level with the binding table and
  `admitted_schemas` monotony rule.
