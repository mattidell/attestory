<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "investment-basis-concept-coverage",
  "status": "Planned. The milestone maps investment basis as a lifecycle, states the canonical propositions the application must be able to make about it, tests them against eight representative cases, and compares candidate adjusted-basis representations. It normally stops after the domain model, coverage account, discriminating evidence, and a consolidated contract specification.",
  "scope": [
    "build a plain-language, owner-readable domain model of US-federal individual investment-property basis (debt obligations and securities as the primary region), keeping evidence, ordinary circumstance, tax determination, adjusted basis, calculation consumption, and presentation as six distinct layers",
    "state canonical propositions the application must be able to assert about basis before selecting any storage shape for them",
    "build a structural coverage matrix distinguishing supported, structurally accommodated, unresolved, and excluded basis cases, tested against eight representative cases spanning increase, decrease, timing, reconciliation, allocation, correction, non-purchase origin, and consumption",
    "compare current-value-only, separately-preserved-components, and hybrid adjusted-basis representations by product behavior (explanation, correction, as-of calculation, overlap/double-count prevention, allocation, rule succession, unsupported disclosure), using the cheapest evidence rung that can discriminate them per proposition",
    "consolidate whatever the evidence selects into a written contract specification before any reuse of prototype or integration code in a production path",
    "name the exact first production vertical the consolidated contracts make buildable without reopening the basis concept"
  ],
  "non_goals": [
    "no universal property, partnership, business-asset, depreciation, estate, or gift-tax basis ontology",
    "no Form 8949 production vertical, general basis ledger, cross-year persistence, or broad production integration in this milestone",
    "no rival prototype built merely for symmetry when paper evidence already discriminates a proposition",
    "no successor ADR correcting another ADR authored within this same milestone; a provisional decision is repaired or consolidated before it becomes accepted, not superseded after acceptance",
    "no treatment of the existing accrued-interest basis consequence (ADR-0071) as the complete basis, adjusted-basis, broker-reconciliation, or disposition concept merely because it already exists",
    "no general process-document edits; this milestone's cadence trial is recorded in its own retrospective, not folded into PROJECT_PLANNING.md"
  ],
  "deep_reads": {
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Owner Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "PROJECT_PLANNING.md#Frontier Reduction and Direct-Build Routing",
      "PROJECT_PLANNING.md#Prototype Economic Gates",
      "docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md#Canonical propositions before storage",
      "docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md#Representation comparison",
      "docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md#Process boundary: four states, not two",
      "docs/domain-models/taxable-interest-translation.md#Cross-year handling: three distinct years, never conflated",
      "docs/adr/0071-rule-owned-current-year-and-basis-consequences.md",
      "docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md#A process boundary the next milestone should draw earlier",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "PROJECT_PLANNING.md#Prototype Economic Gates",
      "docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Investment Basis Concept and Coverage Model

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `investment-basis-concept-coverage`
- State: planned
- Execution posture: domain mapping and paper evidence first; bounded
  prototype evidence only where a product behavior actually discriminates
  between representations; consolidation before any code reuse

## Purpose

Establish a sufficiently complete conceptual model of investment basis
that later tax-treatment breadth can usually be added inside a stable
structure while tax-category completeness is backfilled separately. This
is not a milestone to enumerate or implement every basis rule — it
designs the grammar of investment basis: what has basis, how basis
originates, what changes it, when changes apply, how documentary reports
and ordinary circumstances contribute, how overlapping accounts are
reconciled, how an adjusted-basis projection is produced, and how
downstream calculations consume it.

The milestone should leave the owner able to understand: the stable
backbone of investment basis; which representative tax applications have
demonstrated that backbone; which applications appear structurally
accommodated but remain unbuilt; which cases remain unresolved and could
force the model to reopen; and the exact first production vertical that
should follow.

## Owner-model alignment

`OWNER_MODEL.md`'s Domain Model Model already establishes that a document
model, an ordinary-language interaction, a canonical workspace model, a
tax derivation, and a return presentation can represent related subject
matter for different purposes without becoming the same model, and that
domain models are working material agents may create, revise, or discard
on their own initiative. This milestone applies that directly: it keeps
evidence and attributed reports, ordinary circumstance, tax determination,
adjusted basis, calculation consumption, and presentation as six distinct
layers throughout, rather than letting the layer that already has code
(the ADR-0071 accrued-interest basis consequence) stand in for the whole
concept.

## Layers kept distinct throughout

1. Evidence and attributed reports.
2. Ordinary acquisition, ownership, and lifecycle circumstances.
3. Tax determinations establishing a basis origin or adjustment.
4. Adjusted basis as of a stated time, for a stated property and purpose.
5. Calculations that consume that adjusted basis.
6. Presentation, explanation, coverage, and refusal.

Two accounts must stay separate wherever the current accrued-interest
basis consequence is discussed, because they are easy to collapse into
one:

- **The tax proposition** (RC2, below): when the pre-acquisition accrued
  interest a buyer paid to a bond seller is later received, it is a
  return of the buyer's own capital investment, reducing the buyer's
  remaining basis in the bond. This is a genuine layer-3 proposition,
  fully in scope for this milestone's domain model.
- **The committed representation** (ADR-0071,
  `BASIS_RULE_ID = "tax.us.2025.rule.basis.item-level-consequence.pairing-scoped"`
  in `packages/tax/pairing_consequences.py`, publishing
  `packages/content/tax/2025/rule.basis.item-level-consequence.pairing-scoped.json`):
  this rule republishes the nonnegative accrued-interest amount into a
  pairing/tax-year-identified finding. Its own committed content does not
  encode the affected property or lot, the adjustment's direction, the
  receipt/effective event, the basis purpose the adjustment serves, an
  adjusted-basis result, or a downstream consumer — the rule's own
  `notes` field states plainly that "a later-year disposition consumer
  of this finding is still open."

The committed representation is real, useful evidence for what it
actually proves: an amount is correctly derived and provenanced, its
publication is independently supersedable from the current-year
adjustment, and correction reaches it through shared dependency pins
(see the Representation comparison section). It is not itself a complete
layer-3 basis-adjustment citizen, is not adjusted basis (layer 4),
broker-basis reconciliation (layers 1+4), or a disposition result (layer
5). This milestone does not let the committed artifact define the wider
concept merely because it already exists; it treats it as a partial
implementation exhibit for one representative case, not as a settled
instance of the general layer-3 shape.

## Scope

Concentrate on US-federal individual investment-property basis, using
debt obligations and securities as the primary region. Map neighboring
cases (partnership interests, depreciable business property, estate/gift
basis) only far enough to test the structure — not to resolve them. Use
official controlling authority for controlling tax propositions; IRS
forms and instructions establish reporting operation, and official
publications may supply explanation but are not complete tax ontologies.

## Representative cases

| Case | What it tests | Structural role |
| --- | --- | --- |
| RC1 ordinary cost basis | Starting basis from a purchase | Origin |
| RC2 accrued interest paid to a bond seller (Treas. Reg. § 1.61-7(c), whose text reaches this buyer-side situation — return-of-capital/basis-reduction for interest accrued before purchase — corroborated by IRC § 61(a)(4), Pub. 550's "Bonds Sold Between Interest Dates," and the seller-side Treas. Reg. § 1.61-7(d)) | The tax proposition: a return-of-capital reduction to remaining basis when the pre-acquisition accrued interest is received. A required tax case and a partial implementation exhibit — ADR-0071's committed rule derives and provenances the amount but does not yet encode property/lot identity, direction, effective event, purpose, or a consumer (see "Layers kept distinct" above) | Decrease-on-receipt; required case, partially exhibited |
| RC3 original issue discount on a specific taxable OID debt instrument accrued during the ordinary holding period (excludes stripped bonds, market discount, and contingent-payment debt instruments) | A basis increase under the OID accrual rules for that bounded instrument type and holding pattern | Increase, rule-derived (bounded fact pattern; the assumptions, not "OID in general," are what this milestone maps) |
| RC4a taxable-bond premium amortization: election under IRC § 171(c), amortizable amount under § 171(b), deduction under § 171(a)(1), basis adjustment under § 1016(a)(5) | A basis decrease contingent on the taxpayer's affirmative § 171(c) election, computed under § 171(b) and deducted under § 171(a)(1) | Decrease, election-dependent |
| RC4b tax-exempt-bond premium amortization: § 171(a)(2) disallows the § 171(a)(1) deduction; § 1016(a)(5) still requires the basis adjustment | A basis decrease required regardless of any election, under a structurally different authority chain than RC4a (no deduction, but the same basis-adjustment provision applies) | Decrease, mandatory |
| RC5 broker-reported basis overlapping a product-derived adjustment | Reconciliation between an institutional report and the product's own determination | Reconciliation |
| RC6 partial disposition or lot allocation | Basis attaches to a portion, not the whole position | Allocation |
| RC7 a non-purchase basis origin (e.g. gift or inherited-property basis), mapped as a boundary | Whether the origin concept generalizes past "cost" | Origin boundary, deliberately not built out |
| RC8 correction of an earlier acquisition, adjustment, association, or report | Whether corrections displace exactly their dependents, traced directly across origin, adjustment, report, association, projection, and consumer | Correction (displacement only — see Q7/Q8 for the distinct duplicate-entry question) |

RC2's committed rule output is not reprototyped — this milestone does not rebuild
or re-derive the amount ADR-0071 already publishes. But RC2's *tax
proposition* is not settled by that committed output, and this milestone must
still determine how the proposition maps to property identity, direction,
effective event, purpose, lifecycle, and consumption; the domain model,
canonical propositions, and representation comparison must be honest
about which of those the committed exhibit answers and which remain
open. RC1, RC3–RC8 are mapped at the cheapest evidence able to decide
their architectural question (per the routing table below); not every
case needs an executable prototype.

## Required conceptual work

The domain model (revising or extending
`docs/domain-models/taxable-interest-translation.md`'s sibling — a new
`docs/domain-models/investment-basis.md`) must cover, in plain language
first and with only as much structure below that as needed for
comprehension:

- the property, obligation, security, lot, or portion to which basis
  belongs;
- the tax subject or owner;
- the origin of starting basis;
- basis-affecting events and adjustments;
- amount, direction, currency, effective event, and time;
- governing rule and cited authority;
- evidence and ordinary facts supporting each determination;
- allocation across lots or portions;
- reconciliation with institutionally reported basis;
- purpose-specific use where applicable (e.g. gain/loss on disposition
  versus another consumer);
- corrections, invalidators, supersession, and currentness;
- downstream consumers; and
- supported, structurally accommodated, unresolved, and excluded coverage.

This coverage matrix is a deliberately authored, evidence-cited working
model: for each representative case and canonical proposition it states
which coverage state applies and cites the paper evidence or accepted
contract that supports the claim. It is explicitly not derived
automatically from committed state, and it is a different instrument from
`packages/tax/coverage.py`'s `untranslated_source_findings` — a narrower,
mechanically derived structural read of which fact types the adopted
package's own content never consumes (see
`docs/domain-models/taxable-interest-translation.md`, "T9"). The two
serve different purposes and must not be conflated: the domain coverage
matrix can and should describe cases with no code or fact type at all
(RC7's non-purchase origin, for instance), which a package-consumption
read model has no way to see.

Seek conceptual saturation, not tax-rule enumeration: the useful test at
each step is whether a materially different case (drawn from RC1–RC8)
fills the existing dimensions above or forces a new foundational kind of
proposition. Claim saturation using bounded conceptual adequacy, not an
arbitrary run-length rule: every predeclared structural axis (origin,
increase, decrease, timing, reconciliation, allocation, correction,
consumer) must be exercised by at least one contrasting representative
case; any axis RC1–RC8 does not exercise must be named explicitly rather
than silently assumed covered; and the resulting claim is "adequate for
the bounded US-federal individual investment-property region this
milestone scopes," never "proof of general completeness" — a materially
different case from outside that region (a different property class, a
different jurisdiction) is not evidence against an adequacy claim scoped
this way.

## Canonical propositions before storage

Before selecting schemas or implementation shapes, state what the
application must be able to say. At minimum, investigate propositions of
these forms, each grounded in a representative case above:

1. An identifiable investment has a supported basis origin. (RC1, RC7)
2. A named event creates a basis adjustment. (RC2, RC3, RC4a, RC4b)
3. The adjustment applies to a named property, lot, or portion. (RC6)
4. It becomes applicable at a stated event or time. (RC2, RC4a, RC4b)
5. An external report does or does not establish that the adjustment is
   already reflected. (RC5)
6. Applicable components produce an adjusted basis as of a stated point.
   (all)
7. A downstream calculation relied upon that basis. (layer 5 consumer,
   named but not built — see non-goals)
8. A correction displaced the affected components and dependent results.
   (RC8)

Each proposition gets a plain-language statement, two positive instances,
two meaningful negatives, and a producer → authority → consumer → failure
map before any schema is drafted, per PROJECT_PLANNING.md's Gate 2. One
shared paper scenario may supply evidence for several propositions at once
when it genuinely exercises each. Economy is preserved this way rather
than by narrating forty separate examples; what is not permitted is
dropping proposition-by-proposition traceability — each proposition's
evidence table cites exactly which scenario(s) support it, and *which
account* (the paper tax lifecycle or the committed machinery) actually
supports it, even when the scenario is shared.

**RC2 specifically, rechecked proposition by proposition:** RC2's paper
tax lifecycle (return of capital on receipt, reducing basis) is positive
evidence for proposition 2 (the receipt event creates the adjustment) and
proposition 4 (it becomes applicable at that stated receipt event, not at
acquisition). RC2's *committed machinery* is weaker evidence for both:
the rule fires whenever the pairing's supportability verdict passes, with
no field distinguishing a receipt event from the acquisition itself — so
This milestone must treat "does the committed rule actually model the receipt
event, or only the acquisition-time amount" as an open question, not an
assumed yes. RC2 is **not** positive evidence for proposition 3 (property,
lot, or portion) under either account — the paper lifecycle's single bond
does not exercise allocation, and the committed rule encodes no
property/lot field at all; RC6 remains the case that tests proposition 3.
RC2 contributes to proposition 6 (adjusted basis as of a stated point)
only as a paper lifecycle instance of one adjustment feeding into a
larger adjusted-basis computation that this milestone has not yet built;
the committed rule publishes an amount, not an adjusted-basis projection,
so it is not evidence for proposition 6 by itself.

## Representation comparison

Evaluate, without presupposing the answer, three candidate shapes for
"adjusted basis as of a stated time, for a stated property and purpose".
**Every candidate retains the underlying source evidence and ordinary
facts (layers 1 and 2) unconditionally** — evidence and attributed
reports and ordinary circumstance facts are never at stake in this
comparison; what differs between A, B, and C is only what becomes
*canonical at layer 3/4* (which tax determinations get a durable,
independently addressable identity, versus which are folded directly
into a number):

- **A. Current adjusted-basis value only.** No separately durable tax
  determination citizens; each basis-affecting event is applied directly
  to a running number per property/lot, recomputed forward. What A
  retains for provenance, correction, and historical/as-of use is exactly
  what a fresh recomputation from layers 1–2 can reconstruct — if the
  events themselves are not independently discoverable from durable
  facts, A retains none of that, and this must be stated as A's actual
  cost rather than assumed away.
- **B. Separately preserved origin and adjustment components.** Each tax
  determination (origin, each adjustment) is its own durable, canonical
  citizen at layer 3, independently addressable and cited. When a
  component needs to change, B keeps the currently-authoritative
  component set correctly reflecting that change — whether that means
  replacement, supersession, or re-derivation is a lifecycle question the
  eventual selected contract answers, not one this comparison
  presupposes (see the RC2-generalization discussion below, which
  documents that the codebase's own precedent is re-derivation, not
  in-place correction). Adjusted basis (layer 4) is always computed by
  summing/applying the live components at query time; no layer-4 number
  is itself stored.
- **C. Hybrid.** Layer 3 is durable exactly as in B. Layer 4 additionally
  publishes a current adjusted-basis projection as its own derived
  citizen for cheap consumption, alongside (never instead of) the
  durable components.

B and C are treated as **distinct rivals only if materializing and
publishing the current-value projection changes some named consumer,
currency, persistence, or explanation behavior** that the components
alone do not already provide — for example, a consumer needing basis at
high query volume without recomputation, or a currentness/re-derivation
requirement components alone cannot satisfy cheaply. If this milestone cannot
name such a behavior, record C as an implementation option within a
components model (B), not a manufactured third rival, and do not spend
further evidence discriminating B from C.

Discriminate A from B (and, only if warranted, from C) through product
behavior, not architectural taste: explanation ("why is basis $X"),
correction (does fixing one component require recomputing or re-deriving
the rest, and can A even locate "the rest"), historical/as-of calculation
(basis at a past date for a past return), overlap and double-count
prevention (RC5), allocation (RC6), rule succession (does a new
adjustment-rule version change past-computed adjustments), provenance
under partial coverage, and the unsupported case (RC7-style boundary).
RC2's existing two-rule, pairing-scoped shape (ADR-0071 Decision 2) is a
real exhibit, but only for what it actually demonstrates: two separate
rule artifacts each independently supersedable, each publishing its own
finding with exact upstream dependency pins, and correction displacement
that reaches both consequences through those shared pins (one-hop or
two-hop, per ADR-0071 Decision 6). It does **not** demonstrate durable
workspace persistence, current retrievability of a stored basis value, or
in-place correction of a layer-3 citizen — `packages/derivation/runner.py`'s
`append_publications` exists but has no production caller in this
codebase today, and ADR-0010 establishes that a derived finding is
*re-derived*, producing a new content-addressed finding, never corrected
in place.

**Plan-time hypothesis.** This plan anticipated that persistence,
retrievability, and correction behavior might be the properties that
discriminate the candidate representations, and that testing them could
be what forces the choice beyond paper.

**Final disposition.** They were not. Paper evidence found no named
consumer whose behavior distinguishes A from B: the differences that
survive scrutiny — per-authority attribution, displacement granularity,
and independent supersession — are real but not load-bearing for any
consumer that exists or was named, and persistence turned out to be a
shared, orthogonal gap rather than a discriminator between the shapes.
Under `PROJECT_PLANNING.md`'s Frontier Reduction and Direct-Build
Routing table, fourth row, the choice was therefore deferred at paper
with the missing discriminator recorded. Persistence, retrievability,
and re-derivation-versus-replacement become reopening questions when a
concrete consumer of a composed adjusted basis exists; they were not
established as this milestone's discriminators. The result is in
[`docs/domain-models/investment-basis-coverage.md`](../../../domain-models/investment-basis-coverage.md).

Apply PROJECT_PLANNING.md's paper-first and prototype economic gates
proposition-by-proposition (Gate 0's decision inventory below). Do not
build rivals merely for symmetry when paper evidence already distinguishes
the models for a given proposition. If a rival prototype is warranted for
a specific proposition, freeze the shared scenario and consumer test for
that proposition first.

## Decision inventory and routing (Gate 0/Gate 1)

Every major question below routes to exactly one of: domain mapping,
paper evidence, bounded prototype evidence, or deferral. Routing is a
plan-time judgment call, not a fixed score, and may be revised by the
foreman as evidence accumulates — but a route change is itself reported,
not silently taken.

| # | Question | Route | Why |
| --- | --- | --- | --- |
| Q1 | What are the six layers' boundaries for investment basis specifically? | Domain mapping | No code decision yet; this is comprehension work |
| Q2 | Do canonical propositions 1–8 hold across RC1–RC8 without a new foundational kind? | Paper evidence (Gate 2, per-proposition) | Cheapest rung; likely decidable from producer/authority/consumer/failure maps alone |
| Q3 | A vs. B vs. C for the adjusted-basis representation | Paper evidence first; prototype only if paper leaves the choice genuinely undiscriminated *and* a consumer forces it | **Planned** on the hypothesis that persistence, retrievability, or re-derivation behavior would discriminate the shapes. **Resolved** otherwise: paper found no named consumer whose behavior distinguishes A from B, so the choice was deferred and the missing discriminator recorded (a consumer that must read a composed adjusted basis). Persistence and retrievability proved a shared, orthogonal gap rather than a discriminator. No prototype was chartered |
| Q4 | Broker-basis reconciliation (RC5), framed outside-in: (a) what propositions must the application be able to state to know whether an institutional basis report already reflects a named adjustment; (b) who or what authors each proposition (broker, taxpayer, adopted rule); (c) what evidence and authority is available to support or contest each; (d) what behavior is required when inclusion, exclusion, or overlap is *unknown*; and (e) what corrections and consumers each proposition has | Domain mapping and paper evidence for (a)–(e) first, completing the full account; only once that account is complete does the milestone assess whether accepted association/report machinery (e.g. ADR-0068's shape) can carry any part of it | The product question is what the application must be able to say about reconciliation, not "new citizen or existing machinery" — that is an implementation question subordinate to (a)–(e), and ADR-0068 establishes an accountable *association* between an acquisition and a report, not that a report *establishes tax-adjustment inclusion*; those are different propositions and must not be conflated |
| Q5 | Lot/portion allocation (RC6) | Domain mapping plus paper propositions | No consumer yet exists that would behave differently; per the routing table's fourth row, stay at paper and name the missing discriminator |
| Q6 | Non-purchase origin (RC7) | Domain mapping only, explicitly bounded as a mapped boundary, not built | Owner directive: map neighboring cases only far enough to test the structure |
| Q7 | RC8 correction displacement: does a correction to an origin, adjustment, report, or association displace exactly its dependent adjusted-basis and consumer results? | Paper evidence: trace the dependency graph directly (origin → adjustment → report/association → projection → consumer) for each representative correction case | This is a direct tracing exercise against the selected representation (A/B/C), not a reuse of ADR-0072's reasoning — RC8 asks whether displacement is correct, which is a different question from Q8 below |
| Q8 | The same-obligation-entered-twice-style problem (two independent entries of what may be the same real obligation, with no correlating identifier) | Deferred, named as its own distinct identity/reconciliation boundary | ADR-0072 named a structurally similar residual risk and may inform this question, but ADR-0072's own text answers it only for the legacy/pairing accrued-interest migration case, not for basis generally — this milestone does not claim ADR-0072 resolves RC8 or this deferred boundary |
| Q9 | Whether a first production vertical (a specific RC) is buildable without reopening the concept | Deferred to the closing disposition; a real completion condition — see "First production vertical, or an explicit partial result" below | Depends on how Q2–Q8 resolve; premature to route now |

## Process boundary: four states, not two

The prior milestone's retrospective
(`docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md`,
"A process boundary the next milestone should draw earlier") found that
letting one integration experiment serve simultaneously as contract
revision, production implementation, and publication base was expensive:
curation had to reconstruct history rather than publish it. This
milestone is a deliberate cadence trial of the fix, kept local to this
milestone rather than edited into `PROJECT_PLANNING.md` itself:

1. **Seam or rival evidence** — any per-proposition paper instances or
   bounded prototypes built under the decision-inventory routing above.
2. **Disposable integration evidence** — if more than one proposition's
   prototype needs to be exercised together to test composition, that run
   is expected to be thrown away, contract revisions and all. It is never
   assumed reusable.
3. **Consolidated contracts** — the representation choice(s) and canonical
   propositions as corrected by whatever evidence was gathered, written
   down once, cleanly, before any code from step 1 or 2 is reused.
4. **A clean production build** — reserved for the first production
   vertical (Q9), which this milestone normally does not reach (see
   Stop conditions).

Prototype code is evidence and is disposable by default (Gate 7). If
integration evidence changes a proposed contract, that revision is
consolidated into step 3 before any adoption. No successor ADR corrects
another ADR authored within this same milestone; a provisional decision
is repaired or consolidated before it becomes this milestone's accepted
contract, per this plan's non-goals.

If evidence gathering discovers that integration is expected to revise
several propositions' contracts rather than merely confirm them, that is
itself a trigger to stop and recommend splitting the remaining work into
a following milestone rather than absorbing it here.

## Execution

One paper-evidence unit produces the domain model, the structural
coverage matrix over RC1–RC8, the canonical propositions with paper and
committed-machinery evidence kept separate, the representation
comparison, and a disposition for each question in the decision inventory
above. A further unit is chartered only if a question genuinely requires
evidence beyond paper; chartering one before paper evidence requires it
would violate the "if paper suffices, stop here" rule.

## Non-goals

- No universal property, partnership, business-asset, depreciation,
  estate, or gift-tax basis ontology.
- No Form 8949 vertical, general basis ledger, cross-year persistence, or
  broad production integration.
- No later-year basis-reuse implementation was performed here; that
  remained outside this milestone throughout. The roadmap's "Later-Year
  Basis Reuse Test" is a separate milestone, and the partial basis model
  this milestone produced is the result it was waiting on, so it is now
  unblocked. It is also the natural context in which the deferred
  adjusted-basis representation choice can be tested, since a later-year
  disposition is where a consumer of a composed adjusted basis first
  appears.
- No rival prototype built for symmetry once paper evidence discriminates
  a proposition.
- No repair of ADR-0072's named residual risks (representation-transfer
  adjudication, same-obligation-twice detection) — this milestone may cite
  ADR-0072 as informative precedent for Q8's deferred duplicate-entry
  boundary but does not resolve it, and does not claim ADR-0072 answers
  RC8's correction-displacement question (Q7).
- No production graphical interface, filing, or claim of professional
  authority.

## Deliverables

- `docs/domain-models/investment-basis.md`
- the structural coverage matrix against RC1–RC8, authored and
  evidence-cited (not a mechanical derivation)
- eight canonical propositions with paper evidence (positives, negatives,
  lifecycle trace, producer/authority/consumer/failure map)
- the A/B/C representation-comparison disposition, with the RC2
  generalization question answered
- routed dispositions for Q1–Q9
- any bounded prototype evidence shown to be actually required
- a consolidated contract specification (only if evidence converges enough
  to write one) or an explicit partial-ratification disposition (Gate 6)
  naming what remains open and its reopening trigger
- updated phase roadmap and phase state
- a retrospective evaluating the four-state cadence trial specifically:
  did keeping rival/seam evidence, disposable integration evidence,
  consolidated contracts, and a clean production build distinct actually
  reduce curation cost compared to the prior milestone

## Verification

- Every canonical proposition's positive/negative instances are checked
  against the real accepted contracts they touch (ADR-0068, ADR-0070,
  ADR-0071, ADR-0072) rather than an imagined shape.
- `python3 tools/governance_lint.py`
- `python3 tools/envelope_scan.py --range origin/main..HEAD`
- `git diff --check`
- If any prototype code is written, run its focused tests and the full
  suite for any change under `packages/kernel/` or `packages/derivation/`.
- Rely on the PR `verify` workflow as the gate of record once a PR exists.

## First production vertical, or an explicit partial result

Naming the first production vertical (Q9) is a real completion condition,
not an optional flourish. At closing disposition:

- if the consolidated contracts make a specific representative case (or a
  case close to one of RC1–RC8) buildable without reopening any of the
  canonical propositions or the A/B/C representation choice, name it
  exactly, and state what makes its contract already settled;
- if no such case exists — because a proposition remains genuinely
  undecided, or every candidate first vertical would force reopening a
  canonical proposition or the representation choice — the milestone
  closes only as an **explicit partial result**: state plainly which
  propositions or representation questions remain open, name the concrete
  trigger that would reopen them, and do not claim that the basis
  backbone is ready for tax-treatment breadth. A partial result is a
  legitimate, complete closing disposition under this plan; it is not a
  failure to be dressed up as a full one.

## Data safety

All committed examples use obvious `demo.*` or `demo-*` identities and
wholly synthetic amounts and circumstances. No personal document, tax
fact, prior return, private output, refusal reason, credential, or
absolute workstation path may enter the branch, domain model, fixture,
test, review, or handoff.

## Stop conditions

Stop for the owner when:

- two materially different representations (among A/B/C, or a fourth
  paper evidence surfaces) remain viable for the same proposition after
  the smallest useful discriminating evidence, and choosing one creates
  substantial migration or irreversible identity cost;
- composing more than one proposition's prototype
  reveals contract revisions across several propositions at once — per
  the process-boundary section, this is the trigger to split remaining
  work into a following milestone rather than absorb it here;
- official authority does not support a proposition or exposes a
  materially different fact pattern;
- an honest treatment requires personal or non-synthetic data;
- planning discovers a genuinely small direct build whose contract is
  already settled — report the value and displaced work plainly before
  admitting it, since the plan otherwise stops after consolidation; or
- the foreman cannot explain in plain language what additional work on a
  given proposition would change.

Do not stop merely because the domain model broadens, a representative
case turns out to need more paper evidence than expected, or the plan did
not predict a useful supporting artifact.

## Exit criteria

The milestone is complete when:

1. an ordinary reader can explain basis as a lifecycle (origin, event,
   adjustment, allocation, reconciliation, as-of projection) rather than
   one number;
2. the six layers (evidence, ordinary circumstance, tax determination,
   adjusted basis, calculation consumption, presentation) remain
   recoverably distinct throughout the domain model and coverage matrix;
3. representative increase (RC3), decrease (RC2, RC4a, RC4b), timing (RC2,
   RC4a, RC4b), reconciliation (RC5), allocation (RC6), correction (RC8),
   and consumer (proposition 7) cases have tested the model;
4. viable canonical shapes (A vs. B, and B vs. C only if a named consumer
   behavior warranted treating them as distinct rivals) have been
   discriminated at the cheapest sufficient evidence rung, with the
   RC2-generalization question explicitly answered;
5. coverage states (supported, structurally accommodated, unresolved,
   excluded) distinguish implementation from structural accommodation for
   every representative case, using the deliberately authored domain
   coverage matrix, not `untranslated_source_findings`;
6. the first production vertical is either named exactly with its
   settled contract, or the milestone closes as an explicit partial
   result naming what remains open and its reopening trigger — per
   "First production vertical, or an explicit partial result" above; a
   silent absence of either is not an acceptable close; and
7. remaining frontier questions (Q1–Q9, plus any the work surfaces) have
   concrete reopening triggers, and the retrospective states whether the
   four-state cadence reduced curation cost.
