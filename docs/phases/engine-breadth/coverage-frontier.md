# Engine Breadth — Coverage Frontier

Audience: Product (selection instrument); Shared (status)

## How to read this frontier

A row is a coherent return class the engine either computes or honestly cannot
yet compute. Selection favors a bounded end-to-end change over a wide list of
input boxes. Status is one of:

- **named block** — the unsupported class is represented and refused honestly;
- **candidate** — the class is understood well enough to compare, but is not
  selected;
- **selected** — an owner-selected milestone plan exists;
- **contracted** — required scope contracts are accepted;
- **synthetic complete** — the authoritative path operates end to end on
  committed synthetic fixtures.

“Synthetic complete” is an engine-coverage claim, not a real-data claim.

## Frontier as of 2026-08-01

| Candidate slice | New computable class | Current blocker | Contract novelty | Evidence target | Status |
| --- | --- | --- | --- | --- | --- |
| Form 1099-DIV box 2a → Form 1040 line 7a, Schedule D not required | Returns whose only capital gains are eligible capital-gain distributions and whose contributed component authority establishes that Schedule D is not required | The prior recorded/non-composable box-2a block is retired only for this bounded class; Schedule-D-required and missing-authority cases remain honestly unavailable | ADR-0050 accepts four Exception-1 components, a horizon-closed successor box-2a family, distinct line 7a/7b publications, and the direct-route QDCG handoff | Production-shaped synthetic coordinator, lifecycle, package, explanation, and presentation evidence | **synthetic complete** |
| Covered, long-term, gain-only capital transactions → Schedule D line 8a | Returns whose only capital-gain source is one or more covered, long-term, gain-only, no-adjustment Form 1099-B transactions eligible for direct Schedule D line 8a reporting without Form 8949 | Retired for the bounded covered-long-term-gain-only class; short-term transactions, losses, carryovers, Form 8949, noncovered securities, digital assets, and other Schedule D sources remain honestly outside it | New transaction-identity contract one level below statement identity, a nine-part completeness boundary via component authority, a Schedule D instantiation of the accepted attachment ontology (ADR-0036) reused as content only, and two additive presentation-layer repairs surfaced mid-milestone (ADR-0055 value-checked completeness, ADR-0056 attachment disposition visibility) | Curated paper-first evidence (`docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/`), production-shaped synthetic coordinator, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` | **synthetic complete** |
| Current-year covered capital losses and Schedule D line 21 limitation | Returns whose only capital-transaction activity is one or more covered, basis-reported, no-adjustment Form 1099-B transactions — short-term or long-term, gain or loss — reported directly on Schedule D line 1a or 8a without Form 8949, with the current-year $3,000/$1,500 capital-loss limitation and no inbound carryover | Retired for the bounded gain-or-loss, short-term-or-long-term class; inbound carryovers, Form 8949, noncovered securities, digital assets, and other Schedule D sources remain honestly outside it | Additive successor long-term family (gain-or-loss) and new short-term family (ADR-0057), each preserving the original ADR-0052 gain-only family unedited and package-exclusive against it; a `selected-preferential-base` successor discriminated over both families' closure with a floored (nonnegative) preferential amount and an exact pin table; signed Schedule D lines 1a/7/8a/15/16 and line 21 (ADR-0058); a completeness successor retiring two of the seven boundary declarations while preserving the rest | Paper-first Track 0 decision record and two accepted ADRs, production-shaped synthetic coordinator, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` (Track 1 with one findings-only repair; Track 2 clean), including every prior-milestone regression fixture unmodified | **synthetic complete** |
| Inbound capital-loss carryovers | Returns within the supported covered, basis-reported, no-adjustment capital-transaction class carrying a short-term or long-term capital-loss carryover derived from authoritative 2024 return-line facts, included on 2025 Schedule D lines 6 and 14 | Retired for the bounded class; full 2024 return import, joint-to-separate reallocation, canceled-debt handling, and any 2026 carryforward remain deliberately excluded | A bounded five-fact prior-return authority (ADR-0059) with a two-path completeness gate (declared-absence Path A alongside the full-authority Path B, keeping the existing `no-inbound-capital-loss-carryovers` declaration rather than retiring it); the Capital Loss Carryover Worksheet as an auditable derived rule citizen and the signed line 6/14/7/15/16/21 successors (ADR-0060) | Paper-first Track 0 decision record and two accepted ADRs, production-shaped synthetic coordinator, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` (Track 1 with one findings-only repair; Track 2 clean), including every prior-milestone regression fixture unmodified | **synthetic complete** |
| Form 8949 / noncovered securities / adjustments | Returns with noncovered securities, broker-basis corrections, wash sales, or other Form 8949 adjustment codes | No Form 8949 content, adjustment-code vocabulary, or noncovered-basis authority; deliberately excluded from the current-year-losses slice | Each adjustment code needs its own authority and arithmetic; noncovered securities need a distinct basis-source contract | Its own paper-first contract evidence once selected | candidate |
| Other Schedule D sources | K-1 capital gains (box 9/10), Forms 2439/4684/4797/6252/6781/8824, collectibles, unrecaptured section 1250 gain, QOF computation, or lines 18/19 special-rate sources | No source, authority, or downstream contract for any named form; deliberately excluded from the current-year-losses slice | Each named source needs its own scope and completeness analysis; not one coherent slice | Split into independently selectable rows once any is selected | candidate |
| Schedule K-1 (Form 1065) box-5 interest → Form 1040 line 2b and Schedule B Part I | Returns with taxable partnership interest income reported in box 5 of a 2025 Form-1065 K-1 | Retired for the bounded box-5 class; other K-1 forms and boxes remain outside the declared universe | A distinct horizon-closed source family, five-slot composition successor, and composition-complete multi-family attachment itemization | Production-shaped synthetic identity, correction, late-member, line-2b, Schedule-B, package, explanation, and presentation evidence | **synthetic complete** |
| Payer-reported current-inclusion market-discount interest | Returns with nonnegative market-discount amounts reported in 2025 Form 1099-INT box 10 or Form 1099-OID box 5, where the payer-reported amount is already currently includible as taxable interest | Retired for the bounded two-box payer-reported class; disposition-time amounts, partial principal payments, taxpayer-side accrual, basis, unreported market discount, and general securities history remain honestly unavailable | Two dedicated statement families and a successor seven-family positive-interest composition; reuses the accepted multi-family Schedule B contract with no new evaluator, attachment schema/runtime, or presentation behavior | Paper-grounded IRS box routing, mechanical selected-version inventory, synthetic identity/closure/lifecycle, line-2b, Schedule-B, package, explanation, and one canonical positive presentation golden | **synthetic complete** |
| Schedule B interest adjustments | Returns with nominee distributions, accrued interest paid to a bond seller, or taxable amortizable-bond-premium adjustments | Retired for the bounded three-class adjustment path; other adjustment classes and underlying investment calculations remain honestly outside it | New adjustment authority, closure, explanation, and attachment-row semantics | Paper-first contract evidence, positive/negative adjustment goldens, package compatibility, and production-shaped presentation | **synthetic complete** |
| Form 1099-DIV box 3 nondividend distributions | Returns involving Form 1099-DIV box 3 | Recorded/non-composable; generally not reported on Form 1040, with basis/recovery implications outside the current graph | Requires its own basis/recovery and reporting boundary | Paper-first source and downstream contract when selected | named block |
| Form 1099-DIV box 5 section 199A dividends | Returns involving Form 1099-DIV box 5 | Recorded/non-composable; qualified business income deduction treatment is not in the current graph | Requires its own Form 8995/8995-A and QBI boundary | Paper-first source and downstream contract when selected | named block |
| Form 1099-DIV box 7 foreign tax paid | Returns involving Form 1099-DIV box 7 | Recorded/non-composable; foreign tax credit or deduction treatment is not in the current graph | Requires its own credit/deduction and Form 1116 boundary | Paper-first source and downstream contract when selected | named block |
| Form 1099-DIV box 12 exempt-interest dividends | Returns whose only tax-exempt-interest source is one or more 2025 Form 1099-DIV box-12 amounts, with box 13 absent/zero and all excluded source/dependency declarations closed | Selected bounded class is planned; other tax-exempt sources, box 13, premium adjustments, and excluded downstream consumers remain honestly blocked | Independent box-12 family, residual succession, explicit line-2a completeness authority, and reported-only downstream semantics | Production-shaped source, lifecycle, completeness, package, explanation, and presentation evidence | selected |
| New unrelated income domain | A return class outside the existing W-2/interest/dividend columns | No owner-selected source/form target | Unknown until a concrete source and downstream output are named | Owner selection and a fresh coverage row | candidate |

## Completed synthetic frontier

The first milestone, **Capital-Gain Distributions and Form 1040 Line 7a**,
closed on `main` in PR #128. Its synthetic-complete claim is bounded to the
selected box-2a-only direct-reporting class: production-shaped synthetic
returns reach line 7a, line 9, taxable income, line 16, explanation, package
resolution, and presentation. This is neither real-data evidence nor general
capital-gains support.

The engine will not create Schedule D merely because box 2a is present.
Schedule-D-required and missing-authority returns remain outside this direct
route. A later Schedule D milestone must bring the additional source and
completeness scope that makes the attachment genuinely required; it remains a
distinct candidate rather than the automatically selected successor.

The second milestone, **Schedule K-1 Box-5 Interest Breadth**, is synthetic
complete. Its production-shaped synthetic path preserves logical K-1 identity
and correction lifecycle, contributes a fifth closed positive-interest family,
recomputes Form 1040 line 2b and downstream results, and renders a Schedule B
Part I that is structurally complete against the adopted composition. The claim
is limited to 2025 Schedule K-1 (Form 1065) box 5; it does not include other
K-1 forms or boxes, market discount, subtractive adjustments, partnership
basis, or a real-data operation. Plan: `milestones/k1-interest-breadth.md`.

The third milestone, **Payer-Reported Current-Inclusion Market-Discount
Interest**, is synthetic complete for the bounded 2025 Form 1099-INT box-10 and
Form 1099-OID box-5 class. It accepts the payer-reported current-inclusion
amount only; it does not calculate accrual, election eligibility, basis,
disposition income, or securities history. Plan:
`milestones/market-discount-interest.md`; retrospective:
`docs/milestone-retrospectives/2026-08-01-market-discount-interest.md`.

Official tax-content grounding:

- [2025 Form 1040 instructions, line 7a](https://www.irs.gov/instructions/i1040gi)
  describe the direct-reporting exception and the Schedule-D-not-required
  indicator.
- [2025 Schedule D instructions](https://www.irs.gov/instructions/i1040sd)
  distinguish capital-gain distributions reported directly on Form 1040 from
  those reported through Schedule D.
- [Form 1099-DIV instructions](https://www.irs.gov/instructions/i1099div)
  define box 2a as total capital-gain distributions.

The fourth milestone, **Schedule B Interest Adjustments**, is synthetic complete
for a bounded 2025 class covering nominee distributions, accrued interest paid
to a bond seller, and taxable amortizable-bond-premium adjustments. It is
separate from Schedule D and accepts explicit adjustment authority; it does not
calculate nominee ownership, accrued interest, bond-premium amortization, or
any capital transaction. Plan: `milestones/schedule-b-interest-adjustments.md`;
retrospective:
`docs/milestone-retrospectives/2026-08-03-schedule-b-interest-adjustments.md`.

These sources establish the tax routing. They do not decide the project's
authority, closure, supersession, or explanation contracts; those are the
milestone's prototype questions.
