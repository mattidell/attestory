# Charter: Iteration 1 — Incumbent Source-Family Semantics

Date: 2026-07-12. Plan approved by owner.

- **Branch:** `prototypes/source-family-semantics/it1`
- **Builder:** incumbent, High/high, owner-launched external context.
- **Evidence:** paper examples only. No resolver, evaluator, production schema,
  UI, coverage store, or full interest taxonomy.
- **Questions:** SFS-P1 and SFS-P2 only.

## Assignment

Propose one coherent design in which the closure claim, member universe,
adopted mapping, calculation consumer, and coverage consumer all refer to the
same declared universe. Explicitly distinguish, or prove coextensive:

- Form 1099-INT box-1 statement items;
- taxable-interest facts regardless of document source;
- the broader Form 1040 line-2b result.

Do not use “all my interest income” unless the design actually covers that full
universe.

## Required cases

1. No forms and no interest.
2. Two box-1 statements from one payer.
3. Taxable interest received without Form 1099-INT.
4. One form containing box 1 and box 3 amounts.
5. A late statement discovered after closure and a prior zero.
6. The narrow document family is closed while the broader taxable-interest
   family remains open.

For the proposed design provide:

- at least two positive and two negative outcomes;
- a closure assertion → zero → late discovery → withdrawal/displacement → rerun
  lifecycle;
- a claim → member universe → mapping → calculation → coverage → failure map;
- an explicit answer for whether a closed box-1 family may directly authorize
  line 2b zero, a subtotal zero only, or no tax result;
- one rejected rival shape worked far enough to demonstrate its mismatch.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/examination-it1.md` (≤120 lines)

The examination states SFS-P1 and SFS-P2 separately as settled at paper or
unresolved, cites every case, and names any question that would require a tiny
resolver table.

## Stop conditions

Stop at paper. Extra interest boxes, manual-entry product design, UI copy,
Schedule B, production ids, and coverage persistence are deferred rather than
absorbed.
