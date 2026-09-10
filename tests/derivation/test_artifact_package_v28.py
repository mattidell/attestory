"""ADR-0074: artifact-package.v28 admits rule-artifact.v8.

v26 bytes stay untouched. v27 is reserved by another milestone.
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

V26_CHECKSUM = "4d0bbf0b253d579a39a68330de9996a953915c9f5606902b9d8887840959af72"


def _example(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


class ArtifactPackageV28Schema(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry([DERIVATION_SCHEMA_DIR])

    def test_committed_example_validates(self) -> None:
        self.registry.validate_declared(_example("artifact-package.v28.json"))

    def test_v26_still_rejects_a_v8_member(self) -> None:
        package = _example("artifact-package.v28.json")
        package["schema"] = "artifact-package.v26"
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("artifact-package.v26", package)

    def test_v8_member_requires_admitted_schemas_entry(self) -> None:
        package = _example("artifact-package.v28.json")
        package["admitted_schemas"] = ["rule-artifact.v7"]
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("artifact-package.v28", package)

    def test_v26_manifest_entry_unchanged_and_v28_published(self) -> None:
        manifest = json.loads((DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8"))
        self.assertIn("artifact-package.v28.schema.json", manifest)
        self.assertNotIn("artifact-package.v27.schema.json", manifest)
        self.assertEqual(manifest["artifact-package.v26.schema.json"], V26_CHECKSUM)


if __name__ == "__main__":
    unittest.main()
