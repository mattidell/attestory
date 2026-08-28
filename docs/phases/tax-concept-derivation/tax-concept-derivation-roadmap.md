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

### 2. Tax Concept Representation Contract

Use the vertical-slice evidence to select the smallest durable production
contract. This milestone decides only the representation questions the slice
made concrete: concept identity, item-level classification, subject and period,
rule and authority linkage, coverage declaration, lifecycle, and the boundary
between substantive determination and reporting projection.

It follows the slice so the contract is based on exercised examples rather
than an abstract taxonomy. Prototype conveniences do not become production
contracts by default.

### 3. Production Interest Slice and Return Projection

Reimplement the accepted contract in the production record, derivation, and
tax-content paths. Migrate exactly the selected interest slice and bind its
derived concept result to the simulated Form 1040 line-2b route, with synthetic
positive, adjusted, correction, and unsupported-boundary cases.

This milestone is where return-engine development resumes. It is deliberately
not a general taxable-interest expansion: it proves that the new semantic path
can operate inside the real engine and coexist with unmigrated interest
content.

### 4. Detectable Boundary and One Adjacent Expansion

Exercise one materially different taxable-interest case selected for what it
tests, not for census coverage. The preferred candidates are a substantive
exclusion, a timing distinction, or an election-dependent treatment. The
milestone must first show how the build detects or declares the unsupported
region, then implement at most one adjacent expansion if doing so answers the
selected architectural question.

This milestone tests whether the concept and coverage models remain honest as
the domain widens. It does not turn every newly observed category into scope.

### 5. Contrasting Tax Concept

Apply the method to a concept with a different structure, chosen after the
interest work exposes which properties may be accidental. A deduction or
limitation whose result depends on taxpayer circumstances and another derived
quantity is a stronger contrast than another document-box aggregation.

The purpose is to find which parts of the representation are genuinely common
and which belong only to interest. Confirmation in a second concept is evidence
of transfer, not proof of universality.

### 6. Tax-Concept Question and Explanation Projection

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
| Reported Interest to Tax Concept Vertical Slice | **In closeout — executable slice complete** | Tax-domain model, synthetic fixtures, executed two-shape comparison, derivation boundary |
| Tax Concept Representation Contract | Not selected | Schemas, citizens, lifecycle, adopted artifacts, ADRs if required |
| Production Interest Slice and Return Projection | Not selected | Record, derivation, tax content, return engine, tests |
| Detectable Boundary and One Adjacent Expansion | Not selected | Coverage profile, boundary detection, one bounded tax expansion |
| Contrasting Tax Concept | Not selected | Cross-domain tax modeling and architecture validation |
| Tax-Concept Question and Explanation Projection | Not selected | Presentation, question routing, provenance, user assistance |

The active plan is
[`milestones/reported-interest-tax-concept-vertical-slice.md`](milestones/reported-interest-tax-concept-vertical-slice.md).

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

Reassess after each of the first three milestones.

- If the opening slice cannot distinguish source report, circumstance, and tax
  classification without a governance or citizen decision, stop before
  production and bring that exact decision to the owner.
- If the slice shows that the current rule-artifact model already carries the
  needed semantics recoverably, narrow milestone 2 to the missing declaration
  or linkage rather than inventing a parallel model.
- If production integration requires a large migration of existing interest
  families, keep the selected slice working alongside the legacy path and
  schedule migration by concept boundary; do not absorb the entire migration.
- If a contrasting concept breaks the purported common model, preserve the
  domain-specific distinction rather than forcing a universal abstraction.
