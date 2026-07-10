import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


class DraftCoverageRunnerTests(unittest.TestCase):
    def test_runner_writes_json_coverage_from_drafts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "coverage.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "packages.tax_engine.runners.build_coverage_from_drafts",
                    "--draft",
                    str(DRAFT_DIR / "w2_basic_draft.2025.json"),
                    "--draft",
                    str(DRAFT_DIR / "1099_int_basic_draft.2025.json"),
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output_path.read_text())
            self.assertEqual(payload["tax_year"], 2025)

    def test_runner_writes_markdown_coverage_from_drafts(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.tax_engine.runners.build_coverage_from_drafts",
                "--draft",
                str(DRAFT_DIR / "w2_basic_draft.2025.json"),
                "--format",
                "markdown",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Federal Field Coverage (2025)", result.stdout)


if __name__ == "__main__":
    unittest.main()
