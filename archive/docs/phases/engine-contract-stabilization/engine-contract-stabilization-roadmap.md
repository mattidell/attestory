# Engine Contract Stabilization Roadmap

## Roadmap

### Milestone 1: Source Records And Direct Mapping

Synthetic source document data becomes canonical source records and directly populates the first in-scope federal form fields.

This milestone comes first because the project needs trustworthy source records before computation, review, persistence, or user-facing workflows can build on them.

### Milestone 2: Editable Draft Inputs And Reviewable Coverage

Editable source document drafts become canonical source records, validation results, and coverage views.

This milestone matters because the product workflow starts with editable user records. Separating draft input from canonical engine input keeps the engine stable while allowing future entry surfaces to evolve.

### Milestone 3: Workspace Execution And Golden Artifacts

A synthetic federal workspace runs through one canonical workflow and produces committed expected artifacts.

This milestone turns isolated scripts into a repeatable workflow. Golden artifacts make later changes reviewable and give future application layers a stable integration target.

### Milestone 4: Dependency-Aware Resolution

The engine distinguishes directly resolved fields, computed fields, source-blocked fields, computation-blocked fields, and optional unpopulated fields.

This milestone prepares the workflow for return output. A return artifact needs a resolved field set rather than raw coverage alone.

### Milestone 5: Return Artifact Evaluation

A workspace run produces a deterministic normalized federal return artifact and a human-readable return review.

This milestone is the final engine-boundary proof point before application boundary work. It shows that synthetic records can produce coherent return-like outputs without relying on UI, persistence, or PDF rendering.

### Next Phase: Application Boundary Definition

The next phase defines the product-facing boundary around source entry, workspace execution, run history, and artifact review.

This follows return artifact evaluation because product surfaces should integrate with stable engine artifacts rather than invent output shapes inside the app layer.

## Status

Current phase:
- Engine Contract Stabilization

Phase status:
- Complete; transitioned to Application Boundary Definition.

Active milestone:
- None. Return Artifact Evaluation is complete.

Most recent milestone plan:
- `docs/phases/engine-contract-stabilization/milestones/return-artifact-evaluation.md`

### Milestone 1: Source Records And Direct Mapping

Status:
- Complete.

Implementation notes:
- Introduced source document, direct mapping, federal field catalog, and field coverage contracts.
- Established the synthetic-fixture-only data safety pattern.

Project impact:
- Schemas.
- Source document fixtures.
- Direct mapping definitions.
- Field coverage projection.

Milestone plan:
- `docs/phases/engine-contract-stabilization/milestones/source-records-and-direct-mapping.md`

### Milestone 2: Editable Draft Inputs And Reviewable Coverage

Status:
- Complete.

Implementation notes:
- Introduced source document drafts, draft normalization, source validation, coverage read models, and Markdown coverage output.
- Clarified the distinction between editable user-shaped input and canonical engine-shaped records.

Project impact:
- Schemas.
- Draft fixtures.
- Coverage runners.
- Reviewable Markdown artifacts.

Milestone plan:
- `docs/phases/engine-contract-stabilization/milestones/editable-draft-inputs-and-reviewable-coverage.md`

### Milestone 3: Workspace Execution And Golden Artifacts

Status:
- Complete.

Implementation notes:
- Introduced the tax workspace fixture, canonical workspace runner, run manifest, and committed golden artifacts.
- Established the workspace run as the main integration boundary.

Project impact:
- Workspace workflow.
- CLI runner.
- Run manifest.
- Golden artifact tests.

Milestone plan:
- `docs/phases/engine-contract-stabilization/milestones/workspace-execution-and-golden-artifacts.md`

### Milestone 4: Dependency-Aware Resolution

Status:
- Complete.

Implementation notes:
- Introduced computed field definitions, dependency-aware field resolution, and a field resolution workspace artifact.
- Moved the workflow from raw coverage reporting toward return-ready resolved fields.

Project impact:
- Computed field definitions.
- Field resolver.
- Workspace runner output.
- Golden field resolution artifact.

Milestone plan:
- `docs/phases/engine-contract-stabilization/milestones/dependency-aware-resolution.md`

### Milestone 5: Return Artifact Evaluation

Status:
- Complete.

Implementation notes:
- Introduced the normalized return artifact contract, return artifact generator, compact resolution summary, and Markdown return review.
- Wired return artifacts into the workspace runner, run manifest, and golden workspace fixtures.

Project impact:
- Return artifact contract.
- Workspace runner output.
- Golden artifacts.
- Human-readable review output.

Milestone plan:
- `docs/phases/engine-contract-stabilization/milestones/return-artifact-evaluation.md`

### Application Boundary Definition

Status:
- Active phase.

Implementation notes:
- Began after the return artifact workflow stabilized.
- Expected to define product-facing boundaries around source records, workspace execution, run history, and artifact review.

Project impact:
- Application architecture.
- Storage and API boundaries.
- Future UI workflows.

Phase overview:
- `docs/phases/application-boundary-definition/application-boundary-definition-overview.md`
