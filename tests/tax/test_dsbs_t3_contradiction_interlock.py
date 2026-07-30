"""Track 3 deliverable 4 / ADR-0050 Track 2 re-home: bidirectional admission-locus
contradiction interlock between a current "no" capital-gain-distributions
declaration and the CAPITAL_GAIN_DISTRIBUTION_RECORDED signal.

Track 2 re-homes the signal from historical recorded-boxes field "2a" to a
current non-null successor box-2a family member
(tax.us.2025.f1099div.box2a-capital-gain-distribution). Residual historical
recorded content must not masquerade as the signal.
"""

from __future__ import annotations

import json
import unittest
from typing import Any

from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

CG_DIST = "tax.us.2025.capital-gain-distributions"
BOX2A = "tax.us.2025.f1099div.box2a-capital-gain-distribution"
RECORDED_BOXES_V1 = "tax.us.2025.f1099div.recorded-boxes"
PAYER = "demo.dsbs.t3.payer.alpha"
STATEMENT = "demo.dsbs.t3.stmt.alpha-1"
DECLARATION_FACT_ID = f"{CG_DIST}|tax-year=2025"
BOX2A_FACT_ID = f"{BOX2A}|payer={PAYER},statement={STATEMENT},tax-year=2025"
RECORDED_BOXES_FACT_ID = f"{RECORDED_BOXES_V1}|payer={PAYER},statement={STATEMENT},tax-year=2025"
FAMILY_2A = {"id": "tax.us.2025.f1099div.2a", "version": "v1"}
SCOPE = {"tax-year": "2025"}
H0 = "demo.dsbs.t3.box2a.h0"
H1 = "demo.dsbs.t3.box2a.h1"


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.dsbs.t3.act.{index:03d}",
        "kind": kind,
        "actor": "demo.dsbs.t3.user",
        "at": f"2026-07-20T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _finding(finding_id: str, fact_id: str, value: Any, **extra: Any) -> dict[str, Any]:
    finding: dict[str, Any] = {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }
    finding.update(extra)
    return finding


def _declaration_act(index: int, finding_id: str, value: str, **extra: Any) -> dict[str, Any]:
    return _act(index, "assertion", {"finding": _finding(finding_id, DECLARATION_FACT_ID, value, **extra)})


def _box2a_member_act(index: int, finding_id: str, amount: float, *, predecessor: str, successor: str, **extra: Any) -> dict[str, Any]:
    finding = _finding(finding_id, BOX2A_FACT_ID, amount, **extra)
    return _act(index, "member-transition", {
        "family": FAMILY_2A,
        "scope": SCOPE,
        "member": {"action": "assert", "finding": finding},
        "successor": {"id": successor, "predecessor": predecessor},
    })


class InterlockFixture(unittest.TestCase):
    """Base acts: qdcg + box2a vocabulary, family horizon, payer/statement."""

    def setUp(self) -> None:
        self.registry = tax_registry()
        qdcg_bundle = json.loads((TAX_CONTENT_DIR / "qdcg.bundle.json").read_text("utf-8"))
        box2a_bundle = json.loads((TAX_CONTENT_DIR / "f1099div-box2a.bundle.json").read_text("utf-8"))
        family = json.loads((TAX_CONTENT_DIR / "family.f1099div-2a.json").read_text("utf-8"))
        self.base: tuple[dict[str, Any], ...] = (
            _act(0, "bundle-adoption", {"bundle": qdcg_bundle}),
            _act(1, "bundle-adoption", {"bundle": box2a_bundle}),
            _act(2, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": PAYER, "kind": "tax.us.dividend-payer", "label": "Demo payer",
            }}),
            _act(3, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": STATEMENT, "kind": "tax.us.1099div-statement", "label": "Demo statement",
            }}),
            _act(4, "horizon-genesis", {
                "family": FAMILY_2A,
                "scope": SCOPE,
                "horizon_id": H0,
            }),
        )
        # family citizen is loaded via tax_registry family_member_predicates
        project(self.base, self.registry)


class DeclarationFirstOrder(InterlockFixture):
    def test_signal_contribution_after_a_current_no_declaration_rejects(self) -> None:
        decl = _declaration_act(5, "demo.dsbs.t3.finding.decl", "no")
        state_after_decl = project((*self.base, decl), self.registry)
        self.assertIn("demo.dsbs.t3.finding.decl", state_after_decl.findings)

        signal = _box2a_member_act(6, "demo.dsbs.t3.finding.box2a", 125.5, predecessor=H0, successor=H1)
        with self.assertRaisesRegex(FindingModelError, "contradiction"):
            project((*self.base, decl, signal), self.registry)

    def test_a_declared_yes_never_contradicts_the_signal(self) -> None:
        decl = _declaration_act(5, "demo.dsbs.t3.finding.decl", "yes")
        signal = _box2a_member_act(6, "demo.dsbs.t3.finding.box2a", 125.5, predecessor=H0, successor=H1)
        state = project((*self.base, decl, signal), self.registry)
        self.assertIn("demo.dsbs.t3.finding.decl", state.findings)
        self.assertIn("demo.dsbs.t3.finding.box2a", state.findings)


class SignalFirstOrder(InterlockFixture):
    def test_declaration_contribution_after_a_current_signal_rejects(self) -> None:
        signal = _box2a_member_act(5, "demo.dsbs.t3.finding.box2a", 125.5, predecessor=H0, successor=H1)
        state_after_signal = project((*self.base, signal), self.registry)
        self.assertIn("demo.dsbs.t3.finding.box2a", state_after_signal.findings)

        decl = _declaration_act(6, "demo.dsbs.t3.finding.decl", "no")
        with self.assertRaisesRegex(FindingModelError, "contradiction"):
            project((*self.base, signal, decl), self.registry)


class HistoricalResidualDoesNotSignal(InterlockFixture):
    def test_historical_recorded_boxes_with_2a_does_not_raise_successor_signal(self) -> None:
        """Null/residual historical content may not masquerade as the signal."""
        hist_bundle = json.loads((TAX_CONTENT_DIR / "f1099div.bundle.json").read_text("utf-8"))
        base = (
            *self.base[:1],
            _act(1, "bundle-adoption", {"bundle": hist_bundle}),
            *self.base[2:],
        )
        decl = _declaration_act(5, "demo.dsbs.t3.finding.decl", "no")
        residual = _act(6, "assertion", {"finding": _finding(
            "demo.dsbs.t3.finding.recorded",
            RECORDED_BOXES_FACT_ID,
            {"2a": 125.5, "3": None, "5": None, "7": None, "12": None},
        )})
        # Must admit: historical residual is not the successor signal feed.
        state = project((*base, decl, residual), self.registry)
        self.assertIn("demo.dsbs.t3.finding.decl", state.findings)
        self.assertIn("demo.dsbs.t3.finding.recorded", state.findings)


class ViolatingPairNeverRecorded(InterlockFixture):
    def test_the_rejecting_runs_second_finding_never_lands_in_a_fresh_projection(self) -> None:
        decl = _declaration_act(5, "demo.dsbs.t3.finding.decl", "no")
        signal = _box2a_member_act(6, "demo.dsbs.t3.finding.box2a", 125.5, predecessor=H0, successor=H1)
        with self.assertRaises(FindingModelError):
            project((*self.base, decl, signal), self.registry)
        clean = project((*self.base, decl), self.registry)
        self.assertNotIn("demo.dsbs.t3.finding.box2a", clean.findings)


class SameBatchOrdering(InterlockFixture):
    def _batch_state(self) -> Any:
        evidence_act = _act(5, "evidence-submitted", {"evidence": {
            "schema": "evidence.v1", "id": "demo.dsbs.t3.evidence", "kind": "demo.statement",
            "label": "Demo interlock evidence", "content": {"synthetic": True},
        }})
        return project((*self.base, evidence_act), self.registry)

    def _contribution_act(self, index: int, contribution_id: str) -> dict[str, Any]:
        return _act(index, "contribution", {"contribution": {
            "schema": "contribution.v1", "id": contribution_id,
            "evidence_id": "demo.dsbs.t3.evidence", "content": {"mode": "manual-entry", "synthetic": True},
        }})

    def _box2a_batch_signal(
        self, index: int, finding_id: str, amount: float, *, contribution_id: str
    ) -> dict[str, Any]:
        return _box2a_member_act(
            index,
            finding_id,
            amount,
            predecessor=H0,
            successor=H1,
            contribution_id=contribution_id,
            evidence_ids=["demo.dsbs.t3.evidence"],
        )

    def test_declaration_then_signal_in_one_batch_fails_closed(self) -> None:
        state = self._batch_state()
        contribution_id = "demo.dsbs.t3.contribution"
        contribution_act = self._contribution_act(6, contribution_id)
        decl = _declaration_act(
            7, "f.decl", "no", contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"]
        )
        signal = self._box2a_batch_signal(8, "f.box2a", 125.5, contribution_id=contribution_id)
        with self.assertRaisesRegex(ContributionError, "contradiction"):
            apply_contribution_batch(
                state, contribution_act=contribution_act, successor_acts=[decl, signal],
                registry=self.registry, record_id="demo.dsbs.t3.record",
            )

    def test_signal_then_declaration_in_one_batch_fails_closed(self) -> None:
        state = self._batch_state()
        contribution_id = "demo.dsbs.t3.contribution"
        contribution_act = self._contribution_act(6, contribution_id)
        signal = self._box2a_batch_signal(7, "f.box2a", 125.5, contribution_id=contribution_id)
        decl = _declaration_act(
            8, "f.decl", "no", contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"]
        )
        with self.assertRaisesRegex(ContributionError, "contradiction"):
            apply_contribution_batch(
                state, contribution_act=contribution_act, successor_acts=[signal, decl],
                registry=self.registry, record_id="demo.dsbs.t3.record",
            )

    def test_conforming_pair_in_one_batch_completes(self) -> None:
        state = self._batch_state()
        contribution_id = "demo.dsbs.t3.contribution"
        contribution_act = self._contribution_act(6, contribution_id)
        decl = _declaration_act(
            7, "f.decl", "yes", contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"]
        )
        signal = self._box2a_batch_signal(8, "f.box2a", 125.5, contribution_id=contribution_id)
        result = apply_contribution_batch(
            state, contribution_act=contribution_act, successor_acts=[decl, signal],
            registry=self.registry, record_id="demo.dsbs.t3.record",
        )
        self.assertEqual(result.terminal_record["phase"], "completed")
        self.assertIn("f.decl", result.state.findings)
        self.assertIn("f.box2a", result.state.findings)


if __name__ == "__main__":
    unittest.main()
