<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Layers

This document summarizes the canonical and run-snapshot artifact layers in the fact-centered product architecture. Detailed artifact entries live in the layer-specific documents linked below.

The graph uses only two durability classes:

- `canonical`: a versioned source of truth, reusable definition, or accumulated contributed state.
- `run_snapshot`: an immutable artifact produced or frozen by one workspace run.

Projection-only review models, local-only implementation details, and disposable diagnostics are out of scope unless they become canonical or run-snapshot artifacts later.

## Durability Rule

`run_snapshot` is only for artifacts a run produces or freezes for reproducibility. Contributed artifacts accumulate canonically.

This means user input, source records, provenance records, and fact instances have canonical homes between runs. Runs do not own those artifacts; runs select exact ids or revisions from them through `ProductRunPayload` and record those selections in `RunManifest`.

## Layer Summary

```text
Product Layer
  ProductWorkspace
  ProductContributionPayload
  ProductRunPayload
  ProductRunSummary
  RunManifest

Input Layer
  SourceFamilyInventory
  SourceMappingDefinition
  ManualFactEntryBatch
  SourceRecordSet

Fact Layer
  FactTypeCatalog
  FactDefinitionCatalog
  FactAssertionScope
  ProvenanceRecordSet
  FactInstanceSet

Computation Definition Layer
  FormDefinitionCatalog
  FactToReturnMapping
  CrossFormBridge
  ComputationSpecCatalog
  TaxParameterSet

Run Trace Layer
  FactCoverage
  MappingTrace
  ComputationTrace
  FieldResolution

Production Layer
  ReturnInstance
  ReturnArtifact
```

## Layer Documents

- [Product Layer](artifact-graph-product-layer.md)
- [Input Layer](artifact-graph-input-layer.md)
- [Fact Layer](artifact-graph-fact-layer.md)
- [Computation Definition Layer](artifact-graph-computation-definition-layer.md)
- [Run Trace Layer](artifact-graph-run-trace-layer.md)
- [Production Layer](artifact-graph-production-layer.md)

## Cross-Layer Flow

```text
ProductWorkspace
  -> ManualFactEntryBatch
  -> SourceRecordSet

ManualFactEntryBatch
  -> ProductContributionPayload
  -> FactInstanceSet
  -> ProvenanceRecordSet

ProductContributionPayload
  -> SourceRecordSet
  -> ProvenanceRecordSet
  -> FactInstanceSet

FactInstanceSet
  -> ProductRunPayload
  -> FactCoverage
  -> MappingTrace
  -> ComputationTrace

ProductRunPayload
  -> FactCoverage
  -> MappingTrace
  -> ComputationTrace
  -> FieldResolution
  -> ReturnInstance

FieldResolution
  -> ProductRunSummary
  -> ReturnInstance

SourceRecordSet
  -> ProvenanceRecordSet
  -> FactInstanceSet

SourceMappingDefinition
  -> FactInstanceSet

FactDefinitionCatalog
  -> ManualFactEntryBatch
  -> FactToReturnMapping
  -> ComputationSpecCatalog
  -> FactCoverage

FactToReturnMapping
  -> MappingTrace

ComputationSpecCatalog
  -> ComputationTrace
  -> FactCoverage

TaxParameterSet
  -> ComputationTrace

CrossFormBridge
  -> ComputationTrace
  -> FieldResolution

ProvenanceRecordSet
  -> FactCoverage

FactAssertionScope
  -> FactCoverage

FormDefinitionCatalog
  -> FieldResolution
  -> ReturnInstance

ReturnInstance
  -> ProductRunSummary

ReturnArtifact
  -> RunManifest
```

The cross-layer flow lists production edges that cross layer boundaries, grouped by source artifact. Every artifact also feeds `RunManifest`; those index edges are omitted here for readability. The core edge distinctions and dependency details are defined in [Artifact Graph Core Edges](artifact-graph-core-edges.md).
