<!-- foreman-context-v1
{
  "version": 1,
  "topic": "engine-breadth-phase-close",
  "status": "closed 2026-08-18; no active milestone and no successor selected or named",
  "scope": [
    "record the Engine Breadth phase close and its carried unclosed work"
  ],
  "non_goals": [
    "no active milestone",
    "no selected or named successor phase",
    "no implementation or hardening start"
  ],
  "retrospective": "docs/milestone-retrospectives/2026-08-18-engine-breadth.md",
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-08-18-engine-breadth.md"
    ]
  }
}
-->

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

## Phase close — 2026-08-18

**Engine Breadth is closed.** Its standing test asked whether a milestone turns
a previously honest-blocked valid-return class into an end-to-end computed
result without weakening closure, citation, contribution, or data-boundary
guarantees. The phase met that test repeatedly. Its four exit criteria are also
met: previously blocked classes operate end to end; each completed slice has
synthetic authoritative-surface evidence and keeps unsupported neighbours
explicit; the repaired frontier separates breadth from hardening and migration;
and this roadmap records the owner's decision to close with the next move left
open for owner selection.

**The coverage frontier is not exhausted.** Form 1116, other Schedule D
sources, other Schedule K-1 boxes, and a re-cut noncovered-basis/Form 8949
contract remain live candidates. Closing is a judgment, not an exhaustion:
after roughly twenty completed slices and prerequisite repairs, those rows are
more instances of a vertical shape the phase has already proved. Continuing
would buy more coverage, not a new engine capability.

**Read the completion accurately.** The phase widened what the engine
**computes**. It did not change how the user supplies facts: the user still
hand-edits JSON. It also did not make any return fileable. Real Return's close
already named both gaps; Engine Breadth did not touch them, and no row in this
phase's frontier was named for either one.

**Carried into the next phase, unclosed:**

1. The **noncovered / basis-not-reported Form 8949 milestone must be re-cut**
   against ADR-0066. Its reusable C1 evaluation-ordering analysis and
   `accounts_for` traversal-totality proof are archived, but old proposed
   ADR-0063/0064/0065 were superseded before ratification. Owner blocker C3 is
   still unanswered: may a closure gate pass while documenting
   counterexamples to its own bar?
2. The **P1 rule-artifact/attachment-rule capability-table consolidation**
   (`docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md`)
   remains filed, scoped, deliberately unselected hardening. Seven-to-nine
   hand-maintained version allowlists broke four consecutive milestones,
   including one site fixed by review and then re-broken during curation of
   the same PR.
3. The entry and filing gaps remain outside engine breadth: fact entry still
   requires hand-edited JSON, and the product still cannot file a return.
4. Live breadth candidates remain recorded without being selected: general
   Form 1116, other Schedule D sources, other Schedule K-1 boxes, and the
   re-cut noncovered-basis row.
5. Every Engine Breadth milestone deferral ledger remains open by its own
   terms:

   - `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/declarative-validation-substrate-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/k1-interest-breadth-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale-deferral-ledger.md`
   - `docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers-deferral-ledger.md`

The coverage frontier is now the closed selection instrument of Engine
Breadth. It remains a historical inventory of delivered and unclosed classes;
it does not select, name, or scaffold what follows. That choice is open and
owner-held.

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
8. **Form 1099-G Box 1 → Schedule 1 Line 7 / Form 1040 Line 8** — closed after
   rebase onto Form 8949 + box-8 tip. Plan:
   `milestones/form1099g-box1-schedule1-line7.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-05-form1099g-box1-schedule1-line7.md`.
9. **Form 1099-DIV Box 7 Direct Foreign Tax Credit (No Form 1116)** —
   selected 2026-08-05 and **closed 2026-08-05** after rebase onto Form 8949,
   box-8, and Form 1099-G. Final package is the additive union core **v21** /
   published **v16** / release **v14** / adopt **v21**
   (`artifact-package.v18`, `quantity-vocabulary.v10`, `dividend-universe.v4`).
   Independent review READY. Plan:
   `milestones/form1099div-box7-direct-ftc.md`; retrospective:
   `docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md`.
10. **Fully Taxable IRA Distributions from Form 1099-R to Form 1040 Line 4b**
    — selected 2026-08-05. Bound the class to ordinary, fully taxable
    IRA-family distributions reported on 2025 Form 1099-R; publish line 4b,
    keep line 4a blank/absent, and carry the result through line 9, AGI,
    taxable income, regular tax, package resolution, explanation, exact
    citation pins, and production-shaped presentation. Basis, rollover
    eligibility, and special distribution treatment remain outside the claim.
    Plan:
    `milestones/form1099r-ira-distributions-line4b.md`.
11. **2025 SSA-1099 Benefits through the Social Security Benefits Worksheet and
    Form 1040 Lines 6a/6b** — selected 2026-08-04 and retained as a separate
    planned milestone while the IRA line-4b route is the current active
    milestone. Track 0 must settle ordinary SSA-1099 identity, box
    reconciliation, worksheet eligibility, filing-status/lived-apart
    semantics, component-level closure, and the no-line-9-cycle graph before
    implementation. The planned class excludes RRB, lump-sum election,
    Publication 915 exception paths, excess repayments, foreign/nonresident
    benefits, new IRA/pension/unemployment/Schedule 1 support, and
    withholding/payment paths. Plan:
    `milestones/ssa1099-benefits-line6.md`.
12. **Form 1098 Home-Mortgage Interest through Schedule A and Form 1040 Line
    12e** — owner-chartered 2026-08-05 and **closed 2026-08-10** (PR #168).
    Bounded singleton-closed Form 1098 statement class: deductible interest
    derived through Schedule A line 8a from taxpayer-authority component
    facts, a composition-complete Schedule A for this class, deterministic
    standard-vs-itemized selection at line 12e (guarding the generic
    itemized assertion off whenever a Form 1098 statement is genuinely on
    record, including the contradictory-declaration case), and the correct
    2025 line-13a/13b/14 deduction-spine succession into taxable income.
    Final package is the additive union core **v29** / published **v24** /
    release **v22** / adopt **v29** over the merged SSA-1099 base. Multiple
    mortgages, refinancing, points, PMI, the mortgage-interest credit, and
    general Schedule A support remain outside it. Plan:
    `milestones/f1098-mortgage-interest-line12e.md`; retrospective:
    `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md`.
13. **SSA No-Activity Applicability Repair** — owner-approved as Milestone 1
    of a two-milestone prerequisite to Form 1098-E, and **closed 2026-08-14**
    (PR #173). A return with no applicable Social Security source now
    publishes the legally authorized line-6 zero and reaches total income
    without satisfying 33 Social Security worksheet-scope declarations.
    `rule.ss-benefits-worksheet` v2 is the sole producer of line 6b;
    `no-rrb-or-foreign-social-benefit` stays load-bearing on both routes and
    is recorded as a fourteenth migration candidate for Milestone 2. Final
    package is the additive union core **v30** / published **v25** / release
    **v23** / adopt **v30** over the merged Form 1098 base. Plan:
    `milestones/ssa-no-activity-applicability.md`; retrospective:
    `docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md`.
14. **Fact-type succession with neutral Schedule 1 vocabulary** —
    owner-approved as Milestone 2 of the same Form 1098-E prerequisite,
    and **closed on this branch (PR #177)**. No new tax route. The
    thirteen shared Schedule 1 absence declarations succeed onto
    Schedule-1-native ids via an adopted `migration-artifact.v1`
    (ADR-0063), a fourth named supersession root. Worksheet v3
    retargets the nonempty conditional set; the Milestone 1 empty-route
    contract is unchanged. Publication is the additive union core
    **v31** / published **v26** / release **v24**. Form 1098-E,
    Schedule 1 line 21, Form 1040 line 10, and AGI remain Part 3.
    Plan: `milestones/fact-type-succession-neutral-schedule1.md`;
    retrospective:
    `docs/milestone-retrospectives/2026-08-14-fact-type-succession-neutral-schedule1.md`.
15. **Declarative Structured Validation and Consumer Dependency Substrate**
    — owner-selected 2026-08-12 as a hardening prerequisite, not a new tax
    route: retires the hard-coded Form 8949/Form 1099-B row-guard and
    identity-collision mechanisms the closed covered-wash-sale milestone
    (item 4 below in Status) left in generic runner/package-validator code,
    replacing them with versioned-content member constraints, declared
    cross-family identity exclusivity, and reachability-derived consumer
    prerequisites (ADR-0066). **Closed 2026-08-17.** `runner.py`'s domain
    references went from 24 to 0. Both schedulers proven byte-identical on
    the migrated content, including attachment-bearing citizens (a
    pre-existing `reference_runner.py` gap, repaired in-milestone). An
    independent owner-advisor product review found and repaired a failing
    type gate and a stale cross-milestone test before close. Publication is
    the additive union core **v32** / published **v27** / release **v25** /
    adopt **v32** over the merged core v31 base. Plan:
    `milestones/declarative-validation-substrate.md`; deferral ledger:
    `milestones/declarative-validation-substrate-deferral-ledger.md`;
    retrospective:
    `docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md`.
16. **2025 Form 1098-E Student-Loan Interest through Schedule 1 Lines 21/26
    and AGI** — re-cut and **closed 2026-08-18**. Opens the first Engine
    Breadth route on the income-adjustment side of the return: a single
    2025 Form 1098-E statement's deductible interest, capped at $2,500 and
    reduced by the MAGI phaseout, computed on the Student Loan Interest
    Deduction Worksheet as rule content and carried through Schedule 1
    lines 21/26 into Form 1040 line 10 and AGI (lines 11a/11b). The
    additive `multiply`/`divide`/`collect_categorical_all_equal` expression-
    language extension (ADR-0064) and the first application of ADR-0016
    decision 4 to a mixed absent/present/structural-zero Schedule 1 Part II
    total (ADR-0065). Rebased and rebuilt onto the closed
    declarative-validation-substrate-f8949 base after that milestone merged
    mid-build; the two milestones' packages collided ADD/ADD on the same
    version number, resolved by rebuilding on top of the ratified content
    rather than renumbering schemas. Final package is the additive union
    core **v33** / published **v28** / release **v26** / adopt **v33**,
    over the merged core v32 base. An independent review of PR #178
    (curated object `64c540ce`) returned `CHANGES REQUESTED` on two
    curation-introduced defects; both fixed and the gate re-verified green.
    Plan:
    `milestones/f1098e-student-loan-interest-agi.md`; deferral ledger:
    `milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`;
    retrospective:
    `docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md`.

**Next breadth slice — owner-unselected.**
Inbound capital-loss carryovers, Form 8949/noncovered securities/adjustments,
and other Schedule D sources remain distinct candidates; other Form 1099-R
distribution treatments and unrelated income domains remain outside the
selected class.

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
- **Fact-type succession with neutral Schedule 1 vocabulary — closed
  on this branch (PR #177).** No new tax route. Thirteen Schedule 1
  absence facts succeed onto Schedule-1-native ids (ADR-0063). Empty-route
  SSA contract unchanged except the nonempty CDS retarget. Form 1098-E
  remains unselected. Plan:
  `milestones/fact-type-succession-neutral-schedule1.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-14-fact-type-succession-neutral-schedule1.md`.
- **Declarative Structured Validation and Consumer Dependency Substrate —
  closed 2026-08-17** (PR #174). No new tax route; hardening prerequisite.
  Plan: `milestones/declarative-validation-substrate.md`; retrospective:
  `docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md`.
- **2025 Form 1098-E Student-Loan Interest through Schedule 1 Lines 21/26
  and AGI — closed 2026-08-18.** First Engine Breadth route on the
  income-adjustment side of the return. The bounded single-statement,
  fully-eligible class is synthetic complete through Schedule 1 lines
  21/26, Form 1040 line 10, and AGI. Rebased and rebuilt onto the closed
  declarative-validation-substrate-f8949 base; final package core
  **v33**/published **v28**/release **v26**/adopt **v33**. Independent
  review of the curated PR (#178) returned `CHANGES REQUESTED` on two
  curation-introduced defects; both fixed, gate re-verified green. Plan:
  `milestones/f1098e-student-loan-interest-agi.md`; deferral ledger:
  `milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md`.
- Subtractive adjustments and other market-discount situations remain
  separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
- Subtractive adjustments and other market-discount situations remain
  separate candidates; this selection does not absorb them.
- Real Return — **closed 2026-07-28.** Its final matrix and roadmap remain the
  historical evidence for the bounded slice Engine Breadth starts from.
