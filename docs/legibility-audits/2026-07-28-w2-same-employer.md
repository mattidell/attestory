# Legibility audit — w2-same-employer

**Date:** 2026-07-28  
**Scope:** `w2-same-employer`  
**Scenario:** `packages/sample_data/tax/scenarios/two_w2_same_employer`  
**Auditor posture:** context-starved; no prior project knowledge. Only allowed paths were used (Ontology, Constitution, `packages/schemas/**`, `packages/content/**`, `packages/sample_data/**`, `README.md`). No ADRs, retrospectives, reviews, proposals, prototypes, phases, Commentary, Principles, AGENTS.md, PROJECT_PLANNING.md, memory files, commit messages, or other legibility-audit docs were opened. No accidental forbidden opens.

**Note on workspace state:** The audit working tree initially lacked project files; allowed trees were restored from a sibling agent checkout of the same repository so the committed artifacts could be read. Only Ontology + Constitution were copied from governance (not Commentary or Principles).

---

## Task 1 — Meaning recovery

### Files read
- `docs/governance/ontology.md` (§0–§2 on fact / fact type / finding; register)
- `docs/governance/constitution.md` (Articles 1, 9–12 for citizen/schema/rule posture)
- `packages/schemas/kernel/fact-type.v1.schema.json`
- `packages/schemas/kernel/finding.v1.schema.json`
- `packages/schemas/kernel/entity.v1.schema.json`
- `packages/content/tax/2025/w2.bundle.json` (also skimmed `w2.bundle.v2.json` / `v3.json` titles only as needed for consistency)
- `packages/content/tax/2025/form1040.line-1a.form-field.json`
- `packages/schemas/tax/form-field.v1.schema.json`
- `packages/schemas/tax/form-field.v2.schema.json`
- `packages/content/tax/2025/family.w2.v2.json`
- `packages/content/tax/2025/citation.form1040.line-1a.json`
- `packages/sample_data/tax/workspaces/two_w2_same_employer/acts.jsonl` (bundle adoption carrying the fact-type declaration)

### Recovery attempt

**Citizen chosen:** fact type `tax.us.2025.w2.box1-wages` (schema `fact-type.v1` / bundle instance `fact-type.v2`).

**Real-world thing it represents (from artifact + Ontology):**  
Ontology §2: a *fact type* is “a kind of question the workspace can address.” The declared title states the question: wages, tips, and other compensation in **box 1 of one W-2 slip**, for a given employer, tax year, and W-2-slip thing — not for a submitted document. Nature is `determinable` (world already determines the answer; Ontology: not an elective choice). Value schema: non-negative number.

**What a valid instance asserts:**  
A *finding* of this fact type asserts an answer to that question for one individuated *fact*. From the workspace acts/read-model, a valid documentary finding e.g. `demo-finding-w2-alpha-1-box1` asserts: for employer `demo-employer-alpha`, W-2 slip `demo-w2-slip-alpha-1`, tax year 2025, box-1 wages are `52000`, basis `documentary`, grounded by evidence `demo-evidence-w2-alpha-1`. Two same-employer slips are two facts (title + identity keys: employer + w2-slip + tax-year literal 2025). Supersession policy `free` means a corrected value for the *same* slip displaces the prior finding; it does not merge slips.

Related presentation citizen `tax.us.2025.form1040.line-1a` binds symbol `tax.us.2025.wages.total-w2-box1` and describes Form 1040 (2025) line 1a as the total of box 1 across Forms W-2 — that is the *aggregate* presentation target, not the per-slip fact type.

### Score
**recovered**

### Gaps (none required for score; residual)
- Entity *kinds* `tax.us.employer` and `tax.us.w2-slip` appear only as string patterns on entities; no schema in allowed paths defines what constitutes a “W-2 slip thing” vs a document. Meaning is recoverable for the *fact type* without that, but the entity kinds themselves are thin labels.

---

## Task 2 — Number provenance

### Files read
- `packages/sample_data/tax/scenarios/two_w2_same_employer/scenario.json`
- `packages/sample_data/tax/scenarios/two_w2_same_employer/expected/report.json`
- `packages/sample_data/tax/scenarios/two_w2_same_employer/expected/report.txt`
- `packages/content/tax/2025/rule.wages-line1a.json` (`tax.us.2025.rule.w2-box1-to-line1a`)
- `packages/content/tax/2025/package.first-tax-slice.json`
- `packages/schemas/derivation/rule-artifact.v1.schema.json`
- `packages/schemas/derivation/operation-semantics.v1.schema.json`
- `packages/schemas/derivation/npe-walk.v1.schema.json`
- `README.md` (derive runner: explanation is a walk of pins, not re-evaluation)
- Cross-check only: workspace `acts.jsonl` / `expected/read-model.json` for source finding values (same 52000 / 8000)

### Recovery attempt

**Number:** published derived value  
`tax.us.2025.wages.total-w2-box1 = 60000`  
(finding id `finding:derived:5babb827ccd3a11b09f87b88`, run `tax.us.2025.run.two-w2-same-employer`, stop reason `saturated`).

**Trace from pins / explanation / scenario rule:**

| Role | Identity | Contribution |
|------|----------|----------------|
| Output | `tax.us.2025.wages.total-w2-box1` | `60000` |
| Produced by | `tax.us.2025.rule.w2-box1-to-line1a` v1, role `field-mapping` | Declares the expression |
| Input | `demo-finding-w2-alpha-1-box1` → symbol `tax.us.2025.w2.box1-wages` | `52000` |
| Input | `demo-finding-w2-alpha-2-box1` → same symbol | `8000` |
| Input | `tax.us.2025.finding.rounding-convention` → `rounding.convention` | `half_up` (required dependency) |
| Operation semantics | `round` v1 | Mode from `rounding.convention`; stage `after_aggregate` |
| Adoption | `tax.us.2025.package.first-tax-slice` v1 | Only package member is this rule |
| Governance | `governance.constitution` v1 | Pinned; no numeric role |

**Expression (rule artifact / scenario inline copy):**

1. `collect` all current findings named `tax.us.2025.w2.box1-wages` from source set `tax.us.2025.w2`
2. `add` those values → \(52000 + 8000 = 60000\)
3. `round` the aggregate under mode `half_up`, stage `after_aggregate`

Rule notes state this is Form 1040 (2025) line 1a (“Total amount from Form(s) W-2, box 1…”). Form-field citizen binds that symbol to line 1a.

No separate `parameters` array entries in the scenario; the only parameter-like dependency is the asserted `rounding.convention` input.

### Score
**recovered** for the identity of the number and the causal chain (inputs → collect/add → round → published symbol).

### Residual (does not block this number’s provenance, but incomplete canon)
- Explanation lists `[operation-semantics] round` with `value: null`. Allowed trees contain the *schema* for operation-semantics (modes include `half_up`, unit field required on instances) but **no committed round-semantics instance** under `packages/content/**` or this scenario’s pins with a concrete `unit` / `tie_break`. For integer 52000+8000 the unit is moot; a non-integer aggregate would not be fully reconstructable from these artifacts alone.
- Currency unit (USD dollars vs cents) is never stated on the fact type or published number — only “number” / string `"60000"`.

---

## Task 3 — Distinction recovery

### Files read
- `packages/content/tax/2025/w2.bundle.json` (fact type identity keys + title)
- `packages/sample_data/tax/workspaces/two_w2_same_employer/acts.jsonl`
- `packages/sample_data/tax/workspaces/two_w2_same_employer/expected/read-model.json`
- `packages/sample_data/tax/scenarios/two_w2_same_employer/scenario.json` + expected report
- `packages/content/tax/2025/form1040.line-1a.form-field.json` (dispositions)
- `packages/schemas/tax/form-field.v1.schema.json` (disposition explanation contract)
- `packages/content/tax/2025/family.w2.v2.json`, `closure-mapping.w2.v3.json`
- For zero-disposition contrast (same symbol family): `packages/sample_data/tax/scenarios/present_zero_w2/expected/report.txt`

### Recovery attempt

**Pair A (scenario’s main distinction) — two W-2 box-1 wage findings from the same employer that look “alike” but are different facts:**

| | Slip 1 | Slip 2 |
|--|--------|--------|
| Finding id | `demo-finding-w2-alpha-1-box1` | `demo-finding-w2-alpha-2-box1` |
| Symbol (type) | `tax.us.2025.w2.box1-wages` | same |
| Employer entity | `demo-employer-alpha` | same |
| W-2-slip entity | `demo-w2-slip-alpha-1` | `demo-w2-slip-alpha-2` |
| Value | 52000 | 8000 |
| Evidence | `demo-evidence-w2-alpha-1` | `demo-evidence-w2-alpha-2` |
| Fact id | `…\|employer=…,w2-slip=demo-w2-slip-alpha-1,tax-year=2025` | `…\|…,w2-slip=demo-w2-slip-alpha-2,…` |

**How they differ and why (artifacts alone):**  
Ontology: two findings conflict only if they answer the *same* fact. The fact type keys each question by **employer + w2-slip entity + tax-year**, never by evidence/document. Title text: “two same-employer slips are two facts, and a corrected value for the same slip supersedes.” So 52000 and 8000 are co-current strangers that both feed `collect`, not rivals. The scenario name and both sources sharing the symbol while differing on `finding_id` / slip keys encode that intent.

**Pair B (declared presentation distinction, not exercised by this scenario’s expected output):**  
Form-field dispositions for line 1a distinguish **computed_zero** (“A current derived finding publishes a numeric zero.”) from **closure_backed_zero** (“…numeric zero whose lineage pins a W-2 source-set closure finding.”). Schema `form-field.v1` states they may share render glyph `0` but must never share explanation. `present_zero_w2` shows a published `0` whose explanation pins an input `box1-wages = 0` and **not** a closure finding — i.e. a present zero member path, not a closure-backed empty-family zero. Source-closure fact type / mapping exist in content; this scenario’s read-model leaves `tax.us.2025.w2.source-closure|tax-year=2025` **open** (`current_finding_id: null`) while still publishing the nonempty aggregate — rule notes: nonempty present-source paths only; empty unclosed blocks.

### Score
**recovered** (Pair A fully from this scenario’s artifacts; Pair B recovered as a second system-level distinction from form-field + related sample, with this scenario only showing open closure alongside a nonzero publish).

---

## Task 4 — Honest-boundary recovery

### Files read
(Union of above; plus targeted probes:)
- `packages/content/tax/2025/citation.form1040.line-1a.json`
- `packages/schemas/derivation/operation-semantics.v1.schema.json` (and search for a round instance under allowed trees — none found)
- `packages/content/tax/2025/quantity.wages.v1.json`
- `docs/governance/ontology.md` (borrowing clause; reserved T1)
- `README.md` (phase blurb naming ADRs not present in allowed set)

### Recovery attempt — what these artifacts do **not** let you determine

1. **Legal authority beyond citation stubs.** Citation `tax.us.2025.citation.form1040.line-1a` only records authority family `irs-instructions`, form 1040, year 2025 — no instruction text, URL, or excerpt. Rule notes claim “checked against the official IRS Form 1040 (2025) at Track 1 implementation time,” but that check is not in the artifact. **Imported:** knowledge of what IRS Form 1040 line 1a legally requires.

2. **ADR-numbered decisions.** Rule notes, bundle titles, schema descriptions, form-field schema, source-family schema, and README all cite ADR-0011, ADR-0012, ADR-0016, ADR-0006, ADR-0028, etc. Those documents are outside the audit envelope. **Imported / unrecoverable here:** the normative decisions those IDs encode (beyond what is restated inline).

3. **Concrete rounding canon instance.** Explanation pins `round` operation-semantics with null value; no `operation-semantics` content citizen for `round` (unit, tie_break, stage prose) appears under allowed content/sample paths. Schema alone lists mode names and that `unit` exists. **Missing element for maintainers:** a versioned, pinned round-semantics instance (or embed the unit in the explanation tree).

4. **Currency / scale of numeric values.** Values are bare numbers (`52000`, `60000`). Fact-type `value_schema` is `{type: number, minimum: 0}`. Quantity vocabulary lists token `wages` without unit. **Missing:** unit and decimal scale declaration on the fact type or quantity.

5. **What a “W-2 slip” entity is, ontologically, beyond a label.** Entities are `kind` + `label` only. Whether slip identity tracks EIN+copy, sequence of issuance, corrected vs original Form W-2c, etc. is not declared. **Imported if assumed:** payroll-document domain knowledge.

6. **Why this scenario publishes without W-2 source-closure.** Read-model: closure fact open. Rule notes (and only notes) say nonempty present-source paths publish; empty unclosed blocks; “no closure-to-collect mapping exists yet, ADR-0011.” Closure-mapping content exists in the package tree (`closure-mapping.w2.v3.json`) but is **not** a member of `package.first-tax-slice` and is not pinned in the scenario explanation. A fresh reader cannot tell from the explanation tree alone whether closure is required for line 1a in product law vs deferred in this milestone package. **Missing or misleading:** explanation does not surface “closure not required for this adoption”; only free-text notes on the rule do, and they point at an unreadable ADR.

7. **Derived-finding legal/authorship construction.** Ontology marks fuller authority construction for derived findings as **reserved (T1)**. Artifacts assert instrument framing (adoption + purity) but not a settled legal theory of authorship.

8. **Engine / runner behavior not declared on the rule.** README states any conforming runner yields the same findings and that explanation walks pins — Constitution Art. 11/15 agree in principle — but evaluation edge cases (empty collect without closure; string vs number coercion of `"52000"` vs `52000` across scenario vs workspace) are not fully specified in the rule expression alone.

9. **Scenario packaging vs workspace.** Scenario flattens two sources as symbol+value without embedding fact_ids/entity keys; workspace has full individuation. Provenance of *which slip is which* in the derivation explanation tree is only via finding_id + symbol, not via employer/slip keys in `report.json`. Recoverable from workspace, weaker from explanation-only.

### Score
**recovered** (boundaries above are supported by silence or external references in the allowed artifacts).

### Maintainer fixes (highest leverage)
| Gap | Artifact to fix | Exact missing/misleading element |
|-----|-----------------|----------------------------------|
| Rounding unit / half_up meaning | Pin a `operation-semantics` instance for `round` into the package and explanation tree | Explanation currently has `value: null` for operation-semantics; no content instance |
| Currency scale | `tax.us.2025.w2.box1-wages` value_schema and/or quantity vocabulary | State unit (e.g. USD whole dollars) |
| Closure vs present-source policy | Rule notes + package membership + explanation children | Policy buried in notes + ADR id; not a pin; closure mapping not in adopted package but exists nearby — easy to misread as operative |
| Citation substance | `citation.form1040.line-1a` | Only form/year metadata; no locatable instruction body |
| ADR leak into public notes | `rule.wages-line1a.json` notes, bundle titles | Replace or restating ADR claims so meaning does not require the ADR tree |
| Explanation slip identity | Scenario expected `report.json` explanation nodes | Include identity-key context (employer, w2-slip) on input nodes, not only finding_id |

---

## Scoring summary

| Task | Score |
|------|--------|
| 1 Meaning recovery | recovered |
| 2 Number provenance | recovered |
| 3 Distinction recovery | recovered |
| 4 Honest-boundary recovery | recovered |

**Tally of wrong scores: 0 of 4.**

*(No task scored `wrong` or `unrecoverable`. Task 2 is fully recovered for this integer aggregate; residual unit/rounding-instance gaps are catalogued under Task 4 rather than downgraded to partial, because 60000’s production chain is explicit in pins and rule expression without needing the missing canon for these inputs.)*
