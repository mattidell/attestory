<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "tax-concept-derivation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md",
  "milestone_state": "track-2",
  "status": "Tax Concept Derivation established 2026-08-27 from origin/main at 9159a13d. The opening milestone is a bounded executable exploration: one synthetic 2025 Form 1099-INT box-1 item, one accrued-interest-at-purchase contrast, and one end-to-end path from source report through ordinary circumstance and tax classification to tax concept and simulated return projection. It does not attempt full taxable-interest coverage, select a production representation, or reopen source-family closure and provisional-return design. The source-and-semantic boundary unit is complete: the treatment is grounded in Treas. Reg. 1.61-7(c) rather than the Schedule B reporting mechanic, the incumbent artifact graph is read against it, and six synthetic cases are instantiated in docs/milestones/reported-interest-tax-concept/. The executable-probe track is skipped because the paper evidence answers the necessity question; no candidate implementation has been exercised. A missing Treasury Regulation authority family in citation.v1 is recorded as a production condition and a candidate separate substrate milestone, not addressed here.",
  "current_role": "Independent reviewer — adversarial review of the source-and-semantic boundary findings",
  "current_prompt": "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md#Tracks"
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
- **Active milestone:** Reported Interest to Tax Concept Vertical Slice —
  **PLANNED**.
- **Base:** `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`, which includes the completed
  Taxable Interest Modeling milestone through PR #185.
- **Branch:** `milestone/tax-concept-derivation-phase-definition`.
- **Next move:** charter the source-and-semantic boundary unit. It verifies the
  selected accrued-interest treatment, fixes the synthetic cases, and stops at
  paper if the existing artifact graph already answers the primary
  representation question.
- **Decision posture:** the opening milestone produces executable evidence and
  bounded production-contract questions. It does not itself select a citizen,
  schema, ADR, full tax model, or production migration.

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
  similarity.

## Open and owner-held

- Whether a derived tax concept needs a new citizen or can be declared through
  existing artifacts remains open. The opening slice must make the choice
  concrete before the owner selects a production contract.
- The identity and lifecycle of item-level tax classifications are open,
  including the independent effects of source correction, circumstance
  correction, tax-rule succession, and reporting-artifact succession.
- The minimum durable shape of a concept-coverage profile is open.
- The question of subject on a joint return remains outside the opening slice.
- The first contrasting tax concept is not yet selected.
- `OV-1`, `SC-13`, and `SC-16` remain carried but unselected. This phase does
  not absorb them unless a later milestone explicitly selects them.

## Opening milestone

The active plan is
`docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md`.

Its selected cases hold one Form 1099-INT report constant while changing one
ordinary circumstance. The first work unit verifies the treatment and
instantiates the cases before any executable prototype. Full taxable-interest
coverage, production schemas, and return-engine migration are later milestones.

## Pointers

- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Active milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md`.
- **Starting modeling evidence:**
  `docs/milestones/taxable-interest-model-sufficiency/README.md`.
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
