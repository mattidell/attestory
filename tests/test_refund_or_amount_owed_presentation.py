"""Saved presentations on core-calculations v52 and the explanation walk.

Pattern: ``tests/test_senior_and_dependent_deductions_presentation.py``.
The goldens are the presentation models ``live_coordinate_run`` writes;
the walk uses that run's publications and the existing explanation walker.
Every case here drives ``live_coordinate_run`` directly.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import unittest

from packages.derivation.explanation import explain, index_derived
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import validate_presentation_model

import tests.test_refund_or_amount_owed_track1 as t1
import tests.test_refund_or_amount_owed_track2 as t2

ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "packages" / "sample_data" / "refund_or_amount_owed" / "presentation"
REFUND_GOLDEN = PRESENTATION / "refund-w2-int-withholding-estimated.presentation-model.v1.json"
OWED_GOLDEN = PRESENTATION / "amount-owed-w2-only.presentation-model.v1.json"
RUN_REFUND = "demo.roao.presentation.refund"
RUN_OWED = "demo.roao.presentation.owed"

LINE24 = "tax.us.2025.tax.line24-total-tax"
LINE25A = "tax.us.2025.payments.line25a"
LINE25B = "tax.us.2025.payments.line25b"
LINE25D = "tax.us.2025.payments.line25d"
LINE26 = "tax.us.2025.payments.line26"
LINE33 = "tax.us.2025.payments.line33"
LINE34 = "tax.us.2025.payments.line34-overpaid"
LINE35A = "tax.us.2025.payments.line35a-refunded"
LINE37 = "tax.us.2025.payments.line37-amount-owed"
INT_B4_SUBTOTAL = "tax.us.2025.interest.b4-withholding-subtotal"


def _acts_refund() -> list[dict[str, object]]:
    acts = t1._income_acts(wages=50000.0)
    acts, payer, stmt = t2._reopen_interest_with_real_box1(acts, amount=500.0)
    acts = t2._add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=4500.0)
    t1._close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.roao.pres.w2box2")

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(t1._act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": t1._load("f1099int-box4.bundle.json")})
    add("assertion", {"finding": t1._attested("demo.roao.pres.int.box4", f"tax.us.2025.f1099int.box4-withholding|payer={payer},statement={stmt},tax-year=2025", 100.0)})
    t1._close_empty(acts, family="tax.us.2025.f1099int.b4", version="v1", closure_fact="tax.us.2025.f1099int.b4.source-closure", horizon="demo.roao.pres.intb4")
    t1._close_other_box4_families(acts, skip={"w2-box2", "f1099int-b4"})
    acts = t2._add_bottom_line_answers(acts, estimated=300.0, applied_2026=0.0)
    return t1._finish_v52(acts, "golden: refund from W-2 plus 1099-INT withholding plus estimated payments")


def _acts_owed() -> list[dict[str, object]]:
    acts = t1._income_acts(wages=50000.0)
    acts = t2._add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=1000.0)
    t1._close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.roao.pres.owed.w2box2")
    t1._close_other_box4_families(acts, skip={"w2-box2"})
    acts = t2._add_bottom_line_answers(acts, applied_2026=None)
    return t1._finish_v52(acts, "golden: amount owed, W-2 only")


def _present(
    acts: list[dict[str, object]], run_id: str, surface: Any
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
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        if outcome.presentation_path is None or outcome.publications is None:
            raise AssertionError(f"{run_id} saved no presentation")
        model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text(encoding="utf-8")))
        pubs = {str(pub.finding["symbol"]): pub.finding for pub in outcome.publications}
        return model, pubs


def _present_v52(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    return _present(acts, run_id, t1.SURFACE_V52)


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next(section for section in model["sections"] if section["id"] == section_id)


def _published_numeric(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    if resolved.get("disposition") in {"published_value", "computed_zero", "closure_backed_zero"}:
        return resolved.get("value")
    return resolved


def _load_golden(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AssertionError(f"committed presentation golden required at {path}")
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _nodes(root: Any) -> list[Any]:
    pending = [root]
    found: list[Any] = []
    while pending:
        node = pending.pop()
        found.append(node)
        pending.extend(node.children)
    return found


def _symbol_values(nodes: list[Any], symbol: str) -> set[Decimal]:
    return {Decimal(str(node.value)) for node in nodes if node.symbol == symbol}


def _assert_no_machine_path(model: dict[str, Any]) -> None:
    text = json.dumps(model)
    for needle in ("/" + "Users", "/" + "private"):
        if needle in text:
            raise AssertionError("presentation contains a machine path")


class RefundOrAmountOwedPresentationTests(unittest.TestCase):
    def test_refund_presentation_golden(self) -> None:
        model, _pubs = _present_v52(_acts_refund(), RUN_REFUND)
        golden = _load_golden(REFUND_GOLDEN)
        self.assertEqual(model, golden)
        # Hand-checked from the sources (P0 Sec. 1; Track 2 contract):
        # AGI $50,500 (wages $50,000 + taxable interest $500), taxable
        # income $34,750, tax $3,935 (table).
        self.assertEqual(_published_numeric(model, "line-24"), 3935)
        self.assertEqual(_published_numeric(model, "line-25a"), 4500)
        self.assertEqual(_published_numeric(model, "line-25b"), 100)
        self.assertEqual(_published_numeric(model, "line-25d"), 4600)
        self.assertEqual(_published_numeric(model, "line-26"), 300)
        self.assertEqual(_published_numeric(model, "line-33"), 4900)
        self.assertEqual(_published_numeric(model, "line-34"), 965)
        self.assertEqual(_published_numeric(model, "line-37"), 0)
        _assert_no_machine_path(model)

    def test_amount_owed_presentation_golden(self) -> None:
        model, _pubs = _present_v52(_acts_owed(), RUN_OWED)
        golden = _load_golden(OWED_GOLDEN)
        self.assertEqual(model, golden)
        # Hand-checked: wages $50,000 only, tax $3,875 (table), withholding
        # $1,000 < tax, no estimated payments.
        self.assertEqual(_published_numeric(model, "line-24"), 3875)
        self.assertEqual(_published_numeric(model, "line-25a"), 1000)
        self.assertEqual(_published_numeric(model, "line-25b"), 0)
        self.assertEqual(_published_numeric(model, "line-25d"), 1000)
        self.assertEqual(_published_numeric(model, "line-26"), 0)
        self.assertEqual(_published_numeric(model, "line-33"), 1000)
        self.assertEqual(_published_numeric(model, "line-34"), 0)
        self.assertEqual(_published_numeric(model, "line-37"), 2875)
        _assert_no_machine_path(model)

    def test_line34_explanation_reaches_each_withholding_statement_and_line26(self) -> None:
        _model, pubs = _present_v52(_acts_refund(), RUN_REFUND)
        finding = pubs[LINE34]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(965))
        derived = index_derived(list(pubs.values()))
        node = explain(str(finding["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        self.assertEqual(_symbol_values(nodes, LINE33), {Decimal(4900)})
        self.assertEqual(_symbol_values(nodes, LINE24), {Decimal(3935)})
        self.assertEqual(_symbol_values(nodes, LINE25D), {Decimal(4600)})
        self.assertEqual(_symbol_values(nodes, LINE25A), {Decimal(4500)})
        self.assertEqual(_symbol_values(nodes, LINE25B), {Decimal(100)})
        self.assertEqual(_symbol_values(nodes, INT_B4_SUBTOTAL), {Decimal(100)})
        self.assertEqual(_symbol_values(nodes, LINE26), {Decimal(300)})

    def test_line37_explanation_reaches_the_w2_box2_statement(self) -> None:
        _model, pubs = _present_v52(_acts_owed(), RUN_OWED)
        finding = pubs[LINE37]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(2875))
        derived = index_derived(list(pubs.values()))
        node = explain(str(finding["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        self.assertEqual(_symbol_values(nodes, LINE24), {Decimal(3875)})
        self.assertEqual(_symbol_values(nodes, LINE33), {Decimal(1000)})
        self.assertEqual(_symbol_values(nodes, LINE25A), {Decimal(1000)})
        self.assertEqual(_symbol_values(nodes, LINE26), {Decimal(0)})

    def test_v51_presentation_still_reads_as_before(self) -> None:
        """A saved v51 presentation (committed before this milestone) still
        reads as before -- this milestone's v52 content never touches the
        v51 package or its goldens."""
        import tests.test_senior_and_dependent_deductions_track1 as sdd_track1
        import tests.test_senior_and_dependent_deductions_presentation as sdd_presentation

        model, _pubs = _present(sdd_presentation._acts_joint(), sdd_presentation.RUN_JOINT, sdd_track1.SURFACE_V51)
        golden = _load_golden(sdd_presentation.JOINT_GOLDEN)
        validate_presentation_model(golden)
        self.assertEqual(model, golden)
        self.assertEqual(_published_numeric(model, "line-13b"), 10800)


if __name__ == "__main__":
    unittest.main()
