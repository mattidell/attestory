# Milestone Plan: Return Artifact Evaluation

## Planning Status

Status: complete milestone plan.

This milestone plan was confirmed complete for implementation.

No parallel work manifest is included. Add one only if the user or orchestrating developer explicitly requests parallel execution planning for this milestone.

## Objective

Prove that the resolved federal field set can be converted into a deterministic normalized return artifact and reviewed through a human-readable output.

## Current State

Implemented inputs:
- Tax workspace fixture.
- Workspace runner.
- Source document draft normalization.
- Source validation.
- Direct source-to-form mapping.
- Field coverage.
- Field resolution.
- Run manifest.
- Golden workspace artifact tests.

Stable input artifact:
- `field-resolution.json`

Canonical runner:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

## Scope

In scope:
- Add a normalized return artifact schema.
- Generate a return artifact from field resolution.
- Wire return artifact output into the workspace runner.
- Add return artifact references to the run manifest.
- Commit a golden return artifact for the basic synthetic workspace.
- Add a human-readable Markdown return review.
- Add tests for schema validation, generation, runner output, golden artifacts, and manifest output.

Out of scope:
- Official IRS PDF generation.
- IRS form layout replication.
- Persistence.
- API.
- UI.
- State returns.
- Real personal data.
- Broad expansion of tax form coverage.

## Contracts

New contracts:
- `return-artifact` schema.
- Return artifact loader/validator.
- Return artifact generator from `field-resolution.json`.
- Return review Markdown renderer.

Return artifact shape:
- The return artifact is return-facing and should include resolved return output plus a compact `resolution_summary`.
- `resolution_summary` should summarize resolved, blocked, and optional unpopulated field counts from `field-resolution.json`.
- `field-resolution.json` remains the detailed diagnostic artifact for per-field unresolved, blocked, dependency, and attribution details.
- Do not add a separate unresolved-fields workspace artifact in this milestone unless the plan is revised.

Updated contracts:
- Workspace runner output set.
- `run-manifest.json` expected outputs.
- Golden workspace expected artifacts.

## Fixtures

Primary fixture:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/
```

Expected new artifacts:

```text
packages/sample_data/workspaces/basic_w2_1099_int_2025/expected/return-artifact.json
packages/sample_data/workspaces/basic_w2_1099_int_2025/expected/return-artifact.md
```

Fixture rules:
- Use only synthetic values already present in the workspace.
- Do not introduce personal taxpayer identifiers.
- Do not include absolute local paths.

## Tracks

### Track 19: Return Artifact Contract

Goal:
- Define the durable JSON shape for normalized federal return output.

Boundary:
- No generator logic.
- No runner output changes.
- No Markdown rendering.

Inputs:
- Existing field resolution artifact shape.
- Federal field catalog and form identifiers.

Outputs:
- `return-artifact` schema.
- Return artifact validation module or loader.
- Unit tests for valid synthetic return artifact shape.
- Contract coverage for the `resolution_summary` section.

Verification:
- Schema validation tests pass.
- `python3 -m unittest` passes.

Migration risk:
- None to existing workspace runner output.

Data safety:
- Any sample payload must be synthetic.

### Track 20: Return Artifact Generation

Goal:
- Generate `return-artifact.json` from `field-resolution.json`.

Boundary:
- No Markdown review yet.
- No persistence, API, UI, or PDF generation.

Inputs:
- Field resolution artifact.
- Return artifact schema from Track 19.

Outputs:
- Return artifact generator.
- Workspace runner writes `return-artifact.json`.
- Run manifest includes `return_artifact`.
- Generated return artifact includes `resolution_summary` derived from `field-resolution.json`.
- Runner and generator tests.

Verification:
- Generator tests pass.
- Workspace runner subprocess test proves `return-artifact.json` is written.
- Manifest test includes return artifact output.
- `python3 -m unittest` passes.

Migration risk:
- Workspace runner output shape changes.
- Run manifest expected fixture changes.

Data safety:
- Generated artifact must contain only synthetic workspace values.

### Track 21: Golden Return Fixture

Goal:
- Commit expected return artifact output for the basic synthetic workspace.

Boundary:
- No new generation behavior.
- No Markdown rendering.

Inputs:
- Return artifact generator from Track 20.
- Basic W-2 plus 1099-INT workspace fixture.

Outputs:
- `expected/return-artifact.json`.
- Golden artifact test coverage.

Verification:
- Golden workspace artifact test compares generated return artifact to expected return artifact.
- `python3 -m unittest` passes.

Migration risk:
- Golden expected artifacts change intentionally.

Data safety:
- Review fixture diff for personal values and absolute paths.

### Track 22: Human-Readable Return Review

Goal:
- Render the normalized return artifact as a human-readable Markdown review.

Boundary:
- No official PDF generation.
- No IRS layout replication.
- No UI.

Inputs:
- Return artifact JSON from Track 20.
- Golden return fixture from Track 21.

Outputs:
- Return review Markdown renderer.
- Workspace runner writes `return-artifact.md`.
- Run manifest includes return review output.
- Golden Markdown return review fixture.

Verification:
- Markdown renderer tests pass.
- Workspace runner subprocess test proves `return-artifact.md` is written.
- Golden workspace artifact test compares generated Markdown to expected Markdown.
- `python3 -m unittest` passes.

Migration risk:
- Workspace runner output shape changes.
- Run manifest expected fixture changes.
- Golden expected artifacts change intentionally.

Data safety:
- Markdown output must contain only synthetic values and no local paths.

## Dependencies

Fulfilled:
- Field resolution schema and artifact exist.
- Workspace runner exists.
- Run manifest exists.
- Golden workspace fixture infrastructure exists.

Pending:
- Track 20 depends on Track 19.
- Track 21 depends on Track 20.
- Track 22 depends on Track 20 and should use Track 21 golden output for final review fixtures.

## Constraints

- Do not change `field-resolution.json` shape in this milestone unless this plan is revised first.
- Do not introduce persistence, API, UI, PDF generation, or personal data.
- Do not update unrelated golden artifacts.
- Do not add a parallel work manifest unless explicitly requested.

## Conflict Hotspots

- `packages/schemas/*`
- `packages/tax_engine/tax_workspace_runs.py`
- `packages/tax_engine/runners/run_tax_workspace.py`
- `packages/sample_data/workspaces/basic_w2_1099_int_2025/expected/*`
- `tests/test_tax_workspace_golden_artifacts.py`
- `tests/test_run_manifest.py`
- `README.md`
- this milestone plan

## Verification

Per-track verification is listed in each track.

Milestone integration verification:

```bash
python3 -m unittest
```

Manual runner verification:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

Expected local outputs after milestone completion:

```text
local-data/runs/basic_w2_1099_int_2025/return-artifact.json
local-data/runs/basic_w2_1099_int_2025/return-artifact.md
```

## Exit Criteria

The milestone is complete when:
- Return artifact schema exists.
- Return artifact generation exists.
- Workspace runner emits `return-artifact.json`.
- Workspace runner emits `return-artifact.md`.
- Run manifest records both return artifacts.
- Golden expected return artifacts are committed.
- Tests cover schema, generation, runner output, manifest output, and golden artifacts.
- Full suite passes.
- Committed artifacts remain synthetic and portable.

## Planning Confirmation

Planning status:
- Confirmed complete for implementation.

Implementation status:
- Complete.
