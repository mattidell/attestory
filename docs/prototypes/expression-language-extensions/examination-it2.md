# Examination — expression-language extensions, iteration 2

## ELX-P1 — declared optional scalar default: settled-at-static-level

The design is settled for a scalar, `determinable` fact whose v2 fact-type
declares one exact adopted parameter default.  It does not default an elective
fact, so Article 3/E3.1 remain intact.

The proposed v2 binding resolves current assertion first and otherwise
publishes a marked default-resolution derived finding for the same `fact_id`.
It pins the default parameter; consumers pin `origin: declared_default` or
`origin: assertion`.  A later assertion is an ordinary correction answer to
that fact, and the existing derivation edges then displace the default's
derived consumers.  There is no third edge, stored currency, runner policy,
or mutation of an assertion.

This defeats the recorded workarounds: no multi-publisher staging or output
conflict is used; no scalar becomes a closure-backed collection; and no guard
short-circuit or scheduling order determines whether the default applies.

Evidence by required case:

* **Case 1:** an absent age flag resolves to the adopted false parameter for
  Single and MFJ; elective defaulting and an invalid default parameter reject.
* **Case 2:** the full trace names all initial pins and six derivation edges.
  Later `A-age-true` corrects `D-age0`, displacing `D-std0`,
  `D-taxable0`, and `D-tax0`; rerun uses assertion pins only.
* **Case 3:** explicit false produces the same amount as case 1 but pins the
  assertion and emits no default; required absence still blocks.
* **Case 4:** categorical guards use the normal assertion lineage and do not
  affect default precedence.
* **Case 5:** only the declared optional binding defaults; absent AGI or
  filing status still records `DEPENDENCY_ABSENT`.

Production conditions are mixed-family correction-fold validation, pin-origin
schema validation, two-runner parity, and synthetic assert-after-run fixtures.

## ELX-P2 — categorical comparison: settled-at-static-level

The design adds closed `categorical_compare` and `category_literal` expression
forms, plus one `operation-semantics.v2` citizen.  Its domain is an existing
fact type's declared string enum; package validation requires both operands to
resolve to that same domain.  Decimal `compare` remains numeric-only.

Known domain mismatch is a contained package-member validation issue.  At run
time, an enum-invalid assertion blocks as `DEPENDENCY_INVALID` and a different
categorical/numeric domain blocks as `CATEGORICAL_DOMAIN_MISMATCH`; no value is
published and the run record preserves the rule/read pins.

Evidence by required case:

* **Case 1:** defaulted age does not alter categorical typing.
* **Case 2:** assertion after default retains normal input lineage into any
  categorical downstream guard.
* **Case 3:** an explicit false is still an asserted, typed scalar.
* **Case 4:** `married_filing_jointly` matches and `single` does not without
  decimal coercion; numeric-domain mismatch and enum-invalid `MFJ` contain.
* **Case 5:** missing required filing status blocks; a literal cannot invent it.

ADR-0024 numeric strings migrate only through a versioned code-to-label
migration artifact, presented successor claim, user assertion, and ordinary
fact succession.  New categorical rules reject legacy bindings; they do not
dual-read or silently coerce them.

## Unresolved authority questions

None block these bounded designs.  Defaults for elective facts and automatic
conversion of an asserted legacy code remain expressly unresolved and out of
scope; each would need its own Article-3 or Article-2 decision.
