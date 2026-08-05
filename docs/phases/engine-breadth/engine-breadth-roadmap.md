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
5. **Schedule B Interest Adjustments** — selected 2026-08-02. **Closed
   2026-08-03**. Added a bounded 2025 adjustment path for nominee
   distributions, accrued interest paid to a bond seller, and taxable
   amortizable-bond-premium adjustments; subtracts only explicit, closed
   adjustment authority from the existing positive-interest universe and
   renders the named rows on Schedule B Part I. Schedule D remains separate
   and is not a dependency of this milestone. Plan:
   `milestones/schedule-b-interest-adjustments.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-03-schedule-b-interest-adjustments.md`.
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
7. **Form 1099-DIV Box 12 to Form 1040 Line 2a** — selected 2026-08-03 and
   **closed 2026-08-04**. Promoted exempt-interest dividends into an
   independent closed source family and computed the complete bounded
   box-12-only tax-exempt interest amount on line 2a. The route preserves
   historical residual boxes, explicitly blocks other tax-exempt sources,
   box 13, and excluded downstream dependencies, and does not change line 9,
   taxable income, Schedule B, or Schedule D. The final package is v17 with
   published registry v12, release v10, and adoption v17; the independent
   re-review returned `READY`. Plan:
   `milestones/form1099div-box12-line2a.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md`.
8. **Form 1099-G Box 1 → Schedule 1 Line 7 / Form 1040 Line 8** — closed after rebase onto Form 8949 + box-8 tip. Plan: `milestones/form1099g-box1-schedule1-line7.md`. Retrospective: `docs/milestone-retrospectives/2026-08-05-form1099g-box1-schedule1-line7.md`.

**Next breadth slice — owner-selected from the refreshed frontier.**
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
- **Schedule B Interest Adjustments — closed 2026-08-03.** The bounded three-
  class adjustment path is synthetic complete through line 2b, Schedule B Part
  I, package resolution, explanation, and presentation. Schedule D remains
  outside scope. Plan: `milestones/schedule-b-interest-adjustments.md`.
- **Inbound Capital-Loss Carryovers into 2025 Schedule D — closed 2026-08-04**
  (Track 1 with one findings-only repair, Track 2, both independently
  reviewed `READY`). A bounded five-fact 2024 prior-return authority
  (ADR-0059) with a two-path completeness gate — a cheap declared-absence
  path preserving the existing `no-inbound-capital-loss-carryovers`
  declaration, and a full-authority path running the Capital Loss
  Carryover Worksheet as an auditable derived rule citizen (ADR-0060) —
  makes the short-term/long-term carryover synthetic complete through
  signed Schedule D lines 6/7/14/15/16/21, Form 1040 line 7a/9, package
  resolution, explanation, and presentation, including a carryover-only
  routing case and disposition-visibility parity for the missing-
  authority state. Rebased onto the merged Schedule B interest-
  adjustments milestone; the resulting package-version collision
  (`package.core-calculations` `v15` claimed independently by both) was
  resolved as an additive `v16`/`v11` union, and a latent hardcoded-
  package-version restriction in `packages/derivation/package_validation.py`
  (introduced by the Schedule B build) was generalized so it no longer
  blocks any package version past `v15`. Plan:
  `milestones/schedule-d-inbound-loss-carryovers.md`.
- **Form 1099-DIV Box 12 to Form 1040 Line 2a — closed 2026-08-04.** The
  bounded box-12-only class is synthetic complete through line 2a, explicit
  completeness and box-13 companion authority, reported-only explanation and
  presentation, package/release/adoption resolution, and focused regressions
  for existing dividend, interest, Schedule B, and Schedule D behavior. The
  independent re-review returned `READY`. Other tax-exempt sources and
  excluded downstream consumers remain honestly outside the claim. Plan:
  `milestones/form1099div-box12-line2a.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md`.
- **Covered Form 1099-B Wash-Sale Adjustments through Form 8949 and
  Schedule D Lines 1b/8b — closed 2026-08-05** (Track 1 across three
  repair/re-review rounds, Track 2, both independently reviewed `READY`).
  A covered, basis-reported Form 1099-B transaction routed to Form 8949
  solely by a broker-reported box-1g wash-sale loss (code W) is synthetic
  complete through Form 8949 columns (a)-(h), per-transaction validation
  guards, successor Schedule D lines 1b/7/8b/15/16/21, Form 1040 line 7a/9,
  package resolution, explanation, and presentation. ADR-0061 was amended
  pre-merge after review found the originally-proposed transaction-identity
  mechanism unsafe given a real `source-family.v1` schema constraint;
  resolved with a separate wash-sale fact type and an identity-key
  collision kill-test, wired into the live run path. Rebased onto the
  merged Form 1099-DIV Box 12 milestone; a second package/schema version
  collision (independently-minted `v17`/`v12` and colliding schema
  successors) was caught before either PR merged and resolved as an
  additive union (`v18`/`v13`, `quantity-vocabulary.v7`,
  `artifact-package.v15`). Every other Form 8949 adjustment code,
  noncovered securities, and taxpayer-side wash-sale determination remain
  honestly outside the claim. Plan:
  `milestones/schedule-d-form8949-covered-wash-sale.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-05-schedule-d-form8949-covered-wash-sale.md`.
- **Form 1099-INT Box 8 Tax-Exempt Interest to Form 1040 Line 2a — closed
  2026-08-05.** The bounded box-8 succession of the closed box-12 line-2a
  route is synthetic complete through Path A/B completeness, live-path box-9
  companion, reported-only explanation and presentation, and packaging
  v18/v13/v11/adopt-v18. Independent review returned `READY` with no findings.
  Plan: `milestones/form1099int-box8-line2a.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-05-form1099int-box8-line2a.md`.
- Subtractive adjustments and other market-discount situations remain
  separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
- Subtractive adjustments and other market-discount situations remain
  separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
