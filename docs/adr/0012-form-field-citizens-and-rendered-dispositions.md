# ADR 0012 - Form-Field Citizens and Rendered Dispositions

- Status: accepted (ratified 2026-07-11)
- Tier: 2
- Date: 2026-07-11

## Context

First Tax Slice must connect derived symbols to official Form 1040 fields while
remaining honest about zero, incompleteness, invalidity, and inapplicability.
A rule output symbol alone does not identify an official field, carry form-year
lifecycle, bind a citation, or tell a renderer what absence means.

Per ADR-0005, this proposal cites
`docs/prototypes/tax-citizen-families/evaluation-analysis.md`. Both rival
builders independently introduced a form-field companion family, later
iterations instantiated it across the bounded slice, and fresh-reader reviews
consistently recovered the field/symbol distinction and rendered-disposition
vocabulary. The analysis excludes unresolved package, citation-resolver, and
non-publication explanation contracts.

## Decision

1. **An official form field is a first-class versioned content citizen,
   distinct from a derivation output symbol.** The form field declares what an
   official form location means and how a current derivation disposition is
   presented. It never becomes a fact, finding, rule, or authoritative store of
   a rendered value. (Analysis C4.)

2. **A form-field citizen carries the minimum recoverable content:**

   - schema id, opaque citizen id, and immutable content version;
   - issuing authority, form identity, tax/form year, jurisdiction, and precise
     printed locator;
   - human label and description;
   - the exact derivation output symbol it binds;
   - a source-citation reference for the field meaning; and
   - declared rendering and explanation instructions for the dispositions in
     decision 4.

   These fields are content, not identity inference performed by filename,
   package position, or renderer code. Published versions are immutable. A new
   form year, locator, meaning, binding, or rendering contract is represented by
   a new citizen/version under the project's normal schema-version rules.

3. **The field-to-symbol binding is one-way presentation content.** The rule
   publishes a symbol without knowing which official fields may render it. A
   form field references the symbol it presents. The form field does not own the
   derived finding, participate in fact identity, or authorize derivation.

4. **Form-field content distinguishes five disposition classes** (Analysis
   C5):

   1. `published_value` - a published nonzero value;
   2. `computed_zero` - a published numeric zero grounded in present source or
      input findings;
   3. `closure_backed_zero` - a published numeric zero whose lineage includes a
      current affirmative source-set closure finding;
   4. `blocked` - no published value because required state is absent, invalid,
      or otherwise unavailable; and
   5. `guard_inapplicable` - no value exists because the declared rule guard is
      false and the field/branch is inapplicable.

   Machine records may refine `blocked` into absent, invalid, open-source, or
   other schema'd codes. A renderer may use the same glyph for more than one
   blocked subtype, but it must not erase the machine/explanation distinction.

5. **Rendering never invents state.** A renderer selects instructions from the
   form-field citizen using the actual current output/run disposition. It may
   display a number, zero, dash, blank, or other declared representation; it may
   not infer closure from an empty collection, turn a block into zero, render a
   false guard as a computed blank, or reconstruct missing authority.

6. **Zero provenance remains visible.** `computed_zero` and
   `closure_backed_zero` may render the same numeric glyph, but explanation must
   preserve their different lineage. The field content names the distinction;
   the derivation finding and records remain the authority for which disposition
   applies.

## Not Decided

This ADR does not decide:

- the schema or semantics of citation attachment/resolution;
- which adopted manifest contains form fields or citations;
- package/provenance closure across every content family;
- the explanation API for blocked, invalid, or guard-inapplicable fields;
- coverage-family/read-model contracts;
- UI layout, accessibility text, localization, or filing presentation;
- whether one output symbol may be rendered by multiple official fields; or
- any prototype `form-field.v1` schema bytes or stale prototype `$id` value.

The citation reference is inert content under this ADR. A future resolver
decision governs whether the referenced citation is semantically appropriate.
The disposition vocabulary does not claim that all five explanation walks are
already implemented.

## Consequences

- Track 1 must publish a production form-field schema and hand-written positive
  and isolated negative instances before rule fixtures consume it.
- Rules stay form-agnostic and the engine stays thin; official-form identity and
  rendering meaning remain declared content.
- Cross-year, wrong-line, wrong-version, undeclared-property, and dangling-
  symbol cases become validation negatives at the appropriate content boundary.
- A field can evolve independently of a computation rule while both remain
  explicitly versioned.
- Product and CLI renderers have one declared place to obtain display behavior,
  while authoritative values and dispositions remain in findings and records.
- Explanation work may proceed separately without collapsing blocked,
  invalid, inapplicable, or zero states in the interim.

## Alternatives Considered

- **Treat a form field as an output-symbol naming convention.** Rejected:
  symbols do not carry authority/form/year/locator identity, versioned rendering
  behavior, or source citation. Both rivals independently needed a companion
  citizen.
- **Put form metadata on every rule.** Rejected: computation and presentation
  have different lifecycle and cardinality. It would couple reusable derived
  symbols to one official rendering and duplicate form content across rules.
- **Store rendered form state.** Rejected: current form state is a rebuildable
  view over findings and records, never a second authoritative store (Articles
  5, 7, and 14).
- **Use one generic absent/blank state.** Rejected: it conflates incompleteness,
  invalidity, inapplicability, and zero, violating atomicity and rendering
  honesty. All prototype iterations produced useful pressure for the
  distinction.
- **Make closure-backed zero a renderer convention.** Rejected: closure is an
  authoritative finding pinned by derivation. The renderer may describe that
  lineage but cannot create it.

## Links

- Evidence: `docs/prototypes/tax-citizen-families/evaluation-analysis.md` C4-C5
- Process and exclusions:
  `docs/prototypes/tax-citizen-families/process-retrospective.md`
- Milestone: `docs/phases/foundation/milestones/first-tax-slice.md`, Track 0
- Precedents: ADR-0003 (schema citizens and opaque ids), ADR-0005 (prototype
  evidence), ADR-0006 (rule language), ADR-0008 (record placement)
- Companion proposal: ADR-0011 (tax fact identity and source-set closure)
- Exhibits: `exhibits/tax-citizen-families/it1` through `it4`
