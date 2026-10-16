<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-interest-circumstances",
  "active_plan": "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md",
  "milestone_state": "planned",
  "status": "Initial product phase and opening milestone plan. Investigate mortgage-interest circumstances and assumptions before selecting implementation. No build charter or production change yet.",
  "current_role": "Foreman — refine the mortgage-interest plan from the ordinary case and current behavior",
  "current_prompt": "docs/phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md"
}
-->

# Phase State

## Current direction

The owner has shelved Shared Understanding in Development and returned to
product work. Tax Circumstance Breadth extends the student-loan approach to
additional tax areas: ordinary circumstances are recorded, translated into
tax concepts, used by calculations and explained in a correctable account.

The proposed first application is mortgage interest: what the loan paid for
and how that bears on the interest reported on Form 1098. The form calculation
already has a bounded route; ordinary-circumstance support and its assumption
policy remain to be designed. The next tax area remains unselected.

## Begin here

- [Phase purpose and provisional endpoint](phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md).
- [Roadmap](phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md).
- [Opening milestone actions and decisions](phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md).

Start with the person's situation and the current live calculation. Develop
the plan incrementally, and review its first concrete account before selecting
a representation or build. Defaults and assumptions must have deliberate
behavior for the selected case; no general framework is already selected.

## Inherited position

Evolving Workspace Accounts is concluded at the bounded result delivered
through PR #207. Its visual review, independent reader assessment and use on
personal workspaces remain open. The shelved experiments and their evaluation
are preserved on `milestone/working-model-experiment-statement-scope`; they are
not dependencies of this product branch. This branch starts from `origin/main`.

Interest allocation, mixed-period treatment, external institutional
verification, general intake and the student-loan shared-answer restrictions
remain separate questions. Revisit a deferral when the new case needs it,
without treating an earlier software limitation as the definition of a tax
concept or as a permanent product decision.
