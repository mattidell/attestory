import json
from pathlib import Path
import unittest

from packages.tax_engine.coverage_read_model import (
    build_field_detail_read_model,
    build_grouped_coverage_read_model,
)


ROOT = Path(__file__).resolve().parents[1]
COVERAGE_PATH = ROOT / "packages" / "sample_data" / "field_coverage" / "basic_coverage.2025.json"


class CoverageReadModelTests(unittest.TestCase):
    def setUp(self):
        self.coverage = json.loads(COVERAGE_PATH.read_text())

    def test_grouped_coverage_groups_fields_by_form(self):
        read_model = build_grouped_coverage_read_model(self.coverage)
        forms = {form["form_id"]: form for form in read_model["forms"]}

        self.assertIn("irs.2025.f1040", forms)
        self.assertIn("irs.2025.f1040sb", forms)
        self.assertEqual(forms["irs.2025.f1040"]["status_counts"]["directly_populated"], 2)

    def test_direct_field_detail_includes_source_attribution(self):
        detail = build_field_detail_read_model(self.coverage, "irs.2025.f1040.line1a")

        self.assertEqual(detail["status"], "directly_populated")
        self.assertEqual(detail["source_attributions"][0]["source_field_id"], "w2.box1.wages")
        self.assertEqual(detail["source_attributions"][0]["source_field_label"], "Wages, tips, other compensation")

    def test_computed_field_detail_hides_computation_trace(self):
        detail = build_field_detail_read_model(self.coverage, "irs.2025.f1040.line2b")

        self.assertEqual(detail["status"], "requires_computation")
        self.assertEqual(detail["source_attributions"], [])
        self.assertEqual(detail["values"], [])

    def test_unknown_field_detail_raises_key_error(self):
        with self.assertRaises(KeyError):
            build_field_detail_read_model(self.coverage, "irs.2025.f1040.unknown")


if __name__ == "__main__":
    unittest.main()
