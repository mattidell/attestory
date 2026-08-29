# Clean-Room Review — Round 1

Reviewer: independent, cold-read of `charter-it1.md`, `charter-it2.md`,
`examination-it1.md`, `examination-it2.md` only. No commit-history reading
beyond locating files.

## Legibility verdict, it1

A fresh reader recovers all four items from the charter + examination alone:

- **(a) Mechanism.** Concrete: a `requires`/`pins` entry names
  `{fact_type, field}` instead of a bare symbol; package validation
  statically checks `field` against `value_schema.properties`; marshal
  resolves the current finding at the bound identity, reads `value[field]`,
  and binds a synthetic symbol `<fact_type_id>#<field>` through the
  existing scalar `ref` unchanged. No evaluator op is added.
- **(b) Six cases.** All worked through with concrete fixture values
  (identity `B1/S1/T1/2025`, `42.50`→`45.00` correction, missing optional
  field on `B2/S1/T2/2025`, typo `accrued_interest_paid_to_seler`).
  Traceable without guessing.
- **(c) Grounding vs assertion.** Cited to real paths: `evaluator.py`
  (`env.symbols` flat map, no field descent), `runner.py`
  (`InputFinding.value: Any`), and ADR-0054 (verified real; its "Option A"
  rejection is accurately characterized). One gap: the claim that
  `package_validation.py` "can" check `field` against
  `value_schema.properties` is a proposed extension, not something read out
  of that file today — the doc calls case 6 unsettled but does not
  explicitly flag that the *same* not-yet-built check underlies its
  "settled" calls elsewhere.
- **(d) Settled/rung-2 calls.** Five of six "settled at paper" with
  reasoning tied to cited, existing mechanisms (flat-symbol `ref`,
  `DEPENDENCY_ABSENT`, correction fold, pin-shape granularity). Case 6 is
  correctly flagged unsettled with a falsifiable question, matching Gate
  3's own designation. Well-reasoned, not merely declared.

Candidates A and B are worked for cases 2 and 6 only, as required, each with
a genuine distinguishing argument (A's "computed-only enforcement" gap on
case 2; B's extra machinery for no case-2 benefit over C).

## Legibility verdict, it2

Equally recoverable, with sharper grounding discipline:

- **(a) Mechanism.** Same concrete shape via a named successor schema:
  `rule-artifact.v7`'s `ref_expr` adds optional `field`; dict operand
  required if set; missing key raises `DEPENDENCY_ABSENT`; package
  validation checks `field` against the bound fact type's
  `value_schema.properties`, else `MEMBER_SCHEMA_INVALID`.
- **(b) Six cases.** Worked with a self-consistent fixture
  (`demo.tax.2025.acquisition`, findings `.acq.1/2/3`, hostile type
  `demo.tax.2025.accrued-interest-scalar`).
- **(c) Grounding vs assertion.** More densely and more carefully cited:
  `evaluator.py` (`_as_decimal` on a dict raises `DEPENDENCY_INVALID`, never
  zero), `marshal.py`, `runner.py` `pins_for` (pins are to finding ids, not
  fields — honestly used to explain case 5's real limitation: field-level
  provenance without a pin-schema field slot), and `package_validation.py`
  confirmed to have **no** field-name check today, "because `ref` has no
  `field`" — the document is explicit that the mechanism does not exist yet
  everywhere, not only for case 6. It also names that today's `v6` schema's
  `additionalProperties: false` would reject the `field` key itself (the
  wrong failure mode), a precision it1 does not surface.
- **(d) Settled/rung-2 calls.** Same five-settled/one-rung-2 pattern;
  reasoning is comparably strong and, on case 6, sharper about what "wrong
  failure" would look like against the real schema.

Discipline about "exists today" vs "proposed" is maintained consistently
across all six cases here, not just case 6.

## Convergence analysis

Both documents converge on the same concrete mechanism, not a shared label
with different meanings:

- Same schema move: add an optional `field` to `ref` (it1: `requires`/
  `pins` entry; it2: `rule-artifact.v7` `ref_expr` — same idea, different
  vocabulary for the binding site).
- Same runtime move: read `value[field]` off the *current* bound finding,
  no separate lookup, no second published finding.
- Same failure semantics on all six: hostile scalar excluded by type/
  identity key (not by preference among values); missing field is
  `DEPENDENCY_ABSENT`, never zero; correction flows through the existing
  fold; provenance is field-level via the expression tree, not a new
  pin-schema slot; case 6 is the one case both refuse to settle at paper,
  for the same reason (today's schema/validator do not yet perform the
  field-name check).
- Both reject candidate A for the same structural reason (marshal-side
  projection reinvents type-keyed isolation the object fact type already
  gives for free, risking a hostile scalar entering a shared slot) and
  candidate B for the same reason (duplicates the field name in a second
  citizen for no case-2 gain over C).

Strongest evidence of real convergence: both independently identify the
*expression schema itself* as the blast-radius point — it1's
`{fact_type, field}` pin entry and it2's named `v6`→`v7` `ref_expr`
successor are the identical code change described at different levels of
schema-version precision. it2 is more precise (names the schema version and
the exact reason `v6` cannot express the field), but the two are describing
one change.

The measurable difference is rigor, not conclusion: it2 states plainly, for
every case, whether the needed check exists in `package_validation.py`
today (it does not); it1 asserts by analogy ("same static check as A and
C") without confirming an existing field-check code path.

## Overall statement

A reader relying only on these documents can safely conclude: **both
builders independently selected direct per-item rule access (candidate C /
candidate (c)) for load-bearing reasons** — identical mechanism, identical
failure semantics on all six cases, and the identical single case
(misspelled declaration) correctly left open for a rung-2 climb. This is not
a same-words-different-meaning outcome; the schema-level description (`ref`
gains an optional `field`, checked against `value_schema.properties`,
resolved off the current bound finding) matches down to which existing code
paths are reused (`env.symbols`, `DEPENDENCY_ABSENT`, the correction fold)
and which are deliberately not touched (no new evaluator op, no collectible
family, no second published finding).

Carry-forward for the adversarial/eligibility round: confirm whether it1's
"settled at paper" calls for cases 1/3/4/5 implicitly lean on the same
not-yet-built validation check it1 itself flags as unsettled for case 6, or
whether those cases are genuinely independent of that gap.
