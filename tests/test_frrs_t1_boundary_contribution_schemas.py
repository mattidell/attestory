"""Track 1 First Real Return Slice contracts: boundary and contribution."""

import json
import hashlib
import unittest
from pathlib import Path
from typing import Any, ClassVar, cast

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR, SchemaRegistry, SchemaValidationError
from packages.tax.loader import TAX_SCHEMA_DIR
from tools.generate_frrs_t1_fixtures import render_fixture_files

# Also need boundary schemas
BOUNDARY_SCHEMA_DIR = Path("packages/schemas/boundary")

ROOT = Path("packages/sample_data/frrs_t1")
EXAMPLES = ROOT / "examples"
NEGATIVES = ROOT / "negatives"

ACT_SCHEMA = {
    "act-contribution.v1.json": "act-contribution.v1",
    "act-member-transition.v2.json": "act-member-transition.v2",
    "act-assertion.v2.json": "act-assertion.v2",
    "act-package-adoption.v1.json": "act-package-adoption.v1",
    "act-package-adoption.v1.missing-release.json": "act-package-adoption.v1"
}

NEW_SCHEMAS = {
    "classification.v1", "reserved-illustration-domain.v1", "fixture-provenance-manifest.v1",
    "contribution.v1", "act-contribution.v1", "contribution-record.v1",
    "finding.v2", "act-member-transition.v2", "act-assertion.v2",
    "run-request.v1",
    "release-registry.v1", "act-package-adoption.v1"
}

def load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))

class TrackOneFrrsSchemaContracts(unittest.TestCase):
    registry: ClassVar[SchemaRegistry]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry([
            KERNEL_SCHEMA_DIR,
            DERIVATION_SCHEMA_DIR,
            TAX_SCHEMA_DIR,
            BOUNDARY_SCHEMA_DIR
        ])

    def validate_path(self, path: Path) -> None:
        instance = load(path)
        schema = ACT_SCHEMA.get(path.name)
        if schema is not None:
            self.registry.validate(schema, instance)
        else:
            self.registry.validate_declared(instance)

    def test_every_track_one_schema_is_published(self) -> None:
        self.assertTrue(NEW_SCHEMAS <= set(self.registry.schema_ids()))

    def test_positive_instances_validate(self) -> None:
        paths = sorted(EXAMPLES.glob("*.json"))
        self.assertEqual(len(paths), len(NEW_SCHEMAS))
        for path in paths:
            with self.subTest(path=path.name):
                self.validate_path(path)

    def test_isolated_negative_instances_reject(self) -> None:
        paths = sorted(NEGATIVES.glob("*.json"))
        self.assertGreaterEqual(len(paths), len(NEW_SCHEMAS))
        for path in paths:
            with self.subTest(path=path.name):
                with self.assertRaises(SchemaValidationError):
                    self.validate_path(path)

    def test_never_crosses_requires_a_reason_and_forbids_a_crossing_kind(self) -> None:
        self.registry.validate_declared({
            "schema": "classification.v1",
            "decision": "NEVER_CROSSES",
            "reason": "No public-origin proof is available.",
        })

    def test_fixture_corpus_is_regenerated_from_its_public_pins(self) -> None:
        rendered = render_fixture_files()
        committed = {
            path.relative_to(ROOT).as_posix(): path.read_bytes()
            for path in ROOT.rglob("*.json")
        }
        self.assertEqual(committed, rendered)

        manifest = load(EXAMPLES / "fixture-provenance-manifest.v1.json")
        tracked = {
            item["path"]: item["sha256"]
            for item in manifest["artifacts"]
        }
        self.assertEqual(len(tracked), len(manifest["artifacts"]))
        expected_paths = set(committed) - {"examples/fixture-provenance-manifest.v1.json"}
        self.assertEqual(set(tracked), expected_paths)
        for path, contents in committed.items():
            if path in tracked:
                self.assertEqual(tracked[path], hashlib.sha256(contents).hexdigest())

    def test_track_one_fixtures_are_free_of_private_markers(self) -> None:
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        for path in ROOT.rglob("*.json"):
            with self.subTest(path=path):
                self.assertFalse(any(marker in path.read_text("utf-8") for marker in forbidden))

if __name__ == "__main__":
    unittest.main()
