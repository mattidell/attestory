<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Grammar Census",
  "topic": "grammar-census",
  "active_plan": "docs/phases/grammar-census/milestones/engine-language-map.md",
  "milestone_state": "planned",
  "current_role": "Foreman — planned; no track started",
  "current_prompt": "docs/phases/grammar-census/milestones/engine-language-map.md#Tracks",
  "scope": [
    "bound the term 'engine grammar' against the engine's actual layers and record the boundary map as a required result",
    "independently enumerate declared (schema/contract), implemented (runtime), and used (committed content) construct sets, then reconcile them",
    "produce a per-construct census, a small set of semantically contrastive end-to-end traces, and a tension catalog limited to potentially actionable items",
    "produce a bounded external-comparison brief that scopes a later comparative review without adopting a model to imitate",
    "report a plain-language account of what language the engine has, the most consequential agreements/mismatches/unknowns, reliability of the census, the strongest case against its conclusions, and bounded next-step choices"
  ],
  "non_goals": [
    "no grammar redesign, implementation, standards-conformance exercise, or ADR",
    "no production schema, rule-language, engine, or tax-content change",
    "no exhaustive tax-coverage census — stop expansion once an example repeats an already-described construct",
    "no full comparative-semantics review against external systems — only a bounded brief that scopes one",
    "no PR opened or pushed until the owner explicitly directs it"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/grammar-census/milestones/engine-language-map.md#Objective",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Scope",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Term boundary",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Evidence layers",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Census unit",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Tracks",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Data safety",
      "docs/adr/INDEX.md"
    ],
    "new_milestone": [
      "docs/phases/grammar-census/grammar-census-overview.md",
      "docs/phases/grammar-census/grammar-census-roadmap.md"
    ]
  }
}
-->

# Milestone: Engine Language Map

- Phase: Grammar Census
- Milestone key: `grammar-census`
- Status: **PLANNED 2026-08-19.** No track started.
- Base: `origin/main` at `20cf03ab` (merge of PR #181,
  `milestone/claim-boundary-exploration-phase-definition`)
- Branch: `milestone/grammar-census-engine-language-map`
- Primary worktree: `engine-worktree-2`
- Decision posture: exploratory, documentation-and-evidence only; no ADR is
  produced

## Objective

Produce a trustworthy, reconciled, plain-language account of the declarative
language the engine actually has today — its layers, its constructs, where
each construct's meaning is declared, validated, executed, and tested, which
constructs are actually used and how, and where schema, runtime, content, and
observed behavior agree or diverge. The milestone is owner-selected now,
explicitly and independently of Claim Boundary Exploration's earlier "not
triggered" notation, which described that milestone's opening scope only.

The census is a prerequisite for any later grammar extension or comparison
with external declarative-rule systems (Catala, OpenFisca, DMN/FEEL,
Datalog/RIF, LegalRuleML, etc.), not that comparison itself.

## Current state

The repository carries several plausibly-related but distinct declarative
surfaces accumulated across prior phases (Foundation, Engine Breadth, and
others): rule-artifact schemas, operation-semantics specifications, package
and closure/binding rules, runners and evaluators that interpret them,
committed rule content in `packages/`, and a test suite exercising some of it.
No prior milestone has read these as one reconciled object. Track 0 of Claim
Boundary Exploration and its successors read a narrow slice (the line-2b
support chain) for a different purpose; this milestone does not inherit or
depend on that reading.

No committed artifact is known in advance to designate a single canonical
"current" grammar version across all layers — Claim Boundary Exploration found
this true for at least the core package. Track 0 here establishes, for this
census, whether that also holds for schema and semantics artifacts, and
defines an explicit bounded corpus rather than assuming the highest-numbered
file is current.

## Term boundary — what counts as "grammar"

Do not treat every JSON artifact in the repository as one undifferentiated
grammar. The census must establish and preserve distinctions among at least:

1. the core rule-artifact clause and expression language;
2. dependency, guard, applicability, value, publication, and blocking
   semantics;
3. operation-specific semantic specifications;
4. package selection, binding, closure, and output-ownership rules that
   constrain execution;
5. adjacent declarative predicate or validation languages;
6. runtime behaviors that affect the meaning of a rule but may not themselves
   be grammar;
7. provenance, disposition, and explanation consequences produced by
   execution.

The resulting boundary map — which of these are grammar proper, which are
grammar-adjacent, and why — is itself a required deliverable, not a framing
paragraph to be discarded once cataloguing starts.

## Evidence layers

Reconcile these independently before synthesizing them; do not let one layer's
vocabulary stand in for another's:

1. Accepted contracts and ADR decisions (`docs/adr/`).
2. Every published rule-artifact and operation-semantics schema version
   relevant to the current engine.
3. Runtime evaluators, validators, resolvers, and other consumers that assign
   behavior to the declared forms.
4. Actual committed rule content and packages (`packages/`).
5. Tests and synthetic executions that demonstrate observable behavior.
6. Historical extensions (ADRs, retrospectives, roadmap entries) that explain
   how the present language accumulated.

Do not infer that the highest-numbered file is "current." Every current-
selection claim must cite the exact adoption, registry, package, or other
committed evidence for it. If no single canonical current selection exists,
report that plainly and define an explicit bounded corpus for the census
instead of guessing.

## Census unit

For every construct or construct family, record enough to answer:

- name and layer (per the term boundary above);
- accepted syntax or shape;
- source of authority (schema path, ADR, or other committed artifact);
- the runtime consumer that interprets it;
- semantic effect;
- input and output types or domains;
- evaluation, blocking, invalidity, and nonpublication behavior;
- whether its semantics are separately versioned;
- representative committed uses (citations, not paraphrase);
- status: active, legacy-only, unused, apparently unreachable, or uncertain;
- what provenance or explanation information survives its execution;
- nearby inferences the evidence does not support.

Frequency is useful context but not a substitute for importance — a rare
construct may carry a fundamental semantic distinction and must be recorded
even if it appears once.

A lightweight, committed census tool may be used to make the inventory
reproducible if that is the smallest way to raise confidence (e.g., a script
that enumerates schema-declared construct names, or grep-based construct-use
counts across `packages/`). It must not change production behavior, published
schemas, or tax content, and its output is evidence, not a claim on its own.

## Representative traces

A small set (roughly four to six) of end-to-end traces selected for
**semantic contrast**, not tax-coverage breadth — e.g., arithmetic
composition, conditional applicability, source-set closure and blocking,
categorical reasoning, and a worksheet-like computation. For each trace, show
the path from declared content through validation and evaluation to the
resulting finding, block, nonpublication, or explanation consequence, and
clearly distinguish executed evidence (an actual runner invocation or existing
test) from static reading and inference. Stop adding traces once an additional
example would repeat an already-described construct.

## Tension catalog

Catalog only tensions that could plausibly support later action. Relevant
classes may include: schema/runtime/content disagreement; semantics
implemented in code but not represented in versioned content; declared
operations with no demonstrated use or execution; overlapping constructs
expressing similar ideas differently; tax-specific encodings that may conceal
a more general language need; distinctions collapsed by one layer but
retained by another; grammar choices that limit provenance or user
explanation; extension patterns that create growing complexity or ambiguity.

Do not assume these are defects. For each entry, state the evidence, the
affected layer, the possible user or maintenance consequence, the remaining
uncertainty, and a plausible next action. Do not admit an entry merely to make
the catalog look complete.

## External comparison brief (bounded, not the review itself)

Identify candidate comparison corpora (Catala, OpenFisca, DMN/FEEL,
Datalog/RIF, LegalRuleML, provenance standards, other tax-computation
systems) without presuming any is a model to adopt. The brief states:

- which semantic dimensions are now worth comparing;
- which external systems appear relevant to each dimension;
- what questions a comparison could answer;
- what evidence would change an engine decision;
- which comparisons would be superficial or inapplicable.

## Contracts

Reads, but does not amend, `docs/adr/` and every rule-artifact / operation-
semantics schema version the census identifies as relevant. No new contract
is proposed by this milestone.

## Fixtures

None created. The census reads existing committed rule content under
`packages/` and existing tests as evidence; representative traces may exercise
existing synthetic fixtures already committed for other milestones, cited by
path, not modified.

## Verification

Documentation-only. Completion evidence consists of:

- every material semantic claim in the census citing a committed source
  (schema path + version, ADR, code location, package content, or test) or a
  synthetic execution actually run and shown;
- the declared, implemented, and used construct sets enumerated separately
  before reconciliation, with the reconciliation showing where they agree and
  diverge;
- representative traces distinguishing executed evidence from static
  inference;
- the tension catalog containing only entries with a stated plausible next
  action;
- a final candidate diff whose changed paths are all under `docs/` (plus any
  committed lightweight census tool, kept out of production code paths);
- `python3 tools/governance_lint.py`; and
- CI `verify` on the final candidate as the gate of record.

## Data safety

Only committed repository artifacts (schemas, code, packages, tests, ADRs)
and public documentation of external systems (Catala, OpenFisca, DMN/FEEL,
etc.) may be used. No personal data, real filer data, or non-public source is
read or produced.

## Tracks

### Track 0 — Term boundary and bounded corpus

- Establish the boundary map (Term boundary section above) as a committed
  artifact, not a framing paragraph.
- Identify, for each evidence layer, the exact committed artifacts that are
  in scope, and whether the repository has any single canonical "current"
  designation per layer. Where none exists, define and record the explicit
  bounded corpus this census uses instead.
- Stop and report if the fixture/corpus cannot represent a needed distinction
  without a code or contract change; record that as a tension-catalog entry
  rather than expanding the milestone.

### Track 1 — Independent parallel readings

Three independent readings, isolated from each other's drafts until Track 2,
sharing only the Track 0 packet:

- **Track 1a — Contracts and schema.** Read `docs/adr/` and every relevant
  rule-artifact / operation-semantics schema version. Produce the declared
  construct set: name, layer, accepted syntax, source of authority, whether
  separately versioned.
- **Track 1b — Runtime.** Read the evaluators, validators, resolvers, and
  other runtime consumers. Produce the implemented construct set: which
  declared forms are actually interpreted, what each interpretation does,
  evaluation/blocking/invalidity/nonpublication behavior, and any runtime
  behavior that carries semantic weight without a schema counterpart.
- **Track 1c — Content and tests.** Read committed rule content under
  `packages/` and the test suite. Produce the used construct set: which
  constructs actually appear, representative citations, frequency context,
  and which declared or implemented constructs have no demonstrated use.

Each sub-track produces its own census-unit records per construct, using the
Census unit fields above, without attempting reconciliation.

### Track 2 — Adversarial reconciliation and traces

- Compare the three Track 1 construct sets. Record every agreement,
  disagreement, and gap explicitly — do not silently prefer one layer's
  account.
- Build the representative-trace set (Representative traces section above)
  from the reconciled census.
- Build the tension catalog (Tension catalog section above) from the
  reconciliation, not from Track 1 impressions alone.

### Track 3 — Plain-language synthesis, comparison brief, and report

- Produce the reconciled, casual-but-technically-invested-reader account of
  the engine-language boundary and its major layers.
- Produce the bounded external-comparison brief.
- Assess the exit criteria below and report: what language the engine
  actually has; the most consequential agreements, mismatches, and unknowns;
  whether the census is sufficiently reliable to close; the strongest case
  against its conclusions; and the bounded choices for what follows
  (comparative review, a focused grammar decision/build, further internal
  verification, or stop).

## Track 0 adversarial closure

Not applicable. Track 0 does not settle contributed authority, aggregate or
absence declarations, claim reuse, or a neighboring integration contract. It
bounds a reading corpus for an exploratory documentation census and makes no
implementation-ready decision.

## Exit criteria

The milestone is complete when:

1. a casual but technically invested reader can understand the engine-language
   boundary and its major layers from the synthesis alone;
2. the declared, implemented, and used construct sets are separately
   enumerated and reconciled;
3. every material semantic claim cites a committed source or a synthetic
   execution actually run and shown;
4. material disagreements and unknowns remain visible in the reconciliation
   rather than being normalized away;
5. representative traces connect syntax to observable consequences, with
   executed evidence distinguished from static reading;
6. the tension catalog contains only entries with a stated plausible next
   action;
7. a follow-on comparative review can be scoped from the comparison brief's
   explicit questions rather than a generic survey of other languages; and
8. the result makes no grammar change, product contract, ADR, governance
   interpretation, or external-standards claim.

No exit criterion requires finding a flaw or recommending a redesign.
