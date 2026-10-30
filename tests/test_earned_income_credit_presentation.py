"""Saved presentations of the no-child earned income credit on core v53.

Pattern: ``tests/test_refund_or_amount_owed_presentation.py``. The goldens
are the presentation models ``live_coordinate_run`` writes. The walk uses
that run's publications and the existing explanation walker.
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
from packages.derivation.production_resolver import PublicationSurface

from tests.test_earned_income_credit_track1 import (
    PASSING,
    SURFACE_V53,
    _finish_v53,
    _with_answers,
)
from tests.test_refund_or_amount_owed_presentation import REFUND_GOLDEN, RUN_REFUND, _acts_refund
from tests.test_refund_or_amount_owed_track1 import (
    ROOT,
    SURFACE_V52,
    USER,
    _act,
    _attested,
    _close_empty,
    _close_other_box4_families,
    _sdd,
)
from tests.test_refund_or_amount_owed_track2 import (
    _add_bottom_line_answers,
    _add_box2_only,
    _reopen_interest_with_real_box1,
    _reopen_w2_with_second_slip,
)

PRESENTATION = ROOT / "packages" / "sample_data" / "earned_income_credit" / "presentation"
SINGLE_GOLDEN = PRESENTATION / "single-phaseout-interest.presentation-model.v1.json"
JOINT_GOLDEN = PRESENTATION / "joint-plateau-two-w2.presentation-model.v1.json"
RUN_SINGLE = "demo.eic.presentation.single-phaseout"
RUN_JOINT = "demo.eic.presentation.joint-plateau"

LINE27A = "tax.us.2025.payments.line27a"
LINE2 = "tax.us.2025.eic.worksheet-a.line-2"
LINE6 = "tax.us.2025.eic.worksheet-a.line-6"
TABLE = "tax.us.2025.parameter.eic-table-2025"
WAGES = "tax.us.2025.wages.total-w2-box1"
AGI = "tax.us.2025.income.agi"
INVESTMENT = "tax.us.2025.eic.investment-income"
# Answers the line 27a value chain reads on a credit path. Spouse is read
# by the gate even on a single return. The unsupported-situations answer
# is read in the taken branch, so a later no displaces this line.
REACHED_ANSWERS = (
    "tax.us.2025.eic.answer.no-qualifying-child",
    "tax.us.2025.eic.answer.no-unsupported-situations",
    "tax.us.2025.eic.answer.taxpayer-valid-ssn",
    "tax.us.2025.eic.answer.spouse-valid-ssn",
    "tax.us.2025.eic.answer.not-nonresident-alien",
    "tax.us.2025.eic.answer.age-25-under-65",
    "tax.us.2025.eic.answer.main-home-in-us",
    "tax.us.2025.eic.answer.not-qualifying-child-of-another",
    "tax.us.2025.eic.answer.not-claimable-as-dependent",
)


def _close_withholding(acts: list[dict[str, object]]) -> None:
    _close_empty(
        acts,
        family="tax.us.2025.w2-box2",
        version="v1",
        closure_fact="tax.us.2025.w2-box2.source-closure",
        horizon="demo.eic.t2.w2box2",
    )
    _close_other_box4_families(acts, skip={"w2-box2"})


def _finish_bottom_line(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    acts = _with_answers(acts, PASSING)
    acts = _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)
    return _finish_v53(acts, note)


def _acts_single() -> list[dict[str, object]]:
    """Single, no qualifying child. Wages $12,000 are in the 0-child
    phase-out. Taxable interest $2,000 makes AGI $14,000, so line 6 takes
    the smaller table credit and the credit is the refund."""
    acts = cast(
        list[dict[str, object]],
        _sdd()._senior_acts(wages=12000.0, filing_status="single"),
    )
    acts, _payer, _stmt = _reopen_interest_with_real_box1(acts, amount=2000.0)
    acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0)
    _close_withholding(acts)
    return _finish_bottom_line(acts, "golden: single phase-out wages with interest, credit refunded")


def _acts_joint() -> list[dict[str, object]]:
    """Married filing jointly. One spouse's W-2 is $8,000 and the other's
    is $8,000, so line 1z is $16,000, on the 0-child joint plateau."""
    acts = cast(
        list[dict[str, object]],
        _sdd()._senior_acts(wages=8000.0, filing_status="married_filing_jointly"),
    )
    acts = _reopen_w2_with_second_slip(acts, amount=8000.0)
    acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0)
    acts.append(
        _act(
            len(acts),
            "assertion",
            {
                "finding": _attested(
                    "demo.eic.t2.box2.spouse",
                    "tax.us.2025.w2.box2-withholding|employer=demo.t2.w2second.employer,w2-slip=demo.t2.w2second.slip,tax-year=2025",
                    0.0,
                )
            },
        )
    )
    _close_withholding(acts)
    return _finish_bottom_line(acts, "golden: joint plateau, wages from both spouses, credit on the bottom line")


def _present(
    acts: list[dict[str, object]], run_id: str, surface: PublicationSurface
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=USER,
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


def _assert_no_machine_path(model: dict[str, Any]) -> None:
    text = json.dumps(model)
    for needle in ("/" + "Users", "/" + "private"):
        if needle in text:
            raise AssertionError("presentation contains a machine path")


class EarnedIncomeCreditPresentationTests(unittest.TestCase):
    def test_single_phaseout_presentation_golden(self) -> None:
        model, _pubs = _present(_acts_single(), RUN_SINGLE, SURFACE_V53)
        golden = _load_golden(SINGLE_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        # Hand-checked against the 2025 EIC Table, 0-child other column.
        # Wages $12,000 are in the phase-out: the $12,000 cell is $542.
        # Interest $2,000 makes AGI $14,000: the $14,000 cell is $389.
        # Line 6 takes the smaller amount. Standard deduction $15,750 leaves
        # taxable income $0, so the credit is the refund.
        # Line 1z is line 1a on this class. Line 11 is line 11a.
        self.assertEqual(_published_numeric(model, "line-1a"), 12000)
        self.assertEqual(_published_numeric(model, "line-11a"), 14000)
        self.assertEqual(_published_numeric(model, "line-eic-a-1"), 12000)
        self.assertEqual(_published_numeric(model, "line-eic-a-2"), 542)
        self.assertEqual(_published_numeric(model, "line-eic-a-3"), 14000)
        self.assertEqual(_published_numeric(model, "line-eic-a-5"), 389)
        self.assertEqual(_published_numeric(model, "line-eic-a-6"), 389)
        self.assertEqual(_published_numeric(model, "line-27a"), 389)
        self.assertEqual(_published_numeric(model, "line-32"), 389)
        self.assertEqual(_published_numeric(model, "line-33"), 389)
        self.assertEqual(_published_numeric(model, "line-34"), 389)
        self.assertEqual(_published_numeric(model, "line-37"), 0)
        _assert_no_machine_path(model)

    def test_joint_plateau_presentation_golden(self) -> None:
        model, _pubs = _present(_acts_joint(), RUN_JOINT, SURFACE_V53)
        golden = _load_golden(JOINT_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        # Hand-checked, 0-child joint column. $8,000 plus $8,000 is $16,000,
        # inside the plateau ($8,490 through $17,730), so both table credits
        # are the $649 maximum. AGI is under the phase-out threshold, so
        # line 5 is blank and line 6 is line 2. Tax is $0. The credit is
        # the bottom line.
        self.assertEqual(_published_numeric(model, "line-1a"), 16000)
        self.assertEqual(_published_numeric(model, "line-11a"), 16000)
        self.assertEqual(_published_numeric(model, "line-eic-a-1"), 16000)
        self.assertEqual(_published_numeric(model, "line-eic-a-2"), 649)
        self.assertEqual(_published_numeric(model, "line-eic-a-3"), 16000)
        self.assertEqual(_section(model, "line-eic-a-5")["resolved"]["disposition"], "guard_inapplicable")
        self.assertEqual(_published_numeric(model, "line-eic-a-6"), 649)
        self.assertEqual(_published_numeric(model, "line-27a"), 649)
        self.assertEqual(_published_numeric(model, "line-32"), 649)
        self.assertEqual(_published_numeric(model, "line-33"), 649)
        self.assertEqual(_published_numeric(model, "line-34"), 649)
        self.assertEqual(_published_numeric(model, "line-37"), 0)
        _assert_no_machine_path(model)

    def test_line27a_explanation_reaches_the_worksheet_and_each_answer(self) -> None:
        _model, pubs = _present(_acts_single(), RUN_SINGLE, SURFACE_V53)
        finding = pubs[LINE27A]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(389))
        derived = index_derived(list(pubs.values()))
        node = explain(str(finding["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        symbols = {item.symbol for item in nodes}
        ids = {item.finding_id for item in nodes}
        for symbol in (LINE6, LINE2, WAGES, AGI, INVESTMENT, *REACHED_ANSWERS):
            self.assertIn(symbol, symbols, symbol)
        self.assertIn(TABLE, ids)
        self.assertIn("range_lookup", ids)
        self.assertNotIn("tax.us.2025.eic.table-credit.at-agi", symbols)
        self.assertNotIn("tax.us.2025.eic.band.at-earned-income", symbols)

    def test_v52_presentation_still_reads_as_before(self) -> None:
        model, _pubs = _present(_acts_refund(), RUN_REFUND, SURFACE_V52)
        golden = _load_golden(REFUND_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        self.assertEqual(_published_numeric(model, "line-34"), 965)


if __name__ == "__main__":
    unittest.main()
