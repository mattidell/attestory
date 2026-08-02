# Evaluation — Dividend Composition (D3), round 1

Foreman disposition record (Gate 5 triage), 2026-07-18. Advisory reviews:
`reviews/governance-r1.md`, `reviews/adversary-r1.md` (independent seats,
Medium tier). Owner decides ratification; Tier 2 default + veto.

## Convergence

Both builders independently chose the same fundamentals: admission-locus
structural rejection of 1b > 1a, line-level 3a ≤ 3b by construction, box 2a
recorded non-composable with a return-level signal for D2. The rival (it2)
is the converged answer: governance found it sufficient on both
propositions with zero decision-blocking findings; the adversary reproduced
its five probes and it survived all four named attacks. The incumbent (it1)
does not meet the Gate-6 floor as submitted.

## Triage

| Finding | Class | Disposition |
| --- | --- | --- |
| G1 (it1): composite 1a/1b family contradicts ADR-0016/0026 per-box closure independence | Decision-blocking (it1 only) | Round converges on it2; no repair pass was pre-authorized and none is needed (partial-ratification path). it1's composite shape recorded as a rejected alternative in the ADR. |
| Adversary named item (it1): rung-2 claim cites uncommitted `invariants` mechanism, no transcript | Decision-blocking (it1 only) | Demoted to Rung 1; subsumed by convergence on it2. The `fact-type.v2` invariants array is recorded as a rejected alternative mechanism. |
| A1/A4 (it1): no correction-path locus; 3a/3b order-dependence unaddressed | Decision-blocking (it1 only) | Same disposition as G1. |
| G2 (it1): `requires-schedule-d` signal name overclaims | Non-blocking | it2's neutral `CAPITAL_GAIN_DISTRIBUTION_RECORDED` adopted in the ADR. |
| A2 (both): composing box 2a is paper-unrepresentable but committed evaluator has no runtime guard | Hardening, named production condition | Carried into the ADR's production conditions: Track 1 package validation must reject a rule collecting recorded-non-composable content. |
| Adversary minor (it2): same-batch ordering semantics hand-waved | Hardening, named production condition | Carried: Track 2 must define and kill-test same-batch admission ordering for the paired check. |

## Cap state

Topic Markdown through committee ≈ 1,190 lines including this record,
landing at the plan's ≤ 1,200 target with nothing further authorized. Any
further round requires owner approval.

## Outcome

D3-P2 and D3-P3 settled on it2's shape (P2 at Rung 1, P3's kill-case at
Rung 2 with reproduced probes). D3-P1 remains implement-normally. Candidate
ADR-0035 drafted from it2 with the two named production conditions and the
two rejected alternatives; proceeds to the owner's veto window per Tier 2.
