from pathlib import Path
from tempfile import TemporaryDirectory
import copy
import unittest

from packages.tax_engine.local_workspace_persistence import (
    LocalWorkspaceRepository,
    load_source_draft_latest,
    schema_paths_for_local_storage,
    validate_local_storage_fixture,
)
from packages.tax_engine.product_boundary import load_product_workspace
from packages.tax_engine.source_document_drafts import load_source_document_draft_payload


ROOT = Path(__file__).resolve().parents[1]
PRODUCT_FIXTURE_DIR = ROOT / "packages" / "sample_data" / "product_boundary"
SOURCE_DRAFT_FIXTURE_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"
LOCAL_STORAGE_FIXTURE_ROOT = (
    ROOT / "packages" / "sample_data" / "local_workspace_persistence" / "basic_2025"
)

WORKSPACE_FIXTURE = PRODUCT_FIXTURE_DIR / "product-workspace.basic_2025.json"
W2_DRAFT_FIXTURE = SOURCE_DRAFT_FIXTURE_DIR / "w2_basic_draft.2025.json"
W2_UPDATED_DRAFT_FIXTURE = SOURCE_DRAFT_FIXTURE_DIR / "w2_updated_wages_draft.2025.json"
INT_DRAFT_FIXTURE = SOURCE_DRAFT_FIXTURE_DIR / "1099_int_basic_draft.2025.json"


def empty_workspace_fixture() -> dict:
    workspace = load_product_workspace(WORKSPACE_FIXTURE)
    workspace["source_drafts"] = []
    return workspace


class LocalWorkspacePersistenceTests(unittest.TestCase):
    def test_schema_files_exist_for_local_storage_contracts(self):
        self.assertTrue(all(path.exists() for path in schema_paths_for_local_storage()))

    def test_committed_local_storage_fixture_validates(self):
        validate_local_storage_fixture(LOCAL_STORAGE_FIXTURE_ROOT)
        repository = LocalWorkspaceRepository(LOCAL_STORAGE_FIXTURE_ROOT)

        workspaces = repository.list_workspaces("demo-owner")
        self.assertEqual([workspace["workspace_id"] for workspace in workspaces], ["demo-basic-w2-1099-int-2025"])

        workspace = workspaces[0]
        self.assertEqual(workspace["data_classification"], "synthetic_demo")
        self.assertTrue(all(not draft["uri"].startswith("/") for draft in workspace["source_drafts"]))

        latest_pointer = load_source_draft_latest(
            repository.source_draft_latest_path(
                "demo-owner",
                "demo-basic-w2-1099-int-2025",
                "demo-w2-acme-2025",
            )
        )
        self.assertEqual(latest_pointer["revision_id"], "demo-w2-acme-2025-rev-001")

        summaries = repository.list_run_summaries("demo-owner", "demo-basic-w2-1099-int-2025")
        self.assertEqual([summary["run_id"] for summary in summaries], ["demo-basic-w2-1099-int-2025-run-001"])

    def test_repository_saves_source_draft_revisions_without_mutating_prior_revision(self):
        with TemporaryDirectory() as temp_dir:
            repository = LocalWorkspaceRepository(Path(temp_dir))
            repository.create_workspace(empty_workspace_fixture())

            first_draft = load_source_document_draft_payload(W2_DRAFT_FIXTURE)
            second_draft = load_source_document_draft_payload(W2_UPDATED_DRAFT_FIXTURE)

            repository.save_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=first_draft,
            )
            first_revision_path = repository.source_draft_revision_path(
                "demo-owner",
                "demo-basic-w2-1099-int-2025",
                "demo-w2-acme-2025",
                "demo-w2-acme-2025-rev-001",
            )
            self.assertTrue(first_revision_path.exists())

            repository.save_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=second_draft,
            )

            latest = repository.load_latest_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_id="demo-w2-acme-2025",
            )
            workspace = repository.load_workspace("demo-owner", "demo-basic-w2-1099-int-2025")

            self.assertTrue(first_revision_path.exists())
            self.assertEqual(latest["source_revision_id"], "demo-w2-acme-2025-rev-002")
            self.assertEqual(workspace["source_drafts"][0]["revision_id"], "demo-w2-acme-2025-rev-002")
            self.assertFalse(workspace["source_drafts"][0]["uri"].startswith("/"))

    def test_repository_builds_run_payload_from_latest_active_drafts(self):
        with TemporaryDirectory() as temp_dir:
            repository = LocalWorkspaceRepository(Path(temp_dir))
            repository.create_workspace(empty_workspace_fixture())
            repository.save_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(W2_DRAFT_FIXTURE),
            )
            repository.save_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(W2_UPDATED_DRAFT_FIXTURE),
            )
            repository.save_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(INT_DRAFT_FIXTURE),
            )

            run_payload = repository.build_run_payload(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                run_id="demo-run-001",
            )

            revision_refs = {
                snapshot["draft_id"]: snapshot["revision_id"]
                for snapshot in run_payload["source_draft_snapshots"]
            }
            self.assertEqual(revision_refs["demo-w2-acme-2025"], "demo-w2-acme-2025-rev-002")
            self.assertEqual(
                revision_refs["demo-1099-int-example-bank-2025"],
                "demo-1099-int-example-bank-2025-rev-001",
            )

    def test_repository_executes_and_persists_run_history_and_artifacts(self):
        with TemporaryDirectory() as temp_dir:
            repository = LocalWorkspaceRepository(Path(temp_dir))
            repository.create_workspace(empty_workspace_fixture())
            repository.save_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(W2_DRAFT_FIXTURE),
            )
            repository.save_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(INT_DRAFT_FIXTURE),
            )

            first = repository.execute_and_persist_run(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                run_id="demo-run-001",
                created_at="2026-01-01T00:00:00Z",
                completed_at="2026-01-01T00:00:02Z",
            )
            second = repository.execute_and_persist_run(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                run_id="demo-run-002",
                created_at="2026-01-02T00:00:00Z",
                completed_at="2026-01-02T00:00:02Z",
            )

            summaries = repository.list_run_summaries("demo-owner", "demo-basic-w2-1099-int-2025")
            latest_summary = repository.latest_run_summary("demo-owner", "demo-basic-w2-1099-int-2025")
            run_payload = repository.load_run_payload("demo-owner", "demo-basic-w2-1099-int-2025", "demo-run-001")
            detail = repository.load_run_detail("demo-owner", "demo-basic-w2-1099-int-2025", "demo-run-001")
            detail_path = repository.resolve_artifact_ref(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                artifact_ref=first["run_summary"]["detail_ref"],
            )
            artifact_path = repository.resolve_artifact_ref(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                artifact_ref=first["run_detail"]["artifact_refs"][0],
            )
            manifest_ref = next(
                ref for ref in first["run_detail"]["artifact_refs"] if ref["artifact_type"] == "run_manifest"
            )
            manifest_path = repository.resolve_artifact_ref(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                artifact_ref=manifest_ref,
            )

            self.assertEqual([summary["run_id"] for summary in summaries], ["demo-run-001", "demo-run-002"])
            self.assertEqual(latest_summary["run_id"], second["run_summary"]["run_id"])
            self.assertEqual(run_payload["run_id"], "demo-run-001")
            self.assertEqual(detail["run_payload"]["run_id"], "demo-run-001")
            self.assertTrue(detail_path.exists())
            self.assertTrue(artifact_path.exists())
            self.assertTrue(manifest_path.exists())
            self.assertIn("artifacts", artifact_path.parts)
            self.assertFalse(first["run_summary"]["detail_ref"]["uri"].startswith("/"))
            self.assertTrue(all(not ref["uri"].startswith("/") for ref in first["run_detail"]["artifact_refs"]))

            with self.assertRaises(FileExistsError):
                repository.persist_run_records(
                    owner_id="demo-owner",
                    workspace_id="demo-basic-w2-1099-int-2025",
                    run_payload=copy.deepcopy(first["run_payload"]),
                    run_summary=copy.deepcopy(first["run_summary"]),
                    run_detail=copy.deepcopy(first["run_detail"]),
                    engine_result=copy.deepcopy(first["engine_result"]),
                )

    def test_repository_rejects_unsafe_storage_path_segments(self):
        with TemporaryDirectory() as temp_dir:
            repository = LocalWorkspaceRepository(Path(temp_dir))

            with self.assertRaises(ValueError):
                repository.workspace_path("demo-owner", "../bad-workspace")


if __name__ == "__main__":
    unittest.main()
