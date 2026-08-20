<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Grammar Census",
  "topic": "grammar-census",
  "active_plan": "docs/phases/grammar-census/milestones/engine-language-map.md",
  "milestone_state": "track-0",
  "status": "Plan approved in direction by the owner 2026-08-19 and repaired the same day under a bounded planning repair. Objective unchanged: a reconciled, plain-language census of the declarative language the engine actually has — layers, constructs, sources of authority, runtime interpreters, observed committed use, and where schema, runtime, content, and behavior agree or diverge. Documentation-and-evidence only; no grammar change, ADR, implementation, or external comparative review. Owner approved the repaired plan 2026-08-19; Track 0 is chartered and in flight.",
  "current_role": "Track 0 Builder — term boundary and bounded corpus",
  "current_prompt": "docs/reviews/2026-08-19-grammar-census-track-0-boundary-corpus-builder-charter.md",
  "scope": [
    "bound the term 'engine grammar' against the engine's actual layers and record the boundary map as a required deliverable",
    "independently enumerate the declared (schema/contract), implemented (runtime), and observed-in-use (committed content and tests) construct sets",
    "reconcile those three sets in a separate adversarial track, where all set-difference claims are made",
    "produce a per-construct census, a small set of semantically contrastive end-to-end traces, and a tension catalog limited to potentially actionable items",
    "produce a bounded external-comparison brief that scopes a later comparative review without performing it",
    "report what language the engine has, the consequential agreements/mismatches/unknowns, census reliability, the strongest case against its conclusions, and bounded next-step choices"
  ],
  "non_goals": [
    "no grammar redesign, implementation, standards-conformance exercise, or ADR",
    "no production schema, rule-language, engine, runner, package, or tax-content change",
    "no exhaustive tax-coverage census",
    "no external comparative-semantics review — only the bounded brief that scopes one",
    "no use of unmerged claim-boundary CQ-2 work as evidence",
    "no PR opened or pushed until the owner explicitly directs it"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/grammar-census/milestones/engine-language-map.md#Objective",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Scope",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Non-goals",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Term boundary",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Evidence layers",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Census unit",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Deliverables",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Tracks",
      "docs/phases/grammar-census/milestones/engine-language-map.md#Parallel Work Manifest",
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
- Status: **TRACK 0 IN FLIGHT 2026-08-19.** Owner-approved after a bounded
  planning repair; Track 0 chartered at
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-corpus-builder-charter.md`.
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
constructs are observably used and how, and where schema, runtime, content,
and observed behavior agree or diverge.

The milestone is owner-selected explicitly and independently of Claim Boundary
Exploration. That phase's earlier "not triggered" notation described its own
opening milestone and is not a reason to decline this work.

The census is a prerequisite for any later grammar extension or comparison
with external declarative-rule systems, not that comparison itself.

## Scope

1. Establish and commit the **boundary map**: which of the engine's
   declarative and runtime surfaces are grammar proper, which are
   grammar-adjacent, and why (see `#Term boundary`).
2. Establish and commit the **bounded corpus**: for each evidence layer, the
   exact committed artifacts in scope, with the committed evidence for any
   current-selection claim, or an explicit statement that no canonical current
   selection exists and what bounded corpus is used instead.
3. Enumerate, independently and without cross-reading, three construct sets:
   **declared** (contracts and schema), **implemented** (runtime), and
   **observed in use** (committed content and tests). Each uses the
   `#Census unit` fields.
4. Reconcile the three sets in a separate adversarial track. **All
   declared-versus-implemented-versus-used set-difference claims are made
   here and only here.**
5. Build a small set of **representative traces** selected for semantic
   contrast, distinguishing executed evidence from static reading.
6. Build a **tension catalog** limited to entries with a stated plausible next
   action.
7. Produce a **plain-language synthesis** and a **bounded external-comparison
   brief** that scopes a later comparative review.
8. Report the closing assessment named in `#Exit criteria`.

## Non-goals

- No grammar redesign, implementation, standards-conformance exercise, or ADR.
- No production schema, rule-language, engine, runner, package, release,
  fixture-generation, or tax-content change.
- No exhaustive tax-coverage census. Stop expanding examples once an
  additional one would repeat an already-described construct.
- No external comparative-semantics review. The brief scopes one; it does not
  perform one, and it does not presume any external system is a model to
  adopt.
- No governance interpretation, adopted definition, or external-standards
  claim.
- No use of unmerged Claim Boundary Exploration CQ-2 work (on
  `milestone/declaration-request-claim-boundary-inquiry-cq2`) as evidence at
  any point.
- No personal, private, or real filer data.
- No PR opened or pushed until the owner explicitly directs it.

## Current state

The repository carries several plausibly-related but distinct declarative
surfaces accumulated across prior phases: rule-artifact schemas,
operation-semantics specifications, package and closure/binding rules, runners
and evaluators that interpret them, committed rule content in `packages/`, and
a test suite exercising some of it. No prior milestone has read these as one
reconciled object.

No committed artifact is known in advance to designate a single canonical
"current" grammar version across all layers — Claim Boundary Exploration found
this true for at least the core package. Track 0 establishes, for this census,
whether that also holds for schema and semantics artifacts, and defines an
explicit bounded corpus rather than assuming the highest-numbered file is
current.

## Term boundary

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

Reconcile these independently before synthesizing them; do not let one
layer's vocabulary stand in for another's:

1. Accepted contracts and ADR decisions (`docs/adr/`).
2. Every published rule-artifact and operation-semantics schema version
   relevant to the current engine.
3. Runtime evaluators, validators, resolvers, and other consumers that assign
   behavior to the declared forms.
4. Actual committed rule content and packages (`packages/`).
5. Tests and synthetic executions that demonstrate observable behavior.
6. Historical extensions (ADRs, retrospectives, roadmap entries) that explain
   how the present language accumulated.

Do not infer that the highest-numbered file is "current." Every
current-selection claim must cite the exact adoption, registry, package, or
other committed evidence for it. If no single canonical current selection
exists, report that plainly and define an explicit bounded corpus for the
census instead of guessing.

## Census unit

For every construct or construct family, record enough to answer:

- name and layer (per `#Term boundary`);
- accepted syntax or shape;
- source of authority (schema path and version, ADR, or other committed
  artifact);
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

A construct's `status` value is assigned in Track 2, not in Track 1, because
"unused" and "apparently unreachable" are set-difference judgments. Track 1
sub-tracks record only what their own layer shows and mark the field
`pending-reconciliation`.

A lightweight census tool may be committed if that is the smallest way to make
the inventory reproducible (for example, a script enumerating
schema-declared construct names, or construct-use counts across `packages/`).
It must not change production behavior, published schemas, or tax content, and
its output is evidence, not a claim on its own.

## Deliverables

Every working deliverable has a named path. All are under `docs/` except the
optional census tool.

| Track | Deliverable | Path |
| --- | --- | --- |
| 0 | Boundary map and bounded corpus | `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md` |
| 1a | Declared construct set | `docs/phases/grammar-census/inquiries/track-1a-declared-constructs.md` |
| 1b | Implemented construct set | `docs/phases/grammar-census/inquiries/track-1b-implemented-constructs.md` |
| 1c | Observed-usage construct set | `docs/phases/grammar-census/inquiries/track-1c-observed-usage.md` |
| 2 | Three-way reconciliation and set differences | `docs/phases/grammar-census/inquiries/track-2-reconciliation.md` |
| 2 | Representative traces | `docs/phases/grammar-census/inquiries/track-2-representative-traces.md` |
| 2 | Tension catalog | `docs/phases/grammar-census/inquiries/track-2-tension-catalog.md` |
| 3 | Plain-language engine language map | `docs/phases/grammar-census/inquiries/track-3-engine-language-map.md` |
| 3 | Bounded external-comparison brief | `docs/phases/grammar-census/inquiries/track-3-comparison-brief.md` |
| 3 | Milestone retrospective | `docs/milestone-retrospectives/<date>-grammar-census-engine-language-map.md` |
| any | Optional census tool (only if committed) | `tools/grammar_census.py` |

Plan, phase-state, overview, and roadmap updates land on their existing
paths. No other path is written by this milestone.

## Representative traces

A small set (roughly four to six) selected for **semantic contrast**, not tax
coverage — for example arithmetic composition, conditional applicability,
source-set closure and blocking, categorical reasoning, and a worksheet-like
computation. For each, show the path from declared content through validation
and evaluation to the resulting finding, block, nonpublication, or explanation
consequence, and clearly distinguish executed evidence (an actual runner
invocation or existing test) from static reading and inference. Stop adding
traces once an additional example would repeat an already-described construct.

## Tension catalog

Catalog only tensions that could plausibly support later action. Relevant
classes may include: schema/runtime/content disagreement; semantics
implemented in code but not represented in versioned content; declared
operations with no demonstrated use or execution; overlapping constructs
expressing similar ideas differently; tax-specific encodings that may conceal
a more general language need; distinctions collapsed by one layer but retained
by another; grammar choices that limit provenance or user explanation;
extension patterns that create growing complexity or ambiguity.

Do not assume these are defects. For each entry state the evidence, the
affected layer, the possible user or maintenance consequence, the remaining
uncertainty, and a plausible next action. Do not admit an entry merely to make
the catalog look complete.

## External comparison brief

Identify candidate comparison corpora (for example Catala, OpenFisca,
DMN/FEEL, Datalog/RIF, LegalRuleML, provenance standards, other
tax-computation systems) without presuming any is a model to adopt, and
without conducting the comparison. The brief states:

- which semantic dimensions are now worth comparing;
- which external systems appear relevant to each dimension;
- what questions a comparison could answer;
- what evidence would change an engine decision;
- which comparisons would be superficial or inapplicable.

## Claim-boundary evidence posture

Track 1 sub-tracks read the engine directly and are **independent of Claim
Boundary Exploration's conclusions**. They do not read that phase's inquiry
corpus.

Track 2 and Track 3 **may** use the merged CQ-1 artifacts on `origin/main`
under `docs/phases/claim-boundary-exploration/` as a **bounded validation
lens** — a cross-check on whether a census claim about provenance or
explanation consequence matches what that inquiry independently observed. It
is a lens, not authority: a CQ-1 statement never overrides this census's own
committed evidence, and any use is cited by path.

Unmerged CQ-2 work is out of bounds entirely.

## Contracts

Reads, but does not amend, `docs/adr/` and every rule-artifact and
operation-semantics schema version the census identifies as relevant. No new
contract is proposed.

## Fixtures

None created. The census reads existing committed rule content under
`packages/` and existing tests as evidence. Representative traces may exercise
existing committed synthetic fixtures, cited by path and not modified.

## Verification

Documentation-only. Completion evidence consists of:

- every material semantic claim citing a committed source (schema path and
  version, ADR, code location, package content, or test) or a synthetic
  execution actually run and shown;
- the three construct sets enumerated separately, in their own named
  deliverables, before reconciliation;
- a reconciliation deliverable that shows agreements, disagreements, and gaps
  explicitly;
- representative traces distinguishing executed evidence from static
  inference;
- a tension catalog whose every entry names a plausible next action;
- a final candidate diff whose changed paths are all under `docs/`, plus at
  most `tools/grammar_census.py` if the optional tool is committed;
- `python3 tools/governance_lint.py`;
- `python3 tools/foreman_context.py --ref HEAD --format markdown` succeeding;
  and
- CI `verify` on the final candidate as the gate of record.

## Data safety

Only committed repository artifacts (schemas, code, packages, tests, ADRs)
and public documentation of external systems may be used. No personal data,
real filer data, private workspace path, or non-public source is read or
produced. No stream touches personal or private data.

## Tracks

### Track 0 — Term boundary and bounded corpus

Deliverable: `docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md`

- Commit the boundary map (`#Term boundary`) as an artifact, not a framing
  paragraph: for each of the seven surfaces, whether it is grammar proper or
  grammar-adjacent, and the reason.
- For each evidence layer, identify the exact committed artifacts in scope and
  whether the repository carries any canonical "current" designation for that
  layer. Where none exists, define and record the explicit bounded corpus this
  census uses instead, with the reason it is defensible.
- **Representational gaps are recorded and the track continues.** If the
  corpus cannot represent a needed distinction without a code or contract
  change, record it as a tension-catalog candidate and proceed. Stop and
  report to the Foreman only if a trustworthy census cannot be produced at
  all from the available corpus.

### Track 1 — Independent parallel readings

Three readings run in parallel, isolated from one another's drafts until
Track 2 opens (see `#Parallel Work Manifest`). Each shares only the Track 0
packet and this plan. Each produces its own census-unit records using the
`#Census unit` fields, with `status` left `pending-reconciliation`.

- **Track 1a — Contracts and schema.** Deliverable
  `track-1a-declared-constructs.md`. Read `docs/adr/` and every relevant
  rule-artifact and operation-semantics schema version in the Track 0 corpus.
  Produce the **declared** construct set: name, layer, accepted syntax,
  source of authority, whether separately versioned, and declared
  evaluation/blocking/invalidity/nonpublication behavior where the contract
  states it.
- **Track 1b — Runtime.** Deliverable `track-1b-implemented-constructs.md`.
  Read the evaluators, validators, resolvers, and other runtime consumers.
  Produce the **implemented** construct set: which forms the runtime actually
  interprets, what each interpretation does, its evaluation, blocking,
  invalidity, and nonpublication behavior, what provenance survives it, and
  any runtime behavior carrying semantic weight that it cannot locate in a
  schema.
- **Track 1c — Content and tests.** Deliverable
  `track-1c-observed-usage.md`. Read committed rule content under `packages/`
  and the test suite. Produce the **observed usage** set only: which
  constructs actually appear, representative citations by path, frequency
  context, and which behaviors are demonstrated by an existing test or a
  synthetic execution it ran. **Track 1c reports observation only.** It makes
  no claim that a construct is unused, unreachable, undeclared, or
  unimplemented, and it does not compare its findings against the schema or
  the runtime — every such set difference belongs to Track 2.

### Track 2 — Adversarial reconciliation and traces

Deliverables: `track-2-reconciliation.md`, `track-2-representative-traces.md`,
`track-2-tension-catalog.md`

- Compare the three Track 1 construct sets. Record every agreement,
  disagreement, and gap explicitly; do not silently prefer one layer's
  account. **This is the only track that makes declared-versus-implemented-
  versus-used set-difference claims**, including assigning each construct's
  final `status`.
- Build the representative-trace set (`#Representative traces`) from the
  reconciled census.
- Build the tension catalog (`#Tension catalog`) from the reconciliation, not
  from Track 1 impressions alone, folding in any Track 0 representational-gap
  records that survive as actionable.
- May use merged CQ-1 artifacts as a bounded validation lens per
  `#Claim-boundary evidence posture`.

### Track 3 — Synthesis, comparison brief, and report

Deliverables: `track-3-engine-language-map.md`,
`track-3-comparison-brief.md`, and the milestone retrospective.

- Produce the reconciled, casual-but-technically-invested-reader account of
  the engine-language boundary and its major layers.
- Produce the bounded external-comparison brief (`#External comparison
  brief`).
- Assess the exit criteria and report: what language the engine actually has;
  the most consequential agreements, mismatches, and unknowns; whether the
  census is sufficiently reliable to close; the strongest case against its
  conclusions; and the bounded choices for what follows (comparative review, a
  focused grammar decision or build, further internal verification, or stop).
- The phase remains open after this milestone; Track 3 selects nothing.

## Parallel Work Manifest

Milestone:
- Engine Language Map (`grammar-census`)

Workstreams:
- Track 1a — declared construct set (contracts and schema reading)
- Track 1b — implemented construct set (runtime reading)
- Track 1c — observed-usage construct set (content and test reading)

All three share the milestone's primary branch
`milestone/grammar-census-engine-language-map` and primary worktree
`engine-worktree-2`. No temporary branch is used; the isolation exception is
not invoked.

Dependencies fulfilled:
- Track 0's boundary map and bounded corpus are committed before any Track 1
  stream is chartered. No Track 1 stream begins against an undefined corpus.

Dependencies pending:
- Track 2 depends on all three Track 1 deliverables being committed.
- Track 3 depends on Track 2.
- No Track 1 stream depends on another Track 1 stream.

Constraints — non-overlapping output paths:
- Track 1a writes only
  `docs/phases/grammar-census/inquiries/track-1a-declared-constructs.md`.
- Track 1b writes only
  `docs/phases/grammar-census/inquiries/track-1b-implemented-constructs.md`.
- Track 1c writes only
  `docs/phases/grammar-census/inquiries/track-1c-observed-usage.md`.
- No stream edits `docs/phase-state.md`, the milestone plan, the phase
  overview or roadmap, another stream's deliverable, or any Track 0, 2, or 3
  deliverable. The Foreman owns those paths.
- No stream changes production code, schemas, packages, tests, fixtures, or
  tax content. Every stream is read-only against `packages/`,
  `tools/` (except the optional census tool), and the test suite.
- If a stream believes the optional census tool is warranted, it proposes it
  to the Foreman rather than committing `tools/grammar_census.py` itself;
  the Foreman assigns single ownership of that path.

Conflict hotspots:
- `docs/phase-state.md` — Foreman-owned; a stream that edits it collides with
  every other stream and with the lifecycle pointer.
- `docs/phases/grammar-census/milestones/engine-language-map.md` —
  Foreman-owned.
- `tools/grammar_census.py` — single-owner if it exists at all.
- The shared Git index in `engine-worktree-2`. Every stream acquires the
  worktree commit lock per `docs/process/concurrent-work.md` before staging,
  stages only its own named deliverable path, inspects
  `git diff --cached --name-only`, and releases the lock after committing.

Draft independence:
- Until all three Track 1 deliverables are committed, no stream reads another
  stream's deliverable, draft, or commit message, and no stream is given
  another stream's findings in its charter or context capsule.
- Streams do not read Claim Boundary Exploration inquiry artifacts at all.
- The Foreman does not relay one stream's findings to another during Track 1,
  including as a "clarification." A question that can only be answered by
  another stream's layer is recorded as an open question in the asking
  stream's deliverable and resolved in Track 2.
- Independence ends when the third Track 1 deliverable is committed. Track 2
  reads all three.

Integration order:
1. Track 0 boundary map and bounded corpus.
2. Tracks 1a, 1b, and 1c in any completion order — they are mutually
   independent and their commits do not need to be sequenced relative to one
   another.
3. Track 2 reconciliation, traces, and tension catalog.
4. Track 3 synthesis, comparison brief, and retrospective.

Sync points:
- Each Track 1 stream rebases onto or resets to the branch head carrying
  Track 0 before beginning, and reconfirms `git status --short` before staging
  because a sibling stream may have committed in the interim.
- Track 2 begins only from a branch head containing all three Track 1
  commits.

Verification per stream:
- Each stream cites every material claim to a committed path (and version
  where the artifact is versioned) or to a synthetic execution it actually ran
  and shows.
- Each stream's diff touches only its own named deliverable path:
  `git diff --name-only <track-0-head>..HEAD` names exactly one file.
- `python3 tools/governance_lint.py` before handoff.

Integration verification:
- `python3 tools/governance_lint.py`.
- `python3 tools/foreman_context.py --ref HEAD --format markdown` succeeds.
- `python3 tools/build_orientation_block.py` succeeds for the pointed-at role.
- Final candidate diff paths all under `docs/`, plus at most
  `tools/grammar_census.py`.
- CI `verify` on the final candidate as the gate of record.

Data safety:
- No stream reads or writes personal, private, or real filer data.
- No stream commits a local absolute workstation path.
- Only committed synthetic repository artifacts and public external
  documentation are used.

## Track 0 adversarial closure

Not applicable. Track 0 does not settle contributed authority, aggregate or
absence declarations, claim reuse, or a neighboring integration contract. It
bounds a reading corpus for an exploratory documentation census and makes no
implementation-ready decision.

## Exit criteria

The milestone is complete when:

1. a casual but technically invested reader can understand the
   engine-language boundary and its major layers from the synthesis alone;
2. the declared, implemented, and observed-in-use construct sets are
   separately enumerated in their own deliverables and then reconciled;
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
Completion closes this milestone only. **The Grammar Census phase remains
open**, and the next milestone within it is unselected and owner-held.
