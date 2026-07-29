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

## ADR-0050 repair disposition

| Finding | Status | Closed contract point |
| --- | --- | --- |
| F1 | **CLOSED** | `guard_inapplicable` line 7a fixes line 9 as `blocked(DEPENDENCY_ABSENT)` on selected line 7a and blocks taxable income through line 9; missing-authority blocking and closure-backed zero remain distinct. |
| F2 | **CLOSED** (Repair 2 drafting) | Four explicit Q/L declaration/conclusion pin sets: Q>0/L=0 pins declaration `"no"` + conclusion `"no"`; Q=0/L>0 pins conclusion `"no"` only; Q>0/L>0 pins declaration `"yes"` + conclusion `"no"`; Q=0/L=0 ordinary pins **neither** (R2-Q3). ADR-0038's declaration-free qualified-zero reduction remains declaration/conclusion-free when selected line 7a is also closure-backed zero. |
| F3 | **CLOSED** (Repair 2 drafting) | Direct pins hop by hop; line-16 both-zero set reproduces R2-Q3 exactly; transitive lineage is not restated as direct pins. |
| F4 | **CLOSED** | Line 7b pins the exact 2025 Instructions for Form 1040, Line 7b paragraph beginning “If Exception 1 applies, check the ‘Schedule D not required’ box on line 7b.” |
| F5 | **CLOSED** | ADR-0050 Links and this analysis name `exhibits/capital-gain-distributions-line7a/it1` and `exhibits/capital-gain-distributions-line7a/it2`; status remains proposed/inert. |

| Milestone Contracts 7–8 / history | Status | Result |
| --- | --- | --- |
| Contract 7 — Tax | **CLOSED** by Repair 2 drafting | One evidence-backed declaration/conclusion pin set per Q/L branch, including both-zero ordinary (R2-Q3). |
| Contract 8 — Citation and presentation | **CLOSED** by Repair 2 drafting | Line-7b citation closed earlier; line-16 branch-specific direct-input contract now matches R2-Q1–Q3. |
| History compatibility (ADR-0038 Q-zero) | **CLOSED** by Repair 2 drafting | Both-zero ordinary remains declaration/conclusion-free; other three branch contracts unchanged. |

## Clause-to-evidence map (adopted ADR-0050 decisions)

| ADR-0050 clause | Adopted content | Evidence chain |
| --- | --- | --- |
| D1 Four components + checked conclusion | C1–C4 categorical `{yes,no}`; E; conclusion `"no"` only under E-yes; missing → blocked; any `"no"` → conclusion `"yes"` / guard-inapplicable; C4 not a source family | `final-disposition.md`; `repair2/design.md` §§2–3; confirmation F1/T-F1; `round-1-triage.md` T-F1 |
| D2 Box-2a successor family | Member-only composable path; family/horizon/closure; multi-payer sum; closed-empty 0; correction/removal; non-null signal | `it2/design.md` P2; confirmation regression §; `final-disposition.md` |
| D3 Exclusivity + universe successor | `dividend-universe` successor; historical recorded-boxes immutable; reject mixed graphs; no published-history rewrite | `it2/design.md` P2 sentences 3–4; confirmation regression (exclusivity) |
| D4 Contradiction interlock | `"no"` declaration vs signal; both orders + same batch; successor signal feed | `it2/design.md` P2 sentence 5; ADR-0038 decision 5 consumed; confirmation §8.2 |
| D5 Line 7a / 7b dispositions | Distinct fields; blocked vs guard-inapplicable vs zero vs positive | `repair2/design.md` §§3.1, 4–5 (R2-E/M/N); confirmation F1 disposition table |
| D6 Line 9 once + displacement chain | Line-9 successor adds selected line 7a once; `guard_inapplicable` line 7a blocks line 9 and taxable income through line 9; cascade via ADR-0010 | `it2/design.md` P3; `repair2/design.md` §§4.2, 5 (R2-N), 6 (R2-L); confirmation F2 and N2 |
| D7 Line-16 partition + QDCG | Typed match on line-7a disposition; QDCG if Q>0 or L>0; ordinary only both closure-backed zero; worksheet line 3 = line 7a; four branch pin sets (Q>0/L=0: decl `"no"`+concl `"no"`; Q=0/L>0: concl `"no"` only; Q>0/L>0: decl `"yes"`+concl `"no"`; Q=0/L=0: neither); no raw/assumed zero | `repair2/design.md` §7 R2-Q1–Q3; confirmation F3/F4/T-F2; `reviews/adr0050-contract-recheck.md` R1 residual; `adr0050-recheck-disposition.md` |
| D8 Pins / citations / kill tests | Direct hop-by-hop pin graph; line-16 both-zero direct set = R2-Q3 (no declaration/conclusion); exact line-7b citation; production kill-test inventory | `repair2/design.md` §§4.2, 6–8 and R2-Q3; confirmation F1–F4; 2025 Form 1040 instructions, Line 7b; plan Gate-7 production boundary |
| D9 Relation to ADR-0035 / 0038 | Accepted history immutable; C1–C4 + checked conclusion replace only successor direct-route Schedule-D-required authority; qualified-positive branches retain `capital-gain-distributions`; ADR-0038 declaration-free Q-zero reduction remains free when L is also closure-backed zero | `docs/adr/0038-qdcg-worksheet-and-declared-absence.md` decisions 1–3; `repair2/design.md` R2-Q3; `it2/design.md` P3 sentence 4; repair2 §1 ledger + §7 |

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
| N2 | Line 9 surfaces as blocked when line 7a is guard-inapplicable | Closed by the repair: ADR-0050 adopts `blocked(DEPENDENCY_ABSENT)` on selected line 7a for line 9 and blocks taxable income through line 9; no alternate downstream disposition or zero coercion |

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
the component-backed successor shape. First-review findings F1–F5 and recheck
residual R1 (both-zero direct pins) are closed in proposed ADR-0050 and this
analysis by reproducing R2-Q3's declaration/conclusion-free ordinary set and
stating all four Q/L branch pin sets. The evidence ceiling remains Rung 1
committed synthetic paper evidence. They authorize neither production
implementation, ADR ratification, merge, nor pointer advance. The next
process step is the separately chartered final recheck, not an advance of this
proposed/inert contract.

## Stable evidence refs

- `exhibits/capital-gain-distributions-line7a/it1`
- `exhibits/capital-gain-distributions-line7a/it2`
