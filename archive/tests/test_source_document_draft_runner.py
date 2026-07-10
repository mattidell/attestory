import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


class SourceDocumentDraftRunnerTests(unittest.TestCase):
    def test_runner_normalizes_draft_to_source_document_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "source-document.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "packages.tax_engine.runners.normalize_source_document_draft",
                    "--draft",
                    str(DRAFT_DIR / "w2_basic_draft.2025.json"),
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
            self.assertEqual(payload["source_document_id"], "demo-w2-acme-2025")
            self.assertEqual(payload["fields"][0]["source_field_id"], "w2.box1.wages")


if __name__ == "__main__":
    unittest.main()
