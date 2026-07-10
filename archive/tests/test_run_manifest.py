import json
from pathlib import Path
import unittest

from packages.tax_engine.tax_workspace_runs import build_run_manifest, execute_tax_workspace


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = ROOT / "packages" / "sample_data" / "workspaces" / "basic_w2_1099_int_2025"
WORKSPACE_PATH = WORKSPACE_DIR / "workspace.json"
WORKSPACE_RELATIVE_PATH = Path("packages/sample_data/workspaces/basic_w2_1099_int_2025/workspace.json")
EXPECTED_RELATIVE_DIR = Path("packages/sample_data/workspaces/basic_w2_1099_int_2025/expected")
EXPECTED_DIR = WORKSPACE_DIR / "expected"


class RunManifestTests(unittest.TestCase):
    def test_run_manifest_records_inputs_and_outputs(self):
        result = execute_tax_workspace(WORKSPACE_PATH)
        manifest = build_run_manifest(
            workspace_path=WORKSPACE_RELATIVE_PATH,
            run_result=result,
            output_paths={
                "normalized_source_documents": EXPECTED_RELATIVE_DIR / "normalized-source-documents.json",
                "source_validation": EXPECTED_RELATIVE_DIR / "source-validation.json",
                "field_coverage": EXPECTED_RELATIVE_DIR / "field-coverage.json",
                "field_resolution": EXPECTED_RELATIVE_DIR / "field-resolution.json",
                "return_artifact": EXPECTED_RELATIVE_DIR / "return-artifact.json",
                "return_review_markdown": EXPECTED_RELATIVE_DIR / "return-artifact.md",
                "field_coverage_markdown": EXPECTED_RELATIVE_DIR / "field-coverage.md",
                "run_manifest": EXPECTED_RELATIVE_DIR / "run-manifest.json",
            },
            run_id="demo-basic-w2-1099-int-2025-run-001",
            created_at="2026-01-01T00:00:00Z",
        )

        self.assertEqual(
            manifest,
            json.loads((EXPECTED_DIR / "run-manifest.json").read_text()),
        )
        self.assertEqual(manifest["workspace_id"], "demo-basic-w2-1099-int-2025")
        self.assertEqual(manifest["engine_version"], "prototype")
        self.assertEqual(
            [item["artifact_type"] for item in manifest["inputs"]],
            ["tax_workspace", "source_document_draft", "source_document_draft"],
        )
        self.assertEqual(
            [item["artifact_type"] for item in manifest["outputs"]],
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


if __name__ == "__main__":
    unittest.main()
