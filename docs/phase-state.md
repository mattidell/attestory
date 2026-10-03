<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-deduction-completion",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion.md",
  "milestone_state": "closed",
  "status": "Closed. In one plain, fully supported case, recorded loan and statement links and two ordinary answers decide whether reported student-loan interest counts, through package core-calculations v40; correcting a link changes the deduction and restoring it returns it, and a blocked line 21 names the statement and a reason the person can act on.",
  "current_role": "Foreman — select next milestone",
  "current_prompt": "docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md"
}
-->

# Phase State

## Current result

**Student Loan Deduction Completion is closed.** In one plain, fully supported
case, a person's recorded loan and statement links and two ordinary answers,
not a tax-labelled yes/no, decide whether reported student-loan interest
counts. Package `core-calculations` v40 carries the result through the
existing worksheet to Schedule 1 line 21. Correcting a link changes the
deduction and restoring it returns it. A blocked line 21 names the statement
and gives a reason the person can act on. The favorable result,
`plain-case-supported`, states its basis: what the person said, what a rule
derived, five assumptions made in the person's favor, and four conditions left
with the person. Old-only workspaces keep their results, and a statement
missing one of the old answers now blocks instead of deducting.

Statement corrections are scope-checked at the point of saving, multi-record
saves are atomic, and saved histories with an unreviewed statement rewrite
replay safely. ADR 0077 records the engine contracts.

## Begin here

- [Milestone plan](phases/tax-concept-derivation/milestones/student-loan-deduction-completion.md): the eight sentences, decisions and tracks.
- [Retrospective](milestone-retrospectives/2026-10-03-student-loan-deduction-completion.md): lessons and carried follow-ups.
- [ADR 0077](adr/0077-shared-key-count-basis-same-run-read-and-presence-selection.md): the engine contracts this milestone added.
- [Tax Concept Derivation roadmap](phases/tax-concept-derivation/tax-concept-derivation-roadmap.md): next-milestone selection.

## Immediate next action

Select the next milestone. Publication curation and the independent final
review of this milestone's PR follow on the owner's request.

## Parked

- Person-supplied scoped values where automation stops.
- Explanation of where a return line comes from (roadmap item 13).
- Mixed-period treatment (ADR 0076 Part 3).
