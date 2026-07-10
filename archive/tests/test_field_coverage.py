from pathlib import Path
import unittest

from packages.tax_engine.direct_mapping import load_direct_mapping_payload, run_direct_source_mapping
from packages.tax_engine.field_coverage import (
    STATUS_REQUIRES_COMPUTATION,
    build_field_coverage,
    validate_field_coverage,
)
from packages.tax_engine.source_documents import load_source_document


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "packages" / "sample_data" / "source_documents"


def coverage_by_field_id(coverage: dict) -> dict:
    return {field["field_id"]: field for field in coverage["fields"]}


class FieldCoverageTests(unittest.TestCase):
    def test_field_coverage_validates_against_schema(self):
        documents = [
            load_source_document(FIXTURE_DIR / "w2_basic.2025.json"),
            load_source_document(FIXTURE_DIR / "1099_int_basic.2025.json"),
        ]
        mapping_payload = load_direct_mapping_payload()
        direct_result = run_direct_source_mapping(documents, mapping_payload)
        coverage = build_field_coverage(direct_mapping_result=direct_result, mapping_payload=mapping_payload)

        validate_field_coverage(coverage)

    def test_populated_direct_field_includes_source_attribution(self):
        document = load_source_document(FIXTURE_DIR / "w2_basic.2025.json")
        mapping_payload = load_direct_mapping_payload()
        direct_result = run_direct_source_mapping([document], mapping_payload)
        coverage = coverage_by_field_id(build_field_coverage(direct_mapping_result=direct_result, mapping_payload=mapping_payload))

        line1a = coverage["irs.2025.f1040.line1a"]
        self.assertEqual(line1a["status"], "directly_populated")
        self.assertEqual(line1a["values"][0]["amount"], 8250000)
        self.assertEqual(line1a["source_attributions"][0]["source_document_id"], "demo-w2-acme-2025")
        self.assertEqual(line1a["source_attributions"][0]["source_revision_id"], "demo-w2-acme-2025-rev-001")
        self.assertEqual(line1a["source_attributions"][0]["source_document_label"], "Demo W-2: Acme Robotics")
        self.assertEqual(line1a["source_attributions"][0]["source_field_label"], "Wages, tips, other compensation")

    def test_source_edit_changes_coverage_value_and_revision(self):
        from packages.tax_engine.source_document_drafts import load_source_document_draft_payload, normalize_source_document_draft
        from packages.tax_engine.source_documents import source_document_from_payload

        draft = load_source_document_draft_payload(ROOT / "packages" / "sample_data" / "source_document_drafts" / "w2_updated_wages_draft.2025.json")
        document = source_document_from_payload(normalize_source_document_draft(draft))
        mapping_payload = load_direct_mapping_payload()
        direct_result = run_direct_source_mapping([document], mapping_payload)
        coverage = coverage_by_field_id(build_field_coverage(direct_mapping_result=direct_result, mapping_payload=mapping_payload))

        line1a = coverage["irs.2025.f1040.line1a"]
        self.assertEqual(line1a["values"][0]["amount"], 9000000)
        self.assertEqual(line1a["source_attributions"][0]["source_revision_id"], "demo-w2-acme-2025-rev-002")

    def test_required_missing_source_data_is_reported(self):
        document = load_source_document(FIXTURE_DIR / "w2_missing_required_box1.2025.json")
        mapping_payload = load_direct_mapping_payload()
        direct_result = run_direct_source_mapping([document], mapping_payload)
        coverage = coverage_by_field_id(build_field_coverage(direct_mapping_result=direct_result, mapping_payload=mapping_payload))

        line1a = coverage["irs.2025.f1040.line1a"]
        self.assertEqual(line1a["status"], "missing_required_source_data")
        self.assertEqual(line1a["needed_source_field_ids"], ["w2.box1.wages"])

    def test_computed_fields_do_not_expose_direct_source_attribution(self):
        document = load_source_document(FIXTURE_DIR / "1099_int_basic.2025.json")
        mapping_payload = load_direct_mapping_payload()
        direct_result = run_direct_source_mapping([document], mapping_payload)
        coverage = coverage_by_field_id(build_field_coverage(direct_mapping_result=direct_result, mapping_payload=mapping_payload))

        line2b = coverage["irs.2025.f1040.line2b"]
        self.assertEqual(line2b["status"], STATUS_REQUIRES_COMPUTATION)
        self.assertEqual(line2b["values"], [])
        self.assertEqual(line2b["source_attributions"], [])

    def test_optional_unpopulated_field_is_reported(self):
        document = load_source_document(FIXTURE_DIR / "1099_int_optional_withholding_absent.2025.json")
        mapping_payload = load_direct_mapping_payload()
        direct_result = run_direct_source_mapping([document], mapping_payload)
        coverage = coverage_by_field_id(build_field_coverage(direct_mapping_result=direct_result, mapping_payload=mapping_payload))

        line25b = coverage["irs.2025.f1040.line25b"]
        self.assertEqual(line25b["status"], "optional_not_populated")
        self.assertEqual(line25b["values"], [])


if __name__ == "__main__":
    unittest.main()
