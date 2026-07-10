from pathlib import Path
import unittest

from packages.tax_engine.direct_mapping import (
    STATUS_DIRECTLY_POPULATED,
    STATUS_MISSING_REQUIRED_SOURCE_DATA,
    STATUS_OPTIONAL_NOT_POPULATED,
    run_direct_source_mapping,
)
from packages.tax_engine.source_documents import load_source_document


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "packages" / "sample_data" / "source_documents"


def result_by_mapping_id(result: dict) -> dict:
    return {item["mapping_id"]: item for item in result["direct_mappings"]}


class DirectMappingTests(unittest.TestCase):
    def test_w2_box1_maps_to_form_1040_line1a_with_attribution(self):
        document = load_source_document(FIXTURE_DIR / "w2_basic.2025.json")
        result = run_direct_source_mapping([document])
        mappings = result_by_mapping_id(result)

        line1a = mappings["direct.w2.box1.to.f1040.line1a"]
        self.assertEqual(line1a["status"], STATUS_DIRECTLY_POPULATED)
        self.assertEqual(line1a["destination_field_id"], "irs.2025.f1040.line1a")
        self.assertEqual(line1a["value"]["amount"], 8250000)
        self.assertEqual(line1a["source_attribution"]["source_document_id"], "demo-w2-acme-2025")
        self.assertEqual(line1a["source_attribution"]["source_revision_id"], "demo-w2-acme-2025-rev-001")
        self.assertEqual(line1a["source_attribution"]["source_document_label"], "Demo W-2: Acme Robotics")
        self.assertEqual(line1a["source_attribution"]["source_field_id"], "w2.box1.wages")
        self.assertEqual(line1a["source_attribution"]["source_field_label"], "Wages, tips, other compensation")

    def test_1099_int_box1_maps_to_schedule_b_interest_row(self):
        document = load_source_document(FIXTURE_DIR / "1099_int_basic.2025.json")
        result = run_direct_source_mapping([document])
        mappings = result_by_mapping_id(result)

        interest = mappings["direct.1099_int.box1.to.schedule_b.interest_amount"]
        self.assertEqual(interest["status"], STATUS_DIRECTLY_POPULATED)
        self.assertEqual(interest["destination_field_id"], "irs.2025.f1040sb.part_i.interest_payers.interest_amount")
        self.assertEqual(interest["value"]["amount"], 43210)

    def test_required_null_source_field_is_marked_missing(self):
        document = load_source_document(FIXTURE_DIR / "w2_missing_required_box1.2025.json")
        result = run_direct_source_mapping([document])
        mappings = result_by_mapping_id(result)

        line1a = mappings["direct.w2.box1.to.f1040.line1a"]
        self.assertEqual(line1a["status"], STATUS_MISSING_REQUIRED_SOURCE_DATA)
        self.assertIsNone(line1a["value"])
        self.assertIsNone(line1a["source_attribution"])

    def test_optional_null_source_field_is_marked_optional_not_populated(self):
        document = load_source_document(FIXTURE_DIR / "1099_int_optional_withholding_absent.2025.json")
        result = run_direct_source_mapping([document])
        mappings = result_by_mapping_id(result)

        withholding = mappings["direct.1099_int.box4.to.f1040.line25b"]
        self.assertEqual(withholding["status"], STATUS_OPTIONAL_NOT_POPULATED)
        self.assertIsNone(withholding["value"])


if __name__ == "__main__":
    unittest.main()
