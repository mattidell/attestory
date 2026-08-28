<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "tax-concept-derivation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md",
  "milestone_state": "track-3",
  "status": "Tax Concept Derivation established 2026-08-27 from origin/main at 9159a13d. The opening milestone is a bounded exploration turned completed executable vertical slice: one synthetic 2025 Form 1099-INT box-1 item, one accrued-interest-at-purchase contrast, and the path from source report through ordinary circumstance and tax classification to tax concept and simulated return projection. It does not attempt full taxable-interest coverage, select a production representation, or reopen source-family closure and provisional-return design. OUTCOME. Two rival representation shapes were built and executed on all six cases through the real engine expression evaluator, on exhibit exhibits/reported-interest-tax-concept/it1: a DISTRIBUTED shape (ordinary facts plus a tax rule derive an item-linked result, no durable determination object) and an EXPLICIT DETERMINATION shape (recoverable item-level result holding reported, includible, non-includible, basis consequence, item identity, rule, authority, source facts). Both produce every required number on all six cases, so arithmetic discriminates nothing. The static ten-requirement rubric discriminates nothing either once the distributed shape has authority attached per symbol. Two dynamic probes decide it: under a partial refresh after the 300-to-250 circumstance correction the distributed shape asserts 950 includible while its basis symbol still reads 300 and CANNOT DETECT the disagreement; and its carried basis consequence cannot state the reported or includible amount it is consistent with in a later year, when the producing facts belong to a prior workspace. RECOMMENDATION: the explicit determination shape, on that narrow ground and no other. The honest counter-case is that the distributed shape's lifecycle displacement is more precise, and that the first probe alone would prove nothing if every symbol were always re-run from current facts. SMALLEST REMAINING OWNER DECISION: must a consequence that outlives the tax year be self-checkable? That is a product question about the year-of-disposition experience and no representation experiment can answer it. TWO CLAIMS ARE WITHDRAWN AND MUST NOT BE RE-ASSERTED. First, that the incumbent produces the correct number in all six cases: it is silently wrong on TI-A1, because the 2025 package contains no section 135 or Form 8815 content and box 1 flows to line 2b unreduced. Second, that a tax-year {yes, no} ordinary-circumstance declaration plus a guard clause in the line-2b rule passes the cases: that design was never built or executed and does not follow, because TI-B2 requires the ordinary circumstance, its amount, and item linkage rather than merely yes/no, and TI-N1 must distinguish yes-with-amount from yes-without, which a guard reading only yes/no cannot do. The existing classified Schedule B adjustment cannot stand in for either half; it is a tax conclusion supplied to the engine, and the cases exist to withhold exactly that. Do not describe the necessity hypothesis as defeated: the earlier defeat rested on an unexecuted counterexample, and 'the engine can subtract an already-classified adjustment' establishes working arithmetic, not derivation from ordinary facts. A PAPER CLAIM OVERTURNED BY EXECUTION: conditional_dependency_set was recorded as unable to make an amount conditional on a yes because its members must be ref expressions. True, but it does not bite here, because the ordinary circumstance is a keyed per-item symbol rather than a family collect; executed on TI-N1 the evaluator blocked with DEPENDENCY_ABSENT and named the missing fact. The treatment is grounded in IRS Publication 550 'Bonds Sold Between Interest Dates' against IRC 61(a)(4), NOT in Treas. Reg. 1.61-7(c), which is the traded-flat pattern; 1.61-7(d) reaches only the seller. A missing Treasury Regulation authority family in citation.v1 is recorded as a production condition and a candidate separate substrate milestone, not addressed here. Prototype code is not on the milestone branch; the durable record is docs/prototypes/reported-interest-tax-concept/charter.md and examination.md.",
  "current_role": "Milestone lead — executable slice complete, durable documents reconciled; awaiting fresh whole-candidate independent review",
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
  **IN CLOSEOUT**. A completed executable vertical slice: the six cases ran end
  to end under two rival representation shapes through the engine's real
  expression evaluator. The durable documents report the executed comparison.
- **Base:** `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`, which includes the completed
  Taxable Interest Modeling milestone through PR #185.
- **Branch:** `milestone/tax-concept-derivation-phase-definition`.
- **Next move:** a fresh whole-candidate independent review, then the owner
  decision. The recommendation is the **explicit determination** shape, on the
  narrow ground of two dynamic probes, conditional on one product question:
  must a consequence that outlives the tax year be self-checkable?
- **Withdrawn — do not re-assert.** That the incumbent produces the correct
  number in all six cases: it is **silently wrong on TI-A1**, because the
  package has no § 135 or Form 8815 content. And that a tax-year `{yes, no}`
  fact plus a line-2b guard passes the cases: never built or executed, and it
  does not follow from the cases. Do not describe the necessity hypothesis as
  defeated — that record rested on an unexecuted counterexample.
- **Recanted authority — do not re-assert.** The treatment is Pub. 550 *Bonds
  Sold Between Interest Dates* against IRC § 61(a)(4), not
  Treas. Reg. § 1.61-7(c), which is the traded-flat pattern.
- **Decision posture:** the opening milestone produces executable evidence and
  bounded production-contract questions. It does not itself select a citizen,
  schema, ADR, storage mechanism, full tax model, or production migration. The
  two shapes are prototype evidence and do not become production contracts
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
  existing artifacts is now **recommended, not decided**: the slice recommends a
  separately recoverable determination, and the owner selects the production
  contract. The recommendation reduces to one product question — whether a
  consequence outliving the tax year must be self-checkable.
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
