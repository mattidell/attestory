# Incumbent design — ACM micro-round residuals (MR-P1, MR-P2), it1

Date: 2026-07-15. Builder: Medium-tier incumbent (owner-launched). Charter:
`../charter-it1.md`. Evidence: **Rung 2** — paper schema/canon diffs + static
probes against committed HEAD (`fact-type.v1`, `bundle.v1`,
`act-bundle-adoption.v1`, `source-closure-mapping.v1`, `artifact-package.v1`,
`package_validation.py`, `w2.bundle.json`). Throwaway probes under
`/tmp/acm-micro-round-probes/` (outside the repository). No repository
modifications beyond the two micro-round outputs. Synthetic ids only.

## Boundary

- **Propositions:** **MR-P1** (fact-surface versioning ⋂ wholesale-adoption
  reconciliation) and **MR-P2** (declared composition-obligation trigger).
- **Floor held fixed (ADR-0027):** extend-not-fork `artifact-package.v2`; typed
  closed graph; role canon + load-time role-semantic divergence;
  `admitted_schemas` (no package-embedded schema sha256); package-instance
  immutability; exclusive execution projection; form-field producer integrity;
  `composition` pin provenance-only (ADR-0026 decision 4); reject path-manifest
  / reject main-round it1-alone.
- **Prior art (resolve, do not rubber-stamp):** main-round it1 individual
  `fact-type` pins; main-round it2 `fact-type-bundle` + inclusion; evaluation
  hybrid (bundle pin + exact fact identity in joins); ACM-G1 / ACM-A3 / ACM-A4 /
  ACM-A7. Mechanisms below are re-justified against residual cases 3, 4, 7.
- **Not this design:** ADR draft; exact issue-code bikeshed; citation membership;
  multi-package graphs; UI; reopening ADR-0027 decisions 1–7.

### HEAD probes (committed substrate)

| Probe | Observation |
| --- | --- |
| H1 | `fact-type.v1` properties: `schema, id, title, nature, identity_keys, value_schema, supersession` — **no `version`**. |
| H2 | `bundle.v1` properties: `schema, id, label, fact_types` — **no `version`**. Nested types are full unversioned `fact-type.v1` objects. |
| H3 | `act-bundle-adoption.v1` requires wholesale embedded `bundle` (schema `bundle.v1`); vocabulary entry is body capture, not `(id, version)` pin resolution. |
| H4 | Committed `tax.us.2025.w2-vocabulary` matches H2: bundle `id` only; nested fact types `id` only. |
| H5 | `source-closure-mapping.v1` has `member_fact_type` / `closure_fact_type` as **bare string ids** (no version pins), while `family` is `{id, version}`. |
| H6 | Versioned peers (`rule-artifact`, `parameter-declaration`, `form-field`, `source-family`, mapping, package) all use `version` pattern `^v[0-9]+$`. |

These are the G1/A4/A7 substrate facts. Claiming exact member versions (ADR-0006
decision 6) over the fact surface without schema diffs pretends H1–H4 already
support pin resolution. They do not.

---

## MR-P1 — Fact-surface versioning ⋂ wholesale-adoption reconciliation

### Claim

Exact package membership over the fact surface requires **versioned fact-type
and bundle citizens**, a **dual pin unit** (bundle for vocabulary adoption +
exact fact-type identity in every binding join), and **inclusion joins** that
tie package pins to wholesale workspace adoption so ELX/`input_bindings`,
mapping fact-type edges, and runtime vocabulary cannot drift (ACM-G1, ACM-A7,
ACM-A4).

This design **does not** invent an alternate exact-identity rule that papers
over HEAD. It lands schema successors, then validates packages only against
those successors for the fact surface.

### Schema / contract diffs (paper)

1. **`fact-type.v2`** — all of `fact-type.v1` plus required
   `version: { "type": "string", "pattern": "^v[0-9]+$" }`. Retains ADR-0025
   `optional_default` (determinable scalar → parameter pin) when that field is
   admitted. Historical `fact-type.v1` remains valid unversioned content for
   pre-membership corpora; it is **not** an exact package-member identity.

2. **`bundle.v2`** — required `version` (same pattern); `fact_types` becomes an
   array of **exact nested identities** `{ "id", "version" }` that must resolve
   to published `fact-type.v2` citizens in the corpus (or, equivalently for
   wholesale adoption capture, full nested `fact-type.v2` objects whose
   `(id, version)` match corpus keys). No silent id-only nesting.

3. **`act-bundle-adoption.v2`** — still **wholesale**: the act embeds the full
   `bundle.v2` body (what was adopted is never reconstructed). Kernel validates
   the nested bundle against the schema generation it names. Adoption therefore
   yields a checkable adopted vocabulary set
   `A = { bundle (id, version) → frozenset of fact-type (id, version) }`.

4. **`source-closure-mapping.v2`** (paper-cheap with MR-P1) — upgrade
   `member_fact_type` and `closure_fact_type` from bare strings to exact pins
   `{ "id", "version" }`. Family pin remains `{id, version}`.

5. **`artifact-package.v2` residual fields** (on top of ADR-0027 ratified
   surface):
   - Member role **`fact-type-bundle`**: pin `{ role, id, version }` naming a
     `bundle.v2` citizen. This is the **vocabulary adoption pin unit**.
   - Optional member role **`fact-type`**: pin of an individual `fact-type.v2`
     only when needed as an entrypoint-reachable peer; **not** a substitute for
     bundle vocabulary membership. Binding joins never treat an orphan
     individual pin as workspace-adopted vocabulary without a covering bundle.
   - `input_bindings[].fact_type` is an exact `{id, version}` (ADR-0025 shape),
     not a bare id.

`admitted_schemas` (ADR-0027 decision 3) must list `fact-type.v2` / `bundle.v2`
/ `act-bundle-adoption.v2` / `source-closure-mapping.v2` as used. Unadmitted
generations reject at load — no silent skip.

### Pin unit and inclusion joins

Let `M` be the package’s exact member pin set (ADR-0027 typed graph).

Define the package’s **closed fact surface** `F(P)`:

```
F(P) = ⋃ { nested fact-type (id, version) of each fact-type-bundle member B ∈ M }
     ∪ { (id, version) of each optional individual fact-type member in M }
```

**Outbound joins (must resolve into `F(P)` and into `M` as appropriate):**

| Edge | Resolution |
| --- | --- |
| `input_bindings[].fact_type` | Exact `(id, version) ∈ F(P)` |
| Mapping `member_fact_type` / `closure_fact_type` (v2 pins) | Exact `(id, version) ∈ F(P)` |
| `optional_default` parameter (fact-type.v2) | `parameter` member in `M` |
| Bundle member pin | Corpus `(id, version)` is `bundle.v2`; every nested fact-type pin resolves |

**Inclusion / anti-drift joins (A7):**

| Join | Rule |
| --- | --- |
| **Binding ⊆ bundle** | Every binding-referenced fact-type identity is a nested member of **at least one** package-pinned `fact-type-bundle`. An individual `fact-type` pin alone does **not** satisfy this for binding edges. |
| **Package ⊆ adoption** | At package adoption / run bind: every package `fact-type-bundle` pin `(id, version)` must equal an entry in the workspace’s adopted set `A` from `act-bundle-adoption` acts, with identical nested fact-type set (set equality on nested identities). |
| **No generation swap** | If package pins fact-type `X@v2` via bundle `B@v1`, an adopted bundle `B@v1` that nests `X@v1` (or omits `X`) is **drift** — reject. Id match without version match is not identity. |

**Why dual unit (not it1-alone, not bundle-only):**

- Main-round it1’s individual pins alone fail A7: binding checks can pass while
  wholesale adoption supplies a different vocabulary.
- Bundle-only pins without exact fact identity in joins reintroduce G1/A4: ELX
  and mapping edges become id-fuzzy.
- Hybrid: **bundles pin vocabulary; bindings name exact fact versions; inclusion
  enforces both package-internal and package↔adoption coherence.**

### Corpus resolution rule (ADR-0006 decision 6)

Published fact-type and bundle citizens are keyed by `(id, version)` under the
same registry pattern as other versioned citizens (ADR-0003 / ADR-0027
package-instance immutability for packages; member published-byte verification
as already required by ADR-0027 PC3). Pin resolution is:

```
resolve(pin) = registry[(pin.id, pin.version)]  # absent → MEMBER_ABSENT
```

**HEAD `*.v1` fact types and bundles have no `version` field** — they cannot
appear as the target of an exact pin. A package that admits only
`fact-type.v1` / `bundle.v1` while claiming exact fact pins is either
inexpressible (schema rejects version-bearing pins against v1 citizens) or
rejected at load (`FACT_SURFACE_UNVERSIONED` / `MEMBER_SCHEMA_UNADMITTED`).
There is no “pretend v1 means v1” shim.

### Mapping fact-type gap (A4)

With `source-closure-mapping.v2`, both fact-type fields are exact pins closed
through `F(P)`. A package that pins family + mapping with matching
`admits_symbol` / `authorizes_subtotal` but omits either fact-type identity from
`F(P)` records a contained issue on the mapping member
(`MAPPING_FACT_UNPINNED` / equivalent) and fails adoption. Bare-id mapping.v1
is not admitted into a residual-closed unit that claims exact fact membership.

---

## MR-P2 — Declared composition-obligation trigger

### Claim

Composition license (ADR-0026 decision 4) must be **discoverable as declared
package content** without depending on a composition citizen already being
present (ACM-A3). For every composition-governed published symbol the package
declares, the validator rejects **both** a missing composition member **and** a
missing provenance-only `composition` pin on the producing rule — even when no
composition document exists. Form-fields are presentation-only (ADR-0012) and
are never the obligation authority. The runner carries **no** symbol-name
special cases (Article 11).

### Declaration surface (package content)

On `artifact-package.v2`, add:

```json
"composition_obligations": [
  { "symbol": "tax.us.2025.form1040.line2b.taxable-interest" }
]
```

- Zero or more entries; each `symbol` is a published output symbol of the unit.
- **Discoverability does not consult the composition corpus.** The list is the
  obligation authority. Absence of a composition citizen does not drop the
  entry or skip the check.

### Non-circular enforcement (for each obligation entry `S`)

Contained load-time checks (continue the walk — ADR-0006 decision 3):

1. **Producer:** exactly one adopted package producer for `S`, or a conflict
   rule that **selects** an adopted member producer (ADR-0027 decision 5).
2. **Pin required:** that producer rule **must** carry
   `composition: {id, version}` (rule-artifact generation that admits the
   field). Missing pin → `COMPOSITION_PIN_MISSING` even if no composition
   citizen exists.
3. **Citizen required:** pin resolves to a `composition` member in `M` whose
   `publishes == S`. Absent / wrong version → `COMPOSITION_MEMBER_ABSENT` /
   `MEMBER_ABSENT`.
4. **Provenance-only:** composition pin creates **no** derivation edge
   (ADR-0010 / ADR-0026 decision 4 / ADR-0027).
5. **Bijection:** when the citizen is present, slot set ⇄ rule constituents
   (ADR-0026 decision 2) — `COMPOSITION_SLOT_BIJECTION` on failure.

This is **not** “if composition present then require pin.” The obligation list
fires first; missing citizen and missing pin are both rejectable states.

### Structural multi-source completion (closes bare-sum omit-declaration)

A pure declaration list can be omitted by a careless author. To reject
**undeclared** bare multi-source sums without Article 11 symbol tables, the
validator applies a **structural** trigger on package members (content shape,
not hardcoded line-2b names):

> If a computation member’s value expression aggregates **two or more**
> distinct package-published symbols that are each an `authorizes_subtotal` of
> a pinned `source-family` (multi-family / multi-subtotal fold or explicit
> multi-input sum of those subtots), then that rule’s `publishes` symbol **must**
> appear in `composition_obligations`.

- Missing list entry → `COMPOSITION_OBLIGATION_UNDECLARED` (then stops short of
  inventing a composition; the unit is not adoptable).
- Present entry → full checks 1–5 above, which reject missing pin/citizen.

Single-family subtotals and ordinary non-composition rules are unaffected.
Wages line-1a (one producer, no multi-family fold) does not trip the structural
trigger. Line-2b-shaped units trip it and must declare.

### Explicit rejects (floor integrity)

| Anti-pattern | Disposition |
| --- | --- |
| Infer obligation only from co-located composition file | **Reject as design** — circular; fails case 7 |
| Hardcode `tax.us.2025...line-2b` in runner/validator | **Out of floor** (Article 11) — case 9 |
| Place obligation solely on form-field | **Out of floor** (ADR-0012) — case 9 |
| `composition` as input/choice edge | **Out of floor** (ADR-0010 / 0026 / 0027) |

---

## Claim → contract → validator → issue map

| Claim | Paper change | Validator / adoption behavior | Issue (illustrative; strings Gate-5 deferred) | Level |
| --- | --- | --- | --- | --- |
| Fact types exact-versioned | `fact-type.v2` + `version` | resolve `(id,version)`; v1 not pin-target | `FACT_SURFACE_UNVERSIONED` / `MEMBER_ABSENT` | static |
| Bundles exact-versioned | `bundle.v2` + versioned nested pins | pin + nested resolve | `MEMBER_ABSENT` / `BUNDLE_NESTED_UNPINNED` | static |
| Wholesale adoption reconciled | `act-bundle-adoption.v2` embeds `bundle.v2` | package bundle pins ⊆ adopted `A` with nested set equality | `FACT_PIN_ADOPTION_DRIFT` | static |
| Binding ⊆ bundle | package joins | every `input_bindings` / mapping fact pin ∈ some pinned bundle | `FACT_BINDING_NOT_IN_BUNDLE` | static |
| Mapping fact edges | `source-closure-mapping.v2` pins | both fact fields ∈ `F(P)` | `MAPPING_FACT_UNPINNED` | static |
| Obligation declared | package `composition_obligations` | list drives checks without composition present | — | static |
| Bare multi-source | structural ≥2 family-subtotal fold | must list `publishes` in obligations | `COMPOSITION_OBLIGATION_UNDECLARED` | static |
| Missing pin / citizen | ADR-0026 pin + member | reject both absences for listed symbols | `COMPOSITION_PIN_MISSING` / `COMPOSITION_MEMBER_ABSENT` | static |
| Article 11 / form-field authority | none (negative design) | no symbol table; form-field not obligation source | design reject | static |

---

## Gate-2 cases

### MR-P1

**Case 1 — Positive: versioned fact surface in a closed package.**  
Unit `U-wages@v1` (`artifact-package.v2`): pins computation rule, form-field,
`fact-type-bundle` `tax.us.2025.w2-vocabulary@v2` nesting
`tax.us.2025.w2.box1-wages@v2` + `tax.us.2025.w2.source-closure@v2`, parameter
as required. `input_bindings` / rule refs name those exact fact-type versions.
`admitted_schemas` includes `fact-type.v2`, `bundle.v2`, `rule-artifact.v*`,
`form-field.v1`. **Validates.**

**Case 2 — Positive: bundle adoption inclusion.**  
Workspace adoption act embeds the same `bundle.v2` body at `@v2`. Package pin
matches adopted `(id, version)` and nested set. Join accepts; runtime
vocabulary for the unit is exactly `F(P)`.

**Case 3 — Negative: unversioned / unresolvable pin (G1, mandatory).**  
Against HEAD: pin `{role: fact-type, id: tax.us.2025.w2.box1-wages, version: v1}`
cannot resolve — citizen has no `version` field (H1/H4). A package claiming
exact fact versions while admitting only `fact-type.v1` / `bundle.v1` is
**rejected** (`FACT_SURFACE_UNVERSIONED` / unadmitted generation) or
**inexpressible** once pin targets require `*.v2`. Design picks: **schema
successors required; no HEAD pretence.**

**Case 4 — Negative: pin/bundle drift (A7, mandatory).**  
(a) Package pins / binds `age@v2` via bundle `B@v1`; adopted act supplies `B@v1`
omitting `age` or nesting `age@v1` → **`FACT_PIN_ADOPTION_DRIFT`**.  
(b) Rule binding names fact identity not nested in any package-pinned bundle →
**`FACT_BINDING_NOT_IN_BUNDLE`**. Individual orphan pin without covering bundle
does not pass.

**Case 5 — Negative: mapping fact-type gap (A4).**  
Family + mapping + subtotal joins intact; `member_fact_type` / `closure_fact_type`
pins absent from `F(P)` → **`MAPPING_FACT_UNPINNED`**. Validates only when both
identities sit in a pinned bundle’s nested set.

### MR-P2

**Case 6 — Positive: composition-governed unit.**  
Line-2b-shaped unit: `composition_obligations: [{symbol: line2b}]`, composition
citizen, slot bijection, rule with matching `composition` pin, form-field,
families/mappings/subtotals, fact bundles. **Validates.**

**Case 7 — Negative: bare sum without composition (A3 core, mandatory).**  
Unit ships multi-family publishing rule + form-field; **no** composition
citizen; **no** composition pin. Structural trigger requires `publishes` in
`composition_obligations`.  
- If undeclared → **`COMPOSITION_OBLIGATION_UNDECLARED`**.  
- If declared (obligation list flags the symbol) → **`COMPOSITION_PIN_MISSING`**
  and **`COMPOSITION_MEMBER_ABSENT`** (both; non-circular).  
Does **not** rely on “if composition present then require pin.”

**Case 8 — Negative: obligation without pin.**  
Obligation lists `S`; matching composition citizen is a member; producing rule
omits `composition` pin → **`COMPOSITION_PIN_MISSING`** (ADR-0026 decision 4).

**Case 9 — Negative: Article 11 / presentation leak.**  
Design that hardcodes line-2b symbol names in the runner, or treats form-field as
obligation authority → **out of floor**; rejected in favor of package
`composition_obligations` + structural multi-source shape only.

---

## Explicit unresolved (not fiat)

1. Exact issue-code strings and registry storage layout (Track 4 / Gate 5).
2. Whether reverse-reachability must also treat every nested fact-type as a
   graph node with entrypoint paths (inbound) — outbound + inclusion suffice for
   the residual floor; inbound may reuse ADR-0027 entrypoint roots.
3. Migration tooling for rewriting committed `bundle.v1` content into `bundle.v2`
   (production; not required for paper settlement).
4. Multi-package fact-surface sharing beyond one content unit.

## Floor check (micro-round Gate 6)

- Checkable fact-surface membership without pretending HEAD has version fields
  (cases 3–4) → **met** via `*.v2` + dual pin unit + inclusion.
- Non-circular composition-obligation trigger rejecting bare sums (case 7)
  without runner symbol special cases → **met** via package declaration +
  structural multi-source completion.
- Mapping fact-type closure (case 5) ratified with MR-P1 → **met** on paper.
