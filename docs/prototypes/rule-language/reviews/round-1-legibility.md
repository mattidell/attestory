# Round 1 legibility recovery

I treated the package as self-contained. The statements below report only what I can recover from the package and its two schemas; I did not supply unstated tax rules.

## Package and parameter recovery

### `pkg.2025.us-federal.1040-core.v1`

**Recovery:** This is a version `0.0.1` package for tax year 2025, US federal jurisdiction, containing 22 named rule artifacts and four parameter declarations. Its rule set traces a deliberately narrow Form 1040 path: W-2 wages and 1099-INT interest feed income; an early-withdrawal penalty feeds adjustments; filing status selects a standard deduction and ordinary-tax calculation; W-2 and 1099 withholding feed payments; the result is either an overpayment or amount owed. It also contains a paper-only 2026 evolution example.

**Confidence:** certain.

**Could not interpret exactly:** `"schema_version": "artifact-package.v1.prototype-it1"` has no supplied package schema. The operational meaning of `f10_evolution_probe`, especially `migration_artifact_implicated`, is described narratively but is not executable or schema-defined.

### `param.2025.f1040.standard_deduction.v1`

**Recovery:** A 2025 filing-status lookup table: `single` = 15,750; `mfs` = 15,750; `mfj` = 31,500; `qss` = 31,500; `hoh` = 23,625.

**Confidence:** certain.

**Could not interpret exactly:** The artifact never expands the status abbreviations. The rule schema identifies filing status only by the fact id `tax.choice.filing_status.2025`, so the allowed choice vocabulary and treatment of an unknown status are unstated.

### `param.2025.f1040.regular_tax.v1`

**Recovery:** Taxable income below 100,000 is intended to select a filing-status-specific tax-table row and return its `tax`. At 100,000 or above it selects a filing-status-specific worksheet row and computes `taxable_income * rate - subtraction`.

The supplied below-100,000 rows are:

- `single`: 84,250–84,300 -> 14,156; 99,750–99,800 -> 17,510; the ranges 0–84,250, 84,300–99,750, and 99,800–100,000 contain tax 0.
- `mfj`: 65,000–65,050 -> 7,446.
- `mfs`: 84,250–84,300 -> 14,156.
- `hoh`: 76,000–76,050 -> 10,132.

The supplied worksheet rows are:

- `single`: 100,000–103,350 at 0.22 less 5,086; 103,350–197,300 at 0.24 less 7,153; 197,300–250,525 at 0.32 less 22,937; 250,525–626,350 at 0.35 less 30,452.75; 626,350 upward at 0.37 less 42,979.75.
- `mfj`: 100,000–206,700 at 0.22 less 10,172; 206,700–394,600 at 0.24 less 14,306; 394,600–501,050 at 0.32 less 45,874; 501,050–751,600 at 0.35 less 60,905.50; 751,600 upward at 0.37 less 75,937.50.
- `mfs`: 100,000–103,350 at 0.22 less 5,086; 103,350–197,300 at 0.24 less 7,153; 197,300–250,525 at 0.32 less 22,937; 250,525–375,800 at 0.35 less 30,452.75; 375,800 upward at 0.37 less 37,968.75.
- `hoh`: 100,000–103,350 at 0.22 less 6,825; 103,350–197,300 at 0.24 less 8,892; 197,300–250,500 at 0.32 less 24,676; 250,500–626,350 at 0.35 less 32,191; 626,350 upward at 0.37 less 44,718.

**Confidence:** probable.

**Could not interpret exactly:** Neither schema defines whether `min` or `max` is inclusive. The spans `"tax_table_rows"` and `"tax_computation_worksheet_rows"` do not define missing-row, overlapping-row, or multiple-match behavior. The many zero-valued `single` rows look like placeholders, but the artifact does not say so; the other statuses omit most sub-100,000 rows entirely. `qss` exists in the deduction parameter but has no regular-tax rows. There is no rounding instruction for the computed tax.

### 2026 paper parameters

**Recovery:** `param.2026.f1040.standard_deduction.paper.v1` demonstrates a successor parameter with placeholder amounts (single/mfs 16,100; mfj/qss 32,200; hoh 24,150). `param.2026.f1040.regular_tax.paper.v1` demonstrates successor identity with a 100,000 threshold and empty row tables. The source citations expressly say these are paper-only placeholders, not adopted law.

**Confidence:** certain.

**Could not interpret exactly:** Empty regular-tax tables cannot execute the line-16 rule. The package describes successor identity, but does not contain a 2026 package or 2026 successor rule artifacts.

## Rule recovery attempts

### `rule.2025.w2.box1.to.f1040.line1a.v1`

**Recovery:** Take many W-2 box 1 wage amounts, sum them, then round the total using a required 2025 rounding-mode choice. Publish the result as Form 1040 line 1a wages. Missing wages and a missing rounding choice are identified as blockers.

**Confidence:** probable.

**Could not interpret exactly:** `"op": "round_money"` and `"mode": { "var": "rounding_mode" }` do not define any available modes or their arithmetic. `"required": true` plus `"cardinality": "many"` does not say whether an empty collection is missing. The input has `"block_reason": "missing_w2_box1_wages"`, but the only `block_templates` entry is for missing rounding, so the runtime consequence of missing wages is unclear.

### `rule.2025.1099int.box1.to.scheduleb.line1.v1`

**Recovery:** Sum all available 1099-INT box 1 interest amounts and publish the sum as the Schedule B line 1 payer-rows total. No rounding is declared.

**Confidence:** probable.

**Could not interpret exactly:** `"required": false`, `"cardinality": "many"`, and `"op": "sum"` do not state whether an absent or empty collection yields zero, no output, or an error. Although the label says “payer rows,” the expression produces only a total and preserves no payer rows or identities.

### `rule.2025.scheduleb.line2.v1`

**Recovery:** Copy the required Schedule B line 1 total directly to Schedule B line 2 total interest. It depends on the preceding 1099-INT aggregation rule.

**Confidence:** certain.

**Could not interpret exactly:** The required input names `"block_reason": "missing_schedule_b_line1"`, but `block_templates` is empty; the schemas do not say whether the reason alone creates blocking behavior.

### `rule.2025.scheduleb.line3.excludable.v1`

**Recovery:** Copy a required separately supplied 2025 excludable Series EE/I bond interest fact to Schedule B line 3. If that fact is missing, the named open-fact condition blocks the rule.

**Confidence:** certain for the computation; probable for blocking behavior.

**Could not interpret exactly:** The optional many-valued `box3_interest` input is never referenced by `"expression": { "var": "excludable_interest" }`; the artifact does not say whether box 3 constrains, corroborates, caps, or merely provides context for the supplied exclusion. The method for deriving `tax.fact.series_ee_i_bond_excludable_interest.2025` is absent, so the exclusion amount cannot be recovered from this artifact.

### `rule.2025.scheduleb.line4.to.f1040.line2b.v1`

**Recovery:** Subtract Schedule B line 3 excludable interest from line 2 total interest, round the result after subtraction using the required rounding choice, and publish the same result to Schedule B line 4 and Form 1040 line 2b.

**Confidence:** probable.

**Could not interpret exactly:** The rounding-mode vocabulary and arithmetic are absent. Nothing states whether a negative result is allowed or floored. Inputs line 2 and line 3 each carry a `block_reason`, but the sole block template names only missing rounding.

### `rule.2025.scheduleb.required.interest.v1`

**Recovery:** Schedule B is required by interest exactly when Form 1040 line 2b taxable interest is strictly greater than 1,500. Exactly 1,500 does not satisfy the expression.

**Confidence:** certain.

**Could not interpret exactly:** A missing required taxable-interest input has `"block_reason": "missing_taxable_interest"`, but no block template. The artifact does not state how this boolean combines with any other reasons Schedule B may be required.

### `rule.2025.scheduleb.partiii.required.foreign.v1`

**Recovery:** Require Schedule B Part III when the required combined “foreign account or trust” fact equals boolean `true`.

**Confidence:** certain.

**Could not interpret exactly:** The combined input fact is not derived here, and the artifact does not distinguish foreign accounts from foreign trusts or define what makes the fact true. Its missing-input block reason has no matching block template.

### `rule.2025.withholding.w2.line25a.v1`

**Recovery:** Sum all available W-2 box 2 federal-withholding amounts, round the total using the required rounding choice, and publish Form 1040 line 25a.

**Confidence:** probable.

**Could not interpret exactly:** The rounding modes are undefined. The empty/absent meaning of optional many-valued withholding is unstated. `block_templates` makes a missing rounding choice blocking, even when there are no withholding inputs, but the result in that situation is not specified.

### `rule.2025.withholding.1099.line25b.v1`

**Recovery:** Sum all available 1099-INT box 4 federal-withholding amounts, round the total using the required rounding choice, and publish Form 1040 line 25b.

**Confidence:** probable.

**Could not interpret exactly:** The rounding modes and empty/absent collection behavior are undefined. Despite the output label “Form 1099 withholding,” the only declared source fact type is 1099-INT box 4, so the artifact does not encode other kinds of Form 1099 withholding.

### `rule.2025.withholding.total.line25d.v1`

**Recovery:** Add Form 1040 lines 25a and 25b and publish the result as line 25d total withholding.

**Confidence:** certain.

**Could not interpret exactly:** Both missing inputs have block reasons but no block templates. The word “total” is broader than the encoded sum, which contains only the two declared inputs.

### `rule.2025.standard_deduction.line12e.v1`

**Recovery:** Use the required 2025 filing-status choice as the key into the 2025 standard-deduction parameter and publish the selected amount to Form 1040 line 12e. The table amounts are single 15,750; mfs 15,750; mfj 31,500; qss 31,500; hoh 23,625.

**Confidence:** probable.

**Could not interpret exactly:** Status abbreviations and lookup failure behavior are undefined. The output fact id says `standard_or_itemized_deduction`, while the rule can only select the standard-deduction table; the artifact does not say how an itemized deduction could enter this output.

### `rule.2025.total_income.line9.v1`

**Recovery:** Add Form 1040 line 1a wages and line 2b taxable interest and publish the sum as Form 1040 line 9 total income.

**Confidence:** certain.

**Could not interpret exactly:** “Total income” is limited by the expression to two inputs. Missing inputs carry block reasons but no block templates. No treatment of other income categories is encoded.

### `rule.2025.schedule1.line18.early_withdrawal_penalty.v1`

**Recovery:** Sum all available 1099-INT box 2 early-withdrawal penalties, round the total using the required rounding choice, and publish Schedule 1 line 18.

**Confidence:** probable.

**Could not interpret exactly:** Rounding modes and optional empty-collection behavior are undefined. A missing rounding choice is a declared blocker even when no penalties exist; the resulting behavior is unstated.

### `rule.2025.schedule1.line26.adjustments.v1`

**Recovery:** Copy Schedule 1 line 18 early-withdrawal penalty directly to Schedule 1 line 26 total adjustments to income.

**Confidence:** certain.

**Could not interpret exactly:** The label says “total adjustments,” but the expression contains only line 18. Missing line 18 has a block reason but no block template.

### `rule.2025.agi.line10.v1`

**Recovery:** Copy Schedule 1 line 26 adjustments to Form 1040 line 10 adjustments to income.

**Confidence:** certain.

**Could not interpret exactly:** Missing line 26 has a block reason but no block template. The special input role `"bridge"` has no schema-defined behavior distinct from an ordinary input; the copying behavior is recoverable only from the expression.

### `rule.2025.agi.line11a.v1`

**Recovery:** Subtract Form 1040 line 10 adjustments from line 9 total income. Publish the same adjusted gross income as line 11a and as a line 11b amount carried to page 2.

**Confidence:** certain.

**Could not interpret exactly:** The two-output expression has no explicit mapping of one expression result to each output; I infer both receive the same result because there is one expression and two outputs. Missing inputs carry block reasons but no block templates.

### `rule.2025.taxable_income.line15.v1`

**Recovery:** Subtract the line 12e deduction from adjusted gross income carried on line 11b, take the greater of that result and zero, and publish it as line 15 taxable income.

**Confidence:** certain.

**Could not interpret exactly:** Missing inputs carry block reasons but no block templates. The deduction fact id permits “standard or itemized,” but the only package rule producing it is the standard-deduction lookup.

### `rule.2025.regular_tax.line16.v1`

**Recovery:** Given taxable income, filing status, and the regular-tax parameter: if taxable income is strictly less than 100,000, choose the status-specific tax-table row containing the amount and return its `tax`; otherwise choose the status-specific worksheet row and compute taxable income times its rate minus its subtraction amount. Publish this as Form 1040 line 16 regular tax.

**Confidence:** probable for the branching formula; guessing for full below-threshold execution because most table rows are absent.

**Could not interpret exactly:** `table_row_value`, `table_row`, `param_path`, `let_row`, and `field` are not defined beyond being permitted arbitrary expressions. Row boundary semantics are absent. Missing-row, multiple-row, and unknown-status behavior are absent. The sub-100,000 tables are plainly incomplete for `mfj`, `mfs`, and `hoh`, contain no `qss`, and include large zero-tax spans for `single` without saying whether zero is intentional or a placeholder. No rounding stage is declared for a potentially fractional result. Required-input block reasons have no block templates.

### `rule.2025.total_tax.line24.v1`

**Recovery:** Copy line 16 regular tax directly to line 24 total tax.

**Confidence:** certain.

**Could not interpret exactly:** “Total tax” is limited to the one declared regular-tax input. Missing line 16 has a block reason but no block template.

### `rule.2025.total_payments.line33.v1`

**Recovery:** Copy line 25d total withholding directly to line 33 total payments.

**Confidence:** certain.

**Could not interpret exactly:** “Total payments” is limited to withholding. Missing line 25d has a block reason but no block template.

### `rule.2025.overpayment.line34.v1`

**Recovery:** Compute payments minus tax. Publish Form 1040 line 34 overpayment only when that difference is strictly greater than zero. No line-34 output is published when payments equal or fall below tax.

**Confidence:** probable.

**Could not interpret exactly:** I infer `publish_when` suppresses the output rather than merely annotating it; the schema permits the field but defines no execution semantics. Missing inputs have block reasons but no block templates.

### `rule.2025.amount_owed.line37.v1`

**Recovery:** Compute tax minus payments. Publish Form 1040 line 37 amount owed only when that difference is strictly greater than zero. No line-37 output is published when tax equals or falls below payments.

**Confidence:** probable.

**Could not interpret exactly:** I infer suppression behavior from `publish_when`, whose semantics are not defined. Missing inputs have block reasons but no block templates.

## Schema recovery

### `rule-artifact.v1.prototype-it1.schema.json`

**Recovery:** A rule artifact must identify its schema, citizen kind, rule id, semantic-looking version, label, US-federal scope, and one of four artifact kinds. Inputs can refer to a fact type plus cardinality, a specific fact id, or a parameter id. Outputs are derived facts and may carry a `publish_when` expression. The schema provides optional source, inputs, expression, outputs, rounding stage, block templates, and dependency declarations. It contains one special validation: a label matching `Form 1040 line 2b` requires an output with the line-2b taxable-interest fact id.

**Confidence:** certain about validation shape; guessing about execution semantics.

**Could not interpret exactly:** `$defs.expression` accepts virtually any JSON value and defines no operator vocabulary, arity, typing, evaluation order, table matching, numeric representation, or error behavior. `outputs` is not in the top-level `required` list despite its own `minItems`; therefore a rule can validate with no output. `source`, `inputs`, `expression`, `rounding_stage`, `block_templates`, and `declared_dependencies` are also optional. The schema does not connect an input `block_reason` to `block_templates`, enforce a blocker for every required input, ensure variables refer to declared inputs, ensure dependencies match references, or define how one expression maps to multiple outputs. The label-based line-2b condition is not anchored and relies on prose text rather than artifact identity or kind.

### `parameter-declaration.v1.prototype-it1.schema.json`

**Recovery:** A parameter declaration must identify its schema, citizen kind, parameter id, semantic-looking version, label, US-federal tax-year/family scope, and `values`; it may include an IRS or prototype-paper source citation.

**Confidence:** certain about validation shape.

**Could not interpret exactly:** `"values": {}` imposes no type or shape at all, so the schema does not describe the standard-deduction lookup or tax-table structures used by the rules. It does not validate decimal strings as numbers, row fields, status keys, boundary ordering, overlap, completeness, or consistency with a consuming rule. `source` is optional even though, when present, it has required fields.
