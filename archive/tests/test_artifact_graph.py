import json
import subprocess
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
GRAPH_DIR = ROOT / "docs" / "product" / "artifact-graph"
RENDERER = ROOT / "tools" / "render_artifact_graph.py"


class ArtifactGraphTests(unittest.TestCase):
    def test_graph_is_valid_and_documents_are_fresh(self) -> None:
        result = subprocess.run(
            [sys.executable, str(RENDERER), "--check"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_graph_schema_is_a_valid_json_schema(self) -> None:
        schema = json.loads((GRAPH_DIR / "artifact-graph.schema.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)


if __name__ == "__main__":
    unittest.main()
