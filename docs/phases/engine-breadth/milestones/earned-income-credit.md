<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "earned-income-credit",
  "status": "Planned. P0 verifies the 2025 earned income credit law and recommends a bounded first slice from what the engine already knows about the filer and their income.",
  "scope": [
    "compute the 2025 earned income credit on Form 1040 line 27a for a bounded class of filers the engine can identify, as successor content",
    "ask only the eligibility questions the credit's rules read, each with a meaning that matches its consuming rule",
    "replace the combined lines 27a-31 absence answer with one that leaves the earned income credit out",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no self-employment, farm, clergy or other earned income the engine does not compute; earned income is what the engine already computes",
    "no additional child tax credit, American opportunity credit, adoption credit or Schedule 3 Part II; they stay declared absent",
    "no Form 8862 recertification or prior-year disallowance handling; declared absent",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-22-refund-or-amount-owed.md",
      "docs/phases/engine-breadth/milestones/earned-income-credit.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/earned-income-credit.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/earned-income-credit.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-22-refund-or-amount-owed.md",
      "docs/phases/engine-breadth/milestones/earned-income-credit.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# The 2025 Earned Income Credit

Milestone key: earned-income-credit.
Branch: milestone/earned-income-credit-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-23.
Starting point: `origin/main` at `4a85495a` (PR #219 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216); whichever merges second
takes the next free package, registry and release versions.

## What we are trying to accomplish

On core v52 every computed return reaches a refund or an amount owed, but
lines 27a-31 are $0 only because the person answers that the return claims
none of the refundable credits. The largest of them is the earned income
credit. A low-income worker who is eligible today must either answer that
question falsely and lose the credit, often thousands of dollars, or answer
truthfully and be outside the supported class.

The useful outcome is that an eligible filer in a bounded class gets the
credit on line 27a, computed from the 2025 EIC Table and worksheet, and an
ineligible filer gets $0 for a reason the explanation names. Each eligibility
question is asked only where its answer can change the result.

## What we know

- **Law (downloaded, ignored, under `temp/tax-on-taxable-income/sources/`).**
  The 2025 Form 1040 instructions carry the lines 27a-27c instructions (Steps
  1-6 near text line 2641), EIC Worksheets A and B, and the 2025 EIC Table
  (near text line 3206). Rev. Proc. 2024-40 §2.06 carries the 2025 amounts.
  The investment income limit is $11,950.
- **Engine.** Core v52 computes earned income from W-2 box 1 (line 1z), AGI,
  interest, dividends and capital gains (the inputs to the investment income
  test), filing status, and age-65 and dependent answers. It records valid-SSN
  answers for persons aged 65 or older (senior deduction), and lines 27a-31 as
  one absence answer
  (`tax.us.2025.lines27-31-scope.no-refundable-credits-or-other-payments`).
  It has no model of a qualifying child or dependent.
- **What we do not know.** How the EIC Table can be computed with existing
  operations (the previous Tax Table used a banded midpoint formula); which
  eligibility tests the engine can answer from what it already computes, and
  which need new questions; whether qualifying children can be supported
  without a dependent model (and what the smallest honest model is); how
  married filing separately is treated for 2025; whether the senior
  deduction's valid-SSN answers can be reused or must be asked of everyone;
  and how line 27a's absence answer should be split from lines 28-31.

## Actions the team will take

1. **P0 — verify and scope.** Record the 2025 law with citations: every
   eligibility test, the investment income limit, the earned income and AGI
   computations, the EIC Table's construction, and the phase-in and phase-out
   amounts by number of children and filing status. Classify each test as
   computed from existing facts, a new question, or outside the class.
   Recommend a first slice (for example no qualifying children, or a counted
   number of qualifying children with per-child questions) with its cost.
   Determine whether the EIC Table is expressible with existing operations.
   Hand-compute a case table. No content changes.
2. **Decide.** Settle the contract: the slice, questions, rules, the split of
   the lines 27a-31 answer, versions and compatibility. A new expression
   operation, schema successor or owner-visible choice returns to the owner
   first.
3. **Track 1 — the credit.** Parameters, the EIC Table formula, eligibility
   and worksheet rules, the successor line 27a and line 32 rules, the package
   chain, and cases through the real path.
4. **Track 2 — presentation.** Saved presentations whose explanation walk
   reaches the table row, the earned income and AGI comparison, and each
   eligibility answer.
5. **Close.** Fresh-reader review of the curated candidate, the full lane
   before ready, exact-head CI, retrospective, coverage frontier and parked
   list.

## Cases that will shape the design

- Single, no qualifying children, aged 25-64, wages in the phase-in, the
  plateau and the phase-out; just above the end of the phase-out ($0).
- The same filer aged 24 or 65 (no credit without a qualifying child).
- Investment income at and just above $11,950.
- Married filing jointly with wages from both spouses.
- AGI greater than earned income (for example interest income), where the
  worksheet takes the smaller credit.
- If the slice includes children: one, two and three or more.
- A return answering none of the new questions on the successor package is
  blocked with the missing facts named, never a silent zero.
- Every existing golden keeps its package and its result.

P0 computes the figures for these cases from the sources.
