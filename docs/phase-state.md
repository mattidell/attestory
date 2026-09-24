<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "student-loan-circumstance-association",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md",
  "milestone_state": "track-4",
  "status": "G2 DESIGN REPAIRED, AWAITING OWNER APPROVALS. ADR 0075 accepted. ADR 0076 Parts 1 and 2 drafted as separate contracts with one publication plan (first successor: subject, joined, direction once both accepted; second: wording, lineNote, link_count); Part 3 open. Reader contract repaired: line 21 preserved; view on an experimental surface only (owner: B); parameter vs declared_default distinct; missing classified; statement label from entity labels; bare-statement selection needs link_count (count == 0 unsound under v10, probed). Nothing published. G2 (producer) not reached.",
  "current_role": "Foreman (awaiting owner: ADR 0076 Parts 1-2, reader contract, wording, Part 3)",
  "current_prompt": "docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association.md"
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

**Track 1 is open.** The plan's eight actions are refined and reviewed one at a
time; its state table says how far each has got. A4's second pass found that the
engine cannot publish one conclusion per key of a single subject without a
production change, and the owner chose to build that mechanism as a bounded
track. Track 1 has built it; its joins are single-hop. Track 2 tests, as a bounded
experiment, whether keys carried on same-run sources let a correction reach a
statement. The remaining probes run before any producer is considered.

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

A0 is done, including F9. A1, A2 and A3 have produced their answers; A4's bounds are
produced. **G1 has passed** at `41b77472`, after failing twice on its own conditions. A5 is
unblocked. What waits on the owner is the approval of A1's wording; the approval set
gives each fact, its answers and its effect so the wording question is answerable.
Passing G1 is not evidence that any consumer works — none has been implemented.

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
