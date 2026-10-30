"""Saved presentations of the 2025 earned income credit with qualifying children on core v54.

Pattern: ``tests/test_earned_income_credit_presentation.py``. The goldens
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

from tests.test_earned_income_credit_track1 import SURFACE_V53
from tests.test_earned_income_credit_presentation import (
    SINGLE_GOLDEN as V53_SINGLE_GOLDEN,
    RUN_SINGLE as V53_RUN_SINGLE,
    _acts_single as _v53_acts_single,
)
from tests.test_eic_qualifying_children_track1 import (
    AGE,
    COL_COUNT,
    COUNT,
    L6,
    LINE27A,
    SSN,
    SURFACE_V54,
    TABLE_KEY,
    _build_acts,
    _finish_v54,
    passing_child,
)
from tests.test_refund_or_amount_owed_track1 import (
    ROOT,
    USER,
    _close_empty,
    _close_other_box4_families,
)
from tests.test_refund_or_amount_owed_track2 import (
    _add_bottom_line_answers,
    _add_box2_only,
)

PRESENTATION = (
    ROOT
    / "packages"
    / "sample_data"
    / "eic_qualifying_children"
    / "presentation"
)
HOH_GOLDEN = (
    PRESENTATION
    / "hoh-two-children-refund.presentation-model.v1.json"
)
JOINT_GOLDEN = (
    PRESENTATION
    / "joint-three-children-one-qualifies.presentation-model.v1.json"
)
RUN_HOH = "demo.eic.presentation.hoh-two-children-refund"
RUN_JOINT = "demo.eic.presentation.joint-three-children-one-qualifies"

TABLE = "tax.us.2025.parameter.eic-table-2025"


def _close_withholding(acts: list[dict[str, object]]) -> None:
    _close_empty(
        acts,
        family="tax.us.2025.w2-box2",
        version="v1",
        closure_fact="tax.us.2025.w2-box2.source-closure",
        horizon="demo.eic.t2.w2box2",
    )
    _close_other_box4_families(acts, skip={"w2-box2"})


def _acts_hoh_two_children() -> list[dict[str, object]]:
    """Head of household (unmarried), two qualifying children (demo-child-1,
    demo-child-2), wages $15,000, carried to a refund."""
    acts = _build_acts(
        wages=15000.0,
        filing_status="head_of_household",
        children={
            "demo-child-1": passing_child(),
            "demo-child-2": passing_child(),
        },
    )
    acts = _add_box2_only(
        acts,
        employer="demo.cgd.t2.employer",
        slip="demo.cgd.t2.w2",
        amount=0.0,
    )
    _close_withholding(acts)
    acts = _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)
    return _finish_v54(
        acts,
        "golden: head of household, two qualifying children, credit refunded",
    )


def _acts_joint_three_children_one_qualifying() -> list[dict[str, object]]:
    """Married filing jointly, three children of whom one fails the age test
    and one has no valid SSN, so one child counts, wages $35,000."""
    c1 = passing_child()
    c2 = dict(passing_child(), **{AGE: "no"})
    c3 = dict(passing_child(), **{SSN: "no"})
    acts = _build_acts(
        wages=35000.0,
        filing_status="married_filing_jointly",
        children={
            "demo-child-1": c1,
            "demo-child-2": c2,
            "demo-child-3": c3,
        },
    )
    acts = _add_box2_only(
        acts,
        employer="demo.cgd.t2.employer",
        slip="demo.cgd.t2.w2",
        amount=0.0,
    )
    _close_withholding(acts)
    acts = _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)
    return _finish_v54(
        acts,
        "golden: joint, three children with one qualifying, credit on bottom line",
    )


def _present(
    acts: list[dict[str, object]],
    run_id: str,
    surface: PublicationSurface,
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
            raise AssertionError(
                f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}"
            )
        if outcome.presentation_path is None or outcome.publications is None:
            raise AssertionError(f"{run_id} saved no presentation")
        model = cast(
            dict[str, Any],
            json.loads(outcome.presentation_path.read_text(encoding="utf-8")),
        )
        pubs = {
            str(pub.finding["symbol"]): pub.finding
            for pub in outcome.publications
        }
        return model, pubs


def _section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
    return next(
        section for section in model["sections"] if section["id"] == section_id
    )


def _published_numeric(model: dict[str, Any], section_id: str) -> Any:
    resolved = _section(model, section_id)["resolved"]
    if resolved.get("disposition") in {
        "published_value",
        "computed_zero",
        "closure_backed_zero",
    }:
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


class EicQualifyingChildrenPresentationTests(unittest.TestCase):
    def test_hoh_two_children_presentation_golden(self) -> None:
        model, _pubs = _present(_acts_hoh_two_children(), RUN_HOH, SURFACE_V54)
        golden = _load_golden(HOH_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        # Hand-checked against the 2025 EIC Table:
        # Row: At least 15,000, But less than 15,050
        # Column: Single, head of household, or qualifying surviving spouse and you have 2 children
        # Credit: 6,010.
        # Wages $15,000 (line 1a) -> AGI $15,000 (line 11a).
        # Standard deduction for HOH is $23,625, leaving taxable income $0 (line 15).
        # Tax is $0 (lines 16, 24).
        # EIC line 27a is $6,010. Payments line 32 and line 33 are $6,010.
        # Refund line 34 is $6,010. Amount owed line 37 is $0.
        self.assertEqual(_published_numeric(model, "line-1a"), 15000)
        self.assertEqual(_published_numeric(model, "line-11a"), 15000)
        self.assertEqual(_published_numeric(model, "line-15"), 0)
        self.assertEqual(_published_numeric(model, "line-16"), 0)
        self.assertEqual(_published_numeric(model, "line-24"), 0)
        self.assertEqual(_published_numeric(model, "line-eic-a-1"), 15000)
        self.assertEqual(_published_numeric(model, "line-eic-a-2"), 6010)
        self.assertEqual(_published_numeric(model, "line-eic-a-3"), 15000)
        self.assertEqual(
            _section(model, "line-eic-a-5")["resolved"]["disposition"],
            "guard_inapplicable",
        )
        self.assertEqual(_published_numeric(model, "line-eic-a-6"), 6010)
        self.assertEqual(_published_numeric(model, "line-27a"), 6010)
        self.assertEqual(_published_numeric(model, "line-32"), 6010)
        self.assertEqual(_published_numeric(model, "line-33"), 6010)
        self.assertEqual(_published_numeric(model, "line-34"), 6010)
        self.assertEqual(_published_numeric(model, "line-37"), 0)
        _assert_no_machine_path(model)

    def test_joint_three_children_one_qualifying_presentation_golden(self) -> None:
        model, _pubs = _present(
            _acts_joint_three_children_one_qualifying(),
            RUN_JOINT,
            SURFACE_V54,
        )
        golden = _load_golden(JOINT_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        # Hand-checked against the 2025 EIC Table:
        # Row: At least 35,000, But less than 35,050
        # Column: Married filing jointly and you have 1 child
        # Credit: 3,600.
        # Wages $35,000 (line 1a) -> AGI $35,000 (line 11a).
        # Standard deduction for MFJ is $31,500, leaving taxable income $3,500 (line 15).
        # Tax is $353 (lines 16, 24).
        # EIC line 27a is $3,600. Total payments line 33 is $3,600.
        # Refund line 34 is $3,247 ($3,600 - $353). Amount owed line 37 is $0.
        self.assertEqual(_published_numeric(model, "line-1a"), 35000)
        self.assertEqual(_published_numeric(model, "line-11a"), 35000)
        self.assertEqual(_published_numeric(model, "line-15"), 3500)
        self.assertEqual(_published_numeric(model, "line-16"), 353)
        self.assertEqual(_published_numeric(model, "line-24"), 353)
        self.assertEqual(_published_numeric(model, "line-eic-a-1"), 35000)
        self.assertEqual(_published_numeric(model, "line-eic-a-2"), 3600)
        self.assertEqual(_published_numeric(model, "line-eic-a-3"), 35000)
        self.assertEqual(_published_numeric(model, "line-eic-a-5"), 3600)
        self.assertEqual(_published_numeric(model, "line-eic-a-6"), 3600)
        self.assertEqual(_published_numeric(model, "line-27a"), 3600)
        self.assertEqual(_published_numeric(model, "line-32"), 3600)
        self.assertEqual(_published_numeric(model, "line-33"), 3600)
        self.assertEqual(_published_numeric(model, "line-34"), 3247)
        self.assertEqual(_published_numeric(model, "line-37"), 0)
        _assert_no_machine_path(model)

    def test_line27a_explanation_reaches_worksheet_count_and_child_tests(self) -> None:
        _model, pubs = _present(
            _acts_joint_three_children_one_qualifying(),
            RUN_JOINT,
            SURFACE_V54,
        )
        finding = pubs[LINE27A]
        self.assertEqual(Decimal(str(finding["value"])), Decimal(3600))
        derived = index_derived(list(pubs.values()))
        node = explain(str(finding["id"]), role="output", derived=derived)
        nodes = _nodes(node)
        symbols = {item.symbol for item in nodes}
        ids = {item.finding_id for item in nodes}

        # Worksheet A line 6, the table row/key, and counts
        self.assertIn(L6, symbols)
        self.assertIn(TABLE_KEY, symbols)
        self.assertIn(COUNT, symbols)
        self.assertIn(COL_COUNT, symbols)
        self.assertIn(TABLE, ids)
        self.assertIn("range_lookup", ids)

        # Child 1: passes all tests; all tests and counts are in the walk
        c1_tests = (
            "tax.us.2025.eic.child.relationship-met|tax.us.2025.eic.child.relationship|child=demo-child-1,tax-year=2025",
            "tax.us.2025.eic.child.age-met|tax.us.2025.eic.child.age|child=demo-child-1,tax-year=2025",
            "tax.us.2025.eic.child.residency-met|tax.us.2025.eic.child.residency|child=demo-child-1,tax-year=2025",
            "tax.us.2025.eic.child.joint-return-met|tax.us.2025.eic.child.joint-return|child=demo-child-1,tax-year=2025",
            "tax.us.2025.eic.child.ssn-met|tax.us.2025.eic.child.ssn|child=demo-child-1,tax-year=2025",
            "tax.us.2025.eic.child.other-claimant-clear|tax.us.2025.eic.child.another-may-claim|child=demo-child-1,tax-year=2025",
            "tax.us.2025.eic.child.counts|tax.us.2025.eic.child.relationship|child=demo-child-1,tax-year=2025",
        )
        for sym in c1_tests:
            self.assertIn(sym, symbols)

        # Child 2: fails age; relationship-met, age-met (failing test) and counts are reached
        c2_tests = (
            "tax.us.2025.eic.child.relationship-met|tax.us.2025.eic.child.relationship|child=demo-child-2,tax-year=2025",
            "tax.us.2025.eic.child.age-met|tax.us.2025.eic.child.age|child=demo-child-2,tax-year=2025",
            "tax.us.2025.eic.child.counts|tax.us.2025.eic.child.relationship|child=demo-child-2,tax-year=2025",
        )
        for sym in c2_tests:
            self.assertIn(sym, symbols)

        # Child 3: fails SSN; relationship-met, age-met, residency-met, joint-return-met,
        # ssn-met (failing test) and counts are reached
        c3_tests = (
            "tax.us.2025.eic.child.relationship-met|tax.us.2025.eic.child.relationship|child=demo-child-3,tax-year=2025",
            "tax.us.2025.eic.child.age-met|tax.us.2025.eic.child.age|child=demo-child-3,tax-year=2025",
            "tax.us.2025.eic.child.residency-met|tax.us.2025.eic.child.residency|child=demo-child-3,tax-year=2025",
            "tax.us.2025.eic.child.joint-return-met|tax.us.2025.eic.child.joint-return|child=demo-child-3,tax-year=2025",
            "tax.us.2025.eic.child.ssn-met|tax.us.2025.eic.child.ssn|child=demo-child-3,tax-year=2025",
            "tax.us.2025.eic.child.counts|tax.us.2025.eic.child.relationship|child=demo-child-3,tax-year=2025",
        )
        for sym in c3_tests:
            self.assertIn(sym, symbols)

    def test_v53_presentation_still_reads_as_before(self) -> None:
        model, _pubs = _present(_v53_acts_single(), V53_RUN_SINGLE, SURFACE_V53)
        golden = _load_golden(V53_SINGLE_GOLDEN)
        self.assertEqual(project_presentation_v1(model), golden)
        self.assertEqual(_published_numeric(model, "line-27a"), 389)
        self.assertEqual(_published_numeric(model, "line-34"), 389)


if __name__ == "__main__":
    unittest.main()
