"""Kernel contract for the migration-artifact supersession root (ADR-0063)."""

from __future__ import annotations

import unittest
from dataclasses import replace
from typing import Any

from packages.kernel.currency import DECLARED_EDGE_KINDS, compute_currency
from packages.kernel.facts import FactModelError, facts_of
from packages.kernel.findings import FindingModelError, project
from packages.kernel.schema_registry import SchemaRegistry
from tests.support import act, demo_evidence, demo_finding

PRED = "demo.pred.absence"
SUCC = "demo.succ.absence"
MIGRATION_ID = "demo.schedule1.succession"


def _type(type_id: str, title: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": type_id,
        "version": "v1",
        "title": title,
        "nature": "determinable",
        "identity_keys": [{"kind": "literal", "name": "tax-year", "values": ["2025"]}],
        "value_schema": {"type": "string", "enum": ["yes", "no"]},
        "supersession": {"policy": "free"},
    }


def _bundle(bundle_id: str, *types: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": bundle_id,
        "version": "v1",
        "label": bundle_id,
        "fact_types": list(types),
    }


def _migration(
    *,
    predecessor: str = PRED,
    successor: str = SUCC,
    migration_id: str = MIGRATION_ID,
) -> dict[str, Any]:
    return {
        "schema": "migration-artifact.v1",
        "id": migration_id,
        "version": "v1",
        "title": "Demo succession",
        "finding_mapping": {"policy": "presented-claim"},
        "pairs": [{"predecessor": predecessor, "successor": successor}],
    }


def _yes_no_finding(finding_id: str, fact_id: str, value: str) -> dict[str, Any]:
    return demo_finding(
        finding_id=finding_id,
        fact_id=fact_id,
        value=value,
        evidence_ids=["demo-evidence-001"],
        basis="attested",
    )


class MigrationSupersessionRootTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry()

    def _base(self) -> list[dict[str, Any]]:
        return [
            act(0, "bundle-adoption", {"bundle": _bundle("demo.pred.vocabulary", _type(PRED, "Predecessor"))}),
            act(1, "bundle-adoption", {"bundle": _bundle("demo.succ.vocabulary", _type(SUCC, "Successor"))}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
        ]

    def test_open_predecessor_then_migration_retires_type_and_presents_nothing(self) -> None:
        state = project(
            tuple(self._base())
            + (act(3, "migration-adoption", {"migration": _migration()}),),
            self.registry,
        )
        lattice = facts_of(state.fact_state)
        self.assertNotIn(PRED, state.fact_state.fact_types)
        self.assertIn(PRED, state.fact_state.retired_fact_type_ids)
        self.assertIn(SUCC, state.fact_state.fact_types)
        self.assertTrue(any(f.fact_type_id == SUCC for f in lattice.values()))
        self.assertFalse(any(f.fact_type_id == PRED for f in lattice.values()))
        self.assertEqual(state.presented_successor_claims, ())
        view = compute_currency(state)
        self.assertEqual(view.current_finding_ids, frozenset())

    def test_current_yes_is_displaced_and_presented_not_converted(self) -> None:
        state = project(
            tuple(self._base())
            + (
                act(3, "assertion", {"finding": _yes_no_finding("f-yes", f"{PRED}|tax-year=2025", "yes")}),
                act(4, "migration-adoption", {"migration": _migration()}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertIn("f-yes", view.displaced_finding_ids)
        self.assertNotIn("f-yes", view.current_finding_ids)
        self.assertEqual(view.reasons["f-yes"][0].kind, "supersession")
        self.assertEqual(view.reasons["f-yes"][0].by, MIGRATION_ID)
        self.assertEqual(len(state.presented_successor_claims), 1)
        claim = state.presented_successor_claims[0]
        self.assertEqual(claim["proposed_value"], "yes")
        self.assertEqual(claim["successor_fact_id"], f"{SUCC}|tax-year=2025")
        self.assertEqual(claim["predecessor_finding_id"], "f-yes")
        self.assertNotIn(SUCC + "|tax-year=2025", [f["fact_id"] for f in state.findings.values()])

    def test_current_no_is_displaced_and_presented(self) -> None:
        state = project(
            tuple(self._base())
            + (
                act(3, "assertion", {"finding": _yes_no_finding("f-no", f"{PRED}|tax-year=2025", "no")}),
                act(4, "migration-adoption", {"migration": _migration()}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertIn("f-no", view.displaced_finding_ids)
        self.assertEqual(state.presented_successor_claims[0]["proposed_value"], "no")

    def test_only_last_current_finding_is_presented_after_correction(self) -> None:
        state = project(
            tuple(self._base())
            + (
                act(3, "assertion", {"finding": _yes_no_finding("f-old", f"{PRED}|tax-year=2025", "no")}),
                act(4, "assertion", {"finding": _yes_no_finding("f-new", f"{PRED}|tax-year=2025", "yes")}),
                act(5, "migration-adoption", {"migration": _migration()}),
            ),
            self.registry,
        )
        view = compute_currency(state)
        self.assertIn("f-old", view.displaced_finding_ids)
        self.assertIn("f-new", view.displaced_finding_ids)
        self.assertEqual(len(state.presented_successor_claims), 1)
        self.assertEqual(state.presented_successor_claims[0]["predecessor_finding_id"], "f-new")
        self.assertEqual(state.presented_successor_claims[0]["proposed_value"], "yes")

    def test_user_asserts_presented_claim_successor_becomes_current(self) -> None:
        acts = list(self._base()) + [
            act(3, "assertion", {"finding": _yes_no_finding("f-yes", f"{PRED}|tax-year=2025", "yes")}),
            act(4, "migration-adoption", {"migration": _migration()}),
            act(5, "assertion", {"finding": _yes_no_finding("f-succ", f"{SUCC}|tax-year=2025", "yes")}),
        ]
        state = project(tuple(acts), self.registry)
        view = compute_currency(state)
        self.assertIn("f-succ", view.current_finding_ids)
        self.assertIn("f-yes", view.displaced_finding_ids)
        replayed = project(tuple(acts), self.registry)
        self.assertEqual(state.fact_state.retired_fact_type_ids, replayed.fact_state.retired_fact_type_ids)
        self.assertEqual(compute_currency(replayed).current_finding_ids, view.current_finding_ids)
        self.assertEqual(state.presented_successor_claims, replayed.presented_successor_claims)

    def test_derivation_consumers_cascade_on_existing_edge(self) -> None:
        state = project(
            tuple(self._base())
            + (
                act(3, "assertion", {"finding": _yes_no_finding("f-yes", f"{PRED}|tax-year=2025", "yes")}),
                act(4, "migration-adoption", {"migration": _migration()}),
            ),
            self.registry,
        )
        derived = demo_finding(
            finding_id="derived-consumer",
            fact_id="demo.synthetic-derived|tax-year=2025",
            value="yes",
            evidence_ids=[],
            basis="attested",
        )
        derived["pins"] = {"finding_ids": ["f-yes"], "artifact_ids": ["demo-rule.v1"]}
        state = replace(state, findings={**state.findings, "derived-consumer": derived})
        view = compute_currency(state)
        self.assertIn("derived-consumer", view.displaced_finding_ids)
        self.assertEqual(view.reasons["derived-consumer"][0].kind, "derivation")
        self.assertEqual(view.reasons["derived-consumer"][0].by, "f-yes")
        self.assertEqual(view.reasons["f-yes"][0].kind, "supersession")

    def test_omitting_a_type_from_the_runtime_map_does_not_displace(self) -> None:
        state = project(
            tuple(self._base())
            + (act(3, "assertion", {"finding": _yes_no_finding("f-yes", f"{PRED}|tax-year=2025", "yes")}),),
            self.registry,
        )
        stripped = dict(state.fact_state.fact_types)
        stripped.pop(PRED)
        mutant = replace(state, fact_state=replace(state.fact_state, fact_types=stripped))
        view = compute_currency(mutant)
        self.assertIn("f-yes", view.current_finding_ids)
        self.assertNotIn("f-yes", view.displaced_finding_ids)

    def test_no_individuation_edge_or_third_edge_kind(self) -> None:
        self.assertEqual(DECLARED_EDGE_KINDS, frozenset({"derivation", "individuation"}))
        state = project(
            tuple(self._base())
            + (
                act(3, "assertion", {"finding": _yes_no_finding("f-yes", f"{PRED}|tax-year=2025", "yes")}),
                act(4, "migration-adoption", {"migration": _migration()}),
            ),
            self.registry,
        )
        self.assertEqual(view_kind := compute_currency(state).reasons["f-yes"][0].kind, "supersession")
        self.assertNotEqual(view_kind, "individuation")
        before = project(tuple(self._base()), self.registry)
        pred_fact = facts_of(before.fact_state)[f"{PRED}|tax-year=2025"]
        self.assertEqual(pred_fact.individuated_by, ())
        succ_fact = facts_of(state.fact_state)[f"{SUCC}|tax-year=2025"]
        self.assertEqual(succ_fact.individuated_by, ())

    def test_cannot_assert_on_retired_predecessor(self) -> None:
        base = list(self._base()) + [
            act(3, "migration-adoption", {"migration": _migration()}),
        ]
        with self.assertRaises(FindingModelError):
            project(
                tuple(base)
                + (act(4, "assertion", {"finding": _yes_no_finding("late", f"{PRED}|tax-year=2025", "yes")}),),
                self.registry,
            )

    def test_readoption_of_retired_type_does_not_restore_it(self) -> None:
        state = project(
            tuple(self._base())
            + (
                act(3, "migration-adoption", {"migration": _migration()}),
                act(4, "bundle-adoption", {"bundle": _bundle("demo.pred.vocabulary", _type(PRED, "Predecessor"))}),
            ),
            self.registry,
        )
        self.assertNotIn(PRED, state.fact_state.fact_types)
        self.assertIn(PRED, state.fact_state.retired_fact_type_ids)

    def test_successor_must_already_be_current(self) -> None:
        with self.assertRaises(FactModelError):
            project(
                (
                    act(0, "bundle-adoption", {"bundle": _bundle("demo.pred.vocabulary", _type(PRED, "Predecessor"))}),
                    act(1, "migration-adoption", {"migration": _migration()}),
                ),
                self.registry,
            )

    def test_fresh_successor_workspace_has_no_predecessor_finding_and_no_claim(self) -> None:
        state = project(
            (
                act(0, "bundle-adoption", {"bundle": _bundle("demo.succ.vocabulary", _type(SUCC, "Successor"))}),
                act(1, "migration-adoption", {"migration": _migration()}),
            ),
            self.registry,
        )
        self.assertNotIn(PRED, state.fact_state.fact_types)
        self.assertIn(PRED, state.fact_state.retired_fact_type_ids)
        self.assertEqual(state.presented_successor_claims, ())
        self.assertTrue(any(f.fact_type_id == SUCC for f in facts_of(state.fact_state).values()))
