<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "personal-item-sale-circumstances",
  "active_plan": "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md",
  "milestone_state": "planned",
  "status": "Opening plan for personal-item sales reported on Form 1099-K. P0 must establish the ordinary account, exact 2025 treatment and actual return-integration cost before selecting a design. No implementation has begun.",
  "current_role": "Foreman — refine P0 and charter the initial investigation",
  "current_prompt": "docs/phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md"
}
-->

# Phase State

## Current direction

The next milestone is Personal-Item Sales: What Was Sold and What the Payment
Means. A person has a Form 1099-K and an account of a sale. The application
must connect those without treating reported money as taxable profit by
default or asking the person for a tax conclusion.

Start with one identifiable sale of a purchased, personally used item and one
statement. Investigate both a gain and a personal loss, their reporting paths,
and what ordinary information establishes them. No representation, default
policy, schema or production track is selected yet. The first task is P0:
develop and independently review the concrete account and integration cost.
Keep planning incremental; the active plan lists the team's actions rather
than predicting an implementation before the investigation.

## Inherited result

**Mortgage Interest and What the Loan Paid For is closed.** On a synthetic
account, a person can review one current Form 1098 statement, record
ordinary answers about that home borrowing, and correct them. The
application calculates the bounded interest treatment and saves an
explanation of the answer and the basis it used.

Qualified interest can reach Schedule A. A justified zero publishes zero.
Uncertainty about liability, a mortgage credit certificate, or whether the
loan is the original loan is named, and the amount stays blocked. Known
unsupported cases are named the same way. An over-limit principal blocks.
The explanation says that older debt may have a higher limit.

The adopted line 8a rule that ignored box 2 is repaired on the earlier
confirmation route. The circumstance route reads box 2 directly. ADR 0078
supplies the fixed-date comparison the grandfathering check uses.

There is no browser observation of the page. The route is one statement.
Accounts are synthetic only.

## Begin here

- [Current milestone plan](phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md).
- [Tax Circumstance Breadth roadmap](phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md).
- [Mortgage retrospective](milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md):
  the targeted lessons for this opening investigation.
- [Previous milestone result](phases/tax-circumstance-breadth/milestones/mortgage-interest-circumstances.md)
  and README, "Mortgage statement answers", when inspecting concrete reuse.

## Immediate next action

Read the [opening plan](phases/tax-circumstance-breadth/milestones/personal-item-sale-circumstances.md),
refine P0 and charter the bounded investigation. Review P0 before selecting
the connected design. No production implementation is authorized by this
opening plan. Reassess cost and scope if reporting integration would require
a broad new accounting or capital-asset framework.

The phase stays open. Mortgage is its first additional tax context; this
milestone attempts the contrasting context beyond borrowing. After delivery,
assess the provisional phase endpoint rather than automatically adding work.

## Parked

- Browser observation of the mortgage page.
- Interest allocation, mixed-use amounts, multiple statements, refinancing,
  and the mortgage credit.
- The configured standard deduction, which is not the verified 2025 amount.
- Use of this route on the correction session, which still resolves an
  older registry.
- A general assumption framework, free-text intake, and institutional
  verification.
