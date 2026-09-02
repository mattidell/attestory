<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "investment-basis-concept-coverage",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md",
  "milestone_state": "closed",
  "status": "Investment Basis Concept and Coverage Model CLOSED 2026-09-02 as an explicit partial result. The basis concept, its representative cases (RC1-RC8), canonical propositions, and coverage verdicts are established in docs/domain-models/investment-basis.md and docs/domain-models/investment-basis-coverage.md. The adjusted-basis representation choice (durable components vs. a single published aggregate) is deferred at paper because no concrete consumer behaves differently under either shape; the missing discriminator is a consumer that must read a composed adjusted basis. A first basis-lifecycle production vertical cannot yet be specified: no purchase_price/acquisition_costs vocabulary, no basis-origin producer keyed by the acquisition identity, no content-declared per-acquisition publication path, and no declared traversal from an acquisition-keyed origin through the association record to the sibling accrued-interest consequence. Open questions and their reopening triggers are recorded in the coverage document. No milestone is currently active; the next one is unselected.",
  "current_role": "Foreman — between-milestones selection",
  "current_prompt": "docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md"
}
-->

# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Briefing

**Tax Concept Derivation opened on 2026-08-27.** The phase restores a path to
return-engine development by addressing the semantic gap between what source
documents report and what tax law makes of the taxpayer's facts.

The product should preserve evidence and reported facts, ask the user only for
ordinary facts about their circumstances, use adopted tax rules to classify
those facts, derive tax-concept results, and then project those results onto a
simulated return. Citations and explanations make that method inspectable; they
do not manufacture professional or institutional authority.

The phase begins with one deliberately small taxable-interest slice. It is not
a project to enumerate or implement the entire taxable-interest universe.

## Where the phase stands

- **Phase:** Tax Concept Derivation — **ACTIVE**.
- **Just-closed milestone:** Investment Basis Concept and Coverage Model —
  **CLOSED 2026-09-02 as an explicit partial result.** The basis concept
  and its coverage are established; the adjusted-basis representation
  choice is deferred for want of a consumer that behaves differently
  under either shape. See "Closed milestone" below.
- **No milestone is currently active; the next one is unselected.**
- **Prior milestone:** Document and Ordinary-Fact Translation Vertical —
  **CLOSED 2026-08-30.** Six ADRs accepted (0067–0072).
- **TI-A1.** Prototype refuses coverage. The incumbent cannot determine whether
  § 135 applies and may publish full inclusion. The fixture does not prove the
  published number wrong.
- **Authority (accrued interest paid to a bond seller, distinct from the
  TI-A1 §135 probe above).** The controlling support is **Treas. Reg.
  § 1.61-7(c)**, whose text reaches this buyer-side situation: its
  operative wording covers interest "in arrears but... accrued at the
  time of purchase," stating that such amounts are "not income" to the
  buyer when later received and are instead "returns of capital which
  reduce the remaining cost basis." This is
  corroborated by IRC § 61(a)(4) (the general inclusion rule § 1.61-7(c)
  displaces for the buyer), Pub. 550's "Bonds Sold Between Interest
  Dates" (the IRS's plain-language restatement), and the *seller-side*
  Treas. Reg. § 1.61-7(d), which requires the seller (not the buyer) to
  report that same accrued-interest component as income — a different
  paragraph governing a different party's obligation on the same
  transaction, not the buyer-side basis authority itself. An earlier
  closed milestone's archival analysis
  (`docs/milestones/reported-interest-tax-concept/accrued-interest-item-model.md`,
  unedited, historical record) read § 1.61-7(c) as limited to the
  "bonds traded flat" default-bond pattern and concluded no regulation
  reached the ordinary between-interest-dates buyer; the active
  milestone's own direct reading of the regulation's text found that
  conclusion too narrow, since (c)'s own wording reaches interest that
  has merely "accrued but not been paid," not only defaulted interest. This is recorded here as the active milestone's
  corrected account; it does not edit the closed milestone's own
  archival document or ADR-0071's committed citation pin, neither of
  which this milestone reopens.
- **Decision posture:** ADR-0067 through ADR-0072 are accepted and stand as
  written; none is superseded by another decision in this set. The active
  milestone treats ADR-0071's basis consequence as a required tax case
  (accrued interest received is a return of capital reducing basis) with a
  partial implementation exhibit — the committed rule derives and
  provenances the amount but does not yet encode property/lot identity,
  direction, effective event, purpose, or a consumer — not as a settled,
  complete instance of the general basis concept.

## Standing constraints and postures

- **Separate models.** Evidence, reported facts, ordinary circumstance facts,
  tax classification, tax concepts, reporting projection, execution coverage,
  and explanation connect but do not become one model because one amount moves
  through them.
- **User/product division.** The user supplies facts about their records and
  circumstances. Adopted rules supply tax classifications. The user is never
  asked to certify the product's tax-model coverage.
- **Workspace convention.** The previously selected convention for treating
  workspace inputs as the operative universe stands. This phase does not
  reopen per-family closure, provisional-run, action-scoped confirmation, or
  scenario design.
- **Partial coverage.** Partial tax coverage is expected. It must be described
  separately from the concept's meaning and must not silently redefine that
  meaning to match what is implemented.
- **Authority posture.** Sources support propositions in the model. The product
  aims to help the user reach and inspect a tax result, not to inherit the
  authority of a tax professional or turn defensibility into an end of its own.
- **Artifact-reading safeguard.** Every load-bearing claim about committed
  behavior names the artifact, fields actually read, relevant sibling fields,
  and consumers. A citation to part of an artifact is not proof that the whole
  behavior was examined.
- **Prototype boundary.** Prototype shapes are evidence. They do not become
  production citizens, schemas, or accepted contracts through effort or
  similarity — except where an ADR explicitly promotes a proven mechanism to
  production, as this milestone's six ADRs each did.

## Open and owner-held

- Whether a derived tax concept needs a new citizen beyond the six ADRs'
  fact/finding shapes is **not established** for domains outside
  accrued-interest-at-purchase.
- The identity and lifecycle of item-level tax classifications for a
  *different* tax concept (not this milestone's) are open.
- The minimum durable shape of a concept-coverage profile is open.
- The question of subject on a joint return remains outside the closed slice.
- The first contrasting tax concept is not yet selected.
- `OV-1`, `SC-13`, and `SC-16` remain carried but unselected. This phase does
  not absorb them unless a later milestone explicitly selects them.
- **ADR-0072's named residual risk:** the same obligation entered twice with a
  mismatched amount is not detected by the amount-equality collision signal —
  carried forward for a future milestone that gives the ordinary-language
  mapper a finer correlating identifier, if ever selected.
- **ADR-0072's smallest owner decision:** no nonzero legacy accrued-interest
  claim can currently complete migration while its computational role has
  been taken over by a new pairing; only a genuine same-identity zero
  correction resolves a nonzero claim. Whether to build an explicit,
  accountable representation-transfer adjudication act (in the same spirit as
  ADR-0068's `confirmed_report_match`) that would let a genuinely
  re-established obligation migrate honestly is a real product decision, not
  made here — the alternative is accepting that such a claim simply stays on
  the legacy path (correct on its own terms) until the owner decides
  otherwise.
- **Later-year basis reuse** (roadmap item 4, unblocked): consume the
  item-level basis consequence in a later disposition, exercising
  cross-year identity and correction. It is also the context in which a
  consumer of a composed adjusted basis first appears, and therefore
  where the deferred adjusted-basis representation choice can be tested.
- **The adjusted-basis representation choice** and the four gaps blocking
  a first basis-lifecycle production vertical: see "Closed milestone"
  below and `docs/domain-models/investment-basis-coverage.md` for the
  full statement and reopening triggers.

## Closed milestone

Plan:
`docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md`.
Retrospective:
`docs/milestone-retrospectives/2026-09-02-investment-basis-concept-coverage.md`.

**What is established.** A plain-language model of US-federal individual
investment-property basis as a lifecycle — origin, adjusting events,
allocation, reconciliation, and an as-of projection — keeping evidence,
ordinary circumstance, tax determination, adjusted basis, calculation
consumption, and presentation as six distinct layers
(`docs/domain-models/investment-basis.md`). Against that model: a
structural coverage matrix over eight representative cases, eight
canonical propositions with paper and committed-machinery evidence kept
separate, a comparison of three adjusted-basis representations, and the
open questions with their reopening triggers
(`docs/domain-models/investment-basis-coverage.md`).

**What is deferred, and why.** The representation choice between durable
components and a single published aggregate is undecided. Real
differences exist — per-authority attribution, displacement granularity,
independent supersession — but none is load-bearing for any consumer that
exists or has been named, so the Frontier Reduction routing table's
fourth row applies: stay at paper, record the missing discriminator,
defer. The missing discriminator is a consumer that must read a composed
adjusted basis.

**What blocks a first production vertical.** Four gaps: no
`purchase_price`/`acquisition_costs` vocabulary; no basis-origin producer
keyed by the acquisition identity; no content-declared per-acquisition
publication path; and no declared traversal from an acquisition-keyed
origin, through the association record that holds the acquisition-to-report
mapping, to the sibling accrued-interest consequence (which is keyed by a
derived pairing finding id, not by the acquisition key). None is shown to
require a new evaluator primitive or architectural kind; none is shown
solvable with committed machinery.

**The prior milestone,** Document and Ordinary-Fact Translation Vertical
(closed 2026-08-30), established the six accepted ADRs 0067–0072 this one
builds on; its own retrospective is
`docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md`.

## Pointers

- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Closed milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md`.
- **Retrospective:**
  `docs/milestone-retrospectives/2026-09-02-investment-basis-concept-coverage.md`.
- **Durable result:** `docs/domain-models/investment-basis.md` and
  `docs/domain-models/investment-basis-coverage.md`.
- **Accepted ADRs:** `docs/adr/0067` through `docs/adr/0072`, digested in
  `docs/adr/INDEX.md`.
- **Prior milestone:**
  `docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`,
  retrospective
  `docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md`.
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
