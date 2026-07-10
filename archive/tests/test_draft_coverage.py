from pathlib import Path
import unittest

from packages.tax_engine.draft_coverage import build_field_coverage_from_drafts, build_markdown_coverage_from_drafts


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


def coverage_by_field_id(coverage: dict) -> dict:
    return {field["field_id"]: field for field in coverage["fields"]}


class DraftCoverageTests(unittest.TestCase):
    def test_drafts_build_expected_field_coverage(self):
        coverage = build_field_coverage_from_drafts(
            [
                DRAFT_DIR / "w2_basic_draft.2025.json",
                DRAFT_DIR / "1099_int_basic_draft.2025.json",
            ]
        )
        fields = coverage_by_field_id(coverage)

        self.assertEqual(fields["irs.2025.f1040.line1a"]["values"][0]["amount"], 8250000)
        self.assertEqual(fields["irs.2025.f1040.line25b"]["status"], "optional_not_populated")
        self.assertEqual(fields["irs.2025.f1040.line2b"]["status"], "requires_computation")

    def test_drafts_build_markdown_coverage(self):
        markdown = build_markdown_coverage_from_drafts(
            [
                DRAFT_DIR / "w2_basic_draft.2025.json",
                DRAFT_DIR / "1099_int_basic_draft.2025.json",
            ]
        )

        self.assertIn("# Federal Field Coverage (2025)", markdown)
        self.assertIn("Form 1040 line 1a wages", markdown)


if __name__ == "__main__":
    unittest.main()
