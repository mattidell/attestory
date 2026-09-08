<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "nominee-allocation-assertion-recording",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md",
  "milestone_state": "closed",
  "status": "Nominee Allocation Assertion Recording is CLOSED 2026-09-08; owner-directed repairs 2026-09-08. Three tracks; Tracks 1 and 2 were each independently reviewed READY, and Track 0 was closed by the Foreman on executed evidence rather than by an independent reviewer. The application records, corrects, retracts from current use, and asserts again the ordinary statement that a stated amount of interest reported on an identified Form 1099-INT is allocated to a named other person, and recovers current and historical retracted assertions — what was said, who said it, and who later ended current support — with attribution from a committed act log alone. An allocation assertion requires current ordinary-language-entry evidence whose submitted answers correspond to the mapped finding; production does not invent a synthetic flag. The workspace model is SHARED: one current answer per report and recipient; any recorded actor may correct or retract it; actor is opaque provenance, never admission-validated; no durable text claims the original actor recanted. Hard gate: no user-facing production caller may rely on assert_nominee_allocation until resumable or idempotent recovery of a persisted multi-act prefix is closed. No nominee tax consequence, line-2b change, Schedule B row, information-reporting implementation, legacy migration, or UI. Deferred with triggers: author-bound recantation and permission rules, author-indexed propositions and conflict reconciliation, recipient display-name correction, the R-B source-independent association model, and A10's routing destination. T0-F5 remains deferred behind its hard production gate. The next milestone is unselected.",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md",
  "retrospective": "docs/milestone-retrospectives/2026-09-08-nominee-allocation-assertion-recording.md",
  "deep_reads": {
    "new_milestone": [
      "docs/milestone-retrospectives/2026-09-08-nominee-allocation-assertion-recording.md",
      "docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md",
      "docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md",
      "docs/adr/0073-assertion-standing-and-retraction-lifecycle.md",
      "OWNER_MODEL.md#The Product Model"
    ]
  }
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
- **No active milestone.** The next milestone is **unselected**; selection is
  owner-held and the phase roadmap is the selection instrument.
- **Just-closed milestone:** Nominee Allocation Assertion Recording — **CLOSED
  2026-09-08**, with owner-directed repairs the same day. Three tracks; Tracks 1 and 2 were each independently
  reviewed READY, and Track 0 was closed by the Foreman on executed evidence
  rather than by an independent reviewer. The
  application records, corrects, retracts from current use, and asserts again
  the ordinary statement that a stated amount of interest reported on an
  identified Form 1099-INT is allocated to a named other person, and recovers
  current and historical retracted assertions — what was said, who said it,
  and who later ended current support — with attribution from a committed act
  log alone. **Hard gate:** no user-facing production caller may rely on
  `assert_nominee_allocation` until resumable or idempotent recovery of a
  persisted multi-act prefix is closed. Delivered:
  `tax.us.nominee-allocation.amount` keyed `payer` + `statement` + `tax-year` +
  `recipient`, sharing the committed box-1 report's identity components; the
  `tax.us.interest-allocation-recipient` entity kind with an application-minted
  opaque workspace id; a persisting producer; a separate bounded retraction
  operation; and a recovery view consulting `compute_currency` as the sole
  definition of current standing. An allocation assertion requires current
  ordinary-language-entry evidence whose submitted answers correspond to the
  mapped finding; production does not invent a synthetic flag. **The workspace model is shared:** one current
  answer per report and recipient, any recorded actor may correct or retract it,
  actor is opaque provenance and never admission-validated, and no durable text
  claims the original actor recanted. No nominee tax consequence, line-2b
  change, Schedule B row, information-reporting implementation, migration, or
  UI. **T0-F5 remains deferred** behind its hard production gate. See
  `docs/milestone-retrospectives/2026-09-08-nominee-allocation-assertion-recording.md`.
  **Closure is complete**: the plan, retrospective, roadmap, and this document
  are final, and nothing about this milestone is outstanding. Selecting the
  next milestone is the only remaining action.
- **Prior milestone:** Assertion Standing and Retraction Semantics — **CLOSED
  2026-09-07.** A recorded actor can end the workspace's current
  support for one identified answer without supplying a replacement value, and
  every reader agrees about which answer currently stands. A dedicated act
  contributes a fifth named displacement root behind six admission refusals;
  the two declared cascade edges are unchanged. One resolution of current
  standing replaced two across the kernel admission enforcers, both read
  models, the derivation layer, the migration path, and both tax-layer
  readers, closing a production check that accepted a Social Security
  statement whose filing-status authority had been withdrawn. Entity
  succession and source-family withdrawal were disqualified on executed
  evidence. An admitted retraction means a recorded actor ended current
  support; it never establishes that the original author withdrew, and
  whether it should require the original author is open and owner-held.
  Fifteen fact types remain un-withdrawable because the engine's capability
  limits are written as admission checks; relocating them is a successor
  milestone by owner disposition, not a property of withdrawal. Ratified by
  ADR-0073. See
  `docs/milestone-retrospectives/2026-09-06-assertion-standing-retraction-semantics.md`.
- **Prior milestone:** Nominee Interest Ownership Translation — **CLOSED
  2026-09-05.** Track 0 completed at the **paper** evidence rung across three
  reviewed checkpoints and returned a **decision-ready contract proposal**; no
  production code, schema, ADR, or test changed. The accrued-interest
  translation method **transfers** to an ownership-allocation circumstance:
  supportability transfers unchanged (ADR-0070 Decisions 8–10); report
  association, rule-owned consequences, ordinary-input mapping, and legacy
  coexistence are bounded extensions; owner cardinality is a new decision. The
  contract, production, and integration units remain **conditional and
  unchartered**. The three information-reporting formulations remain
  unreconciled by design. **T0-F5 is deferred behind a hard production gate**:
  no production or integration unit may be accepted as complete for a state
  combining required Schedule B presentation with a nonzero pairing-scoped
  current-year adjustment until it is repaired. See
  `docs/milestone-retrospectives/2026-09-05-nominee-interest-ownership-translation.md`.
- **Prior milestone:** Later-Year Basis Reuse Test — **CLOSED
  2026-09-03 as an explicit partial result.** Neither strategy supplies
  a production-authorized later-year delivery path today (raw same-run
  mixed-scope computation does produce the value), a fifth composition
  gap (the absence of an authorized package/scope contract for composing
  an earlier determination into a later disposition calculation) joins
  the four inherited ones, and the A/B representation choice is deferred
  again because no material product discriminator was established. See
  "Closed milestone" below.
- **Prior milestone:** Investment Basis Concept and Coverage Model —
  **CLOSED 2026-09-02 as an explicit partial result.** The basis concept
  and its coverage are established; the adjusted-basis representation
  choice was deferred for want of a consumer that behaves differently
  under either shape — Later-Year Basis Reuse Test supplied that consumer.
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
- **Later-year basis reuse** (roadmap item 4) closed as an explicit
  partial result — see "Closed milestone" below. Of its three open
  questions, two were answered and one was not: a later-scoped run
  **cannot** reach an earlier determination through any committed
  production-authorized path without an authorized package/scope
  contract, same-investment identity **is** establishable for the
  consequence (via the association's fact ids) but **not** at the cost
  origin, and the consumer shows **structural** differences between
  representations on run observables (pin topology, blocked-row naming)
  with no material product discriminator established. The owner-held
  residue is a set of separate decision areas, each applying only where a
  selected case reaches it: (1) the contract permitting
  cross-scope consumption (gap 5); (2) the later calculation's
  consumption policy and the distinct historical-retention question;
  (3) authorship of the broker-versus-derived comparison claim; (4)
  whether to repair the collect-target universe guard below.
- **The collect-target universe guard** in
  `packages/derivation/package_validation.py` is an owner decision
  independent of this phase's milestone sequence: its allowlist ends at
  `artifact-package.v17` while production is `artifact-package.v26`, so the
  `COLLECT_TARGET_NOT_FAMILY` check has never bound a `rule-artifact.v7`
  collect. Any future claim that a source-family-authorized traversal has
  been established must be re-run against a repaired guard.
- **The adjusted-basis representation choice** and the four gaps blocking
  a first basis-lifecycle production vertical: see "Closed milestone"
  below and `docs/domain-models/investment-basis-coverage.md` for the
  full statement and reopening triggers.

## Closed milestone

Plan:
`docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md`.
Findings:
`docs/prototypes/later-year-basis-reuse/track-0-findings.md`.
Retrospective:
`docs/milestone-retrospectives/2026-09-03-later-year-basis-reuse.md`.

**What is established.** Track 0 supplied the concrete later-year
disposition consumer the prior milestone lacked, and used it to test the
deferred adjusted-basis representation choice for real. Two access
*experiments* were exercised on one real, persisted-boundary experiment;
they are not rival product architectures the owner must pick between.
**AS-1 (retrieval)** is blocked twice independently — the real
`derived-finding.v2` basis consequence cannot enter the act log at all
(`act-derived-publication.v1`'s schema is fixed to `derived-finding.v1`
and is published and immutable, AGENTS.md Article 9 / ADR-0003), and even
a schema-compatible finding that does persist is never surfaced to a later
run (`packages.kernel.findings.apply_act` excludes `derived-publication`
from `KERNEL_ACT_KINDS` unconditionally). **AS-2 (re-execution)**
re-executes the 2025 seam from real projected source facts with no new
schema or kernel machinery for that seam, reproduces the consequence,
passes its later-reporting-year negative control, and absorbs a correction
with no retrieval or injection — but end-to-end later-year use remains
unbuilt, and delivery under an authorized package/scope contract is not
established: a same-run, mixed-scope composition proves the rule
vocabulary can compose across a report-filter year and a declared rule
scope with no injection **and does produce the value**, and proves nothing
about authorization, since nothing in the evaluated path compares them;
with the report filter itself set to the later year (one tested
configuration), no consumer form receives the value without injection.
Re-deriving for consumption does not, by itself, prevent retaining
historical executions for reporting; those remain separate open questions.

**A fifth composition gap, this milestone's own finding.** The absence of
an authorized package/scope contract for composing the 2025 determination
into a later disposition calculation: no adopted 2029 package exists, no
cross-scope composition contract exists in committed content, and
`package_validation.py` independently refuses scope-mismatched package
members (`SCOPE_MISMATCH`). This joins the four gaps inherited from the
prior milestone; all five are must-close and none is closed.

**What is deferred, and why — on a cleaner ground than before.** The A/B
representation choice is deferred again. Structural differences between
representations were observed and executed (direct-versus-transitive pin
topology, direct-versus-indirect blocked-row naming), but no test
exercised `explanation.py`'s `walk_npe` or any other downstream consumer
of either shape, so no material product discriminator is established. The
prior milestone's null (no consumer behaves differently) is not what
survives here; this milestone's null is narrower — no material
discriminator, though structural ones exist.

**A validator/authority gap in committed product code, found as a
byproduct and deliberately not fixed.**
`packages/derivation/package_validation.py`'s `COLLECT_TARGET_NOT_FAMILY`
guard documents itself as binding "artifact-package.v3 onward" but its
allowlist ends at `artifact-package.v17`, while the production package is
`artifact-package.v26`; the guard has never bound a `rule-artifact.v7`
collect. Outside this milestone's boundary (no changes under `packages/`);
escalated to the owner.

**Owner-held decision areas surfaced, none taken here.** Each applies only
where a selected case reaches it. (1) The contract
permitting cross-scope consumption (gap 5). (2) The later calculation's
consumption policy — historical execution, a newly derived determination,
or a policy permitting either — and the distinct question of whether
historical executions should independently be retained and reportable.
(3) Authorship of the broker-versus-derived comparison claim. (4) Whether
to repair the collect-target universe guard. The milestone did not
establish whether resolving gap 5 or the other composition gaps requires
schema, kernel, package, content, or other changes.

**The prior milestone,** Investment Basis Concept and Coverage Model
(closed 2026-09-02), established the basis domain model and coverage this
one tested with a real consumer; its own retrospective is
`docs/milestone-retrospectives/2026-09-02-investment-basis-concept-coverage.md`.

## Pointers

- **Next-milestone selection instrument (owner-held):**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Just-closed milestone:**
  `docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md`,
  retrospective
  `docs/milestone-retrospectives/2026-09-08-nominee-allocation-assertion-recording.md`.
- **Lifecycle contract it consumes:**
  `docs/adr/0073-assertion-standing-and-retraction-lifecycle.md`,
  plan
  `docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md`,
  retrospective
  `docs/milestone-retrospectives/2026-09-06-assertion-standing-retraction-semantics.md`.
- **Prior milestone:**
  `docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md`,
  retrospective
  `docs/milestone-retrospectives/2026-09-05-nominee-interest-ownership-translation.md`.
- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Closed milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md`.
- **Findings:**
  `docs/prototypes/later-year-basis-reuse/track-0-findings.md`.
- **Retrospective:**
  `docs/milestone-retrospectives/2026-09-03-later-year-basis-reuse.md`.
- **Accepted ADRs:** `docs/adr/0067` through `docs/adr/0072`, digested in
  `docs/adr/INDEX.md`.
- **Prior milestone:**
  `docs/phases/tax-concept-derivation/milestones/investment-basis-concept-coverage.md`,
  retrospective
  `docs/milestone-retrospectives/2026-09-02-investment-basis-concept-coverage.md`.
  Durable result: `docs/domain-models/investment-basis.md` and
  `docs/domain-models/investment-basis-coverage.md`.
- **Earlier prior milestone:**
  `docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`,
  retrospective
  `docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md`.
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
