<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "document-ordinary-fact-translation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md",
  "milestone_state": "seam-0",
  "status": "Document and Ordinary-Fact Translation Vertical restarted 2026-08-28 from origin/main at 0869f10a on milestone/document-ordinary-fact-translation-seams. The prior single-track attempt on milestone/document-ordinary-fact-translation built the full canonical slice in one pass and was returned NOT READY by independent adversarial review even after repair; that branch is retained as reference evidence, not as a base. This branch decomposes the same objective into six independently chartered seams (canonical value extraction, identity association, relationship constraints, standing authorization and currentness, rule-owned consequences, ordinary input mapping) plus one integration checkpoint, each seam run under the Prototype Economic Gates with a clean-room rival builder and a clean-room/adversarial/eligibility review committee where a rival is genuinely informative. No seam has been chartered yet.",
  "current_role": "Foreman — owner-directed milestone lead",
  "current_prompt": "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md"
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
- **Active milestone:** Document and Ordinary-Fact Translation Vertical —
  **seam-0, restarted**. No seam chartered yet.
- **Base:** `origin/main` at
  `0869f10a90403f9ed35e27d326ba46dc4da57bba`, including the merged owner
  model.
- **Branch:** `milestone/document-ordinary-fact-translation-seams`.
- **Reference-only branch:** `milestone/document-ordinary-fact-translation` —
  the prior single-track attempt. Its Track 0 domain-model draft and Track 2
  production translation are citable starting evidence for seam charters, but
  its independent adversarial rereview returned NOT READY; do not build on
  it or treat its choices as pre-selected.
- **Next move:** map or revise
  `docs/domain-models/taxable-interest-translation.md`, confirm T1–T9, then
  charter Seam 1 (canonical value extraction) under
  `docs/prototypes/canonical-value-extraction/plan.md` per the Prototype
  Economic Gates. Seam 4 (standing authorization) and Seam 6 (ordinary input
  mapping) may charter in parallel since neither depends on the
  interest-specific seams.
- **Just-closed milestone:** Reported Interest to Tax Concept Vertical Slice —
  **CLOSED 2026-08-28**. Exhibit
  `exhibits/reported-interest-tax-concept/it6`. Four packagings ran on the six
  cases. No representation is recommended on necessity grounds.
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

- None of the six seams are chartered or scored for prototype eligibility
  yet. Seam sequencing (1 -> 2 -> 3 -> 5 dependent; 4 and 6 parallel) is
  proposed in the plan, not yet executed.
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

## Active milestone

The active plan is
`docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`.
It decomposes the translation vertical into six independently chartered
seams plus one integration checkpoint, run under the Prototype Economic
Gates with rival builders and a clean-room/adversarial/eligibility review
committee wherever a rival comparison is genuinely informative.

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
migration remain later work.

## Pointers

- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Active milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`.
- **Reference-only prior attempt:** branch
  `milestone/document-ordinary-fact-translation` (NOT READY; not a base).
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
