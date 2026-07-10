# Milestone Plan: Code Review And Refactor

## Planning Status

Status: complete.

This milestone started after Workspace Workflow Service implementation review identified typing and application-boundary refactor gaps.

The plan was reviewed, confirmed complete by the orchestrating developer, and committed separately from implementation.

No parallel work manifest is included. Add one only if the user or orchestrating developer explicitly requests parallel execution planning for this milestone.

## Objective

Review the current Application Boundary Definition code and refactor the service, persistence, and product boundary so future application work starts from clearer typed boundaries.

This milestone specifically proves that type checking can become more globally applicable across the application instead of remaining a narrow ad hoc check on one new service module.

## Current State

Completed prerequisites:
- Product Boundary Contract is implemented.
- Local Workspace Persistence is implemented.
- Workspace Workflow Service is implemented.
- Baseline unit tests pass.
- Data safety checks pass.

Known gaps:
- The repository has no committed type checker configuration or typing dependency.
- Scoped type checks can be made to pass for touched service files, but full-repo mypy currently exposes missing third-party stubs and older typing gaps in imported engine modules.
- Many durable JSON payloads are schema-first dictionaries without shared Python `TypedDict`, dataclass, or generated type definitions.
- Tests are functional and remain in their current layout for this milestone.

## Scope

In scope:
- Review recent application-boundary code for type clarity, result contracts, exact-vs-latest workflow behavior, and avoidable duplication.
- Add an initial project type-checking setup that can run predictably in this repository.
- Make type checking more globally applicable by resolving enough cross-module typing issues to run beyond a single service file.
- Decide and document the near-term typing strategy for schema-backed JSON payloads.
- Refactor narrow seams where typing reveals unclear boundaries.
- Preserve synthetic-only fixture and data safety rules.

Out of scope:
- Broad product feature work.
- New UI or API behavior.
- New tax computation coverage.
- Large schema redesigns not required for typing or review clarity.
- Replacing JSON Schema validation with Python types.
- Making every historical module perfectly typed if a staged baseline is more practical.
- Rewriting tests into a different test framework.
- Moving or reorganizing the test directory layout.
- Updating project planning rules for future review/refactor checkpoints.
- Updating `AGENTS.md`; any code convention guidance from this milestone remains proposed discussion unless separately approved.

## Contracts

Type-checking decisions:
- Use mypy as the committed checker.
- Add mypy and `types-jsonschema` to dependencies.
- Add a root mypy configuration with strict settings for the scoped application-boundary baseline.
- Start with the application-boundary modules as the first committed type-check baseline:
  - `packages/tax_engine/product_boundary.py`
  - `packages/tax_engine/local_workspace_persistence.py`
  - `packages/tax_engine/workspace_workflow_service.py`
- Use hand-written `TypedDict`s for stable schema-backed payloads in the relevant owning modules, dataclasses for service-level in-process results, and local `JsonObject = dict[str, Any]` aliases only at JSON/schema boundaries.
- Do not introduce a recursive `JsonValue` alias in this milestone.
- Do not introduce generated JSON Schema types in this milestone.

Contract principles:
- Durable JSON schemas remain authoritative for persisted artifact shape.
- Python types should clarify in-process contracts and application boundaries, not replace schema validation.
- Use `dict[str, Any]` only at JSON/schema boundaries unless a narrower type is practical.
- Use `TypedDict`, `Literal`, dataclasses, and type aliases for stable in-process application contracts.
- Exact workflow operations must remain explicit; exact-revision operations must not silently fall back to latest/current behavior.
- Refactors should improve boundary clarity without changing engine artifact outputs unless explicitly replanned.

## Fixtures

Expected fixture strategy:
- Prefer existing synthetic fixtures for type and refactor verification.
- Add no new committed fixtures unless a refactor introduces a new stable contract or test scenario.
- Keep generated type-check or test output out of committed fixtures.

Fixture rules:
- Use only synthetic demo data.
- Do not include personal taxpayer identifiers.
- Do not include absolute local machine paths.
- Keep ad hoc generated output under ignored paths such as `local-data/`.

## Verification

Baseline verification:

```bash
python3 -m unittest
```

Code review and refactor verification:
- Run focused tests for every changed module.
- Run the full unit suite.
- Run the data safety check when persistence, fixtures, manifests, paths, generated artifacts, or local storage behavior changes.
- Run the committed type-check command or baseline.
- Confirm type-check scope and known exclusions are documented if repo-wide clean checking is not achieved in one pass.
- Confirm committed changes do not alter engine artifact golden outputs unless explicitly intended.
- Confirm `git diff --check` passes.
- Confirm unrelated work is not staged before commit.

Final verification status:
- `python3 -m mypy` passed.
- Focused application-boundary tests passed.
- `python3 -m unittest` passed.
- Canonical workspace runner passed.
- `git diff --check` passed.

## Data Safety

This milestone remains synthetic-only.

Do not commit:
- Personal source documents.
- Real uploaded tax documents.
- Personal current-year fact instances.
- Personal manual entries.
- Prior returns.
- Generated artifacts derived from personal data.
- Absolute local machine paths in committed fixtures, manifests, run summaries, or run details.

Personal or ad hoc local work must stay under ignored paths such as:
- `local-data/`
- `temp/`
- `private-archive/`
- `uploads/`
- `generated/user/`

## Exit Criteria

This milestone is complete when:
- The project has a documented and runnable type-check baseline.
- Type checking applies across more than one newly touched service file and has a clear path toward broader coverage.
- Key application-boundary modules have clearer typed contracts.
- Focused tests, full unit tests, type checks, and applicable data safety checks pass.

## Tracks

Track 1: Type Checking Strategy And Baseline
- Goal: add the first committed mypy baseline and make it runnable by future contributors.
- Boundary: do not attempt a full typed rewrite of the whole engine if a staged baseline is safer.
- Inputs: current service typing gaps, existing schema-backed payloads, requirements, and verification commands.
- Outputs: root mypy config, mypy and `types-jsonschema` dependency updates, and documented application-boundary baseline scope.
- Verification: committed type-check command passes.
- Status: complete.
- Migration risk: medium because type-check configuration can expose historical issues.
- Data safety: no fixture or personal-data changes expected.

Track 2: Application Boundary Type Refactor
- Goal: make type checking more globally applicable across product boundary, local persistence, and workspace workflow service.
- Boundary: do not change durable JSON schemas or generated engine artifact shapes unless explicitly replanned.
- Inputs: product boundary contracts, local persistence contracts, workspace workflow service contracts, and schema loaders.
- Outputs: typed aliases, `TypedDict`s, dataclasses, or helper functions where they clarify stable in-process contracts.
- Verification: type checks and focused tests for changed modules.
- Status: complete.
- Migration risk: medium because broad typing may reveal unclear JSON payload assumptions.
- Data safety: no personal records or generated personal artifacts.

Track 3: Final Review And Verification
- Goal: perform a final review pass and verify the milestone before marking it complete.
- Boundary: do not add new product scope during final review.
- Inputs: all changed code, tests, type-check config, and planning docs.
- Outputs: final status update in milestone and roadmap docs.
- Verification: `git diff --check`, type-check baseline, focused tests, `python3 -m unittest`, and applicable data safety checks.
- Status: complete.
- Migration risk: low.
- Data safety: explicit review of committed fixtures and generated paths.
