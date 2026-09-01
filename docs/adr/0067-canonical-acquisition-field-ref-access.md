# ADR 0067 — Direct Per-Item Field-Ref Access for Canonical Object-Valued Facts

- Status: **accepted**
- Tier: 2 — sets the extraction pattern every downstream seam of the
  Document and Ordinary-Fact Translation Vertical (identity association,
  supportability, rule-owned consequences) reads a canonical scalar
  through; not a product-thesis or governance-meaning decision.
- Date: 2026-08-28

## Context

A tax rule needs a scalar amount — `accrued_interest_paid_to_seller` —
that lives as one property on an object-valued acquisition fact. Three
mechanisms could expose it to a rule: project it at runtime into a
separate scalar collectible family; publish it as a second, explicitly
derived numeric finding; or let a rule read the field directly off the
fact already bound to it. The first two both mint a second citizen purely
to re-expose a value the object-valued fact already carries, doubling the
correction-and-supersession surface for no case this milestone's
translation set requires. Direct field access is adopted.

## Decision

1. **No new evaluator op, no new collectible family, no second published
   finding.** `packages/derivation/evaluator.py`'s `ref`/`collect` ops and
   `packages/derivation/marshal.py`'s scalar-symbol resolution are
   extended, not replaced.
2. **A `field` selector on `ref_expr`.** A rule's `ref` node may carry an
   optional `field: string` alongside its existing `name`, naming a
   property on the bound fact type's `value_schema`. When present, the
   marshalled symbol resolves to `finding.value[field]` off the currently
   bound finding (the same finding `ref` already resolves against),
   flowing through the existing scalar path unchanged from that point
   forward — no new symbol kind, no new dependency-tuple shape beyond
   naming the field.
3. **`rule-artifact.v7`, an additive schema successor.** The prior
   schema's `ref_expr` shape (`{"op":"ref","name":string}`,
   `additionalProperties:false`) has no room for a `field` key. `v7`
   widens `ref_expr` to `{"op":"ref","name":string,"field"?:string}`,
   preserving `additionalProperties:false` — bounded, additive growth to
   one schema's one node shape, not a broader expression-language change.
4. **Fail-closed field validation is a load-time obligation.** Package
   validation (`packages/derivation/package_validation.py`) rejects, at
   load time, any `field` naming a property absent from the bound fact
   type's `value_schema.properties`, with a distinct, citable error
   (`FIELD_REF_UNKNOWN_FIELD`) — never a silent `None`/zero flowing
   through evaluation.
5. **Provenance follows the real `pins_for` shape.** The field reference
   is derived as part of the existing expression-tree dependency walk; a
   citation/explanation walk that reaches a field-ref-derived value
   terminates at the same finding-id pin any other `ref` produces, with
   the field name recoverable from the rule artifact's own declared
   `ref_expr`, never a new provenance field.
6. **Hostile-scalar and correction behavior inherit unchanged.** Because
   resolution reads whichever finding is currently bound (the same
   binding `ref` already uses), an independently asserted, unrelated
   scalar fact cannot be picked up by this mechanism, and a correction to
   the acquisition fact's value is visible the next time the same binding
   is marshalled, with no separate cache to invalidate.

## Production conditions (owed to production implementation; never allowlisted)

None outstanding. `tests/derivation/test_rule_artifact_v7_field_ref.py`
covers the hand-written `rule-artifact.v7` positive and negative
instances (correctly-spelled field-ref, misspelled field, a `field` on a
`ref` bound to a fact type with no `value_schema.properties`, a `field`
combined with a bound scalar fact type), multi-acquisition scale (a
binding that could resolve against more than one live acquisition
finding leaves the symbol unbound, matching `marshal.py`'s existing
disagreement behavior), and the hostile-substitution guard on
`marshal.py`'s legacy fallback binding path.

## Consequences

- Identity association and rule-owned consequences charter against a
  real, evidence-backed value-extraction mechanism.
- A future object-valued canonical fact with a single scalar member a
  rule needs to read repeats this field-ref pattern rather than reaching
  for a projected-scalar-family or explicit-derived-finding substrate,
  unless a source needs more than field-level access (computing over
  multiple fields, or fan-in aggregation across a member set) — a future
  decision, not resolved here.
- `rule-artifact.v6` remains valid, immutable history; `v7` is additive.
  No existing rule artifact is edited or reinterpreted by this decision.

## Alternatives Considered

- **Runtime projection into a scalar collection.** Rejected: requires a
  new collectible family and closure mapping per object-valued source,
  disproportionate to a single-field read, and produces a second,
  derived scalar fact whose relationship to the original would itself
  need a provenance story this design gets for free from the existing
  `ref`/pin path.
- **An explicit rule-produced numeric finding.** Rejected: publishes a
  second finding purely to re-expose a value the object-valued fact
  already carries.
- **Treating the schema change as unnecessary ("marshal-layer only").**
  Rejected: the real, unmodified prior schema rejects the widened
  `ref_expr` shape outright before any marshal-layer code would run.
