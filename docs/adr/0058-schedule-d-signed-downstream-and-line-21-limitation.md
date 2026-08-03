# ADR 0058 — Signed Schedule D Downstream Split and Line 21 Limitation

- Status: **accepted** (ratified by the owner 2026-08-03)
- Tier: 2 — content/routing arithmetic for one breadth slice; reuses
  existing expression vocabulary and filing-status parameters.
- Date: 2026-08-03

## Context

ADR-0057 establishes additive short-term and long-term gain-or-loss source
families and the multi-family selected-preferential-base discriminator.
This ADR settles how signed Schedule D results reach Form 1040, how the
preferential-rate input is floored, how completeness retires two absence
declarations, and the owner-bounded claim that no 2026 carryover amount is
computed.

Inspected commitments that force an explicit split:

- `packages/content/tax/2025/rule.form1040-line16.v4.json` feeds
  `selected-preferential-base` unfloored into QDCG ordinary-portion
  subtraction and into the gate `all([Q==0, base==0])` /
  QDCG-when-`Q>0 OR base>0`. A negative base corrupts both.
- `packages/content/tax/2025/rule.form1040-line7a.v2.json` is a pure
  `ref` of selected-preferential-base — correct only while that symbol
  equals the Form 1040 line 7a amount (gain-only slice).
- `packages/content/tax/2025/schedule-d-boundary.bundle.json` carries
  `no-short-term-transactions` and `no-current-capital-losses`, which the
  milestone retires.
- Expression vocabulary already includes `max`, `choose`, `compare`,
  `parameter`, `subtract`, `add`, `any`, `all`
  (`packages/schemas/derivation/rule-artifact.v3.schema.json`;
  `packages/derivation/evaluator.py`). Filing-status-keyed parameters are
  demonstrated by `parameter.standard-deduction-base.json` /
  `rule.form1040-standard-deduction.json`. There is no `min` op; minimum is
  expressed with `choose`+`compare`.

Track 0's paper-first decision record settled this ADR's downstream-split
and completeness contracts against real committed source before this ADR
was drafted; it is distilled here and in the milestone retrospective, not
retained separately.

## Decision

1. **Schedule D lines stay signed through line 16.** For this class:

   - Line 1a (h) = ST proceeds − ST basis (signed).
   - Line 7 = Part I net (line 1a (h) for this bounded class; other Part I
     inputs closure-backed zero under completeness).
   - Line 8a (h) = LT proceeds − LT basis (signed).
   - Line 13 = closed box-2a subtotal once (may be zero).
   - Line 15 = line 8a (h) + line 13 (+ other Part II zeros).
   - Line 16 = line 7 + line 15 (**signed**).

2. **Line 21 — current-year loss limitation only.** When line 16 < 0,
   line 21 publishes the positive allowed loss:

   ```
   min(−line16, capital_loss_limit(filing_status))
   ```

   with `capital_loss_limit` a new filing-status-keyed parameter
   (`demo.parameter.capital-loss-limit.2025`): $3,000 for single, married
   filing jointly, head of household, and qualifying surviving spouse;
   $1,500 for married filing separately. When line 16 ≥ 0, line 21 is not
   a positive deduction (Track 1 uses honest zero or `inapplicable`, not a
   fabricated carry figure). **No** "loss remaining after limitation" and
   **no** 2026-keyed amount is published (Decision 6).

3. **Form 1040 line 7a successor.** Additive content successor:

   - If line 16 ≥ 0: line 7a = line 16.
   - If line 16 < 0: line 7a = −(line 21).

   Line 9 continues to add line 7a once. This **supersedes, for the
   versioned loss-capable graph only**, ADR-0052 Decision 5's identity
   between line 7a and selected-preferential-base on net-loss returns. It
   does not edit ADR-0052's text. Nonnegative Schedule D results and the
   direct box-2a route continue to keep line 7a aligned with the
   preferential base.

4. **Preferential-rate producer floors at the producer.** On the Schedule D
   branch of selected-preferential-base (ADR-0057), the published value is

   ```
   max([schedule_d_line_16, 0])
   ```

   using the existing `max` op. Flooring happens **here**, not inside
   `rule.form1040-line16`'s QDCG consumer. The direct branch remains the
   box-2a subtotal (≥ 0). Consequently no negative value is a valid
   numeric selected-preferential-base publication.

5. **QDCG gate remains correct at zero.** With a floored base of 0 after a
   net Schedule D loss:

   - Q == 0 → ordinary-bracket path (`all([Q==0, base==0])` in line 16 v4
     structure). Correct: no preferential income.
   - Q > 0 → QDCG ladder with L = 0. Correct: qualified dividends still
     preferential; capital loss is not preferential income.

   Line 16 content may still need a successor only to replace its
   gain-only proceeds dependency used for branch pin selection; the QDCG
   arithmetic ops and gate shape are preserved in spirit.

6. **Completeness declaration successor.** Successor Schedule D attachment
   completeness **drops** required answers
   `no-short-term-transactions` and `no-current-capital-losses` (retired;
   replaced by ST/LT family closure under ADR-0057). By inspection of
   `schedule-d-boundary.bundle.json`, these five remain value-checked
   `"yes"` and are **untouched in meaning**:

   - `no-inbound-capital-loss-carryovers`
   - `no-form8949-sources`
   - `no-other-schedule-d-sources`
   - `no-lines-18-19-sources`
   - `no-1099da-or-qof`

   Historical bundle v1 and fact types remain immutable for old packages.

7. **Bounded claim (owner-confirmed, binding).** This milestone computes
   and publishes only the **2025** Schedule D line 21 amount and the Form
   1040 line 7a capital-loss deduction it feeds. It does **not** derive or
   publish any amount carried into **2026**. Inbound carryovers remain an
   honest absence boundary (Decision 6), not a computed input.

## Production conditions (discharged by Track 1's implementation in this milestone)

- Successor rules for lines 1a, 7, 8a, 15, 16, 21; selected-preferential-base
  v2 with floor; line 7a/9/16 successors as required by package pins.
- Parameter citizen for the $3,000/$1,500 limit with filing-status keys.
- Goldens: short-term loss only; long-term loss only; net loss over $3,000;
  MFS over $1,500; mixed offsets producing net gain and net loss; box-2a
  with transaction losses; no negative preferential-base publication
  (explicit negative-injection negative test); prior gain-only fixtures
  unmodified on historical packages.
- Proof that no 2026 carry symbol, fact type, or fixture exists in the
  milestone range.

## Consequences

- Form 1040 line 7a can show a capped capital-loss deduction while QDCG
  never treats a loss as preferential income.
- Completeness honestly requires closed ST and LT families instead of
  false "no short-term / no losses" attestations for this class.
- Multi-year capital-loss carryover remains a separately selectable
  frontier row.

## Alternatives considered

- **Keep line 7a == selected-preferential-base always.** Rejected: after
  flooring, net-loss returns would publish line 7a = 0 and lose the
  §1211 limited deduction.
- **Floor inside the QDCG rule only.** Rejected: leaves other consumers of
  selected-preferential-base exposed; charter/plan require producer-side
  floor.
- **New `min` evaluator op for line 21.** Rejected: `choose`+`compare`
  already express minimum; no substrate gap.
- **Publish carryover remaining to 2026 "for completeness."** Rejected by
  owner-bounded claim (Decision 7).

## Links

- Decision record and Track 0/1 working charters: not retained in the
  repository; distilled into this ADR and the milestone retrospective
  (`docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md`).
- Plan: `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md`
- Builds on: ADR-0036, ADR-0038, ADR-0050, **ADR-0052**, **ADR-0053**,
  ADR-0055, **ADR-0057**
- Implemented by: Track 1's production-route commit in this milestone.
