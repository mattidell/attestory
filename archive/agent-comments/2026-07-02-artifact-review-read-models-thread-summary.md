# Agent Planning And Execution Summary: Artifact Review Read Models

Date: 2026-07-02

## Thread Context

This thread covered planning review, decision clarification, implementation, review-model inspection, milestone completion, and merge for the Application Boundary Definition milestone named Artifact Review Read Models.

The milestone followed Product Boundary Contract, Local Workspace Persistence, Workspace Workflow Service, and Code Review And Refactor. Those earlier milestones created product-facing run contracts, local persisted workspaces and artifacts, a service boundary for workspace workflows, and a scoped mypy baseline for application-boundary modules.

This milestone was implemented on `codex/artifact-review-read-models` and merged into `main` with a non-fast-forward merge commit named for the milestone.

Relevant commits during this milestone work:
- `bfac191` Approve artifact review read model plan
- `311b0a0` Add artifact review read model shell
- `a0fa311` Add validation and coverage review models
- `3cd0a46` Add resolution and return review models
- `b98d83b` Load artifact review models through service
- `f223164` Document artifact review read models
- `5e8c906` Complete artifact review read models milestone
- `4a3192b` Merge milestone Artifact Review Read Models

## Nature Of The Milestone Work

This milestone added product-facing, in-memory read models for reviewing completed run artifacts.

The work did not change the engine artifacts themselves. Instead, it added a derived application layer that reads persisted run artifacts through `ProductRunDetailPayload` artifact references and presents smaller review-oriented sections for application code.

The main implementation added:
- `packages/tax_engine/artifact_review_read_models.py`
- `tests/test_artifact_review_read_models.py`
- `WorkspaceWorkflowService.get_run_review(...)`
- `WorkspaceWorkflowService.get_latest_run_review(...)`
- README and phase documentation for the review boundary.

The aggregate run review model carries run provenance:
- `schema_version`
- `run_id`
- `workspace_id`
- `tax_year`
- `data_classification`
- `sections`

The aggregate model currently includes sections for:
- `source_validation`
- `field_coverage`
- `field_resolution`
- `return_artifact`
- `return_review_markdown`
- `field_coverage_markdown`

Each section preserves artifact reference metadata such as artifact type, media type, and URI. Missing artifact files become explicit unavailable sections rather than changing workspace or run not-found behavior.

## What The Milestone Addresses

Before this milestone, product/application code could load run details and resolve artifact references, but it still had to understand raw engine artifact files directly to render validation, coverage, resolution, and return review information.

This created a coupling problem:
- UI or API code would need to know raw artifact file names and shapes.
- Engine artifacts would become de facto product contracts.
- Missing artifact behavior was not represented as product review state.
- Markdown review content did not have a product-level wrapper.

After this milestone:
- Application code can request an exact-run or latest-run review from `WorkspaceWorkflowService`.
- Product-facing review data is available as derived in-memory read models.
- Engine artifacts remain authoritative and unchanged.
- Review sections are smaller and easier to render than raw engine artifacts.
- Missing review artifact files are represented inside the aggregate read model.
- No durable read-model JSON artifacts were introduced.

## Decisions Discussed With The User

Decision: start with in-memory read models.
- The user approved using in-memory projections instead of durable JSON read-model artifacts.
- This matters because durable JSON artifacts would require new schemas, validators, fixtures, and data-safety checks. The milestone needed a product review boundary, not another persisted artifact contract.

Decision: keep engine artifacts authoritative.
- The read models derive from existing persisted artifacts and do not replace them.
- This matters because the engine contract remains stable and golden fixture coverage continues to protect canonical artifact shapes.

Decision: provide one aggregate review model plus section builders.
- The user approved one aggregate `ProductRunReviewReadModel` along with smaller builders for validation, coverage, resolution, return summary, and Markdown sections.
- This matters because a future UI likely needs one review page load, while tests and future code still benefit from section-level functions.

Decision: add service convenience methods.
- The implementation added exact-run and latest-run review methods to `WorkspaceWorkflowService`.
- This matters because future UI or API code should call the application service boundary rather than assembling paths or reading artifact files directly.

Decision: represent missing review artifacts as unavailable sections.
- Missing review artifact files do not make the whole run review fail.
- This matters because missing workspace or run records are different from a partial review artifact set. The service can still return the run review with precise section-level availability.

Decision: wrap and trim coverage review data.
- The milestone did not expose raw field coverage as the product-facing contract.
- This matters because coverage artifacts contain more detail than a review surface needs, and exposing them wholesale would make UI code depend on engine artifact shape.

Decision: keep Markdown as plain text content.
- Markdown review artifacts are wrapped with metadata and content, not parsed into a rich text model.
- This matters because the current application need is display/review, not editing or structured document manipulation.

Decision: include grouped return summary details.
- The return review model includes grouped form fields, status counts, blocked fields, and optional unpopulated fields.
- This matters because those are the natural review concepts already present in the return artifact and Markdown review.

Decision: follow the milestone branch and per-track commit protocol.
- Planning was committed separately on `main`, implementation happened on `codex/artifact-review-read-models`, tracks were committed separately, and the branch was merged with a milestone-named non-fast-forward merge commit.
- This matters because the milestone history remains reviewable and aligned with `AGENTS.md`.

## Related But Left Out Of Scope

The milestone deliberately left out:
- Web UI.
- API server.
- Editing computed results through review views.
- New tax computation coverage.
- Official IRS PDF generation.
- Changing engine artifact schemas.
- Changing product boundary or storage contracts beyond adding service review methods.
- Durable read-model JSON artifacts.
- New read-model JSON schemas.
- Broad reporting or analytics.
- Markdown AST parsing or rich text editing.
- Personal data workflows.
- Real tax document upload.

These exclusions kept the milestone focused on the application review boundary rather than expanding the product surface or engine scope.

## Verification Performed

Focused verification during implementation:

```bash
python3 -m unittest tests.test_artifact_review_read_models
python3 -m unittest tests.test_artifact_review_read_models tests.test_workspace_workflow_service
python3 -m unittest tests.test_artifact_review_read_models tests.test_workspace_workflow_service tests.test_data_safety
```

Full verification before milestone completion:

```bash
git diff --check
python3 -m mypy
python3 -m unittest
python3 tools/check_data_safety.py
```

Final verification after merge to `main`:

```bash
python3 -m unittest
python3 -m mypy
python3 tools/check_data_safety.py
git diff --check
```

Results:
- Full unit suite passed with 87 tests.
- Scoped mypy passed.
- Data safety check passed.
- Whitespace check passed.
- Worktree was clean after merge.

## Important Implementation Notes

The new read models are in-memory only. They are not written to disk and do not have JSON schemas.

The aggregate read model is built from a product run detail and resolved artifact paths. The service methods are responsible for loading the run detail and resolving artifact references through the existing repository boundary.

Missing artifact files are handled differently from missing runs:
- Missing workspace or run records still produce service-level not-found results.
- Missing review artifact files produce unavailable sections inside an otherwise successful aggregate review model.

Coverage and resolution views intentionally use counts, status summaries, grouped fields, and small row objects rather than duplicating full source attributions and values from raw artifacts.

Return summary review includes values for return artifact fields because those fields are the user-facing return outputs.

Markdown review content is returned as plain text with a label and artifact metadata.

## Follow-Up Points

Potential follow-up work:
- Review the Demo Application Surface milestone plan now that review models exist.
- Decide whether the demo surface should consume the aggregate review model directly or request individual sections.
- Decide whether the future API boundary should expose the same aggregate shape or a narrower transport-specific projection.
- Decide whether read models should eventually become durable JSON artifacts if a UI needs cached review snapshots.
- Consider adding schemas only if review models become durable or cross-process API payloads.
- Consider extending read models when new tax source types or return sections are introduced.
- Consider whether Markdown previews should be truncated or streamed in a future UI/API layer.
- Consider adding section-level filter helpers if review screens need to show only blocked, missing, computed, or optional fields.
- Revisit broader mypy coverage if artifact review code becomes part of the strict checked baseline.

## Current Project State After This Thread

The repository is on `main`.

Artifact Review Read Models is marked complete.

The next planned Application Boundary Definition milestone is Demo Application Surface.

The feature branch `codex/artifact-review-read-models` still exists locally after merge unless separately deleted.
