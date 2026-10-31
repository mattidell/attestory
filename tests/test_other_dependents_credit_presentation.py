"""Track 2: the credit for other dependents in saved presentations on core v56.

The goldens are the presentation models ``live_coordinate_run`` writes for two
synthetic returns, through the real coordinator on v56:

- married filing jointly, wages $70,000, one qualifying child under 17 (SSN valid) and
  one child aged 18 claimed for the credit for other dependents;
- single, wages $30,000, a parent claimed as a qualifying relative, no children.

Each is hand-checked below against Schedule 8812 (2025) and the Form 1040 Tax Table
(2025, ``i1040gi-2025.txt``). Sources are cited by line of the pdftotext text in
``temp/tax-on-taxable-income/sources/``: standard deduction ``:230`` (MFJ $31,500) and
``:228`` (single $15,750); Tax Table rows ``:5127`` (38,500-38,550, MFJ column 4,146) and
``:4948`` (14,250-14,300, single column 1,475; the columns are single, MFJ, MFS, HOH);
Schedule 8812 ``f1040s8.txt``; EIC completed amounts in
``packages/content/tax/2025/parameter.eic-2025.json`` (mfj.2.completed 64,430).
"""

from __future__ import annotations

import json
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.presentation_projection import project_presentation_v1
from packages.derivation.explanation import explain_legacy as explain, index_derived
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability

from tests.test_other_dependents_credit_track1 import (
    PACKAGE_V56,
    RELEASE_V54,
    SURFACE_V56,
    build,
    ctc_child,
    odc_child,
    relative,
)
from tests.test_refund_or_amount_owed_track1 import ROOT, USER
from tests.test_refund_or_amount_owed_track1 import _close_empty, _close_other_box4_families, _finish
from tests.test_refund_or_amount_owed_track2 import _add_bottom_line_answers, _add_box2_only
from tests.test_child_tax_credit_presentation import (
    JOINT_EXACT as CTC_V55_JOINT_EXACT,
    RUN_JOINT as CTC_V55_RUN_JOINT,
    _acts_joint_two_children as _ctc_v55_acts_joint,
    _present as _ctc_v55_present,
)

PRESENTATION = ROOT / "packages" / "sample_data" / "other_dependents_credit" / "presentation"
MFJ_GOLDEN = PRESENTATION / "mfj-child-under-17-and-eighteen-year-old-credit-on-line-19.presentation-model.v1.json"
MFJ_EXACT = PRESENTATION / "mfj-child-under-17-and-eighteen-year-old-credit-on-line-19.exact-pins.presentation-model.v1.json"
SINGLE_GOLDEN = PRESENTATION / "single-qualifying-relative-credit-on-line-19.presentation-model.v1.json"
SINGLE_EXACT = SINGLE_GOLDEN.with_name(SINGLE_GOLDEN.name.replace(".presentation-model.v1.json", ".exact-pins.presentation-model.v1.json"))
RUN_MFJ = "demo.odc.presentation.mfj-child-and-eighteen-year-old"
RUN_SINGLE = "demo.odc.presentation.single-qualifying-relative"

L19 = "tax.us.2025.ctc.form1040-line19"
L6 = "tax.us.2025.ctc.sch8812.line-6"
L7 = "tax.us.2025.ctc.sch8812.line-7"
L8 = "tax.us.2025.ctc.sch8812.line-8"
L12 = "tax.us.2025.ctc.sch8812.line-12"
L14 = "tax.us.2025.ctc.sch8812.line-14"
WA5 = "tax.us.2025.ctc.sch8812.worksheet-a.line-5"
CHILD_COUNT = "tax.us.2025.ctc.child-count"
ODC_CHILD_COUNT = "tax.us.2025.odc.child-count"
ODC_REL_COUNT = "tax.us.2025.odc.relative-count"


def _finish_presentation(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """Adds the W-2 box 2 family (no withholding), closes the other box 4 families, and
    adds the bottom-line answers, as the child tax credit presentation does."""
    acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0)
    _close_empty(
        acts,
        family="tax.us.2025.w2-box2",
        version="v1",
        closure_fact="tax.us.2025.w2-box2.source-closure",
        horizon="demo.odc.t2.w2box2",
    )
    _close_other_box4_families(acts, skip={"w2-box2"})
    acts = _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)
    return _finish(
        acts,
        package_path=PACKAGE_V56,
        package_version="v56",
        release_path=RELEASE_V54,
        release_version="v54",
        note="other dependents presentation golden",
    )


def _acts_mfj() -> list[dict[str, object]]:
    kids = {
        "demo-child-1": ctc_child(),
        "demo-child-2": odc_child(**{"tax.us.2025.ctc.child.under-17": "no"}),
    }
    return _finish_presentation(build(wages=70000.0, filing_status="married_filing_jointly", children=kids))


def _acts_single() -> list[dict[str, object]]:
    return _finish_presentation(build(wages=30000.0, filing_status="single",
                                      relatives={"demo-dependent-1": relative()}))


def _present(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
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
            surface=SURFACE_V56,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        if outcome.presentation_path is None or outcome.publications is None:
            raise AssertionError(f"{run_id} saved no presentation")
        model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text(encoding="utf-8")))
        pubs = {str(pub.finding["symbol"]): pub.finding for pub in outcome.publications}
        return model, pubs


def _numeric(model: dict[str, Any], section_id: str) -> Any:
    section = next(s for s in model["sections"] if s["id"] == section_id)
    resolved = section["resolved"]
    if resolved.get("disposition") in {"published_value", "computed_zero", "closure_backed_zero"}:
        return resolved.get("value")
    return resolved


def _load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AssertionError(f"committed presentation golden required at {path}")
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _walk_symbols(finding: dict[str, Any], pubs: dict[str, dict[str, Any]]) -> set[str]:
    derived = index_derived(list(pubs.values()))
    found: set[str] = set()
    pending = [explain(str(finding["id"]), role="output", derived=derived)]
    while pending:
        node = pending.pop()
        if node.symbol is not None:
            found.add(str(node.symbol))
        pending.extend(node.children)
    return found


def _child_tests(child: str) -> tuple[str, ...]:
    tail = f"child={child},tax-year=2025"
    return (
        f"tax.us.2025.odc.child.counted|tax.us.2025.odc.child.other-dependent-box|{tail}",
        f"tax.us.2025.odc.child.identity-met|tax.us.2025.odc.child.other-dependent-box|{tail}",
        f"tax.us.2025.odc.child.other-tests-met|tax.us.2025.odc.child.other-dependent-box|{tail}",
    )


class OtherDependentPresentationTests(unittest.TestCase):
    def test_mfj_golden_regenerates_and_matches(self) -> None:
        model, _ = _present(_acts_mfj(), RUN_MFJ)
        self.assertEqual(project_presentation_v1(model), _load(MFJ_EXACT))

    def test_single_golden_regenerates_and_matches(self) -> None:
        model, _ = _present(_acts_single(), RUN_SINGLE)
        self.assertEqual(project_presentation_v1(model), _load(SINGLE_EXACT))

    def test_mfj_hand_check(self) -> None:
        model, _ = _present(_acts_mfj(), RUN_MFJ)
        # Wages 70,000 = line 1a = line 11 (no adjustments). Standard deduction 31,500
        # (i1040gi-2025.txt:230): taxable income 38,500. Tax Table row 38,500-38,550,
        # married filing jointly column 4,146 (i1040gi-2025.txt:5127).
        self.assertEqual(_numeric(model, "line-16"), 4146)
        self.assertEqual(_numeric(model, "line-8812-wa-5"), 4146)
        # Schedule 8812: line 4 = 1 (demo-child-1 under 17 with a valid SSN); line 5 = 1 x 2,200
        # = 2,200; line 6 = 1 (demo-child-2, aged 18: other dependent); line 7 = 1 x 500 = 500;
        # line 8 = 2,700; line 9 = 400,000; line 10 = 0; line 11 = 0; line 12 = 2,700;
        # line 13 = Worksheet A = tax 4,146; line 14 = min(2,700, 4,146) = 2,700.
        self.assertEqual(_numeric(model, "line-8812-4"), 1)
        self.assertEqual(_numeric(model, "line-8812-6"), 1)
        self.assertEqual(_numeric(model, "line-8812-7"), 500)
        self.assertEqual(_numeric(model, "line-8812-14"), 2700)
        # Form 1040 line 19 = 2,700 (the whole combined credit; the tax is above it).
        self.assertEqual(_numeric(model, "line-19"), 2700)
        # Line 24 = line 16 - line 19 = 4,146 - 2,700 = 1,446 (no other taxes).
        self.assertEqual(_numeric(model, "line-24"), 1446)
        # EIC: married filing jointly, two qualifying children, completed amount 64,430
        # (parameter.eic-2025.json, mfj.2.completed); 70,000 is above it, so line 27a = 0.
        self.assertEqual(_numeric(model, "line-27a"), 0)
        # Withholding 0 (box 2 = 0), so line 33 = 0; line 37 = 1,446 - 0 = 1,446.
        self.assertEqual(_numeric(model, "line-33"), 0)
        self.assertEqual(_numeric(model, "line-37"), 1446)

    def test_single_hand_check(self) -> None:
        model, _ = _present(_acts_single(), RUN_SINGLE)
        # Wages 30,000. Standard deduction 15,750 (i1040gi-2025.txt:228): taxable 14,250.
        # Tax Table row 14,250-14,300, single column 1,475 (i1040gi-2025.txt:4948).
        self.assertEqual(_numeric(model, "line-16"), 1475)
        self.assertEqual(_numeric(model, "line-8812-wa-5"), 1475)
        # Schedule 8812: line 4 = 0; line 5 = 0; line 6 = 1 (qualifying relative); line 7 = 500;
        # line 8 = 500; line 9 = 200,000; line 10 = 0; line 11 = 0; line 12 = 500;
        # line 13 = 1,475; line 14 = min(500, 1,475) = 500.
        self.assertEqual(_numeric(model, "line-8812-4"), 0)
        self.assertEqual(_numeric(model, "line-8812-6"), 1)
        self.assertEqual(_numeric(model, "line-8812-7"), 500)
        self.assertEqual(_numeric(model, "line-8812-14"), 500)
        # Form 1040 line 19 = 500.
        self.assertEqual(_numeric(model, "line-19"), 500)
        # Line 24 = 1,475 - 500 = 975; no earned income credit (no qualifying child), so line 27a = 0.
        self.assertEqual(_numeric(model, "line-24"), 975)
        self.assertEqual(_numeric(model, "line-27a"), 0)
        # Line 37 = 975 - 0 = 975.
        self.assertEqual(_numeric(model, "line-37"), 975)

    def test_walk_from_line_19_reaches_lines_6_to_14_and_each_dependent(self) -> None:
        _, pubs = _present(_acts_mfj(), RUN_MFJ)
        finding = pubs[L19]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(2700))
        symbols = _walk_symbols(finding, pubs)
        for sym in (L6, L7, L8, L12, L14, WA5, CHILD_COUNT, ODC_CHILD_COUNT):
            self.assertIn(sym, symbols)
        # The other-dependent child (demo-child-2) and the child under 17 are both in the walk.
        for child in ("demo-child-1", "demo-child-2"):
            self.assertIn(f"tax.us.2025.ctc.child.counts|tax.us.2025.eic.child.relationship|child={child},tax-year=2025",
                          symbols)
        for sym in _child_tests("demo-child-2"):
            self.assertIn(sym, symbols)

    def test_walk_from_line_19_reaches_the_relative_tests(self) -> None:
        _, pubs = _present(_acts_single(), RUN_SINGLE)
        finding = pubs[L19]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(500))
        symbols = _walk_symbols(finding, pubs)
        for sym in (L6, L7, L8, L12, L14, WA5, ODC_REL_COUNT):
            self.assertIn(sym, symbols)
        self.assertTrue(any(s.startswith("tax.us.2025.odc.dependent.counted|") for s in symbols))
        self.assertTrue(any(s.startswith("tax.us.2025.odc.dependent.tests-a-met|") for s in symbols))
        self.assertTrue(any(s.startswith("tax.us.2025.odc.dependent.tests-b-met|") for s in symbols))

    def test_v55_child_tax_credit_presentation_reads_as_before(self) -> None:
        model, _ = _ctc_v55_present(_ctc_v55_acts_joint(), CTC_V55_RUN_JOINT)
        self.assertEqual(project_presentation_v1(model), _load(CTC_V55_JOINT_EXACT))


if __name__ == "__main__":
    unittest.main()
