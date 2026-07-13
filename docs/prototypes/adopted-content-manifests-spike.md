# Paper Spike: Adopted-Content Manifests

Audience: Agents

Status: **proposed.**

This spike provides the paper evaluation analysis and draft ADR for candidate decision CTC-P3, satisfying Gate 1 and Gate 2 rules.

## Decision Inventory & Proposal

**CTC-P3 Proposal:**
Each content package must contain a version-locked `manifest.json` file that defines its namespace, schemas, rules, parameters, form-fields, and dependencies. The package loader validates that the declared files and schemas form a closed, self-contained graph, preventing partial package loading.

## Positive Examples

### Positive Example 1: Standard Closed Manifest (`manifest.json`)
```json
{
  "$schema": "https://finances.gov/schemas/manifest.2026-07-13.json",
  "namespace": "tax.us.2025",
  "version": "1.0.0",
  "dependencies": [],
  "schemas": [
    "schemas/kernel.json",
    "schemas/wages.json"
  ],
  "rules": [
    {
      "path": "rules/wages.py",
      "outputs": ["tax.us.2025.wages.total-w2-box1"]
    }
  ],
  "parameters": [
    "parameters/deductions.json"
  ],
  "form_fields": [
    {
      "id": "1040_line_1a",
      "binds": "tax.us.2025.wages.total-w2-box1"
    }
  ]
}
```

## Negative Examples

### Negative Example 1: Missing schema declaration for output type
- **Manifest:**
  - Has rule `rules/interest.py` that claims to output `tax.us.2025.interest.b1-subtotal`.
  - But the `schemas` array does not include the schema defining `tax.us.2025.interest.b1-subtotal`.
- **Validation Result:** Fails validation (Rule output type `tax.us.2025.interest.b1-subtotal` is undefined in package schemas).

### Negative Example 2: Dangling form field binding
- **Manifest:**
  - Has form field `1040_line_2b` binding to `tax.us.2025.interest.taxable-interest`.
  - But no schema or rule in this package (or declared dependencies) defines `tax.us.2025.interest.taxable-interest`.
- **Validation Result:** Fails validation (Form field `1040_line_2b` binds to undeclared finding type `tax.us.2025.interest.taxable-interest`).

## Lifecycle Trace

1. **Package Creation:** Author places rules, schemas, and form fields under `packages/content/tax/2025/`.
2. **Manifest Authoring:** Author creates `packages/content/tax/2025/manifest.json`.
3. **Loader Verification:** Runner starts up and loads `packages/content/tax/2025/`.
   - Reads `manifest.json`.
   - Validates JSON Schema of the manifest.
   - Verifies all files specified in `manifest.json` exist.
   - Resolves all schemas and compiles the validator registry.
   - Asserts all output finding types in `rules` are defined in the schemas.
   - Asserts all form field bindings map to registered schemas.
4. **Execution:** Runner executes cascade. Graph is guaranteed to have no dangling nodes.

## Producer → Authority → Consumer Map

- **Producers:** Content package developers authoring schemas, rules, parameters, form-fields, and the manifest.
- **Authority:** The Package Loader and Validator (`packages/derivation/loader.py` or similar), verifying manifest closure.
- **Consumer:** Saturation runner and workspace calculations that consume verified, version-locked packages.
- **Failure:** A validation failure blocks runner startup entirely, preventing execution of malformed/partial rule packages.

---

# Draft ADR: Adopted-Content Manifests

- Status: proposed
- Tier: 2
- Date: 2026-07-13

## Context

As content packages grow (adding wages, interest, standard deductions, etc.), they become complex graphs of schemas, python rule scripts, form-field citizens, and lookup tables. If a package is partially loaded, or references undefined finding types or missing scripts, the runner can fail at runtime with obscure errors. We need a formal contract to version-lock and validate a package's content dependencies statically before execution begins.

## Decision

1. **Manifest Citizen:** Each content package must include a `manifest.json` at its root conforming to the manifest JSON Schema.
2. **Closed-Graph Validation:** The package loader must validate the manifest before runner execution. The validation checks:
   - File existence: Every path in `rules`, `schemas`, `parameters`, and `form_fields` must exist.
   - Namespace consistency: All citizen and finding IDs declared in the schemas, rules, and form fields must match the package's namespace or a declared dependency namespace.
   - Output closure: Every finding type output by a rule must have a corresponding schema definition in the registry.
   - Binding closure: Every form field binding must map to a registered finding/fact type.
3. **No Dynamic Imports:** The package loader only loads files explicitly registered in the manifest.

## Consequences

- Package loading becomes deterministic and statically checked.
- Runtime errors due to missing files or mismatched finding names are eliminated.
- The manifest acts as the version-locked contract defining the package's exact contents.
