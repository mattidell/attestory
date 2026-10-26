"""Track 2: the child tax credit in saved presentations on core v55.

The goldens are the presentation models ``live_coordinate_run`` writes for two
synthetic returns. Each golden is hand-checked below against Schedule 8812
(2025), the Form 1040 Tax Table (2025, instructions p. 68 onward) and the 2025
EIC Table, and the arithmetic is stated beside each assertion.

Sources cited by line of the pdftotext text in ``temp/tax-on-taxable-income/sources/``:
standard deduction ``i1040gi-2025.txt:230`` (MFJ $31,500) and ``:232`` (HOH $23,625);
Tax Table row 43,500-43,550 ``i1040gi-2025.txt:5191`` (MFJ 4,746);
EIC Table row 18,000-18,050, 2 children, HOH ``i1040gi-2025.txt:3449`` (7,152);
Schedule 8812 ``f1040s8.txt`` and its instructions ``i1040s8.txt``.
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
from packages.derivation.production_resolver import PublicationSurface

from tests.test_child_tax_credit_track1 import (
    CLAIM,
    FAMILY,
    LINE19,
    LINE28,
    REGISTRY_V53,
    RELEASE_V53,
    U17,
    build_acts,
    passing_child,
)
from tests.test_refund_or_amount_owed_track1 import (
    CONTENT,
    ROOT,
    USER,
    _close_empty,
    _close_other_box4_families,
    _finish,
)
from tests.test_refund_or_amount_owed_track2 import _add_bottom_line_answers, _add_box2_only
from tests.test_eic_qualifying_children_presentation import (
    HOH_GOLDEN as V54_HOH_GOLDEN,
    RUN_HOH as V54_RUN_HOH,
    _acts_hoh_two_children as _v54_acts_hoh,
    _present as _v54_present,
)
from tests.test_eic_qualifying_children_track1 import SURFACE_V54

PRESENTATION = ROOT / "packages" / "sample_data" / "child_tax_credit" / "presentation"
JOINT_GOLDEN = PRESENTATION / "joint-two-children-credit-on-line-19.presentation-model.v1.json"
HOH_GOLDEN = PRESENTATION / "hoh-one-child-actc-with-unclaimed-17.presentation-model.v1.json"
RUN_JOINT = "demo.ctc.presentation.joint-two-children-credit-on-line-19"
RUN_HOH = "demo.ctc.presentation.hoh-one-child-actc-with-unclaimed-17"
PACKAGE_V55 = CONTENT / "package.core-calculations.v55.json"
SURFACE_V55 = PublicationSurface(RELEASE_V53.parent, REGISTRY_V53, CONTENT)
L8812_4 = "tax.us.2025.ctc.sch8812.line-4"
L8812_12 = "tax.us.2025.ctc.sch8812.line-12"
L8812_14 = "tax.us.2025.ctc.sch8812.line-14"
L8812_16A = "tax.us.2025.ctc.sch8812.line-16a"
L8812_16B = "tax.us.2025.ctc.sch8812.line-16b"
L8812_17 = "tax.us.2025.ctc.sch8812.line-17"
L8812_20 = "tax.us.2025.ctc.sch8812.line-20"
WA5 = "tax.us.2025.ctc.sch8812.worksheet-a.line-5"
COUNT = "tax.us.2025.ctc.child-count"
LINE27A = "tax.us.2025.payments.line27a"
LINE33 = "tax.us.2025.payments.line33"


def _acts_joint_two_children() -> list[dict[str, object]]:
    """Married filing jointly, two qualifying children (demo-child-1, demo-child-2),
    wages $75,000, W-2 box 2 withholding $0, no estimated payments."""
    kids = {"demo-child-1": passing_child(), "demo-child-2": passing_child()}
    acts = build_acts(wages=75000.0, filing_status="married_filing_jointly", children=kids)
    acts = _finish_presentation(acts, _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0))
    return acts


def _acts_hoh_one_child_and_unclaimed_17() -> list[dict[str, object]]:
    """Head of household, wages $18,000. demo-child-1 is claimed and qualifies. demo-child-2
    is 17 at the end of 2025 and not claimed for the credit: the credit does not count her and
    does not block (a claimed child who failed a test would block), but she is an EIC
    qualifying child (under 19), so the earned income credit counts two children."""
    unclaimed = dict(passing_child(), **{CLAIM: "no", U17: "no"})
    kids = {"demo-child-1": passing_child(), "demo-child-2": unclaimed}
    acts = build_acts(wages=18000.0, filing_status="head_of_household", children=kids)
    return _finish_presentation(acts, _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0))


def _finish_presentation(acts: list[dict[str, object]], with_box2: list[dict[str, object]]) -> list[dict[str, object]]:
    acts = with_box2
    _close_empty(
        acts,
        family="tax.us.2025.w2-box2",
        version="v1",
        closure_fact="tax.us.2025.w2-box2.source-closure",
        horizon="demo.ctc.t2.w2box2",
    )
    _close_other_box4_families(acts, skip={"w2-box2"})
    acts = _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)
    return _finish(
        acts,
        package_path=PACKAGE_V55,
        package_version="v55",
        release_path=RELEASE_V53,
        release_version="v53",
        note="ctc presentation golden",
    )


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
            surface=SURFACE_V55,
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


def _numeric(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    if resolved.get("disposition") in {"published_value", "computed_zero", "closure_backed_zero"}:
        return resolved.get("value")
    return resolved


def _load(path: Path) -> dict[str, Any]:
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


def _child_walk_symbols(child: str) -> tuple[str, ...]:
    """Each per-child test and the count, as the explanation names them (the fact in the
    second position, the child in the identity)."""
    tail = f"child={child},tax-year=2025"
    return (
        f"tax.us.2025.ctc.child.under-17-met|tax.us.2025.ctc.child.under-17|{tail}",
        f"tax.us.2025.ctc.child.lived-with-you-met|tax.us.2025.ctc.child.lived-with-you|{tail}",
        f"tax.us.2025.ctc.child.no-support-met|tax.us.2025.ctc.child.no-over-half-support|{tail}",
        f"tax.us.2025.ctc.child.citizen-met|tax.us.2025.ctc.child.citizen-or-resident|{tail}",
        f"tax.us.2025.ctc.child.claimed-met|tax.us.2025.ctc.child.claimed-as-dependent|{tail}",
        f"tax.us.2025.ctc.child.joint-return-met|tax.us.2025.eic.child.joint-return|{tail}",
        f"tax.us.2025.ctc.child.ssn-met|tax.us.2025.eic.child.ssn|{tail}",
        f"tax.us.2025.ctc.child.other-claimant-clear|tax.us.2025.eic.child.another-may-claim|{tail}",
        f"tax.us.2025.ctc.child.counts|tax.us.2025.eic.child.relationship|{tail}",
    )


class ChildTaxCreditPresentationTests(unittest.TestCase):
    def test_joint_two_children_golden_and_hand_check(self) -> None:
        model, _pubs = _present(_acts_joint_two_children(), RUN_JOINT)
        self.assertEqual(model, _load(JOINT_GOLDEN))
        # Hand check, married filing jointly, two children under 17, wages $75,000.
        # Form 1040 line 1a = line 11a = 75,000 (no adjustments).
        # Standard deduction $31,500 (i1040gi-2025.txt:230): taxable 43,500.
        # Tax Table row 43,500-43,550, married filing jointly column: 4,746 (i1040gi-2025.txt:5191).
        self.assertEqual(_numeric(model, "line-16"), 4746)
        # Schedule 8812: line 4 = 2; line 5 = 2 x 2,200 = 4,400; line 8 = 4,400; line 9 = 400,000;
        # line 10 = 0; line 11 = 0; line 12 = 4,400; line 13 = Worksheet A = tax 4,746;
        # line 14 = min(4,400, 4,746) = 4,400, the whole credit on line 19.
        self.assertEqual(_numeric(model, "line-8812-4"), 2)
        self.assertEqual(_numeric(model, "line-8812-wa-5"), 4746)
        self.assertEqual(_numeric(model, "line-8812-14"), 4400)
        self.assertEqual(_numeric(model, "line-19"), 4400)
        # Line 16a = 4,400 - 4,400 = 0: the additional credit stops; line 28 = 0.
        self.assertEqual(_numeric(model, "line-28"), 0)
        # Line 24 = line 16 - line 19 = 4,746 - 4,400 = 346 (no other taxes).
        self.assertEqual(_numeric(model, "line-24"), 346)
        # Earned income credit: 75,000 is above the 2-child joint completed amount of 64,430
        # (parameter.eic-2025.json, mfj.2.completed), so line 27a = 0; withholding 0, so line 33 = 0.
        self.assertEqual(_numeric(model, "line-27a"), 0)
        self.assertEqual(_numeric(model, "line-33"), 0)
        # Line 37 amount owed = 346 - 0 = 346.
        self.assertEqual(_numeric(model, "line-37"), 346)

    def test_hoh_one_child_actc_golden_and_hand_check(self) -> None:
        model, _pubs = _present(_acts_hoh_one_child_and_unclaimed_17(), RUN_HOH)
        self.assertEqual(model, _load(HOH_GOLDEN))
        # Hand check, head of household, wages $18,000. Standard deduction $23,625
        # (i1040gi-2025.txt:232): taxable income 0, so tax 0 (line 16).
        self.assertEqual(_numeric(model, "line-16"), 0)
        # Schedule 8812: line 4 = 1 (demo-child-2 is not claimed, so not counted);
        # line 5 = 2,200; line 12 = 2,200; line 13 = Worksheet A = 0; line 14 = 0, so line 19 is capped
        # at the tax, which is zero.
        self.assertEqual(_numeric(model, "line-8812-4"), 1)
        self.assertEqual(_numeric(model, "line-8812-14"), 0)
        self.assertEqual(_numeric(model, "line-19"), 0)
        # Line 16a = 2,200 - 0 = 2,200; line 16b = 1 x 1,700 = 1,700; line 17 = 1,700.
        self.assertEqual(_numeric(model, "line-8812-17"), 1700)
        # Line 18a = 18,000; line 19 = 18,000 - 2,500 = 15,500; line 20 = 15% = 2,325.
        self.assertEqual(_numeric(model, "line-8812-20"), 2325)
        # Line 27 = min(1,700, 2,325) = 1,700 = line 28.
        self.assertEqual(_numeric(model, "line-28"), 1700)
        # EIC (2025 EIC Table, i1040gi-2025.txt:3449): 18,000-18,050, head of household, 2 children,
        # 7,152. Line 27a = 7,152.
        self.assertEqual(_numeric(model, "line-27a"), 7152)
        # Line 33 = 7,152 + 1,700 + 0 withholding = 8,852; line 24 = 0.
        self.assertEqual(_numeric(model, "line-33"), 8852)
        self.assertEqual(_numeric(model, "line-24"), 0)
        # Line 34 refund = 8,852 - 0 = 8,852; line 37 = 0.
        self.assertEqual(_numeric(model, "line-34"), 8852)
        self.assertEqual(_numeric(model, "line-37"), 0)

    def test_walk_from_line_19_reaches_part_i_worksheet_a_and_each_child(self) -> None:
        _model, pubs = _present(_acts_joint_two_children(), RUN_JOINT)
        finding = pubs[LINE19]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(4400))
        derived = index_derived(list(pubs.values()))
        symbols = {node.symbol for node in _nodes(explain(str(finding["id"]), role="output", derived=derived))}
        # Part I (lines 4, 8, 12, 14), Worksheet A line 5 and the child count.
        for sym in (L8812_14, L8812_12, WA5, L8812_4, COUNT):
            self.assertIn(sym, symbols)
        for child in ("demo-child-1", "demo-child-2"):
            for sym in _child_walk_symbols(child):
                self.assertIn(sym, symbols)

    def test_walk_from_line_28_reaches_part_ii_a_and_the_failing_age_test(self) -> None:
        _model, pubs = _present(_acts_hoh_one_child_and_unclaimed_17(), RUN_HOH)
        finding = pubs[LINE28]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(1700))
        derived = index_derived(list(pubs.values()))
        symbols = {node.symbol for node in _nodes(explain(str(finding["id"]), role="output", derived=derived))}
        for sym in (L8812_16A, L8812_16B, L8812_17, L8812_20, L8812_14, WA5, COUNT):
            self.assertIn(sym, symbols)
        # The failing age test for demo-child-2 (17 at the end of 2025) is in the walk.
        self.assertIn(
            "tax.us.2025.ctc.child.under-17-met|tax.us.2025.ctc.child.under-17|child=demo-child-2,tax-year=2025",
            symbols,
        )
        for sym in _child_walk_symbols("demo-child-1") + _child_walk_symbols("demo-child-2"):
            self.assertIn(sym, symbols)

    def test_v54_presentation_still_reads_as_before(self) -> None:
        model, _pubs = _v54_present(_v54_acts_hoh(), V54_RUN_HOH, SURFACE_V54)
        self.assertEqual(model, _load(V54_HOH_GOLDEN))


if __name__ == "__main__":
    unittest.main()
