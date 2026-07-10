<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Production Layer

The production layer records the return state produced by a run. It should answer what was produced, while run trace artifacts answer how and why.

## Layer Graph

```text
FieldResolution
  -> ReturnInstance

ComputationTrace
  -> ReturnInstance

FormDefinitionCatalog
  -> ReturnInstance

ReturnInstance
  -> ReturnArtifact
  -> ProductRunSummary

ReturnArtifact
  -> RunManifest
```

## Core Edges

### FieldResolution -> ReturnInstance

Edge type:
- production
- audit

Meaning:
- The return instance is assembled from resolved fields and tables.

Audit value:
- Field resolution explains resolved, blocked, optional, overridden, suppressed, or unavailable output states.

### ComputationTrace -> ReturnInstance

Edge type:
- audit

Meaning:
- Computation trace explains how computed return values were produced.

Notes:
- The return instance should remain the produced return state. It should not need to embed the full computation trace.

### FormDefinitionCatalog -> ReturnInstance

Edge type:
- production

Meaning:
- The return instance conforms to the form and field definitions for its tax year and jurisdiction.

### ReturnInstance -> ReturnArtifact

Edge type:
- production

Meaning:
- The return artifact is a durable output package or normalized projection generated from the return instance.

### ReturnInstance -> ProductRunSummary

Edge type:
- production

Meaning:
- The run summary reports produced return state counts and status.

### ReturnArtifact -> RunManifest

Edge type:
- production

Meaning:
- Run manifest indexes the return artifact as one generated artifact of the run.

## ReturnInstance

Durability:
- `run_snapshot`

Category:
- `production`

Purpose:
- Captures the produced return state for one run: form values, table values, statuses, context, and source run identity.
- Answers what return state was produced, not the full explanation of how it was produced.

Consumes:
- `ProductRunPayload`
- `FieldResolution`
- `FormDefinitionCatalog`

Audit context:
- `ComputationTrace`

Feeds:
- `ReturnArtifact`
- `ProductRunSummary`

Boundary owner:
- `return_production`

Schema status:
- `new_required`

Manifest role:
- `run_output`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## ReturnArtifact

Durability:
- `run_snapshot`

Category:
- `production`

Purpose:
- Provides the durable return-output package or normalized return projection generated from the return instance.

Consumes:
- `ReturnInstance`

Feeds:
- `RunManifest`

Boundary owner:
- `return_production`

Schema status:
- `revise_existing`

Manifest role:
- `run_output`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`
