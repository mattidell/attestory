# Milestone Plan: Dependency-Aware Resolution

## Planning Status

Status: complete.

This milestone plan is backfilled from completed implementation work. It records the contracts, tracks, verification, and exit criteria that were satisfied before the milestone planning protocol existed.

No parallel work manifest is included because this milestone is already complete.

## Objective

Introduce a resolved field set that can distinguish direct values, computed values, source-blocked fields, computation-blocked fields, and optional unpopulated fields.

## Current State

Implemented and complete.

The milestone produced:
- Computed field definitions schema.
- 2025 federal computed field definition file.
- Field resolution schema.
- Field resolver.
- Field resolution workspace artifact.
- Golden field resolution fixture.

## Scope

In scope:
- Small computed field contract.
- Sum and copy operations.
- Dependency resolution from field coverage.
- Blocking status propagation.
- Workspace output integration.
- Golden fixture integration.

Out of scope:
- Broad rules engine.
- Full tax law computation.
- Return artifact generation.
- Computation trace UI.
- Persistence.
- Real personal data.

## Contracts

Contracts introduced:
- `computed-field-definitions` schema.
- `field-resolution` schema.

Definitions introduced:
- Schedule B line 4 total interest as sum of interest amounts.
- Form 1040 line 2b taxable interest as copy from Schedule B line 4.

Workspace artifact introduced:
- `field-resolution.json`

## Fixtures

Primary synthetic workspace:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/
```

Expected artifact:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/expected/field-resolution.json
```

Fixture rules satisfied:
- Synthetic source values only.
- No personal data.
- No absolute local paths.

## Tracks

### Track 17: Computed Field Contract

Goal:
- Define how computed federal fields are declared without adding a broad rules engine.

Outputs:
- Computed field definitions schema.
- Computed field definition loader.
- 2025 federal computed field definitions.

Verification:
- Computed field definition tests.

### Track 18: Dependency-Aware Field Resolution

Goal:
- Resolve direct and computed fields into a single engine artifact suitable for return artifact generation.

Outputs:
- Field resolution schema.
- Field resolver.
- Field resolution workspace artifact.
- Updated run manifest expected output list.
- Golden field resolution artifact.

Verification:
- Field resolution tests.
- Workspace runner tests.
- Golden artifact tests.
- Run manifest tests.

## Verification

Milestone verification:

```bash
python3 -m unittest
```

Canonical runner verification:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

## Exit Criteria

Completed when:
- Computed field definitions validate against schema.
- Field resolution validates against schema.
- Direct fields resolve as direct.
- Computed fields resolve from declared dependencies.
- Missing source data blocks dependent computed fields.
- Missing computation dependencies are explicit.
- Workspace runner emits `field-resolution.json`.
- Run manifest records `field-resolution.json`.
- Golden tests include field resolution.
- Tests pass.
- Committed fixtures remain synthetic and portable.
