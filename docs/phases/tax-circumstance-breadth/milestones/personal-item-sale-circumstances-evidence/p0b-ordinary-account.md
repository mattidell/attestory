# P0b — Ordinary Account of a Personal-Item Sale, Paper Cases, and Integration Cost

- **Launch**: P0b launch (branch `milestone/personal-item-sale-circumstances-translation`)
- **Charter**: P0b ordinary account
- **Posture**: Builder planning and cost investigation. No tax treatment, route, schema, or citizen is implemented or adopted here.
- **Evidence standard**: Cites 2025 primary sources verbatim, repository static code reading with exact line references, current JSON schemas in `packages/schemas/`, and paper-worked synthetic cases. Distinguishes primary sources from engine code reading and interpretation.

---

## Executive Summary: Scope Choices and Findings for the Owner

P0a established that Form 1099-K Box 1a reports unreduced aggregate gross receipts across all transactions and cannot determine proceeds, cost, or taxable gain/loss on its own. It further proved that the adopted 2025 package (`demo.release.sli-worksheet-integration.2025@v43` adopting `package.core-calculations@v45`) has **zero routes** for personal-item sales today:
1. A **gain** must be reported on Form 8949 Box C (short-term) or Box F (long-term) $\rightarrow$ Schedule D line 3 or line 10 $\rightarrow$ line 7 or line 15 $\rightarrow$ Form 1040 line 7a. Neither Box C, Box F, line 3, nor line 10 exists in the package today.
2. A **personal loss reported on Form 1099-K** has two official 2025 routes:
   - **Route 1**: Enter the Form 1099-K amount in the header entry space at the top of Schedule 1 above Part I (*"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"*, `2025 Schedule 1 (Form 1040)`, p. 1). This field does not feed Schedule 1 line 10 or line 26 ($0 net tax effect).
   - **Route 2**: Report on Form 8949 (Box C or Box F) with proceeds in column (d), cost basis in column (e), code **`L`** in column (f), and a positive adjustment in column (g) equal to `basis − proceeds`, resulting in column (h) gain/loss of `$0.00`, flowing to Schedule D line 3 or line 10 ($0 net tax effect).
   Neither Route 1 nor Route 2 exists in the package today.

P0b evaluates the person's side of the account, works 11 synthetic cases on paper, establishes a single-sale reconciliation model, checks current schema capabilities, and presents three bounded scope options for the owner's decision:

| Scope Option | Gain Supported? | Loss Supported? | Break-Even Supported? | Form 8949 Touched? | Schedule D Touched? | Schedule 1 Touched? | Boundary Declaration Impact | Relative Complexity & Citizen Impact | Primary Advantage / Trade-off |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Option 1: Loss route through Schedule 1 only** | **No** (blocked) | **Yes** (Schedule 1 top entry) | **No** (blocked; see §3 Case 4) | **No** (0 change) | **No** (0 change) | **Yes** (top entry field) | `no-form8949-sources` and `no-other-form8949-adjustments` stay unchanged. Existing 1099-B returns unaffected. | **Lowest** (14 new citizens, 2 successors) | Smallest footprint. Does not touch capital gains engine or boundary facts. Leaves gains and break-even sales unsupported. |
| **Option 2: Gain & Loss through Form 8949 (Boxes C/F + Code L)** | **Yes** (Boxes C/F) | **Yes** (Code `L` $\rightarrow$ $0 col h) | **Yes** (col h = $0) | **Yes** (Boxes C/F, code L, col g) | **Yes** (lines 3/10, 7/15, attachments) | **No** (0 change) | `no-other-form8949-adjustments` must be succeeded (it forbids non-1099-B rows and non-W codes). Existing 1099-B returns must migrate or compatibility-map. | **Highest** (28 new citizens, 9 successors) | Uniform capital-asset itemization for all outcomes. High substrate cost: requires Code L adjustment machinery, proceeds-based attachment triggers, and boundary succession. |
| **Option 3: Hybrid (Gain via Form 8949, Loss via Schedule 1)** *(Recommended)* | **Yes** (Boxes C/F) | **Yes** (Schedule 1 top entry) | **Yes** (Boxes C/F col h = $0) | **Yes** (Boxes C/F, cols f/g blank) | **Yes** (lines 3/10, lines 7/15) | **Yes** (top entry field) | `no-other-form8949-adjustments` must be succeeded (admits Box C/F noncovered rows, but keeps adjustments blank). Existing 1099-B returns migrate to succeeded boundary. | **Moderate** (24 new citizens, 8 successors) | Supports gains, losses, and break-even. Avoids Code L adjustment rules and keeps Form 8949 cols (f)–(g) blank for personal items. |

### Recommendation and Key Triggers

**Recommendation: Option 3 (Hybrid: Gain through Form 8949, Loss through Schedule 1 top entry space).**
- **Rationale**:
  - `OWNER_MODEL.md` notes: *"I want a balance between value delivered and effort spent"* (line 95) and *"We are trying to avoid offloading knowledge of the tax significance of life events to the user. The product will help the user enter facts as simply as possible by understanding their tax significance and maintaining records the engine can use"* (lines 133–135).
  - For personal losses reported on Form 1099-K, `[Interpretation]` the IRS provided the dedicated top-of-Schedule-1 entry space (`2025 Schedule 1`, p. 1; `2025 Instructions for Form 1040`, p. 88) as an alternative reporting mechanism that relieves filers from calculating artificial Code L adjustments or filing Form 8949 and Schedule D.
  - For personal gains, Form 8949 Boxes C and F are required by statute (`26 U.S.C. § 1221(a)`), but because they carry only gains, **columns (f) and (g) remain blank**. This completely avoids building Code L adjustment rules and multi-code conflict checks on Form 8949, while Schedule D lines 3 and 10 compute cleanly as `proceeds − basis`.
- **What would change this recommendation**:
  - If the owner wants to keep Schedule D and Form 8949 completely untouched (zero modifications to the capital gains engine or boundary facts), choose **Option 1** (Loss only), acknowledging that gains and break-even sales remain unsupported until the capital-gains substrate is broadened.
  - If the owner requires uniform attachment of Form 8949 for all personal-item transactions reported on Form 1099-K so the IRS matching computer sees itemized proceeds and basis for losses, choose **Option 2**.

---

## 1. The Person's Account

### 1.1 Plain-Language Inventory: What a Person Can Ordinarily Say

When a person sells a personally used item and receives a Form 1099-K, they cannot be expected to know tax concepts such as "capital asset", "holding period", "adjusted basis", "Section 1221 exclusion", or "Code L adjustment". However, they can readily provide an ordinary, plain-language account of what happened:

1. **What the item was**: A plain description (e.g., "dining room table", "mountain bike", "acoustic guitar").
2. **How they got it**: That they **bought** it themselves (not inherited, not received as a gift, not won in a contest, and not manufactured or acquired for inventory/resale).
3. **When they bought it**: The approximate or exact date of purchase (e.g., "around May 2023" or "05/15/2023"). Note: As established in §1.2 and §2.2, the Schedule 1 loss route requires **no dates whatsoever**, whereas Form 8949 column (b) requires a calendar date for gains.
4. **What they paid for it**: The all-in cost paid to buy it, including sales tax and any delivery/freight charge (e.g., "$1,200 total").
5. **How it was used**: That it was used solely for personal, family, or household purposes—**never** rented out to others, never used in a business, and never subject to depreciation on any tax return.
6. **When they sold it**: The date of the sale or when the platform processed the order (e.g., "08/10/2025").
7. **What the buyer paid**: The agreed item sale price paid by the buyer (e.g., "$800").
8. **What was deducted from their payout**: The marketplace commission, payment processing fees, and packaging or shipping label costs paid by the seller (e.g., "$85 platform fees and $40 shipping label").
9. **Pass-through charges and refunds**: Whether sales tax was collected from the buyer by the platform, whether the buyer paid shipping directly to the platform, or whether any refund was issued.
10. **What the statement covers**: Whether this Form 1099-K statement represents **only this one sale**, or includes other sales, personal reimbursements, or gig work.

### 1.2 Tax Facts Required by the Rules and Their Sources

| Tax Fact Required by 2025 Rules | Source | Exact Plain-Language Question or Rule Formulation | Offered Choices / Format | Tax Significance & Why Required |
| --- | --- | --- | --- | --- |
| **Gross reported payments** | **Statement** | Form 1099-K, Box 1a (`Gross amount of payment card/third party network transactions`) | Non-negative currency (e.g., `$800.00`) | IRS reporting witness. Establishes the aggregate payment amount reported by the PSE to the IRS (`26 U.S.C. § 6050W`). |
| **Federal income tax withheld** | **Statement** | Form 1099-K, Box 4 (`Federal income tax withheld`) | Currency (`$0.00` or absent required on this route) | Backup withholding witness (`26 U.S.C. § 3406`). Must be `$0` or absent on this bounded route. |
| **Item description** | **Ordinary answer** | *"What was the item you sold?"* | Text string (e.g., `"used dining table"`) | Form 8949 column (a) description (`2025 Instructions for Form 8949`, p. 6). |
| **Acquisition mode** | **Ordinary answer** | *"How did you acquire this item?"* | • `"I bought it"`<br>• `"Received as a gift"`<br>• `"Inherited it"`<br>• `"Bought or made it for resale/business"`<br>• `"I can't tell"` | Distinguishes cost basis (`26 U.S.C. § 1012`) from gift basis (`§ 1015`), inherited basis (`§ 1014`), or inventory (`§ 1221(a)(1)`). Only `"I bought it"` is admitted. |
| **Purely personal use** | **Ordinary answer** | *"Did you use this item only for personal or household purposes, never for business or rental?"* | • `"Yes, only personal use"`<br>• `"Used for business or rental"`<br>• `"I can't tell"` | Distinguishes capital asset (`26 U.S.C. § 1221(a)`) and nondeductible personal loss (`§§ 165(c), 262(a)`) from depreciable property requiring Form 4797 Part III ordinary recapture (`2025 Instructions for Schedule D`, p. 3). Only `"Yes"` is admitted. |
| **Asset classification exclusions** | **Ordinary answer** | *"Was this item a digital asset (such as cryptocurrency or NFT) or a collectible (such as art, antiques, gems, coins, or stamps)?"* | • `"No, ordinary personal item"`<br>• `"Digital asset"`<br>• `"Collectible"`<br>• `"I can't tell"` | Digital assets must use Form 8949 Boxes I/L (`2025 Form 8949`, p. 1). Collectibles require code `C` and 28% rate worksheet (`26 U.S.C. § 1(h)(4)`). Only `"No"` is admitted. |
| **Single-sale statement coverage** | **Ordinary answer** | *"Does this Form 1099-K report payments from only this single item sale?"* | • `"Yes, only this sale"`<br>• `"No, includes other sales or transactions"`<br>• `"I can't tell"` | Reconciles Box 1a to this sale. Multi-sale statements require an accounting allocation ledger and are blocked on this bounded route. |
| **Purchase cost (Cost basis)** | **Ordinary answer** | *"What did you pay to buy the item, including sales tax and delivery charges?"* | Currency amount (e.g., `$1,200.00`), or explicit choice `"I don't know / I can't tell"` | Basis under `26 U.S.C. § 1012` and `Pub. 551`, pp. 2–3. An unknown cost basis cannot be defaulted to `$0` (`2025 Pub. 544`, p. 4) and blocks determination. |
| **Acquisition date** | **Ordinary answer** | *"When did you buy this item?"* | Exact calendar date (`YYYY-MM-DD` / `MM/DD/YYYY`), or `"I don't recall exact date"` | Form 8949 column (b) date acquired (`2025 Instructions for Form 8949`, p. 6). Required on Form 8949 for gains. **Not asked or required on Schedule 1 loss route.** |
| **Sale date** | **Ordinary answer** | *"When was the item sold or delivered to the buyer?"* | Exact calendar date (`YYYY-MM-DD` / `MM/DD/YYYY`), or choice `"Same date as statement"` | Form 8949 column (c) date sold (`2025 Instructions for Form 8949`, p. 6). Required on Form 8949 for gains. **Not asked or required on Schedule 1 loss route.** |
| **Holding period confirmation** | **Ordinary answer** (if date math not in engine) | *"Did you own this item for more than 1 year before selling it?"* | • `"Yes, owned more than 1 year"`<br>• `"No, owned 1 year or less"`<br>• `"I can't tell"` | Distinguishes short-term (Box C) vs long-term (Box F) on Form 8949 when rule content cannot compute calendar duration (`26 U.S.C. § 1222`). |
| **Buyer gross payment** | **Ordinary answer** | *"What was the agreed sale price the buyer paid for the item?"* | Currency amount (e.g., `$800.00`) | Gross proceeds from property (`26 U.S.C. § 1001(b)`). |
| **Selling expenses** | **Ordinary answer** | *"What selling fees did the platform or payment service deduct, and what did you pay to ship or deliver the item?"* | Currency amount (e.g., `$125.00`), or choice `"None / $0"`, or `"I can't tell"` | Selling expenses under `2025 Instructions for Form 8949`, p. 6 (`net proceeds = gross proceeds − selling expenses`). |
| **Reconciliation pass-through items** | **Ordinary answer** | *"Did Box 1a include sales tax collected by the platform, buyer-paid shipping, or later refunds?"* | Itemized amounts or `"None / matches agreed price"` | Reconciles Box 1a to buyer payment; see §2.2. |
| **Net sale proceeds** | **Derived** | `buyer_gross_payment − selling_expenses` | Non-negative currency (e.g., `$800 − $125 = $675`) | Form 8949 column (d) *Proceeds (Sales Price)* (`2025 Instructions for Form 8949`, p. 6). |
| **Holding period duration** | **Derived or Attested** | Count of days from day after acquisition through date of sale (`2025 Instructions for Form 8949`, p. 2) or attested enum | `short-term` (365 days or less) vs `long-term` (366 days or more) | Determines Form 8949 Part I (Box C) vs Part II (Box F) and preferential rate eligibility (`26 U.S.C. § 1222`). |
| **Transaction outcome (Gain vs Loss)** | **Derived** | `net_sale_proceeds − purchase_cost` | Currency difference | `Gain` if $> 0$; `Loss` if $< 0$; `Break-even` if $= 0$ (`26 U.S.C. § 1001(a)`). |
| **Code L adjustment amount** | **Derived** | `purchase_cost − net_sale_proceeds` (if Loss and Option 2 selected) | Positive currency amount | Form 8949 column (g) adjustment for Code `L` to bring column (h) to `$0` (`2025 Instructions for Form 8949`, p. 3). |

---

## 2. What the Application Might Assume and the Reconciliation Account

### 2.1 Candidate Defaults Evaluated

1. **Candidate: "A Form 1099-K with Box 3 = 1 covers only this single sale"**
   - **Subject and period**: Form 1099-K statement for the 2025 calendar year.
   - **What supports it**: Form 1099-K Box 3 reports the *"Number of payment transactions"* (`f1099k--2024.pdf`, p. 5). When Box 3 is explicitly printed as `1`, exactly one transaction was processed through that PSE account during the calendar year.
   - **What contrary information, uncertainty, or withdrawal does**: If Box 3 is $> 1$, blank, or if the user indicates that other sales occurred, the assumption collapses.
   - **Recommendation**: **Do not adopt as a silent default.** Even if Box 3 is `1`, that single transaction could represent a business service, a personal reimbursement, or a sale of multiple bundled items. Instead, present Box 3 as recognized context ("Your statement shows 1 transaction") and ask the user to confirm: *"Does this statement cover only this one item sale?"*

2. **Candidate: "Form 1099-K Box 1a gross payment equals the buyer's payment"**
   - **Subject and period**: The gross sale amount of the item sold in 2025.
   - **What supports it**: On some peer-to-peer platforms, the gross transaction amount processed through the platform is the item purchase price.
   - **What contrary information, uncertainty, or withdrawal does**: Platforms frequently bundle buyer-paid sales tax, shipping fees, or platform service fees into the gross settled charge, or conversely deduct seller fees prior to settlement.
   - **Recommendation**: **Adopt as an initial pre-fill candidate only, never an immutable default.** Show Box 1a as the suggested buyer payment, but explicitly ask the user to verify what the buyer paid and what selling expenses were withheld.

3. **Candidate: "Selling expenses (platform fees and shipping) default to $0 if not specified"**
   - **Subject and period**: Expenses incurred in 2025 to sell the personal item.
   - **What supports it**: In an in-person, local cash-and-carry sale settled via payment card, there may be no platform fee or shipping charge.
   - **What contrary information, uncertainty, or withdrawal does**: On online marketplaces (eBay, Poshmark, Mercari), fees and shipping are almost universally present. Defaulting fees to `$0` overstates net proceeds, producing an artificially higher taxable gain or lower personal loss.
   - **Recommendation**: **Do not adopt.** Require the user to explicitly confirm fees or affirm that no fees were paid.

4. **Candidate: "Cost basis defaults to $0 when unknown"**
   - **Subject and period**: Original acquisition cost of the item.
   - **What supports it**: Nothing in tax law.
   - **What contrary information, uncertainty, or withdrawal does**: The 2025 IRS instructions (`2025 Instructions for Form 8949`, p. 2; `2025 Pub. 544`, p. 4) give no authority to substitute zero. Substituting zero manufactures a fictitious taxable gain on an item that was actually bought at a loss (e.g., selling a $1,000 couch for $300 would be taxed as a $300 gain if basis is defaulted to $0!).
   - **Recommendation**: **Hard rejection.** As established in P0a and the P0a review, unknown basis is never zero. An unknown cost basis must result in an unresolvable stop condition, clearly explaining to the user what records are required.

5. **Candidate: "Holding period defaults to long-term if purchased 'years ago'"**
   - **Subject and period**: Holding period between purchase and 2025 sale.
   - **What supports it**: Personal furniture, appliances, and clothing are overwhelmingly held for more than one year before disposal.
   - **What contrary information, uncertainty, or withdrawal does**: If an item was bought on clearance and resold 6 months later, treating it as long-term misclassifies short-term gain into preferential rates, violating tax law (`26 U.S.C. § 1222`).
   - **Recommendation**: **Do not adopt as an unprompted assumption.**

---

### 2.2 Explicit Reconciliation Account for a Single-Sale Statement

Form 1099-K Box 1a reports the gross dollar amount of all reportable payment transactions settled through the PSE without adjustments:
> *"Gross amount means the total dollar amount of total reportable payment transactions for each participating payee without regard to any adjustments for credits, cash equivalents, discount amounts, fees, refunded amounts, shipping amounts, or any other amounts. The dollar amount of each transaction is determined on the date of the transaction."* (`Instructions for Form 1099-K (Rev. March 2024)`, p. 4, Box 1a; `Form 1099-K (Rev. March 2024)`, p. 5, Box 1a Note).

On a statement covering exactly one sale, Box 1a can differ from the agreed item price because it contains:

1. **State/Local Sales Tax Collected by the Platform (`"or any other amounts"`)**:
   - Under marketplace facilitator laws, platforms (eBay, Poshmark, Etsy) collect sales tax directly from buyers and remit it to state tax authorities. When settled through the payment settlement entity, this sales tax is often included in Box 1a.
   - Tax characterization (`26 U.S.C. § 1001(b)`): `[Primary Source]` Amount realized includes only money received by the taxpayer. Sales tax collected by a platform and remitted to a state is a fiduciary pass-through, **NOT part of the seller's amount realized**.
2. **Buyer-Paid Shipping Settled Through Platform (`"shipping amounts"`)**:
   - The buyer pays $20 shipping on top of an $80 item; the PSE settles $100 in Box 1a.
   - Tax characterization (`2025 Instructions for Form 8949`, p. 6): If the buyer pays shipping to the seller and the seller purchases the shipping label, the $20 is gross proceeds, and the $20 label cost is a selling expense that reduces gross proceeds to net proceeds (`net proceeds = gross proceeds − selling expenses = $100 − $20 = $80`). If the platform retains the shipping amount directly and issues the label without paying the seller, the shipping charge is a pass-through and **NOT part of the seller's amount realized**.
3. **Selling Expenses / Platform Fees Not Netted (`"fees"`)**:
   - Platform commissions (e.g., 10%) and payment processing fees withheld from the seller's payout are included unreduced in Box 1a.
   - Tax characterization (`2025 Instructions for Form 8949`, p. 6): Platform fees are **selling expenses** that reduce gross proceeds to net proceeds for Form 8949 column (d).
4. **Subsequent Refunds, Returns, or Chargebacks (`"refunded amounts", "credits", "discount amounts"`)**:
   - If an item was sold for $500 in May, but $100 was refunded in June due to damage, Box 1a reflects $500 (determined on transaction date) and is not reduced by the refund.
   - Tax characterization (`26 U.S.C. § 1001(b)`): The refund reduces the amount realized on the sale. The refunded amount is **NOT part of the seller's amount realized**.

#### Policy: What the Route Does When the Person's Account and Box 1a Disagree

Reconciliation identity:
$$\text{Box 1a} = \text{Agreed Item Price} + \text{Platform-Collected Sales Tax} + \text{Buyer-Paid Shipping} - \text{Subsequent Refunds}$$

When the person's stated agreed item price does not equal Box 1a:
1. **Prompt for explanation**: The application presents the difference and asks whether Box 1a included platform-collected sales tax, buyer shipping, platform fees, or a refund.
2. **If explained**: The pass-through components are recorded. Net proceeds are derived as `agreed_item_price − seller_paid_fees_and_shipping`. Form 1099-K Box 1a is reconciled.
3. **If unexplained**:
   - The application **MUST NOT** silently overwrite the person's stated sale price with Box 1a (which would overstate proceeds and overtax the filer).
   - The application **MUST NOT** let an unexplained difference silently disappear (which would create an unreconciled discrepancy with IRS information returns).
   - **Action**: The route **BLOCKS with a named reason: `FORM_1099K_RECONCILIATION_UNEXPLAINED`**.
   - **Saved explanation**:
     > *"Your Form 1099-K reports $1,000.00, but your sale account describes an item price of $850.00, leaving an unexplained difference of $150.00. Tax rules do not permit substituting Form 1099-K gross receipts for your sale proceeds, nor ignoring unexplained differences. Please check your platform account summary for sales tax, shipping, or fee adjustments that account for the difference before completing this return."*

---

## 3. Cases on Paper

### Summary Table of Worked Paper Cases

| Case | Scenario Description | Form 1099-K Box 1a | Cost Basis | Selling Expenses | Net Proceeds | Derived Outcome | 2025 Return Route & Entries | Net Tax Effect | Explanation Summary / Stop Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1** | Short-term gain ($\le$ 1 yr) | $600 | $400 | $50 | $550 | Gain: **+$150** | Form 8949 Part I Box C; Schedule D line 3 $\rightarrow$ line 7 $\rightarrow$ Form 1040 line 7a | **+$150** income | Taxable short-term capital gain of $150 added to ordinary income. |
| **2** | Long-term gain ($>$ 1 yr) | $1,200 | $800 | $100 | $1,100 | Gain: **+$300** | Form 8949 Part II Box F; Schedule D line 10 $\rightarrow$ line 15 $\rightarrow$ Form 1040 line 7a | **+$300** pref. base | Taxable long-term capital gain of $300 eligible for preferential rates. |
| **3a** | Personal loss (Schedule 1 route) | $700 | $1,000 | $0 | $700 | Loss: **−$300** | Schedule 1 top-of-form entry space: enter **$700** | **$0** | Personal loss is nondeductible; $700 reported at top of Schedule 1 to offset 1099-K with $0 tax effect. |
| **3b** | Personal loss (Form 8949 Code L route) | $700 | $1,000 | $0 | $700 | Loss: **−$300** | Form 8949 Box F: col (d) $700, col (e) $1,000, col (f) **`L`**, col (g) **+$300**, col (h) **$0** $\rightarrow$ Sched D line 10 | **$0** | Nondeductible personal loss reported with Code L adjustment of +$300 resulting in $0 net gain/loss. |
| **4** | Proceeds equal to cost (Break-even) | $500 | $500 | $0 | $500 | Break-even: **$0** | **Option 1**: Blocked / no entry space authorization.<br>**Options 2 & 3**: Form 8949 Box F col (d) $500, col (e) $500, col (h) **$0** | **$0** | Genuine zero gain; proceeds equal cost basis. Supported on Options 2 and 3 via Form 8949. Option 1 cannot carry it (see §3.1 Case 4). |
| **5** | Cost unknown | $850 | Unknown | $50 | $800 | Unresolvable | **None** (blocked) | **Blocked** | `COST_BASIS_UNKNOWN`: Cannot determine gain or loss without basis; unknown basis is never zero. |
| **6** | Platform fees and seller shipping | $1,500 | $900 | $250 | $1,250 | Gain: **+$350** | Form 8949 Box F: col (d) **$1,250**, col (e) $900, col (h) **$350** | **+$350** pref. base | Gross Box 1a ($1,500) reduced by fees ($175) and shipping ($75); net proceeds ($1,250) reported in col (d). |
| **7** | Statement covers multiple sales | $4,200 | Varied | Varied | Varied | Unsupported | **None** (blocked) | **Blocked** | `MULTI_SALE_STATEMENT_UNSUPPORTED`: Bounded route does not allocate aggregate Form 1099-K among multiple items. |
| **8** | Acquired by gift / for resale | $950 | N/A | N/A | N/A | Excluded | **None** (blocked) | **Blocked** | `ACQUISITION_MODE_UNSUPPORTED`: Non-purchase acquisitions follow special basis/character rules outside this bounded route. |
| **9** | Prior business or rental use | $2,000 | $1,500 | $100 | $1,900 | Excluded | **None** (blocked) | **Blocked** | `PRIOR_DEPRECIABLE_USE_EXCLUDED`: Property previously used in business/rental requires Form 4797 Part III ordinary recapture. |
| **10** | Collectible held > 1 year | $3,500 | $2,000 | $200 | $3,300 | Excluded | **None** (blocked) | **Blocked** | `COLLECTIBLE_RATE_EXCLUDED`: Long-term gain on collectible requires Code C and 28% Rate Gain Worksheet (Sched D line 18). |
| **11** | Gain beside personal loss (Anti-netting) | $1,900 | Varied | $0 | $1,900 | Loss −$300, Gain +$400 | Top of Schedule 1: **$700**; Form 8949 Box F: col (d) $1,200, col (e) $800, col (h) **+$400** | **+$400** pref. base | Proves anti-netting: loss of $300 on couch cannot offset $400 gain on handbag. Gain is fully taxable. |

---

### 3.1 Case 4: Proceeds Equal to Cost (Break-Even / Genuine Zero) — Per-Option Handling

- **Facts**: Item bought for `$500.00` on `2024-03-10`, sold for `$500.00` on `2025-06-12`. Net proceeds = `$500.00`. Basis = `$500.00`. Net gain/loss = `$0.00`.
- **Primary Source Analysis**:
  - `2025 Schedule 1`, top-of-form entry space text:
    > *"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"* (`f1040s1--2025.pdf`, p. 1).
    The Schedule 1 instructions (p. 88) specify this space only for amounts included in error or for personal items sold at a loss. A break-even sale is not sold at a loss and was not included in error.
  - `2025 Instructions for Form 8949`, p. 9: Code `L` applies only when *"You have a nondeductible loss other than a loss indicated by code W"*. In a break-even sale, there is no loss, so Code `L` does not apply.
  - `2025 Form 8949`, Part II (Box F): Column (d) is `$500.00`, column (e) is `$500.00`, columns (f) and (g) are blank, and column (h) is `$0.00` directly (`d − e = 0`).
- **Per-Option Outcome**:
  - **Option 1 (Schedule 1 loss-only)**:
    - **NOT SUPPORTED**. Option 1 has no Form 8949 route, and the Schedule 1 entry space does not authorize break-even reporting.
    - **What the person sees**: The application identifies that this is a **genuine zero outcome** (no taxable gain, no deductible loss). However, because Option 1 has no Form 8949 reporting citizen, the application cannot generate a return attachment matching Box 1a.
    - Status shown to user: `BREAK_EVEN_NO_TAX_EFFECT` with advisory explanation:
      > *"You sold your bicycle for $500.00, which equals your $500.00 purchase cost. Under tax law, you have $0.00 taxable gain and $0.00 deductible loss; your taxable income is unaffected. However, because this route only supports loss reporting on Schedule 1, Form 8949 is not available to report this transaction to match your Form 1099-K."*
    - It is **not** displayed as an error or unresolved fact; the economic and tax result ($0) is definitive.
  - **Options 2 and 3**:
    - **FULLY SUPPORTED**. Both options provide Form 8949 Box F and Schedule D line 10. The transaction is reported on Form 8949 Box F with col (d) `$500.00`, col (e) `$500.00`, cols (f)–(g) blank, and col (h) `$0.00`, flowing to Schedule D line 10 as `$0.00`. It reconciles Form 1099-K Box 1a to the IRS matching program with zero net tax effect.

---

### 3.2 Handling Imprecise Dates Across Options

`2025 Instructions for Form 8949`, p. 6, under **Column (b)—Date Acquired**, states verbatim:
> *"Enter in this column the date you acquired the property. Enter the trade date for stocks and bonds you purchased on an exchange or over-the-counter market...*
> *Inherited property. Generally, if you disposed of property that you acquired by inheritance, report the sale or exchange on Part II with the appropriate box checked D, E, F, J, K, or L. Enter “INHERITED” in column (b).*
> *Stock or digital assets acquired on various dates. If you sold a block of stock or digital assets (or similar property) that you acquired through several different purchases, you may report the sale on one row and enter “VARIOUS” in column (b). However, you must still report the short-term gain (or loss) on the sale on Part I and the long-term gain (or loss) on Part II."*

- **Primary Source Rule**: Column (b) permits only an exact calendar date, or the specific literals `"INHERITED"` or `"VARIOUS"`. For a single purchased personal item, neither `"INHERITED"` nor `"VARIOUS"` is permitted. The form requires a date.
- **Handling when user answers "don't recall exact date, but owned more than 1 year"**:
  - **On Form 8949 (Options 2 and 3 for gains; Option 2 for losses)**:
    - Entering non-date strings such as "MORE THAN 1 YEAR" is unauthorized by Form 8949 instructions.
    - If the user cannot supply a calendar date (e.g., month and year, converted to the first of that month such as `2023-05-01`), Form 8949 cannot be populated. The transaction is marked **unresolved** with reason `ACQUISITION_DATE_REQUIRED`.
  - **On the Schedule 1 Loss Route (Options 1 and 3 for losses)**:
    - **NO DATES ARE REQUIRED OR ASKED**.
    - The top-of-form entry space on Schedule 1 (`f1040s1--2025.pdf`, p. 1) requires only a single dollar amount. It has no date acquired, no date sold, and no holding period columns.
    - Consequently, when an item is sold at a loss and reported via Schedule 1, the questionnaire **omits the acquisition date and sale date questions entirely**. The user is asked only whether the item was bought, used personally, sold at a loss, and the amounts needed for reconciliation.

---

## 4. Corrections and Lifecycle Changes

### 4.1 Correcting Cost Basis Across the Gain/Loss Boundary
- **Scenario**: User initially entered cost basis as `$400.00` on an item sold for `$600.00` (net proceeds `$550.00`), creating a `+$150.00` short-term gain on Form 8949 Box C. User later finds records showing actual cost was `$750.00`, turning the transaction into a `−$200.00` personal loss.
- **What stays supported**: Statement finding, item description, acquisition mode ("bought it"), personal-use confirmation, sale date, and selling expenses remain supported.
- **What changes**:
  - The previous cost basis finding is superseded by a new finding.
  - The derived transaction outcome switches from `Gain` to `Loss`.
  - Under **Option 3**, the reporting route switches completely:
    - The Form 8949 Box C row and Schedule D line 3/7 entries are removed.
    - Form 1040 line 7a drops from `$150.00` to `$0.00`.
    - The Form 1099-K amount (`$600.00`) is now routed to the Schedule 1 top-of-form entry space.
- **Saved explanation text**:
  > *"Your purchase cost was corrected from $400.00 to $750.00. Because your cost now exceeds your net sale proceeds ($550.00), this sale is now a nondeductible personal loss rather than a taxable gain. The $150.00 gain has been removed from Form 1040 line 7a, and the $600.00 reported on your Form 1099-K is now entered at the top of Schedule 1 with $0.00 net tax effect."*
- **Presentation association**: The saved presentation's `workspace_revision` is now behind the ActLog revision; `associate_saved_run` marks the state as `"recalculation-needed"`.

### 4.2 Withdrawing the Personal-Use Answer
- **Scenario**: User affirmed `"Yes, only personal use"`, then later withdraws that answer.
- **What stays supported**: Statement finding remains in the log.
- **What changes**:
  - A `finding-retracted` act is appended for the personal-use answer finding.
  - The required-rule condition for personal use is no longer satisfied.
  - The route can no longer determine whether capital gains rules, ordinary depreciation recapture (Form 4797 Part III), or business schedule reporting applies.
- **Saved explanation text**:
  > *"The personal-use confirmation for this item was withdrawn. Without confirmation that the item was held solely for personal purposes, the application cannot determine whether capital gains, business property, or depreciation recapture rules apply. This statement is marked unresolved."*
- **Named stop reason**: `PERSONAL_USE_UNCONFIRMED`.

### 4.3 Correcting the Reported Form 1099-K Box 1a Amount
- **Scenario**: The issuer provides a corrected Form 1099-K updating Box 1a from `$1,200.00` to `$1,000.00`.
- **What a Box 1a correction changes**:
  1. On the **loss route (Schedule 1 top entry space)**: The Schedule 1 entry reports the Form 1099-K gross payment attributable to the personal item sold at a loss (`2025 Instructions for Form 1040`, p. 88). A correction to Box 1a directly updates the Schedule 1 top-of-form entry amount from `$1,200.00` to `$1,000.00`.
  2. On the **reconciliation check**: The comparison between Box 1a and the person's account (`agreed_price + sales_tax + shipping − refunds`) is re-checked against the new `$1,000.00` figure.
- **What a Box 1a correction DOES NOT change**:
  - It does **NOT** alter the agreed sale price or selling expenses confirmed by the person.
  - It does **NOT** alter net proceeds (Form 8949 column d).
  - It does **NOT** alter cost basis (Form 8949 column e).
  - It does **NOT** alter the economic gain or loss (`net_proceeds − cost_basis`).
  - It does **NOT** alter taxable capital gain reported on Form 8949 column (h), Schedule D lines 3/10, or Form 1040 line 7a.
- **Saved explanation text**:
  > *"Your Form 1099-K reported gross amount was corrected from $1,200.00 to $1,000.00. This updates your statement reconciliation and the Form 1099-K entry on Schedule 1. Your agreed item price and net sale proceeds remain based on your confirmed transaction records."*

### 4.4 Changing Statement Coverage from Single-Sale to Multiple Sales
- **Scenario**: The user initially answered that the Form 1099-K covered only this one sale. Later, they change the answer to indicate that the statement also includes other sales.
- **What stays supported**: The facts describing this specific item sale remain recorded.
- **What changes**: The single-sale boundary gate fails. The transaction transitions from resolved to an unsupported boundary block.
- **Named stop reason**: `MULTI_SALE_STATEMENT_UNSUPPORTED`.

---

## 5. Reuse Analysis Checked Against Actual Code Consumers

Every candidate below was examined directly in the repository source code at P0b launch.

### 5.1 Mortgage Statement Recording and Circumstances (`packages/tax/f1098_statement_recording.py` and `f1098-circumstances.bundle.v2.json`)
- **Code reading**:
  - Atomic submission provenance (`_require_provenance`, lines 54–57).
  - Currency-scoped finding lookup (`_current_finding`, lines 68–73; `_require_current_statement`, lines 123–135).
  - Staging evidence, contribution, and assertion acts atomically (`_stage_answer`, lines 137–173).
  - Durable replacement (`correct_f1098_statement_answer_durably`, lines 267–304) and retraction (`withdraw_f1098_statement_answer_durably`, lines 356–405).
- **What transfers**: Atomic log-writing, provenance validation, evidence/contribution/finding triple, and currency-checked replacement/retraction patterns transfer directly.
- **What does NOT transfer**: The domain questions and schemas (`f1098-circumstances.bundle.v2.json`) are completely mortgage-specific. A new `f1099k-circumstances.bundle.v1.json` is required. The assertion `len(all_sources) == 1` in `_require_current_statement` (line 133) assumes only one statement exists on the return; a personal-item module must scope currency to the specific statement's keys.

### 5.2 Statement Identity (`packages/tax/statements.py:1-85`)
- **Code reading**:
  - `StatementKey(payer_id, tax_year, payer_ref)` (lines 32–39) and `statement_key()` (lines 41–53) enforce `_EVIDENCE_MARKERS` rejection.
  - `classify_assertion()` (lines 61–85) classifies incoming returns as `NEW_ORIGINAL`, `CORRECTION`, or `DUPLICATE`.
- **What transfers**: Full direct reuse for identifying a Form 1099-K statement: `payer_id` is the PSE/filer ID, `tax_year` is 2025, and `payer_ref` is the account reference.
- **What does NOT transfer**: `StatementKey` identifies a furnished statement, not a sale. Pairing `StatementKey` with a single-sale assertion is required for this bounded milestone.

### 5.3 Same-Statement Withholding Gate (`packages/tax/loader.py:51-145`)
- **Code reading**:
  - `domain_companion_presence_pairs()` (lines 51–123) and `domain_companion_value_domains()` (lines 125–145) enforce companion presence and restrict values (e.g., `f1099g.box4-federal-withholding-authority` restricted to `{None, 0, 0.0}`).
- **What transfers**: **100% direct reuse.** Installing `f1099k.box1a-gross` $\rightarrow$ `f1099k.box4-federal-withholding-authority` with value domain `{None, 0, 0.0}` cleanly prevents any statement with backup withholding from entering without creating Form 1040 line 25b.

### 5.4 Form 8949 Three-Column Pattern (`attachment.f8949.v2.json`, `rule.schedule-d-line1b.v2.json`)
- **Code reading**:
  - `attachment.f8949.v2.json` itemizes columns (d) proceeds, (e) basis, and (g) adjustment from three scalar source families.
  - `rule.schedule-d-line1b.v2.json` computes `d − e + g`.
- **What transfers**: Arithmetic pattern `d − e + g` transfers cleanly to Schedule D line 3 (Box C) and line 10 (Box F).
- **What does NOT transfer (Crucial Schema Finding)**:
  - As verified in `packages/schemas/tax/attachment-rule.v11.schema.json` and `packages/derivation/presentation_projection.py:2934-3165`, **the `attachment-rule` schema family itemizes numeric amounts only**.
  - There is **no mechanism in `attachment-rule` to carry non-numeric row fields** such as column (a) description string, column (b) date acquired, or column (c) date sold! Form 8949 in this engine itemizes only numeric columns (proceeds, basis, adjustment) and presents itemized text/dates through circumstance explanation, not attachment row fields.

### 5.5 Review and Saved-Explanation Path (`packages/tax/f1098_statement_review.py:1-331`)
- **Code reading**:
  - `prepare_f1098_statement_review` (lines 47–115) builds an immutable review snapshot.
  - `associate_saved_run` (lines 260–276) verifies `workspace_revision == current_revision` via `RecordStream`.
  - `review_f1098_statement_with_saved_presentation` (lines 278–331) links the review snapshot to `savedCalculation` or `savedUnresolvedExplanation`.
- **What transfers**: The revision-tracking association engine, recalculation-needed detection, and completed/unresolved explanation architecture transfer directly.
- **What does NOT transfer**: Domain questions and explanation payloads (`mortgageInterestExplanation`) are mortgage-specific; a new personal-item review and explanation builder is required.

---

## 6. Cost, Schema Needs, Boundaries, and Scope Choices

### 6.1 Schema and Rule-Language Capabilities Checked Against Engine Code

1. **Can adopted rule content derive holding period from two recorded dates?**
   - **Engine check**: Inspected `evaluator.py:133-149, 1024-1065` and `docs/adr/0078-fixed-date-comparison-operator.md`.
   - ADR-0078 added `date_compare` to `rule-artifact.v14` (admitted in `artifact-package.v36`). Its shape is:
     ```json
     {"op": "date_compare", "left": {"op": "ref", "name": "..."}, "date": "1987-10-13", "cmp": "lt"}
     ```
   - ADR-0078 explicitly decided:
     > *"This milestone is explicitly not the place to build a general date framework: no date arithmetic, no interval or duration math, no date-to-date comparison between two recorded facts... No right-as-expression form exists."* (ADR-0078, lines 42–48, 91–95).
   - **Conclusion**: **NO**. Rule content cannot compute holding period by comparing or subtracting two recorded dates (`acquisition_date` and `sale_date`).
   - **Resolution for this milestone**:
     - Either add a new evaluator op and schema successor (`rule-artifact.v15`) for date-difference comparison;
     - **OR (Recommended)**: Collect holding period as an attested ordinary circumstance answer: *"Did you own this item for more than 1 year before selling it?"* $\rightarrow$ `{yes, no}`. This avoids any date-math schema addition and allows rule content to branch on a simple categorical symbol.

2. **Can current `attachment-rule` itemizations carry Form 8949 columns (a) description, (b) date acquired, and (c) date sold?**
   - **Engine check**: Checked `packages/schemas/tax/attachment-rule.v11.schema.json:464-494` and `packages/derivation/presentation_projection.py:2980-3050`.
   - Each itemization `part_id` binds to a numeric source family and subtotal symbol.
   - **Conclusion**: **NO**. The current `attachment-rule` schema supports **numeric amounts only**. It cannot carry non-numeric string descriptions or calendar dates. Form 8949 itemizations in the engine carry proceeds, basis, and adjustments; descriptions and dates reside in the circumstance explanation.

3. **Can the Schedule 1 top-of-form entry be a form-field bound to a rule-published symbol under `form-field.v3`?**
   - **Engine check**: Checked `packages/schemas/tax/form-field.v3.schema.json:1-6`.
   - `form-field.v3` requires: `schema`, `id`, `version`, `form` (`authority`, `form_id`, `tax_year`, `jurisdiction`), `line` (any non-empty string), `label`, `description`, `binds_symbol`, and `dispositions`.
   - **Conclusion**: **YES, 100% supported**. A citizen with `id: "tax.us.2025.form.schedule1.top-1099k-personal-loss"`, `form.form_id: "1040-SCH-1"`, `line: "top"`, and `binds_symbol: "tax.us.2025.schedule1.top-1099k-personal-items-loss"` is fully valid under `form-field.v3` without any schema modification.

---

### 6.2 Boundary Declarations per Option and Effect on Existing Returns

1. **`tax.us.2025.schedule-d-boundary.no-form8949-sources`** (`schedule-d-boundary.bundle.json:69`):
   - Definition: Whether the return has no Form 8949 transactions or adjustments.
   - **Option 1**: Stays `"yes"`. Unaffected.
   - **Options 2 & 3**: Evaluates to `"no"` on returns with Form 8949 Box C/F rows. This routes Schedule D attachment and `selected-preferential-base` into Path B.

2. **`tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments`** (`schedule-d-boundary-form8949-w.bundle.json:9`):
   - Definition: *"Whether the return has no Form 8949 adjustment codes other than W, no multi-code rows, and no noncovered/basis-not-reported Form 8949 sources (ADR-0061 Decision 4). Categorical {yes,no}."*
   - **Option 1**: Stays `"yes"`. Unaffected.
   - **Option 2**: **Direct conflict**. Option 2 introduces Box C/F (noncovered sources) and Code L (a code other than W). Answering `"yes"` is impossible. This fact must be succeeded by a new boundary declaration (e.g., `schedule-d-boundary.no-other-form8949-adjustments.v2` or separated into box-scope and code-scope facts). Existing Form 1099-B returns must either answer the successor declaration or be admitted via compatibility rules.
   - **Option 3**: **Partial conflict**. Option 3 introduces Box C/F (noncovered sources), but has **zero adjustments** (columns f and g blank). Because the current fact bundles "no noncovered sources" with "no codes other than W", it cannot be answered `"yes"` as written. Option 3 requires a successor boundary fact that admits noncovered personal-item sources with blank adjustments.
   - **Effect on existing Form 1099-B returns**: In both Option 2 and Option 3, existing Form 1099-B returns that asserted `no-other-form8949-adjustments@v1 = "yes"` must be migrated to the successor declaration version in `published-packages.v46.json`.

3. **Schedule 1 Part I Scope Facts (`tax.us.2025.schedule1-part1-scope.no-sch1-*`)**:
   - `attachment.schedule-1.v2.json:8-70` checks `no-sch1-line1-taxable-refunds`, `no-sch1-line2a-alimony`, `no-sch1-line3-business`, `no-sch1-line4-other-gains`, `no-sch1-line5-rental`, `no-sch1-line6-farm`, and `no-sch1-other-income`.
   - The Schedule 1 top-of-form entry space is in the header above Part I; it is not line 8z or Part I other income.
   - **All Options**: Existing Schedule 1 boundary facts remain valid and their meaning is unchanged.

---

### 6.3 Enumerated Citizen List per Option

#### Option 1: Loss Route Through Schedule 1 Only
- **New Citizens (14)**:
  1. `tax.us.2025.bundle.f1099k.v1`
  2. `tax.us.2025.fact-type.f1099k.box1a-gross.v1`
  3. `tax.us.2025.fact-type.f1099k.box4-federal-withholding-authority.v1`
  4. `tax.us.2025.bundle.personal-item-sale-circumstances.v1`
  5. `tax.us.2025.fact-type.personal-item-sale.item-description.v1`
  6. `tax.us.2025.fact-type.personal-item-sale.bought-it.v1`
  7. `tax.us.2025.fact-type.personal-item-sale.personal-use.v1`
  8. `tax.us.2025.fact-type.personal-item-sale.cost-basis.v1`
  9. `tax.us.2025.fact-type.personal-item-sale.buyer-payment.v1`
  10. `tax.us.2025.fact-type.personal-item-sale.selling-expenses.v1`
  11. `tax.us.2025.fact-type.personal-item-sale.single-sale-coverage.v1`
  12. `tax.us.2025.form-field.schedule1.top-1099k-personal-loss.v1` (schema `form-field.v3`)
  13. `tax.us.2025.rule.schedule1-top-1099k-personal-loss.v1` (schema `rule-artifact.v5`)
  14. `tax.us.2025.citation.schedule1-top-1099k.v1`
- **Successor Citizens (2)**:
  1. `tax.us.2025.rule.attachment.schedule-1.v3` (updates `requirement.subtotals` to attach Schedule 1 when top entry $> 0$)
  2. `tax.us.2025.package.core-calculations.v46` (adopts the citizens above)

---

#### Option 2: Gain & Loss Through Form 8949 (Boxes C/F + Code L)
- **New Citizens (28)**:
  - 1–11: Same statement and circumstance citizens as Option 1, plus `holding-period-duration.v1`.
  - 12–17: Six source families: `box-c-proceeds.v1`, `box-c-basis.v1`, `box-c-adjustment.v1`, `box-f-proceeds.v1`, `box-f-basis.v1`, `box-f-adjustment.v1`.
  - 18–23: Six closure mappings for Box C/F source families.
  - 24–25: Schedule D line computation rules: `rule.schedule-d-line3.v1` (`d − e + g`), `rule.schedule-d-line10.v1` (`d − e + g`).
  - 26–27: Form fields: `form-field.schedule-d.line3.v1`, `form-field.schedule-d.line10.v1`.
  - 28: Succeeded boundary bundle: `schedule-d-boundary.form8949-code-l.vocabulary.v1`.
- **Successor Citizens (9)**:
  1. `tax.us.2025.rule.schedule-d-line7.v4` (incorporates line 3)
  2. `tax.us.2025.rule.schedule-d-line15.v5` (incorporates line 10)
  3. `tax.us.2025.rule.form1040-line7a.v6` (adds lines 3/10 to discriminator)
  4. `tax.us.2025.rule.selected-preferential-base.v5` (adds lines 3/10 to discriminator and Path B completeness)
  5. `tax.us.2025.rule.attachment.f8949.v3` (itemizes Box C and Box F proceeds, basis, adjustments; proceeds-based requirement trigger)
  6. `tax.us.2025.rule.attachment.schedule-d.v7` (itemizes lines 3 and 10)
  7. `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments.v2`
  8. `tax.us.2025.citation.schedule-d.v2`
  9. `tax.us.2025.package.core-calculations.v46`

---

#### Option 3: Hybrid (Gain via Form 8949, Loss via Schedule 1) *(Recommended)*
- **New Citizens (24)**:
  - 1–11: Same statement and circumstance citizens as Option 1, plus `holding-period-duration.v1`.
  - 12–14: Schedule 1 loss path: `form-field.schedule1.top-1099k-personal-loss.v1`, `rule.schedule1-top-1099k-personal-loss.v1`, `citation.schedule1-top-1099k.v1`.
  - 15–18: Four source families for gains: `box-c-proceeds.v1`, `box-c-basis.v1`, `box-f-proceeds.v1`, `box-f-basis.v1` (**zero adjustment families needed**).
  - 19–22: Four closure mappings for Box C/F proceeds and basis.
  - 23–24: Schedule D line computation rules: `rule.schedule-d-line3.v1` (`d − e`), `rule.schedule-d-line10.v1` (`d − e`).
- **Successor Citizens (8)**:
  1. `tax.us.2025.rule.attachment.schedule-1.v3` (updates `requirement.subtotals`)
  2. `tax.us.2025.rule.schedule-d-line7.v4` (incorporates line 3)
  3. `tax.us.2025.rule.schedule-d-line15.v5` (incorporates line 10)
  4. `tax.us.2025.rule.form1040-line7a.v6` (adds lines 3/10 to discriminator)
  5. `tax.us.2025.rule.selected-preferential-base.v5` (adds lines 3/10 to discriminator)
  6. `tax.us.2025.rule.attachment.f8949.v3` (itemizes Box C/F proceeds and basis with blank adjustments)
  7. `tax.us.2025.rule.attachment.schedule-d.v7` (itemizes lines 3 and 10)
  8. `tax.us.2025.package.core-calculations.v46`

---

### 6.4 Capital-Asset and Accounting Framework Traps to Avoid

1. **Multi-sale statement reconciliation ledger**: Do not build a general N-transaction ledger that splits one Form 1099-K across multiple sales, business schedules, and personal items. Bound the milestone strictly to **one statement covering one personal item**.
2. **General basis and depreciation history ledger**: Do not build asset-basis tracking schedules for improvements, depreciation, or gift/inheritance basis. Bound strictly to **one purchased item with known cost**.
3. **General Form 8949 noncovered asset expansion**: Do not open Form 8949 to digital assets (Boxes I/L), real estate (Form 1099-S), or collectibles (28% rate). Gate them out explicitly.
4. **Form 1040 Line 25b withholding aggregation**: Do not build a cross-form line 25b payment aggregator. Gate Form 1099-K Box 4 to null/0 via `domain_companion_presence_pairs`.
