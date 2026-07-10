# Tax Records & Computation Prototype

This project is a prototype tax records system for capturing source document data, normalizing it into auditable records, mapping source fields to federal tax form fields, and preserving the intermediate artifacts used to explain computation history.

It is not a tax filing product or a complete tax return generator. The current Engine Contract Stabilization phase focuses on federal source-document records, direct source-to-form mappings, field coverage, validation, field resolution, normalized return artifacts, and reviewable outputs.

## Current Direction

The Engine Contract Stabilization phase established the federal engine workflow:

- Synthetic W-2 and 1099-INT source document fixtures.
- A source document model independent of personal tax files.
- Direct mappings from source fields to in-scope federal tax form fields.
- Computed field definitions for a small set of dependency-driven federal fields.
- A federal field coverage projection that distinguishes populated, missing, computed, and optional fields.
- A normalized federal return artifact and Markdown return review for the synthetic workspace.

The current Application Boundary Definition phase defines product-facing contracts around that workflow before adding persistence or UI. The first completed product boundary milestone adds user-owned tax-year workspace contracts, workspace-scoped editable source drafts, immutable run payload snapshots, run summaries, run details, URI-addressed artifact references, and synthetic demo data classification.

Personal tax documents, current fact instances, and generated personal artifacts do not belong in this branch.

## Setup

Install the prototype dependencies before running tests or runners:

```bash
python3 -m pip install -r requirements.txt
```

## Runners

### Tests
Run all tests:

```bash
python3 -m unittest
```

Run the current application-boundary type-check baseline:

```bash
python3 -m mypy
```

### Workspace
Run a workspace workflow and write all current workflow artifacts:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

The workspace runner writes `normalized-source-documents.json`, `source-validation.json`, `field-coverage.json`, `field-resolution.json`, `return-artifact.json`, `return-artifact.md`, and `field-coverage.md`.

It also writes `run-manifest.json`, which records the workspace input, source draft inputs, output artifacts, run ID, engine version, and run timestamp. Use `--run-id` and `--created-at` when deterministic manifest metadata is needed for fixtures or tests.

To preserve multiple runs under one output root, add `--timestamp-run`. The runner will write artifacts into a filesystem-safe created-at timestamp directory inside `--output-dir`:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025 \
  --timestamp-run
```

### Other Runners
Build federal field coverage from synthetic source documents:

```bash
python3 -m packages.tax_engine.runners.build_field_coverage \
  --source-document packages/sample_data/source_documents/w2_basic.2025.json \
  --source-document packages/sample_data/source_documents/1099_int_basic.2025.json \
  --output local-data/coverage.json
```

Omit `--output` to write coverage JSON to stdout. Add `--compact` for compact JSON output.

Normalize an editable source document draft into the canonical source document shape:

```bash
python3 -m packages.tax_engine.runners.normalize_source_document_draft \
  --draft packages/sample_data/source_document_drafts/w2_basic_draft.2025.json \
  --output local-data/w2-source-document.json
```

Omit `--output` to write the normalized source document JSON to stdout.

Inspect an existing field coverage JSON artifact as a grouped read model:

```bash
python3 -m packages.tax_engine.runners.inspect_field_coverage \
  --coverage packages/sample_data/field_coverage/basic_coverage.2025.json
```

Inspect one field detail:

```bash
python3 -m packages.tax_engine.runners.inspect_field_coverage \
  --coverage packages/sample_data/field_coverage/basic_coverage.2025.json \
  --field-id irs.2025.f1040.line1a
```

Render coverage in a friendlier Markdown format:

```bash
python3 -m packages.tax_engine.runners.inspect_field_coverage \
  --coverage packages/sample_data/field_coverage/basic_coverage.2025.json \
  --format markdown
```

Build field coverage directly from editable source document drafts:

```bash
python3 -m packages.tax_engine.runners.build_coverage_from_drafts \
  --draft packages/sample_data/source_document_drafts/w2_basic_draft.2025.json \
  --draft packages/sample_data/source_document_drafts/1099_int_basic_draft.2025.json \
  --output local-data/draft-coverage.json
```

Render draft-based coverage as Markdown:

```bash
python3 -m packages.tax_engine.runners.build_coverage_from_drafts \
  --draft packages/sample_data/source_document_drafts/w2_basic_draft.2025.json \
  --draft packages/sample_data/source_document_drafts/1099_int_basic_draft.2025.json \
  --format markdown
```

Validate source document drafts before mapping:

```bash
python3 -m packages.tax_engine.runners.validate_source_documents \
  --draft packages/sample_data/source_document_drafts/w2_missing_required_box1_draft.2025.json \
  --format markdown
```

## Workspace Fixtures

Workspace fixtures define end-to-end synthetic tax record scenarios without adding persistence or UI assumptions. A workspace currently lists the source document draft inputs for one federal tax-year scenario:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json
```

The workspace fixture also includes committed expected artifacts under `expected/`. These golden files define the current end-to-end contract for the basic synthetic scenario and are covered by regression tests.

## Local Workspace Persistence

The Application Boundary Definition phase includes a local filesystem persistence boundary for product workspaces. It is exposed as repository/service code, not as a command-line runner.

The local persistence layer stores product workspaces, source draft revisions, immutable run payloads, run summaries, run details, and generated engine artifacts under a caller-provided storage root. Local experiments should use ignored paths such as:

```text
local-data/workspaces/
```

The storage layout is:

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

Listings are derived from stored records and directory contents. Source draft updates create new revision files and update `latest.json` pointer metadata. Completed runs are immutable; the latest run view is derived from stored run summary timestamps.

Committed local persistence fixtures are synthetic and live under:

```text
packages/sample_data/local_workspace_persistence/basic_2025/
```

## Workspace Workflow Service

The Application Boundary Definition phase also exposes a small class-based service layer over local persistence:

```python
from packages.tax_engine.workspace_workflow_service import WorkspaceWorkflowService

service = WorkspaceWorkflowService(storage_root="local-data/workspaces")
```

The service returns explicit operation result objects for workspace creation and lookup, source draft creation, immutable source draft revision creation, exact and latest draft revision reads, draft history listing, draft archiving, exact-revision run execution, latest-revision convenience runs, run history, run detail, latest-run-with-detail lookup, and artifact reference resolution.

Exact source draft revision IDs are the stable run execution contract. Latest-revision execution is available as a convenience for local application workflows.
