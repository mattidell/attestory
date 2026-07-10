<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Input Layer

The input layer captures user-entered and source-shaped material before it becomes normalized facts. It includes source family planning, source-to-fact mapping, user entry batches, and concrete source records available for run selection.

This layer exists because user input is not the same thing as a fact. A manual entry can be incomplete, source-shaped, unreviewed, superseded, or grouped by document/workspace context before it becomes an accepted fact instance.

## Layer Graph

```text
SourceFamilyInventory
  -> ManualFactEntryBatch
  -> SourceRecordSet

SourceMappingDefinition
  -> ManualFactEntryBatch
  -> SourceRecordSet
  -> FactInstanceSet

ManualFactEntryBatch
  -> SourceRecordSet
  -> FactInstanceSet
  -> ProvenanceRecordSet

SourceRecordSet
  -> ProvenanceRecordSet

ProductWorkspace
  -> SourceRecordSet

FactDefinitionCatalog
  -> ManualFactEntryBatch
```

## Core Edges

### SourceFamilyInventory -> ManualFactEntryBatch

Edge type:
- production

Meaning:
- Manual entry batches are organized around supported source families, such as W-2, 1099-INT, rental manual inputs, prior-year return inputs, Schedule A support, credits support, and depreciation bootstrap inputs.

Audit value:
- The inventory explains why a source family exists, whether it is modeled, and which files or workflows represent it.

### SourceMappingDefinition -> ManualFactEntryBatch

Edge type:
- production
- audit

Meaning:
- Manual entry fields should be constrained by source-to-fact mappings where the input is source-shaped.

Audit value:
- The mapping explains how source-shaped entries are expected to become normalized facts.

### ManualFactEntryBatch -> SourceRecordSet

Edge type:
- production
- audit

Meaning:
- A manual entry batch creates or updates concrete source records in the workspace fact context, such as user-entered W-2 records, reviewed rental input groups, or prior-year return context records.

Audit value:
- Source records should retain the batch, entry labels, source type, and review context needed to explain later facts.

### SourceRecordSet -> ProvenanceRecordSet

Edge type:
- production
- audit

Meaning:
- Provenance records reference source records to explain the origin of fact assertions.

Notes:
- Source records are not limited to source documents. They may represent manual entry batches, prior returns, imports, domain workspaces, depreciation tables, bootstrap data, or derived computation sources.

### ManualFactEntryBatch -> FactInstanceSet

Edge type:
- production
- audit

Meaning:
- Manual entry batches can normalize directly into fact instances when each entry already identifies a target fact.

Notes:
- The `prototype` branch contains `manual-fact-entry.schema.json`, where each entry has `entry_id`, `source_type`, `document_label`, `fact_id`, `value`, and optional `notes`.

### ManualFactEntryBatch -> ProvenanceRecordSet

Edge type:
- production

Meaning:
- Manual entry batches provide the capture context provenance records reference for user-entered facts.

### SourceMappingDefinition -> SourceRecordSet

Edge type:
- production

Meaning:
- Source records for source-shaped input follow the field structure declared by source mapping definitions.

### SourceMappingDefinition -> FactInstanceSet

Edge type:
- production

Meaning:
- Source-shaped entries normalize into fact instances through source mapping definitions.

### SourceFamilyInventory -> SourceRecordSet

Edge type:
- production

Meaning:
- Source records identify the source family they belong to.

### ProductWorkspace -> SourceRecordSet

Edge type:
- production

Meaning:
- Source records are captured within a workspace and inherit its identity and data classification context.

### FactDefinitionCatalog -> ManualFactEntryBatch

Edge type:
- production

Meaning:
- Manual entries that directly target facts must reference known fact definitions.

## SourceFamilyInventory

Durability:
- `canonical`

Category:
- `input`

Purpose:
- Catalogs source families supported by the current-year workflow.
- Records source roles, workspace/UI entry points, current input files, fact files, mapping files, fact definition files, and return mapping status.

Consumes:
- None.

Feeds:
- `ManualFactEntryBatch`
- `SourceRecordSet`

Boundary owner:
- `workspace/product`
- `fact`

Schema status:
- `new_required`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## SourceMappingDefinition

Durability:
- `canonical`

Category:
- `input`

Purpose:
- Defines source-shaped fields and maps them to normalized fact definitions.
- Examples include W-2 box mappings, 1099 mappings, rental manual input mappings, prior-year return mappings, Schedule A support mappings, and credits support mappings.

Consumes:
- None.

Feeds:
- `ManualFactEntryBatch`
- `SourceRecordSet`
- `FactInstanceSet`

Boundary owner:
- `fact`

Schema status:
- `revise_existing`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## ManualFactEntryBatch

Durability:
- `canonical`

Category:
- `input`

Purpose:
- Captures user-entered facts or source-shaped entries for a tax year and jurisdiction.
- Preserves entry ids, source type, document or source label, target fact id, value, and entry notes before or during normalization.
- Accumulates as contributed workspace input between runs; individual runs select exact batch ids or revisions.

Consumes:
- `ProductWorkspace`
- `SourceFamilyInventory`
- `SourceMappingDefinition`
- `FactDefinitionCatalog`

Feeds:
- `ProductContributionPayload`
- `SourceRecordSet`
- `FactInstanceSet`
- `ProvenanceRecordSet`

Boundary owner:
- `workspace/product`
- `fact`

Schema status:
- `revise_existing`

Manifest role:
- `run_input`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`

## SourceRecordSet

Durability:
- `canonical`

Category:
- `input`

Purpose:
- Captures the concrete sources that produced or supported facts.
- Source records may represent tax documents, manual entry batches, prior returns, imported account data, reviewed support workspaces, depreciation tables, or bootstrap sources.
- Accumulates evidence between runs so later arrivals, such as corrected documents, have a durable place to land before the next run.

Consumes:
- `ProductContributionPayload`
- `ManualFactEntryBatch`
- `SourceMappingDefinition`
- `SourceFamilyInventory`
- `ProductWorkspace`

Feeds:
- `ProvenanceRecordSet`
- `FactInstanceSet`

Boundary owner:
- `fact`

Schema status:
- `new_required`

Manifest role:
- `run_input`

Personal data risk:
- `high`

Commit policy:
- `synthetic_fixture_allowed`
- `real_data_local_only`
