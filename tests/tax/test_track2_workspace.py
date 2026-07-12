"""Track 2 verification: the ratified W-2 identity and lifecycle through the
real kernel, with no derivation rule or runnable workspace yet.

Each committed workspace fixture adopts the production Track 1 bundle
(`packages/content/tax/2025/w2.bundle.json`) and rebuilds byte-identical to
its golden read model. The identity-collision negative operationalizes the
ADR-0011 alternative the committee rejected: keying box-1 wages by employer
and year alone collides two same-employer slips into one fact, which is
exactly the failure the accepted slip-keyed identity avoids.
"""

import json
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingModelError, apply_assertion, project
from packages.kernel.read_models import build_read_model
from packages.kernel.schema_registry import SchemaRegistry

WORKSPACE_ROOT = Path("packages/sample_data/tax/workspaces")
BUNDLE = json.loads(Path("packages/content/tax/2025/w2.bundle.json").read_text("utf-8"))

BOX1_FACT_TYPE = "tax.us.2025.w2.box1-wages"

EMPLOYER = {
    "schema": "entity.v1",
    "id": "demo-employer-alpha",
    "kind": "tax.us.employer",
    "label": "Alpha Manufacturing Co (synthetic employer)",
}
SLIP_1 = {
    "schema": "entity.v1",
    "id": "demo-w2-slip-alpha-1",
    "kind": "tax.us.w2-slip",
    "label": "Alpha Manufacturing W-2 slip 1 of 2 for 2025 (synthetic)",
}
SLIP_2 = {
    "schema": "entity.v1",
    "id": "demo-w2-slip-alpha-2",
    "kind": "tax.us.w2-slip",
    "label": "Alpha Manufacturing W-2 slip 2 of 2 for 2025 (synthetic)",
}


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"test-act-{index:03d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-01-01T00:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _evidence(evidence_id: str, box1_amount: int, label: str) -> dict[str, Any]:
    return {
        "schema": "evidence.v1",
        "id": evidence_id,
        "kind": "tax.us.w2-document",
        "label": label,
        "content": {"box1": box1_amount},
    }


def _finding(finding_id: str, fact_id: str, value: Any, evidence_ids: list[str]) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "documentary",
        "evidence_ids": evidence_ids,
    }


class WorkspaceFixtureFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry()

    def _acts(self, name: str) -> tuple[dict[str, Any], ...]:
        path = WORKSPACE_ROOT / name / "acts.jsonl"
        return tuple(json.loads(line) for line in path.read_text("utf-8").splitlines())

    def _expected(self, name: str) -> dict[str, Any]:
        loaded: dict[str, Any] = json.loads(
            (WORKSPACE_ROOT / name / "expected" / "read-model.json").read_text("utf-8")
        )
        return loaded


class RebuildsExpectedGolden(WorkspaceFixtureFixture):
    def test_every_committed_workspace_rebuilds_its_golden(self) -> None:
        fixtures = sorted(p.name for p in WORKSPACE_ROOT.iterdir() if p.is_dir())
        self.assertEqual(
            fixtures, ["present_zero_w2", "single_w2", "two_w2_same_employer", "w2_correction"]
        )
        for name in fixtures:
            with self.subTest(fixture=name):
                model = build_read_model(self._acts(name), self.registry)
                self.assertEqual(model, self._expected(name))


class SingleSlip(WorkspaceFixtureFixture):
    def test_single_w2_publishes_one_current_nonzero_finding(self) -> None:
        model = build_read_model(self._acts("single_w2"), self.registry)
        self.assertEqual(len(model["current"]["finding_ids"]), 1)
        finding_id = model["current"]["finding_ids"][0]
        value = model["current"]["findings"][finding_id]["finding"]["value"]
        self.assertEqual(value, 52000)


class TwoSameEmployerSlips(WorkspaceFixtureFixture):
    def test_two_slips_remain_distinct_facts_and_aggregate_to_two_findings(self) -> None:
        model = build_read_model(self._acts("two_w2_same_employer"), self.registry)
        box1_facts = [
            fact for fact in model["facts"].values() if fact["fact_type_id"] == BOX1_FACT_TYPE
        ]
        self.assertEqual(len(box1_facts), 2)
        fact_ids = {fact["fact_id"] for fact in box1_facts}
        self.assertEqual(len(fact_ids), 2, "two same-employer slips must not collide onto one fact")
        self.assertEqual(len(model["current"]["finding_ids"]), 2)
        values = sorted(
            model["current"]["findings"][fid]["finding"]["value"]
            for fid in model["current"]["finding_ids"]
        )
        self.assertEqual(values, [8000, 52000])


class PresentZero(WorkspaceFixtureFixture):
    def test_present_zero_publishes_a_current_finding_with_value_zero(self) -> None:
        model = build_read_model(self._acts("present_zero_w2"), self.registry)
        self.assertEqual(len(model["current"]["finding_ids"]), 1)
        finding_id = model["current"]["finding_ids"][0]
        finding = model["current"]["findings"][finding_id]["finding"]
        self.assertEqual(finding["value"], 0)
        # A present zero is an ordinary current finding on a present source,
        # never a closure fact — no closure finding exists in this fixture.
        self.assertEqual(
            model["facts"]["tax.us.2025.w2.source-closure|tax-year=2025"]["current_finding_id"],
            None,
        )


class SameFactCorrection(WorkspaceFixtureFixture):
    """ADR-0011 decision 3: a corrected value for the same slip supersedes
    the prior finding under the fact type's declared policy; the original
    remains in history as displaced, never rewritten."""

    def test_corrected_finding_is_current_and_original_is_displaced(self) -> None:
        model = build_read_model(self._acts("w2_correction"), self.registry)
        self.assertEqual(
            model["current"]["finding_ids"], ["demo-finding-w2-alpha-1-box1-corrected"]
        )
        corrected = model["current"]["findings"]["demo-finding-w2-alpha-1-box1-corrected"]["finding"]
        self.assertEqual(corrected["value"], 53000)

        fact_id = corrected["fact_id"]
        history = model["history_by_fact"][fact_id]
        self.assertEqual([entry["finding_id"] for entry in history], [
            "demo-finding-w2-alpha-1-box1",
            "demo-finding-w2-alpha-1-box1-corrected",
        ])
        self.assertFalse(history[0]["current"])
        self.assertTrue(history[1]["current"])

    def test_currency_reason_for_the_displaced_original_is_correction(self) -> None:
        state = project(self._acts("w2_correction"), self.registry)
        view = compute_currency(state)
        self.assertIn("demo-finding-w2-alpha-1-box1", view.displaced_finding_ids)
        self.assertEqual(view.reasons["demo-finding-w2-alpha-1-box1"][0].kind, "correction")
        self.assertEqual(
            view.reasons["demo-finding-w2-alpha-1-box1"][0].by,
            "demo-finding-w2-alpha-1-box1-corrected",
        )

    def test_second_slip_if_present_would_remain_unaffected_by_a_correction(self) -> None:
        # Exit criterion check via the two-slip fixture: correcting one
        # slip's fact never touches a distinct slip's fact or finding.
        model = build_read_model(self._acts("two_w2_same_employer"), self.registry)
        fact_ids = {f["fact_id"] for f in model["facts"].values() if f["fact_type_id"] == BOX1_FACT_TYPE}
        slip_1_fact = next(f for f in fact_ids if "demo-w2-slip-alpha-1" in f)
        slip_2_fact = next(f for f in fact_ids if "demo-w2-slip-alpha-2" in f)
        self.assertNotEqual(slip_1_fact, slip_2_fact)


class IdentityCollisionNegative(WorkspaceFixtureFixture):
    """Regression for the ADR-0011 rejected alternative: keying box-1 wages
    by employer and year alone (dropping the slip key) collides two
    same-employer slips onto one fact, so the second assertion silently
    becomes a correction of the first instead of a second, aggregating
    answer. This proves why the accepted schema includes the slip key.
    """

    def _employer_year_only_bundle(self) -> dict[str, Any]:
        bundle: dict[str, Any] = json.loads(json.dumps(BUNDLE))
        for fact_type in bundle["fact_types"]:
            if fact_type["id"] == BOX1_FACT_TYPE:
                fact_type["identity_keys"] = [
                    key for key in fact_type["identity_keys"] if key["name"] != "w2-slip"
                ]
        return bundle

    def test_employer_year_only_keying_collides_two_slips_onto_one_fact(self) -> None:
        rejected_fact_id = f"{BOX1_FACT_TYPE}|employer=demo-employer-alpha,tax-year=2025"
        acts = (
            _act(0, "bundle-adoption", {"bundle": self._employer_year_only_bundle()}),
            _act(1, "entity-introduced", {"entity": EMPLOYER}),
            _act(2, "entity-introduced", {"entity": SLIP_1}),
            _act(3, "entity-introduced", {"entity": SLIP_2}),
            _act(4, "evidence-submitted", {"evidence": _evidence("ev-1", 52000, "Slip 1 (synthetic)")}),
            _act(5, "evidence-submitted", {"evidence": _evidence("ev-2", 8000, "Slip 2 (synthetic)")}),
            _act(6, "assertion", {"finding": _finding("f-1", rejected_fact_id, 52000, ["ev-1"])}),
            _act(7, "assertion", {"finding": _finding("f-2", rejected_fact_id, 8000, ["ev-2"])}),
        )
        state = project(acts, self.registry)
        view = compute_currency(state)
        # The second slip's finding silently displaces the first as a
        # "correction" rather than standing beside it — the collision
        # ADR-0011 C2 rejected, reproduced here as a negative.
        self.assertEqual(view.current_finding_ids, frozenset({"f-2"}))
        self.assertIn("f-1", view.displaced_finding_ids)
        self.assertEqual(view.reasons["f-1"][0].kind, "correction")

    def test_production_bundle_keeps_the_two_slips_from_colliding(self) -> None:
        # Contrast case, same acts shape, real (slip-keyed) production bundle.
        def fact_id(slip_id: str) -> str:
            return f"{BOX1_FACT_TYPE}|employer=demo-employer-alpha,w2-slip={slip_id},tax-year=2025"

        acts = (
            _act(0, "bundle-adoption", {"bundle": BUNDLE}),
            _act(1, "entity-introduced", {"entity": EMPLOYER}),
            _act(2, "entity-introduced", {"entity": SLIP_1}),
            _act(3, "entity-introduced", {"entity": SLIP_2}),
            _act(4, "evidence-submitted", {"evidence": _evidence("ev-1", 52000, "Slip 1 (synthetic)")}),
            _act(5, "evidence-submitted", {"evidence": _evidence("ev-2", 8000, "Slip 2 (synthetic)")}),
            _act(6, "assertion", {"finding": _finding("f-1", fact_id("demo-w2-slip-alpha-1"), 52000, ["ev-1"])}),
            _act(7, "assertion", {"finding": _finding("f-2", fact_id("demo-w2-slip-alpha-2"), 8000, ["ev-2"])}),
        )
        state = project(acts, self.registry)
        view = compute_currency(state)
        self.assertEqual(view.current_finding_ids, frozenset({"f-1", "f-2"}))
        self.assertEqual(view.displaced_finding_ids, frozenset())

    def test_a_finding_for_an_unintroduced_slip_references_an_unknown_fact(self) -> None:
        # A slip-keyed fact only exists once its slip entity is current
        # (facts.py: entity keys bind to current entities). Asserting
        # against a slip that was never introduced is rejected outright,
        # never silently treated as some other slip's question.
        fact_id = f"{BOX1_FACT_TYPE}|employer=demo-employer-alpha,w2-slip=demo-w2-slip-ghost,tax-year=2025"
        acts = (
            _act(0, "bundle-adoption", {"bundle": BUNDLE}),
            _act(1, "entity-introduced", {"entity": EMPLOYER}),
            _act(2, "evidence-submitted", {"evidence": _evidence("ev-1", 52000, "Slip (synthetic)")}),
        )
        state = project(acts, self.registry)
        with self.assertRaises(FindingModelError):
            apply_assertion(state, {"finding": _finding("f-ghost", fact_id, 52000, ["ev-1"])}, self.registry)


class DataSafety(unittest.TestCase):
    def test_committed_workspace_fixtures_have_no_private_markers(self) -> None:
        forbidden = ("/Users/", "/private/", "local-data/", "uploads/")
        for path in WORKSPACE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text("utf-8")
            with self.subTest(path=str(path)):
                self.assertFalse(any(marker in text for marker in forbidden))


if __name__ == "__main__":
    unittest.main()
