# P0a — 2025 Personal-Item Sale Authority and Adopted Return Path

- **Launch**: P0a launch (branch `milestone/personal-item-sale-circumstances-translation`)
- **Charter**: P0a authority and return path
- **Posture**: Evidence-only investigation for P0b question design. No tax treatment, route, or schema is selected or implemented here.

Every section below keeps three categories visibly separate:
1. **[Primary Source]** — What 2025 federal tax statutes, forms, instructions, and publications state, with exact citations.
2. **[Code reading]** — What the repository's live coordinator and adopted 2025 package at milestone launch contain upon static reading, with exact file paths, citizen IDs, and line numbers (nothing was executed).
3. **[Interpretation for P0b]** — What the primary-source and return-path facts mean for P0b's question design and scope boundaries.

---

## Executive Summary: What This Lets P0b Decide

1. **Why Form 1099-K Box 1a alone cannot determine taxability or proceeds**:
   - **[Primary Source]** Form 1099-K Box 1a reports the annual aggregate *gross amount* of reportable payment transactions settled through a Payment Settlement Entity (PSE) without regard to adjustments for fees, refunded amounts, shipping amounts, credits, cash equivalents, discount amounts, or any other amounts (`Form 1099-K (Rev. March 2024)`, p. 5, Box 1a Note; `Instructions for Form 1099-K (Rev. March 2024)`, p. 4, Box 1a; `26 U.S.C. § 6050W(a)`). A single Form 1099-K can combine multiple personal-item sales (some at a gain, some at a loss), non-personal transactions, or amounts reported in error (`2025 Instructions for Form 1040 (Schedule 1)`, p. 88).
   - **[Interpretation for P0b]** P0b must never treat Form 1099-K Box 1a as the proceeds of a single item sale without establishing whether the statement covers one personal item or multiple transactions and what selling expenses, shipping, refunds, or other adjustments apply.

2. **What ordinary facts determine the tax outcome of one purchased, personally used item**:
   - **[Primary Source]** Gain or loss on a sale is `amount realized − adjusted basis` (`26 U.S.C. § 1001(a)–(b)`). For a non-1099-B/1099-DA/1099-S sale reported on Form 8949, column (d) *Proceeds (Sales Price)* is **net proceeds** (`gross proceeds minus selling expenses` such as broker's fees, commissions, and state and local transfer taxes; `2025 Instructions for Form 8949`, p. 6). Cost basis (`26 U.S.C. §§ 1011(a), 1012(a)`) is the original purchase cost (including sales tax and freight paid to acquire the item) plus capital improvements minus applicable basis reductions, and excluding costs deductible as current expenses (`Pub. 551 (Rev. Dec. 2025)`, pp. 2–3, 6–8; `2025 Pub. 544`, p. 4). The sources require a known basis to determine gain or loss and give no authority to substitute zero (`2025 Instructions for Form 8949`, p. 2; `2025 Pub. 544`, p. 4); leaving unknown basis as never zero is the project's posture.
   - **[Primary Source]** Personal-use property is a capital asset (`26 U.S.C. § 1221(a)`). A gain on its sale is a taxable capital gain (`26 U.S.C. §§ 61(a)(3), 1001(c), 1222`), classified as **short-term** (held 1 year or less) or **long-term** (held more than 1 year, counting from the day after acquisition through the date of sale; `26 U.S.C. § 1222(1)–(4)`; `2025 Instructions for Form 8949`, p. 2). A loss on the sale of personal-use property is **not deductible** (`26 U.S.C. §§ 165(c), 262(a)`; `2025 Instructions for Schedule D`, p. 3; `2025 Instructions for Form 8949`, p. 3).

3. **What 2025 reporting routes exist for gain vs. nondeductible personal loss**:
   - **[Primary Source]** **Gain**: Mandatory reporting on **Form 8949** (**Part I, Box C** if short-term; **Part II, Box F** if long-term, with columns (f) and (g) blank for a non-digital item always held for personal use) $\rightarrow$ **Schedule D** (**line 3** or **line 10** $\rightarrow$ **line 7** or **line 15** $\rightarrow$ **line 16**) $\rightarrow$ **Form 1040, line 7a** (and into the Form 1040 line 16 tax computation via the Qualified Dividends and Capital Gain Tax Worksheet or Schedule D Tax Worksheet when net long-term capital gain applies; if the personal item is a statutory collectible under `26 U.S.C. § 408(m)`, code `C` in column (f) and the 28% Rate Gain Worksheet on Schedule D line 18 apply). Note that if the property was converted from depreciable property to personal use, ordinary income recapture under Form 4797 Part III applies (`2025 Instructions for Schedule D`, p. 3), and digital asset transactions must use Box I or Box L rather than Box C or Box F (`2025 Instructions for Form 8949`, pp. 3–4). The 2025 Schedule 1 instructions explicitly forbid reporting a personal-item gain in the top-of-Schedule-1 entry space (`2025 Instructions for Form 1040 (Schedule 1)`, p. 88).
   - **[Primary Source]** **Nondeductible personal loss (when reported on Form 1099-K)**: The 2025 instructions give the filer **two official choices** (`2025 Instructions for Form 8949`, p. 3; `2025 Instructions for Schedule D`, pp. 3–4; `2025 Instructions for Form 1040 (Schedule 1)`, p. 88):
     - **Option 1 (Schedule 1 top-of-form entry space)**: Enter the Form 1099-K gross amount attributable to the personal item sold at a loss (or reported in error) in the header entry space at the top of Schedule 1 above Part I (*"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"*, `2025 Schedule 1 (Form 1040)`, p. 1). This field does not feed Schedule 1 line 10 or line 26, leaving Form 1040 lines 8, 9, 10, and 11a unchanged (`$0` net effect). Note that the 2025 Schedule 1 instructions for **line 24z** (`p. 100`) explicitly instruct: *"Leave line 24z blank."*
     - **Option 2 (Form 8949 with code `L` $\rightarrow$ Schedule D)**: Report the sale on Form 8949 (**Part I, Box C** if short-term; **Part II, Box F** if long-term) with proceeds in column (d), cost basis in column (e), code **`L`** in column (f), and a positive adjustment (`basis − proceeds`) in column (g) so column (h) gain/loss is `$0`, flowing to Schedule D **line 3** or **line 10** with `$0` net effect on Schedule D lines 7/15/16 and Form 1040 line 7a.
   - **[Primary Source]** **Nondeductible personal loss (when NOT reported on Form 1099-K)**: Not deductible and generally should not be reported on Form 8949, Schedule D, or Schedule 1 (`2025 Instructions for Form 8949`, p. 3; `2025 Instructions for Schedule D`, p. 3).

4. **What the adopted 2025 package (`v45`) can carry today**:
   - **[Code reading]** Static reading of the repository at milestone launch (no code was executed) shows that the highest published release (`demo.release.sli-worksheet-integration.2025@v43`) adopts `tax.us.2025.package.core-calculations@v45`. That package has **no Form 1099-K source family, bundle, or rule**, **no non-1099-B capital-asset sale family**, **no Form 8949 Box C or Box F itemization**, **no Schedule D line 3 or line 10 rule or form-field citizen**, **no Schedule 1 top-of-form 1099-K header field or rule**, and **no Form 1040 line 25b withholding consumer**. Form 8949 (`attachment.f8949.v2.json`) and Schedule D (`attachment.schedule-d.v6.json` and lines `1a`, `1b`, `8a`, `8b`) accept **only** covered Form 1099-B families (`covered-st`, `covered-lt`, `covered-w-st`, `covered-w-lt`) and require `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments = "yes"`.

---

## 1. The Rules, From 2025 Primary Sources

### 1.1 Primary Sources Consulted

All claims in Section 1 are grounded directly in the following primary authorities fetched from `irs.gov/pub/irs-prior/` and `law.cornell.edu/uscode/text/26`:

- **Internal Revenue Code (`26 U.S.C.`)**: `§§ 31, 61, 165, 262, 1001, 1011, 1012, 1221, 1222, 1223, 3406, 6050W`.
- **2025 Form 8949**, *Sales and Other Dispositions of Capital Assets* (Cat. No. 37768Z, Created 5/5/25, `f8949--2025.pdf`, 2 pp.) and **2025 Instructions for Form 8949** (Cat. No. 59421Z, Jan. 20, 2026, `i8949--2025.pdf`, 13 pp.).
- **2025 Schedule D (Form 1040)**, *Capital Gains and Losses* (Cat. No. 11338H, Created 10/6/25, `f1040sd--2025.pdf`, 2 pp.) and **2025 Instructions for Schedule D (Form 1040)** (Cat. No. 24331I, Dec. 11, 2025, `i1040sd--2025.pdf`, 16 pp.).
- **2025 Form 1040**, *U.S. Individual Income Tax Return* (Cat. No. 11320B, Created 9/5/25, `f1040--2025.pdf`, 2 pp.), **2025 Schedule 1 (Form 1040)**, *Additional Income and Adjustments to Income* (Cat. No. 71479F, Created 7/25/25, `f1040s1--2025.pdf`, 2 pp.), and **2025 Instructions for Form 1040 (and 1040-SR)** including the **2025 Instructions for Schedule 1** at pp. 88–100 (Cat. No. 11325E, Feb. 25, 2026, `i1040gi--2025.pdf`, 126 pp.).
- **Form 1099-K (Rev. March 2024)**, *Payment Card and Third Party Network Transactions* (Cat. No. 54118B, `f1099k--2024.pdf`, 6 pp.) and **Instructions for Form 1099-K (Rev. March 2024)** (Cat. No. 54721E, `i1099k--2024.pdf`, 4 pp.). Note: `f1099k--2025.pdf` and `i1099k--2025.pdf` do not exist on `irs.gov/pub/irs-prior/`; the latest revision in `irs.gov/pub/irs-prior/` is `Rev. March 2024` (`f1099k--2024.pdf` and `i1099k--2024.pdf`), which bears an open *"For calendar year"* fill-in entry on Copies A, 1, B, and 2 (`f1099k--2024.pdf`, pp. 2–4, 6).
- **2025 Publication 544**, *Sales and Other Dispositions of Assets* (Cat. No. 15074K, Feb. 6, 2026, `p544--2025.pdf`, 64 pp.).
- **Publication 551 (Rev. December 2025)**, *Basis of Assets* (Cat. No. 15094C, Dec. 2, 2025, `p551--2025.pdf`, 23 pp.).
- **2025 Publication 525**, *Taxable and Nontaxable Income* (Cat. No. 15047D, Feb. 25, 2026, `p525--2025.pdf`, 42 pp.).

---

### 1.2 Determination of Gain or Loss: Amount Realized, Basis, Selling Expenses, and Underlying Ordinary Facts

#### [Primary Source]

1. **Computation of gain or loss (`26 U.S.C. §§ 61(a)(3), 1001(a)–(c)`)**:
   - Under `26 U.S.C. § 61(a)(3)`, gross income includes *"Gains derived from dealings in property."*
   - Under `26 U.S.C. § 1001(a)`, the **gain** from the sale or other disposition of property is the excess of the **amount realized** therefrom over the **adjusted basis** provided in `§ 1011` for determining gain, and the **loss** is the excess of the adjusted basis provided in `§ 1011` for determining loss over the amount realized.
   - Under `26 U.S.C. § 1001(b)`, the **amount realized** from the sale or other disposition of property is the sum of any money received plus the fair market value of the property (other than money) received (`2025 Pub. 544`, ch. 1, p. 4, "Amount realized": total money received plus fair market value of property or services received, plus any liabilities assumed by the buyer).
   - Under `26 U.S.C. § 1001(c)`, except as otherwise provided in Subtitle A, the entire amount of the gain or loss determined under `§ 1001` on the sale or exchange of property shall be recognized.

2. **Treatment of selling expenses and Form 8949 column (d) *Proceeds (Sales Price)* (`2025 Instructions for Form 8949`, pp. 6, 9; `2025 Pub. 544`, pp. 4–5)**:
   - In `2025 Pub. 544`, ch. 1, pp. 4–5 ("Gain or Loss From Sales and Exchanges", Example 1), selling expenses (commissions, advertising, fees paid to sell the property) reduce the gross sales price to arrive at the net amount realized before subtracting adjusted basis.
   - In the `2025 Instructions for Form 8949`, p. 6, under **Column (d)—Proceeds (Sales Price)** $\rightarrow$ **"You didn't receive a Form 1099-B, Form 1099-DA, or Form 1099-S (or substitute statement)"** (which governs a personal item sold through a payment platform, even if a Form 1099-K was received):
     > *"If you didn't receive a Form 1099-B, Form 1099-DA, or Form 1099-S (or substitute statement) for a transaction, enter in column (d) the net proceeds. The net proceeds equal the gross proceeds minus any selling expenses (such as broker's fees, commissions, and state and local transfer taxes)."*
   - By contrast, the instruction immediately following on p. 6 ("You received a Form 1099-B, Form 1099-DA, or Form 1099-S (or substitute statement)") and Code `E` in the adjustment table on p. 9 restrict entering a column (g) negative adjustment with Code `E` in column (f) to cases where a Form 1099-B, Form 1099-DA, or Form 1099-S was received:
     > *"If you received a Form 1099-B, Form 1099-DA, or Form 1099-S (or substitute statement) for a transaction, enter in column (d) the proceeds shown on the form or statement you received. If there are any selling expenses or option premiums that aren't reflected on the form or statement you received (by an adjustment to either the proceeds or basis shown), enter “E” in column (f) and the necessary adjustment in column (g)."* (`2025 Instructions for Form 8949`, p. 6; likewise p. 9, Code `E`: *"You received a Form 1099-B, Form 1099-DA, or Form 1099-S (or substitute statement) for a transaction and there are selling expenses, option premiums, or digital asset transaction costs that aren't reflected on the form or statement by an adjustment to either the proceeds or basis shown"*).
   - **Tension / Reconciliation note across 2025 instructions when Form 1099-K is present**:
     - For a **gain** on a personal item reported on Form 1099-K, `2025 Instructions for Form 8949`, p. 6 directs entering **net proceeds** (`gross proceeds minus selling expenses`) in column (d) because no Form 1099-B, 1099-DA, or 1099-S was received. However, when a Form 1099-K was received and Box 1a includes platform/processing fees or shipping unreduced (`Form 1099-K`, p. 5, Box 1a Note), the 2025 Form 8949 instructions do not explicitly address whether a filer who wants column (d) to match the Form 1099-K Box 1a gross amount may instead enter the gross Form 1099-K amount in column (d) and adjust in column (g), or must strictly enter net proceeds in column (d).
     - For a **loss** on a personal item reported on Form 1099-K, `2025 Instructions for Schedule 1` (`i1040gi--2025.pdf`, p. 88) instructs filers to *"enter the amount that was included in error or for personal items sold at a loss in the entry space at the top of Schedule 1"* (for example, entering `$700` when a Form 1099-K shows `$700` in box 1(a) for a couch bought for `$1,000` and sold for `$700`), and `2025 Instructions for Form 8949`, p. 3 ("Line 1") states for the Form 8949 Code `L` route: *"Enter the proceeds in column (d), enter the cost basis in column (e), enter “L” in column (f), and enter in column (g) the amount of the adjustment that will result in $0 as the gain or loss in column (h)."*

3. **Determination of cost basis and adjusted basis (`26 U.S.C. §§ 1011(a), 1012(a)`; `Pub. 551 (Rev. Dec. 2025)`, pp. 2–3, 6–8; `2025 Instructions for Form 8949`, pp. 2, 6)**:
   - Under `26 U.S.C. § 1012(a)`, *"The basis of property shall be the cost of such property, except as otherwise provided in this subchapter and subchapters C […], K […], and P […]."* (bracketed ellipses mark omitted parenthetical descriptions of the subchapters; statute text not among the extracted 2025 source files and not re-checked)
   - Under `26 U.S.C. § 1011(a)`, the **adjusted basis** for determining the gain or loss from the sale or other disposition of property is the basis determined under `§ 1012` (or other applicable sections), adjusted as provided in `§ 1016`.
   - Under `Pub. 551 (Rev. Dec. 2025)`, pp. 2–3 ("Cost Basis"), *"The basis of property you buy is usually its cost. The cost is the amount you pay in cash, debt obligations, other property, or services. Your cost also includes amounts you pay for the following items."* — followed at the top of **p. 3** by the verbatim bullet items:
     - *"Sales tax."* (`Pub. 551`, p. 3);
     - *"Freight."* (`Pub. 551`, p. 3);
     - *"Installation and testing."* (`Pub. 551`, p. 3);
     - *"Excise taxes."* (`Pub. 551`, p. 3);
     - *"Legal and accounting fees (when they must be capitalized)."* (`Pub. 551`, p. 3);
     - *"Revenue stamps."* (`Pub. 551`, p. 3);
     - *"Recording fees."* (`Pub. 551`, p. 3);
     - *"Real estate taxes (if assumed for the seller)."* (`Pub. 551`, p. 3).
   - Under `Pub. 551`, pp. 6–8 ("Adjusted Basis", including *"Table 1. Examples of Increases and Decreases to Basis"* at p. 7) and `2025 Pub. 544`, p. 4 ("Adjusted basis"):
     - **Deducting vs. capitalizing costs**: Under *"Deducting vs. Capitalizing Costs"* (`Pub. 551`, p. 7), *"Don't add to your basis costs you can deduct as current expenses."*
     - **Increases to basis**: capital improvements or additions with a useful life of more than 1 year and restoration of damaged property (`Pub. 551`, pp. 6–7). Repair and maintenance costs that do not add to the property's value or appreciably prolong its life do not increase basis (`Pub. 551`, p. 6).
     - **Decreases to basis**: *"Rebates treated as adjustments to the sales price."* and *"Casualty and theft losses and insurance reimbursement."* (`Pub. 551`, p. 8; see also Table 1 on p. 7: *"Casualty or theft loss deductions and insurance reimbursements"*). (Depreciation/amortization applies only if the property was used in a business or for the production of income; for a purely personal-use item, no depreciation is allowable.)
   - **Recordkeeping and unknown basis (`2025 Instructions for Form 8949`, p. 2; `2025 Pub. 544`, p. 4)**:
     - *"You must keep accurate records that show the basis and, if applicable, adjusted basis of your property."* (`2025 Instructions for Form 8949`, p. 2, "Basis and Recordkeeping").
     - *"You must know the basis of your property to determine whether you have a gain or loss from its sale or other disposition."* (`2025 Pub. 544`, p. 4, "Basis"). The sources require a known basis and give no authority to substitute zero; leaving unknown cost basis as never treated as `$0` is the project posture (if basis is unknown, gain or loss cannot be determined from the missing figure).

#### [Interpretation for P0b]

For one purchased, personally used item sold through a payment platform, the determination of gain or loss depends on the following **ordinary facts**:
1. **Acquisition & personal-use boundary facts**:
   - That the person **purchased** the item (rather than receiving it as a gift, inheritance, prize, or business inventory, which follow different basis or character rules under `26 U.S.C. §§ 1014, 1015, 1221(a)(1)`).
   - That the person held and used the item **personally** (not in a trade, business, rental, or profit-seeking venture, and not as a collectible or digital asset if the route excludes special-rate/digital-asset classes).
2. **Basis facts (what the item cost the seller)**:
   - What the person paid to buy the item (including sales tax and freight/shipping paid at purchase), plus any lasting improvements, minus any rebates or casualty/insurance recoveries—or whether the person no longer knows or cannot tell what the item cost.
3. **Amount-realized and selling-expense facts (what the seller received and paid to sell it)**:
   - The gross sale price of that specific item (after any buyer refund, return, credit, or price adjustment for that sale).
   - Selling expenses incurred for that sale: platform/marketplace commissions, payment-processing fees, and seller-paid shipping/postage/packaging costs (and whether buyer-paid shipping or platform-collected sales tax was included in the gross payment figure).

---

### 1.3 Character of a Personal-Use Item and Why a Loss Is Not Deductible

#### [Primary Source]

1. **Personal-use property is a capital asset (`26 U.S.C. § 1221(a)`)**:
   - `26 U.S.C. § 1221(a)` defines the term **"capital asset"** as *"property held by the taxpayer (whether or not connected with his trade or business), but does not include—"* eight enumerated exclusions in `§ 1221(a)(1)–(8)` (stock in trade/inventory/property held primarily for sale to customers in the ordinary course of a trade or business; depreciable or real property used in a trade or business; certain self-created copyrights/compositions/patents; accounts or notes receivable acquired in a trade or business; U.S. government publications received other than by purchase at the public price; commodities derivative financial instruments held by a dealer; hedging transactions; and supplies regularly used or consumed in a trade or business).
   - Because an item bought and used personally is property held by the taxpayer and falls outside `§ 1221(a)(1)–(8)`, it is a **capital asset**.
   - Confirmed verbatim in `2025 Instructions for Schedule D (Form 1040)`, p. 1 ("Capital Asset"):
     > *"Most property you own and use for personal purposes or investment is a capital asset. For example, your house, furniture, car, stocks, and bonds are capital assets."*
   - Confirmed in `2025 Pub. 544`, p. 30 ("Personal-use property"; p. 54 repeats the heading with different wording): *"Generally, property held for personal use is a capital asset."*

2. **Gain on the sale of personal-use property is a taxable capital gain (`26 U.S.C. §§ 61(a)(3), 1001(c), 1222`)**:
   - `2025 Instructions for Schedule D (Form 1040)`, p. 3 ("Capital Assets Held for Personal Use"):
     > *"Generally, gain from the sale or exchange of a capital asset held for personal use is a capital gain. Report it on Form 8949 with box C or box I checked (if the transaction is short term) or box F or box L checked (if the transaction is long term)."*
   - `2025 Pub. 525`, p. 35 ("Sale of personal items", following Example 39):
     > *"If you sold an item you owned for personal use, such as a car, refrigerator, furniture, stereo, jewelry, or silverware, your gain is taxable as a capital gain. Report it as explained in the Instructions for Schedule D (Form 1040). You can't deduct a loss."*

3. **Loss on the sale of personal-use property is NOT deductible (`26 U.S.C. §§ 165(c), 165(f), 262(a)`)**:
   - `26 U.S.C. § 165(a)` states the general rule that a deduction is allowed for any loss sustained during the taxable year and not compensated for by insurance or otherwise.
   - `26 U.S.C. § 165(c)` (**Limitation on losses of individuals**) restricts `§ 165(a)` for individuals:
     > *"In the case of an individual, the deduction under subsection (a) shall be limited to—*
     > *(1) losses incurred in a trade or business;*
     > *(2) losses incurred in any transaction entered into for profit, though not connected with a trade or business; and*
     > *(3) except as provided in subsection (h), losses of property not connected with a trade or business or a transaction entered into for profit, if such losses arise from fire, storm, shipwreck, or other casualty, or from theft."*
   - `26 U.S.C. § 165(f)` ("Capital losses") further limits allowable capital losses to the extent provided in `§§ 1211` and `1212` (it does not make a loss deductible if disallowed by `§ 165(c)`).
   - `26 U.S.C. § 262(a)` ("Personal, living, and family expenses") provides: *"Except as otherwise expressly provided in this chapter, no deduction shall be allowed for personal, living, or family expenses."*
   - Because selling a personally used item is not a trade or business (`§ 165(c)(1)`), not a transaction entered into for profit (`§ 165(c)(2)`), and not a casualty or theft (`§ 165(c)(3)`), a loss on its sale is disallowed by statute.
   - Confirmed in `2025 Instructions for Schedule D (Form 1040)`, p. 3 ("Capital Assets Held for Personal Use"):
     > *"Loss from the sale or exchange of a capital asset held for personal use isn't deductible."*
   - Confirmed in `2025 Instructions for Form 8949`, p. 3 ("Line 1"):
     > *"Loss on the sale of personal property is not deductible, and generally should not be reported on Form 8949."*
   - Confirmed in `2025 Pub. 544`, ch. 1, p. 5 ("Amount recognized"):
     > *"Also, a loss from the sale or other disposition of property held for personal use is not deductible, except in the case of a casualty or theft loss."*

#### [Interpretation for P0b]

- A personal loss is **never** a deductible capital loss and **never** offsets capital gains (not even another personal-item gain reported on the same Form 1099-K; see `2025 Instructions for Schedule 1`, p. 88, *"Example–Personal items sold at a loss and a gain"*, where a `$300` loss on a couch and a `$400` gain on a handbag on the same `$1,900` Form 1099-K result in `$700` reported as a zero-effect personal loss and the full `$400` reported as a taxable capital gain on Form 8949 and Schedule D).
- In addition, if a personal item is a **collectible** under `26 U.S.C. § 408(m)` (such as a work of art, rug, antique, metal or gem, stamp or coin, or alcoholic beverage; `26 U.S.C. § 1(h)(4)–(5)`; `2025 Instructions for Schedule D`, p. 11, "28% Rate Gain Worksheet"), a **long-term gain** on that item is a 28% rate gain requiring code `C` in Form 8949 column (f) (`2025 Instructions for Form 8949`, p. 8) and Schedule D line 18. P0b should note whether long-term collectibles are excluded from or handled by the bounded personal-item slice.

---

### 1.4 Holding-Period Distinction and Required Dates

#### [Primary Source]

1. **Statutory threshold (`26 U.S.C. § 1222(1)–(4)`)**:
   - **Short-term capital gain / loss** (`26 U.S.C. § 1222(1)–(2)`): gain or loss from the sale or exchange of a capital asset held for **not more than 1 year** (1 year or less).
   - **Long-term capital gain / loss** (`26 U.S.C. § 1222(3)–(4)`): gain or loss from the sale or exchange of a capital asset held for **more than 1 year**.
   - (`26 U.S.C. § 1223` provides special tacked holding-period rules for exchanges, gifts, and wash sales; none apply to an ordinary purchased personal item.)

2. **Counting rule (`2025 Instructions for Form 8949`, p. 2; `2025 Instructions for Schedule D`, p. 2; `2025 Pub. 544`, ch. 4, p. 54)**:
   - `2025 Instructions for Form 8949`, p. 2 ("Short-Term or Long-Term"):
     > *"Separate your capital gains and losses according to how long you held or owned the property. The holding period for short-term capital gains and losses is generally 1 year or less. ... Report these transactions on Part I of Form 8949 (or line 1a of Schedule D if you can use Exception 1 under the instructions for line 1, later). The holding period for long-term capital gains and losses is generally more than 1 year. ... Report these transactions on Part II of Form 8949 (or line 8a of Schedule D if you can use Exception 1 under the instructions for line 1, later). To figure the holding period, begin counting on the day after you received the property and include the day you disposed of it."*
   - `2025 Pub. 544`, ch. 4, p. 54 ("Holding period", Example):
     > *"Example. If you bought an asset on June 17, 2024, you should start counting on June 18, 2024. If you sold the asset on June 17, 2025, your holding period is not longer than 1 year, but if you sold it on June 19, 2025, your holding period is longer than 1 year."*
     The publication quotation is accurate and leaves June 18, 2025 unclassified. Applying the Form 8949 counting sentence quoted above ("begin counting on the day after you received the property and include the day you disposed of it"), counted from June 18, 2024 through the sale date inclusive, June 17, 2025 is 365 days (not longer than 1 year) and June 18, 2025 is 366 days (more than 1 year, hence long-term). A sale on June 18, 2025, of property acquired June 17, 2024, is long-term.

3. **Dates required by the 2025 forms (`2025 Form 8949`, pp. 1–2; `2025 Instructions for Form 8949`, p. 6; `2025 Schedule 1`, p. 1)**:
   - Whenever a transaction is reported on **Form 8949** (which includes **every gain** on a personal item, and any Form 1099-K **loss** reported via the Form 8949 Code `L` route):
     - **Part selection (Part I vs. Part II)** requires knowing whether the holding period is `1 year or less` (Part I, Short-Term, Box C) or `more than 1 year` (Part II, Long-Term, Box F).
     - **Column (b) (*Date acquired*)** requires entering the acquisition date in `Mo., day, yr.` format (e.g., `05/15/2024`; `2025 Instructions for Form 8949`, p. 6, "Column (b)—Date Acquired"). The instructions allow `"VARIOUS"` only for a permissible aggregate row of transactions (or `"INHERITED"` for inherited property), neither of which replaces the date of a single purchased item.
     - **Column (c) (*Date sold or disposed of*)** requires entering the sale/disposition date in `Mo., day, yr.` format (`2025 Instructions for Form 8949`, p. 6, "Column (c)—Date Sold or Disposed Of").
   - By contrast, when a Form 1099-K personal item sold at a **loss** is reported via the **Schedule 1 top-of-form entry space** (`2025 Schedule 1`, p. 1; `2025 Instructions for Schedule 1`, p. 88), only a single dollar amount is entered at the top of Schedule 1; no acquisition date, sale date, or short-term/long-term distinction appears on Schedule 1.

#### [Interpretation for P0b]

- If the return path uses **Form 8949** (required for any personal-item **gain**, and optional via Code `L` for a Form 1099-K personal-item **loss**), the person must supply `date acquired` and `date sold` (or P0b must define what happens if the person knows whether they owned the item for more than 1 year vs. 1 year or less, or cannot recall the exact day of purchase—since Form 8949 column (b) asks for `Mo., day, yr.`).
- If the person had a **loss** reported on Form 1099-K and uses the **Schedule 1 top-of-form entry space**, neither `date acquired`, `date sold`, nor the 1-year holding period affects the Schedule 1 entry.

---

### 1.5 Every 2025 Reporting Route Named in the Instructions (Gain vs. Nondeductible Personal Loss)

#### [Primary Source]

The 2025 instructions establish the following reporting routes across **Form 8949**, **Schedule D (Form 1040)**, **Schedule 1 (Form 1040)**, and **Form 1040**:

#### Summary Matrix of 2025 Primary-Source Reporting Routes

| Outcome | Form 1099-K Received? | Official 2025 Route(s) | Form 8949 Part / Box / Columns | Schedule D Line(s) | Schedule 1 Line(s) | Form 1040 Line(s) | Filer Choice? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Gain** (`net proceeds > adjusted basis`), held **$\le$ 1 year** (short-term) | Yes or No | **Form 8949 Part I $\rightarrow$ Schedule D Part I $\rightarrow$ Form 1040** (`i8949--2025.pdf` pp. 1, 3–4, 6; `i1040sd--2025.pdf` p. 3; `i1040gi--2025.pdf` p. 88) | **Part I, Box C** checked (for a non-digital item always held for personal use; excludes prior depreciable use requiring Form 4797 Part III and digital assets requiring Box I); col. (a) description, col. (b) date acquired, col. (c) date sold, col. (d) net proceeds, col. (e) basis, cols. (f)–(g) blank, col. (h) `d − e` (gain) | **Line 3** (cols. d, e, g, h) $\rightarrow$ **Line 7** $\rightarrow$ **Line 16** | None (*explicitly forbidden* on Schedule 1 top line, `i1040gi--2025.pdf` p. 88) | **Line 7a** $\rightarrow$ **Line 9** $\rightarrow$ **Line 11a** $\rightarrow$ **Line 15** $\rightarrow$ **Line 16** | **No** — Form 8949 Box C + Schedule D line 3 is mandatory for a non-digital item always held for personal use |
| **Gain** (`net proceeds > adjusted basis`), held **$>$ 1 year** (long-term) | Yes or No | **Form 8949 Part II $\rightarrow$ Schedule D Part II $\rightarrow$ Form 1040** (`i8949--2025.pdf` pp. 1, 3–4, 6, 8; `i1040sd--2025.pdf` pp. 3, 11; `i1040gi--2025.pdf` p. 88) | **Part II, Box F** checked (for a non-digital item always held for personal use; excludes prior depreciable use requiring Form 4797 Part III and digital assets requiring Box L); cols. (a)–(e) as above; cols. (f)–(g) blank (or code `C` + `$0` if `§ 408(m)` collectible); col. (h) `d − e` (gain) | **Line 10** (cols. d, e, g, h) $\rightarrow$ **Line 15** $\rightarrow$ **Line 16** (plus **Line 18** if collectible) | None (*explicitly forbidden* on Schedule 1 top line, `i1040gi--2025.pdf` p. 88) | **Line 7a** $\rightarrow$ **Line 9** $\rightarrow$ **Line 11a** $\rightarrow$ **Line 15** $\rightarrow$ **Line 16** (via QDCG Tax Worksheet or Schedule D Tax Worksheet) | **No** — Form 8949 Box F + Schedule D line 10 is mandatory for a non-digital item always held for personal use |
| **Loss** (`net proceeds < adjusted basis`) | **No** (no Form 1099-K, and not Form 1099-S real estate) | **Do not report** (`i8949--2025.pdf` p. 3; `i1040sd--2025.pdf` p. 3; `p525--2025.pdf` p. 35) | None | None | None | None (`$0` effect) | None (generally should not be reported) |
| **Loss** (`net proceeds < adjusted basis`) | **Yes** (reported on Form 1099-K) | **Option 1**: **Schedule 1 top-of-form entry space** (`f1040s1--2025.pdf` p. 1; `i1040gi--2025.pdf` p. 88; `i8949--2025.pdf` p. 3; `i1040sd--2025.pdf` p. 3) | None | None | **Top-of-form entry space** above Part I: *"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"* (does not feed line 10 or line 26) | None (`$0` effect on lines 7a, 8, 9, 10, 11a) | **Yes** — filer may choose **Option 1** (Schedule 1 top entry space) **or Option 2** (Form 8949 Code `L`) |
| **Loss** (`net proceeds < adjusted basis`) | **Yes** (reported on Form 1099-K) | **Option 2**: **Form 8949 (Code `L`) $\rightarrow$ Schedule D** (`i8949--2025.pdf` pp. 3, 9; `i1040sd--2025.pdf` pp. 3–4; `i1040gi--2025.pdf` p. 88) | **Part I, Box C** (if $\le$ 1 yr) or **Part II, Box F** (if $>$ 1 yr); col. (d) proceeds, col. (e) basis, col. (f) **`"L"`**, col. (g) positive adjustment `e − d`, col. (h) **`$0`** | **Line 3** (if Box C) or **Line 10** (if Box F): cols. (d), (e), (g) carry row totals; col. (h) is `$0` $\rightarrow$ `$0` net effect on lines 7, 15, 16 | None | **Line 7a** receives `$0` net effect from this transaction | **Yes** — alternative to Option 1 |

#### Detailed Citations for Each Route

1. **Gain Route (Form 8949 Box C / Box F $\rightarrow$ Schedule D Line 3 / Line 10 $\rightarrow$ Form 1040 Line 7a)**:
   - `2025 Instructions for Form 8949`, p. 1 (under "Purpose of Form", the "Individuals." paragraph; the quoted text omits intervening bullets with an ellipsis):
     > *"Individuals use Form 8949 to report the following.*
     > *• The sale or exchange of a capital asset reported on a Form 1099-K, Form 1099-B, or Form 1099-DA.*
     > *...*
     > *• The sale or exchange of a capital asset not reported on another form or schedule."*
   - `2025 Instructions for Form 8949`, p. 3 ("Line 1"):
     > *"If you received a Form 1099-K reporting proceeds from the sale of personal property that resulted in gain, that transaction is taxable and must be entered on Form 8949."*
   - `2025 Instructions for Schedule D (Form 1040)`, p. 3 ("Capital Assets Held for Personal Use"):
     > *"Report it on Form 8949 with box C or box I checked (if the transaction is short term) or box F or box L checked (if the transaction is long term). However, if you converted depreciable property to personal use, all or part of the gain on the sale or exchange of that property may have to be recaptured as ordinary income. Use Part III of Form 4797 to figure the amount of ordinary income recapture."*
     Boxes C and F (with columns (f) and (g) blank) apply to a non-digital item that was always held for personal use. Digital asset transactions not reported on Form 1099-DA/1099-B use boxes I and L (`2025 Instructions for Form 8949`, p. 4: *"Digital asset transactions should not be reported using box C or F"*), and property converted from depreciable use requires ordinary income recapture on Form 4797 Part III.
   - `2025 Instructions for Form 8949`, pp. 3–4 ("Box C or Box I" and "Box F or Box L") and `2025 Form 8949`, pp. 1–2:
     - Part I checkboxes (`f8949--2025.pdf`, p. 1): Boxes A and B are for transactions reported on `Form(s) 1099-B`; Boxes G, H, and I are for `digital asset transactions`; **Box C** is:
       > *"(C) Short-term transactions, other than digital asset transactions, not reported to you on Form 1099-B or Form 1099-DA"*
     - Part II checkboxes (`f8949--2025.pdf`, p. 2): Boxes D and E are for transactions reported on `Form(s) 1099-B`; Boxes J, K, and L are for `digital asset transactions`; **Box F** is:
       > *"(F) Long-term transactions, other than digital asset transactions, not reported to you on Form 1099-B or Form 1099-DA"*
     - Note that `Form 8949 Exceptions` (`i8949--2025.pdf`, p. 3; `i1040sd--2025.pdf`, p. 10, "Lines 1a and 8a—Transactions Not Reported on Form 8949") allow aggregating transactions directly on Schedule D line 1a or line 8a **only** when the transactions were reported on **Form 1099-B** or **Form 1099-DA** (or substitute statement) showing basis was reported to the IRS and no adjustments/codes are needed. A non-1099-B/1099-DA personal item sale (including one reported on Form 1099-K) meets none of those conditions and is **never** eligible for Schedule D line 1a or line 8a; it must go through Form 8949 Box C or Box F to Schedule D **line 3** or **line 10** (`f1040sd--2025.pdf`, p. 1).
   - `2025 Instructions for Form 1040 (Schedule 1)`, p. 88 ("Form(s) 1099-K"):
     > *"If you received a Form 1099-K for a personal item that you sold at a gain, don't report this amount in the entry space at the top of Schedule 1; instead, report it as you would report any other capital gain on Form 8949 and Schedule D."*

2. **Nondeductible Personal Loss Route — Two Filer-Elective Options When Reported on Form 1099-K**:
   - `2025 Instructions for Form 8949`, p. 3 ("Line 1"):
     > *"Loss on the sale of personal property is not deductible, and generally should not be reported on Form 8949. However, if you receive a Form 1099-K reporting proceeds from the sale of personal property that resulted in a loss, you should report the loss with an offsetting entry. You can do this either on Form 1040, in the entry space at the top of Schedule 1, or on Form 8949, by entering an adjustment when reporting the proceeds and basis of the property, as follows. Enter “L” in column (f) as the code explaining the loss is nondeductible. Then enter the amount of the nondeductible loss as a positive number in column (g). Enter the proceeds in column (d), enter the cost basis in column (e), enter “L” in column (f), and enter in column (g) the amount of the adjustment that will result in $0 as the gain or loss in column (h)."*
   - `2025 Instructions for Schedule D (Form 1040)`, pp. 3–4 ("Capital Assets Held for Personal Use" and "Certain Nondeductible Losses"):
     > *"Loss from the sale or exchange of a capital asset held for personal use isn't deductible. But if you had a loss from the sale or exchange of real estate held for personal use for which you received a Form 1099-S, you must report the transaction on Form 8949 even though the loss isn't deductible. Also, if you had a loss from the sale or exchange of personal property for which you received a Form 1099-K, you must report the transaction on Form 8949 or on Schedule 1 (Form 1040) even though the loss isn't deductible."* (`p. 3`, "Capital Assets Held for Personal Use")
     >
     > *"Report a transaction that results in a nondeductible loss in Part I or Part II of Form 8949 (depending on how long you held the property). Unless you received a Form 1099-B or Form 1099-DA for the sale or exchange, check box C or box I at the top of Part I or box F or box L at the top of Part II of Form 8949 (depending on how long you owned the property). Complete all columns. Because the loss isn't deductible, enter “L” in column (f). Enter the amount of the nondeductible loss as a positive number in column (g). Complete column (h). See the Instructions for Form 8949, columns (f), (g), and (h)."* (`pp. 3–4`, "Certain Nondeductible Losses")
   - `2025 Instructions for Form 8949`, p. 9 ("How To Complete Form 8949, Columns (f) and (g)" — Code `L`):
     > **Column (f) Code `L`** (*"You have a nondeductible loss other than a loss indicated by code W"*):
     > *"Report the sale or exchange on Form 8949 and enter the amount of the nondeductible loss as a positive number in column (g). See Certain Nondeductible Losses in the Instructions for Schedule D (Form 1040)."*
   - `2025 Schedule 1 (Form 1040)`, p. 1 (top header line above Part I) and `2025 Instructions for Form 1040 (Schedule 1)`, p. 88 ("Form(s) 1099-K"):
     - Printed text at the top of 2025 Schedule 1 (`f1040s1--2025.pdf`, p. 1):
       > *"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"*
     - `2025 Instructions for Schedule 1` (`i1040gi--2025.pdf`, p. 88):
       > *"If, for tax year 2025, you received a Form(s) 1099-K that shows payments that were included in error (for example, money for gifts or reimbursements) or for personal items that you sold at a loss (for example, an old refrigerator), enter the amount that was included in error or for personal items sold at a loss in the entry space at the top of Schedule 1.*
       > *• If the entire amount reported to you on Form(s) 1099-K was in error or for personal items sold at a loss, enter the total amount from Form(s) 1099-K, box 1(a), in the entry space at the top of Schedule 1.*
       > *• If only some of the amount reported to you on Form(s) 1099-K in box 1(a) was in error or for personal items sold at a loss, only enter the amount that was in error or for personal items sold at a loss in the entry space at the top of Schedule 1. The remaining amounts reported to you on Form(s) 1099-K should be reported elsewhere on your return depending on the nature of the transactions.*
       > *• If you received more than one incorrect Form(s) 1099-K, with amounts reported in error or for personal items sold at a loss, add the incorrect amounts together and enter the total incorrect amount in the entry space at the top of Schedule 1. The remaining amounts reported to you on Form(s) 1099-K in box 1(a) should be reported elsewhere on your return depending on the nature of the transactions.*
       > *...*
       > ***Example–Personal item sold at a loss.*** *You bought a couch for $1,000 and sold it through a third-party vendor for $700, which was reported in box 1(a) of your Form 1099-K. You would enter $700 in the entry space at the top of Schedule 1.*
       >
       > ***Example–Personal items sold at a loss and a gain.*** *In addition to selling your couch for $700, you also sold a handbag that you bought for $800 and sold for $1,200. Your Form 1099-K shows $1,900 in box 1(a). You would enter $700 in the entry space at the top of Schedule 1 for your loss on selling the couch, and the remaining $400 of gain from the sale of the handbag would be reported as capital gain on Form 8949 and Schedule D."*
   - **What the 2025 Schedule 1 instructions say about line 24z** (`i1040gi--2025.pdf`, p. 100):
     - Under the heading "Line 24z", the full instruction text is: *"Leave line 24z blank."*
     - The 2025 instruction pages examined for this report name the top-of-Schedule-1 entry space (`i1040gi--2025.pdf`, p. 88) and the Form 8949 Code `L` adjustment (`i8949--2025.pdf`, p. 3) as the offsetting entries for a Form 1099-K personal-item loss. They do not describe an offsetting entry on Schedule 1 lines 8z/24z for this purpose. This report makes no claim about earlier-year guidance or about IRS.gov web pages, which were not examined here.

3. **Zero-Gain / Break-Even Case (`Amount Realized == Adjusted Basis`) When Reported on Form 1099-K**:
   - **[Primary Source]** On **Form 8949** (Box C if short-term, Box F if long-term), entering `column (d) = proceeds` and `column (e) = basis` where `d == e` yields `$0` in `column (h)` directly (`d − e = 0`), with columns (f) and (g) blank (Code `L` applies only when *"You have a nondeductible loss other than a loss indicated by code W"*, `i8949--2025.pdf`, p. 9). By contrast, the 2025 Schedule 1 top-of-form entry space is printed as *"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"* (`f1040s1--2025.pdf`, p. 1; `i1040gi--2025.pdf`, p. 88), and the 2025 Schedule 1 instructions do not explicitly state whether a break-even (`$0` gain / `$0` loss) sale reported on Form 1099-K may be entered at the top of Schedule 1 or must use Form 8949.

#### [Interpretation for P0b]

- P0b faces an explicit architectural/product boundary question for a Form 1099-K personal loss:
  - The 2025 instructions leave the filer a genuine choice between **Schedule 1 top-of-form entry space** and **Form 8949 (Box C/F + Code `L`) $\rightarrow$ Schedule D (line 3/10)**.
  - Notice the asymmetry in fact requirements between the two loss routes:
    - **Schedule 1 top-of-form route** for a personal item sold at a loss requires knowing that the item was a personal item sold at a loss (`net proceeds < adjusted basis`) and the Form 1099-K amount attributable to that sale, **without** requiring exact `date acquired`, `date sold`, or a specific dollar basis figure on the printed form (though the taxpayer must know basis exceeded proceeds to know it was sold at a loss).
    - **Form 8949 Code `L` route** requires exact `date acquired` (column b), `date sold` (column c), short-term vs. long-term classification (Box C vs. Box F), `proceeds` (column d), `cost or other basis` (column e), code `"L"` (column f), and `basis − proceeds` (column g).
  - For a **gain**, only the **Form 8949 (Box C/F) $\rightarrow$ Schedule D (line 3/10) $\rightarrow$ Form 1040 line 7a** route is lawful.

---

### 1.6 Form 1099-K Box-by-Box Analysis, Why Gross Payments Differ From Sale Proceeds, and Direct Return Feeds

#### [Primary Source]

1. **Statutory authority and 2025 reporting threshold (`26 U.S.C. § 6050W`; `2025 Instructions for Form 1040`, pp. 7, 88)**:
   - Under `26 U.S.C. § 6050W(a)–(d)`, a **Payment Settlement Entity (PSE)**—either a merchant acquiring entity for **payment card** transactions (`§ 6050W(b)(1)(A)`) or a **third party settlement organization (TPSO)** for **third party network** transactions (`§ 6050W(b)(1)(B)`, `§ 6050W(d)(3)`)—must file an information return (Form 1099-K) setting forth the gross amount of reportable payment transactions for each participating payee.
   - For 2025, `2025 Instructions for Form 1040`, p. 7 ("Updated reporting requirements for Form 1099-K") and p. 88 (Schedule 1 instructions, "Form(s) 1099-K") state:
     > *"Payment card companies, payment apps, and online marketplaces will be required to send you a Form 1099-K only if the amount of your business transactions during the year is more than $20,000 and the total number of your transactions is more than 200."*
     This sentence governs whether a form must be issued. P0b should not ask the person to reconstruct the threshold in order to report a Form 1099-K already received.

2. **What each box on Form 1099-K (`Rev. March 2024`, in effect for 2025) reports (`f1099k--2024.pdf`, pp. 2, 5; `i1099k--2024.pdf`, pp. 3–4)**:

| Form 1099-K Locator | Official Label | What Primary Sources Say It Reports |
| --- | --- | --- |
| **Filer / PSE Checkboxes** | `FILER'S name...` / `Check to indicate if FILER is a:` (`Payment settlement entity (PSE)` vs. `Electronic Payment Facilitator (EPF)/Other third party`) / `Check to indicate transactions reported are:` (`Payment card` vs. `Third party network`) | Identifies whether the filer is the PSE or an EPF/other third party, and whether the form reports payment card transactions or third party network transactions. If a PSE processes both payment card and third party network transactions for the same payee, it must file separate Forms 1099-K (`i1099k--2024.pdf`, p. 3). |
| **Account number** | `Account number (see instructions)` | Unique number assigned by the filer to distinguish the payee's account; required if the payee has multiple accounts (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4). |
| **Box 1a** | `Gross amount of payment card/third party network transactions` | The aggregate gross dollar amount of all reportable payment transactions made to the payee through the PSE during the calendar year, determined on the date of each transaction, **without regard to any adjustments for credits, cash equivalents, discount amounts, fees, refunded amounts, shipping amounts, or any other amounts** (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4). |
| **Box 1b** | `Card Not Present transactions` | The aggregate gross dollar amount of all reportable payment transactions during the calendar year where the card was not present at the time of the transaction or the card number was keyed in (e.g., online, phone, or catalogue sales). Typically not reported (left blank) when the `Third party network` box is checked (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4). |
| **Box 2** | `Merchant category code` | The 4-digit Merchant Category Code (MCC) used by the payment card industry to classify the payee by the goods or services provided. If the filer (such as a TPSO) does not use an industry classification system, this box is left blank (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4). |
| **Box 3** | `Number of payment transactions` | The total number of payment transactions (**not** including refund transactions) processed through the payment card/third party network during the calendar year (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4). |
| **Box 4** | `Federal income tax withheld` | Backup withholding under `26 U.S.C. § 3406` (24% rate when a payee fails to furnish a correct TIN). Copy B (`f1099k--2024.pdf`, p. 5) instructs the payee: *"Include this amount on your income tax return as tax withheld."* (`i1099k--2024.pdf`, p. 4). |
| **Boxes 5a–5l** | `January` through `December` | The gross amount of reportable payment transactions for each month of the calendar year (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4). |
| **Boxes 6, 7, 8** | `State`, `State identification no.`, `State income tax withheld` | State abbreviation, state ID number, and state income tax withheld for up to two states (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4). |

3. **How Box 1a gross payments differ from the sale proceeds of one personal item (`f1099k--2024.pdf`, p. 5; `i1099k--2024.pdf`, p. 4; `i8949--2025.pdf`, p. 6; `i1040gi--2025.pdf`, p. 88)**:
   - `Instructions for Form 1099-K (Rev. March 2024)`, p. 4 ("Box 1a. Gross Payment Card/Third Party Network Transactions") states verbatim:
     > *"Gross amount means the total dollar amount of total reportable payment transactions for each participating payee without regard to any adjustments for credits, cash equivalents, discount amounts, fees, refunded amounts, shipping amounts, or any other amounts. The dollar amount of each transaction is determined on the date of the transaction."*
   - `Form 1099-K (Rev. March 2024)`, p. 5 (the "Instructions for Payee" panel, Box 1a entry) states verbatim:
     > *"Shows the aggregate gross amount of payment card/third party network transactions made to you through the PSE during the calendar year.*
     > *...*
     > ***Note:*** *The gross amount is the total dollar amount of total reportable payment transactions without regard to any adjustments for credits, cash equivalents, discount amounts, fees, refunded amounts, shipping amounts, or any other amounts. The dollar amount of each transaction is determined on the date of the transaction."*

   Consequently, Form 1099-K Box 1a differs from the net sale proceeds (`amount realized` net of selling expenses) of one personal item in five specific ways:
   - **Fees and commissions (`fees`)**: Box 1a is not reduced by platform fees, marketplace commissions, or payment-processing fees withheld from the seller's payout, whereas Form 8949 column (d) for a non-1099-B/1099-DA/1099-S sale requires **net proceeds** (`gross proceeds minus selling expenses`, `2025 Instructions for Form 8949`, p. 6).
   - **Refunds, returns, credits, and discounts (`refunded amounts`, `credits`, `discount amounts`)**: Box 1a records the gross transaction amount on the transaction date and is **not** reduced when a transaction is later refunded, returned, credited, or discounted (and Box 3's transaction count explicitly excludes refund transactions; `f1099k--2024.pdf`, p. 5).
   - **Shipping amounts (`shipping amounts`)**: Box 1a includes buyer-paid shipping charges settled through the PSE without subtracting shipping/postage labels purchased by the seller.
   - **Sales tax or other pass-through charges (`or any other amounts`)**: If sales tax or other buyer charges are settled as part of the gross transaction amount, Box 1a is unadjusted for them.
   - **Multi-transaction / multi-purpose aggregation (*"the aggregate gross amount of payment card/third party network transactions made to you through the PSE during the calendar year"*, `f1099k--2024.pdf`, p. 5)**: Box 1a sums **every** reportable transaction on that account for the entire calendar year—which can mix multiple personal-item sales (some at a gain and some at a loss, as in the couch + handbag example in `2025 Instructions for Schedule 1`, p. 88), business or gig receipts, or non-taxable gifts/reimbursements included in error.

4. **Whether any Form 1099-K box feeds the return directly**:
   - **Box 4 (`Federal income tax withheld`)** feeds **Form 1040, line 25b (`Federal income tax withheld from: Form(s) 1099`)** directly (`2025 Form 1040`, p. 2, line 25b; `2025 Instructions for Form 1040`, p. 39, "Line 25b—Form(s) 1099": *"If you received a 2025 Form 1099 showing federal income tax withheld on dividends, taxable or tax-exempt interest income, unemployment compensation, social security benefits, railroad retirement benefits, or other income you received, include the amount withheld in the total on line 25b. This should be shown in box 4 of Form 1099, box 6, of Form SSA-1099, or box 10 of Form RRB-1099."*; `Form 1099-K`, p. 5, Box 4; `26 U.S.C. §§ 31(c), 3406`).
   - **Box 1a (`Gross amount...`)** does **not** feed any income, gain, or Schedule D line directly. Even when the filer uses the **Schedule 1 top-of-form entry space** (`2025 Instructions for Schedule 1`, p. 88), Box 1a is entered there in full **only if** the *entire* Form 1099-K was for personal items sold at a loss (or reported in error); if only part of Box 1a was for a personal item sold at a loss, only that attributable portion is entered (`i1040gi--2025.pdf`, p. 88).

---

## 2. The Adopted Return Path, Traced at Milestone Launch

### 2.1 Production Resolver and Adopted Release / Package

#### [Code reading]

*(Note: All findings in Sections 2, 3, and 4 are from static reading of the repository's source files and JSON artifacts at milestone launch. Nothing was executed.)*

1. **Live coordinator authority chain**:
   - `packages/derivation/live.py:405-569` (`live_coordinate_run`) calls `resolve_production_package` (`packages/derivation/production_resolver.py:297-379`).
   - `resolve_production_package` selects the sole current `act-package-adoption.v1` (`packages/derivation/production_resolver.py:134-204`), verifies the pinned `release-registry.v1` document and its `package_registry_sha256` against `surface.package_registry_path` (`lines 210-252`), verifies the pinned `artifact-package` checksum against `load_published_package_checksums` (`lines 336-357`), resolves the exclusive member corpus by exact `(id, version)` and citizen checksum (`lines 258-294, 359-361`), and enforces the hard gate `validate_package(...).ok == True` (`lines 363-378`).
   - `_resolved_run_material` (`packages/derivation/live.py:203-377`) extracts `rules`, `parameters`, `families` (`source-family.v1` / `source-family.v2`), `mappings` (`source-closure-mapping.v2`), `fact_types`, `input_bindings`, and `collect_names` **exclusively** from `resolved.resolved_members`. Unpinned files in `packages/content/tax/2025/` are never loaded or evaluated (`packages/derivation/production_resolver.py:270`).

2. **Current published release and package at milestone launch**:
   - Latest release registry citizen: `demo.release.sli-worksheet-integration.2025@v43` (`packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/demo.release.sli-worksheet-integration.2025.v43.json:1-7`), which attests `package_registry_sha256 = b26bbd9ba2ce138cef0202c443dc1e0d5345e9bd69c7e27094fe0966015c6e9c`.
   - Verified package registry: `packages/content/tax/2025/published-packages.v43.json`, which publishes `tax.us.2025.package.core-calculations@v45`.
   - Verified package body: `packages/content/tax/2025/package.core-calculations.v45.json:1-3456` (`schema: "artifact-package.v36"`, `id: "tax.us.2025.package.core-calculations"`, `version: "v45"`, `package_checksum: "2c0099021ae42fd0c1dc4aa492d14b8a80010f5996105a7239d21297d3ae7cd3"`).
   - *(Note: Every Form 8949, Schedule D, Schedule 1 Part I, Form 1040 line 7a/8/9, and withholding citizen traced below is identical across `package.core-calculations.v38.json` through `v45.json`; `v39`–`v45` evolved only the Form 1098-E / Schedule 1 line 21 / line 26 / Form 1040 line 10 / line 11a and Form 1098 mortgage-interest slices.)*

---

### 2.2 Complete Inventory of Source Families Admitted by `package.core-calculations@v45`

#### [Code reading]

In `packages/content/tax/2025/package.core-calculations.v45.json` (`lines 1605-3403`), the resolved graph contains **35 `source-family` members** (`source-family.v1` and `source-family.v2`: 27 and 8). Not one of them is a Form 1099-K family or a non-1099-B sale family:

| Domain Area | Admitted `source-family` IDs in `package.core-calculations@v45` | Member Fact Type(s) |
| --- | --- | --- |
| **Wages (W-2)** | `tax.us.2025.w2@v2` | `tax.us.2025.w2.box1-wages` |
| **Interest (1099-INT, 1099-OID, K-1 box 5, non-form, Schedule B adjustments)** | `tax.us.2025.f1099int.b1@v1`, `f1099int.b3@v1`, `f1099int.b8@v1`, `f1099int.b10@v1`, `f1099oid.b1@v1`, `f1099oid.b5@v1`, `form1065-k1.box5@v1`, `non-form-interest@v1`, `scheduleb.adjustment.abp-adjustment@v1`, `scheduleb.adjustment.nominee@v1` | Interest / OID / Schedule B adjustment fact types |
| **Dividends (1099-DIV)** | `tax.us.2025.f1099div.1a@v1`, `f1099div.1b@v1`, `f1099div.2a@v1`, `f1099div.7@v1`, `f1099div.12@v1` | `box1a-ordinary`, `box1b-qualified`, `box2a-capital-gain-distribution`, `box7-foreign-tax-paid`, `box12-exempt-interest-dividends` |
| **Unemployment (1099-G)** | `tax.us.2025.f1099g.1@v1` | `tax.us.2025.f1099g.box1-unemployment` |
| **IRA Distributions (1099-R)** | `tax.us.2025.f1099r.ira-fully-taxable@v2` | `tax.us.2025.f1099r.ira-box1-taxable-distribution` |
| **Social Security (SSA-1099)** | `tax.us.2025.ssa1099.benefits@v1` | `tax.us.2025.ssa1099.box5-net-benefits` |
| **Mortgage Interest (1098)** | `tax.us.2025.f1098@v1` | `tax.us.2025.f1098.box1-mortgage-interest` |
| **Student Loan Interest (1098-E)** | `tax.us.2025.f1098e.1@v1` | `tax.us.2025.f1098e.box1-student-loan-interest` |
| **Capital Gains / Losses (Form 1099-B covered only)** | **14 families total** (14 Form 1099-B source-family members: the 4 covered transaction families plus their proceeds, basis, and adjustment families; `lines 1641-1759`):<br>• `tax.us.2025.f1099b.covered-st@v1` (`covered-st-proceeds@v1`, `covered-st-basis@v1`)<br>• `tax.us.2025.f1099b.covered-lt@v1` (`covered-lt-proceeds@v1`, `covered-lt-basis@v1`)<br>• `tax.us.2025.f1099b.covered-w-st@v2` (`covered-w-st-proceeds@v2`, `covered-w-st-basis@v2`, `covered-w-st-adjustment@v2`)<br>• `tax.us.2025.f1099b.covered-w-lt@v2` (`covered-w-lt-proceeds@v2`, `covered-w-lt-basis@v2`, `covered-w-lt-adjustment@v2`) | `tax.us.2025.f1099b.covered-st-txn` (`.proceeds`, `.basis`), `covered-lt-txn` (`.proceeds`, `.basis`), `covered-w-st-txn` (`.proceeds`, `.basis`, `.adjustment`), `covered-w-lt-txn` (`.proceeds`, `.basis`, `.adjustment`) |
| **Form 1099-K / Non-1099-B Sales** | **NONE** | **NONE** (Zero `1099k` or `personal` fact types, bundles, families, closure mappings, form fields, or rules exist anywhere in `packages/`. The four covered Form 1099-B transaction families remain the only sale families.) |

---

### 2.3 Consumer-by-Consumer Trace Across Form 8949, Schedule D, Schedule 1, Form 1040, and Withholding

#### A. Form 8949 Attachment (`tax.us.2025.rule.attachment.f8949@v2`)

#### [Code reading]

- **File**: `packages/content/tax/2025/attachment.f8949.v2.json:1-294` (`schema: "attachment-rule.v8"`, `publishes: "tax.us.2025.form8949.disposition"`).
- **Requirement trigger** (`lines 18-32`): Declared to require attachment only when `tax.us.2025.f1099b.covered-w-st-proceeds-subtotal > 0` or `tax.us.2025.f1099b.covered-w-lt-proceeds-subtotal > 0`.
- **Completeness gate** (`lines 33-44` and `packages/derivation/runner.py`): Requires presence of `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments@v1` (`packages/content/tax/2025/schedule-d-boundary-form8949-w.bundle.json:7-31`), whose title is:
  > *"Whether the return has no Form 8949 adjustment codes other than W, no multi-code rows, and no noncovered/basis-not-reported Form 8949 sources (ADR-0061 Decision 4). Categorical {yes,no}."*
  In `packages/derivation/runner.py`, an attachment rule's `completeness.required_answers` checks that the answer is present and equals `"yes"`.
- **Box categories itemized** (`lines 45-262`):
  - `box-a-proceeds`, `box-a-basis`, `box-a-adjustment`: Form 8949 **Part I, Box A** (short-term covered 1099-B wash sales) over `tax.us.2025.f1099b.covered-w-st-{proceeds,basis,adjustment}@v2`.
  - `box-d-proceeds`, `box-d-basis`, `box-d-adjustment`: Form 8949 **Part II, Box D** (long-term covered 1099-B wash sales) over `tax.us.2025.f1099b.covered-w-lt-{proceeds,basis,adjustment}@v2`.
- **Boxes B, C, E, F (and digital-asset Boxes G–L)**: **Do not exist.** There is no `part_id` for `box-c-*` or `box-f-*`, and no non-1099-B source family is referenced in `attachment.f8949.v2.json`.

#### B. Schedule D Attachment and Schedule D Line Producers

#### [Code reading]

1. **Schedule D Attachment (`tax.us.2025.rule.attachment.schedule-d@v6`, `packages/content/tax/2025/attachment.schedule-d.v6.json:1-314`)**:
   - **Requirement trigger** (`lines 270-288`): Strictly greater than zero on any of: `covered-st-proceeds-subtotal`, `covered-lt-proceeds-subtotal`, `capital-loss-carryover.short-term`, `capital-loss-carryover.long-term`, `covered-w-st-proceeds-subtotal`, `covered-w-lt-proceeds-subtotal`.
   - **Completeness gate** (`lines 8-85`): Requires `no-inbound-capital-loss-carryovers`, `no-form8949-sources`, `no-other-schedule-d-sources`, `no-lines-18-19-sources`, `no-1099da-or-qof`, and when `no-form8949-sources == "no"` adds `no-other-form8949-adjustments` (which must be `"yes"`).
   - **Itemizations** (`lines 87-268`): Itemizes only `line-1a-proceeds`, `line-1a-basis` (`f1099b.covered-st`), `line-8a-proceeds`, `line-8a-basis` (`f1099b.covered-lt`), and `line-13-box2a` (`f1099div.2a`).

2. **Schedule D Part I (Short-Term) Line Producers**:
   - **Line 1a (`tax.us.2025.rule.schedule-d-line1a-gain@v1`, `packages/content/tax/2025/rule.schedule-d-line1a-gain.json:1-47`)**: Publishes `tax.us.2025.schedule-d.line-1a-gain` (bound to form field `tax.us.2025.schedule-d.line-1a@v1`). Accepts **only** `tax.us.2025.f1099b.covered-st-{proceeds,basis}-subtotal` (`when: require_closed("tax.us.2025.f1099b.covered-st")`). Every member of `f1099b.covered-st-txn` requires `broker` (`tax.us.f1099b-broker`), `statement` (`tax.us.f1099b-statement`), `transaction` (`tax.us.f1099b-transaction`), `covered_security: "yes"`, and `basis_reported_to_irs: "yes"`.
   - **Line 1b (`tax.us.2025.rule.schedule-d-line1b@v2`, `packages/content/tax/2025/rule.schedule-d-line1b.v2.json:1-91`)**: Publishes `tax.us.2025.schedule-d.line-1b` (bound to form field `tax.us.2025.schedule-d.line-1b@v1`), representing Form 8949 **Box A** net gain/loss (`d − e + g`). Accepts **only** `tax.us.2025.f1099b.covered-w-st-{proceeds,basis,adjustment}-subtotal` (`when: all(require_closed(covered-w-st), ...)`). Furthermore, `family.f1099b-covered-w-st.v2.json:16-118` enforces `source-family.v2` member constraints requiring `box_1g_wash_sale_adjustment == "yes"`.
   - **Line 2 (Form 8949 Box B / Box H)**: **Absent** (no rule, no symbol, no form-field citizen).
   - **Line 3 (Form 8949 Box C / Box I — where a short-term personal-item sale must go)**: **Absent** (no rule, no symbol, no form-field citizen in `packages/content/tax/2025/`).
   - **Lines 4 and 5**: **Absent**.
   - **Line 6 (`tax.us.2025.rule.schedule-d-line6@v1`, `packages/content/tax/2025/rule.schedule-d-line6.json`)**: Short-term capital loss carryover from 2024 (`tax.us.2025.capital-loss-carryover.short-term`).
   - **Line 7 (`tax.us.2025.rule.schedule-d-line7@v3`, `packages/content/tax/2025/rule.schedule-d-line7.v3.json:1-52`)**: Hard-coded sum of **only** `line-1a-gain + line-1b + line-6` (`lines 34-50`). It has no term for Schedule D line 3.

3. **Schedule D Part II (Long-Term) Line Producers**:
   - **Line 8a (`tax.us.2025.rule.schedule-d-line8a-gain@v2`, `packages/content/tax/2025/rule.schedule-d-line8a-gain.v2.json:1-47`)**: Publishes `tax.us.2025.schedule-d.line-8a-gain` (bound to `tax.us.2025.schedule-d.line-8a@v1`). Accepts **only** `tax.us.2025.f1099b.covered-lt-{proceeds,basis}-subtotal`.
   - **Line 8b (`tax.us.2025.rule.schedule-d-line8b@v2`, `packages/content/tax/2025/rule.schedule-d-line8b.v2.json:1-91`)**: Publishes `tax.us.2025.schedule-d.line-8b` (bound to `tax.us.2025.schedule-d.line-8b@v1`), representing Form 8949 **Box D** net gain/loss (`d − e + g`). Accepts **only** `tax.us.2025.f1099b.covered-w-lt-{proceeds,basis,adjustment}-subtotal`.
   - **Line 9 (Form 8949 Box E / Box K)**: **Absent**.
   - **Line 10 (Form 8949 Box F / Box L — where a long-term personal-item sale must go)**: **Absent** (no rule, no symbol, no form-field citizen in `packages/content/tax/2025/`).
   - **Lines 11 and 12**: **Absent**.
   - **Line 13 (`schedule-d.line-13.form-field.json` / `rule.f1099div-2a-subtotal.json`)**: Capital gain distributions from `tax.us.2025.f1099div.2a@v1` (`tax.us.2025.dividends.2a-subtotal`).
   - **Line 14 (`tax.us.2025.rule.schedule-d-line14@v1`, `packages/content/tax/2025/rule.schedule-d-line14.json`)**: Long-term capital loss carryover from 2024 (`tax.us.2025.capital-loss-carryover.long-term`).
   - **Line 15 (`tax.us.2025.rule.schedule-d-line15@v4`, `packages/content/tax/2025/rule.schedule-d-line15.v4.json:1-58`)**: Hard-coded sum of **only** `line-8a-gain + line-8b + dividends.2a-subtotal + line-14` (`lines 36-56`). It has no term for Schedule D line 10.

4. **Schedule D Part III (Summary) and Downstream Form 1040 Capital-Gain Consumers**:
   - **Line 16 (`tax.us.2025.rule.schedule-d-line16@v2`, `packages/content/tax/2025/rule.schedule-d-line16.v2.json:1-46`)**: `line-7 + line-15`.
   - **Line 21 (`tax.us.2025.rule.schedule-d-line21@v1`, `packages/content/tax/2025/rule.schedule-d-line21.json:1-92`)**: Capital loss limitation when `line-16 < 0`, capped by `demo.parameter.capital-loss-limit.2025` (`$3,000` or `$1,500` MFS).
   - **Preferential base (`tax.us.2025.rule.selected-preferential-base@v4`, `packages/content/tax/2025/rule.selected-preferential-base.v4.json:1-525`)**:
     - Discriminator (`lines 45-101`): Checks whether **any** of `covered-st-proceeds-subtotal > 0`, `covered-lt-proceeds-subtotal > 0`, `capital-loss-carryover.short-term > 0`, `capital-loss-carryover.long-term > 0`, `schedule-d.line-1b != 0`, or `schedule-d.line-8b != 0` holds.
     - Completeness guard (`lines 103-416`): When the Schedule D branch is active, requires `no-form8949-sources`, `no-other-schedule-d-sources == "yes"`, `no-lines-18-19-sources == "yes"`, `no-1099da-or-qof == "yes"`, and (when `no-form8949-sources == "no"`) `no-other-form8949-adjustments == "yes"`.
     - Value (`lines 418-524`): Publishes `min(max(schedule-d.line-15, 0), max(schedule-d.line-16, 0))` on the Schedule D branch (or `dividends.2a-subtotal` on the Exception 1 direct branch when `schedule-d-required.conclusion == "no"`).
   - **Form 1040 Line 7a (`tax.us.2025.rule.form1040-line7a@v5`, `packages/content/tax/2025/rule.form1040-line7a.v5.json:1-137`)**:
     - Uses the same 6-term discriminator (`covered-st-proceeds-subtotal > 0`, `covered-lt-proceeds-subtotal > 0`, `capital-loss-carryover.short-term > 0`, `capital-loss-carryover.long-term > 0`, `schedule-d.line-1b != 0`, `schedule-d.line-8b != 0`, `lines 49-106`).
     - Notice that even if a non-1099-B transaction were added to Schedule D line 3 or line 10, **neither `rule.selected-preferential-base@v4` nor `rule.form1040-line7a@v5` currently includes Schedule D line 3 or line 10 in its Schedule D branch discriminator**! And if a Form 8949 Code `L` personal-loss row produces `$0` net gain/loss on line 3 or line 10, a `!= 0` net-gain check (like `line-1b != 0`) would evaluate to `False`, whereas `attachment.f8949` and `attachment.schedule-d` trigger on `proceeds-subtotal > 0`.
   - **Form 1040 Line 16 (`tax.us.2025.rule.form1040-line16@v5`, `packages/content/tax/2025/rule.form1040-line16.v5.json:1-465`)**:
     - Consumes `tax.us.2025.capital-gains.selected-preferential-base` in the QDCG worksheet calculation, and also carries its own `conditional_dependency_set` guard (`lines 320-463`) conditioned on `covered-st-proceeds-subtotal > 0` or `covered-lt-proceeds-subtotal > 0`.

#### C. Schedule 1 Attachment and Schedule 1 Line Producers (Top Entry Space, Part I Lines 7 / 8z / 9 / 10, Part II Lines 21 / 24z / 25 / 26)

#### [Code reading]

1. **Schedule 1 Top-of-Form 1099-K Entry Space**:
   - **Absent**. There is no `form-field` citizen, no derived symbol, and no rule in `packages/content/tax/2025/` for the Schedule 1 header entry space (*"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"*).
   - Furthermore, in `packages/schemas/tax/form-field.v3.schema.json` (the highest published `form-field` schema), every `form-field` citizen binds to a derived `symbol` published by a rule in the package.

2. **Schedule 1 Part I (Additional Income — Lines 1–10)**:
   - **Line 7 (`tax.us.2025.rule.schedule1-line7@v1`, `packages/content/tax/2025/rule.schedule1-line7.json`)**: Publishes `tax.us.2025.schedule1.line7-unemployment` from `tax.us.2025.unemployment.box1-subtotal` (source family `tax.us.2025.f1099g.1@v1`).
   - **Lines 8a–8z and Line 9 (Other Income)**: **Absent** as producers or form fields. Instead, `packages/content/tax/2025/schedule1-part1-scope.bundle.json:153-177` defines the completeness absence assertion `tax.us.2025.schedule1-part1-scope.no-sch1-other-income@v1` (*"No Schedule 1 other income (lines 8a–8z / line 9 aggregate) is present for the bounded additional-income claim"*).
   - **Line 10 (`tax.us.2025.rule.schedule1-line10@v1`, `packages/content/tax/2025/rule.schedule1-line10.json:1-294`)**: Publishes `tax.us.2025.schedule1.line10-additional-income` equal to `tax.us.2025.schedule1.line7-unemployment` **only when** `tax.us.2025.f1099g.1` is closed and all 10 Part I scope absence facts (`no-sch1-line1-taxable-refunds`, `no-sch1-line2a-alimony`, `no-sch1-line3-business`, `no-sch1-line4-other-gains`, `no-sch1-line5-rental`, `no-sch1-line6-farm`, `no-sch1-other-income`, `no-unemployment-repayment`, `no-f1099g-box2-state-refund`, `no-f1099g-other-payment-classes`) equal `"yes"`.

3. **Schedule 1 Part II (Adjustments to Income — Lines 11–26)**:
   - **Line 21 (`tax.us.2025.rule.sli-worksheet@v5`, `packages/content/tax/2025/rule.sli-worksheet.v5.json:1-901`)**: Publishes `tax.us.2025.schedule1.line21-sli-deduction` from `tax.us.2025.f1098e.1@v1` and student-loan relationship facts.
   - **Lines 24a–24z and Line 25 (Other Adjustments)**: **Absent** as producers or form fields. Instead, `packages/content/tax/2025/schedule1-adjustments-scope.bundle.json:3-28, 320-345` defines `no-line24z-writein@v1` and `no-line25-other-adjustments@v1`.
   - **Line 26 (`tax.us.2025.rule.schedule1-line26@v1`, `packages/content/tax/2025/rule.schedule1-line26.json:1-338`)**: Publishes `tax.us.2025.schedule1.line26-total-adjustments` equal to `tax.us.2025.schedule1.line21-sli-deduction` **only when** all 12 Part II scope absence facts (`no-line11-educator` through `no-line20-ira-deduction`, `no-line23-archer-msa`, and `no-line25-other-adjustments`) equal `"yes"`. Note that `rule.schedule1-line26.json:31` cites the 2025 Schedule 1 instructions (`i1040gi.pdf` p. 99–100) in noting that `no-line25-other-adjustments` subsumes lines 24a–24z.

4. **Schedule 1 Attachment (`tax.us.2025.rule.attachment.schedule-1@v2`, `packages/content/tax/2025/rule.attachment.schedule-1.v2.json:1-190`)**:
   - **Requirement trigger** (`lines 166-180`): Triggered only when `tax.us.2025.unemployment.box1-subtotal > 0` or `tax.us.2025.schedule1.line21-sli-deduction > 0`.
   - **Itemizations** (`lines 103-164`): Itemizes only `line-7-unemployment` (`f1099g.1`) and `line-21-student-loan-interest` (`f1098e.1`).

#### D. Form 1040 Downstream Lines (`7a`, `8`, `9`, `10`, `11a`, `15`, `16`, `20`, `22`) and Withholding (`25b`)

#### [Code reading]

- **Form 1040 Line 7a (`tax.us.2025.rule.form1040-line7a@v5`)**: Publishes `tax.us.2025.capital-gains.line7a-total` (bound to `tax.us.2025.form1040.line-7a@v1`). Feeds `rule.form1040-line9@v7`.
- **Form 1040 Line 8 (`tax.us.2025.rule.form1040-line8@v1`, `packages/content/tax/2025/rule.form1040-line8.json:1-46`)**: Passthrough of `tax.us.2025.schedule1.line10-additional-income` to `tax.us.2025.income.additional-income` (bound to `tax.us.2025.form1040.line-8@v1`).
- **Form 1040 Line 9 (`tax.us.2025.rule.form1040-line9@v7`, `packages/content/tax/2025/rule.form1040-line9.v7.json:1-119`)**: Sums `wages.total-w2-box1`, `interest.taxable-total`, `dividends.ordinary-total`, `capital-gains.line7a-total`, `income.additional-income`, `ira.distributions.line4b`, and `social-security.line6b` into `tax.us.2025.income.total-income`.
- **Form 1040 Line 10 (`tax.us.2025.rule.form1040-line10@v1`, `packages/content/tax/2025/rule.form1040-line10.json:1-46`)**: Passthrough of `tax.us.2025.schedule1.line26-total-adjustments` to `tax.us.2025.income.line10-adjustments` (bound to `tax.us.2025.form1040.line-10@v1`).
- **Form 1040 Line 11a / 11b (`tax.us.2025.rule.form1040-line11@v2`, `packages/content/tax/2025/rule.form1040-line11.v2.json:1-30`)**: Computes `tax.us.2025.income.agi = total-income − schedule1.line26-total-adjustments` (bound to both `form1040.line-11a@v1` and `form1040.line-11b@v1`), feeding `rule.form1040-line15@v2` (`income.taxable-income`), `rule.form1040-line16@v5` (`tax.total-tax`), and `rule.form1040-tax-after-credits@v1` (`tax.after-nonrefundable-credits`, Form 1040 line 22).
- **Withholding consumer (`Form 1040 Line 25a / 25b / 25d / 33`)**: **Absent**.
  - The adopted Form 1040 calculation graph stops at **Form 1040 line 22** (`tax.us.2025.tax.after-nonrefundable-credits`, `packages/content/tax/2025/rule.form1040-tax-after-credits.json:1-130`).
  - There is **no rule, symbol, or form-field citizen** for Form 1040 line 25a, line 25b (*Federal income tax withheld from Form(s) 1099*), line 25c, line 25d, or payments/refunds.
  - Instead, every existing 1099 / SSA-1099 slice in `packages/tax/loader.py:62-144` enforces a **zero/absent companion admission gate** on withholding:
    - `tax.us.2025.f1099g.box4-federal-withholding-authority` is restricted to `frozenset({None, 0, 0.0})` (`packages/tax/loader.py:74, 134`; `packages/content/tax/2025/f1099g-box1.bundle.json:69-110`: *"Only explicit null (absent) or numeric zero is admissible on the bounded unemployment route. A nonzero value is a hard admission block and never creates Form 1040 line 25b or any payments computation."*).
    - `tax.us.2025.ssa1099.box6-withholding` is restricted to `frozenset({None, 0, 0.0})` (`packages/tax/loader.py:109, 140`).

---

## 3. Why No Bounded Execution (`p0a_probe.py`) Occurred

#### [Code reading]

Charter Question 3 states: *"If tracing leaves a specific consumer question open (for example, whether a non-1099-B sale can reach Form 8949 or Schedule D), run the smallest synthetic case through the real live coordinator, reusing an existing fixture's setup, and report the exact outcome. Distinguish a zero, an absent publication and a blocked result. If no execution is needed, say why."*

**Nothing was executed.** Static reading of the production coordinator (`packages/derivation/live.py:203-262`), the marshaler (`packages/derivation/marshal.py`), and the exclusive member graph of `package.core-calculations.v45.json` shows why no non-1099-B sale or Form 1099-K statement can enter the adopted package:

1. **Can a non-1099-B sale or Form 1099-K statement be admitted into `RunContext` in `v45`? (Code reading)**:
   - **No.** In `packages/derivation/live.py:217-238`, `fact_types` and `collect_names` are populated strictly from the `bundle.v2`, `fact-type.v2`, and `source-family.v1`/`v2` citizens pinned in `package.core-calculations.v45.json`. Because no Form 1099-K or non-1099-B sale fact type or family exists in `v45`, and all four capital-gain families in `v45` (`f1099b.covered-st`, `f1099b.covered-lt`, `f1099b.covered-w-st`, `f1099b.covered-w-lt`) require `tax.us.f1099b-broker`, `tax.us.f1099b-statement`, `tax.us.f1099b-transaction`, `covered_security: "yes"`, and `basis_reported_to_irs: "yes"`, there is no input binding through which a non-1099-B personal-item sale can be passed to the coordinator.

2. **[Code reading — interpretation of rule text, not observation] Disposition consequences (`zero` vs. `absent publication` vs. `blocked result`) inferred from reading the `package.core-calculations@v45` rules**:
   - *(Note: The consequences below—which outputs would publish `0`, which would evaluate to `not_required`, and which would block with which codes—are interpretations of the declarative JSON rule definitions and `packages/derivation/runner.py` that were **not** executed.)*
   - **Under the rule text when all four `f1099b.covered-*` families are closed-empty (`0` members) and all Schedule D / Schedule 1 boundary absence declarations are `"yes"`**:
     - By inspection of their rule definitions, `schedule-d.line-1a-gain`, `schedule-d.line-1b`, `schedule-d.line-6`, `schedule-d.line-7`, `schedule-d.line-8a-gain`, `schedule-d.line-8b`, `schedule-d.line-14`, `schedule-d.line-15`, `schedule-d.line-16`, `schedule-d.line-21`, `capital-gains.selected-preferential-base`, `capital-gains.line7a-total`, `schedule1.line7-unemployment`, `schedule1.line10-additional-income`, `income.additional-income`, `schedule1.line21-sli-deduction`, `schedule1.line26-total-adjustments`, and `income.line10-adjustments` are written to publish numeric `0` (`status: "published"`, `value: 0`).
     - By inspection of `attachment.f8949.v2.json`, `attachment.schedule-d.v6.json`, and `rule.attachment.schedule-1.v2.json`, `form8949.disposition`, `schedule-d.disposition`, and `schedule1.disposition` each condition `requirement` on `strictly_greater_than` `0` on their respective subtotals, which corresponds to **`not_required`** when all subtotals are `0`.
   - **Under the rule text when a Schedule D or Schedule 1 boundary absence declaration is set to `"no"`**:
     - By inspection of `attachment.f8949.v2.json:33-44`, `attachment.schedule-d.v6.json:8-85`, and `packages/derivation/runner.py`, setting `tax.us.2025.schedule-d-boundary.no-form8949-sources = "no"` and `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments = "no"` (because a personal-item sale uses Form 8949 Box C / Box F or adjustment code `L`, which is not covered code `W`):
       - causes `attachment.f8949@v2` and `attachment.schedule-d@v6` to fail their `completeness.required_answers` check (`unsatisfied_completeness_witness` / `incomplete_return`) whenever required;
       - on the Schedule D branch of `rule.selected-preferential-base@v4` (`lines 123-244`), causes the `when` guard to fail (`guard_inapplicable`, **absent publication**), which in turn leaves downstream consumers of `tax.us.2025.capital-gains.selected-preferential-base` (`rule.form1040-line16@v5`, `rule.form1040-tax-after-credits@v1`, and the non-Schedule-D branch of `rule.form1040-line7a@v5`) missing that dependency (`DEPENDENCY_ABSENT`).
     - By inspection of `rule.schedule1-line10.json:1-294`, setting `tax.us.2025.schedule1-part1-scope.no-sch1-other-income = "no"` causes `rule.schedule1-line10@v1`'s `when` guard to fail (`guard_inapplicable`), leaving `rule.form1040-line8@v1`, `rule.form1040-line9@v7`, `rule.form1040-line11@v2`, `rule.form1040-line15@v2`, `rule.form1040-line16@v5`, and `rule.form1040-tax-after-credits@v1` with an unproduced upstream dependency (`DEPENDENCY_ABSENT` / `OPEN_DEPENDENCY`).

No `p0a_probe.py` script was executed or committed.

---

## 4. What This Implies for Cost (Missing vs. Reusable Pieces, and Framework Traps to Avoid)

### 4.1 Pieces That Do Not Exist Today (Required for a Bounded Personal-Item / Form 1099-K Route)

Without designing them, any bounded route for one purchased, personally used item sold through a payment platform (with a Form 1099-K) would require the following pieces that **do not exist** in `package.core-calculations@v45`:

1. **Form 1099-K statement source vocabulary and admission gate**:
   - No `bundle.v2` or `fact-type.v2` exists for a Form 1099-K statement (e.g., PSE/filer entity kind, 1099-K statement entity kind, Box 1a gross amount, and a Box 4 backup-withholding zero/absence companion authority witness analogous to `f1099g.box4-federal-withholding-authority` since Form 1040 line 25b does not exist).
2. **Ordinary personal-item sale circumstance / relationship facts**:
   - No `bundle.v2` or `fact-type.v2` exists to record the person's ordinary answers about what the Form 1099-K covers and the circumstances of the personal item sold (such as whether the 1099-K covers one personal item or multiple/other transactions, how the item was acquired and used, whether it is a collectible/digital asset, what the person paid to buy it, what the buyer paid and what selling/shipping fees or refunds applied, and the acquisition/sale dates or holding period).
   - No recording/review module (analogous to `packages/tax/f1098_statement_recording.py` or `packages/tax/sli_relationship_recording.py`) exists for recording those answers against a Form 1099-K statement.
3. **Downstream return-path rules, form fields, and attachment itemizations** (depending on which 2025 outcomes and routes the milestone plan scopes in):
   - **If the milestone includes the Schedule 1 top-of-form route for a personal item sold at a loss**:
     - A `form-field` citizen and rule publishing the Schedule 1 top-of-form 1099-K header entry (*"For 2025, enter the amount reported to you on Form(s) 1099-K that was included in error or for personal items sold at a loss"*), plus any corresponding update to `rule.attachment.schedule-1` (`packages/content/tax/2025/rule.attachment.schedule-1.v2.json`) if the top-of-form entry triggers or appears on the Schedule 1 attachment without altering `schedule1.line10-additional-income` or `schedule1.line26-total-adjustments`.
   - **If the milestone includes the Form 8949 / Schedule D route (mandatory for a personal-item gain; optional via Code `L` for a Form 1099-K personal-item loss)**:
     - Source-family / closure-mapping / subtotal citizens (or per-subject rule outputs) for **Form 8949 Part I Box C** (short-term non-1099-B) and/or **Part II Box F** (long-term non-1099-B) proceeds, basis, and (if Code `L` is supported on Form 8949) column (g) positive adjustment.
     - Successor `attachment.f8949` and `attachment.schedule-d` rules itemizing Box C (`part_id: "box-c-*"`) and/or Box F (`part_id: "box-f-*"`) and updating `requirement.subtotals`.
     - New `form-field` citizens and computation rules for **Schedule D line 3** (`tax.us.2025.schedule-d.line-3`) and/or **Schedule D line 10** (`tax.us.2025.schedule-d.line-10`).
     - Successor rules for **Schedule D line 7** (`rule.schedule-d-line7` to include `line-3`), **Schedule D line 15** (`rule.schedule-d-line15` to include `line-10`), **`rule.selected-preferential-base`** (to include Box C / Box F or line 3 / line 10 in its Schedule D branch discriminator and completeness guard), **`rule.form1040-line7a`** (to include line 3 / line 10 in its Schedule D branch discriminator), and **`rule.form1040-line16`** (if its branch-specific declaration pins depend on non-1099-B proceeds).
     - Narrowing or succeeding the Schedule D boundary declaration `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` (`schedule-d-boundary-form8949-w.bundle.json`), which currently bundles *"no Form 8949 adjustment codes other than W, no multi-code rows, and no noncovered/basis-not-reported Form 8949 sources"* into a single boolean-like `{yes, no}` fact.

---

### 4.2 Existing Pieces That Are Directly Reusable (With Repository Evidence)

#### [Code reading]

1. **Statement sameness and anti-duplication (`packages/tax/statements.py:1-85`)**:
   - `StatementKey(payer_id, tax_year, payer_ref)`, `statement_key()`, `statement_entity_id()`, and `classify_assertion()` are form-agnostic helpers that reject evidence-flavored keys (`_EVIDENCE_MARKERS`) and classify incoming statements as `NEW_ORIGINAL`, `CORRECTION`, or `DUPLICATE`.
2. **Same-statement zero/null withholding companion authority (`packages/tax/loader.py:51-145` & `packages/content/tax/2025/f1099g-box1.bundle.json:69-110`)**:
   - `domain_companion_presence_pairs()` and `domain_companion_value_domains()` in `packages/tax/loader.py` (installed on the live path at `packages/derivation/live.py:445`) already enforce same-statement companion presence and `{None, 0, 0.0}` value restrictions for `f1099g.box4-federal-withholding-authority` and `ssa1099.box6-withholding`. The exact same kernel mechanism can gate Form 1099-K Box 4 (`Federal income tax withheld`) to `{None, 0, 0.0}` without building Form 1040 line 25b.
3. **Ordinary statement-scoped circumstance recording (`packages/tax/f1098_statement_recording.py:1-405` & `packages/content/tax/2025/f1098-circumstances.bundle.v2.json:1-843`) and `rule-artifact.v13` / `v14` evaluation (`packages/content/tax/2025/rule.f1098-line8a.v2.json:1-679`, `packages/content/tax/2025/rule.sli-statement-combined-standing.json:1-200`)**:
   - The repository already has proven patterns for recording ordinary `{"yes", "no", "cannot-tell"}` and numeric/categorical circumstance answers keyed to `(payer, statement, tax-year)` (or a linked item/transaction entity) and translating those answers into a calculation, a `0` publication, or an explicit `block` when an answer is `"cannot-tell"` or out of scope.
4. **Triple-scalar Form 8949 column architecture (`packages/content/tax/2025/f1099b-covered-w-st-scalars.bundle.json:1-219`, `packages/content/tax/2025/attachment.f8949.v2.json:45-262`, `packages/content/tax/2025/rule.schedule-d-line1b.v2.json:1-91`)**:
   - If the Form 8949 / Schedule D route is used, the `attachment-rule.v8` single-column itemization pattern (`proceeds`, `basis`, `adjustment`) and `d − e + g` line rule pattern (`rule.schedule-d-line1b.v2.json`) already exist in the runner and presentation projector.
5. **Existing downstream Schedule D and Form 1040 tax chain (`rule.schedule-d-line16.v2.json`, `rule.schedule-d-line21.json`, `rule.form1040-line9.v7.json`, `rule.form1040-line11.v2.json`, `rule.form1040-line15.v2.json`, `rule.form1040-line16.v5.json`, `rule.form1040-tax-after-credits.json`)**:
   - Once Schedule D lines 7 and 15 (and `selected-preferential-base` / `form1040-line7a`) reflect any capital gain, Schedule D line 16 and the entire Form 1040 lines 7a $\rightarrow$ 9 $\rightarrow$ 11a $\rightarrow$ 15 $\rightarrow$ 16 $\rightarrow$ 22 chain require no new tax-bracket or QDCG worksheet arithmetic.

---

### 4.3 General Capital-Asset / Accounting Framework Traps to Flag and Avoid

#### [Interpretation for P0b]

Per Charter Question 4 (*"Flag anything that looks like a general capital-asset or accounting framework rather than a bounded addition"*), the following should be flagged as **out-of-scope framework traps**:

1. **Multi-transaction / multi-item reconciliation ledger for Form 1099-K**:
   - Form 1099-K Box 1a is an annual aggregate across `Box 3` transactions (`f1099k--2024.pdf`, p. 5) and can mix multiple personal-item gains, multiple personal-item losses, business sales, and reimbursements (`2025 Instructions for Schedule 1`, p. 88). Building a general N-item reconciliation ledger that partitions one Form 1099-K across arbitrary combinations of Schedule 1 top-of-form losses, Form 8949 Box C short-term gains, Form 8949 Box F long-term gains, and Schedule C business receipts would be a general accounting engine rather than a bounded one-item circumstance slice. A bounded slice can instead ask whether the Form 1099-K is for one personal item sale (and block when the statement covers multiple items or mixed transaction types).
2. **General basis-accounting or depreciation/capital-improvement ledger**:
   - `Pub. 551` covers gift basis (`§ 1015`), inherited basis (`§ 1014`), business/rental conversions, partial business depreciation (`§ 1016(a)(2)`), casualty-loss basis reductions, and multi-year capital improvement schedules. Building a general asset-basis ledger is unnecessary for a bounded slice limited to **one purchased, purely personal-use item** (where acquisition other than by purchase, business/rental use, or unknown cost basis can be explicitly gated and blocked).
3. **General Form 8949 / Schedule D noncovered asset framework**:
   - Opening Form 8949 Boxes B, C, E, F, G–L for arbitrary noncovered securities, digital assets (`Form 1099-DA`), real estate (`Form 1099-S`), installment sales (`Form 6252`), collectibles (`28% Rate Gain Worksheet`, Schedule D line 18), or multiple adjustment codes (`B, C, D, E, H, L, M, N, O, P, Q, R, S, T, W, X, Y, Z`) is a broad capital-gains milestone, not a bounded personal-item circumstance slice.
4. **Full Form 1040 Line 25b withholding aggregation**:
   - Building a cross-form Form 1040 line 25b withholding aggregator across Forms 1099-INT, 1099-DIV, 1099-G, 1099-R, 1099-B, and 1099-K (and extending Form 1040 past line 22 into payments/refunds) is a separate return-payments milestone. Gating Form 1099-K Box 4 to `0` / `null` via `domain_companion_presence_pairs` matches the established `1099-G` and `SSA-1099` precedent.
