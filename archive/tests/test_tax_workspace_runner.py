import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_PATH = ROOT / "packages" / "sample_data" / "workspaces" / "basic_w2_1099_int_2025" / "workspace.json"


class TaxWorkspaceRunnerTests(unittest.TestCase):
    def test_runner_writes_workspace_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "run"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "packages.tax_engine.runners.run_tax_workspace",
                    "--workspace",
                    str(WORKSPACE_PATH),
                    "--output-dir",
                    str(output_dir),
                    "--run-id",
                    "test-run-001",
                    "--created-at",
                    "2026-01-01T00:00:00Z",
                ],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertEqual(summary["workspace_id"], "demo-basic-w2-1099-int-2025")

            source_documents = json.loads((output_dir / "normalized-source-documents.json").read_text())
            source_validation = json.loads((output_dir / "source-validation.json").read_text())
            field_coverage = json.loads((output_dir / "field-coverage.json").read_text())
            field_resolution = json.loads((output_dir / "field-resolution.json").read_text())
            return_artifact = json.loads((output_dir / "return-artifact.json").read_text())
            return_review_markdown = (output_dir / "return-artifact.md").read_text()
            field_coverage_markdown = (output_dir / "field-coverage.md").read_text()
            run_manifest = json.loads((output_dir / "run-manifest.json").read_text())

            self.assertEqual(len(source_documents), 2)
            self.assertTrue(source_validation["valid"])
            self.assertEqual(field_coverage["tax_year"], 2025)
            self.assertEqual(field_resolution["tax_year"], 2025)
            self.assertEqual(return_artifact["tax_year"], 2025)
            self.assertIn("# Federal Return Review (2025)", return_review_markdown)
            self.assertIn("# Federal Field Coverage (2025)", field_coverage_markdown)
            self.assertEqual(run_manifest["run_id"], "test-run-001")
            self.assertEqual(run_manifest["created_at"], "2026-01-01T00:00:00Z")
            self.assertEqual(run_manifest["outputs"][-1]["artifact_type"], "run_manifest")

    def test_runner_can_write_artifacts_to_timestamped_output_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "runs"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "packages.tax_engine.runners.run_tax_workspace",
                    "--workspace",
                    str(WORKSPACE_PATH),
                    "--output-dir",
                    str(output_root),
                    "--timestamp-run",
                    "--run-id",
                    "test-run-002",
                    "--created-at",
                    "2026-01-01T00:00:00Z",
                ],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            timestamped_output_dir = output_root / "20260101T000000Z"
            self.assertTrue((timestamped_output_dir / "return-artifact.json").exists())
            self.assertTrue((timestamped_output_dir / "return-artifact.md").exists())

            summary = json.loads(result.stdout)
            self.assertEqual(
                summary["artifacts"]["run_manifest"],
                str(timestamped_output_dir / "run-manifest.json"),
            )

            run_manifest = json.loads((timestamped_output_dir / "run-manifest.json").read_text())
            self.assertEqual(run_manifest["created_at"], "2026-01-01T00:00:00Z")
            self.assertTrue(
                all(
                    item["path"].startswith(str(timestamped_output_dir))
                    for item in run_manifest["outputs"]
                )
            )


if __name__ == "__main__":
    unittest.main()
