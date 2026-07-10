import json
import subprocess
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


class SourceValidationRunnerTests(unittest.TestCase):
    def test_runner_outputs_json_validation_report(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.tax_engine.runners.validate_source_documents",
                "--draft",
                str(DRAFT_DIR / "w2_missing_required_box1_draft.2025.json"),
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["valid"])

    def test_runner_outputs_markdown_validation_report(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.tax_engine.runners.validate_source_documents",
                "--draft",
                str(DRAFT_DIR / "w2_missing_required_box1_draft.2025.json"),
                "--format",
                "markdown",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Source Document Validation", result.stdout)
        self.assertIn("w2.box1.wages", result.stdout)


if __name__ == "__main__":
    unittest.main()
