# Evaluation — QDCG Worksheet and Declared Absence (D2)

Foreman disposition record (Gate 5/7 triage), 2026-07-19. Advisory reviews
across the full arc: `reviews/governance-r1.md`, `reviews/adversary-r1.md`
(Round 1, independent seats, Medium/High), `reviews/confirmation-r1.md`
(not confirmed), `reviews/confirmation-r2.md` (confirmed). Owner decides
ratification; Tier 3 — "the outcome is the owner's actual tax number"
(`plan.md`).

## Convergence, across five documents and two owner interventions

Round 1's two sealed builders (it1 incumbent, it2 clean-room rival) settled
D2-P1 (declared-absence assertion pattern) and D2-P3 (bidirectional
admission-locus contradiction interlock) at paper rung, but neither's D2-P2
supersession/disposition posture converged: it1 demanded both declarations
unconditionally on every return (`round-1-triage.md`, decision-blocking,
conflicts with the owner's factual-completeness boundary); it2 claimed a
dynamic dual-producer selection the committed package contract does not
support. The owner authorized a bounded repair/confirmation pass, not
another rival round.

**Repair 1** converged the posture itself: one versioned successor owns
line 16, qualified-zero takes a lazy ordinary branch reading no
declarations (the reduction property), and a present `"yes"` answer yields
the committed `inapplicable`/`guard_inapplicable` disposition rather than
an invented blocked code. **Confirmation R1** passed five of six
measurements but found one decision-blocking gap (C1): the qualified-
positive, both-declarations-absent case could not name both declarations
in one non-publication walk, because the committed (pre-CMDN) evaluator
raises on the first absent reference and the guard's plain
`all([ref, ref])` short-circuits there. The owner routed the underlying
capability to a separate, narrowly-scoped topic rather than deferring or
absorbing it into D2 — that topic became **ADR-0037**
(`conditional_dependency_set`), ratified and production-hardened through
its own full review chain (Track 0a, PR #30: not-ready → repair → ready).

**Repair 2**, now that the substrate exists, substituted
`conditional_dependency_set` for the plain-`all` guard — placed first and
unconditionally so the node's own false-condition contract, not incidental
operand ordering, grounds the qualified-zero reduction, while its
accumulate-then-raise member loop produces the required two-name (or
correctly single-name) missing-declaration walk. **Confirmation R2**
independently re-verified every claim against committed HEAD source
(`evaluator.py`, `runner.py`, `explanation.py`, `package_validation.py`,
both `rule-artifact.v2`/`v3` schemas) and returned **confirmed**: all eight
measurements pass, including that D2-P1 and D2-P3 are genuinely untouched
by the guard substitution (verified by direct comparison, not asserted).

**All three propositions are now settled at Rung 1**: D2-P1 (declared
absence, presence-before-value, honest present-`"yes"` disposition), D2-P2
(single successor, qualified-zero reduction, and — the piece that took two
repair cycles — the complete two-declaration missing-walk), and D2-P3
(bidirectional admission-locus contradiction interlock, no reach-around to
box 2a or recorded-non-composable content).

## Triage

| Finding | Class | Disposition |
| --- | --- | --- |
| Round 1 G2/A2 (it2): dynamic dual-producer `conflict_semantics` selection | Decision-blocking | Rejected; single versioned successor adopted (Repair 1, carried unchanged through Repair 2). Recorded as a rejected alternative in the ADR. |
| Round 1 G3/A6 (it1): universal unconditional declaration demand | Decision-blocking | Rejected; declarations remain expression dependencies of the qualified-positive path only, never unconditional `requires`. Recorded as a rejected alternative. |
| Round 1 A1 (it1): claimed `DECLARATION_OUT_OF_SCOPE` blocked code | Decision-blocking | Rejected as a claim about HEAD; present-`"yes"` uses the committed `inapplicable`/`guard_inapplicable` disposition. A custom code remains an optional, unauthorized future production condition. |
| Confirmation R1 measurement 3 / finding C1: qualified-positive both-absent walk names only the first missing declaration | Decision-blocking | Resolved by Repair 2's `conditional_dependency_set` substitution; re-verified independently by Confirmation R2 against committed HEAD source, not the design's citations alone. |
| Repair 2 collateral finding: line-16 successor must be `rule-artifact.v3`, not `.v2` | Non-blocking correction | `conditional_dependency_set` is schema-admissible only under v3 (confirmed by direct grep of both schema files in both the foreman's and Confirmation R2's independent passes: zero occurrences in v2, one in v3). Carried into the ADR as the correct package-pin target. |
| Round 1 G4/A8: proposed new `admission-constraint.v1` citizen for D2-P3 | Production condition, deferred | Prefer the lighter existing ADR-0035-style admission-locus mechanism; a new citizen is not required unless implementation demonstrates otherwise. |
| Round 1 A3/A4/A5/A9: HEAD-vs-paper wording, evaluated-access pinning, intermediate-rule discipline, supersession/no-reach-around kill tests | Production conditions | Owed to implementation tracks: coordinator-from-facts goldens for every named case, pins sourced from evaluated access only (never a static `pins` array), no-reach-around to box 2a demonstrated structurally. |
| Round 1 A10: statutory worksheet/table fidelity | Deferred breadth | Outside this topic; synthetic `demo-*` brackets/parameters are not tax authority. Unchanged. |

## Cap state

Five documents (round 1 pair, Repair 1 pair, Confirmation R1) plus this
arc's two additions (Repair 2 pair, Confirmation R2) — no topic-level line
cap was set for this bounded repair/confirmation continuation; each
document independently held its charter's own cap (Repair 2: 179/180 and
80/80 lines; Confirmation R2: no cap specified, delivered at 52 lines).

## Outcome

D2-P1, D2-P2, and D2-P3 are settled at Rung 1 across the full round 1 →
repair 1 → confirmation 1 → repair 2 → confirmation 2 arc. Candidate
ADR-0038 is drafted from the confirmed shape (Repair 2's guard structure,
Repair 1's unchanged D2-P1/D2-P3 posture) with the production conditions
and rejected alternatives above, and proceeds to the owner's Tier 3
ratification decision. No implementation is authorized by this record —
production work is the milestone's Track 3, gated on ratification.
