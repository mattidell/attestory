# Adversarial Review — Round 1: Canonical Value Extraction (Seam 1)

Reviewer: adversarial committee seat. Attacked `examination-it1.md` and
`examination-it2.md` (branches `prototypes/canonical-value-extraction/it1`,
`.../it2`) with equal effort against the six named cases, reading real code
under `packages/derivation/`, `packages/kernel/`, `packages/schemas/derivation/`
rather than trusting either paper's prose.

## Top-line

Both recommend candidate C (direct per-item access); the recommendation
itself is genuine convergence. But the two ground it differently, and it2's
grounding is measurably more accurate about real code. Case 6 is **not
settled** by either paper and the real code confirms why in a specific,
checkable way: no field-name check exists anywhere today, and the schema
gate that would run first (`ref_expr`'s `additionalProperties: false`)
rejects the mechanism itself, correct or misspelled alike — a different
failure than case 6 asks about.

## Case 1 — Authoritative amount

Both settle this correctly. Neither mechanism exists in code yet
(`evaluator.py`'s `ref` returns `env.symbols[name]` verbatim, confirmed —
no field descent), so "authoritative" is a design claim about a proposed
successor, not an enforced behavior today. Both papers say this honestly.
Not a defect at rung 1, but worth naming plainly: asserted, not enforced.

## Case 2 — Hostile independently-asserted scalar

Traced `marshal.py`'s `build_run_context` (~line 250-380): a normal
`input_bindings` entry binds by `(symbol, fact_type_id)`; a different
fact-type id cannot enter that lookup — confirmed, no aliasing path for two
distinct fact types to collide on one symbol.

Found a nuance neither examination raises: the same file has a live
**legacy fallback path** ("symbol == fact type id", ~line 326-380) that
binds any unbound current finding whose fact-type id equals a symbol some
rule `requires`. It still keys strictly by fact-type id, so it does not
break either candidate's case-2 claim, but a rule author who declares
`requires` naming the raw object fact-type id (instead of the intended
field-ref binding) would hit this path, bind the whole object, and a bare
`ref` read of it raises `DEPENDENCY_INVALID` on `_as_decimal` of a dict
(confirmed) — safe, but neither paper traces this adjacent path. Both
papers' "does not silently prefer a hostile value" claim is demonstrated
only for the intended lookup key, not for every way a package could reach
the object fact. Non-blocking.

## Case 3 — Correction

`marshal.py` always resolves against `currency.current_finding_ids`
(confirmed at the call site) — no cached scalar exists to go stale, because
neither candidate persists a second artifact between the object fact and
the reading rule. Downstream displacement is the ordinary ADR-0010 pin
fold, unmodified. Genuinely settled by both, correctly traced to real code.

## Case 4 — Missing field

Confirmed `_as_decimal(dict)` raises `DEPENDENCY_INVALID`, never 0/None —
an object read without field descent already fails closed today. But the
proposed field-ref op doesn't exist, so its own "missing key ->
`DEPENDENCY_ABSENT`" claim is a design commitment, not demonstrated code.
it2 states this with that caveat; it1 states it as settled without one.
No evaluator path today could silently resolve this to 0/None — but only
because the feature doesn't exist yet, not because it was tested.

## Case 5 — Exact provenance

`runner.py`'s `pins_for` pins are `{role, id, version, origin}` to
**finding ids**, not fields (confirmed) — today's pin tuple is object-level.
it2 correctly derives field-level provenance from re-opening the pinned
rule's own expression tree ("expression-as-locator"); it1 instead asserts a
`{fact_type_id, identity, finding_id, field}` pin shape as if it already
exists or is trivially added — not grounded in `runner.py`'s actual tuple.
A real, not superficial, difference: it1's design sketch is imprecise about
where the field name is actually recorded.

## Case 6 — Misspelled declaration failing closed (settling attempt)

Read `package_validation.py` in full and
`rule-artifact.v6.schema.json` directly.

- **No field-name check exists anywhere today.** `validate_package`'s
  `input_bindings` section (~line 1049) checks a bound fact type is in the
  fact surface and that `optional_default` names a real parameter; it has
  no sub-field concept, because `rule-artifact.v6` has none.
- **The current schema rejects the mechanism itself before any semantic
  check could run.** `ref_expr` is `{"op":"ref","name":string}` with
  `additionalProperties:false` (confirmed). Any `field` key on a `ref`
  node — correct or misspelled — fails `PACKAGE_SCHEMA_INVALID` at the
  first `schemas.validate_declared(citizen)` call, before reaching any
  candidate-specific logic. **it2 states this precisely** ("v6 `ref` would
  reject the `field` property itself... wrong failure: cannot express the
  mechanism"). **it1 does not state this at all.**
- it1's mechanism instead lives in `requires`/`pins` entries naming
  `{fact_type, field}`, but `rule-artifact.v6`'s `requires` is declared
  `{"type":"array","items":{"type":"string"}}` (confirmed, line 12) — a
  plain string array. An object entry there is equally schema-rejected
  today, for the identical reason, and it1 never names this gap or the
  schema-version bump it implies. it1's claim "no expression-language
  growth... a marshal/package-validation-layer addition only" is not fully
  supportable: widening `requires` from homogeneous strings to a
  string-or-object union is itself schema-language growth.
- **Verdict:** neither design is settled against real code, and both
  correctly say so. it2's account of *why* is more accurate and more useful
  for the rung-2 climb: it correctly predicts a naive build collides with
  an *existing* fail-closed gate for the wrong reason, and names the real
  rung-2 question (does the *new* field-existence check fire once the
  schema is widened, distinct from the old shape gate that would otherwise
  mask it). it1's target design (a static `value_schema.properties` walk,
  illustrative `FIELD_REF_UNKNOWN_FIELD`) is reasonable but glosses over its
  own syntax choice being schema-incompatible today, the same way it2 flags
  for `ref`.

## Superficial-convergence findings

1. **Case 5:** same conclusion, materially different and not-both-correct
   reasoning — it1's pin-schema shape isn't grounded in `runner.py`'s
   actual tuple; it2's expression-tree derivation is.
2. **Case 6 syntax:** it1 puts the field binding in `requires`/`pins`; it2
   puts it in `ref`. Both are schema-incompatible today in the same way,
   but only it2 says so — same recommendation, only one side's reasoning
   survives contact with the real schema.
3. **Scale gap neither addresses:** both fixtures model one acquisition per
   rule. `marshal.py` binds one symbol to "one current finding," refusing
   when multiple current findings of the same fact type disagree (Track 6b
   guard, ~line 264-291). Neither works through several bond purchases
   needing independent extraction in one run — not one of the six named
   cases, but downstream seams "read whatever value shape this seam
   selects" per `plan.md` Gate 1. Flagged as a production condition, not
   decision-blocking here.

## Rung-2 recommendation

Build a throwaway `rule-artifact.v7` fixture package that widens `ref_expr`
to admit an optional `field` and adds the missing `value_schema.properties`
check in `package_validation.py`, then run a misspelled-field fixture
through the real loader and confirm rejection. Until that exercise runs,
case 6 is correctly unsettled by both papers; treat neither's illustrative
code as evidence.
