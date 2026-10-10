<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "saved-account-resumption",
  "active_plan": "docs/phases/evolving-workspace-accounts/milestones/saved-account-resumption.md",
  "milestone_state": "planned",
  "status": "Initial plan following merged PR #206. Trace reopening the same synthetic workspace after process termination before selecting the recovery implementation.",
  "current_role": "Foreman — review plan and charter P0 stop-and-return investigation",
  "current_prompt": "docs/phases/evolving-workspace-accounts/milestones/saved-account-resumption.md"
}
-->

# Phase State

## Current result

**Reviewing and Correcting the Account Behind a Result is closed.** A person
can open a correction session on a saved student-loan result and choose one
borrowing's answer about whether the loan paid only for school costs. They
read a confirmation that names:

- the borrowing and its recorded relationships;
- the question;
- the current answer and the proposed answer;
- the forms the answer reaches.

They confirm. The correction is saved through the existing reviewed recorder
call, and the return is recalculated under core calculations v42. The new
explanation sits beside the earlier result, which does not change.

The session refuses three things:

- a borrowing it cannot tell apart from another;
- a confirmation whose displayed relationships changed before the save;
- any attempt to save against an answer read from an earlier result.

It reports a correction that was saved but not calculated as exactly that,
and its retry only recalculates. The page is one static file delivered as an
ADR 0049 surface artifact. There is no new schema, ADR or calculation change.
The wording is provisional, and the session works on synthetic workspaces
only.

## Begin here

- [Active plan](phases/evolving-workspace-accounts/milestones/saved-account-resumption.md):
  returning to the same saved account after the process ends.
- [Previous milestone](phases/evolving-workspace-accounts/milestones/account-review-correction.md):
  the walkthrough, the Track 0 selection, the integrated repairs, the
  outcome, and the phase assessment.
- [Retrospective](milestone-retrospectives/2026-10-09-account-review-correction.md):
  lessons and follow-ups.
- [Evolving Workspace Accounts roadmap](phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md).
- README, "Correction session walkthrough": the command for each named state.

## Immediate next action

PR #206 is merged. The owner requested the next milestone:
**Returning to a Saved Account**.
[Active plan](phases/evolving-workspace-accounts/milestones/saved-account-resumption.md).

Charter P0 to trace a correction, a complete process stop, and reopening the
same synthetic workspace from durable records. Establish what already survives,
how the displayed result relates to current answers, and which connection is
missing. Independently review the evidence and plan before selecting the build.
Keep the existing loan-cost question and calculation policy.

The earlier milestones already support the phase's bounded exit. This
additional milestone pursues one returning-user interaction. At its closeout,
reassess phase closure. Owner visual review and the independent-reader
assessment remain open; they are not silently satisfied by this new plan.

## Parked

- The predecessor's five conservatively blocked states, and whether a
  shared-answer "no" should reach the whole return.
- General assumption management, allocation and mixed-period treatment,
  institutional verification, free text, and a general correction or intake
  platform.
- Use of the correction session on a real workspace (the residency path).
