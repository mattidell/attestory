import json
from pathlib import Path
import unittest

from packages.tax_engine.tax_workspace_runs import execute_tax_workspace


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = ROOT / "packages" / "sample_data" / "workspaces" / "basic_w2_1099_int_2025"
WORKSPACE_PATH = WORKSPACE_DIR / "workspace.json"
EXPECTED_DIR = WORKSPACE_DIR / "expected"


class TaxWorkspaceGoldenArtifactTests(unittest.TestCase):
    def test_basic_workspace_matches_expected_run_artifacts(self):
        result = execute_tax_workspace(WORKSPACE_PATH)

        self.assertEqual(
            result["normalized_source_documents"],
            json.loads((EXPECTED_DIR / "normalized-source-documents.json").read_text()),
        )
        self.assertEqual(
            result["source_validation"],
            json.loads((EXPECTED_DIR / "source-validation.json").read_text()),
        )
        self.assertEqual(
            result["field_coverage"],
            json.loads((EXPECTED_DIR / "field-coverage.json").read_text()),
        )
        self.assertEqual(
            result["field_resolution"],
            json.loads((EXPECTED_DIR / "field-resolution.json").read_text()),
        )
        self.assertEqual(
            result["return_artifact"],
            json.loads((EXPECTED_DIR / "return-artifact.json").read_text()),
        )
        self.assertEqual(
            result["return_review_markdown"],
            (EXPECTED_DIR / "return-artifact.md").read_text(),
        )
        self.assertEqual(
            result["field_coverage_markdown"],
            (EXPECTED_DIR / "field-coverage.md").read_text(),
        )


if __name__ == "__main__":
    unittest.main()
