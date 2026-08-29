<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "document-ordinary-fact-translation",
  "active_plan": "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md",
  "milestone_state": "track-2",
  "status": "Tax Concept Derivation remains active. Document and Ordinary-Fact Translation Vertical selected 2026-08-28 from origin/main at 0869f10a. The milestone will create the first fluid taxable-interest translation domain model, establish a source-independent canonical slice joining a Form 1099-INT report to ordinary bond-purchase facts, and proceed into bounded production behavior unless evidence exposes a material owner decision. The later-year basis question is deferred until this current-year translation exists.",
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
  **TRACK 2 REVIEWED 2026-08-28 — READY at `c4e74837`**.
- **Base:** `origin/main` at
  `0869f10a90403f9ed35e27d326ba46dc4da57bba`, including the merged owner model.
- **Branch:** `milestone/document-ordinary-fact-translation`, draft PR #188.
- **Next move:** owner decision on merging PR #188. Independent review
  (Grok CLI reviewer, charter
  `docs/reviews/charter-2026-08-28-document-ordinary-fact-translation-review.md`,
  record alongside it) returned **READY** at `0cac5ce9` with one non-blocking
  finding; that finding and three test-honesty defects it surfaced are
  repaired at `c4e74837`. Track 1 collapsed: Track 0 left one viable
  canonical shape, so a discriminating prototype would compare it only against
  shapes already known non-viable or already decided.
- **Track 2 result.** The canonical slice is implemented and projected onto
  line 2b and Schedule B; evidence is
  `docs/milestones/document-ordinary-fact-translation/production-translation.md`.
  Two schema successors were minted: `source-family.v3` (`identity_association`,
  designed in Track 0) and `attachment-rule.v9`, which was **not** predicted —
  the adjustment-row `kind` is a class-authority key, not a display hint, so
  the fourth adjustment class could not borrow an existing one. T1–T9 run as
  15 package-level tests. Two items are named future work: statement-level
  association, and the masking-sibling amount guard, which would need a
  cross-family value read and therefore a decision about ADR-0066's closed
  predicate language.
- **Pre-existing, not this milestone's:** six `fast-lane budget exceeded`
  failures, set-identical at `6758be16` and on this branch, confirmed
  independently by the reviewer in sequential detached runs. Budget decay, not
  logic failure. The count is timing-sensitive under `-n auto` (a contended run
  produced 18 vs 17); compare the sets, not the counts. This wants its own
  scheduled work — it is accumulating and no milestone owns it.
- **Track 0 result.** The fluid domain model is
  `docs/domain-models/taxable-interest-translation.md`; the canonical slice,
  payloads, contract comparison, and adversarial closure are
  `docs/milestones/document-ordinary-fact-translation/canonical-slice.md`.
  New entity kinds and object-valued canonical members cost no schema change.
  The one genuine gap is a **required cross-family association** check, added
  as an additive `source-family.v3` successor to ADR-0066's existing
  `identity_exclusivity` machinery.
- **Just-closed evidence:** Reported Interest to Tax Concept Vertical Slice —
  **CLOSED 2026-08-28**. Exhibit
  `exhibits/reported-interest-tax-concept/it6`. Four packagings ran on six
  cases; no new citizen was established as necessary.
- **TI-A1.** Prototype refuses coverage. The incumbent cannot determine whether
  § 135 applies and may publish full inclusion. The fixture does not prove the
  published number wrong.
- **Authority.** Pub. 550 *Bonds Sold Between Interest Dates* against
  IRC § 61(a)(4), not Treas. Reg. § 1.61-7(c).
- **Decision posture:** a source-independent canonical layer is selected
  product direction. Its exact facts, identities, relationships, and fit with
  current contracts are to be established through domain modeling and
  executable evidence, then implemented when no material choice remains.

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

- The minimum canonical facts and relationships joining a documentary interest
  report to an ordinary acquisition circumstance remain open.
- The exact identity and lifecycle of the bounded canonical slice remain open,
  including the independent effects of source correction, circumstance
  correction, tax-rule succession, and reporting-artifact succession.
- Whether any derived tax concept needs separately durable workspace standing
  is subordinate and unselected until a named consumer makes it material.
- The minimum durable shape of a concept-coverage profile is open.
- The question of subject on a joint return remains outside the opening slice.
- The first contrasting tax concept is not yet selected.
- `OV-1`, `SC-13`, and `SC-16` remain carried but unselected. This phase does
  not absorb them unless a later milestone explicitly selects them.

## Active milestone

The active plan is
`docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`.
It establishes the first fluid domain model and the first canonical translation
slice connecting documentary and ordinary inputs. The plan expects bounded
production implementation after any genuinely discriminating prototype work.

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
migration beyond the active bounded translation remain later work.

## Pointers

- **Phase overview:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-overview.md`.
- **Phase roadmap:**
  `docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md`.
- **Active milestone plan:**
  `docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md`.
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
