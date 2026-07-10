import unittest

from packages.tax_engine.computed_fields import computed_fields_by_destination, load_computed_field_definitions


class ComputedFieldDefinitionTests(unittest.TestCase):
    def test_computed_field_definitions_load_from_contract(self):
        computations = load_computed_field_definitions()

        self.assertEqual(len(computations), 2)
        self.assertEqual(computations[0].destination_field_id, "irs.2025.f1040sb.line4")
        self.assertEqual(computations[0].operation, "sum")

    def test_computed_field_definitions_are_addressable_by_destination(self):
        computations = computed_fields_by_destination(load_computed_field_definitions())

        self.assertEqual(
            computations["irs.2025.f1040.line2b"].input_field_ids,
            ("irs.2025.f1040sb.line4",),
        )


if __name__ == "__main__":
    unittest.main()
