<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "saved-account-resumption",
  "active_plan": "docs/phases/evolving-workspace-accounts/milestones/saved-account-resumption.md",
  "milestone_state": "closed",
  "status": "Closed. A synthetic correction account can be initialized once, corrected, stopped and reopened by a new process from its files alone; the reopened page shows each loan-cost answer with its predecessor, the latest earlier result and the calculation state, calculates without saving again, and continues the correction. The foreman recommends concluding the phase; that is the owner's decision.",
  "current_role": "Foreman — select next milestone",
  "current_prompt": "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md"
}
-->

# Phase State

## Current result

**Returning to a Saved Account is closed.** A person can initialize a
synthetic student-loan account once, in a directory outside the repository,
and correct a borrowing's loan-cost answer through the correction page. They
can stop the process. A new process then opens the same directory from its
files alone, without seeding it. The opened page shows:

- each borrowing's current loan-cost answer and its earlier answer;
- the latest earlier result, labelled as earlier;
- whether a calculation started and did not finish.

Calculating saves no answer. The correction interaction then continues, and
the next correction names the previous one as its predecessor.

No saved result is presented as describing the current answers, because the
files do not establish that. A token from a stopped process is refused, and
the page says it cannot tell what happened rather than "Not saved". Missing,
duplicate and unreadable result files, and an unreadable record stream, each
have their own sentence, and the answers stay visible in every case.

There is no new schema, ADR, durable store or calculation change. The wording
is provisional, and accounts are synthetic only.

## Begin here

- [Milestone plan](phases/evolving-workspace-accounts/milestones/saved-account-resumption.md):
  the P0 trace, the Track 0 route, the integrated reviews and repairs, the
  outcome, and the phase assessment.
- [Retrospective](milestone-retrospectives/2026-10-11-saved-account-resumption.md):
  lessons and follow-ups.
- [Evolving Workspace Accounts roadmap](phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md).
- README, "Correction session walkthrough" and "Returning to a saved
  account".

## Immediate next action

The owner decides whether to conclude Evolving Workspace Accounts. The
foreman recommends concluding it. The phase's bounded exit was met by the
first two milestones, and this one adds the returning-user path. Three items
stay open, and none needs a new milestone in this phase:

- the owner's visual check of the interaction, with any wording changes;
- an independent reader assessment;
- the real-workspace residency decision.

No tax case is proposed. The milestone PR is published after curation, the
final review and CI binding its head. The owner merges.

## Parked

- The five conservatively blocked states from the account-refinement
  milestone, and whether a shared-answer "no" should reach the whole return.
- General assumption management, allocation and mixed-period treatment,
  institutional verification, free text, and a general correction or intake
  platform.
- Use of the correction session on a real workspace (the residency path).
- Recording a calculation that fails before its run starts.
