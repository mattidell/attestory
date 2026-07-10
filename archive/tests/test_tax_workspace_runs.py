from pathlib import Path
import unittest

from packages.tax_engine.tax_workspace_runs import execute_tax_workspace


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_PATH = ROOT / "packages" / "sample_data" / "workspaces" / "basic_w2_1099_int_2025" / "workspace.json"


class TaxWorkspaceRunTests(unittest.TestCase):
    def test_workspace_run_produces_current_workflow_artifacts(self):
        result = execute_tax_workspace(WORKSPACE_PATH)

        self.assertEqual(result["workspace_id"], "demo-basic-w2-1099-int-2025")
        self.assertEqual(len(result["normalized_source_documents"]), 2)
        self.assertTrue(result["source_validation"]["valid"])
        self.assertEqual(result["field_coverage"]["tax_year"], 2025)
        self.assertEqual(result["field_resolution"]["tax_year"], 2025)
        self.assertEqual(result["return_artifact"]["tax_year"], 2025)
        self.assertEqual(result["return_artifact"]["resolution_summary"]["field_count"], 7)
        self.assertIn("# Federal Field Coverage (2025)", result["field_coverage_markdown"])
        self.assertIn("# Federal Return Review (2025)", result["return_review_markdown"])


if __name__ == "__main__":
    unittest.main()
