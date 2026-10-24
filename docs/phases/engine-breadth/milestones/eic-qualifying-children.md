<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-qualifying-children",
  "status": "Planned. P0 designs the smallest honest model of an EIC qualifying child from the law and the engine's existing entity facts, and verifies the 1, 2 and 3-or-more child columns.",
  "scope": [
    "compute the 2025 earned income credit with one, two, or three or more qualifying children, as successor content",
    "record each qualifying child as a small set of per-child answers whose meaning matches the rules that read them",
    "refuse, rather than guess, when the engine cannot settle who may claim a child",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no child tax credit, credit for other dependents, additional child tax credit or dependency exemption logic beyond what the EIC reads",
    "no tie-breaker computation between taxpayers; a child another person may also claim is outside the class",
    "no head-of-household eligibility check; filing status stays an answer",
    "no Worksheet B, Form 8862, combat pay, Medicaid waiver exclusion or Worksheet 1; they stay outside the class by the existing answer",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-23-earned-income-credit.md",
      "docs/phases/engine-breadth/milestones/eic-qualifying-children.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-qualifying-children.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-qualifying-children.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-23-earned-income-credit.md",
      "docs/phases/engine-breadth/milestones/eic-qualifying-children.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# The 2025 Earned Income Credit with Qualifying Children

Milestone key: eic-qualifying-children.
Branch: milestone/eic-qualifying-children-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-23.
Starting point: `origin/main` at `0beec295` (PR #220 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216); whichever merges second
takes the next free package, registry and release versions.

## What we are trying to accomplish

On core v53 a filer with no qualifying child gets the earned income credit.
A filer who answers that they have a qualifying child is outside the class,
and that is most of the credit's value: the 2025 maximum is $649 with no
child and $4,328, $7,152 and $8,046 with one, two and three or more.

The useful outcome is that a filer with qualifying children gets the credit
from the right table column, each child counted only when the law's tests
are met from answers about that child, and the explanation names each child
counted and each test. Where the law needs facts about another taxpayer (the
tie-breaker rules), the engine refuses rather than picks.

## What we know

- **Law (downloaded, ignored, under `temp/tax-on-taxable-income/sources/`).**
  The 2025 Form 1040 instructions carry Step 1 (the child-count AGI tests),
  Step 3 (qualifying child: relationship, age, residency, joint return, SSN),
  the "qualifying child of more than one person" rules, the separated-spouse
  rule for married filing separately, and the EIC Table's 1, 2 and 3-or-more
  columns. Rev. Proc. 2024-40 §2.06 has the amounts.
- **Engine (core v53).** `tax.us.2025.parameter.eic-2025` already holds every
  child count's amounts and rates. `tax.us.2025.parameter.eic-table-2025`
  holds only the 0-child columns. The previous P0 formula
  (`earned-income-credit-evidence/probe.py`) reproduces all columns. The
  qualifying-child answer `tax.us.2025.eic.no-qualifying-child` is one
  return-level yes/no. Fact types can carry entity identity keys (for
  example the W-2's employer and slip keys). There is no model of a child or
  dependent.
- **What we do not know.** The smallest per-child model: which tests can be
  one answer per child and which must be separate; how a child is identified
  and counted with existing operations (`count`, `collect` over a source
  family); whether recording per-child answers needs any recording work
  beyond fact types and a family; how "another person can also claim the
  child" is asked so that the refusal is honest; how the separated-spouse
  rule and head of household interact with the child columns; how the
  qualifying-child answer from v53 is succeeded; and the qualifying child
  who lacks an SSN (who keeps the filer off the childless credit).

## Actions the team will take

1. **P0 — model and verify.** Record the child tests with citations. Design
   the per-child model and trace it on the real path (recorded acts, family,
   closure, count, marshalling). Verify the 1, 2 and 3-or-more table columns
   against the printed table, as the 0-child columns were. Hand-compute a
   case table. No content changes.
2. **Decide.** Settle the contract: the per-child facts and family, the
   refusal, the successor to the qualifying-child answer, rules, versions and
   compatibility. A new schema, expression operation or owner-visible choice
   returns to the owner first.
3. **Track 1 — the credit with children.** Per-child facts, the child count,
   the table columns, the successor rules, the package chain and cases
   through the real path.
4. **Track 2 — presentation.** Saved presentations whose explanation walk
   names each counted child and each test.
5. **Close.** Fresh-reader review, the full lane before ready, exact-head CI,
   retrospective, coverage frontier and parked list.

Charters for each unit name the readability and required-versus-read checks
up front, the two lessons of the previous milestone: a rule set must explain
as the worksheet does, and every answer a rule requires must be read on the
path that publishes the result.

## Cases that will shape the design

- One, two and three children on the phase-in, plateau and phase-out, single
  and joint; four children (same column as three).
- A child who fails one test (too old, lived with the filer half the year or
  less, filed a joint return); that child is not counted.
- A qualifying child without a valid SSN: not counted for the child columns,
  and the filer cannot take the childless credit.
- A child another person may also claim: outside the class.
- Married filing separately with a qualifying child, under and not under the
  separated-spouse rule; head of household with children.
- A return with children above its column's completed amount ($0) and the
  existing early stops.
- Every existing golden keeps its package and its result.

P0 computes the figures for these cases from the sources.
