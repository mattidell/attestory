# Engine Contract Stabilization Overview

## Purpose

Engine Contract Stabilization establishes the reliable core of the tax record workflow. It turns synthetic federal source document drafts into validated source records, maps and resolves federal form fields, and produces deterministic artifacts that future product surfaces can trust.

The phase creates the engine boundary for a shareable portfolio application: clear schemas, repeatable runners, safe fixtures, golden artifacts, and reviewable outputs.

## Product Framing

The system captures source document data, normalizes that data into auditable records, maps and computes federal form fields, and emits reviewable artifacts for a tax record workflow.

## Scope

In scope:
- Synthetic federal tax-year workspaces.
- Source document drafts for W-2 and 1099-INT.
- Normalization into canonical source documents.
- Schema validation for durable artifacts.
- Direct source-to-form mappings.
- Computed field definitions for a small federal field set.
- Field coverage and field resolution artifacts.
- Workspace run manifests.
- Golden fixture tests.
- Human-readable review artifacts for generated outputs.

Out of scope:
- Real personal tax data.
- State returns.
- Authentication.
- Database persistence.
- Web UI.
- API service.
- File upload storage.
- OCR/document parsing.
- Official IRS PDF generation.
- E-file submission.

This scope proves the core workflow before the project adds product surfaces. Synthetic workspaces and schemas make the engine safe to develop publicly, direct mappings and computed fields prove the record-to-form transformation path, and golden artifacts give future application work a stable contract to integrate against.

## Current Workflow

Implemented workflow:

```text
tax workspace
  -> source document drafts
  -> canonical source documents
  -> source validation
  -> direct source mappings
  -> field coverage
  -> field resolution
  -> return artifact
  -> return review
  -> run manifest
```

Canonical runner:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

## Definition Of Done

This phase is done when:
- The workspace runner produces normalized source documents.
- The workspace runner produces source validation.
- The workspace runner produces field coverage.
- The workspace runner produces field resolution.
- The workspace runner produces a run manifest.
- The workspace runner produces a normalized return artifact.
- The workspace runner produces a human-readable return review.
- Durable artifacts have schemas where appropriate.
- The basic synthetic workspace has committed golden expected artifacts.
- Golden tests compare generated artifacts to expected artifacts.
- The full test suite passes with `python3 -m unittest`.
- Committed fixtures contain only synthetic data.
- Committed fixtures contain no absolute local machine paths.
- Documentation explains the canonical workflow and phase boundary.

## Exit Criteria

The project may leave this phase when:
- The definition of done above is satisfied.
- The active phase roadmap marks Engine Contract Stabilization complete.
- `docs/phases/application-boundary-definition/application-boundary-definition-overview.md` is confirmed as the next active phase overview.
- Superseded planning documents are archived.
- Any consumer-facing changelog plan or root `CHANGELOG.md` direction is resolved, if release-style versioning begins.

## Data Safety

Personal data remains outside committed project artifacts for this phase.

Do not commit:
- Personal source documents.
- Real uploaded tax documents.
- Personal current-year fact instances.
- Prior returns.
- Generated artifacts derived from personal data.
- Absolute local paths in golden fixtures or manifests.

Personal experiments, if any, must live under ignored paths such as `local-data/` and must not be used to update committed expected artifacts.

## Verification Baseline

Baseline verification:

```bash
python3 -m unittest
```

For runner changes, also run the canonical workspace runner manually or through a subprocess test.

Golden fixture changes must be intentional and reviewed as artifact contract changes.
