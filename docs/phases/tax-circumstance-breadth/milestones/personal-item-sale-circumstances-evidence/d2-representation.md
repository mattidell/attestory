# D2 — Representation Decisions and Track 0 Closure for Personal Item Sale Circumstances

## Context and Scope

- **Milestone**: `personal-item-sale-circumstances`
- **Primary Branch**: `milestone/personal-item-sale-circumstances-translation`
- **Charter**: D2 representation
- **Launch**: D2 launch
- **Stage 1 Action 0**: apply D1 review corrections to personal-item loss connected account
- **Stage 1 Initial Representation**: initial representation decisions
- **Owner Decision (2026-10-16)**: *Completeness only where Schedule 1 is used; income and tax do not depend on Form 1099-K*. Supersedes D1 Section 7.
- **Seat / Role**: Builder (Stage 1 Repair to Owner Decision & D1 Comparison; Stage 2 Probing)
- **Scope Boundary**: Repaired Stage 1 Decisions & Track 0 Tables; Stage 2 Probe Execution and Closure Gate.
- **Evidence Ceiling**: Static code, schema, and content reading. All claims cite verified repository `file:line` locations or 2025 IRS instructions (`2025 Instructions for Form 1040`, page 88, `i1040gi--2025.txt:6366-6376`). No unverified claims are asserted.

---

# Part 1 — Representation Decisions

This section resolves every question from D1 Section 10 and Charter Section 1, updated to incorporate the Owner Decision (2026-10-16) and D1 Review Finding 1. For each decision, the precedent or capability is cited by `file:line`, the displaced alternative is identified, and the consumer that would behave differently is named.

---

## 1. D1 Section 10 Questions

### 1.1 Entity Structure: Modeling Item and Sale
- **Decision**: Model circumstance answers and economic amounts directly under `StatementKey` (`payer`, `statement`, `tax-year`), without introducing independent `Item` or `Sale` entity types in the kernel fact graph.
- **Precedent / Capability**: `packages/tax/f1098_statement_recording.py:1-6, 370-384`, `packages/kernel/facts.py:fact_id_for`, and `packages/derivation/subject_dispatch.py:1-18`. In `packages/derivation/subject_dispatch.py:9-13`, subject dispatch joins collected fact types to the subject by agreeing values on shared key names using a single-hop join; types connected only through a third type or sharing no key names are unreachable. Scoping all Form 1099-K circumstance facts directly to the statement keys enables single-hop subject dispatch for every statement.
- **Alternative Displaced**: Introducing dedicated `Item` and `Sale` entity instances using `entity.v1` (`packages/schemas/kernel/published.json:24`) and `act-entity-introduced.v1` (`packages/schemas/kernel/published.json:7`), with multi-entity relationship links.
- **Consumer Behaving Differently**: `packages/derivation/subject_dispatch.py:1-18` (which would fail single-hop join without complex bridge facts) and `packages/tax/statements.py` (which would have to manage entity lifecycle and foreign keys rather than statement-scoped currency).

### 1.2 Schedule 1 Header Entry Space Representation
- **Decision**: Model the top-of-form entry space as a `form-field.v3` citizen (`tax.us.2025.schedule1.top-entry.form-field`) bound to published symbol `tax.us.2025.schedule1.top-entry`.
- **Precedent / Capability**: `packages/content/tax/2025/schedule1.line-7.form-field.json:1-48` (`schema: form-field.v3`). Visual entry spaces on IRS forms are represented as form fields for presentation projection (`packages/derivation/presentation_projection.py:2934-3165`). The 2025 Instructions for Form 1040 (`i1040gi--2025.txt:6366-6376`) describe this as a specific visual space: *"Enter 'Form 1099-K' and the amount in the entry space at the top of Schedule 1"*.
- **Alternative Displaced**: Modeling the entry space solely as an internal attachment itemization subtotal without a corresponding `form-field.v3` citizen.
- **Consumer Behaving Differently**: `packages/derivation/presentation_projection.py:2934-3165` (which requires a form-field citizen to project visual fields into `presentation["sections"]`) and downstream UI/PDF field renderers.

### 1.3 Schedule 1 Attachment Trigger and Completeness Answer
- **Decision**: A return that determines Schedule 1 attachment disposition must carry a Form 1099-K completeness answer in ordinary words (*"Did you receive any Form 1099-K for 2025?"*). Answering "No" asserts closure of `tax.us.2025.f1099k` at genesis horizon `h0` (`source-closure` = True), allowing `collect` over `source_set: "tax.us.2025.f1099k"` to publish an explicit closed-empty zero (`0.00`) for `tax.us.2025.schedule1.top-entry`. Succeed `rule.attachment.schedule-1.v2.json` to `v3` (`schema: attachment-rule.v4`) by adding `tax.us.2025.schedule1.top-entry` to `requirement.subtotals`. A return that never reaches the Schedule 1 attachment decision (such as a W-2-only return) is asked nothing.
- **Precedent / Capability**: `packages/content/tax/2025/rule.attachment.schedule-1.v2.json:166-188` (`schema: attachment-rule.v4`), `packages/derivation/runner.py:1870-1898`, and `packages/derivation/evaluator.py:361-377`.
  - In `runner.py:1871-1874`, if any symbol in `requirement["subtotals"]` is absent from `self.symbols`, the attachment blocks with `BLOCK_ABSENT`.
  - In `evaluator.py:368-376`, an empty source set produces `[]` (evaluating to zero) **only** if `source_set in env.closed_sets`; otherwise it raises `EvalBlocked(BLOCK_CLOSURE)`. Thus, "no new question" was false: an empty family requires a closure assertion.
  - Per the Owner Decision (2026-10-16), this completeness question binds only returns that determine Schedule 1. On a closed-empty 1099-K return, `tax.us.2025.schedule1.top-entry` evaluates to `0.00`, so `Decimal("0.00") > Decimal("0")` is False (`runner.py:1894`), and Schedule 1 attaches if and only if another subtotal (unemployment line 7 or student loan line 21) is > 0. A supported 1099-K loss with Box 1a > 0 evaluates to True, attaching Schedule 1.
- **Alternative Displaced**: Assuming an empty source set automatically zeroes without human closure authority (which `evaluator.py:373-374` explicitly rejects), or creating multiple uncoordinated attachment rules.
- **Consumer Behaving Differently**: `packages/derivation/runner.py:1870-1905` (`attempt_attachment`), `packages/derivation/evaluator.py:361-377`, and filing packet assembly.

### 1.4 Income and Tax Blocking Mechanism (Superseded per Owner Decision)
- **Decision**: Form 1040 income lines (line 8, line 9) and tax calculation lines (lines 16, 24) **do not depend on Form 1099-K**. An unsupported, unresolved, or excluded Form 1099-K statement does **not** block Form 1040 income or tax. Instead, it withholds the Schedule 1 result (the Schedule 1 attachment disposition blocks with the statement's named stop reason) and is displayed to the user as an unresolved condition via `tax.us.2025.form.f1099k.unresolved`. The saved explanation explicitly states: *"Because this statement is unresolved, the return's income does not yet account for this Form 1099-K statement."*
- **Authority / Supersession**: This supersedes D1 Section 7 per the Owner Decision (2026-10-16, `docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md`).
- **Precedent / Capability**: `packages/content/tax/2025/f1098.residence-interest-unresolved.form-field.json:1-42`, `packages/content/tax/2025/rule.form1040-line8.json:18-42`, `packages/content/tax/2025/rule.form1040-line9.v7.json:66-100`, and `packages/tax/f1098_statement_review.py:309-329`.
- **Alternative Displaced**: D1 Section 7's provisional choice to block Form 1040 lines 8 and 9, which would have forced core calculation graph dependencies onto returns that have unreviewed or unsupported 1099-K forms.
- **Consumer Behaving Differently**: Form 1040 income calculation engine and presentation review.

### 1.5 Circumstance Bundle Packaging
- **Decision**: Package all Form 1099-K circumstance questions, shipping arrangement inputs, and reconciliation inputs into a single unified bundle: `tax.us.2025.f1099k-circumstances.bundle.v1.json` (`schema: bundle.v2`).
- **Precedent / Capability**: `packages/content/tax/2025/f1098-circumstances.bundle.json:1-40` (`schema: bundle.v2`), `packages/tax/loader.py:220-250`.
- **Alternative Displaced**: Splitting reconciliation facts from sale circumstance facts into separate bundles (`f1099k-reconciliation.bundle.v1` and `f1099k-sale-circumstances.bundle.v1`).
- **Consumer Behaving Differently**: `packages/tax/loader.py` and ActLog bundle adoption records (`act-bundle-adoption.v2`).

---

## 2. Charter Section 1 Requirements

### 2.1 Statement Vocabulary
- **Source Family**: `tax.us.2025.f1099k` (`schema: source-family.v1`, `version: v1`).
  - Precedent: `packages/content/tax/2025/family.f1098.json:1-17`.
  - Canonical Member Predicate: `tax.us.2025.f1099k.box1a-gross-amount`.
  - Authorized Subtotal: `tax.us.2025.schedule1.top-entry`.
  - Closure Claim: The family closure claim authorizes one statement's Box 1a or a closed-empty zero; it does not authorize a multi-payer sum.
- **Source Closure Mapping**: `tax.us.2025.closure-mapping.f1099k` (`schema: source-closure-mapping.v2`, `version: v1`).
  - Precedent: `packages/content/tax/2025/closure-mapping.f1098.json:1-23`.
  - Closure Fact Type: `tax.us.2025.f1099k.source-closure`.
  - Closure Horizon Key: `"family-horizon"`.
  - Admission Condition: `"current-literal-true"`.
- **Fact Types**:
  - `tax.us.2025.f1099k.box1a-gross-amount`: `schema: fact-type.v2`, nature: `determinable` (per `fact-type.v2.schema.json` and probe line 165), identity keys: `payer` (string), `statement` (string), `tax-year` (integer, 2025).
  - `tax.us.2025.f1099k.box4-federal-withholding`: `schema: fact-type.v2`, nature: `determinable` (probe line 175), identity keys: `payer`, `statement`, `tax-year`.
  - `tax.us.2025.f1099k.source-closure`: `schema: fact-type.v2`, nature: `determinable` (probe line 186), identity key: `family-horizon`, domain: boolean.
  - *Completeness Fact Displaced*: In `packages/derivation/source_authority.py:144-165`, closure admission strictly requires `closure_fact_type` (`tax.us.2025.f1099k.source-closure`) keyed on `family-horizon` with boolean `True`. An unkeyed `yes`/`no` fact cannot be admitted as family closure authority. The unread fact `tax.us.2025.f1099k-scope.no-form1099k-statement` and its cross-check sentence are deleted per review Finding 3.
- **Exact Schema Versions Verified from `packages/schemas/`**:
  - `packages/schemas/kernel/published.json`: `fact-type.v2.schema.json` (line 27), `fact-type.v3.schema.json` (line 28), `bundle.v2.schema.json` (line 20), `family-horizon.v1.schema.json` (line 29), `act-assertion.v2.schema.json` (line 3), `act-finding-retracted.v1.schema.json` (line 11).
  - `packages/schemas/derivation/published.json`: `source-family.v1.schema.json` (line 84), `source-family.v2.schema.json` (line 85), `source-closure-mapping.v2.schema.json` (line 83), `rule-artifact.v14.schema.json` (line 72), `artifact-package.v36.schema.json` (line 34), `release-registry.v1.schema.json` (line 66), `parameter-declaration.v1.schema.json` (line 65).
  - `packages/schemas/tax/published.json`: `form-field.v3.schema.json` (line 13), `attachment-rule.v4.schema.json` (line 7).

### 2.2 The Person's Answers and Unanswered / Withdrawn Representation
- **Circumstance Fact Types** (all `schema: fact-type.v2`, nature: `determinable`, identity keys: `payer`, `statement`, `tax-year`):
  - `tax.us.2025.f1099k.covers-only-single-item` (Q1: `yes`, `no`, `cannot-tell`, `not-asked`)
  - `tax.us.2025.f1099k.acquired-by-purchase` (Q3: `yes`, `no`, `cannot-tell`, `not-asked`)
  - `tax.us.2025.f1099k.primary-purpose-at-acquisition` (Q4: `personal-use`, `investment-or-profit`, `resale-or-inventory`, `cannot-tell`, `not-asked`)
  - `tax.us.2025.f1099k.exclusive-personal-use` (Q5: `yes`, `no`, `cannot-tell`, `not-asked`)
  - `tax.us.2025.f1099k.digital-asset-involvement` (Q7: `no`, `yes`, `cannot-tell`, `not-asked`)
  - `tax.us.2025.f1099k.agreed-item-price` (Q8: decimal amount, no default; optional_default parameter `tax.us.2025.parameter.f1099k-not-asked-default`)
  - `tax.us.2025.f1099k.shipping-arrangement` (Q8-shipping: enum `platform-pass-through`, `seller-received-shipping`, `none`, `cannot-tell`, `not-asked`)
  - `tax.us.2025.f1099k.platform-fees` (Q9-fees: decimal amount, no default; optional_default parameter)
  - `tax.us.2025.f1099k.seller-paid-shipping` (Q9-seller-shipping: decimal amount, no default; optional_default parameter)
  - `tax.us.2025.f1099k.sales-tax-collected-by-platform` (Q10: decimal amount, no default; optional_default parameter)
  - `tax.us.2025.f1099k.refund-amount` (Q10-refund: decimal amount, no default; optional_default parameter)
  - `tax.us.2025.f1099k.buyer-paid-shipping` (Q11: decimal amount, no default; optional_default parameter)
  - `tax.us.2025.f1099k.cost-basis-known` (Q12 gate: `yes`, `cannot-tell`, `not-asked`)
  - `tax.us.2025.f1099k.purchase-cost` (Q12 amount: decimal amount, no default; optional_default parameter)
  - `tax.us.2025.f1099k.lasting-improvements-or-adjustments` (Q13: `no`, `yes`, `cannot-tell`, `not-asked`)
  - *Note on Q2 Item Description*: Dropped per review Finding 4 until a model records it.
- **Unanswered / Withdrawn Representation and Absence Mechanics (Finding 1)**:
  - **No numeric default to zero**: Circumstance amounts do NOT bind to `tax.us.2025.parameter.default-zero`. An omitted or retracted amount must never default to `$0.00` to manufacture a favorable loss comparison.
  - **Engine Absence Representation**: In `packages/derivation/subject_dispatch.py:696-700, 761-771`, an absent finding without `optional_default` causes `SubjectBlocked(DEPENDENCY_ABSENT)` preventing rule evaluation. In `packages/derivation/evaluator.py:334-335`, missing symbol references raise `EvalBlocked(BLOCK_ABSENT)`; no presence-check operator exists. The engine expresses "this numeric fact has no current value" without a favorable numeric default by declaring `optional_default` bound to a structural `"not-asked"` sentinel parameter (`tax.us.2025.parameter.f1099k-not-asked-default`). Each amount fact declares `value_schema` with `oneOf`: `[{"type": "number", "minimum": 0}, {"type": "string", "enum": ["cannot-tell", "not-asked"]}]`.
  - When an amount or categorical answer is missing or retracted by `act-finding-retracted.v1`, runner subject dispatch binds `"not-asked"`.
  - In `tax.us.2025.rule.f1099k-statement-loss-reason`, each input is checked against `"cannot-tell"` and `"not-asked"` before arithmetic:
    - Q1: `multi-sale-statement-unsupported` (if "no"), `cannot-tell-sale-scope` ("It is not known whether the statement covers only a single personal item sale."), `single-sale-unanswered` ("The question regarding single item sale scope has no current answer.")
    - Q3: `non-purchase-acquisition-unsupported` (if "no"), `cannot-tell-acquisition` ("It is not known whether the item was acquired by purchase."), `acquisition-type-unanswered` ("The question regarding acquisition by purchase has no current answer.")
    - Q4: `resale-inventory-excluded`, `investment-purpose-excluded`, `cannot-tell-purpose` ("It is not known whether the item was acquired for personal use."), `purpose-unanswered` ("The question regarding primary purpose at acquisition has no current answer.")
    - Q5: `prior-depreciable-use-excluded` (if "no"), `cannot-tell-use` ("It is not known whether the item was used exclusively for personal purposes."), `personal-use-unconfirmed` ("The question regarding exclusive personal use has no current answer.")
    - Q7: `digital-asset-excluded` (if "yes"), `cannot-tell-asset-type` ("It is not known whether the transaction involved digital assets or virtual currency."), `asset-type-unanswered` ("The question regarding digital assets has no current answer.")
    - Q8 price: `buyer-payment-unknown` ("The agreed item price is unknown."), `agreed-price-unanswered` ("The question regarding agreed item price has no current answer.")
    - Q8 shipping arrangement: `shipping-arrangement-unknown` ("The shipping arrangement is unknown."), `shipping-arrangement-unanswered` ("The question regarding shipping arrangement has no current answer.")
    - Q9 fees: `platform-fees-unknown` ("The platform selling fees amount is unknown."), `platform-fees-unanswered` ("The question regarding platform selling fees has no current answer.")
    - Q9 seller shipping: `seller-shipping-unknown` ("The seller-paid shipping amount is unknown."), `seller-shipping-unanswered` ("The question regarding seller-paid shipping has no current answer.")
    - Q10 tax: `platform-tax-unknown` ("The platform sales tax amount is unknown."), `platform-tax-unanswered` ("The question regarding platform sales tax has no current answer.")
    - Q10 refund: `refund-status-unknown` ("The refund amount is unknown."), `refund-status-unanswered` ("The question regarding refunds given back has no current answer.")
    - Q11 buyer shipping: `buyer-shipping-unknown` ("The buyer-paid shipping amount is unknown."), `buyer-shipping-unanswered` ("The question regarding buyer-paid shipping has no current answer.")
    - Q12 gate: `cost-basis-unknown` ("The original purchase cost of the item is unknown."), `cost-basis-unanswered` ("The question regarding cost basis has no current answer.")
    - Q12 cost: `cost-basis-unknown`, `cost-basis-unanswered`
    - Q13 improvements: `basis-adjustment-unsupported` (if "yes"), `cannot-tell-improvements` ("It is not known whether lasting improvements or other basis adjustments were made to the item."), `improvements-unanswered` ("The question regarding lasting improvements has no current answer.")
  - **Invariance**: `supported-loss` is published ONLY when every amount has an affirmative current numeric value. An omitted or retracted amount leaves the question unanswered (`"not-asked"`), stopping the route with its named stop and never publishing `supported-loss` or entering Box 1a.

### 2.3 Absence, Closure, and Closed-Empty Zeroes
- **"No New Question" is False**:
  - Under `packages/derivation/evaluator.py:361-377`, an empty source set raises `EvalBlocked(BLOCK_CLOSURE)` unless that source set has been explicitly asserted closed by human authority. A machine cannot fabricate closure from silence.
  - Per the Owner Decision (2026-10-16), any return that reaches the Schedule 1 attachment decision must carry a Form 1099-K completeness answer (*"Did you receive any Form 1099-K for 2025?"*).
  - Answering "No" asserts closure of `tax.us.2025.f1099k` at genesis horizon `h0` (`tax.us.2025.f1099k.source-closure` = True).
  - `packages/derivation/source_authority.py:100-160` resolves closure admissions: mapping pins match family, and finding matches current horizon `h0`. The family enters `env.closed_sets`.
  - Evaluator `collect` (`evaluator.py:361-377`) sees `rows` is empty, verifies `source_set in env.closed_sets`, and returns `[]`.
  - Evaluator `add` (`evaluator.py:423-424`) produces `0.00`. `rule.schedule1-top-entry` publishes `0.00`.
- **How Existing Schedule 1 Subtotals Obtain Closure Today**:
  - *Unemployment Box 1 Subtotal* (`tax.us.2025.unemployment.box1-subtotal`): Authorized by `family.f1099g-1.json:1-17` (`source-family.v1`). Evaluated by `rule.f1099g-1-subtotal.json:35-51` via `collect` over `source_set: "tax.us.2025.f1099g.1"`. In `tests/test_form1099g_box1_schedule1_line7.py:285-300` and `tests/test_schedule1_line26_track4.py:128-145`, returns asserting closed-empty unemployment assert `tax.us.2025.f1099g.1.source-closure` on `family-horizon: g0` with `True`. If unclosed, `evaluator.py:374` raises `EvalBlocked(BLOCK_CLOSURE, ["tax.us.2025.f1099g.1"])`.
  - *Student Loan Interest Line 21 Deduction* (`tax.us.2025.schedule1.line21-sli-deduction`): Authorized by `family.f1098e-1.json:1-17` (`source-family.v1`). Evaluated by `rule.sli-worksheet-line1-subtotal.json:35-51` via `collect` over `source_set: "tax.us.2025.f1098e.1"`. In `tests/test_schedule1_line26_track4.py:120-125`, closure is asserted via `tax.us.2025.f1098e.1.source-closure` on `family-horizon: h0` with `True`.
- **What a W-2-Only Return's Schedule 1 Disposition is Now**:
  - Under `package.core-calculations`, a W-2-only return evaluates `tax.us.2025.schedule1.disposition` to `blocked` (`DEPENDENCY_ABSENT`) both before and after this design because the student loan adjustment subtotal is absent. The filer is asked nothing about Form 1099-K, and income and tax calculations are completely unaffected.
  - *Presentation Row Behavior and Engine Constraint (Finding 6)*: In `packages/derivation/runner.py:1184-1198` and `packages/derivation/presentation_projection.py:500-503`, field disposition is `guard_inapplicable` only when rule `when` evaluates to `False`. On a W-2 return with no 1099-K activity, `require_closed` raises `EvalBlocked(BLOCK_CLOSURE)`. Under `runner.py:1184-1198` and `presentation_projection.py`, a rule blocked on evaluation projects field disposition `blocked` (rendering `"Form 1099-K loss entry cannot be computed."`). The engine cannot make the W-2 top-entry row `guard_inapplicable` without changing neighbors: removing or bypassing `require_closed` would break unclosed Schedule 1 returns (Path 3), which must block attachment. The Form 1099-K unresolved condition row evaluates to `guard_inapplicable` ("No open condition: statements resolved or no statement received."), requiring no entry or action from the person.
- **Late-Member Invalidation**:
  - When a Form 1099-K statement is subsequently asserted, `act-member-transition.v2` mints horizon `h1` (`packages/derivation/source_authority.py:65-73`).
  - Current horizon becomes `h1`. The prior closure finding at `h0` no longer matches (`h0 != h1` in `source_authority.py:146-156`).
  - `tax.us.2025.f1099k` drops out of `env.closed_sets`. Any subsequent attempt to evaluate `tax.us.2025.rule.schedule1-top-entry` raises `EvalBlocked(BLOCK_CLOSURE)` until a new closure assertion at `h1` is committed.

### 2.4 Per-Statement Determination and Rule Operations
- **Single Economic Comparison (D1 Review Finding 1, Corrected)**:
  - **Amount Realized**:
    $$\text{Amount Realized} = \text{Agreed Item Price} + \text{Buyer Shipping Received} - \text{Refunds Given Back}$$
    - Where `Buyer Shipping Received = buyer-paid-shipping` if `shipping-arrangement == "seller-received-shipping"`, else `$0.00`.
    - Where `Refunds Given Back = refund-amount`.
  - **Selling Expenses**:
    $$\text{Selling Expenses} = \text{Platform Fees} + \text{Seller-Paid Shipping Deducted}$$
    - Where `Seller-Paid Shipping Deducted = seller-paid-shipping` if `shipping-arrangement` is `"seller-received-shipping"` (the shipping label cost) or `"none"` (seller-paid shipping when buyer was not charged), else `$0.00`.
    - If `shipping-arrangement == "platform-pass-through"`, the platform retained the shipping funds to issue the label; seller incurred no label expense and deducts `$0.00` shipping.
  - **Net Amount (Net Proceeds)**:
    $$\text{Net Amount} = \text{Amount Realized} - \text{Selling Expenses}$$
  - **Adjusted Basis**:
    $$\text{Adjusted Basis} = \text{Purchase Cost (Q12)} \quad \text{only when Q13 is 'no'}$$
  - **Loss Condition**:
    $$\text{Loss Condition} = (\text{Net Amount} < \text{Adjusted Basis}) \quad \text{AND} \quad (\text{Q13 lasting-improvements} == \text{'no'})$$
    - If `Net Amount > Adjusted Basis`: blocks with `unsupported-gain`.
    - If `Net Amount == Adjusted Basis`: blocks with `break-even-sale`.
    - If Q13 is 'yes': blocks with `basis-adjustment-unsupported` ("Lasting improvements or other basis adjustments were made to the item.").
    - If Q13 is 'cannot-tell': blocks with `cannot-tell-improvements` ("It is not known whether lasting improvements or other basis adjustments were made to the item.").
    - If Q13 is 'not-asked': blocks with `improvements-unanswered` ("The question regarding lasting improvements has no current answer.").
- **Box 1a Reconciliation Check**:
  $$\text{Expected Box 1a} = \text{Agreed Item Price (Q8)} + \text{Platform Sales Tax (Q10)} + \text{Buyer Shipping (Q11)}$$
  - If Box 1a != Expected Box 1a: blocks with `unexplained-reconciliation-discrepancy`.
- **Box 4 Backup Withholding Check**:
  - If Box 4 > `$0.00`: blocks with `backup-withholding-unsupported`.
- **Circumstance Stops**:
  - Q1 != "yes": `multi-sale-statement-unsupported` (if "no"), `cannot-tell-sale-scope` (if "cannot-tell"), `single-sale-unanswered` (if "not-asked").
  - Q3 != "yes": `non-purchase-acquisition-unsupported` (if "no"), `cannot-tell-acquisition` (if "cannot-tell"), `acquisition-type-unanswered` (if "not-asked").
  - Q4 != "personal-use": `investment-purpose-excluded` (if "investment-or-profit"), `resale-inventory-excluded` (if "resale-or-inventory"), `cannot-tell-purpose` (if "cannot-tell"), `purpose-unanswered` (if "not-asked").
  - Q5 != "yes": `prior-depreciable-use-excluded` (if "no"), `cannot-tell-use` (if "cannot-tell"), `personal-use-unconfirmed` (if "not-asked").
  - Q7 != "no": `digital-asset-excluded` (if "yes"), `cannot-tell-asset-type` (if "cannot-tell"), `asset-type-unanswered` (if "not-asked").
  - Q8 agreed price: `buyer-payment-unknown` (if "cannot-tell"), `agreed-price-unanswered` (if "not-asked").
  - Q8 shipping arrangement: `shipping-arrangement-unknown` (if "cannot-tell"), `shipping-arrangement-unanswered` (if "not-asked").
  - Q9 platform fees: `platform-fees-unknown` (if "cannot-tell"), `platform-fees-unanswered` (if "not-asked").
  - Q9 seller shipping: `seller-shipping-unknown` (if "cannot-tell"), `seller-shipping-unanswered` (if "not-asked").
  - Q10 platform tax: `platform-tax-unknown` (if "cannot-tell"), `platform-tax-unanswered` (if "not-asked").
  - Q10 refund: `refund-status-unknown` (if "cannot-tell"), `refund-status-unanswered` (if "not-asked").
  - Q11 buyer shipping: `buyer-shipping-unknown` (if "cannot-tell"), `buyer-shipping-unanswered` (if "not-asked").
  - Q12 cost basis: `cost-basis-unknown` (if gate or cost "cannot-tell"), `cost-basis-unanswered` (if gate or cost "not-asked").
- **Rule Operations Confirmed in Current Schemas and `packages/derivation/evaluator.py`**:
  - `ref`: `packages/derivation/evaluator.py:332-360`
  - `category_literal`: `packages/derivation/evaluator.py:487-488`
  - `categorical_compare`: `packages/derivation/evaluator.py:480-485`
  - `compare`: `packages/derivation/evaluator.py:438-442`
  - `add`: `packages/derivation/evaluator.py:423-424`
  - `subtract`: `packages/derivation/evaluator.py:426-427`
  - `choose`: `packages/derivation/evaluator.py:455-457`
  - `all`: `packages/derivation/evaluator.py:446-447`
  - `any`: `packages/derivation/evaluator.py:449-450`
  - `not`: `packages/derivation/evaluator.py:452-453`
  - `block`: `packages/derivation/evaluator.py:403-404`
  - `require_closed`: `packages/derivation/evaluator.py:473-478`
  - `collect`: `packages/derivation/evaluator.py:361-377`
  - Missing operations: **None**.

### 2.5 The Return-Level Result and Categorical Reason Projection
- **Representation Choice (Foreman Decision / R1 & R2)**:
  Replace the numeric per-statement sum with the existing categorical pattern projected by the presentation reader (`packages/derivation/presentation_projection.py:157-377`).
  - **Per-statement categorical reason rule**: `tax.us.2025.rule.f1099k-statement-loss-reason` (`schema: rule-artifact.v14`, `version: v1`).
    - Evaluates statement-level circumstances and publishes the categorical reason `tax.us.2025.f1099k.statement-loss-reason`.
    - Produces `"supported-loss"` if all criteria are satisfied (single sale, purchased, personal use, non-digital, Box 1a reconciled, Net Amount < Adjusted Basis, improvements == 'no', Box 4 == $0).
    - Produces a specific categorical stop string if any criteria fail (e.g. `"unsupported-gain"`, `"break-even-sale"`, `"investment-purpose-excluded"`, `"resale-inventory-excluded"`, `"prior-depreciable-use-excluded"`, `"digital-asset-excluded"`, `"multi-sale-statement-unsupported"`, `"non-purchase-acquisition-unsupported"`, `"basis-adjustment-unsupported"`, `"cannot-tell-improvements"`, `"backup-withholding-unsupported"`, `"cost-basis-unknown"`, `"cost-basis-unanswered"`, `"platform-fees-unanswered"`, `"agreed-price-unanswered"`, `"unexplained-reconciliation-discrepancy"`, etc.).
    - Precedent: `packages/content/tax/2025/rule.f1098-residence-interest-reason.v2.json:1-85`. Descriptions for each reason are declared in `oneOf` under `f1099k.bundle.json:1-95`.
  - **Schedule 1 top-entry rule**: `tax.us.2025.rule.schedule1-top-entry` (`schema: rule-artifact.v14`, `version: v1`).
    - Precedent: `packages/content/tax/2025/rule.f1098-line8a.v2.json:35-70`.
    - Publishes: `tax.us.2025.schedule1.top-entry`.
    - Guard (`when`): Checks `{"op": "require_closed", "source_set": "tax.us.2025.f1099k"}`. Enforces the one Form 1099-K per return limit (R2): if `count > 1`, blocks with `MULTIPLE_F1099K_OUT_OF_SCOPE` (token: `multiple-f1099k-out-of-scope`).
    - Value (`value`): If `count == 0` (closed-empty family), evaluates to `0` (the closed-empty zero). If `count == 1`, evaluates `collect_categorical_all_equal("statement-loss-reason", "supported-loss")`: if True, publishes that statement's Box 1a; if False (any named stop), blocks with `DEPENDENCY_ABSENT`.
  - **Unresolved selection rule**: `tax.us.2025.rule.f1099k-unresolved` (`schema: rule-artifact.v14`, `version: v1`).
    - Precedent: `packages/content/tax/2025/rule.f1098-residence-interest-unresolved.v2.json:1-36`.
    - Mode: `exclusive_presence`, with `reads_subject_results: [{"symbol": "tax.us.2025.f1099k.statement-loss-reason", ...}]`. If `count > 1`, blocks with `MULTIPLE_F1099K_OUT_OF_SCOPE` (token: `multiple-f1099k-out-of-scope`).
    - Reader: Projected by `packages/derivation/presentation_projection.py:157-377`, which reads the categorical reason and renders its plain-language description from the bundle schema `oneOf`.
  - **Published Loss Explanation (Finding 6)**:
    - Supported-loss description: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."*
    - Modeled on the publishing path: in `tax.us.2025.schedule1.top-entry.form-field`, `dispositions.published_value.explain` declares this sentence, projected when `tax.us.2025.schedule1.top-entry` is published.

### 2.6 Relationship to Income and Tax (Owner Decision 2026-10-16)
- **Income and Tax Invariance**:
  - Form 1040 line 8 (`tax.us.2025.income.additional-income`) equals Schedule 1 line 10 (`packages/content/tax/2025/rule.form1040-line8.json:18-42`).
  - Schedule 1 top entry is above Part I and does not feed Part I line 10 (`packages/content/tax/2025/rule.schedule1-line10.json:2-16`).
  - Form 1040 line 9 (`tax.us.2025.income.total-income`) sums income sources (`packages/content/tax/2025/rule.form1040-line9.v7.json:66-100`).
  - **Income and tax do not depend on Form 1099-K**.
- **Attachment and Unresolved Presentation Withholding**:
  - If any Form 1099-K statement is unsupported, unresolved, or excluded:
    1. `tax.us.2025.schedule1.top-entry` is not published.
    2. `rule.attachment.schedule-1.v3` detects missing subtotal `tax.us.2025.schedule1.top-entry` and blocks attachment with `BLOCK_ABSENT` (`packages/derivation/runner.py:1871-1874`).
    3. The unresolved condition is presented on `tax.us.2025.form.f1099k.unresolved`.
    4. The saved explanation states: *"Because this statement is unresolved, the return's income does not yet account for this Form 1099-K statement."*
  - **Supersession**: This supersedes D1 Section 7 per the Owner Decision (2026-10-16).

### 2.7 Schedule 1 Form Field and Attachment Successor
- **Header Form Field**: `tax.us.2025.schedule1.top-entry.form-field` (`schema: form-field.v3`, `version: v1`). Line `"sch1-top"`, binds symbol `tax.us.2025.schedule1.top-entry`.
- **Attachment Rule Successor**: `tax.us.2025.rule.attachment.schedule-1` (`schema: attachment-rule.v4`, `version: v3`).
  - Subtotals: `["tax.us.2025.unemployment.box1-subtotal", "tax.us.2025.schedule1.line21-sli-deduction", "tax.us.2025.schedule1.top-entry"]`.

### 2.8 Recording, Correction, and Withdrawal
- Transfers from `packages/tax/f1098_statement_recording.py`: durable evidence submission (`evidence-submitted.v1`), assertions (`act-assertion.v2`), retractions (`act-finding-retracted.v1`).
- Statement-scoped currency: Form 1099-K statement individuated by `StatementKey`. Returns with more than one statement reach the explicit named stop `MULTIPLE_F1099K_OUT_OF_SCOPE` (`multiple-f1099k-out-of-scope`).
- Withdrawal semantics: retracting an answer leaves the question unanswered, binding `"not-asked"` via parameter `optional_default` and triggering an explicit named stop.

### 2.9 The Saved Explanation
- Function: `review_f1099k_statement_with_saved_presentation` (precedent: `packages/tax/f1098_statement_review.py:278-330`).
- Plain-language explanation for supported loss (Outcome 1) shows statement details, math comparison, and Schedule 1 entry amount.
- For unsupported / unresolved / excluded statements (Outcomes 2–6): names the stop reason, and includes the required owner-specified sentence:
  > *"Because this statement is unresolved, the return's income does not yet account for this Form 1099-K statement."*

### 2.10 Citizens and Versions
- All citizen IDs, schemas, and versions:
  1. `tax.us.2025.f1099k` (`schema: source-family.v1`, `version: v1`)
  2. `tax.us.2025.closure-mapping.f1099k` (`schema: source-closure-mapping.v2`, `version: v1`)
  3. `tax.us.2025.f1099k.box1a-gross-amount` (`schema: fact-type.v2`, `version: v1`)
  4. `tax.us.2025.f1099k.box4-federal-withholding` (`schema: fact-type.v2`, `version: v1`)
  5. `tax.us.2025.f1099k.source-closure` (`schema: fact-type.v2`, `version: v1`)
  6. `tax.us.2025.f1099k-circumstances.bundle.v1` (`schema: bundle.v2`, `version: v1`)
  7. `tax.us.2025.f1099k.statement-loss-reason` (`schema: fact-type.v2`, `version: v1` with `oneOf` categorical reason descriptions in `f1099k.bundle.json`)
  8. Circumstance fact types Q1, Q3–Q5, Q7–Q13 (each `schema: fact-type.v2`, `version: v1`)
  9. Default parameter for `"not-asked"` (`schema: parameter-declaration.v1`, `version: v1`)
  10. `tax.us.2025.rule.f1099k-statement-loss-reason` (`schema: rule-artifact.v14`, `version: v1`)
  11. `tax.us.2025.rule.schedule1-top-entry` (`schema: rule-artifact.v14`, `version: v1`)
  12. `tax.us.2025.rule.f1099k-unresolved` (`schema: rule-artifact.v14`, `version: v1`)
  13. `tax.us.2025.rule.attachment.schedule-1.v3` (successor to `v2`, `schema: attachment-rule.v4`, `version: v3`)
  14. `tax.us.2025.schedule1.top-entry.form-field` (`schema: form-field.v3`, `version: v1`)
  15. `tax.us.2025.form.f1099k.unresolved.form-field` (`schema: form-field.v3`, `version: v1`)
- Package successor: `package.core-calculations.v46.json` (`schema: artifact-package.v36`, `version: v46`).
- Release registry: `demo.release.sli-worksheet-integration.2025` `v44` (`schema: release-registry.v1`), adopting package `v46`, as the probe builds it.
- No new schema or ADR is needed.

---

# Part 2 — Track 0 Gate Artifacts

---

### Artifact 1: Authority-Lifecycle Table

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" Artifact 1. Covers every contributed fact, reused declaration, aggregate declaration, and absence authority.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `tax.us.2025.f1099k.box1a-gross-amount` | Reported gross payment transactions, Box 1a | One statement (`payer`, `statement`, `tax-year`) | Furnished Form 1099-K | Later assertion on the same statement keys (issuer correction); retraction of the statement |
| `tax.us.2025.f1099k.box4-federal-withholding` | Reported federal income tax withheld, Box 4 | Same statement keys | Furnished Form 1099-K | Later assertion on the same keys |
| `tax.us.2025.f1099k.covers-only-single-item` (Q1) | Person's confirmation that statement covers only this one item | Same statement keys | Person's affirmative answer | Later assertion (correction); retraction (leaves question unanswered / `not-asked`, stopping route with `single-sale-unanswered`) |
| `tax.us.2025.f1099k.acquired-by-purchase` (Q3) | Confirmation item was bought by the person | Same statement keys | Person's affirmative answer | Later assertion; retraction (stops with `acquisition-type-unanswered`) |
| `tax.us.2025.f1099k.primary-purpose-at-acquisition` (Q4) | Primary purpose when item was acquired | Same statement keys | Person's affirmative answer | Later assertion; retraction (stops with `purpose-unanswered`) |
| `tax.us.2025.f1099k.exclusive-personal-use` (Q5) | Sole personal use (no business, rental, or mixed use) | Same statement keys | Person's affirmative answer | Later assertion; retraction (stops with `personal-use-unconfirmed`) |
| `tax.us.2025.f1099k.digital-asset-involvement` (Q7) | Confirmation item is not a digital asset/NFT | Same statement keys | Person's affirmative answer | Later assertion; retraction (stops with `asset-type-unanswered`) |
| `tax.us.2025.f1099k.agreed-item-price` (Q8) | Agreed selling price of the personal item | Same statement keys | Person's entered amount | Later assertion; retraction (stops with `agreed-price-unanswered`; never defaults to zero) |
| `tax.us.2025.f1099k.sales-tax-collected-by-platform` (Q10) | Platform-collected sales tax included in Box 1a | Same statement keys | Person's entered amount | Later assertion; retraction (stops with `platform-tax-unanswered`; never defaults to zero) |
| `tax.us.2025.f1099k.buyer-paid-shipping` (Q11) | Buyer-paid shipping costs included in Box 1a | Same statement keys | Person's entered amount | Later assertion; retraction (stops with `buyer-shipping-unanswered`; never defaults to zero) |
| `tax.us.2025.f1099k.refund-amount` (Q10-refund) | Refunds given back to the buyer | Same statement keys | Person's entered amount | Later assertion; retraction (stops with `refund-status-unanswered`; never defaults to zero) |
| `tax.us.2025.f1099k.shipping-arrangement` (Q8-shipping) | How shipping was handled (pass-through, seller-received, none) | Same statement keys | Person's affirmative answer | Later assertion; retraction (stops with `shipping-arrangement-unanswered`) |
| `tax.us.2025.f1099k.platform-fees` (Q9-fees) | Marketplace fees deducted by the platform | Same statement keys | Person's entered amount | Later assertion; retraction (stops with `platform-fees-unanswered`; never defaults to zero) |
| `tax.us.2025.f1099k.seller-paid-shipping` (Q9-seller-shipping) | Out-of-pocket shipping paid by seller (label or free-shipping cost) | Same statement keys | Person's entered amount | Later assertion; retraction (stops with `seller-shipping-unanswered`; never defaults to zero) |
| `tax.us.2025.f1099k.cost-basis-known` (Q12 gate) | Person's confirmation whether original purchase cost is known | Same statement keys | Person's affirmative answer | Later assertion; retraction (stops with `cost-basis-unanswered`) |
| `tax.us.2025.f1099k.purchase-cost` (Q12) | Original purchase cost paid for the item | Same statement keys | Person's entered amount | Later assertion; retraction (stops with `cost-basis-unanswered`; never defaults to zero) |
| `tax.us.2025.f1099k.lasting-improvements-or-adjustments` (Q13) | Confirmation no lasting improvements were made | Same statement keys | Person's affirmative answer | Later assertion; retraction (stops with `improvements-unanswered`) |
| `tax.us.2025.f1099k.source-closure` | Declaration that the Form 1099-K family is closed (authorizes one statement's Box 1a or closed-empty zero; does not authorize multi-payer sum) | Family horizon (`family-horizon`) | Taxpayer's closing assertion | Later assertion on a successor horizon (`h1`, `h2`) |
| `tax.us.2025.f1099k.statement-loss-reason` | Per-statement categorical circumstance reason (`"supported-loss"` or named stop) | Same statement keys | Box 1a, Box 4, circumstance answers Q1–Q13, single comparison | Invalidation or correction of any statement input; issuer statement replacement |
| `tax.us.2025.schedule1.top-entry` | Single statement Box 1a for supported loss, closed-empty 0.00, or blocked | Return (`tax-year`) | Categorical reason over closed `tax.us.2025.f1099k` family (1 statement max) | Any statement transitioning from supported to unsupported; count > 1 (`multiple-f1099k-out-of-scope`); family horizon change; unclosed family |
| `tax.us.2025.rule.attachment.schedule-1.v3` | Requirement disposition for Schedule 1 attachment | Return (`tax-year`) | Unemployment subtotal, SLI subtotal, Schedule 1 top entry | Invalidation of any requirement subtotal |

---

### Artifact 2: Empty/Nonempty Authority Matrix

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" Artifact 2. Exercises all required states for the `tax.us.2025.f1099k` source family under the Owner Decision (2026-10-16).

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| **Closed empty** | Completeness answer: "No Form 1099-K received". Family closed at `h0` (`source-closure` = True) | Inapplicable | `tax.us.2025.schedule1.top-entry` publishes explicit `0.00` via closed-empty `collect`. Top entry form field renders `0`. Schedule 1 attachment rule evaluates `0.00 > 0` as False. | Schedule 1 attachment evaluates without blocking (`BLOCK_ABSENT` avoided). Unemployment line 7 and student loan line 21 determine attachment as today. Income lines 8/9 unaffected. Return complete. |
| **Closed empty (unclosed)** | Completeness answer missing / unanswered. Closure finding missing. | Any | Blocked: `tax.us.2025.rule.schedule1-top-entry` raises `EvalBlocked(BLOCK_CLOSURE, ["tax.us.2025.f1099k"])`. Top entry symbol absent. | Schedule 1 attachment blocks with `BLOCK_ABSENT` on missing `tax.us.2025.schedule1.top-entry`. **Income lines 8/9 unaffected**. Return filing withheld at Schedule 1 attachment. |
| **Nonempty** (1 statement) | Statement admitted, complete closure, all answers favorable, Net Amount < Adjusted Basis, Q13 is "no" | Eligible, positive | `statement-loss-reason` publishes `"supported-loss"`. `tax.us.2025.schedule1.top-entry` publishes Box 1a. Top entry form field renders Box 1a with explanation: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | Schedule 1 attachment rule evaluates `Box 1a > 0` as True; Schedule 1 attaches. Income lines 8/9 unchanged ($0 net tax effect). Return complete. |
| **Nonempty** (1 statement) | Statement admitted, complete closure, but ineligible (gain, break-even, excluded circumstance, unanswered, or reconciliation discrepancy) | Ineligible / blocked | `statement-loss-reason` publishes specific categorical stop code. `tax.us.2025.schedule1.top-entry` blocks (`DEPENDENCY_ABSENT`). Top entry form field renders `""`. Unresolved field records and projects named stop description. | Schedule 1 attachment blocks (`BLOCK_ABSENT`). **Income lines 8/9 unaffected**. Review presents stop explanation with sentence *"Because this statement is unresolved, the return's income does not yet account for this Form 1099-K statement."* Return filing withheld. |
| **Nonempty** (2 statements) | Two statements admitted | Out of scope (Foreman Decision / R2) | Top entry blocks with named stop `MULTIPLE_F1099K_OUT_OF_SCOPE` (`multiple-f1099k-out-of-scope`). Top entry form field renders `""`. Unresolved field records `multiple-f1099k-out-of-scope`. | Schedule 1 attachment blocks (`BLOCK_ABSENT`). Income lines 8/9 unaffected. Return filing withheld. |

---

### Artifact 3: Late-Authority Counterexample Trace

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" Artifact 3. Follows the required paper trace: `attest → close → compute → add member → reclose → recompute`.

```text
attest → close → compute → add member → reclose → recompute
```

1. **Attest**:
   - The platform furnishes Form 1099-K statement A (`payer: "OnlineMarket"`, `statement: "stmt-1"`, `tax-year: 2025`) with Box 1a = `$880.00`, Box 4 = `$0.00`.
   - Member transition mints horizon `h1` for `tax.us.2025.f1099k`.
   - The person records circumstance answers: agreed price `$800.00`, buyer shipping `$24.00`, platform tax `$56.00` (reconciliation `$880 == $800 + $56 + $24` holds); shipping arrangement `"seller-received-shipping"`; seller-paid shipping (label) `$24.00`; platform fees `$80.00`; refund `$0.00`; purchase cost `$1,200.00`; lasting improvements `"no"`.
2. **Close**:
   - Taxpayer asserts closure finding for `tax.us.2025.f1099k.source-closure` keyed on horizon `h1` with value `True`.
   - `packages/derivation/source_authority.py:100-160` resolves closure admissions: horizon `h1` matches current horizon. `tax.us.2025.f1099k` enters `env.closed_sets`.
3. **Compute**:
   - Statement A evaluates single comparison:
     - Amount Realized = `$800.00 + $24.00 - $0.00 = $824.00`.
     - Selling Expenses = `$80.00 + $24.00 = $104.00`.
     - Net Amount = `$824.00 - $104.00 = $720.00`.
     - Adjusted Basis = `$1,200.00`.
     - Net Amount (`$720.00`) < Adjusted Basis (`$1,200.00`) and improvements == "no" $\rightarrow$ Loss established.
   - `tax.us.2025.rule.f1099k-statement-loss-reason` publishes categorical reason `"supported-loss"` for statement A.
   - `tax.us.2025.rule.schedule1-top-entry` checks single-statement scope (`count == 1`) and favorable reason, publishing `$880.00`.
   - `rule.attachment.schedule-1.v3` evaluates: `subtotals` includes `top-entry` (`$880.00`). Because `$880.00 > $0.00`, Schedule 1 is attached. Return is complete with `$0.00` net tax effect.
4. **Add Member**:
   - A second Form 1099-K statement B (`payer: "TicketResale"`, `statement: "stmt-2"`, `tax-year: 2025`) is asserted with Box 1a = `$400.00`.
   - Member transition mints horizon `h2` for `tax.us.2025.f1099k`. Current horizon is now `h2`.
   - **Invalidation**: The closure finding asserted in Step 2 names horizon `h1`. In `source_authority.py:146-156`, `record.horizon_id == current` fails (`h1 != h2`).
   - Consequently, `tax.us.2025.f1099k` drops out of `env.closed_sets`.
   - **What becomes unusable**: The Step 3 publications for `tax.us.2025.schedule1.top-entry` and the Schedule 1 attachment disposition are immediately unusable and invalidated. If recomputation is attempted before reclosing, `collect` over `tax.us.2025.f1099k` raises `EvalBlocked(BLOCK_CLOSURE)`, blocking Schedule 1 attachment. Form 1040 income lines 8/9 remain unaffected.
5. **Reclose**:
   - The person completes answers for statement B and asserts a new closure finding for `tax.us.2025.f1099k.source-closure` keyed on successor horizon `h2` with value `True`.
   - `source_authority.py:100-160` resolves closure admissions against current horizon `h2`. `tax.us.2025.f1099k` re-enters `env.closed_sets`.
6. **Recompute**:
   - Runner evaluates with both statements present:
     - `count` over `tax.us.2025.f1099k` evaluates to 2.
     - Per foreman decision (R2), returns with more than one Form 1099-K statement reach the named stop `MULTIPLE_F1099K_OUT_OF_SCOPE` (`multiple-f1099k-out-of-scope`).
     - `rule.schedule1-top-entry` blocks with `MULTIPLE_F1099K_OUT_OF_SCOPE`.
     - `rule.f1099k-unresolved` blocks with `MULTIPLE_F1099K_OUT_OF_SCOPE` and presents the out-of-scope stop to the filer.
     - Schedule 1 attachment blocks (`BLOCK_ABSENT`), withholding the return from filing completion while leaving Form 1040 income lines 8/9 completely unaffected.

---

### Artifact 4: Claim-Reuse Proof

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" Artifact 4. Demonstrates proposition, lifecycle, and authority scope for every reused declaration.

| Reused claim | Same proposition? | Same identity and lifecycle? | Same authority scope and explanation? | Verdict |
| --- | --- | --- | --- | --- |
| `tax.us.2025.rule.attachment.schedule-1` (succeeded `v2` $\rightarrow$ `v3`) | **Additive requirement proposition, same form attachment meaning**: "Schedule 1 is required when any of its admitted subtotals exceeds zero." v3 adds `tax.us.2025.schedule1.top-entry` to `requirement.subtotals`. | Same rule ID, version bumped to `v3`. Lifecycle tied to tax year 2025 return calculation. | Same authority scope: IRS Schedule 1 instructions and filing packet attachment. Explanation updated to cite 1099-K loss subtotal. | **PASS, versioned as additive successor** |
| `tax.us.2025.parameter.default-zero` (`v1`) | Reused only for Box 4 federal withholding and attachment threshold comparisons; NOT used as a default for blank circumstance amounts (which require affirmative values or route to unanswered stops via the structural 'not-asked' sentinel per Finding 1). | Yes — same parameter ID and version `v1`. Immutable parameter lifecycle. | Yes — threshold value `0.00`. | **PASS** |
| `tax.us.2025.citation.attachment.schedule-1` (`v1`) | Yes — citation for Schedule 1 attachment authority. | Yes — same citation ID and version `v1`. | Yes — IRS Form 1040 Schedule 1 instructions. | **PASS** |
| `tax.us.2025.rule.schedule1-line10` (`v1`) | Yes — "Schedule 1 line 10 sums Part I lines 1 through 9; top entry is not in Part I and does not feed line 10." | Yes — same ID and version. Unchanged. | Yes — Schedule 1 Part I scope. | **PASS** |
| `tax.us.2025.rule.form1040-line8` (`v1`) | Yes — "Form 1040 line 8 equals Schedule 1 line 10." | Yes — same ID and version. Unchanged. | Yes — Form 1040 instructions page 33. | **PASS** |
| `tax.us.2025.rule.form1040-line9` (`v7`) | Yes — "Total income sums W-2, interest, dividends, capital gains, line 8, IRA, and pensions." | Yes — same ID and version. Unchanged. | Yes — Form 1040 instructions page 34. | **PASS** |
| `tax.us.2025.schedule-d-boundary.no-form8949-sources` (`v1`) | Yes — "Filer has no transactions requiring Form 8949." Supported loss routes to Schedule 1, not Form 8949. | Yes — same ID and version. | Yes — Schedule D boundary bundle. | **PASS** |

---

### Artifact 5: Neighboring-Capability Dependency Diff

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" Artifact 5. Lists prerequisites before and after for each neighbor.

| Neighboring capability | Prerequisites before this design | Prerequisites after this design | What happens if lacking completeness answer? |
| --- | --- | --- | --- |
| **W-2-only return** (`tests/test_frrs_t4_w2_live_integration.py`) | W-2 source findings; standard deduction parameters. Schedule 1 attachment evaluates to `blocked` (`DEPENDENCY_ABSENT`) due to absent student loan adjustment subtotal. | **Unchanged**. Asked nothing. Schedule 1 attachment disposition evaluates to `blocked` (`DEPENDENCY_ABSENT`) before and after, income lines 8/9 unaffected, with 2 added presentation rows. | N/A — asked nothing; completeness answer is not required. |
| **Unemployment return (Schedule 1 line 7)** (`tests/test_form1099g_box1_schedule1_line7.py`) | Form 1099-G Box 1 closed subtotal > 0; Part I absence facts. | Form 1099-G Box 1 subtotal > 0; Part I absence facts; **PLUS Form 1099-K family closure** (`source-closure` on `h0`). | If lacking, `tax.us.2025.f1099k` is unclosed; `tax.us.2025.schedule1.top-entry` is absent from `self.symbols`; `rule.attachment.schedule-1.v3` blocks with `BLOCK_ABSENT` on missing `tax.us.2025.schedule1.top-entry`. Schedule 1 attachment is blocked. |
| **Student loan deduction return (Schedule 1 line 21)** (`tests/test_schedule1_line26_track4.py`, `tests/test_f1098e_student_loan_interest_agi_track6.py`) | Form 1098-E closed subtotal > 0; line 21 deduction > 0. | Form 1098-E closed subtotal > 0; line 21 deduction > 0; **PLUS Form 1099-K family closure**. | If lacking, `tax.us.2025.schedule1.top-entry` is absent; Schedule 1 attachment blocks with `BLOCK_ABSENT`. |
| **Form 1040 Line 8 (Additional Income)** | Schedule 1 line 10. | **Unchanged**. Form 1040 line 8 does not depend on Form 1099-K. | Unaffected ($0.00 net effect). |
| **Form 1040 Line 9 (Total Income)** | Form 1040 line 8 and other income sources. | **Unchanged**. Form 1040 line 9 does not depend on Form 1099-K. | Unaffected. |

#### Measured Baseline Comparison for Neighbor Returns (R3)

Measured directly against the current adopted production release (`demo.release.sli-worksheet-integration.2025.v43.json` on `published-packages.v43.json` / package `v45`) versus the candidate surface (`v44` release on package `v46`):

| Return Scenario | Schedule 1 Att Disposition (Baseline v43) | Schedule 1 Att Disposition (Candidate v46) | Line 9 Income (Baseline) | Line 9 Income (Candidate) | Presentation Rows (Baseline) | Presentation Rows (Candidate) |
|---|---|---|---|---|---|---|
| **1. W-2-only return** | `blocked` (`DEPENDENCY_ABSENT`) | `blocked` (`DEPENDENCY_ABSENT`) | `$90,000.00` | `$90,000.00` | 43 | 45 |
| **2. Unemployment return ($500.00) + 1099-K completeness closure** | `published` (attached; `$500.00`) | `published` (attached; `$500.00`) | `$90,500.00` | `$90,500.00` | 43 | 45 |
| **2. Unemployment return ($500.00) - 1099-K completeness closure** | `published` (attached; `$500.00`) | `blocked` (`BLOCK_CLOSURE` on 1099-K) | `$90,500.00` | `$90,500.00` | 43 | 45 |
| **3. Student loan interest return ($1,500.00) + 1099-K completeness closure** | `published` (attached; `$1,500.00`) | `published` (attached; `$1,500.00`) | `$90,000.00` | `$90,000.00` | 43 | 45 |
| **3. Student loan interest return ($1,500.00) - 1099-K completeness closure** | `published` (attached; `$1,500.00`) | `blocked` (`BLOCK_CLOSURE` on 1099-K) | `$90,000.00` | `$90,000.00` | 43 | 45 |

**Plain-Language Statement on W-2 Returns**:
A W-2-only return's Schedule 1 attachment disposition does NOT change (it is `blocked` with `DEPENDENCY_ABSENT` before and after due to absent student loan adjustment subtotal). Its Line 9 Total Income does NOT change (`$90,000.00` before and after). Only 2 presentation rows are added to the presentation model (`tax.us.2025.schedule1.top-entry.form-field` and `tax.us.2025.form.f1099k.unresolved.form-field`), neither of which disrupts or alters the return calculation. The two added presentation rows show the Schedule 1 top-entry row blocked and the Form 1099-K unresolved condition row inapplicable ("No open condition: statements resolved or no statement received."), requiring no entry or action from the person.

#### Existing Workspaces, Fixtures, and Tests Needing the New Completeness Answer

Grep across `packages/sample_data/` and `tests/` identifies the following suites and fixtures that determine `tax.us.2025.rule.attachment.schedule-1`:
1. `tests/test_form1099g_box1_schedule1_line7.py`
2. `tests/test_schedule1_line26_track4.py`
3. `tests/test_f1098e_student_loan_interest_agi_track6.py`
4. `tests/test_f1098e_student_loan_interest_track8_presentation.py`
5. `tests/test_form1099div_box7_direct_ftc.py`
6. `tests/test_sli_line21_explanation_page.py`
7. `tests/test_sli_line21_page_reasons.py`
8. `packages/sample_data/form1099g_box1_schedule1_line7/presentation/form1099g-box1-line8.presentation-model.v1.json`
9. `packages/sample_data/f1098e_student_loan_interest_track6/presentation/below-floor.presentation-model.v1.json`
10. `packages/sample_data/f1098e_student_loan_interest_track6/presentation/closed-empty.presentation-model.v1.json`
11. `packages/sample_data/f1098e_student_loan_interest_track6/presentation/universal-violation.presentation-model.v1.json`
12. `packages/sample_data/form1099div_box7_direct_ftc/presentation/box7-direct-ftc.presentation-model.v1.json`

**Consequence if lacking**: In each test/fixture above, `rule.attachment.schedule-1.v3` requires `tax.us.2025.schedule1.top-entry` to be present in `self.symbols`. Without the Form 1099-K closure assertion at `h0`, `collect` raises `EvalBlocked(BLOCK_CLOSURE)` (`evaluator.py:374`), causing `runner.py:1871-1874` to block Schedule 1 attachment with `BLOCK_ABSENT` on missing `tax.us.2025.schedule1.top-entry`. Migration requires adding the Form 1099-K closure assertion (`source-closure` on `h0` with `True`) to these fixtures when upgrading to package `v46`.

---

### Artifact 6: Integration Surface and Disposition Paths

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" Artifact 6.

#### 1. External Symbol Bindings and Cardinalities

| Published symbol | Consumer | Binding artifact or join | Cardinality expected | Satisfied by design? |
| --- | --- | --- | --- | --- |
| `tax.us.2025.schedule1.top-entry` | Form field presentation projection | `tax.us.2025.schedule1.top-entry.form-field` (`schema: form-field.v3`) | **Exactly one** disposition row per symbol (`presentation_projection._one_row`) | **Yes**. Produced by exactly one rule citizen (`tax.us.2025.rule.schedule1-top-entry`). On closed-empty, publishes `0`. On supported loss, publishes Box 1a. On unsupported or >1 statement, blocks with single blocked row. |
| `tax.us.2025.schedule1.top-entry` | Schedule 1 attachment evaluation | `tax.us.2025.rule.attachment.schedule-1.v3` (`requirement.subtotals`) | Exactly one symbol value in `self.symbols` | **Yes**. Evaluated once per run. |
| `tax.us.2025.f1099k.unresolved` | Unresolved condition presentation | `tax.us.2025.form.f1099k.unresolved.form-field` (`schema: form-field.v3`) | **Exactly one** disposition row per symbol (`presentation_projection._one_row`) | **Yes**. Produced by exactly one rule citizen (`tax.us.2025.rule.f1099k-unresolved`). |
| `tax.us.2025.f1099k.statement-loss-reason` | Top entry rule & Unresolved selection rule | `tax.us.2025.rule.schedule1-top-entry` & `tax.us.2025.rule.f1099k-unresolved` | Exactly one finding per statement subject | **Yes**. Subject-scoped rule produces exactly one categorical finding per statement subject. |

#### 2. Materially Distinct Disposition Paths for Stage 2 Probe

Stage 2 (`d2_probe.py`) must assemble throwaway candidate citizens and exercise each of the following 33 materially distinct disposition paths through `live_coordinate_run` and the real presentation model:

1. **Closed-empty return with 1099-K completeness closure**: Completeness assertion (`source-closure` on `h0` with `True`) asserts closure at `h0`; top entry publishes `0`; Schedule 1 inapplicable; return complete.
2. **Existing Schedule 1 return (Unemployment) with 1099-K completeness closure**: Unemployment line 7 > 0; 1099-K closed-empty `0`; Schedule 1 attaches.
3. **Existing Schedule 1 return (Unemployment) WITHOUT 1099-K completeness closure**: Unemployment line 7 > 0; 1099-K unclosed; Schedule 1 attachment blocks with `BLOCK_ABSENT` on missing `tax.us.2025.schedule1.top-entry`.
4. **W-2-only return**: Pure W-2 return; Schedule 1 attachment evaluates to `blocked` (`DEPENDENCY_ABSENT`) before and after due to absent student loan adjustment subtotal; asked nothing; 2 added presentation rows show Schedule 1 top-entry blocked and unresolved condition inapplicable; income unaffected.
5. **Single supported loss (platform pass-through shipping)**: Agreed price `$800.00`, buyer shipping `$24.00` retained by platform; seller receives `$800.00`, fees `$80.00`; net proceeds `$720.00` < cost `$1,000.00`; Box 1a `$880.00` published on Schedule 1 top entry; Schedule 1 attached.
6. **Single supported loss (seller-received shipping)**: Agreed price `$800.00`, buyer shipping `$24.00` disbursed to seller; seller pays `$24.00` label, fees `$80.00`; amount realized `$824.00`, selling expenses `$104.00`; net proceeds `$720.00` < cost `$1,000.00`; Box 1a `$880.00` published; Schedule 1 attached.
7. **Single supported loss with refund**: Agreed price `$800.00`, refund `$100.00`, fees `$80.00`; amount realized `$700.00`, net proceeds `$620.00` < cost `$1,000.00`; Box 1a `$800.00` published; Schedule 1 attached.
8. **Single supported loss with seller-paid shipping on free shipping**: Agreed price `$800.00`, buyer shipping none; seller pays `$30.00` shipping out of pocket, fees `$80.00`; net proceeds `$690.00` < cost `$1,000.00`; Box 1a `$800.00` published; Schedule 1 attached.
9. **Two statements (out of scope)**: Two Form 1099-K statements admitted (Statement A `$880.00`, Statement B `$400.00`); count > 1; reaches named stop `multiple-f1099k-out-of-scope` (following the Form 1098 pattern); top entry blocks with `DEPENDENCY_ABSENT`; Schedule 1 attachment blocks; unresolved condition displays `multiple-f1099k-out-of-scope`; income lines 8/9 unaffected.
10. **Unsupported capital gain**: Proceeds (`$1,100.00`) > Cost (`$800.00`); blocks `UNSUPPORTED_GAIN_NOT_REPORTED`; Schedule 1 attachment blocks; income lines unaffected; unresolved condition displayed.
11. **Break-even sale**: Proceeds (`$700.00`) == Cost (`$700.00`); blocks `BREAK_EVEN_SALE_UNSUPPORTED`; Schedule 1 attachment blocks; income lines unaffected.
12. **Excluded circumstance: Investment / profit purpose (Q4)**: Blocks `INVESTMENT_PURPOSE_EXCLUDED`; Schedule 1 attachment blocks; income lines unaffected.
13. **Excluded circumstance: Resale / inventory purpose (Q4)**: Blocks `RESALE_OR_INVENTORY_EXCLUDED`; Schedule 1 attachment blocks.
14. **Excluded circumstance: Prior business / rental depreciable use (Q5)**: Blocks `PRIOR_DEPRECIABLE_USE_EXCLUDED`; Schedule 1 attachment blocks.
15. **Excluded circumstance: Digital asset / virtual currency (Q7)**: Blocks `DIGITAL_ASSET_EXCLUDED`; Schedule 1 attachment blocks.
16. **Multiple sales on single statement (Q1)**: Blocks `MULTI_SALE_STATEMENT_UNSUPPORTED`; Schedule 1 attachment blocks.
17. **Non-purchase acquisition (Q3)**: Blocks `NON_PURCHASE_ACQUISITION_UNSUPPORTED`; Schedule 1 attachment blocks.
18. **Lasting improvements / basis adjustments (Q13)**: Answer "yes" blocks `BASIS_ADJUSTMENT_PRESENT_OR_UNKNOWN`; Schedule 1 attachment blocks.
19. **Backup withholding present in Box 4**: Box 4 > `$0.00`; blocks `BACKUP_WITHHOLDING_UNSUPPORTED`; Schedule 1 attachment blocks.
20. **Cost basis unknown (Q12)**: Person answers "can't tell"; blocks `COST_BASIS_UNKNOWN`; Schedule 1 attachment blocks.
21. **Unanswered question / withdrawn answer**: Answer withdrawn leaving question unanswered; parameter default binds `"not-asked"`; blocks with named stop (e.g. `PERSONAL_USE_UNCONFIRMED`); Schedule 1 attachment blocks.
22. **Unexplained reconciliation discrepancy**: Box 1a (`$850.00`) != Agreed Price (`$700.00`) + Tax (`$0.00`) + Shipping (`$0.00`); blocks `FORM_1099K_RECONCILIATION_UNEXPLAINED`; Schedule 1 attachment blocks.
23. **Supported loss alongside unsupported statement**: Statement A supported loss, Statement B unsupported gain; count > 1; top entry blocks with `DEPENDENCY_ABSENT` on stop `multiple-f1099k-out-of-scope`; Schedule 1 attachment blocks; income lines unaffected.
24. **Late statement added after closure**: Horizon transitions `h1` $\rightarrow$ `h2`; closure at `h1` invalidated; computation blocks `BLOCK_CLOSURE` until reclosure at `h2`.
25. **Correction across gain/loss boundary**: Cost basis corrected from `$1,200.00` to `$600.00` (proceeds `$720.00`); transitions from supported loss to `UNSUPPORTED_GAIN_NOT_REPORTED`; Schedule 1 attachment transitions from attached to blocked.
26. **Omitted platform selling fee (F1)**: Platform fee omitted / not asked; binds to parameter default `"not-asked"`; blocks with `platform-fees-unanswered`; top entry blocked; unresolved blocked; sentence explains question has no current answer.
27. **Withdrawn agreed item price (F1)**: Agreed price withdrawn leaving question unanswered; binds to parameter default `"not-asked"`; blocks with `agreed-price-unanswered`; top entry blocked; unresolved blocked; sentence explains question has no current answer.
28. **Improvements / basis adjustments "can't tell" (F6)**: Person answers "cannot-tell" on lasting improvements / basis adjustments; blocks with distinct stop `cannot-tell-improvements`; top entry blocked; unresolved blocked; sentence: *"It is not known whether lasting improvements or other basis adjustments were made to the item."*
29. **Boundary Case 1: Seller-received shipping gain (F2)**: Agreed price `$800.00`, shipping arrangement seller-received, buyer shipping `$100.00`, seller-paid label `$20.00`, platform fee `$0.00`, sales tax `$0.00`, refund `$0.00`, cost `$850.00`; Box 1a `$900.00`; net amount `$880.00` > cost `$850.00`; blocks `unsupported-gain`; top entry blocked. A price-only comparison would have published a loss.
30. **Boundary Case 2: Refund loss (F2)**: Agreed price `$800.00`, arrangement none, refund `$100.00`, fees and shipping `$0.00`, cost `$750.00`; Box 1a `$800.00`; net amount `$700.00` < cost `$750.00`; supported loss; top entry published Box 1a `800.0`, not the net `700`.
31. **Boundary Case 3: Seller-paid shipping loss (F2)**: Agreed price `$800.00`, arrangement none, seller-paid shipping `$100.00`, fees `$0.00`, refund `$0.00`, cost `$750.00`; Box 1a `$800.00`; net amount `$700.00` < cost `$750.00`; supported loss; top entry published Box 1a `800.0`.
32. **Boundary Case 4: Pass-through shipping loss (F2)**: Agreed price `$800.00`, platform pass-through shipping `$100.00`, fees and seller shipping `$0.00`, cost `$850.00`; Box 1a `$900.00`; net amount `$800.00` < cost `$850.00`; supported loss; top entry published Box 1a `900.0`.
33. **Boundary Case 5: Pass-through with seller-paid shipping gain (F2)**: Agreed price `$900.00`, platform pass-through, seller-paid shipping `$100.00` not deducted because the seller did not receive the shipping, cost `$850.00`; Box 1a `$900.00`; net amount `$900.00` > cost `$850.00`; blocks `unsupported-gain`.

---

## Stage 2 — Built Models and Probe Results

Invocation:
```sh
python3 docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances-evidence/d2_probe.py
```

### 1. Probe Execution Matrix (33 Paths)

Every path from the Stage 1 list was constructed as a synthetic candidate workspace and executed against the real engine: `live_coordinate_run` followed by `build_presentation_model`. All 33 paths executed cleanly with 0 exceptions and 0 refusals.

| # | Disposition Path | Actual Reason Token | Top Entry (`tax.us.2025.schedule1.top-entry`) | Schedule 1 Att (`tax.us.2025.rule.attachment.schedule-1.v3`) | Unresolved (`tax.us.2025.form.f1099k.unresolved.form-field`) | Presentation Sentence(s) | Status |
|---|---|---|---|---|---|---|---|
| 1 | `closed-empty-with-completeness` | `0` | Published: `0` | Inapplicable (`guard_result: False`) | `guard_inapplicable` | None (complete return; 45 rows) | **PASS** |
| 2 | `unemployment-with-completeness` | `0` | Published: `0` | Published (attached; UI: `$500.00`) | `guard_inapplicable` | None (complete return; 45 rows) | **PASS** |
| 3 | `unemployment-without-completeness` | `SOURCE_SET_UNCLOSED` | Blocked: `BLOCK_CLOSURE` | Blocked: `BLOCK_ABSENT` | `guard_inapplicable` | Top Entry: *"Form 1099-K loss entry cannot be computed."* | **PASS** |
| 4 | `w2-only-return` | `SOURCE_SET_UNCLOSED` | Blocked: `BLOCK_CLOSURE` | Blocked: `DEPENDENCY_ABSENT` | `guard_inapplicable` | Top Entry: *"Form 1099-K loss entry cannot be computed."*; Unresolved: inapplicable | **PASS** |
| 5 | `supported-loss-pass-through-shipping` | `supported-loss` | Published: `880.0` | Published (attached) | `guard_inapplicable` | Top Entry: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | **PASS** |
| 6 | `supported-loss-seller-received-shipping` | `supported-loss` | Published: `880.0` | Published (attached) | `guard_inapplicable` | Top Entry: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | **PASS** |
| 7 | `supported-loss-with-refund` | `supported-loss` | Published: `800.0` | Published (attached) | `guard_inapplicable` | Top Entry: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | **PASS** |
| 8 | `supported-loss-free-shipping-seller-paid` | `supported-loss` | Published: `800.0` | Published (attached) | `guard_inapplicable` | Top Entry: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | **PASS** |
| 9 | `two-statements-out-of-scope` | `multiple-f1099k-out-of-scope` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `multiple-f1099k-out-of-scope` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"More than one Form 1099-K statement was received; reporting personal item sale losses across multiple statements is outside the supported scope of this return."* | **PASS** |
| 10 | `unsupported-gain` | `unsupported-gain` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `unsupported-gain` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."* | **PASS** |
| 11 | `break-even-sale` | `break-even-sale` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `break-even-sale` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The sale broke even with no gain or loss, so no adjustment is reported on Schedule 1."* | **PASS** |
| 12 | `investment-purpose-excluded` | `investment-purpose-excluded` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `investment-purpose-excluded` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The item was acquired for investment or profit; personal item loss treatment does not apply."* | **PASS** |
| 13 | `resale-inventory-excluded` | `resale-inventory-excluded` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `resale-inventory-excluded` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The item was acquired for resale or business inventory; personal item loss treatment does not apply."* | **PASS** |
| 14 | `prior-depreciable-use-excluded` | `prior-depreciable-use-excluded` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `prior-depreciable-use-excluded` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The item was used for business or rental purposes; personal item loss treatment does not apply."* | **PASS** |
| 15 | `digital-asset-excluded` | `digital-asset-excluded` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `digital-asset-excluded` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The transaction involved digital assets or virtual currency, which are outside the scope of this personal item sale route."* | **PASS** |
| 16 | `multi-sale-statement-unsupported` | `multi-sale-statement-unsupported` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `multi-sale-statement-unsupported` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The Form 1099-K statement covers more than a single personal item sale."* | **PASS** |
| 17 | `non-purchase-acquisition-unsupported` | `non-purchase-acquisition-unsupported` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `non-purchase-acquisition-unsupported` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The item was not acquired by purchase."* | **PASS** |
| 18 | `basis-adjustment-unsupported` | `basis-adjustment-unsupported` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `basis-adjustment-unsupported` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"Lasting improvements or other basis adjustments were made to the item."* | **PASS** |
| 19 | `backup-withholding-unsupported` | `backup-withholding-unsupported` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `backup-withholding-unsupported` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"Federal income tax was withheld (Box 4), which requires separate reporting."* | **PASS** |
| 20 | `cost-basis-unknown` | `cost-basis-unknown` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `cost-basis-unknown` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The original purchase cost of the item is unknown."* | **PASS** |
| 21 | `unanswered-stop` | `personal-use-unconfirmed` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `personal-use-unconfirmed` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The question regarding exclusive personal use has no current answer."* | **PASS** |
| 22 | `unexplained-reconciliation-discrepancy` | `unexplained-reconciliation-discrepancy` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `unexplained-reconciliation-discrepancy` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The reported Box 1a amount does not reconcile with the item price, sales tax, and shipping amounts."* | **PASS** |
| 23 | `supported-alongside-unsupported` | `multiple-f1099k-out-of-scope` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `multiple-f1099k-out-of-scope` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"More than one Form 1099-K statement was received; reporting personal item sale losses across multiple statements is outside the supported scope of this return."* | **PASS** |
| 24 | `late-member-after-closure` | `multiple-f1099k-out-of-scope` | Blocked: `SOURCE_SET_UNCLOSED` | Blocked: `BLOCK_ABSENT` | Blocked: `multiple-f1099k-out-of-scope` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"More than one Form 1099-K statement was received; reporting personal item sale losses across multiple statements is outside the supported scope of this return."* | **PASS** |
| 25 | `gain-loss-boundary-correction` | `unsupported-gain` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `unsupported-gain` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."* | **PASS** |
| 26 | `omitted-platform-fee` | `platform-fees-unanswered` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `platform-fees-unanswered` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The question regarding platform selling fees has no current answer."* | **PASS** |
| 27 | `withdrawn-amount` | `agreed-price-unanswered` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `agreed-price-unanswered` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The question regarding agreed item price has no current answer."* | **PASS** |
| 28 | `cannot-tell-improvements` | `cannot-tell-improvements` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `cannot-tell-improvements` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"It is not known whether lasting improvements or other basis adjustments were made to the item."* | **PASS** |
| 29 | `boundary-case-1-seller-received-shipping-gain` | `unsupported-gain` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `unsupported-gain` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."* | **PASS** |
| 30 | `boundary-case-2-refund-loss` | `supported-loss` | Published: `800.0` | Published (attached) | `guard_inapplicable` | Top Entry: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | **PASS** |
| 31 | `boundary-case-3-none-shipping-seller-paid-loss` | `supported-loss` | Published: `800.0` | Published (attached) | `guard_inapplicable` | Top Entry: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | **PASS** |
| 32 | `boundary-case-4-pass-through-shipping-loss` | `supported-loss` | Published: `900.0` | Published (attached) | `guard_inapplicable` | Top Entry: *"This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1."* | **PASS** |
| 33 | `boundary-case-5-pass-through-seller-paid-gain` | `unsupported-gain` | Blocked: `DEPENDENCY_ABSENT` | Blocked: `BLOCK_ABSENT` | Blocked: `unsupported-gain` | Top Entry: *"Form 1099-K loss entry cannot be computed."*<br>Unresolved: *"The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."* | **PASS** |

---

### 2. Resolution of Prior Substrate Findings via Architectural Choices

The probe's earlier iterations encountered two substrate limits that halted `build_presentation_model`:
1. **Prior Substrate Finding 1 (Presentation Projection Reader Gap on Numeric Selection Rules)**:
   In `packages/derivation/presentation_projection.py:348-377`, `_selection_blocked_reasons` previously assumed categorical classification rules with `collect_categorical_all_equal` expressions. When a selection rule performed numeric `sum` over blocked statements, `PresentationModelError` was raised.
   - **Resolution (Foreman Decision R1)**: Rather than attempting to aggregate numeric sums over blocked items, the architecture adopts the proven Form 1098 categorical reason pattern:
     - The per-statement rule publishes a categorical reason `tax.us.2025.f1099k.statement-loss-reason` (`"supported-loss"` or a named stop code).
     - The unresolved field rule `tax.us.2025.rule.f1099k-unresolved` is an exclusive-presence selection rule over that reason, following `rule.f1098-residence-interest-unresolved.v2.json:1-36`.
     - The presentation projection reader (`presentation_projection.py:157-377`) natively projects each named stop's plain-language description from `oneOf` constraints in `f1099k.bundle.json:1-95`.
2. **Prior Substrate Finding 2 (Multi-Statement Circumstance Scoping in `marshal.py`)**:
   In `packages/derivation/marshal.py:397-421`, multiple Form 1099-K statements with differing circumstance answers caused ambiguity in circumstance scoping.
    - **Resolution (Foreman Decision R2)**: Form 1099-K personal item sale circumstances in this milestone are bounded to one statement per return, matching the Form 1098 mortgage precedent (`packages/content/tax/2025/rule.f1098-line8a.v2.json:56`). Returns with more than one statement reach the explicit named stop `multiple-f1099k-out-of-scope`. Multi-statement returns are withheld safely from filing completion with an unresolved condition, leaving income lines 8/9 unaffected.

---

## Track 0 adversarial closure

Per `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate". Evidence below is this design's text (Artifacts 1–6) and `d2_probe.py`'s measured execution results.

### Line-by-Line Declaration

| Gate Line | Status | Concrete Evidence and Disposition |
|---|---|---|
| **Artifact 1: Authority-lifecycle table** | **PASS** | Complete table provided in Section 3, distinguishing storage identity from authority scope across all contributed facts, companion circumstances, defaults, and closure assertions. Load-bearing relationships and invalidation triggers are fully specified. |
| **Artifact 2: Empty/nonempty authority matrix** | **PASS** | Mandatory states (Closed empty with authority, Closed empty without authority, Nonempty eligible, Nonempty ineligible, Multi-statement out-of-scope) fully specified in Section 3. Corroborated live by probe Paths 1, 3, 5, 9, 10–22, 26–33. |
| **Artifact 3: Late-authority counterexample** | **PASS** | Paper trace `attest → close → compute → add member → reclose → recompute` fully demonstrated in Section 3. Corroborated by probe Path 24 proving that horizon advance invalidates prior closure and blocks until reclosure. |
| **Artifact 4: Claim-reuse proof** | **PASS** | Semantic, lifecycle, and authority scope equivalence verified in Section 3. Schedule 1 attachment rule (`rule.attachment.schedule-1.v3`) reuse is explicitly analyzed and confirmed to preserve exact semantics across all paths. |
| **Artifact 5: Neighboring-capability dependency diff** | **PASS** | Complete prerequisite analysis and empirical before/after measurements provided in Section 3 across all neighbors (W-2, 1099-G unemployment, student loan interest, Schedule 1 attachment). Corroborates that W-2-only Schedule 1 result is unchanged, and that Form 1040 line 9 (income) and tax computation never depend on Form 1099-K closure, strictly obeying the Owner Decision of 2026-10-16. |
| **Artifact 6: Integration surface and disposition paths** | **PASS** | All external symbol bindings and cardinalities are enumerated. All 33 materially distinct disposition paths in `d2_probe.py` execute cleanly through the real `live_coordinate_run` and the real presentation model (`build_presentation_model`), asserting and verifying the exact expected categorical reason token, top-entry row publication amount (Box 1a on supported-loss, 0 on closed-empty, none on stops/blocked), top-entry row sentence ("Form 1099-K loss entry cannot be computed." on blocked; "This sale resulted in a nondeductible personal loss whose Box 1a gross amount is entered at the top of Schedule 1." on supported-loss), and unresolved row projected sentence for every path with 0 failures, 0 exceptions, and 0 refusals (0 failed paths). |

### Known Limitations Affecting Correctness

- **One Form 1099-K Statement per Return Scope**: Returns reporting personal item sale circumstances on multiple Form 1099-K statements reach the explicit named stop `multiple-f1099k-out-of-scope` per foreman decision (R2), mirroring the Form 1098 precedent. Multi-statement returns are safely withheld with an unresolved condition while leaving income lines unaffected.
- **Substrate Changes Required**: None. All 33 disposition paths execute cleanly under the current derivation and presentation substrate.
