# Agent Planning And Execution Summary: Code Review And Refactor

Date: 2026-07-02

## Thread Context

This thread covered planning review, decision clarification, implementation, verification, merge, and branch cleanup for the Application Boundary Definition milestone named Code Review And Refactor.

The milestone followed Product Boundary Contract, Local Workspace Persistence, and Workspace Workflow Service. Those earlier milestones created product-facing payload contracts, local filesystem persistence, and a class-based workflow service. This milestone existed as a cleanup and stabilization gate before continuing into more product-facing artifact review read models.

The work was planned and implemented on a feature branch, then merged into `main-next` with a merge commit named for the milestone. The local feature branch was deleted after the merge.

Relevant commits during the milestone work:
- `6c3356a` Approve code review and refactor plan
- `7fc8858` Add application boundary mypy baseline
- `94e7aef` Type application boundary payload contracts
- `a9ee369` Complete code review and refactor milestone
- `e41195c` Merge milestone Code Review And Refactor

## Nature Of The Milestone Work

This milestone was a technical stabilization milestone, not a product feature milestone.

The implementation added a first committed type-checking baseline and tightened application-boundary types around:
- Product boundary payloads and artifact references.
- Local workspace persistence repository inputs and outputs.
- Workspace workflow service result surfaces.

The milestone intentionally kept JSON Schema as the authoritative durable artifact contract. Python typing was added to clarify in-process boundaries and reduce anonymous dictionary use inside application-boundary code.

The work added:
- `mypy.ini` as the root mypy configuration.
- `mypy` and `types-jsonschema` to `requirements.txt`.
- A documented `python3 -m mypy` command in `README.md`.
- Strict mypy checking for the scoped application-boundary baseline:
  - `packages/tax_engine/product_boundary.py`
  - `packages/tax_engine/local_workspace_persistence.py`
  - `packages/tax_engine/workspace_workflow_service.py`
- Module-owned `TypedDict` payload contracts in the modules that own the relevant schema or behavior.
- Status updates marking the milestone complete in phase and milestone docs.

## What The Milestone Addresses

The milestone addressed the risk that application-boundary code was becoming too dependent on loosely typed `dict` payloads.

Before this milestone:
- The repository had no committed type checker configuration.
- Product, persistence, and service code worked, but many application-boundary records were represented as generic dictionaries.
- Full-repo type checking exposed historical engine typing gaps outside the intended cleanup boundary.
- Future application work would have had to build on service and persistence surfaces whose Python contracts were less explicit than their JSON schemas.

After this milestone:
- The project has a runnable scoped mypy baseline.
- Application-boundary modules are checked under strict mypy settings.
- Product workspaces, run payloads, run summaries, run details, artifact references, source draft references, local latest pointers, and run records have clearer in-process types.
- Runtime schema validation remains the authority for persisted JSON shapes.
- The project has a practical path to broader type-check coverage without forcing a full historical engine typing rewrite.

## Decisions Discussed With The User

Decision: use mypy.
- The user chose mypy as the type checker.
- This matters because the milestone needed one concrete, repeatable type-check command rather than an informal typing preference.

Decision: add mypy and `types-jsonschema` to requirements.
- The user chose to commit the type-checker dependency and JSON Schema stubs.
- This matters because future contributors and agents can run the same baseline without relying on local environment state.

Decision: use a root config, not only a documented scoped command.
- The user chose a root mypy configuration with a scoped baseline.
- This matters because config keeps type-checking options centralized while still avoiding a false claim that the whole repo is clean under mypy.

Decision: start with application-boundary modules.
- The baseline intentionally covers product boundary, local persistence, and workspace workflow service.
- This matters because those modules are the current architecture boundary for future application and review-model work.
- Historical engine modules remain outside the first baseline except as skipped imports.

Decision: use strict scoped mypy settings.
- The user chose the strict option to evaluate how noisy it would be.
- This matters because strict settings expose unclear payload and return contracts quickly, while the scoped file list keeps the work bounded.

Decision: do not use a recursive `JsonValue` alias.
- The user rejected recursive JSON typing for this milestone.
- This matters because recursive JSON unions can make ordinary JSON manipulation noisy and would distract from clarifying stable application-boundary records.

Decision: keep payload types with relevant modules.
- The user chose not to create a shared application boundary type module.
- This matters because ownership stays local: `product_boundary.py` owns product payload shapes, `local_workspace_persistence.py` owns persistence-specific records, and `workspace_workflow_service.py` owns service result objects.
- A separate type module is reserved for future genuinely generic base types, if they emerge.

Decision: use a hybrid payload typing strategy.
- `TypedDict` is used for stable JSON-shaped records.
- Dataclasses remain appropriate for service-level in-process results.
- `dict[str, Any]` remains a local JSON boundary escape hatch.
- This matters because durable JSON remains schema-first while Python code gains clearer in-process contracts.

Decision: remove test organization from milestone scope.
- The user noted that the test directory cannot stay flat forever, but chose to leave test movement out of this milestone.
- This matters because moving tests during a typing/refactor milestone would add noisy diffs and make behavioral review harder.

Decision: remove future planning-rule changes from scope.
- The user chose to handle future code reviews ad hoc rather than adding a required Code Review And Refactor checkpoint to every future milestone.
- This matters because the milestone should improve current code boundaries without expanding repository process rules.

Decision: remove AGENTS.md updates from scope.
- The user asked for proposed AGENTS.md language to be output in the chat instead of applied.
- This matters because code conventions were discussed, but the milestone should not change agent operating rules without separate approval.

Decision: implement with pull-request-style branch workflow and one commit per track.
- The work was done on `codex/code-review-and-refactor`, then merged back with a merge commit.
- This matters because the milestone history remains reviewable by track rather than compressed into one broad implementation commit.

## Related But Left Out Of Scope

The milestone deliberately left out:
- Broad product feature work.
- New UI or API behavior.
- New tax computation coverage.
- Large schema redesigns.
- Replacing JSON Schema validation with Python types.
- Full-repo mypy cleanup.
- Generated Python types from JSON Schema.
- A recursive `JsonValue` model.
- Moving or reorganizing the test directory layout.
- Updating `PROJECT_PLANNING.md` to require future review/refactor checkpoints.
- Updating `AGENTS.md` with code conventions.
- Creating a shared application-boundary type module.

These exclusions kept the milestone focused on making the existing application boundary safer before building more application-facing review data.

## Verification Performed

Focused type verification:

```bash
python3 -m mypy
```

Result:
- Passed.
- Checked the three configured application-boundary source files.

Focused test verification:

```bash
python3 -m unittest tests.test_product_boundary tests.test_local_workspace_persistence tests.test_workspace_workflow_service
```

Result:
- Passed.
- 14 tests.

Full baseline verification:

```bash
python3 -m unittest
```

Result:
- Passed.
- 72 tests.

Workspace runner verification:

```bash
python3 -m packages.tax_engine.runners.run_tax_workspace \
  --workspace packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json \
  --output-dir local-data/runs/basic_w2_1099_int_2025
```

Result:
- Passed.
- Artifacts were generated under ignored `local-data/`.

Whitespace verification:

```bash
git diff --check
```

Result:
- Passed.

## Important Implementation Notes

The root mypy config uses scoped files and strict per-module settings. It also uses skipped imports so the first baseline does not try to type-check historical engine modules that are outside this milestone.

This is intentionally a staged baseline:
- The application boundary is checked strictly.
- Imported historical engine modules are not yet part of the guarantee.
- Broader mypy coverage can be added module by module in future milestones.

The payload typing strategy is module-owned:
- Product payload types live with product boundary behavior.
- Persistence-specific records live with local persistence behavior.
- Service dataclasses remain with workflow service behavior.

The implementation uses casts after schema validation when converting loaded JSON dictionaries into `TypedDict` shapes. This reflects the project contract: JSON Schema validates durable shapes at runtime, while Python types clarify in-process usage after validation.

## Proposed AGENTS.md Guidance Discussed But Not Applied

The thread produced proposed AGENTS.md guidance, but the user chose not to apply it during this milestone.

The proposed guidance covered:
- Public service and repository boundaries should have explicit parameter and return types.
- Use `dataclass`, `TypedDict`, `Literal`, and type aliases for stable in-process contracts.
- Keep schema-backed payload types with the module that owns the relevant schema or boundary behavior.
- Use shared type modules only when a type is genuinely reused across package boundaries.
- Use `dict[str, Any]` only at JSON, schema, file, or third-party API boundaries unless a narrower type is practical.
- Durable JSON artifacts remain schema-first and still require schemas, loaders or validators, synthetic fixtures, and tests.
- Exact operations should not silently fall back to latest/current behavior.
- Before review or commit, run `git diff --check`, focused tests, applicable full tests, data safety checks when applicable, and type checks for typed boundary work.

This can be revisited later if the user wants repository-wide coding conventions.

## Follow-Up Points

Potential follow-up work:
- Decide when to broaden mypy beyond the three application-boundary modules.
- Decide whether old engine modules should be typed opportunistically as future milestones touch them.
- Revisit test directory organization once the value outweighs the diff churn.
- Consider a future shared type module only if generic base response or base payload types emerge naturally.
- Decide whether service create/update methods should eventually accept narrower source draft `TypedDict`s instead of `JsonObject`.
- Review whether `follow_imports = skip` should be removed or narrowed as imported engine modules become typed.
- Consider adding a CI-style command list once type checking becomes part of regular verification.
- Revisit AGENTS.md code convention guidance if ad hoc review starts repeating the same typing or review comments.
- Check whether agent-comments files are intended to be committed, ignored, or kept as local-only working notes.
