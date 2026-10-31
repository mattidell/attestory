<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "current-core-harnesses",
  "status": "Open. Track 1 builds committed test helpers that make complete current-core returns reaching Form 1040 line 2a, Schedule 8812 line 21 and Schedule 1 line 21 (Form 1098-E), and drives the checks that were structural only.",
  "scope": [
    "committed, reusable helpers that build complete returns on the latest core reaching line 2a (Form 1099-INT box 8 and Form 1099-DIV box 12), Schedule 8812 line 21 (W-2 boxes 4 and 6), and Schedule 1 line 21 (Form 1098-E student loan interest)",
    "the live checks that recent milestones could only make structurally, now driven on the real coordinator",
    "no change to any product code, content or package"
  ],
  "non_goals": [
    "no product, content, package or schema change; a defect found is reported, not fixed here",
    "no rewrite of existing test helpers beyond what the new ones reuse"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/milestone-retrospectives/2026-10-31-itemization-cents.md",
      "docs/milestone-retrospectives/2026-10-31-correction-current-core.md",
      "docs/phases/engineering-health/milestones/current-core-harnesses.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/current-core-harnesses.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engineering-health/milestones/current-core-harnesses.md"
    ],
    "new_milestone": [
      "docs/phases/engineering-health/milestones/current-core-harnesses.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md"
    ]
  }
}
-->

# Complete Current-Core Returns for Tests

Milestone key: current-core-harnesses.
Branch: milestone/current-core-harnesses, stacked on
`milestone/entry-loop-current-core-2025` (PR #242).
Phase: Engineering Health. Opening plan: 2026-10-31.

## What we are trying to accomplish

Three milestones in a row could not drive a line on the real coordinator
because no committed helper builds a complete return on the current core
that reaches it:

- **Form 1040 line 2a and Schedule 8812 line 21** (statements with cents):
  the only harnesses are on old cores; the line 2a one fails on current cores
  with "no active Social Security family chain", and no current-core recorder
  exists for the Form 1099-INT box 9 companion fact. Checked by evaluating
  rule bodies only.
- **Schedule 1 line 21, student loan interest (Form 1098-E)** (statements
  with cents; a correction on the current core): every harness blocks the
  worksheet on unrelated missing inputs.

Each future milestone touching these lines pays the same cost or settles for
a structural check. The useful outcome: one committed place that builds each
such return on the latest core, used to drive the checks that were left
structural.

## Actions the team will take

1. **Track 1 — helpers and live checks.** Build the helpers (in
   `tests/helpers/`), each producing a complete, unblocked return on the
   latest core with its family closures and answers. Drive, live: line 2a
   with cents (two Form 1099-INT box 8 amounts of 100.40); Schedule 8812
   line 21 with Part II-B applying; Schedule 1 line 21 with Form 1098-E
   interest, including cents; and `_line21_view` in the correction session on
   v66. Compare with hand values. If a live check fails, report it as a
   defect and stop on that check; do not fix product code.
2. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to a Sonnet 5.5 Agent sub-agent. Stop means stop.
