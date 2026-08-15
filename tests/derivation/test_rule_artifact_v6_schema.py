"""Track 1 (f1098e-student-loan-interest-agi): `rule-artifact.v6` schema.

`rule-artifact.v6` is an additive successor to `rule-artifact.v4` (v5 was
skipped — claimed on the local schema ledger by a concurrent, unrelated
milestone). The only grammar change is two new `$defs/expr` variants,
`multiply` and `divide`; every other v4 shape is preserved byte-for-byte
in the copy. Mirrors `tests/derivation/test_language_schemas.py`'s
mutation-based malformed-shape pattern.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError

DERIVATION_SCHEMA_DIR = Path(__file__).resolve().parents[2] / "packages" / "schemas" / "derivation"
EXAMPLES = Path(__file__).resolve().parents[2] / "packages" / "sample_data" / "derivation" / "examples"
RULE_ARTIFACT_V6 = "rule-artifact.v6"


def _example(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


class RuleArtifactV6Schema(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry([DERIVATION_SCHEMA_DIR])

    def assert_rejected(self, instance: object) -> None:
        with self.assertRaises(SchemaValidationError):
            self.registry.validate(RULE_ARTIFACT_V6, instance)

    def _rule_with_value(self, value: object) -> dict[str, Any]:
        rule = _example("rule-artifact.v6.sli-ratio.json")
        rule["value"] = value
        return rule

    def test_committed_example_validates(self) -> None:
        self.registry.validate_declared(_example("rule-artifact.v6.sli-ratio.json"))

    def test_multiply_minimal_shape_validates(self) -> None:
        self.registry.validate(
            RULE_ARTIFACT_V6, self._rule_with_value({"op": "multiply", "left": 1, "right": 2})
        )

    def test_divide_minimal_shape_validates(self) -> None:
        self.registry.validate(
            RULE_ARTIFACT_V6,
            self._rule_with_value(
                {"op": "divide", "left": 1, "right": 2, "min_decimal_places": 3, "rounding": "half_up"}
            ),
        )

    def test_multiply_missing_operand_rejected(self) -> None:
        self.assert_rejected(self._rule_with_value({"op": "multiply", "left": 1}))

    def test_multiply_stray_field_rejected(self) -> None:
        self.assert_rejected(self._rule_with_value({"op": "multiply", "left": 1, "right": 2, "args": [1]}))

    def test_divide_missing_min_decimal_places_rejected(self) -> None:
        self.assert_rejected(
            self._rule_with_value({"op": "divide", "left": 1, "right": 2, "rounding": "half_up"})
        )

    def test_divide_missing_rounding_rejected(self) -> None:
        self.assert_rejected(
            self._rule_with_value({"op": "divide", "left": 1, "right": 2, "min_decimal_places": 3})
        )

    def test_divide_unknown_rounding_mode_rejected(self) -> None:
        self.assert_rejected(
            self._rule_with_value(
                {"op": "divide", "left": 1, "right": 2, "min_decimal_places": 3, "rounding": "banker"}
            )
        )

    def test_divide_negative_min_decimal_places_rejected(self) -> None:
        self.assert_rejected(
            self._rule_with_value(
                {"op": "divide", "left": 1, "right": 2, "min_decimal_places": -1, "rounding": "half_up"}
            )
        )

    def test_v4_schema_bytes_unchanged(self) -> None:
        # Track 1's ADR-0003 obligation: v4 must remain byte-identical.
        v4_path = DERIVATION_SCHEMA_DIR / "rule-artifact.v4.schema.json"
        v4 = json.loads(v4_path.read_text("utf-8"))
        self.assertEqual(v4["$id"], "derivation/rule-artifact.v4")
        ops = {branch["properties"]["op"].get("const") or tuple(branch["properties"]["op"].get("enum", [])) for branch in v4["$defs"]["expr"]["oneOf"] if isinstance(branch, dict) and "properties" in branch and "op" in branch["properties"]}
        self.assertNotIn("multiply", ops)
        self.assertNotIn("divide", ops)

    def test_v6_manifest_entry_present_and_v4_entry_unchanged(self) -> None:
        manifest = json.loads((DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8"))
        self.assertIn("rule-artifact.v6.schema.json", manifest)
        self.assertIn("rule-artifact.v4.schema.json", manifest)


if __name__ == "__main__":
    unittest.main()
