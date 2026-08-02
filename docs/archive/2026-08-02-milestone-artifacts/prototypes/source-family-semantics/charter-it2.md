# Charter: Iteration 2 — Clean-Room Rival Source-Family Semantics

Date: 2026-07-12. Owner-approved plan; clean-room rival.

- **Branch:** `prototypes/source-family-semantics/it2`
- **Builder:** rival, High/high, owner-launched external context.
- **Evidence:** paper only. No code, resolver, production schema, UI, coverage
  store, or full interest taxonomy.
- **Questions:** SFS-P1 and SFS-P2 only.
- **Isolation:** do not read `it1/`, `examination-it1.md`, its exhibit tag,
  process log, or incumbent-derived material.

## Assignment

Independently design source-family closure semantics so the user-facing claim,
member universe, adopted mapping, calculation consumer, and coverage consumer
refer to the same universe. State the relationship among Form 1099-INT box-1
statement items, taxable-interest facts regardless of source, and Form 1040 line
2b. Do not assume they are identical without proving it through every case.

## Required cases

1. No forms and no interest.
2. Two box-1 statements from one payer.
3. Taxable interest received without Form 1099-INT.
4. One form containing box 1 and box 3 amounts.
5. A late statement discovered after closure and a prior zero.
6. A narrower family is closed while a broader taxable-interest family remains
   open.

Provide at least two positive and two negative outcomes; a closure → zero → late
discovery → withdrawal/displacement → rerun lifecycle; a claim → members →
mapping → calculation → coverage → failure map; and a direct answer whether a
closed box-1 family authorizes line-2b zero, a subtotal only, or no result. Work
one rejected alternative far enough to show its mismatch.

## Outputs and stop

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/examination-it2.md` (≤120 lines)

Report SFS-P1 and SFS-P2 separately as settled or unresolved. Stop at paper;
defer extra boxes, manual-entry product design, UI copy, Schedule B, production
ids, coverage persistence, and implementation.
