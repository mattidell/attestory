# Milestone Plan: Product Boundary Contract

## Planning Status

Status: complete milestone plan; implementation complete.

This milestone plan was reviewed, confirmed complete, committed, and implemented.

No parallel work manifest is included. Add one only if the user or orchestrating developer explicitly requests parallel execution planning for this milestone.

## Objective

Define the product-facing contract around the stabilized engine workflow so future persistence, API, and UI work can depend on explicit workspace, source draft, run, and artifact boundaries.

This milestone answers what the product consumes and produces around the engine. It does not build the final product experience.

## Current State

Implemented engine workflow:
- Tax workspace fixture.
- Source document draft schemas and normalization.
- Source validation.
- Direct source-to-form mapping.
- Field coverage.
- Field resolution.
- Normalized return artifact.
- Markdown return review.
- Run manifest.
- Golden workspace artifact tests.

Stable engine runner:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

Stable synthetic workspace:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/
```

Phase prerequisite:
- Engine Contract Stabilization should be marked complete before implementation begins.

## Scope

In scope:
- Define the product boundary terminology for workspaces, supported source drafts, run execution, run summaries, and artifact review.
- Add durable product-facing contract schemas where JSON payloads become application boundary artifacts.
- Add loaders or validators for the new product boundary contracts.
- Add synthetic fixtures for supported product boundary payloads.
- Add tests proving product boundary payloads validate and remain separate from engine internals.
- Add a minimal application boundary module or service facade that calls the existing engine workflow without changing engine artifact shapes.
- Define how product-facing run summaries reference generated engine artifacts.
- Document how the next persistence and application-surface milestones should consume the boundary.

Out of scope:
- Database or filesystem persistence for user-created workspaces.
- Web UI.
- API server.
- Authentication.
- Real personal document upload.
- OCR or source document parsing.
- State returns.
- Official IRS PDF generation.
- New tax computation coverage.
- Changing existing engine artifact schemas unless a contract gap is found and explicitly replanned.

## Contracts

Product model decisions:
- A workspace is user-owned.
- A workspace is specific to one tax year.
- A workspace has a jurisdiction list. Only `federal` is supported now, but the list leaves room for future state scopes inside the same tax-year workspace.
- Source drafts exist in a workspace context. They are not independent top-level product records.
- Source drafts are editable product records with `draft_id`, `revision_id`, and lifecycle status.
- Draft lifecycle status starts with `active` and `archived`.
- A run payload is an immutable execution snapshot derived from workspace source drafts.
- Source draft snapshots are part of a run payload, not independent product objects.
- A run summary stays small and points to run detail or artifacts.
- Run detail carries the full run payload and artifact references.
- Artifacts are addressed through artifact references with URIs. Committed fixtures must not use absolute local machine paths.
- Product fixtures include `data_classification`, starting with `synthetic_demo`.

Product concept definitions:
- Owner: the product actor that owns tax-year workspaces. This milestone models ownership with `owner_id` only and does not introduce authentication.
- Workspace: the editable, user-owned, tax-year-specific container for source drafts and runs.
- Source draft: an editable workspace-scoped source record in product shape.
- Draft revision: a stable version marker for an editable source draft.
- Run payload: the immutable input snapshot used for one engine execution.
- Run summary: a small history/list payload with run identity, timing, status, input revision references, result counts, and a detail reference.
- Run detail: the detailed run payload and generated artifact reference set.
- Artifact reference: a typed pointer to a generated artifact, addressed by URI and media type.
- Data classification: an explicit marker for whether product data is synthetic demo data or a future personal-data class.

New contracts to add during implementation:
- Product workspace contract.
- Product run payload contract.
- Product run summary contract.
- Product run detail contract.
- Product artifact reference definition, likely as shared schema `$defs` unless a top-level artifact index is clearly useful.

Contract principles:
- Product contracts should wrap or reference engine contracts rather than duplicating engine artifact details.
- Product run summaries should expose stable review information, not raw implementation paths as the only integration surface.
- Engine artifacts remain authoritative for normalized source documents, validation, coverage, resolution, return artifacts, and Markdown reviews.
- Existing engine schemas remain stable unless the milestone plan is revised.
- Any new durable JSON payload must have a schema, validator or loader, synthetic fixture, and tests.

Expected contract shapes:

```text
product workspace
  -> owner_id
  -> workspace_id
  -> tax_year
  -> jurisdictions
  -> data_classification
  -> source_drafts

product run payload
  -> run_id
  -> workspace_id
  -> owner_id
  -> tax_year
  -> jurisdictions
  -> data_classification
  -> source_draft_snapshots

product run summary
  -> run_id
  -> workspace_id
  -> tax_year
  -> created_at
  -> completed_at
  -> status
  -> input_revision_refs
  -> result_summary
  -> detail_ref

product run detail
  -> run_summary
  -> run_payload
  -> artifact_refs
```

Boundary decisions deferred from this milestone:
- Detailed failure model.
- User review workflow state.
- Broad configurability model.
- Broad extensibility model.
- State return execution.

## Fixtures

Primary fixture source:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/
```

Expected new synthetic fixtures:
- Product workspace fixture.
- Product run payload fixture.
- Product run summary fixture.
- Product run detail fixture.

Fixture rules:
- Use only synthetic demo workspace data.
- Use demo labels and obvious synthetic IDs.
- Do not introduce personal taxpayer identifiers.
- Do not include absolute local machine paths in committed fixtures.
- Use relative or logical artifact URIs in committed fixtures.
- Use `data_classification: "synthetic_demo"`.
- Keep generated local outputs under ignored paths such as `local-data/`.

## Verification

Baseline verification:

```bash
python3 -m unittest
```

Contract verification:
- Schema validation tests for every new product boundary JSON contract.
- Loader or validator tests for valid synthetic fixtures.
- Negative tests for invalid or incomplete boundary payloads where behavior depends on validation.

Boundary verification:
- Tests proving the product boundary can execute the existing engine workflow against the synthetic workspace.
- Tests proving product run summaries reference expected engine artifacts.
- Tests proving product boundary code does not mutate engine artifact shapes.

Data safety verification:
- Run the repository data safety check.
- Confirm committed product fixtures contain no absolute local paths.
- Confirm committed product fixtures use only synthetic data.

## Data Safety

This milestone remains synthetic-only.

Do not commit:
- Personal source documents.
- Real uploaded tax documents.
- Personal current-year fact instances.
- Prior returns.
- Generated artifacts derived from personal data.
- Absolute local machine paths in committed product fixtures or run summaries.

Personal or ad hoc local work must stay under ignored paths such as:
- `local-data/`
- `temp/`
- `private-archive/`
- `uploads/`
- `generated/user/`

If implementation introduces broader safety checks for product boundary artifacts, keep them separate from unrelated feature work.

## Exit Criteria

This milestone is complete when:
- Product boundary terminology is documented.
- Product-facing workspace, source draft, run payload, run summary, run detail, and artifact reference decisions are explicit.
- Every new durable JSON product boundary payload has a schema and validator or loader.
- Synthetic fixtures exist for all new product boundary contracts.
- Tests cover valid product boundary payloads.
- Tests cover meaningful invalid product boundary payloads.
- Product boundary execution can call the existing workspace engine flow without changing engine artifact shapes.
- Product run summaries can reference generated validation, coverage, resolution, return artifact, return review, and manifest outputs.
- Documentation explains how the persistence milestone should consume the product boundary.
- Data safety checks pass.
- `python3 -m unittest` passes.

## Tracks

### Track 1: Boundary Inventory And Terminology

Goal:
- Identify the product-facing concepts that wrap the existing engine workflow.

Boundary:
- No schemas, code, persistence, or UI.

Inputs:
- Application Boundary Definition overview and roadmap.
- Engine Contract Stabilization overview and roadmap.
- Existing workspace runner and engine artifacts.

Outputs:
- Product boundary terminology and decisions documented in this milestone plan or a supporting design document.
- Explicit list of product-visible engine artifacts.
- Explicit list of supported source draft types for the first product boundary.
- Explicit confirmation that source drafts are workspace-scoped editable records.
- Explicit confirmation that run payloads carry immutable source draft snapshots.

Verification:
- Planning diff clearly states product concepts and non-goals.

Migration risk:
- None to runtime behavior.

Data safety:
- Documentation only; no personal data.

### Track 2: Product Boundary Schemas

Goal:
- Define durable JSON contracts for product-facing workspace, run, and artifact payloads.

Boundary:
- No persistence.
- No UI.
- No engine artifact shape changes unless the plan is revised.

Inputs:
- Track 1 boundary decisions.
- Existing engine schemas and run manifest.

Outputs:
- New product boundary schemas.
- Valid synthetic fixture payloads.
- Invalid or missing-data fixtures where useful.
- Shared artifact reference definition using URI-based references.

Verification:
- Schema validation tests pass.
- `python3 -m unittest` passes.

Migration risk:
- New contracts only.

Data safety:
- Fixtures must use synthetic demo IDs and portable references.

### Track 3: Product Boundary Validators And Read Models

Goal:
- Add code that loads, validates, and prepares product-facing read models without exposing engine internals as the application contract.

Boundary:
- No storage implementation.
- No API server.
- No UI.

Inputs:
- Product boundary schemas from Track 2.
- Existing engine artifact contracts.

Outputs:
- Loader or validator code for product boundary payloads.
- Product-facing read model builders for workspaces, run payloads, run summaries, run details, and artifact references.
- Unit tests for read model behavior.

Verification:
- Focused unit tests pass.
- `python3 -m unittest` passes.

Migration risk:
- Low if engine artifacts remain unchanged.

Data safety:
- Read models must not introduce absolute local paths into committed fixtures.

### Track 4: Engine Workflow Facade

Goal:
- Provide a minimal application boundary facade that executes the existing engine workflow and returns product-facing run information.

Boundary:
- No durable persistence.
- No web service.
- No UI.
- No new tax computation behavior.

Inputs:
- Product run payload contract.
- Existing workspace runner workflow.
- Product run summary contract.

Outputs:
- Application boundary execution module or service facade.
- Tests proving the facade executes the synthetic workspace.
- Tests proving returned product run summary and detail reference expected artifacts.

Verification:
- Facade tests pass.
- Existing workspace runner tests pass.
- `python3 -m unittest` passes.

Migration risk:
- Medium if path handling or runner orchestration changes; keep changes additive.

Data safety:
- Execution output remains under ignored local paths during tests or uses temporary directories.

### Track 5: Documentation And Next-Milestone Handoff

Goal:
- Document how Local Workspace Persistence should consume the product boundary contracts.

Boundary:
- No persistence implementation.
- No UI implementation.

Inputs:
- Completed product boundary schemas and facade.
- Application Boundary Definition roadmap.

Outputs:
- README or docs updates for the product boundary, if user-facing commands or concepts change.
- Roadmap status updates.
- Notes for Local Workspace Persistence inputs and constraints.

Verification:
- Documentation matches implemented behavior.
- `python3 -m unittest` passes.

Migration risk:
- Documentation-only unless README commands change.

Data safety:
- Documentation must preserve synthetic-only constraints for this phase.
