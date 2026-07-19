# Charter: Iteration 1 — Dividend Composition (Incumbent)

Date: 2026-07-18. Plan approved by owner (PR #24, merged `5cb7efc`). Track 0,
topic D3 of the Dividends and Schedule B Slice milestone.

- **Builder:** incumbent, High tier, independent context.
- **Working location:** `docs/prototypes/dividend-composition/it1/`; foreman
  holds git custody.
- **Evidence:** Rung 1 (static schema/canon diffs and paper cases) for D3-P2;
  **Rung 2 probes for D3-P3 case 2 only** — throwaway probes against the
  committed validation/admission machinery demonstrating the 1b > 1a
  rejection at your chosen locus, and that a schema-only route cannot
  express it. No repository modifications beyond the two outputs; no git
  write commands.
- **Questions:** D3-P2 (ordinary-dividend composition, line 3b, declared
  universe with recorded-non-composable exclusions) and D3-P3 (qualified
  subset, line 3a, structural enforcement locus). D3-P1 (statement identity
  and family) is **settled as implement-normally** — instantiate the
  ADR-0015 pattern as your substrate without buying it new evidence.

## Binding context (build on, do not reopen)

The statement→family→composition→line pipeline is ratified: ADR-0015
(statement-instance identity), ADR-0016 (family claim and composition),
ADR-0026 (declared coextensive composition, line 2b — the pattern, not the
universe), ADR-0014/0017 (horizon-keyed closure), ADR-0023 (member
transitions), ADR-0032 (contribution — consumed as-is). Owner directions
recorded in the milestone plan bind: the dividend universe is boxes 1a/1b;
boxes 2a/3/5/7/12 are **recorded but non-composable** on the statement —
box 2a's presence must be visible to a return-level disposition (D2's
contradiction check feeds on it), so a design that refuses out-of-universe
boxes at admission is invalid. Owner default (veto window open): **1b > 1a
is rejected structurally, not recorded**. Foreclosure principles:
schema-as-canon, honest blocking, no silent drop of any box. Exceptions
escalate to Tier 3 — do not design one in.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **D3-P2.** Line 3b composes from box 1a over the closed 1099-DIV family;
   the universe declaration names its exclusions; excluded boxes ride the
   statement as recorded, non-composable content with a named return-level
   consequence for 2a (walked, not hand-waved) and a named-only recording
   for the rest.
2. **D3-P3.** Line 3a composes from box 1b. The subset invariant — 1b ≤ 1a
   per statement, 3a ≤ 3b per line — enforced structurally. Name the locus
   (admission machinery, composition contract, or both), justify it, and
   show the line-level relation holds by construction when both lines
   compose over the same closed family (prove it; if the declared sets can
   ever diverge, name the guard).

## Required cases

The plan's six Gate-2 cases: (1) two positives (single statement 900/600;
two statements 900/600 + 400/0 → 3b=1300, 3a=600); (2) **subset kill-case,
mandatory** — a 1b > 1a statement dies at your named locus, probe-backed;
(3) line-level subset by construction, proven; (4) **out-of-universe box 2a,
mandatory** — admits, records, lines publish, return-level disposition
walked; contrast box 7; (5) empty family closes honestly (zeros publish;
undeclared family blocks); (6) **universe creep, mandatory** — composing 2a
into any line is unrepresentable, not merely untested. For each: claim →
schema/contract change → machinery behavior → produced findings and pins.

## Outputs

- `docs/prototypes/dividend-composition/it1/design.md` (≤250 lines)
- `docs/prototypes/dividend-composition/examination-it1.md` (≤100 lines)
  stating D3-P2 and D3-P3 separately as settled-at-rung or unresolved,
  citing every case.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADRs 0014–0017,
0023, 0026, 0032, and the committed `packages/` schemas and validation
machinery. Before writing, echo scope, the rung boundary, and stop
conditions.

## Stop conditions

Stop at the two static files. No production composition code, no schema
edits in the repo, no git writes. If a design needs a contract change you
cannot represent as a versioned schema/canon diff on paper, stop and report.
Every payer, value, and identifier in your outputs is synthetic (`demo-*`);
real 1099-DIV shapes inform cases only by stated re-expression (ADR-0031).
