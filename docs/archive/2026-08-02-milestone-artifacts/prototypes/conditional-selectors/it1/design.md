# Design Proposal: Conditional Selectors in the Derivation Cascade

This document presents the iteration 1 design for modeling and resolving conditional tax selectors—specifically standard deduction status lookups and tax bracket selection—within the derivation engine. It compares two architectural shapes:

* **Shape A (Rule-driven Cascade):** Logic is modeled as a cascade of standard rule and parameter citizens.
* **Shape B (First-class Selector Citizen):** A specialized `selector-artifact.v1` citizen type is added to the derivation schemas and evaluated natively by the runner.

---

## Shape A: Rule-driven Cascade

Shape A utilizes the existing `rule-artifact.v1` and `parameter-declaration.v1` schemas. It expresses conditional logic by decomposing the calculation into atomic rules and parameter lookups, mapping relationships via the dependency graph.

### 1. Schema Utilization
Shape A relies entirely on the existing production schemas:
* [rule-artifact.v1.schema.json](../../../../../../packages/schemas/derivation/rule-artifact.v1.schema.json)
* [parameter-declaration.v1.schema.json](../../../../../../packages/schemas/derivation/parameter-declaration.v1.schema.json)

### 2. Instance Payloads

#### Parameters

##### [NEW] `parameter.standard-deduction-base.2025.json`
Represents the base standard deduction amounts by filing status.
```json
{
  "schema": "parameter-declaration.v1",
  "id": "demo.parameter.standard-deduction-base.2025",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax",
    "effective_from": "2025-01-01"
  },
  "values": {
    "single": "15000",
    "married_filing_jointly": "30000",
    "married_filing_separately": "15000",
    "head_of_household": "22500",
    "qualifying_surviving_spouse": "30000"
  }
}
```

##### [NEW] `parameter.additional-deduction-rate.2025.json`
Defines the additional standard deduction amount for age/blindness.
```json
{
  "schema": "parameter-declaration.v1",
  "id": "demo.parameter.additional-deduction-rate.2025",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax",
    "effective_from": "2025-01-01"
  },
  "values": {
    "single_or_hoh": "2000",
    "married_or_spouse": "1550"
  }
}
```

##### [NEW] `parameter.tax-brackets.2025.json`
Progressive tax rate limits and rates.
```json
{
  "schema": "parameter-declaration.v1",
  "id": "demo.parameter.tax-brackets.2025",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax",
    "effective_from": "2025-01-01"
  },
  "values": {
    "single": [
      { "limit": "11600", "rate": "0.10" },
      { "limit": "47150", "rate": "0.12" },
      { "limit": "100525", "rate": "0.22" }
    ],
    "married_filing_jointly": [
      { "limit": "23200", "rate": "0.10" },
      { "limit": "94300", "rate": "0.12" },
      { "limit": "201050", "rate": "0.22" }
    ]
  }
}
```

#### Rules

##### [NEW] `rule.spouse-over-65-default.2025.json`
Injects a default `false` for `spouse_over_65` if the taxpayer is single/HoH, preventing dependency blocking.
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.spouse-over-65-default.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "applicability",
  "requires": ["filing_status"],
  "when": {
    "op": "not",
    "value": {
      "op": "any",
      "args": [
        { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_jointly" },
        { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_separately" }
      ]
    }
  },
  "value": false,
  "publishes": "spouse_over_65",
  "blocked": { "code": "OPEN_DEPENDENCY", "missing": ["filing_status"] }
}
```

##### [NEW] `rule.spouse-blind-default.2025.json`
Injects a default `false` for `spouse_blind` if the taxpayer is single/HoH.
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.spouse-blind-default.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "applicability",
  "requires": ["filing_status"],
  "when": {
    "op": "not",
    "value": {
      "op": "any",
      "args": [
        { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_jointly" },
        { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_separately" }
      ]
    }
  },
  "value": false,
  "publishes": "spouse_blind",
  "blocked": { "code": "OPEN_DEPENDENCY", "missing": ["filing_status"] }
}
```

##### [NEW] `rule.base-standard-deduction.2025.json`
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.base-standard-deduction.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "computation",
  "requires": ["filing_status"],
  "when": true,
  "value": {
    "op": "parameter",
    "parameter_id": "demo.parameter.standard-deduction-base.2025",
    "key": { "op": "ref", "name": "filing_status" }
  },
  "publishes": "demo.form1040.standard_deduction_base",
  "blocked": { "code": "OPEN_DEPENDENCY", "missing": ["filing_status"] }
}
```

##### [NEW] `rule.additional-share-rate.2025.json`
Selects the additional standard deduction share rate ($2,000 for single/HoH, $1,550 for married/surviving spouse).
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.additional-share-rate.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "computation",
  "requires": ["filing_status"],
  "when": true,
  "value": {
    "op": "choose",
    "when": {
      "op": "any",
      "args": [
        { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "single" },
        { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "head_of_household" }
      ]
    },
    "then": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": "single_or_hoh" },
    "else": { "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": "married_or_spouse" }
  },
  "publishes": "demo.form1040.additional_share_rate",
  "blocked": { "code": "OPEN_DEPENDENCY", "missing": ["filing_status"] }
}
```

##### [NEW] `rule.taxpayer-shares.2025.json`
Counts additional deduction shares for the primary taxpayer (age $\ge$ 65, blindness).
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.taxpayer-shares.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "computation",
  "requires": ["taxpayer_over_65", "taxpayer_blind"],
  "when": true,
  "value": {
    "op": "add",
    "args": [
      { "op": "choose", "when": { "op": "ref", "name": "taxpayer_over_65" }, "then": 1, "else": 0 },
      { "op": "choose", "when": { "op": "ref", "name": "taxpayer_blind" }, "then": 1, "else": 0 }
    ]
  },
  "publishes": "demo.form1040.taxpayer_shares",
  "blocked": { "code": "OPEN_DEPENDENCY", "missing": ["taxpayer_over_65", "taxpayer_blind"] }
}
```

##### [NEW] `rule.spouse-shares.2025.json`
Counts additional deduction shares for the spouse (only if married).
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.spouse-shares.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "computation",
  "requires": ["spouse_over_65", "spouse_blind"],
  "when": true,
  "value": {
    "op": "add",
    "args": [
      { "op": "choose", "when": { "op": "ref", "name": "spouse_over_65" }, "then": 1, "else": 0 },
      { "op": "choose", "when": { "op": "ref", "name": "spouse_blind" }, "then": 1, "else": 0 }
    ]
  },
  "publishes": "demo.form1040.spouse_shares",
  "blocked": { "code": "OPEN_DEPENDENCY", "missing": ["spouse_over_65", "spouse_blind"] }
}
```

##### [NEW] `rule.total-standard-deduction.2025.json`
Combines base and additional deductions. Since the core expression syntax does not support multiplication (`multiply`), standard deduction additional shares must be folded via a conditional addition cascade (`choose`/`add`).
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.total-standard-deduction.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "computation",
  "requires": [
    "demo.form1040.standard_deduction_base",
    "demo.form1040.additional_share_rate",
    "demo.form1040.taxpayer_shares",
    "demo.form1040.spouse_shares"
  ],
  "when": true,
  "value": {
    "op": "add",
    "args": [
      { "op": "ref", "name": "demo.form1040.standard_deduction_base" },
      {
        "op": "choose",
        "when": {
          "op": "compare",
          "left": {
            "op": "add",
            "args": [
              { "op": "ref", "name": "demo.form1040.taxpayer_shares" },
              { "op": "ref", "name": "demo.form1040.spouse_shares" }
            ]
          },
          "cmp": "eq",
          "right": 0
        },
        "then": 0,
        "else": {
          "op": "choose",
          "when": {
            "op": "compare",
            "left": {
              "op": "add",
              "args": [
                { "op": "ref", "name": "demo.form1040.taxpayer_shares" },
                { "op": "ref", "name": "demo.form1040.spouse_shares" }
              ]
            },
            "cmp": "eq",
            "right": 1
          },
          "then": { "op": "ref", "name": "demo.form1040.additional_share_rate" },
          "else": {
            "op": "choose",
            "when": {
              "op": "compare",
              "left": {
                "op": "add",
                "args": [
                  { "op": "ref", "name": "demo.form1040.taxpayer_shares" },
                  { "op": "ref", "name": "demo.form1040.spouse_shares" }
                ]
              },
              "cmp": "eq",
              "right": 2
            },
            "then": {
              "op": "add",
              "args": [
                { "op": "ref", "name": "demo.form1040.additional_share_rate" },
                { "op": "ref", "name": "demo.form1040.additional_share_rate" }
              ]
            },
            "else": {
              "op": "choose",
              "when": {
                "op": "compare",
                "left": {
                  "op": "add",
                  "args": [
                    { "op": "ref", "name": "demo.form1040.taxpayer_shares" },
                    { "op": "ref", "name": "demo.form1040.spouse_shares" }
                  ]
                },
                "cmp": "eq",
                "right": 3
              },
              "then": {
                "op": "add",
                "args": [
                  { "op": "ref", "name": "demo.form1040.additional_share_rate" },
                  { "op": "ref", "name": "demo.form1040.additional_share_rate" },
                  { "op": "ref", "name": "demo.form1040.additional_share_rate" }
                ]
              },
              "else": {
                "op": "add",
                "args": [
                  { "op": "ref", "name": "demo.form1040.additional_share_rate" },
                  { "op": "ref", "name": "demo.form1040.additional_share_rate" },
                  { "op": "ref", "name": "demo.form1040.additional_share_rate" },
                  { "op": "ref", "name": "demo.form1040.additional_share_rate" }
                ]
              }
            }
          }
        }
      }
    ]
  },
  "publishes": "demo.form1040.standard_deduction",
  "blocked": {
    "code": "OPEN_DEPENDENCY",
    "missing": [
      "demo.form1040.standard_deduction_base",
      "demo.form1040.additional_share_rate",
      "demo.form1040.taxpayer_shares",
      "demo.form1040.spouse_shares"
    ]
  }
}
```

##### [NEW] `rule.tax-calculation.2025.json`
Performs progressive tax bracket lookup using the existing `bracket_fold` operation.
```json
{
  "schema": "rule-artifact.v1",
  "id": "demo.rule.tax-calculation.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "role": "computation",
  "requires": ["demo.form1040.taxable_income", "filing_status", "rounding.convention"],
  "when": true,
  "value": {
    "op": "round",
    "value": {
      "op": "bracket_fold",
      "table_id": "demo.parameter.tax-brackets.2025",
      "key": { "op": "ref", "name": "filing_status" },
      "value": { "op": "ref", "name": "demo.form1040.taxable_income" }
    },
    "mode": { "op": "ref", "name": "rounding.convention" },
    "stage": "final"
  },
  "publishes": "demo.form1040.tax_due",
  "blocked": { "code": "OPEN_DEPENDENCY", "missing": ["demo.form1040.taxable_income", "filing_status"] }
}
```

---

### 3. Step-by-Step Cascade Walkthroughs (Shape A)

#### Case 1: Single filer, standard deduction ($15,000 for 2025)
* **Inputs Asserted:**
  * `filing_status` = `"single"`
  * `taxpayer_over_65` = `false`
  * `taxpayer_blind` = `false`
  * `rounding.convention` = `"nearest"`
* **Derivation Sequence:**
  1. `rule.spouse-over-65-default` and `rule.spouse-blind-default` evaluate because `filing_status` is available and not married. They publish `spouse_over_65` = `false` and `spouse_blind` = `false`.
  2. `rule.base-standard-deduction` evaluates using `filing_status` = `"single"`. Parameter lookup resolves to `"15000"`. Publishes `demo.form1040.standard_deduction_base` = `15000`.
  3. `rule.additional-share-rate` evaluates. The guard checks if filing status is single/HoH (True) and resolves to parameter key `single_or_hoh` = `"2000"`. Publishes `demo.form1040.additional_share_rate` = `2000`.
  4. `rule.taxpayer-shares` evaluates. `add(choose(false, 1, 0), choose(false, 1, 0))` = `0`. Publishes `demo.form1040.taxpayer_shares` = `0`.
  5. `rule.spouse-shares` evaluates. Since `spouse_over_65` and `spouse_blind` were defaulted to `false`, it resolves to `0`. Publishes `demo.form1040.spouse_shares` = `0`.
  6. `rule.total-standard-deduction` evaluates. Total shares = `add(0, 0)` = `0`. The choose block falls into the `0` share case. Final standard deduction = `add(15000, 0)` = `15000`. Publishes `demo.form1040.standard_deduction` = `15000`.

#### Case 2: Married Filing Jointly, standard deduction ($30,000 for 2025)
* **Inputs Asserted:**
  * `filing_status` = `"married_filing_jointly"`
  * `taxpayer_over_65` = `false`
  * `taxpayer_blind` = `false`
  * `spouse_over_65` = `false`
  * `spouse_blind` = `false`
* **Derivation Sequence:**
  1. Default injection rules `rule.spouse-*` do not execute because their `when` guards evaluate to `false` (since the status is married). The explicitly asserted spouse inputs satisfy downstream dependencies.
  2. `rule.base-standard-deduction` evaluates. Parameter lookup for `"married_filing_jointly"` resolves to `"30000"`. Publishes `demo.form1040.standard_deduction_base` = `30000`.
  3. `rule.additional-share-rate` evaluates. The guard checks single/HoH (False) and selects the `else` branch mapping to `"1550"`. Publishes `demo.form1040.additional_share_rate` = `1550`.
  4. `rule.taxpayer-shares` evaluates to `0`. Publishes `demo.form1040.taxpayer_shares` = `0`.
  5. `rule.spouse-shares` evaluates to `0`. Publishes `demo.form1040.spouse_shares` = `0`.
  6. `rule.total-standard-deduction` evaluates. Total shares = `0`. Final standard deduction = `add(30000, 0)` = `30000`. Publishes `demo.form1040.standard_deduction` = `30000`.

#### Case 3: Single filer, over 65 (additional standard deduction $2,000)
* **Inputs Asserted:**
  * `filing_status` = `"single"`
  * `taxpayer_over_65` = `true`
  * `taxpayer_blind` = `false`
* **Derivation Sequence:**
  1. `spouse_over_65` and `spouse_blind` default to `false`.
  2. `demo.form1040.standard_deduction_base` resolves to `15000`.
  3. `demo.form1040.additional_share_rate` resolves to `2000`.
  4. `rule.taxpayer-shares` evaluates: `add(choose(true, 1, 0), choose(false, 1, 0))` = `add(1, 0)` = `1`. Publishes `demo.form1040.taxpayer_shares` = `1`.
  5. `rule.spouse-shares` evaluates to `0`.
  6. `rule.total-standard-deduction` evaluates. Total shares = `add(1, 0)` = `1`. The choose block matches `1` share and adds `2000`. Final standard deduction = `add(15000, 2000)` = `17000`. Publishes `demo.form1040.standard_deduction` = `17000`.

#### Case 4: Married filer, blind (additional standard deduction $1,550)
* **Inputs Asserted:**
  * `filing_status` = `"married_filing_jointly"`
  * `taxpayer_over_65` = `false`
  * `taxpayer_blind` = `true`
  * `spouse_over_65` = `false`
  * `spouse_blind` = `false`
* **Derivation Sequence:**
  1. `demo.form1040.standard_deduction_base` resolves to `30000`.
  2. `demo.form1040.additional_share_rate` resolves to `1550`.
  3. `rule.taxpayer-shares` evaluates: `add(choose(false, 1, 0), choose(true, 1, 0))` = `1`.
  4. `rule.spouse-shares` evaluates to `0`.
  5. `rule.total-standard-deduction` evaluates. Total shares = `add(1, 0)` = `1`. Choose block matches `1` share and adds `1550`. Final standard deduction = `add(30000, 1550)` = `31550`. Publishes `demo.form1040.standard_deduction` = `31550`.

#### Case 5: Tax bracket lookup crossing a threshold (Single, $15,000 taxable income)
* **Inputs Asserted:**
  * `demo.form1040.taxable_income` = `15000`
  * `filing_status` = `"single"`
  * `rounding.convention` = `"nearest"`
* **Derivation Sequence:**
  1. `rule.tax-calculation` evaluates. It retrieves the table `demo.parameter.tax-brackets.2025`.
  2. Since `filing_status` is `"single"`, the array `values.single` is selected:
     * Bracket 1: limit `11600`, rate `0.10`
     * Bracket 2: limit `47150`, rate `0.12`
  3. The `bracket_fold` operation accumulates:
     * Bracket 1: $\min(15000, 11600) \times 0.10 = 11600 \times 0.10 = 1160$. Remaining income = $15000 - 11600 = 3400$.
     * Bracket 2: $\min(3400, 47150 - 11600) \times 0.12 = 3400 \times 0.12 = 408$. Remaining income = $0$.
     * Sum = $1160 + 408 = 1568$.
  4. The result `1568` is rounded to nearest integer under `"nearest"` convention, publishing `demo.form1040.tax_due` = `1568`.

---

## Shape B: First-class Selector Citizen

Shape B introduces a new first-class citizen type: `selector-artifact.v1`. A selector groups multiple conditional execution branches and defaults directly inside one citizen document. Crucially, it distinguishes between **mandatory dependencies** (which block execution) and **optional dependencies** (which default or are bypassed if unused), resolving optional dependency blocking natively inside the runner rather than requiring default-injector rules.

### 1. Schema Definition

##### [NEW] `selector-artifact.v1.schema.json`
Draft JSON Schema defining the new first-class citizen.
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "derivation/selector-artifact.v1",
  "title": "Selector artifact",
  "description": "A first-class conditional selector citizen that maps complex inputs to values or parameter lookups natively. Evaluated as a single node in the derivation cascade, resolving optional dependency blocking internally without cascading rule clutter.",
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
      "items": { "type": "string", "minLength": 1 },
      "uniqueItems": true,
      "description": "Optional symbols. If missing, references to these in values resolve to null or false rather than blocking evaluation."
    },
    "cases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["when", "value"],
        "additionalProperties": false,
        "properties": {
          "when": { "$ref": "rule-artifact.v1#/$defs/expr", "description": "Applicability guard. Triggers the case if true." },
          "value": { "$ref": "rule-artifact.v1#/$defs/expr", "description": "Expression representing the output value if this case is selected." }
        }
      }
    },
    "notes": { "type": "string" }
  },
  "required": ["schema", "id", "version", "scope", "publishes", "requires", "cases"],
  "additionalProperties": false
}
```

---

### 2. Instance Payloads

##### [NEW] `selector.standard-deduction.2025.json`
Expresses standard deduction base lookups and age/blind adjustments inside a single selector file.
```json
{
  "schema": "selector-artifact.v1",
  "id": "demo.selector.standard-deduction.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "publishes": "demo.form1040.standard_deduction",
  "requires": ["filing_status", "taxpayer_over_65", "taxpayer_blind"],
  "optional": ["spouse_over_65", "spouse_blind"],
  "cases": [
    {
      "when": { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "single" },
      "value": {
        "op": "add",
        "args": [
          15000,
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_over_65" }, "then": 2000, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_blind" }, "then": 2000, "else": 0 }
        ]
      }
    },
    {
      "when": { "op": "compare", "left": { "op": "ref", "name": "filing_status" }, "cmp": "eq", "right": "married_filing_jointly" },
      "value": {
        "op": "add",
        "args": [
          30000,
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_over_65" }, "then": 1550, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "taxpayer_blind" }, "then": 1550, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "spouse_over_65" }, "then": 1550, "else": 0 },
          { "op": "choose", "when": { "op": "ref", "name": "spouse_blind" }, "then": 1550, "else": 0 }
        ]
      }
    }
  ]
}
```

##### [NEW] `selector.tax-calculation.2025.json`
Groups tax calculation parameters and progressive calculation inside one selector file.
```json
{
  "schema": "selector-artifact.v1",
  "id": "demo.selector.tax-calculation.2025",
  "version": "v1",
  "scope": { "tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax" },
  "publishes": "demo.form1040.tax_due",
  "requires": ["demo.form1040.taxable_income", "filing_status", "rounding.convention"],
  "cases": [
    {
      "when": true,
      "value": {
        "op": "round",
        "value": {
          "op": "bracket_fold",
          "table_id": "demo.parameter.tax-brackets.2025",
          "key": { "op": "ref", "name": "filing_status" },
          "value": { "op": "ref", "name": "demo.form1040.taxable_income" }
        },
        "mode": { "op": "ref", "name": "rounding.convention" },
        "stage": "final"
      }
    }
  ]
}
```

---

### 3. Step-by-Step Cascade Walkthroughs (Shape B)

#### Case 1: Single filer, standard deduction ($15,000 for 2025)
* **Inputs Asserted:**
  * `filing_status` = `"single"`
  * `taxpayer_over_65` = `false`
  * `taxpayer_blind` = `false`
* **Derivation Sequence:**
  1. The runner schedules `demo.selector.standard-deduction.2025` for evaluation. It checks the `requires` symbols: `filing_status`, `taxpayer_over_65`, and `taxpayer_blind` are all present. Optional dependencies `spouse_over_65` and `spouse_blind` are absent, so their references inside expressions are initialized to `false`.
  2. The runner evaluates `cases` sequentially:
     * Case 1: `when` check `filing_status == "single"` evaluates to `true`.
     * The runner evaluates Case 1's `value` expression:
       `add(15000, choose(false, 2000, 0), choose(false, 2000, 0))` = `add(15000, 0, 0)` = `15000`.
  3. The runner publishes `demo.form1040.standard_deduction` = `15000` and exits (Case 2 is never evaluated).

#### Case 2: Married Filing Jointly, standard deduction ($30,000 for 2025)
* **Inputs Asserted:**
  * `filing_status` = `"married_filing_jointly"`
  * `taxpayer_over_65` = `false`
  * `taxpayer_blind` = `false`
  * `spouse_over_65` = `false`
  * `spouse_blind` = `false`
* **Derivation Sequence:**
  1. The runner schedules the selector. All mandatory (`requires`) and optional (`optional`) inputs are present.
  2. The runner evaluates `cases`:
     * Case 1: `filing_status == "single"` evaluates to `false`.
     * Case 2: `filing_status == "married_filing_jointly"` evaluates to `true`.
     * The runner evaluates Case 2's `value` expression:
       `add(30000, choose(false, 1550, 0), choose(false, 1550, 0), choose(false, 1550, 0), choose(false, 1550, 0))` = `30000`.
  3. The runner publishes `demo.form1040.standard_deduction` = `30000`.

#### Case 3: Single filer, over 65 (additional standard deduction $2,000)
* **Inputs Asserted:**
  * `filing_status` = `"single"`
  * `taxpayer_over_65` = `true`
  * `taxpayer_blind` = `false`
* **Derivation Sequence:**
  1. The runner schedules the selector (mandatory inputs present; optional inputs missing and defaulted to `false`).
  2. Case 1 is selected (`filing_status == "single"`).
  3. Evaluates expression:
     `add(15000, choose(true, 2000, 0), choose(false, 2000, 0))` = `add(15000, 2000, 0)` = `17000`.
  4. Publishes `demo.form1040.standard_deduction` = `17000`.

#### Case 4: Married filer, blind (additional standard deduction $1,550)
* **Inputs Asserted:**
  * `filing_status` = `"married_filing_jointly"`
  * `taxpayer_over_65` = `false`
  * `taxpayer_blind` = `true`
  * `spouse_over_65` = `false`
  * `spouse_blind` = `false`
* **Derivation Sequence:**
  1. The runner schedules the selector (all inputs present).
  2. Case 2 is selected (`filing_status == "married_filing_jointly"`).
  3. Evaluates expression:
     `add(30000, choose(false, 1550, 0), choose(true, 1550, 0), choose(false, 1550, 0), choose(false, 1550, 0))` = `add(30000, 0, 1550, 0, 0)` = `31550`.
  4. Publishes `demo.form1040.standard_deduction` = `31550`.

#### Case 5: Tax bracket lookup crossing a threshold (Single, $15,000 taxable income)
* **Inputs Asserted:**
  * `demo.form1040.taxable_income` = `15000`
  * `filing_status` = `"single"`
  * `rounding.convention` = `"nearest"`
* **Derivation Sequence:**
  1. The runner schedules `demo.selector.tax-calculation.2025`.
  2. Case 1 guard is `true`. The runner evaluates the `value` expression, executing `bracket_fold` on `demo.parameter.tax-brackets.2025` using `filing_status` = `"single"` and value `15000`.
  3. Progressive calculation yields `1568`. Rounding yields `1568`.
  4. Publishes `demo.form1040.tax_due` = `1568`.

---

## Comparative Analysis

| Dimension | Shape A (Rule-driven Cascade) | Shape B (First-class Selector) |
|---|---|---|
| **Graph Complexity** | **High.** Standard deduction requires 7 rules, 2 parameter files, and 2 default-injector rules (9 files total). | **Low.** Standard deduction requires 1 selector citizen and 1 base parameter table (2 files total). |
| **Dependency Resolution** | **Fragile.** Requires explicit default-injection rules to prevent runner deadlock on optional/unasserted inputs (e.g. spouse fields). | **Robust.** Native support for `optional` inputs resolves missing dependencies gracefully at evaluation time. |
| **Expression Expressiveness** | **Poor.** Restricted by closed operation vocabulary (e.g. lacks `multiply`), forcing deep, nested `choose` cascades to count shares. | **Clean.** While it uses the same expression language, grouping allows encapsulation of complex branches in one file. |
| **Traceability / Explainability** | **Fragmented.** A trace is a chain of 7 different rule executions, making explanation generation verbose and complex. | **Unified.** A single step explains standard deduction or tax selection, recording exactly which case matched. |
| **Runner Modification Cost** | **Zero.** Works on the current engine without changing schemas or the saturation runner. | **Medium.** Requires updating kernel/derivation schemas and implementing selector evaluation logic in the runner. |
