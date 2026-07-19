# Charter: Iteration 1 — QDCG Worksheet and Declared Absence (Incumbent)

Date: 2026-07-19. Plan approved by owner (PR #28, merged `eccb0d6`). Track 0,
topic D2 of the Dividends and Schedule B Slice milestone.

- **Builder:** incumbent, High tier, independent context.
- **Working location:** `docs/prototypes/qdcg-worksheet/it1/`; foreman holds
  git custody.
- **Evidence:** Rung 1 for all propositions; **rung-2 throwaway probes for
  two named questions only** — (a) committed expression-language
  expressibility of the ladder's min/max/split steps, only if paper cannot
  cite it from ADR-0006/0025 contract text; (b) committed currency
  displacement (ADR-0010) when a pinned declaration is superseded — cite or
  probe. No repository modifications beyond the two outputs; no git writes.
- **Questions:** D2-P1 (declared-absence fact types on the ratified
  assertion pattern), D2-P2 (the worksheet ladder as declared expression
  content; the reduction property; supersession of the existing line-16
  rule), D2-P3 (the bidirectional contradiction mechanism).

## Binding context (build on, do not reopen)

Ratified and consumed as-is: ADR-0006/0024/0025 (rule and expression
language), ADR-0010 (currency and displacement), ADR-0032 (contribution),
**ADR-0035** (`CAPITAL_GAIN_DISTRIBUTION_RECORDED` — the box-2a signal your
contradiction mechanism consumes; the recorded-non-composable universe your
case 6 must respect), **ADR-0036** (the categorical `{yes, no}`
presence-semantics assertion pattern your declarations instantiate; its
presence-not-truthiness production condition binds you). Owner rulings bind
and are not relitigated: the worksheet is built (block-on-3a retired);
declared zero is factual completeness; a declaration contradicted by facts
on record is a hard error in **both temporal orders**. The ordinary tax
computation is existing ratified content — your worksheet's ordinary
sub-steps reuse it unchanged. Foreclosure: honest blocking, trace over
answer, schema-as-canon. Exceptions escalate to Tier 3 — do not design one
in.

## Assignment

Design all three propositions against the committed contracts at `HEAD`:

1. **D2-P1.** Two declared-absence fact types (no capital-gain
   distributions; no Schedule D requirement) on the ADR-0036 pattern —
   categorical domains, presence semantics, unconditional pinning —
   contributed via ADR-0032 unchanged.
2. **D2-P2.** The QDCG ladder as citable expression content over
   filing-status-keyed parameter declarations (0/15/20% breakpoints):
   split, per-rate portions, comparison, final min. The **reduction
   property shown by algebra** (qualified = 0 ⇒ worksheet = ordinary
   result). The supersession posture: one worksheet rule superseding the
   existing line-16 rule as versioned content, or a conditional selector —
   choose and justify against anti-wizard and honest-blocking.
3. **D2-P3.** The contradiction mechanism: a declared-absence finding and a
   `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal may never both be current.
   Name the mechanism for each temporal order (declaration first, statement
   later; statement first, declaration attempted) and for the same-batch
   case. Line 16 must be unable to publish over a contradiction — by
   construction, not policy.

## Required cases

The plan's six Gate-2 cases: (1) worksheet positive, full ladder walked,
every step citable, result below ordinary; (2) **reduction property,
mandatory** — by algebra, plus the supersession posture; (3) **missing
declaration blocks, mandatory** — walkable, naming both contributable
facts; (4) **contradiction kill-case, mandatory, both orders and
same-batch** — show the mechanism and what the user is told; (5)
declared-zero publishes with declarations pinned (displacement edge shown);
(6) **no reach-around, mandatory** — the worksheet cannot read box 2a or
any recorded-non-composable content; unrepresentable, not untested.
Producer → authority → consumer → failure map per proposition.

## Outputs

- `docs/prototypes/qdcg-worksheet/it1/design.md` (≤300 lines)
- `docs/prototypes/qdcg-worksheet/examination-it1.md` (≤100 lines) stating
  D2-P1, D2-P2, and D2-P3 separately as settled-at-rung or unresolved,
  citing every case.

Read: the topic `plan.md`, this charter, `docs/governance/`, the ADRs named
above, the existing line-16 rule content under `packages/content/`, and the
committed evaluator/runner source. Before writing, echo scope, the rung
boundary and two authorized probe questions, and stop conditions.

## Stop conditions

Stop at the two static files. No production code, no schema edits in the
repo, no git writes. If a design needs a contract change you cannot
represent as a versioned schema/canon diff on paper, stop and report. Every
income, amount, payer, and identifier in your outputs is synthetic
(`demo-*`); real shapes inform cases only by stated re-expression
(ADR-0031).
