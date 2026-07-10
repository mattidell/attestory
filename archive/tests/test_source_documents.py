from pathlib import Path
import unittest

from packages.tax_engine.source_documents import load_source_document, load_source_document_payload


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "packages" / "sample_data" / "source_documents"


class SourceDocumentTests(unittest.TestCase):
    def test_w2_fixture_loads_with_required_metadata(self):
        document = load_source_document(FIXTURE_DIR / "w2_basic.2025.json")

        self.assertEqual(document.source_document_id, "demo-w2-acme-2025")
        self.assertEqual(document.source_revision_id, "demo-w2-acme-2025-rev-001")
        self.assertEqual(document.document_type, "w2")
        self.assertEqual(document.tax_year, 2025)
        self.assertEqual(document.field("w2.box1.wages").field_number, "1")
        self.assertEqual(document.field("w2.box1.wages").value["amount"], 8250000)

    def test_1099_int_fixture_loads_with_optional_absent_value(self):
        document = load_source_document(FIXTURE_DIR / "1099_int_basic.2025.json")
        withholding = document.field("1099_int.box4.federal_income_tax_withheld")

        self.assertFalse(withholding.required)
        self.assertFalse(withholding.has_value)

    def test_all_source_document_fixtures_validate_against_schema(self):
        for fixture_path in FIXTURE_DIR.glob("*.json"):
            with self.subTest(fixture=fixture_path.name):
                payload = load_source_document_payload(fixture_path)
                self.assertEqual(payload["schema_version"], "1.0.0")


if __name__ == "__main__":
    unittest.main()
