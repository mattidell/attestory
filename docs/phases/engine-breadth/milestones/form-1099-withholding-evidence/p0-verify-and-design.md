# P0: Verify the Line 25b Law and Design the Withholding Sources

Milestone: `docs/phases/engine-breadth/milestones/form-1099-withholding.md`
Base commit: `9f577c655b374531247dc0b8d8862909e6dbfee3`
Working branch: `milestone/form-1099-withholding-2025`

---

## 1. Law Table

The federal income tax withholding lines appear on 2025 Form 1040, Page 2, under the "Payments" section:
- Form 1040 line 25a: "Form(s) W-2" (`temp/tax-on-taxable-income/sources/f1040-2025.txt:115`)
- Form 1040 line 25b: "Form(s) 1099" (`temp/tax-on-taxable-income/sources/f1040-2025.txt:116`)
- Form 1040 line 25c: "Other forms (see instructions)" (`temp/tax-on-taxable-income/sources/f1040-2025.txt:117`)
- Form 1040 line 25d: "Add lines 25a through 25c" (`temp/tax-on-taxable-income/sources/f1040-2025.txt:118`)

The controlling source is the 2025 Form 1040 Instructions (`temp/tax-on-taxable-income/sources/i1040gi-2025.txt`). Due to multi-column OCR extraction of Page 39, Line 25c begins at line 2587 and wraps to column 3 at lines 2516–2526.

| Form 1040 Line | Document / Source Form | Box / Field Carrying Withholding | Citation (`file:line`) | Description & Law Requirements |
|---|---|---|---|---|
| **25a** | Form W-2 | Box 2 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2551-2557`<br>`temp/tax-on-taxable-income/sources/iw2w3-2025.txt:1481` | "Add the amounts shown as federal income tax withheld on your Form(s) W-2. Enter the total on line 25a. The amount withheld should be shown in box 2 of Form W-2. Attach your Form(s) W-2 to your return." |
| **25b** | Form 1099-R | Box 4 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2559-2565` | "Include on line 25b any federal income tax withheld on your Form(s) 1099-R. The amount withheld should be shown in box 4. Attach your Form(s) 1099-R to the front of your return if federal income tax was withheld." |
| **25b** | Form 1099-DIV | Box 4 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2566-2585` | Included under: "dividends ... shown in box 4 of Form 1099". |
| **25b** | Form 1099-INT | Box 4 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2566-2585` | Included under: "taxable or tax-exempt interest income ... shown in box 4 of Form 1099". |
| **25b** | Form 1099-G | Box 4 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2566-2585` | Included under: "unemployment compensation ... shown in box 4 of Form 1099". |
| **25b** | Form SSA-1099 | Box 6 ("Voluntary Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2566-2585` | Included under: "social security benefits ... shown in ... box 6, of Form SSA-1099". |
| **25b** | Form RRB-1099 | Box 10 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2566-2585` | Included under: "railroad retirement benefits ... shown in ... box 10 of Form RRB-1099". (Not read by engine; out of scope). |
| **25b** | Other Form 1099 series (e.g. 1099-K, 1099-MISC, 1099-NEC) | Box 4 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2566-2585` | Included under: "or other income you received ... shown in box 4 of Form 1099". |
| **25c** | Form W-2G | Box 4 ("Federal income tax withheld") | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2587-2594` | "Federal income tax withheld on your Form(s) W-2G. The amount withheld should be shown in box 4. Attach Form(s) W-2G to the front of your return if federal income tax was withheld." |
| **25c** | Form 8959 | Line 24 | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2516-2519` | "Additional Medicare Tax you had withheld. Include the amount shown on Form 8959, line 24, in the total on line 25c. Attach Form 8959." |
| **25c** | Schedule K-1 | Not specified in instructions | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2520-2521` | "Federal income tax withheld that is shown on a Schedule K-1." Instructions do not specify box number. |
| **25c** | Form 1042-S, Form 8805, Form 8288-A | Not specified in instructions | `temp/tax-on-taxable-income/sources/i1040gi-2025.txt:2522-2526` | "Tax withheld that is shown on Form 1042-S, Form 8805, or Form 8288-A. To assist in processing, attach the form to your return to claim a credit for the withholding." Box numbers not specified in instructions. |

### Document Partitioning between 25b and 25c
- **Line 25b** strictly receives federal income tax withheld from **Form(s) 1099** (specifically 1099-R box 4, 1099 box 4 for dividends, interest, unemployment, or other income), **Form SSA-1099 box 6**, and **Form RRB-1099 box 10**.
- **Line 25c** strictly receives withholding from **Other Forms**: Form W-2G (gambling), Form 8959 line 24 (Additional Medicare Tax), Schedule K-1, Form 1042-S, Form 8805, and Form 8288-A.
- Form W-2G withholding is legally distinct from Line 25b and never enters 25b.
- Estimated payments are on Line 26, not Line 25.


---

## 2. What the Engine Has

Survey of `packages/content/tax/2025/`, `package.core-calculations.v58.json`, and `packages/tax/loader.py`:

| Source Form | Withholding Fact ID | Exact Title | Family ID & Version | Closure Mapping & Fact | Rule Reading Fact | Nonzero Value Behavior Today |
|---|---|---|---|---|---|---|
| **1099-INT** | `tax.us.2025.f1099int.box4-withholding` | "Federal income tax withheld in box 4 of one logical Form 1099-INT statement instance furnished by a payer for 2025; same payer/statement/tax-year identity as box 1, box 3, box 8, and box 10 on the same statement, but a separate fact and a separate family. Nonnegative source amount only." | `tax.us.2025.f1099int.b4` (v1) | `tax.us.2025.closure-mapping.f1099int-b4` (v1); closure fact: `tax.us.2025.f1099int.b4.source-closure` (v1) | `tax.us.2025.rule.f1099int-b4-subtotal` (v1) publishes `tax.us.2025.interest.b4-withholding-subtotal`; read by `tax.us.2025.rule.form1040-line25b` | **Counts**: Summed into `tax.us.2025.interest.b4-withholding-subtotal` and added to Line 25b. |
| **1099-DIV** | `tax.us.2025.f1099div.box4-withholding` | "Federal income tax withheld in box 4 of one logical Form 1099-DIV statement instance furnished by a payer for 2025; same payer/statement/tax-year identity as box 1a, box 2a, box 7, and box 12 on the same statement, but a separate fact and a separate family. Nonnegative source amount only." | `tax.us.2025.f1099div.b4` (v1) | `tax.us.2025.closure-mapping.f1099div-b4` (v1); closure fact: `tax.us.2025.f1099div.b4.source-closure` (v1) | `tax.us.2025.rule.f1099div-b4-subtotal` (v1) publishes `tax.us.2025.dividends.b4-withholding-subtotal`; read by `tax.us.2025.rule.form1040-line25b` | **Counts**: Summed into `tax.us.2025.dividends.b4-withholding-subtotal` and added to Line 25b. |
| **1099-R** | `tax.us.2025.f1099r.ira-box4-withholding` | "Box 4 federal income tax withheld on the same logical 2025 Form 1099-R IRA-family statement as box 1 (same payer/statement/tax-year identity), aggregated via the existing tax.us.2025.f1099r.ira-fully-taxable family and closure. Not a presence-enforced companion (packages/tax/loader.py domain_companion_presence_pairs is a global, unscoped kernel invariant; adding one here would retroactively require box 4 on every existing IRA box-1 assertion and break existing tests on main -- Track 1 stop condition, not added). A recorded distribution without a box-4 answer is simply excluded from the aggregate, the same present-sources-skip-closure posture box 1 and the other three withholding documents already have." | `tax.us.2025.f1099r.box4` (v1) | `tax.us.2025.closure-mapping.f1099r-box4` (v1); closure fact: `tax.us.2025.f1099r.box4.source-closure` (v1) | `tax.us.2025.rule.f1099r-box4-subtotal` (v1) publishes `tax.us.2025.ira.box4-withholding-subtotal`; read by `tax.us.2025.rule.form1040-line25b` | **Counts**: Summed into `tax.us.2025.ira.box4-withholding-subtotal` and added to Line 25b. |
| **1099-G** | `tax.us.2025.f1099g.box4-federal-withholding-authority` | "Explicit companion authority for Form 1099-G box 4 (federal income tax withheld) on the same logical statement as a box-1 member. Only explicit null (absent) or numeric zero is admissible on the bounded unemployment route. A nonzero value is a hard admission block and never creates Form 1040 line 25b or any payments computation. This is an authority witness, not a composed amount and never reduces box-1 income." | None | None | None (enforced at admission via schema `value_schema: anyOf [null, const: 0]` and `packages/tax/loader.py:domain_companion_value_domains`) | **Blocks**: A nonzero value is rejected at admission; cannot be asserted. |
| **SSA-1099** | `tax.us.2025.ssa1099.box6-withholding` | "Box 6 voluntary federal income tax withheld; bounded class admits only absent/zero." | None for withholding. Required companion to `tax.us.2025.ssa1099.box5-net-benefits` in `family.ssa1099-benefits.json` (v1) | Closure fact: `tax.us.2025.ssa1099.source-closure` (v1) requires "box-6 withholding absent or zero" | None (enforced at admission via schema `value_schema: enum [0, 0.0, null]` and `packages/tax/loader.py:domain_companion_value_domains`) | **Blocks**: A nonzero value is rejected at admission; putting filer outside the bounded ordinary class. |
| **1099-K** | `tax.us.2025.f1099k.box4-federal-withholding` | "Form 1099-K box 4 federal income tax withheld" | None for withholding | None | Read by `tax.us.2025.rule.f1099k-statement-loss-reason.v4` as a condition | **Blocks**: If box 4 > 0, loss reason becomes `backup-withholding-unsupported`, causing `tax.us.2025.rule.f1099k-unresolved.v3` to block with `DEPENDENCY_ABSENT`. Never reaches Line 25b. |

*(Note: In the `fact-type.v2` schema, fact definitions carry a `title` field; there is no separate `description` field).*

### Discrepancies between Form-Field / Citation Text and the Rule
1. **`tax.us.2025.form1040.line-25b` (v1) vs `tax.us.2025.rule.form1040-line25b` (v1)**:
   - Form field description (`form1040.line-25b.form-field.json:16`):
     `"Form 1040 line 25b: federal income tax withheld from Form(s) 1099 (1099-INT, 1099-DIV, 1099-R box 4, and 1099-K box 4)."`
   - Form field explanation (`published_value.explain`):
     `"Form 1040 line 25b equals the sum of the four 1099-document withholding subtotals."`
   - **Discrepancy**: The rule `rule.form1040-line25b.json` only adds **three** subtotals (INT, DIV, 1099-R). Form 1099-K box 4 was omitted due to the SC-R1 obstacle and is not summed anywhere.
2. **Missing 1099-G and SSA-1099**: Neither the form-field description nor the rule's addends include Form 1099-G box 4 or Form SSA-1099 box 6, even though IRS instructions specifically instruct taxpayers to include them on line 25b.
3. **Citation Text**: `citation.form1040.line-25b.json` cites Form 1040 instructions broadly without noting the omission of 1099-G and SSA-1099 withholding or the non-inclusion of 1099-K box 4.


---

## 3. Form 1099-G Box 4 and SSA-1099 Box 6 Admission & Design

### Admission Architecture Today
Form 1099-G box 4 and Form SSA-1099 box 6 are governed by admission invariants registered in `packages/tax/loader.py` and enforced during workspace projection in `packages/derivation/live.py:live_coordinate_run`:

1. **Registration in `loader.py`**:
   - `domain_companion_presence_pairs` maps `tax.us.2025.f1099g.box1-unemployment` to `tax.us.2025.f1099g.box4-federal-withholding-authority`.
   - `domain_companion_presence_pairs` maps `tax.us.2025.ssa1099.box5-net-benefits` to `tax.us.2025.ssa1099.box6-withholding`.
   - `domain_companion_value_domains` restricts both companion facts to `frozenset({None, 0, 0.0})`.
2. **Enforcement in `live.py` / `kernel/findings.py`**:
   - `live_coordinate_run()` calls `tax_registry()` during setup, populating `registry.companion_presence_pairs` and `registry.companion_value_domains`.
   - On every finding assertion, `packages/kernel/findings.py:_apply_assertion()` calls `_enforce_companion_presence()`.
   - Asserting a non-zero box 4 on Form 1099-G or non-zero box 6 on Form SSA-1099 triggers an immediate kernel refusal:
     ```text
     packages.kernel.findings.FindingModelError: finding value does not conform to value_schema: anyOf [null, const: 0]
     ```
   - This refusal occurs at **finding admission in the coordinator**, prior to and independent of rule evaluation or execution.

### Empirical Evaluation of Design Options

#### Option (a): Relax the Check in Global Tables in `loader.py`/`live.py`
We probed relaxing `domain_companion_value_domains` in `packages/tax/loader.py` to permit positive numbers, then ran a complete v58 answer set through `live_coordinate_run()` with $6,000 unemployment income and $600 box 4 withholding:
- **Income & Tax Computation**: Unemployment subtotal (`tax.us.2025.unemployment.b1-subtotal`) published $6,000, Schedule 1 line 7 published $6,000, Form 1040 line 8 published $6,000, taxable income published $40,250, and total tax (line 24) published $4,592.
- **Line 25b Behavior on v58**: The v58 rule `tax.us.2025.rule.form1040-line25b.v1` requires and sums only three subtotals: `tax.us.2025.interest.b4-withholding-subtotal`, `tax.us.2025.dividends.b4-withholding-subtotal`, and `tax.us.2025.ira.box4-withholding-subtotal`. It has no input pin or awareness of Form 1099-G or SSA-1099.
- **Exact Outcome**:
  - `tax.us.2025.payments.line25b` published `0`.
  - Form 1040 line 25d (total withholding) published `$4,500` (W-2 only).
  - Form 1040 line 33 (total payments) published `$4,500`.
  - Form 1040 line 37 (amount owed) published `$92` (tax $4,592 - payments $4,500).
- **Finding**: v58 **silently drops withholding**. The $600 withholding is admitted into the act log, but completely and silently omitted from the return calculations, converting a $508 refund into a $92 tax bill. This silent omission is a severe computation hazard.

#### Option (b): Restrict Check to Packages That Do Not Declare the New Family
To prevent silent omission on legacy packages, admission validation could be package-scoped: packages declaring the new withholding families (`tax.us.2025.f1099g.b4` and `tax.us.2025.ssa1099.b6`) permit non-zero withholding, while legacy packages (v58 and earlier) continue to enforce the `{None, 0}` refusal.
- **Required Code Changes**:
  - `packages/kernel/findings.py:project`: Must inspect `proj.acts` for `act-package-adoption.v1` and scope `_enforce_companion_presence()` against the active package adoption rather than a static global registry.
  - `packages/kernel/act_log.py:append`: Must also scope companion validation at mutation time.
  - `packages/derivation/live.py`: Must pass package family declarations into the projection state.
- **Engine vs Content Classification**: Because `findings.py` and `act_log.py` reside under `packages/kernel/`, this is definitively an **engine change** (substrate change). Under the single-source rule and milestone boundaries, modifying the kernel cannot be performed under a content-only track.

#### Option (c): Keep the Check and Route Withholding Through a Different Path
We evaluated whether a content-only path exists that keeps the `{None, 0}` check on authority witnesses and routes withholding through a separate fact:
- Form 1099-G box 1 and SSA-1099 box 5 unconditionally require same-statement companion authority facts (`f1099g.box4-federal-withholding-authority` and `ssa1099.box6-withholding`).
- If a filer enters a 1099-G statement with $600 withheld, routing withholding through a separate fact would require the filer to assert an authority witness of `0` (or `null`) to pass admission.
- Under ADR-0038 and Article 9, asserting a false zero-withholding witness to bypass an admission gate violates document integrity and introduces semantic contradictions into the workspace act log.
- **Finding**: **No content-only path exists** that avoids falsifying document witnesses.

### Engine-Change Status & Recommendation
- **Status**: No architecturally sound path avoids an engine change. Option (a) avoids editing `packages/kernel/`, but introduces silent withholding omission into legacy v58 runs. Option (b) is the robust, correct architecture, but requires modifying `packages/kernel/findings.py` and `packages/kernel/act_log.py`.
- **Recommendation**: Milestone Track 1 should adopt Option (b) with an explicit substrate engine change approved by the owner, parameterizing finding admission companion validation by the adopted package's declared families.

---

### Successor Withholding Design per Source

Following the established pattern from `family.f1099int-b4.json`, `closure-mapping.f1099int-b4.json`, and `rule.f1099int-b4-subtotal.json`:

#### Form 1099-G Box 4 Design
1. **Fact Type**: `tax.us.2025.f1099g.box4-withholding` (schema `fact-type.v2`, version `v1` in `f1099g-box4.bundle.json`).
   - *Identity keys*: `payer` (`tax.us.unemployment-payer`), `statement` (`tax.us.1099g-statement`), `tax-year` (literal `2025`).
   - *Value schema*: `{"type": "number", "minimum": 0}`.
   - *Title*: "Federal income tax withheld in box 4 of one logical Form 1099-G statement instance furnished by a payer for 2025; same payer/statement/tax-year identity as box 1 on the same statement, but a separate fact and a separate family. Nonnegative source amount only."
2. **Source Family**: `tax.us.2025.f1099g.b4` (schema `source-family.v1`, version `v1` in `family.f1099g-b4.json`).
   - *Member predicate*: `tax.us.2025.f1099g.box4-withholding`.
   - *Authorizes subtotal*: `tax.us.2025.unemployment.b4-withholding-subtotal`.
   - *Closure claim*: "Every federal income tax withheld amount reported in box 4 of a Form 1099-G furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon. This claim covers Form 1099-G box 4 only: it says nothing about box 1 unemployment compensation, box 2, or other Schedule 1 items. Closed with members authorizes the sum of current members; closed-empty authorizes subtotal 0."
3. **Closure Fact Type**: `tax.us.2025.f1099g.b4.source-closure` (schema `fact-type.v2`, version `v1` in `f1099g-box4.bundle.json`).
   - *Identity keys*: `family-horizon` (`kernel.family-horizon`), `tax-year` (literal `2025`).
   - *Value schema*: `{"type": "boolean"}`.
4. **Closure Mapping**: `tax.us.2025.closure-mapping.f1099g-b4` (schema `source-closure-mapping.v2`, version `v1` in `closure-mapping.f1099g-b4.json`).
   - Admits `tax.us.2025.unemployment.b4-withholding-subtotal` on `current-literal-true`.
5. **Subtotal Rule**: `tax.us.2025.rule.f1099g-b4-subtotal` (schema `rule-artifact.v3`, version `v1` in `rule.f1099g-b4-subtotal.json`).
   - Collects `tax.us.2025.f1099g.box4-withholding` over source set `tax.us.2025.f1099g.b4`, adds, and rounds with `rounding.convention`.
   - Publishes `tax.us.2025.unemployment.b4-withholding-subtotal`.

#### Form SSA-1099 Box 6 Design
1. **Fact Type**: `tax.us.2025.ssa1099.box6-voluntary-withholding` (schema `fact-type.v2`, version `v1` in `ssa1099-box6.bundle.json`).
   - *Identity keys*: `statement` (`tax.us.ssa1099-statement`), `tax-year` (literal `2025`).
   - *Value schema*: `{"type": "number", "minimum": 0}`.
   - *Title*: "Voluntary federal income tax withheld in box 6 of one logical Form SSA-1099 statement instance furnished to the taxpayer or spouse for 2025; same statement/tax-year identity as box 5 net benefits on the same statement, but a separate fact and a separate family. Nonnegative source amount only."
2. **Source Family**: `tax.us.2025.ssa1099.b6` (schema `source-family.v1`, version `v1` in `family.ssa1099-b6.json`).
   - *Member predicate*: `tax.us.2025.ssa1099.box6-voluntary-withholding`.
   - *Authorizes subtotal*: `tax.us.2025.ssa1099.b6-withholding-subtotal`.
   - *Closure claim*: "Every voluntary federal income tax withheld amount reported in box 6 of a Form SSA-1099 furnished to the taxpayer or spouse for tax year 2025 is recorded as a statement item as of the keyed horizon. This claim covers Form SSA-1099 box 6 only: it says nothing about box 5 net benefits, repayments, or Social Security worksheet completeness. Closed with members authorizes the sum of current members; closed-empty authorizes subtotal 0."
3. **Closure Fact Type**: `tax.us.2025.ssa1099.b6.source-closure` (schema `fact-type.v2`, version `v1` in `ssa1099-box6.bundle.json`).
   - *Identity keys*: `family-horizon` (`kernel.family-horizon`), `tax-year` (literal `2025`).
   - *Value schema*: `{"type": "boolean"}`.
4. **Closure Mapping**: `tax.us.2025.closure-mapping.ssa1099-b6` (schema `source-closure-mapping.v2`, version `v1` in `closure-mapping.ssa1099-b6.json`).
   - Admits `tax.us.2025.ssa1099.b6-withholding-subtotal` on `current-literal-true`.
5. **Subtotal Rule**: `tax.us.2025.rule.ssa1099-b6-subtotal` (schema `rule-artifact.v3`, version `v1` in `rule.ssa1099-b6-subtotal.json`).
   - Collects `tax.us.2025.ssa1099.box6-voluntary-withholding` over source set `tax.us.2025.ssa1099.b6`, adds, and rounds with `rounding.convention`.
   - Publishes `tax.us.2025.ssa1099.b6-withholding-subtotal`.
6. **Succession of Social Security Benefits Family & Mapping**:
   - `family.ssa1099-benefits.json` (v1) contains closure claim text: `"box-6 withholding absent or zero"`.
   - Succeeded by `family.ssa1099-benefits.v2.json` (v2), striking the `"box-6 withholding absent or zero"` limitation so statements with voluntary withholding can be members of the ordinary benefits family.
   - `closure-mapping.ssa1099-benefits.v2.json` (v2) succeeds v1 to point to `family.ssa1099-benefits` v2.

#### Form 1040 Line 25b Successor Rule
- `tax.us.2025.rule.form1040-line25b.v2` (`rule.form1040-line25b.v2.json`, schema `rule-artifact.v3`, version `v2`).
- Publishes: `tax.us.2025.payments.line25b`.
- Requires and adds 5 document subtotals:
  1. `tax.us.2025.interest.b4-withholding-subtotal` (Form 1099-INT)
  2. `tax.us.2025.dividends.b4-withholding-subtotal` (Form 1099-DIV)
  3. `tax.us.2025.ira.box4-withholding-subtotal` (Form 1099-R)
  4. `tax.us.2025.unemployment.b4-withholding-subtotal` (Form 1099-G)
  5. `tax.us.2025.ssa1099.b6-withholding-subtotal` (Form SSA-1099)
  and `rounding.convention`.
- Explanations walk from line 25b to each individual document subtotal.


---

## 4. Form 1099-K Box 4

### Testing the SC-R1 Obstacle
To empirically test the SC-R1 obstacle recorded in the notes of `rule.form1040-line25b.json`, a throwaway probe was executed on today's branch.
The probe declared a source family in `packages/content/tax/2025/family.f1099k-box4.json`:
```json
{
  "schema": "source-family.v1",
  "id": "tax.us.2025.f1099k.b4",
  "version": "v1",
  "title": "Form 1099-K box 4 statement items, tax year 2025",
  "scope": {
    "family": "individual-income-tax",
    "jurisdiction": "US-federal",
    "tax_year": 2025
  },
  "member_predicate": {
    "fact_type": "tax.us.2025.f1099k.box4-federal-withholding"
  },
  "authorizes_subtotal": "tax.us.2025.f1099k.b4-withholding-subtotal",
  "closure_claim": "Every federal income tax withheld amount reported in box 4 of a Form 1099-K furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon."
}
```

The probe then ran `pytest tests/test_f1099k_statement_removal_increment_c.py tests/test_family_handover_recording.py` and cleanly removed the throwaway file.

### Exact Test Output
- **Baseline (without throwaway family)**:
  `12 passed in 3.37s`
- **With throwaway family declared**:
  `9 failed, 3 passed in 3.52s`
  Exit code: `1`

#### Failing Tests:
1. `tests/test_f1099k_statement_removal_increment_c.py::F1099KStatementRemovalIncrementCTests::test_removal_and_closure_refusals`
2. `tests/test_f1099k_statement_removal_increment_c.py::F1099KStatementRemovalIncrementCTests::test_removal_of_last_remaining_statement_and_no_statements_closure`
3. `tests/test_f1099k_statement_removal_increment_c.py::F1099KStatementRemovalIncrementCTests::test_save_path_removal_via_review`
4. `tests/test_f1099k_statement_removal_increment_c.py::F1099KStatementRemovalIncrementCTests::test_atomic_statement_removal_with_sibling_standing`
5. `tests/test_f1099k_statement_removal_increment_c.py::F1099KStatementRemovalIncrementCTests::test_close_f1099k_family_durably_after_removal`
6. `tests/test_family_handover_recording.py::test_atomic_handover_replaces_closure_and_zero`
7. `tests/test_family_handover_recording.py::test_closed_nonempty_handover_replaces_closure_and_subtotal`
8. `tests/test_family_handover_recording.py::test_untouched_workspace_standing`
9. `tests/test_family_handover_recording.py::test_writer_refuses_handover_to_older_version`

#### Root Cause:
In `packages/tax/loader.py:349`, `tax_registry()` populates `registry.family_member_predicates` from all declared families in content.
When `record_f1099k_statement_durably()` records a 1099-K statement, it records box 1a gross proceeds via a `member-transition`, but records box 4 withholding via a plain `assertion` act (`packages/tax/f1099k_statement_recording.py:818`).
Under SC-R1 (`packages/kernel/findings.py:756-775`), `_apply_assertion()` forbids asserting a member fact through a plain assertion:
```text
packages.kernel.contribution.ContributionError: contribution batch failed: cannot assert member fact tax.us.2025.f1099k.box4-federal-withholding|payer=demo.payer.1,statement=stmt.demo.payer.1.2025.stmt.001,tax-year=2025 through a plain assertion; must use a member-transition instead
```

The obstacle recorded in the notes of `rule.form1040-line25b.json` is completely corroborated.

### Design Alternatives for 1099-K Box 4
1. **Alternative A (Recommended): Maintain Current Refusal Posture & Correct Form-Field Text.**
   - *Design*: Keep Form 1099-K box 4 out of the Line 25b family set. When `tax.us.2025.f1099k.box4-federal-withholding > 0`, `rule.f1099k-statement-loss-reason.v4` already sets the loss reason to `backup-withholding-unsupported`, causing `rule.f1099k-unresolved.v3` to refuse the return with `DEPENDENCY_ABSENT`.
   - *Form-Field Correction*: Publish `tax.us.2025.form1040.line-25b` v2 with corrected description and explain text that omits `1099-K box 4` and reflects the actual 5 participating withholding documents (1099-INT, 1099-DIV, 1099-R, 1099-G, SSA-1099).
   - *Cost*: Zero recording/schema risk; no backward-compatibility breaks.
2. **Alternative B: Successor Fact and Statement Recorder Overhaul.**
   - *Design*: Introduce a successor fact `tax.us.2025.f1099k.box4-withholding-member` and update `record_f1099k_statement_durably()` to manage two simultaneous family member-transitions (one for box 1a and one for box 4).
   - *Cost*: Significant code churn in `f1099k_statement_recording.py`, potential migration friction for existing 1099-K workspaces, for an edge case (backup withholding on payment cards) that is virtually never encountered for standard personal returns.


---

## 5. Closure Questions and Answer Set Behavior

### Successor Shape Execution on v58 Answer Sets
We empirically ran the three characteristic v58 answer sets through `packages.derivation.live.live_coordinate_run` against the successor package shape (where `rule.form1040-line25b.v2` aggregates all 5 withholding subtotals):
1. **Answer Set 1 (UI without withholding)**: Filer has wages ($50,000) and Form 1099-G unemployment ($6,000), but no unemployment withholding and no Social Security benefits.
2. **Answer Set 2 (SS without withholding)**: Filer has wages ($40,000) and Form SSA-1099 Social Security benefits ($12,000), but no voluntary withholding and no unemployment.
3. **Answer Set 3 (Neither UI nor SS)**: Simple return with only W-2 wages ($50,000), having neither Form 1099-G nor Form SSA-1099.

#### Exact Blocked Rules, Codes, and Missing Facts
Across all three answer sets, without new closure facts, the coordinator produced the identical blocking disposition on exactly three rules:

1. **`tax.us.2025.rule.f1099g-b4-subtotal`**:
   - `disposition`: `blocked`
   - `code`: `SOURCE_SET_UNCLOSED`
   - `missing`: `['tax.us.2025.f1099g.b4']`
2. **`tax.us.2025.rule.ssa1099-b6-subtotal`**:
   - `disposition`: `blocked`
   - `code`: `SOURCE_SET_UNCLOSED`
   - `missing`: `['tax.us.2025.ssa1099.b6']`
3. **`tax.us.2025.rule.form1040-line25b.v2`**:
   - `disposition`: `blocked`
   - `code`: `DEPENDENCY_ABSENT`
   - `missing`: `['tax.us.2025.unemployment.b4-withholding-subtotal', 'tax.us.2025.ssa1099.b6-withholding-subtotal']`

Every v58 return upgraded to the successor package without asserting the two new closure facts blocks at Line 25b.

### How Form 1099-INT Box 4 Works Today
In v58, Form 1099-INT box 4 withholding is organized into source family `tax.us.2025.f1099int.b4` and closure mapping `tax.us.2025.closure-mapping.f1099int-b4`.
- **Does a return without 1099-INT withholding need a closure fact?**
  **Yes.** Every tax return computed on v58 unconditionally requires `tax.us.2025.f1099int.b4.source-closure = true` (asserted at genesis horizon `demo.h.int.0`), even if the filer has no 1099-INT statements and no interest income.
- **Why?**
  `rule.form1040-line25b.v1` statically pins and requires `tax.us.2025.interest.b4-withholding-subtotal`. Under ADR-0016, that subtotal symbol is only admitted into the publication lattice when its underlying source family is closed. If `tax.us.2025.f1099int.b4.source-closure` is absent, the subtotal rule blocks with `SOURCE_SET_UNCLOSED`, and Line 25b blocks with `DEPENDENCY_ABSENT`. Closed-empty evaluation is what publishes `$0` for filers without 1099-INT statements.

### Can Closures Be Asked Conditionally?
We evaluated whether the filer interview could ask for withholding closures conditionally (i.e. only asking for Form 1099-G box 4 closure when the filer reports unemployment income, and omitting the question otherwise):

- **Ontology and Rule Architecture Barriers**:
  1. Under ADR-0016, a `source-closure-mapping.v2` artifact admits a symbol if and only if the specified family has a valid closure fact asserted for its current horizon.
  2. Under the rule grammar (`rule-artifact.v3`), `requires` is a static list of symbols. The derivation coordinator requires all symbols in `requires` to be admitted and published before a rule can compute.
  3. Form 1040 line 25b v2 has a static dependency on all 5 document subtotals:
     ```json
     "requires": [
       "tax.us.2025.interest.b4-withholding-subtotal",
       "tax.us.2025.dividends.b4-withholding-subtotal",
       "tax.us.2025.ira.box4-withholding-subtotal",
       "tax.us.2025.unemployment.b4-withholding-subtotal",
       "tax.us.2025.ssa1099.b6-withholding-subtotal",
       "rounding.convention"
     ]
     ```
  4. The engine has no concept of "optional input pins" or "conditional dependencies" in rule artifacts. A missing subtotal unconditionally blocks Line 25b.
- **What Makes It Impossible**:
  To allow conditional closures without blocking Line 25b would require either:
  - An engine extension to `packages/derivation/` supporting optional dependencies and fallback defaults in rule evaluation; or
  - An alternative rule structure with shadow/default rules publishing `$0` subtotals when negative income declarations exist, which introduces complex rule competition and precedence conflicts.
- **Conclusion**:
  Under current engine contracts, **closures cannot be conditional**. Every return adopting the successor package must assert closed-empty closures (`source-closure = true` at horizon `h0`) for all withholding families where no statements were furnished.

---

### Missing Box 4 Answer on Recorded Statements
We additionally probed whether a recorded statement that reports income but omits a box 4 answer blocks the return:
- **Empirical Probe**: On `package.core-calculations.v52`, Statement 1 had $500 box 1 interest and no box 4 answer; Statement 2 had $300 box 1 interest and $45 box 4 withholding. Both box 1 and box 4 families were closed.
- **Outcome**: The coordinator cleanly published $45 on line 25b. Statement 1 was simply excluded from the `tax.us.2025.f1099int.b4` collection without error.
- **Recommendation**: Maintain this posture across all 5 withholding sources. Do not add box 4 or box 6 to `domain_companion_presence_pairs` as a mandatory companion on income statements; allow statements without withholding to simply be excluded from the withholding family.


## Section 6: Probe on the Real Coordinator

The committed probe script `docs/phases/engine-breadth/milestones/form-1099-withholding-evidence/withholding_probe.py` evaluates the proposed successor architecture through `packages.derivation.live.live_coordinate_run` against a throwaway publication surface in a temporary directory.

### Filer Statement Recording Discipline
Unlike earlier synthetic shortcuts that asserted member findings via plain `assertion` acts and closed families at genesis horizons, `withholding_probe.py` records statement entries exactly as a real filer would:
1. **Entities Introduced**: Payer and statement entities are introduced (`entity-introduced`) with required schemas and labels.
2. **Statement Companions Asserted**: Same-statement income facts and required companions are asserted:
   - Form 1099-INT: Box 1 interest income companion.
   - Form 1099-DIV: Box 1a ordinary dividends companion.
   - Form 1099-R: Box 2a taxable amount, distribution code (`"7"`), IRA/SEP/SIMPLE checkbox (`true`), and box 2b not determined (`false`) companions asserted before Box 1 taxable distribution.
   - Form 1099-G: Box 4 authority witness (`0.0`) asserted before Box 1 unemployment compensation ($6,000).
   - Form SSA-1099: Box 6 authority witness (`0.0`), Box 3 benefits paid, Box 4 repayment (`0.0`), recipient (`"taxpayer"`), statement kind (`"ssa-1099"`), and lump-sum election (`false`) asserted before Box 5 net benefits ($12,000).
3. **Withholding Recorded via Member-Transitions**:
   - Each non-zero withholding amount is asserted using an `act-member-transition` (`member-transition`), advancing the family horizon from its genesis predecessor (`demo.h.<family>.0`) to a successor horizon (`demo.h.<family>.1`).
4. **Family Closures Asserted at Active Horizon**:
   - For families with recorded members, the closure fact is asserted at the active successor horizon (`demo.h.<family>.1`).
   - For empty families, the closure fact is asserted at the genesis horizon (`demo.h.<family>.0`).

### Structure of the Probe Surface
- **Throwaway Publication Surface**:
  - Synthesizes an artifact package declaring all 5 source families (`f1099int.b4`, `f1099div.b4`, `f1099r.box4`, `f1099g.b4`, `ssa1099.b6`), all 5 closure mappings, all 5 subtotal rules, the v2 successor Line 25b rule (`tax.us.2025.rule.form1040-line25b.v2`), and a baseline v58 Line 25b rule (`tax.us.2025.rule.form1040-line25b.v1` publishing to `tax.us.2025.payments.line25b.v58`).
  - Registers fact types for all income companions, authority witnesses, withholding member facts, closure facts, and subtotal symbols.
- **Cases Evaluated**:
  - **Case 1 (1099-G Withholding Reaches Line 25b)**: A synthetic 1099-G statement records $6,000 unemployment and $250 withholding via member-transition. All families closed. The subtotal rule computes $250, and Line 25b computes $250.
  - **Case 2 (SSA-1099 Box 6 Reaches Line 25b)**: A synthetic SSA-1099 statement records $12,000 benefits and $380 voluntary withholding via member-transition alongside a 1099-R statement with $120 withholding. The SSA-1099 subtotal computes $380, the 1099-R subtotal computes $120, and Line 25b sums all 5 subtotals to $500.
  - **Case 3 (v58 Answer Set Equivalence)**: An answer set with no withholding statements has all 5 families closed empty. Both the successor Line 25b rule and the v58 baseline rule compute exactly 0.
  - **Case 4 (Unclosed New Family Blocks with Fact/Family Named)**: Family `tax.us.2025.f1099g.b4` has no closure assertion asserted. The subtotal rule `tax.us.2025.rule.f1099g-b4-subtotal` blocks with disposition `blocked`, code `SOURCE_SET_UNCLOSED`, and missing `['tax.us.2025.f1099g.b4']`. Form 1040 line 25b v2 blocks with disposition `blocked`, code `DEPENDENCY_ABSENT`, and missing `['tax.us.2025.unemployment.b4-withholding-subtotal']`.

### Exact Output of `withholding_probe.py`
```
=== Withholding Real Coordinator Probe ===

--- Case 1: 1099-G withholding reaches line 25b ---
1099-G Subtotal (tax.us.2025.unemployment.b4-withholding-subtotal): 250
Line 25b (tax.us.2025.payments.line25b): 250
pubs1: {'tax.us.2025.interest.b4-withholding-subtotal': '0', 'tax.us.2025.dividends.b4-withholding-subtotal': '0', 'tax.us.2025.ira.box4-withholding-subtotal': '0', 'tax.us.2025.unemployment.b4-withholding-subtotal': '250', 'tax.us.2025.ssa1099.b6-withholding-subtotal': '0', 'tax.us.2025.payments.line25b': '250', 'tax.us.2025.payments.line25b.v58': '0'}
blk1: []
PASS: 1099-G withholding reaches line 25b.

--- Case 2: SSA-1099 box 6 reaches line 25b (along with 1099-R) ---
SSA-1099 Subtotal (tax.us.2025.ssa1099.b6-withholding-subtotal): 380
1099-R Subtotal (tax.us.2025.ira.box4-withholding-subtotal): 120
Line 25b (tax.us.2025.payments.line25b): 500
PASS: SSA-1099 box 6 withholding reaches line 25b.

--- Case 3: v58-shaped answer set with no withholding ---
Line 25b successor (tax.us.2025.payments.line25b): 0
Line 25b v58 baseline (tax.us.2025.payments.line25b.v58): 0
PASS: v58 answer set without withholding matches v58 baseline (both 0).

--- Case 4: Unclosed new family blocks with fact named ---
Line 25b published: None
1099-G Subtotal disposition: blocked, code: SOURCE_SET_UNCLOSED, missing: ['tax.us.2025.f1099g.b4']
Line 25b disposition: blocked, code: DEPENDENCY_ABSENT, missing: ['tax.us.2025.unemployment.b4-withholding-subtotal']
PASS: Unclosed family blocks subtotal and Line 25b with fact/family named.
```


## Section 7: Successor Rule, Family, Bundle, and Package Versions

This catalog names every successor and newly introduced rule, family, closure mapping, bundle, form field, citation, and package version for the Track 1 implementation. Every entry is cross-checked against active package `package.core-calculations.v58.json`, published registry `published-packages.v56.json`, and release `demo.release.sli-worksheet-integration.2025.v56.json`:

| Artifact Type | File Name | Artifact ID | Artifact Version | Schema Version | Prior Version | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| **Package** | `package.core-calculations.v59.json` | `tax.us.2025.package.core-calculations` | `v59` | `package.v2` | `v58` | Successor core calculations package adopting new families, closure mappings, and rules |
| **Registry** | `published-packages.v57.json` | `package-registry.v57` | `v57` | `package-registry.v1` | `v56` | Appends checksum of core package v59 |
| **Release** | `demo.release.sli-worksheet-integration.2025.v57.json` | `demo.release.sli-worksheet-integration.2025` | `v57` | `release-registry.v1` | `v56` | Successor integration release |
| **Rule** | `rule.form1040-line25b.v2.json` | `tax.us.2025.rule.form1040-line25b` | `v2` | `rule-artifact.v3` | `v1` | Replaces 3-way sum with 5-way sum (INT, DIV, 1099-R, 1099-G, SSA-1099) |
| **Form Field** | `form1040.line-25b.form-field.v2.json` | `tax.us.2025.form1040.line-25b` | `v2` | `form-field.v1` | `v1` | Corrects description to include 1099-G and SSA-1099; removes 1099-K |
| **Citation** | `citation.form1040.line-25b.v2.json` | `tax.us.2025.citation.form1040.line-25b` | `v2` | `authority-citation.v1` | `v1` | Updated line range and verbatim text from 2025 Form 1040 instructions |
| **Bundle (1099-G)** | `f1099g-box4.bundle.json` | `tax.us.2025.f1099g.box4.vocabulary` | `v1` | `bundle.v2` | None (New) | Declares box 4 fact, closure fact, and subtotal fact |
| **Family (1099-G)** | `family.f1099g-b4.json` | `tax.us.2025.f1099g.b4` | `v1` | `source-family.v1` | None (New) | Member predicate: `tax.us.2025.f1099g.box4-withholding` |
| **Closure Mapping (1099-G)** | `closure-mapping.f1099g-b4.json` | `tax.us.2025.closure-mapping.f1099g-b4` | `v1` | `source-closure-mapping.v2` | None (New) | Admits `tax.us.2025.unemployment.b4-withholding-subtotal` on closure |
| **Rule (1099-G Subtotal)** | `rule.f1099g-b4-subtotal.json` | `tax.us.2025.rule.f1099g-b4-subtotal` | `v1` | `rule-artifact.v3` | None (New) | Aggregates 1099-G box 4 findings |
| **Bundle (SSA-1099)** | `ssa1099-box6.bundle.json` | `tax.us.2025.ssa1099.box6.vocabulary` | `v1` | `bundle.v2` | None (New) | Declares box 6 fact, closure fact, and subtotal fact |
| **Family (SSA-1099)** | `family.ssa1099-b6.json` | `tax.us.2025.ssa1099.b6` | `v1` | `source-family.v1` | None (New) | Member predicate: `tax.us.2025.ssa1099.box6-voluntary-withholding` |
| **Closure Mapping (SSA-1099)** | `closure-mapping.ssa1099-b6.json` | `tax.us.2025.closure-mapping.ssa1099-b6` | `v1` | `source-closure-mapping.v2` | None (New) | Admits `tax.us.2025.ssa1099.b6-withholding-subtotal` on closure |
| **Rule (SSA-1099 Subtotal)** | `rule.ssa1099-b6-subtotal.json` | `tax.us.2025.rule.ssa1099-b6-subtotal` | `v1` | `rule-artifact.v3` | None (New) | Aggregates SSA-1099 box 6 findings |
| **Family (SSA-1099 Benefits)** | `family.ssa1099-benefits.v2.json` | `tax.us.2025.ssa1099.benefits` | `v2` | `source-family.v1` | `v1` | Succeeded to strike `"box-6 withholding absent or zero"` limitation |
| **Closure Mapping (SSA Benefits)**| `closure-mapping.ssa1099-benefits.v2.json`| `tax.us.2025.closure-mapping.ssa1099-benefits` | `v2` | `source-closure-mapping.v2` | `v1` | Binds to `family.ssa1099-benefits` v2 |


## Section 8: Case Table and Reproduction Script

The committed script `docs/phases/engine-breadth/milestones/form-1099-withholding-evidence/compute_cases.py` evaluates and reproduces the exact figures for the six cases identified in the milestone plan (`docs/phases/engine-breadth/milestones/form-1099-withholding.md`).

### Evaluation Methodology & Rate Schedule Reconciliation
- **Coordinator Governing Figures**: Where cases compute on v58 or the successor shape, figures are evaluated using `packages.derivation.live.live_coordinate_run`. In accordance with statutory Form 1040 rules (`rule.form1040-line16` and `rule.qdcg-worksheet.line-24`), taxable income under $100,000 is figured using the IRS Tax Table on $50 band midpoints (`floor(income / 50) * 50 + 25`).
- **Continuous Schedule Reconciliation**: For filers in the 12% bracket whose taxable income is an exact multiple of $50, the $25 midpoint offset adds exactly $25 * 0.12 = $3.00 in tax (e.g. $4,595 Tax Table vs $4,592 continuous schedule in Case 1; $3,875 Tax Table vs $3,872 continuous schedule in Case 5A). Per milestone stop condition 2, the coordinator numbers govern; both are reported below.

### Case Table

| Case | Description | Form 1040 Line 24 (Total Tax) | Line 25a (W-2 Withholding) | Line 25b (1099 Withholding) | Line 25d (Total Withholding) | Line 33 (Total Payments) | Line 35a (Refund) | Line 37 (Amount Owed) | Key Finding / Effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Case 1** | Unemployment with 10% withheld ($600 on $6,000 UI) | $4,595 *(cont: $4,592)* | $4,500 | $600 | $5,100 | $5,100 | $505 *(cont: $508)* | $0 | Line 25b includes $600; bottom line moves by exactly +$600 (from -$95 owed on v58 to +$505 refund) |
| **Case 2A**| SSA-1099 box 6 voluntary withholding alone ($800) | $3,719 *(cont: $3,716)* | $2,500 | $800 | $3,300 | $3,300 | $0 | $419 *(cont: $416)* | Box 6 voluntary withholding credited to line 25b, reducing amount owed from $1,219 to $419 |
| **Case 2B**| SSA-1099 box 6 ($800) + Form 1099-R gross $10,000 with box 4 ($1,200) | $4,919 *(cont: $4,916)* | $2,500 | $2,000 | $4,500 | $4,500 | $0 | $419 *(cont: $416)* | 1099-R gross adds $10,000 income (12% tax = +$1,200); withholding also +$1,200; owed stays $419 |
| **Case 3** | Form 1099-K with backup withholding in box 4 | Refused | Refused | Refused | Refused | Refused | Refused | Refused | SC-R1 obstacle; 1099-K box 4 refused outside class; does not compute line 25b |
| **Case 4** | MFJ return with withholding on two 1099-Gs ($500 TP + $400 SP) | $6,426 *(cont: $6,423)* | $7,000 | $900 | $7,900 | $7,900 | $1,474 *(cont: $1,477)* | $0 | 1099-G subtotal sums both statements ($500 + $400 = $900) across spouses into line 25b |
| **Case 5A**| v58 answer set without withholding on successor v59 | $3,875 *(cont: $3,872)* | $4,500 | $0 | $4,500 | $4,500 | $625 *(cont: $628)* | $0 | Closed-empty families publish 0; exact preservation of v58 coordinator result ($3,875 tax, $625 refund) |
| **Case 5B**| Nonzero 1099-G box 4 ($600) transition (v58 -> v59) | $4,595 *(cont: $4,592)* | $4,500 | $600 | $5,100 | $5,100 | $505 *(cont: $508)* | $0 | Transitions from REFUSED on v58 (authority witness rejection) to COMPUTED on v59; refund = $505 |
| **Case 6** | Form 1099-INT recorded without box 4 answer on 1 of 2 statements | $3,971 *(cont: $3,968)* | $4,500 | $50 | $4,550 | $4,550 | $579 *(cont: $582)* | $0 | Statement without box 4 answer excluded; subtotal collects asserted statement ($50) without error |

### Explanation of Case 2B Numbers
In the milestone plan, Case 2B introduces a Form 1099-R statement on top of Case 2A. A question arose regarding why total tax increased from $3,719 in Case 2A to $4,919 in Case 2B:
1. **Case 2A Baseline**:
   - Wages: $40,000.
   - Form SSA-1099: $12,000 gross benefits ($8,700 taxable Social Security under the 85% statutory formula).
   - Standard Deduction (Single): $15,750.
   - Taxable Income: $40,000 + $8,700 - $15,750 = **$32,950**.
   - Total Tax (Line 24): **$3,719** (Tax Table midpoint $32,975; continuous schedule $3,716).
   - Payments: W-2 ($2,500) + SSA-1099 box 6 voluntary withholding ($800) = **$3,300**.
   - Amount Owed: $3,719 - $3,300 = **$419** (continuous schedule: $416).
2. **Case 2B Addition**:
   - Case 2B adds a Form 1099-R statement reporting a **$10,000 gross distribution** with **$1,200 box 4 federal income tax withheld**.
   - Because taxable Social Security is already capped at the maximum 85% ($8,700), the entire $10,000 distribution is included in gross income.
   - Taxable Income: $32,950 + $10,000 = **$42,950** (+ $10,000).
   - **Marginal Rate**: Both $32,950 and $42,950 fall entirely within the 2025 12% marginal tax bracket ($11,925 to $48,475 for Single filers).
   - **Tax Increase**: 12% of $10,000 is exactly **$1,200**. Total tax rises from $3,719 to **$4,919** (+$1,200; continuous schedule: $3,716 + $1,200 = $4,916).
   - **Withholding Increase**: Form 1099-R box 4 adds **$1,200** to Line 25b ($800 SSA + $1,200 R = $2,000), raising total payments from $3,300 to **$4,500** (+$1,200).
   - **Net Bottom Line**: The $1,200 tax increase is exactly offset by the $1,200 withholding increase. The amount owed remains identical at **$419** ($4,919 tax - $4,500 payments).
3. **P0 First Pass Defect**: The initial draft of P0 suffered from unquoted shell variable substitution, which truncated "$10,000 gross distribution" from the text and obscured the source of the income increase.

### Script Reproduction
The reproduction script is executed as follows:
```sh
python3 docs/phases/engine-breadth/milestones/form-1099-withholding-evidence/compute_cases.py
```
Output matches the table above.


## Section 9: Findings for the Owner

This section synthesizes the critical architectural findings and decisions developed during P0 verification for the owner's disposition:

### 1. The Core Architectural Question: Substrate Engine Change vs Global Table Relaxation

The fundamental architectural dilemma uncovered by P0 is that Form 1099-G box 4 and Form SSA-1099 box 6 withholding are currently blocked at finding admission in the coordinator, not by calculation rules.

#### What Would Change (Option b: Substrate Engine Change)
To support withholding cleanly without breaking legacy package semantics:
- `packages/kernel/findings.py:_apply_assertion` and `packages/kernel/act_log.py:append` must be updated to inspect `proj.acts` for active package adoption (`act-package-adoption.v1`).
- Companion presence and value domain enforcement (`_enforce_companion_presence`) must be parameterized by the active package's declared source families.
- Packages declaring `tax.us.2025.f1099g.b4` and `tax.us.2025.ssa1099.b6` admit positive withholding; legacy packages (v58 and earlier) retain the strict refusal.

#### What Option (b) Costs
- **Substrate Work**: Requires editing `packages/kernel/` files.
- **Verification Gate**: Under `AGENTS.md`, any substrate change under `packages/kernel/` requires running the **full test suite** (`pytest`, ~7 minutes) before PR merge, rather than the fast lane.
- **Milestone Scope**: Requires owner authorization to expand this milestone's charter beyond content-only artifacts into kernel machinery.

#### What Happens If We Don't (Option a: Global Table Relaxation)
- Relaxing `domain_companion_value_domains` in `packages/tax/loader.py` avoids editing `packages/kernel/`.
- However, our empirical probe proved that running a v58 answer set through the coordinator with relaxed tables results in **silent withholding omission**:
  - The $600 unemployment withholding is admitted into the workspace.
  - Unemployment income ($6,000) flows to Schedule 1 line 7, Form 1040 line 8, and increases total tax to $4,595.
  - But `rule.form1040-line25b.v1` on v58 only sums INT, DIV, and 1099-R. It ignores the 1099-G withholding.
  - Line 25b publishes 0, Line 33 publishes only W-2 withholding ($4,500), and the taxpayer is assessed $92 in tax owed instead of receiving a $508 refund.
  - The withholding is completely and silently lost from the return calculation.

#### Why Content-Only (Option c) Is Invalid
- Form 1099-G box 1 and SSA-1099 box 5 unconditionally require same-statement companion authority facts restricted to `{None, 0}`.
- Routing withholding through an alternate fact would require filers to assert a false `box4-authority = 0` witness on statements that actually had withholding, directly violating Article 9 and ADR-0038 documentary integrity.

#### Decision Required of the Owner
Does the owner authorize expanding milestone scope to implement Option (b) (package-scoped admission in `packages/kernel/findings.py`), or does the owner direct adopting Option (a) with documented acceptance of the legacy silent-omission behavior?

---

### 2. Form 1099-K Box 4 SC-R1 Obstacle and Recommended Posture
- **Finding**: Declaring a source family with member predicate `tax.us.2025.f1099k.box4-federal-withholding` causes `tax_registry()` to register that fact type in `registry.family_member_predicates`. Because `record_f1099k_statement_durably()` records statements by emitting plain `assertion` acts, kernel rule SC-R1 (`packages/kernel/findings.py:756-775`) immediately fails with:
  `ContributionError: cannot assert member fact ... through a plain assertion; must use a member-transition instead`
  This breaks 9 existing unit tests on main across `tests/test_f1099k_statement_removal_increment_c.py` and `tests/test_family_handover_recording.py`.
- **Recommendation**:
  Adopt **Alternative A** (as recommended in Section 4). Leave Form 1099-K box 4 outside the class by refusal (`DEPENDENCY_ABSENT` via `backup-withholding-unsupported`). In Track 2, update the Form 1040 Line 25b form-field description (`form1040.line-25b.form-field.v2.json`) to remove Form 1099-K from the cited document list. This avoids complex kernel migrations, does not invalidate existing 1099-K statement logs, and accurately reflects that 1099-K backup withholding remains parked.

---

### 3. Mandatory Closure Fact Attestation on Successor Packages
- **Finding**: Because `rule.form1040-line25b.v2` statically requires all 5 document withholding subtotals, and the engine lacks dynamic/conditional rule input pins, every filer upgraded to the successor package must assert closed-empty closures (`source-closure = true` at horizon `h0`) for all withholding families not reported on the return.
- **Coordination**: The interview layer / coordinator must ensure that closed-empty assertions are supplied for unentered withholding families to prevent Line 25b from blocking on `DEPENDENCY_ABSENT`.

---

### 4. Missing Box 4 / Box 6 Answer Posture
- **Finding**: Statements recorded without a box 4 or box 6 answer are cleanly excluded from withholding source collections without error.
- **Recommendation**:
  Do **not** enforce companion presence for box 4 / box 6 across income statements. Requiring box 4 on every statement would be a breaking change across all v58 answer sets, tests, and fixtures. The standing present-sources-skip-closure posture is safe, clean, and consistent across all five Form 1099 withholding sources.

---

### 5. Form 1040 Line 25 Law Partitioning Confirmed
- **Finding**: Primary IRS instructions (`i1040gi-2025.txt` lines 2559–2576 and 2577–2604) establish that:
  - **Line 25b** strictly includes Form(s) 1099-R box 4, Form(s) 1099 box 4 (including 1099-INT, 1099-DIV, 1099-G), Form SSA-1099 box 6, and Form RRB-1099 box 10.
  - **Line 25c** is reserved for Form W-2G box 4, Form 8959 line 24, Schedule K-1 withholding, and foreign withholding forms (1042-S, 8805, 8288-A).
  Gambling withholding on Form W-2G belongs on Line 25c, not Line 25b. The milestone plan's scope boundary focusing Line 25b on 1099-G and SSA-1099 is exactly aligned with federal tax law.


## Section 10: Retrospective on the Initial P0 Pass

1. **What it misidentified**: It misidentified Form 1099-G box 4 and Form SSA-1099 box 6 as a content-only rule milestone, failing to recognize that admission invariants in `loader.py`/`live.py` reject non-zero withholding findings before computation rules ever execute.
2. **What it missed**: It missed that relaxing global admission tables causes legacy packages (v58) to silently drop withholding from Line 25b, and that preventing this silent omission across package versions requires an engine change in `packages/kernel/findings.py`.
3. **Why (Root Cause)**: It relied on isolated synthetic throwaway packages with hand-asserted findings rather than running end-to-end evaluations through the real coordinator with authentic statement companions and legacy package comparison.

