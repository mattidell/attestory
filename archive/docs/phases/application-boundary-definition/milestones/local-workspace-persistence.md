# Milestone Plan: Local Workspace Persistence

## Planning Status

Status: complete milestone plan; implementation complete.

This milestone plan was reviewed, confirmed complete, committed, and implemented.

No parallel work manifest is included. Add one only if the user or orchestrating developer explicitly requests parallel execution planning for this milestone.

## Objective

Persist product workspaces, editable source draft records, run metadata, and generated artifact references locally so the application boundary can maintain user-created work over time without changing engine artifact contracts.

This milestone proves the storage boundary for the product model. It does not build the final UI or introduce personal-data intake.

## Current State

Implemented product boundary:
- Product workspace schema and validator.
- Product run payload schema and validator.
- Product run summary schema and validator.
- Product run detail schema and validator.
- URI-addressed artifact references.
- Synthetic demo product boundary fixtures.
- A product boundary execution facade that runs the stabilized engine workflow from immutable run payload snapshots.

Stable product boundary fixture directory:

```text
packages/sample_data/product_boundary/
```

Stable engine runner:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

Important existing decisions:
- Product workspaces are user-owned tax-year containers.
- Source drafts are workspace-scoped editable records.
- Run payloads are immutable snapshots derived from workspace source draft revisions.
- Run summaries are small history records that point to run details and generated artifacts.
- Generated engine artifacts remain authoritative for validation, coverage, resolution, return artifact, and Markdown review content.
- Committed fixtures must use synthetic demo data and portable references.

## Scope

In scope:
- Define a local storage layout for product workspaces, source drafts, runs, run details, and generated artifact files.
- Add durable schemas or schema updates for storage-owned indexes or manifests if the storage layer creates new JSON artifacts.
- Add local repository code that creates, reads, updates, and lists product workspaces and source drafts.
- Add local repository code that records run payloads, run summaries, run details, and generated engine artifacts after product boundary execution.
- Add deterministic synthetic storage fixtures that prove the storage layout and repository behavior.
- Add tests for create, load, update, list, run recording, artifact reference resolution, and data safety.
- Add service functions needed to exercise the local persistence workflow from tests and future application code.
- Update documentation for the local storage layout and supported workflow.

Out of scope:
- Web UI.
- API server.
- Authentication or user account management beyond existing `owner_id`.
- Database server setup.
- Real personal document upload.
- OCR or source document parsing.
- State returns.
- New tax computation coverage.
- Official IRS PDF generation.
- Changing engine artifact schemas.
- Changing product boundary schemas unless a storage boundary gap is found and explicitly replanned.
- New command-line runner.
- Partial-write recovery or durable failed-run records.

## Contracts

Storage model decisions:
- Local persistence should consume the existing product boundary contracts instead of inventing parallel workspace or run shapes.
- The first storage backend should be filesystem-based and deterministic.
- Workspace and run listings should be derived from stored records and directory contents instead of a separate index unless implementation proves an index is necessary.
- The storage root must be configurable by caller, test, or runner, with local ad hoc defaults under ignored paths such as `local-data/workspaces/`.
- Committed storage fixtures should live under `packages/sample_data/` and contain only synthetic demo data.
- Storage-owned references should remain relative to the storage root or use logical URI prefixes. Committed fixtures must not contain absolute local machine paths.
- Source draft updates should create a new `revision_id` rather than mutating the meaning of an existing revision.
- Source draft `latest.json` should be a small pointer or metadata file for the latest revision, not a duplicate copy of the draft payload.
- Completed run records should be append-only after completion. Corrective behavior should create a new run rather than rewriting a completed run record, except for clearly documented test fixture regeneration.
- The current or latest run view should be derived from immutable run history, initially by stored run summary timestamps, instead of maintained as a mutable current-run record.
- Artifact references in product run summaries and run details should keep the current relative product URI shape, such as `runs/<run-id>/...`. The storage layer may resolve those URIs to local paths internally but should not expose absolute paths through committed product records.
- The storage layer should keep generated engine artifacts separate from editable workspace records.
- Committed synthetic storage fixtures should focus on storage and product records. Generated artifact persistence should be tested through temporary directories unless a later golden coverage decision explicitly requires a full committed artifact tree.
- This milestone should not add a new runner.
- Partial-write recovery is deferred. Implementation should avoid durable failed or partial run records for now.

Expected local storage shape:

```text
<storage-root>/
  workspaces/
    <owner-id>/
      <workspace-id>/
        workspace.json
        source-drafts/
          <draft-id>/
            <revision-id>.json
            latest.json
        runs/
          <run-id>/
            product-run-payload.json
            product-run-summary.json
            product-run-detail.json
            artifacts/
              normalized-source-documents.json
              source-validation.json
              field-coverage.json
              field-resolution.json
              return-artifact.json
              return-artifact.md
              field-coverage.md
              run-manifest.json
```

Expected repository capabilities:
- Create a product workspace record.
- Load one product workspace record.
- List workspaces for an owner.
- Add or update a source draft revision in a workspace.
- Load the latest source draft revision.
- Build an immutable product run payload from current workspace draft revisions.
- Execute the product boundary workflow.
- Persist the run payload, run summary, run detail, and generated engine artifacts.
- List run summaries for a workspace.
- Derive the latest run summary for a workspace from immutable stored run summaries.
- Load run detail and resolve artifact references for local inspection.

New contracts to consider during implementation:
- Local storage manifest or workspace index, only if listing cannot be derived safely and deterministically from existing product records.
- Source draft latest pointer metadata, if `latest.json` becomes a durable storage-owned JSON artifact.
- Stored artifact index, if product run detail does not provide enough information for storage-local resolution.

Contract principles:
- Prefer deriving indexes from existing product records unless a manifest materially improves clarity or verification.
- Avoid new storage-owned JSON schemas unless `latest.json`, storage manifests, artifact indexes, or another storage artifact becomes durable. Any new durable JSON payload must have a schema, validator or loader, synthetic fixture, and tests.
- Product boundary contracts remain the application-facing payloads.
- Storage internals should not leak into engine artifacts.
- Engine workflow output names should match existing runner artifact names.

Deferred decisions:
- Encryption.
- Multi-user authentication.
- Cross-device synchronization.
- Import/export packaging.
- Deletion and retention policy for personal data.
- Migration tooling for future schema versions.
- Failure and partial-run recovery.

## Fixtures

Primary product fixture source:

```text
packages/sample_data/product_boundary/
```

Expected new synthetic fixtures:
- Local storage root fixture for the basic 2025 demo workspace.
- Stored workspace fixture.
- Stored source draft revision fixtures.
- Stored run summary fixture.
- Stored run detail fixture.
- Stored generated artifact fixtures only if golden coverage explicitly requires a full committed artifact tree.

Fixture rules:
- Use only synthetic demo workspace data.
- Use demo labels and obvious synthetic IDs.
- Use `data_classification: "synthetic_demo"`.
- Do not introduce personal taxpayer identifiers.
- Do not include absolute local machine paths.
- Keep ad hoc generated output under ignored paths such as `local-data/`.
- Golden fixture updates must be intentional and reviewed.

## Verification

Baseline verification:

```bash
python3 -m unittest
```

Storage verification:
- Tests validate any new storage-owned schema fixtures.
- Repository tests create and load workspaces from a temporary storage root.
- Repository tests add source draft revisions without mutating prior revisions.
- Repository tests build run payloads from the latest source draft revisions.
- Repository tests execute and persist the synthetic product run.
- Repository tests list run summaries in deterministic order.
- Repository tests load run detail and resolve artifact references without exposing absolute paths in stored product records.

Data safety verification:
- Run the repository data safety check.
- Confirm committed storage fixtures contain no absolute local paths.
- Confirm committed storage fixtures use only synthetic demo data.
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
- Absolute local machine paths in committed fixtures, manifests, run summaries, or run details.

Personal or ad hoc local work must stay under ignored paths such as:
- `local-data/`
- `temp/`
- `private-archive/`
- `uploads/`
- `generated/user/`

The storage root must be caller-controlled so tests can use temporary directories and local experiments can remain ignored.

## Exit Criteria

This milestone is complete when:
- The local storage layout is implemented and documented.
- Product workspaces can be created, loaded, and listed locally.
- Workspace-scoped source drafts can be saved as revisions and loaded by latest revision.
- Product run payloads can be built from persisted draft revisions.
- Product boundary execution can persist run payload, run summary, run detail, and generated engine artifacts.
- Run summaries can be listed for a persisted workspace.
- Run detail and artifact references can be loaded for local inspection.
- Every new durable JSON storage artifact has a schema and validator or loader.
- Synthetic fixtures cover the local storage workflow.
- Tests cover create, update, list, run recording, artifact reference resolution, and data safety.
- Documentation explains the local persistence workflow and storage root expectations.
- `python3 -m unittest` passes.

## Tracks

### Track 1: Storage Layout And Contract Inventory

Goal:
- Define the filesystem storage layout and identify whether storage-owned JSON contracts are needed.

Boundary:
- No runtime storage implementation.
- No product boundary schema changes unless a gap is documented.

Inputs:
- Product boundary schemas and fixtures.
- Product boundary execution facade.
- Existing workspace runner artifact names.
- Application Boundary Definition roadmap.

Outputs:
- Finalized storage layout documented in this milestone plan or a supporting design note.
- Explicit list of storage-owned durable artifacts.
- Explicit list of product boundary contracts reused unchanged.
- Decision on whether a storage manifest or index schema is needed.

Verification:
- Planning diff clearly states storage contracts, non-goals, and data safety rules.

Migration risk:
- None to runtime behavior.

Data safety:
- Documentation only; no personal data.

### Track 2: Local Repository Core

Goal:
- Add filesystem repository code for product workspace and source draft persistence.

Boundary:
- No run execution persistence yet.
- No UI or API.
- No database server.

Inputs:
- Storage layout from Track 1.
- Product workspace schema.
- Source document draft schema.

Outputs:
- Local storage module or repository.
- Create, load, and list workspace operations.
- Save source draft revision operation.
- Load latest source draft revision operation.
- Focused repository tests using temporary directories.

Verification:
- Focused repository tests pass.
- `python3 -m unittest` passes.

Migration risk:
- Low if storage code is additive.

Data safety:
- Tests use temporary directories and synthetic payloads.
- Stored product records must not expose absolute local paths.

### Track 3: Run Recording And Artifact Persistence

Goal:
- Persist product run records and generated engine artifacts from the product boundary execution facade.

Boundary:
- No new tax computation behavior.
- No changes to engine artifact schemas.
- No broad failure recovery model beyond deterministic local writes.

Inputs:
- Local repository core from Track 2.
- Product run payload, summary, and detail contracts.
- Product boundary execution facade.
- Engine artifact names from existing runners.

Outputs:
- Build run payload from persisted workspace draft revisions.
- Execute product run payload.
- Persist run payload, summary, detail, and generated engine artifacts.
- List run summaries for a workspace.
- Load run detail for a workspace.
- Resolve artifact references to local files internally.
- Tests for run recording and artifact persistence.

Verification:
- Focused run recording tests pass.
- Existing product boundary tests pass.
- `python3 -m unittest` passes.

Migration risk:
- Medium if artifact naming or path handling overlaps with existing runner behavior; keep integration additive.

Data safety:
- Persisted product records use relative or logical URIs.
- Local path resolution stays internal and out of committed fixture payloads.

### Track 4: Synthetic Storage Fixtures And Golden Coverage

Goal:
- Add deterministic synthetic fixtures that represent the local persistence workflow.

Boundary:
- Do not regenerate unrelated engine golden artifacts.
- Do not introduce personal or private data.

Inputs:
- Repository behavior from Tracks 2 and 3.
- Existing product boundary fixtures.
- Existing synthetic workspace expected artifacts.

Outputs:
- Synthetic local storage fixture tree or equivalent fixture payloads.
- Golden expected stored run records and artifact references.
- Tests that validate committed storage fixtures.
- Data safety assertions for storage fixtures.

Verification:
- Storage fixture validation tests pass.
- Data safety tests pass.
- `python3 -m unittest` passes.

Migration risk:
- Medium because committed fixtures become durable contracts; review diffs carefully.

Data safety:
- Fixtures must use synthetic demo IDs and no absolute local paths.

### Track 5: Runner And Documentation Handoff

Goal:
- Document local workspace persistence and hand off to the Application Surface milestone.

Boundary:
- No UI.
- No API server.
- No personal-data intake.
- No new runner.

Inputs:
- Completed local repository workflow.
- Storage fixtures and tests.
- README runner conventions.
- Application Boundary Definition roadmap.

Outputs:
- README or docs updates for local storage root, commands, and ignored output paths.
- Roadmap status updates and next-milestone handoff notes.

Verification:
- Documentation matches implemented behavior.
- `python3 -m unittest` passes.

Migration risk:
- Low if documentation and runner behavior are additive.

Data safety:
- Document ignored local output paths.
- Do not document commands that encourage committing local personal data.
