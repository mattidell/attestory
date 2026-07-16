# Design: Iteration 2 — ACM Micro-Round Residuals

This document presents the clean-room rival design for **MR-P1** (Fact-Surface Versioning & Wholesale-Adoption Reconciliation) and **MR-P2** (Declared Composition-Obligation Trigger), conforming to the ADR-0027 floor.

---

## MR-P1: Fact-Surface Versioning & Wholesale-Adoption Reconciliation

### 1. Schema Extensions
To meet the ADR-0006 decision 6 requirement for exact member versions, we introduce versioned successor schemas to replace the unversioned HEAD kernel schemas.

#### `fact-type.v2`
Extends `fact-type.v1` by requiring an explicit version field:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "kernel/fact-type.v2",
  "type": "object",
  "properties": {
    "schema": { "const": "fact-type.v2" },
    "id": { "type": "string", "pattern": "^[a-z][a-z0-9]*(\\.[a-z0-9-]+)+$" },
    "version": { "type": "string", "pattern": "^v[0-9]+$" },
    "title": { "type": "string", "minLength": 1 },
    "nature": { "enum": ["determinable", "elective"] },
    "identity_keys": { "type": "array", "minItems": 1 },
    "value_schema": { "type": "object" },
    "supersession": { "type": "object" }
  },
  "required": ["schema", "id", "version", "title", "nature", "identity_keys", "value_schema", "supersession"]
}
```

#### `bundle.v2`
Extends `bundle.v1` by requiring a version and nesting `fact-type.v2` objects:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "kernel/bundle.v2",
  "type": "object",
  "properties": {
    "schema": { "const": "bundle.v2" },
    "id": { "type": "string", "pattern": "^[a-z][a-z0-9]*(\\.[a-z0-9-]+)+$" },
    "version": { "type": "string", "pattern": "^v[0-9]+$" },
    "label": { "type": "string", "minLength": 1 },
    "fact_types": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": { "schema": { "const": "fact-type.v2" } },
        "required": ["schema"]
      }
    }
  },
  "required": ["schema", "id", "version", "label", "fact_types"]
}
```

#### `artifact-package.v2`
Extends the member pin roles to support pinning fact types and bundles:
```json
{
  "role": {
    "enum": [
      "parameter", "computation", "applicability", "field-mapping", "cross-form-bridge",
      "input", "choice", "adoption", "governance", "engine", "package", "operation-semantics",
      "fact-type", "fact-type-bundle"
    ]
  }
}
```

### 2. Validation & Inclusion Joins
- **Fact Surface Definition:** The fact surface of a package consists of all `fact-type` pins declared in its `members`.
- **Inclusion Join (Drift Protection):** For every `fact-type` pin `(id, version)` in the package:
  - It must be defined in at least one adopted `bundle.v2` in the workspace.
  - The version of the fact-type inside the adopted bundle must match the package's pinned version.
- **Mapping Fact-Type Gap:** For every `source-closure-mapping` in the package members, the validator rejects if `member_fact_type` or `closure_fact_type` are missing from the package's fact surface.

---

## MR-P2: Declared Composition-Obligation Trigger

### 1. The `composition-obligation.v1` Citizen
To avoid circular dependency on the composition citizen being present, we declare composition obligations via a separate, versioned governance citizen:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "derivation/composition-obligation.v1",
  "title": "Composition obligation",
  "description": "Declares that a published symbol is composition-governed.",
  "type": "object",
  "properties": {
    "schema": { "const": "composition-obligation.v1" },
    "id": { "type": "string", "pattern": "^[a-z][a-z0-9]*(\\.[a-z0-9-]+)+$" },
    "version": { "type": "string", "pattern": "^v[0-9]+$" },
    "symbol": { "type": "string", "minLength": 1 }
  },
  "required": ["schema", "id", "version", "symbol"],
  "additionalProperties": false
}
```

### 2. Non-Circular Validation
The package pins the obligation citizen using `role: "governance"`.
When validating, the validator:
1. Gathers all pinned `composition-obligation.v1` citizens.
2. For each obligated symbol `S`:
   - Verifies the package contains a member pin with `role: "composition"` whose target citizen publishes `S`. If missing, rejects with `COMPOSITION_CITIZEN_MISSING` (resolving Case 7).
   - Verifies that the package rule publishing `S` contains a provenance-only `composition` pin pointing to that composition citizen. If missing, rejects with `COMPOSITION_PIN_MISSING` (resolving Case 8).
3. Evaluates form-fields as presentation-only (no presentation leak; Case 9).
4. Employs no hardcoded runner symbol tables (conforms to Article 11; Case 9).
