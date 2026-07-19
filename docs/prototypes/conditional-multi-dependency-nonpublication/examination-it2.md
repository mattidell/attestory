# Examination: Iteration 2 — Conditional Multi-Dependency Non-Publication

Status: **Rung-1 paper only (clean-room rival)**

## CMDN-P1 — Settled at Rung 1

An active declared condition jointly requires a declared set of factual
dependencies and names every absent member in the non-publication disposition.

The `conditional_requires` block declares a condition expression and a finite
member array. When the condition is truthy, all members are checked (no
short-circuit); absent members appear in `missing` under
`CONDITIONAL_DEPENDENCY_ABSENT`. The NPE walk reads `code` and `missing`
from the ledger and surfaces them as `unmet_references` — existing walker
path, no code change.

**Rung-1 sufficiency.** Cases 1–6 demonstrate correct missing-member sets
for every combination. The mechanism is a declared existence check over a
declared array — the same class as the committed `requires` gate.

**Production conditions.** New rule-artifact schema version
(`conditional_requires` field); new record-schema blocking code; runner
pre-guard step.

## CMDN-P2 — Settled at Rung 1

Conditional dependency sets and their missing-member reporting are declared
artifact semantics, not runner policy.

`conditional_requires` is schema-validated artifact content. The member set
is a JSON array of symbol names. The condition is an expression in the closed
evaluator vocabulary. No runner-internal table, UI, form definition, or
post-processing list supplies the member set. Case 6 demonstrates no
alternative pathway. Art. 11, E11.2, E11.3 conformance follows from the
mechanism being artifact-declared and expression-evaluated.

**Production conditions.** Same schema version as P1.

## CMDN-P3 — Settled at Rung 1

Currency/pinning uses the existing two-edge model without a third edge and
without demanding dependencies while the condition is inactive.

When inactive, members are not checked and no ref enters the AccessLog — no
derivation edge exists. Superseding an unread member has no currency effect
(Art. 7, E7.2). When active and published, `value` reads members via `ref`,
pins carry derivation edges, and displacement propagates through the existing
closure. The condition's truth is a pinned ref; a change from false to true
displaces the prior finding along its derivation edge. Contribution of a
missing member is a fresh re-run, not a currency event.

Case 5 walks eight states using only the two committed edge kinds.

**Production conditions.** None beyond P1. Currency and projection unchanged.

## Summary

| Proposition | Status | Rung | Unresolved |
|---|---|---|---|
| CMDN-P1 | Settled | 1 | None |
| CMDN-P2 | Settled | 1 | None |
| CMDN-P3 | Settled | 1 | None |

Three production conditions: schema version, blocking code, runner step.
No existing surface requires behavioral change.
