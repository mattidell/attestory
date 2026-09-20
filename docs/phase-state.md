<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-circumstance-association",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
  "milestone_state": "planned",
  "status": "Student Loan Circumstance Association: PLANNED, no track open. Replace the prior experiment's stipulated statement-to-loan-and-period relationship with a bounded recorded ordinary-fact path and a tested consumer. Organised as eight actions the development team will take, refined and reviewed one at a time; progress reads on two axes -- the state table for how specific each action is, and three readiness gates for whether dependent work may begin, the gate governing where they could disagree. A0 (model the tax concept facts) is done and reviewed; A1, A2 and A3 are specified; A4's refinement is drafted and repaired after review; A5, A6 and A7 are stated only. Load-bearing findings: a fact of the matter can be reached by more than one route and routes are not ranked (box 1 and an enumeration of loans both reach total deductible student loan interest); 'on the path' and 'sits behind' are relative to a route and not mutually exclusive (filing status is both -- it gates the MFS exclusion and keys the threshold and phase-range parameters); representing a fact does not make it mandatory, since obligation comes from a named consumer's declaration, so the question is which consumer needs the information and what it does when absent; member identity is not lost by an aggregate Boolean, because witness facts are keyed lender + statement + tax-year and the runner pins every collected finding, so what is limited is what an expression can branch on; and the pairing-scope observation bounds the one environment tested -- a shape rebuilt in a test module mirroring a nominee-specific adapter -- not the dispatcher, leaving the mechanism choice open. No representation, mechanism or contract is selected. This is Tax Concept Derivation: forms do not model tax concepts, a translation layer sits between ordinary circumstances and form data, and the work stays in the engine until the facts are modelled there.",
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

A0 is done and reviewed. A1, A2 and A3 are specified. A4's refinement is drafted
and repaired after review, and is the last thing G1 waits on.

Four premises were corrected after review and matter to whoever picks this up:
"on the path" and "sits behind" are relative to a route and not mutually
exclusive; representing a fact does not make it mandatory, because obligation
comes from a named consumer's declaration; an aggregate Boolean does not erase
member identity, which the keyed witness facts and the runner's pinning preserve;
and the pairing-scope observation bounds the one environment tested rather than
the dispatcher.

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
