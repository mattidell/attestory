"""Differential checks for projection-local current-lattice reuse."""

from __future__ import annotations

import dataclasses
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from typing import Any

from packages.kernel import facts
from packages.kernel.currency import compute_currency
from packages.kernel.findings import (
    FindingModelError,
    FindingState,
    _CurrentLatticeHolder,
    _apply_assertion,
    apply_act,
    initial_state,
    project,
)
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    demo_payment_fact_id,
    registry_with_demo_kinds,
)


class ProjectionLatticeReuse(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self.tmp.name))

    def base(self) -> tuple[dict[str, Any], ...]:
        return (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "A")}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
        )

    def uncached_fold(self, acts: tuple[dict[str, Any], ...]) -> FindingState:
        state = initial_state()
        for row in acts:
            state = apply_act(state, row, self.registry)
        return state

    def test_repeated_assertions_reuse_one_lattice_and_match_uncached_fold(self) -> None:
        rows = self.base() + tuple(
            act(
                i + 3,
                "assertion",
                {"finding": demo_finding(f"demo.finding.{i}", value=1200 + i)},
            )
            for i in range(6)
        )
        original = facts.facts_of
        builds = 0

        def counted(
            state: facts.KernelState, *, include_displaced: bool = False
        ) -> dict[str, facts.Fact]:
            nonlocal builds
            builds += 1
            return original(state, include_displaced=include_displaced)

        with patch.object(facts, "facts_of", side_effect=counted):
            optimized = project(rows, self.registry)
        self.assertEqual(builds, 1)
        cold = self.uncached_fold(rows)
        self.assertEqual(optimized, cold)
        self.assertEqual(compute_currency(optimized), compute_currency(cold))

    def test_direct_public_applier_remains_uncached(self) -> None:
        state = self.uncached_fold(self.base())
        row = act(3, "assertion", {"finding": demo_finding()})
        original = facts.facts_of
        builds = 0

        def counted(
            state: facts.KernelState, *, include_displaced: bool = False
        ) -> dict[str, facts.Fact]:
            nonlocal builds
            builds += 1
            return original(state, include_displaced=include_displaced)

        with patch.object(facts, "facts_of", side_effect=counted):
            apply_act(state, row, self.registry)
        self.assertEqual(builds, 2)

    def test_bundle_readoption_rebuilds_after_identity_and_nature_change(self) -> None:
        bundle = demo_bundle()
        rows = self.base() + (
            act(3, "assertion", {"finding": demo_finding()}),
            act(
                4,
                "bundle-adoption",
                {"bundle": {**bundle, "fact_types": [
                    {**bundle["fact_types"][0], "nature": "elective",
                     "identity_keys": [*bundle["fact_types"][0]["identity_keys"],
                                       {"name": "channel", "kind": "literal", "values": ["demo"]}]},
                    bundle["fact_types"][1],
                ]}},
            ),
            act(5, "assertion", {"finding": demo_finding(
                "demo.readopted", "demo.counterparty-payment|counterparty=demo-corp-a,period=2025,channel=demo",
                basis="elective",
            )}),
        )
        optimized = project(rows, self.registry)
        cold = self.uncached_fold(rows)
        self.assertEqual(optimized, cold)
        self.assertEqual(compute_currency(optimized), compute_currency(cold))
        self.assertIn("demo.readopted", optimized.findings)

    def test_closed_empty_member_add_reclose_uses_successor_horizon(self) -> None:
        bundle = {
            "schema": "bundle.v1", "id": "demo.family.bundle", "label": "Demo family",
            "fact_types": [
                {"schema": "fact-type.v1", "id": "demo.family.member", "title": "Member",
                 "nature": "determinable", "identity_keys": [
                     {"name": "member", "kind": "entity", "entity_kind": "demo.member"}],
                 "value_schema": {"type": "number"}, "supersession": {"policy": "free"}},
                {"schema": "fact-type.v1", "id": "demo.family.closure", "title": "Closure",
                 "nature": "determinable", "identity_keys": [
                     {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"}],
                 "value_schema": {"type": "boolean"}, "supersession": {"policy": "free"}},
            ],
        }
        family = {"id": "demo.family", "version": "v1"}
        scope = {"subject": "demo.subject"}
        rows = (
            act(0, "bundle-adoption", {"bundle": bundle}),
            act(1, "entity-introduced", {"entity": demo_entity("demo.member.a", "Member A", "demo.member")}),
            act(2, "horizon-genesis", {"family": family, "scope": scope, "horizon_id": "demo.family.h0"}),
            act(3, "assertion", {"finding": {"schema": "finding.v1", "id": "demo.close.0",
                "fact_id": "demo.family.closure|family-horizon=demo.family.h0", "value": True,
                "basis": "attested", "evidence_ids": []}}),
            act(4, "member-transition", {"family": family, "scope": scope,
                "member": {"action": "assert", "finding": {"schema": "finding.v1", "id": "demo.member.finding",
                    "fact_id": "demo.family.member|member=demo.member.a", "value": 3,
                    "basis": "attested", "evidence_ids": []}},
                "successor": {"id": "demo.family.h1", "predecessor": "demo.family.h0"}}),
            act(5, "assertion", {"finding": {"schema": "finding.v1", "id": "demo.close.1",
                "fact_id": "demo.family.closure|family-horizon=demo.family.h1", "value": True,
                "basis": "attested", "evidence_ids": []}}),
        )
        optimized = project(rows, self.registry)
        cold = self.uncached_fold(rows)
        self.assertEqual(optimized, cold)
        self.assertEqual(compute_currency(optimized), compute_currency(cold))

    def test_family_handover_invalidates_after_prior_current_lookup(self) -> None:
        bundle = {
            "schema": "bundle.v1", "id": "demo.handover.bundle", "label": "Demo handover",
            "fact_types": [{
                "schema": "fact-type.v1", "id": "demo.handover.closure", "title": "Closure",
                "nature": "determinable", "identity_keys": [{
                    "name": "family-horizon", "kind": "entity",
                    "entity_kind": "kernel.family-horizon",
                }], "value_schema": {"type": "boolean"},
                "supersession": {"policy": "free"},
            }],
        }
        family_v1 = {"id": "demo.handover", "version": "v1"}
        family_v2 = {"id": "demo.handover", "version": "v2"}
        scope = {"subject": "demo.subject"}
        rows = (
            act(0, "bundle-adoption", {"bundle": bundle}),
            act(1, "horizon-genesis", {"family": family_v1, "scope": scope,
                                         "horizon_id": "demo.handover.v1.h0"}),
            act(2, "assertion", {"finding": {
                "schema": "finding.v1", "id": "demo.handover.close.v1",
                "fact_id": "demo.handover.closure|family-horizon=demo.handover.v1.h0",
                "value": True, "basis": "attested", "evidence_ids": [],
            }}),
            act(3, "family-handover", {"predecessor": {
                "family": family_v1, "scope": scope, "horizon_id": "demo.handover.v1.h0",
            }, "successor": {
                "family": family_v2, "scope": scope, "horizon_id": "demo.handover.v2.h0",
            }}),
            act(4, "assertion", {"finding": {
                "schema": "finding.v1", "id": "demo.handover.close.v2",
                "fact_id": "demo.handover.closure|family-horizon=demo.handover.v2.h0",
                "value": True, "basis": "attested", "evidence_ids": [],
            }}),
        )
        original = facts.facts_of
        builds = 0

        def counted(state: facts.KernelState, *, include_displaced: bool = False) -> dict[str, facts.Fact]:
            nonlocal builds
            builds += 1
            return original(state, include_displaced=include_displaced)

        with patch.object(facts, "facts_of", side_effect=counted):
            optimized = project(rows, self.registry)
        cold = self.uncached_fold(rows)
        self.assertEqual(builds, 2)
        self.assertEqual(optimized, cold)
        self.assertEqual(compute_currency(optimized), compute_currency(cold))
        self.assertIn("demo.handover.close.v2", optimized.findings)

    def test_historical_retraction_after_current_lookup_inside_fold(self) -> None:
        rows = self.base() + (
            act(3, "assertion", {"finding": demo_finding("demo.finding.a")}),
            act(4, "entity-superseded", {"entity_id": "demo-corp-a",
                "replacement": demo_entity("demo-corp-b", "B")}),
            act(5, "assertion", {"finding": demo_finding("demo.finding.b", demo_payment_fact_id("demo-corp-b"))}),
            act(6, "finding-retracted", {"finding_id": "demo.finding.a"}),
        )
        with self.assertRaisesRegex(FindingModelError, "individuation by demo-corp-a") as optimized_error:
            project(rows, self.registry)
        with self.assertRaisesRegex(FindingModelError, "individuation by demo-corp-a") as cold_error:
            self.uncached_fold(rows)
        self.assertEqual(str(optimized_error.exception), str(cold_error.exception))

    def test_projects_do_not_share_holder_after_caller_mutation(self) -> None:
        rows = self.base() + (act(3, "assertion", {"finding": demo_finding()}),)
        project(rows, self.registry)
        rows[0]["payload"]["bundle"]["fact_types"][0]["nature"] = "elective"
        with self.assertRaisesRegex(FindingModelError, "fact .* is elective") as optimized_error:
            project(rows, self.registry)
        with self.assertRaisesRegex(FindingModelError, "fact .* is elective") as cold_error:
            self.uncached_fold(rows)
        self.assertEqual(str(optimized_error.exception), str(cold_error.exception))

    def test_invalid_findings_keep_same_exception_and_refusal_boundary(self) -> None:
        scenarios = {
            "unknown": self.base() + (act(3, "assertion", {"finding": demo_finding(
                fact_id="demo.unknown|period=2025")}),),
            "malformed": self.base() + (act(3, "assertion", {"finding": demo_finding(
                value="not numeric")}),),
            "duplicate": self.base() + tuple(
                act(i, "assertion", {"finding": demo_finding("demo.duplicate")})
                for i in (3, 4)
            ),
        }
        for label, rows in scenarios.items():
            with self.subTest(label=label):
                with self.assertRaises(FindingModelError) as optimized_error:
                    project(rows, self.registry)
                with self.assertRaises(FindingModelError) as cold_error:
                    self.uncached_fold(rows)
                self.assertEqual(str(optimized_error.exception), str(cold_error.exception))

    def test_locked_correction_matches_fold_holder_and_uncached_applier(self) -> None:
        state = self.uncached_fold(self.base() + (
            act(3, "assertion", {"finding": demo_finding("demo.locked.1")}),
        ))
        locked_type = {
            **state.fact_state.fact_types["demo.counterparty-payment"],
            "supersession": {"policy": "locked"},
        }
        state = dataclasses.replace(
            state,
            fact_state=dataclasses.replace(
                state.fact_state,
                fact_types={**state.fact_state.fact_types,
                            "demo.counterparty-payment": locked_type},
            ),
        )
        payload = {"finding": demo_finding("demo.locked.2", value=1300)}
        with self.assertRaises(FindingModelError) as optimized_error:
            _apply_assertion(state, payload, self.registry, _CurrentLatticeHolder())
        with self.assertRaises(FindingModelError) as cold_error:
            apply_act(state, act(4, "assertion", payload), self.registry)
        self.assertEqual(str(optimized_error.exception), str(cold_error.exception))


if __name__ == "__main__":
    unittest.main()
