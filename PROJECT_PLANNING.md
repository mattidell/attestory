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

**Termination.** Every iteration opens with declared questions. An iteration that resolves no new questions forces a stop-and-decide. Default cap: three iterations before an owner check-in.

**Artifacts.** `docs/prototypes/<topic>/` holds charters, iteration examinations, committee review notes, and the final evaluation analysis — these merge to `main`. Prototype code lives on maintained branches named `prototype/<topic>/it<N>`; prototype branches are evidence exhibits — never merged to `main`, never deleted.

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
