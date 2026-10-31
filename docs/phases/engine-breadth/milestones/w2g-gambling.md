<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "w2g-gambling",
  "status": "Open. P0 designed the Form W-2G route (two families, Schedule 1 line 8b, line 25c); Track 1 builds it on core v65.",
  "scope": [
    "a return with gambling winnings reported on Form W-2G computes: box 1 on Schedule 1 line 8b, box 4 federal withholding on Form 1040 line 25c",
    "each W-2G family has its own closure, and an unconfirmed family blocks its lines",
    "gambling outside the bounded class (unreported winnings, losses, professional gamblers) stays refused by answer",
    "earlier packages and every return without gambling keep their results"
  ],
  "non_goals": [
    "no gambling losses on Schedule A line 16 unless P0 shows the class is wrong without them, and then only after a decision",
    "no professional gambler (Schedule C) and no state withholding",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package, parameter or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/milestone-retrospectives/2026-10-28-form-1099-withholding.md",
      "docs/phases/engine-breadth/milestones/w2g-gambling.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/w2g-gambling.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/w2g-gambling.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/w2g-gambling.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Gambling Winnings on Form W-2G (2025)

Milestone key: w2g-gambling.
Branch: milestone/w2g-gambling-2025, stacked on
`milestone/credit-line-explanations-2025` (`56532ac1`, PR #236), so the
successor package is core v65, registry v63, release v63.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

Form 1040 line 25c publishes a constant zero: its rule notes say the 2025
instructions name only Form W-2G box 4 there and "the engine reads no W-2G".
A filer with gambling winnings is refused by an answer (a Schedule 1 Part I
or Schedule A boundary question). Gambling winnings reported on Form W-2G
are among the most common "other income" a household sees, and the form
carries both the income and the withholding.

The useful outcome: a filer who records each Form W-2G, and confirms every
one is recorded, sees box 1 on Schedule 1 line 8b (and through total income
to the bottom line) and box 4 on line 25c, each walkable to its statement;
anything outside the bounded class is still refused by answer.

## What we know

- **Engine (core v64).** `rule.form1040-line25c` publishes `round(0)`.
  `rule.schedule-a-boundary-no-gambling-other` and the Schedule A attachment
  mention gambling. Schedule 1 Part I is gated by absence answers read by
  Schedule 1 line 10.
- **The closure lessons of the last three milestones apply:** every new
  subtotal guards its own collect with `require_closed`, and the regression
  test (`tests/test_collect_closure_regression.py`) will fail otherwise.
- **Form 1099 withholding precedent:** the form-1099-withholding milestone
  added new families with their own closure, and companion admission rules
  per package (ADR-0082).
- **What we do not know:** exactly which answers refuse a gambling return
  today and what replacing them means for an existing workspace; whether
  Schedule 1 line 8b exists as a route or must be added with its own
  attachment row; whether winnings not on a W-2G must be asked about (they
  are still income), and so whether the class can be "W-2G only" honestly;
  what to do about gambling losses (itemized only, limited to winnings).

## Actions the team will take

1. **P0 — trace and design.** The law with citations (Form 1040 and
   Schedule 1 instructions for line 8b and line 25c; Form W-2G boxes). How a
   gambling return is refused on v64, from content and a run. The family,
   closure, questions, successors and the v64 → v65 change set; what an
   existing workspace is asked. Hand-computed cases. No content changes.
   Stop if an engine change is needed, or if the honest class needs gambling
   losses.
2. **Decide.**
3. **Track 1 — winnings and withholding.** Successors, core v65 / registry
   v63 / release v63 with `tools/package_successor.py`, cases on the real
   coordinator, v64 pinned.
4. **Track 2 — presentation,** if P0 shows a saved return needs new form
   fields or attachment rows to explain the lines.
5. **Close.** Fresh-reader review, curated history, retrospective, roadmap,
   frontier.

## Cases that will shape the design

- One W-2G, $1,200 slot winnings, no withholding.
- One W-2G, $6,000 with $1,440 (24%) withheld: line 8b, line 25c and the
  refund move by exactly those amounts.
- Two W-2Gs, one for each spouse on a joint return.
- A recorded W-2G with its family unconfirmed: lines 8b and 25c block.
- Gambling winnings not reported on a W-2G, and gambling losses: refused by
  answer, never left out.
- A v64 return with no gambling: unchanged on v65.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Each unit commits as it goes. Stop
means stop.

## P0 result

P0 is in [trace and design](w2g-gambling-evidence/p0-trace-and-design.md),
with the probe and its output beside it.

- **Law.** Schedule 1 line 8b is gambling winnings not from a trade or
  business, whether or not on a Form W-2G (i1040gi-2025, Schedule 1 line 8b);
  line 25c is W-2G box 4. Only boxes 1 and 4 change an amount. Losses are a
  Schedule A line 16 itemized deduction limited to winnings (100 percent for
  2025). The Form W-2G itself is not in the local sources; box 1 to line 8b
  is from the form and needs corroboration in review.
- **Today.** v64 has no W-2G fact type. The answer
  `schedule1-part1-scope.no-sch1-other-income` refuses any other income, so
  line 10 is inapplicable and line 8 blocks; line 25c is a constant 0.
- **Design.** Two families with their own closures (`w2g.b1`, `w2g.b4`),
  two guarded subtotals, a new `rule.schedule1-line8b`, and one new absence
  answer (no Schedule 1 other income except Form W-2G winnings). Successors:
  Schedule 1 line 10 v2→v3, line 25c v1→v2, the Schedule 1 attachment v4→v5,
  and form fields for Schedule 1 lines 8b and 10 and Form 1040 lines 8 and
  25c. No schema.
- **Class boundary.** The new answer refuses winnings with no W-2G, other
  line 8 income and business gambling; when a W-2G is recorded the winnings
  subtotal also reads the existing Schedule A gambling declaration, so
  losses stay refused by answer.
- **On adoption** a workspace with no gambling is asked three questions: the
  two closures and the new other-income answer.

## Decisions

Foreman, 2026-10-31, on P0's section 6:

1. **One v65** with the form fields in Track 1 (D1).
2. **The loader companion entries are authorized** (D7): a W-2G recorded
   under a package that cannot read it must be refused at recording, never
   computed without it (ADR-0082), so the W-2G presence pairs are declared
   for every package and v65 declares what it admits, as v59 did for Form
   1099-G and SSA-1099 withholding. This is `packages/tax/loader.py` data,
   not an engine change.
3. **Asked afresh** (D5, D6): the three adoption questions, and the new
   other-income answer, rather than carrying the old answer over in code.
4. **Parked:** a standard-deduction filer with gambling losses is refused,
   though losses do not change a standard-deduction return (D2); the
   Schedule A absence answers are inert unless Schedule A is required (D3).

## Tracks

1. **Track 1 — winnings and withholding.** The citizens in P0 section 3;
   core v65 / registry v63 / release v63 with `tools/package_successor.py`;
   the loader entries; cases on the real coordinator for every case in P0
   section 5; v64 pinned; the closure regression test passing with the new
   collects.
