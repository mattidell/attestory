# Agent Operating Guide

This file defines how agents should work in this repository. It is a canonical project meta document. Follow it before making code, fixture, schema, runner, or planning changes.

## Canonical References

Read these before substantial work:
- `docs/governance/`: the ratified governance set — Constitution (norms), Ontology (meaning), Engineering Constraints (implementation patterns and detections), Principles (interpretation where the others are silent), Commentary (rationale). This is the sole contract authority; see `docs/governance/README.md` for the authority order.
- `README.md`: current usage and runner commands.
- `PROJECT_PLANNING.md`: planning process, milestone rules, parallel work rules, and archival rules.
- `docs/phase-state.md`: summary pointer to the active phase.
- `docs/phases/<phase-name>/<phase-name>-overview.md`: phase purpose, scope, and exit criteria.
- `docs/phases/<phase-name>/<phase-name>-roadmap.md`: phase roadmap, active milestone, milestone status, and implementation notes.
- `docs/phases/<phase-name>/milestones/*.md`: milestone execution plans with track-level plans.
- Up to the five most recent files in `docs/milestone-retrospectives/`, newest first, before planning a new milestone.

## Owner Posture and Collaboration Rules

The owner's development posture is defined in `PROJECT_PLANNING.md` (Development Posture). Operational consequences for agents:

- **Apologize rather than ask permission.** For reversible work inside an agreed direction, proceed and disclose plainly — in the commit, the retrospective, or the report — rather than blocking on questions. Reserve questions for irreversible actions (history rewrites, data deletion, publishing) and genuine direction changes.
- **Snapshot-and-reset protocol.** When the owner directs that merged work be unwound: (1) create `snapshot/<date>-<topic>` at the current `main` tip; (2) verify the snapshot ref exists; (3) reset `main` to the directed commit; (4) record what was unwound and why in `docs/reviews/` or the relevant retrospective. Never reset or rewrite `main` without the snapshot ref, and never on your own initiative.
- **Worktree and branch hygiene.** Keep open worktrees to a minimum. Remove worktrees that are clean and no longer needed, including stale ones left by other agents. Delete merged milestone and continuation branches after confirming their commits are reachable from `main`. Do not leave uncommitted work in a worktree at hand-off: commit it, snapshot it, or discard it and say so.
- **Hand-offs.** If you resume another agent's interrupted work, say so in the retrospective, note what you adopted versus reworked, and leave the tree clean for the next agent.
- **Review records.** Critical reviews of merged work live under `docs/reviews/` with dated filenames. A review is advisory: the owner decides whether to act, ignore, or snapshot-and-reset.
- **Prototype-process dispatch.** If the active milestone (per `docs/phase-state.md`) is a prototype-process milestone, do not start working generally: read the seat file (`docs/prototypes/<topic>/SEAT.md`) and take the seat it assigns, under that seat's role charter. Do not self-assign the foreman seat unless the seat file marks it vacant; record any succession in the process log. Context-starved seats are never taken by generic resumption — they are launched by the owner with the role file's launch line.

## Development Priorities

Prioritize in this order:
1. Data safety.
2. Contract clarity.
3. Deterministic fixtures and tests.
4. Small atomic commits.
5. Documentation that reflects actual behavior.
6. Product/app work only after stable engine boundaries exist.

Do not optimize for UI, persistence, or broad tax coverage before the current engine contracts are stable.

## Planning Rules

Follow `PROJECT_PLANNING.md` for the full planning protocol. That document is authoritative for milestone planning, track planning, planning commits, parallel work manifests, roadmap conventions, and archive rules.

High-level requirements:
- Phase documents live under `docs/phases/<phase-name>/`.
- Each phase has `<phase-name>-overview.md` and `<phase-name>-roadmap.md`.
- Milestone plans live under the relevant phase's `milestones/` directory.
- Track plans sit inside the relevant milestone plan.
- Initial milestone plan generation must be committed before the milestone execution branch begins implementation.
- Planning must contain the required milestone-plan contents and be committed before implementation starts.
- Planning and implementation must be committed separately.
- Milestone implementation must happen on a dedicated milestone execution branch, not directly on `main`.
- Each completed track must be committed separately before the next track starts, unless the milestone plan explicitly groups tracks.
- At the end of milestone implementation, the branch history must contain the expected per-track commits rather than one combined milestone implementation commit.
- When all milestone tracks are complete, report milestone status, and continue the planning/development loop.
- Milestone completion uses a non-fast-forward merge from the milestone branch into `main`, with the milestone name in the merge commit message.
- Parallel work manifests belong only in milestone plans and only when parallel execution is part of the milestone plan.
- Roadmaps are milestone-level product documents and carry phase status, not detailed execution plans.
- Follow-up plan clarifications before implementation default to being squashed into the relevant planning commit to keep planning history clean.
- Before planning a new milestone, read up to the five most recent milestone retrospective files from `docs/milestone-retrospectives/` and carry forward relevant lessons into the milestone plan.
- Architectural changes made during a milestone must be documented in ADRs under `docs/adr/`, using the decision tier to choose the record shape.
- After each milestone, write a milestone retrospective under `docs/milestone-retrospectives/` before starting the next milestone plan.

## Decision Records

Use ADRs for architectural changes, boundary decisions, contract commitments, and decisions that shape future implementation.

Prototype evidence rules (see `PROJECT_PLANNING.md`, Prototype-Driven Decisions):
- Tier 3 ADRs and contract-foundational Tier 2 ADRs require a prototype evaluation analysis as cited evidence. Do not propose an ADR whose central design element is still a placeholder.
- You are authorized to build prototypes before proposing such ADRs — do not ask permission. Keep prototype code on `prototypes/<topic>/it<N>` branches; never merge it to `main`; never delete those branches. Only the documents under `docs/prototypes/<topic>/` merge.
- A decision that shapes all future content (for example, the language tax rules are written in) is Tier 3, not a contracts line-item in a milestone plan. It gets the prototype process and its own ratification.
- Prototype roles are separated: the builder never reviews their own iteration; the foreman never reviews artifacts produced under their own charter. Review notes must report measurements against a pre-declared check, not impressions.

ADR location and naming:
- Store ADRs under `docs/adr/`.
- Use numbered kebab-case filenames, for example `0001-rule-artifacts-are-versioned.md`.
- Do not edit accepted ADR decisions in place to change history. Add a superseding ADR when a decision changes materially.

Decision tiers:
- Tier 1: reversible internal implementation choices, such as file layout, helper structure, local typing strategy, or fixture organization. Document in the milestone retrospective unless the choice affects an architectural boundary; use an ADR only when the decision is likely to be reused or cited.
- Tier 2: contract or architecture choices future surfaces consume, such as schema shape, artifact identity, runner behavior, persistence boundaries, or fixture contract structure. Create or update an ADR in `docs/adr/`.
- Tier 3: product thesis, user-visible concepts, naming, irreversible boundaries, data safety posture, or legal/governance meaning. Create or update an ADR in `docs/adr/` with context, decision, consequences, and alternatives considered.

ADR entries should state:
- Status: proposed, accepted, superseded, or retired.
- Tier: 1, 2, or 3.
- Context: the milestone and problem that forced the decision.
- Decision: the commitment made.
- Consequences: what this enables, forecloses, or requires.
- Links: related milestone plan, retrospective, schemas, fixtures, or superseding ADRs.

## Milestone Retrospectives

After each milestone, create a retrospective in `docs/milestone-retrospectives/`.

Retrospective filenames should be dated and milestone-specific, for example `2026-07-10-engine-contract-stabilization.md`.

Each retrospective should include:
- Milestone: name, branch, and merge commit when applicable.
- Shipped: concise capability summary.
- Verification: commands run and results.
- Decisions: Tier 1/2/3 decisions made, with links to ADRs for Tier 2 and Tier 3 items.
- Deviations: where implementation differed from the plan and why.
- Data safety: statement of synthetic-only committed data and any relevant checks.
- Follow-ups: concrete work items for future milestones.
- Planning lessons: what should change in the next milestone plan.

## Contract-First Development

Contracts descend from the governance set in `docs/governance/`. Schemas, artifact shapes, runner behavior, and persistence boundaries must conform to the Constitution's articles and the Ontology's definitions; the Engineering Constraints state the foreclosed implementation patterns and the detections that catch violations. When a contract decision is not determined by the governance set, it is a Tier 2 or Tier 3 decision: record an ADR.

Guardrails:
- The `archive/` tree is historical reference only. It holds the pre-governance v2 engine, which predates the Ontology and violates it in places. Use it for tax-domain reference and sanity checks, never as a source of contracts, schemas, or patterns.
- Do not build on reserved or deferred ontology entries (T1 derived-finding authority construction; T2 stance; redaction). If a milestone appears to need one, stop and surface the resolution as a Tier 3 decision instead of improvising doctrine.
- Changes to `docs/governance/` require a new version and user ratification; agents may propose governance changes but never adopt them.

## Fixture Rules

Fixtures must be synthetic and safe to publish.

Use committed fixtures for:
- Stable sample source data.
- Stable workspace scenarios.
- Expected golden artifacts.
- Contract-level tests.

Use ignored local output for:
- Ad hoc runner output.
- Personal experiments.
- Generated scratch files.

Golden fixture changes must be intentional. Regenerate only when the contract or expected behavior changed, then inspect the diff.

## Data Safety Rules

Never commit:
- Personal source documents.
- Real uploaded tax documents.
- Personal current-year fact instances.
- Personal manual entries.
- Prior returns.
- Generated artifacts derived from personal data.
- Absolute local machine paths in committed fixtures or manifests.

Personal or ad hoc local work must stay under ignored paths such as:
- `local-data/`
- `temp/`
- `private-archive/`
- `uploads/`
- `generated/user/`

Synthetic committed files should use demo labels and obviously synthetic IDs.

Run data safety tests when changing fixtures, manifests, paths, or generated artifacts.

## Commit Rules

Prefer one atomic conceptual change per commit.

Good commits:
- Add one schema and its loader/tests.
- Add one runner and its subprocess tests.
- Add one artifact to the workspace runner and golden fixtures.
- Add one planning update.

Avoid commits that mix:
- Planning rewrites and implementation.
- Schema shape changes and unrelated refactors.
- Golden fixture regeneration and broad code cleanup.
- Data safety changes and feature work.

Commit messages should describe the capability or contract added.

Planning commits should precede implementation commits and should not be made on the milestone execution branch. If a plan is revised before implementation begins, keep the planning history clean by squashing revisions into the relevant planning commit.

Milestone implementation should be one completed track per commit. A completed milestone branch should show distinct commits for each completed track, unless the milestone plan explicitly specified a grouped track commit before implementation. Do not squash, rebase away, or collapse track commits when completing a milestone unless the milestone plan explicitly requires that history shape.

Milestone branch completion must be done after planned tracks are complete and required verification passes. Merge the milestone branch into `main` with a non-fast-forward merge commit and include the milestone name in the merge commit message.

## Documentation Rules

Update docs when behavior changes.

Use root all-caps documents for canonical meta process:
- `PROJECT_PLANNING.md`
- `AGENTS.md`
- future `CHANGELOG.md`

Use `docs/` lower-case planning documents for phase, milestone, and historical planning:
- `docs/phase-state.md`
- `docs/phases/<phase-name>/<phase-name>-overview.md`
- `docs/phases/<phase-name>/<phase-name>-roadmap.md`
- `docs/phases/<phase-name>/milestones/*.md`

Do not silently overwrite obsolete plans. Archive superseded plans under `docs/archive/` with a short rationale.

Consumer-facing changelogs should describe capabilities and should not list commit hashes.
