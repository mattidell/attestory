"""Track 3 deliverable 4: the bidirectional admission-locus contradiction
interlock (ADR-0038 decision 5) between a current "no"
capital-gain-distributions declaration and the CAPITAL_GAIN_DISTRIBUTION_
RECORDED signal (a contributed 1099-DIV box 2a, ADR-0035).

These are kernel/admission-level tests, not coordinator goldens - the
charter (docs/reviews/charter-2026-07-19-dsbs-t3-qdcg-line16.md, deliverable
4) names them as tests that "may be admission-level tests rather than
coordinator goldens where the defect is not fact-log-observable, but must be
executed, not asserted by comment." The mechanism
(``registry.declaration_signal_contradictions``, enforced generically in
``packages.kernel.findings``) is exercised through ordinary
``project()``/``apply_contribution_batch`` calls against the real committed
``tax.us.2025.capital-gain-distributions`` and
``tax.us.2025.f1099div.recorded-boxes`` fact types - the same admission
surface the live coordinator's ``project()`` call uses, and the same
mechanism shape Track 2's box 1b <= 1a subset invariant already established
(``tests/tax/test_dsbs_t2_dividend_admission.py``).

Kill-tested in all three orders named by the charter: declaration-first
(the signal contribution rejects), signal-first (the declaration
contribution rejects), and same-batch (ADR-0032 terminal batch semantics -
the batch fails closed regardless of which finding within it is admitted
first).
"""

from __future__ import annotations

import json
import unittest
from typing import Any

from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

CG_DIST = "tax.us.2025.capital-gain-distributions"
RECORDED_BOXES = "tax.us.2025.f1099div.recorded-boxes"
PAYER = "demo.dsbs.t3.payer.alpha"
STATEMENT = "demo.dsbs.t3.stmt.alpha-1"
DECLARATION_FACT_ID = f"{CG_DIST}|tax-year=2025"
RECORDED_BOXES_FACT_ID = f"{RECORDED_BOXES}|payer={PAYER},statement={STATEMENT},tax-year=2025"


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


def _all_boxes_absent(box_2a: float | None) -> dict[str, float | None]:
    return {"2a": box_2a, "3": None, "5": None, "7": None, "12": None}


def _recorded_boxes_act(index: int, finding_id: str, box_2a: float | None, **extra: Any) -> dict[str, Any]:
    value = _all_boxes_absent(box_2a)
    return _act(index, "assertion", {"finding": _finding(finding_id, RECORDED_BOXES_FACT_ID, value, **extra)})


class InterlockFixture(unittest.TestCase):
    """Base acts: both committed bundles adopted, one payer/statement pair
    introduced. Every test extends this tuple."""

    def setUp(self) -> None:
        self.registry = tax_registry()
        qdcg_bundle = json.loads((TAX_CONTENT_DIR / "qdcg.bundle.json").read_text("utf-8"))
        div_bundle = json.loads((TAX_CONTENT_DIR / "f1099div.bundle.json").read_text("utf-8"))
        self.base: tuple[dict[str, Any], ...] = (
            _act(0, "bundle-adoption", {"bundle": qdcg_bundle}),
            _act(1, "bundle-adoption", {"bundle": div_bundle}),
            _act(2, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": PAYER, "kind": "tax.us.dividend-payer", "label": "Demo payer",
            }}),
            _act(3, "entity-introduced", {"entity": {
                "schema": "entity.v1", "id": STATEMENT, "kind": "tax.us.1099div-statement", "label": "Demo statement",
            }}),
        )
        # sanity: the base acts alone admit cleanly.
        project(self.base, self.registry)


class DeclarationFirstOrder(InterlockFixture):
    def test_signal_contribution_after_a_current_no_declaration_rejects(self) -> None:
        decl = _declaration_act(4, "demo.dsbs.t3.finding.decl", "no")
        state_after_decl = project((*self.base, decl), self.registry)
        self.assertIn("demo.dsbs.t3.finding.decl", state_after_decl.findings)

        signal = _recorded_boxes_act(5, "demo.dsbs.t3.finding.recorded", 125.5)
        with self.assertRaisesRegex(FindingModelError, "contradiction"):
            project((*self.base, decl, signal), self.registry)

    def test_a_declared_yes_never_contradicts_the_signal(self) -> None:
        decl = _declaration_act(4, "demo.dsbs.t3.finding.decl", "yes")
        signal = _recorded_boxes_act(5, "demo.dsbs.t3.finding.recorded", 125.5)
        state = project((*self.base, decl, signal), self.registry)
        self.assertIn("demo.dsbs.t3.finding.decl", state.findings)
        self.assertIn("demo.dsbs.t3.finding.recorded", state.findings)

    def test_all_boxes_absent_never_contradicts_a_no_declaration(self) -> None:
        decl = _declaration_act(4, "demo.dsbs.t3.finding.decl", "no")
        signal = _recorded_boxes_act(5, "demo.dsbs.t3.finding.recorded", None)
        state = project((*self.base, decl, signal), self.registry)
        self.assertIn("demo.dsbs.t3.finding.decl", state.findings)
        self.assertIn("demo.dsbs.t3.finding.recorded", state.findings)


class SignalFirstOrder(InterlockFixture):
    def test_declaration_contribution_after_a_current_signal_rejects(self) -> None:
        signal = _recorded_boxes_act(4, "demo.dsbs.t3.finding.recorded", 125.5)
        state_after_signal = project((*self.base, signal), self.registry)
        self.assertIn("demo.dsbs.t3.finding.recorded", state_after_signal.findings)

        decl = _declaration_act(5, "demo.dsbs.t3.finding.decl", "no")
        with self.assertRaisesRegex(FindingModelError, "contradiction"):
            project((*self.base, signal, decl), self.registry)


class ViolatingPairNeverRecorded(InterlockFixture):
    def test_the_rejecting_runs_second_finding_never_lands_in_a_fresh_projection(self) -> None:
        decl = _declaration_act(4, "demo.dsbs.t3.finding.decl", "no")
        signal = _recorded_boxes_act(5, "demo.dsbs.t3.finding.recorded", 125.5)
        with self.assertRaises(FindingModelError):
            project((*self.base, decl, signal), self.registry)
        clean = project((*self.base, decl), self.registry)
        self.assertNotIn("demo.dsbs.t3.finding.recorded", clean.findings)


class SameBatchOrdering(InterlockFixture):
    """ADR-0032 terminal batch semantics: the pair cannot be sequenced
    around when both the declaration and the signal arrive in one
    contribution batch."""

    def _batch_state(self) -> Any:
        evidence_act = _act(4, "evidence-submitted", {"evidence": {
            "schema": "evidence.v1", "id": "demo.dsbs.t3.evidence", "kind": "demo.statement",
            "label": "Demo interlock evidence", "content": {"synthetic": True},
        }})
        return project((*self.base, evidence_act), self.registry)

    def _contribution_act(self, index: int, contribution_id: str) -> dict[str, Any]:
        return _act(index, "contribution", {"contribution": {
            "schema": "contribution.v1", "id": contribution_id,
            "evidence_id": "demo.dsbs.t3.evidence", "content": {"mode": "manual-entry", "synthetic": True},
        }})

    def test_declaration_then_signal_in_one_batch_fails_closed(self) -> None:
        state = self._batch_state()
        contribution_id = "demo.dsbs.t3.contribution"
        contribution_act = self._contribution_act(5, contribution_id)
        decl = _declaration_act(6, "f.decl", "no", contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"])
        signal = _recorded_boxes_act(7, "f.recorded", 125.5, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"])
        with self.assertRaisesRegex(ContributionError, "contradiction"):
            apply_contribution_batch(
                state, contribution_act=contribution_act, successor_acts=[decl, signal],
                registry=self.registry, record_id="demo.dsbs.t3.record",
            )

    def test_signal_then_declaration_in_one_batch_fails_closed(self) -> None:
        state = self._batch_state()
        contribution_id = "demo.dsbs.t3.contribution"
        contribution_act = self._contribution_act(5, contribution_id)
        signal = _recorded_boxes_act(6, "f.recorded", 125.5, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"])
        decl = _declaration_act(7, "f.decl", "no", contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"])
        with self.assertRaisesRegex(ContributionError, "contradiction"):
            apply_contribution_batch(
                state, contribution_act=contribution_act, successor_acts=[signal, decl],
                registry=self.registry, record_id="demo.dsbs.t3.record",
            )

    def test_conforming_pair_in_one_batch_completes(self) -> None:
        """Not a blanket same-batch rejection - a "yes" declaration
        alongside a recorded box 2a completes normally in one batch."""
        state = self._batch_state()
        contribution_id = "demo.dsbs.t3.contribution"
        contribution_act = self._contribution_act(5, contribution_id)
        decl = _declaration_act(6, "f.decl", "yes", contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"])
        signal = _recorded_boxes_act(7, "f.recorded", 125.5, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t3.evidence"])
        result = apply_contribution_batch(
            state, contribution_act=contribution_act, successor_acts=[decl, signal],
            registry=self.registry, record_id="demo.dsbs.t3.record",
        )
        self.assertEqual(result.terminal_record["phase"], "completed")
        self.assertIn("f.decl", result.state.findings)
        self.assertIn("f.recorded", result.state.findings)


if __name__ == "__main__":
    unittest.main()
