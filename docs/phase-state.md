<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-circumstance-association",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
  "milestone_state": "planned",
  "status": "Student Loan Circumstance Association remains planned -- no track is open. Work sequence item 1, the product and evidence outline, is complete and independently reviewed with no material findings. Recording, recovery, confirmed association and lifecycle have adopted production precedent on the structurally identical Form 1099-INT aggregation problem. Following an asserted relationship is possible only through ADR-0070/0071 pairing dispatch, outside the evaluator; the prior milestone's bounded consumer cannot be lifted into that scope unchanged and must be restructured without its cardinality gate. Iteration completeness -- a statement with no relationship is never visited -- has no adopted precedent and is now Track 0's gate. The plan is organised as seven actions the development team will take, refined and reviewed one at a time; the plan's state table is the authority on progress. A0 was added after planning was under way and blocks most of the rest: the plan began at what we ask a person, which presupposes a model of the tax concept facts that question would connect to. A0 models those facts -- which facts of the matter exist, at which stage, which routes reach each, and what each route does and does not establish. Box 1 and an enumeration of loans are both routes to total deductible student loan interest, neither a proxy for the other; loan eligibility sits behind that fact rather than on the path to it. A0 is drafted and under review. A1 and A3 returned to outlined because their refinements presumed a prerequisite that does not exist. A2 survives. This is Tax Concept Derivation: the work stays in the engine until the facts are modelled there and does not reach toward the user before that.",
  "current_role": "Foreman (refine the plan one action at a time; A0 added and drafted, blocks A1/A3/A5)",
  "current_prompt": "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md#A0 in detail — modelling the tax concept facts"
}
-->

# Phase State

## Current work

**Tax Concept Derivation is active.** The selected milestone is
**Student Loan Circumstance Association**, on
`milestone/student-loan-circumstance-association` in `engine-worktree-1`.

The previous experiment demonstrated a bounded translation from an ordinary
schooling circumstance to a tax consequence. It supplied the connection to
reported interest itself. This milestone obtains and records that connection,
keeps its subjects distinct, and lets a consumer use recovered current support.

**The plan is developed one action at a time.** It describes seven things the
development team will do, in ordinary language, and is refined one action per
round with an independent review of each refinement before the next. The plan's
own state table says how far along each action is; nothing counts as specified
because related technical work succeeded.

## Begin here

Read the [milestone plan](phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md),
then the [product and evidence outline](phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/outline-product-and-evidence.md)
it now leads with. Everything the outline says about existing software is
evidence level `read`.

Read the plan at whichever of its three levels you need: the opening paragraph,
the seven actions, or the one action refined so far.

The plan now opens with **A0 — model the tax concept facts the engine operates
with**, added after planning was under way and kept at the front so the change
stays visible. Nothing downstream can be settled first: the translation layer
between a person's ordinary circumstances and form data cannot be defined until
the facts it translates into are modelled.

A0 is drafted and under review. A2 — when an answer can still be relied on —
remains specified. A1 and A3 returned to `outlined`: both refinements presumed
the person must supply a missing prerequisite, and box 1 is itself a route to the
deduction total, so nothing is missing by default.

A2 established one thing worth carrying: what a person would now say is never
observable, so it produces an obligation to ask rather than a determination, and
a claim must never stand merely because nobody said otherwise. A4 has partly run and its results are recorded as bounds on
the other actions, with their ceilings, in the
[readiness-gate results](phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/readiness-gate-results.md).

The plan's open-decisions table names which choices are the owner's. Two are:
whether one undescribed statement should block the others, and whether honest
refusal is adequate for the two multi-borrowing cases.

The intended result is adopted recording and recovery with an executed bounded
consumer. Full worksheet integration, favorable eligibility, and a deep user
journey remain outside this milestone. No new general evaluation framework or
institutional catalog is presumed necessary.

## Context

- [Phase purpose](phases/tax-concept-derivation/tax-concept-derivation-overview.md)
  and [roadmap](phases/tax-concept-derivation/tax-concept-derivation-roadmap.md).
- [Previous milestone retrospective](milestone-retrospectives/2026-09-15-student-loan-interest-bounded-method-transfer.md).
- [Relationship and other deferrals](phases/tax-concept-derivation/milestones/student-loan-interest-bounded-method-transfer-evidence/track-0-adversarial-closure.md#55-deferral-ledger).
- [Owner Model](../OWNER_MODEL.md).

No implementation unit is currently dispatched. The milestone plan is the
current source for scope and the next action.
