"""Saved presentations on core-calculations v51 and the explanation walk.

Pattern: ``tests/test_tax_on_taxable_income_track2.py``. The goldens are the
presentation models ``live_coordinate_run`` writes; the walk uses that run's
publications and the existing explanation walker. Every case here drives
``live_coordinate_run`` directly.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import unittest

from packages.derivation.presentation_projection import project_presentation_v1
from packages.derivation.explanation import explain_legacy as explain, index_derived
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import validate_presentation_model

import tests.test_senior_and_dependent_deductions_track1 as track1
import tests.test_tax_on_taxable_income_track1 as toti
from tests.test_tax_on_taxable_income_track2 import (
    P1_GOLDEN,
    RUN_P1,
    _acts_p1,
    _assert_no_machine_path,
    _ids,
    _load_golden,
    _nodes,
    _section,
    _symbol_values,
)

ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "packages" / "sample_data" / "senior_and_dependent_deductions" / "presentation"
JOINT_GOLDEN = PRESENTATION / "joint-65-ssn.presentation-model.v1.json"
DEPENDENT_GOLDEN = PRESENTATION / "dependent-66-blind.presentation-model.v1.json"
RUN_JOINT = "demo.sdd.presentation.joint65"
RUN_DEPENDENT = "demo.sdd.presentation.dependent66blind"

LINE_12E = track1.LINE_12E
LINE_13B = track1.LINE_13B
LINE_37 = track1.LINE_37
LINE_36A = track1.LINE_36A
LINE_36B = track1.LINE_36B
LINE_35 = "tax.us.2025.schedule1a.line35-per-person-amount"
LINE_34 = "tax.us.2025.schedule1a.line34-reduction"
LINE_33 = "tax.us.2025.schedule1a.line33-magi-excess"
SENIOR_MAX = "tax.us.2025.parameter.senior-deduction-max"
SENIOR_THRESHOLD = "tax.us.2025.parameter.senior-deduction-magi-threshold"
SENIOR_RATE = "tax.us.2025.parameter.senior-deduction-reduction-rate"
STD = toti.STD
LINE4C = "tax.us.2025.dependents-worksheet.line4c"
LINE4A = "tax.us.2025.dependents-worksheet.line4a"
LINE4B = "tax.us.2025.dependents-worksheet.line4b"
LINE2 = "tax.us.2025.dependents-worksheet.line2"
LINE1Z = "tax.us.2025.wages.total-w2-box1"


def _acts_joint() -> list[dict[str, object]]:
    return track1._finish_v51(
        track1._senior_acts(
            wages=160000,
            filing_status="married_filing_jointly",
            taxpayer_over_65=True,
            spouse_over_65=True,
            taxpayer_ssn="yes",
            spouse_ssn="yes",
            parts_ii_iv="yes",
            can_be_claimed="no",
        ),
        "synthetic golden: joint, both 65+, valid SSNs, AGI $160,000",
    )


def _acts_dependent() -> list[dict[str, object]]:
    return track1._finish_v51(
        track1._senior_acts(
            wages=3000,
            filing_status="single",
            taxpayer_over_65=True,
            taxpayer_blind=True,
            taxpayer_ssn="yes",
            parts_ii_iv="yes",
            can_be_claimed="yes",
        ),
        "synthetic golden: single dependent, 66 and blind, wages $3,000",
    )


def _present(
    acts: list[dict[str, object]], run_id: str
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user="demo.user.filer-1",
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=track1.SURFACE_V51,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        if outcome.presentation_path is None or outcome.publications is None:
            raise AssertionError(f"{run_id} saved no presentation")
        model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text(encoding="utf-8")))
        pubs = {str(pub.finding["symbol"]): pub.finding for pub in outcome.publications}
        return model, pubs


def _published_numeric(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    if resolved.get("disposition") in {"published_value", "computed_zero", "closure_backed_zero"}:
        return resolved.get("value")
    return resolved


class SeniorAndDependentDeductionsPresentationTests(unittest.TestCase):
    def test_joint_65_presentation_golden(self) -> None:
        model, _pubs = _present(_acts_joint(), RUN_JOINT)
        golden = _load_golden(JOINT_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        self.assertEqual(_published_numeric(model, "line-12e"), 34700)
        self.assertEqual(_published_numeric(model, "line-13b"), 10800)
        _assert_no_machine_path(model)

    def test_dependent_66_blind_presentation_golden(self) -> None:
        model, _pubs = _present(_acts_dependent(), RUN_DEPENDENT)
        golden = _load_golden(DEPENDENT_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        self.assertEqual(_published_numeric(model, "line-12e"), 7450)
        self.assertEqual(_published_numeric(model, "line-13b"), 6000)
        _assert_no_machine_path(model)

    def test_line_13b_explanation_reaches_schedule1a_part_v(self) -> None:
        _model, pubs = _present(_acts_joint(), RUN_JOINT)
        finding = pubs[LINE_13B]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(10800))
        derived = index_derived(list(pubs.values()))
        node = explain(str(finding["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        self.assertEqual(_symbol_values(nodes, LINE_37), {Decimal(10800)})
        self.assertEqual(_symbol_values(nodes, LINE_36A), {Decimal(5400)})
        self.assertEqual(_symbol_values(nodes, LINE_36B), {Decimal(5400)})
        self.assertEqual(_symbol_values(nodes, LINE_35), {Decimal(5400)})
        self.assertEqual(_symbol_values(nodes, LINE_34), {Decimal(600)})
        self.assertEqual(_symbol_values(nodes, LINE_33), {Decimal(10000)})
        parameters = _ids(nodes, "parameter")
        self.assertIn(SENIOR_MAX, parameters)
        self.assertIn(SENIOR_THRESHOLD, parameters)
        self.assertIn(SENIOR_RATE, parameters)

    def test_line_12e_explanation_reaches_dependents_worksheet(self) -> None:
        _model, pubs = _present(_acts_dependent(), RUN_DEPENDENT)
        finding = pubs[LINE_12E]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(7450))
        derived = index_derived(list(pubs.values()))
        node = explain(str(finding["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        self.assertEqual(_symbol_values(nodes, STD), {Decimal(7450)})
        self.assertEqual(_symbol_values(nodes, LINE4C), {Decimal(7450)})
        self.assertEqual(_symbol_values(nodes, LINE4A), {Decimal(3450)})
        self.assertEqual(_symbol_values(nodes, LINE4B), {Decimal(4000)})
        self.assertEqual(_symbol_values(nodes, LINE2), {Decimal(3450)})
        self.assertEqual(_symbol_values(nodes, LINE1Z), {Decimal(3000)})

    def test_v50_presentation_still_reads_as_before(self) -> None:
        """A saved v50 presentation (committed before this milestone) still
        reads as before -- this milestone's v51 content never touches the
        v50 package or its goldens."""
        acts = _acts_p1()
        with TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope={"jurisdiction": "us", "year": "2025"},
                scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"},
                run_id=RUN_P1,
                governance_pins=[],
                surface=toti.SURFACE_V50,
                output_name="out.json",
            )
            if outcome.refusal is not None:
                raise AssertionError(f"{RUN_P1} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
            assert outcome.presentation_path is not None
            model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text(encoding="utf-8")))
        golden = _load_golden(P1_GOLDEN)
        validate_presentation_model(golden)
        self.assertEqual(project_presentation_v1(model), golden)
        self.assertEqual(_published_numeric(model, "line-12e"), 15750)


if __name__ == "__main__":
    unittest.main()
