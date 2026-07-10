from pathlib import Path
import unittest

import jsonschema

from packages.tax_engine.product_boundary import (
    artifact_refs_for_run,
    execute_product_run_payload,
    load_product_run_detail,
    load_product_run_payload,
    load_product_run_summary,
    load_product_workspace,
    validate_product_run_payload,
    validate_product_workspace,
)


ROOT = Path(__file__).resolve().parents[1]
PRODUCT_FIXTURE_DIR = ROOT / "packages" / "sample_data" / "product_boundary"

WORKSPACE_FIXTURE = PRODUCT_FIXTURE_DIR / "product-workspace.basic_2025.json"
RUN_PAYLOAD_FIXTURE = PRODUCT_FIXTURE_DIR / "product-run-payload.basic_2025.json"
RUN_SUMMARY_FIXTURE = PRODUCT_FIXTURE_DIR / "product-run-summary.basic_2025.json"
RUN_DETAIL_FIXTURE = PRODUCT_FIXTURE_DIR / "product-run-detail.basic_2025.json"


class ProductBoundaryContractTests(unittest.TestCase):
    def test_product_boundary_fixtures_validate(self):
        workspace = load_product_workspace(WORKSPACE_FIXTURE)
        run_payload = load_product_run_payload(RUN_PAYLOAD_FIXTURE)
        run_summary = load_product_run_summary(RUN_SUMMARY_FIXTURE)
        run_detail = load_product_run_detail(RUN_DETAIL_FIXTURE)

        self.assertEqual(workspace["owner_id"], "demo-owner")
        self.assertEqual(workspace["jurisdictions"], ["federal"])
        self.assertEqual(workspace["data_classification"], "synthetic_demo")
        self.assertEqual(run_payload["source_draft_snapshots"][0]["draft_id"], "demo-w2-acme-2025")
        self.assertEqual(run_summary["result_summary"]["generated_artifact_count"], 8)
        self.assertEqual(run_detail["artifact_refs"][0]["artifact_type"], "normalized_source_documents")

    def test_product_workspace_rejects_absolute_source_draft_uri(self):
        workspace = load_product_workspace(WORKSPACE_FIXTURE)
        workspace["source_drafts"][0]["uri"] = "/Users/demo/private/w2.json"

        with self.assertRaises(jsonschema.ValidationError):
            validate_product_workspace(workspace)

    def test_product_run_payload_rejects_snapshot_revision_mismatch(self):
        run_payload = load_product_run_payload(RUN_PAYLOAD_FIXTURE)
        run_payload["source_draft_snapshots"][0]["revision_id"] = "unexpected-revision"

        with self.assertRaises(ValueError):
            validate_product_run_payload(run_payload)

    def test_artifact_refs_use_relative_uris(self):
        refs = artifact_refs_for_run("demo-run")

        self.assertEqual(len(refs), 8)
        self.assertEqual(refs[0]["uri"], "runs/demo-run/normalized-source-documents.json")
        self.assertTrue(all(not ref["uri"].startswith("/") for ref in refs))

    def test_product_run_payload_executes_engine_workflow_and_returns_product_run_detail(self):
        run_payload = load_product_run_payload(RUN_PAYLOAD_FIXTURE)
        result = execute_product_run_payload(
            run_payload,
            created_at="2026-01-01T00:00:00Z",
            completed_at="2026-01-01T00:00:02Z",
        )

        summary = result["run_summary"]
        detail = result["run_detail"]
        engine_result = result["engine_result"]

        self.assertEqual(summary["status"], "succeeded")
        self.assertEqual(summary["result_summary"]["validation_error_count"], 0)
        self.assertEqual(summary["result_summary"]["blocked_field_count"], 0)
        self.assertEqual(summary["result_summary"]["generated_artifact_count"], 8)
        self.assertEqual(detail["run_payload"], run_payload)
        self.assertEqual(
            [ref["artifact_type"] for ref in detail["artifact_refs"]],
            [
                "normalized_source_documents",
                "source_validation",
                "field_coverage",
                "field_resolution",
                "return_artifact",
                "return_review_markdown",
                "field_coverage_markdown",
                "run_manifest",
            ],
        )
        self.assertEqual(engine_result["return_artifact"]["tax_year"], 2025)
        self.assertIn("# Federal Return Review (2025)", engine_result["return_review_markdown"])


if __name__ == "__main__":
    unittest.main()
