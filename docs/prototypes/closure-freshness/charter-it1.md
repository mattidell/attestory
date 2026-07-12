# Charter: Iteration 1 — Incumbent Closure-Freshness Design

Date: 2026-07-12. Owner-approved Tier-3 plan.

- **Branch:** `prototypes/closure-freshness/it1`
- **Builder:** incumbent, High/high, owner-launched external context.
- **Evidence:** paper only. No reducer, schema, production runner, persistence,
  governance edit, or adopted artifact.
- **Questions:** CF-P1 and CF-P2 separately.

## Assignment

Propose one record-derived design in which a relevant later family-member act
makes prior closure authority stale and every closure-backed zero that used it
noncurrent, without manual closure withdrawal. Classify every standing effect as
an existing derivation or individuation relation. If the design needs reserved
derived-finding authority or a third edge, expose that need and fail the design.

## Required cases

1. Empty family → current true closure → closure-backed zero.
2. Later new member assertion; old closure/zero become stale/noncurrent.
3. Same member corrected; known-input subtotal displacement without unnecessary
   family reopening.
4. Member displaced/removed; no resurrection of the old zero.
5. Re-attestation after change; explicit rerun may publish successor.
6. Full rebuild from acts equals incremental currency.
7. Two families; changing one does not invalidate the other.

Provide an ordered act/state table; producer → authority → edge → currency
consumer → failure map; at least two positives/two negatives; exact pins; and a
diagram/list of every derivation and individuation edge. Work one rejected rival
far enough to demonstrate its failure.

## Outputs

- `docs/prototypes/closure-freshness/it1/design.md`
- `docs/prototypes/closure-freshness/examination-it1.md` (≤150 lines)

The examination reports CF-P1 and CF-P2 independently: settled at paper,
requires a tiny reducer, or conflicts with reserved governance.

## Stop

Stop at paper. UI, tax content, coverage display, production ids/schemas, and
workspace implementation are excluded. A reducer need is a finding, not
authorization.
