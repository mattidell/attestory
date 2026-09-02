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

### 2. Document and Ordinary-Fact Translation Vertical

Create the first fluid, agent-maintained domain model of the taxable-interest
translation frontier, then establish one source-independent canonical fact
slice in which a Form 1099-INT report and an ordinary account of a bond purchase
can jointly support the accrued-interest treatment.

The milestone treats the canonical layer as selected product direction. It
does not ask whether a document model can serve instead. It maps the broader
frontier for product comprehension, selects only the canonical facts needed by
the bounded slice, prototypes materially different identity or relationship
shapes only when a product behavior discriminates them, and proceeds into the
production interest and line-2b path when no consequential owner decision
remains.

This milestone deliberately tests the cadence of domain map → canonical slice
→ discriminating evidence → production build → simple abstraction. Fusing
several independent architectural decisions into one artifact makes it hard
to attribute a defect to a specific choice, so the milestone decomposes into
six independently chartered seams (canonical value extraction, identity
association, relationship constraints, standing authorization and
currentness, rule-owned consequences, and ordinary input mapping), each
resolved on its own smallest discriminating evidence before any shape is
treated as selected, followed by one integration checkpoint. Its
retrospective decides what should be repeated or simplified before the
roadmap is projected farther. Plan:
[`milestones/document-ordinary-fact-translation.md`](milestones/document-ordinary-fact-translation.md).

### 3. Investment Basis Concept and Coverage Model

Establish a sufficiently complete conceptual model of investment basis —
what has basis, how basis originates, what changes it, when changes apply,
how documentary reports and ordinary circumstances contribute, how
overlapping accounts are reconciled, how an adjusted-basis projection is
produced, and how downstream calculations consume it — so that later
tax-treatment breadth can usually be added inside a stable structure while
tax-category completeness is backfilled separately.

It is sequenced before the later-year basis reuse test and before a first
basis-lifecycle production vertical because both depend on knowing what
"basis" durably means beyond the single accrued-interest adjustment
milestone 2 produced. The milestone concentrates on US-federal individual
investment-property basis (debt obligations and securities), maps
neighboring cases only far enough to test the structure, and normally
stops after the domain model, structural coverage matrix, canonical
propositions, and a consolidated contract specification — not a
production vertical. Plan:
[`milestones/investment-basis-concept-coverage.md`](milestones/investment-basis-concept-coverage.md).

### 4. Later-Year Basis Reuse Test

Use a later disposition of the same synthetic obligation to test whether the
canonical acquisition and obligation model established by milestone 2, and
the adjusted-basis model established by milestone 3, remain coherent when a
basis consequence matters in a later year. Later documentary evidence is an
input to reconcile, not a substitute for the canonical history.

This milestone is deferred until milestone 3's basis model exists. It may
expose new lifecycle or persistence requirements, but it does not reopen
whether documentary and ordinary facts need a shared source-independent model.

### 5. Adjacent Translation Case

Apply the established cadence to one materially different taxable-interest
translation selected for what it tests: ownership and allocation, a substantive
exclusion, or an election-dependent treatment. Map the wider region, build
directly where the canonical contract transfers, and use frontier reduction
only for a genuinely new identity, authority, lifecycle, or interaction
question.

This is the first normalization test. It determines whether the accrued-
interest result is a reusable product method or a case-specific success.

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
| Document and Ordinary-Fact Translation Vertical | **Closed 2026-08-30 — six ADRs accepted (0067-0072).** | Canonical workspace slice, identity association, supportability, standing authorization, rule-owned consequences, ordinary input mapping, legacy-migration decision |
| Investment Basis Concept and Coverage Model | **Active — planned 2026-09-01.** | Basis domain model, structural coverage matrix, canonical propositions, representation-comparison disposition |
| Later-Year Basis Reuse Test | Blocked on milestone 3 | Cross-year reuse, reconciliation, lifecycle and persistence evidence |
| Adjacent Translation Case | Not selected | Cadence normalization, canonical-model reuse, one bounded tax expansion |
| Contrasting Tax Concept | Not selected | Cross-domain tax modeling and architecture validation |
| Tax-Concept Question and Explanation Projection | Not selected | Presentation, question routing, provenance, user assistance |

The Document and Ordinary-Fact Translation Vertical's plan is
[`milestones/document-ordinary-fact-translation.md`](milestones/document-ordinary-fact-translation.md);
its retrospective is
[`2026-08-29-document-ordinary-fact-translation-seams.md`](../../milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md).
The active milestone's plan is
[`milestones/investment-basis-concept-coverage.md`](milestones/investment-basis-concept-coverage.md);
`docs/phase-state.md` is the current, single re-entry pointer.
The prior just-closed milestone remains
recorded in
[`2026-08-28-reported-interest-tax-concept.md`](../../milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md).

## Starting evidence

The completed Taxable Interest Modeling milestone supplies exploratory
architecture and adversarial cases. The reported-interest experiment then
showed that arithmetic and packaging do not decide the canonical model and
that the incumbent cannot accept the ordinary purchase circumstance. Together
they establish the starting distinction among evidence, reported facts,
ordinary circumstances, tax classification, tax concepts, reporting,
execution, claim scope, and presentation. They do not supply the missing
translation layer.

The Claim Boundary Exploration phase remains useful downstream: once a real
tax-concept derivation exists, its explanation-tree method can test whether a
reader can navigate the result. It does not determine the model's substantive
content.

## Scope control

The taxable-interest universe is a fluid domain map, not an implementation
backlog. Agents may broaden that map whenever doing so improves comprehension,
interaction design, refusal, handoff, or roadmap selection. Canonical and
production scope remains selected by product value and evidence. A candidate
enters implementation when the plan names:

- the architectural distinction it exercises;
- the observable result that would differ;
- the cheapest evidence capable of resolving the question; and
- the work that is displaced or deferred if the candidate is admitted.

The active milestone may locate neighboring interest categories in its domain
model but does not implement original issue discount, education exclusions,
nominee ownership, bond-premium and market-discount elections, frozen-deposit
timing, seller-financed mortgage interest, K-1 interest, joint-return subject
modeling, general Schedule B triggers, full line-2b coverage, filing, or a
production graphical interface.

## Roadmap reassessment points

Reassess after each of the next three milestones.

- After the active milestone, decide whether the four-state cadence trial
  (rival/seam evidence, disposable integration evidence, consolidated
  contracts, clean production build) reduced curation cost versus the prior
  milestone, and whether the resulting basis domain model and coverage
  matrix are stable enough to build the named first production vertical
  directly.
- If production integration requires a large migration of existing interest
  families, keep the selected slice working alongside the legacy path unless a
  broader migration has a better explicit value case.
- If the later-year consumer reveals no new product behavior, record the reuse
  result and stop rather than inventing persistence machinery.
- If the adjacent case transfers cleanly, build subsequent instances directly.
  If it exposes a new domain distinction, update the fluid map and reduce only
  that frontier.
- If a contrasting concept breaks the purported common model, preserve the
  domain-specific distinction rather than forcing a universal abstraction.
