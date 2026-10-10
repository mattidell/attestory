<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "account-review-correction",
  "active_plan": "docs/phases/evolving-workspace-accounts/milestones/account-review-correction.md",
  "milestone_state": "closed",
  "status": "Closed. A person can open a saved line 21 result, choose one borrowing's loan-cost answer, confirm a correction, save it through the reviewed recorder, and read the recalculated result beside the unchanged earlier one. The foreman recommends concluding the phase; that is the owner's decision.",
  "current_role": "Foreman — select next milestone",
  "current_prompt": "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md"
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

- [Milestone plan](phases/evolving-workspace-accounts/milestones/account-review-correction.md):
  the walkthrough, the Track 0 selection, the integrated repairs, the
  outcome, and the phase assessment.
- [Retrospective](milestone-retrospectives/2026-10-09-account-review-correction.md):
  lessons and follow-ups.
- [Evolving Workspace Accounts roadmap](phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md).
- README, "Correction session walkthrough": the command for each named state.

## Immediate next action

The owner decides whether to conclude Evolving Workspace Accounts. The
foreman recommends concluding it at this bounded result. Two items stay
open, and neither needs a new milestone in this phase:

- the owner's visual check of the interaction, with any wording changes;
- an independent reader assessment.

No tax vertical is proposed. The milestone PR is published after curation,
the final review, and CI binding its head. The owner merges.

## Parked

- The predecessor's five conservatively blocked states, and whether a
  shared-answer "no" should reach the whole return.
- General assumption management, allocation and mixed-period treatment,
  institutional verification, free text, and a general correction or intake
  platform.
- Use of the correction session on a real workspace (the residency path).
