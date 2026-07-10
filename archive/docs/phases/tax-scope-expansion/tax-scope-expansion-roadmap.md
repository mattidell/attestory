# Tax Scope Expansion Roadmap

## Roadmap

### Milestone 1: Coverage Selection And Contract Inventory

Select the next federal coverage increments and inventory the schemas, mappings, computed fields, fixtures, runners, and review outputs each increment requires.

This milestone matters because tax scope should expand only through explicit contracts and deterministic verification.

### Milestone 2: Additional Income Source Documents

Add a small set of additional federal income source documents and related direct mappings.

This milestone matters because income source coverage is the next natural expansion after W-2 and 1099-INT support.

### Milestone 3: Adjustment And Deduction Inputs

Add selected adjustment or deduction inputs with explicit source draft contracts, mapping rules, coverage behavior, and review output.

This milestone matters because common return workflows require more than income fields, but each addition should stay bounded.

### Milestone 4: Expanded Computed Dependencies

Extend computed field definitions and dependency-aware resolution for the newly supported fields.

This milestone matters because expanded source coverage should flow through auditable computation rather than manual result edits.

### Milestone 5: Expanded Scenario Golden Workspaces

Create synthetic golden workspace scenarios that prove the added source types, mappings, computations, and review outputs work end to end.

This milestone matters because broader coverage is only durable when expected artifacts are committed and regression-tested.

## Status

Phase status:
- Future high-level phase.

Active milestone:
- None.

Implementation notes:
- This phase should not begin until product and data safety boundaries are stable.
- Milestone plans should be created under `docs/phases/tax-scope-expansion/milestones/` before implementation.
- Coverage increments should remain federal-only unless a later phase explicitly introduces state scope.

Project impact:
- Source document schemas.
- Field catalog and mapping definitions.
- Computed field definitions.
- Workspace runner outputs.
- Golden fixtures.
- Review models and application displays.
