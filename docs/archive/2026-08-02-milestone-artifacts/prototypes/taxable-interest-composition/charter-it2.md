# Charter: Iteration 2 — Taxable-Interest Composition (Clean-Room Rival)

Date: 2026-07-14. Plan approved by owner (2026-07-14). Issued after the it1 incumbent exhibit passed foreman conformance (commit `4ea0b6c`).

- **Builder:** clean-room rival, High tier, owner-launched external context.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/taxable-interest-composition/it2/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs, composition and lifecycle traces against the committed runner and ratified horizon/currency machinery, and throwaway probes in a scratch directory **outside** the repository. No repository modifications beyond the two outputs.
- **Questions:** TIC-P1 (coextensive line-2b universe + declaration mechanism) and TIC-P2 (honest coextensive zero + late-member lifecycle) — the same two propositions the incumbent addressed.

## Clean-room boundary (mandatory)

This is a genuine independent rival, not a critique or a variation. **Do not read** any of: `it1/design.md`, `examination-it1.md`, the inert `taxable-interest-composition-spike.md`, or the inert `docs/adr/0021-taxable-interest-composition-and-line-2b.md`. Do not seek their content by any indirect means. **In particular, derive the line-2b member boundary yourself** from the Form 1040 line-2b definition and the ratified ADR-0016 constraints — do not look for a prior answer to inherit. The boundary question (which interest sources compose line 2b) is the primary convergence test of this round; a contaminated rival is worthless as evidence. If you have already seen any of those documents, stop and report that to the foreman instead of proceeding.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **TIC-P1.** Determine the **coextensive taxable-interest universe** for Form 1040 line 2b and **justify its member boundary against the line-2b definition** (line 2b is *taxable* interest; line 2a is tax-exempt) — do not assert it. Then design the mechanism by which the composition is *declared coextensive*: a checkable claim over the whole universe that a validator **rejects** when a constituent is missing, so consuming the constituent subtotals satisfies ADR-0016 decision 4 and is not the "implicit subtotal promotion" decision 5 rejects. Hard constraints: no new standing-affecting edge (Article 7, ADR-0010); no change to the ratified horizon/currency machinery (ADR-0017); coverage must never report the broader universe complete from a narrow closure (ADR-0016 decision 3). If your justified boundary omits or adds a source relative to what a naive "one 1099-INT box each" reading suggests, say so and why.
2. **TIC-P2.** Honest coextensive zero and the late-member lifecycle. An empty line-2b zero publishes **only** when every constituent family is coextensively closed (never from box-1 closure alone, ADR-0016 decision 5). A late member transitions family membership, blocks line 2b, and re-derives on re-attestation **through the existing individuation/derivation edges only** — the old coextensive zero leaves current state with no manual withdrawal and no new edge.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADRs 0002, 0004, 0006–0012, 0014, 0015, 0016, 0017, and committed `packages/derivation/` and `packages/kernel/` source and schemas, plus the committed b1-subtotal / source-family / horizon content from the Source Completeness slice. The it1 outputs, the spike, and ADR-0021 are **out of scope** (clean-room boundary above).

## Required cases

The plan's six Gate-2 cases, each (where applicable) with two positive instances, two negatives, and the claim → schema/contract change → runner/horizon behavior → derived finding and pin map. **Case 5 (narrow-substitution must block) and Case 6 (late-member lifecycle) are mandatory;** Case 6's trace must name every finding, pin, and edge and show the old coextensive zero leaving current state through existing edges only.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/taxable-interest-composition/it2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/taxable-interest-composition/examination-it2.md` (≤120 lines) stating TIC-P1 and TIC-P2 separately as settled-at-static-level or unresolved, citing every case.

Before writing, echo scope, the paper/Rung-2 boundary, the clean-room boundary, and stop conditions. Report unresolved authority questions explicitly rather than resolving them by fiat.

## Stop conditions

Stop at the two static files. No runner/schema/horizon edits, no git write commands. If a design requires a contract change you cannot represent as a versioned schema/canon diff on paper, stop and report rather than improvising.
