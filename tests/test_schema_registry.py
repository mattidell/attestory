"""Schema registry tests: strict validation and published-version immutability.

Mutation cases prove the checks are live: a mutated published schema,
an unlisted schema file, and a repair-shaped acceptance are all caught.
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

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


class TestContentAddressedMemos(unittest.TestCase):
    """The load and validation memos must be indistinguishable from no memo.

    Both are keyed on content digests rather than on paths or schema ids, so
    these tests pin the property that makes that safe: the same schema id
    carrying different published bytes is a different key, never a shared
    verdict.
    """

    def _dir_with(self, schema: dict[str, Any]) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        directory = Path(tmp.name)
        (directory / "demo-citizen.v1.schema.json").write_text(
            json.dumps(schema, indent=2), "utf-8"
        )
        write_manifest(directory)
        return directory

    def test_same_schema_id_different_bytes_do_not_share_a_verdict(self) -> None:
        # The defect this guards: keying the memo on (schema_id, instance)
        # alone would let the permissive registry's PASS stand in for the
        # strict one, silently disabling validation.
        strict = SchemaRegistry(self._dir_with(DEMO_SCHEMA))
        relaxed_schema = json.loads(json.dumps(DEMO_SCHEMA))
        relaxed_schema["required"] = ["schema", "id"]
        relaxed = SchemaRegistry(self._dir_with(relaxed_schema))

        no_label = {"schema": "demo-citizen.v1", "id": "demo-1"}

        # Permissive first, then strict: a shared verdict would wrongly pass.
        self.assertEqual(relaxed.validate_declared(no_label), "demo-citizen.v1")
        with self.assertRaises(SchemaValidationError):
            strict.validate_declared(no_label)

        # And the reverse order: a shared verdict would wrongly fail.
        self.assertEqual(relaxed.validate_declared(no_label), "demo-citizen.v1")

    def test_repeated_validation_is_identical_pass_and_fail(self) -> None:
        registry = SchemaRegistry(self._dir_with(DEMO_SCHEMA))
        good = {"schema": "demo-citizen.v1", "id": "demo-1", "label": "Demo"}
        bad = {"schema": "demo-citizen.v1", "id": "demo-1"}

        for _ in range(3):
            self.assertEqual(registry.validate_declared(good), "demo-citizen.v1")

        first: list[str] | None = None
        for _ in range(3):
            with self.assertRaises(SchemaValidationError) as ctx:
                registry.validate_declared(bad)
            if first is None:
                first = ctx.exception.errors
            # A memoized failure must reproduce the whole error list, not a
            # truncated or reordered one.
            self.assertEqual(ctx.exception.errors, first)

    def test_a_mutated_published_schema_is_still_caught_after_a_clean_load(self) -> None:
        # The load memo must never let a mutation reuse the pre-mutation
        # compile: every file is re-hashed on every construction.
        directory = self._dir_with(DEMO_SCHEMA)
        SchemaRegistry(directory)

        mutated = json.loads(json.dumps(DEMO_SCHEMA))
        mutated["required"] = ["schema"]
        (directory / "demo-citizen.v1.schema.json").write_text(
            json.dumps(mutated, indent=2), "utf-8"
        )
        with self.assertRaises(SchemaRegistryError) as ctx:
            SchemaRegistry(directory)
        self.assertIn("mutated", str(ctx.exception))

    def test_unkeyable_instance_still_validates(self) -> None:
        # Not every instance can be canonically serialized; those must take
        # the uncached path rather than be keyed on a lossy stand-in.
        registry = SchemaRegistry(self._dir_with(DEMO_SCHEMA))
        with self.assertRaises(SchemaValidationError):
            registry.validate_declared(
                {"schema": "demo-citizen.v1", "id": "demo-1", "label": {1, 2}}
            )


if __name__ == "__main__":
    unittest.main()
