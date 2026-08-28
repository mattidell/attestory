<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "tax-concept-derivation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md",
  "milestone_state": "track-3",
  "status": "Tax Concept Derivation established 2026-08-27 from origin/main at 9159a13d. Opening milestone: one synthetic 2025 Form 1099-INT box-1 item, one accrued-interest-at-purchase contrast, a distinct box-3 TI-A1 coverage probe. Current exhibit exhibits/reported-interest-tax-concept/it5 (it1-it4 unchanged historical exhibits). Four packagings ran through the real evaluator. Source-report is independent of tax-slice coverage. Copied C fields and E targets validate producing rule identity; a displaced producing evaluation cannot support a current partition explanation. Later-year grants are in-memory objects (artifact-object-only, currentness, object-store access, full-workspace); serialization was not executed. Task 6 is fact_version_current of used dependencies, not general usability. RECOMMENDATION: none on necessity grounds. Owner decision: product consequence of split state after a current partition explanation is unavailable. TI-A1: treatment refuses; source report of 840 remains. Treatment: Pub. 550 Bonds Sold Between Interest Dates against IRC 61(a)(4). Prototype code is not on the milestone branch. Durable record: docs/milestones/reported-interest-tax-concept/ and docs/prototypes/reported-interest-tax-concept/.",
  "current_role": "Milestone lead — current evidence reconciled on it5; awaiting fresh whole-candidate independent review",
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
  **IN CLOSEOUT, NOT CLOSED**. Current exhibit
  `exhibits/reported-interest-tax-concept/it5`. Four packagings ran on the six
  cases. No representation is recommended on necessity grounds.
- **Base:** `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`, which includes the completed
  Taxable Interest Modeling milestone through PR #185.
- **Branch:** `milestone/tax-concept-derivation-phase-definition`.
- **Next move:** a fresh whole-candidate independent review, then the owner
  decision. Remaining owner question: the product consequence of a split
  state after a current partition explanation is unavailable (recompute,
  retain as historical, withhold, or a named later-year task for an
  independently current basis amount).
- **TI-A1.** Prototype refuses coverage. The incumbent cannot determine whether
  § 135 applies and may publish full inclusion. The fixture does not prove the
  published number wrong.
- **Authority.** Pub. 550 *Bonds Sold Between Interest Dates* against
  IRC § 61(a)(4), not Treas. Reg. § 1.61-7(c).
- **Decision posture:** executable evidence and bounded production-contract
  questions. No citizen, schema, ADR, or production migration is selected.

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

- Whether a derived tax concept needs a new citizen is **not established**.
  A copied or referenced partition cannot support a current explanation after
  a producing evaluation is displaced. Remaining product questions concern
  what to do in that split state.
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
ordinary circumstance. The treatment was verified from official sources and the
cases instantiated before the prototype; the executed comparison is in
`docs/prototypes/reported-interest-tax-concept/examination.md`. Full
taxable-interest coverage, production schemas, and return-engine migration are
later milestones.

## Pointers

- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Active milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md`.
- **Starting modeling evidence:**
  `docs/milestones/taxable-interest-model-sufficiency/README.md`.
- **Executed prototype record:**
  `docs/prototypes/reported-interest-tax-concept/examination.md` (charter
  alongside it; code at tag `exhibits/reported-interest-tax-concept/it5`).
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
