import json
from pathlib import Path
import unittest

from packages.tax_engine.coverage_summary import build_coverage_summary


ROOT = Path(__file__).resolve().parents[1]
COVERAGE_PATH = ROOT / "packages" / "sample_data" / "field_coverage" / "basic_coverage.2025.json"


class CoverageSummaryTests(unittest.TestCase):
    def test_summary_counts_statuses(self):
        coverage = json.loads(COVERAGE_PATH.read_text())
        summary = build_coverage_summary(coverage)

        self.assertEqual(summary["field_count"], 7)
        self.assertEqual(summary["status_counts"]["directly_populated"], 4)
        self.assertEqual(summary["status_counts"]["requires_computation"], 2)
        self.assertEqual(summary["status_counts"]["optional_not_populated"], 1)
        self.assertEqual(summary["status_counts"].get("missing_required_source_data", 0), 0)

    def test_summary_lists_computed_fields(self):
        coverage = json.loads(COVERAGE_PATH.read_text())
        summary = build_coverage_summary(coverage)
        computed_field_ids = [field["field_id"] for field in summary["computed_fields"]]

        self.assertEqual(
            computed_field_ids,
            ["irs.2025.f1040sb.line4", "irs.2025.f1040.line2b"],
        )


if __name__ == "__main__":
    unittest.main()
