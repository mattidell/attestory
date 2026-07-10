# Agent Planning And Execution Summary: Local Workspace Persistence

Date: 2026-07-02

## Thread Context

This thread covered planning, decision clarification, implementation, verification, and commit cleanup for the Application Boundary Definition milestone named Local Workspace Persistence.

The milestone follows Product Boundary Contract work. Product Boundary Contract established product-facing workspace, run payload, run summary, run detail, and artifact reference contracts around the existing engine workflow. Local Workspace Persistence then gave those product contracts a filesystem-backed place to live without introducing a UI, API, database, authentication, or personal-data intake.

The planning work was committed separately before implementation, per repository planning rules. Follow-up planning clarifications were squashed/amended into the planning commit after the user noted that plan updates should be squashed.

Relevant commits at completion:
- `58c0755 Plan local workspace persistence`
- `b5f2829 Add local workspace persistence`

## Nature Of The Milestone Work

This milestone implemented a local filesystem repository boundary for synthetic product workspaces.

The implementation added:
- A `LocalWorkspaceRepository` service module.
- A storage-owned `local-source-draft-latest` schema for `latest.json` pointer metadata.
- Synthetic committed local persistence fixtures.
- Tests for workspace creation, workspace listing, source draft revision persistence, latest-draft loading, run payload construction, run execution/persistence, run summary listing, latest-run derivation, artifact reference resolution, duplicate run protection, and fixture validation.
- README documentation for the local storage layout.
- Phase and milestone status updates marking Local Workspace Persistence complete.

The repository stores product records and generated artifacts under a caller-provided storage root:

```text
<storage-root>/
  workspaces/
    <owner-id>/
      <workspace-id>/
        workspace.json
        source-drafts/
          <draft-id>/
            <revision-id>.json
            latest.json
        runs/
          <run-id>/
            product-run-payload.json
            product-run-summary.json
            product-run-detail.json
            artifacts/
              normalized-source-documents.json
              source-validation.json
              field-coverage.json
              field-resolution.json
              return-artifact.json
              return-artifact.md
              field-coverage.md
              run-manifest.json
```

The storage layer consumes product boundary contracts rather than redefining workspace or run shapes. Product contracts remain the application-facing interface; storage path resolution stays internal.

## What The Milestone Addresses

This milestone addresses the persistence gap between product boundary contracts and a future application surface.

Before this work, the project had product-shaped payloads and an execution facade, but no durable local repository for:
- user-owned product workspaces,
- workspace-scoped editable source draft revisions,
- immutable product run payloads,
- run summaries and run details,
- generated engine artifacts,
- run history listing,
- latest draft and latest run lookup.

The milestone makes the next application-layer work possible because future UI or service code can use one local repository boundary for workspace state and run history. It keeps the engine workflow stable and avoids making persistence details part of engine artifact contracts.

## User Decisions Discussed

Several milestone-shaping decisions were discussed and recorded in the plan.

Decision: derive workspace and run listings.
- The user chose derived listings rather than explicit index files.
- This matters because it keeps the first persistence boundary simpler and avoids introducing mutable index contracts before the storage shape proves it needs them.

Decision: caller-configurable storage root with a default convention.
- The user chose caller-configurable storage with a local default convention.
- The plan and README use ignored local paths such as `local-data/workspaces/` for ad hoc storage.
- This matters because tests can use temporary directories, local experiments stay out of committed fixtures, and future application code can choose its own storage root.

Decision: `latest.json` as pointer metadata.
- The user accepted the default of immutable source draft revision files plus `latest.json` as a small pointer/metadata file.
- This matters because draft updates do not mutate prior revisions or duplicate full payloads in the latest pointer.
- Because `latest.json` is a durable storage-owned JSON artifact, the implementation added a schema for it.

Decision: hybrid run history behavior.
- The user chose append-only immutable run history plus a derived current/latest run view.
- Completed runs are not overwritten.
- Latest run is derived from stored run summary timestamps.
- This matters because it preserves auditability while still supporting ergonomic application behavior like “show the latest result.”

Decision: no new runner.
- The user chose not to add a command-line runner for this milestone.
- The implementation is repository/service behavior with tests and documentation.
- This matters because the milestone is a storage boundary, not a user-facing workflow surface.

Decision: no partial-write recovery now.
- The user chose to defer partial-write recovery and durable failed-run records.
- The implementation persists completed/succeeded runs and rejects duplicate run directories.
- This matters because it avoids expanding the product status/failure model before the application surface needs it.

Decision: otherwise defaults.
- Defaults kept artifact references in the current relative URI shape, such as `runs/<run-id>/...`.
- Defaults kept committed synthetic fixtures focused on product/storage records, while generated artifact persistence is verified in temporary directories.
- Defaults avoided new storage-owned schemas unless a durable storage artifact required one.

## Related But Out Of Scope

The milestone deliberately left these out of scope:
- Web UI.
- API server.
- Authentication or user account management beyond existing `owner_id`.
- Database server setup.
- Real personal document upload.
- OCR or automatic source document parsing.
- State returns.
- New tax computation coverage.
- Official IRS PDF generation.
- New command-line runner.
- Partial-write recovery.
- Durable failed-run records.
- Encryption.
- Cross-device synchronization.
- Import/export packaging.
- Deletion and retention policy for personal data.
- Migration tooling for future schema versions.

These exclusions matter because the phase priority is application boundary definition around stable engine contracts. Persistence needed to become concrete enough for future application work, but not broad enough to pull in product UI, account, sync, or personal-data lifecycle concerns prematurely.

## Verification Performed

Focused verification:

```bash
python3 -m unittest tests.test_local_workspace_persistence
```

Result:
- Passed.
- 6 tests.

Baseline verification:

```bash
python3 -m unittest
```

Result:
- Passed.
- 69 tests.

Data safety verification:

```bash
python3 tools/check_data_safety.py
```

Result:
- Passed.
- No personal-data guardrail violations found.

## Important Implementation Notes

The committed fixture tree lives under:

```text
packages/sample_data/local_workspace_persistence/basic_2025/
```

The fixture includes product/storage records:
- `workspace.json`
- source draft revision payloads
- source draft `latest.json` pointer files
- product run payload
- product run summary
- product run detail

It does not include a full generated artifact tree. Generated artifact persistence is tested in temporary directories so committed fixture churn stays focused.

The repository uses path segment validation for owner IDs, workspace IDs, draft IDs, revision IDs, run IDs, and resolved artifact file names. Product records keep relative URIs; absolute local paths are not exposed through committed records.

`run-manifest.json` is generated as a local persisted artifact for runs. It references product run payloads, source draft revision files, product run records, and engine artifacts using relative storage paths.

Completed runs are protected from accidental overwrite by rejecting persistence when the run directory already exists.

## Follow-Up Points

Potential follow-up work:
- Plan or begin the Application Surface milestone now that local persistence is available.
- Decide whether future UI/service work should consume `LocalWorkspaceRepository` directly or wrap it in a higher-level application workflow service.
- Decide when to introduce durable failed-run records and a broader run status model.
- Decide whether partial-write recovery should use staging directories, atomic rename, explicit failed records, or cleanup-only behavior.
- Decide whether derived listings remain sufficient once there are many workspaces/runs, or whether a storage index becomes useful.
- Decide whether artifact review needs additional read models over persisted `field-coverage`, `field-resolution`, `return-artifact`, and Markdown artifacts.
- Decide when personal-data storage, deletion, retention, export, and privacy boundaries should be planned before real uploads are allowed.
- Consider migration/versioning strategy before changing any committed storage-owned schema beyond `local-source-draft-latest`.
