from pathlib import Path
import unittest

from packages.tax_engine.source_document_drafts import load_source_document_draft_payload, normalize_source_document_draft
from packages.tax_engine.source_documents import source_document_from_payload
from packages.tax_engine.source_validation import build_source_validation_report, render_source_validation_report_markdown


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


class SourceValidationTests(unittest.TestCase):
    def test_report_identifies_missing_required_source_fields(self):
        draft = load_source_document_draft_payload(DRAFT_DIR / "w2_missing_required_box1_draft.2025.json")
        document = source_document_from_payload(normalize_source_document_draft(draft))
        report = build_source_validation_report([document])

        self.assertFalse(report["valid"])
        self.assertEqual(report["documents"][0]["missing_required_fields"][0]["source_field_id"], "w2.box1.wages")

    def test_report_markdown_lists_missing_required_source_fields(self):
        draft = load_source_document_draft_payload(DRAFT_DIR / "w2_missing_required_box1_draft.2025.json")
        document = source_document_from_payload(normalize_source_document_draft(draft))
        markdown = render_source_validation_report_markdown(build_source_validation_report([document]))

        self.assertIn("# Source Document Validation", markdown)
        self.assertIn("w2.box1.wages", markdown)
        self.assertIn("Valid: no", markdown)


if __name__ == "__main__":
    unittest.main()
