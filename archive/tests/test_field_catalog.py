import unittest

from packages.tax_engine.field_catalog import load_field_catalog, load_field_catalog_payload


class FieldCatalogTests(unittest.TestCase):
    def test_federal_field_catalog_validates_against_schema(self):
        payload = load_field_catalog_payload()

        self.assertEqual(payload["schema_version"], "1.0.0")
        self.assertEqual(payload["jurisdiction"], "federal")

    def test_federal_field_catalog_has_unique_field_ids(self):
        fields = load_field_catalog()
        field_ids = [field.field_id for field in fields]

        self.assertEqual(len(field_ids), len(set(field_ids)))

    def test_catalog_marks_schedule_b_total_and_1040_interest_as_computed(self):
        fields = {field.field_id: field for field in load_field_catalog()}

        self.assertEqual(fields["irs.2025.f1040sb.line4"].population_mode, "computed")
        self.assertEqual(fields["irs.2025.f1040.line2b"].population_mode, "computed")


if __name__ == "__main__":
    unittest.main()
