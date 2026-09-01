<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "document-ordinary-fact-translation",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-29-document-ordinary-fact-translation-seams.md",
  "status": "CLOSED 2026-08-30. Six ADRs accepted (0067-0072), decomposed by architectural seam: direct field-ref extraction; two-tiered obligation identity association with mandatory, report-scoped confirmation; per-pairing and aggregate accrued-amount supportability; standing workspace authorization; rule-owned pairing-scoped current-year and basis consequences; legacy/pairing coexistence and migration that never silently discards a live claim; a fluid domain model and structural unsupported-coverage disclosure; and integration through the real production package resolver, live coordinator, and presentation projection. Merged into main. See docs/phase-state.md for the current, single re-entry pointer.",
  "current_role": "Foreman — between-milestones selection",
  "current_prompt": "docs/phases/tax-concept-derivation/tax-concept-derivation-roadmap.md",
  "scope": [
    "model the taxable-interest translation frontier in plain language and keep that domain model fluid and non-contractual",
    "resolve six named architectural seams independently, each on its own smallest discriminating fixtures, before any seam's shape is treated as selected",
    "derive the bounded accrued-interest treatment through adopted rules and project it to the existing return path without accepting a preclassified adjustment as the ordinary input",
    "run one integration experiment only after the seams converge, to confirm provenance and lifecycle compose across seam boundaries",
    "continue into bounded production implementation only for seams whose evidence selects a coherent shape"
  ],
  "non_goals": [
    "no universal tax ontology, general securities ledger, whole taxable-interest census, filing system, or production user interface",
    "no attempt to make a tax-document schema or an ordinary-language question template the canonical workspace model",
    "no later-year disposition implementation or decision about durable derived-result storage unless the current slice makes it immediately load-bearing",
    "no full rival architectures compared end to end; rivals are scoped to one seam at a time",
    "no prototype iteration whose alternatives cannot change a named product behavior"
  ],
  "deep_reads": {
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Owner Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "PROJECT_PLANNING.md#Frontier Reduction and Direct-Build Routing",
      "PROJECT_PLANNING.md#Prototype-Driven Decisions",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Owner-model alignment",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Selected product direction",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Synthetic scenarios",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Seams",
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
      "PROJECT_PLANNING.md#Prototype-Driven Decisions",
      "docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Document and Ordinary-Fact Translation Vertical (seam-decomposed)

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `document-ordinary-fact-translation`
- State: closed
- Base: `origin/main` at `0869f10a90403f9ed35e27d326ba46dc4da57bba`
- Branch: `milestone/document-ordinary-fact-translation-seams`, merged into
  `main`
- Execution posture: owner-directed milestone lead runs a sequence of small
  discriminating prototypes, one per architectural seam, followed by one
  integration experiment; a separately launched committee reviews each seam

## Why this milestone is decomposed by seam

Fusing several independent architectural decisions into one build makes it
difficult to know which specific choice caused a success or a failure.
Comparing two complete architectures — the incumbent or a full rival — would
compound that difficulty into a costly combinatorial exercise on top of it.

The better approach, and the one this branch adopts, is a sequence of small
discriminating prototypes around individual seams, followed by one
integration experiment. Isolation determines what each component means and
how it fails; integration then confirms that their provenance and lifecycle
compose correctly. This branch does not carry over the prior branch's
production code. It treats that branch's artifacts
(`docs/milestones/document-ordinary-fact-translation/`,
`docs/domain-models/taxable-interest-translation.md`, the rejected review) as
reference evidence a seam charter may cite, not as a starting implementation.

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

The milestone should reach bounded production behavior. It stops a seam at
modeling or prototype evidence only when materially different shapes remain
and the evidence cannot resolve a consequential identity, lifecycle,
authority, or migration choice for that seam.

## Selected product direction

The following are selected directions, not prototype questions:

- Tax documents are evidence and document-shaped reporting models. They are
  not the canonical tax-domain model.
- The ordinary-language input surface is a structured projection for
  eliciting and reviewing facts. It is not the canonical model either.
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

## Domain frontier model

Reuse or revise `docs/domain-models/taxable-interest-translation.md` as an
agent-maintained working model (the prior branch's version is a starting
draft, not a frozen artifact). It should have a short plain-language stratum
that explains: the life circumstance being translated; what the document
contributes; what the person contributes; what law, administrative rules, and
professional or institutional conventions contribute; what translation the
application performs; what reaches the return; and what the application
cannot yet determine or translate.

Below that simple stratum, map only enough of the surrounding frontier to
locate each seam honestly. The model may change freely during the milestone.
It should not be graded as a contract or exhaustive ontology.

## Synthetic scenarios

Use obviously synthetic identities and amounts. Every seam's fixtures must
share this stable semantic account, restricted to the sub-cases each seam
actually exercises (named per seam below).

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

If a proposed seam shape cannot express its assigned subset of T1–T9 honestly,
it is not a viable candidate for that seam.

## Semantic questions

The lead must answer these before selecting a production shape for the
integrated vertical. Each is answered by one or more seams below.

1. What proposition does the Form 1099-INT actually contribute, and who is its
   author? (Seam 1, Seam 2)
2. What ordinary propositions can the person reasonably supply without being
   asked for a tax classification? (Seam 6)
3. What real-world referent lets the report and purchase facts concern the
   same thing? (Seam 2)
4. Which identity and relationship distinctions are necessary to avoid
   attaching one adjustment to the wrong reported item or obligation? (Seam 2,
   Seam 3)
5. What does the tax rule derive that neither input source establishes alone?
   (Seam 5)
6. How are document correction, ordinary-fact correction, tax-rule succession,
   and reporting succession separated? (Seam 2, Seam 5)
7. What can the product say or help the person do when a report exists but the
   necessary ordinary fact is missing, when the ordinary fact has no matching
   report, or when association is ambiguous? (Seam 2, Seam 3)
8. Which aspects belong only in the fluid frontier model, which belong in
   canonical workspace facts, and which remain derived or projected? (all
   seams; reconciled at Integration)

Questions about durable storage of derived tax determinations are subordinate.
They enter only when the selected current slice or a named consumer makes the
choice behaviorally material.

## Seams

Six seams decide the architecture. Each seam is scoped to answer one question
on the smallest fixtures that could discriminate its rivals — not to build a
usable end-to-end path. A seam that has one clearly superior implementation
after execution is selected and closed; prototyping does not continue on a
converged seam merely because other seams are still open.

Each seam is chartered separately under
[`PROJECT_PLANNING.md`, **Prototype-Driven Decisions**](../../../../PROJECT_PLANNING.md#prototype-driven-decisions)
and the **Prototype Economic Gates** (`docs/adr/0013-prototype-economic-gates.md`,
gate mechanics now governed by `PROJECT_PLANNING.md`). A seam's charter lives
at `docs/prototypes/<seam-key>/plan.md` and runs Gates 0–8: decision
inventory, eligibility score, paper-evidence plan, evidence ladder, fixed
caps, review triage, minimum acceptable converged subset, and production
adoption boundary. This milestone plan fixes each seam's question, rival
axes, and test subset; the seam charter fixes the score, caps, and role
dispatch.

### Rival-builder and review protocol (applies to every seam that scores prototype-eligible)

- **Builders.** One incumbent-track builder plus one **clean-room rival**
  builder who reads only the seam's charter, the governance set, official tax
  authority where relevant, and the frozen fixtures — never the incumbent's
  design, code, or prior review notes. Follow
  `docs/roles/builder.md` for shared obligations; the rival additionally
  follows a per-seam `roles/builder-rival.md` (independence obligation, no
  access to incumbent artifacts). A seam with no genuine second stance
  (Seam 4, and Seam 6 per the guidance below) may skip the rival and run one
  builder against the charter's tests instead of manufacturing an artificial
  second design.
- **Reviewers.** Every seam that reaches a build gets a three-seat committee,
  each reading only what its charter names:
  - **Clean-room reviewer** — has not read either builder's design rationale
    or the process log; reads only the charter, the fixtures, and the
    finished artifact(s), and reports whether a fresh reader can recover
    correct meaning, provenance, and failure behavior from the artifact
    alone. This is the fresh-reader legibility seat.
  - **Adversarial reviewer** — attacks both rivals (or the sole build) with
    equal effort against the seam's test list: hostile/independently
    asserted values, corrections, missing fields, misspelled or malformed
    declarations, masking cases, and any case named in the seam's row below.
    Reports what survives and what a rival quietly assumed rather than
    proved.
  - **Eligibility reviewer** — checks the seam against the Prototype
    Economic Gates rather than against the domain content: was this seam
    actually prototype-eligible (Gate 1) or could it have been built
    directly; did the evidence stop at the cheapest rung that answered the
    question (Gate 3) instead of over-building; does the result meet the
    seam's minimum acceptable converged subset (Gate 6); and is the winning
    shape actually eligible to cross into production (Gate 7), i.e. does it
    map to an accepted ADR statement or milestone disposition with a real
    production test, not just a prototype instance. This seat is the
    safeguard against re-running the prior branch's mistake of quietly
    fusing several decisions into one artifact.
  - A fourth, narrower seat (an implementation/expressiveness reviewer) opens
    only if the seam climbs to a code evidence rung, per the source
    families precedent in
    `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-completeness/plan.md`.
- **Disposition.** The foreman triages every finding (decision-blocking,
  production-condition, separate-decision, deferred-breadth, non-blocking)
  before authorizing another builder round. Only a decision-blocking finding
  may reopen a seam already scored converged.

### Seam 1 — Canonical value extraction

**Question.** Given an object-valued acquisition fact containing
`accrued_interest_paid_to_seller`, how should a rule obtain that amount?

**Rivals to compare.**
- runtime projection into a scalar collection;
- an explicit rule-produced numeric finding;
- direct per-item rule access, if it can be demonstrated without broadening
  the expression language excessively.

**Test only:** one authoritative amount; a hostile independently asserted
scalar; correction; missing field; exact provenance; a misspelled declaration
failing closed.

**Decision rule.** This seam decides whether a projected scalar family is
necessary at all. If direct per-item access resolves every test without
expression-language growth, prefer it and skip building the other two rivals
past paper.

### Seam 2 — Identity association

**Question.** How does the application establish that one acquisition
concerns one reported interest item? Keep tax arithmetic out of this
experiment — this seam produces an accountable relationship or a refusal,
never a tax adjustment.

**Rivals to compare.**
- generic family-declared association;
- a dedicated translation/association artifact;
- an existing rule-owned relationship mechanism, if one genuinely exists.

**Test:** one match; no match; several matches; report correction;
acquisition correction; addition and removal; exact document and acquisition
provenance.

**Decision rule.** Select the shape that gives every test case an accountable
relationship or a refusal, with exact provenance, at the least new machinery.

### Seam 3 — Relationship constraints

**Question.** Where should the rule "the accrued amount cannot exceed the
associated reported amount" live? Separate this from identity: identity says
which items correspond, this seam says whether the proposed tax treatment is
supported.

**Rivals to compare.**
- a constraint attached to the association;
- an adopted tax rule consuming the relationship;
- a generic relationship-validation mechanism.

**Test:** the unrelated-report masking case; multiple acquisitions sharing one
report.

**Decision rule.** This test tells us whether `constrain_amount` is genuinely
association machinery or tax-rule machinery — decide that question explicitly
rather than defaulting to wherever it was first written.

### Seam 4 — Standing authorization and currentness

**Question.** Can one standing workspace authorization supply calculation
currentness without becoming another taxpayer's or another year's authority?
The product semantics here are already selected, so this is a focused
implementation probe, not a rival comparison, unless the probe itself
surfaces a real second stance.

**Test:** correct taxpayer and year; wrong taxpayer; wrong year; ordinary
additions and removals; suspension or withdrawal; no renewed per-family
confirmation.

**Constraint.** This experiment must not involve accrued-interest tax
semantics — it tests authorization currentness alone.

**Decision rule.** One builder, the full committee (clean-room, adversarial,
eligibility) still reviews it. No rival is chartered unless the probe
discovers a second materially different currentness mechanism worth
comparing.

### Seam 5 — Rule-owned consequences

**Question.** Once the facts and relationship from Seams 1–3 are established,
how does an adopted rule publish both consequences: the current-year interest
adjustment and the item-level basis consequence?

**Rivals to compare.** The current hard-coded runner side effect against a
real declared mechanism (the mechanism the rule language and act log
already support for adopted-rule output). Expect the hard-coded side effect
to lose; charter the comparison so that expectation is falsifiable, not
assumed.

**Test:** exact rule identity; acquisition and report dependencies;
association support; tax citation; rule succession; correction displacement.

**Decision rule.** Select the mechanism that publishes both consequences with
exact dependencies and correction displacement without a hard-coded side
effect in the runner.

### Seam 6 — Ordinary input mapping

**Question.** This is mostly implementation repair, not an architectural
contest — no rival builder is required by default. Repair the existing
mapper so that:

- its subject and scope agree;
- it accepts ordinary-language structured answers;
- contribution admission validates its output;
- it emits only canonical circumstance facts;
- no tax classification is requested from the user.

**Decision rule.** One builder repairs the mapper against the charter's
tests; the eligibility reviewer confirms this seam was correctly routed as
direct-build rather than prototype (Gate 1 in `PROJECT_PLANNING.md`'s
routing table), and the clean-room and adversarial reviewers still examine
the repaired mapper before Integration consumes it.

## Integration checkpoint

Only after Seams 1–6 each select or explicitly defer a shape does one vertical
combine them and rerun T1–T9 in full. Integration tests the composed path:

```
standing authorization
        |
acquisition -- association -- reported item
        |                         |
        +---- adopted tax rule ---+
                     |
          current-year adjustment
          item-level basis consequence
```

Integration is not a seventh place to relitigate seam decisions. It confirms
that the seams' provenance and lifecycle compose: a document correction
displaces exactly the dependent conclusions; an acquisition correction does
the same; a suspended standing authorization blocks currentness without
touching tax semantics; the rule-owned consequence mechanism from Seam 5
reads the association from Seam 2 and the constraint from Seam 3 and the
value from Seam 1 without a hand-fused shortcut. Run this as one bounded
implementation spike (Track 2 below), not a new prototype round, unless
Integration itself exposes a cross-seam interaction no seam charter
anticipated — in which case name that interaction, treat it as its own
narrow decision inventory item, and route it through Gate 1 before building
further.

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
  store merely because a seam's prototype used one.
- No full rival architectures compared end to end; every rival comparison is
  scoped to exactly one seam's smallest discriminating fixtures.
- No repetition of the completed four-packaging comparison unless a new
  product behavior genuinely distinguishes the alternatives.

## Contracts and authority posture

Expected existing surfaces include the append-only act log, finding and
derived-finding machinery, rule artifacts, source contribution and statement
identity, currency and provenance, package adoption, citations, the current
interest composition, and the line-2b projection. Each seam charter must read
the exact accepted ADR text and committed consumers before relying on any of
them.

No existing contract is presumed adequate merely because it accepts a nearby
payload. If an honest canonical fact instance cannot be constructed under an
existing schema, record the collision in plain language and compare
successor, reuse, or replacement paths against the product behavior. Do not
mutate a published schema or accepted ADR history.

Official tax sources support the bounded treatment. Professional and
institutional practices may inform the fluid domain model and user
interaction, but must not be presented as controlling law. Every load-bearing
tax proposition must state the type and force of its support.

## Evidence and development route

1. **Map first.** Write or revise the fluid domain model and confirm T1–T9
   before chartering any seam.
2. **Inventory second.** Reconstruct the current document, adjustment,
   derivation, and projection paths from committed artifacts and consumers —
   the prior branch's Track 0 inventory is reusable starting evidence, to be
   re-verified, not re-trusted.
3. **Charter each seam independently**, in the order Seam 1 -> Seam 2 ->
   Seam 3 -> Seam 5 (each depends on the identity or value the previous
   seam selected), with Seam 4 and Seam 6 chartered in parallel since
   neither depends on the interest-specific seams.
4. **Prototype only contested seams**, per the rival-builder and review
   protocol above, on the seam's own smallest discriminating fixtures.
5. **Build after each seam selects.** Reimplement the selected shape for
   that seam in the production fact, rule, package, or projection path
   before opening the next dependent seam, so later seams charter against
   real committed consumers rather than another seam's still-open
   prototype.
6. **Integrate.** Run the Integration checkpoint above once all six seams
   have selected or explicitly deferred a shape.
7. **Review the whole vertical.** Independent review attacks the domain
   account, user-facing ordinary-fact projection, canonical semantics,
   authority, lifecycle, unsupported behavior, and production evidence
   together — this is in addition to, not a replacement for, each seam's own
   committee review.

## Deliverables

- `docs/domain-models/taxable-interest-translation.md`
- one `docs/prototypes/<seam-key>/plan.md` per chartered seam, with its
  Gate 0–8 record, rival branches (where run), and committee review notes
- source-independent canonical fact and relationship artifacts required by
  the selected seam shapes, using existing schemas or additive successors as
  evidence requires
- one structured ordinary-fact input projection and a reviewable
  plain-language rendering of the synthetic answer (Seam 6)
- adopted tax rule content deriving the bounded treatment (Seam 5)
- bounded integration with taxable interest and Form 1040 line 2b
- synthetic fixtures and tests for T1 through T9, both per-seam subsets and
  the full Integration run
- updated phase roadmap and phase state at close
- a short retrospective evaluating product value, the seam decomposition
  itself, and the tested cadence — including whether isolating seams
  actually made it possible to tell which choice caused which result,
  compared to the prior single-track attempt

Working comparison notes and prototypes are retained only when they remain
useful evidence. Final deliverables contain no review transcripts, role
metadata, session URLs, or execution diary.

## Verification

Each seam charter must name focused tests once its selected files and
consumers are known. Before Integration and before final handoff:

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

## Review gate

Each seam's own committee (clean-room, adversarial, eligibility, plus the
conditional implementation seat) closes that seam before its production
build begins. After Integration, have one fresh reviewer examine the exact
final candidate against the Product Model, fluid domain model, this plan,
primary tax authority, committed consumers, T1 through T9, and the complete
production diff. Repair substantive findings, then have the foreman retain
only useful abstractions and evidence, evaluate the seam-decomposition
cadence in the retrospective, and prepare the milestone for owner merge.

## Stop conditions

Stop for the owner when:

- two materially different shapes remain viable for the same seam after the
  smallest useful executable comparison and choosing one creates substantial
  migration or irreversible identity cost;
- the work turns on interpreting reserved governance doctrine;
- official authority does not support the selected treatment or exposes a
  materially different fact pattern;
- an honest implementation requires personal or non-synthetic data;
- a proposed input asks the user to supply a tax classification rather than
  an ordinary fact and no alternative projection is viable; or
- the lead cannot explain in plain language what additional work on a given
  seam would change.

Do not stop merely because a current contract is inconvenient, the domain
model broadens, implementation scope grows, or the plan did not predict a
useful supporting artifact. Make the value, cost, risk, and displaced-work
case under `OWNER_MODEL.md`, keep the change reviewable, and proceed when the
choice is reversible and aligned.

## Exit criteria

The milestone is complete when:

1. a useful fluid domain model explains the wider translation frontier and
   the selected slice in plain language without claiming contract or
   exhaustive status;
2. each of the six seams has either selected a shape with committee-reviewed
   evidence or recorded an explicit, owner-legible deferral;
3. the document contribution, ordinary-language contribution, canonical
   facts, tax classification, tax concept, and return projection remain
   recoverably distinct;
4. both input paths refer to shared source-independent identities and the
   implementation detects missing or ambiguous association;
5. the user is never required to enter an accrued-interest tax adjustment as
   the ordinary fact the product is supposed to derive;
6. T1 through T9 are instantiated and the applicable production cases
   execute through real contribution, derivation, and presentation consumers
   at Integration;
7. document and ordinary-fact corrections displace exactly the conclusions
   whose provenance depends on them;
8. the bounded result reaches taxable interest and line 2b without silently
   claiming full taxable-interest or neighboring-case coverage;
9. a fresh reader can recover what the source reported, what the person
   said, what rule translated it, what the product concluded, and what
   remains unsupported;
10. any new canonical shape has concrete positive instances, exact
    consumers, reviewed lifecycle behavior, and an explicit relationship to
    existing contracts; and
11. the retrospective states whether the seam decomposition let the owner
    attribute success or failure to a specific architectural choice, whether
    the map -> seam -> discriminate -> build -> integrate cadence produced
    enough value to repeat, and what should be simplified before the next
    milestone.
