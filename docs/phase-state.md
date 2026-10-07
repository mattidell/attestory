<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-result-explanation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/student-loan-result-explanation.md",
  "milestone_state": "closed",
  "status": "Closed. Schedule 1 line 21 explains its saved result on the existing reader: each statement, its amount and loan, what the person said, what the application assumed, what is left with the person, how the amount was worked out, and which statement a blocking reason names. No calculation changed.",
  "current_role": "Foreman — select next milestone",
  "current_prompt": "docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md"
}
-->

# Phase State

## Current result

**Student Loan Result Explanation is closed.** A person can now understand
the bounded student-loan deduction from its saved result on the existing
reader. Starting at Schedule 1 line 21, the page shows:

- each Form 1098-E statement, its loan and the amount it reported;
- for a supported statement, three separate groups: what the person said,
  what the application took as given, and the conditions left with them;
- how the amount was worked out from the interest reported, the income the
  worksheet read and the limits it pinned;
- which run and workspace revision the explanation describes.

On a blocked line, each reason names its statement by structured identity.
A statement a reason names shows no favorable detail. No calculation changed.

The milestone rests on Student Loan Deduction Completion (PR #203). In that
work, recorded loan and statement links and two ordinary answers decide the
deduction through package `core-calculations` v41, and ADR 0077 records the
engine contracts.

## Begin here

- [Milestone plan](phases/tax-concept-derivation/milestones/student-loan-result-explanation.md):
  the design (P1–P9), the deferred input-transition design, and the phase
  assessment.
- [Retrospective](milestone-retrospectives/2026-10-06-student-loan-result-explanation.md):
  lessons and carried follow-ups.
- [Tax Concept Derivation roadmap](phases/tax-concept-derivation/tax-concept-derivation-roadmap.md):
  next-milestone selection.

## Immediate next action

Select the next milestone. The plan's phase assessment recommends weighing
closure of Tax Concept Derivation against adding another vertical: its exit
criteria are met in bounded form. This milestone's PR is curated, and the
owner merges after the independent final review and CI bind its final head.

## Parked

- Mixed-method input and assumption management (the plan's deferred design).
- Person-supplied scoped values where automation stops.
- Mixed-period treatment (ADR 0076 Part 3).
- Institutional verification, a broad input journey and a general reader.
