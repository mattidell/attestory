"""E7.2 (Supersession) - No third edge.

Detection per the Engineering Constraints: every cascade path maps to a
declared derivation or individuation edge. Undeclared dependencies do
not affect standing.
"""

import tempfile
import unittest
from pathlib import Path

from packages.kernel.currency import compute_currency, displacement_closure
from packages.kernel.findings import project
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    registry_with_demo_kinds,
)


class TestE72NoThirdEdge(unittest.TestCase):
    def test_cascade_closure_is_exactly_declared_edges(self) -> None:
        edges = {
            "derivation": {
                "input-finding": {"derived-a"},
                "derived-a": {"derived-b"},
            },
            "individuation": {
                "demo-corp-a": {"keyed-finding"},
            },
            "evidence": {
                "demo-evidence-001": {"document-child-shaped-dependent"},
            },
        }
        displaced, _ = displacement_closure(
            {"input-finding", "demo-corp-a", "demo-evidence-001"},
            edges,
        )
        self.assertEqual(
            displaced,
            {
                "input-finding",
                "derived-a",
                "derived-b",
                "demo-corp-a",
                "keyed-finding",
                "demo-evidence-001",
            },
        )
        self.assertNotIn("document-child-shaped-dependent", displaced)

    def test_evidence_dependency_does_not_displace_a_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            registry = registry_with_demo_kinds(Path(tmp))
            state = project(
                (
                    act(0, "bundle-adoption", {"bundle": demo_bundle()}),
                    act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
                    act(2, "evidence-submitted", {"evidence": demo_evidence()}),
                    act(3, "assertion", {"finding": demo_finding("finding-from-evidence")}),
                    act(4, "evidence-replaced", {"evidence_id": "demo-evidence-001"}),
                ),
                registry,
            )

        view = compute_currency(
            state,
            root_displacements={"demo-evidence-001"},
            extra_edges={
                "evidence": {
                    "demo-evidence-001": {"finding-from-evidence"},
                }
            },
        )
        self.assertEqual(view.current_finding_ids, frozenset({"finding-from-evidence"}))
        self.assertEqual(view.displaced_finding_ids, frozenset())


if __name__ == "__main__":
    unittest.main()
