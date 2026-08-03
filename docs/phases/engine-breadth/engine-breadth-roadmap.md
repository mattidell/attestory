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
4. **Covered Long-Term Gains, Schedule D Line 8a** — selected 2026-08-01.
   **Closed 2026-08-02** (Track 2/3 independently reviewed `READY`). Added
   a transaction source family for covered, long-term, gain-only Form
   1099-B transactions, the nine-part Schedule D completeness boundary
   through component authority, Schedule D (line 8a, Part II line 15, Part
   III line 16) as content on the accepted attachment ontology (ADR-0036),
   and superseded the QDCG/line-16 path additively to use the Schedule D
   result for this class without editing ADR-0050. Two additive
   architecture repairs surfaced mid-milestone and were ratified in-scope:
   ADR-0055 (attachment completeness must check declared-answer *value*,
   not only presence) and ADR-0056 (blocked/not-required attachment
   dispositions must be visible on the presentation surface, not silently
   omitted). The bounded class is synthetic complete; short-term
   transactions, losses, carryovers, Form 8949, noncovered securities,
   digital assets, and other Schedule D sources remain honestly outside
   it. Plan: `milestones/schedule-d-covered-ltcg-8a.md`; curated contract
   evidence: `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/`;
   retrospective: `docs/milestone-retrospectives/2026-08-02-schedule-d-covered-ltcg-8a.md`;
   deferral ledger:
   `milestones/schedule-d-covered-ltcg-8a-deferral-ledger.md`.
5. **Schedule B Interest Adjustments** — selected 2026-08-02. Add a bounded
   2025 adjustment path for nominee distributions, accrued interest paid to a
   bond seller, and taxable amortizable-bond-premium adjustments; subtract only
   explicit, closed adjustment authority from the existing positive-interest
   universe and render the named rows on Schedule B Part I. Schedule D remains
   separate and is not a dependency of this milestone. Plan:
   `milestones/schedule-b-interest-adjustments.md`.
6. **Current-Year Capital Losses and Schedule D Line 21** — selected
   2026-08-03. **Closed 2026-08-03** (Track 1 with one findings-only
   repair, Track 2, both independently reviewed `READY`). Added an
   additive successor long-term family (gain-or-loss) and a new
   short-term family (ADR-0057), each preserving the original ADR-0052
   gain-only family unedited and package-exclusive against it; a
   `selected-preferential-base` successor with a multi-family
   discriminator, an exact pin table, and a producer-side floor to
   nonnegative; signed Schedule D lines 1a/7/8a/15/16 and line 21's
   §1211 current-year loss cap (ADR-0058); and a completeness successor
   retiring two of the seven boundary declarations while preserving the
   rest. The bounded class is synthetic complete; inbound carryovers,
   Form 8949, noncovered securities, digital assets, and other Schedule D
   sources remain honestly outside it. Plan:
   `milestones/schedule-d-current-year-losses.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md`;
   deferral ledger:
   `milestones/schedule-d-current-year-losses-deferral-ledger.md`.
7. **Next breadth slice — owner-selected from the refreshed frontier.**
   Inbound capital-loss carryovers, Form 8949/noncovered securities/
   adjustments, and other Schedule D sources deferred out of item 6 remain
   distinct candidates; other adjustment classes and unrelated income domains
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
- **Covered Long-Term Gains, Schedule D Line 8a — closed 2026-08-02**
  (independently reviewed `READY`). The bounded covered, long-term,
  gain-only, no-adjustment Form 1099-B class is synthetic complete through
  Schedule D (line 8a/13/15/16), Form 1040 line 7a/9, the Schedule
  D-bound QDCG line-16 path, package resolution, explanation, and
  presentation, including honest visibility for blocked/not-required
  attachment states (ADR-0056). Plan:
  `milestones/schedule-d-covered-ltcg-8a.md`.
- **Current-Year Capital Losses and Schedule D Line 21 — closed
  2026-08-03** (Track 1 with one findings-only repair, Track 2, both
  independently reviewed `READY`). The bounded covered, basis-reported,
  short-term-or-long-term, gain-or-loss Form 1099-B class is synthetic
  complete through signed Schedule D lines 1a/7/8a/15/16, the §1211
  current-year loss cap (line 21), Form 1040 line 7a/9, the Schedule
  D-bound QDCG line-16 path at any sign of Schedule D's result, package
  resolution, explanation, and presentation, including honest visibility
  for the new `SOURCE_SET_UNCLOSED` and `COMPLETENESS_VALUE_VIOLATION`
  states. Plan: `milestones/schedule-d-current-year-losses.md`.
- **Schedule B Interest Adjustments — planned 2026-08-02.** The selected scope
  is independent of Schedule D and begins with a paper boundary checkpoint for
  nominee distributions, accrued interest paid to a seller, and taxable
  amortizable-bond-premium adjustments. Plan:
  `milestones/schedule-b-interest-adjustments.md`.
- Subtractive adjustments and other market-discount situations remain
  separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
