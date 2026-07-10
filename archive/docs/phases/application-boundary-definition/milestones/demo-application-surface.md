# Milestone Plan: Demo Application Surface

## Planning Status

Status: draft future milestone plan; implementation not started.

This milestone should start after Artifact Review Read Models is implemented, verified, and committed.

No parallel work manifest is included. Add one only if the user or orchestrating developer explicitly requests parallel execution planning for this milestone.

## Objective

Provide a focused demo application surface that lets a user create or load a synthetic workspace, edit supported W-2 and 1099-INT source drafts, run the workspace, view run history, and inspect generated review artifacts.

This milestone proves the Application Boundary Definition phase as a usable product slice without introducing real personal data intake.

## Current State

Expected prerequisites:
- Product boundary contracts are implemented.
- Local workspace persistence is implemented.
- Workspace Workflow Service exposes stable application operations.
- Artifact Review Read Models expose reviewable validation, coverage, resolution, return summary, and Markdown review content.
- Synthetic demo fixtures exist for the basic W-2 and 1099-INT workspace.

## Scope

In scope:
- Add a minimal user-facing demo surface for the supported synthetic federal workflow.
- Support workspace selection or creation for synthetic demo data.
- Support editing supported source draft fields for W-2 and 1099-INT records.
- Support saving source draft revisions.
- Support running the workspace through the service layer.
- Support viewing run history and latest run status.
- Support inspecting validation, coverage, resolution, return summary, and Markdown review content.
- Add tests appropriate to the chosen surface.
- Update README or docs with the demo workflow and commands.

Out of scope:
- Real personal document upload.
- OCR or automatic document parsing.
- Authentication or multi-user account management beyond existing `owner_id`.
- Production deployment.
- Database server setup.
- State returns.
- New tax computation coverage.
- Official IRS PDF generation.
- E-file or filing submission.
- Payment or refund integrations.
- Tax advice.
- Broad design system work.

## Contracts

Application surface decisions:
- The surface should call the Workspace Workflow Service and Artifact Review Read Models, not raw engine modules or storage internals.
- Demo mode must remain synthetic-only and safe to share publicly.
- Source draft edits should persist as revisions.
- Run execution should create immutable run records.
- Run history should be read from persisted run summaries.
- Review views should be derived from persisted run artifacts.
- Any user-facing command or workflow must write local generated data under ignored paths by default.
- The surface should make unsupported scope explicit through product behavior or documentation rather than silently accepting unsupported tax situations.

New contracts to consider during implementation:
- A small demo app configuration file only if the surface needs durable settings.
- A UI/API response shape only if the chosen surface requires stable serialized responses.

Contract principles:
- Keep the application surface thin over service and read-model contracts.
- Avoid introducing persistence or engine shortcuts from the UI layer.
- Do not expand tax scope to make the demo look complete.
- Keep synthetic demo data clearly marked.

## Fixtures

Expected fixture strategy:
- Reuse synthetic product boundary and persistence fixtures.
- Use temporary storage roots for interaction tests where possible.
- Add committed UI or workflow fixtures only when needed for stable contract tests.

Fixture rules:
- Use only synthetic demo workspace data.
- Use demo labels and obvious synthetic IDs.
- Use `data_classification: "synthetic_demo"`.
- Do not introduce personal taxpayer identifiers.
- Do not include absolute local machine paths.
- Keep ad hoc generated output under ignored paths such as `local-data/`.

## Verification

Baseline verification:

```bash
python3 -m unittest
```

Surface verification:
- Tests cover creating or loading a synthetic workspace through the surface.
- Tests cover editing and saving supported source draft fields.
- Tests cover running the workspace through the service layer.
- Tests cover viewing run history and latest run status.
- Tests cover inspecting validation, coverage, resolution, return summary, and Markdown review content.
- Tests prove generated data defaults to ignored local paths.

Data safety verification:
- Run the repository data safety check.
- Confirm committed surface fixtures contain no absolute local paths.
- Confirm committed surface fixtures use only synthetic demo data.
- Confirm generated local outputs stay under ignored paths.

## Data Safety

This milestone remains synthetic-only.

Do not commit:
- Personal source documents.
- Real uploaded tax documents.
- Personal current-year fact instances.
- Personal manual entries.
- Prior returns.
- Generated artifacts derived from personal data.
- Absolute local machine paths in committed fixtures, manifests, run summaries, run details, review models, or app configuration.

Personal or ad hoc local work must stay under ignored paths such as:
- `local-data/`
- `temp/`
- `private-archive/`
- `uploads/`
- `generated/user/`

## Exit Criteria

This milestone is complete when:
- A user can operate the supported synthetic workflow through the demo surface.
- Source draft edits persist as revisions.
- Workspace runs execute through the service layer.
- Run history and generated artifacts are inspectable through product-facing review models.
- Demo mode remains synthetic-only and safe to share publicly.
- Tests cover the primary demo workflow.
- Documentation explains how to run and verify the demo.
- Data safety tests pass.

## Tracks

Track 1: Surface choice and workflow design
- Goal: choose the minimal demo surface and define supported user workflows.
- Boundary: do not start broad UI design or deployment work.
- Inputs: service and read-model contracts.
- Outputs: app structure and workflow documentation.
- Verification: import or smoke tests for the chosen surface.
- Migration risk: medium because this sets the application entrypoint.
- Data safety: synthetic defaults only.

Track 2: Workspace and source draft interactions
- Goal: let users create or load synthetic workspaces and edit supported source draft fields.
- Boundary: do not add real document upload or parsing.
- Inputs: Workspace Workflow Service.
- Outputs: interaction code and tests.
- Verification: source draft revision tests through the surface.
- Migration risk: medium.
- Data safety: no personal intake.

Track 3: Run execution and history interactions
- Goal: let users run the workspace and inspect run history.
- Boundary: do not call engine internals directly.
- Inputs: Workspace Workflow Service.
- Outputs: run interaction code and tests.
- Verification: synthetic run workflow tests.
- Migration risk: medium.
- Data safety: generated outputs stay ignored.

Track 4: Artifact review interactions
- Goal: let users inspect validation, coverage, resolution, return summary, and Markdown review outputs.
- Boundary: do not modify review artifact contracts.
- Inputs: Artifact Review Read Models.
- Outputs: review interaction code and tests.
- Verification: review display or response tests.
- Migration risk: medium because this validates read-model adequacy.
- Data safety: synthetic review content only.

Track 5: Documentation and phase readiness review
- Goal: document the demo workflow and evaluate whether Application Boundary Definition exit criteria are met.
- Boundary: do not transition phases without explicit review.
- Inputs: completed demo behavior.
- Outputs: README and phase roadmap status updates.
- Verification: `python3 -m unittest`, demo smoke test, and data safety tests.
- Migration risk: low.
- Data safety: explicit final safety review.
