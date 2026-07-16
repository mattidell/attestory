# Charter: Iteration 2 — Conditional Selectors (Clean-Room Rival)

Date: 2026-07-13. Issued by the principal foreman under the owner-approved plan (Gates 4 and 8) and the round-1R triage. The plan's clean-room rival seat was never filled in the original run; this charter fills it. ADR-0019 (selector citizen) is rejected; the accepted direction is the Shape A family.

- **Builder:** clean-room rival, High tier, owner-launched external context.
- **Working location:** `docs/prototypes/conditional-selectors/it2/` on the milestone branch; foreman holds git custody (no branch, tag, merge, or commit by the builder).
- **Evidence:** rule/parameter citizen payloads, paper walkthroughs, and static executability traces against the committed evaluator. Rung 2 authorized: the builder may *run* the committed evaluator read-only on synthetic payloads in a scratch directory, but may not modify any repository file outside the two chartered outputs.
- **Questions:** CS-P1 and CS-P2.

## Clean-room exclusions

Do **not** read: `it1/`, `examination-it1.md`, `repair1/`, `charter-repair1.md`, `examination-repair1.md`, `reviews/`, `round-1-triage.md`, `round-1r-triage.md`, `round-2-triage.md`, `evaluation-analysis.md`, `SEAT.md`, `process-log.md`, `docs/adr/0019-*.md`, `docs/adr/0020-*.md`, other prototype topics' iteration/review material, or the git branches `wip/track3-core-conditions` and `archive/core-tax-conditions-pre-reset`.

May read: `plan.md`, this charter, `docs/governance/`, ADRs 0002, 0004, 0006–0010, 0012, 0016, 0017, and committed `packages/derivation/` and `packages/kernel/` source and schemas at `HEAD`.

## Assignment

Design conditional standard-deduction selection and tax-computation-method selection **in the existing rule language** — rule artifacts, parameter citizens, guards — with no new citizen type and no new runner pathway. Produce the strongest form you can. Hard requirements (these are known failure modes of prior work, restated here as constraints rather than disclosed designs):

1. **Executability is the bar.** Every guard and value expression you write must execute under the committed evaluator's actual operation and comparison contracts — trace each against `packages/derivation/evaluator.py` as it is, not as the rule schema alone permits. In particular: choose a categorical representation for filing status that the committed comparison semantics genuinely support; author every `operation-semantics.v1` canon citizen your expressions require (e.g. for rounding and bracket folding); and use the canon's legal bracket-table row shape.
2. **Exhaustiveness.** All five filing statuses (single, MFJ, MFS, HoH, QSS), with age/blindness/spousal adjustments correctly scoped per status.
3. **Policy/logic separation (CS-P2).** Every amount and rate lives in a versioned parameter citizen; rules carry only logic and references.
4. **Optional-input honesty.** Unasserted age/blindness/spousal inputs must become operative through declared content (not runner-resident policy), must never silently overwrite an input a user has already asserted, and must displace correctly when the input is asserted after a run (Article 7 — no third edge kind).
5. Zero and negative taxable income, bracket-threshold boundaries (state your boundary convention explicitly), and the asserted itemization override must be handled or explicitly scoped out with reasons.

## Required cases

The plan's five synthetic cases, each with two positive instances, two negatives, one lifecycle trace, and the claim → citizen payloads → evaluator execution path → derived finding map. Add one displacement trace: an optional input asserted after an initial run.

## Outputs

- `docs/prototypes/conditional-selectors/it2/design.md`
- `docs/prototypes/conditional-selectors/examination-it2.md` (≤120 lines) stating CS-P1 and CS-P2 separately as settled-at-static-level or unresolved, citing every case.

Before writing, echo scope, paper boundary, stop conditions, and clean-room exclusions. Report unresolved authority questions explicitly rather than resolving them by fiat.

## Stop conditions

Stop at the two static files. No repository modifications outside them, no schema changes, no runner/evaluator changes, no git write commands.
