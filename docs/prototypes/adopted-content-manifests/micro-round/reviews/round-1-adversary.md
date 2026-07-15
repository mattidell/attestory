# Adversary Review — ACM Micro-Round Residuals (Round 1)

Date: 2026-07-15. Seat: Medium-tier Adversary Reviewer (owner-launched, independent
context). Role: `roles/reviewer-adversary.md`. Plan: `micro-round/plan.md`.

**Exhibits under attack:** `it1/design.md` + `examination-it1.md` (incumbent);
`it2/design.md` + `examination-it2.md` (clean-room rival).

**Independence:** Did not read `reviews/round-1-governance.md`, any residual
ADR-0028 draft/notes, or any other reviewer output. Paper attacks only; grounded
in `docs/governance/`, accepted ADRs 0003, 0006, 0010, 0012, 0014, 0025, 0026,
0027, and committed HEAD schemas (`fact-type.v1`, `bundle.v1`,
`act-bundle-adoption.v1`, `source-closure-mapping.v1`, `artifact-package.v1`).

**Advisory.** Findings do not repair designs, amend ADR-0027, or draft residual
ADR text.

---

## Understanding (echo before findings)

| Item | Understanding |
| --- | --- |
| **MR-P1** | Fact-surface versioning ⋂ wholesale-adoption reconciliation: how exact member versions apply to fact types/bundles given HEAD unversioned `fact-type.v1` / `bundle.v1` and wholesale `act-bundle-adoption`; pin unit; inclusion joins so ELX/`input_bindings` and runtime vocabulary cannot drift; mapping fact-type edges closed through the same surface. ADR-0006 decision 6 without pretending HEAD already has `version`. |
| **MR-P2** | Declared composition-obligation trigger: package/rule content declares which published symbols are composition-governed **without** circular dependence on a composition citizen already being present; reject missing composition citizen **and** missing provenance-only `composition` pin; ADR-0026 decision 4; no runner symbol special cases (Article 11); form-fields presentation-only (ADR-0012). |
| **ADR-0027 floor (settled — not re-opened)** | Extend-not-fork `artifact-package.v2`; typed closed graph; role canon + load-time role-semantic divergence; `admitted_schemas` (no package-embedded schema sha256); package-instance immutability; exclusive execution projection; form-field producer integrity; `composition` pin provenance-only; reject path-manifest / reject main-round it1-alone. Attack residual mechanisms only (N1/N2). |
| **Independence exclusions** | No governance review; no ADR-0028 drafts/notes; no other reviewer output. |
| **Required output** | This file only. Findings **MR-A1…**. Concrete input → expected → per-design fail/survive. Classify each finding. Verdict **per proposition per design**. No repairs, no commits, no other-file edits, no ADR decisions. |

### Design shapes (attack surface summary)

| | **it1 (incumbent)** | **it2 (rival)** |
| --- | --- | --- |
| MR-P1 pin unit | Dual: `fact-type-bundle` vocabulary pin + exact fact `(id,version)` in joins; optional individual `fact-type` not a binding substitute | Individual `fact-type` pins define fact surface; role enum adds `fact-type-bundle` but validation text does not use bundle pins |
| Schema successors | `fact-type.v2`, `bundle.v2`, `act-bundle-adoption.v2`, `source-closure-mapping.v2` | `fact-type.v2`, `bundle.v2`; package role enum; **no** adoption-act successor; **no** mapping-field version upgrade |
| Inclusion | Binding ⊆ package-pinned bundle; package bundle pins ⊆ adopted set `A` with nested set equality | Each pinned fact-type must appear in some adopted `bundle.v2` at matching version |
| MR-P2 trigger | Package field `composition_obligations[{symbol}]` + structural multi-source fold (≥2 family-`authorizes_subtotal` inputs → must list `publishes`) | Separate `composition-obligation.v1` governance citizen pinned with `role: governance` |
| Bare-sum story | Structural force-declare, then pin+citizen checks (non-circular for listed / structurally forced symbols) | Checks only for symbols gathered from pinned obligation citizens |

---

## Attack method

Each finding states a synthetic package/workspace **input**, the **expected
result** under residual Gate-2 / ADR-0006/0026 intent, then where **it1** and
**it2** fail or survive. Classifications:

- **decision-blocking** — residual proposition cannot be claimed settled; Track 4
  membership closure must not ratify this mechanism as-is.
- **production condition** — mechanism direction may hold if named condition is
  met before implementation.
- **non-blocking** — documentation, issue-code, or narrow edge that does not
  overturn the proposition.

---

## Findings

### MR-A1 — G1 residual: exact-version claims against unversioned HEAD citizens

**Attack input.**

```text
Corpus C (HEAD-shaped):
  fact-type citizen:
    { "schema": "fact-type.v1", "id": "tax.us.2025.w2.box1-wages",
      /* no version field */, ... }

Package P:
  admitted_schemas includes fact-type.v1 (or omits any fact-type.v2 admission)
  members include pin:
    { "role": "fact-type", "id": "tax.us.2025.w2.box1-wages", "version": "v1" }
  # or ELX input_bindings name the same exact pin
```

**Expected.** Reject or make the pin **inexpressible**. Exact membership
(ADR-0006 decision 6) cannot resolve against a citizen with no checkable
version. Id-only fallback is forbidden. Omitting a schema-successor migration
while shipping version-bearing pins is a design failure.

| Design | Result |
| --- | --- |
| **it1** | **Survives.** Explicit HEAD probes H1–H4; `fact-type.v2` / `bundle.v2` required; resolve is `registry[(id,version)]`; v1 is not a pin-target; `FACT_SURFACE_UNVERSIONED` / `MEMBER_SCHEMA_UNADMITTED`. Case 3 spelled as mandatory. |
| **it2** | **Survives the pin-vs-unversioned-citizen cut** (examination: unresolvable pin → `UNVERSIONED_OR_UNRESOLVABLE_PIN`). **Weak on migration completeness:** design never specifies `act-bundle-adoption` successor or how wholesale adoption yields versioned nested fact identities from committed `act-bundle-adoption.v1` (embeds `bundle.v1` only). Package can require `fact-type.v2` while the only adoption path still captures unversioned bodies — G1 is only half-closed (see MR-A7). |

**Classification:** **production condition** for it2 (must name adoption-act /
bundle-body migration with nested exact identities); it1 clear on the pin side.
Not decision-blocking against either design's *stated* reject of unversioned
pin targets.

---

### MR-A2 — G1 residual: id-only resolution / omit successor on mapping edges

**Attack input.**

```text
Package P (claims exact fact membership):
  pins source-closure-mapping M@v1 with HEAD field shapes:
    member_fact_type: "tax.us.2025.w2.box1-wages"   # bare string id
    closure_fact_type: "tax.us.2025.w2.source-closure"
  pins fact-type tax.us.2025.w2.box1-wages@v2
  # corpus also has (or later publishes) box1-wages@v1 with different value_schema

Workspace: adopts whatever vocabulary the design requires for the box1@v2 pin.
```

**Expected.** Mapping fact-type edges must be exact identities closed through
the fact surface (case 5 / A4 lineage). Bare-id mapping fields while the package
claims exact membership are **reject** or **inexpressible** once the residual
surface is admitted — not silent id match to whichever generation is pinned.

| Design | Result |
| --- | --- |
| **it1** | **Survives.** `source-closure-mapping.v2` upgrades both fields to `{id,version}` ∈ `F(P)`. Bare-id mapping.v1 not admitted into a residual-closed unit. |
| **it2** | **Fails.** Design checks `mapping[member_fact_type]` (a bare id string) with `ft_id not in fact_surface` where `fact_surface` is `id → version`. That is **id-only** membership: `box1-wages` present at `@v2` satisfies a mapping that never names a version. Generation swap on the mapping edge is invisible. No mapping schema successor is proposed. |

**Classification:** **decision-blocking** for **it2 MR-P1** (A4/G1 through mapping).
**it1:** survives (non-finding against it1).

---

### MR-A3 — A7 drift: binding identity vs adopted / package vocabulary

**Attack input (A7 classic).**

```text
Package P:
  computation rule R publishes wages-line with:
    input_bindings: [ { fact_type: { id: "tax.us.2025.w2.box1-wages", version: "v2" } } ]
  # it1 also pins fact-type-bundle B@v1 nesting box1-wages@v2
  # it2 pins only individual fact-type box1-wages@v2 (no bundle pin used)

Workspace adoption act A:
  embeds bundle body B@v1 nesting box1-wages@v1   # different generation
  # or omits box1-wages entirely while still "adopting B"
```

**Expected.** Reject pin/bundle (or pin/adoption) drift. Binding must not pass
while workspace vocabulary supplies a different generation or omits the type.

| Design | Result |
| --- | --- |
| **it1** | **Survives.** Nested set equality on package `fact-type-bundle` pins vs adopted set `A`; generation swap → `FACT_PIN_ADOPTION_DRIFT`. Binding not nested in any package-pinned bundle → `FACT_BINDING_NOT_IN_BUNDLE`. |
| **it2** | **Partial survive / partial fail.** Inclusion requires pinned fact-type `(id,version)` appear in *some* adopted bundle at matching version — generation swap on the pinned fact is rejected (`PIN_BUNDLE_VERSION_DRIFT` / `PIN_NOT_ADOPTED`). **Fails the package-claimed vocabulary half of A7:** (1) no package-level bundle pin is enforced, so the package never names which bundle body it closes over; (2) design text never states that `input_bindings[].fact_type` must resolve into the package fact surface — only that fact-type *pins* define the surface and mapping fields must be in it. A rule whose binding names `box1-wages@v2` while the package pin table omits that fact-type (binding-only reference) is not rejected by the written joins. |

**Concrete it2 binding-omit subcase.**

```text
Package P2:
  members: [ computation R@v1, form-field F@v1 ]   # no fact-type pins
  R.input_bindings → box1-wages@v2
Workspace: adopts bundle containing box1-wages@v2
```

**Expected:** reject (fact surface incomplete; ELX not closed).  
**it2 written validator:** fact_surface empty; mapping loop N/A; no binding walk →
**validates** under the published pseudocode. **it1:** binding ⊄ `F(P)` / not in
pinned bundle → reject.

**Classification:** **decision-blocking** for **it2 MR-P1** (A7 incomplete;
missing binding→surface join). **it1:** survives main A7 cases.

---

### MR-A4 — A7 / dual-unit hole: orphan individual pin closes mapping without adoption cover (it1)

**Attack input.**

```text
Package P (it1 dual unit):
  members:
    - fact-type-bundle B@v1 nesting { box1-wages@v2 }   # wages covered
    - fact-type age@v2                                   # orphan individual pin
    - source-closure-mapping M@v2:
        family: fam@v1
        member_fact_type: { id: age, version: v2 }
        closure_fact_type: { id: age-closure, version: v2 }
    - source-family fam@v1, computation, form-field as needed
  # age-closure@v2 also only as individual pin (or nested nowhere)

Workspace adoption:
  act embeds B@v1 with nested set { box1-wages@v2 } only
  # no adopted vocabulary entry for age@v2
```

**Expected under residual anti-drift intent.** Mapping fact-types are part of the
fact surface and must not drift from adopted vocabulary. Orphan individual pins
must not launder mapping (or other) edges past package↔adoption inclusion.

| Design | Result |
| --- | --- |
| **it1** | **Fails this cut.** Design: `F(P)` includes optional individual `fact-type` members; mapping pins need only `(id,version) ∈ F(P)`. Binding ⊆ bundle is **restricted to binding edges**, not mapping. Package ⊆ adoption join is defined only over `fact-type-bundle` pins — individual pins are **not** checked against adopted set `A`. Mapping through orphan `age@v2` passes while adoption omits age. Contradicts the design's own anti-orphan prose for bindings, applied unevenly. |
| **it2** | Different pin model. Mapping requires member/closure ids ∈ fact_surface (package pins). Those pins still need appearance in some adopted bundle — so this specific orphan path is **blocked** for it2 *if* fact-type pins are required for mapping fields. (it2 still fails MR-A2 id-only mapping.) |

**Classification:** **production condition** for **it1 MR-P1** — extend inclusion
so *every* identity in `F(P)` used by mapping/binding is nested under a
package-pinned bundle that participates in package⊆adoption set equality; or
forbid individual pins from satisfying mapping closure. Not the classic A7
bundle-vs-binding miss (that it1 blocks), but a dual-unit completeness hole.

---

### MR-A5 — A4 mapping gap: family/subtotal intact, fact-types absent from surface

**Attack input.**

```text
Package P:
  pins: source-family SF@v1 (authorizes_subtotal S),
        source-closure-mapping M@v1/v2 (family → SF, admits_symbol S),
        computation publishing S, form-field binds S
  does NOT pin / close member_fact_type or closure_fact_type into fact surface
  # family pin, admits_symbol, subtotal producer all coherent
```

**Expected.** Reject (`MAPPING_FACT_UNPINNED` / equivalent). Case 5.

| Design | Result |
| --- | --- |
| **it1** | **Survives** when residual mapping.v2 is admitted: both fact pins must ∈ `F(P)`. |
| **it2** | **Survives the absence cut** (`MAPPING_FACT_TYPE_GAP` if id missing from fact_surface). **Does not survive versioned A4** (MR-A2): presence is id-only. |

**Classification:** Case-5 absence: both designs reject. Residual versioned A4 is
absorbed into **MR-A2** (decision-blocking it2).

---

### MR-A6 — A3 bare multi-source sum: no composition citizen, no pin, omit obligation

**Attack input (mandatory case 7).**

```text
Package P_bare:
  members:
    - computation R@v1:
        publishes: "tax.us.2025.form1040.line2b.taxable-interest"
        value: sum( of three package-published family subtots
                    SF1.authorizes_subtotal,
                    SF2.authorizes_subtotal,
                    SF3.authorizes_subtotal )
        # NO composition pin on R
    - form-field FF binds that symbol
    - source-family SF1, SF2, SF3 + mappings + subtotal rules
    # NO composition citizen member
    # NO composition_obligations field (it1)
    # NO composition-obligation.v1 governance pin (it2)
```

**Expected.** Reject. Must not rely on “if composition present then require pin.”
Obligation must be discoverable (declared content or equivalent non-circular
structural check). Bare sum must not validate.

| Design | Result |
| --- | --- |
| **it1** | **Survives the family-subtotal fold shape.** Structural trigger: ≥2 distinct package-published symbols each an `authorizes_subtotal` of a pinned source-family → `publishes` must appear in `composition_obligations`. Undeclared → `COMPOSITION_OBLIGATION_UNDECLARED`. If author adds the list entry without citizen/pin → both `COMPOSITION_PIN_MISSING` and `COMPOSITION_MEMBER_ABSENT`. Non-circular for this shape. |
| **it2** | **Fails hard.** Obligation symbols are gathered only from pinned `composition-obligation.v1` citizens. With none pinned, `obligated_symbols = ∅` and the validation loop is a no-op. Missing citizen/pin never consulted. **Bare sum validates.** This is exactly the circular/omit-declaration hole residual N2 was chartered to close. |

**Classification:** **decision-blocking** for **it2 MR-P2**. **it1:** survives case 7
for the multi-family fold shape (see MR-A8 for structural miss).

---

### MR-A7 — A3 structural miss: multi-source without family-subtotal shape (it1)

**Attack input.**

```text
Package P_raw:
  members:
    - fact-type-bundle(s) covering three interest amount fact types
    - computation R@v1:
        publishes: "tax.us.2025.form1040.line2b.taxable-interest"
        value: add( ELX(box1-amount), ELX(box3-amount), ELX(oid-amount) )
        # three fact ELX inputs — multi-source sum of raw amounts
        # NO composition pin
    - form-field binds line2b symbol
    # intentionally OMIT source-family / mapping members
    # omit composition_obligations
    # omit composition citizen
```

**Expected under residual A3 intent.** A multi-source publishing rule for a
composition-shaped line must not validate as a bare sum. Designs that only force
obligation when family machinery is already present leave an omit path.

| Design | Result |
| --- | --- |
| **it1** | **Fails this cut.** Structural trigger requires inputs that are each an `authorizes_subtotal` of a **pinned** source-family. No families pinned → trigger does not fire → no `COMPOSITION_OBLIGATION_UNDECLARED` → pin/citizen checks never run → **validates**. Author omits the declaration surface entirely. |
| **it2** | Also fails (MR-A6) for any bare sum without obligation citizen — broader miss. |

**Classification:** **decision-blocking** for **it1 MR-P2** completeness of
non-circular bare-sum rejection (structural trigger is incomplete). Shared
theme with it2: declaration can be omitted unless the force-declare net is
tighter than “already using family subtots.”

*Note:* A narrower reading of case 7 (“line-2b-shaped unit that already has
families”) would demote this to production condition. This review treats residual
A3 as requiring that **no** multi-source publishing path validates without
composition license, not only the family-fold path — consistent with “must not
rely on if composition present” and “bare sum cannot omit the declaration.”

---

### MR-A8 — Obligation without pin (case 8)

**Attack input.**

```text
Package P_pinless:
  # it1: composition_obligations: [{ symbol: line2b }]
  # it2: pins composition-obligation.v1 with symbol: line2b
  members also include:
    - composition citizen C@v1 with publishes: line2b, slots OK
    - computation R publishes line2b with constituents matching slots
      but R omits composition: {id, version} pin
    - form-field binds line2b
```

**Expected.** Reject `COMPOSITION_PIN_MISSING` (ADR-0026 decision 4). Citizen
presence must not waive the pin.

| Design | Result |
| --- | --- |
| **it1** | **Survives.** Obligation list fires; pin required regardless of citizen presence. |
| **it2** | **Survives case 8 when obligation + composition members are both present** (examination checks rule pins for `role == composition`). **Adjacent defect:** if obligation is present but composition citizen is missing, pseudocode `continue`s after `COMPOSITION_CITIZEN_MISSING` and **skips** the pin check — so dual-defect reporting is incomplete (pin missing not always recorded). Still rejects via citizen missing. |

**Classification:** Case 8 core: both **survive**. Incomplete dual-issue walk on
it2: **non-blocking** (contained issues / ADR-0006 decision 3 quality).

---

### MR-A9 — Article 11 / presentation leak

**Attack A — runner symbol table.**

```text
Validator/runner fragment (hypothetical implementation of a design):
  if publishes == "tax.us.2025.form1040.line2b.taxable-interest":
      require_composition_pin()
```

**Expected.** Out of floor (Article 11 / E11.3). Obligation must come from
declared content, not hardcoded symbols.

| Design | Result |
| --- | --- |
| **it1** | **Survives as design.** Explicitly out-of-floor; uses package list + structural shape only. No symbol table in the residual contract. |
| **it2** | **Survives as design intent** (obligation citizen carries `symbol`). **Examination leak:** pseudocode special-cases `citizen["schema"] == "taxable-interest-composition.v1"` when gathering composition members — a schema-name whitelist for “what counts as composition,” not a line-2b string, but still runner-resident tax-structure knowledge. A future `oid-composition.v1` / generic `composition.v1` would be invisible unless the runner list grows (Article 11 pressure). |

**Attack B — form-field as obligation authority.**

```text
Package: form-field binds line2b; no package obligations; no obligation citizen;
         multi-source rule without composition pin
# Design under test claims form-field presence implies composition obligation
```

**Expected.** Out of floor (ADR-0012 presentation-only).

| Design | Result |
| --- | --- |
| **it1** | Rejects that pattern as design; form-field never obligation source. |
| **it2** | Same stated reject; obligation only from governance citizen. |

**Classification:** Attack B: both survive. Attack A it2 schema whitelist:
**production condition** (composition membership must be by role/pin or
admitted composition schema family via `admitted_schemas` / role canon — not a
hardcoded single `$id` string in validator prose).

---

### MR-A10 — Adoption reconciliation: wholesale act body vs pin resolution

**Attack A — nested set ≠ package pin claim.**

```text
Package pins vocabulary as:
  it1: fact-type-bundle B@v2 nested { wages@v2, closure@v2 }
  it2: fact-type pins wages@v2, closure@v2

Adoption act wholesale body:
  bundle id B, version v2 (if versioned), nested { wages@v1, closure@v2 }
  # body captured whole — reconstruction forbidden (HEAD act-bundle-adoption posture)
```

**Expected.** Reject. Package pin resolution must not accept a wholesale body
whose nested exact identities differ from what the package closes over.

| Design | Result |
| --- | --- |
| **it1** | **Survives.** `act-bundle-adoption.v2` + nested set equality on package bundle pin vs adopted `A`. |
| **it2** | **Survives fact-level generation mismatch** (wages@v2 pin vs nested wages@v1 → drift). **Fails package↔bundle identity reconciliation:** package never pins `B@v2`, so it cannot detect “package claims bundle B@v2 but adopted body is B@v3 with same fact pins,” nor “two bundles supply the same fact pins with different bundle-level provenance.” Wholesale adoption identity is only indirectly constrained. |

**Attack B — package role `fact-type-bundle` dead / unused (it2).**

```text
Package P:
  members:
    - { role: fact-type-bundle, id: B, version: v2 }  # nested in corpus: {wages@v2}
    - computation with input_bindings wages@v2
  # omits individual fact-type pin for wages
Workspace: adopts B@v2 correctly
```

**Expected.** Either bundle pins participate in `F(P)` (accept) or the role is
not part of the residual surface (inexpressible). Must not silently ignore the
pin while also requiring individual fact-type pins for the same surface.

| Design | Result |
| --- | --- |
| **it1** | Bundle pin is the primary vocabulary unit; nested facts enter `F(P)`. Accept when consistent. |
| **it2** | Role enum includes `fact-type-bundle`, but validation gathers fact surface only from `role == fact-type`. Bundle pin is ignored → fact_surface misses wages → if bindings were checked they would fail; as written (MR-A3), bindings may not be checked — **incoherent pin unit**. |

**Attack C — it2 adoption path still HEAD `bundle.v1`.**

```text
Committed act-bundle-adoption.v1 embeds bundle.v1 (no bundle version;
nested fact-type.v1 without version).
Package requires fact-type.v2 pins (id, version).
```

**Expected.** Design must specify successor adoption capture or an explicit
bridge. Leaving HEAD adoption unversioned while requiring versioned fact pins
makes positive case 2 **unimplementable** on committed substrate.

| Design | Result |
| --- | --- |
| **it1** | Names `act-bundle-adoption.v2` embedding `bundle.v2`. Positive cases 1–2 are expressible on paper. |
| **it2** | **Fails.** No adoption-act schema diff. Inclusion assumes `adopted_bundles` with versioned nested `fact_types`, but the only committed act shape cannot supply them. |

**Classification:** Attack A/B/C together: **decision-blocking** for **it2 MR-P1**
(adoption reconciliation incomplete; pin unit incoherent). **it1:** survives A/C;
B N/A.

---

### MR-A11 — Package pins bundle version ≠ adopted nested set (explicit A7 adoption form)

**Attack input.**

```text
Corpus publishes:
  bundle B@v1 nested { wages@v2, age@v2 }
  bundle B@v2 nested { wages@v2 }            # age dropped in v2

Package (it1): pins fact-type-bundle B@v2, bindings use wages@v2 only.
Workspace: user adopts act that embedded B@v1 body (still current on disk /
           mistaken re-use), nested { wages@v2, age@v2 }.
```

**Expected.** Reject: package pin `(B, v2)` must equal an adopted entry with
**identical** nested set — not merely “shares some fact pins.”

| Design | Result |
| --- | --- |
| **it1** | **Survives** if adoption records `B@v1` vs package `B@v2` (id,version mismatch) or nested set inequality. |
| **it2** | Package does not pin B. Pins wages@v2 only; adopted B@v1 body contains wages@v2 → **accepts**. Extra age@v2 in workspace vocabulary is invisible to package inclusion. Runtime exclusive projection (ADR-0027 floor) may hide age for *package members*, but wholesale adoption still took up age — package↔adoption reconciliation is not set-equal. Drift of “what the user adopted” vs “what the package claims” remains. |

**Classification:** **decision-blocking** for **it2 MR-P1** (bundle-level
reconciliation absent). Reinforces MR-A10.

---

### MR-A12 — it2 composition gather hardcodes composition schema; pin role vs schema

**Attack input.**

```text
Package pins:
  - composition-obligation.v1 for symbol line2b
  - composition member with schema "composition.v1" (generic) or
    "taxable-interest-composition.v2", publishes line2b
  - rule with composition pin to that member
```

**Expected.** Citizen presence detected by package role `composition` /
admitted composition schemas, not a single hardcoded schema const in
examination code.

| Design | Result |
| --- | --- |
| **it1** | Pin resolves to `composition` member in `M` with `publishes == S` — role-based. Survives. |
| **it2** | Design prose says role `composition` for the pin check; examination gather uses `taxable-interest-composition.v1` only. Generic composition members not found → false `COMPOSITION_CITIZEN_MISSING` or vacuous pin match. |

**Classification:** **production condition** for it2 (align gather with role canon
/ admitted composition schema family). Related to MR-A9.

---

## Cross-cut matrix (required attack themes)

| Theme | Finding | it1 | it2 |
| --- | --- | --- | --- |
| G1 unversioned citizens | MR-A1 | survive | survive pin; weak migration |
| G1 id-only / successor omit | MR-A2 | survive | **fail** mapping versions |
| A7 pin vs adopted / binding | MR-A3, MR-A11 | survive | **fail** binding join + bundle claim |
| A7 orphan dual-unit | MR-A4 | **fail** mapping via orphan pin | N/A / other model |
| A4 mapping gap (absent) | MR-A5 | survive | survive absence; fail versioned |
| A3 bare sum omit declaration | MR-A6, MR-A7 | fail raw multi-ELX (A7); survive family-fold | **fail** all bare omit |
| Obligation without pin | MR-A8 | survive | survive |
| Article 11 / form-field authority | MR-A9 | survive | intent OK; schema whitelist PC |
| Adoption reconciliation | MR-A10, MR-A11 | survive | **fail** |

---

## Verdicts (per proposition per design)

### it1 (incumbent)

| Proposition | Verdict | Rationale |
| --- | --- | --- |
| **MR-P1** | **Conditionally acceptable** (not clean settle) | Core G1 (unversioned pin targets), classic A7 binding/adoption nested equality, and A4 absence are paper-solid with explicit schema successors and dual pin unit. **MR-A4** leaves mapping closure through orphan individual pins outside package⊆adoption — production condition before Track 4. Not decision-blocking on the mandatory case 3–4 path if individual pins are restricted or inclusion is extended. |
| **MR-P2** | **Not settled (decision-blocking residual)** | Family-subtotal structural force-declare **does** break the circular “if composition present” pattern for the main line-2b fold (case 7 primary shape) and case 8 is clean. **MR-A7** shows a multi-source bare sum that omits families, obligations, citizen, and pin still validates — declaration remains omittable. Residual N2 requires a non-omittable net; it1's net has a hole. |

### it2 (clean-room rival)

| Proposition | Verdict | Rationale |
| --- | --- | --- |
| **MR-P1** | **Reject (decision-blocking)** | Multiple independent breaks: no `input_bindings` → fact-surface join (MR-A3); mapping fact fields remain id-only (MR-A2); no `act-bundle-adoption` successor / wholesale nested exact identities (MR-A10); package does not pin or set-equal bundle vocabulary (MR-A10/A11); `fact-type-bundle` role is dead weight. Does not meet Gate 6 fact-surface floor. |
| **MR-P2** | **Reject (decision-blocking)** | Obligation discoverability depends entirely on an author-supplied governance citizen. Omitting that citizen yields empty obligation set and **no checks** (MR-A6) — the ACM-A3 circularity residual in pure form. Case 8 works only when the author already declared; case 7 mandatory bare sum does not. Article 11 intent is stated but examination special-cases composition schema names (MR-A9/A12). |

### Comparative note (high value asymmetries)

| Break | Hits |
| --- | --- |
| Bare sum with zero obligation artifacts validates | **it2 only** (total); **it1** only for non-family multi-ELX |
| Binding ELX not closed into package fact surface | **it2 only** |
| Mapping fact-type version identity | **it2 only** (it1 upgrades pins) |
| Orphan individual pin + mapping bypasses adoption set equality | **it1 only** |
| Wholesale adoption act still unversioned on paper | **it2 only** |
| Obligation without pin while citizen present | neither (both reject) |
| Form-field as sole obligation authority | neither (both reject as design) |

---

## Gate-2 case scoreboard (adversary view)

| Case | it1 | it2 |
| --- | --- | --- |
| 1 Positive versioned surface | met on paper | claimed; undermined by missing binding join & adoption successor |
| 2 Positive adoption inclusion | met on paper (`act-bundle-adoption.v2`) | not expressible on HEAD adoption shape; no act successor |
| 3 G1 unversioned pin **(mandatory)** | met | met for pin resolve; incomplete migration story |
| 4 A7 drift **(mandatory)** | met for binding/bundle/adoption equality; hole on mapping+orphan (MR-A4) | **not met** (no binding walk; no bundle pin equality) |
| 5 A4 mapping gap | met (v2 exact pins) | absence met; versioned identity **not met** |
| 6 Positive composition unit | met | met if obligation+composition+pin authored |
| 7 Bare sum **(mandatory)** | met for multi-family fold; **not met** for raw multi-ELX omit (MR-A7) | **not met** |
| 8 Obligation without pin | met | met when obligation present |
| 9 Article 11 / presentation | met as design | intent met; schema whitelist PC |

---

## Summary for foreman triage

1. **Neither design fully settles both propositions.** it2 fails both residual floors on decision-blocking counterexamples. it1 nearly settles MR-P1 (one production-condition dual-unit hole) but does **not** fully settle MR-P2 because bare multi-source sums can omit the declaration surface when they avoid the family-subtotal structural pattern.
2. **Highest-value single breaks:** it2 empty-obligation bare sum (MR-A6); it2 missing binding→surface join (MR-A3); it1 structural-trigger bypass (MR-A7).
3. **Do not ratify residual ADR text** from either exhibit alone without closing the decision-blocking items. This review does not draft ADR-0028 or choose a hybrid.

— End round-1 adversary review (MR-A1–MR-A12) —
