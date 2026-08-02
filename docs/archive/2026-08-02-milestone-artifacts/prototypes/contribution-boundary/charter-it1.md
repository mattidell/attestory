# Charter: Iteration 1 — Contribution Boundary (Incumbent)

Date: 2026-07-16. Plan approved by owner (PR #4, merged `548318b`). Track 0,
topic D2 of the First Real Return Slice milestone.

- **Builder:** incumbent, High tier, independent context.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/contribution-boundary/it1/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper schema/canon diffs plus **throwaway probes** against the committed kernel/derivation machinery and a scratch out-of-repo live workspace (per ADR-0031 residency). No repository modifications beyond the two outputs; no git write commands.
- **Questions:** D2-P1 (contribution event + provenance linkage + structurally-enforced runs-consume-facts invariant) and D2-P2 (manual entry as an any-order anti-wizard event + correction by supersession).

## Binding context (build on, do not reopen)

D1 is ratified as **ADR-0031** (residency boundary): a contribution writes real
values only into the out-of-repo live workspace, never into the repository or a
pushable artifact. Consume it; do not redesign it. Facts and transitions are
governed by the committed kernel/derivation machinery and ADR-0023 (member
assertion and transition boundaries); supersession by Article 7; derived-finding
lineage by Article 12; declaration-before-instances by Article 10; the record by
Article 14. The milestone foreclosure clause binds: **anti-wizard** (any batch,
any order), **runs consume facts not inputs**, **schema-as-canon**. An exception
to any of these escalates to Tier 3 — do not design one in.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **D2-P1.** The **contribution event**: a recorded product act, distinct from a
   run, turning manually-entered real values into asserted facts. (a) Its
   **schema** as a declared citizen (Article 10). (b) The **provenance linkage**:
   each produced fact pins which contribution produced it, from which document at
   what version (Article 12). (c) The **runs-consume-facts invariant** enforced
   **structurally** — a run consumes published facts only and has no representable
   path to raw contribution inputs (not a policy; show why the path cannot exist).
2. **D2-P2.** **Manual entry as an any-order event.** Contribution is initiated by
   the user with any batch in any order, producing member-transition facts
   (ADR-0023) with contribution provenance; no step depends on a prior step. A
   **correction** is a new contribution that supersedes the prior fact through the
   existing individuation/derivation edges (Article 7) — no edit, no manual
   withdrawal, both contributions on the record.

## Required cases

The plan's six Gate-2 cases: (1) contribution produces provenance-bearing facts;
(2) **runs consume facts, not inputs — mandatory kill-test** (raw-input path
provably absent); (3) any-order equivalence (two orders → same fact state);
(4) correction by supersession; (5) contribution stays in quarantine — **D1
(ADR-0031) kill-test** on the repo/push surface; (6) **run reaching a raw input —
mandatory kill-test** (cannot silently succeed). For each: claim → schema/contract
change → kernel/derivation behavior → produced fact and provenance pins. Cases 2,
3, 6 are mandatory.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/contribution-boundary/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/contribution-boundary/examination-it1.md` (≤120 lines) stating
  D2-P1 and D2-P2 separately as settled-at-Rung-2 or unresolved, citing every case.

Read: the topic `plan.md`, this charter, `docs/governance/` (Articles 7, 10, 12,
14), ADR-0023, ADR-0031, and the committed `packages/kernel/` and
`packages/derivation/` source and schemas. Before writing, echo scope, the
Rung-2 / outside-repo boundary, and stop conditions.

## Stop conditions

Stop at the two static files. No contribution code committed, no schema/kernel
edits in the repo, no git writes. If a design needs a contract change you cannot
represent as a versioned schema/canon diff on paper, stop and report. Every value,
payer, and identifier in your outputs is synthetic; real inputs live only in the
out-of-repo scratch workspace.
