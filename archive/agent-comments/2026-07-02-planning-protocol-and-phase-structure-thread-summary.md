# Agent Planning And Execution Summary: Planning Protocol And Phase Structure

Date: 2026-07-02

## Thread Context

This work thread focused on moving the project from ad hoc prototype planning toward a more deliberate planning and execution discipline.

The project already had an engine workflow, phase direction, milestone plans, and implementation history. The user wanted the planning system itself to become clearer before continuing implementation: who each document is for, where phase and milestone documents live, how planning is committed, how milestone execution is reviewed, and how the agent should operate without collapsing product-level planning into implementation mechanics.

## Nature Of The Work

The thread addressed planning architecture rather than tax-engine behavior.

The main work was to formalize:
- A canonical planning protocol in `PROJECT_PLANNING.md`.
- Agent operating expectations in `AGENTS.md`.
- Phase-specific planning directories under `docs/phases/`.
- Separate phase overview and roadmap documents.
- Milestone plans nested under the phase they belong to.
- Audience distinctions for User, Agent, and User+Agent documentation.
- A milestone execution branch protocol.
- A clearer separation between user-facing planning structure and agent-facing process details.

The work also backfilled and reorganized planning docs around the current phase sequence, especially Engine Contract Stabilization and the transition toward Application Boundary Definition.

## What Was Addressed

The thread clarified the planning hierarchy:
- Meta documents describe repository-wide planning and agent behavior.
- Phase overviews describe purpose, scope, and exit criteria.
- Phase roadmaps describe milestone sequence, current status, lessons learned, and project impact.
- Milestone plans describe executable planning details such as tracks, contracts, fixtures, verification, and exit criteria.
- Tracks describe atomic implementation units inside a milestone.

The planning protocol was revised so user-facing sections describe product direction and capability rather than issuing instructions. Formalities, constraints, directory layout, branch rules, and execution protocols were moved under process-oriented sections targeted to User+Agent or Agent audiences.

The active phase structure was also reorganized so phase documents live under phase-specific directories, with milestone plans nested inside the relevant phase.

## Decisions Discussed With The User

The user moved the project away from generic phase labels such as Prototype, MVP, and Production.

Why it matters:
- Those labels were too broad to guide implementation.
- The new phase names describe actual project risks and boundaries, such as Engine Contract Stabilization, Application Boundary Definition, Personal Workflow Readiness, Tax Scope Expansion, Review Package And Export, and Shareable Portfolio Application.

The user chose milestones over informal track groups.

Why it matters:
- Milestones are easier to evaluate from a product and architecture perspective.
- Tracks remain useful for implementation, but milestones become the planning and review boundary.

The user clarified that roadmap documents are for humans.

Why it matters:
- Roadmaps should explain capability, sequencing, and project impact.
- Detailed implementation mechanics belong in milestone plans and process sections.

The user clarified that the `Audience` section itself is user-targeted.

Why it matters:
- The section should describe the distinction between audiences, not instruct agents how to write.
- It established a broader rule: user-targeted documentation should describe direction and capability, not contain implementation instructions.

The user asked for phase documents to split into overview and roadmap.

Why it matters:
- The overview can remain relatively stable as the phase purpose and scope.
- The roadmap can carry milestone status, lessons learned, active milestone state, and pivots.

The user established that milestone execution should happen on a dedicated branch and that implementation commits should remain track-level.

Why it matters:
- It preserves reviewable implementation history.
- It prevents a whole milestone from becoming one opaque commit.
- It gives the orchestrating developer a clear review point before milestone completion.

## Related But Left Out Of Scope

This thread did not implement new tax-engine functionality.

The following remained out of scope:
- New return artifact behavior.
- New source document models.
- Persistence, database design, API, UI, or worker implementation.
- Personal-data workflows.
- Tax form scope expansion.
- PDF generation or e-file support.
- Formal completion of the current phase.
- Merge or cleanup decisions for unrelated local changes.

The thread also did not resolve whether existing untracked or deleted files in `agent-comments/` or historical changelog files should be committed, archived, restored, or ignored. Those are repository hygiene decisions that should be handled explicitly.

## Why This Matters To The Current Phase

Engine Contract Stabilization depends on stable contracts and reviewable workflow artifacts. The planning system now mirrors that same discipline:
- Phase documents define the boundary.
- Milestone plans define the implementation contract.
- Track commits preserve atomic execution history.
- Roadmaps capture status and project impact.
- Audience targeting keeps human-facing planning readable while preserving agent-level rigor.

This matters before Application Boundary Definition because application work will introduce more surfaces: persistence, services, UI, run history, and artifact review. Without a clear planning protocol, those layers could easily blur product intent, architecture boundaries, and implementation mechanics.

## Follow-Up Points

Potential follow-up work:
- Decide whether `agent-comments/` should be committed, ignored, or treated as local-only agent working notes.
- Decide what should happen to `docs/prototype-changelog.md`, which has appeared as a deleted working-tree file in prior turns.
- Review whether all phase roadmaps follow the updated user-targeted roadmap style.
- Review whether all milestone plans are sufficiently agent-targeted and contain the required track, fixture, verification, and data-safety details.
- Decide when Engine Contract Stabilization is formally complete and when Application Boundary Definition becomes active.
- Consider adding a small root `CHANGELOG.md` once the project needs consumer-facing capability history.
- Consider adding a planning review checklist to milestone completion so roadmap status, phase state, and follow-up notes are updated consistently.
