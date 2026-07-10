<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Product Layer

The product layer owns workspace and run lifecycle artifacts. It does not own tax semantics or computation rules.

## Layer Graph

```text
ProductWorkspace
  -> ProductRunPayload
  -> ManualFactEntryBatch
  -> ProductContributionPayload

ProductRunPayload
  -> ProductRunSummary
  -> RunManifest
  -> FactCoverage
  -> MappingTrace
  -> ComputationTrace
  -> FieldResolution
  -> ReturnInstance

ProductRunSummary
  -> RunManifest

ManualFactEntryBatch
  -> ProductContributionPayload

ProductContributionPayload
  -> SourceRecordSet
  -> ProvenanceRecordSet
  -> FactInstanceSet

FactInstanceSet
  -> ProductRunPayload

FieldResolution
  -> ProductRunSummary
```

## Core Edges

### ProductWorkspace -> ProductRunPayload

Edge type:
- production

Meaning:
- A run payload snapshots the selected workspace state and input revisions for a specific execution.

Notes:
- The workspace remains mutable over time.
- The run payload must be immutable once created.

### ProductWorkspace -> ManualFactEntryBatch

Edge type:
- production

Meaning:
- Manual entry batches are created within a workspace and inherit workspace identity, tax year, jurisdiction, and data classification context.

Notes:
- A run should snapshot exact manual entry revisions rather than reading mutable latest workspace input state.

### ProductRunPayload -> ProductRunSummary

Edge type:
- production

Meaning:
- A run summary records the outcome of executing one run payload.

Notes:
- The summary should reference exact input revisions and generated output counts.

### ProductRunPayload -> RunManifest

Edge type:
- production

Meaning:
- A run manifest belongs to one run payload and indexes the exact inputs, definitions, and generated artifacts for that run.

Notes:
- The manifest should refer to artifacts by stable artifact references, not absolute local paths.

### ProductRunSummary -> RunManifest

Edge type:
- production

Meaning:
- Run manifest embeds or references the corresponding run summary so product surfaces can move from run lists to run inspection.

### ProductWorkspace -> ProductContributionPayload

Edge type:
- production

Meaning:
- Contribution events are workspace-scoped and inherit workspace identity, tax year, jurisdiction, and data classification context.

### ManualFactEntryBatch -> ProductContributionPayload

Edge type:
- production

Meaning:
- The contribution payload freezes the exact manual entry batch ids or revisions submitted for normalization.

### ProductContributionPayload -> SourceRecordSet

Edge type:
- production
- audit

Meaning:
- A contribution event creates or updates the source records for the submitted material.

Audit value:
- The contribution payload explains when and through which submission a source record entered the workspace.

### ProductContributionPayload -> ProvenanceRecordSet

Edge type:
- production
- audit

Meaning:
- A contribution event appends the provenance records for the facts it produced.

Audit value:
- The contribution payload explains the capture context and normalization pass behind provenance records.

### ProductContributionPayload -> FactInstanceSet

Edge type:
- production
- audit

Meaning:
- A contribution event appends the produced fact instances to the canonical ledger.

Audit value:
- The contribution payload explains when and how facts entered the ledger, including supersessions created by corrections.

### FactInstanceSet -> ProductRunPayload

Edge type:
- production

Meaning:
- The run payload records the exact fact instance ids selected from the canonical fact instance set.

### ProductRunPayload -> FactCoverage

Edge type:
- production

Meaning:
- Run outputs derive from the exact inputs selected by the run payload.

### ProductRunPayload -> MappingTrace

Edge type:
- production

Meaning:
- Run outputs derive from the exact inputs selected by the run payload.

### ProductRunPayload -> ComputationTrace

Edge type:
- production

Meaning:
- Run outputs derive from the exact inputs selected by the run payload.

### ProductRunPayload -> FieldResolution

Edge type:
- production

Meaning:
- Run outputs derive from the exact inputs selected by the run payload.

### ProductRunPayload -> ReturnInstance

Edge type:
- production

Meaning:
- Run outputs derive from the exact inputs selected by the run payload.

### FieldResolution -> ProductRunSummary

Edge type:
- production

Meaning:
- The run summary reports result counts and statuses derived from field resolution.

## ProductWorkspace

Durability:
- `canonical`

Category:
- `product`

Purpose:
- Defines a user-owned or demo-owned tax-year workspace.
- Owns workspace identity, tax year, supported jurisdictions, data classification, input references, and run history entry points.

Consumes:
- None.

Feeds:
- `ProductRunPayload`
- `ManualFactEntryBatch`
- `ProductContributionPayload`
- `SourceRecordSet`

Boundary owner:
- `workspace/product`

Schema status:
- `revise_existing`

Manifest role:
- `run_input`

Personal data risk:
- `medium`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## ProductContributionPayload

Durability:
- `canonical`

Category:
- `product`

Purpose:
- Captures one contribution event: the exact workspace input submitted for normalization into facts.
- Freezes the manual entry batch ids or revisions the contribution normalized; future upload or import references belong here as well.
- Records the source record, provenance record, and fact instance ids the contribution produced.
- Provides the product boundary for input-to-facts, symmetric to `ProductRunPayload` for facts-to-return. Contribution and run are distinct product events.
- Accumulates as append-only workspace event history; each contribution payload is immutable once created.

Consumes:
- `ProductWorkspace`
- `ManualFactEntryBatch`

Feeds:
- `SourceRecordSet`
- `ProvenanceRecordSet`
- `FactInstanceSet`

Boundary owner:
- `workspace/product`

Schema status:
- `new_required`

Manifest role:
- `run_input`

Personal data risk:
- `medium`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## ProductRunPayload

Durability:
- `run_snapshot`

Category:
- `product`

Purpose:
- Captures the exact workspace inputs selected for a run.
- Provides the immutable run input boundary between product workspace state and fact/computation execution.
- Records the exact fact instance ids selected from the canonical `FactInstanceSet`.
- Does not re-freeze entry batches, source records, or provenance ids; input-side evidence remains reachable transitively through fact provenance.
- Provides the product boundary for facts-to-return; contribution events are captured separately by `ProductContributionPayload`.

Consumes:
- `ProductWorkspace`
- `FactInstanceSet`

Feeds:
- `ProductRunSummary`
- `RunManifest`
- `FactCoverage`
- `MappingTrace`
- `ComputationTrace`
- `FieldResolution`
- `ReturnInstance`

Boundary owner:
- `workspace/product`

Schema status:
- `revise_existing`

Manifest role:
- `run_input`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## ProductRunSummary

Durability:
- `run_snapshot`

Category:
- `product`

Purpose:
- Records the list-view summary of a completed run: status, timestamps, input revisions, result counts, and manifest reference.

Consumes:
- `ProductRunPayload`
- `FieldResolution`
- `ReturnInstance`

Feeds:
- `RunManifest`

Boundary owner:
- `workspace/product`

Schema status:
- `revise_existing`

Manifest role:
- `run_output`

Personal data risk:
- `medium`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## RunManifest

Durability:
- `run_snapshot`

Category:
- `product`

Purpose:
- Records the exact artifact references for a completed run.
- Serves as the canonical product-facing and reproducibility index for run inputs, definition inputs, and run-snapshot outputs.
- Replaces a separate product run detail artifact in the canonical graph; any run detail screen or read model should project from this manifest and related artifacts.

Consumes:
- `ProductRunPayload`
- `ProductRunSummary`
- `ReturnArtifact`
- `FactTypeCatalog`
- `FactDefinitionCatalog`
- `FactAssertionScope`
- `SourceFamilyInventory`
- `SourceMappingDefinition`
- `FormDefinitionCatalog`
- `FactToReturnMapping`
- `CrossFormBridge`
- `ComputationSpecCatalog`
- `TaxParameterSet`
- `ProductWorkspace`
- `ProductContributionPayload`
- `ManualFactEntryBatch`
- `SourceRecordSet`
- `ProvenanceRecordSet`
- `FactInstanceSet`
- `FactCoverage`
- `MappingTrace`
- `ComputationTrace`
- `FieldResolution`
- `ReturnInstance`

Feeds:
- None.

Boundary owner:
- `workspace/product`

Schema status:
- `revise_existing`

Manifest role:
- `run_output`

Personal data risk:
- `medium`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`
