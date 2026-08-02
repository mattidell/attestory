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
- **Merge does not imply permanent endorsement.** A completed milestone may
  later prove undesirable or point in a direction the owner no longer wants.
  That is an expected outcome, not a process failure. Development remains
  provisional on the milestone branch; `main` carries the curated milestone
  state the owner chose to publish.
- **Snapshot and reset, not open-ended branches.** The owner does not want many worktrees or long-lived branches open at once. When merged work is deemed undesired, the remedy is: snapshot the current state (a `snapshot/<date>-<topic>` branch or tag at the abandoned tip), then reset `main` to an earlier commit and proceed. History is preserved in snapshots; `main` tells the current story. Resets of `main` are owner-directed; agents perform them only on direction, and never without creating the snapshot ref first.
- **Multiple agents collaborate.** Sessions get interrupted and resumed by different agents. Hand-offs are disclosed in retrospectives; interrupted work is either committed, snapshotted, or cleanly discarded — not left as ambient worktree state.

This posture coexists with the milestone protocol below: planning discipline governs how work is built; the posture governs how finished work is judged and, when necessary, unwound.

## Prototype-Driven Decisions

Audience: Shared

Consequential decisions are made from evidence, not intention. A Tier 3 ADR, or a Tier 2 ADR that fixes a contract future content or surfaces will be authored against (a *contract-foundational* decision), must **cite its evidence** — the exhibits, review notes, and recorded results the decision rests on. An ADR whose central design element is a placeholder is not ready to propose. Exceptions (trivially reversible decisions, or decisions forced by an external constraint) must say so in the ADR.

**Standing permission.** Agents need no approval to build prototypes before proposing such ADRs. Prototyping is the expected first move when a consequential contract is undesigned — do not ask permission to start one.

**The loop.** Each prototype iteration runs:

1. **Charter** — declare the questions this iteration must answer and the fixtures or edge cases in scope. Fixture selection is itself reviewed: the charter names the classes of case the design must survive, drawn from real content and prior-iteration lessons.
2. **Build** — implement on a prototype branch.
3. **Examine** — record the contracts that emerged and the implementation results against the charter's questions.
4. **Committee review** — multiple reviewers with distinct charters (see below).
5. **Disposition** — enumerate the questions that remain; decide whether to iterate (new charter: more fixtures, edge cases, or a rival design) or to conclude.
6. Repeat until the reviewers agree the evidence suffices, then draft the ADR against the evidence.

**The evaluation analysis is conditional.** A separate
`docs/prototypes/<topic>/evaluation-analysis.md` — what was built, what
questions were asked and answered, what evidence supports each conclusion, what
dissent remains — is **required only when the evidence did not converge in one
clean round**. Write one when any of these holds:

- the topic ran more than one build-and-review round;
- a rival changed the shape of the answer rather than confirming it;
- dissent is unresolved at the close.

Otherwise there is nothing for an analysis to reconcile, and writing one only
restates the round: the ADR cites the charter, the exhibit tag, and the review
notes directly, and no analysis file exists. The foreman decides this at the
closing disposition and records which branch applied.

**Committee.** At least two reviewers besides the builder, with distinct review charters — for example: contract fidelity against the governance set; implementation results and expressiveness against the charter's fixtures; fresh-reader legibility (can a reader recover the meaning from the artifact alone?). The owner's disposition closes each round. Dissent is recorded in the round's review notes, never resolved by wordsmithing; unresolved dissent is cited in the ADR.

**Reviewer launch.** Committee reviewers launch like any other role: the
foreman charters them and runs them at the plan-assigned tier in isolated
contexts, recording the direction before launch, and reviewers do not see each
other's in-progress work. Whether the foreman spawns them or the owner launches
them is the spawn question in `AGENTS.md` ("Dispatch authorization"), not a
precondition on the review happening. Prototype legibility review
is a normal reviewer charter, while the starved fresh-reader rigor lives in the
periodic owner-spawned **Legibility Audit** (`docs/legibility-audits/`).

**Reviews are measurements.** A review charter must define what it measures and what failure looks like before reviewing begins, and its notes must report falsifiable results — a scored recovery attempt, a fixture the design failed, a contract clause it violates, or an explicit attestation that a defined check was run and found nothing. "Reviewed, looks good" is not a valid review. The owner audits by sampling: one review per round examined for whether its measurements are real, rather than reading everything.

**Role separation.** Builder, reviewers, and foreman are distinct agents or fresh contexts. The builder never reviews their own iteration. The foreman (the agent leading the effort: chartering, sequencing, recommending dispositions) never serves as a committee reviewer of work produced under their own charter — the foreman reviews the process, not the artifacts.

**Rivals, not refinements.** Before the committee may conclude, the evidence must include at least one rival design exercised on the same fixture charter — a genuinely different shape, not a parameter tweak of the first attempt. A design that has only ever competed against its own earlier drafts has not been tested. If the analysis concludes without a rival, it must argue explicitly why comparison was unnecessary, and that argument is itself subject to committee dissent.

**Termination.** Every iteration opens with declared questions. An iteration that resolves no new questions forces a stop-and-decide. Default cap: three iterations before an owner check-in. The owner may kill the effort at any disposition point; a killed prototype is snapshotted like any other abandoned work.

**Artifacts.** While a topic is active, `docs/prototypes/<topic>/` holds its
working charter, examinations, committee notes, and any required evaluation
analysis on the milestone branch. Prototype code lives on a branch named
`prototypes/<topic>/it<N>` only while its iteration is active; prototype code
never enters the milestone merge. When an iteration concludes, the foreman
tags its tip as `exhibits/<topic>/it<N>` and deletes the branch ref. At
milestone close, the ADR retains the material decision and evidence summary;
the closed working set moves to the dated archive and does not remain mixed
with active prototype work. Exhibit tags are landmarks, not active authority.

**Traceability.** Every conclusion cites a specific exhibit — a drafted artifact at a path on a named prototype branch, a recorded test result, a review note. A conclusion the reader cannot follow to its exhibit is not evidence and does not support an ADR. The chain is the ADR to its evidence, and — where an evaluation analysis exists — through the analysis to the exhibits it cites. A break anywhere in that chain is grounds to send the ADR back.

**Process evaluation.** The process itself is evaluated while it runs. The
foreman keeps a working process log on the milestone branch for material
incidents: hollow measurements, context leaks, no-progress iterations, charter
drift, wordsmithed dissent, role breaches, and foreman errors. The log is an
input to closeout, not automatically a permanent artifact. The retrospective
retains incidents that changed scope, evidence, risk, or reusable practice;
routine routing and mechanical recovery disappear with the working record.
The foreman's participant review is conformance-only; artifact quality belongs
to the committee. Material lessons amend the process document that norms them,
not an ADR.

### Prototype Economic Gates

Audience: Shared

The first prototype run (Tax Citizen Families, First Tax Slice Track 0) was consequential but uneconomical: it combined several distinct Tier 2 decisions and used production-path integration as the acceptance standard for all of them, so review thoroughness became unbounded scope growth. The gates below exist to pay for the cheapest evidence capable of changing the decision, then stop. They are not advisory: each is instantiated in the prototype plan and enforced by the foreman.

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
- **Gate 4 — Fixed caps and session-bounded cost review.** There is no cost-ratio trigger; session usage is already bounded, so a session boundary is the natural point to review the shape of cost incurred and still to come. Fixed caps apply and each forces stop-and-decide when crossed, never automatic charter expansion: two builder iterations including one rival; one owner-directed repair pass; two default reviewers, a third only for a named uncertainty; and context-starved legibility only when recoverability is itself a decision. **Builder and review documents have no line or Markdown-length cap.** Their cost is bounded by the pre-declared scope, cases, evidence rung, and measurement charter; authors stop when those obligations are completely reported, not when a file reaches an economic target. Rival iterations are clean-room. A repair pass is named `repair<N>`, not as another iteration, and defaults to the original incumbent builder for deliberate defect continuity unless the disposition explicitly assigns a different builder.
- **Gate 5 — Review triage (foreman-owned).** Every finding is classified before another iteration may open: `decision-blocking`, `production-condition`, `separate-decision`, `deferred-breadth`, or `non-blocking defect`. The foreman performs this triage and is accountable for it. Only a `decision-blocking` finding, and only after the owner ratifies the amendment, may enlarge the active charter. Production conditions go to the milestone plan; separate decisions get their own Gate 1 score; breadth and non-blocking defects are logged and deferred. A review measures and may recommend an action, but does not enlarge scope: the foreman rejects or reroutes any proposed action that exceeds the charter and records the disposition in the process log.
- **Gate 6 — Partial ratification.** A closing disposition may accept a coherent converged subset and explicitly defer the rest; ADR scope matches the evidence that actually converged. Do not hold a prototype open until every adjacent boundary is solved.
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

**Foreman as scope-and-economy steward.** Beyond chartering, sequencing, conformance review, and disposition recommendations, the foreman is the accountable steward of scope and economy. The foreman: (1) keeps the implementation — including reviews and the actions reviews propose — inside the declared scope boundaries and the spirit of economic efficiency, triaging findings (Gate 5) and rejecting or rerouting out-of-charter proposals rather than expanding scope; (2) enforces the evidence ladder and paper-first rule, never climbing to a more expensive rung than the open question requires; (3) tracks the fixed caps and triggers stop-and-decide rather than letting a run drift; (4) assigns each role's capability tier and reasoning effort in the plan and revises them as the run progresses — as decision boundaries and specifications clarify, the required capability for the next launch usually drops, and each change and its rationale is logged at launch time; and (5) chooses spawn versus owner-launch for each role on economy and independence grounds (`docs/roles/foreman.md`, "Spawn versus owner-launch"), spawning only where `AGENTS.md` ("Dispatch authorization") permits it. These are stewardship duties, not authority over artifact quality: the foreman still never reviews artifact quality, overrules a committee finding on the merits, or resolves dissent by rewording it.

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
follow their existing gates. Milestone selection begins with the initial
briefing and owner checkpoint in `docs/roles/foreman.md`, before the foreman
loads proposed follow-up context. Retrospectives are targeted follow-up sources,
not a fixed boot set. If the capsule refuses, read the named committed sources
directly, reconcile the selected ref, and do not work around the refusal with a
prose summary.

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

**`docs/phase-state.md` is the single re-entry document.** It carries the
high level milestone briefing, the current operational state, the durable
pointers, and one
`foreman-context-v1` block holding the phase, topic, active plan, status,
`milestone_state`, `current_role`, and `current_prompt` — which
`tools/foreman_context.py` and `tools/build_orientation_block.py` read from a
resolved ref. There is no
separate handoff note: two re-entry documents meant two statuses that could
disagree, and the same milestone advance had to be written twice. The foreman keeps `current_role` and `current_prompt` accurate:
before a plan or role cycle is marked complete, it prepares the next sequential
role's charter and updates those fields. Prompt preparation records plan
sequence; it does not launch or dispatch a role.

### Phase-State Context Firewall

Phase state is a context firewall, not a project diary. It gives a
returning foreman a curated allowlist: what the product can do now, the current
product question, the active plan, the immediate next action, and explicitly
parked work. It does not repeat track history, review narratives, milestone
scores, retrospective lessons, or a foreman's interpretation of why prior work
was important. `milestone_state` reports workflow position only; it is never
evidence of product quality or direction.

A foreman does not search old plans, reviews, retrospectives, branches, or
other repository history to discover scope or choose work. Follow-up history
is loaded only when the owner, phase state, or active plan names the specific
source and the current question it is meant to answer. Unnamed history remains
available as history, not as boot context.

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
1. Create a milestone branch from the ratified line.
2. Draft and commit the milestone plan as the branch's first milestone commit.
3. Open one draft milestone PR; the owner approves the plan without merging it.
4. Implement, verify, and independently review each atomic track on that branch.
5. Amend or squash provisional checkpoints and repairs into the track they
   complete before the milestone's final review.
6. Distill material decisions and lessons, remove unpromoted working records,
   and complete closeout on the same branch.
7. Mark the PR ready, obtain green CI on the final candidate, and merge the
   whole milestone to the ratified line.
8. Remove the merged branch and any clean milestone worktree.

The plan remains provisional until the milestone merges. Planning changes stay
separate from implementation while work is in flight, but clarifications and
superseded wording are folded into the final planning commit before closeout.
Implementation is never folded into planning.

### Lean Production Loop

Audience: Agents

Once a product contract is settled, production work defaults to one Builder
and one independent Reviewer. Rival prototypes and committee review remain for
genuine design choices; they are not the default way to implement an accepted
contract.

Before chartering a production track, the Foreman performs a lightweight
readiness check against the proposed base. Confirm that the real entrypoint can
resolve every required citizen, symbol, package, release, and binding; identify
the legacy or compatibility examples that must remain valid; and express the
work as observable positive, negative, and compatibility cases. Put the result
in the Builder charter, not in a separate readiness record.

The charter is an executable work packet:

- a compact table of cases, mutations, and expected outcomes;
- the exact implementation boundary and stop conditions;
- focused tests plus applicable static checks; and
- the semantic or boundary questions the independent review must attack.

The Builder turns the case table into tests, demonstrates the important
negative cases against the base when practical, implements the change, and
runs the focused tests and applicable static checks before handoff. For typed
Python work, this includes repository mypy. The Reviewer concentrates on
semantic correctness, omitted adversarial cases, compatibility, and boundary
violations rather than repeating routine verification.

The normal sequence is readiness → build → independent review → one recovery
cycle if needed → CI. Completion records are Foreman work, not a separate
Builder/Reviewer track, unless closing a disputed product claim requires fresh
judgment.

**When the first pass misses:** do not automatically defer the work or change
the milestone's posture.

- A defect against the existing work packet returns to the same Builder. A
  Reviewer rechecks only when the repair still turns on semantic judgment;
  mechanical and typing repairs go to the focused checks and CI.
- A bounded missing prerequisite already implied by the accepted contract is
  added to the current sequence after the Foreman verifies its boundary. It
  does not require a new design round merely because it was discovered late.
- A new product decision, material scope expansion, or unresolved legacy
  compatibility question stops the loop. The Foreman gives the owner plain
  choices to continue, rescope, defer, or stop; none is presumed.
- If the recovery recheck finds another substantive defect, there is no second
  automatic repair cycle. Return to the owner with what failed and the cost of
  another attempt.

Additional agent cycles must answer a newly discovered product question or
close a concrete semantic defect. Moving custody, repairing records prose, or
confirming a deterministic mechanical edit is not enough by itself.

### Branch, PR, and Merge Protocol

Audience: Agents

This is the normative home for how work reaches `main` or another ratified
line. The ratified line is the curated product record. Development is allowed
to be provisional on a milestone branch; accepted ADRs, published schemas, and
data-safety rules retain their own immutability boundaries.

**One milestone, one PR.** Create the milestone branch from the ratified line,
commit the plan, and open one draft PR. The owner approves the plan while the
PR remains open. Prototype decisions, production tracks, review and repair,
closeout, and the retrospective continue on that branch. The PR becomes ready
only when the final proposed repository state is complete and independently
reviewed. Its merge publishes the milestone as one coherent capability.

**Tracks are commits, not PRs.** Each final track is one atomic implementation
commit inside the milestone PR. A builder may use temporary checkpoint and fix
commits during development. Before final review, amend or squash those commits
into the track they complete so the final history presents the working state
change rather than the debugging transcript. Keep planning and implementation
as separate commits.

**The working record is rewriteable.** Charters, interim reviews, repair
instructions, process notes, and checkpoint commits exist to coordinate the
open milestone. They may be committed so fresh agents can orient, and the
milestone branch may be force-pushed while it is draft. At closeout, remove
unpromoted working files and obsolete commits. Preserve material content by
destination: product contracts in ADRs, behavior in tests and fixtures,
process lessons in the retrospective, and current direction in phase docs.

**Review binds the curated candidate.** Independent reviews occur at track
boundaries. Findings return to the same builder when appropriate; repaired
work is folded into the track commit and rechecked where semantic judgment is
still involved. Before the PR is marked ready, an independent reviewer checks
the curated branch range after working-record cleanup. CI then verifies the
exact final PR head. Intermediate review prose need not survive that final
measurement unless it is deliberately promoted as material evidence.

**A separate PR is exceptional.** An independently reusable prerequisite may
merge before the milestone only when the plan names why another consumer needs
it early, parallel work requires a stable published dependency, or delaying
publication creates material risk. The exception is a plan decision, not a
convenience for smaller diffs.

**Every merge to a ratified line is non-fast-forward.** The repository merge
method remains merge-commit only, and the merge commit keeps its
`Merge pull request #N` line. The milestone's curated internal commits retain
track-level legibility and permit targeted reversion when appropriate.

**Agents push; the owner merges.** Agents may push the milestone branch and
open or update its PR. The owner holds the merge. Direct ratified-line work is
limited to the exceptions below. Force-push only the open milestone branch,
never the ratified line, and never after the owner has begun final approval
without first saying that the candidate changed.

**A push is publication, regardless of repository visibility.** The remote hosts
a copy of the record on a third party and visibility is a mutable setting, so
anything ever pushed is treated as potentially world-readable and possibly
cached or indexed after deletion. The synthetic-only fixture-safety suite is a
**pre-push gate**, not a pre-commit courtesy; live data is never in the
repository *or* on any remote.

**What gets its own PR:** one complete milestone; or a process/instruction
change made outside a milestone. A prototype plan is part of its milestone PR.
Branch/worktree removal and optional landmark tags are post-merge repository
maintenance, not commits, so they get no PR.

**What survives inside the milestone PR:** the final plan, atomic track
commits, accepted ADRs and material evidence summaries, tests and fixtures,
the retrospective, and the phase/roadmap/closeout state. Execution ceremony
survives only when deliberately promoted under the durability test above.

**Direct-main exception:** an inconsequential correction to
`docs/phase-state.md` may be committed directly between milestones when it
changes no plan, capability claim, or next-milestone choice. Normal milestone
start, progress, and closeout state belongs in the milestone PR. Process and
instruction changes made between milestones get their own PR.

**Do not narrow a PR below reviewability.** The complete milestone PR must show
the product capability, its contract decisions, executable evidence, material
dissent, and final review posture without requiring reconstruction from
deleted working documents.

**Two-phase commit referencing.** A unit's name is its identity; commits are
transient until the milestone merge freezes them.

- **Before the milestone merges, cite units by name** — ADR number, track name,
  branch, or PR number. Do not make a working SHA a durable cross-reference;
  branch curation may orphan it.
- **Cite a SHA only once it is reachable from `main`.** Post-merge records
  backfill the unit's no-ff **merge-commit** SHA as the anchor for the whole
  unit.
- **Annotated tags are reserved for landmarks** — ratified ADRs, milestone
  closes — applied on `main` post-merge. Not every track; tag sprawl is its own
  legibility cost.

**Re-entry pointer discipline.** During development, the milestone branch's
`docs/phase-state.md` and working charters make that branch self-describing.
The ratified line continues to describe the last completed milestone until the
new milestone merges. The final PR must contain a coherent closed pointer.

**Before starting a milestone:** branch from the ratified line, commit the
complete plan separately, open the draft milestone PR, and obtain owner plan
approval before implementation.

**While executing:** implement one track at a time unless the plan explicitly
groups them; run the track's focused verification; keep temporary checkpoints
recoverable; and curate each completed track into one implementation commit
before final review.

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

## Decision Records

Audience: Shared

ADRs record **product and contract decisions only** — the governance set, the
kernel and act log, schemas and citizen shapes, the rule language, composition
and closure semantics, data-residency and trust boundaries. Process is the
owner's operational domain and is changed by direction plus an edit to the
document that norms it (ADR-0045, decision 5). Do not write a process ADR.

ADRs live under `docs/adr/` with numbered kebab-case filenames, for example
`0001-rule-artifacts-are-versioned.md`. **Never edit an accepted ADR's decision
text in place.** A material change is a new ADR that supersedes it.

**Decision tiers.**

- **Tier 1** — reversible internal implementation choices: file layout, helper
  structure, local typing strategy, fixture organization. Record in the
  milestone retrospective. Use an ADR only when the choice is likely to be cited
  later or touches an architectural boundary.
- **Tier 2** — contract or architecture choices that future surfaces consume:
  schema shape, artifact identity, runner behavior, persistence boundaries,
  fixture contract structure. Create or update an ADR.
- **Tier 3** — product thesis, user-visible concepts, naming, irreversible
  boundaries, data-safety posture, legal or governance meaning. Create or update
  an ADR, and state the alternatives considered.

**An ADR entry states:**

- **Status** — `proposed`, `accepted`, `superseded`, `rejected`, or `retired`.
  Only `accepted` binds; every other status is inert.
- **Tier** — 1, 2, or 3.
- **Context** — the milestone and the problem that forced the decision.
- **Decision** — the commitment made.
- **Consequences** — what this enables, forecloses, or requires.
- **Links** — the milestone plan, evidence, schemas, fixtures, superseded or
  superseding ADRs.

**Write the ADR in plain language.** The record itself must be readable by
someone who was not in the room: name the thing before using it, prefer a
sentence to a term of art, and say what a clause costs as well as what it buys.
An ADR does not get a separate plain-language companion — the five existing
files under `docs/adr/analyses/` stand as history and are not extended.

## Milestone Retrospectives

Audience: Shared

After each milestone, write one retrospective in
`docs/milestone-retrospectives/`, named `YYYY-MM-DD-<milestone-slug>.md`.

A retrospective carries **lessons, not a record**. What shipped is in the merge
commits, what was verified is the green `verify` check, what was decided is the
ADR index, and data safety is `envelope_scan`. Restating any of those is
duplication, and the whole document should run to roughly forty lines:

```md
# Retrospective — <Milestone>

## What differed from the plan
(and why)

## What it cost
(rounds, repairs, and what drove them)

## Follow-ups
(concrete, each with the trigger that reactivates it)

## What should change in the next plan
```

Material lessons take effect by an owner-directed edit to the document that
norms the practice — not by a new ADR.

## Milestone Lifecycle States

Audience: Agents

A milestone is always in exactly one of three persisted state shapes, declared as
`milestone_state` in `docs/phase-state.md`'s `foreman-context-v1` block. The
active plan remains the source of scope, status prose, and deep reads; it does
not own lifecycle state. The foreman does not
infer the state from prose and does not need to: the capsule reports it and
checks that the selected commit contains the artifacts its state requires.

| State | Meaning | Next transition |
| --- | --- | --- |
| `planned` | The plan is committed on the milestone branch and approved in its draft PR; no track has started | Start the first track |
| `track-<n>` | Track *n* is in flight | Finish track *n*, then the next track or the closing unit |
| `closed` | The milestone is complete | Select the next milestone |

`closed` is also how "no milestone is running" is expressed: `docs/phase-state.md`
keeps pointing at the just-closed plan, so `active_plan` is never empty and a
foreman that reads `closed` knows its job is selection, not execution.

**The committed state describes its own branch.** The ratified line remains at
the last completed milestone while a draft milestone PR is open. On the
milestone branch, the planning commit carries `planned`, track commits advance
through `track-<n>`, and the final candidate carries `closed`. The single merge
therefore publishes a self-consistent completed state rather than exposing
in-flight lifecycle values on the ratified line.

The selected commit must contain its active plan. A `closed` commit must also
name and contain its retrospective. `tools/foreman_context.py` validates those
facts in the selected tree. It fetches and reports the ratified line and branch
divergence separately, so a prospective `planned` or `closed` state is not
rejected merely because its boundary PR has not merged yet.

The plan and closing transitions both occur on the milestone branch; only the
closed transition reaches the ratified line.

## Milestone Start

Create the milestone branch from the ratified line, commit the complete plan,
set the branch's lifecycle to `planned`, and open the draft milestone PR. The
owner's approval of that plan starts implementation without merging the PR.

## Milestone Closeout

Audience: Agents

A milestone closes in its one milestone PR. Closeout makes the proposed
repository self-describing and curates the branch before the PR is marked
ready. Treat closeout as bookkeeping and distillation, not a chance to
reinterpret results. If a capability, maturity, or next-step claim needs new
judgment or evidence, stop and raise it as a project-execution question.

1. Before final review:
   - fold checkpoint and repair commits into their completed track commits;
   - remove working charters, interim reviews, repair instructions, and process
     notes unless a material item is explicitly promoted;
   - archive a closed prototype working set when its evidence remains useful;
     and
   - confirm that ADRs, tests/fixtures, and the retrospective carry every
     decision, behavioral claim, dissent, and reusable lesson needed after the
     working record disappears.
2. In the final milestone candidate:
   - set `docs/phase-state.md`'s `milestone_state` to `closed`, replace conditional
     status prose with the completed result, complete its execution record,
     remove `initial_briefing_follow_up`, and route `deep_reads.new_milestone`
     through the retrospective;
   - update `docs/phase-state.md` so its briefing, current state, pointers, and
     next action describe the completed milestone and leave the next milestone
     unselected;
   - update the phase roadmap's milestone status; and
   - include the retrospective.
   - run `git diff --check`, `python3 tools/governance_lint.py`, and
      `python3 tools/envelope_scan.py --range <base>..HEAD` before pushing.
   - run `python3 tools/foreman_context.py --ref HEAD --format markdown`.
      It must report `closed`, select-a-new-milestone as the next transition, 
      no temporary follow-up capsule, and the initial briefing checkpoint. 
3. Have an independent reviewer inspect the curated candidate range. Address
   any finding under the lean production loop, then obtain green CI on the
   exact final PR head.

The merge leaves the milestone closed for re-entry. `docs/phase-state.md` continues
to point to the just-closed plan until the next milestone branch is selected.
After the merge is visible on the ratified line, delete the merged branch and
remove clean milestone worktrees or temporary aliases. Never remove a worktree
used by a live session.

## Recording Owner Assent

Audience: Agents

**The merge is the durable record.** Owner directions made while the milestone
is open guide the working branch. The final plan, ADRs, and retrospective
distill any direction whose effect must survive. Merging the milestone PR
publishes that curated result; do not preserve redundant assent prose merely
to reproduce the conversation that produced it.

**`authorize` is about dispatch and nothing else.** In agent-process text the
word means one thing — the owner granting a foreman sub-agent spawns in one
thread, per `AGENTS.md` ("Dispatch authorization"). The owner *approves* plans,
*accepts* findings, and *directs* work. None of those is an authorization, and
none of them gates the work: the foreman runs the milestone loop without asking.

This was linted for a while, because foremen kept reaching for the word and
then inflating it into a permission gate on progress. The lint is gone — it
treated a comprehension failure as a spelling problem. The comprehension is
fixed at the source, in the `AGENTS.md` section itself.

`Owner Authorization` is separately a ratified product-domain term (ADR-0044):
one of four trust domains, naming the owner's deliberate acts inside the tax
system. It has nothing to do with dispatch.

**Do not restate an `AGENTS.md` rule — including by denying it.** The
single-source rule already forbids repeating a rule in a second document. A
*negation* restates it just as surely: a reader told "this record does not
authorize a dispatch" has been taught that records bear on dispatch, which is
the premise the rule exists to deny. If a document needs to disclaim a rule, the
document is addressed to the wrong reader.

**Charters declare their audience.** A charter is a work order addressed to the
role that executes it, and says so (`Audience: Builder`). Content only the owner
or the foreman can act on belongs in `docs/phase-state.md`, whose
`foreman-context-v1` block is the foreman↔owner channel. A charter that reports
the foreman's own compliance has the wrong reader; a builder cannot dispatch,
and did not launch itself.

None of the rules in this section is machine-checked; they are caught in
review.

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

Milestone planning happens on a new milestone branch before implementation.
The initial plan is that branch's first milestone commit and opens the draft
milestone PR. If the plan changes during implementation, keep the change
separate from code while it is being evaluated; fold obsolete planning edits
into the final planning commit during closeout.

Planning commits are mandatory. A plan is ready for execution when it contains
the required milestone-plan contents, is committed separately from
implementation, and the owner has approved it in the still-open draft PR.

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

Parallel workstreams may use temporary branches or worktrees, but they do not
open independent PRs by default. Their reviewed commits integrate into the
milestone branch in dependency order, and the milestone's one PR remains the
publication unit.

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
- Dependencies pending: any workstream whose implementation or integration depends on another workstream.
- Constraints: files, schemas, artifacts, or behavior that must not change in each stream.
- Conflict hotspots: files or directories likely to conflict.
- Integration order: the dependency-first order in which workstreams join the milestone branch.
- Sync points: when downstream branches must rebase onto or otherwise adopt producer commits.
- Verification per stream: tests or commands required for each stream.
- Integration verification: tests or commands required after the streams join the milestone branch.
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
- Track 20 generation depends on the Track 19 schema integration.
- Golden return fixtures depend on the Track 20 generation integration.

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

Integration order:
1. Integrate the return artifact contract into the milestone branch.
2. Rebase generation work on the integrated contract.
3. Integrate generation.
4. Rebase golden fixture and renderer work.
5. Integrate fixtures and renderer.

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

Parallel work should integrate in dependency order, not completion order. A
branch finishing first is not a reason to integrate first if another pending
workstream defines the contract it consumes.

Golden fixture updates require single-owner coordination. Do not update the
same expected artifact from multiple branches unless the manifest explicitly
defines the integration order and regeneration authority.

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

`docs/archive/` preserves useful historical context and is never authority.
Archive movement changes a document's routing status, not Git history or
repository size.

At phase or milestone cleanup:

- use a dated archive root with a README explaining the boundary;
- preserve enough original topology for the evidence to remain navigable;
- repair concrete inbound references rather than leaving broken links or a
  directory full of forwarding stubs;
- keep active replacements at their expected paths; and
- never archive accepted ADRs, governance, published schemas, current phase
  direction, or the active milestone plan.

Working charters, interim reviews, repair instructions, checkpoints, and raw
process logs are not archived by default; remove them after distilling material
content. Archive them only when they are necessary evidence for a durable ADR,
material dissent, or a retrospective lesson. Completed prototype evidence and
closed-phase milestone plans may be archived because their current conclusions
live in ADRs, retrospectives, and phase summaries.

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
