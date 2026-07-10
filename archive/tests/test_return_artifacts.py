from pathlib import Path
import unittest

from packages.tax_engine.draft_coverage import build_field_coverage_from_drafts
from packages.tax_engine.field_resolution import build_field_resolution
from packages.tax_engine.return_artifacts import build_return_artifact
from packages.tax_engine.return_review import render_return_review_markdown


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "packages" / "sample_data" / "source_document_drafts"


class ReturnArtifactTests(unittest.TestCase):
    def test_return_artifact_groups_resolved_fields_and_summarizes_resolution(self):
        coverage = build_field_coverage_from_drafts([
            DRAFT_DIR / "w2_basic_draft.2025.json",
            DRAFT_DIR / "1099_int_basic_draft.2025.json",
        ])
        artifact = build_return_artifact(build_field_resolution(coverage))

        self.assertEqual(artifact["tax_year"], 2025)
        self.assertEqual(
            [form["form_id"] for form in artifact["forms"]],
            ["irs.2025.f1040", "irs.2025.f1040sb"],
        )
        form_1040_fields = {
            field["field_id"]: field
            for field in artifact["forms"][0]["fields"]
        }
        self.assertEqual(form_1040_fields["irs.2025.f1040.line1a"]["status"], "resolved_direct")
        self.assertEqual(form_1040_fields["irs.2025.f1040.line2b"]["status"], "resolved_computed")

        summary = artifact["resolution_summary"]
        self.assertEqual(summary["field_count"], 7)
        self.assertEqual(summary["status_counts"]["resolved_direct"], 4)
        self.assertEqual(summary["status_counts"]["resolved_computed"], 2)
        self.assertEqual(summary["status_counts"]["optional_not_populated"], 1)
        self.assertEqual(
            summary["optional_unpopulated_fields"][0]["field_id"],
            "irs.2025.f1040.line25b",
        )

    def test_return_artifact_summarizes_blocked_fields_without_returning_them(self):
        coverage = build_field_coverage_from_drafts([
            DRAFT_DIR / "w2_basic_draft.2025.json",
            DRAFT_DIR / "w2_missing_required_box1_draft.2025.json",
        ])
        artifact = build_return_artifact(build_field_resolution(coverage))
        returned_field_ids = {
            field["field_id"]
            for form in artifact["forms"]
            for field in form["fields"]
        }

        self.assertNotIn("irs.2025.f1040sb.line4", returned_field_ids)
        self.assertEqual(
            artifact["resolution_summary"]["status_counts"]["blocked_missing_source"],
            4,
        )
        self.assertEqual(
            artifact["resolution_summary"]["blocked_fields"][0]["status"],
            "blocked_missing_source",
        )


class ReturnReviewTests(unittest.TestCase):
    def test_return_review_renders_summary_and_return_lines(self):
        coverage = build_field_coverage_from_drafts([
            DRAFT_DIR / "w2_basic_draft.2025.json",
            DRAFT_DIR / "1099_int_basic_draft.2025.json",
        ])
        markdown = render_return_review_markdown(build_return_artifact(build_field_resolution(coverage)))

        self.assertIn("# Federal Return Review (2025)", markdown)
        self.assertIn("- Resolved direct: 4", markdown)
        self.assertIn("`irs.2025.f1040.line1a`", markdown)
        self.assertIn("$82,500.00", markdown)
        self.assertIn("## Optional Unpopulated Fields", markdown)


if __name__ == "__main__":
    unittest.main()
