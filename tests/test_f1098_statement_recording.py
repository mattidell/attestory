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
from packages.kernel.facts import fact_id_for, facts_of
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

    def test_direct_save_accepts_exact_statement_among_multiple_current_statements(self) -> None:
        multi = ActLog(Path(self.temp.name) / "multi-workspace", self.registry)
        from tests.test_f1098_statement_review import _base_acts
        multi.append_batch(_base_acts(second_interest=5000), expected_revision=0)
        before = multi.read()
        saved = record_f1098_statement_answers_durably(
            multi, self.registry,
            statement_keys={"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"},
            answers=BASE_ANSWERS, submission_id="demo.f1098.multiple-direct",
            evidence_ids=_evidence_ids(BASE_ANSWERS), actor=USER, at="2026-10-15T12:41:30Z",
            expected_revision=before.revision,
        )
        self.assertEqual(len(saved["finding_ids"]), 9)
        self.assertEqual(saved["revision"], multi.read().revision)

    def test_direct_save_refuses_missing_exact_statement_among_multiple_current_statements(self) -> None:
        multi = ActLog(Path(self.temp.name) / "missing-exact-workspace", self.registry)
        from tests.test_f1098_statement_review import _base_acts
        multi.append_batch(_base_acts(second_interest=5000), expected_revision=0)
        before = multi.read()
        with self.assertRaises(F1098RecordingRefused):
            record_f1098_statement_answers_durably(
                multi, self.registry,
                statement_keys={"payer": "demo.f1098.lender.missing", "statement": "demo.f1098.stmt.missing", "tax-year": "2025"},
                answers=BASE_ANSWERS, submission_id="demo.f1098.missing-direct",
                evidence_ids=_evidence_ids(BASE_ANSWERS), actor=USER, at="2026-10-15T12:41:31Z",
                expected_revision=before.revision,
            )
        self.assertEqual(multi.read().revision, before.revision)

    def test_two_exact_reports_keep_independent_answers_when_one_is_corrected(self) -> None:
        multi = ActLog(Path(self.temp.name) / "independent-workspace", self.registry)
        from tests.test_f1098_statement_review import _base_acts
        multi.append_batch(_base_acts(second_interest=5000), expected_revision=0)
        keys_a = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
        keys_b = {"payer": "demo.f1098.lender.b", "statement": "demo.f1098.stmt.b", "tax-year": "2025"}
        saved_a = record_f1098_statement_answers_durably(
            multi, self.registry, statement_keys=keys_a, answers=BASE_ANSWERS,
            submission_id="demo.f1098.independent.a", evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.f1098.a"),
            actor=USER, at="2026-10-15T12:45:00Z", expected_revision=multi.read().revision)
        saved_b = record_f1098_statement_answers_durably(
            multi, self.registry, statement_keys=keys_b, answers=BASE_ANSWERS,
            submission_id="demo.f1098.independent.b", evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.f1098.b"),
            actor=USER, at="2026-10-15T12:46:00Z", expected_revision=multi.read().revision)
        before = project(multi.read().acts, self.registry)
        before_current = compute_currency(before).current_finding_ids
        b_fact_ids = {fact_id_for(f"tax.us.2025.f1098.{question}", tuple(sorted(keys_b.items())))
                      for question in BASE_ANSWERS}
        b_findings = {fid: row for fid, row in before.findings.items()
                      if fid in before_current and row["fact_id"] in b_fact_ids}
        b_evidence_ids = {evidence_id for row in b_findings.values() for evidence_id in row["evidence_ids"]}
        b_evidence = {evidence_id: before.evidence[evidence_id].evidence for evidence_id in b_evidence_ids}
        paid_fact_id = fact_id_for("tax.us.2025.f1098.paid-the-interest", tuple(sorted(keys_a.items())))
        paid_predecessor = next(fid for fid, row in before.findings.items()
                                if fid in before_current and row["fact_id"] == paid_fact_id)
        correct_f1098_statement_answer_durably(
            multi, self.registry, statement_keys=keys_a, question="paid-the-interest", answer="no",
            predecessor_finding_id=paid_predecessor, submission_id="demo.f1098.independent.a.correct",
            evidence_id="demo.f1098.independent.a.correct.evidence", actor=USER,
            at="2026-10-15T12:47:00Z", expected_revision=multi.read().revision)
        after = project(multi.read().acts, self.registry)
        after_current = compute_currency(after).current_finding_ids
        self.assertEqual(b_findings, {fid: row for fid, row in after.findings.items()
                                     if fid in after_current and row["fact_id"] in b_fact_ids})
        self.assertEqual(b_evidence, {evidence_id: after.evidence[evidence_id].evidence for evidence_id in b_evidence_ids})
        self.assertEqual(len(saved_a["finding_ids"]), 9)
        self.assertEqual(len(saved_b["finding_ids"]), 9)

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
