<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Run Trace Layer

The run trace layer records how a run moved from accepted facts through mappings and computation to resolved return fields. These artifacts explain production; they are not the produced return itself.

## Layer Graph

```text
FactCoverage
  -> MappingTrace
  -> FieldResolution

MappingTrace
  -> ComputationTrace
  -> FieldResolution

ComputationTrace
  -> FieldResolution

ProvenanceRecordSet
  -> MappingTrace
  -> ComputationTrace
  -> FieldResolution
  -> FactCoverage

FactInstanceSet
  -> MappingTrace
  -> ComputationTrace

FactDefinitionCatalog
  -> FactCoverage

ComputationSpecCatalog
  -> FactCoverage

FactAssertionScope
  -> FactCoverage

FormDefinitionCatalog
  -> FieldResolution
```

## Core Edges

### FactCoverage -> MappingTrace

Edge type:
- production
- audit

Meaning:
- Mapping can distinguish between available, missing, optional, or blocked facts when creating trace entries.

### MappingTrace -> ComputationTrace

Edge type:
- production
- audit

Meaning:
- Computations consume mapped fact values and intermediate inputs.

Audit value:
- Lets a reviewer trace from computation output back to mapped facts.

### MappingTrace -> FieldResolution

Edge type:
- production
- audit

Meaning:
- Field resolution uses mapping trace to resolve direct fields and explain unavailable direct fields.

### ComputationTrace -> FieldResolution

Edge type:
- production
- audit

Meaning:
- Field resolution uses computation trace to resolve computed fields, blocked computed fields, and dependency chains.

### FactCoverage -> FieldResolution

Edge type:
- audit

Meaning:
- Fact coverage explains missing or optional input conditions that appear in field resolution.

Notes:
- Field resolution should not need to duplicate the full fact coverage payload.

### ProvenanceRecordSet -> MappingTrace

Edge type:
- audit

Meaning:
- Provenance records explain where mapped facts came from.

### ProvenanceRecordSet -> ComputationTrace

Edge type:
- audit

Meaning:
- Provenance records allow computation outputs to trace back through input facts to source records or prior derivations.

### ProvenanceRecordSet -> FieldResolution

Edge type:
- audit

Meaning:
- Field resolution can reference provenance so output fields remain explainable without embedding all source detail.

### FactInstanceSet -> MappingTrace

Edge type:
- production

Meaning:
- The mapping trace cannot be produced without the selected fact instances.

### FactInstanceSet -> ComputationTrace

Edge type:
- production

Meaning:
- Computation trace records the fact instance inputs computations consumed.

### FactDefinitionCatalog -> FactCoverage

Edge type:
- production

Meaning:
- Fact coverage evaluates expected and required facts against known fact definitions.

### ComputationSpecCatalog -> FactCoverage

Edge type:
- production

Meaning:
- Fact coverage derives expected fact needs from computation spec input requirements.

### ProvenanceRecordSet -> FactCoverage

Edge type:
- production

Meaning:
- Coverage review states derive from provenance record review context.

### FactAssertionScope -> FactCoverage

Edge type:
- production

Meaning:
- Coverage conflict and supersession evaluation uses assertion scopes to group competing fact instances.

### FormDefinitionCatalog -> FieldResolution

Edge type:
- production

Meaning:
- Field resolution resolves outcomes for the fields declared by form definitions.

## FactCoverage

Durability:
- `run_snapshot`

Category:
- `run_trace`

Purpose:
- Records whether expected or required facts are present, missing, optional, unreviewed, conflicting, or superseded for a run.
- Generalizes the current source-field coverage artifact around facts rather than source documents.

Consumes:
- `ProductRunPayload`
- `FactInstanceSet`
- `FactDefinitionCatalog`
- `ComputationSpecCatalog`
- `ProvenanceRecordSet`
- `FactAssertionScope`

Feeds:
- `MappingTrace`

Explains:
- `FieldResolution`

Boundary owner:
- `audit/run_trace`

Schema status:
- `new_required`

Manifest role:
- `run_output`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## MappingTrace

Durability:
- `run_snapshot`

Category:
- `run_trace`

Purpose:
- Records which fact instances mapped to which return or computation fields, which mapping definition applied, and which facts were ignored, filtered, or unavailable.

Consumes:
- `ProductRunPayload`
- `FactToReturnMapping`
- `FactCoverage`
- `FactInstanceSet`

Audit context:
- `ProvenanceRecordSet`

Feeds:
- `ComputationTrace`
- `FieldResolution`

Boundary owner:
- `audit/run_trace`

Schema status:
- `new_required`

Manifest role:
- `run_output`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## ComputationTrace

Durability:
- `run_snapshot`

Category:
- `run_trace`

Purpose:
- Records computation execution at the domain level: computation specs used, parameters used, input values, output values, dependency edges, blocked computations, and implementation identity.
- Does not need to expose every line of code execution.

Consumes:
- `ProductRunPayload`
- `ComputationSpecCatalog`
- `TaxParameterSet`
- `CrossFormBridge`
- `MappingTrace`
- `FactInstanceSet`

Audit context:
- `ProvenanceRecordSet`

Feeds:
- `FieldResolution`

Explains:
- `ReturnInstance`

Boundary owner:
- `audit/run_trace`

Schema status:
- `new_required`

Manifest role:
- `run_output`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## FieldResolution

Durability:
- `run_snapshot`

Category:
- `run_trace`

Purpose:
- Records the per-return-field outcome of a run after mapping and computation.
- Captures resolved direct values, resolved computed values, blocked fields, optional fields, dependency fields, blocking inputs, and audit references.

Consumes:
- `ProductRunPayload`
- `CrossFormBridge`
- `MappingTrace`
- `ComputationTrace`
- `FormDefinitionCatalog`

Audit context:
- `FactCoverage`
- `ProvenanceRecordSet`

Feeds:
- `ProductRunSummary`
- `ReturnInstance`

Boundary owner:
- `audit/run_trace`

Schema status:
- `revise_existing`

Manifest role:
- `run_output`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`
