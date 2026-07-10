import json
import subprocess
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
COVERAGE_PATH = ROOT / "packages" / "sample_data" / "field_coverage" / "basic_coverage.2025.json"


class FieldCoverageInspectionRunnerTests(unittest.TestCase):
    def test_runner_outputs_grouped_coverage_when_field_id_is_omitted(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.tax_engine.runners.inspect_field_coverage",
                "--coverage",
                str(COVERAGE_PATH),
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("forms", payload)

    def test_runner_outputs_field_detail_when_field_id_is_provided(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.tax_engine.runners.inspect_field_coverage",
                "--coverage",
                str(COVERAGE_PATH),
                "--field-id",
                "irs.2025.f1040.line1a",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["field_id"], "irs.2025.f1040.line1a")
        self.assertEqual(payload["source_attributions"][0]["source_field_id"], "w2.box1.wages")

    def test_runner_outputs_grouped_coverage_as_markdown(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.tax_engine.runners.inspect_field_coverage",
                "--coverage",
                str(COVERAGE_PATH),
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
        self.assertIn("## Summary", result.stdout)
        self.assertIn("| Field | Status | Value | Source |", result.stdout)
        self.assertIn("Form 1040 line 1a wages", result.stdout)
        self.assertIn("Demo W-2: Acme Robotics, field 1", result.stdout)

    def test_runner_outputs_field_detail_as_markdown(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "packages.tax_engine.runners.inspect_field_coverage",
                "--coverage",
                str(COVERAGE_PATH),
                "--field-id",
                "irs.2025.f1040.line1a",
                "--format",
                "markdown",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Form 1040 line 1a wages", result.stdout)
        self.assertIn("- Status: Direct", result.stdout)


if __name__ == "__main__":
    unittest.main()
