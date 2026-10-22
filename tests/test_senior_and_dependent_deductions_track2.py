"""Track 2: a dependent's standard deduction (Standard Deduction Worksheet
for Dependents), proved through the real coordinator on core-calculations
v51 -- extended in place by Track 2 (same v51/registry v49/release v49;
unmerged, so no v52).

Reuses Track 1's own act-log builder and real-coordinator runner
(``tests.test_senior_and_dependent_deductions_track1``), which itself
reuses the tax-on-taxable-income P0 probe. Every case here drives
``live_coordinate_run`` transitively through Track 1's ``_run`` (named
here explicitly so the fast-lane budget's live-module heuristic in
``tests/conftest.py`` -- a source-token scan of this file, not a
transitive-import walk -- marks this module live correctly; it is an
honest integration test, not a fast-lane candidate).
"""

from __future__ import annotations

from decimal import Decimal

import unittest

from tests import test_senior_and_dependent_deductions_track1 as track1
from tests import test_tax_on_taxable_income_track1 as toti

STD = toti.STD
LINE_13B = track1.LINE_13B
LINE_12E = track1.LINE_12E
LINE4C = "tax.us.2025.dependents-worksheet.line4c"
CAN_BE_CLAIMED = track1.CAN_BE_CLAIMED

_senior_acts = track1._senior_acts
_finish_v51 = track1._finish_v51
_run = track1._run
_value = track1._value


class DependentStandardDeductionTrack2Tests(unittest.TestCase):
    def test_dependent_single_wages_3000(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=3000, can_be_claimed="yes"),
            "synthetic case: dependent, single, wages $3,000",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case1")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(3450))

    def test_dependent_wages_500(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=500, can_be_claimed="yes"),
            "synthetic case: dependent, wages $500",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case2")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(1350))

    def test_dependent_wages_20000_capped(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=20000, can_be_claimed="yes"),
            "synthetic case: dependent, wages $20,000 (capped)",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case3")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(15750))

    def test_dependent_66_and_blind_wages_3000(self) -> None:
        acts = _finish_v51(
            _senior_acts(
                wages=3000,
                can_be_claimed="yes",
                taxpayer_over_65=True,
                taxpayer_blind=True,
                taxpayer_ssn="yes",
            ),
            "synthetic case: dependent, 66 and blind, wages $3,000",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case4")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(7450))

    def test_earned_income_exactly_900(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=900, can_be_claimed="yes"),
            "synthetic boundary: earned income exactly $900",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case.boundary900")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(1350))

    def test_earned_income_exactly_901(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=901, can_be_claimed="yes"),
            "synthetic boundary: earned income exactly $901",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case.boundary901")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(1351))

    def test_joint_only_spouse_claimed(self) -> None:
        acts = _finish_v51(
            _senior_acts(
                wages=40000,
                filing_status="married_filing_jointly",
                can_be_claimed="yes",
            ),
            "synthetic case: joint, only the spouse can be claimed",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case.joint-spouse")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(31500))

    def test_dependent_also_65_gets_senior_deduction_too(self) -> None:
        """The law is silent on a dependent claiming the senior deduction;
        nothing bars it. Both the dependents' worksheet (line 12e/standard
        deduction) and Schedule 1-A Part V (line 13b) compute for the same
        return without conflict."""
        acts = _finish_v51(
            _senior_acts(
                wages=3000,
                can_be_claimed="yes",
                taxpayer_over_65=True,
                taxpayer_ssn="yes",
            ),
            "synthetic case: dependent who is also 65 or older",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case.dependent-senior")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(5450))
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(6000))

    def test_non_dependent_unchanged_from_track1(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=80000, can_be_claimed="no"),
            "synthetic case: non-dependent, unchanged",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case.nondependent")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(15750))

    def test_single_dependent_spouse_box_not_counted(self) -> None:
        """Repair round 1: line 1 gates the spouse boxes exactly as v2
        gates its own spouse additions -- single is not married_filing_
        jointly/_separately/qualifying_surviving_spouse, so a recorded
        spouse_over_65 on a single return adds no box, same as if it were
        never recorded (test_dependent_single_wages_3000)."""
        acts = _finish_v51(
            _senior_acts(wages=3000, can_be_claimed="yes", spouse_over_65=True),
            "synthetic case: single dependent, spouse_over_65 recorded true",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case.spousegate")
        self.assertEqual(_value(pubs, blocked, STD), Decimal(3450))

    def test_non_dependent_v51_matches_v50_every_filing_status(self) -> None:
        """For each filing status, with all four age/blindness boxes true,
        a non-dependent's v51 line 12e equals the v50 result -- the real-
        path identity repair round 1 establishes between v2 and
        line 3 + line 4b."""
        for status in (
            "single",
            "married_filing_jointly",
            "married_filing_separately",
            "head_of_household",
            "qualifying_surviving_spouse",
        ):
            with self.subTest(status=status):
                v50_acts = toti._finish_v50(
                    toti._age(
                        toti._probe()._base_acts(wages=80000, filing_status=status),
                        taxpayer_over_65=True,
                        taxpayer_blind=True,
                        spouse_over_65=True,
                        spouse_blind=True,
                    ),
                    f"synthetic v50 comparison, {status}, all four boxes",
                )
                v50_pubs, v50_blocked = toti._run(v50_acts, f"demo.sdd2.case.v50.{status}")
                v50_value = _value(v50_pubs, v50_blocked, LINE_12E)

                v51_acts = _finish_v51(
                    _senior_acts(
                        wages=80000,
                        filing_status=status,
                        can_be_claimed="no",
                        taxpayer_over_65=True,
                        taxpayer_blind=True,
                        spouse_over_65=True,
                        spouse_blind=True,
                    ),
                    f"synthetic v51 comparison, {status}, all four boxes",
                )
                v51_pubs, v51_blocked = _run(v51_acts, f"demo.sdd2.case.v51.{status}")
                v51_value = _value(v51_pubs, v51_blocked, LINE_12E)

                self.assertEqual(v51_value, v50_value, status)

    def test_missing_dependent_answer_blocks(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=80000, can_be_claimed=None),
            "synthetic case: missing dependent answer",
        )
        pubs, blocked = _run(acts, "demo.sdd2.case.missing")
        self.assertNotIn(STD, pubs)
        found = any(CAN_BE_CLAIMED in str(row.get("missing", [])) for row in blocked)
        self.assertTrue(found, f"expected {CAN_BE_CLAIMED} named in a blocked disposition; blocked={blocked}")


if __name__ == "__main__":
    unittest.main()
