from pathlib import Path
import unittest

from packages.tax_engine.draft_coverage import build_field_coverage_from_drafts
from packages.tax_engine.field_resolution import build_field_resolution


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


class FieldResolutionTests(unittest.TestCase):
    def test_resolution_computes_declared_field_dependencies(self):
        coverage = build_field_coverage_from_drafts([
            DRAFT_DIR / "w2_basic_draft.2025.json",
            DRAFT_DIR / "1099_int_basic_draft.2025.json",
        ])
        resolution = build_field_resolution(coverage)
        fields = {
            field["field_id"]: field
            for field in resolution["fields"]
        }

        self.assertEqual(fields["irs.2025.f1040.line1a"]["status"], "resolved_direct")
        self.assertEqual(fields["irs.2025.f1040sb.line4"]["status"], "resolved_computed")
        self.assertEqual(fields["irs.2025.f1040sb.line4"]["value"]["amount"], 43210)
        self.assertEqual(fields["irs.2025.f1040.line2b"]["status"], "resolved_computed")
        self.assertEqual(fields["irs.2025.f1040.line2b"]["dependency_field_ids"], ["irs.2025.f1040sb.line4"])

    def test_resolution_blocks_computed_fields_when_required_source_data_is_missing(self):
        coverage = build_field_coverage_from_drafts([
            DRAFT_DIR / "w2_basic_draft.2025.json",
            DRAFT_DIR / "w2_missing_required_box1_draft.2025.json",
        ])
        resolution = build_field_resolution(coverage)
        fields = {
            field["field_id"]: field
            for field in resolution["fields"]
        }

        self.assertEqual(fields["irs.2025.f1040sb.line4"]["status"], "blocked_missing_source")
        self.assertEqual(
            fields["irs.2025.f1040sb.line4"]["blocking_field_ids"],
            ["1099_int.box1.interest_income"],
        )
        self.assertEqual(fields["irs.2025.f1040.line2b"]["status"], "blocked_missing_source")


if __name__ == "__main__":
    unittest.main()
