# Legibility audit — interest-closure

**Date:** 2026-07-28  
**Scope:** `interest-closure`  
**Scenario:** `packages/sample_data/tax/scenarios/closure_backed_zero_1099int`  
**Auditor posture:** Context-starved. No prior project knowledge. Only Ontology, Constitution, `packages/schemas/**`, `packages/content/**`, `packages/sample_data/**` (scenario-focused), and `README.md` were used. Forbidden paths (ADRs, Commentary, Principles, reviews, proposals, memory, commit messages, other legibility audits, etc.) were not opened. No accidental open of answer-key paths.

**Accident note:** Workspace at session start was empty; allowed trees were copied from a sibling checkout of the same project for reading. Only allowed paths were copied and read.

---

## 1. Meaning recovery

### Files read
- `docs/governance/ontology.md` (§0–§2; register)
- `docs/governance/constitution.md` (Articles 9–12, 15 for schema/legibility framing)
- `packages/content/tax/2025/f1099int.bundle.json`
- `packages/schemas/kernel/fact-type.v2.schema.json`
- `packages/content/tax/2025/quantity.taxable-interest.json`
- `packages/schemas/kernel/quantity-vocabulary.v1.schema.json`
- `README.md` (project framing only)

### Recovery attempt

**Citizen chosen:** content fact type `tax.us.2025.f1099int.box1-interest` (schema `fact-type.v2`), from `packages/content/tax/2025/f1099int.bundle.json`.

**Real-world thing it represents (from the artifact + Ontology):**

- Ontology §2: a *fact type* is a declared kind of question the workspace can address; a *finding* is a determination of a particular fact of that type; identity keys distinguish one question-instance from another; nature and value shape are declared on the type.
- The fact type’s own `title` states the question: interest income reported in **box 1** of **one logical Form 1099-INT statement instance** furnished by a payer for tax year **2025**. Identity is keyed on payer entity (`tax.us.interest-payer`), statement entity (`tax.us.1099int-statement`), and tax-year literal `2025`. The title explicitly says statement identity is peer to evidence and carries no file/upload/scan/document key; multiple originals from one payer are distinct statements; a corrected copy of the same logical return answers the same fact and supersedes.

**What a valid instance (finding) asserts:**

- A **determinable** answer (`nature: "determinable"`) whose value is a **number** (`value_schema: {"type": "number"}`): the box-1 interest amount for that payer–statement–2025 fact.
- Supersession is free (`supersession.policy: free`).
- It is marked `source_amount: true` and pins quantity vocabulary entry `tax.us.2025.quantity.taxable-interest` / token `taxable-interest` — i.e. the system classifies this amount as a residual-closed source amount of the taxable-interest quantity kind, without further denotation of that token in the vocabulary artifact.

### Score

**recovered**

The fact-type title plus Ontology §2 is enough to state the real-world question and what a finding asserts. Residual gap on what “taxable-interest” *means* as a quantity token is not required to recover this citizen’s primary meaning; it is noted under honest boundaries.

---

## 2. Number provenance

### Files read
- `packages/sample_data/tax/scenarios/closure_backed_zero_1099int/scenario.json`
- `packages/sample_data/tax/scenarios/closure_backed_zero_1099int/expected/report.json`
- `packages/sample_data/tax/scenarios/closure_backed_zero_1099int/expected/report.txt`
- `packages/content/tax/2025/rule.f1099int-b1-subtotal.json`
- `packages/content/tax/2025/family.f1099int-b1.json`
- `packages/content/tax/2025/closure-mapping.f1099int-b1.json`
- `packages/content/tax/2025/package.interest-slice.json`
- `packages/schemas/derivation/source-family.v1.schema.json`
- `packages/schemas/derivation/source-closure-mapping.v1.schema.json`
- `packages/schemas/derivation/source-closure-mapping.v2.schema.json`
- `packages/schemas/derivation/rule-artifact.v2.schema.json`
- `packages/schemas/derivation/operation-semantics.v1.schema.json`
- `packages/schemas/derivation/operation-semantics.v2.schema.json`
- `README.md` (derive/explanation contract: walk of pins, not re-evaluation)

### Recovery attempt

**The number:** published derived finding  
`tax.us.2025.interest.b1-subtotal = 0`  
(`finding:derived:d42720a0eafd9096f5c8979c`), run `tax.us.2025.run.closure-backed-zero-1099int`, stop reason `saturated`.

**What the number is (from family + rule + README):**  
The authorized **Form 1099-INT box-1 source subtotal** for the adopted family `tax.us.2025.f1099int.b1` — sum of current `tax.us.2025.f1099int.box1-interest` members, rounded — **not** Form 1040 line 2b / total taxable interest. Family `closure_claim` and rule `notes` both fence that meaning.

**Trace from explanation pins (`report.txt` / `report.json`):**

| Pin kind | Id / symbol | Role in this zero |
|---|---|---|
| computation (producer) | `tax.us.2025.rule.f1099int-b1-subtotal` v1 | Publishes the symbol |
| adoption | `tax.us.2025.package.interest-slice` v1 | Adopted machinery |
| governance | `governance.constitution` v1 | Governance pin |
| input | `tax.us.2025.f1099int.b1.source-closure` = **true** (`demo-finding-b1-closure-h0`) | Closure admission evidence |
| input | `rounding.convention` = `half_up` | Round mode |
| operation-semantics | `round` | Rounding op |
| package | `tax.us.2025.closure-mapping.f1099int-b1` | Admission mapping |
| package | `tax.us.2025.f1099int.b1` | Source-family declaration |

**Inputs / rule / parameters from scenario + content rule:**

- `sources: []` — no box-1 interest findings.
- Rule expression (scenario / content):  
  `round( add( collect(name=tax.us.2025.f1099int.box1-interest, source_set=tax.us.2025.f1099int.b1) ), mode=ref(rounding.convention) )`  
  with `requires: ["rounding.convention"]` only (no other parameters).
- Mapping: admits `tax.us.2025.interest.b1-subtotal` when closure finding is `current-literal-true` on fact type `tax.us.2025.f1099int.b1.source-closure`, horizon key `family-horizon`, family horizon current id `b1.h0`.
- Rule notes: empty family publishes zero **only** through a current literal-true closure finding admitted by the adopted mapping; otherwise blocks.

**Partial reconstruction of the arithmetic path:**  
No member amounts appear in the explanation tree (consistent with empty sources). Closure is true. The published value is `0`. Inferring that the empty `collect`/`add` evaluates to zero **and** that closure is what makes empty aggregation publish rather than block requires the rule **notes** and sibling scenarios, not a machine-declared empty-fold axiom in the explanation tree or a versioned `add`/`collect` operation-semantics citizen.

Gaps that block full confidence:
1. Explanation lists `operation-semantics` / `round` with `finding_id: "round"` but pins **no versioned round canon instance** (modes, unit, stage, tie-break). Schema `operation-semantics.v1` defines that shape; no such content citizen is pinned in the scenario explanation.
2. Rule expression does **not** contain `require_closed`; empty-vs-block behavior lives in engine notes / mapping admission, not in the published expression tree the explanation claims to walk.
3. Scenario embeds `rule-artifact.v1` with `stage: "after_aggregate"`; content rule is `rule-artifact.v2` without `stage`. Explanation does not surface stage.
4. Notes cite ADR-0014 / ADR-0016 — not readable under audit constraints; residual meaning of those citations is opaque.

### Score

**partial**

Recovered: which symbol, which rule, which pins, that there were no statement amounts, and that a true source-closure finding is on the path.  
Blocked: fully justifying from pins alone that empty aggregation is *defined as* zero and is *licensed only* by that closure condition, without leaning on free-text notes or implied engine behavior.

### Maintainer fix (for the unrecovered part)
- **Artifact:** explanation output for empty closed families (`expected/report.json` / engine explanation builder).  
  **Missing:** an explicit child for the empty collect (e.g. zero member inputs or `collect_cardinality: 0`), and a pin to a versioned **round** (and ideally **add**/**collect**) operation-semantics citizen that states empty-aggregate → 0.
- **Artifact:** `packages/content/tax/2025/rule.f1099int-b1-subtotal.json`.  
  **Missing / misleading:** empty-family publish/block policy is only in `notes` (with ADR pointers), not in the `value` expression (e.g. no `require_closed` or declared empty-set clause). Encode the admission dependency in the rule expression or a pinned, versioned semantics citizen so the explanation walk can cite it without ADR prose.

---

## 3. Distinction recovery

### Files read
- `packages/sample_data/tax/scenarios/closure_backed_zero_1099int/scenario.json`
- `packages/sample_data/tax/scenarios/closure_backed_zero_1099int/expected/report.txt`
- `packages/sample_data/tax/scenarios/closure_backed_zero_1099int/expected/report.json`
- `packages/sample_data/tax/scenarios/present_zero_1099int/scenario.json`
- `packages/sample_data/tax/scenarios/present_zero_1099int/expected/report.txt`
- `packages/sample_data/tax/scenarios/present_zero_1099int/expected/report.json`
- `packages/sample_data/tax/scenarios/open_empty_1099int/scenario.json`
- `packages/sample_data/tax/scenarios/open_empty_1099int/expected/report.txt`
- `packages/sample_data/tax/scenarios/open_empty_1099int/expected/report.json`
- `packages/content/tax/2025/form1040.line-2b.form-field.json`
- `packages/schemas/tax/form-field.v2.schema.json`
- `packages/content/tax/2025/f1099int.bundle.json` (closure vs member fact types)

### Recovery attempt

**Pair A — two zeros that look the same at publication surface**

| | `closure_backed_zero_1099int` | `present_zero_1099int` |
|---|---|---|
| Published | `tax.us.2025.interest.b1-subtotal = 0` | same symbol = 0 |
| Sources | `sources: []` | one finding `tax.us.2025.f1099int.box1-interest = "0"` |
| Closure block | present; finding `source-closure = true` on horizon `b1.h0` | no `closure` section |
| Explanation inputs | **source-closure = True**, rounding, round, mapping package, family package | **box1-interest = 0**, rounding, round |
| Mapping / family pins in explanation | yes | no |

**How they differ and why (artifacts alone):**

1. **Closure-backed zero:** no statement items are recorded; the user-attested closure fact (`tax.us.2025.f1099int.b1.source-closure`, title: every furnished 1099-INT box-1 statement item is recorded as of the family-horizon) is literal true; mapping admission is `current-literal-true`; empty family is allowed to publish the subtotal as 0. Explanation proves the zero rests on **closure authority**, not on summing amounts.
2. **Present (computed) zero:** a real member finding exists with value 0; the subtotal is the aggregate of that present amount. Explanation proves the zero rests on a **zero statement amount**, not on empty-family closure.

Same rendered number; different facts, different derivation edges, different legal-epistemic claims (“I have all statements and they sum to nothing recorded” vs “I have a statement that reports zero”).

**Pair B — empty family with vs without closure (confirms the distinction is load-bearing)**

`open_empty_1099int` also has empty sources and the same rule/mapping family declarations, but **`closure.findings: []`**. Result: **nothing published**; blocked `SOURCE_SET_UNCLOSED` missing `tax.us.2025.f1099int.b1`. So emptiness alone is not a zero — closure is the fork.

**Presentation vocabulary (adjacent, not used by this scenario’s published symbol):**  
`form1040.line-2b` dispositions separately name `computed_zero` vs `closure_backed_zero`, matching the distinction above at Form 1040 line 2b level — evidence the system treats the pair as first-class presentation categories even though this scenario only exercises the B1 subtotal.

### Score

**recovered**

The three scenarios’ inputs and explanation trees are sufficient without external knowledge.

---

## 4. Honest-boundary recovery

### Files read
- All files listed in tasks 1–3
- `docs/governance/ontology.md` (full register scan for source-family / horizon / closure terms)
- `packages/content/tax/2025/interest-composition.json`
- `packages/sample_data/core_tax_conditions/examples/operation-semantics.v2.json`
- `packages/sample_data/core_tax_conditions/examples/source-closure-mapping.v2.json`

### Recovery attempt — what these artifacts do **not** let you determine

1. **Ontology coverage gap for this scenario’s core nouns.**  
   Ontology register defines fact type, finding, rule artifact, adoption, pinning, etc., but has **no entries** for source family, source-closure mapping, family horizon, or “closure claim.” Those meanings are carried by schema `description` strings and content `title`/`closure_claim` prose that repeatedly cite **ADR-0014 / ADR-0016 / ADR-0017** — which are out of scope for this audit and not present in Ontology/Constitution. A reader can approximate from prose, but cannot resolve the terms as Ontology citizens.

2. **Imported IRS / form knowledge.**  
   That “Form 1099-INT box 1” is interest paid by a payer on an information return, how it relates to Schedule B, or why box 1 ≠ line 2b, is assumed English/tax literacy plus the family `closure_claim` fence. There is no citation citizen attached to the B1 subtotal rule itself (unlike form-field line 2b, which pins a citation).

3. **Quantity denotation.**  
   `quantity.taxable-interest` only lists enum tokens `["taxable-interest", "wages"]`. No unit, currency, residual definition, or coextensiveness with the composition universe beyond other content files. What “taxable-interest” *is* as a quantity is a label, not a recorded definition.

4. **Operation evaluation without pinned canon instances.**  
   - `round` is referenced in explanations without a versioned round semantics *instance* (unit, stages, tie-break).  
   - `add` / `collect` have no operation-semantics citizens in the allowed trees.  
   - Empty-set aggregation → 0 is not a declared axiom.  
   - `half_up` is an allowed mode name in the schema enum, not a fully specified numeric policy in the scenario pins.

5. **Engine-only gate not in the rule expression.**  
   Block code `SOURCE_SET_UNCLOSED` appears in expected output for the open-empty scenario, but the rule’s `value` tree has no `require_closed` node; `operation-semantics.v2` defines `require_closed` as a possible op, yet this rule does not use it. Why collect-over-source_set blocks when unclosed is **engine knowledge** smuggled past the legible rule body.

6. **Scenario vs published content drift.**  
   Scenario embeds `rule-artifact.v1` / `source-closure-mapping.v1` shapes; content package members are `rule-artifact.v2` / `source-closure-mapping.v2`. A fresh reader cannot tell from the scenario alone whether the committed content package is what the expected report actually executed, or a parallel fixture dialect.

7. **Horizon mechanics.**  
   Closure fact type title mentions “membership horizon,” succession, and re-attestation. Scenario supplies `current_horizons: { "tax.us.2025.f1099int.b1": "b1.h0" }` and finding `horizon_id: "b1.h0"`. No horizon citizen schema content in the scenario explains what `b1.h0` is, how membership transitions work, or why horizon identity keys closure. Meaning is partially in the fact-type title; operational detail is missing.

8. **What this zero is *not* authorized to mean** is well fenced in prose (not line 2b, not other boxes, not non-form interest). **What additional interest still exists outside box 1** for this taxpayer is unknowable from the scenario — by design, but also un-queryable: the scenario never states the rest of the interest universe’s status.

### Score

**recovered**

The task is to surface imported vs recorded meaning; the gaps above are specific and artifact-grounded.

### Maintainer fixes (highest leverage)
| Gap | Artifact to fix | Missing element |
|---|---|---|
| Source-family / horizon vocabulary | `docs/governance/ontology.md` (or a declared schema citizen family with Ontology register entries) | Defined entries for source family, family horizon, source-closure mapping, closure finding — without ADR-only definitions |
| Empty-set and closure gate | `rule.f1099int-b1-subtotal.json` + operation-semantics content instances | Express `require_closed` (or equivalent) in the rule; pin versioned `round`/`add`/`collect` semantics including empty aggregate |
| Explanation honesty | explanation builder / `expected/report.json` | Pin actual operation-semantics versions; show zero-member collect; stop citing bare `finding_id: "round"` |
| Quantity meaning | `quantity.taxable-interest` (or companion definition citizen) | Human-readable denotation of `taxable-interest` beyond enum membership |
| Scenario/content alignment | scenario fixtures vs `package.interest-slice` members | Same schema versions as adopted package, or an explicit “scenario-local embed” contract |

---

## Tally

**Scores:** meaning **recovered**; number provenance **partial**; distinction **recovered**; honest-boundary **recovered**.

**Wrong count: 0 of 4 scored wrong.**
