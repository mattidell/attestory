# Track 3 Stage 1: Computation Feasibility, Reader Design, and Saved Explanations

**Status:** Complete\
**Milestone Key:** `personal-item-sale-circumstances`\
**Milestone Branch:** `milestone/personal-item-sale-circumstances-translation`\
**Charter:** Track 3 computation charter\
**Launch Verified:** Verified at Track 3 computation launch

---

## 1. Published Amounts Beside Named Stops

### 1.1 The Engine Execution Model and Dependency Check
In the derivation engine, rule prerequisites are governed by two distinct layers:
1. **Pre-Evaluation Dependency Checking in `subject_dispatch.py` and `runner.py`**:
   - In `packages/derivation/subject_dispatch.py:691-700`, for each subject of a subject-dispatched rule, the engine loops over `required = _requires(rule)`. If any required symbol is neither matched by an in-scope finding nor covered by a declared parameter default via `_optional_default(run, req)` (`packages/derivation/subject_dispatch.py:697-700, 720-723`), it is appended to `absent`.
   - In `packages/derivation/subject_dispatch.py:761-771`, if `absent` is non-empty, `subject_dispatch` immediately records a `SubjectBlocked` disposition with `code: DEPENDENCY_ABSENT`, `missing: tuple(absent)` and terminates evaluation for that subject via `continue` (`packages/derivation/subject_dispatch.py:771`). **The rule's AST is never evaluated.**
   - Similarly, for non-subject rules in `packages/derivation/runner.py:2779-2793`, `missing = [req for req in rule["requires"] if req not in self.symbols]`. If `missing` is non-empty, the runner immediately appends `code: BLOCK_ABSENT` (or `"DEPENDENCY_ABSENT"`) and continues to the next rule without evaluating the rule AST.

2. **AST Evaluation and Lazy Branching in `evaluator.py`**:
   - In `packages/derivation/evaluator.py:455-457`, `choose` evaluates its `when` condition; only the selected branch (`then` or `else`) is evaluated:
     ```python
     if op == "choose":
         branch = "then" if bool(evaluate(expr["when"], env, access)) else "else"
         return evaluate(expr[branch], env, access)
     ```
   - In `packages/derivation/evaluator.py:332-336`, `ref` looks up `expr["name"]` in `env.symbols`:
     ```python
     if op == "ref":
         access.refs.add(expr["name"])
         if expr["name"] not in env.symbols:
             raise EvalBlocked(BLOCK_ABSENT, [expr["name"]])
         val = env.symbols[expr["name"]]
     ```
   - Crucially, in `packages/derivation/subject_dispatch.py:640, 691-729`, `local_symbols` (which becomes `env.symbols` at line 792) is populated **only** from the symbols declared in `required`. If a rule attempts to access an undeclared symbol via `ref`, `env.symbols` does not contain it, raising `EvalBlocked(BLOCK_ABSENT)`.

### 1.2 The Hypothetical Architecture: Successor Reason Rule Requiring Computation Rules
Suppose per-statement computation rules publish:
- `tax.us.2025.f1099k.amount-realized`
- `tax.us.2025.f1099k.selling-expenses`
- `tax.us.2025.f1099k.net-proceeds`
- `tax.us.2025.f1099k.adjusted-basis`

And suppose a successor reason rule requires `net-proceeds` and `adjusted-basis` in order to compare them.

**What happens when an amount answer is `not-asked` or `cannot-tell`?**
- When platform fees (`tax.us.2025.f1099k.platform-fees`) are omitted or unanswered, `rule.f1099k-selling-expenses` cannot evaluate its arithmetic addition (`packages/derivation/evaluator.py:423-424`), because platform fees are a non-numeric string (`"not-asked"`). The rule blocks with `DEPENDENCY_ABSENT` and does not publish `selling-expenses`.
- In turn, `rule.f1099k-net-proceeds` requires `selling-expenses`, so it also does not publish.
- When `rule.f1099k-statement-loss-reason` is dispatched, `subject_dispatch.py:699` sees that `net-proceeds` is absent. Because `net-proceeds` is a derived intermediate finding without an `optional_default` parameter, `absent.append("tax.us.2025.f1099k.net-proceeds")`.
- At `packages/derivation/subject_dispatch.py:761-771`, `if absent:` blocks the entire reason rule with `DEPENDENCY_ABSENT`, recording `missing: ['tax.us.2025.f1099k.net-proceeds']`.
- **Result:** The reason rule's `choose` tree is **never entered**. The specific named stop (`platform-fees-unanswered`) is completely **lost**, replaced by an opaque, generic dependency failure on an internal intermediate symbol.

This failure was empirically proven in Part 1B of `docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances-evidence/track3_probe.py`:
```text
1B (Platform Fees Unanswered): Reason publications count = 0
    Reason dispositions = [{'artifact_id': 'tax.us.2025.rule.f1099k-statement-loss-reason', 'code': 'DEPENDENCY_ABSENT', 'disposition': 'blocked', 'missing': ['tax.us.2025.f1099k.net-proceeds'], ...}]
    -> CONFIRMED: Successor reason rule blocked with generic DEPENDENCY_ABSENT.
    -> CONFIRMED: Named stop 'platform-fees-unanswered' was LOST because prerequisite NET_PROCEEDS did not publish.
```

### 1.3 The Single-Source Architecture: Total Computation Rules with Successor Reason Comparison
The parallel architecture (where the reason rule preserves inline arithmetic while four separate computation rules compute the same amounts independently) was rejected during review because figures shown in presentation would originate from different rules than the comparison that established the determination—they would agree only because formulas were duplicated.

In the **single-source architecture**, the determination comparison is performed directly on the published computation findings without duplicate arithmetic, while completely preserving all 36 named stops:

1. **Total Publication in Computation Rules via `not-computed` Category Literals**:
   - Each of the four computation rules (`rule.f1099k-amount-realized`, `rule.f1099k-selling-expenses`, `rule.f1099k-net-proceeds`, and `rule.f1099k-adjusted-basis`) ALWAYS publishes a finding for every statement.
   - When all required arithmetic inputs are numeric, the rule evaluates its formula and publishes the resulting number.
   - When any required input is incomplete, omitted, or uncertain (e.g. `"not-asked"` or `"cannot-tell"`), the rule emits the categorical token `"not-computed"` using a `category_literal` matching vocabulary bundle `tax.us.2025.f1099k.vocabulary`.
   - Each computation fact type's `value_schema` admits both shapes via `oneOf`:
     ```json
     {
       "oneOf": [
         {"type": "number"},
         {"type": "string", "enum": ["not-computed"]}
       ]
     }
     ```
   - **Absence Prevention**: Because every raw input fact type possesses an `optional_default` binding parameter (`parameter: "not-asked"`), `subject_dispatch.py:691-729` never marks them as `absent`. The computation rules never block with `SubjectBlocked(DEPENDENCY_ABSENT)`—they always evaluate their AST and publish a finding.
   - **Intermediate Chaining**: `rule.f1099k-net-proceeds` checks whether `amount-realized` or `selling-expenses` equals `"not-computed"`. If either is `"not-computed"`, it publishes `"not-computed"`; otherwise it evaluates `amount-realized - selling-expenses`. Because intermediate computation rules always publish, downstream computation rules are never starved of prerequisite findings.

2. **The Successor Reason Rule Contains No Arithmetic**:
   - `tax.us.2025.rule.f1099k-statement-loss-reason` requires the four published computation symbols (`amount-realized`, `selling-expenses`, `net-proceeds`, `adjusted-basis`) in addition to the raw circumstance answers.
   - It maintains the exact same top-to-bottom order of named stops evaluated directly from raw answers first (unasked questions, invalid answers, exclusions, unknown amounts, reconciliations).
   - Only on the fully-answered branch—where all circumstance conditions are satisfied—does it evaluate the outcome.
   - On this branch, it first references `amount-realized` and `selling-expenses` (verifying they are not `"not-computed"`), and then compares the published `net-proceeds` and `adjusted-basis` findings directly:
     - If `net-proceeds < adjusted-basis`: publishes `supported-loss`
     - If `net-proceeds > adjusted-basis`: publishes `unsupported-gain`
     - Else: publishes `break-even-sale`
   - **Zero Arithmetic**: The reason rule performs no addition, subtraction, or formula calculation. The figures compared to establish the disposition are the exact figures published by the computation rules.
   - **Pinning Guarantee**: Under `packages/derivation/runner.py:649-653` and `548-560` (`dependency_pins_for_access`), intermediate findings are pinned to the reason finding only when they are accessed in `access.refs` during evaluation. Gating on `computed_ready` guarantees that all four computation findings (`amount-realized`, `selling-expenses`, `net-proceeds`, `adjusted-basis`) are accessed and included in `reason_finding["pins"]`.

#### Empirical Verification in `track3_probe.py`
The single-source design was implemented and verified in `docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances-evidence/track3_probe.py`:

1. **Derived Findings with Token Value Accepted by Runner and Validation (Point d)**:
   - When platform fees are omitted, `amount-realized` publishes `800.0`, `selling-expenses` publishes `'not-computed'`, `net-proceeds` publishes `'not-computed'`, and `adjusted-basis` publishes `1000.0`.
   - Engine validation and execution trace:
     - In `packages/derivation/subject_dispatch.py:534-545`, `_publication` validates each finding against schema via `run.schemas.validate_declared(finding)` and renders the string value with `_value_str(value)`.
     - In `packages/schemas/derivation/derived-finding.v2.schema.json:5`, `"value": {}` accepts any JSON value, admitting string `"not-computed"`.
     - In `packages/derivation/runner.py:409-414`, `self.symbols[symbol] = value` stores string values in the symbol table.
     - In `packages/derivation/live.py:538-546`, live execution coordinates and outputs findings into the run output without schema or type rejection.
     - In `packages/derivation/package_validation.py:1450-1490, 3776-3798`, AST validation permits `category_literal` with `(id, version)` matching the vocabulary bundle.
     - In `packages/derivation/evaluator.py:480-488, 1005-1026`, `categorical_compare` allows testing equality without domain membership exception because `value_schema` uses `oneOf` rather than a top-level `enum`.

2. **Named Stops Preserved (Point a)**:
   - Omitted platform fee -> `platform-fees-unanswered`
   - Withdrawn price -> `agreed-price-unanswered`
   - Cannot-tell platform fee -> `platform-fees-unknown`
   - Cannot-tell improvements -> `cannot-tell-improvements`
   - Investment purpose exclusion -> `investment-purpose-excluded`
   - All 36 named stops evaluate and publish accurately before computation comparison is reached.

3. **Reason Finding Pins Include All 4 Computation Findings (Point c)**:
   - On complete loss (Probe Path 5):
     - `tax.us.2025.f1099k.amount-realized`: `finding:derived:feb70dac9ce6b71382364670`
     - `tax.us.2025.f1099k.selling-expenses`: `finding:derived:226df5cd652e05f474ff6f6e`
     - `tax.us.2025.f1099k.net-proceeds`: `finding:derived:e15e292f133afbe49024ec75`
     - `tax.us.2025.f1099k.adjusted-basis`: `finding:derived:78f234faba66ab7403c6e1db`
   - All 4 finding IDs are present in `reason_finding["pins"]`, allowing the presentation reader to traverse and display them directly.

4. **Regression Verification Across All 33 Track 1 Paths (Point b)**:
   - All 33 Track 1 disposition paths were executed through `live_coordinate_run` reusing their exact figures.
   - All 33 paths PASSED (55.24s): `supported-loss`, `unsupported-gain`, `break-even-sale`, exclusions, and incomplete-answer stops produced identical reason findings, dispositions, and Schedule 1 top-entry amounts as the current v46 rule.

---

## 2. Shown Without Recomputation

### 2.1 Current Presentation Reader Inspection
Inspection of `packages/derivation/presentation_projection.py` reveals that intermediate derived computation amounts are **not** projected into presentation models by standard form-field rows:
1. **Schedule 1 Top-Entry (`form-field.v3`)**:
   - In `packages/derivation/presentation_projection.py:486-540` (`_resolve_field_row`), for `disposition == "published"`, line 523 converts the field's bound finding to a numeric value (`value = _numeric_value(finding["value"], symbol=finding["symbol"])`).
   - Line 524 calls `_raw_leaves(finding["pins"], publications_by_id=publications_by_id, state=state, root_id=finding_id)`.
   - In `packages/derivation/presentation_projection.py:402-426` (`_leaf_pins`), the reader recursively walks `finding["pins"]` and **discards all intermediate derived findings** (lines 421-423: `derived = publications_by_id.get(finding_id); if derived is not None: leaves |= _leaf_pins(...)`). Only non-derived input assertions are collected for citation sites (lines 527-536).
   - In the resulting section dictionary (`top_entry_field["resolved"]`), the dictionary contains only `disposition`, `value` (e.g. `880`), and `act`. None of the intermediate computation amounts (`amount-realized`, `selling-expenses`, `net-proceeds`, `adjusted-basis`) appear.
2. **Unresolved Sentinel Field (`form-field.v3`)**:
   - On a gain stop (`unsupported-gain`), the unresolved rule blocks by design (`value: {"op": "block", "code": "DEPENDENCY_ABSENT"}`).
   - In `packages/derivation/presentation_projection.py:497-499`:
     ```python
     if disposition == "blocked":
         codes = [row["code"]] if "code" in row else []
         return {"disposition": "blocked", "activeCodes": codes, "act": None}, []
     ```
   - Because `act` is set to `None`, no finding is attached.
   - In `packages/derivation/presentation_projection.py:3236-3243` and `219-395` (`_selection_blocked_reasons`), the reader inspects the reason rule finding pinned by the selection path and extracts only the descriptive sentence matching `oneOf.description` (e.g., `"The sale resulted in a gain or profit, which cannot be reported as a personal item loss on Schedule 1."`). No computation amounts or labels appear.

### 2.2 Precedent: Mortgage Interest Explanation (`946b5b6a`)
The precedent for retaining a rich structured account of statement determinations without recomputation is commit `946b5b6a3d3a18c2de0741e6da205188a26ef561` (*"Name uncertain and unsupported mortgage conditions (core calculations v45)"*).

Rather than attempting to force intermediate computation amounts into generic form-field definitions, `946b5b6a` implemented:
1. `_mortgage_interest_explanation` (`packages/derivation/presentation_projection.py:2292-2428`) and `_mortgage_basis_answers` (`packages/derivation/presentation_projection.py:1345-1510`).
2. The reader locates the reason publication for the statement, traverses its pinned findings, and queries `exact_types` from `resolved_members` to resolve titles and categorical `responseLabel` values.
3. The reader attaches a dedicated, structured account directly to `presentation["mortgageInterestExplanation"]`.
4. **Zero Recomputation**: The reader performs no arithmetic. It reads recorded strings and numbers directly from published findings, assembling them into an auditable account.

### 2.3 The Smallest Reader Change: Projection of Recorded Computation and Comparison
To ensure the presentation reader never recomputes or re-compares numbers, the reader change is designed as follows:

1. **Target Files and Functions**:
   - `packages/derivation/presentation_projection.py`: helper `_f1099k_statement_computation(reason_finding, publications_by_id)` integrated into statement presentation projection.
   - `packages/tax/f1099k_statement_review.py`: helper `statement_computation_review(reason_finding, publications_by_id)`.

2. **What the Reader Reads**:
   - Locates the statement's published reason finding (`tax.us.2025.f1099k.statement-loss-reason`).
   - Walks `reason_finding["pins"]` directly to identify the 4 computation findings by symbol (`amount-realized`, `selling-expenses`, `net-proceeds`, `adjusted-basis`).
   - For each finding ID, retrieves the published record from `publications_by_id`.
   - Reads the recorded finding value:
     - If numeric: formats as decimal amount (e.g. `800.0`).
     - If `"not-computed"` (or if missing): records as `None` (uncomputed).
   - Reads the published reason category (`reason_finding["value"]`) to state which comparison held:
     - `"supported-loss"` -> `"net-proceeds < adjusted-basis"`
     - `"unsupported-gain"` -> `"net-proceeds > adjusted-basis"`
     - `"break-even-sale"` -> `"net-proceeds == adjusted-basis"`
     - Any named stop code -> `None` (comparison not reached due to named stop)

3. **Populating the Structured Computation Block**:
   ```json
   {
     "amountRealized": 800.0,
     "sellingExpenses": 80.0,
     "netProceeds": 720.0,
     "adjustedBasis": 1000.0,
     "comparison": "net-proceeds < adjusted-basis",
     "assumptionsUsed": []
   }
   ```
   If any figure is uncomputed (e.g. in a missing-answer stop), the respective key is `None`, and the reason code/sentence explains why.

4. **Contract Guarantees**:
   - **No Python Comparison**: The reader never executes comparison operators (`<`, `>`, `==`) against computation amounts. The comparison displayed is strictly derived from the reason category published by the engine rule.
   - **No Python Arithmetic**: Presentation code contains zero arithmetic operators (`+`, `-`, `*`, `/`).
   - **Single Source of Truth**: The displayed figures and the displayed comparison originate from the exact same engine publications that decided the return's top-entry Schedule 1 amount.

---

## 3. The Design in Enumerated Citizens

### 3.1 Candidate Fact Types
Admitted in successor bundle `tax.us.2025.f1099k.vocabulary` (`version: "v2"`):
1. `tax.us.2025.f1099k.amount-realized` (`version: "v1"`):
   - Schema: `fact-type.v2`
   - Identity keys: `payer` (`tax.us.1099k-platform`), `statement` (`tax.us.1099k-statement`), `tax-year` (`"2025"`).
   - Value schema: `{"oneOf": [{"type": "number", "minimum": 0}, {"type": "string", "enum": ["not-computed"]}]}`.
   - Categories: `["not-computed"]`.
   - Title: "Amount realized from single personal item sale".
2. `tax.us.2025.f1099k.selling-expenses` (`version: "v1"`):
   - Schema: `fact-type.v2`
   - Identity keys: `payer`, `statement`, `tax-year`.
   - Value schema: `{"oneOf": [{"type": "number", "minimum": 0}, {"type": "string", "enum": ["not-computed"]}]}`.
   - Categories: `["not-computed"]`.
   - Title: "Selling expenses for single personal item sale".
3. `tax.us.2025.f1099k.net-proceeds` (`version: "v1"`):
   - Schema: `fact-type.v2`
   - Identity keys: `payer`, `statement`, `tax-year`.
   - Value schema: `{"oneOf": [{"type": "number"}, {"type": "string", "enum": ["not-computed"]}]}`.
   - Categories: `["not-computed"]`.
   - Title: "Net proceeds from single personal item sale".
4. `tax.us.2025.f1099k.adjusted-basis` (`version: "v1"`):
   - Schema: `fact-type.v2`
   - Identity keys: `payer`, `statement`, `tax-year`.
   - Value schema: `{"oneOf": [{"type": "number", "minimum": 0}, {"type": "string", "enum": ["not-computed"]}]}`.
   - Categories: `["not-computed"]`.
   - Title: "Adjusted basis of personal item".

### 3.2 Candidate Computation Rules
All rules are authored under schema `rule-artifact.v14`, role `"computation"`, subject `tax.us.2025.f1099k.box1a-gross-amount`:
1. `tax.us.2025.rule.f1099k-amount-realized` (`version: "v1"`):
   - Requires: `agreed-item-price`, `shipping-arrangement`, `refund-amount`, `buyer-paid-shipping`.
   - Evaluates:
     - If `agreed-item-price` in `["not-asked", "cannot-tell"]` or `shipping-arrangement` in `["not-asked", "cannot-tell"]` or `refund-amount` in `["not-asked", "cannot-tell"]` or (`shipping-arrangement == "seller-received-shipping"` and `buyer-paid-shipping` in `["not-asked", "cannot-tell"]`):
       Publishes category literal `not-computed`.
     - Else:
       Publishes numeric formula `(agreed-item-price + (buyer-paid-shipping if shipping-arrangement == "seller-received-shipping" else 0)) - refund-amount`.
   - Publishes: `tax.us.2025.f1099k.amount-realized`.
2. `tax.us.2025.rule.f1099k-selling-expenses` (`version: "v1"`):
   - Requires: `shipping-arrangement`, `platform-fees`, `seller-paid-shipping`.
   - Evaluates:
     - If `platform-fees` in `["not-asked", "cannot-tell"]` or `shipping-arrangement` in `["not-asked", "cannot-tell"]` or (`shipping-arrangement` in `["seller-received-shipping", "none"]` and `seller-paid-shipping` in `["not-asked", "cannot-tell"]`):
       Publishes category literal `not-computed`.
     - Else:
       Publishes numeric formula `platform-fees + (seller-paid-shipping if shipping-arrangement in ["seller-received-shipping", "none"] else 0)`.
   - Publishes: `tax.us.2025.f1099k.selling-expenses`.
3. `tax.us.2025.rule.f1099k-net-proceeds` (`version: "v1"`):
   - Requires: `amount-realized`, `selling-expenses`.
   - Evaluates:
     - If `amount-realized == "not-computed"` or `selling-expenses == "not-computed"`:
       Publishes category literal `not-computed`.
     - Else:
       Publishes numeric formula `amount-realized - selling-expenses`.
   - Publishes: `tax.us.2025.f1099k.net-proceeds`.
4. `tax.us.2025.rule.f1099k-adjusted-basis` (`version: "v1"`):
   - Requires: `purchase-cost`, `cost-basis-known`, `lasting-improvements-or-adjustments`.
   - Evaluates:
     - If `cost-basis-known != "yes"` or `lasting-improvements-or-adjustments != "no"` or `purchase-cost` in `["not-asked", "cannot-tell"]`:
       Publishes category literal `not-computed`.
     - Else:
       Publishes numeric formula `purchase-cost`.
   - Publishes: `tax.us.2025.f1099k.adjusted-basis`.

### 3.3 Reason Rule Successor
- `tax.us.2025.rule.f1099k-statement-loss-reason` (`version: "v2"`):
  - Requires: 4 computed symbols (`amount-realized`, `selling-expenses`, `net-proceeds`, `adjusted-basis`) plus 15 raw circumstance answers.
  - Structure:
    - Maintains the complete 15-circumstance raw answer check for named stops in identical order and tokens as v46.
    - Contains **zero inline arithmetic**.
    - On the fully-answered branch:
      - Checks `computed_ready` (verifying `amount-realized != "not-computed"` and `selling-expenses != "not-computed"`, thereby accessing and pinning both intermediate symbols).
      - Directly compares published `net-proceeds` and `adjusted-basis`:
        - `net-proceeds < adjusted-basis` -> publishes `supported-loss`
        - `net-proceeds > adjusted-basis` -> publishes `unsupported-gain`
        - Else -> publishes `break-even-sale`
  - Pins the raw circumstance facts and all 4 computation findings directly via AST access.

### 3.4 Package, Registry, and Release Hierarchy
- Package: `tax.us.2025.package.core-calculations` (`version: "v47"`):
  - Admits `tax.us.2025.f1099k.vocabulary` `v2`.
  - Admits the 4 computation rules.
  - Retains all input bindings and defaults.
- Registry: `published-packages.v45.json` (pointing to package `v47`).
- Release: `demo.release.sli-worksheet-integration.2025.v45.json` (pointing to registry `v45`).

### 3.5 Test Migration Plan
In adherence to ADR-0003:
- **Prior Published History**:
  - `package.core-calculations.v45.json` and release `v43` remain immutable.
  - `package.core-calculations.v46.json` and release `v44` remain immutable.
- **Active Tests Migrating to `v45`**:
  - `tests/test_f1099k_personal_item_sale_track1.py`: Updates fixture adoption to release `v45` and package `v47`.
  - `tests/test_f1099k_statement_recording.py`: Updates fixture adoption to release `v45`.
  - `tests/test_f1099k_statement_review.py`: Updates fixture adoption to release `v45` and verifies projection of recorded computation figures.
  - `tests/test_f1099k_computation_rules.py` (new in Track 3): Tests the 4 computation rules across all shipping arrangements and refund variations.

---

## 4. Explanation Wording for the Four Cases

Every explanation below cites verbatim 2025 IRS instructions (`i1040gi--2025.txt`) and explicitly verifies that no assumption was used.

### 4.1 Case 1: Supported Loss (e.g. Probe Path 5)
- **Primary Source (Verbatim IRS 2025 Schedule 1 Instructions, `i1040gi--2025.txt`, lines 6366-6376, 6378-6385)**:
  > *"If, for tax year 2025, you received a Form(s) 1099-K that shows payments that were included in error (for example, money for gifts or reimbursements) or for personal items that you sold at a loss (for example, an old refrigerator), enter the amount that was included in error or for personal items sold at a loss in the entry space at the top of Schedule 1."*\
  > *"• If the entire amount reported to you on Form(s) 1099-K was in error or for personal items sold at a loss, enter the total amount from Form(s) 1099-K, box 1(a), in the entry space at the top of Schedule 1."*
- **Saved Explanation Text**:
  > **Form 1099-K Personal Item Sale Loss Determination**\
  > **Platform:** Synthetic platform (`demo.platform.a`)\
  > **Statement:** Synthetic Form 1099-K (`demo.stmt.a`)\
  > **Reported Box 1a Gross Amount:** $880.00
  >
  > **Recorded Transaction Computation:**\
  > - Agreed Item Price: $800.00
  > - Buyer-Paid Shipping (Platform pass-through, not received by seller): $24.00
  > - Sales Tax Collected by Platform: $56.00
  > - Refunds Given Back: $0.00
  > - **Amount Realized:** $800.00 (Published finding `tax.us.2025.f1099k.amount-realized`)
  > - Platform Selling Fees: $80.00
  > - Seller-Paid Shipping: $0.00
  > - **Selling Expenses:** $80.00 (Published finding `tax.us.2025.f1099k.selling-expenses`)
  > - **Net Proceeds from Sale:** $720.00 (Published finding `tax.us.2025.f1099k.net-proceeds`)
  > - Original Purchase Cost: $1,000.00
  > - Lasting Improvements: None ($0.00)
  > - **Adjusted Basis:** $1,000.00 (Published finding `tax.us.2025.f1099k.adjusted-basis`)
  >
  > **Disposition:**\
  > Because the net proceeds ($720.00) are less than the adjusted basis ($1,000.00) (as established by published reason `supported-loss`), this transaction resulted in a nondeductible personal loss of $280.00. Pursuant to IRS Schedule 1 instructions, the gross payment amount reported in Box 1(a) ($880.00) is entered in the entry space at the top of Schedule 1.
  >
  > **Assumptions used: None.**

### 4.2 Case 2: Supported Zero (Closed-Empty Horizon / No Statements Received)
- **Primary Source (Verbatim IRS 2025 Schedule 1 Instructions, `i1040gi--2025.txt`, line 6366)**:
  > *"If, for tax year 2025, you received a Form(s) 1099-K that shows payments that were included in error... or for personal items that you sold at a loss... enter the amount..."*
- **Saved Explanation Text**:
  > **Schedule 1 Top-Entry Determination**\
  > **Reported Form 1099-K Statements:** None (Source family `tax.us.2025.f1099k` closed empty).
  >
  > **Disposition:**\
  > No Form 1099-K statements showing personal item sales or reportable payment card transactions were received for tax year 2025. Consequently, the entry space at the top of Schedule 1 evaluates to $0.00.
  >
  > **Assumptions used: None.**

### 4.3 Case 3: Gain Stop (`unsupported-gain`)
- **Primary Source (Verbatim IRS 2025 Schedule 1 Instructions, `i1040gi--2025.txt`, lines 6348-6353)**:
  > *"If you received a Form 1099-K for a personal item that you sold at a gain, don't report this amount in the entry space at the top of Schedule 1; instead, report it as you would report any other capital gain on Form 8949 and Schedule D."*
- **Saved Explanation Text**:
  > **Form 1099-K Personal Item Sale Determination: Gain Out of Scope**\
  > **Platform:** Synthetic platform (`demo.platform.a`)\
  > **Statement:** Synthetic Form 1099-K (`demo.stmt.a`)\
  > **Reported Box 1a Gross Amount:** $1,200.00
  >
  > **Recorded Transaction Computation:**\
  > - Agreed Item Price: $1,200.00
  > - Refunds Given Back: $0.00
  > - **Amount Realized:** $1,200.00 (Published finding `tax.us.2025.f1099k.amount-realized`)
  > - Platform Selling Fees: $100.00
  > - **Selling Expenses:** $100.00 (Published finding `tax.us.2025.f1099k.selling-expenses`)
  > - **Net Proceeds from Sale:** $1,100.00 (Published finding `tax.us.2025.f1099k.net-proceeds`)
  > - Original Purchase Cost: $800.00
  > - Lasting Improvements: None
  > - **Adjusted Basis:** $800.00 (Published finding `tax.us.2025.f1099k.adjusted-basis`)
  >
  > **Disposition:**\
  > The net proceeds from the sale ($1,100.00) exceed the adjusted basis of the item ($800.00) (as established by published reason `unsupported-gain`), resulting in a taxable capital gain of $300.00. Under IRS Schedule 1 instructions: *"If you received a Form 1099-K for a personal item that you sold at a gain, don't report this amount in the entry space at the top of Schedule 1; instead, report it as you would report any other capital gain on Form 8949 and Schedule D."*
  >
  > Because reporting personal item gains on Form 8949 / Schedule D is outside the scope of this return module, this statement is unresolved and blocked (`unsupported-gain`). The return's income does not yet account for this Form 1099-K statement, and no amount is entered at the top of Schedule 1.
  >
  > **Assumptions used: None.**

### 4.4 Case 4: Missing-Answer Stop (`platform-fees-unanswered`)
- **Primary Source (Verbatim IRS 2025 Schedule 1 Instructions, `i1040gi--2025.txt`, line 6348-6353, 6366-6376)**:
  > *"If you received a Form 1099-K for a personal item that you sold at a gain, don't report this amount in the entry space at the top of Schedule 1; instead, report it as you would report any other capital gain on Form 8949 and Schedule D."*
- **Saved Explanation Text**:
  > **Form 1099-K Personal Item Sale Determination: Incomplete Circumstances**\
  > **Platform:** Synthetic platform (`demo.platform.a`)\
  > **Statement:** Synthetic Form 1099-K (`demo.stmt.a`)\
  > **Reported Box 1a Gross Amount:** $880.00
  >
  > **Recorded Circumstances Status:**\
  > - Platform Selling Fees: Unanswered (`not-asked`)
  > - **Amount Realized:** $800.00 (Published finding `tax.us.2025.f1099k.amount-realized`)
  > - **Selling Expenses:** Not computed (`not-computed` token published; platform selling fees unanswered)
  > - **Net Proceeds:** Not computed (`not-computed` token published; selling expenses not computed)
  > - **Adjusted Basis:** $1,000.00 (Published finding `tax.us.2025.f1099k.adjusted-basis`)
  >
  > **Disposition:**\
  > The question regarding platform selling fees has no current answer (`platform-fees-unanswered`). Without platform selling fees, selling expenses and net proceeds cannot be computed, and no comparison is performed. The return cannot determine whether the sale resulted in a nondeductible loss or a taxable capital gain.
  >
  > Because this statement is unresolved, the return's income does not yet account for this Form 1099-K statement, and no amount is entered at the top of Schedule 1.
  >
  > **Assumptions used: None.**
