<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "tax-concept-derivation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md",
  "milestone_state": "track-3",
  "status": "Tax Concept Derivation established 2026-08-27 from origin/main at 9159a13d. The opening milestone is a bounded exploration turned completed executable vertical slice whose deciding evidence was repaired: one synthetic 2025 Form 1099-INT box-1 item, one accrued-interest-at-purchase contrast, a distinct box-3 TI-A1 fixture, and the path from source report through ordinary circumstance and tax classification to tax concept and simulated return projection. It does not attempt full taxable-interest coverage, select a production representation, or reopen source-family closure and provisional-return design. OUTCOME. Three rival shapes ran on all six cases through the real engine evaluator under one shared execution and currentness policy, on exhibit exhibits/reported-interest-tax-concept/it2 (it1 retained unchanged as historical prototype evidence): distributed (A), distributed with a partition edge (A+), and explicit item-level determination (B). Arithmetic does not discriminate. Partial refresh is deleted as deciding evidence. The hard-coded cross-year verdict is deleted. RECOMMENDATION: none on necessity grounds. A later-year consumer performing six concrete recovery tasks fails one task under shape A only when the later year holds the carried artifact alone; A+ and B both pass. That does not establish that a new citizen kind is necessary. SMALLEST REMAINING OWNER DECISION: when a later year needs the basis consequence, does it hold only the carried artifact, or may it re-open the source year? WITHDRAWN AND MUST NOT BE RE-ASSERTED. (1) That the incumbent produces the correct number in all six cases: it is silently wrong on TI-A1; box 3 flows unreduced into selected line-2b v4, and no committed rule computes the section 135 exclusion. The package does contain Form 8815 content as tax.us.2025.ss-benefits-scope.no-form-8815, consumed by the Social Security Benefits Worksheet, not by line 2b. (2) That a tax-year {yes, no} fact plus a line-2b guard passes the cases: never built or executed, and it does not follow. (3) That two dynamic probes on it1 decide the representation, or that the explicit determination is recommended on that evidence. (4) That the prototype was never built, that Track 1 never ran, or that paper plus the incumbent answered the representation question. Do not describe the necessity hypothesis as defeated on the earlier unexecuted counterexample, and do not describe it as supported by it1's probes. A PAPER CLAIM OVERTURNED BY EXECUTION: conditional_dependency_set was recorded as unable to make an amount conditional on a yes because its members must be ref expressions. True, but it does not bite here; executed on TI-N1 the evaluator blocked with DEPENDENCY_ABSENT and named the missing fact. The treatment is grounded in IRS Publication 550 'Bonds Sold Between Interest Dates' against IRC 61(a)(4), NOT in Treas. Reg. 1.61-7(c). Prototype code is not on the milestone branch; the durable record is docs/prototypes/reported-interest-tax-concept/charter.md and examination.md.",
  "current_role": "Milestone lead — repaired executable evidence and durable documents reconciled; awaiting fresh whole-candidate independent review",
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
  **IN CLOSEOUT, NOT CLOSED**. A completed executable vertical slice whose
  deciding evidence was repaired: the six cases ran end to end under three
  rival representation shapes through the engine's real expression evaluator,
  on exhibit `exhibits/reported-interest-tax-concept/it2`. The durable
  documents report that comparison. No representation is recommended on
  necessity grounds.
- **Base:** `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`, which includes the completed
  Taxable Interest Modeling milestone through PR #185.
- **Branch:** `milestone/tax-concept-derivation-phase-definition`.
- **Next move:** a fresh whole-candidate independent review, then the owner
  decision. The remaining owner-held product requirement is: when a later year
  needs the basis consequence, does it hold only the carried artifact, or may
  it re-open the source year?
- **Withdrawn — do not re-assert.** That the incumbent produces the correct
  number in all six cases: it is **silently wrong on TI-A1**. Box 3 flows
  unreduced into selected line-2b v4; no committed rule computes the § 135
  exclusion. Form 8815 content exists as
  `tax.us.2025.ss-benefits-scope.no-form-8815`, consumed by the Social Security
  Benefits Worksheet, not by line 2b. That a tax-year `{yes, no}` fact plus a
  line-2b guard passes the cases: never built or executed, and it does not
  follow from the cases. That two dynamic probes on it1 decide the
  representation, or that the explicit determination is recommended on that
  evidence. That the prototype was never built, that Track 1 never ran, or
  that paper plus the incumbent answered the representation question. Do not
  describe the necessity hypothesis as defeated on the earlier unexecuted
  counterexample, and do not describe it as supported by it1's probes.
- **Recanted authority — do not re-assert.** The treatment is Pub. 550 *Bonds
  Sold Between Interest Dates* against IRC § 61(a)(4), not
  Treas. Reg. § 1.61-7(c), which is the traded-flat pattern.
- **Decision posture:** the opening milestone produces executable evidence and
  bounded production-contract questions. It does not itself select a citizen,
  schema, ADR, storage mechanism, full tax model, or production migration. The
  three shapes are prototype evidence and do not become production contracts
  through effort or similarity.

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
  existing artifacts is **not decided and not recommended** on the repaired
  evidence. The executed difference reduces to an owner-held product
  requirement: when a later year needs the basis consequence, what does it
  hold? A durable relationship edge on the carried artifact closes the one
  failing later-year task; that is not the same claim as a new citizen kind.
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
  alongside it; code at tag `exhibits/reported-interest-tax-concept/it1`).
- **Previous phase close:**
  `docs/milestone-retrospectives/2026-08-20-claim-boundary-exploration.md`.
