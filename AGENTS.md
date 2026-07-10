# Agent Operating Guide

This file defines how agents should work in this repository. It is a canonical project meta document. Follow it before making code, fixture, schema, runner, or planning changes.

## Canonical References

Read these before substantial work:
- `README.md`: current usage and runner commands.
- `PROJECT_PLANNING.md`: planning process, milestone rules, parallel work rules, and archival rules.
- `docs/phase-state.md`: summary pointer to the active phase.
- `docs/phases/<phase-name>/<phase-name>-overview.md`: phase purpose, scope, and exit criteria.
- `docs/phases/<phase-name>/<phase-name>-roadmap.md`: phase roadmap, active milestone, milestone status, and implementation notes.
- `docs/phases/<phase-name>/milestones/*.md`: milestone execution plans with track-level plans.

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
- The orchestrating developer must confirm planning is complete before implementation starts.
- Planning and implementation must be committed separately.
- Milestone implementation must happen on a dedicated milestone execution branch, not directly on `main`.
- Each completed track must be committed separately before the next track starts, unless the milestone plan explicitly groups tracks.
- At the end of milestone implementation, the branch history must contain the expected per-track commits rather than one combined milestone implementation commit.
- When all milestone tracks are complete, stop for orchestrating developer review before completing the milestone.
- Milestone completion requires explicit instruction and uses a non-fast-forward merge from the milestone branch into `main`, with the milestone name in the merge commit message.
- Parallel work manifests belong only in milestone plans and only when explicitly requested.
- Roadmaps are milestone-level product documents and carry phase status, not detailed execution plans.
- Follow-up plan clarifications default to being squashed into the relevant planning commit when directed by the orchestrating developer.

## Contract-First Development

Refer to governance documents

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

Golden fixture changes must be intentional. Regenerate only when the contract or expected behavior changed, then review the diff.

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

Planning commits should precede implementation commits and should not be made on the milestone execution branch unless the orchestrating developer explicitly directs otherwise. If a plan is revised before implementation begins, keep the planning history clean by squashing revisions into the relevant planning commit when directed by the orchestrating developer.

Milestone implementation should be one completed track per commit. A completed milestone branch should show distinct commits for each completed track, unless the milestone plan explicitly approved a grouped track commit before implementation. Do not squash, rebase away, or collapse track commits when completing a milestone unless the orchestrating developer explicitly directs that history shape.

Milestone branch completion must be done only after orchestrating developer approval. Merge the milestone branch into `main` with a non-fast-forward merge commit and include the milestone name in the merge commit message.

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
