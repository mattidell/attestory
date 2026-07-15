# Charter: Scoped Confirmation — ADR-0028 Decision 7 (Same-Quantity Force-Declare)

Date: 2026-07-15. **Not** a full builder round. Owner-launched **Medium Adversary**
confirmation after foreman retype of decision 7 (post `review-feedback-adr0028.md`).

## Purpose

Decision 7 was retyped post-committee without a re-test. Confirm the **trigger
boundary in both directions** before ADR-0028 may go to owner ratification.

## Seal / independence

**Do not read** any draft residual ADR text beyond the decision-7 wording quoted
in this charter (or the current decision 7 in `docs/adr/0028-…` if needed for
exact predicate). Do not re-litigate MR-P1, it2 reject, or non-circular
discoverability (decisions 1–6). Prior reviews may be read for MR-A7 context only.

## The rule under test (normative summary)

Force-declare `S` into `composition_obligations` when the producer of `S` has
≥2 distinct adopted inputs that are **alternative sources/subtotals of `S`'s own
tax quantity** (family `authorizes_subtotal` **or** raw source amounts of that
same quantity). Do **not** force-declare merely because `S` aggregates ≥2 inputs
of **different** quantities.

## Required attacks / cases

1. **Under-trigger still closed (MR-A7):** line-2b-shaped rule as raw
   `add(ELX(box1), ELX(box3), ELX(oid))` (or equivalent same-quantity raw
   amounts), no family pins, no composition_obligations, no composition citizen
   → must **reject** under the retyped rule.
2. **Over-trigger must not fire (line 9):** rule publishing total income as
   line 1a + line 2b (two distinct quantities), no composition_obligations →
   must **accept** (validate) under the retyped rule.
3. **At least one further cross-quantity control** among lines 11 / 15 / 16
   style folds → must **accept** without composition obligation.
4. **Family-subtotal line-2b still force-declares** when ≥2 family
   authorizes_subtotal inputs and obligations omitted → **reject**.

Paper/static only. Classify each result. End with: **confirm** (boundary holds
both ways) / **fail** (name which direction) / **needs redesign** (predicate
still ambiguous).

## Output

`docs/prototypes/adopted-content-manifests/micro-round/reviews/confirm-decision7-adversary.md`

Findings labeled **MR-C1…**. No ADR edits. No git writes. Foreman holds custody.
