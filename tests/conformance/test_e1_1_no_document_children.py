"""E1.1 (Peerage) — No document-child schemas.

Detection per the Engineering Constraints: no fact-type identity key
references a source-flavor citizen, and removing evidence from a test
workspace must alter no finding's content or identity — only its
evidentiary standing.

Part one (this milestone, Track 3): the wall is structural. The
fact-type schema's identity-key kinds are ``entity`` and ``literal``
only; every spelling of a source-flavor key is schema-invalid, and the
strict registry rejects rather than repairs. Part two (Track 4) extends
this file with the evidence-removal drill.
"""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import SchemaValidationError
from tests.support import demo_fact_type_payment, registry_with_demo_kinds


class TestE11NoSourceFlavorIdentityKeys(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def _assert_rejected(self, key: dict[str, Any]) -> None:
        fact_type = demo_fact_type_payment()
        fact_type["identity_keys"] = [key]
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("fact-type.v1", fact_type)

    def test_source_key_kind_is_schema_invalid(self) -> None:
        self._assert_rejected({"name": "w2", "kind": "source", "source_kind": "demo.w2"})

    def test_evidence_key_kind_is_schema_invalid(self) -> None:
        self._assert_rejected({"name": "doc", "kind": "evidence", "evidence_kind": "demo.receipt"})

    def test_document_reference_key_is_schema_invalid(self) -> None:
        self._assert_rejected({"name": "file", "kind": "document", "document_id": "demo-doc-1"})

    def test_entity_key_smuggling_a_source_field_is_schema_invalid(self) -> None:
        # additionalProperties: false on the key forms — an entity key
        # cannot carry a source reference alongside its declared fields.
        self._assert_rejected(
            {
                "name": "counterparty",
                "kind": "entity",
                "entity_kind": "demo.counterparty",
                "source_document": "demo-doc-1",
            }
        )

    def test_declared_key_kinds_still_pass(self) -> None:
        fact_type = demo_fact_type_payment()
        self.registry.validate("fact-type.v1", fact_type)


if __name__ == "__main__":
    unittest.main()
