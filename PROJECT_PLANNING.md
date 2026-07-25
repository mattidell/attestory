# Project Planning

## Audience

Project documentation serves three distinct audiences: Product, Agent, and Shared.

Product-facing documentation is for readers making product, portfolio, or sequencing decisions. It emphasizes product direction, capability, sequencing, and why the work matters.

Agent-targeted documentation is for implementation work. It contains the operational detail needed to change the project safely: file paths, constraints, verification commands, dependency notes, track sequencing, and guardrails.

Shared documentation is planning context that connects reader-friendly project intent to enough implementation precision for safe execution.

## Overview

This document defines how planning works in this repository. It keeps product direction, implementation planning, and execution guardrails separate so each decision is made at the right level.

Product intent and phase direction are inputs to planning. The agent owns translating that direction into explicit planning documents, preserving data safety, identifying contract dependencies, determining readiness from the planning requirements, making atomic implementation changes, and verifying the result.

Planning should make the next implementation step obvious before code changes begin. Phase documents describe where the project is going. Roadmaps describe the milestone sequence and status. Milestone plans describe the tracks, contracts, fixtures, and verification needed to implement safely.

## Development Posture

Audience: Shared

The project is early. The owner's stated posture, which planning and execution should assume:

- **Iteration over meticulous upfront planning.** Work is treated as prototype-grade until proven otherwise. Backtracking and repeating work is an acceptable — often preferred — alternative to exhaustive up-front design. The goal of the project is to refine taste, design, and governance iteratively; discarded work that sharpened a decision was not wasted.
- **Merge does not imply endorsement.** Work lands on `main` that the owner or a later agent may judge undesired, unsatisfactory, or simply pointed in a direction no longer wanted. That is an expected outcome, not a failure. Reviews of merged work are normal and recorded under `docs/reviews/`.
- **Snapshot and reset, not open-ended branches.** The owner does not want many worktrees or long-lived branches open at once. When merged work is deemed undesired, the remedy is: snapshot the current state (a `snapshot/<date>-<topic>` branch or tag at the abandoned tip), then reset `main` to an earlier commit and proceed. History is preserved in snapshots; `main` tells the current story. Resets of `main` are owner-directed; agents perform them only on direction, and never without creating the snapshot ref first.
- **Multiple agents collaborate.** Sessions get interrupted and resumed by different agents. Hand-offs are disclosed in retrospectives; interrupted work is either committed, snapshotted, or cleanly discarded — not left as ambient worktree state.

This posture coexists with the milestone protocol below: planning discipline governs how work is built; the posture governs how finished work is judged and, when necessary, unwound.

## Prototype-Driven Decisions

Audience: Shared

Consequential decisions are made from evidence, not intention. A Tier 3 ADR, or a Tier 2 ADR that fixes a contract future content or surfaces will be authored against (a *contract-foundational* decision), must cite a **prototype evaluation analysis** as evidence. An ADR whose central design element is a placeholder is not ready to propose. Exceptions (trivially reversible decisions, or decisions forced by an external constraint) must say so in the ADR.

**Authorization.** Agents are pre-authorized to build prototypes before proposing such ADRs. Prototyping is the expected first move when a consequential contract is undesigned — do not ask permission to start one.

**The loop.** Each prototype iteration runs:

1. **Charter** — declare the questions this iteration must answer and the fixtures or edge cases in scope. Fixture selection is itself reviewed: the charter names the classes of case the design must survive, drawn from real content and prior-iteration lessons.
2. **Build** — implement on a prototype branch.
3. **Examine** — record the contracts that emerged and the implementation results against the charter's questions.
4. **Committee review** — multiple reviewers with distinct charters (see below).
5. **Disposition** — enumerate the questions that remain; decide whether to iterate (new charter: more fixtures, edge cases, or a rival design) or to conclude.
6. Repeat until the reviewers agree the evidence suffices. Then write the **prototype evaluation analysis** — what was built, what questions were asked and answered, what evidence supports each conclusion, what dissent remains — and only then draft the ADR, citing it.

**Committee.** At least two reviewers besides the builder, with distinct review charters — for example: contract fidelity against the governance set; implementation results and expressiveness against the charter's fixtures; fresh-reader legibility (can a reader recover the meaning from the artifact alone?). The owner's disposition closes each round. Dissent is recorded in the round's review notes, never resolved by wordsmithing; unresolved dissent is cited in the ADR.

**Reviewer dispatch.** Every reviewer dispatch requires the owner's immediate,
explicit approval for the current topic, role, and charter (ADR-0034). Owner
approval of a prototype plan names eligible seats and tiers only; it is never
standing launch authority. Once approved, the foreman launches reviewers at the
plan-assigned tier in isolated contexts and records the direction before launch;
reviewers do not see each other's in-progress work. Prototype legibility review
is a normal reviewer charter, while the starved fresh-reader rigor lives in the
periodic owner-spawned **Legibility Audit** (`docs/legibility-audits/`).

**Reviews are measurements.** A review charter must define what it measures and what failure looks like before reviewing begins, and its notes must report falsifiable results — a scored recovery attempt, a fixture the design failed, a contract clause it violates, or an explicit attestation that a defined check was run and found nothing. "Reviewed, looks good" is not a valid review. The owner audits by sampling: one review per round examined for whether its measurements are real, rather than reading everything.

**Role separation.** Builder, reviewers, and foreman are distinct agents or fresh contexts. The builder never reviews their own iteration. The foreman (the agent leading the effort: chartering, sequencing, recommending dispositions) never serves as a committee reviewer of work produced under their own charter — the foreman reviews the process, not the artifacts.

**Rivals, not refinements.** Before the committee may conclude, the evidence must include at least one rival design exercised on the same fixture charter — a genuinely different shape, not a parameter tweak of the first attempt. A design that has only ever competed against its own earlier drafts has not been tested. If the analysis concludes without a rival, it must argue explicitly why comparison was unnecessary, and that argument is itself subject to committee dissent.

**Termination.** Every iteration opens with declared questions. An iteration that resolves no new questions forces a stop-and-decide. Default cap: three iterations before an owner check-in. The owner may kill the effort at any disposition point; a killed prototype is snapshotted like any other abandoned work.

**Artifacts.** `docs/prototypes/<topic>/` holds charters, iteration examinations, committee review notes, and the final evaluation analysis — these merge to `main`. Prototype code lives on a branch named `prototypes/<topic>/it<N>` only while its iteration is active; prototype code never merges to `main`. When an iteration concludes, the foreman tags its tip as `exhibits/<topic>/it<N>` and deletes the branch ref: the commits are preserved permanently and cited by tag, and the branch list holds only the actively-building iteration. Exhibit tags are never deleted or moved.

**Traceability.** Every conclusion in the evaluation analysis cites a specific exhibit — a drafted artifact at a path on a named prototype branch, a recorded test result, a review note. A conclusion the reader cannot follow to its exhibit is not evidence and does not support an ADR. The same rule flows downstream: the ADR cites the analysis, the analysis cites exhibits, and a break anywhere in that chain is grounds to send the ADR back.

**Plain-language ADR analysis.** Every new or materially revised ADR has a
separate, non-normative companion at `docs/adr/analyses/<adr-number>-<slug>.md`,
linked near the top of the ADR. It explains what changes, why it is needed, what
it enables or protects, and what it does not do, without duplicating the
normative contract. The ADR governs on any conflict. Historical ADRs are not
backfilled solely for this protocol; create a companion when one is materially
revisited.

**Process evaluation.** The process itself is under evaluation while it runs, not only in the retrospective. The foreman maintains a dated **process log** (`docs/prototypes/<topic>/process-log.md`), written as incidents happen — never reconstructed afterward — against declared incident categories: hollow measurements, context leaks, no-progress iterations, charter drift, wordsmithed dissent, role breaches, and foreman errors. The foreman's participant review is **conformance review only** (did the reviewer run its charter's checks; did roles stay separated), never a second judgment on artifact findings — quality belongs to the committee. Owner check-ins at disposition points have a fixed shape: evidence status against the charter, process incidents since the last check-in, and a recommendation; the owner then sample-audits one review. The retrospective treats the process — foreman included — as a subject, and material lessons amend the process by superseding ADR.

### Prototype Economic Gates

Audience: Shared

The first prototype run (Tax Citizen Families, First Tax Slice Track 0) was consequential but uneconomical: it combined several distinct Tier 2 decisions and used production-path integration as the acceptance standard for all of them, so review thoroughness became unbounded scope growth. The gates below (ratified by ADR-0013, extending ADR-0005) exist to pay for the cheapest evidence capable of changing the decision, then stop. They are not advisory: each is instantiated in the prototype plan and enforced by the foreman.

- **Gate 0 — Decision inventory.** The plan lists every independent proposition that could become an ADR sentence. One prototype topic carries at most one primary proposition plus at most two tightly dependent secondaries; the rest are split into their own scored entries or deferred. Propositions carry ids that charters, budgets, and exit criteria reference.
- **Gate 1 — Eligibility score.** Each proposition scores 0–2 on four axes: future blast radius, migration cost, residual uncertainty after paper examples, and inability to test cheaply during implementation. 0–3 implement normally (retrospective or Tier 1 record); 4–5 paper spike plus ADR draft; 6–8 prototype-eligible. Tier 2/3 status alone does not authorize the most expensive evidence — contract-foundational reach plus unresolved uncertainty does.
- **Gate 2 — Paper instantiation (first rung).** Before any code, per primary proposition: two positive instances, two meaningful negatives, one lifecycle trace, and a producer → authority → consumer → failure map. If paper distinguishes the alternatives, stop at paper. If paper exposes a missing production substrate, route that substrate as a separate patch or decision before domain prototyping — do not absorb it into the charter. This is the prototype-side twin of the Payload Instantiation Gate.
- **Gate 3 — Evidence ladder.** Four rungs: (1) static schema/content examples; (2) resolver/validator mutations; (3) throwaway evaluator; (4) persisted end-to-end integration. The plan names the currently authorized rung and the single open question that alone would justify climbing. Climb one rung at a time; never demand rung 4 for every citizen shape in one charter.
- **Per-question progression.** Iteration scope and evidence depth are separate:
  one bounded iteration may carry several related propositions, while each
  proposition advances only to the cheapest evidence level that answers its own
  question. Reviews report proposition-by-proposition sufficiency and dissent;
  they never issue one monolithic pass/fail merely because questions shared an
  iteration.
- **Gate 4 — Fixed caps and session-bounded cost review.** There is no cost-ratio trigger; session usage is already bounded, so a session boundary is the natural point to review the shape of cost incurred and still to come. Fixed caps apply and each forces stop-and-decide when crossed, never automatic charter expansion: two builder iterations including one rival; one owner-authorized repair pass; two default reviewers, a third only for a named uncertainty; and context-starved legibility only when recoverability is itself a decision. **Builder and review documents have no line or Markdown-length cap.** Their cost is bounded by the pre-declared scope, cases, evidence rung, and measurement charter; authors stop when those obligations are completely reported, not when a file reaches an economic target. Rival iterations are clean-room. A repair pass is named `repair<N>`, not as another iteration, and defaults to the original incumbent builder for deliberate defect continuity unless the disposition explicitly assigns a different builder.
- **Gate 5 — Review triage (foreman-owned).** Every finding is classified before another iteration may open: `decision-blocking`, `production-condition`, `separate-decision`, `deferred-breadth`, or `non-blocking defect`. The foreman performs this triage and is accountable for it. Only a `decision-blocking` finding, and only after the owner ratifies the amendment, may enlarge the active charter. Production conditions go to the milestone plan; separate decisions get their own Gate 1 score; breadth and non-blocking defects are logged and deferred. A review measures and may recommend an action, but does not enlarge scope: the foreman rejects or reroutes any proposed action that exceeds the charter and records the disposition in the process log.
- **Gate 6 — Partial ratification.** An evaluation analysis may accept a coherent converged subset and explicitly defer the rest; ADR scope matches the evidence that actually converged. Do not hold a prototype open until every adjacent boundary is solved.
- **Gate 7 — Production adoption.** Prototype code never becomes a production candidate by effort or similarity (see Artifacts and Traceability above). Accepted contracts are reimplemented on the milestone branch; prototype code is cited and selectively translated only after each piece maps to an accepted ADR statement and a production test.
- **Gate 8 — Role capability budget.** Reasoning capability is a priced input, so the plan assigns each role a capability tier and reasoning effort matched to the role's difficulty and the current evidence rung — not defaulted to maximum. A novel-synthesis builder needs a high tier; an imitation or repair build does not. Fresh-reader legibility review is *more faithful* at a lower tier, because a strong model reconstructs the missing meaning the test is meant to expose — there a lower tier is a better measurement, not merely a saving.

**The prototype plan.** An owner-approved, committed `docs/prototypes/<topic>/plan.md` precedes the first charter of any prototype topic — it is to the prototype process what the milestone plan is to implementation, and it is reviewed by the owner alone (not the committee). Its sections discharge the gates explicitly: decision inventory (Gate 0); eligibility scores (Gate 1); paper-evidence plan with an "if paper suffices, stop here" line (Gate 2); currently authorized evidence rung (Gate 3); fixed caps (Gate 4); triage rules naming the foreman as owner (Gate 5); minimum acceptable converged subset (Gate 6); the role and capability plan with abstract tiers per role including the foreman (Gate 8); and the production-adoption boundary (Gate 7).

**Role capability tiers.** Prototype plans use the abstract tier names High / Medium / Economy so they do not rot as models release. The named-model example map below binds each tier to current models across families; it is illustrative as of mid-July 2026 and is refreshed as families ship — the tier semantics, not the roster, are load-bearing. A role calls for a tier, and any family's model at that tier satisfies it.

| Tier | Anthropic | ChatGPT (OpenAI) | Gemini (Google) | Grok (xAI) | Open source |
|---|---|---|---|---|---|
| High | Opus 4.8, Fable 5 | GPT-5.6 Sol, o3-pro | Gemini 3.1 Pro, Gemini 3 Pro Deep Think | Grok 4.5 | GLM-5.2, DeepSeek V4 (Pro/large), Llama 4 (large) |
| Medium | Sonnet 5 | GPT-5.6 Terra, o4-mini | Gemini 3.5 Flash, Gemini 3.1 Flash | Grok 4 (variants) | Qwen3 / Qwen 3.5–3.6 (e.g. 72B/35B), Mistral Large 3 |
| Economy | Haiku 4.5 | GPT-5.6 Luna | Gemini 3.1 Flash-Lite | Grok 3/4 mini | Llama 3.1/4 smaller, Ministral, Gemma 4 smaller, Qwen smaller variants |

Default starting guidance: Foreman High/high (judgment-dense, low build volume); novel-synthesis Builder High/high; imitation or repair Builder Medium/medium; contract-fidelity and adversary Reviewers High/high; expressiveness Reviewer Medium–High/medium; starved legibility Reviewer Economy–Medium/low–medium.

**Foreman as scope-and-economy steward.** Beyond chartering, sequencing, conformance review, and disposition recommendations, the foreman is the accountable steward of scope and economy. The foreman: (1) keeps the implementation — including reviews and the actions reviews propose — inside the declared scope boundaries and the spirit of economic efficiency, triaging findings (Gate 5) and rejecting or rerouting out-of-charter proposals rather than expanding scope; (2) enforces the evidence ladder and paper-first rule, never authorizing a more expensive rung than the open question requires; (3) tracks the fixed caps and triggers stop-and-decide rather than letting a run drift; (4) assigns each role's capability tier and reasoning effort in the plan and revises them as the run progresses — as decision boundaries and specifications clarify, the required capability for the next dispatch usually drops, and each change and its rationale is logged at dispatch time; and (5) obtains the owner's immediate, explicit approval before dispatching **any** role, including committee reviewers (ADR-0034; see Reviewer dispatch above). These are stewardship duties, not authority over artifact quality: the foreman still never reviews artifact quality, overrules a committee finding on the merits, or resolves dissent by rewording it.

**Mechanical work (no helper seat).** The clerical work of the prototype process — maintaining the `SEAT.md` table, assembling round files, tagging exhibits and deleting branch refs, log-hygiene formatting, confirming each cited exhibit tag exists, running data-safety scans on merged documents, collating the fixed-shape disposition packet, applying status or wording edits — is the foreman's own, and the foreman is accountable for all of it. ADR-0045 retired the clerk seat: a spawned mechanical helper costs a cold-agent boot on top of the foreman turns spent spawning and receiving, which is strictly more expensive than the foreman doing it inline. Do it inline when it is small; write a tool when it recurs or its output is bulky enough to pollute the foreman thread. None of this work may involve judgment — triaging findings, recommending a disposition, assigning capability tiers, changing scope, composing what a status line means, reviewing artifact quality, or ratifying anything remain foreman or committee acts regardless of how they are executed.

### Foreman context routing

Audience: Agents

A routine foreman resume begins by rendering
`tools/foreman_context.py --ref <explicit-ref>`. The output is an advisory,
provenance-bearing capsule: it reads only one committed ref, names the source
blobs that supplied its state, reports worktree drift separately, and refuses
missing, malformed, or contradictory re-entry metadata. It is never a second
authority. `AGENTS.md`, accepted ADRs, governance, role seeds, milestone plans,
and charters control on any conflict; a capsule omission never grants an
exception.

The capsule routes the foreman to the complete documents required for the
proposed action. Before dispatch, ADR drafting, schema/fixture work,
merge/records work, or any other mapped action, read those sources in full and
follow their existing gates. Before **planning a new milestone**, read up to the
five most recent milestone retrospectives, newest first, even when the capsule
already names them. That historical read is a planning prerequisite, not a
wholesale requirement for resuming an already planned or executing milestone.
If the capsule refuses, read the named committed sources directly, reconcile the
selected ref, and do not work around the refusal with a prose summary.

**External builder handoff.** When a builder is intentionally resumed in an
owner-controlled context, the foreman first makes the repository state
self-describing: `SEAT.md` binds the seat to its role, charter, branch, and
worktree; the charter carries scope and stop conditions; and the role carries
the completion contract. The foreman's handoff message ends with exactly
`ready for builder prompt?`. If the owner answers affirmatively, the foreman's
next response contains only the builder prompt. The prompt points through the
repository entry chain and asks the builder to echo its understood scope, rung
ceiling, and stop conditions before writing. It does not duplicate the charter.

### Builder and reviewer context capsules

Audience: Agents

The foreman prepares a compact **Context Capsule** in every new builder or
review charter. It names the source ref and resolved launch commit, exact
object/range, role, scope, evidence-rung ceiling where applicable, stop
conditions, and complete deep reads. A builder or reviewer uses it to orient,
verifies the ref against Git, then reads the controlling charter and cited
sources. The capsule is part of the charter's routing surface only: it never
widens scope or replaces exact text.

The Trusted Advisor is owner-launched strategic counsel and is outside this
operational-capsule rule. There is no clerk seat and no Clerk Task Capsule
(ADR-0045); mechanical work is one foreman turn, or a tool when it recurs or
its output is bulky.

The current role and prompt are not a separate document. They live in the
`foreman-context-v1` block at the top of `docs/foreman-handoff.md`, which
`tools/foreman_context.py` and `tools/build_orientation_block.py` read from a
resolved ref. The foreman keeps `current_role` and `current_prompt` accurate:
before a plan or role cycle is marked complete, it prepares the next sequential
role's charter and updates those fields. Prompt preparation records plan
sequence; it does not launch or dispatch a role.

Dispatch authorization is normed in `AGENTS.md` ("Dispatch authorization") and
is not restated here.

Charters use this compact shape:

```md
## Context Capsule

- Source ref and resolved launch commit:
- Exact object or commit range:
- Role:
- Scope and evidence-rung ceiling (if applicable):
- Stop conditions:
- Full reads before acting:
```

**Log hygiene during open rounds.** Process-log entries and commit messages for landed same-round reviews are event-only while the round is open; outcome summaries are written only at round close.

**Foreman succession.** If the foreman seat is vacant and an agent takes it, it records a dated succession entry in the topic's `process-log.md` before proceeding.

## Canonical Meta Documents

Canonical project implementation meta documents live at the repository root and use all-caps filenames.

Examples:
- `README.md`: project entry point and current usage.
- `PROJECT_PLANNING.md`: planning process and document lifecycle.
- `AGENTS.md`: development conventions, guardrails, and agent operating instructions.
- `CHANGELOG.md`: consumer-facing capability history, when introduced.

These documents should be stable references for contributors and agents. They should not be tied to one milestone unless the file name explicitly says so.

## Planning Structure

Planning is organized around phases, milestones, and tracks.

Product direction and priorities set the planning context. The agent turns that context into structured planning, identifies implementation dependencies, and keeps execution aligned with the committed plan.

### Phases

Phases describe major periods of project development. A phase explains where the project is headed, what capabilities matter most during that period, and what evidence shows the project is ready to move to the next phase.

Each phase has an overview and a roadmap. The overview describes the phase purpose, scope, and exit criteria. The roadmap describes the milestone sequence, current status, lessons learned, and how each milestone changes the project.

Phase documents capture product intent and desired direction. The agent maintains the phase documents so they match the current project state and give future implementation work a clear boundary.

### Milestones

Milestones are bounded product or architecture capabilities inside a phase. A milestone describes what becomes true for the project, why that capability matters, and how it fits into the surrounding sequence.

Milestones replace informal track groups. They make progress easier to evaluate because each one has a concrete outcome, a clear relationship to the phase roadmap, and a defined point at which the project can reassess direction.

Milestone documents state the capability value and sequencing rationale. The agent translates the milestone into executable planning, including contracts, fixtures, verification, and track-level implementation steps.

### Tracks

Tracks are the implementation steps inside a milestone. A track is small enough to reason about independently and specific enough to verify when complete.

Tracks give the agent a practical execution unit while keeping milestone-level progress visible. Track boundaries make implementation easier to verify and keep commits aligned with the plan.

## Process

Audience: Shared

Planning precedes implementation.

Documentation should preserve the distinction between audience and instruction. Product-facing sections describe product direction and capability; they do not tell the reader how to perform implementation work. Agent-targeted sections carry instructions, constraints, commands, and guardrails. Shared sections may include structured scope and exit criteria when that detail is necessary to align product intent with implementation boundaries.

The default sequence is:
1. Create or update the relevant planning document.
2. Commit planning changes separately.
3. Create or switch to a dedicated milestone execution branch from the committed planning state.
4. Implement one atomic track.
5. Run verification for that track.
6. Commit the completed track before starting the next track.
7. Repeat track implementation, verification, and commit until milestone work is complete.
8. Complete the milestone branch using the milestone completion protocol.
9. Update status, roadmap notes, or consumer-facing docs when behavior changes.

If planning changes during implementation, separate the planning update from code changes whenever possible. Follow-up planning clarifications before implementation should usually be squashed into the relevant planning commit to keep planning history clean. Do not squash implementation commits into planning commits.

### Milestone Execution Branch Protocol

Audience: Agents

Milestone implementation happens on a separate milestone execution branch. Do not implement milestone tracks directly on `main`.

Before creating the milestone execution branch:
- Commit the milestone planning changes separately from implementation work.
- Ensure the milestone plan has the required contents and is committed.

Before implementing the first track:
- Create a dedicated branch for the milestone from the committed planning state, normally based on `main`, unless the milestone plan specifies another base.
- Use a branch name that clearly identifies the milestone.
- Confirm the milestone execution branch includes the committed planning state but does not include uncommitted planning changes.

During milestone execution:
- Implement one track at a time unless the milestone plan explicitly groups tracks.
- Run the verification named for the track before committing it.
- Create one implementation commit per completed track.
- Do not combine all milestone implementation work into one final commit.
- Keep planning changes, if any are needed during execution, separate from implementation commits whenever possible.
- Do not merge the milestone branch to `main` until all planned tracks are complete and verified.

When all tracks are complete, the milestone branch history should show a distinct commit for each completed track, unless the milestone plan explicitly specified a grouped track commit before implementation. The agent records the branch, track commits, verification performed, and any residual risks in the appropriate status or completion note, then completes the milestone.

Milestone completion requires completed tracks, passing required verification, and a branch history that matches the milestone plan. To complete the milestone:
- Switch to `main`.
- Update `main` from the expected upstream if one is configured.
- Confirm the milestone branch contains the expected per-track commits rather than a single combined milestone implementation commit.
- Merge the milestone execution branch into `main` using a non-fast-forward merge commit.
- Put the milestone name in the merge commit message.
- Run the required integration verification after the merge.
- Report the merge commit and verification result.

Do not squash, rebase away, or collapse the per-track implementation commits during milestone completion unless the milestone plan explicitly requires that history shape.

### Document Layout

Specific planning documents live under `docs/` and use lower-case kebab-case filenames.

Phase documents live under a phase-specific directory:

```text
docs/phases/
  engine-contract-stabilization/
    engine-contract-stabilization-overview.md
    engine-contract-stabilization-roadmap.md
    milestones/
      return-artifact-evaluation.md
```

Each phase should have two phase-level documents:
- `<phase-name>-overview.md`: product-facing phase purpose and shared scope.
- `<phase-name>-roadmap.md`: product-facing milestone roadmap followed by roadmap status and implementation notes.

The roadmap document is the canonical phase state document for that phase. It should contain the active milestone, milestone status, implementation notes, pivots, lessons learned, and impacted project areas.

Milestone plans live under the relevant phase's `milestones/` directory. A milestone plan is the execution planning document for one bounded milestone and should include that milestone's tracks.

Roadmaps are milestone-level product documents. Each roadmap item should explain what capability is delivered, why it matters, and why it is sequenced where it is. Detailed track plans belong in milestone plans, not roadmaps.

Roadmaps should be relatively static. If a roadmap item changes after initial planning, annotate that item with `(updated: YYYY-MM-DD)` and explain the change in the status section.

## Required Milestone Plan Contents

Before starting a new milestone, create or update a planning document with:
- Objective: the capability the milestone proves.
- Current state: what already exists and what assumptions are stable.
- Scope: what will be implemented.
- Non-goals: what must not be included yet.
- Contracts: schemas, artifacts, definitions, runners, or APIs expected to exist.
- Fixtures: synthetic scenarios used to validate behavior.
- Verification: tests, golden files, and runner commands required for completion.
- Data safety: how personal documents and personal data remain excluded.
- Exit criteria: the exact definition of done.
- Tracks: the atomic implementation tracks that make up the milestone.

Milestone planning should happen before implementation and before creating the milestone execution branch. If the plan changes during implementation, update the plan in a separate commit or clearly separate the planning change from code changes.

Planning commits are mandatory. Initial plan generation must be committed before the milestone execution branch begins implementation. A planning document is ready for execution when it contains the required milestone-plan contents and is committed separately from implementation.

## Track Planning Checklist

Before implementing a track, identify:
- Goal: one sentence describing the behavior or contract being added.
- Boundary: what the track will not do.
- Inputs: schemas, fixtures, runners, or artifacts consumed.
- Outputs: files, schemas, artifacts, runner behavior, or docs changed.
- Verification: the exact test or command proving the change.
- Migration risk: whether existing artifact shapes or golden fixtures change.
- Data safety: whether any local, private, or generated data path is touched.
- Payload instantiation: if the track commits a schema that carries or references a payload, one hand-written, fully-resolved instance of that payload, committed alongside the schema as its positive example, before the schema is committed. A payload specified only by reference to another citizen is not yet instantiated.

## Payload Instantiation Gate

A schema that names another citizen as its payload — a `$ref`, "carries a finding," "wraps an act" — has deferred a modeling decision, not made one. The deferral stays invisible until something must *produce* the payload, often several tracks later in runner code, at which point discovering a bad fit costs a half-built runner instead of a paper example. This gate pulls that discovery left, to the cheapest point.

Discharge the gate by instantiation, not inspection: write the payload out as concrete data, filling every required field of every referenced type with an honest value, and **commit the instance alongside the schema as its positive example** — the counterpart of the negative examples schemas already ship with. An uncommitted instance is an unauditable gate: a reviewer cannot distinguish a discharged gate from a claimed one, and checks here leave evidence. The committed instance does triple duty: gate evidence, documentation for a fresh reader, and a seed fixture for the track's tests.

Resolution is bounded, not endless: expand references until you reach a contract that already has a committed positive instance, then *cite* that instance rather than re-expanding it. The gate's cost is one layer of new modeling per track, by construction.

Two failure modes then surface immediately and for free:
- Invariant collision: a referenced type requires a field the new producer cannot supply honestly — a machine output forced to name a human `basis`, say. The instance cannot be written without lying.
- Reserved-boundary contact: filling a field honestly would require constructing doctrine the project has reserved. The instance cannot be written without improvising.

Either failure is now a planning-time signal that the track needs its own decision — usually a Tier 2/3 ADR — before code depends on the contract. Motivating incident: ADR-0009 (derived-finding shape) was forced during runner implementation because `act-derived-publication.v1` was committed referencing the kernel `finding.v1` with no worked derived-finding instance; a single hand-written instance would have hit the missing, un-suppliable `basis` at track-planning time, and the ADR would have been written and ratified before the runner was attempted.

The gate binds any track whose outputs include a schema. It does not bind tracks that only add code, tests, or fixtures against contracts already instantiated by an earlier track.

## Parallel Work Rules

Parallel work is allowed, but only when dependencies and constraints are explicit before execution.

The project is contract-heavy. Parallel tracks are safe when they do not compete over the same schemas, artifact shapes, runner outputs, definitions, or golden fixtures. Parallel tracks are risky when they both change integration surfaces or when one track consumes an artifact contract that another track has not stabilized.

Parallelization levels:
- Safe parallel: unrelated docs, tests, isolated fixtures, isolated renderers, or data safety checks.
- Conditional parallel: producer and consumer work where the producer contract is already stable or a temporary fixture contract is explicitly declared.
- Unsafe parallel: concurrent changes to the same schema, artifact shape, canonical runner output, definition file, or golden fixture directory.

Before parallel work begins, create or update the relevant milestone plan with a parallel work manifest. A parallel work manifest belongs only in a milestone planning document under the phase's `milestones/` directory, not in phase overviews or roadmaps.

Do not add a parallel work manifest by default. Add it only when parallel execution is part of the milestone plan.

The manifest must include:
- Milestone: the milestone the parallel work belongs to.
- Branches or workstreams: each parallel branch or stream and its owner if applicable.
- Dependencies fulfilled: the contracts, fixtures, or prior tracks already completed.
- Dependencies pending: any workstream whose implementation or merge depends on another workstream.
- Constraints: files, schemas, artifacts, or behavior that must not change in each stream.
- Conflict hotspots: files or directories likely to conflict.
- Merge order: the dependency-first order in which work should be merged.
- Rebase points: when downstream branches must rebase onto producer branches.
- Verification per stream: tests or commands required for each stream.
- Integration verification: tests or commands required after the streams are merged.
- Data safety notes: statement that no stream touches personal or private data.

Template:

```md
## Parallel Work Manifest

Milestone:
- Return Artifact Evaluation

Workstreams:
- Track 19 return artifact contract
- Track 22 return artifact renderer using a static sample fixture
- Documentation update for prototype transition

Dependencies fulfilled:
- Field resolution schema and workspace artifact are stable.

Dependencies pending:
- Track 20 generation depends on the Track 19 schema merge.
- Golden return fixtures depend on the Track 20 generation merge.

Constraints:
- Do not change `field-resolution.json` shape.
- Do not update existing golden workspace artifacts outside the assigned stream.

Conflict hotspots:
- `packages/schemas/*`
- `packages/tax_engine/tax_workspace_runs.py`
- `packages/tax_engine/runners/run_tax_workspace.py`
- `packages/sample_data/workspaces/*/expected/*`
- `README.md`
- active milestone planning docs

Merge order:
1. Merge return artifact contract.
2. Rebase generation work on the merged contract.
3. Merge generation.
4. Rebase golden fixture and renderer work.
5. Merge fixtures and renderer.

Verification per stream:
- Run focused unit tests for changed modules.
- Run relevant runner subprocess tests.

Integration verification:
- Run `python3 -m unittest`.
- Run the canonical workspace runner.

Data safety:
- Only synthetic fixtures may be committed.
- No local absolute paths may be added to golden fixtures or manifests.
```

Parallel work should merge in dependency order, not completion order. A branch finishing first is not a reason to merge first if another unmerged branch defines the contract it consumes.

Golden fixture updates require single-owner coordination. Do not update the same expected artifact from multiple branches unless the manifest explicitly defines the merge order and regeneration authority.

## Roadmap Rules

Roadmaps should be coarse-grained and milestone-oriented.

Each roadmap starts with the planned roadmap. The roadmap itself should use only product-facing language and describe the milestone sequence, delivered capability, why the milestone matters, and why it is sequenced where it is.

After the roadmap, include a status section. The status section should include each milestone, implementation notes, pivots, lessons learned, active milestone state, and the part of the project impacted, such as CLIs, runners, workspace workflows, schemas, fixtures, UI, API, persistence, or architecture boundaries.

Roadmaps should not duplicate detailed track plans. If a roadmap item needs execution detail, create or update a milestone plan under that phase's `milestones/` directory.

## Planning Maintenance

Planning should be checked for currency at milestone boundaries and before any transition to a new project phase.

Maintenance checks:
- Does the current plan still describe what the code does?
- Are obsolete assumptions marked obsolete or archived?
- Are active plans still actionable?
- Are planned artifacts reflected in schemas, fixtures, tests, and runner docs?
- Are personal-data guardrails still explicit?

If any check fails, update planning before continuing implementation.

### Periodic Legibility Audit

At phase boundaries, and after any milestone that introduces a new citizen family or contract vocabulary, the owner should consider running a **Legibility Audit** (`docs/legibility-audits/`): an owner-spawned, context-starved fresh reader attempts declared recovery tasks against a curated artifact slice, testing whether the shipped system's numbers explain themselves from the artifacts alone. It is a project-level fitness function for the auditability thesis, distinct from the per-iteration prototype legibility review; its findings are advisory and feed the backlog. Launch prompt: `docs/legibility-audits/audit-prompt.md`.

## Archive Rules

Do not silently overwrite planning documents that represent a completed or superseded phase.

When a plan becomes obsolete:
- Move a copy to `docs/archive/`.
- Use a dated folder or filename.
- Add a short note explaining why it was archived.
- Keep the active replacement plan in the expected active location when appropriate.

Archived plans are historical context. Active plans should describe current direction.

## Changelog Rules

The project may keep two kinds of changelog-like documents:
- Internal changelogs in `docs/` can include implementation history and technical sequencing.
- A root `CHANGELOG.md`, when introduced, should be consumer-facing and should not list commit hashes.

Consumer-facing changelog entries should describe capabilities:
- Added synthetic workspace execution.
- Added field resolution artifact.
- Added return artifact inspection.

They should not describe low-level commit mechanics unless relevant to readers or integrators.

## Data Safety Rules

Planning and implementation must preserve the shareable nature of the project.

Committed files must not include:
- Personal tax documents.
- Personal current-year fact instances.
- Personal manual entries.
- Prior returns.
- Uploaded private documents.
- Generated artifacts derived from personal data.
- Absolute local machine paths in committed fixtures.

Synthetic fixtures must be clearly synthetic and must remain safe to publish.

## Transition Discipline

Moving between phases requires an explicit plan update.

The transition should define:
- The phase being exited.
- The next phase being entered.
- The artifacts that prove the old phase is complete.
- The contracts that future app, API, or persistence work may depend on.
- The new verification baseline.

Product surfaces should wrap stable contracts rather than define them implicitly.
