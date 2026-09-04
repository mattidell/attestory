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

### 3. Investment Basis Concept and Coverage Model (updated: 2026-09-02)

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

### 4. Later-Year Basis Reuse Test (closed 2026-09-03, updated: 2026-09-03)

Use a later disposition of the same synthetic obligation to test whether the
canonical acquisition and obligation model established by milestone 2, and
the adjusted-basis model established by milestone 3, remain coherent when a
basis consequence matters in a later year. Later documentary evidence is an
input to reconcile, not a substitute for the canonical history.

Milestone 3's basis model now exists, so this milestone is unblocked. It
is also the natural context in which a concrete consumer of a composed
adjusted basis first appears — the consumer milestone 3 lacked, and
therefore the setting in which milestone 3's deferred representation
choice can be tested. Testing it there may discriminate the candidates or
may show no material difference; neither outcome is assumed. It may
expose new lifecycle or persistence requirements, but it does not reopen
whether documentary and ordinary facts need a shared source-independent model.

**Track 0's result, recorded here so the roadmap is not silent about it.**
It did expose a new requirement, and it is prior to the ones this entry
anticipated. **No authorized package/scope contract exists in committed
content for composing a basis consequence into a later disposition
calculation.** A raw same-run rule composes across a report-filter year and
a rule's declared scope year with no injection — proving mixed-scope
same-run computation is mechanically expressible, and proving nothing
about authorization, since nothing in the evaluated path compares
`reporting_year` to a rule's declared `scope.tax_year`. With the report
filter itself set to the later year (one tested configuration, not the
space of possible compositions), re-deriving there fails — the 2025 report
does not associate under a later reporting year, which is correct
behaviour — and carrying it across through the act log fails twice
independently, at persistence and at projection. No adopted 2029 package
exists, no cross-scope composition contract exists in committed content,
and `package_validation.py` independently refuses scope-mismatched package
members (`SCOPE_MISMATCH`). This is recorded as a **fifth composition
gap** (cross-context handoff / scope composition) alongside the four
milestone 3 named; all five are classified must-close and none is closed.
Track 0 therefore closes as an **explicit partial result** and charters no
contract, production, or integration unit. The A/B representation question
was tested: structural differences were observed and executed (pin
topology, blocked-row naming), but no material product discriminator was
established, because no test exercises the explanation walker or any other
downstream consumer of either shape. The choice is **deferred again**, on
that cleaner ground — no material discriminator, not a measured tradeoff —
and also because two of shape B's three recorded structural advantages
cannot be measured under the only reachable experimental access path.

**A byproduct finding, also outside Track 0's boundary to fix:**
`package_validation.py`'s `COLLECT_TARGET_NOT_FAMILY` guard documents
itself as binding "artifact-package.v3 onward" but its allowlist ends at
`artifact-package.v17`, while the production package is
`artifact-package.v26`; the guard has therefore never bound a
`rule-artifact.v7` collect. Recorded and deliberately not fixed; owner's
call.

**Closed 2026-09-03 as an explicit partial result.** Plan:
[`milestones/later-year-basis-reuse.md`](milestones/later-year-basis-reuse.md).
Findings:
[`../../prototypes/later-year-basis-reuse/track-0-findings.md`](../../prototypes/later-year-basis-reuse/track-0-findings.md).
Retrospective:
[`../../milestone-retrospectives/2026-09-03-later-year-basis-reuse.md`](../../milestone-retrospectives/2026-09-03-later-year-basis-reuse.md).
Owner-facing decision areas are surfaced and not taken, each with its own
applicability rather than as a blanket set: (1) the
**contract permitting cross-scope consumption** (gap 5); (2) the later
calculation's **consumption policy** — historical execution, a newly
derived determination, or a policy permitting either — and the distinct
**historical-retention/reportability** question (re-deriving for
consumption does not prevent retaining history for reporting; neither
policy is selected); (3) **authorship of the broker-versus-derived
comparison claim**; (4) whether to repair the **collect-target universe
guard** (`COLLECT_TARGET_NOT_FAMILY`) recorded in
`packages/derivation/package_validation.py` (byproduct finding, outside
this milestone's boundary to fix). Re-executing the existing 2025 seam
required no new schema or kernel machinery — that is executed and true —
but end-to-end later-year use remains unbuilt, and the milestone did not
establish whether resolving gap 5 (or the other composition gaps)
requires schema, kernel, package, content, or other changes.
**Consequence for later items:** gap 5 (the cross-context handoff /
scope-composition gap) is a prerequisite for a consumer that must use a
determination from another tax context or scope — not for every later-year
calculation. **Milestone 5 (Adjacent Translation Case) remains selectable**;
gap 5 becomes a prerequisite for it only if the case it selects turns out to
need a determination from another tax context or scope. None of the five
composition gaps this phase has now named is closed. A milestone selecting a
first basis-lifecycle production vertical resolves the owner-held questions
that its own selected case actually reaches — the cross-scope contract for
cross-context reuse; the consumption policy when selecting what a later
calculation consumes; historical retention/reportability only when that
capability is selected; broker-comparison authorship when documentary
reconciliation is in scope; and the collect-target guard if the chosen route
depends on that traversal, otherwise as an independent maintenance decision.

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
| Investment Basis Concept and Coverage Model | **Closed 2026-09-02 — explicit partial result.** | Basis domain model, structural coverage matrix, canonical propositions, A/B representation comparison deferred at paper (no forcing consumer), four named composition gaps recorded as reopening triggers |
| Later-Year Basis Reuse Test | **Closed 2026-09-03 — explicit partial result** | Access experiments vs representation strategy held separate. **Neither strategy supplies a production-authorized later-year delivery path today** (raw same-run mixed-scope computation does produce the value): AS-1 is blocked twice and needs a *successor* publication-act schema plus an independent projection change; AS-2 re-executes the 2025 seam with no new schema or kernel machinery for that seam, but end-to-end later-year use remains unbuilt and delivery under an authorized package/scope contract is unestablished. Consumption policy and historical retention are distinct open questions, not a forced choice. A **fifth composition gap** — cross-context handoff / scope composition, i.e. the absence of an authorized package/scope contract for composing the 2025 determination into a later disposition calculation — joins the four inherited ones, and a cross-context basis-reuse vertical meets it first. Structural differences (pin topology, blocked-row naming) were observed and executed on two run observables, but no material product discriminator was established, so the A/B choice is deferred again on that ground, not a measured tradeoff |
| Adjacent Translation Case | Not selected | Cadence normalization, canonical-model reuse, one bounded tax expansion |
| Contrasting Tax Concept | Not selected | Cross-domain tax modeling and architecture validation |
| Tax-Concept Question and Explanation Projection | Not selected | Presentation, question routing, provenance, user assistance |

The Document and Ordinary-Fact Translation Vertical's plan is
[`milestones/document-ordinary-fact-translation.md`](milestones/document-ordinary-fact-translation.md);
its retrospective is
[`2026-08-29-document-ordinary-fact-translation-seams.md`](../../milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md).
**Roadmap changes on 2026-09-02.** Items 3 and 4 are annotated because
both changed after initial planning. Item 3 was planned to stop after a
consolidated contract specification and, if the evidence allowed, to name
a first production vertical; it closed instead as an explicit partial
result, because no concrete consumer distinguishes the candidate
adjusted-basis representations and four concrete gaps stand between the
established concept and a buildable vertical. Item 4 changed from
"blocked on milestone 3" to unblocked, and gained a second purpose: it is
now also the context in which milestone 3's deferred representation
choice can be tested, since a later-year disposition is where a consumer
of a composed adjusted basis first appears. That test may discriminate
the candidates or may show no material difference.

**Roadmap change on 2026-09-02 (second entry).** Item 4 became the
**selected** milestone; its plan is
[`milestones/later-year-basis-reuse.md`](milestones/later-year-basis-reuse.md).
The plan constrains it against a hazard the roadmap language did not name:
the repository contains only `packages/content/tax/2025/`, so the milestone
must not silently become the implementation of a 2026 package. Production
tax-year content is a boundary to surface to the owner rather than a step
to take. The plan also separates two dimensions the roadmap entry had
folded together — **access** (how a later calculation obtains the earlier
consequence) and **representation** (the deferred aggregate-versus-
components choice) — and fixes the evidence posture: a disposable
in-memory consumer would establish only that the rule vocabulary can
express the calculation, not that a later run *finds* an earlier result, so
one narrow disposable persisted-boundary experiment against a
manual-injection negative control is required. That separation is what let
the milestone keep consumption policy and historical retention as distinct
open questions while the representation question stays deferred.

**Two carry-forwards from item 4 that bear on later selection.** First, the
**fifth composition gap** — cross-context handoff / scope composition —
which a **cross-context basis-reuse** vertical meets before any of the four
inherited gaps, so no implementation item whose consumer must use a
determination from another tax context or scope is selectable until the owner
settles it.
Second, a **validator/authority gap in committed product code**, recorded
and deliberately not fixed, that being outside the milestone's boundary:
`packages/derivation/package_validation.py`'s collect-target universe guard
documents itself as binding "artifact-package.v3 onward" but its allowlist
ends at `artifact-package.v17`, so it is inactive for the current
`artifact-package.v26` production package and has never bound a
`rule-artifact.v7` collect. That is an **owner decision item independent of
this phase's milestone sequence**, and any future claim that a
source-family-authorized traversal has been established must be re-run
against a repaired guard.

**Roadmap change on 2026-09-03.** Item 4 **closed** as an explicit partial
result — see the item-4 entry above for the full account. Its plan is
[`milestones/later-year-basis-reuse.md`](milestones/later-year-basis-reuse.md);
its retrospective is
[`2026-09-03-later-year-basis-reuse.md`](../../milestone-retrospectives/2026-09-03-later-year-basis-reuse.md).
No milestone is currently selected. The prior just-closed milestone's plan
is
[`milestones/investment-basis-concept-coverage.md`](milestones/investment-basis-concept-coverage.md);
its retrospective is
[`2026-09-02-investment-basis-concept-coverage.md`](../../milestone-retrospectives/2026-09-02-investment-basis-concept-coverage.md).
It closed as an explicit partial result: the basis domain model, coverage
matrix, and canonical propositions are established, while the A/B
representation choice was deferred at paper for want of a concrete
consumer — item 4 supplied that consumer. `docs/phase-state.md` is the
current, single re-entry pointer. An earlier just-closed milestone remains
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
