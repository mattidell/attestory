<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "cf-loss-limit",
  "status": "Closed 2026-11-18. Tests only; no package version change.",
  "retrospective": "docs/milestone-retrospectives/2026-11-18-cf-loss-limit.md",
  "scope": [
    "a return whose capital loss comes from Form 8949 box C or F sales (no Form 1099-B) gets the right Schedule D line 21 loss limit ($3,000, or $1,500 married filing separately), the same as box A, B, D and E losses; the 2026 carryover is out of scope (Decision 1)",
    "the behaviour is pinned by tests through the real coordinator and saved page"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "inbound carryovers from 2024 stay as they are (the boundary answer)",
    "no change to boxes A, B, D or E behaviour"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/cf-loss-limit.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/cf-loss-limit.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/cf-loss-limit.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/cf-loss-limit.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Box C and F Losses Are Limited and Carried (2025)

Milestone key: cf-loss-limit.
Branch: milestone/cf-loss-limit-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-18.
Starting point: main at `fbd81501` (core v96, registry v94, release v94).
Expected target: tests only if P0 finds the behaviour right; core v97,
registry v95, release v95 if a content repair is needed.

## What we are trying to accomplish

Schedule D line 21 limits a net capital loss to $3,000 ($1,500 when
married filing separately), and the excess carries to 2026. The parked
list records that neither the separate-return limit nor the carryover
is exercised for losses from Form 8949 boxes C and F (sales with no
Form 1099-B). A filer with only such sales should get the same limit
and carryover as one whose losses come from a broker statement. The
useful outcome is evidence that they do, pinned by tests, or a bounded
repair if they do not.

## Stages

1. **P0.** Build synthetic returns that reach line 21 and the carryover
   from box C and F losses under every filing status the engine
   supports, run them through the real coordinator and saved page,
   compare against hand values from the 2025 Schedule D instructions
   and the Capital Loss Carryover Worksheet, and the same losses through
   box A/D as a control. If a value is wrong, trace it and name the
   smallest repair.
2. **Track 1.** Pin the cases as tests; publish a content repair only if
   P0 needs one, with the strict full-surface replay
   (`tools/recorded_replay.py`, `full`) over the 775 recorded lists.
3. **Fresh review**, repair, closeout.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/cf-loss-limit-evidence/p0.md`
(scripts `cases.py`, `hand.py`, `compare.py`; outputs `runs.json`,
`comparison.json`).

- 90 synthetic returns on core v96: box C, box F and C plus F, and the same
  amounts through box A/D as a control, under all five filing statuses, with
  the loss below, at and above the limit. Every return ran through
  `live_coordinate_run` and the saved page to `saturated` with no blocked
  rule and no question.
- All 900 line checks (Schedule D lines 7, 15, 16, 21, the box line, Form
  1040 lines 7a and 15) match the hand values from the 2025 Schedule D
  instructions. Every box C/F return equals its A/D control on every line,
  disposition and question; only the Form 8949 attachment differs, as it
  should.
- The engine computes only the inbound 2024 to 2025 carryover (Schedule D
  lines 6 and 14). No 2025 to 2026 carryover is computed or shown for any
  box, by ADR-0058 and ADR-0060 Decision 7. The hand values for it are in
  the evidence (2,000 in each over-limit case; 250 short-term and 1,750
  long-term for the split married-filing-separately case).
- Recommendation: tests only. No content repair.
- For the foreman: the plan's "right 2026 carryover" conflicts with those
  ADRs; narrow the milestone to the limit (recommended) or open a
  superseding ADR and a separate milestone. Also whether line 21's page
  text should say the excess carries forward.

## Decisions

1. **Narrow to the limit; tests only (2026-11-18, foreman, on P0's
   recommendation).** P0 ran 90 returns (boxes C, F, C plus F and an
   A/D control; all five filing statuses; below, at and above the
   limit): 900 of 900 line checks match hand values, and every C/F
   return equals its A/D control. No content repair is needed. The plan
   also asked for "the right 2026 carryover", but the engine computes
   no 2025-to-2026 carryover for any box, by accepted ADR-0058 and
   ADR-0060 (Decision 7 of each). That is a product boundary, not a box
   C/F defect; this milestone does not cross it. Track 1 pins the cases
   and asserts that no 2026 carryover is published, so the boundary
   stays visible.
2. **Park the carryover and the line 21 wording for the owner.**
   Whether to compute the 2026 carryover needs a superseding ADR the
   owner accepts. Whether line 21's page text should say the excess
   carries forward is a content successor, but it speaks to a boundary
   the ADRs set, so it waits on the same owner question.
3. **Note, outside scope.** Head of household and qualifying surviving
   spouse were accepted with no qualifying person recorded. Parked as
   an observation.
4. **Repair the review notes (2026-11-18, foreman).** The fresh review
   (`docs/reviews/cf-loss-limit/review.md`) is READY with notes; its
   mutations (separate-return limit raised, box C or F dropped, a 2026
   carryover published) each fail the tests. CFL-R1 to R3 are
   corrected: the test docstring states the per-worker run cost,
   track1.md the 30 returns and 12 controls, and the plan's scope drops
   the carryover. CFL-R4 is accepted as a limit: the boundary test reads
   published names, so a carryover under another name or only in page
   text would pass it; the full-surface replay is the stronger check
   when a milestone touches that boundary. CFL-R5 and R6 are
   informational.

## Closeout

Closed 2026-11-18. Box C and F losses get the same Schedule D line 21
limit as box A/D losses under all five filing statuses: 900 of 900 line
checks match hand values from the 2025 Schedule D instructions, and
every C/F return equals its A/D control. 72 live and 10 fast tests pin
it, including that no 2025-to-2026 carryover is published (ADR-0058 and
ADR-0060 Decision 7). Whether to compute that carryover, and whether
line 21 should say the excess carries forward, are parked for the
owner.

