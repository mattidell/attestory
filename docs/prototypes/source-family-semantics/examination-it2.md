# Examination — Source-Family Semantics, Iteration 2

Date: 2026-07-12

Charter: `charter-it2.md`

Evidence rung: paper only; no code or production contract was built.

## What was tested

The design tested whether a closure claim, its member universe, an adopted
mapping, a calculation consumer, and a coverage consumer can retain one
recoverable meaning when a Form 1099-INT box-1 subtotal is adjacent to taxable
interest and Form 1040 line 2b.

The paper examples use only synthetic Demo Payer statements and synthetic
labels. They treat documents as evidence, not fact identities.

## Measurements against the charter

| Required measurement | Result |
| --- | --- |
| No forms/no interest | A closed box-1 family yields only a box-1 zero; an independent taxable-interest family remains required for line 2b. |
| Two box-1 statements, one payer | Two statement-item members remain distinct; payer identity cannot collapse them. |
| Taxable interest without Form 1099-INT | This counterexample proves box-1 is not coextensive with taxable interest. |
| One form, box 1 and box 3 | A form is not the family: box 3 is outside the box-1 member predicate, whatever a future tax mapping decides. |
| Late statement after zero | Closure withdrawal/displacement removes the prior zero from current state; an explicit rerun alone can publish a successor. |
| Narrow closed/broad open | The narrow subtotal stays valid and coverage-complete for its own family while line 2b remains blocked. |
| Two positives | Two-statement aggregation; narrow-complete/broad-open composition. |
| Two negatives | Non-form interest rejects line-2b zero; box-3-on-the-same-form rejects form-level closure. |
| Lifecycle | Closure → zero → late discovery → withdrawal/displacement → assertion/closure → rerun is stated in `it2/design.md` §5. |
| Failure map | Claim → members → mapping → calculation → coverage → failure is stated in `it2/design.md` §3. |

## Findings

### SFS-P1 — settled

A source-family closure must assert completeness of one named closure domain.
The family membership predicate, its fact questions, mapping input, and
coverage observation all use that domain. A calculation can publish that
family's subtotal, but a broader calculation must name an explicit composition
of families. This prevents a document-family closure from acquiring tax-concept
authority merely because a downstream rule is convenient.

### SFS-P2 — settled

Box-1 statement items (`B1`) and taxable-interest facts regardless of source
(`TI`) are distinct in the charter's non-form-interest case. Form 1040 line 2b
(`L2B`) is a result, not either source universe. Therefore a closed `B1`
family authorizes a closed box-1 subtotal (including zero) and **no line-2b
result**. A future line-2b zero needs a declared and closed `TI` universe (or a
proven coextensive composition) plus its own rule guard.

## Rejected rival alternative

Treating “all 1099-INT documents” as a tax-interest closure fails: it emits a
false line-2b zero for non-form interest, cannot state what a box-3 item means,
and risks collapsing two same-payer statement items. Adding exceptions simply
creates an undeclared second family.

## Scope stop

This iteration stops at paper semantics. It does not specify extra boxes,
manual-entry product design, UI copy, Schedule B, production identifiers,
schemas, coverage persistence, resolvers, or implementation. Reviewers should
test the stated universe-alignment invariant and the six cases, not expand the
taxonomy.
