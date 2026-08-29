# Case 6 Rung-2 Spike: Misspelled Field Fails Closed

Rung: 2 (throwaway validator exercise against a real, synthetic package
fixture, per `plan.md` Gate 3). Answers the single question that justified
climbing past paper (`examination-it1.md` "Rung disposition per case",
`reviews/adversary-r1.md` "Rung-2 recommendation", `reviews/eligibility-r1.md`
Gate 6): does the real schema-validation mechanism actually reject an
unknown `field` name in a widened `ref_expr`, distinct from today's
`additionalProperties: false` masking gate?

## What was built

All under `docs/prototypes/canonical-value-extraction/spike/`, nothing
under `packages/`:

- `rule-artifact.v7.schema.json` — a draft, spike-local copy of the real
  `packages/schemas/derivation/rule-artifact.v6.schema.json`, widening only
  `ref_expr` to `{"op":"ref","name":string,"field"?:string}` with
  `additionalProperties: false` preserved. Not a real schema version bump;
  never written to `packages/schemas/`.
- `published.json` — checksum manifest for the spike schema, required by the
  real `SchemaRegistry` loader (`packages/kernel/schema_registry.py`).
- `case6_spike.py` — imports and drives the real, unmodified
  `packages.kernel.schema_registry.SchemaRegistry`/`SchemaValidationError`
  (the mechanism `packages/derivation/loader.py`'s `DerivationSchemas` wraps
  and `package_validation.py`'s `validate_package` calls as
  `schemas.validate_declared`), plus a narrowly-scoped
  `check_field_ref_bindings` semantic check written in
  `package_validation.py`'s own style (walking `value_schema.properties`,
  as `_is_yes_no_domain` does), since no field-existence check exists in
  production today (confirmed by `reviews/adversary-r1.md` reading
  `validate_package`'s `input_bindings` section).

## Command run

`python3 docs/prototypes/canonical-value-extraction/spike/case6_spike.py`

## Evidence

Four assertions, all passed:

1. **Baseline** — the real, unmodified `rule-artifact.v6` schema
   (`packages/schemas/derivation/rule-artifact.v6.schema.json`, untouched)
   rejects a `ref_expr` carrying `field` at all, correctly-spelled or not:
   `SchemaValidationError` on "is not valid under any of the given schemas".
   Reproduces the committee's diagnosis against real code, not prose.
2. **Draft v7 schema-level acceptance** — the spike's `rule-artifact.v7`
   registry (real `SchemaRegistry`, spike-local schema file) accepts the
   widened `ref_expr` shape for *both* `accrued_interest_paid_to_seller`
   and the misspelled `accrued_interest_paid_to_seler`. Expected: schema
   shape alone cannot distinguish a real field from a typo — the gap case 6
   is about — confirming the semantic check below is a separate, necessary
   phase, not something a v7 schema bump alone supplies.
3. **Positive case** — `check_field_ref_bindings` accepts
   `accrued_interest_paid_to_seller` against the synthetic
   `tax.us.2025.acquisition.bond-purchase` fact type's
   `value_schema.properties` (which does list it).
4. **Negative case** — `check_field_ref_bindings` raises
   `FieldRefValidationError` (`FIELD_REF_UNKNOWN_FIELD`) for the misspelled
   `accrued_interest_paid_to_seler`, naming the offending citizen, the bound
   symbol, and the known property set. It never returns `None`/zero or lets
   the citizen load silently.

Full run output:
```
PASS baseline: real unmodified rule-artifact.v6 rejects any `field` key on ref_expr (correct or misspelled alike) — value: {...} is not valid under any of the given schemas
PASS: draft rule-artifact.v7 schema accepts the widened `ref_expr` `field` key at the schema-validation stage for both a correctly-spelled and a misspelled field name (schema alone cannot tell them apart — this is the gap case 6 asks about).
PASS positive: correctly-spelled field 'accrued_interest_paid_to_seller' accepted by the semantic value_schema.properties check.
PASS negative: misspelled field rejected at load time — tax.us.2025.rule.scheduleb-adjustment.accrued-interest-from-acquisition: field-ref names 'accrued_interest_paid_to_seler' on 'tax.us.2025.acquisition.bond-purchase', which has no such property in its value_schema (known: ['accrued_interest_paid_to_seller', 'purchase_price', 'quantity', 'trade_date']) [FIELD_REF_UNKNOWN_FIELD]
All case-6 rung-2 assertions passed.
```

## Incidental design refinement (not a new decision)

The fixture uses `requires: ["tax.us.2025.acquisition.bond-purchase"]` (a
bare fact-type-id string, schema-legal under v6/v7 unchanged) rather than
it1's `{fact_type, field}` object entry, putting `field` on the `ref` node
instead (it2's syntax, endorsed by both `reviews/adversary-r1.md` and
`reviews/clean-room-r1.md`). This binds via `marshal.py`'s existing "symbol
== fact type id" legacy fallback path (~326-380), so `requires`'s schema
type needs no growth — only `ref_expr` does. Not a new decision; confirms,
against real code, which converged paper's syntax is schema-cheaper, per
Gate 6's CV-P2 framing ("growth is real but bounded").

## Conclusion

Case 6 is now settled for CV-P1: a widened `ref_expr.field` on a `v7`
successor schema, paired with a load-time `value_schema.properties` check in
the style `package_validation.py` already uses elsewhere, demonstrably fails
closed against the real schema-validation mechanism — a misspelled field
never reaches marshal or evaluation, and never resolves to a silent
`None`/zero. Gate 6's floor for Seam 1 ("CV-P1's mechanism selection, with
fail-closed behavior demonstrated against the real rule loader") is met.
What remains before Gate 7 production adoption is exactly what
`reviews/eligibility-r1.md` already enumerated (schema version boundary,
validation obligation, runtime resolution contract, provenance/citation
shape, CV-P2's bounded-not-zero growth, explicit non-adoption of A and B) —
none of which this spike needed to resolve, since it was scoped to case 6
only.
