"""The current-core return helpers (``tests/helpers/current_core_returns.py``), each driven live.

A helper is only worth keeping if its return really is complete on the latest core (v66), so
each case runs the return through ``live_coordinate_run`` and asserts that the target line
publishes, that nothing is blocked, and that nothing unrelated moved. The hand values come
from the 2025 Tax Table and the form lines, worked before the engine ran:

- Base: single, wages 50,000, standard deduction 15,750 -> taxable income 34,250; the Tax
  Table row 34,250-34,300 has midpoint 34,275, tax 1,192.50 + 12% of 22,350 = 3,874.50 -> 3,875;
  withholding 4,500 -> refund 625.
- Form 1098-E interest of 100.40 twice: 200.80 -> line 21 rounds once to 201 (not 100 + 100 = 200);
  AGI 49,799, taxable income 34,049, tax (row 34,000-34,050, midpoint 34,025) 3,844.50 -> 3,845,
  refund 655.
- Line 2a: 100.40 + 100.40 = 200.80 -> 201 (box 8 twice), box 8 plus box 12 of 100.40 each
  200.80 -> 201 (not 100 + 100 = 200). Line 2a is not income: AGI and refund do not move.
- Schedule 8812 line 21 with box 4 and box 6 of 100.40 each: 200.80 -> 201.

Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import unittest
from decimal import Decimal

from tests.helpers import current_core_returns as c
from tests.helpers.current_core_returns import CurrentRun, P

AGI = P + "income.agi"
TAXABLE = P + "income.taxable-income"
TAX = P + "tax.line24-total-tax"
REFUND = P + "payments.line35a-refunded"
LINE26 = P + "ctc.sch8812.line-26"
NEEDED = P + "ctc.sch8812.part-ii-b-needed"
SCH1_LINE26 = P + "schedule1.line26-total-adjustments"


def _run(acts: list[dict[str, object]], name: str) -> CurrentRun:
    return c.run_current_core(acts, f"demo.ccr.{name}")


class BaseReturn(unittest.TestCase):
    def test_base_return_publishes_with_nothing_blocked(self) -> None:
        run = _run(c.base_return(), "base")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(AGI), Decimal("50000"))
        self.assertEqual(run.value(TAXABLE), Decimal("34250"))
        self.assertEqual(run.value(TAX), Decimal("3875"))
        self.assertEqual(run.value(REFUND), Decimal("625"))
        # No statement of any family: each target line publishes 0.
        for target in (c.LINE2A, c.SCH1_LINE21, c.SCH8812_LINE21):
            self.assertEqual(run.value(target), Decimal("0"), target)


class HelperDiscipline(unittest.TestCase):
    def test_a_member_that_contradicts_a_base_declaration_raises(self) -> None:
        # Box 8 members recorded without changing the base's "no tax-exempt interest" answer.
        acts = c._record_members(
            c.base_return(), P + "f1099int.b8", [100.40], tag="b8", companions=[(c.BOX9_COMPANION, None)])
        with self.assertRaises(AssertionError) as raised:
            _run(acts, "contradiction")
        self.assertIn(c.LINE2A_NO_INT_SCOPE, str(raised.exception))
        self.assertIn("adder", str(raised.exception))

    def test_a_second_call_on_the_same_return_raises(self) -> None:
        acts = c.add_student_loan_interest_1098e(c.base_return(), [100.40])
        with self.assertRaises(AssertionError) as raised:
            c.add_student_loan_interest_1098e(acts, [50.0])
        self.assertIn("one call", str(raised.exception))

    def test_an_adder_leaves_the_list_it_was_given_unchanged(self) -> None:
        base = c.base_return()
        before = repr(base)
        c.add_tax_exempt_interest_1099int(base, [100.40])
        self.assertEqual(repr(base), before)


class Line2a(unittest.TestCase):
    def test_box_8_twice_publishes_line_2a_rounded_once(self) -> None:
        run = _run(c.add_tax_exempt_interest_1099int(c.base_return(), [100.40, 100.40]), "b8")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(c.BOX8_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(run.value(c.LINE2A), Decimal("201"))
        # Line 2a is reported, not taxed: the bottom line is the base return's.
        self.assertEqual(run.value(AGI), Decimal("50000"))
        self.assertEqual(run.value(REFUND), Decimal("625"))

    def test_box_12_twice_publishes_line_2a_rounded_once(self) -> None:
        run = _run(c.add_exempt_interest_dividends_1099div(c.base_return(), [100.40, 100.40]), "b12")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(c.BOX12_SUBTOTAL), Decimal("200.8"))
        self.assertEqual(run.value(c.LINE2A), Decimal("201"))
        self.assertEqual(run.value(AGI), Decimal("50000"))
        self.assertEqual(run.value(REFUND), Decimal("625"))

    def test_both_families_add_before_the_one_rounding(self) -> None:
        acts = c.add_tax_exempt_interest_1099int(c.base_return(), [100.40])
        acts = c.add_exempt_interest_dividends_1099div(acts, [100.40])
        run = _run(acts, "b8b12")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(c.LINE2A), Decimal("201"))


class StudentLoanInterest(unittest.TestCase):
    def test_two_statements_publish_schedule_1_line_21(self) -> None:
        run = _run(c.add_student_loan_interest_1098e(c.base_return(), [100.40, 100.40]), "sli")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(P + "sli-worksheet.line1-total-interest-paid-subtotal"), Decimal("200.8"))
        self.assertEqual(run.value(c.SCH1_LINE21), Decimal("201"))
        self.assertEqual(run.value(SCH1_LINE26), Decimal("201"))
        self.assertEqual(run.value(AGI), Decimal("49799"))
        self.assertEqual(run.value(TAXABLE), Decimal("34049"))
        self.assertEqual(run.value(TAX), Decimal("3845"))
        self.assertEqual(run.value(REFUND), Decimal("655"))


class PartIIB(unittest.TestCase):
    def test_three_children_with_box_4_and_6_publish_line_21(self) -> None:
        """Wages 15,000, three children: line 20 = 15% of (15,000 - 2,500) = 1,875, below line 17
        (5,100), so Part II-B applies. Line 21 = box 4 930 + box 6 218 = 1,148 (the 6.2 and 1.45
        percent of wages, to the dollar); line 24 is the earned income credit 6,761; line 25 =
        max(1,148 - 6,761, 0) = 0; line 26 = 1,875."""
        run = _run(c.part_ii_b_return(box4=930.0, box6=218.0), "p2b")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(NEEDED), Decimal("1"))
        self.assertEqual(run.value(c.SCH8812_LINE21), Decimal("1148"))
        self.assertEqual(run.value(P + "ctc.sch8812.line-24"), Decimal("6761"))
        self.assertEqual(run.value(P + "ctc.sch8812.line-25"), Decimal("0"))
        self.assertEqual(run.value(LINE26), Decimal("1875"))

    def test_two_children_do_not_read_part_ii_b(self) -> None:
        """Part II-B is needed from three children: with two, it is not needed (0), line 21 is 0
        and the box 4 total is not read."""
        run = _run(c.part_ii_b_return(box4=930.0, box6=218.0, children=2), "p2b-two")
        self.assertEqual(run.blocked_names(), set())
        self.assertEqual(run.value(NEEDED), Decimal("0"))
        self.assertEqual(run.value(c.SCH8812_LINE21), Decimal("0"))
        self.assertNotIn(P + "w2.box4-total", run.pubs)


if __name__ == "__main__":
    unittest.main()
