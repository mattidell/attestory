"""Currency tests: supersession is derived from the record projection."""

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any

from packages.kernel.currency import (
    CurrencyMaterializationError,
    assert_materialization_matches,
    compute_currency,
    displacement_closure,
)
from packages.kernel.findings import project
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    registry_with_demo_kinds,
)


class CurrencyFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def base_acts(self) -> tuple[dict[str, Any], ...]:
        return (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
        )


class TestFindingCurrency(CurrencyFixture):
    def test_later_finding_for_same_fact_displaces_earlier_finding(self) -> None:
        state = project(
            self.base_acts()
            + (
                act(3, "assertion", {"finding": demo_finding("finding-old", value=1200)}),
                act(4, "assertion", {"finding": demo_finding("finding-new", value=1300)}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertEqual(view.current_finding_ids, frozenset({"finding-new"}))
        self.assertEqual(view.displaced_finding_ids, frozenset({"finding-old"}))
        self.assertEqual(view.reasons["finding-old"][0].kind, "correction")

    def test_derivation_edge_cascades_from_displaced_input(self) -> None:
        state = project(
            self.base_acts()
            + (
                act(3, "assertion", {"finding": demo_finding("finding-old", value=1200)}),
                act(4, "assertion", {"finding": demo_finding("finding-new", value=1300)}),
            ),
            self.registry,
        )
        derived = demo_finding(
            finding_id="derived-stand-in",
            fact_id="demo.synthetic-derived|period=2025",
            value=2400,
            evidence_ids=[],
            basis="attested",
        )
        derived["pins"] = {"finding_ids": ["finding-old"], "artifact_ids": ["demo-rule.v1"]}
        state = replace(state, findings={**state.findings, "derived-stand-in": derived})

        view = compute_currency(state)
        self.assertIn("derived-stand-in", view.displaced_finding_ids)
        self.assertEqual(view.reasons["derived-stand-in"][0].kind, "derivation")

    def test_evidence_replacement_does_not_displace_finding(self) -> None:
        state = project(
            self.base_acts()
            + (
                act(3, "assertion", {"finding": demo_finding("finding-from-evidence")}),
                act(4, "evidence-replaced", {"evidence_id": "demo-evidence-001"}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertEqual(view.current_finding_ids, frozenset({"finding-from-evidence"}))
        self.assertEqual(view.displaced_evidence_ids, frozenset({"demo-evidence-001"}))

    def test_individuation_edge_displaces_finding_when_keyed_citizen_is_superseded(self) -> None:
        state = project(
            self.base_acts()
            + (
                act(3, "assertion", {"finding": demo_finding("finding-keyed")}),
                act(
                    4,
                    "entity-superseded",
                    {
                        "entity_id": "demo-corp-a",
                        "replacement": demo_entity("demo-corp-a2", "Corp A (corrected)"),
                    },
                ),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertIn("finding-keyed", view.displaced_finding_ids)
        self.assertEqual(view.reasons["finding-keyed"][0].kind, "individuation")
        self.assertEqual(view.reasons["finding-keyed"][0].by, "demo-corp-a")

    def test_succession_leaves_successor_facts_open_not_answered(self) -> None:
        state = project(
            self.base_acts()
            + (
                act(3, "assertion", {"finding": demo_finding("finding-keyed")}),
                act(
                    4,
                    "entity-superseded",
                    {
                        "entity_id": "demo-corp-a",
                        "replacement": demo_entity("demo-corp-a2", "Corp A (corrected)"),
                    },
                ),
            ),
            self.registry,
        )
        view = compute_currency(state)
        # The old answer does not migrate to the successor's fact; the
        # successor's question is open, which is the truth about where
        # things stand.
        self.assertEqual(view.current_finding_ids, frozenset())


class TestDisplacementEdges(unittest.TestCase):
    def test_closure_walks_only_declared_edges(self) -> None:
        edges = {
            "derivation": {"root": {"derived"}},
            "individuation": {"root": {"keyed"}},
            "evidence": {"root": {"document-child"}},
        }
        displaced, reasons = displacement_closure({"root"}, edges)
        self.assertEqual(displaced, {"root", "derived", "keyed"})
        self.assertNotIn("document-child", displaced)
        self.assertEqual({r.kind for r in reasons["derived"]}, {"derivation"})
        self.assertEqual({r.kind for r in reasons["keyed"]}, {"individuation"})


class TestMaterializationDiff(CurrencyFixture):
    def test_stale_materialized_current_flag_is_caught(self) -> None:
        state = project(
            self.base_acts()
            + (
                act(3, "assertion", {"finding": demo_finding("finding-old", value=1200)}),
                act(4, "assertion", {"finding": demo_finding("finding-new", value=1300)}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        good = {
            "findings": {
                "finding-old": {"current": False},
                "finding-new": {"current": True},
            }
        }
        assert_materialization_matches(view, good)

        stale = {
            "findings": {
                "finding-old": {"current": True},
                "finding-new": {"current": True},
            }
        }
        with self.assertRaises(CurrencyMaterializationError):
            assert_materialization_matches(view, stale)


if __name__ == "__main__":
    unittest.main()
