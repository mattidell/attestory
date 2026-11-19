<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "gain-break-even",
  "status": "Closed 2026-11-19. Tests only; no package version change.",
  "retrospective": "docs/milestone-retrospectives/2026-11-19-gain-break-even.md",
  "scope": [
    "a sale with a gain or exactly zero gain reaches Form 8949 and Schedule D correctly on every sale path the engine accepts (covered and noncovered Form 1099-B, code B, code W, no Form 1099-B; short and long term), the same way a loss does",
    "the behaviour is pinned by tests against hand values, or a bounded content repair if P0 finds a wrong value"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "Form 8949 codes other than B and W, collectibles and section 1250 gain, Form 2439 and K-1 capital gains stay out",
    "no 2026 carryover (ADR-0058 and ADR-0060 Decision 7)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/gain-break-even.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/gain-break-even.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/gain-break-even.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/gain-break-even.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Gains and Break-Even Sales Reach Schedule D (2025)

Milestone key: gain-break-even.
Branch: milestone/gain-break-even-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `07583f69` (core v96, registry v94, release v94).
Expected target: tests only if P0 finds the behaviour right; core v97,
registry v95, release v95 if a content repair is needed.

## What we are trying to accomplish

The parked list carries "Gain and break-even reporting on Form 8949 and
Schedule D" from before the phase-state retirement, with no detail.
Schedule D current-year losses (closed 2026-08-03) made the covered,
basis-reported class gain-or-loss, and later milestones added
noncovered, code B, code W and no-Form-1099-B sales, mostly exercised
with losses. The useful outcome is evidence that a gain and an exact
break-even on each of those paths reach Form 8949, Schedule D lines 7,
15, 16 and Form 1040 line 7a correctly (and, for a net gain, the
qualified-dividends-and-capital-gain tax path), pinned by tests; or a
bounded repair. If the item turns out already covered, closing it with
the evidence is the outcome.

## Stages

1. **P0.** Census which sale paths existing tests already exercise with
   a gain and a break-even; build synthetic returns for the gaps; run
   them through the real coordinator and saved page; compare to hand
   values from the 2025 Form 8949 and Schedule D instructions. Check
   the accepted ADRs and each rule's notes for a bound before treating
   a missing value as a defect (cf-loss-limit retrospective).
2. **Track 1.** Pin the gaps as tests; publish a content repair only if
   P0 needs one, with the full-surface replay (`tools/recorded_replay.py
   full`) over the recorded lists.
3. **Fresh review**, repair, closeout.

## Decisions

1. **Tests only, a 27-return subset (2026-11-19, foreman, on P0's
   recommendation).** On core v96 all 1,134 line checks across 50
   ordinary returns match hand values; every path already ran a gain
   and a break-even on older cores, but no test does on v96, and the
   long-term break-even with no Form 1099-B never ran on any core.
   Track 1 pins 22 single-filer cases (including that one), one joint
   long-term gain, the three mixed returns netting to a gain, and one
   code W gain probe that must block (ADR-0062 Decision 2 via ADR-0066).
2. **Bounds recorded, no change.** A break-even return files Schedule D
   with line 16 of 0 even when both Exception 1 answers are yes. The
   Form 1040 Exception 1 wording is literally met by a sale that nets
   zero, but the Form 8949 instructions, Line 1 ("Enter all sales and
   exchanges…"), require the sale to be reported, and no dollar changes
   (review GBE-R4). On returns with no long-term gain the worksheet
   lines still publish as intermediates; line 25 equals the Tax Table
   amount.
3. **Parked.** A code W gain block asks the filer no question; the page
   explains the reason. Added to the parked list at closeout.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/gain-break-even-evidence/p0.md`
(scripts `cases.py`, `hand.py`, `compare.py`, `census.py`,
`gbe_census_plugin.py`; outputs `runs.json`, `comparison.json`,
`census.json`).

- Census: a scratch plugin recorded every live coordinator run with a sale
  across the 94 sale-related test files (2,245 runs from 25 files). Gains and
  break-evens run on every path, but only on cores v11 to v94; on the current
  v96 only losses run. The long-term no-Form-1099-B break-even has never run.
- 54 synthetic returns on core v96 through `live_coordinate_run` and the
  saved page: a gain and a break-even on every path (covered as the control,
  code W, code B, noncovered, no Form 1099-B), short and long term, single
  and joint; three mixed returns netting to a gain; four code W probes.
- All 1,134 checks on the 50 ordinary returns match the hand values from the
  2025 Form 8949, Schedule D and Form 1040 instructions: Form 8949 part
  totals, Schedule D lines 1a-16, Form 1040 lines 7a, 15 and 16, the
  preferential base and the capital gain worksheet. Every return saturated
  with no block and no question.
- Bound: a code W row with a positive box 1g on a gain or break-even blocks
  (ADR-0062 Decision 2, mechanism ADR-0066); a code W gain with box 1g 0
  computes. A break-even sale files Schedule D with line 16 = 0 by the v10
  rule; worksheet lines publish as intermediates on non-preferential returns
  with no dollar effect.
- Recommendation: tests only. No content repair and no replay.
- For the foreman: Track 1's case subset (27 suggested), and two noted-only
  observations (break-even and Exception 1; no question on a code W gain
  block).
4. **Repair the review notes (2026-11-19, foreman).** The fresh review
   (`docs/reviews/gain-break-even/review.md`) is READY with notes; 12
   in-memory mutations all fail the tests. GBE-R1: the code W probe is
   held by a second rule (`ADJUSTMENT_EXCEEDS_LOSS`) too, so the test
   must also assert the code-W-on-gain sentence the page shows on line
   1b. GBE-R2 and R3: correct the evidence docstrings and state the
   measured cost. GBE-R4: Decision 2 now cites the Form 8949 Line 1
   instruction.

## Closeout

Closed 2026-11-19. On core v96 a gain and an exact break-even reach Form
8949, Schedule D, Form 1040 line 7a and the line 16 tax correctly on
every accepted sale path: 1,134 of 1,134 line checks across 50 returns
match hand values. No test had run a gain on v96, and the long-term
no-Form-1099-B break-even had never run. 27 returns are pinned (28 live
tests) with 17 fast hand-value tests; the code W gain probe asserts both
the block and its page sentence.

