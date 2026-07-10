<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Edge Types

This document defines the edge types used by the artifact graph. Concrete edge instances live in the layer documents:

- [Product Layer](artifact-graph-product-layer.md)
- [Input Layer](artifact-graph-input-layer.md)
- [Fact Layer](artifact-graph-fact-layer.md)
- [Computation Definition Layer](artifact-graph-computation-definition-layer.md)
- [Run Trace Layer](artifact-graph-run-trace-layer.md)
- [Production Layer](artifact-graph-production-layer.md)

Projection-only review models, local-only implementation details, and disposable diagnostics are out of scope unless they become canonical or run-snapshot artifacts later.

## Production Edge

A production edge means the upstream artifact is required to produce the downstream artifact.

Example:

```text
FactInstanceSet -> MappingTrace
```

The mapping trace cannot be produced without the selected fact instances.

Production edges are dependency edges. They answer:

- What must already exist before this artifact can be built?
- What should be recorded as a run input or definition input?
- What affects reproducibility if it changes?

## Audit Edge

An audit edge means the upstream artifact explains, supports, or provides traceability for the downstream artifact, but the downstream artifact can remain meaningful as a produced state without embedding the full trace.

Example:

```text
ComputationTrace -> ReturnInstance
```

The return instance records the produced return state. The computation trace explains how that state was produced.

Audit edges answer:

- What explains this output?
- What should a reviewer inspect to understand a value?
- What provides provenance, dependency, blocking, or rule-version context?

## Mixed Edge

Some relationships are both production and audit edges.

Example:

```text
FieldResolution -> ReturnInstance
```

The return instance is assembled from resolved fields, so this is a production edge. It is also an audit edge because field resolution preserves status, dependency, and blocking context that explains the produced fields.

When an edge is mixed, the graph should name both roles instead of forcing a single label.

## Reproducibility Edges

Reproducibility edges are production edges that should be recorded directly or indirectly in `RunManifest`.

Definition inputs:
- `SourceFamilyInventory`
- `SourceMappingDefinition`
- `FactTypeCatalog`
- `FactDefinitionCatalog`
- `FactAssertionScope`
- `FormDefinitionCatalog`
- `FactToReturnMapping`
- `CrossFormBridge`
- `ComputationSpecCatalog`
- `TaxParameterSet`

Run-selected inputs:
- `ProductWorkspace`
- `ProductContributionPayload`
- `ProductRunPayload`
- `ManualFactEntryBatch`
- `SourceRecordSet`
- `ProvenanceRecordSet`
- `FactInstanceSet`

Run outputs:
- `ProductRunSummary`
- `RunManifest`
- `FactCoverage`
- `MappingTrace`
- `ComputationTrace`
- `FieldResolution`
- `ReturnInstance`
- `ReturnArtifact`

`RunManifest` should identify exact artifact versions or revisions where available. When artifact identity is not yet versioned, it should at least record stable artifact type, path or URI, schema version, run id, and the exact fact instance ids selected from `FactInstanceSet`.
