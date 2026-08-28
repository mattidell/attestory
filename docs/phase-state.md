<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "tax-concept-derivation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md",
  "status": "Tax Concept Derivation remains active. Opening milestone Reported Interest to Tax Concept Vertical Slice closed 2026-08-28 from origin/main at 9159a13d. Bounded slice: one synthetic 2025 Form 1099-INT box-1 item, one accrued-interest-at-purchase contrast, a distinct box-3 TI-A1 coverage probe. Exhibit exhibits/reported-interest-tax-concept/it6. No representation is recommended on necessity grounds. Durable record: docs/milestones/reported-interest-tax-concept/. Prototype working set archived under docs/archive/2026-08-28-reported-interest-tax-concept/. Next milestone unselected. Named candidate, if chosen: Later-Year Basis Consequence Frontier.",
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
- **Just-closed milestone:** Reported Interest to Tax Concept Vertical Slice —
  **CLOSED 2026-08-28**. Exhibit
  `exhibits/reported-interest-tax-concept/it6`. Four packagings ran on the six
  cases. No representation is recommended on necessity grounds.
- **Base:** `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`, which includes the completed
  Taxable Interest Modeling milestone through PR #185.
- **Branch:** `milestone/tax-concept-derivation-phase-definition`.
- **Next move:** select the next milestone. None is selected. The named
  candidate is Later-Year Basis Consequence Frontier. Carried product
  question from the closed slice: the product consequence of a split state
  after a current partition explanation is unavailable (recompute, retain as
  historical, withhold, or a named later-year task for an independently
  current basis amount).
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

## Just-closed milestone

The just-closed plan is
`docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md`.
The retrospective is
`docs/milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md`.

Its selected cases hold one Form 1099-INT report constant while changing one
ordinary circumstance. The treatment was verified from official sources and the
cases instantiated before the prototype; the executed comparison is in
`docs/archive/2026-08-28-reported-interest-tax-concept/prototypes/reported-interest-tax-concept/examination.md`.
Full taxable-interest coverage, production schemas, and return-engine
migration remain later work. The next milestone is unselected.

## Pointers

- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Just-closed milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md`.
- **Retrospective:**
  `docs/milestone-retrospectives/2026-08-28-reported-interest-tax-concept.md`.
- **Starting modeling evidence:**
  `docs/milestones/taxable-interest-model-sufficiency/README.md`.
- **Executed prototype record:**
  `docs/archive/2026-08-28-reported-interest-tax-concept/` (charter and
  examination; code at tag `exhibits/reported-interest-tax-concept/it6`).
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
