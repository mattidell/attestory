"""Regressions for fact-type schema-check reuse and historical-lattice reuse."""

from __future__ import annotations

import gc
import tempfile
import weakref
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import jsonschema

from packages.kernel import facts
from packages.kernel.currency import CurrencyView, compute_currency
from packages.kernel.facts import FactModelError, apply_bundle_adoption, initial_state
from packages.kernel.findings import apply_act, project
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_fact_type_payment,
    demo_fact_type_rate_choice,
    demo_finding,
    demo_payment_fact_id,
    registry_with_demo_kinds,
)

_SCHEMA_A: dict[str, Any] = {"type": "number", "$comment": "track2-schema-a"}
_SCHEMA_B: dict[str, Any] = {"type": "string", "$comment": "track2-schema-b"}
_SCHEMA_INVALID: dict[str, Any] = {
    "type": "not-a-json-schema-type",
    "$comment": "track2-invalid",
}
_CURRENCY_FIELDS = (
    "current_finding_ids",
    "displaced_finding_ids",
    "current_evidence_ids",
    "displaced_evidence_ids",
    "reasons",
)


def _bundle(fact_type: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "bundle.v1",
        "id": "demo.track2.bundle",
        "label": "Track 2",
        "fact_types": [fact_type],
    }


class SchemaAndHistoricalLatticeReuse(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self.tmp.name))

    def _adopt(
        self, state: facts.KernelState, fact_type: dict[str, Any]
    ) -> facts.KernelState:
        return apply_bundle_adoption(
            state, {"bundle": _bundle(fact_type)}, self.registry
        )

    def test_a_tuple_twin_of_a_cached_valid_schema_is_still_refused(self) -> None:
        # json.dumps writes a tuple like a list, but Draft 2020-12 requires an
        # array. A cached success for the list form must not admit the tuple.
        listed = demo_fact_type_payment()
        listed["value_schema"] = {
            "type": "object",
            "required": ["amount"],
            "$comment": "track2-tuple-twin",
        }
        twin = demo_fact_type_rate_choice()
        twin["id"] = "demo.tuple-form"
        twin["value_schema"] = {
            "type": "object",
            "required": ("amount",),
            "$comment": "track2-tuple-twin",
        }
        state = self._adopt(initial_state(), listed)
        with self.assertRaisesRegex(
            FactModelError, "demo.tuple-form: value_schema is not valid JSON Schema"
        ):
            self._adopt(state, twin)
        with self.assertRaisesRegex(FactModelError, "demo.tuple-form"):
            self._adopt(state, twin)

    def test_a_collected_state_leaves_no_entry_and_a_recycled_id_is_rebuilt(self) -> None:
        memo = facts._HISTORICAL_LATTICES
        state = initial_state()
        facts.facts_of(state, include_displaced=True)
        ident = id(state)
        self.assertIn(ident, memo._entries)
        del state
        gc.collect()
        self.assertNotIn(ident, memo._entries)

        # A stale entry whose weak reference no longer names this object must
        # not be returned for a new object that happens to have the same id.
        gone = initial_state()
        dead = weakref.ref(gone)
        del gone
        gc.collect()
        self.assertIsNone(dead())
        fresh = initial_state()
        memo._entries[id(fresh)] = (dead, {"demo.stale": None})  # type: ignore[dict-item]
        rebuilt = facts.facts_of(fresh, include_displaced=True)
        self.assertNotIn("demo.stale", rebuilt)
        self.assertEqual(rebuilt, facts._project_fact_lattice(fresh, include_displaced=True))

    def test_invalid_value_schema_is_refused_on_every_fold(self) -> None:
        checks = 0
        original = jsonschema.Draft202012Validator.check_schema

        def counted(schema: Any) -> None:
            nonlocal checks
            checks += 1
            original(schema)

        with patch.object(jsonschema.Draft202012Validator, "check_schema", counted):
            for fact_id in ("demo.bad-one", "demo.bad-two"):
                fact_type = demo_fact_type_payment()
                fact_type["id"] = fact_id
                fact_type["value_schema"] = dict(_SCHEMA_INVALID)
                with self.assertRaises(FactModelError) as caught:
                    self._adopt(initial_state(), fact_type)
                self.assertIn(fact_id, str(caught.exception))
                self.assertIn("not valid JSON Schema", str(caught.exception))
        self.assertEqual(checks, 2)

    def test_changed_schema_is_checked_once_per_document_and_other_checks_still_run(
        self,
    ) -> None:
        checks = 0
        declared = 0
        original_check = jsonschema.Draft202012Validator.check_schema
        original_declared = self.registry.validate_declared

        def counted_check(schema: Any) -> None:
            nonlocal checks
            checks += 1
            original_check(schema)

        def counted_declared(instance: dict[str, Any]) -> str:
            nonlocal declared
            declared += 1
            return original_declared(instance)

        payment = demo_fact_type_payment()
        payment["value_schema"] = dict(_SCHEMA_A)
        rate = demo_fact_type_rate_choice()
        rate["value_schema"] = dict(_SCHEMA_A)
        revised_payment = demo_fact_type_payment()
        revised_payment["value_schema"] = dict(_SCHEMA_B)
        duplicate = demo_fact_type_payment()
        duplicate["id"] = "demo.duplicate-keys"
        duplicate["value_schema"] = dict(_SCHEMA_A)
        duplicate["identity_keys"] = [
            {"name": "period", "kind": "literal", "values": ["2025"]},
            {"name": "period", "kind": "literal", "values": ["2026"]},
        ]

        with patch.object(
            jsonschema.Draft202012Validator, "check_schema", counted_check
        ), patch.object(self.registry, "validate_declared", counted_declared):
            state = self._adopt(initial_state(), payment)
            self.assertEqual(checks, 1)
            state = self._adopt(state, rate)
            self.assertEqual(checks, 1)
            state = self._adopt(state, revised_payment)
            self.assertEqual(checks, 2)
            self.assertEqual(
                state.fact_types["demo.counterparty-payment"]["value_schema"],
                _SCHEMA_B,
            )
            state = self._adopt(state, rate)
            self.assertEqual(checks, 2)
            with self.assertRaisesRegex(FactModelError, "duplicate identity key"):
                self._adopt(state, duplicate)
        self.assertEqual(declared, 10)

    def test_new_fact_state_rebuilds_the_historical_lattice_and_matches_currency(
        self,
    ) -> None:
        before = project(
            (
                act(0, "bundle-adoption", {"bundle": demo_bundle()}),
                act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
                act(2, "evidence-submitted", {"evidence": demo_evidence()}),
                act(3, "assertion", {"finding": demo_finding("finding-keyed")}),
            ),
            self.registry,
        )
        after = apply_act(
            before,
            act(
                4,
                "entity-superseded",
                {
                    "entity_id": "demo-corp-a",
                    "replacement": demo_entity("demo-corp-a2", "Corp A (corrected)"),
                },
            ),
            self.registry,
        )
        self.assertIsNot(before.fact_state, after.fact_state)

        historical_builds = 0
        real = facts._project_fact_lattice

        def counted(
            state: facts.KernelState, *, include_displaced: bool = False
        ) -> dict[str, facts.Fact]:
            nonlocal historical_builds
            if include_displaced:
                historical_builds += 1
            return real(state, include_displaced=include_displaced)

        with patch.object(facts, "_project_fact_lattice", side_effect=counted):
            compute_currency(before)
            compute_currency(before)
            self.assertEqual(historical_builds, 1)
            view = compute_currency(after)
            compute_currency(after)
            self.assertEqual(historical_builds, 2)

        before_lattice = facts.facts_of(before.fact_state, include_displaced=True)
        after_lattice = facts.facts_of(after.fact_state, include_displaced=True)
        successor = demo_payment_fact_id("demo-corp-a2")
        self.assertIsNot(before_lattice, after_lattice)
        self.assertNotIn(successor, before_lattice)
        self.assertIn(successor, after_lattice)
        self.assertEqual(after_lattice, real(after.fact_state, include_displaced=True))

        with patch("packages.kernel.currency.facts_of", side_effect=real):
            uncached = compute_currency(after)
        self.assertIsInstance(view, CurrencyView)
        for field_name in _CURRENCY_FIELDS:
            self.assertEqual(
                getattr(view, field_name),
                getattr(uncached, field_name),
                field_name,
            )
        self.assertEqual(view.displaced_finding_ids, frozenset({"finding-keyed"}))
        self.assertEqual(view.current_finding_ids, frozenset())
        self.assertEqual(view.reasons["finding-keyed"][0].kind, "individuation")
        self.assertEqual(view.reasons["finding-keyed"][0].by, "demo-corp-a")
        self.assertIn(
            "finding-keyed", compute_currency(before).current_finding_ids
        )


if __name__ == "__main__":
    unittest.main()
