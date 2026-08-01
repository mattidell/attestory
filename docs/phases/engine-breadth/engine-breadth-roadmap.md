# Engine Breadth Phase — Roadmap

Audience: Product (roadmap); Shared (status)

## Thesis

The engine already computes one real, auditable return slice. Engine Breadth
widens the set of valid returns it can compute by retiring one named honest
block at a time through complete vertical slices.

## How milestones are selected

Milestones are selected from `coverage-frontier.md`. A candidate must name the
unsupported return class, authoritative facts or declarations, downstream
publication or attachment, current blocker, and cheapest sufficient evidence.
Owner selection remains Tier 3.

Hardening does not become breadth because a deferral is old or important.
Security substrate, historical migration, presentation-session follow-ups, and
operational cleanup stay visible in their existing ledgers but do not enter this
roadmap unless a selected breadth slice directly depends on them.

## Planned roadmap

1. **Capital-Gain Distributions and Form 1040 Line 7a** — promote Form
   1099-DIV box 2a from recorded/non-composable content into a closed source
   path; establish explicit authority for the Schedule-D-not-required route;
   publish line 7a and carry it through total income, taxable income, QDCG tax,
   explanation, packaging, and presentation on production-shaped synthetic
   fixtures.
   **Closed 2026-07-31** (PR #128). The bounded direct-reporting class is
   synthetic complete; Schedule-D-required returns remain honestly outside it.
2. **Schedule K-1 Box-5 Interest Breadth** — add 2025 Schedule K-1 (Form 1065)
   box-5 taxable interest as its own closed positive-interest family, carry it
   through Form 1040 line 2b, and replace Schedule B's temporary box-1-only
   Part-I simplification with a composition-complete multi-family itemization.
   **Closed 2026-07-31** (PR #133). The bounded Form-1065 box-5 class is synthetic
   complete; other K-1 forms and boxes, market discount, and subtractive
   adjustments remain outside it. Plan:
   `milestones/k1-interest-breadth.md`.
3. **Payer-Reported Current-Inclusion Market-Discount Interest** — closed
   2026-08-01. Add Form 1099-INT box 10 and Form 1099-OID box 5 as separate
   payer-reported current-inclusion source families, route both through the
   positive-interest composition, Form 1040 line 2b, and composition-complete
   Schedule B Part I, and stop at the statement boundary before disposition,
   basis, or transaction machinery. The bounded class is synthetic complete;
   disposition-time market discount, partial principal payments, taxpayer-side
   accrual, basis, and broader transaction situations remain outside it. Plan:
   `milestones/market-discount-interest.md`.
4. **Next breadth slice — owner-selected from the refreshed frontier.** A true
   Schedule D source slice and subtractive interest adjustments remain distinct
   candidates; other market-discount situations and unrelated income domains
   remain outside the selected class.

## Why line 7a comes before Schedule D

The 2025 Form 1040 instructions permit eligible capital-gain distributions to
be reported directly on line 7a with Schedule D marked not required. A
box-2a-only milestone that nevertheless manufactures Schedule D would encode
the wrong dependency shape and would violate the project's
dependency-form-completeness discipline. Schedule D follows only when its own
source and completeness boundary is selected.

## Status

- **Capital-Gain Distributions and Form 1040 Line 7a — closed 2026-07-31.**
  The bounded direct-reporting class is synthetic complete on `main` after PR
  #128. Plan:
  `milestones/capital-gain-distributions-line7a.md`.
- **Schedule K-1 Box-5 Interest Breadth — closed 2026-07-31** (PR #133). The bounded
  Form-1065 box-5 path is synthetic complete through line 2b, Schedule B,
  downstream results, package resolution, explanation, and presentation.
  Plan: `milestones/k1-interest-breadth.md`.
- **Payer-Reported Current-Inclusion Market-Discount Interest — closed
  2026-08-01.** The bounded box-10/box-5 payer-reported class is synthetic
  complete through line 2b, Schedule B, package resolution, explanation, and
  one canonical positive presentation golden; disposition, basis,
  taxpayer-side accrual, subtractive adjustments, and broader securities
  history remain outside it. Plan:
  `milestones/market-discount-interest.md`.
- Schedule D, subtractive adjustments, and other market-discount situations
  remain separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
