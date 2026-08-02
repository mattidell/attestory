# Examination: QDCG Worksheet and Declared Absence (D2, Incumbent It1)

Rung 1 only. Each proposition is **settled-at-rung** or **unresolved**, citing
cases. Authorized probes (a) ladder expressibility and (b) currency
displacement were **not executed**: both settle from committed contract text
(ADR-0006/0025 + `rule-artifact.v2` `$defs.expr` + `evaluator.py`; ADR-0010
D3–D5 + `packages/derivation/projection.py`). Design:
`docs/archive/2026-08-02-milestone-artifacts/prototypes/qdcg-worksheet/it1/design.md`. Synthetic `demo-*` only.

## D2-P1 — Declared-absence fact types — **settled at Rung 1**

Two `fact-type.v2` assertions (`demo.assertion.capital-gain-distributions`,
`demo.assertion.schedule-d-required`) on the ADR-0036 pattern: categorical
`{yes, no}` (never boolean), presence-before-value, no `optional_default`,
unconditional `input` pins, contributed via ADR-0032. Settled by:

- **Case 3 (mandatory):** missing findings → `DEPENDENCY_ABSENT` naming **both**
  contributable facts (runner requires-before-value); not implied zero.
- **Case 5:** `"no"`/`"no"` present → declared-zero is factual completeness;
  CG input bound to literal 0 under the guard; pins give supersession an edge.
- **Presence-not-truthiness:** package must reject boolean domains (ADR-0036
  PC2, recorded as production condition — not a design gap).

No representation gap beyond versioned fact-type content.

## D2-P2 — Worksheet ladder, reduction, supersession — **settled at Rung 1**

Ladder is citable `rule-artifact.v2` expression content over filing-status-keyed
parameters. **min** = `choose`+`compare lte`; **max**/**subtract**/**add** committed;
preferential rates via single-band `bracket_fold` (canon multiplies — no bare
multiply op). Ordinary sub-steps reuse existing `bracket_fold`+`round`.

- **Case 1:** full walk (split, per-rate portions, comparison/`min` final,
  parameters cited); result strictly below full ordinary; pins 3a,
  declarations, parameters.
- **Case 2 (mandatory):** algebra Q=CG=0 ⇒ pref=0 ⇒ ordinary-portion=T ⇒
  worksheet-sum = OrdTax(T) = full ordinary ⇒ line16 = OrdTax(T). **Supersession
  posture:** one v2 successor rule for all returns (unique symbol ownership,
  anti-wizard, honest-blocking); conditional selector rejected (§D2-P2 table).
- **Case 5:** displacement of line 16 when a pinned declaration is superseded
  follows ADR-0010 input-pin edges — cited, not probed.
- **Probe (a)/(b):** not consumed; contract text suffices.

## D2-P3 — Bidirectional contradiction — **settled at Rung 1**

**Mechanism: admission-locus mutual exclusion** (ADR-0035 analogue) between
declaration `"no"` and `CAPITAL_GAIN_DISTRIBUTION_RECORDED` (box_2a ≠ null).
Before state mutation; contribution fails closed.

- **Case 4 (mandatory):** (a) declaration first, then box 2a → contribution
  rejected; (b) box 2a first, then `"no"` → assertion rejected; (c) same batch
  → staged pair fails closed, neither current. User told the contradiction in
  each path. Line 16 never publishes over it — **by construction** (no both-
  current state), not policy at derivation time.
- **Case 6 (mandatory):** worksheet cannot read box 2a / recorded-non-composable
  content — **unrepresentable** under ADR-0035 universe guard + package
  validation; only route to line 16 is the P3 hard error.
- Currency-only and derivation-time-only alternatives rejected (transient
  both-current; declared-zero degrades to assumed-zero).

## Convergence

| Proposition | Outcome | Cases |
|---|---|---|
| D2-P1 | settled at Rung 1 | 3, 5 |
| D2-P2 | settled at Rung 1 | 1, 2, 5 |
| D2-P3 | settled at Rung 1 | 4, 6 |

Mandatory cases 2, 3, 4, 6 hold; supporting 1 and 5 complete the map. Gate-6
floor met: citable ladder with algebraic reduction; capital-gain inputs only
via declared-absence presence semantics; missing declarations block; bidirectional
(+ same-batch) contradiction with no both-current state. Paper settles the
ladder and contradiction mechanism — **stop at paper** (plan Gate 2). Five
production conditions hand to Tracks 1–3 / candidate ADR-0037; none is an
unresolved design question. No authorized climb consumed. No contract change
required beyond versioned schema/content diffs stated on paper.
