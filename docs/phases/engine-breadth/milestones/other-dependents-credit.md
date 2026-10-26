<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "other-dependents-credit",
  "status": "Planned. P0 verifies the 2025 credit for other dependents and Credit Limit Worksheet B, and designs the dependents beyond qualifying children.",
  "scope": [
    "compute the 2025 credit for other dependents on Schedule 8812 line 8 and line 19 for a bounded class, as successor content",
    "record dependents who are not qualifying children for the child tax credit, from answers about each, whose meaning matches the rules that read them",
    "decide whether Credit Limit Worksheet B is computed or stays outside the class by answer",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no head-of-household or dependency-exemption logic beyond what the credit reads",
    "no tie-breaker computation; a dependent another person may also claim is outside the class",
    "no new income source",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-24-child-tax-credit.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-24-child-tax-credit.md",
      "docs/phases/engine-breadth/milestones/other-dependents-credit.md",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# The 2025 Credit for Other Dependents

Milestone key: other-dependents-credit.
Branch: milestone/other-dependents-credit-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-25.
Starting point: `origin/main` at `c35c0896` (PR #224 merged). Runs in parallel
with the mortgage same-borrowing milestone (PR #216); whichever merges second
takes the next free package, registry and release versions.

## What we are trying to accomplish

On core v55 the child tax credit is computed for qualifying children under
17, but a return with any other dependent is blocked: a child aged 17 or
older, a child whose identification number is not an SSN valid for
employment, or a qualifying relative such as a parent. Schedule 8812 gives
$500 for each other dependent (line 6), combined with the child tax credit on
lines 8 to 14 and capped at tax. Credit Limit Worksheet B replaces Worksheet A
for some returns. Finishing these completes Schedule 8812 for the engine's
bounded class.

The useful outcome is that a family with other dependents gets the credit,
each dependent counted from answers about that dependent, and a return that
needs something outside the class is refused, never given $0.

## What we know

- **Engine (core v55).** A credit roster over the EIC child kind counts
  qualifying children under 17 with an SSN valid for employment
  (`tax.us.2025.ctc.child-roster`). A required return-level answer says the
  return has no other dependent; `no` blocks. Credit Limit Worksheet A is
  computed; Worksheet B's conditions are outside the class by answer.
- **Law.** Schedule 8812 and its instructions are downloaded
  (`temp/tax-on-taxable-income/sources/f1040s8.txt`, `i1040s8.txt`); the Form
  1040 instructions carry the dependency rules (qualifying child and
  qualifying relative steps from about text line 918).
- **What we do not know.** How a dependent who is not a child is modelled
  (qualifying relative: relationship or member of household, gross income
  below the 2025 limit, over half support, not anyone's qualifying child);
  whether children who fail the under-17 or SSN test move to this credit from
  the existing roster or need a second count; the identification-number test
  for this credit (SSN, ITIN or ATIN by the due date); the U.S. citizen,
  national or resident alien test (Canada and Mexico residents can be
  dependents but not for this credit); whether Worksheet B's conditions can
  arise on the engine's routes; and how the "no other dependent" answer is
  succeeded.

## Actions the team will take

1. **P0 — verify and design.** Law with citations; classify each test;
   design the dependent model and trace it on the real coordinator; decide
   Worksheet B; hand-compute cases. No content changes.
2. **Decide.** The model, questions, successors and versions.
3. **Track 1 — the credit.** Per-dependent answers and count, Schedule 8812
   lines 6-14 with both credits, the successor package and cases.
4. **Track 2 — presentation.**
5. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, frontier and parked list.

## Cases that will shape the design

- A child aged 17 or 18 living with the filer; a qualifying child with an
  ITIN; a parent who is a qualifying relative; each with and without
  qualifying children under 17.
- A dependent who fails a test (gross income at or above the limit; not a
  U.S. citizen, national or resident alien).
- Tax below the combined credit (the cap), and the phase-out reducing the
  combined credit.
- A return answering none of the new questions blocks with the facts named;
  every existing golden keeps its result.
