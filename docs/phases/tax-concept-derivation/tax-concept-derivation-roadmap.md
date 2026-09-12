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
calculation. **Milestone 5 (Nominee Interest Ownership Translation) is now
CLOSED (2026-09-05)**, and **gap 5 did not bind it**: the bounded nominee case is
same-year and same-report throughout, so it never needed a determination from
another tax context or scope.
None of the five
composition gaps this phase has now named is closed. A milestone selecting a
first basis-lifecycle production vertical resolves the owner-held questions
that its own selected case actually reaches — the cross-scope contract for
cross-context reuse; the consumption policy when selecting what a later
calculation consumes; historical retention/reportability only when that
capability is selected; broker-comparison authorship when documentary
reconciliation is in scope; and the collect-target guard if the chosen route
depends on that traversal, otherwise as an independent maintenance decision.

### 5. Nominee Interest Ownership Translation

Apply the established cadence to one materially different taxable-interest
translation: a payer reports interest to the taxpayer, while the taxpayer says
that a stated portion belongs to another non-spouse owner. Preserve the payer
report, solicit an ordinary ownership/allocation statement, derive the
ownership-based return adjustment (the taxpayer's share and Schedule B nominee
reduction), and separately determine what facts establish any
information-reporting consequence -- without asking the user to supply the tax
classification.

The two consequences are not assumed to share a factual predicate, and neither
is assumed to follow automatically from the other. The Schedule B instructions
speak broadly of interest belonging to another person; IRC 6049(a)(2) speaks of
a nominee who makes payments to that person. Establishing what separately
supports each is assigned to planning gate P2.

**CLOSED 2026-09-05.** The first normalization test answered its question: the
accrued-interest method **does** transfer from a purchase circumstance to an
ownership-allocation circumstance. Supportability transfers unchanged
(ADR-0070 Decisions 8–10); report association, rule-owned consequences,
ordinary-input mapping, and legacy coexistence are **bounded extensions**; owner
cardinality is a **new decision**.

Track 0 completed at the **paper** evidence rung across three reviewed
checkpoints and returned a **decision-ready contract proposal** — eleven clauses
a production successor must satisfy. Adversarial closure: artifacts 1–5 PASS,
artifact 6 N-A (no successor producer of an externally bound symbol proposed).
**No production code, schema, ADR, or test changed.**

**Bounded capability delivered:** a reviewed contract **proposal** for nominee
ownership translation — specified and independently reviewed, but **not an
accepted contract**: no ADR or schema is proposed or ratified by this milestone. **Not delivered, by design:** any implementation. The
plan's contract, production, and integration units remain **conditional and
unchartered**.

**Deferred, with triggers:** the R-A/R-B representation choice (no case
discriminates them); owner-cardinality shapes; the explanation extension that
would expose attribution to a reader; whether N12's onward transfer falls within
another § 6049 route. The three information-reporting formulations remain
**unreconciled by design** — a unified predicate would require authoritative
reconciliation beyond what Gate P2 could retrieve, and the owner may set a
product posture but does not determine unresolved law.

**Production gate (owner disposition, 2026-09-05).** T0-F5 is deferred: no
production or integration unit may be accepted as complete for a state combining
required Schedule B presentation with a nonzero pairing-scoped current-year
adjustment, until it is repaired. Inherited, not caused by nominee interest.

Plan:
[`milestones/nominee-interest-ownership-translation.md`](milestones/nominee-interest-ownership-translation.md).
Retrospective:
[`2026-09-05-nominee-interest-ownership-translation.md`](../../milestone-retrospectives/2026-09-05-nominee-interest-ownership-translation.md).

### 6. Assertion Standing and Retraction Semantics

Establish how a human-authored answer to a stable fact becomes current, is
corrected, is retracted without asserting an opposite value, and is later
asserted again. The milestone starts from that product lifecycle rather than
repurposing entity succession or source-family membership because those
mechanisms happen to remove a finding from one current view.

The forcing case is the ordinary allocation statement surfaced by milestone 5,
but the result is a bounded substrate contract rather than nominee-interest tax
content. It must also resolve the observed disagreement between full currency
projection and admission-time current-value readers, so every affected consumer
agrees about whether an answer currently supplies support.

**CLOSED 2026-09-06.** Both planning gates ran as reviewed cycles before any
charter. Track 0 selected a dedicated act ending one finding's current support
and disqualified entity succession and source-family withdrawal on executed
evidence. ADR-0073 states the contract; one resolution of current standing now
serves every reader, closing a production check that read a withdrawn
filing-status authority as though it still stood. Fifteen fact types remain
un-withdrawable because capability limits sit in the admission layer; that
relocation is deferred to a successor milestone by owner disposition and is not
a property of withdrawal. Plan:
[`milestones/assertion-standing-retraction-semantics.md`](milestones/assertion-standing-retraction-semantics.md);
retrospective: [`docs/milestone-retrospectives/2026-09-06-assertion-standing-retraction-semantics.md`](/docs/milestone-retrospectives/2026-09-06-assertion-standing-retraction-semantics.md).

### 7. Nominee Allocation Assertion Recording

The first production stage of nominee-interest support, built on item 6's
assertion-standing contract. Records the ordinary, attributed statement
that a stated amount from one identified payer report belongs to one named other
person, with stable proposition identity, correction, retraction, reassertion,
and recoverable provenance. Do not ask the user to supply the nominee-interest
tax classification.

This stage is separate from deriving the nominee reduction, reconciling the
legacy adjustment, and integrating line 2b and Schedule B. It consumes item 6's
lifecycle contract rather than an entity or source-family workaround.

**CLOSED 2026-09-08; owner-directed repairs 2026-09-08.** Two reviewed planning
gates ran before any charter, and three tracks. Tracks 1 and 2 were each
independently reviewed READY; Track 0 was closed by the Foreman on executed
evidence rather than by an independent reviewer. Delivered: the
`tax.us.nominee-allocation.amount` fact type (`bundle.v2` / `fact-type.v2`,
keyed `payer` + `statement` + `tax-year` + `recipient`, sharing the committed
box-1 report's identity components, `exclusiveMinimum: 0`, `free` supersession,
no admission invariant over the amount); the
`tax.us.interest-allocation-recipient` entity kind with an application-minted
opaque workspace id; a producer that persists assertion and correction through
the real contribution boundary; a separate bounded retraction operation on
`act-finding-retracted.v1`; and recovery of current allocations and historical
retracted assertions (what was said, who said it, who later ended current
support), labels, contribution and evidence provenance, attribution, and the
report join from a committed act log alone. An allocation assertion requires
current `ordinary-language-entry` evidence whose submitted answers correspond
to the mapped finding; missing, malformed, document-report, and unrelated
modes are refused; production contribution construction does not invent
whether the interaction was synthetic. **Hard gate:** no user-facing
production caller may rely on `assert_nominee_allocation` until resumable or
idempotent recovery of a persisted multi-act prefix is closed.

The selected operation is **workspace-support retraction** under a **shared**
workspace model: one current answer per report and recipient, any recorded actor
may correct or retract it, actor is opaque provenance and never
admission-validated, and no durable text claims the original actor recanted.
The entity and source-family lifecycle candidates were disqualified on executed
evidence — both remove the fact, so the proposition ceases to exist and its
identity must be abandoned to answer again.

Deferred with triggers: author-bound recantation and permission rules;
author-indexed propositions and conflict reconciliation; recipient display-name
correction (`entity.v1` labels are immutable); the R-B source-independent
association model; and A10's routing destination, which no committed module
owns. T0-F5 remains deferred behind its hard production gate. Plan:
[`milestones/nominee-allocation-assertion-recording.md`](milestones/nominee-allocation-assertion-recording.md);
retrospective:
[`2026-09-08-nominee-allocation-assertion-recording.md`](../../milestone-retrospectives/2026-09-08-nominee-allocation-assertion-recording.md).

### 8. Nominee Interest Tax Consequence and Supportability (updated: 2026-09-09)

The second production stage of nominee-interest support. Consume the current,
attributed ordinary allocation statements delivered by item 7 and let an
adopted tax rule derive a report-scoped nominee reduction and taxpayer
remainder. Prove zero-, single-, multi-recipient, over-allocation, correction,
retraction, reassertion, and cross-report behavior with truthful provenance.

This stage deliberately stops before legacy migration and return presentation.
It must first determine how the real runner groups current recipient-level
allocations for one report and what authority supports the zero-allocation
case. The semantic over-allocation posture from ADR-0070 is a precedent; its
pairing-specific implementation is not assumed to transfer. The milestone also
preserves the prior authority-indexed information-reporting boundary rather than
inventing one normalized legal predicate.

Three independently reviewed planning checkpoints precede Track 0. Production
begins only after the product/tax boundary, committed artifact map, and
executable design agree. The Schedule B T0-F5 defect remains a hard gate on the
later legacy-and-return-integration stage; it does not prevent this internal
tax-consequence stage from being built and tested outside the affected return
surface.

**CLOSED 2026-09-09.** Three independently reviewed planning gates ran before
any charter, then a paper Track 0 contract closure, a ratified ADR, and two
implementation tracks. ADR-0074 was independently reviewed and owner-ratified
before Track 1 implemented against it; Track 1 and Track 2 were each
independently reviewed, and Track 1 took two owner-directed repairs after its
review.

Delivered, bounded exactly: an adopted rule derives a report-scoped nominee
reduction from the current attributed allocation assertions of one identified
Form 1099-INT report, executing through the real projection, marshalling,
package, and `run()` boundary on `package.core-calculations` v36 — **for
uniquely rendered identities**. The remainder is observed only, not published.
The result is a `RunResult` publication, not act-log standing. Whole-set
over-allocation blocks the report group without clamping, subsetting, or a
negative remainder; a report with no current allocation produces no nominee
consequence at all rather than a published zero; groups stay isolated across
reports and across tax years.

New citizens: `bound_sources` on `rule-artifact.v8` — deliberately not a
`collect`, and therefore outside ADR-0035's collect-family requirement rather
than exempted from it; `artifact-package.v28`; and `derivation-record.v9`, whose
`no_groups_selected` inapplicable branch is scoped **in the schema** to the
nominee rule alone. **ADR-0074** narrows ADR-0020 Decisions 1/1a/4 for that exact
rule id only, and introduces no reusable grouped-rule class or marker.

Not done, and deliberately: Form 1040 line 2b, Schedule B, legacy
nominee migration, information-return filing, and UI. **T0-F5 remains a hard
gate** on the later legacy-and-return-integration stage. A second dependency
joins it: the kernel's `fact_id` rendering is **non-injective**, so this
milestone's coordinator refuses ambiguously rendered identities at execution
time — a guard, not an intake gate. Closing that needs either a general identity
repair or a real pre-execution intake restriction; neither is chosen here.

Plan:
[`milestones/nominee-interest-tax-consequence-supportability.md`](milestones/nominee-interest-tax-consequence-supportability.md).
Retrospective:
[`../../milestone-retrospectives/2026-09-09-nominee-interest-tax-consequence-supportability.md`](../../milestone-retrospectives/2026-09-09-nominee-interest-tax-consequence-supportability.md).

### 9. Nominee Interest Return Integration (closed 2026-09-12, updated: 2026-09-12)

Complete the nominee-interest vertical by connecting the current report-scoped
reduction to the bounded 2025 taxable-interest calculation and Schedule B Part I
presentation. Repair T0-F5 so Schedule B accounts for the pairing-scoped
current-year adjustment already subtracted by line 2b, add nominee status as an
independent Schedule B trigger below the ordinary dollar threshold, and ensure
the new consequence is subtracted exactly once.

This is not a mechanical wiring milestone. The legacy path asks the user to
enter a tax-labelled Schedule B adjustment that cannot be assumed to identify
the report, recipient, attribution, or ordinary proposition represented by the
new allocation facts. Planning must therefore select an explicit compatibility,
transition, or refusal policy for legacy-only, new-only, and both-present
workspaces. It must also close the current ambiguous-identity failure before a
durable run start or output reservation, either with a general identity repair
or a clean pre-execution refusal.

The result remains bounded. It does not establish that the repository's
`tax.us.2025.interest.taxable-total` is a complete model of Schedule B line 4 or
Form 1040 line 2b; the known section 135/Form 8815 and broader interest-coverage
gaps remain. The plan develops tax/form, artifact/consumer, and executable
design evidence in independently reviewed increments before Track 0 or
implementation.

Plan:
[`milestones/nominee-interest-return-integration.md`](milestones/nominee-interest-return-integration.md).
Retrospective:
[`../../milestone-retrospectives/2026-09-12-nominee-interest-return-integration.md`](../../milestone-retrospectives/2026-09-12-nominee-interest-return-integration.md).

### 10. Contrasting Tax Concept

Apply the method to a concept with a different structure, chosen after the
interest work exposes which properties may be accidental. A deduction or
limitation whose result depends on taxpayer circumstances and another derived
quantity is a stronger contrast than another document-box aggregation.

The purpose is to find which parts of the representation are genuinely common
and which belong only to interest. Confirmation in a second concept is evidence
of transfer, not proof of universality.

### 11. Tax-Concept Question and Explanation Projection

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
| Nominee Interest Ownership Translation | **Closed 2026-09-05 — Track 0 complete at the paper rung; decision-ready contract proposal; no implementation chartered** | First cadence-normalization test: ownership/allocation translation, legacy nominee-path reconciliation, and early independent review during planning and Track 0 |
| Assertion Standing and Retraction Semantics | **Closed 2026-09-06** | Withdrawal without a replacement value; one current-standing path across every reader; ADR-0073 |
| Nominee Allocation Assertion Recording | **CLOSED 2026-09-08** | Ordinary allocation assertion recorded, corrected, retracted from current use, asserted again, and recovered from the log with attribution; no tax consequence or return integration |
| Nominee Interest Tax Consequence and Supportability | **CLOSED 2026-09-09** | Rule-owned report-scoped nominee reduction derived and executed on package v36 for uniquely rendered identities, with whole-set blocking, cross-report and cross-year isolation, and walkable provenance; remainder observed only; no return integration, legacy migration, or information reporting |
| Nominee Interest Return Integration | **CLOSED 2026-09-12** | Bounded line-2b and Schedule B integration on package v38; T0-F5 repaired; nominee applicability below threshold; legacy-only / new-only / both-present refusal; pre-run identity refusal. Form 8815 / §135, filing, general fact-id repair, and I4 causal-block explanation remain out |
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
ends at `artifact-package.v17`, so it was inactive for the then-production
v35 / `artifact-package.v26` package and remains inactive for the current
v36 / `artifact-package.v28` package. It has never bound a `rule-artifact.v7`
collect. That is an **owner decision item independent of
this phase's milestone sequence**, and any future claim that a
source-family-authorized traversal has been established must be re-run
against a repaired guard.

**Roadmap change on 2026-09-03.** Item 4 **closed** as an explicit partial
result — see the item-4 entry above for the full account. Its plan is
[`milestones/later-year-basis-reuse.md`](milestones/later-year-basis-reuse.md);
its retrospective is
[`2026-09-03-later-year-basis-reuse.md`](../../milestone-retrospectives/2026-09-03-later-year-basis-reuse.md).
At that checkpoint no next milestone had been selected. The earlier milestone
plan referenced by that decision was
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
