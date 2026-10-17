<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "multiple-statement-circumstances",
  "active_plan": "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md",
  "milestone_state": "planned",
  "status": "Opening plan for the consolidation milestone. Investigate why the Form 1099-K and Form 1098 circumstance routes stop at a second statement, and what keeping each statement's answers with that statement requires. P0 first; no representation, engine change or production track is selected.",
  "current_role": "Foreman — P0: trace the one-statement limit",
  "current_prompt": "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md"
}
-->

# Phase State

## Current direction

The next milestone is More Than One Statement: Keeping Each Account With Its
Form. Both circumstance routes this phase delivered (one Form 1098, one Form
1099-K) stop at a second statement. The engine cannot keep two statements'
different answers apart, so it treats them as unanswered. Ordinary households
often have two statements. The 2025 Schedule 1 instructions add several Forms
1099-K into the one entry.

Make each statement keep its own account: answered, evaluated, corrected and
explained on its own, with results combined only where the tax rules combine
them. Start with P0: trace the actual cause and test whether existing keyed
joins or the student-loan relationship mechanism already cover it. Then get
P0 independently reviewed and bring back the integration cost and the Form 1098
scope choice. The plan lists actions, not a predicted implementation.

## Inherited result

**Personal-Item Sales: What Was Sold and What the Payment Means** closed
2026-10-17 (PR #210). One Form 1099-K for one personally used item bought and
sold at a loss enters its Box 1a amount at the top of 2025 Schedule 1. The
ordinary account is recorded and corrected, and a saved explanation shows the
report, answers, assumptions, published computation and named reasons. Other
outcomes are named and enter nothing.

**Mortgage Interest and What the Loan Paid For** closed 2026-10-15 (PR #209)
for one current Form 1098 statement.

## Begin here

- [Milestone plan](phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md).
- [Tax Circumstance Breadth roadmap](phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md).
- [Personal-item sale retrospective](milestone-retrospectives/2026-10-17-personal-item-sale-circumstances.md)
  and its plan's phase assessment, for the gap and lessons.
- README, "Personal-item sale on Form 1099-K" and "Mortgage statement
  answers", for the two routes as delivered.

## Immediate next action

Begin P0 under the plan's "Actions the team will take". Write the
plain-language two-statement account and trace the cause from the code. Show
the failure with a bounded synthetic run and test the reuse candidates by
execution. Commit P0 and obtain independent review before any design is
selected.

## Parked

- Gain and break-even reporting on Form 8949 and Schedule D.
- Additional seller-paid shipping under platform pass-through.
- The adopted preferential-rate base taxes short-term covered gains at
  preferential rates. It is recorded and awaits owner disposition.
- The 22 fast-lane budget failures, and phase-state validation in
  `governance_lint`: engineering-health candidates.
- Browser observation of the mortgage and sale pages.
- Interest allocation above the debt limit, mixed-use amounts, refinancing
  and the mortgage credit, unless selected after P0.
- The configured standard deduction, which is not the verified 2025 amount.
- Use of the circumstance routes on the correction session, which still
  resolves an older registry.
- A general assumption framework, free-text intake and institutional
  verification.
