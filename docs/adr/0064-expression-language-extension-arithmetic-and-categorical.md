# ADR 0064 — Expression-Language Extension: Arithmetic and Categorical Collection

- Status: **accepted** (Track 1 and 6b of `f1098e-student-loan-interest-agi`)
- Tier: 2 — contract/architecture choice for schema shape and evaluator behavior.
- Date: 2026-08-16

*(Note: Re-numbering this ADR at merge time is expected and acceptable practice in this repository due to concurrent unmerged work.)*

## Context

The Student Loan Interest Deduction Worksheet requires arithmetic operations (`multiply` and `divide`) to compute the phaseout ratio and the deductible amount. Additionally, Form 1098-E's eligibility logic requires verifying per-statement categorical witness properties across a multi-statement family without order-dependence (Track 6b repair).

## Decision

1. **Additive Extension, Not an Amendment.** This is a genuinely additive extension to the `rule-artifact.v6` expression language. It is **not** an amendment to ADR-0025; ADR-0025's decision list is silent on arithmetic operations and categorical-collection operators.
2. **Arithmetic Operators.** Added `multiply` and `divide`. `divide` is defined with a `min_decimal_places` floor on the ratio's precision and a `rounding` mode, categorically distinct from the whole-dollar `round` operator. This is evidenced by `tests/derivation/test_multiply_divide.py`.
3. **Categorical Collection.** Added `collect_categorical_all_equal` to read every current finding for a fact type from marshalled source rows directly and require all of them to match an expected category. This replaces unkeyed `ref` usage for multi-member universal witnesses, making the evaluation order-independent. Evidenced by `tests/derivation/test_collect_categorical_all_equal.py`.
4. **Implementation.** These operations are live and utilized by the `tax.us.2025.rule.sli-worksheet` (`packages/content/tax/2025/rule.sli-worksheet.json`) and its sibling `packages/content/tax/2025/rule.sli-worksheet-line1-subtotal.json`.

## Consequences

- `rule-artifact.v6` now carries a stable, general-purpose arithmetic pair
  (`multiply`, `divide`) alongside the existing `add`/`subtract`/`max`. Any
  future rule needing a ratio or a product (a phaseout fraction, a
  proration, an allocation split) can use these ops directly instead of
  inventing a new one; `divide`'s `min_decimal_places`/`rounding` contract
  is now the corpus's one way to express a non-whole-dollar quotient,
  distinct from the whole-dollar `round` operator.
- `collect_categorical_all_equal` is now the corpus's one way to express a
  "no member disagrees" universal test over a multi-member fact family
  read from marshalled source rows. Any future rule needing a categorical
  (non-numeric) multi-member universal witness — not just Form 1098-E's
  per-statement eligibility flags — can use this op rather than relying on
  unkeyed `ref`, which Track 6b showed is order-dependent and silently
  drops disagreeing members.
- `collect` itself is untouched: it still force-coerces every row to
  `Decimal` via `_as_decimal` and remains the corpus's numeric-aggregation
  op. `collect_categorical_all_equal` is a genuinely separate op, not a
  mode flag on `collect`, so existing `collect` call sites keep their
  current coercion behavior with zero risk of a categorical row silently
  reaching a numeric fold.
- Both ops are additive to `rule-artifact.v6`; `rule-artifact.v4`'s bytes
  and every rule pinned to it are unaffected. No existing rule's computed
  value changes as a result of this ADR.
- Future work that needs a third arithmetic shape (e.g. exponentiation, a
  running average) or a partial-match categorical test (e.g. "at least one
  member equals," not "all members equal") is not covered by this
  decision and needs its own additive op, following the same pattern.

## Alternatives considered

- **Extend `collect` to tolerate categorical values instead of adding
  `collect_categorical_all_equal`.** Rejected. `collect`'s force-coercion
  of every row through `_as_decimal` is relied on by every existing
  numeric-aggregation call site in the corpus; weakening or branching that
  coercion to accept non-numeric rows would be a silent behavior change to
  an already-shipped op, not an additive one. A new, separate op keeps
  `collect`'s contract exactly as it is.
- **Auto-fold unkeyed `ref` reads universally in `packages/derivation/
  marshal.py` so a multi-member family resolves to a single agreed value
  without a dedicated evaluator op.** This is the owner's own disposition
  on the Track 6b repair (milestone plan, "## Tracks", Track 6b,
  disposition (D)): "do NOT make unkeyed refs auto-fold universally —
  that would be new semantics needing an ADR; refusing ambiguity does
  not." That disposition is not re-litigated here; it is the reason the
  fix for the categorical universal-witness case is a new evaluator op
  (this ADR) plus a narrower `marshal.py` disagreement guard (Track 6b,
  no ADR needed), rather than a change to unkeyed-ref semantics itself.
- **A generic `divide` with no precision/rounding contract, deferring
  rounding to the caller.** Rejected: the Student Loan Interest
  Worksheet's phaseout ratio has an IRS-specified decimal-places floor,
  and leaving rounding ad hoc per call site would let two rules compute
  the same ratio to different precision. `divide`'s
  `min_decimal_places`/`rounding` parameters make that contract explicit
  and checkable, mirroring `round`'s own explicit `rounding` mode rather
  than inventing a second, looser convention.

## Links

- Track charter: milestone plan
  `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md`,
  "## Tracks", Track 1 (`multiply`/`divide` and `rule-artifact.v6`) and
  Track 6b (owner disposition (A)-(E), quoted above for (D)).
- Prior expression-language decisions: ADR-0024, ADR-0025 (declared
  optional defaults and categorical comparison; silent on arithmetic and
  categorical-collection ops, per Decision 1 above).
- Evaluator: `packages/derivation/evaluator.py` (`multiply`, `divide`,
  `collect`, `collect_categorical_all_equal` dispatch).
- Schema: `rule-artifact.v6` (additive successor to `rule-artifact.v4`).
- Tests: `tests/derivation/test_multiply_divide.py`,
  `tests/derivation/test_collect_categorical_all_equal.py`.
- Content: `packages/content/tax/2025/rule.sli-worksheet.json`,
  `packages/content/tax/2025/rule.sli-worksheet-line1-subtotal.json`.
