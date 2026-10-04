"""The enrollment answer belongs to the schooling the loan paid for.

ADR 0077 Part 2 names the enrollment answer as said "for the named period,
institution, and programme". The person answers it about the schooling this
loan paid for. When the loan's schooling links change (a financing link is
affirmed, answered no or cannot-tell, corrected or withdrawn), the old answer
no longer names the schooling the loan now pays for. The recorder ends that
borrowing's current enrollment answer in the same save, so it reads as
missing and the person is asked again. The loan-cost answer is about the loan,
not the schooling, and stays.

Every result is read through ``live_coordinate_run`` over a fresh recovery of
the saved log (Track 5's ``run_live``, which also runs the reference runner).
"""
from __future__ import annotations

import json
import unittest
from typing import Any, Sequence
from unittest import mock

import pytest

from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import project
from packages.tax import sli_relationship_review as review_mod
import tests.test_sli_track4_support_chain as T4
import tests.test_sli_track5_worksheet_integration as t5
from tests.test_sli_track7_interruption_safety import _Interrupted, interrupt_at

# Integration by construction: each case runs core calculations v41 live.
pytestmark = pytest.mark.live

AT = "2026-10-03T15:00:00Z"
ENROLLMENT_MISSING = (
    "The loan on this statement has no answer yet to: was the student enrolled at least half-time in a degree "
    "or certificate program during the schooling it paid for? Answer that question. A missing answer is not "
    "treated as no.")


def current_ids(ws: t5.Return, fact_type: str, borrowing: str) -> list[str]:
    """Current finding ids of one borrowing answer, from a fresh recovery."""
    state = project(ws.acts(), ws.registry)
    current = compute_currency(state).current_finding_ids
    fact_id = fact_id_for(fact_type, (("borrowing", ws.borrowing[borrowing]),))
    return sorted(fid for fid, row in state.findings.items() if fid in current and row.get("fact_id") == fact_id)


def correct_schooling(ws: t5.Return, borrowing: str, old: str, new: str) -> None:
    """Correct the loan's financing link from one schooling to another, through the review."""
    name = ws._name(f"correct-financing-{borrowing}-{old}-{new}")
    review_mod.correct_review_claim(
        ws.log, ws.registry, finding_id=ws.claims.pop(("financing", borrowing, old)), review=ws._review(name),
        **ws._clause("financing", borrowing, new, "yes"), actor=t5.USER, at=AT,
        submission_id=f"demo.enroll-follows.submission.{name}", evidence_id=f"demo.evidence.enroll-follows.{name}")


class EnrollmentFollowsSchooling(unittest.TestCase):

    def setUp(self) -> None:
        self.step = 0

    def ws(self, **kwargs: Any) -> t5.Return:
        ws = t5.Return(**kwargs)
        self.addCleanup(ws.raw.cleanup)
        ws.plain()
        return ws

    def run_return(self, ws: t5.Return) -> t5.Outcome:
        self.step += 1
        return t5.run_live(ws.acts(), f"demo.run.enroll-follows.{self._testMethodName}.{self.step:02d}")

    def standing(self, ws: t5.Return, outcome: t5.Outcome, statement: str = "cedar") -> str:
        return str(T4.published(outcome.forward, t5.STANDING)[ws.statement[statement]]["value"])

    def assert_deducts(self, ws: t5.Return, outcome: t5.Outcome, amount: int) -> None:
        self.assertEqual((outcome.line21["disposition"], outcome.value()), ("published_value", amount))
        self.assertEqual(self.standing(ws, outcome), "none")

    def assert_asks_enrollment_again(self, ws: t5.Return, outcome: t5.Outcome, loan_answer: list[str]) -> None:
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertNotIn("value", outcome.line21)
        self.assertEqual(self.standing(ws, outcome), "enrollment-answer-missing")
        self.assertEqual(t5.line21_text(outcome), [f"{t5.CEDAR}: {ENROLLMENT_MISSING}"])
        self.assertEqual(current_ids(ws, T4.ENROLL, "autumn"), [], "the old enrollment answer is still current")
        self.assertEqual(current_ids(ws, T4.LOAN, "autumn"), loan_answer, "the loan-cost answer changed")

    def test_relinking_the_loan_to_another_schooling_asks_enrollment_again(self) -> None:
        # The review's reproduction: no on the link to A, then a link to B.
        ws = self.ws()
        self.assert_deducts(ws, self.run_return(ws), 2500)
        loan = current_ids(ws, T4.LOAN, "autumn")
        ws.outcome("financing", "autumn", "autumn", "no")
        self.assertEqual(self.standing(ws, self.run_return(ws)), "no-schooling-link")
        self.assertEqual(current_ids(ws, T4.ENROLL, "autumn"), [])
        ws.link("financing", "autumn", "spring")
        self.assert_asks_enrollment_again(ws, self.run_return(ws), loan)
        ws.answer("enroll", "autumn", "yes")
        self.assert_deducts(ws, self.run_return(ws), 2500)

    def test_correcting_the_link_to_another_schooling_asks_enrollment_again(self) -> None:
        ws = self.ws()
        loan = current_ids(ws, T4.LOAN, "autumn")
        correct_schooling(ws, "autumn", "autumn", "spring")
        self.assert_asks_enrollment_again(ws, self.run_return(ws), loan)
        ws.answer("enroll", "autumn", "yes")
        self.assert_deducts(ws, self.run_return(ws), 2500)

    def test_withdrawing_or_adding_a_schooling_ends_the_answer(self) -> None:
        for change in ("withdrawn", "cannot-tell", "second-schooling"):
            with self.subTest(change=change):
                ws = self.ws()
                loan = current_ids(ws, T4.LOAN, "autumn")
                if change == "second-schooling":
                    ws.link("financing", "autumn", "spring")
                else:
                    ws.outcome("financing", "autumn", "autumn", change)
                self.assertEqual(current_ids(ws, T4.ENROLL, "autumn"), [])
                self.assertEqual(current_ids(ws, T4.LOAN, "autumn"), loan)

    def test_the_plain_case_and_a_same_schooling_correction_keep_the_answer(self) -> None:
        ws = self.ws()
        enrolled = current_ids(ws, T4.ENROLL, "autumn")
        self.assertEqual(len(enrolled), 1)
        self.assert_deducts(ws, self.run_return(ws), 2500)
        # A link to the statement is not a schooling link.
        ws.outcome("statement-inclusion", "autumn", "cedar", "no")
        ws.link("statement-inclusion", "autumn", "cedar", "yes")
        # Correcting the financing link to the same schooling leaves the set as it was.
        correct_schooling(ws, "autumn", "autumn", "autumn")
        self.assertEqual(current_ids(ws, T4.ENROLL, "autumn"), enrolled)
        self.assert_deducts(ws, self.run_return(ws), 2500)

    def test_an_unrelated_borrowing_keeps_its_answer(self) -> None:
        ws = self.ws(amounts={"cedar": 1500.0, "birch": 1000.0})
        ws.plain("spring", "spring", "birch")
        self.assert_deducts(ws, self.run_return(ws), 2500)
        spring = (current_ids(ws, T4.ENROLL, "spring"), current_ids(ws, T4.LOAN, "spring"))
        correct_schooling(ws, "autumn", "autumn", "spring")
        self.assertEqual((current_ids(ws, T4.ENROLL, "spring"), current_ids(ws, T4.LOAN, "spring")), spring)
        outcome = self.run_return(ws)
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertEqual(self.standing(ws, outcome), "enrollment-answer-missing")
        self.assertEqual(self.standing(ws, outcome, "birch"), "none")

    def test_an_interrupted_relink_is_never_more_favorable(self) -> None:
        ws = self.ws()
        before = ws.acts()
        enrolled = current_ids(ws, T4.ENROLL, "autumn")
        financing = ws.claims[("financing", "autumn", "autumn")]
        baseline = self.run_return(ws)
        self.assert_deducts(ws, baseline, 2500)
        sizes: list[int] = []
        batches: list[list[dict[str, Any]]] = []
        real_batch = ActLog.append_batch

        def counted(log: ActLog, items: Sequence[dict[str, Any]], expected_revision: int) -> int:
            sizes.append(len(items))
            batches.append(list(items))
            return real_batch(log, items, expected_revision)

        # Learn the save's size, then crash before each of its lines in turn.
        with mock.patch.object(ActLog, "append_batch", counted), \
                interrupt_at(lambda line: True, torn=False), self.assertRaises(_Interrupted):
            correct_schooling(ws, "autumn", "autumn", "spring")
        self.assertEqual(ws.acts(), before)
        [size] = sizes
        # The end of the enrollment answer is part of the one save.
        self.assertIn({"finding_id": enrolled[0]},
                      [item["payload"] for item in batches[0] if item["kind"] == "finding-retracted"])
        for line in range(size):
            for torn in (False, True):
                with self.subTest(line=line, torn=torn):
                    ws.claims[("financing", "autumn", "autumn")] = financing

                    def stop_at(k: int, stop: int = line) -> bool:
                        return k == stop

                    with interrupt_at(stop_at, torn=torn), self.assertRaises(_Interrupted):
                        correct_schooling(ws, "autumn", "autumn", "spring")
                    # Recovered fresh, the log is the state before the save.
                    self.assertEqual(ws.acts(), before)
                    self.assertEqual(current_ids(ws, T4.ENROLL, "autumn"), enrolled)
        recovered = self.run_return(ws)
        self.assert_deducts(ws, recovered, 2500)
        self.assertEqual(json.dumps(recovered.line21, sort_keys=True).replace(recovered.model["runId"], ""),
                         json.dumps(baseline.line21, sort_keys=True).replace(baseline.model["runId"], ""))


if __name__ == "__main__":
    unittest.main()
