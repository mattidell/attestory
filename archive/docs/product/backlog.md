# Working Backlog

Status: working checklist, not binding. Owner: Matt. Captured 2026-07-04
from the product-development guidance thread. Items are grouped by area;
checkboxes are open work, ✅ is done, ⊘ is superseded. Prune freely.

Critical path: B1 → B2 → C3 (accept ADR-0001, write ADR-0002, implement the
facts model) unblocks most of C and E. The doc family (A) proceeds in
parallel. F1 is independent and time-sensitive. E2 is the one to protect
time for — it is the only pure product-design practice item on the list.

## A. Product Document Family

- ✅ Product thesis: one page, ordinary words, frozen.
- [ ] Vision doc restructure: ontology (belief structure) on top → principles,
  each with a *because* (up to the ontology) and a *forecloses* (down to
  designs) → anti-goals → aspects → traces. Candidate opening: "they model
  your return; we model your evidence."
- [ ] Conceptual model doc (~1 page, not a glossary): placement rulings
  (fact, return, optionally truth) / semantic concepts defined relationally /
  realization mappings to artifacts. One status sentence: informative, not
  binding; where this doc and an artifact disagree, the artifact wins.
- [ ] Story doc: the ordinary-words → terms-of-art migration as memoir.
  Subsumes the prototype retrospective. Scenes: the wizard midpoint, checking
  a number before trusting it, where the California bridge surprised you,
  what you would refuse to give up if main replaced the prototype tomorrow.
- [ ] Commit the doc family when it settles; decide the fate of untracked
  `PRODUCT_PROJECT_NOTES.md`.
- ⊘ Competitive teardown of TurboTax — superseded by the story doc.
- ⊘ Standalone prototype retrospective — merged into the story doc.

## B. Decisions and ADRs

- [ ] Review ADR-0001 (contribution/run split): check the Consequences
  negatives for completeness and the deferred third alternative (contribution
  payload vs separate contribution manifest); flip to accepted; commit.
- [ ] Backfill ADR-0002: facts-model reintroduction. First solo ADR
  composition. Scope includes the product-boundary layer disposition: keep
  workspace, run, and draft-revision as canon nouns; dissolve or demote
  re-presentations.
- [ ] Future ADR: views as canon nouns (view definitions and instances;
  "views select, filter, group, rename, aggregate — pipelines compute").
  Deferred until the demo surface needs its first projection.
- [ ] F3 disposition: `ProductRunSummary` result-counts purpose line is view
  territory; one-line data edit, lands together with the two summary edges
  (`FieldResolution → ProductRunSummary`, `ReturnInstance → ProductRunSummary`).
- [ ] Resolve the 4 remaining `review_note` edges in `artifact-graph.json`.
  All four reduce to one question: do consumers read definition artifacts
  directly, or only through the traces that applied them?
- [ ] F6 leftovers: where input validation lives; confirm overrides are facts
  with `provenance kind: user_override`; note the California bridge as
  `CrossFormBridge`'s cross-jurisdiction test case.
- [ ] Method authority / justifiable accounting conventions (design hook now,
  features deferred): the engine already applies conventions wherever law
  under-determines a method — currently unlabeled and indistinguishable from
  prescribed rules. Reserve authority provenance in the computation-definition
  layer when `ComputationSpecCatalog` is designed: authority enum (prescribed /
  elected / delegated / conventional / asserted) + optional basis reference,
  flowing into `ComputationTrace`. Elections and asserted positions are facts
  (user decisions with provenance) — no model change needed. Labels replace
  disclaimer footnotes structurally; "show convention-dependent values" becomes
  a view. Deferred: conventions corpus, pre-production highlighting, separate
  app. Also: short scope-boundary doc (system labels authority, never selects
  among methods; positions are the user's); "convention/position" as a
  conceptual-model placement ruling; "is this the right way?" added to the
  ordinary-words inventory. Domain precedent: ASC 740 uncertain tax positions,
  IRS Form 8275 disclosure. Input-layer pattern (duplex allocation exemplar):
  the evidenced/decision/derived fact triple — monolithic evidenced fact
  (1098), allocation decision fact (delegated authority, Pub. 527 "any
  reasonable method"), derived facts with provenance to both; all three enter
  via one contribution event; derived facts are legitimate return inputs.
  Open fork (flag, don't settle): derivation at contribution time (start
  here) vs generic allocation computation parameterized by decision facts
  (promote if decisions churn) — provenance shape identical either way.
  Coverage extension: missing decision facts surface as blocked inputs
  ("decisions as coverage") — the non-wizard mechanism for offloaded choices.
  Scope correction (2026-07-05): the system does not enumerate delegation
  points or detect pre-derived fact entry — no preemptive boundary warnings.
  Claim is fidelity, not omniscience: bare manual entries carry told-by-you
  provenance (never dressed as evidence); supersession retrofits bare facts
  into triples later. Two convention audiences: user conventions live in the
  fact layer; computation-layer authority labels disclose engine-author
  interpretations where instructions are ambiguous (vendors genuinely diverge
  on e.g. state-refund taxability edge cases). Refinement (2026-07-05):
  material interpretations hoist into the fact layer as proposal-and-blessing
  — the system derives a good-faith default fact (method-referenced, e.g.
  prior-year benefit amount derived from the workspace prior return), and the
  user's decision is the blessing (review state → accepted). "The system
  proposes, you sign." Cross-year derivations (depreciation roll-forward,
  carryovers, refund benefit) follow the same pattern with prior returns as
  evidence sources — in-system prior years yield multi-year provenance
  continuity. Granularity limit: only material, contestable interpretations
  hoist (else wizard-by-ledger); trivial readings stay in code with thin spec
  labels. Boundary surfaces via coverage and return metadata counting inputs
  by authority class (evidenced / blessed default / asserted / election).
- [ ] Schema evolution policy (ADR candidate): artifacts are evidence and are
  never migrated in place; lift-on-read as default (one loader per artifact
  type owns all historical versions), derivation with provenance links for
  heavy cases; accretive changes as the mechanical default rule, breaking
  changes require a declared compatibility method in the milestone plan;
  enforcement via retained per-version golden fixtures. The compatibility
  clock starts at the first non-regenerable artifact (the dogfood run) —
  before that, schemas break freely and fixtures regenerate. Tools comply by
  construction if the lift loader is the only sanctioned reader; projection
  consumers sit outside the treaty under view contracts.

## C. Engineering and Mechanization

- [ ] Engine-level fitness functions, two or three to start:
  provenance-completeness walk (every return field back-reachable to facts),
  no-literal-thresholds lint (thresholds come from parameter artifacts),
  pipeline purity (stages read artifacts, not each other's internals).
  Graph-level checks exist; engine-level do not.
- [ ] Maturity matrix: aspects × domain coverage. Becomes the
  milestone-selection frontier. Second reading: each row is an ordinary word
  being operationalized.
- [ ] First frontier cell: facts-model implementation milestone, specced as
  an artifact-fidelity spec, parity-checked against the `prototype` branch.
  Full rehearsal of the invariant-driven method.
- [ ] First hard tax case: Schedule B $1,500 conditional-form-requirement as
  a trace slice — a rule type neither prototype has.
- [ ] Port-one-domain cadence when tax scope expands: prototype
  `definitions/computation/*.json` as the source, parity as verification.

## D. Process and Agent Workflow

- [ ] Encode the tiered decision protocol (Tier 1/2/3) into
  PROJECT_PLANNING/AGENTS, including a "Decisions for the user" section
  (max ~3 Tier-3 items) in milestone plans.
- [ ] Brief header template: 10-line decision summary atop agent briefs —
  what shipped, decisions by tier, questions pending, next default action.
- [ ] Consolidated decision log for the follow-up points scattered across
  agent-comments briefs (~50 orphaned items).
- [ ] Collapse approval gates for low-risk milestones: approve plan +
  pre-authorize completion-on-green; keep two gates only for milestones
  carrying Tier-3 decisions.
- [ ] Jurisprudence Phase-1 vectors (optional, adopt at will): a citation
  comment on every mechanical check; a "principles touched" clause in plans;
  the "defensible but arbitrary" sensation treated as an escalation trigger.
  Review and commit the explorations set itself when it has earned it.

## E. Product Forward Moves

- [ ] Demo surface choice — made by Matt, before the milestone starts.
  Recommendation on record: thin local web app; port the prototype viewer
  shape (`ui/return-view.js` against the new service layer).
- [ ] Sketch the run review screen. Every visible number answers "where did
  this come from?" in one click. The story doc's information architecture,
  with buttons. Hand this to agents rather than letting read models dictate
  the UI.
- [ ] Ordinary-words inventory: the frontier list of frustrations awaiting
  terms of art — "what changed since last run" (nearly there), "I don't
  trust this yet" (partial), "conflict" (partial), and "ready to file"
  (no term of art exists; highest-stakes gap).
- [ ] Plan the dogfood moment: real 2025 facts through main's engine under
  ignored `local-data/`, parity against the prototype's output. Candidate
  exit criterion for the phase after the demo surface.

## F. Safety

- [ ] Prototype-branch data strategy — the only time-sensitive item. Family
  tax documents live in the `prototype` branch's git history. Before any
  remote or shareable-portfolio step: decide separate repo vs
  `git filter-repo` excision, and write the decision into the data safety
  rules.
