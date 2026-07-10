# Milestone Plan: Editable Draft Inputs And Reviewable Coverage

## Planning Status

Status: complete.

This milestone plan is backfilled from completed implementation work. It records the contracts, tracks, verification, and exit criteria that were satisfied before the milestone planning protocol existed.

No parallel work manifest is included because this milestone is already complete.

## Objective

Introduce user-editable source document drafts and reviewable coverage outputs while keeping canonical engine inputs stable.

## Current State

Implemented and complete.

The milestone produced:
- Editable source document draft schema.
- Draft-to-canonical normalization.
- Source revision refresh semantics.
- Coverage read models.
- Coverage inspection runner.
- Markdown coverage output.
- Draft-to-coverage workflow.
- Coverage summary projection.
- Source validation reports.
- Readable source attribution labels.

## Scope

In scope:
- Sparse editable source document draft values.
- Normalization into canonical source documents.
- Source revision propagation.
- Grouped and field-detail coverage read models.
- Markdown coverage rendering.
- Validation reporting for source documents.
- Human-readable attribution labels.

Out of scope:
- Workspace manifests.
- Run manifests.
- Computed field execution.
- Return artifact generation.
- Persistence.
- UI.
- Real personal data.

## Contracts

Contracts introduced or extended:
- `source-document-draft` schema.
- Source document schema with source revision support.
- Coverage read model shape.
- Source validation report shape.

Definitions used:
- Source field definitions for W-2 and 1099-INT.

## Fixtures

Synthetic fixtures:
- Basic W-2 draft.
- Updated W-2 draft.
- W-2 draft missing required source data.
- Basic 1099-INT draft.
- Optional withholding absent scenarios.

Fixture rules satisfied:
- Synthetic IDs and labels.
- No personal tax documents.
- No absolute local paths.

## Tracks

### Track 5: Field Coverage Runner

Goal:
- Add executable coverage generation from canonical source documents.

Outputs:
- `build_field_coverage` runner.
- Output path support.
- Sample coverage fixture.

Verification:
- Runner subprocess tests.

### Track 6: Source Document Drafts

Goal:
- Separate user-editable draft input shape from canonical source document shape.

Outputs:
- Draft schema.
- Draft normalization.
- Draft normalization runner.

Verification:
- Draft schema tests.
- Draft normalization tests.
- Draft runner tests.

### Track 7: Source Revision Refresh Semantics

Goal:
- Propagate source revisions through mapped output and coverage so edited records can refresh attribution.

Outputs:
- `source_revision_id` on drafts and canonical source documents.
- Revision-aware source attribution.

Verification:
- Tests proving updated source values refresh mapped values and attribution.

### Track 8: Coverage Read Models

Goal:
- Make coverage reviewable by form and by selected field.

Outputs:
- Grouped coverage read model.
- Field-detail read model.
- Coverage inspection runner.

Verification:
- Read model tests.
- Inspection runner tests.

### Track 9: Draft-To-Coverage Workflow

Goal:
- Generate coverage directly from editable drafts.

Outputs:
- Draft coverage workflow.
- Draft coverage runner.

Verification:
- Draft coverage tests.
- Runner subprocess tests.

### Track 10: Coverage Summary Projection

Goal:
- Summarize coverage status counts for easier review.

Outputs:
- Coverage summary projection.
- Summary section in Markdown coverage output.

Verification:
- Coverage summary tests.

### Track 11: Source Validation Report

Goal:
- Report missing required source data after schema validation and normalization.

Outputs:
- Source validation report.
- JSON and Markdown validation output.
- Validation runner.

Verification:
- Source validation tests.
- Validation runner tests.

### Track 12: Readable Source Attribution Labels

Goal:
- Make attribution useful to humans while preserving stable IDs.

Outputs:
- Source document labels in attribution.
- Source field labels in attribution.
- Updated Markdown coverage source rendering.

Verification:
- Updated direct mapping, coverage, read model, and runner tests.

## Verification

Milestone verification:

```bash
python3 -m unittest
```

Representative draft-to-coverage verification:

```bash
python3 -m packages.tax_engine.runners.build_coverage_from_drafts \
  --draft packages/sample_data/source_document_drafts/w2_basic_draft.2025.json \
  --draft packages/sample_data/source_document_drafts/1099_int_basic_draft.2025.json \
  --format markdown
```

## Exit Criteria

Completed when:
- Drafts validate against schema.
- Drafts normalize into canonical source documents.
- Canonical documents validate after normalization.
- Source revisions propagate through coverage.
- Coverage can be inspected by form and field.
- Coverage can be rendered as Markdown.
- Missing required source data can be reported.
- Attribution includes stable IDs and readable labels.
- Tests pass.
- Committed fixtures remain synthetic and portable.
