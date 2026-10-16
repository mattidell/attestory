"""Track 4 direct durable-recorder admission and refusal checks."""
from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest

from packages.kernel.act_log import ActLog
from packages.tax.f1098_statement_recording import (
    F1098RecordingRefused, answer_f1098_statement_answer_durably,
    correct_f1098_statement_answer_durably,
    record_f1098_statement_answers_durably, withdraw_f1098_statement_answer_durably,
)
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.loader import tax_registry
from tests.test_f1098_statement_review import BASE_ANSWERS, USER, _append_seed, _evidence_ids, _review, _save


@pytest.mark.live(reason="real durable admission over the complete synthetic Form 1098 workspace exceeds the 3 second fast-lane budget")
class F1098StatementRecordingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1098-answer-recording-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)
        _append_seed(self.log)

    def test_single_first_ordinary_answer_builds_incomplete_account(self) -> None:
        keys = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
        saved = answer_f1098_statement_answer_durably(
            self.log, self.registry, statement_keys=keys, question="paid-the-interest", answer="yes",
            submission_id="demo.f1098.first-ordinary-answer",
            evidence_id="demo.f1098.first-ordinary-answer.evidence", actor=USER,
            at="2026-10-15T12:48:00Z", expected_revision=self.log.read().revision,
        )
        self.assertEqual(len(saved["finding_ids"]), 1)
        review = _review(self.log, self.registry)
        self.assertEqual(review["questions"]["paid-the-interest"]["answer"], "yes")
        self.assertEqual(sum(row["state"] == "answered" for row in review["questions"].values()), 1)
        self.assertTrue(all(
            review["questions"][question]["state"] == "absent"
            for question in BASE_ANSWERS if question != "paid-the-interest"
        ))

    def test_direct_save_revalidates_the_expected_revision_and_reused_answers_refuse(self) -> None:
        keys = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
        revision = self.log.read().revision
        saved = record_f1098_statement_answers_durably(
            self.log, self.registry, statement_keys=keys, answers=BASE_ANSWERS,
            submission_id="demo.f1098.direct", evidence_ids=_evidence_ids(BASE_ANSWERS), actor=USER,
            at="2026-10-15T12:40:00Z", expected_revision=revision,
        )
        self.assertEqual(len(saved["finding_ids"]), 9)
        with self.assertRaises(F1098RecordingRefused):
            record_f1098_statement_answers_durably(
                self.log, self.registry, statement_keys=keys, answers=BASE_ANSWERS,
                submission_id="demo.f1098.reused", evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.f1098.evidence.second"),
                actor=USER, at="2026-10-15T12:41:00Z", expected_revision=self.log.read().revision,
            )

    def test_direct_save_refuses_multiple_current_statements_even_with_exact_first_keys(self) -> None:
        multi = ActLog(Path(self.temp.name) / "multi-workspace", self.registry)
        from tests.test_f1098_statement_review import _base_acts
        multi.append_batch(_base_acts(second_interest=5000), expected_revision=0)
        before = multi.read()
        with self.assertRaises(F1098RecordingRefused):
            record_f1098_statement_answers_durably(
                multi, self.registry,
                statement_keys={"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"},
                answers=BASE_ANSWERS, submission_id="demo.f1098.multiple-direct",
                evidence_ids=_evidence_ids(BASE_ANSWERS), actor=USER, at="2026-10-15T12:41:30Z",
                expected_revision=before.revision,
            )
        self.assertEqual(multi.read().revision, before.revision)

    def test_evidence_records_normalized_answer_and_statement_identity(self) -> None:
        _save(self.log, self.registry, BASE_ANSWERS, "demo.f1098.evidence-shape")
        saved_evidence = [row["payload"]["evidence"] for row in self.log.read().acts
                          if row["kind"] == "evidence-submitted"]
        payment = next(row for row in saved_evidence if row["content"]["question"].endswith("paid-the-interest"))
        self.assertEqual(payment["kind"], "tax.mortgage.f1098-statement-answer")
        self.assertEqual(payment["content"]["submission_id"], "demo.f1098.evidence-shape")
        self.assertEqual(payment["content"]["answer"], "yes")
        self.assertEqual(payment["content"]["statement"], {
            "payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025",
        })

    def test_public_withdrawal_rejects_non_answer_and_reused_submission_identity(self) -> None:
        _save(self.log, self.registry, BASE_ANSWERS, "demo.f1098.identity-start")
        state = project(self.log.read().acts, self.registry)
        current = compute_currency(state).current_finding_ids
        lattice = facts_of(state.fact_state, include_displaced=True)
        unrelated = next(fid for fid, finding in state.findings.items() if fid in current
                         and not lattice[finding["fact_id"]].fact_type_id.startswith("tax.us.2025.f1098."))
        revision = self.log.read().revision
        with self.assertRaises(F1098RecordingRefused):
            withdraw_f1098_statement_answer_durably(
                self.log, self.registry, current_findings=[unrelated], submission_id="demo.f1098.bad-withdraw",
                actor=USER, at="2026-10-15T12:42:00Z", expected_revision=revision,
            )
        self.assertEqual(self.log.read().revision, revision)
        keys = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
        review = __import__("tests.test_f1098_statement_review", fromlist=["_review"])._review(self.log, self.registry)
        from packages.tax.f1098_statement_review import correct_f1098_statement_review_answer
        correct_f1098_statement_review_answer(
            self.log, self.registry, review, question="paid-the-interest", answer="no",
            submission_id="demo.f1098.reused-submission", evidence_id="demo.f1098.reused-submission.first",
            actor=USER, at="2026-10-15T12:43:00Z",
        )
        current_review = __import__("tests.test_f1098_statement_review", fromlist=["_review"])._review(self.log, self.registry)
        with self.assertRaises(F1098RecordingRefused):
            correct_f1098_statement_answer_durably(
                self.log, self.registry, statement_keys=keys, question="home-is-collateral", answer="no",
                predecessor_finding_id=current_review["questions"]["home-is-collateral"]["finding_id"],
                submission_id="demo.f1098.reused-submission", evidence_id="demo.f1098.reused-submission.second",
                actor=USER, at="2026-10-15T12:44:00Z", expected_revision=self.log.read().revision,
            )
