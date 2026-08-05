# ADR 0062 — Form 8949 Attachment, Arithmetic, Validation, and Schedule D Lines 1b/8b Composition

- Status: **accepted** (ratified by the owner 2026-08-04)
- Tier: 2 — additive attachment citizen and Schedule D composition
  successor for one breadth slice; reuses existing itemization,
  `collect_members`, and evaluator-op vocabulary without a new schema kind
  or evaluator op.
- Date: 2026-08-04

## Context

ADR-0061 establishes the `covered-w-st`/`covered-w-lt` families and the
Path A/B completeness successor on `no-form8949-sources`. This ADR settles
how those families' proceeds/basis/adjustment scalars become a **Form 8949**
attachment citizen, how column (h) arithmetic and validation are expressed,
and how the box-A/box-D totals compose into successor Schedule D lines
1b/7/8b/15/16/21 and Form 1040 line 7a/9.

Inspected commitments that force explicit decisions:

- `attachment.schedule-d.v4.json` uses `attachment-rule.v4`; the current
  latest schema, `attachment-rule.v6`, is byte-shape-identical to v3–v5
  (only the `schema` const/`$id` differ across versions inspected in
  `packages/schemas/tax/attachment-rule.v{3,4,5,6}.schema.json`) — no new
  schema kind is needed for Form 8949 to be its own attachment citizen.
- `packages/derivation/runner.py`'s `attempt_attachment` produces exactly
  **one subtotal per itemization part** via `collect_members` over a single
  source family; it has no native multi-column-per-row tie-out. The
  existing ST/LT proceeds/basis split (two families, two itemization
  parts, two subtotals) is the direct precedent for representing Form
  8949 columns (d)/(e)/(g) as three single-column parts per box.
- Expression vocabulary already includes `add`, `subtract`, `max`,
  `choose`, `compare` (ADR-0058/ADR-0060); no new evaluator op is needed
  for `h = d − e + g` or for the validation guards below.
- `rule.selected-preferential-base.v3.json` (ADR-0060) branches on
  `any([st_proceeds > 0, lt_proceeds > 0, W8 > 0, W13 > 0])` and must
  extend without disturbing the existing four terms.
- ADR-0058 keeps Schedule D signed through line 16 and floors preferential
  base at the producer; this ADR must not edit that text, only add
  content successors.

## Decision

1. **Form 8949 as its own attachment citizen.** Publish
   `tax.us.2025.rule.attachment.f8949` (schema `attachment-rule.v6`, no
   new schema kind). Two itemization groups, mirroring the existing
   ST/LT split:

   - **Part I, box A** (short-term): three single-column itemization
     parts over `covered-w-st-proceeds`, `covered-w-st-basis`,
     `covered-w-st-adjustment`, each `collect_members`-tying to its own
     subtotal symbol (columns d/e/g). Column (f) is the fixed literal
     `"W"` for every row in this slice (no code vocabulary).
   - **Part II, box D** (long-term): the parallel three parts over the
     `covered-w-lt-*` families.

   Column (h) per box is a **downstream rule**, not itemization output:

   ```text
   box_a_h = box_a_d_subtotal - box_a_e_subtotal + box_a_g_subtotal
   box_d_h = box_d_d_subtotal - box_d_e_subtotal + box_d_g_subtotal
   ```

   using `subtract`/`add`, the same pattern `rule.schedule-d-line1a-gain
   .json` already uses for `(d)-(e)`. `tie_out` on each itemization part
   binds to its own subtotal; a page/part total tie-out compares the
   summed member subtotals against the published box total, the same
   `ITEMIZATION_TIE_OUT_VIOLATION` mechanism every existing attachment
   already uses — no new tie-out kind.

2. **Validation guards (rule content, not schema constraints).** Two
   guards, each a named block/violation code, evaluated per contributing
   transaction before that transaction's amount is folded into a box
   subtotal:

   ```text
   guard_nonloss_adjustment:
     block if (g > 0) AND (d >= e)          # code W on a gain/break-even txn

   guard_adjustment_exceeds_loss:
     block if g > max(e - d, 0)             # adjustment exceeds otherwise-deductible loss
   ```

   `g >= 0` itself is a schema-level `minimum: 0` constraint on the
   ADR-0061 scalar fact type, not a rule guard. Whole-dollar rounding
   follows the existing per-line rounding boundary already applied to
   every other Schedule D/Form 8949-adjacent line — no new rounding
   contract.

3. **Successor Schedule D lines 1b/8b.** New `rule.schedule-d-line1b` /
   `rule.schedule-d-line8b` publish `box_a_h` / `box_d_h` respectively,
   pinning the Form 8949 attachment's tie-out and the underlying box
   subtotals.

4. **Successor lines 7/15.** `rule.schedule-d-line7` (v3) = line 1a (h) +
   line 1b (h) + line 6 (existing carryover). `rule.schedule-d-line15`
   (v4) = line 8a (h) + line 8b (h) + line 13 (box 2a) + line 14 (existing
   carryover). Every existing addend keeps its exact pin; only the new
   1b/8b terms are added. Line 16/21 and Form 1040 line 7a/9 are content
   successors over the recomputed net per ADR-0058 — that text is not
   edited.

5. **`selected-preferential-base` successor (v4).** Extend the branch
   condition to:

   ```text
   any([st_proceeds > 0, lt_proceeds > 0, W8 > 0, W13 > 0,
        box_a_h != 0, box_d_h != 0])
   ```

   preserving every existing term's exact pin. Direct branch remains the
   box-2a-only path when the predicate is false.

6. **Attachment requirement.** `attachment.schedule-d` successor
   (`.v5`) extends the existing threshold any-over subtotal list with
   `box_a_proceeds_subtotal` and `box_d_proceeds_subtotal` (mirroring how
   ST/LT proceeds subtotals already trigger the requirement) — a
   wash-sale-only return with nonzero Form 8949 proceeds honestly
   requires Schedule D even if the direct families are empty.

7. **Explanation and presentation.** Form 8949 rows and box totals join
   the existing citation-walk model (ADR-0046) with new citations
   (`citation.attachment.f8949`, `citation.schedule-d.line-1b`,
   `citation.schedule-d.line-8b`) mirroring the existing line-1a/8a/6/14
   citations. No new presentation mechanism; blocked/missing-authority
   states render through the existing disposition-tagged `attachments`
   model key (ADR-0056).

## Production conditions (owed to Track 1; never allowlisted)

1. `attachment.f8949` content implementing Decision 1, with goldens for
   single-transaction, multi-transaction-aggregated, and box-A/box-D
   coexistence.
2. Guard rules implementing Decision 2 with named block codes; goldens
   for code W on a gain transaction, adjustment exceeding the otherwise-
   deductible loss, and the passing boundary case (adjustment exactly
   equal to the loss).
3. Successor Schedule D lines 1b/7/8b/15/16/21 and Form 1040 line 7a/9
   (Decisions 3–4); goldens for coexistence with existing 1a/8a, box-2a,
   and carryover lines, and downstream net gain / under-cap loss /
   over-cap loss.
4. `selected-preferential-base` v4 (Decision 5) with the full exact pin
   table extended by the two new terms.
5. `attachment.schedule-d.v5` (Decision 6) with a carryover-and-W-only
   and a W-only-no-direct-families golden.
6. Every existing current-year-losses and inbound-carryover regression
   fixture unmodified.

## Consequences

- Form 8949 becomes representable with the project's existing itemization
  substrate — no new schema kind, evaluator op, or tie-out mechanism.
- Column (h) stays an auditable downstream computation over cited
  subtotals rather than itemization output, consistent with every other
  Schedule D line's arithmetic-as-rule-content pattern.
- The validation guards make "code W on a gain" and "adjustment exceeds
  the loss" honestly blocked states rather than silently wrong numbers.

## Alternatives considered

- **New attachment schema kind for multi-column rows.** Rejected: v3–v6
  are shape-identical; the existing single-column-per-part itemization,
  already used for ST/LT proceeds/basis, extends directly to (d)/(e)/(g)
  without a schema gap.
- **New `min`/multi-column evaluator op for column (h).** Rejected:
  `subtract`+`add` already express `d - e + g`; ADR-0058/ADR-0060
  precedent is to compose existing ops, not add new ones for one
  arithmetic shape.
- **Express the adjustment-exceeds-loss guard as a schema constraint on
  the scalar fact type.** Rejected: the bound (`e - d`) is data-dependent
  across two other facts, not a structural property expressible in a
  single fact type's `value_schema`.

## Links

- Track 0's decision record settled this ADR's contracts before drafting;
  distilled here and in the milestone plan.
- Plan:
  `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md`
- IRS authority: 2025 Instructions for Form 8949; 2025 Instructions for
  Schedule D (Form 1040); 2025 Form 8949
- Builds on: ADR-0003, ADR-0036, ADR-0046, ADR-0053, ADR-0056,
  **ADR-0057**, **ADR-0058**, **ADR-0060**, **ADR-0061**
- Companion: **ADR-0061** (transaction authority, family topology,
  completeness successor)
