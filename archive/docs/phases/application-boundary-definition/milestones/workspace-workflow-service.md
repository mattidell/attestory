# Milestone Plan: Workspace Workflow Service

## Planning Status

Status: complete milestone plan; implementation complete.

This milestone plan was reviewed, confirmed complete, committed, and implemented.

No parallel work manifest is included. Add one only if the user or orchestrating developer explicitly requests parallel execution planning for this milestone.

## Objective

Add a small application service layer that exposes workspace, source draft, run execution, run history, run detail, and artifact lookup operations on top of local persistence and the existing product boundary.

This milestone proves that future UI or API code can depend on product operations instead of filesystem layout, engine runner internals, or ad hoc fixture paths.

## Current State

Completed prerequisites:
- Product boundary contracts are implemented.
- Local workspace persistence is implemented.
- Product workspaces can be created, loaded, and listed from a caller-controlled storage root.
- Source draft revisions can be persisted and loaded.
- Product run payloads can be built from persisted draft revisions.
- Product boundary execution can persist run payloads, run summaries, run details, and generated engine artifacts.

Stable prior contracts:
- Product workspace.
- Product run payload.
- Product run summary.
- Product run detail.
- Product artifact references.
- Local storage layout and repository behavior from the Local Workspace Persistence milestone.

## Scope

In scope:
- Add a class-based service boundary for workspace creation, workspace loading, workspace listing, source draft creation, source draft revision creation, latest source draft loading, exact source draft revision loading, source draft revision listing, source draft archiving, run execution, run summary listing, latest run lookup, run detail loading, and artifact reference resolution.
- Keep the service storage-root controlled by callers and tests.
- Return product boundary payloads and explicit operation results rather than raw engine internals.
- Allow service conveniences that compose existing product boundary and local persistence behavior, such as latest-run-with-detail lookup, without creating UI or API assumptions.
- Add deterministic synthetic service fixtures only if needed to prove service behavior.
- Add focused tests for the service workflow over temporary storage roots.
- Update docs to describe the supported application workflow and service boundary.

Out of scope:
- Web UI.
- API server.
- Authentication or user account management beyond existing `owner_id`.
- Database server setup.
- Real personal document upload.
- OCR or source document parsing.
- New tax computation coverage.
- Official IRS PDF generation.
- Changing engine artifact schemas.
- Changing product boundary or storage contracts unless a gap is found and explicitly replanned.
- Introducing a new command-line runner unless the milestone plan is revised.

## Contracts

Service model decisions:
- The service should use a class-based boundary so callers can configure the storage root and repository dependencies once.
- Service methods should compose product boundary and local persistence contracts.
- The service should expose application actions, not storage implementation details.
- Product boundary payloads remain the application-facing durable payloads.
- The storage root remains caller-controlled.
- Service methods should return explicit operation result objects for success, validation, not-found, conflict, and execution-failure states.
- Operation result objects should be stable enough for future UI or API callers and should be tested as an application-facing service contract.
- Service conveniences may combine existing operations when they do not bypass persisted product records or expose storage internals as the primary contract.
- Service results and stored product records should not expose absolute local machine paths through committed product records.
- Artifact lookup should return a resolved object containing the logical artifact URI and the resolved local path or content metadata for runtime inspection, while stored product records keep relative or logical artifact URIs.
- Service operations should be deterministic for synthetic fixtures and tests.
- New source draft operations should create workspace-scoped draft records without requiring document parsing or personal document upload.
- Source draft revision operations should create immutable draft versions through the persistence layer without mutating prior revisions.
- Source draft read operations should support latest-revision lookup, exact-revision lookup, and revision-history listing.
- Source draft archive operations may mark drafts inactive or archived, but should not delete revision history.
- Run execution should support exact source draft revision IDs so callers can execute deterministic snapshots.
- Run execution may provide a convenience path that uses latest draft revisions, but the exact-revision path is the stable service contract.
- Run history should be derived from persisted immutable run summaries.

New contracts to consider during implementation:
- Explicit operation result objects for success, validation, not-found, conflict, and execution-failure states.
- Stable service error definitions or status codes if operation result objects need typed failure categories.

Contract principles:
- Do not duplicate product boundary schemas in service-specific shapes without a clear reason.
- Do not let UI or API assumptions leak into the service layer.
- Keep engine artifacts authoritative for computation and review content.
- Add schemas and validators for any new durable JSON artifact.

## Fixtures

Expected fixture strategy:
- Prefer temporary storage roots in tests.
- Reuse synthetic product boundary fixtures and local storage fixtures from earlier milestones.
- Add committed service fixtures only when they prove a stable service contract that cannot be covered by temporary fixtures.

Fixture rules:
- Use only synthetic demo workspace data.
- Use demo labels and obvious synthetic IDs.
- Use `data_classification: "synthetic_demo"`.
- Do not include personal taxpayer identifiers.
- Do not include absolute local machine paths.
- Keep ad hoc generated output under ignored paths such as `local-data/`.

## Verification

Baseline verification:

```bash
python3 -m unittest
```

Service verification:
- Tests create, load, and list workspaces through service functions.
- Tests create new source drafts, create new source draft revisions, load latest revisions, load exact revisions, list revision history, and archive drafts through service functions.
- Tests execute a synthetic workspace run through the service layer using exact source draft revision IDs.
- Tests cover latest-revision run execution as a convenience path if implemented.
- Tests list run summaries in deterministic order.
- Tests load the latest run and run detail through the service layer.
- Tests cover explicit operation result objects for success and expected failure states.
- Tests resolve artifact references without committing absolute local paths.
- Tests prove service functions do not mutate engine artifact shapes.

Data safety verification:
- Run the repository data safety check.
- Confirm committed service fixtures contain no absolute local paths.
- Confirm committed service fixtures use only synthetic demo data.
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
- Absolute local machine paths in committed fixtures, manifests, run summaries, or run details.

Personal or ad hoc local work must stay under ignored paths such as:
- `local-data/`
- `temp/`
- `private-archive/`
- `uploads/`
- `generated/user/`

## Exit Criteria

This milestone is complete when:
- Application service functions cover workspace creation, granular source draft creation and versioning, run execution, run history, run detail, and artifact lookup.
- Future UI or API code can exercise the supported workflow without depending on local storage layout or engine internals.
- Tests cover the full synthetic service workflow.
- Any new durable JSON payload has a schema and validator or loader.
- Documentation describes the service boundary and supported workflow.
- Data safety tests pass.

## Tracks

Track 1: Service boundary design
- Goal: define the class-based service module, operation names, explicit operation result objects, inputs, outputs, and ownership boundaries.
- Boundary: do not implement UI, API, or new persistence contracts; do not change product or storage contracts unless the plan is revised first.
- Inputs: product boundary contracts and local persistence contracts.
- Outputs: service module skeleton, operation result definitions, and documentation notes.
- Verification: focused import and shape tests.
- Migration risk: medium because operation results become a stable service contract.
- Data safety: synthetic fixtures only.

Status:
- Complete.

Track 2: Workspace and source draft operations
- Goal: expose workspace creation, loading, listing, source draft creation, source draft revision creation, exact revision loading, latest revision loading, revision history listing, and draft archiving.
- Boundary: do not add personal document intake or parsing.
- Inputs: persisted workspace and source draft records.
- Outputs: service functions and tests.
- Verification: temporary storage root tests.
- Migration risk: low if product contracts remain unchanged.
- Data safety: no personal records.

Status:
- Complete.

Track 3: Run execution and history operations
- Goal: build run payloads from selected exact source draft revision IDs in draft version history, optionally support latest-revision convenience execution, execute the product boundary workflow, persist results, and list run summaries.
- Boundary: do not change engine artifacts or committed golden workspace outputs.
- Inputs: persisted drafts and product boundary execution facade.
- Outputs: service run functions and tests.
- Verification: synthetic run execution tests.
- Migration risk: medium because this composes storage and engine workflow.
- Data safety: generated outputs stay under temporary or ignored paths.

Status:
- Complete.

Track 4: Run detail and artifact lookup operations
- Goal: load run details, provide allowed read convenience operations, and resolve artifact references for local inspection.
- Boundary: do not expose absolute paths in committed product records.
- Inputs: persisted run details and artifact references.
- Outputs: artifact lookup functions and tests.
- Verification: artifact reference resolution tests.
- Migration risk: medium if artifact URI assumptions need adjustment.
- Data safety: no committed absolute paths.

Status:
- Complete.

Track 5: Documentation and safety verification
- Goal: document the service workflow and verify data safety.
- Boundary: do not introduce new product scope.
- Inputs: implemented service behavior.
- Outputs: README or phase documentation updates.
- Verification: `python3 -m unittest` and data safety tests.
- Migration risk: low.
- Data safety: explicit review of committed fixtures and generated paths.

Status:
- Complete.
