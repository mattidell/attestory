# D1 — Connected Account for a Personal Item Sold at a Loss

- **Launch**: D1 launch (branch `milestone/personal-item-sale-circumstances-translation`).
- **Charter**: D1 connected account
- **Role & posture**: Builder (D1 connected account). Paper design and static code reading; no production code, schema, fixture, or rule edits.
- **Evidence standard**: Verbatim quotations from 2025 IRS sources (`f1040s1--2025.txt`, `i1040gi--2025.txt`, `f1099k--2024.txt`, `p544--2025.txt`, `p551--2025.txt`); static code reading with exact `file:line` citations; and explicit `[Interpretation]` labels. Does not invent dates, amounts, or counts.
- **Understood scope**: One Form 1099-K statement covering one identifiable sale of an item bought and used personally. When established as sold at a loss, enter Box 1a at the top of Schedule 1 with $0 net tax effect. Gains, break-even sales, multi-sale statements, investment items, and business uses are named as unsupported/excluded and block return publication.
- **Evidence ceiling**: Paper design and static code reading.
- **Stop conditions**: Stop and report if the loss-only shape cannot be made honest, if governance interpretation is required, or if out-of-scope files must be touched.

---

## 1. What the Person Experiences

A person who received a Form 1099-K for selling a personally used item enters their statement, provides an ordinary account of the purchase and sale, and encounters one of six mutually exclusive outcomes for that statement. A statement whose whole Box 1a is a supported personal loss contributes that Box 1a to the 2025 Schedule 1 entry space (with the entry being the sum of Box 1a across all independently supported statements). Every other admitted statement withholds a complete return with a named reason:

```
[Statement Received (Box 1a)]
           │
           ▼
[Single-Sale & Scope Checks] ──(Multi-sale / Investment / Business / Resale / Digital / Box 4 Withholding)──► Outcome 5: Excluded Circumstance
           │
           ▼
[Reconciliation: Agreed Price vs Box 1a] ──(Unexplained Difference)──► Outcome 6: Unexplained Difference
           │
           ▼
[Cost Basis & Adjustment Checks] ──(Unknown Basis / Unanswered / Improvements / Rebates)──► Outcome 4: Unresolved "Can't Tell" or Unanswered
           │
           ▼
[Economic Comparison: Net Proceeds vs Purchase Cost]
           ├───────────────────────────┬───────────────────────────┐
           ▼                           ▼                           ▼
Outcome 1: Supported Loss     Outcome 2: Unsupported Gain   Outcome 3: Break-Even Sale
(Schedule 1 top entry: Box 1a)   (Named stop: gain unhandled)  (Named stop: break-even unhandled)
```

1. **Outcome 1: Supported Loss Result**
   - **What it shows**: The statement is reconciled. The comparison proves the item sold for less than its purchase cost. The Form 1099-K Box 1a amount is reported in the 2025 Schedule 1 top entry space (summed across all supported statements). Schedule 1 attaches to Form 1040. Form 1040 line 8, line 9, and the tax lines are unchanged ($0.00 net tax effect).
   - **What it asks the person to do**: Review the explanation, confirm the figures, and proceed to file.

2. **Outcome 2: Unsupported Gain**
   - **What it shows**: The comparison indicates that net proceeds exceed cost (taxable gain). The application states that reporting capital gains from Form 1099-K requires Form 8949 and Schedule D, which this milestone does not support.
   - **What it asks the person to do**: Use an external tax preparation route or specialized filing software that supports Form 8949 Boxes C/F and Schedule D for personal-item gains.

3. **Outcome 3: Break-Even Sale (Unsupported)**
   - **What it shows**: The comparison indicates that net proceeds equal cost (break-even). The application states that reporting break-even sales from Form 1099-K requires Form 8949 with adjustment code L, which this milestone does not support.
   - **What it asks the person to do**: Use an external filing route supporting Form 8949 break-even reporting.

4. **Outcome 4: Unresolved "Can't Tell" or Unanswered**
   - **What it shows**: A required factual determination could not be completed because a question was left unanswered, an answer was withdrawn leaving it unanswered, or the person selected "I can't tell" (e.g., unknown purchase cost, unknown buyer payment, or unknown acquisition mode). Under product posture grounded in IRS rules, unknown basis cannot be assumed zero.
   - **What it asks the person to do**: Locate purchase receipts, platform account summaries, or bank records before proceeding.

5. **Outcome 5: Excluded Circumstance**
   - **What it shows**: The transaction involves an excluded circumstance: personal use not affirmed (the allowing answer is strictly personal use: no business use, no rental use, no holding to resell or make money, and no mixed use); acquired other than by purchase (gift under `26 U.S.C. § 1015`, inheritance under `§ 1014`); acquired for resale or as inventory under `§ 1221(a)(1)` (`RESALE_OR_INVENTORY_EXCLUDED`); bought mainly as an investment or to make a profit (which under `§ 165(c)(2)` may be a deductible loss on Form 8949/Schedule D, stopping with `INVESTMENT_PURPOSE_EXCLUDED`); prior business/rental use requiring depreciation recapture (`PRIOR_DEPRECIABLE_USE_EXCLUDED`); a digital asset (reported on Form 8949 Boxes G through L, stopping with `DIGITAL_ASSET_EXCLUDED`); a statement covering multiple sales (`MULTI_SALE_STATEMENT_UNSUPPORTED`); or backup withholding in Box 4 (`BACKUP_WITHHOLDING_UNSUPPORTED`). For each excluded purpose, the explanation states that this route does not support it; deductible capital-loss treatment is stated only for the profit-transaction answer.
   - **What it asks the person to do**: File using the appropriate investment, business (Schedule C), rental (Schedule E), or capital asset schedule.

6. **Outcome 6: Unexplained Difference Between Box 1a and Account**
   - **What it shows**: Form 1099-K Box 1a does not match the agreed item price, and the difference is not accounted for by components charged to the buyer (platform-collected sales tax or buyer-paid shipping). The explanation states that the application cannot tell which part of Box 1a is the personal item, so it enters no amount on Schedule 1 and withholds a complete return.
   - **What it asks the person to do**: Inspect the platform's annual seller report to reconcile the gross charge before completing the return.

---

## 2. What Establishes "Sold at a Loss" (Central Product Choice)

We compare two evaluation approaches on paper across five edge cases:

| Criterion / Scenario | Approach (a): Recorded Amounts & Derived Comparison | Approach (b): Ordinary Categorical Comparison Question |
| --- | --- | --- |
| **Mechanics** | Ask exact purchase cost, agreed item price, fees, shipping received/paid, refunds, and adjustments. Use one comparison: Amount realized is the agreed price, plus buyer-paid shipping the seller received, minus refunds. Selling expenses are platform fees, plus the label only when the seller received that shipping, plus shipping the seller paid and the buyer was not charged. Net proceeds = Amount Realized − Selling Expenses. A loss is that net amount below adjusted basis, and only when Q12 is "no" (where purchase cost is adjusted basis). | Ask: *"After the platform's fees and anything you refunded, did you get back less than you paid to buy the item?"* with `{yes, no, cannot-tell}`. Separately ask presence of improvements/rebates. |
| **Tax Facts Established** | Proves amount realized (`26 U.S.C. § 1001(b)`), cost basis (`§ 1012`), and nondeductible loss (`§ 165(c)`). Retains auditable dollar quantities. | Establishes only the sign of the transaction ($\Delta < 0$). Does not record basis or proceeds figures. |
| **What It Cannot Establish** | Cannot proceed if the person cannot state an exact purchase cost, even if they know the sale was an obvious loss. | Cannot verify arithmetic; cannot detect if the user forgot sales tax, fees, or refunds in their mental math. |
| **Disguised Tax Conclusion?** | **No**. Asks purely factual transaction events. The engine performs all tax characterization and arithmetic. | **Risk of disguised conclusion**. Asking whether one "got back less than you paid" requires the filer to decide what counts as "what you paid" (e.g., sales tax, freight) and "got back" (net vs gross). |
| **Platform Fees & Shipping** | Deterministic under the single comparison: platform fees and seller-paid shipping reduce amount realized to net proceeds. Compared against adjusted basis $\rightarrow$ Loss. | Person must perform multi-step mental arithmetic to evaluate if $800 − $85 − $40 < $1,000. |
| **Subsequent Refunds** | Deterministic: refund ($100) reduces amount realized. Net proceeds reduced accordingly vs adjusted basis $\rightarrow$ Loss. | Person must factor the refund into their mental comparison. |
| **Improvements & Rebates** | Gated or itemized: improvement increases basis; rebate reduces basis (`Pub. 551`, pp. 2–3). When Q12 is "no", purchase cost is adjusted basis. | Must ask separate absence questions; if present, the qualitative question collapses. |
| **Behavior on Correction** | If cost is corrected from $1,200 to $600 against $700 proceeds, engine automatically flips from Loss to Gain, triggering the unsupported stop. | User must be re-prompted to re-evaluate their mental comparison. |

- **Provisional Choice: Approach (a) (Amounts)**.
  - **Reason**: Aligns directly with `OWNER_MODEL.md:133-135` (*"avoid offloading knowledge of the tax significance of life events to the user... maintaining records the engine can use"*). It eliminates user math errors on platform fees and refunds, automatically detects boundary crossings upon correction, and maintains an auditable record.
  - **Alternative Displaced**: Approach (b) (Categorical comparison), which offloads multi-component arithmetic to the filer and cannot verify the integrity of the loss condition.
  - **Rule on Basis**: Unknown cost basis is **never defaulted to zero**, maintained as the product posture (grounded in `2025 Instructions for Form 8949`, p. 2; `2025 Pub. 544`, p. 4; `p0a-review.md:37-42`, which require a known basis and provide no authority to substitute zero). An unknown cost blocks determination with `COST_BASIS_UNKNOWN`.

---

## 3. The Amount That Reaches the Return

### 3.1 Primary Source Authority
From `2025 Schedule 1 (Form 1040)`, page 1 (`f1040s1--2025.txt:11-14`):
> *"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .*
> *Note: The remaining amounts reported to you on Form(s) 1099-K should be reported elsewhere on your return depending on the nature of the transaction. See www.irs.gov/1099k."*

From `2025 Instructions for Form 1040`, Schedule 1 instructions, page footer 88 (`i1040gi--2025.txt:6380-6385`):
> *"• If the entire amount reported to you on Form(s) 1099-K was in error or for personal items sold at a loss, enter the total amount from Form(s) 1099-K, box 1(a), in the entry space at the top of Schedule 1."*

From the Schedule 1 instructions example (`i1040gi--2025.txt:6375-6380`):
> *"Example–Personal item sold at a loss. You bought a couch for $1,000 and sold it through a third-party vendor for $700, which was reported in box 1(a) of your Form 1099-K. You would enter $700 in the entry space at the top of Schedule 1."*

### 3.2 Schedule 1 Entry Amount vs. Loss Determination Amounts and Shipping Trace
- `[Interpretation]` On a single-sale statement where the sale is confirmed to be at a loss, the entire statement amount is for a personal item sold at a loss. Therefore, **the amount entered at the top of Schedule 1 is Box 1a in full**. Where multiple Form 1099-K statements are admitted, the Schedule 1 entry is the sum of Box 1a for every statement that independently establishes a personal loss; any other admitted Form 1099-K blocks publication.
- The Schedule 1 entry is an IRS matching figure; it does **not** equal net proceeds, cost basis, or the economic loss amount.
- **Box 1a Reconciliation Rule (`p0-review.md:17-19`)**: Box 1a is the unreduced gross charge determined on the transaction date (`Instructions for Form 1099-K (Rev. March 2024)`, p. 4). Only charges actually added to the buyer's payment explain why Box 1a exceeds the agreed item price:
  $$\text{Box 1a} = \text{Agreed Item Price} + \text{Platform-Collected Sales Tax} + \text{Buyer-Paid Shipping}$$
  Seller platform fees are deductions from the seller payout, not amounts added to the buyer charge. Refunds the seller later gives back reduce amount realized (`26 U.S.C. § 1001(b)`), but do not alter Box 1a and do not explain a Box 1a excess.
- **Buyer-Paid Shipping Treatment**:
  - `[Interpretation]` Whether buyer-paid shipping is part of amount realized depends on whether the seller actually received the shipping money, evaluated under the single comparison:
    1. **Platform-managed pass-through shipping**: The platform charges shipping to the buyer and retains it directly to issue the label. The seller never receives the shipping funds. The shipping is a pass-through, **NOT part of the seller's amount realized**. The seller incurs no shipping expense; the label cost is **NOT** deducted under Q9.
    2. **Seller-received shipping**: The platform disburses the buyer's shipping payment to the seller. Under `26 U.S.C. § 1001(b)`, shipping received is **part of amount realized**. The cost of the shipping label paid by the seller is a **selling expense** deducted under Q9 (`2025 Instructions for Form 8949`, p. 6).
    The questionnaire asks which arrangement occurred. This avoids double-counting: label cost is deducted only when shipping was included in gross proceeds / amount realized.
- **Worked Trace (Camera Sale)**:
  - **Facts**: Seller bought a camera for `$1,200.00`. In 2025, seller agrees to sell it for `$800.00`. The platform charges the buyer `$56.00` state sales tax (remitted by platform) and `$24.00` shipping. The PSE settles `$880.00` in Box 1a (`$800 + $56 + $24`). Platform deducts `$80.00` seller commission.
  - **Reconciliation**:
    $\text{Box 1a } (\$880.00) = \text{Agreed Price } (\$800.00) + \text{Platform Sales Tax } (\$56.00) + \text{Buyer Shipping } (\$24.00)$. Reconciled.
  - **Loss Determination (Single Comparison)**:
    - *Under Platform Pass-Through Shipping (Platform retained $24)*:
      Amount realized = `$800.00`.
      Selling expenses = `$80.00` (commission only).
      Net proceeds = $\$800.00 - \$80.00 = \$720.00$.
      Adjusted basis (cost basis when Q12 is "no") = `$1,200.00`.
      Loss = $\$720.00 - \$1,200.00 = -\$480.00$. Condition established.
    - *Under Seller-Received Shipping (Seller received $24 and bought $24 label)*:
      Amount realized = `$800.00 + $24.00 = $824.00`.
      Selling expenses = `$80.00` (commission) + `$24.00` (label) = `$104.00`.
      Net proceeds = $\$824.00 - \$104.00 = \$720.00$.
      Adjusted basis (cost basis when Q12 is "no") = `$1,200.00`.
      Loss = $\$720.00 - \$1,200.00 = -\$480.00$. Condition established.
  - **Return Reporting**:
    Schedule 1 top-of-form entry space: **`$880.00`** (Box 1a in full, or sum across all supported statements).
    Form 1040 line 8: **unchanged** (top entry space does not flow to Part I line 10; line 8, line 9, and the tax lines are unchanged, with $0.00 net tax effect).

---

## 4. Identities and What Answers Attach To

### 4.1 Required Entities
1. **Filer / Filing Unit**: The taxpayer(s) filing the Form 1040.
2. **Statement**: A furnished Form 1099-K information return, keyed deterministically by `StatementKey(payer_id, tax_year, payer_ref)` (`packages/tax/statements.py:32-39`).
3. **Item**: The physical personal property (description, purchase cost, use history).
4. **Sale**: The disposition event (agreed price, fees, refunds, reconciliation).

`[Provisional Choice]`: For this bounded single-sale milestone (1 statement : 1 sale : 1 item), answers in the ActLog are scoped to the `statement_keys` (`payer`, `statement`, `tax-year`), exactly matching the pattern in `packages/tax/f1098_statement_recording.py:123-146`. D2 will decide whether to introduce explicit `item_id` / `sale_id` keys.

### 4.2 Code Readings and Invariants
- `packages/tax/statements.py:41-53`: Rejects evidence markers (`_EVIDENCE_MARKERS`, line 21). `classify_assertion` (lines 61–85) classifies `NEW_ORIGINAL`, `CORRECTION`, or `DUPLICATE`.
- `packages/tax/f1098_statement_recording.py:123-135`: `_require_current_statement` asserts `len(sources) == 1 and len(all_sources) == 1` (line 133). For Form 1099-K, currency must be scoped to the specific statement key rather than asserting return-wide uniqueness.
- **Invariant**: **Never retarget an affirmed answer to a different sale.** Answers given about an item sold on eBay statement A cannot be automatically attached to statement B.

### 4.3 Staleness and Invalidation Triggers
- **Corrected Statement (Amended Box 1a)**: Re-runs the reconciliation equation and updates the Schedule 1 entry amount. Does **not** invalidate item purchase cost or agreed sale price if records remain unchanged.
- **Second Statement from Another Platform**: Individuated as a separate `StatementKey`. Does not invalidate or overwrite answers on the first statement. Each statement's answers stay on that statement. The Schedule 1 entry is the sum of Box 1a for every statement that independently establishes a personal loss. Any other admitted Form 1099-K blocks publication.
- **Change in Single-Sale Coverage**: If the user changes statement coverage from "only this sale" to "includes other sales", the 1:1 binding fails. All sale conclusions are invalidated; the route stops with `MULTI_SALE_STATEMENT_UNSUPPORTED`.

---

## 5. The Finite Ordinary Questions

| # | Plain-Language Question | Offered Choices | Normalized Value | Tax Proposition Supported | Exclusion / Stop Behavior |
| --- | --- | --- | --- | --- | --- |
| **Q1** | *"Does this Form 1099-K report payments from only this single item sale?"* | • Yes, only this sale<br>• No, includes other sales/transactions<br>• I can't tell | `only-this-sale`<br>`multiple-sales`<br>`cannot-tell` | Single-sale reconciliation boundary (`2025 Instructions for Form 1040`, Schedule 1, p. 88, entire-amount vs partial-amount bullets). | `No` or `Can't tell` stops: `MULTI_SALE_STATEMENT_UNSUPPORTED`. |
| **Q2** | *"What was the item you sold?"* | Short text (e.g. `"dining table"`), or blank | string | Context for saved explanation and user review; no tax characterization effect. | Optional; empty text defaults to `"personal item"`. **No stop.** |
| **Q3** | *"How did you acquire this item?"* | • I bought it<br>• Received as a gift<br>• Inherited it<br>• Acquired for resale/inventory<br>• I can't tell | `purchased`<br>`gift`<br>`inherited`<br>`resale-inventory`<br>`cannot-tell` | Cost basis under `26 U.S.C. § 1012`. Distinguishes gift (`§ 1015`), inheritance (`§ 1014`), inventory (`§ 1221(a)(1)`). | Any choice other than `purchased` stops: `ACQUISITION_MODE_UNSUPPORTED`. |
| **Q4** | *"Did you use this item personally in your everyday life, or was it used for business/rental, bought to resell, or bought as an investment?"* | • Used it personally in my everyday life or household<br>• Acquired or held for resale or as inventory<br>• Bought mainly as an investment or to make money<br>• Used it for business or rental<br>• I can't tell | `personal-use`<br>`resale-inventory`<br>`investment`<br>`business-or-rental`<br>`cannot-tell` | The allowing answer is strictly personal use: no business use, no rental use, no holding to resell or make money, and no mixed use (`26 U.S.C. §§ 165(c), 262(a)`). Distinguishes deductible investment loss (`§ 165(c)(2)`), inventory (`§ 1221(a)(1)`), and depreciable business/rental property subject to Form 4797 Part III recapture (`2025 Instructions for Schedule D`, p. 3). | • `resale-inventory` stops: `RESALE_OR_INVENTORY_EXCLUDED`<br>• `investment` stops: `INVESTMENT_PURPOSE_EXCLUDED` (deductible capital loss under § 165(c)(2) reported on Form 8949/Schedule D)<br>• `business-or-rental` stops: `PRIOR_DEPRECIABLE_USE_EXCLUDED`<br>• `cannot-tell` stops: `PERSONAL_USE_UNCONFIRMED`. For each excluded purpose, the explanation says this route does not support it; deductible capital-loss treatment is stated only for the profit-transaction answer. |
| **Q5** | *"Was this item a digital asset (such as cryptocurrency or NFT)?"* | • No<br>• Yes<br>• I can't tell | `no`<br>`yes`<br>`cannot-tell` | Digital assets must use Form 8949 Boxes G through L (`2025 Instructions for Form 8949`, "Digital Assets", p. 2). | `Yes` or `Can't tell` stops: `DIGITAL_ASSET_EXCLUDED`. |
| **Q6** | *"What was the agreed sale price paid by the buyer?"* | Currency amount (e.g. `$700.00`), or choice `"I can't tell"` | currency / `cannot-tell` | Gross proceeds from property (`26 U.S.C. § 1001(b)`). | `Can't tell` stops: `BUYER_PAYMENT_UNKNOWN`. |
| **Q7** | *"Box 1a is [amount]. What additional charges paid by the buyer were included in that total?"* | • Platform-collected sales tax (amount)<br>• Buyer-paid shipping charged by platform (amount)<br>• None / Box 1a matches price<br>• I can't tell | record of buyer-paid additions | Reconciles Box 1a (`Instructions for Form 1099-K (Rev. March 2024)`, p. 4). Only buyer-paid charges explain Box 1a > price. | Unexplained difference stops: `FORM_1099K_RECONCILIATION_UNEXPLAINED`. |
| **Q8** | *"If the buyer paid shipping, did you receive that shipping money and buy the label yourself, or did the platform keep the shipping money and provide the label?"* | • Platform kept shipping / provided label<br>• I received shipping and bought label<br>• No buyer shipping charged<br>• I can't tell | `platform-pass-through`<br>`seller-received-shipping`<br>`none`<br>`cannot-tell` | Determines whether shipping is part of amount realized (`26 U.S.C. § 1001(b)`) and prevents double-counting label expense under the single comparison. | `Can't tell` stops: `SHIPPING_ARRANGEMENT_UNKNOWN`. |
| **Q9** | *"What selling fees did the platform deduct, or what did you pay out of pocket to ship the item?"* | Currency amount (e.g. `$85.00`), choice `"$0 / None"`, or `"I can't tell"` | currency / `cannot-tell` | Selling expenses reducing amount realized to net proceeds under the single comparison (`2025 Instructions for Form 8949`, p. 6; `2025 Pub. 544`, p. 4): platform fees, plus the label only when the seller received that shipping, plus shipping the seller paid and the buyer was not charged. | `Can't tell` stops: `SELLING_EXPENSES_UNKNOWN`. |
| **Q10** | *"Did you issue any refund to the buyer?"* | Currency amount (e.g. `$0.00`), or choice `"I can't tell"` | currency / `cannot-tell` | Reduces amount realized (`26 U.S.C. § 1001(b)`; `p0-review.md:17-19`). | `Can't tell` stops: `REFUND_STATUS_UNKNOWN`. |
| **Q11** | *"What did you pay to purchase the item, including sales tax and delivery?"* | Currency amount (e.g. `$1,000.00`), or choice `"I can't tell"` | currency / `cannot-tell` | Cost basis (`26 U.S.C. § 1012`; `Pub. 551`, pp. 2–3). | `Can't tell` stops: `COST_BASIS_UNKNOWN`. |
| **Q12** | *"Did you make lasting improvements to the item, receive manufacturer rebates, or receive insurance/casualty payouts?"* | • No<br>• Yes<br>• I can't tell | `no`<br>`yes`<br>`cannot-tell` | Basis adjustments under `26 U.S.C. § 1016` (`Pub. 551`, pp. 2–3; `p0-review.md:41-43`). When answer is "no", purchase cost equals adjusted basis. | `Yes` or `Can't tell` stops: `BASIS_ADJUSTMENT_PRESENT_OR_UNKNOWN`. |

### 5.1 Reconsideration of Collectibles (Former Q6)
`[Interpretation]` Under `26 U.S.C. § 1(h)(4)`, the 28% maximum capital gains rate applies exclusively to **gain** on the sale of a collectible. Under `26 U.S.C. §§ 165(c), 262(a)`, a personal loss on a collectible is nondeductible, exactly like any other personally used item. Furthermore, `2025 Instructions for Form 1040`, page 88 (`i1040gi--2025.txt:6366-6376`) admits any personal item sold at a loss to the top entry space of Schedule 1 without exception. Once Q4 explicitly asks and excludes investment or profit-seeking purpose (which routes deductible investment losses to Form 8949/Schedule D under `§ 165(c)(2)`), and Outcome 2 excludes all gains, **no tax reason remains to ask a separate collectible exclusion question for personal-use items sold at a loss**. A personal collectible held for personal enjoyment and sold at a loss qualifies for the Schedule 1 top entry space. Q6 is therefore retired.

- **No Date Questions**: Verified in `p0b-ordinary-account.md:209-213`: Schedule 1 loss route requires no calendar dates (no acquisition date, no sale date, no holding period).
- **Box 4 Backup Withholding**: Recorded on the statement (`Instructions for Form 1099-K (Rev. 03-2024)`, Box 4). The current loader (`packages/tax/loader.py:125-145`) does not enforce Form 1099-K Box 4. The application stops with `BACKUP_WITHHOLDING_UNSUPPORTED` unless Box 4 is absent or zero.

---

## 6. Assumptions

### 6.1 Evaluation of Candidate Defaults
1. **Candidate: Box 3 = 1 implies single sale**: **Rejected**. A single transaction can cover bundled goods, services, or reimbursements. Q1 explicitly asks coverage.
2. **Candidate: Box 1a pre-fills buyer payment**: **Provisional Adoption as prompt default only**. Box 1a is suggested as the agreed price, but becomes a recorded fact only after user confirmation and reconciliation (`p0-review.md:43-44`).
3. **Candidate: Selling expenses default to $0**: **Rejected**. Marketplace sales almost universally incur fees. Q9 requires explicit amount or affirmative `$0`.
4. **Candidate: Cost basis defaults to $0 when unknown**: **Hard Rejection**. Zero basis manufactures artificial gain; tax rules give no authority to assume zero (`2025 Instructions for Form 8949`, p. 2; `2025 Pub. 544`, p. 4).
5. **Candidate: Holding period default**: **Irrelevant**. Holding period does not enter the Schedule 1 loss route.

- **Provisional Choice: Zero-Default Policy**. No silent tax-determining defaults are adopted.
- **Withdrawal Invariant**: Withdrawing an answer must never produce a more favorable result. A withdrawn answer leaves that question unanswered. Unanswered is a named stop on every question except the optional description (`Q2`). The allowing choice is an affirmative current answer.

---

## 7. Outcomes and the Rest of the Return

### 7.1 Outcomes Matrix

| Outcome | Schedule 1 Top Entry | Schedule 1 Attached? | Form 1040 Line 8 | Form 1040 Line 9 (Total Income) | Form 1040 Tax Lines (16, 24) | Return Filing Status |
| --- | --- | --- | --- | --- | --- | --- |
| **1. Supported Loss** | **Box 1a** (or sum across supported statements) | **Yes** | Unchanged ($0 effect) | Unchanged ($0 effect) | Unchanged ($0 effect) | **Complete / Ready to file** |
| **2. Unsupported Gain** | `$0.00` / Blank | No (solely for 1099-K) | Blocked / Incomplete | Blocked | Blocked | **Blocked: `UNSUPPORTED_GAIN_NOT_REPORTED`** |
| **3. Break-Even Sale** | `$0.00` / Blank | No (solely for 1099-K) | Blocked / Incomplete | Blocked | Blocked | **Blocked: `BREAK_EVEN_SALE_UNSUPPORTED`** |
| **4. Unresolved "Can't Tell" or Unanswered** | `$0.00` / Blank | No (solely for 1099-K) | Blocked / Incomplete | Blocked | Blocked | **Blocked: `OPEN_CIRCUMSTANCE_ANSWER` / named unanswered stop** |
| **5. Excluded Circumstance** | `$0.00` / Blank | No (solely for 1099-K) | Blocked / Incomplete | Blocked | Blocked | **Blocked: Named exclusion code** (`INVESTMENT_PURPOSE_EXCLUDED`, `RESALE_OR_INVENTORY_EXCLUDED`, `PRIOR_DEPRECIABLE_USE_EXCLUDED`, `DIGITAL_ASSET_EXCLUDED`, etc.) |
| **6. Unexplained Difference** | `$0.00` / Blank | No (solely for 1099-K) | Blocked / Incomplete | Blocked | Blocked | **Blocked: `FORM_1099K_RECONCILIATION_UNEXPLAINED`** |

### 7.2 Income Blocking Choice
- `[Provisional Choice]`: **When one or more Form 1099-K statements are admitted to the return, the Schedule 1 entry is the sum of Box 1a for every statement that independently establishes a personal loss. Any other admitted Form 1099-K blocks publication (unsupported gain, break-even sale, unresolved or unanswered question, excluded circumstance, or unexplained reconciliation discrepancy). The return's income and tax cannot be published as complete if any admitted statement is not a supported personal loss, because potential taxable income reported to the IRS would otherwise be omitted.**
- **Alternative Displaced**: Publishing the return with a silent omission of the Form 1099-K, which would risk IRS underreporting notices (CP2000).

### 7.3 Interaction with Existing Schedule D and Schedule 1 Boundaries
- **Schedule D Boundaries**:
  - `tax.us.2025.schedule-d-boundary.no-form8949-sources` (`packages/content/tax/2025/schedule-d-boundary.bundle.json:69`): On a supported personal loss, no Form 8949 transaction exists. Filers answer `"yes"`. Unaffected.
  - `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` (`packages/content/tax/2025/schedule-d-boundary-form8949-w.bundle.json:9`): Stays `"yes"`. Unaffected.
  - If a gain occurs, the filer cannot answer `"yes"` to `no-form8949-sources`; routing to Schedule D lines 3/10 fails because they do not exist in `packages/content/tax/2025/rule.schedule-d-line7.v3.json` or `rule.schedule-d-line15.v4.json`.
- **Schedule 1 Boundaries and Rules**:
  - `packages/content/tax/2025/rule.schedule1-line10.json:2-16, 38-96`: Requires all Part I absence facts (`no-sch1-line1-taxable-refunds` through `no-sch1-other-income`, `schedule1-part1-scope.bundle.json:3-99`) to be `"yes"`. The top entry space is above Part I and does not feed line 10. These absence facts remain `"yes"`.
  - `packages/content/tax/2025/rule.form1040-line8.json:18-42`: Publishes `tax.us.2025.income.additional-income` equal to Schedule 1 line 10. Line 8, line 9, and the tax lines are unchanged ($0.00 net tax effect).
  - `packages/content/tax/2025/rule.form1040-line9.v7.json:66-100`: Total income sums W-2, interest, dividends, capital gains, line 8, IRA, and Social Security. Total income is unaffected.
  - `packages/content/tax/2025/rule.attachment.schedule-1.v2.json:166-180`: Currently requires either `tax.us.2025.unemployment.box1-subtotal` or `tax.us.2025.schedule1.line21-sli-deduction` to be strictly greater than zero. Under `packages/derivation/runner.py:1870-1873`, if any symbol in `requirement.subtotals` is absent, the attachment blocks. Therefore, D2 must specify publishing an explicit closed-empty zero when the return has no Form 1099-K, and succeeding `rule.attachment.schedule-1.v2` to `v3` to include the Form 1099-K loss subtotal in `requirement.subtotals` only together with that publication. Asking no new questions, returns with no Form 1099-K preserve their current attachment outcome, while a supported loss with Box 1a > 0 satisfies `runner.py:1897` and attaches Schedule 1.
- **Return with No Form 1099-K**: Remains 100% unchanged. No new questions are asked, and existing boundary facts evaluate identically.

---

## 8. Corrections and Lifecycle Changes

1. **Correcting Cost Basis Across the Gain/Loss Boundary**:
   - Initial: Cost `$1,200`, Net Proceeds `$700` $\rightarrow$ Loss −`$500`. Schedule 1 entry = `$700`. Return complete.
   - Correction: Cost corrected to `$600` via a new finding.
   - Result: Net Proceeds (`$700`) > Cost (`$600`) $\rightarrow$ Gain +`$100`.
   - Effect: Schedule 1 entry is cleared. The transaction transitions from complete to blocked (`UNSUPPORTED_GAIN_NOT_REPORTED`). Return filing is blocked.
2. **Withdrawing the Personal-Use Answer**:
   - A `finding-retracted` act is appended (`packages/tax/f1098_statement_recording.py:399-402`).
   - Retraction displaces the finding without asserting an opposite answer. Under the withdrawal rule (Finding 6), a withdrawn answer leaves the question unanswered. Unanswered is a named stop on every question except the optional description (`Q2`). The route stops with `PERSONAL_USE_UNCONFIRMED`. Schedule 1 entry is cleared; return blocked.
3. **Corrected Statement with Different Box 1a**:
   - Initial: Form 1099-K Box 1a was `$700.00`. The person recorded an agreed sale price of `$700.00`, purchase cost of `$1,000.00`, and `$0.00` sales tax/shipping. Reconciliation succeeded ($\$700 = \$700$). Net proceeds `$700.00` < cost `$1,000.00` yielded a supported loss of `-$300.00`. Schedule 1 top entry showed `$700.00`; return was complete.
   - Issuer Correction Received: Platform issues an amended Form 1099-K correcting Box 1a from `$700.00` to `$650.00`.
   - Immediate Reconciliation Failure: The application re-evaluates reconciliation against the person's existing recorded answers: Box 1a (`$650.00`) does not equal recorded agreed price (`$700.00`), creating an unexplained discrepancy of `-$50.00`. Reconciliation fails. The Schedule 1 top entry is immediately **withdrawn** (cleared to `$0.00`), and return completion is blocked with `FORM_1099K_RECONCILIATION_UNEXPLAINED`.
   - Person Corrects Price: The person checks their platform order records, finds that the agreed item price was actually `$650.00`, and records a corrected price of `$650.00`.
   - Restored Outcome: Reconciliation succeeds: Box 1a (`$650.00`) == Agreed Price (`$650.00`). Economic comparison re-evaluates: Net proceeds (`$650.00`) < Cost (`$1,000.00`) $\rightarrow$ Loss −`$350.00`. The Schedule 1 top entry is restored with the corrected Box 1a amount: **`$650.00`**. The return is restored to complete with `$0.00` net tax effect.
4. **Changing Statement Coverage to Multiple Sales**:
   - User edits Q1 from "only this sale" to "includes other sales".
   - Single-sale gate fails. Route stops with `MULTI_SALE_STATEMENT_UNSUPPORTED`. Schedule 1 entry cleared; return blocked.
5. **Unrelated Existing Source (e.g. W-2) Recorded Alongside**:
   - W-2 wages on Form 1040 line 1a remain completely distinct in the ActLog.
   - Revising the personal item sale changes ActLog revision, prompting recalculation, but does not alter W-2 findings.

---

## 9. The Saved Explanation

Each explanation records: (1) statement details; (2) material answers in plain language; (3) absence of assumptions; (4) mathematical comparison; (5) entry amount; and (6) named stop reason if incomplete.
- **Handling of Item Description (Q2)**: When provided, the explanation names the specific item (e.g., *"for your sale of a used dining table"*). If omitted by the user, the explanation reads smoothly using a generic descriptor: *"for your sale of a personal item"*. Tax determinations and Schedule 1 entries are identical in both cases.

### Worked Plain-Language Explanations

1. **Outcome 1: Supported Loss**:
   > *"You reported Form 1099-K from OnlineMarket Inc showing $700.00 in Box 1a for your sale of a used dining table [or: a personal item]. You confirmed this statement covers only this one item, that you bought it yourself for $1,000.00, used it solely for personal purposes, and made no lasting improvements. Your agreed sale price was $700.00 with $0.00 selling fees and $0.00 refunds, resulting in net proceeds of $700.00. Because your net proceeds ($700.00) are less than your purchase cost ($1,000.00), this sale is a nondeductible personal loss. Under 2025 IRS rules, this loss cannot be deducted from your income. To account for your Form 1099-K, $700.00 is entered in the entry space at the top of Schedule 1, with $0.00 net effect on your taxable income."*

2. **Outcome 2: Unsupported Gain**:
   > *"You reported Form 1099-K from VintageSales LLC showing $1,200.00 in Box 1a for your sale of an acoustic guitar. You confirmed you bought it for $800.00 and sold it for $1,200.00 with $100.00 in marketplace fees, resulting in net proceeds of $1,100.00. Because your net proceeds ($1,100.00) exceed your purchase cost ($800.00), you realized a taxable capital gain of $300.00. Under IRS rules, personal-item capital gains must be reported on Form 8949 and Schedule D. This application does not currently support Form 8949 reporting for Form 1099-K sales. This return cannot be completed as filed (Stop Reason: UNSUPPORTED_GAIN_NOT_REPORTED)."*

3. **Outcome 3: Break-Even Sale (Unsupported)**:
   > *"You reported Form 1099-K from OnlineMarket Inc showing $700.00 in Box 1a for your sale of a personal item. You confirmed you bought it for $700.00 and sold it for $700.00 with $0.00 in fees and refunds, resulting in net proceeds of $700.00. Because your net proceeds equal your purchase cost ($700.00), this sale broke even. Under IRS rules, break-even sales from Form 1099-K are reported on Form 8949 with adjustment code 'L'. This application does not currently support Form 8949 reporting for Form 1099-K sales. This return cannot be completed as filed (Stop Reason: BREAK_EVEN_SALE_UNSUPPORTED)."*

4. **Outcome 4: Unresolved "Can't Tell" or Unanswered (Unknown Basis / Answers)**:
   > *"You reported Form 1099-K from P2P Payments showing $500.00 in Box 1a for a road bicycle. You indicated that you cannot determine what you originally paid for the bicycle. Under federal tax law, you must know your cost basis to establish whether a sale resulted in a gain or a loss, and the application cannot assume your cost was zero. Please check your purchase records before completing your return (Stop Reason: COST_BASIS_UNKNOWN)."*

5. **Outcome 5: Excluded Circumstance (Investment, Resale/Inventory, or Business/Rental Purpose)**:
   > *"You reported Form 1099-K from CoinMarket showing $900.00 in Box 1a for collectible coins. You indicated that this item was bought mainly as an investment or to make a profit. Under federal tax law (26 U.S.C. § 165(c)(2)), a loss on property held for investment or profit may be a deductible capital loss reported on Form 8949 and Schedule D, rather than a nondeductible personal loss entered on Schedule 1. This application route does not support investment property (Stop Reason: INVESTMENT_PURPOSE_EXCLUDED)."*
   >
   > *(Note: For property acquired for resale or inventory, the route stops with `RESALE_OR_INVENTORY_EXCLUDED` stating this route does not support business inventory; for business/rental property subject to depreciation recapture, the route stops with `PRIOR_DEPRECIABLE_USE_EXCLUDED`. Deductible capital-loss treatment is stated only for the profit-seeking/investment answer.)*

6. **Outcome 6: Unexplained Difference**:
   > *"You reported Form 1099-K from ResaleApp showing $850.00 in Box 1a, but your account stated an agreed item price of $700.00, leaving an unexplained difference of $150.00 that was not accounted for by platform-collected sales tax or buyer-paid shipping. Because the application cannot tell which part of Box 1a represents the personal item, it enters no amount on Schedule 1 and withholds a complete return (Stop Reason: FORM_1099K_RECONCILIATION_UNEXPLAINED)."*

---

## 10. What D2 Must Decide

The representation questions D1 leaves open for D2:

| # | Representation Question for D2 | Consumer Behaving Differently |
| --- | --- | --- |
| **1** | **Entity Structure**: Should Item and Sale be modeled as independent entity instances in the fact graph, or scoped as keys under `StatementKey`? | `packages/tax/statements.py`, ActLog assertion staging, and currency projection in `packages/kernel/findings.py`. |
| **2** | **Schedule 1 Header Representation**: Model the top-of-form entry space as a `form-field.v3` citizen bound to a published symbol, or as an attachment itemization subtotal? | `packages/derivation/presentation_projection.py` (lines 2934–3165) and PDF rendering pipeline. |
| **3** | **Schedule 1 Attachment Trigger**: Under Finding 3, `packages/derivation/runner.py:1870-1897` blocks attachment if any subtotal in `requirement.subtotals` is absent. Should the design publish an explicit closed-empty zero when the return has no Form 1099-K and succeed `rule.attachment.schedule-1.v2` to `v3` adding the 1099-K subtotal to `requirement.subtotals`, or create an independent attachment citizen? | Evaluator attachment engine (`packages/derivation/runner.py`) and Schedule 1 filing packet assembly. |
| **4** | **Income Blocking Mechanism**: Enforce income blocking via rule-graph dependency pins (open dependency on Form 1040 line 8 / line 9) or via review presentation gate (`savedUnresolvedExplanation` preventing filing approval)? | Core calculation graph execution vs `packages/tax/f1098_statement_review.py` review association. |
| **5** | **Circumstance Bundle Packaging**: Package Form 1099-K questions into a single bundle `f1099k-circumstances.bundle.v1.json`, or split statement reconciliation from item sale questions? | `packages/tax/loader.py` and bundle adoption in statement recording functions. |
