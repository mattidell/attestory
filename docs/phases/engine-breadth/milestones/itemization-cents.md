<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "itemization-cents",
  "status": "Open. P0 traces why amounts with cents block attachments and whether the engine rounds where the instructions say to.",
  "scope": [
    "a return whose statements carry cents computes and attaches, on a successor core package",
    "each line rounds where the 2025 instructions say: cents are included when adding amounts, and only the total is rounded",
    "earlier packages keep their results; a return in whole dollars is unchanged"
  ],
  "non_goals": [
    "no change to the rounding convention itself (whole-dollar returns)",
    "no engine, runner or schema change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/itemization-cents.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/itemization-cents.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/itemization-cents.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/itemization-cents.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Statements With Cents (2025)

Milestone key: itemization-cents.
Branch: milestone/itemization-cents-2025, stacked on
`milestone/w2g-gambling-2025` (`e15146ee`, PR #237), so a successor
package is core v66, registry v64, release v64.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

Two Form 1099-G box 1 amounts of $100.40 publish an unemployment subtotal of
201 and block the Schedule 1 attachment with `ITEMIZATION_TIE_OUT_VIOLATION`
(v64; the same for Form W-2G on v65). Real statements carry cents. The
attachment's tie-out in `attempt_attachment`
(`packages/derivation/runner.py`) compares the raw row sum (200.80) with the
subtotal, and the subtotal rule rounds.

The 2025 instructions (`i1040gi-2025.txt`, "Rounding Off to Whole Dollars",
about lines 1319-1337) say a filer may round to whole dollars, and "if you
have to add two or more amounts to figure the amount to enter on a line,
include cents when adding the amounts and round off only the total." A
subtotal that rounds before its line adds it may disagree with that by a
dollar, and it is what breaks the tie-out.

The useful outcome: statements with cents compute and attach, and every line
rounds once, at its total.

## What we know

- Subtotal rules typically have `value = round(add(collect …))` with the
  rounding convention; lines add the rounded subtotals and round again.
- The tie-out compares the unrounded row sum with the subtotal symbol.

## Actions the team will take

1. **P0 — trace and design.** Cite the rounding rule. List every subtotal in
   core v65 that rounds before a line adds it, and every attachment row set
   it feeds. Reproduce the tie-out block on the real coordinator for each
   attachment, and a case where rounding subtotals first changes a line by a
   dollar against rounding only the total. Design the smallest successor
   set (likely: subtotals stop rounding; the lines that add them round once),
   with the v65 → v66 change set. Stop if the fix needs a runner or schema
   change, or more than twelve successor citizens (propose a split).
2. **Decide.**
3. **Track 1.** Successors, core v66, cases, v65 pinned.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Stop means stop.

## P0 result

P0 is in [trace and design](itemization-cents-evidence/p0-trace-and-design.md).
It met the citizen stop: the fix needs 39 successors, against a limit of 12.

- Two members of 100.40 block the attachment tie-out in every rounding
  family on v65. That covers Schedule 1 (Form 1099-G, Form W-2G), Schedule B
  Parts I and II, and Schedule D line 13.
- Rounding subtotals before a line adds them moves line 2b by a dollar in
  three live cases. It also moves line 25b and the refund by a dollar.
- The proposed design is five tracks of at most 11 citizens each.
  Subtotals that tie out stop rounding, and the lines that read them round
  once. One track adds a rounded sibling for line 2b, because the validator
  fixes Schedule B Part I's line symbol.

## Decisions

Pending (2026-10-31). These questions were left when the usage limit was
reached:

1. Approve P0's five-track split or direct another cut.
2. Choose whether the Schedule B $1,500 test reads the rounded figure or
   the figure with cents (P0 rounds it).
3. Choose between the rounded line 2b sibling (content only) and a
   `package_validation.py` change.
