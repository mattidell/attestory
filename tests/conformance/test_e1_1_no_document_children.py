"""E1.1 (Peerage) — No document-child schemas.

Detection per the Engineering Constraints: no fact-type identity key
references a source-flavor citizen, and removing evidence from a test
workspace must alter no finding's content or identity — only its
evidentiary standing.

The first half is structural: fact-type identity-key kinds are
``entity`` and ``literal`` only, so source-flavor keys are
schema-invalid. The second half is behavioral: evidence lifecycle acts
change only a derived evidentiary-standing view, not finding content or
identity.
"""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.findings import evidentiary_standing, project
from packages.kernel.schema_registry import SchemaValidationError
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_fact_type_payment,
    demo_finding,
    registry_with_demo_kinds,
)


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


class TestE11EvidenceLifecycleDoesNotRewriteFindings(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))
        self.finding = demo_finding()
        self.base_acts = (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
            act(3, "assertion", {"finding": self.finding}),
        )

    def test_replacing_evidence_changes_only_evidentiary_standing(self) -> None:
        before = project(self.base_acts, self.registry)
        after = project(
            self.base_acts
            + (
                act(
                    4,
                    "evidence-replaced",
                    {
                        "evidence_id": "demo-evidence-001",
                        "replacement": demo_evidence(
                            "demo-evidence-002", "Corrected demo statement"
                        ),
                    },
                ),
            ),
            self.registry,
        )

        self.assertEqual(before.findings, after.findings)
        self.assertEqual(after.findings["demo-finding-001"], self.finding)
        before_standing = evidentiary_standing(before)["demo-finding-001"]
        after_standing = evidentiary_standing(after)["demo-finding-001"]
        self.assertEqual(before_standing.finding, after_standing.finding)
        self.assertEqual(before_standing.evidence[0].status, "current")
        self.assertEqual(after_standing.evidence[0].status, "replaced")
        self.assertEqual(after_standing.evidence[0].successor_id, "demo-evidence-002")

    def test_withdrawing_evidence_changes_only_evidentiary_standing(self) -> None:
        before = project(self.base_acts, self.registry)
        after = project(
            self.base_acts
            + (
                act(4, "evidence-replaced", {"evidence_id": "demo-evidence-001"}),
            ),
            self.registry,
        )

        self.assertEqual(before.findings, after.findings)
        before_standing = evidentiary_standing(before)["demo-finding-001"]
        after_standing = evidentiary_standing(after)["demo-finding-001"]
        self.assertEqual(before_standing.finding, after_standing.finding)
        self.assertEqual(before_standing.evidence[0].status, "current")
        self.assertEqual(after_standing.evidence[0].status, "withdrawn")
        self.assertIsNone(after_standing.evidence[0].successor_id)


if __name__ == "__main__":
    unittest.main()
