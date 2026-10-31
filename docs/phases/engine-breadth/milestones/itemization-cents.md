<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "itemization-cents",
  "status": "Closed. On core v66 statements with cents attach on Schedule 1, Schedule D line 13 and Schedule B Part II, and lines 7, 8b, 3b, 2a, 25b and Schedule 8812 line 21 round once at their total. Schedule B Part I interest (line 2b) still rounds per subtotal: deferred on an owner-held validator question.",
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
      "docs/milestone-retrospectives/2026-10-31-itemization-cents.md",
      "docs/phases/engine-breadth/milestones/itemization-cents.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-itemization-cents.md"
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

Owner direction 2026-10-31 ("proceed"), applied on P0's recommendations:

1. **The five-track split is approved** (P0 section 4): Schedule 1 (6),
   Schedule D line 13 and line 3b (7), the line 2b rounded sibling (5),
   Schedule B Part I subtotals (10), and the other adding lines (11), in the
   order 1, 2, 3a, 3b, 4. The twelve-citizen stop is waived for this
   milestone; each track stays at or under eleven.
2. **The Schedule B $1,500 test reads the rounded figure** (P0 rounds
   `interest-positive-total`).
3. **Line 2b gets a rounded sibling** (content only), not a
   `package_validation.py` change.
4. **One core v66.** Each track extends the same change set and regenerates
   the unmerged v66 / registry v64 / release v64 candidate, deleting the
   previous candidate files first.

5. **Tracks 3a and 3b are deferred (same day).** The rounded line 2b sibling
   needs `form1040.line-2b` v6. The successor-graph table in
   `packages/derivation/package_validation.py` (about lines 2707-2740) pins
   that field at `form-field.v3`/v5 for every later interest-composition
   package, and refuses v6 (`NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED`). Without
   the sibling, Schedule B Part I's subtotals cannot stop rounding without
   line 2b printing cents. Extending the table is a validator change and an
   open owner-held question. Until it is answered, interest amounts with
   cents still block the Schedule B Part I tie-out, and line 2b rounds each
   subtotal first. Track 4 proceeds.

## Tracks

1. Track 1 — Schedule 1. 2. Track 2 — Schedule D line 13 and line 3b.
3. Track 3a — line 2b rounded sibling. 4. Track 3b — Schedule B Part I.
5. Track 4 — lines 25b, 2a and Schedule 8812 line 21.

## Review dispositions

Fresh-reader review of P0 and Tracks 1, 2 and 4: no required findings.
About twenty cents cases (three members, one member, mixed with whole
dollars, .50 rounding up) attached on v66 where v65 blocked, with values
matching hand computation; four line 25b cases matched; the Schedule B
$1,500 test stays on the rounded figure (1,500.40 does not trigger it,
1,500.50 does); four further whole-dollar returns matched v65 numerically;
every changed subtotal kept its guard.

1. *An attachment is now required by a sub-dollar statement* (recommended).
   A Form 1099-G of $0.40 makes Schedule 1 required with line 7 at 0.
   Accepted as intended (a recorded statement makes its schedule required)
   and pinned in tests.
2. *Line 25b's text still said "equals the sum"* (recommended). Fixed with a
   form-field successor.
3. *Whole-dollar subtotals print "300.0" where v65 printed "300"* (note).
   Accepted: the inputs already print that way, and no filed line changes.
4. *Lines 2a and Schedule 8812 line 21 are checked by evaluating their rule
   bodies, not live* (note). No current-core harness reaches them; parked.
5. *The deferral is accurate, and the table also pins `rule.form1040-line2b`
   v8 and `attachment.schedule-b` v7* (note). Recorded in the owner question.

## Execution record

- Sonnet 5.5 sub-agents: P0 about 13 minutes (it met the citizen stop and
  proposed five tracks); one builder for Tracks 1, 2 and 4 and the repair,
  stopping once on a presentation-representation check and once on the
  validator table; one review.
- Each track regenerated the one unmerged v66 candidate.

## Outcome

On core v66, statements with cents compute and attach on Schedule 1
(Forms 1099-G and W-2G), Schedule D line 13 and Schedule B Part II, where v65
blocked them on the tie-out. Lines 7, 8b, 3b, Schedule D line 13, 2a, 25b and
Schedule 8812 line 21 include cents when adding and round once at the
total, as the 2025 instructions say; line 25b over two families of $100.40
is 201, where v65 gave 200. Whole-dollar returns compute as on v65. 25
successors; no engine or schema change.

Not delivered: Schedule B Part I interest. The interest subtotals still
round before line 2b adds them, and interest amounts with cents still block
the Schedule B Part I tie-out, because the package validator pins line 2b's
rule, field and attachment versions. That is an open owner-held question.
