# Charter: Iteration 2 — Contribution Boundary (Clean-Room Rival)

Date: 2026-07-16. Plan approved by owner (PR #4, merged `548318b`). Track 0,
topic D2 of the First Real Return Slice milestone.

- **Builder:** clean-room rival, High tier, independent context, **sealed from
  the incumbent**.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/contribution-boundary/it2/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs plus **throwaway probes** against the committed kernel/derivation machinery and a scratch out-of-repo live workspace (per ADR-0031). No repository modifications beyond the two outputs; no git write commands.
- **Questions:** D2-P1 (contribution event + provenance linkage + structurally-enforced runs-consume-facts invariant) and D2-P2 (manual entry as an any-order anti-wizard event + correction by supersession).

## Clean-room seal (mandatory)

You are the independent rival. **Do not read** `it1/`, `examination-it1.md`, or
any incumbent output; if you encounter incumbent material, stop and report. Derive
the contribution contract independently from the committed contracts and the plan.
Genuine rivalry per round is required (ADR-0013 amendment 2026-07-13). Where you
reach the same shape it must be by independent justification; where you diverge,
say so and why — divergence is committee signal.

## Binding context (build on, do not reopen)

D1 is ratified as **ADR-0031**: a contribution writes real values only into the
out-of-repo live workspace, never into the repository or a pushable artifact.
Consume it. Facts/transitions follow the committed kernel/derivation machinery and
ADR-0023; supersession Article 7; lineage Article 12; declaration-before-instances
Article 10; record Article 14. The foreclosure clause binds: **anti-wizard**,
**runs consume facts not inputs**, **schema-as-canon**; an exception escalates to
Tier 3.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **D2-P1.** The **contribution event** distinct from a run: (a) its **schema**
   as a declared citizen (Article 10); (b) the **provenance linkage** — each fact
   pins its contribution, source document, and version (Article 12); (c) the
   **runs-consume-facts invariant** enforced **structurally** — a run consumes
   published facts only and has no representable path to raw contribution inputs.
2. **D2-P2.** **Manual entry as an any-order event** producing member-transition
   facts (ADR-0023) with contribution provenance, no forced sequence; **correction
   by supersession** through existing edges (Article 7), never an edit.

## Required cases

The plan's six Gate-2 cases: (1) contribution produces provenance-bearing facts;
(2) **runs consume facts, not inputs — mandatory kill-test**; (3) any-order
equivalence; (4) correction by supersession; (5) contribution stays in quarantine
— **D1 (ADR-0031) kill-test**; (6) **run reaching a raw input — mandatory
kill-test**. For each: claim → schema/contract change → kernel/derivation behavior
→ produced fact and provenance pins. Cases 2, 3, 6 mandatory.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/contribution-boundary/it2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/contribution-boundary/examination-it2.md` (≤120 lines) stating
  D2-P1 and D2-P2 separately as settled-at-Rung-2 or unresolved, citing every case.

Read: the topic `plan.md`, this charter, `docs/governance/` (Articles 7, 10, 12,
14), ADR-0023, ADR-0031, and the committed `packages/kernel/` and
`packages/derivation/` source and schemas. **Do not read incumbent material.**
Before writing, echo scope, the seal, the Rung-2 / outside-repo boundary, and stop
conditions.

## Stop conditions

Stop at the two static files. No contribution code committed, no schema/kernel
edits, no git writes. If a design needs a contract change you cannot represent as
a versioned diff on paper, stop and report. Every value, payer, and identifier is
synthetic; real inputs live only in the out-of-repo scratch workspace.
