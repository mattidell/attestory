"""Offered review wrappers retain the exact scopes of durable claims."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

import pytest

from packages.kernel.act_log import ActLog
from packages.tax.loader import tax_registry
from packages.tax.mortgage_borrowing_recording import introduce_mortgage_borrowing_reference_durably
from packages.tax.mortgage_borrowing_recording import record_mortgage_borrowing_claim_durably
from packages.tax.mortgage_borrowing_review import (
    MortgageBorrowingReviewRefused, correct_mortgage_borrowing_review_answer,
    clear_mortgage_borrowing_review_account, prepare_mortgage_borrowing_review,
    record_mortgage_borrowing_review_answer,
    withdraw_mortgage_borrowing_review_answer,
)
from tests.test_f1098_statement_review import _append_seed
from packages.tax.f1098_statement_review import (
    F1098ReviewRefused, answer_f1098_statement_review_question,
    correct_f1098_statement_review_answer, prepare_f1098_statement_review,
)

pytestmark = pytest.mark.live(
    reason="durable ActLog admission and mortgage review snapshots exceed the fast-lane budget"
)


class MortgageBorrowingReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="mortgage-borrowing-review-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)
        _append_seed(self.log, second_interest=3500)
        self.actor = "demo.taxpayer"
        self.borrowing = "demo.mortgage.borrowing.review"
        introduce_mortgage_borrowing_reference_durably(
            self.log, self.registry, reference_id=self.borrowing,
            description="Synthetic original mortgage", actor=self.actor,
            at="2026-10-24T10:00:00Z")

    def test_linked_report_offers_shared_facts_once_and_keeps_prior_local_correctable(self) -> None:
        keys = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
        local_review = prepare_f1098_statement_review(
            self.log, self.registry, review_id="demo.f1098.review.before-link",
            shown_at="2026-10-24T10:00:30Z", statement_keys=keys)
        prior_local = answer_f1098_statement_review_question(
            self.log, self.registry, local_review, question="this-is-the-original-loan", answer="yes",
            submission_id="demo.f1098.original-before-link", evidence_id="demo.f1098.original-before-link.evidence",
            actor=self.actor, at="2026-10-24T10:00:31Z")
        record_mortgage_borrowing_claim_durably(
            self.log, self.registry, claim="report-inclusion", borrowing_ref=self.borrowing,
            value="affirmed", submission_id="demo.mortgage.link-a", evidence_id="demo.mortgage.link-a.evidence",
            actor=self.actor, at="2026-10-24T10:00:32Z", statement_keys=keys,
            expected_revision=self.log.read().revision)
        linked_review = prepare_f1098_statement_review(
            self.log, self.registry, review_id="demo.f1098.review.after-link",
            shown_at="2026-10-24T10:00:33Z", statement_keys=keys)
        self.assertEqual(linked_review["linkedBorrowings"], [self.borrowing])
        original = linked_review["questions"]["this-is-the-original-loan"]
        self.assertEqual(original["collectionScope"], "borrowing")
        self.assertEqual(original["offerMode"], "historical-answer-correctable")
        self.assertEqual(original["finding_id"], prior_local["finding_ids"][0])
        owes = linked_review["questions"]["owes-the-loan"]
        self.assertEqual(owes["offerMode"], "use-borrowing-review")
        with self.assertRaises(F1098ReviewRefused):
            answer_f1098_statement_review_question(
                self.log, self.registry, linked_review, question="owes-the-loan", answer="yes",
                submission_id="demo.f1098.owes-after-link", evidence_id="demo.f1098.owes-after-link.evidence",
                actor=self.actor, at="2026-10-24T10:00:34Z")
        corrected = correct_f1098_statement_review_answer(
            self.log, self.registry, linked_review, question="this-is-the-original-loan", answer="no",
            submission_id="demo.f1098.original-correction", evidence_id="demo.f1098.original-correction.evidence",
            actor=self.actor, at="2026-10-24T10:00:35Z")
        self.assertNotEqual(corrected["finding_ids"], prior_local["finding_ids"])
        self.assertEqual(corrected["state"].findings[corrected["finding_ids"][0]]["value"], "no")

    def test_review_distinguishes_absent_ceiling_and_exact_report_links(self) -> None:
        review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.one",
            shown_at="2026-10-24T10:01:00Z", borrowing_ref=self.borrowing)
        ceiling = next(row for row in review["answers"] if row["claim"] == "annual-ceiling")
        self.assertEqual(ceiling["state"], "absent")
        self.assertIsNone(ceiling["value"])
        links = [row for row in review["answers"] if row["claim"] == "report-inclusion"]
        self.assertEqual(len(links), 2)
        self.assertTrue(all(row["state"] == "absent" for row in links))
        self.assertEqual({row["scope"]["statement"] for row in links},
                         {"demo.f1098.stmt.a", "demo.f1098.stmt.b"})
        questions = {row["claim"]: row for row in review["questions"]}
        recognition = questions["continuing-borrowing"]
        self.assertNotIn("same original", recognition["question"].lower())
        self.assertIn("one borrowing", recognition["help"])
        self.assertIn("original loan or a refinance is a separate question", recognition["help"])
        no_others = {choice["value"]: choice["label"]
                     for choice in questions["no-one-else-owes-it"]["choices"]}
        self.assertEqual(no_others["yes"], "No one else owes it")
        self.assertEqual(no_others["no"], "Someone else owes it")
        self.assertEqual(questions["no-one-else-owes-it"]["question"],
                         "Do only you and, if filing jointly, your spouse owe this borrowing?")
        self.assertIn("Only when you file jointly", questions["no-one-else-owes-it"]["help"])
        self.assertEqual(questions["other-secured-home-debt"]["question"],
                         "Besides this borrowing, did you have debt secured by your main home or a second home in 2025?")
        self.assertIn("Do not count the named borrowing", questions["other-secured-home-debt"]["help"])
        self.assertEqual(questions["annual-ceiling"]["question"],
                         "What is a dollar amount you are confident the balance on this borrowing did not go above at any point during 2025? It can be higher than the exact highest balance.")
        self.assertIn("company collecting payments does not", questions["this-is-the-original-loan"]["help"])
        self.assertIn("once across its linked reports", questions["this-is-the-original-loan"]["scope"])
        shared_questions = [row for row in review["questions"]
                            if row["claim"] in {"owes-the-loan", "no-one-else-owes-it",
                                                "what-the-money-paid-for", "this-is-the-original-loan",
                                                "mortgage-credit-certificate-received"}]
        self.assertEqual(len(shared_questions), 5)
        self.assertEqual(len({row["claim"] for row in shared_questions}), 5)
        self.assertTrue(all("once across its linked reports" in row["scope"] for row in shared_questions))
        self.assertEqual(questions["annual-ceiling"]["inputKind"], "nonnegative-number")
        self.assertEqual(questions["annual-ceiling"]["minimum"], 0)
        self.assertEqual(questions["annual-ceiling"]["unanswered"], {"state": "absent", "value": None})

    def test_obligor_help_is_conditional_on_joint_filing_on_both_review_surfaces(self) -> None:
        keys = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
        expected_choices = {"yes": "No one else owes it", "no": "Someone else owes it",
                            "cannot-tell": "I can't tell"}
        for filing_status in ("married_filing_separately", "married_filing_jointly"):
            with self.subTest(filing_status=filing_status):
                log = ActLog(Path(self.temp.name) / filing_status, self.registry)
                _append_seed(log, filing_status=filing_status, second_interest=3500)
                borrowing = f"demo.mortgage.borrowing.{filing_status}"
                introduce_mortgage_borrowing_reference_durably(
                    log, self.registry, reference_id=borrowing,
                    description="Synthetic mortgage borrowing", actor=self.actor,
                    at="2026-10-24T10:00:00Z")
                local = prepare_f1098_statement_review(
                    log, self.registry, review_id=f"demo.local.{filing_status}",
                    shown_at="2026-10-24T10:00:30Z", statement_keys=keys)
                shared = prepare_mortgage_borrowing_review(
                    log, self.registry, review_id=f"demo.shared.{filing_status}",
                    shown_at="2026-10-24T10:00:31Z", borrowing_ref=borrowing)
                local_question = local["questions"]["no-one-else-owes-it"]
                shared_question = next(row for row in shared["questions"]
                                       if row["claim"] == "no-one-else-owes-it")
                for question in (local_question, shared_question):
                    self.assertIn("Only when you file jointly", question["help"])
                    self.assertIn("If you file separately", question["help"])
                    self.assertEqual(question["question"],
                                     "Do only you and, if filing jointly, your spouse owe this "
                                     + ("loan?" if question is local_question else "borrowing?"))
                self.assertEqual(local_question["labels"], expected_choices)
                self.assertEqual({choice["value"]: choice["label"]
                                  for choice in shared_question["choices"]}, expected_choices)

    def test_reviewed_claim_write_rechecks_revision(self) -> None:
        review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.stale",
            shown_at="2026-10-24T10:02:00Z", borrowing_ref=self.borrowing)
        record_mortgage_borrowing_review_answer(
            self.log, self.registry, review, claim="continuing-borrowing",
            borrowing_ref=self.borrowing, value="yes", submission_id="demo.mortgage.recognition",
            evidence_id="demo.mortgage.recognition.evidence", actor=self.actor,
            at="2026-10-24T10:03:00Z")
        before = self.log.read().revision
        with self.assertRaises(MortgageBorrowingReviewRefused):
            record_mortgage_borrowing_review_answer(
                self.log, self.registry, review, claim="annual-ceiling",
                borrowing_ref=self.borrowing, value=250000, submission_id="demo.mortgage.ceiling",
                evidence_id="demo.mortgage.ceiling.evidence", actor=self.actor,
                at="2026-10-24T10:04:00Z")
        self.assertEqual(self.log.read().revision, before)

    def test_recognition_correction_and_withdrawal_keep_the_named_scope(self) -> None:
        review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.lifecycle",
            shown_at="2026-10-24T10:05:00Z", borrowing_ref=self.borrowing)
        first = record_mortgage_borrowing_review_answer(
            self.log, self.registry, review, claim="continuing-borrowing",
            borrowing_ref=self.borrowing, value="yes", submission_id="demo.mortgage.recognition.lifecycle",
            evidence_id="demo.mortgage.recognition.lifecycle.evidence", actor=self.actor,
            at="2026-10-24T10:06:00Z")
        shown = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.correct",
            shown_at="2026-10-24T10:07:00Z", borrowing_ref=self.borrowing)
        current = next(row for row in shown["claims"] if row["claim"] == "continuing-borrowing")
        corrected = correct_mortgage_borrowing_review_answer(
            self.log, self.registry, shown, claim="continuing-borrowing", borrowing_ref=self.borrowing,
            finding_id=current["findingId"], value="cannot-tell",
            submission_id="demo.mortgage.recognition.corrected",
            evidence_id="demo.mortgage.recognition.corrected.evidence", actor=self.actor,
            at="2026-10-24T10:08:00Z")
        corrected_review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.withdraw",
            shown_at="2026-10-24T10:09:00Z", borrowing_ref=self.borrowing)
        successor = next(row for row in corrected_review["claims"] if row["claim"] == "continuing-borrowing")
        withdrawn = withdraw_mortgage_borrowing_review_answer(
            self.log, self.registry, corrected_review, claim="continuing-borrowing",
            borrowing_ref=self.borrowing, finding_id=successor["findingId"], actor=self.actor,
            at="2026-10-24T10:10:00Z", submission_id="demo.mortgage.recognition.withdrawn",
            evidence_id="demo.mortgage.recognition.withdrawn.evidence")
        self.assertNotEqual(first["finding_id"], corrected["finding_id"])
        self.assertEqual(withdrawn["state"].findings[withdrawn["finding_id"]]["value"], "withdrawn")

    def test_displayed_borrowing_scope_and_snapshot_are_bound_before_write(self) -> None:
        other = "demo.mortgage.borrowing.other-review"
        introduce_mortgage_borrowing_reference_durably(
            self.log, self.registry, reference_id=other, description="Other synthetic borrowing",
            actor=self.actor, at="2026-10-24T10:11:00Z")
        shown_a = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.only-a",
            shown_at="2026-10-24T10:12:00Z", borrowing_ref=self.borrowing)
        before = self.log.read().revision
        with self.assertRaises(MortgageBorrowingReviewRefused):
            record_mortgage_borrowing_review_answer(
                self.log, self.registry, shown_a, claim="continuing-borrowing", borrowing_ref=other,
                value="yes", submission_id="demo.mortgage.hidden-b.record",
                evidence_id="demo.mortgage.hidden-b.record.evidence", actor=self.actor,
                at="2026-10-24T10:13:00Z")
        self.assertEqual(self.log.read().revision, before)
        altered = dict(shown_a)
        altered["reports"] = []
        with self.assertRaises(MortgageBorrowingReviewRefused):
            record_mortgage_borrowing_review_answer(
                self.log, self.registry, altered, claim="continuing-borrowing", borrowing_ref=self.borrowing,
                value="yes", submission_id="demo.mortgage.altered-snapshot.record",
                evidence_id="demo.mortgage.altered-snapshot.record.evidence", actor=self.actor,
                at="2026-10-24T10:14:00Z")
        self.assertEqual(self.log.read().revision, before)

    def test_displayed_borrowing_cannot_correct_withdraw_or_clear_another(self) -> None:
        from packages.tax.mortgage_borrowing_recording import record_mortgage_borrowing_claim_durably

        other = "demo.mortgage.borrowing.hidden"
        introduce_mortgage_borrowing_reference_durably(
            self.log, self.registry, reference_id=other, description="Other synthetic borrowing",
            actor=self.actor, at="2026-10-24T10:15:00Z")
        existing = record_mortgage_borrowing_claim_durably(
            self.log, self.registry, claim="continuing-borrowing", borrowing_ref=other,
            value="yes", submission_id="demo.mortgage.hidden-existing",
            evidence_id="demo.mortgage.hidden-existing.evidence", actor=self.actor,
            at="2026-10-24T10:16:00Z")
        shown_a = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.scope-a",
            shown_at="2026-10-24T10:17:00Z", borrowing_ref=self.borrowing)
        before = self.log.read().revision
        with self.assertRaises(MortgageBorrowingReviewRefused):
            correct_mortgage_borrowing_review_answer(
                self.log, self.registry, shown_a, claim="continuing-borrowing", borrowing_ref=other,
                finding_id=existing["finding_id"], value="no", submission_id="demo.mortgage.hidden-correct",
                evidence_id="demo.mortgage.hidden-correct.evidence", actor=self.actor,
                at="2026-10-24T10:18:00Z")
        with self.assertRaises(MortgageBorrowingReviewRefused):
            withdraw_mortgage_borrowing_review_answer(
                self.log, self.registry, shown_a, claim="continuing-borrowing", borrowing_ref=other,
                finding_id=existing["finding_id"], actor=self.actor, at="2026-10-24T10:19:00Z")
        with self.assertRaises(MortgageBorrowingReviewRefused):
            clear_mortgage_borrowing_review_account(
                self.log, self.registry, shown_a, borrowing_ref=other,
                actor=self.actor, at="2026-10-24T10:20:00Z")
        self.assertEqual(self.log.read().revision, before)


if __name__ == "__main__":
    unittest.main()
