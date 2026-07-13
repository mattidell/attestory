# Design Proposal: Conditional Selectors — Shape B Repair Pass

This document details the refined **Shape B (First-class Selector Citizen)** design for the `conditional-selectors` prototype, modified during the Repair 1 iteration to resolve all governance violations and adversary defects identified in Round 1 reviews.

---

## Refined Architecture of Shape B

The repaired design addresses the core failures of the initial draft:
1. **Logic/Parameter Separation (CS-G2):** All standard deduction bases and additional rates are moved to external parameter citizens. The selector rule contains only logic expressions that query these tables.
2. **Explicit Optional Defaults & V0 Absence Pinning (CS-G1):** The selector declares optional inputs and their explicit defaults directly in its payload. When evaluating, the runner records a "V0 Absence Pin" for missing optional inputs. If these are subsequently asserted, they natural-supersede V0 and trigger displacement without violating Article 7.
3. **Case Exclusivity & Order Independence (CS-A1):** The runner enforces that case guards must be mutually exclusive. If multiple guards match, it throws a collision error. An explicit `default` fallback is supported.
4. **Filing Status & Progressive Bracket Edge Cases (CS-A4, CS-A5):** Standard deduction payloads cover all 5 statuses. The progressive tax lookup (`bracket_fold`) clamps taxable income at zero, validates sorted brackets, and supports an open-ended final bracket (`limit: null`).

---

## 1. Schema Definitions

### Selector Schema: `selector-artifact.v1.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "derivation/selector-artifact.v1",
  "title": "Selector artifact",
  "description": "A first-class conditional selector citizen mapping multidimensional inputs to values or parameter lookups natively. Defines mandatory and optional dependencies with explicit defaults, evaluated as a single cascade node.",
  "type": "object",
  "properties": {
    "schema": { "const": "selector-artifact.v1" },
    "id": { "type": "string", "minLength": 1 },
    "version": { "type": "string", "pattern": "^v[0-9]+$" },
    "scope": {
      "type": "object",
      "properties": {
        "tax_year": { "type": "integer" },
        "jurisdiction": { "type": "string", "minLength": 1 },
        "family": { "type": "string", "minLength": 1 },
        "effective_from": { "type": "string", "format": "date" }
      },
      "required": ["tax_year", "jurisdiction", "family"],
      "additionalProperties": false
    },
    "publishes": { "type": "string", "minLength": 1 },
    "requires": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "uniqueItems": true,
      "description": "Mandatory symbols that must be present in the cascade to begin evaluating this selector."
    },
    "optional": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["symbol", "default"],
        "additionalProperties": false,
        "properties": {
          "symbol": { "type": "string", "minLength": 1 },
          "default": { "type": ["string", "number", "boolean", "null"] }
        }
      },
      "uniqueItems": true,
      "description": "Optional symbols. If missing in the cascade, they default to the declared value instead of blocking execution."
    },
    "cases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["when", "value"],
        "additionalProperties": false,
        "properties": {
          "when": { "$ref": "rule-artifact.v1#/$defs/expr", "description": "Mutually exclusive guard expression." },
          "value": { "$ref": "rule-artifact.v1#/$defs/expr", "description": "Value expression evaluated if this guard is true." }
        }
      }
    },
    "default": {
      "$ref": "rule-artifact.v1#/$defs/expr",
      "description": "Fallback value expression evaluated if no case guard matches."
    },
    "notes": { "type": "string" }
  },
  "required": ["schema", "id", "version", "scope", "publishes", "requires", "cases"],
  "additionalProperties": false
}
```

### Updated Bracket Definition inside Parameter Schema
To support open-ended brackets and sorted limit validation, progressive tax tables represent the final bracket with `"limit": null`:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "required": ["limit", "rate"],
    "additionalProperties": false,
    "properties": {
      "limit": { "type": ["string", "null"], "description": "Numerical upper bound or null for infinite final bracket." },
      "rate": { "type": "string" }
    }
  }
}
```

---

## 2. Refined Instance Payloads

### Parameter: Standard Deduction Base Amounts (All 5 Statuses)
##### `demo.parameter.standard-deduction-base.2025.json`
```json
{
  "schema": "parameter-declaration.v1",
  "id": "demo.parameter.standard-deduction-base.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01" },
  "values": {
    "single": "15000",
    "married_filing_jointly": "30000",
    "married_filing_separately": "15000",
    "head_of_household": "22500",
    "qualifying_surviving_spouse": "30000"
  }
}
```

### Parameter: Additional Standard Deduction Rates
Directly maps filing status to rate, simplifying logic.
##### `demo.parameter.additional-deduction-rate.2025.json`
```json
{
  "schema": "parameter-declaration.v1",
  "id": "demo.parameter.additional-deduction-rate.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01" },
  "values": {
    "single": "2000",
    "head_of_household": "2000",
    "married_filing_jointly": "1550",
    "married_filing_separately": "1550",
    "qualifying_surviving_spouse": "1550"
  }
}
```

### Parameter: Repaired Tax Brackets (With Open-Ended Final Bracket)
##### `demo.parameter.tax-brackets.2025.json`
```json
{
  "schema": "parameter-declaration.v1",
  "id": "demo.parameter.tax-brackets.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax", "effective_from": "2025-01-01" },
  "values": {
    "single": [
      { "limit": "11600", "rate": "0.10" },
      { "limit": "47150", "rate": "0.12" },
      { "limit": null, "rate": "0.22" }
    ],
    "married_filing_jointly": [
      { "limit": "23200", "rate": "0.10" },
      { "limit": "94300", "rate": "0.12" },
      { "limit": null, "rate": "0.22" }
    ]
  }
}
```

### Selector: Repaired Standard Deduction Selector
##### `demo.selector.standard-deduction.2025.json`
```json
{
  "schema": "selector-artifact.v1",
  "id": "demo.selector.standard-deduction.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "publishes": "demo.form1040.standard_deduction",
  "requires": ["filing_status", "taxpayer_over_65", "taxpayer_blind"],
  "optional": [
    { "symbol": "spouse_over_65", "default": false },
    { "symbol": "spouse_blind", "default": false }
  ],
  "cases": [
    {
      "when": {
        "op": "any",
        "args": [
          { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "single" },
          { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "head_of_household" }
        ]
      },
      "value": {
        "op": "add",
        "args": [
          { "op": "parameter", "parameter_id": "demo.parameter.standard-deduction-base.2025", "key": { "op": "ref", "name": "filing_status" } },
          {
            "op": "choose",
            "when": { "op": "ref", "name": "taxpayer_over_65" },
            "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } },
            "else": 0
          },
          {
            "op": "choose",
            "when": { "op": "ref", "name": "taxpayer_blind" },
            "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } },
            "else": 0
          }
        ]
      }
    },
    {
      "when": {
        "op": "any",
        "args": [
          { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_jointly" },
          { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_separately" },
          { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "qualifying_surviving_spouse" }
        ]
      },
      "value": {
        "op": "add",
        "args": [
          { "op": "parameter", "parameter_id": "demo.parameter.standard-deduction-base.2025", "key": { "op": "ref", "name": "filing_status" } },
          {
            "op": "choose",
            "when": { "op": "ref", "name": "taxpayer_over_65" },
            "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } },
            "else": 0
          },
          {
            "op": "choose",
            "when": { "op": "ref", "name": "taxpayer_blind" },
            "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } },
            "else": 0
          },
          {
            "op": "choose",
            "when": { "op": "ref", "name": "spouse_over_65" },
            "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } },
            "else": 0
          },
          {
            "op": "choose",
            "when": { "op": "ref", "name": "spouse_blind" },
            "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } },
            "else": 0
          }
        ]
      }
    }
  ],
  "default": null
}
```

---

## 3. Runner Evaluation and Displacement Mechanics

The runner's evaluation lifecycle for a selector citizen is structured to preserve data hygiene (Article 11/12) and strict incremental dependency tracking (Article 7).

### Mandatory and Optional Evaluation
1. **Mandatory Check:** The runner blocks selector evaluation until all symbols listed in `requires` are present. If any are absent, execution is deferred.
2. **Optional Matching & Default Injection:** The runner checks each entry in `optional`.
   * If the optional symbol is **present** in the workspace, its value is bound to the expression evaluator.
   * If the optional symbol is **absent**, the runner binds its declared `default` value in the local evaluation context.

### Pinning and Displacement (V0 Absence Pinning)
To ensure the derived finding correctly displaces when an unasserted optional input is later provided (without violating Article 7's two-edge constraint), the runner uses standard version-supersession:
* For each optional input that was **present**, the runner appends a standard pin pointing to its derived/evidence version:
  `{"role": "input", "id": "spouse_over_65", "version": "v1"}`.
* For each optional input that was **absent**, the runner appends a **V0 Absence Pin**:
  `{"role": "input", "id": "spouse_over_65", "version": "v0"}`.
* **Supersession Trigger:** If a user later asserts `spouse_over_65`, it enters the workspace with version `"v1"`. Since `"v1"` supersedes `"v0"`, the derived finding's pin for `spouse_over_65` becomes stale, triggering standard displacement.

### Case Exclusivity Verification
Before evaluating case value expressions:
1. The runner evaluates the `when` guards for all cases in the `cases` array.
2. It counts how many guards evaluate to `true`.
   * **Collision:** If $> 1$ guard is `true`, it raises `SELECTOR_COLLISION_ERROR`.
   * **Single Match:** If exactly one guard is `true`, its corresponding `value` expression is evaluated and published.
   * **No Match:** If $0$ guards are `true`, it evaluates the `default` fallback expression. If no `default` expression is provided, it raises `SELECTOR_NO_MATCH_ERROR`.

### Repaired `bracket_fold` Operations
When executing progressive tax calculations, the runner applies three strict validations:
1. **Income Clamping:** Clamps taxable income at `0` (e.g. `income = max(0, taxable_income)`). Negative inputs yield `0` tax due.
2. **Limit Sorting Check:** Validates that `limit` keys are in strictly ascending order (with `null` as the final value). If a limit is less than or equal to the previous limit, it throws `INVALID_BRACKET_ORDER`.
3. **Open-Ended Accumulation:** Accumulates tax. For any bracket $i$:
   * Width $W_i = \text{limit}_i - \text{limit}_{i-1}$ (or $\infty$ if $\text{limit}_i$ is `null`).
   * Taxed amount $A_i = \min(\text{remaining\_income}, W_i)$.
   * $\text{tax} = \text{tax} + (A_i \times \text{rate}_i)$.
   * $\text{remaining\_income} = \text{remaining\_income} - A_i$.
   * If $\text{remaining\_income} == 0$ or $\text{limit}_i$ is `null`, exit loop.

---

## 4. Synthetic Case Walkthroughs

We trace how the repaired Shape B resolves each charter case.

### Case 1: Single filer, standard deduction ($15,000 for 2025)
* **Inputs Asserted:**
  * `filing_status` = `"single"`
  * `taxpayer_over_65` = `false`
  * `taxpayer_blind` = `false`
* **Cascade Trace:**
  1. Mandatory checks pass. `spouse_over_65` and `spouse_blind` are absent; runner binds them to `false` and writes V0 pins.
  2. Guards check: Case 1 evaluates to `true` (status is single). Case 2 evaluates to `false`.
  3. Value evaluation: Looks up base deduction for `"single"` ($15,000). Evaluates choose blocks for age/blindness to 0. Total = $15,000.
  4. Publishes standard deduction finding pinning `filing_status` (v1), `taxpayer_over_65` (v1), `taxpayer_blind` (v1), `spouse_over_65` (v0), `spouse_blind` (v0).

### Case 2: Married Filing Jointly, standard deduction ($30,000 for 2025)
* **Inputs Asserted:**
  * `filing_status` = `"married_filing_jointly"`
  * `taxpayer_over_65` = `false`; `taxpayer_blind` = `false`
  * `spouse_over_65` = `false`; `spouse_blind` = `false`
* **Cascade Trace:**
  1. Mandatory and optional checks pass (all inputs present).
  2. Case 2 matches (status is MFJ).
  3. Value lookup resolves base to $30,000, additions to 0. Total = $30,000.
  4. Publishes finding pinning all inputs at v1.

### Case 3: Single filer, over 65 (additional standard deduction $2,000)
* **Inputs Asserted:**
  * `filing_status` = `"single"`
  * `taxpayer_over_65` = `true`
  * `taxpayer_blind` = `false`
* **Cascade Trace:**
  1. Case 1 matches (status is single).
  2. Base deduction resolves to $15,000. Additional rate lookup for `"single"` resolves to $2,000.
  3. Age choose block evaluates to `then` branch ($2,000). Blindness choose evaluates to 0.
  4. Total deduction = $15,000 + $2,000 = $17,000.

### Case 4: Married filer, blind (additional standard deduction $1,550)
* **Inputs Asserted:**
  * `filing_status` = `"married_filing_jointly"`
  * `taxpayer_over_65` = `false`; `taxpayer_blind` = `true`
  * `spouse_over_65` = `false`; `spouse_blind` = `false`
* **Cascade Trace:**
  1. Case 2 matches (status is MFJ).
  2. Base deduction resolves to $30,000. Additional rate lookup for `"married_filing_jointly"` resolves to $1,550.
  3. Taxpayer blind choose block evaluates to $1,550. All other choose blocks evaluate to 0.
  4. Total deduction = $30,000 + $1,550 = $31,550.

### Case 5: Tax bracket lookup crossing a threshold (Single, $15,000 taxable income)
* **Inputs Asserted:**
  * `demo.form1040.taxable_income` = `15000`
  * `filing_status` = `"single"`
  * `rounding.convention` = `"nearest"`
* **Cascade Trace:**
  1. `demo.selector.tax-calculation.2025` runs. Guard is `true`.
  2. Tax brackets table loaded. Validation confirms brackets are sorted.
  3. Clamps taxable income to `max(0, 15000) = 15000`.
  4. Accumulation starts:
     * Bracket 1: limit `11600`. Accumulation: $\min(15000, 11600) \times 0.10 = 1160$. Remaining = $3400$.
     * Bracket 2: limit `47150`. Width = $47150 - 11600 = 35550$. Accumulation: $\min(3400, 35550) \times 0.12 = 408$. Remaining = $0$.
  5. Total tax is rounded to nearest integer: $1160 + 408 = 1568$.
