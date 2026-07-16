# ADR 0022 — Adopted-Content Manifests

- Status: **superseded** by ADR-0027 (retained; inert single-author draft — path-manifest approach rejected)
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

- Package loading becomes destructive and statically checked.
- Runtime errors due to missing files or mismatched finding names are eliminated.
- The manifest acts as the version-locked contract defining the package's exact contents.
