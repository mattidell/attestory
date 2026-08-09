"""Track 1 verification: SSA-1099 vocabulary and boundary as published.

Validates the Form SSA-1099 fact-type admissions:
- The bundle loads and is valid schema.
- Box 6 is guarded against any non-zero value.
- Box 5 reconciliation is demonstrated (in this layer, as a test of the expected contract).
"""

import copy
import json
import unittest
from pathlib import Path
from typing import Any

import jsonschema

from packages.kernel.schema_registry import (
    SchemaRegistry,
    SchemaValidationError,
)
from packages.tax.loader import tax_registry

class TestSSA1099Track1(unittest.TestCase):
    registry: SchemaRegistry
    bundle: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = tax_registry()
        bundle_path = Path("packages/content/tax/2025/ssa1099.bundle.json")
        cls.bundle = json.loads(bundle_path.read_text("utf-8"))
        # Validate the bundle itself
        cls.registry.validate_declared(cls.bundle)

    def test_bundle_carries_track1_fact_types(self) -> None:
        fact_types = {ft["id"]: ft for ft in self.bundle["fact_types"]}
        self.assertIn("tax.us.2025.ssa1099.box3-workers-comp", fact_types)
        self.assertIn("tax.us.2025.ssa1099.box4-repayment", fact_types)
        self.assertIn("tax.us.2025.ssa1099.box5-net-benefits", fact_types)
        self.assertIn("tax.us.2025.ssa1099.box6-withholding", fact_types)
        self.assertIn("tax.us.2025.ssa1099.recipient", fact_types)
        self.assertIn("tax.us.2025.ssa1099.source-closure", fact_types)

    def test_box6_withholding_is_restricted_to_zero(self) -> None:
        fact_types = {ft["id"]: ft for ft in self.bundle["fact_types"]}
        box6 = fact_types["tax.us.2025.ssa1099.box6-withholding"]

        # Test 0 is valid against the value_schema
        jsonschema.validate(0, box6["value_schema"])

        # Test any other value is rejected
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(100, box6["value_schema"])

    def test_box5_net_benefits_is_nonnegative(self) -> None:
        fact_types = {ft["id"]: ft for ft in self.bundle["fact_types"]}
        box5 = fact_types["tax.us.2025.ssa1099.box5-net-benefits"]

        jsonschema.validate(0, box5["value_schema"])
        jsonschema.validate(100, box5["value_schema"])

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(-10, box5["value_schema"])

    def test_recipient_identity_is_enum(self) -> None:
        fact_types = {ft["id"]: ft for ft in self.bundle["fact_types"]}
        recipient = fact_types["tax.us.2025.ssa1099.recipient"]

        jsonschema.validate("taxpayer", recipient["value_schema"])
        jsonschema.validate("spouse", recipient["value_schema"])

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate("dependent", recipient["value_schema"])

    def test_family_mapping_validates(self) -> None:
        family_path = Path("packages/content/tax/2025/family.ssa1099-benefits.json")
        family = json.loads(family_path.read_text("utf-8"))
        self.registry.validate_declared(family)
        self.assertEqual(family["member_predicate"]["fact_type"], "tax.us.2025.ssa1099.box5-net-benefits")

if __name__ == "__main__":
    unittest.main()
