# Charter: Repair Pass 3 — Shape-A Authority Construction Boundary

Date: 2026-07-12. Foreman-authorized after round-2 adversary review under the
owner's delegated, bounded-iteration authority.

- **Branch:** `prototypes/source-completeness/repair3`
- **Evidence level:** focused resolver/evaluator refinement over existing
  throwaway code; no production imports or edits.
- **Builder:** original it1 builder, deliberate continuity, High/high.
- **Scope:** SC-P1 shape A (dedicated reusable mapping) only. Shape B is rejected
  for rule-evolution outage. SC-P2, SC-P3, SC-D1, schemas, and persistence are
  excluded.

## Question

Can the evaluator accept completeness authority only through validated shape-A
resolution—rejecting caller-fabricated or duplicate carriers before
publication—while preserving one exact current-true closure finding per family
for explanation?

## Deliverables

Under `docs/prototypes/source-completeness/repair3/`, plus
`examination-repair3.md` (≤ 200 lines):

1. Minimal refinement of the repair1/repair2 boundary so arbitrary callers
   cannot create an evaluator-accepted resolved-authority carrier. Use a
   resolver-controlled construction path or mandatory validation with explicit
   provenance and invariants; explain what the contract guarantees rather than
   claiming language-level cryptographic unforgeability.
2. Enforce exactly one authority per family and exact correspondence among the
   mapping version, closure fact type/identity, current literal-true finding,
   and retained explanation pin.
3. Tests showing:
   - genuine shape-A resolver output publishes empty-source zero and exact pin;
   - directly fabricated authority/carrier is rejected;
   - duplicate same-family authorities are rejected, regardless of ordering;
   - stale-first/current-second cannot publish or select the stale pin;
   - false, absent, displaced, truthy, ambiguous, and bare-family cases remain
     blocked through publication;
   - present-member aggregation and computed Layer-1 zero do not consult or pin
     closure authority.
4. A constructor-bypass mutant or deliberately unsafe carrier path killed by
   fabricated/duplicate-authority cases.
5. Examination with commands/results, every negative, correspondence to the
   round-2 finding, and one final sufficiency call.

## Stop conditions

Stop after the construction/invariant question. Do not restore shape B, create
production schemas, or exercise persisted workspace behavior. A residual must
identify a production-only enforcement fact that this boundary cannot model.
