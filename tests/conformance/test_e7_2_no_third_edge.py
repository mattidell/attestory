"""E7.2 (Supersession) - No third edge.

Detection per the Engineering Constraints: every cascade path maps to a
declared derivation or individuation edge. Undeclared dependencies do
not affect standing, and displacement is driven by the record alone —
there is no API for injecting displacement from outside it.
"""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.currency import compute_currency, displacement_closure
from packages.kernel.findings import project
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    demo_payment_fact_id,
    registry_with_demo_kinds,
)


class TestE72NoThirdEdge(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def test_closure_walks_only_declared_edge_kinds(self) -> None:
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

    def test_evidence_supersession_displaces_no_finding(self) -> None:
        # Evidence is provenance, not an edge. Superseding it from the
        # record changes evidentiary standing only (E1.1); a cascade
        # from evidence to findings would be the third edge.
        state = project(
            (
                act(0, "bundle-adoption", {"bundle": demo_bundle()}),
                act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
                act(2, "evidence-submitted", {"evidence": demo_evidence()}),
                act(3, "assertion", {"finding": demo_finding("finding-from-evidence")}),
                act(4, "evidence-replaced", {"evidence_id": "demo-evidence-001"}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertEqual(view.current_finding_ids, frozenset({"finding-from-evidence"}))
        self.assertEqual(view.displaced_finding_ids, frozenset())
        self.assertIn("demo-evidence-001", view.displaced_evidence_ids)

    def test_entity_supersession_displaces_exactly_the_keyed_findings(self) -> None:
        # Closure equality from the record: superseding one entity
        # displaces the findings on its facts and nothing else.
        finding_a: dict[str, Any] = demo_finding(
            "finding-a", fact_id=demo_payment_fact_id("demo-corp-a")
        )
        finding_b: dict[str, Any] = demo_finding(
            "finding-b", fact_id=demo_payment_fact_id("demo-corp-b")
        )
        state = project(
            (
                act(0, "bundle-adoption", {"bundle": demo_bundle()}),
                act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
                act(2, "entity-introduced", {"entity": demo_entity("demo-corp-b", "Corp B")}),
                act(3, "evidence-submitted", {"evidence": demo_evidence()}),
                act(4, "assertion", {"finding": finding_a}),
                act(5, "assertion", {"finding": finding_b}),
                act(6, "entity-superseded", {"entity_id": "demo-corp-a"}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertEqual(view.displaced_finding_ids, frozenset({"finding-a"}))
        self.assertEqual(view.current_finding_ids, frozenset({"finding-b"}))
        self.assertEqual(
            {reason.kind for reason in view.reasons["finding-a"]},
            {"individuation"},
        )

    def test_no_injection_surface_exists(self) -> None:
        # The violation-shaped affordance this suite once relied on is
        # gone: currency accepts the projection and nothing else.
        import inspect

        parameters = inspect.signature(compute_currency).parameters
        self.assertEqual(list(parameters), ["state"])


if __name__ == "__main__":
    unittest.main()
