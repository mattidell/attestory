from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from packages.tax_engine.product_boundary import load_product_workspace
from packages.tax_engine.source_document_drafts import load_source_document_draft_payload
from packages.tax_engine.workspace_workflow_service import (
    RESULT_CONFLICT,
    RESULT_EXECUTION_FAILED,
    RESULT_NOT_FOUND,
    RESULT_SUCCESS,
    RESULT_VALIDATION_ERROR,
    WorkspaceWorkflowService,
)


ROOT = Path(__file__).resolve().parents[1]
PRODUCT_FIXTURE_DIR = ROOT / "packages" / "sample_data" / "product_boundary"
SOURCE_DRAFT_FIXTURE_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"

WORKSPACE_FIXTURE = PRODUCT_FIXTURE_DIR / "product-workspace.basic_2025.json"
W2_DRAFT_FIXTURE = SOURCE_DRAFT_FIXTURE_DIR / "w2_basic_draft.2025.json"
W2_UPDATED_DRAFT_FIXTURE = SOURCE_DRAFT_FIXTURE_DIR / "w2_updated_wages_draft.2025.json"
INT_DRAFT_FIXTURE = SOURCE_DRAFT_FIXTURE_DIR / "1099_int_basic_draft.2025.json"


def empty_workspace_fixture() -> dict:
    workspace = load_product_workspace(WORKSPACE_FIXTURE)
    workspace["source_drafts"] = []
    return workspace


class WorkspaceWorkflowServiceTests(unittest.TestCase):
    def test_service_manages_source_draft_lifecycle_with_operation_results(self):
        with TemporaryDirectory() as temp_dir:
            service = WorkspaceWorkflowService(storage_root=Path(temp_dir))
            workspace_result = service.create_workspace(empty_workspace_fixture())
            first_draft = load_source_document_draft_payload(W2_DRAFT_FIXTURE)
            second_draft = load_source_document_draft_payload(W2_UPDATED_DRAFT_FIXTURE)

            create_result = service.create_source_draft(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=first_draft,
            )
            duplicate_result = service.create_source_draft(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=first_draft,
            )
            revision_result = service.create_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=second_draft,
            )
            latest_result = service.get_latest_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_id="demo-w2-acme-2025",
            )
            exact_result = service.get_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_id="demo-w2-acme-2025",
                revision_id="demo-w2-acme-2025-rev-001",
            )
            history_result = service.list_source_draft_revisions(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_id="demo-w2-acme-2025",
            )
            archive_result = service.archive_source_draft(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_id="demo-w2-acme-2025",
            )

            self.assertEqual(workspace_result.status, RESULT_SUCCESS)
            self.assertTrue(create_result.ok)
            self.assertEqual(create_result.value["latest_pointer"]["revision_id"], "demo-w2-acme-2025-rev-001")
            self.assertEqual(duplicate_result.status, RESULT_CONFLICT)
            self.assertEqual(revision_result.value["latest_pointer"]["revision_id"], "demo-w2-acme-2025-rev-002")
            self.assertEqual(latest_result.value["source_revision_id"], "demo-w2-acme-2025-rev-002")
            self.assertEqual(exact_result.value["source_revision_id"], "demo-w2-acme-2025-rev-001")
            self.assertEqual(
                [draft["source_revision_id"] for draft in history_result.value],
                ["demo-w2-acme-2025-rev-001", "demo-w2-acme-2025-rev-002"],
            )
            self.assertEqual(archive_result.value["status"], "archived")

    def test_service_executes_exact_revision_runs_and_latest_revision_convenience_runs(self):
        with TemporaryDirectory() as temp_dir:
            service = WorkspaceWorkflowService(storage_root=Path(temp_dir))
            service.create_workspace(empty_workspace_fixture())
            service.create_source_draft(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(W2_DRAFT_FIXTURE),
            )
            service.create_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(W2_UPDATED_DRAFT_FIXTURE),
            )
            service.create_source_draft(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload=load_source_document_draft_payload(INT_DRAFT_FIXTURE),
            )

            exact_run = service.execute_run(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                run_id="demo-run-exact",
                created_at="2026-01-01T00:00:00Z",
                completed_at="2026-01-01T00:00:02Z",
                source_revision_refs=[
                    {
                        "draft_id": "demo-w2-acme-2025",
                        "revision_id": "demo-w2-acme-2025-rev-001",
                    },
                    {
                        "draft_id": "demo-1099-int-example-bank-2025",
                        "revision_id": "demo-1099-int-example-bank-2025-rev-001",
                    },
                ],
            )
            latest_run = service.execute_run_from_latest_revisions(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                run_id="demo-run-latest",
                created_at="2026-01-02T00:00:00Z",
                completed_at="2026-01-02T00:00:02Z",
            )
            summaries_result = service.list_run_summaries("demo-owner", "demo-basic-w2-1099-int-2025")
            latest_detail_result = service.get_latest_run_detail("demo-owner", "demo-basic-w2-1099-int-2025")
            artifact_result = service.resolve_artifact_ref(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                artifact_ref=exact_run.value["run_detail"]["artifact_refs"][0],
            )

            exact_refs = {
                ref["draft_id"]: ref["revision_id"]
                for ref in exact_run.value["run_summary"]["input_revision_refs"]
            }
            latest_refs = {
                ref["draft_id"]: ref["revision_id"]
                for ref in latest_run.value["run_summary"]["input_revision_refs"]
            }

            self.assertTrue(exact_run.ok)
            self.assertEqual(exact_refs["demo-w2-acme-2025"], "demo-w2-acme-2025-rev-001")
            self.assertEqual(latest_refs["demo-w2-acme-2025"], "demo-w2-acme-2025-rev-002")
            self.assertEqual(
                [summary["run_id"] for summary in summaries_result.value],
                ["demo-run-exact", "demo-run-latest"],
            )
            self.assertEqual(latest_detail_result.value["run_summary"]["run_id"], "demo-run-latest")
            self.assertTrue(artifact_result.value.exists)
            self.assertFalse(artifact_result.value.artifact_ref["uri"].startswith("/"))

    def test_service_returns_not_found_and_validation_results(self):
        with TemporaryDirectory() as temp_dir:
            service = WorkspaceWorkflowService(storage_root=Path(temp_dir))
            missing_workspace = service.get_workspace("demo-owner", "missing-workspace")
            service.create_workspace(empty_workspace_fixture())
            missing_revision = service.get_source_draft_revision(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_id="missing-draft",
                revision_id="missing-revision",
            )
            invalid_draft = service.create_source_draft(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                draft_payload={"source_document_id": "bad-draft"},
            )
            empty_exact_run = service.execute_run(
                owner_id="demo-owner",
                workspace_id="demo-basic-w2-1099-int-2025",
                run_id="demo-empty-exact-run",
                created_at="2026-01-01T00:00:00Z",
                completed_at="2026-01-01T00:00:02Z",
                source_revision_refs=[],
            )

            self.assertEqual(missing_workspace.status, RESULT_NOT_FOUND)
            self.assertEqual(missing_revision.status, RESULT_NOT_FOUND)
            self.assertEqual(invalid_draft.status, RESULT_VALIDATION_ERROR)
            self.assertEqual(empty_exact_run.status, RESULT_EXECUTION_FAILED)
            self.assertFalse(invalid_draft.ok)
            self.assertTrue(invalid_draft.errors)


if __name__ == "__main__":
    unittest.main()
