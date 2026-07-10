<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Computation Definition Layer

The computation definition layer owns canonical return-construction definitions: form structure, mappings, bridges, computation contracts, and tax parameters. It models computation contracts without requiring every algorithm to be declarative data.

## Layer Graph

```text
FactDefinitionCatalog
  -> FactToReturnMapping
  -> ComputationSpecCatalog

FormDefinitionCatalog
  -> FactToReturnMapping
  -> ComputationSpecCatalog
  -> CrossFormBridge

FactToReturnMapping
  -> MappingTrace

TaxParameterSet
  -> ComputationSpecCatalog
  -> ComputationTrace

ComputationSpecCatalog
  -> ComputationTrace

CrossFormBridge
  -> ComputationTrace
  -> FieldResolution
```

## Core Edges

### FactDefinitionCatalog -> FactToReturnMapping

Edge type:
- production

Meaning:
- Mappings must reference known fact definitions.

### FormDefinitionCatalog -> FactToReturnMapping

Edge type:
- production

Meaning:
- Mappings must target known form, schedule, worksheet, field, or intermediate computation definitions.

### FactToReturnMapping -> MappingTrace

Edge type:
- production
- audit

Meaning:
- The mapping trace records which mapping definitions were applied to selected fact instances.

Audit value:
- Explains why a fact did or did not feed a return field or computation input.

### FormDefinitionCatalog -> ComputationSpecCatalog

Edge type:
- production

Meaning:
- Computation specs identify the form fields, schedule fields, worksheet fields, or intermediate outputs they produce.

### TaxParameterSet -> ComputationSpecCatalog

Edge type:
- production

Meaning:
- Computation specs reference parameter sets used by tax-year computations.

### ComputationSpecCatalog -> ComputationTrace

Edge type:
- production
- audit

Meaning:
- Computation trace records which computation specs ran, which inputs they used, which outputs they produced, and what blocked or changed execution.

Audit value:
- Gives rule, parameter, implementation, and dependency context without requiring every algorithm step to be modeled as data.

### TaxParameterSet -> ComputationTrace

Edge type:
- production
- audit

Meaning:
- Computation trace must record the parameter sets used for reproducibility and review.

### CrossFormBridge -> ComputationTrace

Edge type:
- production
- audit

Meaning:
- Cross-form bridge definitions participate in schedule-to-return and form-to-form value flow.

Audit value:
- Explains why a value moved from one form or schedule to another.

### FormDefinitionCatalog -> CrossFormBridge

Edge type:
- production

Meaning:
- Cross-form bridges reference known form and schedule definitions on both ends of the flow.

### FactDefinitionCatalog -> ComputationSpecCatalog

Edge type:
- production

Meaning:
- Computation specs declare consumed inputs against known fact definitions.

### CrossFormBridge -> FieldResolution

Edge type:
- production

Meaning:
- Field resolution applies cross-form bridge flows when resolving dependent fields.

## FormDefinitionCatalog

Durability:
- `canonical`

Category:
- `computation_definition`

Purpose:
- Defines form, schedule, worksheet, field, table, part, and display structure for a tax year and jurisdiction.

Consumes:
- None.

Feeds:
- `FactToReturnMapping`
- `ComputationSpecCatalog`
- `CrossFormBridge`
- `FieldResolution`
- `ReturnInstance`

Boundary owner:
- `computation`

Schema status:
- `new_required`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## FactToReturnMapping

Durability:
- `canonical`

Category:
- `computation_definition`

Purpose:
- Defines how normalized facts feed return fields, schedules, worksheets, or intermediate computation inputs.

Consumes:
- `FactDefinitionCatalog`
- `FormDefinitionCatalog`

Feeds:
- `MappingTrace`

Boundary owner:
- `computation`

Schema status:
- `revise_existing`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## CrossFormBridge

Durability:
- `canonical`

Category:
- `computation_definition`

Purpose:
- Defines explicit cross-form relationships, such as schedule totals flowing to Form 1040 fields.
- Keeps cross-form dependencies reviewable outside individual computation implementations.

Consumes:
- `FormDefinitionCatalog`

Feeds:
- `ComputationTrace`
- `FieldResolution`

Boundary owner:
- `computation`

Schema status:
- `revise_existing`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## ComputationSpecCatalog

Durability:
- `canonical`

Category:
- `computation_definition`

Purpose:
- Defines computation contracts: computation identity, tax year, jurisdiction, consumed inputs, produced outputs, parameter references, implementation identity, dependencies, and verification scope.
- Models the computation process contract without forcing every algorithm into declarative JSON.

Consumes:
- `FormDefinitionCatalog`
- `TaxParameterSet`
- `FactDefinitionCatalog`

Feeds:
- `ComputationTrace`
- `FactCoverage`

Boundary owner:
- `computation`

Schema status:
- `new_required`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## TaxParameterSet

Durability:
- `canonical`

Category:
- `computation_definition`

Purpose:
- Defines tax-year parameter data used by computations, such as thresholds, rates, caps, phaseout ranges, and lookup tables.

Consumes:
- None.

Feeds:
- `ComputationSpecCatalog`
- `ComputationTrace`

Boundary owner:
- `computation`

Schema status:
- `new_required`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`
