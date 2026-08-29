<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "document-ordinary-fact-translation",
  "milestone_state": "track-2",
  "status": "Selected 2026-08-28. Establish the first source-independent canonical fact slice through which a Form 1099-INT report and a structured ordinary purchase account can jointly support an accrued-interest tax treatment. Create the first fluid agent-maintained domain model, compare only consequential canonical shapes, and continue into a bounded production path unless evidence exposes a material owner decision.",
  "current_role": "Foreman — owner-directed milestone lead",
  "current_prompt": "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md",
  "scope": [
    "model the taxable-interest translation frontier in plain language and keep that domain model fluid and non-contractual",
    "define and exercise a source-independent canonical slice joining a documentary report to ordinary purchase facts about the same obligation",
    "derive the bounded accrued-interest treatment through adopted rules and project it to the existing return path without accepting a preclassified adjustment as the ordinary input",
    "continue into bounded production implementation when the evidence selects a coherent shape"
  ],
  "non_goals": [
    "no universal tax ontology, general securities ledger, whole taxable-interest census, filing system, or production user interface",
    "no attempt to make a tax-document schema or an ordinary-language question template the canonical workspace model",
    "no later-year disposition implementation or decision about durable derived-result storage unless the current slice makes it immediately load-bearing",
    "no prototype iteration whose alternatives cannot change a named product behavior"
  ],
  "deep_reads": {
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Owner Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Owner-model alignment",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Selected product direction",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Scope",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Synthetic scenarios",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Tracks",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Stop conditions",
      "docs/milestones/reported-interest-tax-concept/README.md#What else is established",
      "docs/milestones/reported-interest-tax-concept/incumbent-representation.md#The shape underneath all six",
      "docs/milestones/reported-interest-tax-concept/synthetic-case-specification.md#What the six cases jointly show",
      "docs/roles/qualitative-review.md#Start by drawing the box",
      "docs/roles/qualitative-review.md#Make evidence load-bearing",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Document and Ordinary-Fact Translation Vertical

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `document-ordinary-fact-translation`
- State: planned 2026-08-28
- Base: `origin/main` at `0869f10a90403f9ed35e27d326ba46dc4da57bba`
- Branch: `milestone/document-ordinary-fact-translation`
- Execution posture: owner-directed milestone lead for modeling, evidence, and
  bounded implementation; a separately launched independent reviewer examines
  the final candidate

## Owner-model alignment

The product exists to help a person navigate between documents, ordinary life,
tax rules, tax concepts, and return reporting. It should not require the user
to know the tax classification of their own circumstances before the product
can help.

This milestone uses two kinds of model deliberately:

- a fluid textual domain model maps the wider translation frontier for
  comprehension, product interaction, unsupported-case articulation, and
  later roadmap selection; and
- a precise canonical slice represents only the facts and relationships needed
  to execute the selected accrued-interest treatment.

The fluid model is not a contract and need not become schema. The canonical
slice is not defined by either the document shape or the user-facing question
shape. The lead has the standing discretion described in `OWNER_MODEL.md` to
broaden the working domain model and, after making a plain-language value case,
the implementation scope.

## Objective

Establish and execute the first source-independent workspace translation in
which:

1. a Form 1099-INT contributes an attributed report of what the payer said;
2. a structured ordinary-language interaction contributes facts about an
   identified bond acquisition and accrued-interest payment;
3. both input paths refer to shared canonical entities or events without being
   collapsed into one proposition;
4. adopted tax content derives the bounded current-year treatment rather than
   accepting a preclassified Schedule B adjustment as user input; and
5. the resulting tax concept is projected to the simulated return with an
   explanation that separates source report, user-supplied circumstance, rule,
   conclusion, and unsupported boundary.

The milestone should reach bounded production behavior. It stops at modeling
or prototype evidence only when materially different canonical shapes remain
and the evidence cannot resolve a consequential identity, lifecycle,
authority, or migration choice.

## Current state

The completed reported-interest experiment established several useful facts:

- the production engine already computes the selected subtraction when given
  an amount already classified as an accrued-interest adjustment;
- arithmetic and packaging did not establish a need for a new citizen;
- the 2025 content domain contains documents, document rows, issuer roles, and
  engine infrastructure, but no obligation, acquisition, account, purchase, or
  disposition referent for the ordinary circumstance;
- the current adjustment cannot name the reported item it reduces; and
- the reporting label does not itself assert the substantive tax proposition
  or its authority.

That work did not establish a canonical fact model or a translation from
ordinary user facts into one. The named later-year basis frontier is therefore
deferred: a later consumer should test a current canonical model, not decide
whether the missing model should exist.

## Selected product direction

The following are selected directions, not prototype questions:

- Tax documents are evidence and document-shaped reporting models. They are
  not the canonical tax-domain model.
- The ordinary-language input surface is a structured projection for eliciting
  and reviewing facts. It is not the canonical model either.
- The workspace needs a source-independent canonical account of the relevant
  entities, events, quantities, relationships, and attributed propositions so
  documentary and ordinary inputs can participate in the same tax reasoning.
- A document field may map directly into a bounded tax concept only when an
  adopted rule establishes that equivalence. Form location alone does not
  define substantive tax meaning.
- Tax rules, not the user-facing question or document adapter, own the tax
  classification.
- The wider domain frontier remains in scope for fluid textual modeling even
  when most of it is not selected for canonical representation or production
  implementation.

The work may discover that the current schema or accepted artifact contracts
do not fit this direction. That is evidence for a successor or replacement,
not a reason to force the selected product model back into a document shape.

## Domain frontier model

Create `docs/domain-models/taxable-interest-translation.md` as an
agent-maintained working model. It should have a short plain-language stratum
that explains:

- the life circumstance being translated;
- what the document contributes;
- what the person contributes;
- what law, administrative rules, and professional or institutional
  conventions contribute;
- what translation the application performs;
- what reaches the return; and
- what the application cannot yet determine or translate.

Below that simple stratum, map only enough of the surrounding frontier to
locate the slice honestly: taxpayer, obligation, acquisition, accrued interest,
payer or broker reporting, tax authority, classification, basis consequence,
return projection, explanation, user adoption, refusal, and professional
handoff. The model may change freely during the milestone. It should not be
graded as a contract or exhaustive ontology.

## Scope

### Domain and product modeling

- Establish the first useful textual model of the taxable-interest translation
  frontier and its multiple perspectives.
- Describe the application's function as an alternative transparent
  translation process, not a reproduction of a CPA's internal reasoning or
  professional authority.
- Identify the supported translation, adjacent unknowns, and useful product
  behavior when the translation cannot be completed.

### Canonical fact slice

- Represent the minimum referents needed for the bounded case. Candidates may
  include taxpayer, obligation, acquisition, reported-interest observation,
  accrued-interest payment or allocation, amounts, dates, and their
  relationships.
- Keep attributed reported propositions distinct from ordinary circumstance
  facts and derived tax conclusions.
- Give documentary correction and ordinary-fact correction independent,
  observable effects.
- Make ambiguous or missing association detectable rather than silently attach
  an adjustment to an aggregate.

### Input projections

- Map the existing Form 1099-INT source path into the bounded reported
  proposition without redefining it as taxable income.
- Define a structured, comprehensible ordinary-language input projection for
  the acquisition circumstance. It must be possible to render a reviewable
  plain-language account of what the person supplied.
- Exercise the mappings with synthetic contributions through the closest
  production boundary available. A blank-text interpretation system is out of
  scope.

### Derivation and return projection

- Derive the selected accrued-interest treatment from the canonical reported
  and ordinary facts through adopted rule content.
- Preserve the source-reported amount while deriving the bounded includible
  amount and the separately accountable basis consequence.
- Project the current-year result to the existing taxable-interest and
  Form 1040 line-2b path without claiming full taxable-interest coverage.
- Preserve exact provenance and visible refusal for missing or ambiguous
  dependencies.

### Cadence evidence

- Record which part of the work was broad domain mapping, canonical design,
  discriminating prototype evidence, and production implementation.
- At close, state in plain language whether the cadence produced a reusable
  pattern, what it cost, and what should be repeated or simplified.
- Update the domain model's simple stratum when doing so remains useful; do not
  preserve working explanations merely because they were written.

## Non-goals

- No universal model of investments, transactions, ordinary life, tax law, or
  professional practice.
- No general securities ledger, lot-selection system, disposition engine, or
  later-year return implementation.
- No whole taxable-interest census, education-exclusion implementation,
  nominee allocation, bond-premium computation, market-discount election, or
  joint-return subject model.
- No production graphical interface, conversational free-text interpretation,
  filing, transmission, or claim of professional authority.
- No attempt to make the fluid domain model complete, canonical, binding, or
  mechanically validated.
- No automatic new citizen, schema family, ADR, or persistent derived-result
  store merely because an exploratory model used one.
- No repetition of the completed four-packaging comparison unless a new
  product behavior genuinely distinguishes the alternatives.

## Semantic questions

The lead must answer these before selecting a production shape:

1. What proposition does the Form 1099-INT actually contribute, and who is its
   author?
2. What ordinary propositions can the person reasonably supply without being
   asked for a tax classification?
3. What real-world referent lets the report and purchase facts concern the same
   thing?
4. Which identity and relationship distinctions are necessary to avoid
   attaching one adjustment to the wrong reported item or obligation?
5. What does the tax rule derive that neither input source establishes alone?
6. How are document correction, ordinary-fact correction, tax-rule succession,
   and reporting succession separated?
7. What can the product say or help the person do when a report exists but the
   necessary ordinary fact is missing, when the ordinary fact has no matching
   report, or when association is ambiguous?
8. Which aspects belong only in the fluid frontier model, which belong in
   canonical workspace facts, and which remain derived or projected?

Questions about durable storage of derived tax determinations are subordinate.
They enter only when the selected current slice or a named consumer makes the
choice behaviorally material.

## Synthetic scenarios

Use obviously synthetic identities and amounts. The exact amounts may be
selected during modeling, but every case must share a stable semantic account.

| Case | Documentary input | Ordinary input | Required observation |
| --- | --- | --- | --- |
| T1 fully includible | One box-1 report | No between-dates acquisition circumstance applies | Report survives; adopted rule produces the fully includible bounded result |
| T2 accrued-interest treatment | Same reported amount | Identified acquisition and accrued-interest payment | Report survives unchanged; rule produces a different current-year result and basis consequence |
| T3 missing circumstance answer | Report present | Required ordinary answer absent | Product names the missing ordinary question or refuses; no preclassified default |
| T4 ordinary fact without report | No matching report | Acquisition circumstance present | Fact remains understandable; no unsupported return contribution is invented |
| T5 ambiguous association | Multiple plausible reported items or obligations | One acquisition circumstance | Product refuses silent association and identifies the ambiguity |
| T6 document correction | Corrected reported amount | Acquisition fact unchanged | Only dependent conclusions change; the ordinary fact is not rewritten |
| T7 circumstance correction | Report unchanged | Corrected accrued amount or association | Report remains what the source said; dependent tax conclusions change |
| T8 identity discriminator | More than one obligation under one payer or account | Facts concern exactly one obligation | Canonical identity, not form-row or payer aggregate identity, selects the affected item |
| T9 unsupported neighbor | A source or circumstance outside the bounded treatment | Enough facts to recognize the neighboring region | Product describes the translation it cannot perform and does not silently claim coverage |

If a proposed canonical shape cannot express T1 through T9 honestly, it is not
a viable implementation candidate.

## Contracts and authority posture

Expected existing surfaces include the append-only act log, finding and
derived-finding machinery, rule artifacts, source contribution and statement
identity, currency and provenance, package adoption, citations, the current
interest composition, and the line-2b projection. The lead must read the exact
accepted ADR text and committed consumers before relying on any of them.

No existing contract is presumed adequate merely because it accepts a nearby
payload. If an honest canonical fact instance cannot be constructed under an
existing schema, record the collision in plain language and compare successor,
reuse, or replacement paths against the product behavior. Do not mutate a
published schema or accepted ADR history.

Official tax sources support the bounded treatment. Professional and
institutional practices may inform the fluid domain model and user interaction,
but must not be presented as controlling law. Every load-bearing tax
proposition must state the type and force of its support.

## Evidence and development route

1. **Map first.** Write the fluid domain model and fixed semantic cases before
   selecting fields or citizens.
2. **Inventory second.** Reconstruct the current document, adjustment,
   derivation, and projection paths from committed artifacts and consumers.
3. **Instantiate candidates.** Write fully resolved synthetic examples for
   every proposed canonical payload before schema or runner work.
4. **Prototype only contested shapes.** If two materially different identities
   or relationships remain plausible, compare the smallest versions against
   T1 through T9. If no consumer behavior differs, choose the simpler
   reversible path or defer the choice rather than polishing rivals.
5. **Build after selection.** Implement the selected bounded translation in
   the production fact, rule, package, and projection paths.
6. **Review the whole translation.** Independent review attacks the domain
   account, user-facing ordinary-fact projection, canonical semantics,
   authority, lifecycle, unsupported behavior, and production evidence
   together.

## Deliverables

- `docs/domain-models/taxable-interest-translation.md`
- source-independent canonical fact and relationship artifacts required by the
  selected slice, using existing schemas or additive successors as evidence
  requires
- one structured ordinary-fact input projection and a reviewable plain-language
  rendering of the synthetic answer
- adopted tax rule content deriving the bounded treatment
- bounded integration with taxable interest and Form 1040 line 2b
- synthetic fixtures and tests for T1 through T9
- updated phase roadmap and phase state at close
- a short retrospective evaluating both product value and the tested cadence

Working comparison notes and prototypes are retained only when they remain
useful evidence. Final deliverables contain no review transcripts, role
metadata, session URLs, or execution diary.

## Verification

The implementation plan must name focused tests once the selected files and
consumers are known. Before handoff:

- run the cheapest focused tests during iteration;
- run the full test suite for any change under `packages/kernel/` or
  `packages/derivation/`;
- exercise the selected positive, correction, ambiguity, missing-input, and
  unsupported cases through the real contribution and derivation boundaries;
- verify exact currentness and provenance, not only numeric output;
- verify the existing unmigrated interest path remains honest;
- run `python3 tools/governance_lint.py`;
- run `python3 tools/envelope_scan.py --range origin/main..HEAD`;
- run `git diff --check`; and
- rely on the PR `verify` workflow as the gate of record.

## Data safety

All committed examples use obvious `demo.*` or `demo-*` identities and wholly
synthetic amounts and circumstances. No personal document, tax fact, prior
return, private output, refusal reason, credential, or absolute workstation
path may enter the branch, domain model, fixture, test, review, or handoff.

## Track 0 adversarial closure

This declaration is intentionally pending in the initial plan. Track 0 must
replace each pending item with concrete evidence before production schema or
shared-runtime implementation begins.

- Authority-lifecycle table: PENDING — reported observation, ordinary facts,
  association, derived current-year treatment, basis consequence, and return
  projection must each name meaning, author, dependencies, and invalidators.
- Empty/nonempty authority matrix: PENDING/N-A — apply to every family or
  absence claim the selected shape reuses; mark N-A only when the canonical
  path introduces no such dependency.
- Late-member lifecycle: PENDING/N-A — trace any reused or new aggregate whose
  membership can change; do not invent closure merely to satisfy the table.
- Neighboring capability dependency diff: PENDING — compare the current
  line-2b and Schedule B prerequisites with the selected translation on active,
  absent, ambiguous, and unsupported paths.
- Reused-claim semantic/lifecycle equivalence: PENDING — no existing document,
  adjustment, or closure claim is presumed to mean the canonical ordinary fact
  or tax conclusion.
- Integration surface: PENDING — enumerate every binding of each externally
  consumed symbol and build each materially distinct disposition through its
  real consumer.
- Known limitations affecting correctness: PENDING — owner disposition is
  required only for a material unresolved choice that evidence cannot settle.

## Tracks

### Track 0 — Domain frontier and canonical semantic box

Create the fluid taxable-interest translation model; verify the bounded tax
treatment; fix T1 through T9; reconstruct the incumbent path and its consumers;
identify candidate canonical referents and relationships; instantiate honest
payload examples; and complete the adversarial-closure declaration.

Do not stop because the domain map expands beyond the current implementation.
Stop only if the selected slice itself cannot be stated without an owner-held
product choice or governance interpretation.

### Track 1 — Discriminating canonical prototype

Run this track only where Track 0 leaves two or more materially different
canonical identities, relationships, or correction behaviors. Compare them on
the same T1 through T9 cases and the same access assumptions. Record what each
prototype establishes and does not establish. Select or defer; do not iterate
on prose after the product requirements stabilize.

If Track 0 leaves one coherent reversible shape and committed machinery can
instantiate it honestly, this track collapses into focused implementation
spikes inside Track 2 rather than becoming a mandatory prototype round.

### Track 2 — Bounded production translation

Implement the selected canonical facts and relationships, document and
ordinary-input mappings, tax classification, provenance, correction behavior,
coverage refusal, and line-2b projection. Keep legacy interest content working
alongside the selected slice unless evidence justifies and reviews a broader
migration.

## Review gate

Have a fresh reviewer examine the exact final candidate against the Product
Model, fluid domain model, plan, primary tax authority, committed consumers,
T1 through T9, and the complete production diff. Repair substantive findings,
then have the foreman retain only useful abstractions and evidence, evaluate
the cadence in the retrospective, and prepare the milestone for owner merge.

## Stop conditions

Stop for the owner when:

- two materially different product translations remain viable after the
  smallest useful executable comparison and choosing one creates substantial
  migration or irreversible identity cost;
- the work turns on interpreting reserved governance doctrine;
- official authority does not support the selected treatment or exposes a
  materially different fact pattern;
- an honest implementation requires personal or non-synthetic data;
- a proposed input asks the user to supply a tax classification rather than an
  ordinary fact and no alternative projection is viable; or
- the lead cannot explain in plain language what additional work would change.

Do not stop merely because a current contract is inconvenient, the domain
model broadens, implementation scope grows, or the plan did not predict a
useful supporting artifact. Make the value, cost, risk, and displaced-work case
under `OWNER_MODEL.md`, keep the change reviewable, and proceed when the choice
is reversible and aligned.

## Exit criteria

The milestone is complete when:

1. a useful fluid domain model explains the wider translation frontier and the
   selected slice in plain language without claiming contract or exhaustive
   status;
2. the document contribution, ordinary-language contribution, canonical
   facts, tax classification, tax concept, and return projection remain
   recoverably distinct;
3. both input paths refer to shared source-independent identities and the
   implementation detects missing or ambiguous association;
4. the user is never required to enter an accrued-interest tax adjustment as
   the ordinary fact the product is supposed to derive;
5. T1 through T9 are instantiated and the applicable production cases execute
   through real contribution, derivation, and presentation consumers;
6. document and ordinary-fact corrections displace exactly the conclusions
   whose provenance depends on them;
7. the bounded result reaches taxable interest and line 2b without silently
   claiming full taxable-interest or neighboring-case coverage;
8. a fresh reader can recover what the source reported, what the person said,
   what rule translated it, what the product concluded, and what remains
   unsupported;
9. any new canonical shape has concrete positive instances, exact consumers,
   reviewed lifecycle behavior, and an explicit relationship to existing
   contracts; and
10. the retrospective states whether the map → canonical slice → discriminate
    → build → abstract cadence produced enough value to repeat, simplify, or
    revise before projecting a longer roadmap.
