<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "tax-on-taxable-income",
  "status": "Opening plan. P0 verifies the 2025 rate schedule, Tax Table rule, preferential-rate bands and standard deduction from primary sources, inventories every demo parameter, traces line 16, and measures golden impact. No content change is chosen before P0.",
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
    ]
  }
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
