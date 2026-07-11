"""Patch verification: a registry spanning kernel + derivation families.

ADR-0010 mechanism: the workspace act log stores kernel acts and
derived-publication acts, so one registry must validate both. Schema ids are
unique across the two directories, and both families' schemas resolve.
"""

import json
import unittest
from pathlib import Path

from packages.kernel.schema_registry import SchemaRegistryError
from packages.derivation.loader import workspace_registry

EXAMPLES = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "derivation" / "examples"


class CombinedRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = workspace_registry()

    def test_resolves_both_families(self) -> None:
        ids = self.registry.schema_ids()
        self.assertIn("finding.v1", ids)                    # kernel
        self.assertIn("act.v1", ids)                        # kernel envelope
        self.assertIn("act-derived-publication.v1", ids)    # derivation act payload
        self.assertIn("derived-finding.v1", ids)            # derivation

    def test_validates_a_derived_publication_payload(self) -> None:
        payload = json.loads((EXAMPLES / "act-derived-publication.json").read_text("utf-8"))
        self.registry.validate("act-derived-publication.v1", payload)
        self.registry.validate_declared(payload["finding"])

    def test_validates_a_kernel_finding(self) -> None:
        finding = {
            "schema": "finding.v1", "id": "f1", "fact_id": "demo.fact",
            "value": 1, "basis": "attested", "evidence_ids": [],
        }
        self.registry.validate_declared(finding)

    def test_no_id_collision_across_families(self) -> None:
        # Every id appears once; construction would have raised on a duplicate.
        ids = self.registry.schema_ids()
        self.assertEqual(len(ids), len(set(ids)))

    def test_duplicate_directories_rejected(self) -> None:
        from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR, SchemaRegistry
        with self.assertRaises(SchemaRegistryError):
            SchemaRegistry([KERNEL_SCHEMA_DIR, KERNEL_SCHEMA_DIR])


if __name__ == "__main__":
    unittest.main()
