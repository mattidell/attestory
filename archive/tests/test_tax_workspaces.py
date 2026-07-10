from pathlib import Path
import unittest

from packages.tax_engine.source_document_drafts import load_source_document_draft_payload
from packages.tax_engine.tax_workspaces import load_tax_workspace, load_tax_workspace_payload


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_PATH = ROOT / "packages" / "sample_data" / "workspaces" / "basic_w2_1099_int_2025" / "workspace.json"


class TaxWorkspaceTests(unittest.TestCase):
    def test_basic_workspace_fixture_validates_against_schema(self):
        payload = load_tax_workspace_payload(WORKSPACE_PATH)

        self.assertEqual(payload["workspace_id"], "demo-basic-w2-1099-int-2025")
        self.assertEqual(payload["jurisdiction"], "federal")

    def test_basic_workspace_resolves_source_document_draft_paths(self):
        workspace = load_tax_workspace(WORKSPACE_PATH)

        self.assertEqual(workspace.tax_year, 2025)
        self.assertEqual(len(workspace.source_document_draft_paths), 2)
        self.assertTrue(workspace.source_document_draft_paths[0].is_file())
        self.assertTrue(workspace.source_document_draft_paths[1].is_file())

    def test_basic_workspace_references_valid_draft_payloads(self):
        workspace = load_tax_workspace(WORKSPACE_PATH)
        drafts = [
            load_source_document_draft_payload(path)
            for path in workspace.source_document_draft_paths
        ]

        self.assertEqual(
            [draft["document_type"] for draft in drafts],
            ["w2", "1099-int"],
        )


if __name__ == "__main__":
    unittest.main()
