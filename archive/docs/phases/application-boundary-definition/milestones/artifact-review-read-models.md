# Milestone Plan: Artifact Review Read Models

## Planning Status

Status: draft future milestone plan; implementation not started.

This milestone should start after Workspace Workflow Service is implemented, verified, and committed.

No parallel work manifest is included. Add one only if the user or orchestrating developer explicitly requests parallel execution planning for this milestone.

## Objective

Create product-facing read models for persisted validation, field coverage, field resolution, return artifact, and Markdown review outputs so application code can inspect and render review information without coupling to raw engine artifact files.

This milestone proves the review boundary while keeping generated engine artifacts authoritative.

## Current State

Expected prerequisites:
- Local workspace persistence stores generated engine artifacts for completed runs.
- Workspace Workflow Service can load run details and resolve artifact references.
- Engine artifacts remain stable and covered by golden fixture tests.

Relevant existing artifacts:
- `source-validation.json`
- `field-coverage.json`
- `field-resolution.json`
- `return-artifact.json`
- `return-artifact.md`
- `field-coverage.md`
- `run-manifest.json`

## Scope

In scope:
- Define the review views needed by a product surface for validation, coverage, resolution, return summary, and Markdown review content.
- Add read-model builders that consume persisted engine artifacts through artifact references.
- Add stable in-memory or durable read-model shapes as needed.
- Add schemas and validators if any read model becomes a durable JSON artifact.
- Add synthetic fixtures and tests for read-model generation.
- Add tests proving read models reflect persisted artifacts without mutating engine artifact contracts.
- Update docs to describe the artifact review boundary.

Out of scope:
- Web UI.
- API server.
- Editing computed results through review views.
- New tax computation coverage.
- Official IRS PDF generation.
- Changing engine artifact schemas.
- Changing product boundary or storage contracts unless a gap is found and explicitly replanned.
- Broad reporting or analytics.

## Contracts

Review model decisions:
- Engine artifacts remain authoritative.
- Read models are derived projections for application inspection and rendering.
- Read models should prefer stable identifiers already present in engine artifacts, such as field IDs, artifact types, source document IDs, and run IDs.
- Read models should preserve enough provenance for users to trace review data back to the run and artifact reference.
- Markdown review content may remain text content; do not invent a rich text contract unless the application surface requires it.
- Missing artifact behavior should be explicit and tested.
- If read models are stored durably, they require schemas, validators or loaders, fixtures, and data safety tests.

New contracts to consider during implementation:
- Product validation review read model.
- Product coverage review read model.
- Product resolution review read model.
- Product return summary read model.
- Product Markdown review content wrapper.

Contract principles:
- Keep read models smaller and more UI-friendly than raw engine artifacts.
- Do not duplicate entire engine artifacts unless that duplication is explicitly useful.
- Prefer derived read models over modifying engine artifact shapes.
- Keep committed review fixtures synthetic and portable.

## Fixtures

Expected fixture strategy:
- Use persisted synthetic run artifacts from temporary storage roots for most tests.
- Add committed read-model fixtures only if read models become durable JSON contracts.
- Reuse the basic W-2 and 1099-INT synthetic scenario.

Fixture rules:
- Use only synthetic demo workspace data.
- Use demo labels and obvious synthetic IDs.
- Use `data_classification: "synthetic_demo"` when product payloads are involved.
- Do not introduce personal taxpayer identifiers.
- Do not include absolute local machine paths.
- Keep ad hoc generated output under ignored paths such as `local-data/`.

## Verification

Baseline verification:

```bash
python3 -m unittest
```

Read-model verification:
- Tests build validation review models from persisted validation artifacts.
- Tests build coverage review models from persisted coverage artifacts.
- Tests build resolution review models from persisted resolution artifacts.
- Tests build return summary review models from persisted return artifacts.
- Tests load Markdown review content through artifact references.
- Tests cover missing artifact behavior.
- Tests prove engine artifact fixtures and schemas remain unchanged.

Data safety verification:
- Run the repository data safety check.
- Confirm committed read-model fixtures contain no absolute local paths.
- Confirm committed read-model fixtures use only synthetic demo data.
- Confirm generated local outputs stay under ignored paths.

## Data Safety

This milestone remains synthetic-only.

Do not commit:
- Personal source documents.
- Real uploaded tax documents.
- Personal current-year fact instances.
- Personal manual entries.
- Prior returns.
- Generated artifacts derived from personal data.
- Absolute local machine paths in committed fixtures, manifests, run summaries, run details, or review models.

Personal or ad hoc local work must stay under ignored paths such as:
- `local-data/`
- `temp/`
- `private-archive/`
- `uploads/`
- `generated/user/`

## Exit Criteria

This milestone is complete when:
- Product-facing review read models exist for validation, coverage, resolution, return summary, and Markdown review content.
- Application code can load review data through run detail and artifact references instead of raw path assumptions.
- Tests cover read-model generation and missing artifact behavior.
- Any durable read-model JSON payload has a schema and validator or loader.
- Documentation describes the review boundary.
- Data safety tests pass.

## Tracks

Track 1: Review boundary design
- Goal: define the review read models and decide which shapes are durable.
- Boundary: do not change engine artifacts.
- Inputs: persisted run detail and engine artifact references.
- Outputs: design notes and initial read-model module structure.
- Verification: focused shape tests.
- Migration risk: low unless durable schemas are introduced.
- Data safety: synthetic fixtures only.

Track 2: Validation and coverage read models
- Goal: expose product-friendly validation and coverage review data.
- Boundary: do not alter source validation or field coverage artifact schemas.
- Inputs: `source-validation.json` and `field-coverage.json`.
- Outputs: builders and tests.
- Verification: synthetic persisted artifact tests.
- Migration risk: medium because these are likely primary UI inputs.
- Data safety: no personal records.

Track 3: Resolution and return read models
- Goal: expose product-friendly field resolution and return summary review data.
- Boundary: do not change field resolution or return artifact schemas.
- Inputs: `field-resolution.json` and `return-artifact.json`.
- Outputs: builders and tests.
- Verification: synthetic persisted artifact tests.
- Migration risk: medium because these summarize computation outputs.
- Data safety: no personal records.

Track 4: Markdown review content access
- Goal: load Markdown review artifacts through product artifact references.
- Boundary: do not invent a rich text editor or document model.
- Inputs: `return-artifact.md` and `field-coverage.md`.
- Outputs: content loader and tests.
- Verification: artifact reference content tests.
- Migration risk: low.
- Data safety: synthetic content only.

Track 5: Documentation and safety verification
- Goal: document review read models and run full verification.
- Boundary: do not introduce UI behavior.
- Inputs: implemented read models.
- Outputs: documentation updates.
- Verification: `python3 -m unittest` and data safety tests.
- Migration risk: low.
- Data safety: explicit fixture review.
