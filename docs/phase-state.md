<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-circumstance-association",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
  "milestone_state": "planned",
  "status": "Student Loan Circumstance Association remains planned -- no track is open. The plan is organised as eight actions the development team will take, refined and reviewed one at a time; the plan's own state table is the authority on progress. A0 -- model the tax concept facts the engine operates with -- was added after planning was under way and blocks most of the rest, because the plan began at what we ask a person, which presupposes a model of the facts that question connects to. A fact of the matter can be reached by more than one route and the routes are not ranked: box 1 of a Form 1098-E and an enumeration of loans and their terms both reach total deductible student loan interest, and neither is a deficient proxy for the other. Separately, some facts sit behind a fact without being on any path to it -- whether every loan is eligible bears on the deduction total without being a step toward computing it. A0 is drafted and under review. A2 is specified and survives A0 because its distinctions hold whatever route reaches a fact. A1 and A3 returned to outlined: their refinements presumed the person must supply a missing prerequisite, and box 1 is itself a route, so nothing is missing by default. A4 has partly run -- following a recorded connection works and refuses by name when the named target is gone, and the prior milestone's calculation cannot be reused inside that mechanism. No representation or mechanism is selected. This is Tax Concept Derivation: forms do not model tax concepts, a translation layer sits between ordinary circumstances and form data, and the work stays in the engine until the facts are modelled there rather than reaching toward the user first.",
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
the eight actions, or the actions refined so far.

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
