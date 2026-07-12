# Charter: Repair Pass 4 — Single Evaluation Entry

Date: 2026-07-12. Foreman-authorized after round-3 review.

- **Branch:** `prototypes/source-completeness/repair4`
- **Builder:** original it1 builder, deliberate continuity, High/high.
- **Scope:** SC-P1 shape A construction boundary only; focused throwaway
  evaluator refinement. No production, schemas, persistence, SC-P2/3/D1, or
  shape B.

## Question

Can the selected prototype surface expose one supported calculation entry that
accepts only declared mapping + findings, derives and consumes authority
internally as one operation, and offers no accepted carrier/raw-evaluator path
for fabricated, duck-typed, duplicate, or stale authority?

## Deliverables

Under `docs/prototypes/source-completeness/repair4/`, plus
`examination-repair4.md` (≤ 200 lines):

1. A self-contained selected runtime surface. Its one public calculation entry
   takes rule, source rows, adopted shape-A mapping, and closure findings; it
   resolves/validates authority internally immediately before the faithful
   two-layer check. No external authority carrier, closed-family set, raw `Env`,
   validator callback, or alternate evaluator is accepted or re-exported.
2. Unsafe carrier, caller-union, and presence-only mutants exist only inside the
   test file or test fixture—not the selected runtime module.
3. Tests for every prior value/currency/ambiguity/pin case plus:
   - duck carrier cannot be supplied because no public parameter accepts it;
   - fabricated/duplicate/stale carriers cannot enter the supported call;
   - runtime public-surface inspection finds no alternate evaluation entry;
   - present aggregation and computed Layer-1 zero omit closure pins;
   - mapping/finding inputs are the exact values used for resolution and pins.
4. Demonstrate the rejected duck and direct-raw paths as test-local mutants and
   show their divergence without exporting them.
5. Examination states the supported-surface contract, correspondence to the
   faithful two-layer behavior, commands/results, negatives, and final call.

## Stop conditions

Stop after no-bypass reachability is measured for the selected prototype
surface. Do not claim Python privacy is a security boundary; the contract is
that production exposes and dispatches only the validated entry. Any residual
must identify a production-only routing fact this prototype cannot model.
