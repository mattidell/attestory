# Application Boundary Definition Roadmap

## Roadmap

### Milestone 1: Product Boundary Contract

Define the product-facing contract around the existing engine workflow.

This milestone matters because the application layer needs a stable interface for workspaces, source drafts, runs, and artifacts before storage or UI decisions become durable.

Milestone plan:
- `docs/phases/application-boundary-definition/milestones/product-boundary-contract.md`

### Milestone 2: Local Workspace Persistence

Persist workspaces, draft source records, run metadata, and generated artifact references.

This milestone gives the application a practical way to maintain user-created records and computation history while keeping engine artifacts separate from storage implementation details.

Milestone plan:
- `docs/phases/application-boundary-definition/milestones/local-workspace-persistence.md`

### Milestone 3: Workspace Workflow Service

Expose the local persistence and product boundary workflow through a small application service layer.

This milestone matters because future UI or API code should call stable product operations for workspace creation, source draft updates, run execution, run history, and run detail lookup instead of coupling directly to filesystem layout or engine internals.

Milestone plan:
- `docs/phases/application-boundary-definition/milestones/workspace-workflow-service.md`

### Milestone 4: Code Review And Refactor

Review and refactor the application-boundary code before adding more product-facing read models or surfaces.

This milestone matters because recent service and persistence work exposed typing and application-boundary clarity gaps that should be addressed while the application boundary is still small.

Milestone plan:
- `docs/phases/application-boundary-definition/milestones/code-review-and-refactor.md`

### Milestone 5: Artifact Review Read Models

Create product-facing read models for persisted validation, coverage, resolution, return artifact, and Markdown review outputs.

This milestone matters because the application needs stable review data that is easy to inspect, test, and render without changing the engine artifacts that remain authoritative.

Milestone plan:
- `docs/phases/application-boundary-definition/milestones/artifact-review-read-models.md`

### Milestone 6: Demo Application Surface

Provide a focused user-facing surface to create and edit source drafts, run the workspace, and review artifacts.

This milestone turns the engine workflow into a usable product slice and validates that the application boundary supports real interactions.

Milestone plan:
- `docs/phases/application-boundary-definition/milestones/demo-application-surface.md`

## Status

Phase status:
- Active.

Active milestone:
- None. Code Review And Refactor is complete.

Implementation notes:
- Product Boundary Contract introduced product-facing workspace, run payload, run summary, run detail, and artifact reference contracts.
- Product boundary contracts model user-owned tax-year workspaces, workspace-scoped editable source drafts, immutable run payload snapshots, URI-addressed artifact references, and synthetic demo data classification.
- Local Workspace Persistence added a filesystem repository boundary for synthetic product workspaces, source draft revisions, immutable run records, generated artifact persistence, derived workspace and run listings, latest-draft pointer metadata, and latest-run derivation from run summaries.
- Workspace Workflow Service added a class-based application service layer over product boundary and local persistence operations, explicit operation result objects, granular source draft creation and versioning operations, exact-revision run execution, latest-revision convenience execution, run history/detail lookup, latest-run-with-detail lookup, and artifact reference resolution.
- Code Review And Refactor added a strict scoped mypy baseline for application-boundary modules and clarified product boundary, local persistence, and workflow service payload types before Artifact Review Read Models begins.
- Artifact Review Read Models and Demo Application Surface are draft future milestone plans and should be reviewed before their implementation begins.

Project impact:
- Application architecture.
- Product boundary schemas.
- Synthetic product boundary fixtures.
- Product boundary validators and execution facade.
- Future storage boundaries.
- Application service boundary.
- Code review, refactor, and type-checking conventions.
- Application-boundary type-checking baseline.
- Future API boundaries.
- Future user-facing source entry and artifact review workflows.
