"""Source Completeness Track 2: atomic horizon projection and currency.

ADR-0017 in the kernel: horizon chains fold from immutable accepted
acts; succession feeds the existing individuation root set through the
projected horizon entity, so closure findings keyed on a superseded
horizon displace along the two declared edges only. Every admission
negative recorded by Track 1 is rejected atomically here.
"""

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import workspace_registry
from packages.derivation.projection import workspace_currency
from packages.kernel import facts, findings, horizons
from packages.kernel.act_log import ActLog
from packages.kernel.currency import DECLARED_EDGE_KINDS, compute_currency
from packages.kernel.findings import FindingModelError
from packages.kernel.horizons import HorizonModelError
from packages.kernel.schema_registry import SchemaRegistry

ADMISSION_NEGATIVES = Path("packages/sample_data/source_authority/negatives/admission")

FAMILY = {"id": "sc.family.demo", "version": "v1"}
SCOPE = {"subject": "s1"}
MEMBER_FACT_TYPE = {
    "schema": "fact-type.v1",
    "id": "sc.member.amount",
    "title": "Demo member amount",
    "nature": "determinable",
    "identity_keys": [
        {"name": "slip", "kind": "entity", "entity_kind": "sc.slip"},
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"type": "number"},
    "supersession": {"policy": "free"},
}
CLOSURE_FACT_TYPE = {
    "schema": "fact-type.v1",
    "id": "sc.family.closure",
    "title": "Demo family closure",
    "nature": "determinable",
    "identity_keys": [
        {
            "name": "family-horizon",
            "kind": "entity",
            "entity_kind": "kernel.family-horizon",
        },
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"type": "boolean"},
    "supersession": {"policy": "free"},
}

MEMBER_FACT_SLIP1 = "sc.member.amount|slip=sc.slip-1,year=2025"
MEMBER_FACT_SLIP2 = "sc.member.amount|slip=sc.slip-2,year=2025"


def closure_fact(horizon_id: str) -> str:
    return f"sc.family.closure|family-horizon={horizon_id},year=2025"


def act(kind: str, payload: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"sc-act-{index:03d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-07-12T01:{index:02d}:00Z",
        "committed_against": index,
        "payload": payload,
    }


def finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def base_acts() -> list[dict[str, Any]]:
    """Bundle, one slip, genesis h0, closure attested true on h0."""
    return [
        act(
            "bundle-adoption",
            {
                "bundle": {
                    "schema": "bundle.v1",
                    "id": "sc.vocabulary",
                    "label": "Source-completeness demo vocabulary",
                    "fact_types": [MEMBER_FACT_TYPE, CLOSURE_FACT_TYPE],
                }
            },
            0,
        ),
        act(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "sc.slip-1",
                    "kind": "sc.slip",
                    "label": "Demo slip 1",
                }
            },
            1,
        ),
        act(
            "horizon-genesis",
            {"family": FAMILY, "scope": SCOPE, "horizon_id": "sc.h0"},
            2,
        ),
        act(
            "assertion",
            {"finding": finding("sc.closure.h0", closure_fact("sc.h0"), True)},
            3,
        ),
    ]


def transition_act(
    index: int,
    member: dict[str, Any],
    successor_id: str,
    predecessor_id: str,
) -> dict[str, Any]:
    return act(
        "member-transition",
        {
            "family": FAMILY,
            "scope": SCOPE,
            "member": member,
            "successor": {"id": successor_id, "predecessor": predecessor_id},
        },
        index,
    )


def assert_member(finding_id: str, fact_id: str, value: float) -> dict[str, Any]:
    return {"action": "assert", "finding": finding(finding_id, fact_id, value)}


class HorizonFixture(unittest.TestCase):
    registry: SchemaRegistry

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry()

    def project(self, acts: list[dict[str, Any]]) -> findings.FindingState:
        return findings.project(tuple(acts), self.registry)


class GenesisProjection(HorizonFixture):
    def test_genesis_projects_horizon_and_closure_fact(self) -> None:
        state = self.project(base_acts())
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE), "sc.h0"
        )
        lattice = facts.facts_of(state.fact_state)
        self.assertIn(closure_fact("sc.h0"), lattice)
        entity = state.fact_state.entities["sc.h0"].entity
        self.assertEqual(entity["kind"], horizons.HORIZON_ENTITY_KIND)

    def test_transition_before_genesis_is_rejected(self) -> None:
        acts = base_acts()
        del acts[2:]  # no genesis, no closure
        state = self.project(acts)
        move = transition_act(
            4, assert_member("sc.m1", MEMBER_FACT_SLIP1, 100), "sc.h1", "sc.h0"
        )
        with self.assertRaisesRegex(HorizonModelError, "genesis is required"):
            findings.apply_act(state, move, self.registry)

    def test_horizon_id_colliding_with_entity_is_rejected(self) -> None:
        state = self.project(base_acts()[:2])
        genesis = act(
            "horizon-genesis",
            {"family": FAMILY, "scope": SCOPE, "horizon_id": "sc.slip-1"},
            2,
        )
        with self.assertRaisesRegex(FindingModelError, "collides"):
            findings.apply_act(state, genesis, self.registry)


class SuccessionDisplacement(HorizonFixture):
    def scenario(self) -> list[dict[str, Any]]:
        return base_acts() + [
            transition_act(
                4, assert_member("sc.m1", MEMBER_FACT_SLIP1, 100), "sc.h1", "sc.h0"
            )
        ]

    def test_closure_current_before_transition(self) -> None:
        view = compute_currency(self.project(base_acts()))
        self.assertIn("sc.closure.h0", view.current_finding_ids)

    def test_transition_displaces_predecessor_closure_via_individuation(self) -> None:
        state = self.project(self.scenario())
        view = compute_currency(state)
        self.assertIn("sc.closure.h0", view.displaced_finding_ids)
        self.assertIn("sc.m1", view.current_finding_ids)
        reasons = {reason.kind for reason in view.reasons["sc.closure.h0"]}
        self.assertEqual(reasons, {"individuation"})
        # The successor's closure question exists and is unanswered:
        # re-attestation is required before any successor closure-backed
        # result may publish (ADR-0017 decision 7).
        lattice = facts.facts_of(state.fact_state)
        self.assertIn(closure_fact("sc.h1"), lattice)
        answered = {f["fact_id"] for f in state.findings.values()}
        self.assertNotIn(closure_fact("sc.h1"), answered)

    def test_no_resurrection_after_removal(self) -> None:
        acts = self.scenario() + [
            transition_act(
                5, {"action": "remove", "fact_id": MEMBER_FACT_SLIP1}, "sc.h2", "sc.h1"
            )
        ]
        view = compute_currency(self.project(acts))
        # Supersession roots accumulate: removing the member advances the
        # horizon again; it never restores the h0 closure or the zero
        # that stood on it.
        self.assertIn("sc.closure.h0", view.displaced_finding_ids)
        self.assertIn("sc.m1", view.displaced_finding_ids)
        withdrawal = [
            reason
            for reason in view.reasons["sc.m1"]
            if reason.kind == "withdrawal"
        ]
        self.assertTrue(withdrawal)

    def test_family_isolation(self) -> None:
        other_family = {"id": "sc.family.other", "version": "v1"}
        acts = base_acts() + [
            act(
                "horizon-genesis",
                {"family": other_family, "scope": SCOPE, "horizon_id": "sc.g0"},
                4,
            ),
            act(
                "assertion",
                {"finding": finding("sc.closure.g0", closure_fact("sc.g0"), True)},
                5,
            ),
            transition_act(
                6, assert_member("sc.m1", MEMBER_FACT_SLIP1, 100), "sc.h1", "sc.h0"
            ),
        ]
        view = compute_currency(self.project(acts))
        self.assertIn("sc.closure.h0", view.displaced_finding_ids)
        self.assertIn("sc.closure.g0", view.current_finding_ids)

    def test_correction_does_not_advance_horizon_reclassification_does(self) -> None:
        acts = self.scenario() + [
            act(
                "assertion",
                {"finding": finding("sc.m1.corrected", MEMBER_FACT_SLIP1, 110)},
                5,
            ),
        ]
        state = self.project(acts)
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE), "sc.h1"
        )
        view = compute_currency(state)
        self.assertIn("sc.m1.corrected", view.current_finding_ids)
        self.assertIn("sc.m1", view.displaced_finding_ids)

        acts += [
            act(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "sc.slip-2",
                        "kind": "sc.slip",
                        "label": "Demo slip 2",
                    }
                },
                6,
            ),
            transition_act(
                7,
                {
                    "action": "reclassify",
                    "fact_id": MEMBER_FACT_SLIP1,
                    "finding": finding("sc.m2", MEMBER_FACT_SLIP2, 110),
                },
                "sc.h2",
                "sc.h1",
            ),
        ]
        state = self.project(acts)
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE), "sc.h2"
        )
        view = compute_currency(state)
        self.assertIn("sc.m2", view.current_finding_ids)
        self.assertIn("sc.m1.corrected", view.displaced_finding_ids)


class RebuildEquality(HorizonFixture):
    def test_incremental_and_full_rebuild_agree_after_every_act(self) -> None:
        acts = base_acts() + [
            transition_act(
                4, assert_member("sc.m1", MEMBER_FACT_SLIP1, 100), "sc.h1", "sc.h0"
            ),
            transition_act(
                5, {"action": "remove", "fact_id": MEMBER_FACT_SLIP1}, "sc.h2", "sc.h1"
            ),
        ]
        incremental = findings.initial_state()
        for index, one_act in enumerate(acts):
            incremental = findings.apply_act(incremental, one_act, self.registry)
            rebuilt = self.project(acts[: index + 1])
            self.assertEqual(incremental, rebuilt)
            self.assertEqual(
                compute_currency(incremental), compute_currency(rebuilt)
            )


class AtomicAdmission(HorizonFixture):
    """The Track 1 admission-negative corpus rejects atomically."""

    def corpus_state(self) -> findings.FindingState:
        """A chain matching the corpus names: h0 recorded, h1 current."""
        w2_family = {"id": "tax.us.2025.family.w2-box1", "version": "v1"}
        w2_scope = {"tax-year": "2025", "subject": "taxpayer-primary"}
        prefix = "horizon.w2-box1.taxpayer-primary.2025"
        acts = base_acts()[:2] + [
            act(
                "horizon-genesis",
                {"family": w2_family, "scope": w2_scope, "horizon_id": f"{prefix}.h0"},
                2,
            ),
            act(
                "member-transition",
                {
                    "family": w2_family,
                    "scope": w2_scope,
                    "member": assert_member("sc.m1", MEMBER_FACT_SLIP1, 100),
                    "successor": {
                        "id": f"{prefix}.h1",
                        "predecessor": f"{prefix}.h0",
                    },
                },
                3,
            ),
        ]
        return self.project(acts)

    def test_every_admission_negative_rejects_and_changes_nothing(self) -> None:
        state = self.corpus_state()
        paths = sorted(ADMISSION_NEGATIVES.glob("*.json"))
        self.assertEqual(len(paths), 4, "expected the four-instance corpus")
        for path in paths:
            negative = json.loads(path.read_text("utf-8"))
            with self.subTest(negative=path.name):
                with self.assertRaises(HorizonModelError):
                    findings.apply_act(state, negative, self.registry)
        # Pure fold: a rejected act produced no successor state, so the
        # member half and horizon half both still read exactly as before.
        self.assertEqual(state, self.corpus_state())

    def test_replaying_an_accepted_transition_is_rejected(self) -> None:
        acts = base_acts() + [
            transition_act(
                4, assert_member("sc.m1", MEMBER_FACT_SLIP1, 100), "sc.h1", "sc.h0"
            )
        ]
        state = self.project(acts)
        with self.assertRaisesRegex(HorizonModelError, "replayed successor"):
            findings.apply_act(state, acts[-1], self.registry)


class InterruptionSafety(HorizonFixture):
    def test_uncommitted_transition_tail_changes_neither_half(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = ActLog(Path(tmp), self.registry)
            revision = 0
            for one_act in base_acts():
                revision = log.append(one_act, revision)
            move = transition_act(
                4, assert_member("sc.m1", MEMBER_FACT_SLIP1, 100), "sc.h1", "sc.h0"
            )
            with log.path.open("ab") as handle:
                handle.write(json.dumps(move).encode("utf-8"))  # no newline
            contents = log.read()
            self.assertIsNotNone(contents.incomplete_tail)
            state = findings.project(contents.acts, self.registry)
            self.assertEqual(
                horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE),
                "sc.h0",
            )
            self.assertNotIn("sc.m1", state.findings)
            view = compute_currency(state)
            self.assertIn("sc.closure.h0", view.current_finding_ids)


class EdgeClosure(HorizonFixture):
    def test_declared_edge_kinds_are_still_exactly_two(self) -> None:
        # E7.2 / ADR-0017 decision 5: succession rides individuation;
        # withdrawal is a root, never a third edge kind.
        self.assertEqual(DECLARED_EDGE_KINDS, frozenset({"derivation", "individuation"}))

    def test_closure_backed_derived_finding_falls_through_derivation_edge(self) -> None:
        registry = workspace_registry()
        derived = {
            "schema": "derived-finding.v1",
            "id": "sc.derived.zero",
            "symbol": "sc.family.subtotal",
            "value": "0",
            "version": "v1",
            "pins": [
                {"role": "input", "id": "sc.closure.h0", "version": "v1"},
                {"role": "field-mapping", "id": "sc.rule.demo", "version": "v1"},
                {"role": "adoption", "id": "sc.act.adopt", "version": "v1"},
            ],
        }
        acts = base_acts() + [
            act("derived-publication", {"run_id": "sc.run.1", "finding": derived}, 4)
        ]
        kernel_view, derivation_view = workspace_currency(tuple(acts), registry)
        self.assertIn("sc.derived.zero", derivation_view.current_derived_ids)

        acts.insert(
            4,
            transition_act(
                4, assert_member("sc.m1", MEMBER_FACT_SLIP1, 100), "sc.h1", "sc.h0"
            ),
        )
        kernel_view, derivation_view = workspace_currency(tuple(acts), registry)
        self.assertIn("sc.closure.h0", kernel_view.displaced_finding_ids)
        self.assertIn("sc.derived.zero", derivation_view.displaced_derived_ids)


if __name__ == "__main__":
    unittest.main()
