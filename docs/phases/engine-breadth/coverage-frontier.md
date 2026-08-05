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

## Frontier as of 2026-08-05

| Candidate slice | New computable class | Current blocker | Contract novelty | Evidence target | Status |
| --- | --- | --- | --- | --- | --- |
| Form 1099-DIV box 2a → Form 1040 line 7a, Schedule D not required | Returns whose only capital gains are eligible capital-gain distributions and whose contributed component authority establishes that Schedule D is not required | The prior recorded/non-composable box-2a block is retired only for this bounded class; Schedule-D-required and missing-authority cases remain honestly unavailable | ADR-0050 accepts four Exception-1 components, a horizon-closed successor box-2a family, distinct line 7a/7b publications, and the direct-route QDCG handoff | Production-shaped synthetic coordinator, lifecycle, package, explanation, and presentation evidence | **synthetic complete** |
| Covered, long-term, gain-only capital transactions → Schedule D line 8a | Returns whose only capital-gain source is one or more covered, long-term, gain-only, no-adjustment Form 1099-B transactions eligible for direct Schedule D line 8a reporting without Form 8949 | Retired for the bounded covered-long-term-gain-only class; short-term transactions, losses, carryovers, Form 8949, noncovered securities, digital assets, and other Schedule D sources remain honestly outside it | New transaction-identity contract one level below statement identity, a nine-part completeness boundary via component authority, a Schedule D instantiation of the accepted attachment ontology (ADR-0036) reused as content only, and two additive presentation-layer repairs surfaced mid-milestone (ADR-0055 value-checked completeness, ADR-0056 attachment disposition visibility) | Curated paper-first evidence (`docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/`), production-shaped synthetic coordinator, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` | **synthetic complete** |
| Current-year covered capital losses and Schedule D line 21 limitation | Returns whose only capital-transaction activity is one or more covered, basis-reported, no-adjustment Form 1099-B transactions — short-term or long-term, gain or loss — reported directly on Schedule D line 1a or 8a without Form 8949, with the current-year $3,000/$1,500 capital-loss limitation and no inbound carryover | Retired for the bounded gain-or-loss, short-term-or-long-term class; inbound carryovers, Form 8949, noncovered securities, digital assets, and other Schedule D sources remain honestly outside it | Additive successor long-term family (gain-or-loss) and new short-term family (ADR-0057), each preserving the original ADR-0052 gain-only family unedited and package-exclusive against it; a `selected-preferential-base` successor discriminated over both families' closure with a floored (nonnegative) preferential amount and an exact pin table; signed Schedule D lines 1a/7/8a/15/16 and line 21 (ADR-0058); a completeness successor retiring two of the seven boundary declarations while preserving the rest | Paper-first Track 0 decision record and two accepted ADRs, production-shaped synthetic coordinator, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` (Track 1 with one findings-only repair; Track 2 clean), including every prior-milestone regression fixture unmodified | **synthetic complete** |
| Inbound capital-loss carryovers | Returns within the supported covered, basis-reported, no-adjustment capital-transaction class carrying a short-term or long-term capital-loss carryover derived from authoritative 2024 return-line facts, included on 2025 Schedule D lines 6 and 14 | Retired for the bounded class; full 2024 return import, joint-to-separate reallocation, canceled-debt handling, and any 2026 carryforward remain deliberately excluded | A bounded five-fact prior-return authority (ADR-0059) with a two-path completeness gate (declared-absence Path A alongside the full-authority Path B, keeping the existing `no-inbound-capital-loss-carryovers` declaration rather than retiring it); the Capital Loss Carryover Worksheet as an auditable derived rule citizen and the signed line 6/14/7/15/16/21 successors (ADR-0060) | Paper-first Track 0 decision record and two accepted ADRs, production-shaped synthetic coordinator, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` (Track 1 with one findings-only repair; Track 2 clean), including every prior-milestone regression fixture unmodified | **synthetic complete** |
| Covered, basis-reported code-W wash-sale adjustments through Form 8949 → Schedule D lines 1b/8b | Returns within the supported covered, basis-reported capital-transaction class carrying one or more Form 1099-B transactions routed to Form 8949 solely because box 1g reports a nondeductible wash-sale loss (code W), the amount accepted as correct | Retired for the bounded single-code-W, basis-reported-to-IRS, accepted-as-correct case; every other adjustment code, noncovered securities, and taxpayer-side wash-sale determination remain deliberately excluded | ADR-0061 (transaction authority — a separate wash-sale fact type plus an identity-key collision kill-test, amended pre-merge after the originally-proposed mechanism proved unsafe given a `source-family.v1` constraint) and ADR-0062 (Form 8949 attachment, per-transaction arithmetic/validation guards, Schedule D 1b/8b composition) | Paper-first Track 0 decision record and two accepted ADRs, production-shaped synthetic coordinator, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` (Track 1 across three repair/re-review rounds; Track 2 clean), including every prior-milestone regression fixture unmodified | **synthetic complete** |
| Noncovered / basis-not-reported Form 8949 transactions | Returns with noncovered securities, broker-basis corrections, or other Form 8949 adjustment codes besides W | No noncovered-basis authority or other adjustment-code content; deliberately excluded from the code-W slice | Each remaining adjustment code needs its own authority and arithmetic; noncovered securities need a distinct basis-source contract | Its own paper-first contract evidence once selected | candidate |
| Other Schedule D sources | K-1 capital gains (box 9/10), Forms 2439/4684/4797/6252/6781/8824, collectibles, unrecaptured section 1250 gain, QOF computation, or lines 18/19 special-rate sources | No source, authority, or downstream contract for any named form; deliberately excluded from the current-year-losses slice | Each named source needs its own scope and completeness analysis; not one coherent slice | Split into independently selectable rows once any is selected | candidate |
| Schedule K-1 (Form 1065) box-5 interest → Form 1040 line 2b and Schedule B Part I | Returns with taxable partnership interest income reported in box 5 of a 2025 Form-1065 K-1 | Retired for the bounded box-5 class; other K-1 forms and boxes remain outside the declared universe | A distinct horizon-closed source family, five-slot composition successor, and composition-complete multi-family attachment itemization | Production-shaped synthetic identity, correction, late-member, line-2b, Schedule-B, package, explanation, and presentation evidence | **synthetic complete** |
| Payer-reported current-inclusion market-discount interest | Returns with nonnegative market-discount amounts reported in 2025 Form 1099-INT box 10 or Form 1099-OID box 5, where the payer-reported amount is already currently includible as taxable interest | Retired for the bounded two-box payer-reported class; disposition-time amounts, partial principal payments, taxpayer-side accrual, basis, unreported market discount, and general securities history remain honestly unavailable | Two dedicated statement families and a successor seven-family positive-interest composition; reuses the accepted multi-family Schedule B contract with no new evaluator, attachment schema/runtime, or presentation behavior | Paper-grounded IRS box routing, mechanical selected-version inventory, synthetic identity/closure/lifecycle, line-2b, Schedule-B, package, explanation, and one canonical positive presentation golden | **synthetic complete** |
| Schedule B interest adjustments | Returns with nominee distributions, accrued interest paid to a bond seller, or taxable amortizable-bond-premium adjustments | Retired for the bounded three-class adjustment path; other adjustment classes and underlying investment calculations remain honestly outside it | New adjustment authority, closure, explanation, and attachment-row semantics | Paper-first contract evidence, positive/negative adjustment goldens, package compatibility, and production-shaped presentation | **synthetic complete** |
| Form 1099-DIV box 3 nondividend distributions | Returns involving Form 1099-DIV box 3 | Recorded/non-composable; generally not reported on Form 1040, with basis/recovery implications outside the current graph | Requires its own basis/recovery and reporting boundary | Paper-first source and downstream contract when selected | named block |
| Form 1099-DIV box 5 section 199A dividends | Returns involving Form 1099-DIV box 5 | Recorded/non-composable; qualified business income deduction treatment is not in the current graph | Requires its own Form 8995/8995-A and QBI boundary | Paper-first source and downstream contract when selected | named block |
| Form 1099-DIV box 7 → direct foreign tax credit without Form 1116 | Returns with 2025 Form 1099-DIV box-7 foreign tax paid that qualify for and elect the direct credit (passive payee-statement income, ≤$300/$600, explicit election, no Form 1116), carried through Schedule 3 line 1/8 and Form 1040 line 20 | Retired for the bounded direct-election class; general Form 1116 FTC, foreign-tax deduction, non-1099-DIV foreign tax, and other Schedule 3 credits remain honestly outside it | Independent box-7 family, residual succession (3+5 only), creditability/election authority, regular-tax cap, Schedule 3 completeness, and tax-after-credit succession | Production-shaped source, eligibility, Schedule 3/Form 1040, package, explanation, and presentation evidence after rebase onto Form 8949 + box-8 + 1099-G tip; independently reviewed READY | **synthetic complete** |
| Form 1099-DIV box 7 → general Form 1116 foreign tax credit | Returns needing Form 1116 limitation calculation or multi-category foreign tax credit | No Form 1116 content, separate-limitation engine, or general FTC framework | Full Form 1116 and Pub. 514 limitation machinery | Own milestone after direct-election class | candidate |
| Form 1099-DIV box 7 → foreign-tax deduction election | Returns electing to deduct foreign taxes on Schedule A instead of claiming a credit | No Schedule A foreign-tax deduction path; deliberately excluded from the direct-credit class | Schedule A itemized-deduction authority and credit-vs-deduction exclusivity | Own paper-first milestone when selected | candidate |
| Form 1099-DIV box 12 exempt-interest dividends | Returns whose only tax-exempt-interest source is one or more 2025 Form 1099-DIV box-12 amounts, with box 13 absent/zero and all excluded source/dependency declarations closed | Retired for the bounded box-12-only class; other tax-exempt sources, nonzero box 13, premium adjustments, and excluded downstream consumers remain honestly blocked | Independent box-12 family, residual succession, explicit line-2a completeness authority, reported-only downstream semantics, and production-path box-13 companion enforcement | Production-shaped source, lifecycle, completeness, package, explanation, and presentation evidence, independently reviewed `READY` | **synthetic complete** |
| Form 1099-INT box 8 tax-exempt interest → Form 1040 line 2a | Returns with one or more 2025 Form 1099-INT box-8 amounts (box 9 absent/zero), aggregated with the closed box-12 family (or closed-empty box-12) into Form 1040 line 2a under a two-path Form 1099-INT completeness gate | Retired for the bounded box-8 succession class; Form 1099-OID tax-exempt, unreported interest, premium adjustments, nonzero box 9 / Form 6251, and excluded downstream consumers remain honestly outside it | Independent box-8 family; live-path box-9 companion; Alternative B line-2a@v2 dual-family succession; Path A/B completeness; packaging v18/v13 | Production-shaped synthetic coordinator, lifecycle, Path A/B, package, explanation, and presentation evidence, independently reviewed `READY` | **synthetic complete** |
| Form 1099-G box 1 unemployment compensation → Schedule 1 line 7 → Form 1040 line 8 | Returns with one or more 2025 Form 1099-G box-1 taxable unemployment amounts, box 4 null/zero, no repayments, no other Schedule 1 income | Retired for the bounded unemployment class; other Form 1099-G boxes and other Schedule 1 income remain outside it | Schedule 1 Alternative A completeness; line-8; line-9 v5; package v20 union of ratified v19 | Production-shaped synthetic evidence after rebase onto Form 8949 + box-8 tip | **synthetic complete** |
| Fully taxable IRA-family distributions from Form 1099-R → Form 1040 line 4b | Returns with one or more 2025 Form 1099-R ordinary, fully taxable IRA-family distributions, with line 4a blank/absent and the statement facts sufficient to identify the bounded class | No IRA-family source, line-4b successor, or Form 1099-R completeness boundary in the ratified graph; basis, rollover eligibility, and special distribution treatment remain excluded | Narrow independent Form 1099-R authority and completeness boundary; successor line 4b and line 9/AGI/taxable-income composition; package, explanation, exact citation pins, and production-shaped presentation | Paper-first Track 0 decision record plus Track 1/Track 2 synthetic source, lifecycle, closure, downstream, package, explanation, and presentation evidence | **selected — planned** |
| 2025 SSA-1099 benefits → Social Security Benefits Worksheet → Form 1040 lines 6a/6b/9 | Returns with one or more ordinary 2025 Form SSA-1099 statements for the taxpayer or joint-return spouse, reconciled nonnegative box-5 benefits, standard worksheet eligibility, and closed component-level authority for every prescribed worksheet input | No SSA-1099 source family, line-6a/6b citizens, worksheet, component-level line-1z/4b/5b/8/Schedule-1 completeness, or Social Security line-9 successor on the ratified base; the merged IRA line-4b route and any later line-8/line-7a successors integrate first | New bounded SSA-1099 family and lifecycle, auditable non-filed worksheet, exact line-6 indicators, component-level closure, and additive line-9 succession; reuse accepted identity, closure, explanation, package, and presentation contracts | Paper-first exception inventory, production-shaped synthetic source/lifecycle/worksheet, exact-once component pins, package/explanation/presentation evidence, and independent review | **selected — planned** |
| Other Form 1099-G boxes (2, 5–7, 9) and box-4 withholding | Returns with other 1099-G payment classes | Not part of unemployment box-1 route | Each box needs its own contract | Independently selectable | named block |
| Other Schedule 1 Part I income sources | Business, rental, farm, Form 4797, other income, etc. | Outside unemployment slice | Each class needs its own analysis | Independently selectable | named block |
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

The **Form 1099-DIV Box 12 to Form 1040 Line 2a** milestone is synthetic
complete for the bounded 2025 box-12-only tax-exempt-interest class. Its
independent family, residual succession, explicit completeness boundary,
box-13 companion guard, reported-only line-2a semantics, package graph,
explanation, and presentation are covered by the milestone plan and its
retrospective. Form 1099-INT/OID tax-exempt sources, unreported interest,
premium adjustments, and excluded downstream consumers remain separate
frontier work.

The **Form 1099-INT Box 8 Tax-Exempt Interest to Form 1040 Line 2a**
milestone is synthetic complete. It extends the closed box-12 route with an
independent box-8 family, live-path box-9 companion, Path A/B completeness,
and successor line-2a aggregation. Plan:
`milestones/form1099int-box8-line2a.md`; retrospective:
`docs/milestone-retrospectives/2026-08-05-form1099int-box8-line2a.md`.

The **Form 1099-DIV Box 7 Direct Foreign Tax Credit (No Form 1116)** milestone
is synthetic complete for the bounded 2025 direct-election class after rebase
onto the ratified tip that includes Form 8949, Form 1099-INT box 8, and Form
1099-G. General Form 1116 calculation and foreign-tax deduction remain separate
frontier work.
