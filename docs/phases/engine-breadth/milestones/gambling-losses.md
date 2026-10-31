<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "gambling-losses",
  "status": "Open. P0 designed a gambling-losses family and Schedule A line 16 limited to winnings, entering the deduction choice; Track 1 builds them on core v67.",
  "scope": [
    "a filer with Form W-2G winnings and gambling losses computes: on the standard deduction, losses do not change the return and are no longer refused; when itemizing, losses up to winnings reach Schedule A line 16",
    "losses are recorded and confirmed complete like any other family",
    "every return without gambling losses keeps its result"
  ],
  "non_goals": [
    "no professional gambler (Schedule C) and no losses beyond winnings carried anywhere",
    "no change to how the choice between standard and itemized deduction is made, unless P0 shows the losses must enter it",
    "no engine, kernel or schema change unless P0 shows one is required, and then only after owner direction",
    "no edit to any published citizen; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-10-31-w2g-gambling.md",
      "docs/phases/engine-breadth/milestones/w2g-gambling.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/gambling-losses.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Gambling Losses (2025)

Milestone key: gambling-losses.
Branch: milestone/gambling-losses-2025, stacked on
`milestone/closure-live-confirmation` (PR #244); a successor package is core
v67, registry v65, release v65.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The Form W-2G milestone kept gambling losses refused by answer: when a W-2G
is recorded, the winnings subtotal reads the Schedule A gambling declaration,
and a filer who says they have losses is refused. Two parked consequences:

- A filer on the standard deduction with gambling losses is refused, though
  losses change nothing on that return.
- A filer who itemizes cannot deduct losses on Schedule A line 16, limited to
  winnings (100 percent for 2025).

The useful outcome: both returns compute, and the explanation shows where
the losses went or why they did not count.

## Actions the team will take

1. **P0 — trace and design.** The law, with citations (Schedule A line 16
   and the 2025 limit; whether a standard-deduction filer reports losses at
   all). How v66 refuses each case, from a run. The design: a losses family
   and closure, a Schedule A line 16 rule limited to winnings, successors
   for the declaration-reading winnings subtotal and Schedule A, and whether
   losses enter the standard-or-itemized choice. Hand-computed cases, using
   `tests/helpers/current_core_returns.py`. No content changes. Stop if the
   engine's deduction choice cannot read the new line without an engine
   change, or if the honest class needs Schedule C.
2. **Decide.**
3. **Track 1.** Successors, core v67 with `tools/package_successor.py`,
   cases on the real coordinator, v66 pinned.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Stop means stop.

## P0 result

P0 is in [trace and design](gambling-losses-evidence/p0-trace-and-design.md),
with the probe beside it.

- **Law.** The 2025 Form 1040 instructions send gambling losses to Schedule
  A line 16 (i1040gi-2025 l.6564-6571); Schedule A is the itemizer's form.
  P.L. 119-21 sec. 70114 sets 90 percent only after 2025, so 2025 is 100
  percent of losses, limited to winnings. The Schedule A instructions are not
  in the local sources; the winnings limit rests on the statute's text there.
- **Today (v66).** With losses declared, `rule.w2g-b1-subtotal` is held, so
  line 8b and everything below block, for a standard-deduction filer as for
  an itemizer. An itemizer is also refused by the Schedule A attachment's
  completeness check on the same declaration.
- **Design (13 citizens, one track).** A losses family with its closure; a
  losses subtotal; `rule.schedule-a-line16` as `choose(no winnings, 0,
  min(losses, winnings))` (a comparison inside `choose`, no new operation);
  a narrower declaration ("no other line 16 deduction") replacing the old
  one; successors for the winnings subtotal (no longer reads the
  declaration), the Schedule A total and its closed-empty form, line 12e
  (line 16 enters the itemized side, so losses can decide the choice), and
  the Schedule A attachment (line 16 as a second itemized part). Core v67.

## Decisions

Foreman, 2026-10-31, on P0's recommendations:

1. **Existing W-2G returns confirm the losses family once** (D1); the old
   declaration does not carry forward with a second meaning.
2. **A hand-entered itemized total and a nonzero line 16 together are
   refused by name** (D2), so losses cannot be counted twice.
3. **Wagering expenses stay out; losses with no winnings count as zero**
   (D3), which is the winnings limit, not a refusal.

## Tracks

1. **Track 1 — losses.** The 13 citizens in P0 section 3, core v67 / registry
   v65 / release v65 with `tools/package_successor.py`, the v67 companion
   entry, the D2 refusal, cases on the real coordinator for P0's section 4,
   v66 pinned.
