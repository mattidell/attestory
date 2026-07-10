import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "packages" / "sample_data" / "source_documents"
EXPECTED_PATH = ROOT / "packages" / "sample_data" / "field_coverage" / "basic_coverage.2025.json"


class FieldCoverageRunnerTests(unittest.TestCase):
    def test_runner_writes_expected_basic_coverage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "coverage.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "packages.tax_engine.runners.build_field_coverage",
                    "--source-document",
                    str(SOURCE_DIR / "w2_basic.2025.json"),
                    "--source-document",
                    str(SOURCE_DIR / "1099_int_basic.2025.json"),
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output_path.read_text()), json.loads(EXPECTED_PATH.read_text()))


if __name__ == "__main__":
    unittest.main()
