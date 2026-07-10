"""Read model tests: current state, history, and open facts are derived."""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.read_models import (
    build_read_model,
    current_state,
    fact_history,
    open_facts,
)
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    registry_with_demo_kinds,
)


class ReadModelFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def workspace_acts(self) -> tuple[dict[str, Any], ...]:
        return (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
            act(3, "assertion", {"finding": demo_finding("finding-old", value=1200)}),
            act(4, "assertion", {"finding": demo_finding("finding-new", value=1300)}),
        )


class TestReadModels(ReadModelFixture):
    def test_current_state_contains_only_current_findings(self) -> None:
        current = current_state(self.workspace_acts(), self.registry)
        self.assertEqual(current["finding_ids"], ["finding-new"])
        self.assertEqual(current["evidence_ids"], ["demo-evidence-001"])
        self.assertEqual(
            current["findings"]["finding-new"]["finding"]["value"],
            1300,
        )

    def test_fact_history_preserves_superseded_findings(self) -> None:
        history = fact_history(self.workspace_acts(), self.registry)
        entries = history["demo.counterparty-payment|counterparty=demo-corp-a,period=2025"]
        self.assertEqual(
            [(entry["finding_id"], entry["current"]) for entry in entries],
            [("finding-old", False), ("finding-new", True)],
        )

    def test_open_facts_report_unanswered_questions(self) -> None:
        facts = open_facts(self.workspace_acts(), self.registry)
        self.assertEqual(facts, ["demo.rate-choice|period=2025"])

    def test_read_model_is_deterministic(self) -> None:
        first = build_read_model(self.workspace_acts(), self.registry)
        second = build_read_model(self.workspace_acts(), self.registry)
        self.assertEqual(first, second)

    def test_evidence_standing_is_a_view_not_a_finding_mutation(self) -> None:
        acts = self.workspace_acts() + (
            act(5, "evidence-replaced", {"evidence_id": "demo-evidence-001"}),
        )
        model = build_read_model(acts, self.registry)
        finding_view = model["current"]["findings"]["finding-new"]
        self.assertEqual(finding_view["finding"]["id"], "finding-new")
        self.assertEqual(finding_view["evidence"][0]["status"], "withdrawn")


if __name__ == "__main__":
    unittest.main()
