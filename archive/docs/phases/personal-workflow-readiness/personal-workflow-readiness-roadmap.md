# Personal Workflow Readiness Roadmap

## Roadmap

### Milestone 1: Mode Separation Contract

Define the contract that separates synthetic demo workspaces from personal workspaces across storage, services, API responses, UI labels, logs, and generated artifacts.

This milestone matters because personal data safety depends on unambiguous mode boundaries before any personal workflow is enabled.

### Milestone 2: Personal Storage Controls

Implement local personal storage defaults, ignored output locations, path validation, and configuration rules for personal workspaces and generated artifacts.

This milestone matters because personal data should never be written through the same assumptions used for committed synthetic fixtures.

### Milestone 3: Export And Deletion Workflows

Add explicit workflows for exporting a personal workspace and deleting personal workspace data, generated artifacts, and related indexes.

This milestone matters because personal workflows are not credible without a way to retrieve and remove local data.

### Milestone 4: Redaction And Support Bundles

Define redacted diagnostic outputs and support bundle rules that preserve run structure without exposing personal values.

This milestone matters because debugging personal workflows requires artifacts that can be inspected safely.

### Milestone 5: Personal Workflow Safety Review

Run a phase-level safety review covering fixtures, manifests, logs, exports, deletion behavior, documentation, and user-facing warnings.

This milestone matters because the phase should prove personal workflow readiness before tax scope expands.

## Status

Phase status:
- Future high-level phase.

Active milestone:
- None.

Implementation notes:
- This phase should not begin until Shareable Portfolio Application is complete.
- Milestone plans should be created under `docs/phases/personal-workflow-readiness/milestones/` before implementation.
- The phase should preserve synthetic demo mode as the publicly shareable path.

Project impact:
- Data safety controls.
- Local storage and export behavior.
- Logs and diagnostics.
- Support artifacts.
- Documentation and user-facing boundaries.
