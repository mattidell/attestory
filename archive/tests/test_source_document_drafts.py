from pathlib import Path
import unittest

from packages.tax_engine.source_document_drafts import (
    load_source_document_draft_payload,
    normalize_source_document_draft,
)
from packages.tax_engine.source_documents import source_document_from_payload


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


class SourceDocumentDraftTests(unittest.TestCase):
    def test_w2_draft_normalizes_to_canonical_source_document(self):
        draft = load_source_document_draft_payload(DRAFT_DIR / "w2_basic_draft.2025.json")
        normalized = normalize_source_document_draft(draft)
        document = source_document_from_payload(normalized)

        self.assertEqual(document.source_document_id, "demo-w2-acme-2025")
        self.assertEqual(document.source_revision_id, "demo-w2-acme-2025-rev-001")
        self.assertEqual(document.field("w2.box1.wages").field_number, "1")
        self.assertEqual(document.field("w2.box1.wages").value["amount"], 8250000)

    def test_missing_required_draft_value_normalizes_to_null_source_field(self):
        draft = load_source_document_draft_payload(DRAFT_DIR / "w2_missing_required_box1_draft.2025.json")
        normalized = normalize_source_document_draft(draft)
        document = source_document_from_payload(normalized)

        wages = document.field("w2.box1.wages")
        self.assertTrue(wages.required)
        self.assertIsNone(wages.value)

    def test_1099_int_draft_adds_absent_optional_withholding_field(self):
        draft = load_source_document_draft_payload(DRAFT_DIR / "1099_int_basic_draft.2025.json")
        normalized = normalize_source_document_draft(draft)
        document = source_document_from_payload(normalized)

        withholding = document.field("1099_int.box4.federal_income_tax_withheld")
        self.assertFalse(withholding.required)
        self.assertIsNone(withholding.value)


if __name__ == "__main__":
    unittest.main()
