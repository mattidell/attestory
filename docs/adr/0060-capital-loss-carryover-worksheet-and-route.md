# ADR 0060 — Capital Loss Carryover Worksheet, Sign, Route Selection, and 2026 Bound

- Status: **accepted** (ratified by the owner 2026-08-04)
- Tier: 2 — content/routing arithmetic for one breadth slice; reuses existing
  expression vocabulary and attachment threshold semantics without a new
  schema kind.
- Date: 2026-08-04

## Context

ADR-0059 establishes the bounded 2024 prior-return authority and retires the
`no-inbound-capital-loss-carryovers` completeness declaration. This ADR
settles how those facts feed the **IRS Capital Loss Carryover
Worksheet—Lines 6 and 14** (2025 Instructions for Schedule D, carryovers
**from 2024 to 2025**), how worksheet results enter signed Schedule D lines 6
and 14, how a **carryover-only** return requires Schedule D and selects the
Schedule D preferential-base producer, and the binding proof that **no 2026
carry amount** is derived.

Inspected commitments that force explicit decisions:

- Attachment requirement today
  (`packages/content/tax/2025/attachment.schedule-d.v3.json`) is threshold
  any-over on ST/LT **proceeds** subtotals only. Runner semantics
  (`packages/derivation/runner.py`): any subtotal > threshold ⇒ required;
  both zero ⇒ not required; missing subtotal ⇒ blocked.
- `rule.selected-preferential-base.v2.json` selects the Schedule D branch
  only when `any([st_proceeds > 0, lt_proceeds > 0])`.
- ADR-0038's QDCG worksheet is declared **rule content** with internal
  `choose` / gates — not a separate worksheet schema kind.
- ADR-0058 keeps Schedule D signed through line 16, floors preferential base
  at the producer, and forbids publishing a 2026 carry amount from the
  current-year limitation work.
- Expression vocabulary already includes `max`, `choose`, `compare`, `add`,
  `subtract` (minimum expressed as `choose`+`compare`; no new `min` op).

Track 0's paper-first decision record settled this ADR's arithmetic, pin,
routing, and boundary contracts before this ADR was drafted; it is
distilled here and in the milestone retrospective, not retained separately.

## Decision

1. **Worksheet as declared rule content (ADR-0038 shape).** The Capital Loss
   Carryover Worksheet is implemented as versioned `rule-artifact.v3`
   content (one rule or a small published intermediate chain) under the 2025
   package. **No new schema kind** and no new evaluator op.

2. **Eligibility gate** (IRS worksheet preamble). Runs only on ADR-0059's
   Path B (the declaration is `"no"` and the five facts are contributed);
   Path A (declared no carryover) short-circuits to **W8 = 0** / **W13 = 0**
   without this gate or any body arithmetic, per ADR-0059 Decision 5. Uses
   the five prior-return facts (P1 = Form 1040 line 15, P2 = Schedule D
   line 21, P3 = line 7, P4 = line 15, P5 = line 16):

   ```text
   eligible =
     (P2 < 0)
     AND (
       (P5 < 0 AND abs(P2) < abs(P5))
       OR (P1 < 0)
     )
   ```

   If not eligible, publish short-term carryover **W8 = 0** and long-term
   carryover **W13 = 0**, still pinning all five prior-return facts so the
   zero result is auditable.

3. **Body arithmetic when eligible** (IRS lines 1–13; floors are "if zero or
   less, enter -0-"):

   ```text
   W1 = P1
   W2 = -P2
   W3 = max(W1 + W2, 0)
   W4 = min(W2, W3)            # choose+compare; no new min op

   if P3 < 0:
     W5 = -P3
     W6 = max(P4, 0)
     W7 = W4 + W6
     W8 = max(W5 - W7, 0)      # short-term capital loss carryover for 2025
   else:
     W5 = 0
     W8 = 0                    # IRS: -0- on line 5; go to line 9

   if P4 < 0:
     W9  = -P4
     W10 = max(P3, 0)
     W11 = max(W4 - W5, 0)
     W12 = W10 + W11
     W13 = max(W9 - W12, 0)    # long-term capital loss carryover for 2025
   else:
     W13 = 0                   # skip lines 9–13
   ```

   W8 and W13 are **nonnegative** (IRS worksheet result lines).

4. **Sign into Schedule D lines 6 and 14.**

   - Schedule D **line 6** publishes the **signed loss** `−W8` (zero when
     W8 = 0).
   - Schedule D **line 14** publishes the **signed loss** `−W13`.
   - Successor **line 7** = line 1a (h) + line 6 (+ other Part I zeros under
     completeness).
   - Successor **line 15** = line 8a (h) + line 13 (box 2a once) + line 14
     (+ other Part II zeros).
   - **Line 16**, **line 21**, and **Form 1040 line 7a** follow ADR-0058 over
     the recomputed line 16. ADR-0058's text is not edited; content
     successors only.

5. **Attachment requirement without new schema.** Successor Schedule D
   attachment content extends the existing **threshold any-over**
   multi-subtotal list:

   ```text
   subtotals = [
     st_proceeds_subtotal,
     lt_proceeds_subtotal,
     W8,
     W13,
   ]
   threshold = tax.us.2025.parameter.default-zero
   comparison = strictly_greater_than
   ```

   A carryover-only return (both transaction families closed-empty, W8 or W13
   > 0) **requires** Schedule D. Both carryovers zero and both families empty
   ⇒ not required by this trigger. W8 and W13 must always be published
   (including 0) when the attachment is evaluated — guaranteed under either
   ADR-0059 Decision 5 path: Path A publishes both as `0` directly from the
   declaration; Path B always runs the worksheet to a numeric pair (Decision
   2 above), including a legitimate zero result.

6. **selected-preferential-base successor.** Extend the Schedule D branch
   condition to:

   ```text
   any([st_proceeds > 0, lt_proceeds > 0, W8 > 0, W13 > 0])
   ```

   Schedule D branch still publishes `max(line_16, 0)` (ADR-0058 producer
   floor). Direct branch remains the box-2a path when the predicate is
   false. Exact pin signatures:

   | Producer | Exact direct pins on numeric selected-preferential-base |
   | --- | --- |
   | Direct | box-2a subtotal; its family/mapping/horizon/closure; checked Schedule D conclusion `"no"` as under the current direct path |
   | Schedule D | Schedule D line 16; attachment `required-and-complete`; ST/LT/box-2a closures; the **four** retained boundary declarations value-checked `"yes"` (ADR-0059 Decision 5); prior-return authority presence; W8; W13 |

7. **2026 boundary (owner-confirmed, binding).** This milestone derives and
   publishes only **2024 → 2025** carryover amounts onto **2025** Schedule D
   lines 6 and 14 (and the 2025 downstream recomputation). It does **not**
   derive or publish any amount carried from **2025 into 2026**. In
   particular:

   - No `tax.us.2026.*` carryover citizen, symbol, or fixture appears in the
     milestone range.
   - Line 21 remains the ADR-0058 current-year limitation only — no "loss
     remaining after limitation" and no "carryover to 2026" publication.
   - The IRS tip that carryover **to 2026** is figured on the **2026**
     Capital Loss Carryover Worksheet is out of scope.

## Production conditions (owed to Track 1; never allowlisted)

1. Worksheet rule content implementing Decisions 2–3 with citations to the
   IRS worksheet lines; goldens for both-carryover, ST-only, LT-only,
   partial offset in both directions, taxable-income-limited, zero-result,
   and ineligible cases (Path B), plus the Path A declared-no-carryover
   short-circuit (ADR-0059 Decision 5).
2. Successor Schedule D line 6 / 14 / 7 / 15 rules; line 16 / 21 / line 7a
   behavior per ADR-0058 over recomputed nets.
3. Successor attachment threshold list and selected-preferential-base
   predicate; goldens for carryover-only, carryover+current-year gain,
   carryover+current-year loss (under and over §1211), carryover+box-2a.
4. Package / fixture proof of Decision 7 (no 2026 carry symbol in the
   committed range).
5. Every existing current-year-losses regression fixture unmodified.

## Consequences

- Carryover-only returns honestly require Schedule D and take the Schedule D
  preferential-base producer without a new attachment schema.
- Worksheet results stay citable as nonnegative IRS amounts while Schedule D
  arithmetic stays signed through line 16.
- Multi-year carryover **into 2026** remains a separately selectable future
  slice; this ADR forbids sneaking it in as a side publication.

## Alternatives considered

- **New worksheet schema kind.** Rejected: ADR-0038 precedent is declared
  rule content; no substrate gap.
- **New `min` evaluator op.** Rejected: `choose`+`compare` already express
  minimum (ADR-0058).
- **`attachment-rule.v5` / new `family_nonempty` for carryovers.** Rejected:
  threshold multi-subtotal already implements any-over (ADR-0057 Decision 7).
- **Keep preferential-base branch on proceeds only.** Rejected: carryover-only
  returns would silently take the direct path.
- **Publish 2026 carry "for completeness."** Rejected by owner-bounded claim
  (Decision 7) and ADR-0058 Decision 7.

## Links

- Track 0's decision record settled this ADR's contracts before drafting;
  distilled into this ADR and the milestone retrospective
  (`docs/milestone-retrospectives/2026-08-04-schedule-d-inbound-loss-carryovers.md`),
  not retained separately.
- Plan:
  `docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md`
- IRS authority: 2025 Instructions for Schedule D (Form 1040), Capital Loss
  Carryover Worksheet—Lines 6 and 14 (carryovers from 2024 to 2025)
- Builds on: ADR-0003, ADR-0006, ADR-0010, ADR-0036, ADR-0038, **ADR-0057**,
  **ADR-0058**, **ADR-0059**
- Companion: **ADR-0059** (prior-return authority, completeness, correction)
