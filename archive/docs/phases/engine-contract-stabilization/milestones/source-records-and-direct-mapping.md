# Milestone Plan: Source Records And Direct Mapping

## Planning Status

Status: complete.

This milestone plan is backfilled from completed implementation work. It records the contracts, tracks, verification, and exit criteria that were satisfied before the milestone planning protocol existed.

No parallel work manifest is included because this milestone is already complete.

## Objective

Establish the first stable engine boundary: synthetic federal source document records can be represented as canonical records and directly mapped to in-scope federal form fields.

## Current State

Implemented and complete.

The milestone produced:
- Canonical source document schema and model.
- Synthetic W-2 and 1099-INT source document fixtures.
- Direct source-to-form mapping definitions.
- Direct mapping execution.
- Federal field catalog.
- Field coverage projection.

## Scope

In scope:
- Synthetic source documents.
- W-2 and 1099-INT source document fields.
- Direct source-to-form mappings.
- Federal field catalog entries needed for the initial mapping slice.
- Field coverage statuses for direct, missing source, optional, and computation-required fields.

Out of scope:
- Editable draft inputs.
- Workspace execution.
- Computed field execution.
- Persistence.
- UI.
- Real personal data.

## Contracts

Contracts introduced:
- `source-document` schema.
- `direct-source-mapping` schema.
- `federal-field-catalog` schema.
- `field-coverage` schema.

Definitions introduced:
- Direct source-to-form mapping definitions.
- Federal field catalog definitions.

## Fixtures

Synthetic fixtures:
- W-2 source document fixture.
- 1099-INT source document fixture.
- Basic field coverage fixture.

Fixture rules satisfied:
- Synthetic IDs and labels.
- No personal tax documents.
- No absolute local paths.

## Tracks

### Track 1: Clean Foundation And Guardrails

Goal:
- Establish a clean shareable branch with personal-data guardrails.

Outputs:
- Clean project skeleton.
- Personal data safety check.
- Planning docs preserved from the initial architecture discussion.

Verification:
- Data safety tests.

### Track 2: Source Document Contract

Goal:
- Define canonical source document records for synthetic federal source data.

Outputs:
- Source document schema.
- Source document loader/model.
- Synthetic W-2 and 1099-INT fixtures.

Verification:
- Source document schema/model tests.

### Track 3: Direct Source Mapping

Goal:
- Map canonical source document fields directly to federal destination fields where no computation is required.

Outputs:
- Direct source mapping schema.
- Direct mapping definition file.
- Direct mapping runner.
- Source attribution in mapping output.

Verification:
- Direct mapping contract tests.
- Direct mapping runner tests.

### Track 4: Federal Field Coverage

Goal:
- Project mapped values and field catalog metadata into a coverage artifact.

Outputs:
- Federal field catalog schema.
- Federal field catalog definition.
- Field coverage schema.
- Field coverage projection.

Verification:
- Field catalog tests.
- Field coverage projection tests.

## Verification

Milestone verification:

```bash
python3 -m unittest
```

Coverage runner verification:

```bash
python3 -m packages.tax_engine.runners.build_field_coverage \
  --source-document packages/sample_data/source_documents/w2_basic.2025.json \
  --source-document packages/sample_data/source_documents/1099_int_basic.2025.json \
  --output local-data/coverage.json
```

## Exit Criteria

Completed when:
- Source documents validate against schema.
- Direct mapping definitions validate against schema.
- Federal field catalog validates against schema.
- Field coverage validates against schema.
- Directly mapped fields include values and source attribution.
- Missing required source data is represented explicitly.
- Optional unpopulated source data is represented explicitly.
- Tests pass.
- Committed fixtures remain synthetic and portable.
