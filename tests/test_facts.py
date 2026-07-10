"""Fact model tests: adoption, individuation, and the derived lattice."""

import tempfile
import unittest
from pathlib import Path

from packages.kernel.facts import (
    FactModelError,
    apply_act,
    facts_of,
    initial_state,
    project,
)
from packages.kernel.schema_registry import SchemaValidationError
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_fact_type_payment,
    registry_with_demo_kinds,
)


class FactsFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        schema_dir = Path(self._tmp.name)
        self.registry = registry_with_demo_kinds(schema_dir)


class TestAdoptionAndIndividuation(FactsFixture):
    def test_literal_keyed_facts_arrive_with_the_territory(self) -> None:
        state = project(
            (act(0, "bundle-adoption", {"bundle": demo_bundle()}),), self.registry
        )
        lattice = facts_of(state)
        self.assertIn("demo.rate-choice|period=2025", lattice)
        # No counterparty entities yet: the payment questions don't exist.
        payment_facts = [
            f for f in lattice.values() if f.fact_type_id == "demo.counterparty-payment"
        ]
        self.assertEqual(payment_facts, [])

    def test_entities_individuate_facts_into_existence(self) -> None:
        state = project(
            (
                act(0, "bundle-adoption", {"bundle": demo_bundle()}),
                act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
                act(2, "entity-introduced", {"entity": demo_entity("demo-corp-b", "Corp B")}),
            ),
            self.registry,
        )
        lattice = facts_of(state)
        self.assertIn("demo.counterparty-payment|counterparty=demo-corp-a,period=2025", lattice)
        self.assertIn("demo.counterparty-payment|counterparty=demo-corp-b,period=2025", lattice)
        fact = lattice["demo.counterparty-payment|counterparty=demo-corp-a,period=2025"]
        self.assertEqual(fact.individuated_by, ("demo-corp-a",))
        self.assertEqual(fact.nature, "determinable")

    def test_unrelated_entity_kinds_individuate_nothing(self) -> None:
        state = project(
            (
                act(0, "bundle-adoption", {"bundle": demo_bundle()}),
                act(1, "entity-introduced", {"entity": demo_entity("demo-acct", "Account", kind="demo.account")}),
            ),
            self.registry,
        )
        payment_facts = [
            f for f in facts_of(state).values()
            if f.fact_type_id == "demo.counterparty-payment"
        ]
        self.assertEqual(payment_facts, [])

    def test_readoption_supersedes_fact_type_declaration(self) -> None:
        revised = demo_bundle()
        revised["fact_types"][1]["title"] = "Rate treatment (revised)"
        state = project(
            (
                act(0, "bundle-adoption", {"bundle": demo_bundle()}),
                act(1, "bundle-adoption", {"bundle": revised}),
            ),
            self.registry,
        )
        self.assertEqual(
            state.fact_types["demo.rate-choice"]["title"], "Rate treatment (revised)"
        )

    def test_lattice_is_deterministic(self) -> None:
        acts = (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
        )
        first = facts_of(project(acts, self.registry))
        second = facts_of(project(acts, self.registry))
        self.assertEqual(first, second)


class TestEntitySupersession(FactsFixture):
    def _adopted_with_corp_a(self) -> tuple[dict[str, object], ...]:
        return (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
        )

    def test_superseding_an_entity_removes_its_facts_from_current_lattice(self) -> None:
        state = project(
            self._adopted_with_corp_a()
            + (act(2, "entity-superseded", {"entity_id": "demo-corp-a"}),),
            self.registry,
        )
        current = facts_of(state)
        self.assertNotIn(
            "demo.counterparty-payment|counterparty=demo-corp-a,period=2025", current
        )
        full = facts_of(state, include_displaced=True)
        self.assertIn(
            "demo.counterparty-payment|counterparty=demo-corp-a,period=2025", full
        )

    def test_replacement_entity_individuates_successor_facts(self) -> None:
        state = project(
            self._adopted_with_corp_a()
            + (
                act(
                    2,
                    "entity-superseded",
                    {
                        "entity_id": "demo-corp-a",
                        "replacement": demo_entity("demo-corp-a2", "Corp A (corrected)"),
                    },
                ),
            ),
            self.registry,
        )
        current = facts_of(state)
        self.assertIn(
            "demo.counterparty-payment|counterparty=demo-corp-a2,period=2025", current
        )
        self.assertEqual(state.entities["demo-corp-a"].status, "superseded")
        self.assertEqual(state.entities["demo-corp-a"].successor_id, "demo-corp-a2")

    def test_superseding_unknown_or_non_current_entity_is_rejected(self) -> None:
        state = project(self._adopted_with_corp_a(), self.registry)
        with self.assertRaises(FactModelError):
            apply_act(
                state, act(2, "entity-superseded", {"entity_id": "demo-ghost"}), self.registry
            )
        superseded = apply_act(
            state, act(2, "entity-superseded", {"entity_id": "demo-corp-a"}), self.registry
        )
        with self.assertRaises(FactModelError):
            apply_act(
                superseded,
                act(3, "entity-superseded", {"entity_id": "demo-corp-a"}),
                self.registry,
            )


class TestSemanticRejection(FactsFixture):
    def test_duplicate_entity_id_is_rejected(self) -> None:
        state = apply_act(
            initial_state(),
            act(0, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
            self.registry,
        )
        with self.assertRaises(FactModelError):
            apply_act(
                state,
                act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Again")}),
                self.registry,
            )

    def test_duplicate_identity_key_names_are_rejected(self) -> None:
        fact_type = demo_fact_type_payment()
        fact_type["identity_keys"].append(
            {"name": "counterparty", "kind": "literal", "values": ["x"]}
        )
        bundle = demo_bundle()
        bundle["fact_types"] = [fact_type]
        with self.assertRaises(FactModelError):
            apply_act(
                initial_state(),
                act(0, "bundle-adoption", {"bundle": bundle}),
                self.registry,
            )

    def test_invalid_value_schema_is_rejected(self) -> None:
        fact_type = demo_fact_type_payment()
        fact_type["value_schema"] = {"type": "not-a-type"}
        bundle = demo_bundle()
        bundle["fact_types"] = [fact_type]
        with self.assertRaises(FactModelError):
            apply_act(
                initial_state(),
                act(0, "bundle-adoption", {"bundle": bundle}),
                self.registry,
            )

    def test_duplicate_fact_type_in_bundle_is_rejected(self) -> None:
        bundle = demo_bundle()
        bundle["fact_types"] = [demo_fact_type_payment(), demo_fact_type_payment()]
        with self.assertRaises(FactModelError):
            apply_act(
                initial_state(),
                act(0, "bundle-adoption", {"bundle": bundle}),
                self.registry,
            )

    def test_malformed_nested_fact_type_is_rejected_not_repaired(self) -> None:
        bundle = demo_bundle()
        del bundle["fact_types"][0]["nature"]
        with self.assertRaises(SchemaValidationError):
            apply_act(
                initial_state(),
                act(0, "bundle-adoption", {"bundle": bundle}),
                self.registry,
            )


if __name__ == "__main__":
    unittest.main()
