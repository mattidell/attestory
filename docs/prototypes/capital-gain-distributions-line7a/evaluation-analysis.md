# Evaluation — Capital-Gain Distributions to Form 1040 Line 7a

Foreman disposition record for contract synthesis (Track 0 Gate-7 boundary),
2026-07-28. Advisory reviews and confirmations across the arc:
`reviews/contract-adversary.md`, `reviews/expressiveness.md`,
`reviews/repair1-confirmation.md` (`NOT READY`),
`reviews/repair2-confirmation.md` (`READY`). Owner topology selection:
`round-1-triage.md`. Selected surface: `final-disposition.md`. Controlling
composite paper: `it2/design.md` as amended by `repair2/design.md`. Candidate
ADR: `docs/adr/0050-capital-gain-distributions-and-line-7a.md` (**proposed**,
inert). Production remains blocked.

## Convergence

| Proposition | Status | Controlling evidence |
| --- | --- | --- |
| P1 — direct-route authority | Settled at Rung 1 after Repair 2 | Owner selected component-backed topology (`round-1-triage.md`). T-F1 completeness (four Exception-1 components including boxes 2b/2c/2d absence) confirmed in `reviews/repair2-confirmation.md` F1/T-F1 against `repair2/design.md` §§2–6. |
| P2 — box-2a family promotion | Settled at Rung 1 (retained) | `it2/design.md` P2 successor member/family/horizon/closure, non-null signal, historical/successor exclusivity; regression boundary intact at final confirmation (`reviews/repair2-confirmation.md` §Regression). |
| P3 — line-7a and QDCG handoff | Settled at Rung 1 after Repair 2 | T-F2 QDCG selection/binding confirmed (`reviews/repair2-confirmation.md` F3/F4/T-F2) against `repair2/design.md` §7; Case 10 ordinary-only path retired. |

Two repair cycles were required after owner selection: Repair 1 failed focused
confirmation (hollow pins/lifecycle and live Case-10 contradiction;
`repair1-confirmation-disposition.md`). The owner authorized one final Rung-1
repair limited to F1–F4. Repair 2 reconciled the composite paper; final
confirmation returned **READY** on F1–F4, T-F1/T-F2, and the retained
regression boundary.

## Clause-to-evidence map (adopted ADR-0050 decisions)

| ADR-0050 clause | Adopted content | Evidence chain |
| --- | --- | --- |
| D1 Four components + checked conclusion | C1–C4 categorical `{yes,no}`; E; conclusion `"no"` only under E-yes; missing → blocked; any `"no"` → conclusion `"yes"` / guard-inapplicable; C4 not a source family | `final-disposition.md`; `repair2/design.md` §§2–3; confirmation F1/T-F1; `round-1-triage.md` T-F1 |
| D2 Box-2a successor family | Member-only composable path; family/horizon/closure; multi-payer sum; closed-empty 0; correction/removal; non-null signal | `it2/design.md` P2; confirmation regression §; `final-disposition.md` |
| D3 Exclusivity + universe successor | `dividend-universe` successor; historical recorded-boxes immutable; reject mixed graphs; no published-history rewrite | `it2/design.md` P2 sentences 3–4; confirmation regression (exclusivity) |
| D4 Contradiction interlock | `"no"` declaration vs signal; both orders + same batch; successor signal feed | `it2/design.md` P2 sentence 5; ADR-0038 decision 5 consumed; confirmation §8.2 |
| D5 Line 7a / 7b dispositions | Distinct fields; blocked vs guard-inapplicable vs zero vs positive | `repair2/design.md` §§3.1, 4–5 (R2-E/M/N); confirmation F1 disposition table |
| D6 Line 9 once + displacement chain | Line-9 successor adds selected line 7a once; cascade via ADR-0010 | `it2/design.md` P3; `repair2/design.md` §§4.2, 6 (R2-L); confirmation F2 |
| D7 Line-16 partition + QDCG | Typed match on line-7a disposition; QDCG if Q>0 or L>0; ordinary only both closure-backed zero; worksheet line 3 = line 7a; no raw/assumed zero | `repair2/design.md` §7; confirmation F3/F4/T-F2; `round-1-triage.md` T-F2 |
| D8 Pins / citations / kill tests | Full pin sets; production kill-test inventory | `repair2/design.md` §§4–8; confirmation F1–F4; plan Gate-7 production boundary |
| D9 Relation to ADR-0035 / 0038 | Accepted history immutable; named successor-graph supersessions only | Charter assignment item 9; `it2/design.md` immutability; repair2 §1 ledger + §8 |

## Rejected alternatives

| Alternative | Why rejected | Evidence |
| --- | --- | --- |
| Conclusion-level sole `schedule-d-required` authority (it1) | Owner selected explicit, correctable Exception-1 components over thinner owner-honest conclusion | `round-1-triage.md` Owner disposition; `it1/design.md` topology; CA-F04 / EXP-001 cost contrast |
| Repair 1 composite as-shipped | Incomplete eligible pins/lifecycle; Case 10 still ordinary-only for Q=0/L>0; three-component leftovers live | `reviews/repair1-confirmation.md`; `repair1-confirmation-disposition.md` |
| Assumed zero / inferred eligibility | Violates factual completeness and Exception-1 honesty | Plan non-goals; confirmation §7.1 / §8.5; ADR-0011 precedent |
| Raw box-2a or historical recorded-boxes into line 9 / QDCG | Double-count and reach-around | `it2/design.md` P3 sentence 6 / Cases 8–9; confirmation §8.4 |
| Fabricating Schedule D when conclusion is `"yes"` | Milestone non-goal; honest inapplicability only | Plan non-goals; R2-N; confirmation F1 |

## Accepted topology costs and production conditions

| Item | Class | Carry-forward |
| --- | --- | --- |
| CA-F01 — extra displacement hop through checked conclusion | Accepted topology cost | Production correction-chain tests through conclusion → 7a → 9 → TI → 16 (`reviews/contract-adversary.md`) |
| CA-F07 — C1 couples authority to future capital-gain sources | Accepted topology cost | Future-version / future-source maintenance tests when new gain families appear |
| EXP-002 — additional contribution surface (+4 categorical facts after Repair 2) | Production condition | Explicit missing-component explanations and contribution UX/tests (`reviews/expressiveness.md`; `repair2/design.md` §3.3) |
| Mixed-graph mechanical rejection | Production kill test | Package validation; not a prototype Rung-2 climb (`round-1-triage.md` contract-review note; `it2/design.md` P2) |
| Contradiction both orders + batch | Production kill test | Successor signal feed (`it2/design.md` P2; ADR-0038 pattern) |
| QDCG partition rows (blocked / inapplicable / Q=0 L>0 / Q>0 L=0 / both zero) | Production goldens | `repair2/design.md` §7; confirmation F4 |
| Pin and citation completeness on every publication | Production condition | Decision 8; confirmation cases R2-E / R2-L / R2-Q* |

## Non-blocking observations (final confirmation)

| Id | Observation | Disposition |
| --- | --- | --- |
| N1 | Pin formality variance across QDCG case rows (alias table vs prose constituents) | Recorded in ADR-0050; not decision-blocking at Rung 1 (`reviews/repair2-confirmation.md`) |
| N2 | Line 9 surfaces as blocked when line 7a is guard-inapplicable | Recorded in ADR-0050; production may refine inapplicable-upstream presentation without coercing zero |

## Cap and process notes

- Prototype repair cap was amended once by the owner after Repair 1 `NOT READY`
  (`repair1-confirmation-disposition.md`); Repair 2 was final.
- Process incident (Repair 1 hollow measurement) is logged in `process-log.md`
  and does not reopen topology selection.
- Committee Case-10 ordinary-tax acceptance in round-1 reviews was a
  process-conformance incident (`round-1-triage.md`); focused confirmation
  against official-instruction binding, not those broad READY verdicts, settled
  T-F2.

## Outcome

P1, P2, and the coherent direct-route portion of P3 are settled at Rung 1 on
the component-backed successor shape. Proposed ADR-0050 and this analysis are
the Track 0 contract-synthesis unit. They authorize neither production
implementation, ADR ratification, merge, nor pointer advance. Next step is
author-independent ADR review under a separate charter, then owner ratification.
