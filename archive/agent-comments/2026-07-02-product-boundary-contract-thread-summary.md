# Agent Planning And Execution Summary: Product Boundary Contract

Date: 2026-07-02

## Thread Context

This work thread covered the transition from Engine Contract Stabilization into Application Boundary Definition.

The project already had a deterministic synthetic federal engine workflow: source document drafts, normalized source documents, source validation, direct mappings, field coverage, field resolution, return artifact, return review, and run manifest. The open question was what a product should consume from that workflow without coupling future persistence, API, or UI code directly to engine internals or fixture layout.

The user reviewed and approved the first Application Boundary Definition milestone plan, then instructed execution.

## Nature Of The Work

The milestone was Product Boundary Contract.

The work defined the application-facing contract around the engine workflow. It did not build a UI, database, API server, or personal-data workflow. Instead, it introduced the product concepts and durable payloads that later persistence and application surfaces can depend on:
- Product workspace.
- Product run payload.
- Product run summary.
- Product run detail.
- Artifact reference.
- Synthetic demo data classification.

Implementation followed the repository's contract-first pattern:
- Markdown milestone planning.
- JSON schemas.
- Synthetic fixtures.
- Validators and builders.
- Tests.
- Documentation and roadmap status updates.

## What This Milestone Addresses

This milestone answers what the product boundary is.

The product is not the engine runner itself. The runner is a project execution tool. The product boundary is the layer a future persisted workflow, API, or UI should consume.

The implemented model draws these boundaries:
- A workspace is user-owned and specific to one tax year.
- A workspace has a jurisdiction list, currently limited to `["federal"]`.
- Source drafts are editable records scoped to a workspace.
- Source drafts carry `draft_id`, `revision_id`, and lifecycle status.
- A run payload is an immutable execution snapshot derived from workspace source drafts.
- Source draft snapshots are part of a run payload, not independent product objects.
- A run summary stays light and points toward detail.
- Run detail carries the full run payload and generated artifact references.
- Artifacts are addressed through typed references with URIs.
- Product fixtures use `data_classification: "synthetic_demo"`.

The implemented files include:
- `packages/schemas/product-workspace.schema.json`
- `packages/schemas/product-run-payload.schema.json`
- `packages/schemas/product-run-summary.schema.json`
- `packages/schemas/product-run-detail.schema.json`
- `packages/sample_data/product_boundary/*.json`
- `packages/tax_engine/product_boundary.py`
- `tests/test_product_boundary.py`

## Related But Left Out Of Scope

Several related topics were intentionally deferred.

Persistence was left out of scope. This milestone defines what Local Workspace Persistence should store, but it does not decide or implement a storage layout.

UI and API surfaces were left out of scope. The milestone creates contracts that future UI or API code can use, but it does not introduce interaction design, routes, forms, or service endpoints.

Authentication and ownership enforcement were left out of scope. The model includes `owner_id`, but there is no auth system.

State return execution was left out of scope. The user noted that state returns generally depend on federal returns and should not require separate workspaces. The chosen shape uses a workspace-level jurisdiction list so future state scopes can live inside the same tax-year workspace, but only `federal` is supported now.

Detailed failure modeling was left out of scope. The run summary currently stays simple; richer failure states can be added when persistence, service operations, or UI flows need them.

User review workflow state was left out of scope. Review remains artifact-based for now.

Broad configurability and extensibility were left out of scope. The contracts anticipate more document types and jurisdictions structurally, but validation remains narrow.

## Decisions Discussed With The User

The user decided that a workspace should be user-owned and tax-year-specific.

Why it matters:
- It gives persistence and run history a clear product container.
- It avoids making source drafts or runs float independently without owner, year, or workflow context.

The user questioned whether jurisdiction should be a single field.

Decision:
- Use a jurisdiction list instead of a single jurisdiction.
- Support only `federal` for now.

Why it matters:
- Future state returns can live inside the same tax-year workspace.
- The model leaves room for federal-to-state dependency without splitting one user's tax year into unrelated workspaces.

The user decided source drafts should exist in workspace context.

Why it matters:
- Drafts need owner, tax year, jurisdiction scope, lifecycle, and run history context.
- Workspace-scoped draft identity keeps the product model easier to persist and reason about.

The user raised versioning as a product distinction.

Decision:
- Editable source drafts remain mutable from the user perspective.
- Run payloads capture immutable snapshots for execution.

Why it matters:
- Users expect to edit source drafts.
- Runs need reproducibility and auditability after drafts change.

The user preferred run payload snapshots over independent snapshot product objects.

Why it matters:
- Independent snapshots may be useful internally, but they are confusing as product-level objects.
- "A run captured what it executed" is a clearer product concept.

The user asked what belongs in a run summary.

Decision:
- Keep run summary light.
- Put detailed payload and artifact references in run detail.

Why it matters:
- Run history views need compact status and counts.
- Artifact inspection and exact execution inputs belong in detail views.

The user noted artifacts are often addressed by paths or URIs.

Decision:
- Use artifact references with `uri`.
- Avoid absolute local machine paths in committed fixtures.

Why it matters:
- Later storage can use file paths, app-relative URIs, object storage URIs, or HTTP URLs without changing the contract shape.
- Fixtures remain portable and data-safe.

The user agreed to include data classification.

Why it matters:
- The project is synthetic-only now.
- Explicit classification creates a future boundary for personal data handling rather than letting it appear implicitly.

## Execution Notes

Planning was committed separately before implementation, following repository rules.

The implementation added product boundary schemas, fixtures, validators, and an execution facade. The facade executes a product run payload through the existing in-memory engine workflow and returns product-facing run summary and run detail data while preserving engine artifacts as authoritative outputs.

Verification at the time of execution:
- `python3 -m unittest` passed.
- `python3 tools/check_data_safety.py` passed.

The thread also updated planning/status docs so Application Boundary Definition became active and Product Boundary Contract was marked complete.

## Follow-Up Points

Useful follow-up areas:
- Local Workspace Persistence should consume these product boundary contracts rather than inventing new storage shapes.
- Persistence needs to decide how workspace draft revisions, immutable run payloads, run summaries, run details, and artifact references are stored.
- A future milestone can add richer run failure statuses once service operations and UI flows need them.
- A future milestone should clarify how state jurisdictions depend on federal outputs inside one tax-year workspace.
- A future milestone should decide how `data_classification` expands beyond `synthetic_demo` before personal data is allowed.
- Artifact URI semantics should be revisited when storage has a concrete backend.
- Review workflow state should remain separate from engine artifacts until there is a user-facing review surface.
- The safety checker could eventually inspect committed product fixtures for absolute paths and data classification, rather than relying only on path/name guardrails.
