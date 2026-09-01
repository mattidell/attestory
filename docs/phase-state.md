<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "document-ordinary-fact-translation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md",
  "status": "Document and Ordinary-Fact Translation Vertical CLOSED 2026-08-30. Six ADRs accepted (0067-0072), establishing the first source-independent workspace translation: a documentary Form 1099-INT box-1 finding and an ordinary bond-acquisition circumstance associate through an explicit, accountable confirmation (never an inferred match); a supported pairing dispatches to rule-owned current-year and basis consequences; aggregate supportability catches a shared-report over-claim; standing authorization gates run currentness independent of per-family closure; the incumbent legacy accrued-interest surface coexists with, and can migrate to, the pairing path without ever silently discarding a live claim. package.core-calculations.v34 admits the full seam capability alongside the still-live legacy surface (coexistence); v35 is additive, admitting the migrated single-subtractand successor reached only through a real migration-adoption act. Merged into main. No milestone is currently active; the next one is unselected.",
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
- **Just-closed milestone:** Document and Ordinary-Fact Translation Vertical —
  **CLOSED 2026-08-30.** Six ADRs accepted (0067–0072). See "Closed
  milestone" below for the full design summary.
- **Branch:** `milestone/document-ordinary-fact-translation-seams`, merged
  into `main`.
- **No milestone is currently active; the next one is unselected.**
- **TI-A1.** Prototype refuses coverage. The incumbent cannot determine whether
  § 135 applies and may publish full inclusion. The fixture does not prove the
  published number wrong.
- **Authority.** Pub. 550 *Bonds Sold Between Interest Dates* against
  IRC § 61(a)(4), not Treas. Reg. § 1.61-7(c).
- **Decision posture:** ADR-0067 through ADR-0072 are accepted and stand as
  written; none is superseded by another decision in this set.

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
- **Later-year basis reuse** (the roadmap's next candidate): consume this
  slice's item-level basis consequence in a later disposition, exercising
  cross-year identity and correction, to determine whether the canonical
  model transfers beyond the current-year line-2b calculation.

## Closed milestone

The plan lived at
`docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`;
the retrospective is
`docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md`.

Six ADRs, decomposed by architectural seam:

1. **Direct field-ref extraction (ADR-0067).** A rule reads one named field
   of a canonical object-valued fact directly, without a redundant per-field
   scalar collectible.
2. **Two-tiered obligation identity association (ADR-0068).**
   Entity-kind payer/obligation/statement identity (exact string
   canonicalization, arbitrary cardinality, not real-world entity
   resolution). Association locates a candidate report by a named
   statement/account reference or a coarse payer+year join, but a single
   candidate is never associated on the match alone: `confirmed_report_match`
   is a mandatory, explicit, accountable assertion scoped to the specific
   report named, and a stale confirmation refuses rather than retargeting
   when the sole candidate's identity changes.
3. **Accrued-amount supportability, per-pairing and aggregate (ADR-0070).** A pairing's claimed amount is bounded by its report's own
   amount; a separate aggregate check catches a shared report whose several
   attested pairings jointly exceed it, retracting the group's findings and
   blocking the current-year subtotal rather than presenting a
   differently-scoped total as settled.
4. **Standing workspace authorization (ADR-0069).** An out-of-kernel act-log
   fold, decoupled from per-family closure; absence resolves to an explicit
   non-current status; the re-authorization boundary can never fall below
   what a run actually executes; resolved status is persisted to the durable
   run output and presentation root.
5. **Rule-owned pairing-scoped consequences (ADR-0071).** A supported
   pairing's current-year and basis consequences are declared, checksum-
   published rules whose own value expression genuinely controls execution,
   with truthful dependency pins matching ordinary-rule fidelity.
6. **Legacy/pairing coexistence and migration (ADR-0072).** The incumbent
   accrued-interest surface is retired for new obligations; migration never
   silently discards a live, nonzero legacy claim; only a genuine
   same-identity zero correction resolves one.
7. **Fluid domain model and structural unsupported-coverage disclosure.** A
   non-contractual domain model maps the wider translation frontier; a
   coverage read model names an adopted-but-unconsumed fact type from exact
   semantic reference fields, never incidental metadata.
8. **Integration.** The seams compose through the real production package
   resolver, live coordinator, and presentation projection, proven through
   `live_coordinate_run` rather than hand-built contexts.

## Pointers

- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Closed milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`.
- **Retrospective:**
  `docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md`.
- **Accepted ADRs:** `docs/adr/0067` through `docs/adr/0072`, digested in
  `docs/adr/INDEX.md`.
- **Prior just-closed milestone:**
  `docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md`,
  retrospective
  `docs/milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md`.
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
