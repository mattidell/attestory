"""Track 1 production contracts: published schemas and isolated payloads only."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from packages.derivation.loader import DERIVATION_SCHEMA_DIR
from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR, SchemaRegistry, SchemaRegistryError, SchemaValidationError
from packages.tax.loader import TAX_SCHEMA_DIR


ROOT = Path("packages/sample_data/core_tax_conditions")
EXAMPLES = ROOT / "examples"
NEGATIVES = ROOT / "negatives"
ACT_SCHEMA = {"act-bundle-adoption.v2.json": "act-bundle-adoption.v2"}
NEW_SCHEMAS = {
    "quantity-vocabulary.v1", "role-canon.v1", "fact-type.v2", "bundle.v2",
    "act-bundle-adoption.v2", "derived-finding.v2", "operation-semantics.v2",
    "rule-artifact.v2", "source-closure-mapping.v2", "derivation-record.v2",
    "npe-walk.v1", "artifact-package.v2", "form-field.v2",
    "taxable-interest-composition.v1", "citation.v1",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


class TrackOneSchemaContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR])

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

    def test_registry_immutability_catches_each_new_family(self) -> None:
        cases = (
            (KERNEL_SCHEMA_DIR, "fact-type.v2.schema.json"),
            (DERIVATION_SCHEMA_DIR, "rule-artifact.v2.schema.json"),
            (TAX_SCHEMA_DIR, "form-field.v2.schema.json"),
        )
        for source, filename in cases:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmp:
                copied = Path(tmp) / source.name
                shutil.copytree(source, copied)
                path = copied / filename
                document = load(path)
                document["title"] = "mutated published bytes"
                path.write_text(json.dumps(document), "utf-8")
                with self.assertRaises(SchemaRegistryError):
                    SchemaRegistry(copied)

    def test_npe_fixture_repair_has_one_disposition_per_artifact(self) -> None:
        record = load(Path("packages/sample_data/derivation/examples/derivation-record.completed.json"))
        by_artifact = {row["artifact_id"]: row["disposition"] for row in record["dispositions"]}
        self.assertEqual(by_artifact["demo.rule.tax-table-line16"], "inapplicable")
        self.assertEqual(record["blocked"], [])


if __name__ == "__main__":
    unittest.main()
