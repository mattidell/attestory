# Tax Concept Derivation Roadmap

## Planned roadmap

### 1. Reported Interest to Tax Concept Vertical Slice

Build a bounded, executable model of one Form 1099-INT box-1 item in two
synthetic circumstances: the reported amount is fully includible, and the same
reported amount is subject to a bounded accrued-interest treatment established
from official sources.

The milestone proves whether the project can preserve the source report,
represent an ordinary non-document circumstance, derive an item-level tax
classification, aggregate the classified item as a tax concept, and project
the result to a simulated return without collapsing those layers. It is first
because every broader milestone otherwise risks encoding the current
source-box-to-form-line shortcut in a larger vocabulary.

### 2. Later-Year Basis Consequence Frontier (updated: 2026-08-27)

Use the accrued-interest basis reduction in one concrete later disposition of
the same synthetic obligation. The primary proposition is whether the existing
fact, rule, derived-artifact, and provenance model can carry that consequence
honestly, or whether the consumer demonstrates a need for a separately durable
item-level determination.

This milestone deliberately applies
[`PROJECT_PLANNING.md`, **Frontier Reduction and Direct-Build
Routing**](../../../PROJECT_PLANNING.md#frontier-reduction-and-direct-build-routing).
It first fixes the later-year consumer, source-year and disposition facts,
correction trace, and failure test on paper. If the accepted model already
serves the consumer, build the bounded path directly. If materially different
representations remain, exercise only the smallest rival prototypes under the
same consumer and lifecycle rubric. The disposition must state what was
eliminated, what survived, and whether a production contract is selected or
still deferred.

It does not design general investment-lot storage, a securities ledger, or a
universal cross-year tax ontology. Before treating broker-reported basis as a
reason to carry another artifact, it checks whether the later statement already
supplies the required value and what product behavior still depends on the
source-year determination.

### 3. Tax Concept Representation Contract

Select the smallest durable production contract only after the later-year
consumer supplies a discriminator. This milestone decides the representation
questions the two slices made concrete: concept identity, item-level
classification, subject and period, rule and authority linkage, coverage,
lifecycle, and the boundary between substantive determination and reporting
projection. If the frontier disposition supports direct use of existing
contracts, narrow this milestone to the missing facts, linkage, or citation
contract rather than creating a new citizen.

### 4. Production Interest Slice and Return Projection

Reimplement the accepted contract in the production record, derivation, and
tax-content paths. Migrate exactly the selected interest slice and bind its
derived concept result to the simulated Form 1040 line-2b route, with synthetic
positive, adjusted, correction, and unsupported-boundary cases.

This milestone is where return-engine development resumes. It is deliberately
not a general taxable-interest expansion: it proves that the new semantic path
can operate inside the real engine and coexist with unmigrated interest
content.

### 5. Detectable Boundary and One Adjacent Expansion

Exercise one materially different taxable-interest case selected for what it
tests, not for census coverage. The preferred candidates are a substantive
exclusion, a timing distinction, or an election-dependent treatment. The
milestone must first show how the build detects or declares the unsupported
region, then implement at most one adjacent expansion if doing so answers the
selected architectural question.

This milestone tests whether the concept and coverage models remain honest as
the domain widens. It does not turn every newly observed category into scope.

### 6. Contrasting Tax Concept

Apply the method to a concept with a different structure, chosen after the
interest work exposes which properties may be accidental. A deduction or
limitation whose result depends on taxpayer circumstances and another derived
quantity is a stronger contrast than another document-box aggregation.

The purpose is to find which parts of the representation are genuinely common
and which belong only to interest. Confirmation in a second concept is evidence
of transfer, not proof of universality.

### 7. Tax-Concept Question and Explanation Projection

Expose the committed model as user assistance: what the source reported, which
ordinary fact changed its treatment, which rule performed the classification,
where the result appears, what question would resolve an open branch, and where
an authoritative answer can be checked.

This milestone comes after production semantics so explanation is projected
from real structure rather than used to compensate for missing structure. It
may produce interface work, but it is not limited to explainability; the same
model must continue to serve computation and return generation.

## Status

| Milestone | State | Project impact |
| --- | --- | --- |
| Reported Interest to Tax Concept Vertical Slice | **Closed 2026-08-28 — no representation recommended** | Tax-domain model, synthetic fixtures, four-packaging comparison, derivation boundary |
| Later-Year Basis Consequence Frontier | **Named, not selected** | Concrete later-year consumer, cross-year consequence, representation discriminator |
| Tax Concept Representation Contract | Not selected | Schemas, citizens, lifecycle, adopted artifacts, ADRs if required |
| Production Interest Slice and Return Projection | Not selected | Record, derivation, tax content, return engine, tests |
| Detectable Boundary and One Adjacent Expansion | Not selected | Coverage profile, boundary detection, one bounded tax expansion |
| Contrasting Tax Concept | Not selected | Cross-domain tax modeling and architecture validation |
| Tax-Concept Question and Explanation Projection | Not selected | Presentation, question routing, provenance, user assistance |

The just-closed plan is
[`milestones/reported-interest-tax-concept-vertical-slice.md`](milestones/reported-interest-tax-concept-vertical-slice.md).
The next milestone is unselected. The named candidate, if chosen, is Later-Year
Basis Consequence Frontier. The retrospective is
[`2026-08-28-reported-interest-tax-concept.md`](../../milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md).

## Starting evidence

The completed Taxable Interest Modeling milestone supplies exploratory
architecture and adversarial cases, not an accepted representation contract.
Its durable contribution is the separation among evidence, reported facts,
economic facts, substantive classification, reporting, execution, claim scope,
and presentation. The opening milestone deliberately instantiates only the
minimum part of that separation needed to distinguish two outcomes over the
same source report.

The Claim Boundary Exploration phase remains useful downstream: once a real
tax-concept derivation exists, its explanation-tree method can test whether a
reader can navigate the result. It does not determine the model's substantive
content.

## Scope control

The taxable-interest universe is a context map, not the opening milestone's
work queue. A candidate enters a milestone only when the plan names:

- the architectural distinction it exercises;
- the observable result that would differ;
- the cheapest evidence capable of resolving the question; and
- the work that is displaced or deferred if the candidate is admitted.

The following are explicitly outside the opening milestone: original issue
discount, education exclusions, nominee ownership, bond-premium and
market-discount elections, frozen-deposit timing, seller-financed mortgage
interest, K-1 interest, joint-return subject modeling, Schedule B attachment
triggers, full line-2b coverage, filing, and user-interface implementation.

## Roadmap reassessment points

Reassess after each of the first four milestones.

- If the opening slice cannot distinguish source report, circumstance, and tax
  classification without a governance or citizen decision, stop before
  production and bring that exact decision to the owner.
- If the later-year basis consumer is served by the current rule-artifact model,
  narrow milestone 3 to the missing facts, linkage, citation, or production
  adoption work rather than inventing a parallel citizen.
- If no concrete later-year behavior distinguishes the representations, defer
  the citizen decision and preserve the bounded requirements instead of
  prolonging the prototype.
- If production integration requires a large migration of existing interest
  families, keep the selected slice working alongside the legacy path and
  schedule migration by concept boundary; do not absorb the entire migration.
- If a contrasting concept breaks the purported common model, preserve the
  domain-specific distinction rather than forcing a universal abstraction.
