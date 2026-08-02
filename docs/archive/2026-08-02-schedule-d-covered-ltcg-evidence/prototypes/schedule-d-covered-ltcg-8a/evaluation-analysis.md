# Evaluation Analysis — Covered Long-Term Gains, Schedule D Line 8a

Audience: prototype committee, owner, and the reader of proposed ADR-0052.
Evidence ceiling: Rung 1, static paper only, throughout the cited chain.

This analysis exists because the topic did not converge in one clean round
(`PROJECT_PLANNING.md`, "Prototype-Driven Decisions"): two Builder iterations
ran (incumbent and rival), the rival changed the shape of P2's and P3's
answers rather than merely confirming the incumbent, and one decision-blocking
dissent (CA-04) was open after the first committee round and required a
repair pass before close. It routes every ADR-0052 clause to its exhibit; it
does not retell every worked case, which remain in the cited files.

## 1. Round summary

| Round | Object | Result |
| --- | --- | --- |
| Charter | `plan.md` | P1/P2/P3 scored (Gate 1: P1=6, P2=6, P3=5); rung 1 authorized; eleven shared cases fixed. |
| it1 (incumbent) | `it1/design.md`, `it1/examination.md` | Nested-member identity + synthesized checked conclusion. Self-reported "settled" for P1/P2, "partially settled" for P3. |
| it2 (rival) | `it2/design.md`, `it2/examination.md` | Independent anchor-keyed family + direct multi-read completeness + shared `selected-preferential-base` `P`. Self-reported "settled" for P1/P2/P3. |
| Round 1 committee | `reviews/contract-adversary.md` (NOT READY), `reviews/expressiveness.md` (READY for rival) | Independent reviews converge on rejecting the incumbent and preferring the rival, with one shared corroborated defect (incumbent drops box-2a gain in case 6) and one unresolved rival dissent (CA-04). |
| Triage | `round-1-triage.md` | Owner disposition: rival topology selected, incumbent not carried forward; CA-02/P2-S5A adopted; CA-04 repair authorized (the plan's single fixed repair pass). |
| repair1 | `repair1/design.md`, `repair1/examination.md` | P2-S5A (box-2a must be closed, not closed-empty) and P3-S8 (exact `P` pin-signature contract) supplied as amendments to `it2/design.md`. |
| Confirmation | `reviews/repair1-confirmation.md` | CA-02: CONFIRMED. CA-04: CONFIRMED. Regression boundary intact. Overall verdict: **READY**. |

The composite controlling paper for ADR-0052 is `it2/design.md` as amended by
`repair1/design.md` — the same evidentiary structure ADR-0050 itself used for
its own `it2`-plus-`repair2` composite.

## 2. Clause-to-evidence routing

| ADR-0052 decision | Adopted from | Exact citation |
| --- | --- | --- |
| Decision 1 (P1 transaction source family and identity) | `it2/design.md` §3, unchanged by repair1 | P1-S1 through P1-S7 (§3.2); positives (§3.3, shared cases 1–3); negatives (§3.4, shared cases 4, 11); lifecycle (§3.5, shared case 8); producer/authority/consumer/failure map (§3.6) |
| Decision 2 (P2 nine-part completeness boundary, adopted P2-S5A) | `it2/design.md` §4 for P2-S1 through P2-S4 and P2-S6 through P2-S8; `repair1/design.md` §1 for P2-S5A | P2-S1–P2-S8 (`it2/design.md` §4.2); adopted replacement P2-S5A (`repair1/design.md` §1); positives (`it2/design.md` §4.3, shared cases 1, 6, rechecked in `repair1/design.md` §3.2–3.3); negatives (`it2/design.md` §4.4, shared case 5, all nine variants; §4.4, shared case 9) |
| Decision 3 (Schedule D content as an ADR-0036 instantiation; CA-05 named, not resolved) | `it2/design.md` §5.2 (P3-S1–S3), unchanged by repair1 | P3-S1–S3 (`it2/design.md` §5.2); CA-05 finding (`reviews/contract-adversary.md`, "CA-05"); triage disposition (`round-1-triage.md`, finding table, CA-05 row) |
| Decision 4 (shared `P` symbol, P3-S4/S7 topology, exact P3-S8 pin contract; CA-06 named, not resolved) | `it2/design.md` §5.3 (P3-S4, P3-S7), unchanged by repair1; `repair1/design.md` §2 for P3-S8 | P3-S4, P3-S7 (`it2/design.md` §5.3); exact pin signatures and P3-S8 (`repair1/design.md` §2.1–2.2); four-row ADR-0050 Decision 7 rewrite in terms of `P` (`repair1/design.md` §2.3); atomic outcome ledger (`repair1/design.md` §2.4); worked cases (`repair1/design.md` §3.1–3.3); forward/reverse correction traces (`repair1/design.md` §4.1–4.2); CA-06 finding (`reviews/contract-adversary.md`, "CA-06"); confirmation of the no-route-tag claim (`reviews/repair1-confirmation.md`, "CA-04: CONFIRMED", "Independent assessment of the no-route-tag claim") |
| Decision 5 (line 7a, 7b, line 9) | `it2/design.md` §5.3 (P3-S5), §5.4 (Decision 5/6 ledger rows) | P3-S5 (`it2/design.md` §5.3); ledger rows for ADR-0050 Decisions 5 and 6 (`it2/design.md` §5.4); worked cases (`it2/design.md` §5.5–5.6; `repair1/design.md` §3.1–3.3) |
| Decision 6 (relationship to ADR-0036 and ADR-0050) | `it2/design.md` §5.1 (accepted contracts consumed unchanged), §5.4 (exact supersession ledger); `repair1/design.md` §2.3 (Decision 7 rewritten in terms of `P`) | `it2/design.md` §5.4 ledger; `repair1/design.md` §2.2–2.3 (P3-S8 and the four-row rewrite, replacing only the pin-location part of P3-S6 and the corresponding ledger row) |
| Decision 7 (pins, citations, presentation, kill tests) | `it2/design.md` §2.3–2.4 (official grounding, publications/pin sets), §6 (shared case ledger); `repair1/design.md` §2.4 (atomic outcome and pin ledger) | Citation grounding (`it2/design.md` §2.4); pin sets (`it2/design.md` §2.3); shared case ledger recovering all eleven cases from one place (`it2/design.md` §6); kill-test sources (`it2/design.md` §3.7, §4.7, §5.10) |
| Rejected incumbent (Alternatives Considered) | `it1/design.md`, `it1/examination.md` | CA-01 (P1 admits too-broad source class), CA-03 (P3 omits QDCG `Q` input and full correction chain), corroborated box-2a data-loss defect in shared case 6 (`reviews/contract-adversary.md`, "CA-02"; `reviews/expressiveness.md`, §2 "Shared Case 6", §3.1) |

## 3. Recorded dissent and its resolution

**CA-04** (`reviews/contract-adversary.md`, "CA-04 — Rival P3 hides route-sensitive
ADR-0050 pins behind a supposedly route-neutral `P`") is the one recorded
review dissent. The contract/adversary review classified it `decision-blocking`:
the rival's route-neutral symbol `P` was asserted to carry ADR-0050's
route-specific direct declaration/conclusion pins with no stated pin-location
rule, and the rival case-6 worked example (C1 `"no"`, checked conclusion
`"yes"`) showed the pin set must differ by producer without the design saying
how. The expressiveness review reached `READY` without identifying this gap —
`round-1-triage.md` records this explicitly as a genuine measurement-scope
difference between the two review charters, not a disagreement, per
`PROJECT_PLANNING.md`'s instruction that dissent is recorded, not resolved by
wordsmithing.

The owner authorized the plan's single fixed repair pass, scoped to CA-04
(plus restating P2-S5 as an explicit adopted sentence, CA-02).
`repair1/design.md` §2 supplies the exact successor sentence, P3-S8, and the
four-row rewrite of ADR-0050 Decision 7 in terms of `P`, showing that the two
producer signatures (`P-direct`, `P-schedule-d`) pin disjoint authority sets
and are therefore mechanically distinguishable from `P`'s own direct-pin
lineage without a route tag. `reviews/repair1-confirmation.md` independently
re-verified every CA-04 clause against the artifact text itself (not the
examination's self-report), confirmed no accepted Decision 7 pin moved, no new
direct line-16 pin was created beyond the `selected_line7a -> P` substitution,
and returned overall verdict **READY**. CA-04 is resolved as of that
confirmation.

## 4. Production conditions carried forward (owed, not resolved by ADR-0052)

- **CA-05.** `attachment-rule.v2`'s `requirement` block is structurally
  threshold-only (`subtotals`/`threshold_parameter`/
  `comparison: strictly_greater_than`, all required —
  `packages/schemas/tax/attachment-rule.v2.schema.json`; ADR-0036 Decision 2).
  Schedule D's required/not-required disposition is categorical, driven by
  the nine-part completeness boundary, not a numeric threshold. Both designs
  need this; only the incumbent named it precisely
  (`reviews/contract-adversary.md`, "CA-05"). This is a `separate-decision`
  prerequisite (Gate-5 classification), not blocking topology or contract
  selection, and it is not resolved by ADR-0052. An additive
  `attachment-rule.v3` (or equivalent) successor is owed before Schedule D's
  attachment disposition can be produced.
- **CA-06.** The rival's exactly-one-producer requirement for `P` is a
  paper-contract statement (`it2/design.md` P3-S7), not a resolved generic
  representation: whether two mutually exclusive rule citizens may publish
  one symbol, or a dedicated selected-binding citizen is required, is left
  open (`reviews/contract-adversary.md`, "CA-06"). `reviews/repair1-confirmation.md`
  independently confirms this scoping is accurate: disjoint pin sets plus
  mutually exclusive producers make the current producer recoverable on
  paper, but Rung 1 cannot show the committed schema/validator substrate
  mechanically enforces the exclusivity. This is a `separate-decision`
  prerequisite, appropriately scoped to a narrow Rung-2 validator/
  distinguishability question only after CA-04's contract-level resolution —
  which this ADR now supplies. It is not resolved by ADR-0052.

## 5. Non-blocking observations

- `reviews/contract-adversary.md`'s CA-07 (incumbent's synthesized-conclusion
  binding locus unselected) is moot: the incumbent is not carried forward.
- `round-1-triage.md`'s EXP finding (the expressiveness review's case 1/11
  recovery table reproduces the incumbent's narrow predicate without flagging
  it) is a process observation only; CA-01 already covers the underlying
  defect and the incumbent is rejected regardless.
- `repair1/design.md` §5 ("Repair boundary") and `reviews/repair1-confirmation.md`
  ("Uncertainty Rung 1 cannot distinguish") both independently state that the
  repair answers only pin location, not the CA-06 mechanical-enforcement
  question — consistent with this analysis's §4.

## 6. Traceability statement

Every ADR-0052 clause above cites a specific file and section on the
prototype branches `prototypes/schedule-d-covered-ltcg-8a/it1` and
`prototypes/schedule-d-covered-ltcg-8a/it2` (repair1 and the committee
reviews are committed on the `it2` line). No ADR-0052 sentence introduces a
proposition, case, or successor contract that is not traceable to one of the
rows in §2. Prototype code, if any existed beyond the paper artifacts cited
here, never became a production candidate (`PROJECT_PLANNING.md`, Gate 7) and
is not cited as evidence.
