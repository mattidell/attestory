<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "multiple-statement-circumstances",
  "active_plan": "docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md",
  "milestone_state": "closed",
  "status": "Closed. A person with more than one Form 1099-K records, corrects, withdraws and removes each statement's own sale account; when every current statement is a supported personal loss, the Box 1a amounts are combined once at the top of 2025 Schedule 1, and each statement keeps its own reason, figures and saved explanation. ADR 0079 adds a recorded family-version handover. One Form 1098 remains the mortgage limit. The next milestone is unselected.",
  "current_role": "Foreman — select next milestone",
  "current_prompt": "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md"
}
-->

# Phase State

## Current result

**More Than One Statement: Keeping Each Account With Its Form is closed.**
On a synthetic account, a person can record any number of Forms 1099-K, or
that none was received, and answer the ordinary sale questions for each
statement. They can correct, withdraw or remove one statement's account
without changing another's. When the family is closed and every current
statement is a supported personal loss, the Box 1a amounts are added and
entered once at the top of 2025 Schedule 1. Income and tax do not change.
Any other reason, a blocked statement or an unclosed family blocks the entry,
and each statement's saved explanation keeps its own reason and figures.

ADR 0079 adds a recorded family-version handover. A workspace recorded on the
earlier Form 1099-K family hands over to the successor in the same save as its
next write, and completeness is asked again. One Form 1098 remains the
mortgage limit. Accounts are synthetic only.

## Inherited result

**Personal-Item Sales** closed 2026-10-17 (one Form 1099-K, one sale at a
loss). **Mortgage Interest and What the Loan Paid For** closed 2026-10-15
(one Form 1098).

## Begin here

- [Milestone plan](phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md):
  the Track 0 closure, execution record, outcome and phase assessment.
- [Retrospective](milestone-retrospectives/2026-10-19-multiple-statement-circumstances.md):
  lessons and follow-ups.
- [ADR 0079](adr/0079-family-version-handover-and-containment.md).
- [Tax Circumstance Breadth roadmap](phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md).
- README, "Personal-item sale on Form 1099-K".

## Immediate next action

Select the next milestone. The phase assessment finds the provisional endpoint
met and recommends concluding the phase. Its strongest next candidate is a
bounded engineering-health milestone: CI `verify` takes about 2.5 hours and
the full suite about 29 minutes. Gain reporting, more than one Form 1098 and
the inherited preferential-rate defect are the product candidates.

## Parked

- Gain and break-even reporting on Form 8949 and Schedule D.
- Additional seller-paid shipping under platform pass-through.
- The adopted preferential-rate base taxes short-term covered gains at
  preferential rates. It is recorded and awaits owner disposition.
- Suite and CI duration, the 22 fast-lane budget failures, and phase-state
  validation in `governance_lint`: engineering-health candidates.
- A v1 Form 1099-K workspace re-answers its completeness question under the
  successor package; recovery for a log with two current family versions; a
  full pre-save fold for every act kind.
- Browser observation of the mortgage and sale pages.
- Multiple Form 1098 support, interest allocation above the debt limit,
  second-home extension, mixed-use amounts, refinancing and the mortgage credit.
- The configured standard deduction, which is not the verified 2025 amount.
- Use of the circumstance routes on the correction session, which still
  resolves an older registry.
- A general assumption framework, free-text intake and institutional
  verification.
