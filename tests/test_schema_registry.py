"""Schema registry tests: strict validation and published-version immutability.

Mutation cases prove the checks are live: a mutated published schema,
an unlisted schema file, and a repair-shaped acceptance are all caught.
"""

import json
import tempfile
import unittest
from pathlib import Path

from packages.kernel.schema_registry import (
    SchemaRegistry,
    SchemaRegistryError,
    SchemaValidationError,
    write_manifest,
)

DEMO_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "schema": {"const": "demo-citizen.v1"},
        "id": {"type": "string", "minLength": 1},
        "label": {"type": "string"},
    },
    "required": ["schema", "id", "label"],
    "additionalProperties": False,
}


class RegistryFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.schema_dir = Path(self._tmp.name)
        (self.schema_dir / "demo-citizen.v1.schema.json").write_text(
            json.dumps(DEMO_SCHEMA, indent=2), "utf-8"
        )
        write_manifest(self.schema_dir)


class TestStrictValidation(RegistryFixture):
    def test_conformant_instance_passes(self) -> None:
        registry = SchemaRegistry(self.schema_dir)
        instance = {"schema": "demo-citizen.v1", "id": "demo-1", "label": "Demo"}
        self.assertEqual(registry.validate_declared(instance), "demo-citizen.v1")

    def test_undeclared_shape_is_rejected_not_repaired(self) -> None:
        registry = SchemaRegistry(self.schema_dir)
        # Missing required field and an undeclared extra: a tolerant
        # reader would accept or repair; the registry must reject.
        instance = {"schema": "demo-citizen.v1", "id": "demo-1", "extra": True}
        with self.assertRaises(SchemaValidationError) as ctx:
            registry.validate_declared(instance)
        self.assertEqual(ctx.exception.schema_id, "demo-citizen.v1")
        self.assertTrue(any("label" in e for e in ctx.exception.errors))
        self.assertTrue(any("extra" in e for e in ctx.exception.errors))

    def test_instance_naming_no_schema_is_rejected(self) -> None:
        registry = SchemaRegistry(self.schema_dir)
        with self.assertRaises(SchemaValidationError):
            registry.validate_declared({"id": "demo-1", "label": "Demo"})

    def test_unknown_schema_version_is_a_registry_error(self) -> None:
        registry = SchemaRegistry(self.schema_dir)
        with self.assertRaises(SchemaRegistryError):
            registry.validate("demo-citizen.v9", {})


class TestImmutability(RegistryFixture):
    def test_mutated_published_schema_is_caught(self) -> None:
        path = self.schema_dir / "demo-citizen.v1.schema.json"
        mutated = json.loads(path.read_text("utf-8"))
        mutated["properties"]["label"] = {"type": "integer"}
        path.write_text(json.dumps(mutated, indent=2), "utf-8")
        with self.assertRaises(SchemaRegistryError) as ctx:
            SchemaRegistry(self.schema_dir)
        self.assertIn("mutated", str(ctx.exception))

    def test_unpublished_schema_file_is_caught(self) -> None:
        (self.schema_dir / "shadow.v1.schema.json").write_text(
            json.dumps(DEMO_SCHEMA), "utf-8"
        )
        with self.assertRaises(SchemaRegistryError) as ctx:
            SchemaRegistry(self.schema_dir)
        self.assertIn("not published", str(ctx.exception))

    def test_missing_published_file_is_caught(self) -> None:
        (self.schema_dir / "demo-citizen.v1.schema.json").unlink()
        with self.assertRaises(SchemaRegistryError) as ctx:
            SchemaRegistry(self.schema_dir)
        self.assertIn("missing", str(ctx.exception))

    def test_manifest_tool_refuses_republication_of_mutated_schema(self) -> None:
        path = self.schema_dir / "demo-citizen.v1.schema.json"
        mutated = json.loads(path.read_text("utf-8"))
        mutated["title"] = "drifted"
        path.write_text(json.dumps(mutated, indent=2), "utf-8")
        with self.assertRaises(SchemaRegistryError) as ctx:
            write_manifest(self.schema_dir)
        self.assertIn("refusing to republish", str(ctx.exception))

    def test_manifest_tool_allows_adding_new_version(self) -> None:
        v2 = json.loads(json.dumps(DEMO_SCHEMA))
        v2["properties"]["schema"] = {"const": "demo-citizen.v2"}
        (self.schema_dir / "demo-citizen.v2.schema.json").write_text(
            json.dumps(v2, indent=2), "utf-8"
        )
        manifest = write_manifest(self.schema_dir)
        self.assertIn("demo-citizen.v2.schema.json", manifest)
        registry = SchemaRegistry(self.schema_dir)
        self.assertEqual(
            registry.schema_ids(), ["demo-citizen.v1", "demo-citizen.v2"]
        )


class TestKernelSchemaDirectory(unittest.TestCase):
    def test_default_registry_loads_kernel_schemas(self) -> None:
        registry = SchemaRegistry()
        # Contents grow by track; loading must always verify cleanly.
        self.assertIsInstance(registry.schema_ids(), list)


if __name__ == "__main__":
    unittest.main()
