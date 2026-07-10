# Milestone Plan: Workspace Execution And Golden Artifacts

## Planning Status

Status: complete.

This milestone plan is backfilled from completed implementation work. It records the contracts, tracks, verification, and exit criteria that were satisfied before the milestone planning protocol existed.

No parallel work manifest is included because this milestone is already complete.

## Objective

Create a repeatable workspace execution boundary that runs the current engine workflow from a synthetic workspace manifest and validates the output through committed golden artifacts.

## Current State

Implemented and complete.

The milestone produced:
- Tax workspace schema.
- Basic synthetic federal workspace fixture.
- Workspace runner.
- Expected workspace artifacts.
- Golden artifact tests.
- Run manifest schema and output.

## Scope

In scope:
- Synthetic workspace manifest.
- Workspace-level draft input references.
- Workspace execution through the canonical runner.
- Normalized source document output.
- Source validation output.
- Field coverage JSON and Markdown output.
- Run manifest output.
- Golden expected artifacts.

Out of scope:
- Field resolution.
- Return artifact generation.
- Persistence.
- API.
- UI.
- Real personal data.

## Contracts

Contracts introduced:
- `tax-workspace` schema.
- `run-manifest` schema.

Workspace artifacts:
- `normalized-source-documents.json`
- `source-validation.json`
- `field-coverage.json`
- `field-coverage.md`
- `run-manifest.json`

## Fixtures

Primary synthetic workspace:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/
```

Expected artifacts:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/expected/
```

Fixture rules satisfied:
- Synthetic source drafts.
- Portable manifest paths.
- No personal data.
- No absolute local paths in committed manifests.

## Tracks

### Track 13: Workspace Fixture Contract

Goal:
- Define a synthetic workspace manifest that groups source document drafts into a tax-year scenario.

Outputs:
- Workspace schema.
- Basic W-2 plus 1099-INT workspace fixture.
- Workspace loader.

Verification:
- Workspace schema and fixture tests.

### Track 14: Workspace Run Orchestrator

Goal:
- Run the current workflow from a workspace manifest and write artifacts to an output directory.

Outputs:
- Workspace execution module.
- `run_tax_workspace` runner.
- Runner output for normalized source documents, validation, coverage JSON, and coverage Markdown.

Verification:
- Workspace execution tests.
- Workspace runner subprocess tests.

### Track 15: Golden Run Artifacts

Goal:
- Commit expected workspace artifacts and compare generated output to them.

Outputs:
- Expected artifacts under the basic workspace.
- Golden artifact regression tests.

Verification:
- Golden artifact tests.

### Track 16: Run Manifest

Goal:
- Emit a manifest describing the workspace run inputs and outputs.

Outputs:
- Run manifest schema.
- `run-manifest.json` workspace artifact.
- Deterministic `--run-id` and `--created-at` runner arguments.

Verification:
- Run manifest tests.
- Runner tests proving manifest output.

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
- Workspace fixture validates against schema.
- Workspace runner writes the expected artifact set.
- Golden artifacts are committed.
- Golden tests compare generated output to expected output.
- Run manifest records inputs and outputs.
- Run manifest fixture paths are portable.
- Tests pass.
- Committed fixtures remain synthetic and portable.
