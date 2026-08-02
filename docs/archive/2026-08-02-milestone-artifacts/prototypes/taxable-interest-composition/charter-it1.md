# Charter: Iteration 1 — Taxable-Interest Composition (Incumbent)

Date: 2026-07-14. Plan proposed to and approved by owner (2026-07-14 directive to charter now). Track 0.a of the Core Tax Conditions milestone remediation.

- **Builder:** incumbent, High tier, owner-launched external context.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/taxable-interest-composition/it1/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs, composition and lifecycle traces against the committed runner and the ratified horizon/currency machinery, and throwaway probes in a scratch directory **outside** the repository. No repository modifications beyond the two outputs.
- **Questions:** TIC-P1 (coextensive line-2b interest universe + declaration mechanism) and TIC-P2 (honest coextensive zero + late-member lifecycle).

## Prior art (in scope, to supersede — not to inherit)

You **may** read the inert `docs/archive/2026-08-02-milestone-artifacts/prototypes/taxable-interest-composition-spike.md` and the inert `docs/adr/0021-taxable-interest-composition-and-line-2b.md` as prior art the conforming ADR will supersede. **Do not inherit their boundary or their bare `sum`.** The spike *asserts* the universe is `{1099-INT box 1, box 3, non-form interest}` and computes `sum(...)` without establishing coextensiveness — that is the exact gap you must close by construction and justification, not repetition. If your design reaches the same membership set, it must be because you independently justified it against the line-2b definition, and your coextensiveness mechanism must defeat the narrow-substitution case (5) that the spike does not.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **TIC-P1.** The **coextensive taxable-interest universe** for Form 1040 line 2b. Fix its exact member boundary and **justify it against the line-2b definition** (what is in — box 1, box 3 US-savings-bond/Treasury interest, non-form interest; what is out — line-2a/box-8 tax-exempt interest), not by assertion. Design the mechanism by which the composition is *declared coextensive*: a checkable claim over the whole universe (a versioned composition declaration referencing each constituent family's ADR-0016 declaration/predicate) that a validator **rejects** when a constituent is missing — so consuming the subtotals satisfies ADR-0016 decision 4 and is not the "implicit subtotal promotion" decision 5 rejects. Hard constraints: no new standing-affecting edge (Article 7, ADR-0010); no change to the ratified horizon/currency machinery (ADR-0017); coverage must never report the broader universe complete from a narrow closure (ADR-0016 decision 3).
2. **TIC-P2.** Honest coextensive zero and the late-member lifecycle. An empty line-2b zero publishes **only** when every constituent family is coextensively closed (never from box-1 closure alone, ADR-0016 decision 5). A late member transitions family membership, blocks line 2b, and re-derives on re-attestation **through the existing individuation/derivation edges only** — the old coextensive zero leaves current state with no manual withdrawal and no new edge.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADRs 0002, 0004, 0006–0012, 0014, 0015, 0016, 0017, and committed `packages/derivation/` and `packages/kernel/` source and schemas, plus the committed b1-subtotal / source-family / horizon content from the Source Completeness slice.

## Required cases

The plan's six Gate-2 cases, each (where applicable) with two positive instances, two negatives, and the claim → schema/contract change → runner/horizon behavior → derived finding and pin map. **Case 5 (narrow-substitution must block) and Case 6 (late-member lifecycle) are mandatory;** Case 6's trace must name every finding, pin, and edge and show the old coextensive zero leaving current state through existing edges only.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/taxable-interest-composition/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/taxable-interest-composition/examination-it1.md` (≤120 lines) stating TIC-P1 and TIC-P2 separately as settled-at-static-level or unresolved, citing every case.

Before writing, echo scope, the paper/Rung-2 boundary, the prior-art (supersede-not-inherit) boundary, and stop conditions. Report unresolved authority questions explicitly rather than resolving them by fiat.

## Stop conditions

Stop at the two static files. No runner/schema/horizon edits, no git write commands. If a design requires a contract change you cannot represent as a versioned schema/canon diff on paper, stop and report rather than improvising.
