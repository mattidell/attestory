# ADR 0035 — 1099-DIV Dividend Composition and Lines 3a/3b

- Status: **accepted** (owner ratification 2026-07-18; Tier 2 default +
  veto, window closed without veto)
- Tier: 2
- Date: 2026-07-18

## Context

The Dividends and Schedule B Slice milestone brings 1099-DIV facts into the
return: line 3b (ordinary dividends) and line 3a (qualified dividends), the
first *coupled* line pair — 3a is by definition a subset of 3b. The
statement→family→composition→line pipeline is ratified (ADR-0015/0016/0026;
ADR-0014/0017 closure), but no existing composition couples two lines by a
subset relation, and JSON Schema (Draft 2020-12) cannot express a
cross-field numeric comparison, so the enforcement locus was undesigned.
Prototype evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/dividend-composition/` (plan, two
sealed builders, independent governance and adversary reviews,
`evaluation-analysis.md`). Both builders independently converged on
admission-locus enforcement; the clean-room rival's design survived all
named attacks with reproduced probes and is the shape ratified here. Owner
directions from the milestone plan bind: universe is boxes 1a/1b;
2a/3/5/7/12 recorded but non-composable; box 2a visible to D2's
contradiction check; 1b > 1a rejected structurally.

## Decision

1. **Substrate (implement normally).** 1099-DIV statement identity and
   family membership instantiate the ADR-0015 pattern (statement entity,
   payer + tax-year + payer_ref sameness); member transitions, horizons,
   and contribution per ADR-0017/0023/0032. Recorded as a Gate-0
   implement-normally finding; no prototype evidence was bought for it.

2. **Two independent per-box families.** `tax.us.2025.f1099div.1a` (member
   fact `box1a-ordinary`, authorizes the ordinary subtotal → line 3b) and
   `tax.us.2025.f1099div.1b` (member fact `box1b-qualified`, authorizes the
   qualified subtotal → line 3a), each with its own horizon-keyed closure
   and `source-closure-mapping.v2`. Each line rule `require_closed`s its
   own family: closed-empty publishes an honest zero; undeclared or open
   blocks that line. The lines may block independently (per-box closure
   independence, ADR-0016/0026 precedent).

3. **Declared dividend universe.** A `dividend-universe.v1` citizen names
   composable boxes {1a → 3b family, 1b → 3a family} and
   recorded-non-composable boxes {2a, 3, 5, 7, 12}. Excluded boxes ride a
   non-member `recorded-boxes` fact type keyed to the same statement
   (explicit `null` = declared absence of that box). Box 2a present raises
   the return-level signal **`CAPITAL_GAIN_DISTRIBUTION_RECORDED`**
   (statement and finding pins), the named feed for D2's contradiction
   check; the other excluded boxes are named-only recordings with no D2
   linkage. No rule may collect recorded-non-composable content; the
   universe claims completeness only over {1a, 1b}.

4. **Subset invariant, admission locus.** The per-statement invariant
   **1b ≤ 1a is enforced at tax-layer admission** — after per-finding
   `value_schema` validation, before state mutation, on every path that
   admits a box1a or box1b finding (assertion or member transition).
   Rejection semantics: qualified present with ordinary absent rejects;
   qualified > ordinary rejects; a correction of the ordinary value
   re-checks the current qualified value for the same statement; removing
   ordinary while qualified remains current rejects. Contribution batches
   fail closed (ADR-0032 terminal). A violating pair is never recorded —
   rejection, not recording, is the ratified posture (owner default,
   unvetoed). The line-level relation **3a ≤ 3b holds by construction**
   (sum inequality over admission-checked pairs; the divergence guard and
   proof are in the prototype design). Schema-only enforcement is
   unrepresentable — probe-backed (P1–P5, adversary-reproduced): Draft
   2020-12 `value_schema` cannot compare fields and `$data` is a
   SchemaError.

## Production conditions (owed to Tracks 1–2; never allowlisted)

- **Runtime universe guard (adversary A2):** Track 1 package validation
  must reject any rule whose collect targets a non-family fact type or
  whose inputs include recorded-non-composable content — the paper
  unrepresentability becomes a mechanical check.
- **Same-batch ordering (adversary minor):** Track 2 must define and
  kill-test admission ordering when both boxes' findings arrive in one
  batch, so the paired check cannot be sequenced around.
- Schema citizens, families, mappings, rules, form fields, citations, and
  the coordinator-from-facts goldens named in the milestone plan's
  Verification section.

## Consequences

- The subset-coupled composition pattern (admission invariant + same-family
  construction) is set for every future coupled line (Schedule D's 3a-adjacent
  shapes inherit it).
- D2's contradiction check gains its declared feed
  (`CAPITAL_GAIN_DISTRIBUTION_RECORDED`) without D3 widening into
  capital-gains scope.
- A 1099-DIV carrying only excluded boxes still contributes statements and
  recorded content but composes nothing — honest by the universe
  declaration.

## Alternatives Considered

- **Composite single-family shape (incumbent it1).** One fact/family
  carrying both boxes. Rejected: contradicts ratified per-box closure
  independence (ADR-0016 decision 5, ADR-0026 decision 3) and cannot
  represent one line blocking while the other publishes (governance G1).
- **`invariants` expression array on `fact-type.v2` (incumbent
  mechanism).** Rejected: a new schema surface the check does not need; its
  supporting rung-2 claim cited uncommitted machinery and was demoted on
  adversary reproduction. The admission-path check achieves the same
  structural rejection against committed contracts.
- **Record-then-flag (composition-only check).** Rejected by the milestone
  foreclosure clause: recording a violating pair and "handling it later" is
  silent wrongness.
- **Schema-only enforcement.** Structurally unavailable (probes P1–P5).

## Links

- Prototype evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/dividend-composition/` (it2 design
  is the ratified shape; `evaluation-analysis.md` carries triage)
- Builds on: ADR-0014/0015/0016/0017 (statements, families, closure),
  ADR-0023 (transitions), ADR-0026 (composition precedent), ADR-0032
  (contribution)
- Consumed by: D1 (Schedule B itemization reads statement facts), D2 (the
  box-2a signal), milestone Tracks 1–2
