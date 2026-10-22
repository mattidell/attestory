<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "tax-on-taxable-income",
  "status": "Closed. On core v50, Form 1040 line 16 and the standard deduction follow 2025 law: seven brackets through the Tax Table or Tax Computation Worksheet, the capital gains worksheet published line by line, only long-term gain preferential, and the 2025 standard deduction. Earlier packages keep their results.",
  "scope": [
    "replace the demo parameters behind Form 1040 line 16 and the standard deduction with primary-source 2025 values, as successor content",
    "compute tax as the 2025 instructions prescribe, including the Tax Table below $100,000 and the 0/15/20 percent preferential bands",
    "repair the preferential-rate base so short-term gains are taxed at ordinary rates",
    "re-verify every affected golden as an intended change and keep saved history readable"
  ],
  "non_goals": [
    "no new income source, form or attachment",
    "no alternative minimum tax, net investment income tax, additional Medicare tax or credits beyond those already routed",
    "no new 2025 deductions (for example the senior, tips or overtime deductions); they are named frontier rows, not hidden work",
    "no dependent's limited standard deduction unless P0 shows the current route already admits dependents",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md",
      "docs/milestone-retrospectives/2026-10-17-personal-item-sale-circumstances.md",
      "docs/phases/engine-breadth/milestones/tax-on-taxable-income.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/tax-on-taxable-income.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/tax-on-taxable-income.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-22-tax-on-taxable-income.md",
      "docs/phases/engine-breadth/milestones/tax-on-taxable-income.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-22-tax-on-taxable-income.md"
}
-->

# The 2025 Tax on Taxable Income

Milestone key: tax-on-taxable-income.
Branch: milestone/tax-on-taxable-income-verified-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-22.
Starting point: `origin/main` at `903d2619` (PR #215 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216) in its own worktree.

## What we are trying to accomplish

Every route the engine computes ends in the tax on taxable income, Form 1040
line 16, and most pass through the standard deduction. Both still run on
parameters marked `demo.*` in the adopted package (core v49):

- `demo.parameter.tax-brackets.2025` v2 has three brackets (10, 12 and 22
  percent, the last unbounded) at 2024 thresholds. The 2025 schedule has seven
  brackets up to 37 percent.
- `demo.parameter.qdcg-preferential-brackets.2025` v2 taxes every preferential
  amount at a flat 15 percent; there are no 0 or 20 percent bands.
- `demo.parameter.standard-deduction-base.2025` v1 holds $15,000 / $30,000 /
  $22,500, which the parked list already records as not the verified 2025
  amount.
- No rule applies the Tax Table, which the 2025 instructions require below
  $100,000 of taxable income.
- A recorded, unrepaired defect: the preferential-rate base taxes short-term
  covered gains at preferential rates.

So line 16 is wrong for most returns, and badly wrong above about $100,000.
The engine's explanation and provenance are careful, but the law they explain
is a placeholder. The useful outcome is a line 16 and standard deduction that
match the 2025 instructions for every return class the engine already
computes, with each changed result traced to a verified source.

This is a bounded return to Engine Breadth: no new return class becomes
computable, but every existing one becomes correct. It does not retract earlier
synthetic-complete claims, which were about routing, closure and explanation.

## What we know

- Consumers in core v49: `rule.form1040-line16.v5` (rate schedule and
  preferential brackets), `rule.form1040-standard-deduction` v1 (base and
  additional amount), `rule.schedule-d-line21` v1 (capital-loss limit) and
  `rule.ss-benefits-worksheet.v3` (four Social Security worksheet amounts). All
  nine `demo.parameter.*` members are in that set.
- Line 16 v5 requires taxable income, filing status, qualified dividends, the
  selected preferential base and the covered short- and long-term proceeds
  subtotals. Its note says the QDCG arithmetic is unchanged since earlier
  versions.
- The standard-deduction rule already reads age-65 and blindness facts for the
  taxpayer and spouse.
- What we do not know: whether the rule language can express the Tax Table's
  banded midpoint lookup exactly, or needs an expression extension; where the
  short-term defect sits (`rule.selected-preferential-base.v4` or line 16); how
  many goldens and saved presentations change; and whether any other numeric
  2025 law (for example Schedule B's $1,500 threshold, the student-loan cap
  and phase-out, or the mortgage debt limit) is also unverified.

## Actions the team will take

1. **P0 — verify and trace.** From primary sources (the 2025 inflation
   adjustment revenue procedure, the 2025 legislative changes to the standard
   deduction, the 2025 Form 1040 instructions with the Tax Table, the Tax
   Computation Worksheet and the Qualified Dividends and Capital Gain Tax
   Worksheet), record each 2025 value with its citation. Inventory every
   numeric parameter in core v49, `demo.*` or not, against its source. Trace
   line 16, the preferential base and the standard deduction through the real
   coordinator on a few synthetic returns spanning the bands. Locate the
   short-term defect. Determine whether the Tax Table is expressible with the
   current expression language. Count the goldens and saved models each change
   would alter. No content is changed in P0.
2. **Decide.** Settle the contract in this plan: successor parameter ids and
   versions (verified ids, not `demo.*`), how the Tax Table is computed, the
   short-term repair, and compatibility for saved history. Any new expression
   operation, schema successor or owner-visible choice returns to the owner
   first.
3. **Track 1 — successor content.** Add the verified parameters, successor
   line 16, preferential-base and standard-deduction rules, and one successor
   package, registry and release. Prior versions stay byte-identical.
4. **Track 2 — goldens and explanations.** Regenerate affected goldens and
   inspect every changed value against a hand computation from the cited
   source. Saved presentations from earlier packages keep reading as they did.
5. **Close.** Independent review of the curated candidate, exact-head CI,
   retrospective, coverage-frontier and parked-list updates.

## Cases that will shape the design

- Taxable income in each 2025 bracket for each filing status, including
  exactly at a threshold, and just under and over $100,000 (Tax Table versus
  Tax Computation Worksheet).
- Qualified dividends and long-term gains entirely in the 0 percent band,
  straddling 0/15 and 15/20, and above the 20 percent threshold.
- Short-term gain alone, long-term gain alone, both, and a net loss limited by
  line 21: short-term gain must be taxed at ordinary rates.
- Standard deduction for each filing status, with age-65 and blindness
  additions for taxpayer and spouse.
- Every existing route's golden: W-2 only, interest and dividends, Schedule D,
  Social Security, IRA, unemployment, student loan, mortgage, personal sale.

## P0 result

P0 is complete ([2025 law and inventory](tax-on-taxable-income-evidence/p0-law-and-inventory.md),
[path and cost](tax-on-taxable-income-evidence/p0-path-and-cost.md)). Four of
the nine `demo.*` parameters are wrong for 2025:

- **Rate schedule:** three brackets at 2024 thresholds, against seven (Rev. Proc. 2024-40 §2.01).
- **Preferential rates:** a flat 15%, against the 0/15/20 bands (Rev. Proc. 2024-40 §3.03).
- **Standard deduction:** $15,000 / $30,000 / $22,500, against $15,750 / $31,500 / $23,625 (Pub. L. 119-21 §70102; 2025 Form 1040 instructions).
- **Married additional amount:** $1,550, against $1,600 (Rev. Proc. 2024-40).

The capital-loss limit and the four Social Security worksheet amounts are
statutory and match. The Foreman checked the non-`demo` numeric parameters
P0 did not inventory. The Schedule B $1,500 threshold, the student-loan $2,500
cap with its $85,000 / $170,000 threshold and $15,000 / $30,000 range, and the
$750,000 / $375,000 mortgage limit all match 2025 law.

The line 16 mechanism (preferential split, take the smaller) is sound. Its
parameters are wrong, it never uses the Tax Table, and
`rule.selected-preferential-base` v4 publishes `max(Schedule D line 16, 0)`
where the 2025 Qualified Dividends and Capital Gain Tax Worksheet line 3 takes
the smaller of Schedule D lines 15 and 16, or zero if either is a loss. On a
synthetic $5,000 short-term / $1,000 long-term case that alone understates tax
by $350 at today's rates. On the real path, a $596,850 single return computes
$126,360 against $178,445 under 2025 law.

Two P0 statements were corrected by the Foreman against the downloaded
instructions:

- The Tax Table's first rows are not uniform $25 bands. $0–5 is $0, $5–15
  is $1 and $15–25 is $2, after which the table runs in $25 bands to $3,000 and
  $50 bands to $100,000. The midpoint method needs these three rows stated
  explicitly.
- The Tax Table also governs the worksheet's own lines 22 and 24 ("If the
  amount ... is less than $100,000, use the Tax Table"), not only returns
  without preferential income.

P0's change count was also too high. Tests and goldens pin the package
version they run (for example core v20), so existing goldens remain the
record of what their packages computed and do not change. The cost is one
successor package and new cases on it.

## Contract

1. **Successor parameters with verified ids.** These carry citations and keep
   the `demo.*` files untouched:
   - `tax.us.2025.parameter.ordinary-rate-schedule` v1;
   - `tax.us.2025.parameter.preferential-rate-bands` v1;
   - `tax.us.2025.parameter.standard-deduction-base` v1;
   - `tax.us.2025.parameter.additional-standard-deduction` v1.
   - `tax.us.2025.parameter.tax-table-ceiling` v1 (the $100,000 Tax Table limit).

   The matching `demo.*` parameters stay adopted only by earlier packages.
   Statutory amounts that already match (the capital-loss limit and the Social
   Security worksheet) stay as they are in this milestone; their ids are
   named as a follow-up rather than churned.
2. **Tax on an amount.** Below $100,000 it is the Tax Table: the tax on the
   band midpoint at the 2025 rates, rounded to the nearest dollar. Bands are
   $25 up to $3,000 and $50 up to $100,000, with the three rows below $25
   stated explicitly. At $100,000 or more it is the Tax Computation Worksheet.
   This uses the existing operations (`divide` rounding down, `multiply`,
   `add`, `bracket_fold`, `round`, `choose`). No new expression operation and
   no literal table are needed: the formula is the smaller auditable artifact,
   and the explanation names the band.
3. **The capital gains worksheet as auditable steps.** The successor line 16
   publishes the worksheet's material lines as findings, following the
   Capital Loss Carryover Worksheet precedent (ADR-0060):
   - the ordinary amount (line 5);
   - the tax on it (line 22, by the Tax Table or the worksheet);
   - the 0, 15 and 20 percent amounts and their tax (line 23);
   - the tax on all taxable income (line 24);
   - the smaller of the two (line 25).

   Returns with no qualified dividends and no preferential gain take the tax
   on taxable income directly.
4. **Preferential base repair.** The successor `selected-preferential-base`
   uses the smaller of Schedule D lines 15 and 16, or zero if either is blank
   or a loss. Its no-Schedule-D branch (Form 1040 line 7a) is unchanged.
5. **Standard deduction.** The successor rule uses the verified base and
   additional amounts with today's age-65 and blindness facts. Two 2025 rules
   are not computed, and the rule's `left_with_person` says so whenever they
   could apply:
   - the dependent's limited standard deduction;
   - the deduction for a taxpayer or spouse aged 65 or older (Schedule 1-A).
6. **One successor package, registry and release** (next free versions at
   merge). They are additive over core v49 except for the replaced members.
   Earlier packages, their goldens and saved results are unchanged; a
   workspace gets the corrected tax by adopting the new package.

## Tracks

- **Track 1 — content and live cases.** Items 1–6 above, with tests through
  `live_coordinate_run` on the successor package, against the cases below.
- **Track 2 — presentation and record.** One or two saved presentation
  goldens on the new package that show the worksheet steps and the Tax Table
  band; README and coverage-frontier updates; parked-list changes.
- **Close.** Independent review of the curated candidate, then exact-head CI.

### Cases

Single filers on the successor package unless stated otherwise. Expectations
were hand-computed from the verified figures, and each Tax Table value was
checked against the published 2025 table.

| # | Case | Expected |
| --- | --- | --- |
| 1 | Tax on taxable income $46,850 (Tax Table band 46,850–46,900) | 5,387 |
| 2 | $99,999 (last Tax Table band) | 16,909 |
| 3 | $100,000 (Tax Computation Worksheet) | 16,914 |
| 4 | $596,850 (35% bracket) | 178,444.75 before the existing rounding convention (178,445) |
| 5 | Married filing jointly, $150,000 | 22,828 |
| 6 | Bottom rows: $3, $10, $20, $1,000, $2,990, $3,000 | 0, 1, 2, 101, 299, 303 |
| 7 | Qualified dividends $5,000, taxable income $25,000, all in the 0% band | line 5 20,000; line 22 2,165; line 24 2,765; line 16 2,165 |
| 8 | Straddling 0/15: qualified dividends $20,000, taxable income $54,250 | 0% amount 14,100; 15% amount 5,900; line 22 3,875; line 23 4,760; line 24 6,855; line 16 4,760 |
| 9 | Straddling 15/20: qualified dividends $100,000, taxable income $600,000 | 15% amount 33,400; 20% amount 66,600; line 22 144,547.25; line 16 162,877.25 before rounding |
| 10 | Short-term defect: short-term gain $5,000, long-term gain $1,000, taxable income $80,250 | preferential base 1,000 (not 6,000); line 22 12,355; line 23 12,505; line 16 12,505 |
| 11 | Short-term gain $5,000, long-term loss $2,000 | preferential base 0 |
| 12 | Long-term gain $4,000, short-term loss $1,000 | preferential base 3,000 |
| 13 | Standard deduction: single 15,750; married filing jointly with both spouses 65+ 34,700; single, blind and 65+ 19,750; head of household 65+ 25,625; married filing separately 15,750 | as stated |
| 14 | A return with an age-65 fact | the standard-deduction finding's basis names the uncomputed senior deduction; the dependent's limited deduction is named in the same basis |
| 15 | No-Schedule-D route (Form 1040 line 7a capital-gain distributions) on the successor package | preferential base still equals line 7a |
| 16 | Compatibility: a W-2 return on core v49 | unchanged result (line 16 5,390); no existing test or golden edited |

## Execution record

| Unit | Result |
| --- | --- |
| P0 | Four `demo.*` parameters wrong for 2025, no Tax Table, short-term gains in the preferential base; Tax Table expressible with existing operations. Foreman corrected the Tax Table's bottom rows, its use inside the worksheet, and the change count. |
| Track 1 | Core v50, registry v48 and release v48. Verified parameters; the Tax Table and Tax Computation Worksheet; the capital gains worksheet published line by line (lines 4–25); the preferential base as the smaller of Schedule D lines 15 and 16; standard deduction v2 with the line 12 citation and the uncomputed senior and dependent deductions named. All 16 cases pass through the coordinator; core v49 still computes its old result. One repair: the first worksheet rules expanded filing-status choices into 68–83KB expressions, so they were split into one rule per line, each under 5KB, with ceilings looked up by filing status. The first ready-PR `verify` then failed a full-lane data-safety gate that flags six-digit amounts in content: the $100,000 limit became the cited `tax-table-ceiling` parameter, and the three statutory parameters joined the gate's per-id exemptions. |
| Track 2 | Two saved presentation goldens on core v50 (line 16 of 5,387 on a W-2 return and 4,760 on a qualified-dividend straddle); the explanation walk from line 16 reaches worksheet lines 22–25, 9 and 17 and the verified parameters, and from the standard deduction the verified base and line 12 citation; no `demo.*` parameter appears. No projection or explanation change. |


## Outcome

**Work.** Core calculations v50 (registry v48, release v48) computes the 2025
tax for every return class the engine already supports. A single return with
$596,850 of taxable income now computes $178,445 against $126,360 before; one
with $46,850 computes the published Tax Table's $5,387 against $5,390. A
$5,000 short-term gain is no longer taxed at preferential rates. Earlier
packages and their goldens are unchanged; a workspace gets the corrected tax by
adopting v50.

**Assurance.** Sixteen coordinator cases with hand-computed expectations, each
Tax Table anchor checked against the published 2025 table; two v50
presentation goldens; explanation walks that reach each worksheet step and the
verified parameters. No engine, kernel, schema or existing content change.

**Remaining.**
- The deduction for a taxpayer or spouse aged 65 or older (Schedule 1-A) and
  a dependent's limited standard deduction are named, not computed.
- The worksheet lines are reachable through the explanation, but the saved
  presentation does not show them as rows.
- The capital-loss limit and Social Security worksheet amounts are correct but
  keep `demo.*` ids.
- Citation artifacts can name only an instruction family and form, not a
  revenue procedure or statute.

## Readiness, evidence and contracts

Published schemas and adopted content are immutable; every change is a
successor. If a new schema version is needed, record intent in the
schema-intent ledger before editing. Raw source downloads and probe output stay
under `temp/`; committed evidence cites sources by URL and page.

Implementation uses the targeted lanes and `python -m mypy`; any change under
`packages/derivation/` or `packages/kernel/` runs the full suite before the PR
is marked ready. Full CI on the ready head is the gate. Final review of the
curated candidate is independent.

Concurrency: PR #216 may also need a successor core package. Whichever
milestone merges second rebases and takes the next free package, registry and
release versions; neither renumbers the other's merged content.
