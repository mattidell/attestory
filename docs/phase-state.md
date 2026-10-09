<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Evolving Workspace Accounts",
  "topic": "account-refinement",
  "active_plan": "docs/phases/evolving-workspace-accounts/milestones/account-refinement.md",
  "milestone_state": "closed",
  "status": "Closed. One Form 1098-E can gain loan detail while another keeps its older answer. Line 21 combines each form's older answer and current detail (core calculations v42, worksheet v5) without retiring any answer, and the saved explanation separates what was said, used, assumed and recorded but not used.",
  "current_role": "Foreman — select next milestone",
  "current_prompt": "docs/phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md"
}
-->

# Phase State

## Current result

**Updating an Account Without Losing Its Meaning is closed.** A person can
add borrowing and schooling details to one Form 1098-E while another form
keeps its older eligibility answer. Line 21 no longer refuses the return
because the two forms use different kinds of input.

For each form, the application reads the person's current answers:

| The form's current answers | Result for that form |
| --- | --- |
| The detail agrees with the older answer | Supported |
| The detail is missing, withdrawn or denied | Supported; the older "yes" covers it |
| A "cannot tell" answer | Not supported; the answer is named |
| A contradicting answer, or an older "no" | Not supported; the contrary answer is named |

No answer is retired to satisfy the engine. Each amount is counted once,
and the cap, phase-out and scope limits apply to the return's total. The
saved explanation shows, for each form:

- what the person said;
- what the calculation used;
- what it assumed;
- what was recorded but not used.

Its wording is provisional.

Production is package `core-calculations` v42, with `rule.sli-worksheet` v5.
By owner decision, the worksheet is `rule-artifact.v13` with an inert second
path. ADR 0077 records the change in an amendment line.

## Begin here

- [Milestone plan](phases/evolving-workspace-accounts/milestones/account-refinement.md):
  the staged investigation, the Track 0 selection and closure, and the
  outcome with its limits.
- [Retrospective](milestone-retrospectives/2026-10-08-account-refinement.md):
  lessons and follow-ups.
- [Evolving Workspace Accounts roadmap](phases/evolving-workspace-accounts/evolving-workspace-accounts-roadmap.md):
  next-milestone selection.

## Immediate next action

Select the next milestone, or conclude the phase; that is the owner's
decision. The plan's phase assessment separates two things:

- the calculation transition, which is firmly demonstrated;
- the saved explanation, which needed two post-closeout repairs and is
  still provisional in wording and unassessed by a fresh reader.

The milestone PR is published after curation, final review and CI bind its
head. The owner merges.

## Parked

- Five conservatively blocked states, as deferred design (see the
  retrospective).
- Whether a shared-answer "no" should reach the whole return (P0 question
  1).
- General assumption management, person-supplied scoped values, and
  mixed-period treatment (ADR 0076 Part 3).
- Institutional verification, a broad input journey and a general reader.
