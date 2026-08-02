# ADR 0016 - Source-Family Claim and Composition

- Status: accepted (ratified 2026-07-12)
- Tier: 2
- Date: 2026-07-12

## Context

ADR-0014 adopts reusable closure mappings but does not define the semantic
universe a source family closes. Paper rivals tested Form 1099-INT box-1 items,
non-form taxable interest, box 3, late discovery, and narrow-closed/broad-open
cases.

Evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/evaluation-analysis.md`.

## Decision

1. A versioned source-family declaration carries an exact closure claim and a
   canonical member predicate. Together they are semantic authority.
2. Opaque ids, titles, shorthand labels, rule symbols, and UI wording cannot
   broaden or replace that declared meaning.
3. Mapping, subtotal calculation, and coverage reference/pin the same family
   declaration. Coverage presents the exact claim or an explicit reference to
   it; a rollup cannot silently report a broader universe complete.
4. A family subtotal carries its declaration/predicate. A broader final result
   may consume it only when the required universe is identical or an explicit
   composition is established as coextensive.
5. Closure of Form 1099-INT box-1 statement items may authorize only the box-1
   subtotal, including subtotal zero. It does not authorize Form 1040 line-2b
   zero or “all taxable interest complete.”

## Not Decided

- full taxable-interest family taxonomy;
- exact production schema ids/bytes;
- UI presentation beyond preserving authoritative meaning;
- statement sameness mechanics already conditioned by ADR-0015; or
- late-member freshness/currency machinery.

The last item is a separate Tier-3 boundary: ADR-0010 cannot make an old empty
zero depend on a future member, and no frontier, derived authority citizen, or
new standing-affecting edge is authorized here.

## Consequences

- Validators reject claim/predicate mismatch and narrow-subtotal substitution.
- Coverage cannot use friendly shorthand as authoritative broader completion.
- The interest slice may implement B1 present-source subtotal behavior, but
  closure-backed zero must wait for the separate freshness decision.

## Alternatives Considered

- Document-level “all 1099-INT” closure: rejected by box-specific meaning.
- B1 equals taxable interest: rejected by non-form interest.
- Internal equality with labels as meaning: rejected by consistent mislabeling.
- Implicit subtotal promotion: rejected because it hides open inputs.

## Links

- Analysis: `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/evaluation-analysis.md`
- Exhibits: `exhibits/source-family-semantics/it1`, `it2`, `repair1`
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/foundation/milestones/source-completeness-and-interest-slice.md`
- Precedents: ADR-0005, ADR-0010, ADR-0011, ADR-0014, ADR-0015
