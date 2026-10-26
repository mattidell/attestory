"""Track 1b: Schedule 8812 Part II-B (lines 21-27) on core v55, with W-2 boxes 4 and 6.

Proved through the real coordinator (`live_coordinate_run`, via the Track 1a run helper).
Each expected figure is hand-computed
from Schedule 8812 (2025) and stated beside its assertion. The three-child
and four-child cases use the EIC's printed table value for 3 children, single,
$15,000 (6,761; see tests/test_eic_qualifying_children_track1.py), so the EIC
line (Form 1040 line 27a) is read as a computed figure.

Hand-computed inputs (not from Schedule 8812): W-2 box 4 is 6.2 percent and box
6 is 1.45 percent of box 1 wages (Form W-2 instructions), rounded to the dollar
where the rate gives cents. The larger-branch case uses a box 4 amount above
that rate, labelled synthetic, because no realistic three-child, under $36,500
return has payroll tax above its earned income credit.
"""

from __future__ import annotations

import sys
from typing import Any, Mapping, cast

import unittest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))

from tests.test_refund_or_amount_owed_track1 import _act, _attested, _close_empty, _load  # noqa: E402
from tests.test_child_tax_credit_track1 import (  # noqa: E402
    LINE19,
    LINE28,
    TAX,
    build_acts as build_ctc_acts,
    passing_child,
    run_v55,
    value,
)

YEAR = "2025"
EIC_FAMILY = "tax.us.2025.eic.child-roster"
EIC_CLOSURE = "tax.us.2025.eic.child-roster.source-closure"
EIC_AGE = "tax.us.2025.eic.child.age"
EIC_RES = "tax.us.2025.eic.child.residency"
EIC_NOT_QC = "tax.us.2025.eic.not-qualifying-child-of-another"
EIC_SP_SSN = "tax.us.2025.eic.spouse-valid-ssn"
L2931 = "tax.us.2025.lines29-31-scope.no-other-refundable-credits"
SCH1_15 = "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se"
SCH2_OTHER = "tax.us.2025.schedule2-partii-scope.no-line21-additional-taxes"
BOX4 = "tax.us.2025.w2.box4-social-security"
BOX6 = "tax.us.2025.w2.box6-medicare"
BASE_EMPLOYER = "demo.cgd.t2.employer"
BASE_SLIP = "demo.cgd.t2.w2"
PAY27A = "tax.us.2025.payments.line27a"
L21 = "tax.us.2025.ctc.sch8812.line-21"
L23 = "tax.us.2025.ctc.sch8812.line-23"
L24 = "tax.us.2025.ctc.sch8812.line-24"
L25 = "tax.us.2025.ctc.sch8812.line-25"
L26 = "tax.us.2025.ctc.sch8812.line-26"
L27 = LINE28
NEEDED = "tax.us.2025.ctc.sch8812.part-ii-b-needed"
BOX4_ROW = "tax.us.2025.rule.w2-box4-total"
BOX6_ROW = "tax.us.2025.rule.w2-box6-total"


def _w2_identity(fid: str, employer: str, slip: str) -> str:
    return f"{fid}|employer={employer},w2-slip={slip},tax-year={YEAR}"


def build(
    *,
    wages: float,
    filing_status: str = "single",
    children: int = 3,
    slips: list[tuple[str, str, float, float]] | None = None,
    base_box: tuple[float | None, float | None] = (0.0, 0.0),
) -> list[dict[str, object]]:
    """A v55 return with ``children`` counted children, the EIC roster for the same
    children, and W-2 box 4 and 6 answers.

    ``base_box`` is the base slip's (box 4, box 6); ``None`` leaves that box unanswered.
    ``slips`` are extra W-2 slips as (employer, slip, box 4, box 6) with their box 1
    wages given as the extra wages list in ``slips`` by the caller's construction.
    """
    kids = {f"demo-child-{i}": passing_child() for i in range(1, children + 1)}
    acts = build_ctc_acts(wages=wages, filing_status=filing_status, children=kids)
    acts = _add_box_bundles(acts)
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("refund-or-amount-owed-questions.bundle.json")}))
    for fid in (SCH1_15, SCH2_OTHER):
        acts.append(_act(len(acts), "assertion", {"finding": _attested(
            f"demo.1b.{fid.split('.')[-1]}", f"{fid}|tax-year={YEAR}", "yes")}))
    b4, b6 = base_box
    if b4 is not None:
        _add_box(acts, "w2-box4", BASE_EMPLOYER, BASE_SLIP, b4)
    if b6 is not None:
        _add_box(acts, "w2-box6", BASE_EMPLOYER, BASE_SLIP, b6)
    _close_box(acts, "w2-box4")
    _close_box(acts, "w2-box6")
    return acts


def _add_box_bundles(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("w2-box4.bundle.json")}))
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("w2-box6.bundle.json")}))
    return acts


def _add_box(acts: list[dict[str, object]], box: str, employer: str, slip: str, amount: float | None) -> None:
    if amount is None:
        return
    fid = BOX4 if box == "w2-box4" else BOX6
    acts.append(_act(len(acts), "assertion", {"finding": _attested(
        f"demo.1b.{box}.{slip}", _w2_identity(fid, employer, slip), amount)}))


def _close_box(acts: list[dict[str, object]], box: str) -> None:
    fam = f"tax.us.2025.{box}"
    _close_empty(acts, family=fam, version="v1", closure_fact=f"{fam}.source-closure", horizon=f"demo.1b.{box}.h0")


def _expect(row: dict[str, Any] | None) -> dict[str, Any]:
    assert row is not None, "expected a blocked row"
    return row


def _blocked_missing(blocked: list[dict[str, Any]], fact: str) -> list[str]:
    return [row["artifact_id"] for row in blocked if fact in row.get("missing", [])]


class PartIIBComputed(unittest.TestCase):
    def test_three_children_part_ii_b_smaller_than_line_20_takes_no_extra(self) -> None:
        """Single, 3 children, wages 15,000 (AGI 15,000, tax 0).
        Hand: line 8 = 6,600; line 12 = 6,600; line 13 = tax 0; line 14 = 0;
        line 16a = 6,600; line 16b = 5,100; line 17 = 5,100.
        Line 18a = 15,000; line 19 = 12,500; line 20 = 15% of 12,500 = 1,875 (below 5,100: Part II-B).
        Line 21 = box 4 930 + box 6 218 = 1,148 (W-2 rates: 6.2% and 1.45% of 15,000 = 930 and 217.50, to the dollar).
        Line 22 = 0 (absent). Line 23 = 1,148. Line 24 = EIC 6,761 + Schedule 3 line 11 0 = 6,761.
        Line 25 = max(1,148 - 6,761, 0) = 0. Line 26 = max(1,875, 0) = 1,875. Line 27 = min(5,100, 1,875) = 1,875.
        Form 1040 line 19 = 0 (tax 0); line 28 = 1,875."""
        acts = build(wages=15000.0, children=3, base_box=(930.0, 218.0))
        pubs, blocked = run_v55(acts, "b-smaller")
        self.assertEqual(value(pubs, L21), 1148)
        self.assertEqual(value(pubs, L23), 1148)
        self.assertEqual(value(pubs, L24), 6761)
        self.assertEqual(value(pubs, L25), 0)
        self.assertEqual(value(pubs, L26), 1875)
        self.assertEqual(value(pubs, L27), 1875)
        self.assertEqual(value(pubs, LINE19), 0)

    def test_three_children_part_ii_b_larger_than_line_20_is_used(self) -> None:
        """As above but box 4 is a synthetic 9,000 (not a payroll-rate amount) and box 6 is 0.
        Hand: line 21 = 9,000; line 23 = 9,000; line 24 = 6,761; line 25 = 2,239;
        line 26 = max(1,875, 2,239) = 2,239; line 27 = min(5,100, 2,239) = 2,239."""
        acts = build(wages=15000.0, children=3, base_box=(9000.0, 0.0))
        pubs, _ = run_v55(acts, "b-larger")
        self.assertEqual(value(pubs, L21), 9000)
        self.assertEqual(value(pubs, L25), 2239)
        self.assertEqual(value(pubs, L26), 2239)
        self.assertEqual(value(pubs, L27), 2239)

    def test_two_w2_slips_are_summed(self) -> None:
        """Slip A: wages 9,000, box 4 558, box 6 131 (6.2% and 1.45%, to the dollar: 558.00 and 130.50 -> 131).
        Slip B: wages 6,000, box 4 372, box 6 87 (372.00 and 87.00). Box 4 sum 930; box 6 sum 218.
        Line 21 = 1,148; line 27 = 1,875, the same as the one-slip case."""
        acts = build(wages=9000.0, children=3, base_box=(558.0, 131.0))
        acts = _second_slip(acts, employer="demo.1b.slipB.employer", slip="demo.1b.slipB.w2", wages=6000.0, box4=372.0, box6=87.0)
        pubs, _ = run_v55(acts, "b-two-slips")
        self.assertEqual(value(pubs, L21), 1148)
        self.assertEqual(value(pubs, L27), 1875)

    def test_zero_box_answers_are_valid(self) -> None:
        """Box 4 and box 6 both 0 (a valid answer). Line 21 = 0; line 25 = max(0 - 6,761, 0) = 0;
        line 26 = 1,875; line 27 = 1,875."""
        acts = build(wages=15000.0, children=3, base_box=(0.0, 0.0))
        pubs, _ = run_v55(acts, "b-zero")
        self.assertEqual(value(pubs, L21), 0)
        self.assertEqual(value(pubs, L27), 1875)

    def test_fewer_than_three_children_never_asks_box_4_or_6(self) -> None:
        """Two children, wages 15,000 without any box answer: Part II-B is not read, so no
        box 4 or box 6 is asked and the credit is line 17 or line 20.
        Hand: line 20 = 1,875; line 17 = min(4,400 - 0, 3,400) = 3,400; line 27 = min(3,400, 1,875) = 1,875."""
        acts = build(wages=15000.0, children=2, base_box=(None, None))
        pubs, blocked = run_v55(acts, "b-two")
        self.assertEqual(value(pubs, L27), 1875)
        self.assertEqual(_blocked_missing(blocked, BOX4), [])
        self.assertEqual(_blocked_missing(blocked, BOX6), [])

    def test_three_children_at_or_above_line_17_never_asks_box_4_or_6(self) -> None:
        """Single, 3 children, wages 60,000: line 20 = 15% of 57,500 = 8,625, at or above line 17,
        so Part II-B is skipped (f1040s8 lines 61-64). Line 27 = line 17 = min(16a, 5,100) with 16a =
        6,600 - tax. No box answer is asked."""
        acts = build(wages=60000.0, children=3, base_box=(None, None))
        pubs, blocked = run_v55(acts, "b-high")
        tax = int(value(pubs, TAX))
        self.assertEqual(value(pubs, L27), min(6600 - tax, 5100))
        self.assertEqual(_blocked_missing(blocked, BOX4), [])


class PartIIBBlocks(unittest.TestCase):
    def test_missing_box_4_blocks_and_names_the_box_fact(self) -> None:
        acts = build(wages=15000.0, children=3, base_box=(None, 218.0))
        pubs, blocked = run_v55(acts, "b-miss4")
        self.assertNotIn(L27, pubs)
        self.assertIn(BOX4, _expect(_find(blocked, BOX4_ROW))["missing"])

    def test_missing_box_6_blocks_and_names_the_box_fact(self) -> None:
        acts = build(wages=15000.0, children=3, base_box=(930.0, None))
        pubs, blocked = run_v55(acts, "b-miss6")
        self.assertNotIn(L27, pubs)
        self.assertIn(BOX6, _expect(_find(blocked, BOX6_ROW))["missing"])


def _find(blocked: list[dict[str, Any]], artifact: str) -> dict[str, Any] | None:
    for row in blocked:
        if row.get("artifact_id") == artifact:
            return row
    return None


def _second_slip(acts: list[dict[str, object]], *, employer: str, slip: str, wages: float, box4: float, box6: float) -> list[dict[str, object]]:
    """Adds a second W-2 slip to the box 1 family (reopened, as the refund test does)."""
    kept = []
    for act in acts:
        if act.get("kind") == "assertion":
            payload = cast(dict[str, Any], act.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            if str(finding.get("fact_id", "")).startswith("tax.us.2025.w2.source-closure"):
                continue
        kept.append(act)
    acts = kept

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": employer, "kind": "tax.us.employer", "label": "Synthetic second employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": slip, "kind": "tax.us.w2-slip", "label": "Synthetic second W-2 slip"}})
    add("member-transition", {
        "family": {"id": "tax.us.2025.w2", "version": "v2"},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(
            f"demo.1b.w2b.wages", _w2_identity("tax.us.2025.w2.box1-wages", employer, slip), wages)},
        "successor": {"id": "demo.1b.w2.h2", "predecessor": "demo.cgd.t2.w2.h1"},
    })
    add("assertion", {"finding": _attested("demo.1b.w2.reclose", "tax.us.2025.w2.source-closure|family-horizon=demo.1b.w2.h2,tax-year=2025", True)})
    _add_box(acts, "w2-box4", employer, slip, box4)
    _add_box(acts, "w2-box6", employer, slip, box6)
    return acts


if __name__ == "__main__":
    unittest.main()
