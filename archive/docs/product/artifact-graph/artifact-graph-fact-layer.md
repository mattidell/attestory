<!-- Generated from artifact-graph.json by tools/render_artifact_graph.py. Do not edit by hand; edit the JSON and re-run the renderer. -->

# Artifact Graph Fact Layer

The fact layer is the stable semantic input center. It models fact meaning, assertion scope, accumulated fact assertions, supersession, and provenance. User-entered and source-shaped material is captured in the input layer before it becomes normalized facts.

## Layer Graph

```text
FactTypeCatalog
  -> FactDefinitionCatalog
  -> FactInstanceSet

FactDefinitionCatalog
  -> FactInstanceSet
  -> FactAssertionScope
  -> ProvenanceRecordSet

FactAssertionScope
  -> FactInstanceSet

ProvenanceRecordSet
  -> FactInstanceSet

FactInstanceSet
  -> FactCoverage
  -> FactInstanceSet

SourceRecordSet
  -> FactInstanceSet
```

## Core Edges

### FactTypeCatalog -> FactDefinitionCatalog

Edge type:
- production

Meaning:
- Fact definitions use fact types to declare their value shapes.

Notes:
- Both artifacts are canonical definition inputs.

### FactDefinitionCatalog -> FactInstanceSet

Edge type:
- production
- audit

Meaning:
- Each fact instance must identify a known fact definition.

Audit value:
- The definition explains the semantic meaning of the instance.

### FactAssertionScope -> FactInstanceSet

Edge type:
- production
- audit

Meaning:
- Each fact instance belongs to an assertion scope that defines what counts as the same current-valued assertion.

Audit value:
- Scope prevents supersession and current-tip logic from confusing similar facts that can coexist, such as W-2 wages from different employers or rental expenses for different properties.

Notes:
- Scope should use domain identity dimensions, not source record identity.
- Examples include employer, payer, property, account, dependent, activity, period, taxpayer, jurisdiction, and tax year.
- Source records belong in provenance so corrected documents can supersede prior facts in the same assertion scope.

### ProvenanceRecordSet -> FactInstanceSet

Edge type:
- production
- audit

Meaning:
- Fact instances should be connected to provenance records that explain why the fact is believed and how it entered the run.

Notes:
- This replaces a hard requirement that fact instances directly contain `document_id`.

### FactInstanceSet -> FactCoverage

Edge type:
- production
- audit

Meaning:
- Fact coverage evaluates the selected fact instances against expected or required fact needs for a run.

Audit value:
- Shows present, missing, optional, unreviewed, conflicting, or superseded facts before return production.

### FactInstanceSet -> FactInstanceSet

Edge type:
- audit

Meaning:
- Fact instances may reference prior fact instances with `supersedes_fact_instance_id`.

Audit value:
- Supersession preserves correction history without introducing a separate ledger artifact.

Notes:
- Supersession should only link instances with the same `fact_id` and same assertion scope.
- Supersession chains must not contain cycles.
- The current tip for a scoped assertion can be computed as the instance not superseded by another instance in the same set.

### FactDefinitionCatalog -> FactAssertionScope

Edge type:
- production

Meaning:
- Assertion scopes declare which identity dimensions apply to which fact definitions.

### FactDefinitionCatalog -> ProvenanceRecordSet

Edge type:
- production

Meaning:
- Provenance records reference the fact definitions their evidence supports.

### FactTypeCatalog -> FactInstanceSet

Edge type:
- production

Meaning:
- Fact instance values conform to the value shapes declared by fact types.

### SourceRecordSet -> FactInstanceSet

Edge type:
- production

Meaning:
- Fact instances derive from the concrete source records that support them.

## FactTypeCatalog

Durability:
- `canonical`

Category:
- `fact`

Purpose:
- Defines reusable value shapes for facts, such as money, boolean, date, scalar strings, and structured object facts.

Consumes:
- None.

Feeds:
- `FactDefinitionCatalog`
- `FactInstanceSet`

Boundary owner:
- `fact`

Schema status:
- `new_required`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## FactDefinitionCatalog

Durability:
- `canonical`

Category:
- `fact`

Purpose:
- Defines the semantic facts the system understands, independent of a specific taxpayer run.
- Examples include W-2 wages, interest income, rental property facts, prior-year return facts, dependent eligibility facts, and depreciation support facts.

Consumes:
- `FactTypeCatalog`

Feeds:
- `ManualFactEntryBatch`
- `FactInstanceSet`
- `FactAssertionScope`
- `ProvenanceRecordSet`
- `FactToReturnMapping`
- `ComputationSpecCatalog`
- `FactCoverage`

Boundary owner:
- `fact`

Schema status:
- `new_required`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## FactAssertionScope

Durability:
- `canonical`

Category:
- `fact`

Purpose:
- Defines the identity dimensions used to decide whether fact instances are competing revisions of the same assertion or separate facts that can coexist.
- Typical scope dimensions include tax year, jurisdiction, subject, employer, payer, property, account, dependent, activity, period, or other domain-specific entity ids.
- Excludes source record identity. Different source records can provide evidence for the same scoped assertion, especially when corrected documents arrive.

Consumes:
- `FactDefinitionCatalog`

Feeds:
- `FactInstanceSet`
- `FactCoverage`

Boundary owner:
- `fact`

Schema status:
- `new_required`

Manifest role:
- `definition_input`

Personal data risk:
- `low`

Commit policy:
- `canonical_definition_allowed`

## ProvenanceRecordSet

Durability:
- `canonical`

Category:
- `fact`

Purpose:
- Records why each fact is believed, where it came from, how it was captured or derived, and what review state applies.
- Generalizes beyond source documents to cover manual entry, prior returns, imports, reviewed domain inputs, bootstrap data, and derived facts.
- Records the mapping definition versions and contribution context applied when facts were normalized.
- Accumulates evidence links between runs; run snapshots select exact provenance ids relevant to selected facts.

Consumes:
- `ProductContributionPayload`
- `SourceRecordSet`
- `ManualFactEntryBatch`
- `FactDefinitionCatalog`

Feeds:
- `FactInstanceSet`
- `FactCoverage`

Explains:
- `MappingTrace`
- `ComputationTrace`
- `FieldResolution`

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

## FactInstanceSet

Durability:
- `canonical`

Category:
- `fact`

Purpose:
- Captures the accumulated normalized fact assertions for a workspace or product fact context.
- Provides the durable identity space for facts between runs.
- This is the stable semantic input center from which runs select exact fact instances.
- May contain supersession chains through optional `supersedes_fact_instance_id` links.
- Current fact state is computed as the tip per `fact_id` plus assertion scope.
- A run snapshot records exact fact instance ids, normally current tips but optionally historical instances when intentionally selected.

Consumes:
- `ProductContributionPayload`
- `ManualFactEntryBatch`
- `SourceMappingDefinition`
- `FactDefinitionCatalog`
- `FactAssertionScope`
- `ProvenanceRecordSet`
- `FactTypeCatalog`
- `SourceRecordSet`

Feeds:
- `ProductRunPayload`
- `FactCoverage`
- `MappingTrace`
- `ComputationTrace`

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

### Supersession Semantics

Fact instances are immutable. Corrections or replacements create a new fact instance that optionally points to the prior instance it supersedes. Supersession belongs in the canonical `FactInstanceSet`; individual runs snapshot exact fact instance ids from that set.

Minimal fact instance additions:

```json
{
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "federal",
    "subject_id": "taxpayer.primary",
    "employer_id": "employer.acme"
  },
  "supersedes_fact_instance_id": "fact.example.previous"
}
```

Validation expectations:
- A fact instance may supersede at most one prior fact instance.
- The superseded instance must have the same `fact_id`.
- The superseded instance must have the same assertion scope.
- A fact instance cannot supersede itself.
- Supersession chains must not contain cycles.
- Multiple unsuperseded tips for the same `fact_id` and assertion scope are conflicts unless the fact definition explicitly allows concurrent instances.
- A run snapshot should record exact fact instance ids, whether they are current tips or intentionally selected historical instances.

### Standing Trace Test: W-2c Correction

The common W-2c correction case should remain the standing test for fact scope and supersession.

Initial W-2:
- `SourceRecordSet` contains a source record for the original W-2 from Employer A.
- `ProvenanceRecordSet` records that the original W-2 supports `irs.w2.wages_box1`.
- `FactInstanceSet` contains a wages fact scoped by taxpayer, tax year, jurisdiction, and employer.

Corrected W-2c:
- `SourceRecordSet` gets a new source record for the W-2c.
- `ProvenanceRecordSet` records that the W-2c supports a replacement wages fact.
- `FactInstanceSet` gets a new wages fact with the same `fact_id` and same domain scope, using `supersedes_fact_instance_id` to point to the original wages fact.

Result:
- The original W-2 and W-2c remain distinct source records in provenance.
- The corrected wages fact can supersede the original because source record identity is not part of assertion scope.
- A run before the correction can still reference the original fact instance.
- A run after the correction normally selects the W-2c fact as the current tip.
