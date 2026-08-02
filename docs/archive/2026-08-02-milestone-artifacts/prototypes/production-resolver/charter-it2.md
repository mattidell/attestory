# Charter: Iteration 2 — Production Package Resolver (Clean-Room Rival)

Date: 2026-07-16. Plan approved by owner (PR #6, merged `a213cf3`). Track 0,
topic D3 (last Track-0 decision) of the First Real Return Slice milestone.

- **Builder:** clean-room rival, High tier, independent context, **sealed from
  the incumbent**.
- **Working location:** `docs/archive/2026-08-02-milestone-artifacts/prototypes/production-resolver/it2/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper resolver/validation diffs plus **throwaway probes** against the committed loader/validation and a scratch out-of-repo workspace holding a synthetic adopted package (per ADR-0031). No repository modifications beyond the two outputs; no git write commands.
- **Questions:** D3-P1 (production resolution contract — exclusive member graph + byte-verification beyond the fixture boundary, a strict superset of the fixture path) and D3-P2 (discharge/defer ledger against ADR-0027/0028 named production conditions).

## Clean-room seal (mandatory)

You are the independent rival. **Do not read** `it1/`, `examination-it1.md`, or
any incumbent output; if you encounter incumbent material, stop and report. Derive
the resolution contract independently from the committed contracts and the plan.
Genuine rivalry per round is required (ADR-0013 amendment 2026-07-13). Where you
reach the same shape it must be by independent justification; where you diverge,
say so and why — divergence is committee signal.

## Binding context (build on, do not reopen)

ADR-0027 decision 7 (exclusive execution projection) and ADR-0028 (member +
package-instance byte-verification, quantity/composition closure, fail-closed at
load) are ratified **inside the fixture boundary**; D3 extends them to a
live-workspace source. D1 (ADR-0031) owns the residency + leak wall — **consume
it, do not re-prove or weaken it**. D2 (ADR-0032) owns contribution. The committed
`packages/derivation/loader.py`, `package_validation.py`, and runner are the
fixture-path reference the production path must strictly superset.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **D3-P1.** The **production resolution contract**: how adopted package(s)
   resolve to their **exclusive resolved member graph** in a live workspace `L`
   (ADR-0031) — (a) locating the adopted package; (b) **byte-verifying** every
   member and the package instance **fail-closed** at load (ADR-0028); (c)
   projecting the exclusive graph so co-located unpinned files are inert
   (ADR-0027 d7); (d) a demonstrated **strict superset** of the fixture path's
   guarantees, never a weaker sibling.
2. **D3-P2.** The **discharge/defer ledger**: each ADR-0027/0028 named production
   condition mapped to *discharged-here* or *deferred-with-reason*; no item
   unaccounted, no silent partial discharge.

## Required cases

The plan's six Gate-2 cases: (1) clean production resolution with fixture parity;
(2) exclusive projection — co-located unpinned file inert; (3) **byte-verification
— mandatory** (member + package-instance mismatch reject fail-closed); (4) D1
interlock — no leak of live content into a tracked/pushable artifact; (5) negative
— no silent partial load; (6) **discharge/defer ledger — mandatory**. For each:
claim → resolver/validation change → load/projection behavior → resolved graph and
reject/accept observed. Cases 3 and 6 mandatory.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/production-resolver/it2/design.md` (≤ 300 lines)
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/production-resolver/examination-it2.md` (≤ 120 lines) stating
  D3-P1 and D3-P2 separately as settled-at-Rung-2 or unresolved, citing every case.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADR-0027, ADR-0028,
ADR-0031, and the committed `packages/derivation/` loader/validation/runner source
and schemas. **Do not read incumbent material.** Before writing, echo scope, the
seal, the Rung-2 / outside-repo boundary, and stop conditions.

## Stop conditions

Stop at the two static files. No resolver code committed, no loader/validation
edits, no git writes. If a design needs a contract change you cannot represent as
a versioned diff on paper, stop and report. Every package, member, value, and
identifier is synthetic; the "production" source is an out-of-repo scratch workspace.
