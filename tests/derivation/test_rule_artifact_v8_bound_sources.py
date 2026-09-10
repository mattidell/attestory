"""ADR-0074: rule-artifact.v8 bound_sources operator.

v8 is v7 plus one expr branch (`op`, `name`; no `source_set`;
`additionalProperties: false`). Predecessor bytes stay untouched.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError

EXAMPLES = (
    Path(__file__).resolve().parents[2]
    / "packages"
    / "sample_data"
    / "derivation"
    / "examples"
)

V7_CHECKSUM = "c1596110d0ce378746329f8332ab1010c49e36d42fd4144ada70eafd957c7697"


def _example(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


class RuleArtifactV8Schema(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry([DERIVATION_SCHEMA_DIR])

    def test_committed_example_validates(self) -> None:
        self.registry.validate_declared(_example("rule-artifact.v8.bound-sources.json"))

    def test_bound_sources_minimal_shape_validates(self) -> None:
        rule = _example("rule-artifact.v8.bound-sources.json")
        rule["value"] = {"op": "bound_sources", "name": "demo.allocation.amount"}
        self.registry.validate("rule-artifact.v8", rule)

    def test_bound_sources_with_source_set_is_rejected(self) -> None:
        rule = _example("rule-artifact.v8.bound-sources.json")
        rule["value"] = {
            "op": "bound_sources",
            "name": "demo.allocation.amount",
            "source_set": "demo.family",
        }
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("rule-artifact.v8", rule)

    def test_bound_sources_missing_name_is_rejected(self) -> None:
        rule = _example("rule-artifact.v8.bound-sources.json")
        rule["value"] = {"op": "bound_sources"}
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("rule-artifact.v8", rule)

    def test_v7_still_rejects_bound_sources(self) -> None:
        rule = _example("rule-artifact.v8.bound-sources.json")
        rule["schema"] = "rule-artifact.v7"
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("rule-artifact.v7", rule)

    def test_v7_manifest_entry_unchanged_and_v8_published(self) -> None:
        manifest = json.loads((DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8"))
        self.assertIn("rule-artifact.v8.schema.json", manifest)
        self.assertEqual(manifest["rule-artifact.v7.schema.json"], V7_CHECKSUM)


if __name__ == "__main__":
    unittest.main()
