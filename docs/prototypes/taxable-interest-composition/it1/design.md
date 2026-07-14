# Taxable-Interest Composition — Iteration 1 Design (Incumbent)

Date: 2026-07-14. Builder: incumbent. Evidence depth: Rung 2 (paper schema/canon diffs and traces against committed runner and ratified horizon/currency machinery). Working location: `docs/prototypes/taxable-interest-composition/it1/`. No repository modifications beyond this design and `examination-it1.md`.

## Scope, paper boundary, prior-art boundary, stop conditions

**Scope.** Design TIC-P1 (coextensive Form 1040 line-2b universe + checkable coextensiveness declaration) and TIC-P2 (honest coextensive zero + late-member lifecycle through existing edges only). Discharge all six Gate-2 cases; cases 5 and 6 are mandatory.

**Rung-2 / paper boundary.** Static design only: versioned schema/canon diffs on paper, composition and lifecycle traces against the committed runner (`packages/derivation/`) and ratified horizon/currency machinery (`packages/kernel/horizons.py`, `currency.py`, ADR-0017). Throwaway probes, if any, stay outside the repository. No runner, schema, horizon, or content package edits in this iteration. No git writes.

**Prior-art boundary (supersede, do not inherit).** The inert `taxable-interest-composition-spike.md` and inert ADR-0021 may be read as prior art the conforming ADR (candidate 0026) will supersede. This design does **not** inherit their asserted `{box1, box3, non-form}` membership by repetition, nor their bare `sum(...)` as the coextensiveness mechanism. Membership is re-justified against the line-2b definition; coextensiveness is a validator-rejectable declaration that defeats narrow substitution (case 5), which the spike does not.

**Stop conditions.** Stop at `it1/design.md` and `examination-it1.md`. If a needed contract change cannot be represented as a versioned schema/canon diff on paper, report rather than improvise. Unresolved authority questions are listed explicitly, not closed by fiat.

---

## 1. Authority inventory (what is already decided)

| Source | Binding consequence for this topic |
|---|---|
| ADR-0016 dec. 1–2 | Family meaning = exact `closure_claim` + `member_predicate`; ids/labels/symbols cannot broaden. |
| ADR-0016 dec. 3 | Coverage presents the exact claim; a rollup cannot silently report a broader universe complete. |
| ADR-0016 dec. 4 | Broader final may consume a subtotal only when universes are identical **or** an explicit composition is established as coextensive. |
| ADR-0016 dec. 5 | Box-1 closure authorizes only the box-1 subtotal (incl. zero); never line-2b zero or “all taxable interest complete.” |
| ADR-0016 Not Decided | Full taxable-interest taxonomy left open — this topic’s primary gap. |
| ADR-0014 | Empty collect zero only via adopted mapping + current literal-true closure; pins mapping + declaration + closure finding. |
| ADR-0017 | Membership-horizon succession is an individuation root; displaces horizon-keyed closure; derivation edges then displace closure-backed results. No third edge. |
| ADR-0010 | Derivation edges from `input`/`choice` pins only; derived findings are targets never roots; no new standing-affecting edge. |
| ADR-0015 | 1099-INT facts keyed by statement instance, not evidence. |
| ADR-0012 | Line 2b is a form-field citizen binding a symbol; five dispositions; renderer invents nothing. |
| Committed B1 content | `tax.us.2025.f1099int.b1` + mapping + `rule.f1099int-b1-subtotal` publishing `tax.us.2025.interest.b1-subtotal` only. |
| `audit_collect_authority` | A rule that **collects** over a mapped family must publish exactly that family’s `authorizes_subtotal` — blocks collect→line-2b, but **does not** block `ref(b1-subtotal)`→line-2b. That residual is the narrow-substitution hole this design closes. |

---

## 2. TIC-P1 — Coextensive line-2b universe and declaration mechanism

### 2.1 Line-2b definition (justification, not assertion)

Form 1040 partitions interest into two printed lines:

- **Line 2a — Tax-exempt interest.** Amounts that are interest for tax-administration purposes but excluded from taxable income (prominently Form 1099-INT **box 8**, and related tax-exempt interest reported to the taxpayer). These are **out** of line 2b by the form’s own partition.
- **Line 2b — Taxable interest.** The taxpayer’s **taxable** interest income for the year — the amount that rolls into total income (line 9) and downstream taxable income.

Against that definition, what must be able to contribute to line 2b is every amount that is (i) interest and (ii) taxable, not merely every amount that appears in one 1099-INT box.

**In (taxable interest contributors):**

| Constituent | Why it is in line 2b | Why it is its own family |
|---|---|---|
| **B1** — Form 1099-INT box 1 interest income | Box 1 is ordinary interest income; taxable and reportable as taxable interest. | Distinct box/predicate; committed declaration already excludes other boxes and non-form amounts (family `tax.us.2025.f1099int.b1`). |
| **B3** — Form 1099-INT box 3 interest on U.S. Savings Bonds and Treasury obligations | Federal taxable interest (even when state-exempt). The 1040 interest partition places taxable Treasury/savings-bond interest in the taxable-interest line, not line 2a. | Different box and fact type from box 1. ADR-0016 and SFS analysis use box 3 as a concrete counterexample to “B1 = taxable interest.” Document-level “all 1099-INT” was rejected. |
| **NF** — Non-form taxable interest | Taxable interest that is not a member of B1 or B3 predicates (e.g. interest below information-return thresholds, informal loans, payer never issued 1099-INT). Still taxable interest under the line-2b definition. | Not a 1099-INT statement item; cannot be closed by B1/B3 horizons. ADR-0016 rejects B1 as coextensive precisely because of non-form interest. |

**Out (not line 2b):**

| Amount | Destination | Why out |
|---|---|---|
| Form 1099-INT **box 8** tax-exempt interest | Line **2a** | Form partition: tax-exempt ≠ taxable. Including it would misstate line 2b. |
| Other non-interest 1099-INT boxes (e.g. penalties, federal tax withheld) | Not line 2b interest | Not interest income for the line-2b question. |

**Coextensive universe (this composition version).** Let Pred(F) be family F’s canonical member predicate (fact type + scope). The required universe for the line-2b composition is the **union of the constituent predicates**:

U_2b^v1 = Pred(B1) ∪ Pred(B3) ∪ Pred(NF)

with pairwise fact-type disjointness so no amount is double-counted under two families. Coextensiveness means: **every amount the composition claims to cover is in exactly one constituent predicate, and the composition’s exact claim is the coverage authority for “taxable interest under this composition”** — not a label, not a single subtotal, and not silent promotion of B1.

This is the same three-way partition the inert spike named, but membership is re-derived from the line-2b definition and from ADR-0016’s already-ratified counterexamples (box 3; non-form), not copied from the spike. The **mechanism** that makes the set coextensive is §2.3, not the `sum` operator.

### 2.2 Unresolved authority questions (not resolved by fiat)

These do **not** block designing the declaration mechanism or the six Gate-2 cases, but they must not be silently absorbed:

1. **Form 1099-OID and other information returns.** Original issue discount and similar amounts can be taxable interest for line 2b. Source-completeness non-goals deferred OID. **Question:** must OID (and peer forms) be additional constituents before a composition may claim legal coextensiveness with Form 1040 line 2b, or is U_2b^v1 an intentional versioned content surface that grows by composition version? **This design treats U_2b^v1 as a versioned content surface:** adding OID requires a new composition version and validator re-check, not a silent label change. The exact claim must not say “every conceivable taxable interest in the Code” if constituents omit OID.
2. **Pass-through / K-1 interest, seller-financed mortgage interest, foreign-source interest without 1099-INT.** Same class as (1): either enter NF’s predicate by content authoring, or become new constituents in a later composition version. Predicate text for NF must be authored so it does not falsely claim those shapes if they are excluded.
3. **Series EE/I education exclusion and other adjustments.** Whether gross taxable interest is composed first and reduced by a later rule, or adjusted inside a constituent — **not decided here** (Gate 5 defers subtotal arithmetic wording). Composition concerns source-family coextensiveness, not every downstream adjustment.
4. **Schedule B threshold / presentation.** Out of scope (milestone non-goal). Line 2b rollup does not require Schedule B content.
5. **Exact production schema ids/bytes.** Deferred (ADR-0016 Not Decided; Gate 5). Paper ids below are design placeholders.
6. **Composition pin role.** Whether the line-2b finding must carry a dedicated pin role `composition` or package membership alone pins the declaration — see §2.3.3 note.

### 2.3 Coextensiveness declaration (checkable claim)

ADR-0016 decision 4 requires an **explicit composition established as coextensive**. A bare rule `sum(refs…)` is arithmetic only; without a pinned declaration, a second rule can publish the line-2b symbol from a **subset** of subtotals (`ref` of B1 only). Existing `audit_collect_authority` catches collect→broad-symbol, **not** ref-subset→broad-symbol. That is the spike’s gap and case 5’s attack.

#### 2.3.1 New citizen (paper schema) — `coextensive-composition.v1`

```json
{
  "schema": "coextensive-composition.v1",
  "id": "tax.us.2025.composition.taxable-interest.line-2b",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax"
  },
  "required_universe": {
    "form": { "authority": "IRS", "form_id": "1040", "tax_year": 2025, "line": "2b" },
    "claim": "Taxable interest for this taxpayer and tax year 2025 under the constituent source families of this composition: every amount that is a member of exactly one constituent member predicate is accounted for when every constituent family is closed on its current horizon. This claim is the composition's exact coverage claim for Form 1040 line 2b under version v1. It excludes tax-exempt interest (Form 1040 line 2a / Form 1099-INT box 8). It does not assert completeness of source families outside the constituent list."
  },
  "constituents": [
    {
      "family": { "id": "tax.us.2025.f1099int.b1", "version": "v1" },
      "authorizes_subtotal": "tax.us.2025.interest.b1-subtotal"
    },
    {
      "family": { "id": "tax.us.2025.f1099int.b3", "version": "v1" },
      "authorizes_subtotal": "tax.us.2025.interest.b3-subtotal"
    },
    {
      "family": { "id": "tax.us.2025.interest.non-form", "version": "v1" },
      "authorizes_subtotal": "tax.us.2025.interest.non-form-subtotal"
    }
  ],
  "publishes": "tax.us.2025.interest.line-2b",
  "coextensiveness": {
    "kind": "partition-union",
    "statement": "required_universe equals the disjoint union of the pinned constituents' member predicates; each constituent subtotal carries only its family declaration (ADR-0016 dec. 4)."
  }
}
```

**Schema requirements (paper):** `schema`, `id`, `version`, `scope`, `required_universe.claim` (minLength ≥ 1), `required_universe.form`, non-empty `constituents[]` with unique `family.id` and unique `authorizes_subtotal`, `publishes`, `coextensiveness.kind` enum including `partition-union`. `additionalProperties: false`.

#### 2.3.2 Paper content: B3 and NF families (parallel to committed B1)

Only B1 is committed. B3 and NF are **paper** declarations for the composition surface (Track 2 implements later):

```json
{
  "schema": "source-family.v1",
  "id": "tax.us.2025.f1099int.b3",
  "version": "v1",
  "title": "Form 1099-INT box 3 statement items, tax year 2025",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "closure_claim": "Every interest amount reported in box 3 of a Form 1099-INT furnished to the taxpayer for tax year 2025 is recorded as a statement item. This claim covers Form 1099-INT box 3 only: it says nothing about box 1, box 8, non-form interest, or total taxable interest without the line-2b composition.",
  "member_predicate": { "fact_type": "tax.us.2025.f1099int.box3-interest" },
  "authorizes_subtotal": "tax.us.2025.interest.b3-subtotal"
}
```

```json
{
  "schema": "source-family.v1",
  "id": "tax.us.2025.interest.non-form",
  "version": "v1",
  "title": "Non-form taxable interest, tax year 2025",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "closure_claim": "Every taxable interest amount for tax year 2025 that is not a member of the Form 1099-INT box-1 or box-3 statement-item predicates is recorded. This claim covers the residual non-form taxable-interest family only; it is not tax-exempt interest and is not alone Form 1040 line 2b.",
  "member_predicate": { "fact_type": "tax.us.2025.interest.non-form" },
  "authorizes_subtotal": "tax.us.2025.interest.non-form-subtotal"
}
```

Each gets a `source-closure-mapping.v1` and a subtotal rule shaped like committed `rule.f1099int-b1-subtotal` (collect over own `source_set`, publish own `authorizes_subtotal` only). Horizon genesis/transition machinery is unchanged (ADR-0017).

#### 2.3.3 Validator: `audit_composition_authority` (paper contract delta on `source_authority.py`)

Load-time / package-validation checks (structural; no runner tax meaning):

| Check | Rejects |
|---|---|
| V1 | Composition constituent `family` pin missing from adopted declarations, or `authorizes_subtotal` ≠ declaration’s. |
| V2 | Duplicate family id or duplicate subtotal symbol among constituents. |
| V3 | Two compositions in one package claim the same `publishes` symbol without declared conflict semantics (ADR-0006 unique ownership). |
| V4 | A rule with `publishes == composition.publishes` is not bound to that composition (package membership pairing). |
| V5 | That rule’s `value`/`when` expression tree does not `ref` **every** constituent `authorizes_subtotal` (missing constituent → reject). **This defeats case 5.** |
| V6 | That rule `collect`s over any mapped family (reinforces `audit_collect_authority`; narrow family must not stand behind line 2b). |
| V7 | That rule `ref`s a subtotal symbol that is not in the composition’s constituent list (extra predicate → reject). |
| V8 | Coverage/composition rollup status is CLOSED only if **every** constituent family’s admission is CLOSED; rollup text is `required_universe.claim` verbatim or an explicit reference to the composition id/version — never B1’s claim alone (ADR-0016 dec. 3). |

**Note on pinning the composition.** Derived-finding pin roles today are closed (`parameter`, rule roles, `input`, `choice`, `adoption`, `governance`, `engine`, `package`, `operation-semantics`). Prefer **package-level binding**: composition is a package member; the line-2b rule is a package member; validation binds them by shared package + `publishes` match. Extending pin roles with `composition` is optional production polish (unresolved minor; either satisfies “checkable declaration” if V4–V7 run at package validation and runs pin package/adoption). Paper chooses package-level binding + V4–V7; the line-2b finding pins constituent subtotals as `input` via `ref`, and pins the rule + adoption as today.

#### 2.3.4 Line-2b rule (paper)

```json
{
  "schema": "rule-artifact.v1",
  "id": "tax.us.2025.rule.interest.line-2b",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax",
    "effective_from": "2025-01-01"
  },
  "role": "computation",
  "requires": [
    "rounding.convention",
    "tax.us.2025.interest.b1-subtotal",
    "tax.us.2025.interest.b3-subtotal",
    "tax.us.2025.interest.non-form-subtotal"
  ],
  "when": true,
  "value": {
    "op": "round",
    "value": {
      "op": "add",
      "args": [
        { "op": "ref", "name": "tax.us.2025.interest.b1-subtotal" },
        { "op": "ref", "name": "tax.us.2025.interest.b3-subtotal" },
        { "op": "ref", "name": "tax.us.2025.interest.non-form-subtotal" }
      ]
    },
    "mode": { "op": "ref", "name": "rounding.convention" },
    "stage": "after_aggregate"
  },
  "publishes": "tax.us.2025.interest.line-2b",
  "blocked": {
    "code": "OPEN_DEPENDENCY",
    "missing": [
      "rounding.convention",
      "tax.us.2025.interest.b1-subtotal",
      "tax.us.2025.interest.b3-subtotal",
      "tax.us.2025.interest.non-form-subtotal"
    ]
  },
  "notes": "Publishes Form 1040 line 2b taxable interest only under coextensive-composition tax.us.2025.composition.taxable-interest.line-2b v1. Each ref'd subtotal carries its own family declaration; this rule does not collect any source family and cannot fire until every constituent subtotal is published (including closure-backed zeros)."
}
```

**Why this is not implicit subtotal promotion:** promotion would let B1’s closure or B1’s subtotal alone authorize line 2b. Here (a) package validation requires the composition’s full constituent set in the expression, (b) eligibility requires all three symbols present, (c) each empty zero still needs its own ADR-0014 admission, (d) coverage CLOSED for the composition requires all three admissions.

#### 2.3.5 Form field (paper, ADR-0012)

Citizen `tax.us.2025.form1040.line-2b` binds symbol `tax.us.2025.interest.line-2b`, locator line `2b`, label taxable interest. Dispositions reuse the five-class vocabulary; `closure_backed_zero` explanation walks pins through all three subtotals and their closure findings when the published zero’s lineage includes those closure inputs.

---

## 3. TIC-P2 — Honest coextensive zero and late-member lifecycle

### 3.1 Honest coextensive zero

A line-2b **numeric zero** publishes only when:

1. The line-2b rule is package-valid under the composition (V4–V7);
2. Every constituent subtotal rule has published (eligibility);
3. For each constituent that is empty, publication was via current literal-true closure on the **current** horizon (ADR-0014 + ADR-0017) — never via absent closure.

Therefore: **box-1 closure alone cannot produce line 2b = 0** (decision 5). B1 may publish `b1-subtotal = 0` while B3/NF subtotals remain blocked → line 2b ineligible/blocked.

Disposition: when all three subtotals are closure-backed zeros, line 2b is a **coextensive closure-backed zero** (lineage includes three closure findings). When any subtotal is a present-source aggregate, lineage follows those pins; the form field’s disposition is selected from the line-2b finding’s actual pins (ADR-0012: renderer invents nothing). Paper does not invent a sixth disposition.

### 3.2 Late-member lifecycle (existing edges only)

No new standing-affecting edge. Mechanism is exactly ADR-0017 + ADR-0010:

1. **Member-transition** (atomic) advances family horizon (individuation root).
2. Closure facts keyed on the predecessor horizon are displaced (individuation).
3. Subtotal derived findings that pinned the displaced closure finding as `input` are displaced (derivation).
4. Line-2b derived finding that pinned that subtotal as `input` is displaced (derivation).
5. New true closure on the successor horizon + **explicit rerun** may publish successors (ADR-0017 dec. 7).

Same-member value correction does **not** advance the horizon (ADR-0017 dec. 4); only the member finding → present subtotal derivation edge fires.

### 3.3 Case 6 mandatory named trace

Synthetic identifiers throughout. Scope for all families: `{ "tax-year": "2025", "subject": "taxpayer-primary" }`.

#### Phase A — Coextensive empty zero

| Step | Act / run | Recorded citizens (ids) |
|---|---|---|
| A1 | `horizon-genesis` ×3 | `H_B1_0`, `H_B3_0`, `H_NF_0` (predecessors null) |
| A2 | Assertion of closure findings (true) keyed on those horizons | `CF_B1` on `H_B1_0`; `CF_B3` on `H_B3_0`; `CF_NF` on `H_NF_0` |
| A3 | Explicit derivation run R_A | — |

**Publications of R_A:**

| Derived finding | Symbol | Value | Material pins (role → id) |
|---|---|---|---|
| `DF_B1_0` | `…b1-subtotal` | `0` | `computation`→B1 rule; `package`→B1 mapping+declaration; `input`→`CF_B1`; adoption; governance; round semantics |
| `DF_B3_0` | `…b3-subtotal` | `0` | same pattern on B3 |
| `DF_NF_0` | `…non-form-subtotal` | `0` | same pattern on NF |
| `DF_2b_0` | `…line-2b` | `0` | `computation`→line-2b rule; `input`→`DF_B1_0`, `DF_B3_0`, `DF_NF_0`; adoption; governance; round |

Composition coverage: all three families CLOSED; rollup claim = composition `required_universe.claim`.

#### Phase B — Late 1099-INT box-1 arrival

| Step | Act | Effect |
|---|---|---|
| B1 | `member-transition` on family B1: `member.action=assert` finding `MF_B1_BankA` value `120` (fact type box1-interest, statement instance Bank A); `successor.id=H_B1_1`, `predecessor=H_B1_0` | Horizon chain: `H_B1_0` superseded, `H_B1_1` current. |

**Edges (no new kind):**

| Edge kind | From | To | Why |
|---|---|---|---|
| Individuation | `H_B1_0` superseded | Closure fact/finding `CF_B1` | Closure keyed on predecessor horizon (ADR-0017 dec. 5) |
| Derivation | `CF_B1` displaced | `DF_B1_0` | `DF_B1_0` pinned `CF_B1` as `input` |
| Derivation | `DF_B1_0` displaced | `DF_2b_0` | `DF_2b_0` pinned `DF_B1_0` as `input` |

**Non-effects:** `CF_B3`, `CF_NF`, `DF_B3_0`, `DF_NF_0` remain current (different families/horizons). No manual closure withdrawal. No member→line-2b edge. No stored stale flag.

**Current state after B1 (before re-attest/rerun):** `DF_2b_0` noncurrent; B1 family OPEN on `H_B1_1`; line 2b blocked/absent; coverage must **not** report composition complete (B1 open).

#### Phase C — Re-attestation and republish

| Step | Act / run | Result |
|---|---|---|
| C1 | Assert `CF_B1_1` true on `H_B1_1` | B1 admitted again |
| C2 | Explicit rerun R_C | — |

**Publications of R_C:**

| Derived finding | Symbol | Value | Notes |
|---|---|---|---|
| `DF_B1_1` | `…b1-subtotal` | `120` | Present-source path; pins `MF_B1_BankA` as `input`; does **not** pin closure (ADR-0014 dec. 5) |
| `DF_B3_0` | (still current) | `0` | Unchanged if still current |
| `DF_NF_0` | (still current) | `0` | Unchanged |
| `DF_2b_1` | `…line-2b` | `120` | Pins `DF_B1_1`, `DF_B3_0`, `DF_NF_0` as `input` |

Old `DF_2b_0` remains in history, noncurrent; supersession roots accumulate — removal cannot resurrect it (ADR-0017 dec. 6).

---

## 4. Gate-2 cases (claim → schema/contract → runner/horizon → finding/pin map)

Convention: two positives and two negatives are embedded across cases 1–5; case 6 is the lifecycle. All amounts synthetic.

### Case 1 — Empty filer, coextensive zero

**Claim.** Line 2b publishes `$0` only as coextensive zero under the composition, not as a promoted B1 zero.

**Schema/contract.** Composition v1 + three families/mappings/subtotal rules + line-2b rule; V5 requires all three refs.

**Runner/horizon.** Genesis horizons; three true closures; collect empty→0 on each admitted family; line-2b `add` of three refs.

**Findings/pins.** As Phase A: `DF_2b_0=0` pins three zero subtotals; each zero subtotal pins its own `CF_*`.

**Positives:** (P1a) all three closed empty → `line-2b=0` published; (P1b) same with explicit composition coverage CLOSED and exact claim text.  
**Negatives:** (N1a) only B1+B3 closed, NF unclosed → line 2b blocked; (N1b) all closed but composition missing from package → load reject (V4).

### Case 2 — Box-1 only (others closed empty)

**Claim.** Present B1 + closed-empty B3/NF → line 2b equals B1 sum, published.

**Contract.** Unchanged composition; present-source B1 does not consult closure; empty B3/NF still need closure.

**Runner.** B1 collect non-empty → sum; B3/NF closure zeros; line 2b adds.

**Findings.** `DF_B1` pins member findings; `DF_B3`/`DF_NF` pin closures; `DF_2b` pins all three subtotals.

**Positives:** (P2a) one B1=$120 → line 2b=$120; (P2b) two B1 statements same payer different instances → sum both (ADR-0015).  
**Negatives:** (N2a) B1 present, B3 unclosed → block; (N2b) B1 present, NF unclosed → block.

### Case 3 — Multi-source

**Claim.** B1 + NF present, all constituents closed → full sum.

**Contract.** Same.

**Runner.** Two present subtotals + B3 closed zero (or B3 present as well).

**Findings.** `DF_2b` pins all constituent subtotals; composition coverage CLOSED.

**Positives:** (P3a) B1=$120, NF=$50, B3 closed empty → $170; (P3b) B1+B3+NF all present → full three-way sum.  
**Negatives:** (N3a) omit NF from composition declaration while rule still refs it → V1/V5 inconsistency reject; (N3b) rule refs only B1+NF while composition lists three → V5 reject.

### Case 4 — Negative: one constituent unclosed

**Claim.** Any single unclosed constituent → line 2b blocked; coverage must not report taxable-interest composition complete (ADR-0016 dec. 3).

**Contract.** V8 rollup; eligibility on three symbols.

**Runner.** Unclosed empty family → subtotal `EvalBlocked(BLOCK_CLOSURE)`; symbol absent; line-2b not eligible.

**Findings.** No current `DF_2b`; FamilyCoverage for open family `status=open`; composition rollup open.

**Instances:** (N4a) B3 unclosed only; (N4b) NF unclosed only. Present-source B1 may still publish its subtotal without closure under committed collect semantics; composition still requires B3/NF closed for line 2b and for composition coverage CLOSED.

### Case 5 — Negative: narrow substitution (mandatory)

**Claim.** Attempt to publish line 2b from box-1 closure/subtotal alone must reject/block (ADR-0016 dec. 5).

**Attack vectors and defeats:**

| Attack | Defeat |
|---|---|
| Rule collects B1 family, publishes `…line-2b` | Existing `audit_collect_authority` |
| Rule refs only `…b1-subtotal`, publishes `…line-2b` | **V5** (missing B3/NF refs) — spike does not have this |
| Mapping admits `…line-2b` for B1 family | `validate_mapping_against_family` (admits_symbol ≠ authorizes_subtotal) |
| Coverage treats B1 CLOSED as composition complete | **V8** exact composition claim / all-constituent CLOSED |
| Package omits B3/NF families but ships line-2b rule | V1 / package closure |

**Instances:** (N5a) load-time reject of narrow rule; (N5b) runtime: only B1 closed empty, B3/NF unclosed → no line-2b publication under adopted package.

### Case 6 — Lifecycle (mandatory) — see §3.3

Claim → contract (no horizon machine change) → runner (explicit rerun) → full finding/pin/edge map in §3.3. Old coextensive zero leaves current state through individuation then derivation only.

---

## 5. Claim → contract change summary (paper diffs only)

| Artifact | Change |
|---|---|
| `packages/schemas/derivation/coextensive-composition.v1.schema.json` | **New** schema (paper). |
| `packages/derivation/source_authority.py` | **Paper delta:** `audit_composition_authority` (V1–V7); keep `audit_collect_authority`. |
| `packages/derivation/package_validation.py` | **Paper delta:** invoke composition audit; composition as package member role (exact role name TBD with package schema — unresolved minor). |
| `packages/tax/coverage.py` | **Paper delta:** composition rollup over constituent `FamilyCoverage` (V8); no second store. |
| `packages/content/tax/2025/` | **Paper:** B3/NF families, mappings, subtotal rules, composition citizen, line-2b rule, form-field; extend interest-slice package members. |
| Horizon/currency/ADR-0017 | **No change.** |
| Act kinds / third edge | **No change.** |

---

## 6. What this design refuses

- Inheriting spike/ADR-0021 bare `sum` as coextensiveness.
- Treating B1 closure as line-2b authority.
- A new standing-affecting edge for late members.
- Silent “all taxable interest complete” coverage from any proper subset of constituents.
- Fiat closure of OID/K-1/adjustment taxonomy (§2.2).

## 7. Proposition status at static level

- **TIC-P1:** Settled at static/paper level for the declaration mechanism and for the justified U_2b^v1 partition {B1, B3, NF}, subject to open taxonomy questions in §2.2 (versioned surface, not hidden completeness).
- **TIC-P2:** Settled at static/paper level: honest zero requires all constituents; late-member trace uses only existing individuation and derivation edges under committed ADR-0017/0010 machinery.
