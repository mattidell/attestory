"""Track 2: saved core v50 presentations and the explanation walk.

The goldens are the presentation models ``live_coordinate_run`` writes.
The walk uses that run's publications and the existing explanation walker.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import unittest

from packages.derivation.presentation_projection import project_presentation_v1
from packages.derivation.explanation import ExplanationNode, explain_legacy as explain, index_derived
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import validate_presentation_model
from packages.derivation.records import RECORD_STREAM_FILENAME
import tests.test_tax_on_taxable_income_track1 as track1

ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "packages" / "sample_data" / "tax_on_taxable_income" / "presentation"
P1_GOLDEN = PRESENTATION / "w2-only-single.presentation-model.v1.json"
P2_GOLDEN = PRESENTATION / "qdcg-straddle.presentation-model.v1.json"
RUN_P1 = "demo.toti.presentation.p1"
RUN_P2 = "demo.toti.presentation.p2"
PACKAGE_ID = "tax.us.2025.package.core-calculations"
STD_BASE = "tax.us.2025.parameter.standard-deduction-base"

_WORKSHEET_VALUES = {
    25: Decimal(4760),
    24: Decimal(6855),
    23: Decimal(4760),
    22: Decimal(3875),
    9: Decimal(14100),
    17: Decimal(5900),
}


def _acts_p1() -> list[dict[str, object]]:
    probe = track1._probe()
    return track1._finish_v50(
        probe._base_acts(wages=track1._wages(46850), filing_status="single"),
        "synthetic p1",
    )


def _acts_p2() -> list[dict[str, object]]:
    probe = track1._probe()
    return track1._finish_v50(
        probe._base_acts(
            wages=track1._wages(54250, other=20000),
            ordinary_dividends=20000,
            qualified_dividends=20000,
        ),
        "synthetic p2",
    )


def _records(workspace: WorkspaceCapability) -> list[dict[str, Any]]:
    # live_coordinate_run writes the derivation record stream under the
    # capability root. The completion record carries the workspace revision.
    path = workspace.location / "records" / RECORD_STREAM_FILENAME
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        if isinstance(row, dict):
            rows.append(cast(dict[str, Any], row))
    return rows


def _present(
    acts: list[dict[str, object]], run_id: str
) -> tuple[str, dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Run the real coordinator and read the presentation it saved."""
    probe = track1._probe()
    with TemporaryDirectory() as tmp:
        workspace = WorkspaceCapability(Path(tmp) / "L")
        outcome = live_coordinate_run(
            workspace,
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=probe.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=track1.SURFACE_V50,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        if outcome.presentation_path is None or outcome.publications is None:
            raise AssertionError(f"{run_id} saved no presentation")
        raw = outcome.presentation_path.read_text(encoding="utf-8")
        model = cast(dict[str, Any], json.loads(raw))
        pubs = {str(pub.finding["symbol"]): pub.finding for pub in outcome.publications}
        return raw, model, pubs, _records(workspace)


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next(section for section in model["sections"] if section["id"] == section_id)


def _published_numeric(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    if resolved.get("disposition") in {"published_value", "computed_zero", "closure_backed_zero"}:
        return resolved.get("value")
    return resolved


def _line16_finding(model: dict[str, Any]) -> dict[str, Any]:
    act = _section(model, "line-16")["resolved"]["act"]
    if not isinstance(act, dict):
        raise AssertionError("line 16 has no saved finding")
    finding = act["finding"]
    if not isinstance(finding, dict):
        raise AssertionError("line 16 has no saved finding")
    return finding


def _load_golden(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AssertionError(f"committed presentation golden required at {path}")
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _nodes(root: ExplanationNode) -> list[ExplanationNode]:
    pending = [root]
    found: list[ExplanationNode] = []
    while pending:
        node = pending.pop()
        found.append(node)
        pending.extend(node.children)
    return found


def _symbol_values(nodes: list[ExplanationNode], symbol: str) -> set[Decimal]:
    return {Decimal(str(node.value)) for node in nodes if node.symbol == symbol}


def _ids(nodes: list[ExplanationNode], kind: str) -> set[str]:
    return {node.finding_id for node in nodes if node.kind == kind}


def _assert_no_machine_path(model: dict[str, Any]) -> None:
    text = json.dumps(model)
    for needle in ("/" + "Users", "/" + "private"):
        if needle in text:
            raise AssertionError("presentation contains a machine path")


class TaxOnTaxableIncomeTrack2Tests(unittest.TestCase):
    def test_p1_presentation_golden_structural_equality(self) -> None:
        _raw, model, _pubs, _records_out = _present(_acts_p1(), RUN_P1)
        golden = _load_golden(P1_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        self.assertEqual(_published_numeric(model, "line-15"), 46850)
        self.assertEqual(_published_numeric(model, "line-16"), 5387)
        self.assertEqual(_published_numeric(model, "line-12e"), 15750)
        section = _section(model, "line-16")
        self.assertTrue(section.get("citationSites") or model.get("citationGroups"))
        _assert_no_machine_path(model)

    def test_p2_presentation_golden_structural_equality(self) -> None:
        _raw, model, _pubs, _records_out = _present(_acts_p2(), RUN_P2)
        golden = _load_golden(P2_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        self.assertEqual(_published_numeric(model, "line-16"), 4760)
        section = _section(model, "line-16")
        self.assertTrue(section.get("citationSites") or model.get("citationGroups"))
        _assert_no_machine_path(model)

    def test_p3_line16_explanation_reaches_worksheet(self) -> None:
        _raw, model, pubs, _records_out = _present(_acts_p2(), RUN_P2)
        saved = _line16_finding(model)
        self.assertEqual(saved["id"], pubs[track1.TOTAL]["id"])
        self.assertEqual(Decimal(str(saved["value"])), Decimal(4760))
        derived = index_derived(list(pubs.values()))
        node = explain(str(saved["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        for number, expected in _WORKSHEET_VALUES.items():
            self.assertEqual(_symbol_values(nodes, track1._line(number)), {expected}, number)
        parameters = _ids(nodes, "parameter")
        self.assertIn(track1.ORD, parameters)
        self.assertIn(track1.ZERO_CEILING, parameters)
        self.assertIn(track1.FIFTEEN_CEILING, parameters)
        self.assertEqual([item for item in parameters if item.startswith("demo.")], [])

    def test_p4_standard_deduction_explanation_reaches_base_and_citation(self) -> None:
        _raw, model, pubs, _records_out = _present(_acts_p1(), RUN_P1)
        self.assertEqual(_published_numeric(model, "line-12e"), 15750)
        derived = index_derived(list(pubs.values()))
        node = explain(str(pubs[track1.STD]["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        self.assertEqual(_symbol_values(nodes, track1.STD), {Decimal(15750)})
        self.assertIn(STD_BASE, _ids(nodes, "parameter"))
        self.assertIn(track1.LINE12_CITE, _ids(nodes, "citation"))
        self.assertEqual([item for item in _ids(nodes, "parameter") if item.startswith("demo.")], [])

    def test_p5_fresh_reload_reproduces_p1(self) -> None:
        acts = _acts_p1()
        _raw, model, _pubs, records = _present(acts, RUN_P1)
        reloaded = _load_golden(P1_GOLDEN)
        validate_presentation_model(reloaded)
        self.assertEqual(reloaded, project_presentation_v1(model))
        self.assertEqual(reloaded["runId"], RUN_P1)
        completed = [
            row for row in records if row.get("run_id") == RUN_P1 and row.get("phase") == "completed"
        ]
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0]["workspace_revision"], len(acts))
        self.assertEqual(reloaded["runId"], completed[0]["run_id"])
        adoption = [
            pin for pin in _line16_finding(reloaded)["pins"] if pin.get("role") == "adoption"
        ]
        self.assertEqual(adoption, [{"role": "adoption", "id": PACKAGE_ID, "version": "v50"}])
