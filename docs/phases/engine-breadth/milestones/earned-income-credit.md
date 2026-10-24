<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "earned-income-credit",
  "status": "Track 1 complete: the earned income credit for filers with no qualifying child on core v53. Track 2 adds saved presentations.",
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

## P0 result

P0 is complete ([law and scope](earned-income-credit-evidence/p0-law-and-scope.md)).
No schema successor, expression operation or engine change is needed.

- **The 2025 EIC Table is a formula with existing operations.** $50 bands,
  the credit at the band midpoint rounded half up, with three corners: the
  earned income amount, the phase-out threshold, and the starred band that
  holds the completed phase-out amount. `probe.py` matched all 1,374 bands,
  10,984 cells and 8 footnote bands. The rates (7.65, 34, 40 and 45 percent;
  phase-out 7.65, 15.98 and 21.06 percent) are not printed; they reproduce
  every maximum and cell.
- **Slice (a), filers with no qualifying child, is recommended first.**
  Earned income is W-2 box 1, AGI and investment income (taxable and
  tax-exempt interest, ordinary dividends, the positive part of line 7a) are
  already computed. Married filing separately and head of household without a
  qualifying child are $0 from filing status. Qualifying children (slice b)
  need a per-child model and a tie-breaker refusal; they follow.
- **The senior deduction's SSN and age answers are not the EIC's.** The EIC
  SSN test adds two card conditions, applies to every filer, and the EIC age
  test includes someone born January 1, 1961. The EIC gets its own answers.
- **The lines 27a-31 answer needs a successor for lines 28-31 only.** A v52
  workspace that answered it is blocked on the successor package until the
  new answers are given; it does not keep a silent $0.

## Contract

1. **Slice (a).** The credit for filers with no qualifying child, Worksheet A
   on W-2 box 1, the 0-child column (joint for married filing jointly, other
   for single and qualifying surviving spouse). Married filing separately
   and head of household without a qualifying child are $0.
2. **Questions, each `yes`/`no`, no default:**
   - no qualifying child for the EIC (`no` is outside the slice and blocks);
   - the filer's SSN is valid for the EIC, and the spouse's on a joint return;
   - not a nonresident alien for any part of 2025 (filer and spouse);
   - age: the filer, or the spouse on a joint return, was born after
     December 31, 1960 and before January 2, 2001;
   - main home in the United States for more than half of 2025;
   - not a qualifying child of another person, and not claimable as a
     dependent (each asked only when the return is not joint);
   - **one answer for the unsupported situations:** none of Form 2555, Form
     8862 or a disallowance bar, Worksheet B (self-employment, clergy, church
     employee, statutory employee), the combat pay election, a Medicaid
     waiver exclusion, or the Worksheet 1 items (Schedule E, Form 4797, Form
     8814, personal-property rental, passive activity). `no` blocks;
   - lines 28-31: the return claims none of the additional child tax credit,
     American opportunity credit, refundable adoption credit or Schedule 3
     Part II.

   The draft wording in the P0 evidence is the starting point; each title says
   exactly what its rule reads.
3. **Asked only where the answer can change the result.**
   - No EIC question is required when investment income is over $11,950, or
     when earned income or AGI is at or above $68,675 (the largest completed
     phase-out amount); line 27a is $0 with the reason named.
   - Otherwise the qualifying-child answer is required. With no qualifying
     child, the remaining EIC questions are required only when earned income
     and AGI are below the 0-child completed amount for the column ($19,104
     other, $26,214 joint) and the filing status is single, married filing
     jointly or qualifying surviving spouse.
   - A failing eligibility answer gives $0 with that test named. A missing
     required answer blocks with the fact named.
   - The lines 28-31 answer is required on every return that adopts the
     successor package.
4. **Rules, one per worksheet line:** investment income, eligibility, Worksheet
   A lines 1, 2, 3, 5 and 6 (line 4 is the branch inside line 6), line 27a,
   lines 28-31, the lines 27a-31 total v2 and line 32 v2. One cited parameter
   `tax.us.2025.parameter.eic-2025` holds the $11,950 limit and every child
   count's amounts and rates, so a later child slice reuses it. Each rule
   under 5KB, or the size reported with the reason.
5. **Successor content only:** core v53, registry v51, release v51 (unless PR
   #216 merges first), an adoption fixture and new goldens. Earlier packages,
   saved presentations and goldens stay byte-identical.
6. **Data safety and lanes:** synthetic amounts only; the full lane runs
   before the PR is marked ready.

## Parked by this milestone

- Qualifying children (slice b): per-child facts, the separated-spouse rule,
  and a refusal when another person can claim the same child.
- Worksheet B, Form 8862, combat pay, the Medicaid waiver exclusion and
  Worksheet 1, each outside the class by one answer.
- A spouse who died in 2025 for the age test; the line 27c election not to
  claim the credit.
