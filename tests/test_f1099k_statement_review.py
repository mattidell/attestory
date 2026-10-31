"""Track 2 Form 1099-K review snapshot, atomic recording, and saved run association."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
import unittest
from unittest.mock import patch
import pytest

from packages.derivation.live import LiveCoordinatorOutcome, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    record_f1099k_no_statements_durably,
    record_f1099k_statement_answers_durably,
    record_f1099k_statement_durably,
)
from packages.tax.f1099k_statement_review import (
    F1099KReviewRefused,
    answer_f1099k_statement_review_question,
    associate_saved_run,
    correct_f1099k_statement_review_answer,
    prepare_f1099k_statement_review,
    review_f1099k_statement_with_saved_presentation,
    save_f1099k_statement_review,
    withdraw_f1099k_statement_review_answers,
)
from packages.tax.loader import tax_registry
from tests.test_f1099k_personal_item_sale_track1 import (
    ROOT,
    SCOPE,
    SURFACE,
    SURFACE_V45,
    TOP_ENTRY_SYMBOL,
    UNRESOLVED_SYMBOL,
    USER,
    _finish_acts,
    _finish_acts_v45,
    _make_base_acts,
)
from tests.test_f1099k_statement_recording import BASE_ANSWERS, PAYER, STMT, _evidence_ids


def _seed_workspace(log: ActLog) -> None:
    seed_acts = _finish_acts(_make_base_acts())
    log.append_batch(seed_acts, expected_revision=0)


def _run_workspace(
    capability: WorkspaceCapability,
    log: ActLog,
    run_id: str,
) -> LiveCoordinatorOutcome:
    contents = log.read()
    return live_coordinate_run(
        capability,
        repo_root=ROOT,
        authoritative_acts=contents.acts,
        workspace_revision=contents.revision,
        run_scope=SCOPE,
        scope_user=USER,
        request={"schema": "run-request.v1"},
        run_id=run_id,
        governance_pins=[],
        surface=SURFACE,
        output_name=f"{run_id}.json",
    )


def _seed_workspace_v45(log: ActLog) -> None:
    seed_acts = _finish_acts_v45(_make_base_acts())
    log.append_batch(seed_acts, expected_revision=0)


def _run_workspace_v45(
    capability: WorkspaceCapability,
    log: ActLog,
    run_id: str,
) -> LiveCoordinatorOutcome:
    contents = log.read()
    return live_coordinate_run(
        capability,
        repo_root=ROOT,
        authoritative_acts=contents.acts,
        workspace_revision=contents.revision,
        run_scope=SCOPE,
        scope_user=USER,
        request={"schema": "run-request.v1"},
        run_id=run_id,
        governance_pins=[],
        surface=SURFACE_V45,
        output_name=f"{run_id}.json",
    )


class F1099KStatementReviewUnitTests(unittest.TestCase):
    """Direct unit tests for Form 1099-K review preparation, save, correction, and withdrawal."""

    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1099k-review-unit-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)
        _seed_workspace(self.log)
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.stmt",
            evidence_id="demo.f1099k.ev.stmt",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        self.stmt_keys = stmt_res["statement_keys"]

    def test_review_preparation_and_human_labels(self) -> None:
        review = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.1",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=self.stmt_keys,
        )
        self.assertEqual(review["statement"]["payerLabel"], "Synthetic platform")
        self.assertEqual(review["statement"]["taxYear"], "2025")
        self.assertEqual(review["statement"]["box1a"], 880.0)
        self.assertEqual(review["statement"]["box4"], 0.0)
        self.assertEqual(len(review["questions"]), 15)

        # Check categorical question labels
        q1 = review["questions"]["covers-only-single-item"]
        self.assertEqual(q1["kind"], "categorical")
        self.assertIn("single item sale", q1["question"])
        self.assertEqual(q1["state"], "absent")
        self.assertEqual(q1["label"], "Not answered")
        self.assertIn("yes", q1["labels"])
        self.assertIn("cannot-tell", q1["labels"])

        # Check numeric question labels
        q_price = review["questions"]["agreed-item-price"]
        self.assertEqual(q_price["kind"], "amount")
        self.assertIn("agreed sale price", q_price["question"])
        self.assertEqual(q_price["state"], "absent")

    def test_atomic_save_of_review_answers(self) -> None:
        review = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.save",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=self.stmt_keys,
        )
        before_rev = self.log.read().revision
        evidence_ids = _evidence_ids(BASE_ANSWERS)
        saved = save_f1099k_statement_review(
            self.log,
            self.registry,
            review,
            answers=BASE_ANSWERS,
            submission_id="demo.f1099k.sub.all",
            evidence_ids=evidence_ids,
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        self.assertEqual(len(saved["finding_ids"]), 15)
        self.assertGreater(saved["revision"], before_rev)

        fresh_review = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.fresh",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=self.stmt_keys,
        )
        for q_name in BASE_ANSWERS:
            q_info = fresh_review["questions"][q_name]
            self.assertEqual(q_info["state"], "answered")
            self.assertIsNotNone(q_info["finding_id"])

    def test_atomic_save_interrupted_leaves_log_clean(self) -> None:
        review = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.interrupt",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=self.stmt_keys,
        )
        before_bytes = self.log.path.read_bytes()
        before_rev = self.log.read().revision

        with patch("packages.kernel.act_log.os.replace", side_effect=OSError("simulated interruption")):
            with self.assertRaises(OSError):
                save_f1099k_statement_review(
                    self.log,
                    self.registry,
                    review,
                    answers=BASE_ANSWERS,
                    submission_id="demo.f1099k.sub.interrupt",
                    evidence_ids=_evidence_ids(BASE_ANSWERS),
                    actor=USER,
                    at="2026-10-16T12:02:00Z",
                )
        self.assertEqual(self.log.path.read_bytes(), before_bytes)
        self.assertEqual(self.log.read().revision, before_rev)

    def test_tampered_review_question_or_choice_refused(self) -> None:
        review = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.tamper",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=self.stmt_keys,
        )
        bad_answers = dict(BASE_ANSWERS)
        bad_answers["covers-only-single-item"] = "unsupported-choice"
        with self.assertRaises(F1099KReviewRefused):
            save_f1099k_statement_review(
                self.log,
                self.registry,
                review,
                answers=bad_answers,
                submission_id="demo.f1099k.sub.bad-choice",
                evidence_ids=_evidence_ids(bad_answers),
                actor=USER,
                at="2026-10-16T12:02:00Z",
            )

        with self.assertRaises(F1099KReviewRefused):
            answer_f1099k_statement_review_question(
                self.log,
                self.registry,
                review,
                question="unknown-question-name",
                answer="yes",
                submission_id="demo.f1099k.sub.unknown-q",
                evidence_id="demo.f1099k.ev.unknown-q",
                actor=USER,
                at="2026-10-16T12:03:00Z",
            )

    def test_review_answer_and_correction_and_withdrawal(self) -> None:
        review = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.ops",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=self.stmt_keys,
        )
        # Single answer
        ans = answer_f1099k_statement_review_question(
            self.log,
            self.registry,
            review,
            question="covers-only-single-item",
            answer="yes",
            submission_id="demo.f1099k.sub.q1",
            evidence_id="demo.f1099k.ev.q1",
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        self.assertEqual(len(ans["finding_ids"]), 1)
        rev2 = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.ops2",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=self.stmt_keys,
        )
        self.assertEqual(rev2["questions"]["covers-only-single-item"]["state"], "answered")

        # Correction
        corr = correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            rev2,
            question="covers-only-single-item",
            answer="no",
            submission_id="demo.f1099k.sub.q1-corr",
            evidence_id="demo.f1099k.ev.q1-corr",
            actor=USER,
            at="2026-10-16T12:04:00Z",
        )
        self.assertEqual(len(corr["finding_ids"]), 1)
        rev3 = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.ops3",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=self.stmt_keys,
        )
        self.assertEqual(rev3["questions"]["covers-only-single-item"]["answer"], "no")

        # Withdrawal
        withdraw_f1099k_statement_review_answers(
            self.log,
            self.registry,
            rev3,
            questions=["covers-only-single-item"],
            submission_id="demo.f1099k.sub.q1-w",
            actor=USER,
            at="2026-10-16T12:06:00Z",
        )
        rev4 = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.ops4",
            shown_at="2026-10-16T12:07:00Z",
            statement_keys=self.stmt_keys,
        )
        self.assertEqual(rev4["questions"]["covers-only-single-item"]["state"], "absent")


@pytest.mark.live(reason="derivation runs through live_coordinate_run exceed fast-lane budget")
class F1099KStatementReviewLiveDerivationTests(unittest.TestCase):
    """End-to-end derivation checks covering all 12 chartered cases plus saved run association."""

    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1099k-live-derivation-")
        self.addCleanup(self.temp.cleanup)
        self.ws_dir = Path(self.temp.name) / "workspace"
        self.capability = WorkspaceCapability(self.ws_dir)
        self.registry = tax_registry()
        self.log = ActLog(self.ws_dir, self.registry)
        _seed_workspace(self.log)
        self.records = RecordStream(self.ws_dir / "records", DerivationSchemas())

    def _record_loss_statement(self, box1a: float = 880.0) -> dict[str, str]:
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=box1a,
            box4=0.0,
            submission_id="demo.f1099k.sub.stmt",
            evidence_id="demo.f1099k.ev.stmt",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = stmt_res["statement_keys"]
        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=stmt_keys,
            answers=BASE_ANSWERS,
            submission_id="demo.f1099k.sub.answers",
            evidence_ids=_evidence_ids(BASE_ANSWERS),
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=self.log.read().revision,
        )
        return cast(dict[str, str], stmt_keys)

    def test_case1_record_statement_and_all_answers_for_loss(self) -> None:
        """Case 1: Record statement + all answers for a loss -> supported loss; top entry = Box 1a; review labels."""
        stmt_keys = self._record_loss_statement()
        outcome = _run_workspace(self.capability, self.log, "case1-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case1.rev",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-supported-loss")
        self.assertIsNotNone(review["savedCalculation"])
        calc = review["savedCalculation"]
        self.assertEqual(calc["status"], "supported-loss")
        self.assertEqual(calc["box1a"], 880.0)
        self.assertIn("nondeductible personal loss", calc["sentence"])

        # Check publications: top entry equals Box 1a
        pubs = [p.finding for p in (outcome.publications or ())]
        top_pub = next(p for p in pubs if p.get("symbol") == TOP_ENTRY_SYMBOL)
        self.assertEqual(float(str(top_pub.get("value"))), 880.0)

    def test_case2_no_form_1099k_on_schedule1_return(self) -> None:
        """Case 2: 'No Form 1099-K' on a Schedule 1 return -> top entry 0; Schedule 1 result as without route."""
        record_f1099k_no_statements_durably(
            self.log,
            self.registry,
            submission_id="demo.case2.no-1099k",
            evidence_id="demo.case2.no-1099k.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        outcome = _run_workspace(self.capability, self.log, "case2-run")
        self.assertIsNone(outcome.refusal)

        pubs = [p.finding for p in (outcome.publications or ())]
        top_pub = next(p for p in pubs if p.get("symbol") == TOP_ENTRY_SYMBOL)
        self.assertEqual(str(top_pub.get("value")), "0")

    def test_case3_correct_cost_across_loss_gain_boundary(self) -> None:
        """Case 3: Correct cost across the loss/gain boundary -> unsupported-gain; history keeps both answers."""
        stmt_keys = self._record_loss_statement()
        rev_before = prepare_f1099k_statement_review(
            self.log, self.registry, review_id="demo.case3.rev1", shown_at="2026-10-16T12:02:00Z",
            statement_keys=stmt_keys,
        )
        # Correct purchase cost from 1000.0 to 500.0 (price 800 - cost 500 -> gain)
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            rev_before,
            question="purchase-cost",
            answer=500.0,
            submission_id="demo.case3.corr-cost",
            evidence_id="demo.case3.corr-cost.ev",
            actor=USER,
            at="2026-10-16T12:03:00Z",
        )
        # Verify history preserves both answers
        state = project(self.log.read().acts, self.registry)
        cost_findings = [f for f in state.findings.values() if "purchase-cost" in f["fact_id"]]
        self.assertEqual(len(cost_findings), 2)
        values = sorted(f["value"] for f in cost_findings)
        self.assertEqual(values, [500.0, 1000.0])

        outcome = _run_workspace(self.capability, self.log, "case3-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case3.rev2",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        self.assertIsNotNone(review["savedUnresolvedExplanation"])
        unres = review["savedUnresolvedExplanation"]
        self.assertTrue(any("gain or profit" in s for s in unres["reasonSentences"]))
        self.assertIn("does not yet account for this Form 1099-K", unres["incomeSentence"])

    def test_case4_withdraw_personal_use_answer(self) -> None:
        """Case 4: Withdraw the personal-use answer -> personal-use-unconfirmed; nothing entered."""
        stmt_keys = self._record_loss_statement()
        rev = prepare_f1099k_statement_review(
            self.log, self.registry, review_id="demo.case4.rev1", shown_at="2026-10-16T12:02:00Z",
            statement_keys=stmt_keys,
        )
        withdraw_f1099k_statement_review_answers(
            self.log,
            self.registry,
            rev,
            questions=["exclusive-personal-use"],
            submission_id="demo.case4.withdraw-use",
            actor=USER,
            at="2026-10-16T12:03:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "case4-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        # Verify nothing entered at top entry
        pubs = [p.finding for p in (outcome.publications or ())]
        top_pubs = [p for p in pubs if p.get("symbol") == TOP_ENTRY_SYMBOL]
        self.assertEqual(len(top_pubs), 0)

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case4.rev2",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        unres = review["savedUnresolvedExplanation"]
        self.assertTrue(any("exclusive personal use has no current answer" in s for s in unres["reasonSentences"]))

    def test_case5_withdraw_an_amount(self) -> None:
        """Case 5: Withdraw an amount -> that amount's unanswered stop."""
        stmt_keys = self._record_loss_statement()
        rev = prepare_f1099k_statement_review(
            self.log, self.registry, review_id="demo.case5.rev1", shown_at="2026-10-16T12:02:00Z",
            statement_keys=stmt_keys,
        )
        withdraw_f1099k_statement_review_answers(
            self.log,
            self.registry,
            rev,
            questions=["platform-fees"],
            submission_id="demo.case5.withdraw-fees",
            actor=USER,
            at="2026-10-16T12:03:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "case5-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case5.rev2",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        unres = review["savedUnresolvedExplanation"]
        self.assertTrue(any("platform selling fees has no current answer" in s for s in unres["reasonSentences"]))

    def test_case6_answer_cannot_tell_for_an_amount(self) -> None:
        """Case 6: Answer 'I can't tell' for an amount -> that amount's can't-tell stop."""
        stmt_keys = self._record_loss_statement()
        rev = prepare_f1099k_statement_review(
            self.log, self.registry, review_id="demo.case6.rev1", shown_at="2026-10-16T12:02:00Z",
            statement_keys=stmt_keys,
        )
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            rev,
            question="purchase-cost",
            answer="cannot-tell",
            submission_id="demo.case6.cant-tell-cost",
            evidence_id="demo.case6.cant-tell-cost.ev",
            actor=USER,
            at="2026-10-16T12:03:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "case6-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case6.rev2",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        unres = review["savedUnresolvedExplanation"]
        self.assertTrue(any("original purchase cost of the item is unknown" in s for s in unres["reasonSentences"]))

    def test_case7_corrected_statement_reconciliation_stop(self) -> None:
        """Case 7: Corrected statement with different Box 1a, answers unchanged -> reconciliation stop."""
        stmt_keys = self._record_loss_statement(box1a=880.0)
        # Correct Box 1a to 950.0 (reconciliation mismatch: 800 price + 24 ship + 56 tax = 880 != 950)
        record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=950.0,
            box4=0.0,
            corrected=True,
            submission_id="demo.case7.corr-stmt",
            evidence_id="demo.case7.corr-stmt.ev",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=self.log.read().revision,
        )
        outcome = _run_workspace(self.capability, self.log, "case7-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case7.rev",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        unres = review["savedUnresolvedExplanation"]
        self.assertTrue(any("does not reconcile with the item price" in s for s in unres["reasonSentences"]))

    def test_case8_second_statement_multiple_statement_stop(self) -> None:
        """Case 8: Second statement recorded -> multiple-statement stop."""
        stmt_keys = self._record_loss_statement()
        # Record second statement from platform B
        record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id="demo.platform.b",
            statement_ref="demo.stmt.b",
            box1a=350.0,
            box4=0.0,
            submission_id="demo.case8.stmt2",
            evidence_id="demo.case8.stmt2.ev",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=self.log.read().revision,
        )
        outcome = _run_workspace(self.capability, self.log, "case8-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case8.rev",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        unres = review["savedUnresolvedExplanation"]
        self.assertTrue(any("More than one Form 1099-K statement was received" in s for s in unres["reasonSentences"]))

    def test_case9_statement_recorded_after_no_1099k(self) -> None:
        """Case 9: Statement recorded after 'no Form 1099-K' -> entry unpublished until answered."""
        # 1. Record no Form 1099-K
        record_f1099k_no_statements_durably(
            self.log,
            self.registry,
            submission_id="demo.case9.no-stmts",
            evidence_id="demo.case9.no-stmts.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        run1 = _run_workspace(self.capability, self.log, "case9-run1")
        self.assertIsNone(run1.refusal)
        top1 = next(p for p in (run1.publications or ()) if p.finding.get("symbol") == TOP_ENTRY_SYMBOL)
        self.assertEqual(str(top1.finding.get("value")), "0")

        # 2. Record statement afterwards
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.case9.new-stmt",
            evidence_id="demo.case9.new-stmt.ev",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = stmt_res["statement_keys"]
        # Statement is recorded, but questions have not yet been answered
        run2 = _run_workspace(self.capability, self.log, "case9-run2")
        self.assertIsNone(run2.refusal)
        # Entry unpublished: not present in publications
        top_pubs2 = [p for p in (run2.publications or ()) if p.finding.get("symbol") == TOP_ENTRY_SYMBOL]
        self.assertEqual(len(top_pubs2), 0)

        # 3. Answer questions
        record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=stmt_keys,
            answers=BASE_ANSWERS,
            submission_id="demo.case9.answers",
            evidence_ids=_evidence_ids(BASE_ANSWERS),
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=self.log.read().revision,
        )
        run3 = _run_workspace(self.capability, self.log, "case9-run3")
        self.assertIsNone(run3.refusal)
        top3 = next(p for p in (run3.publications or ()) if p.finding.get("symbol") == TOP_ENTRY_SYMBOL)
        self.assertEqual(float(str(top3.finding.get("value"))), 880.0)

    def test_case12_unrelated_w2_untouched_through_changes(self) -> None:
        """Case 12: Unrelated W-2 recorded alongside -> W-2 findings untouched through every change."""
        initial_state = project(self.log.read().acts, self.registry)
        w2_finding = next(
            f for f in initial_state.findings.values()
            if "tax.us.2025.w2.box1-wages" in f["fact_id"]
        )
        w2_fid = w2_finding["id"]
        w2_val = w2_finding["value"]
        self.assertEqual(w2_val, 90000.0)

        # 1. Record statement
        stmt_keys = self._record_loss_statement()
        state1 = project(self.log.read().acts, self.registry)
        self.assertIn(w2_fid, compute_currency(state1).current_finding_ids)
        self.assertEqual(state1.findings[w2_fid]["value"], w2_val)

        # 2. Correct an answer
        rev = prepare_f1099k_statement_review(
            self.log, self.registry, review_id="demo.case12.rev1", shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        correct_f1099k_statement_review_answer(
            self.log, self.registry, rev, question="purchase-cost", answer=500.0,
            submission_id="demo.case12.corr", evidence_id="demo.case12.corr.ev",
            actor=USER, at="2026-10-16T12:04:00Z",
        )
        state2 = project(self.log.read().acts, self.registry)
        self.assertIn(w2_fid, compute_currency(state2).current_finding_ids)
        self.assertEqual(state2.findings[w2_fid]["value"], w2_val)

        # 3. Withdraw an answer
        rev2 = prepare_f1099k_statement_review(
            self.log, self.registry, review_id="demo.case12.rev2", shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        withdraw_f1099k_statement_review_answers(
            self.log, self.registry, rev2, questions=["platform-fees"],
            submission_id="demo.case12.w", actor=USER, at="2026-10-16T12:06:00Z",
        )
        state3 = project(self.log.read().acts, self.registry)
        self.assertIn(w2_fid, compute_currency(state3).current_finding_ids)
        self.assertEqual(state3.findings[w2_fid]["value"], w2_val)

    def test_case13_saved_run_recalculation_needed_on_correction(self) -> None:
        """Case 13: Saved run, then a correction -> recalculation-needed."""
        stmt_keys = self._record_loss_statement()
        outcome = _run_workspace(self.capability, self.log, "case13-run1")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review1 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case13.rev1",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review1["calculationAssociation"]["state"], "current")
        self.assertEqual(review1["savedCalculationState"], "current-supported-loss")

        # Correct an answer
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            review1,
            question="purchase-cost",
            answer=500.0,
            submission_id="demo.case13.corr",
            evidence_id="demo.case13.corr.ev",
            actor=USER,
            at="2026-10-16T12:06:00Z",
        )

        # Re-check saved presentation without running coordinator: must report recalculation-needed!
        review2 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.case13.rev2",
            shown_at="2026-10-16T12:07:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review2["calculationAssociation"]["state"], "recalculation-needed")
        self.assertEqual(review2["savedCalculationState"], "recalculation-needed")
        self.assertIsNone(review2["savedCalculation"])

    def test_shipping_question_to_recorded_value_discriminating_example(self) -> None:
        """Question to recorded value to result for seller-received shipping."""
        # Statement: Box 1a = 900.0 ($800 price + $100 buyer shipping), Box 4 = 0.0
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=900.0,
            box4=0.0,
            submission_id="demo.shipping.stmt",
            evidence_id="demo.shipping.stmt.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = stmt_res["statement_keys"]
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.shipping.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )

        # Assert question/help text for seller-paid-shipping states what to include
        q_ship = rev["questions"]["seller-paid-shipping"]
        self.assertIn("postage", q_ship["question"].lower() + q_ship["help"].lower())
        self.assertIn("bought with shipping money", q_ship["help"].lower())

        # An honest seller records the $20 label bought with the buyer's shipping money
        answers_supported = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 800.0,
            "shipping-arrangement": "seller-received-shipping",
            "platform-fees": 0.0,
            "seller-paid-shipping": 20.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 100.0,
            "purchase-cost": 890.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev,
            answers=answers_supported,
            submission_id="demo.shipping.ans",
            evidence_ids=_evidence_ids(answers_supported, prefix="demo.shipping.ev"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome1 = _run_workspace(self.capability, self.log, "shipping-loss-run")
        self.assertIsNone(outcome1.refusal)
        assert outcome1.presentation_path is not None

        review1 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome1.presentation_path,
            self.records,
            review_id="demo.shipping.rev1",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review1["savedCalculationState"], "current-supported-loss")
        self.assertIsNotNone(review1["savedCalculation"])
        self.assertEqual(review1["savedCalculation"]["box1a"], 900.0)
        self.assertIn("nondeductible personal loss", review1["savedCalculation"]["sentence"])

        # Show that recording $0 instead gives the gain stop, so the test can discriminate
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            review1,
            question="seller-paid-shipping",
            answer=0.0,
            submission_id="demo.shipping.corr.zero",
            evidence_id="demo.shipping.corr.zero.ev",
            actor=USER,
            at="2026-10-16T12:04:00Z",
        )
        outcome2 = _run_workspace(self.capability, self.log, "shipping-gain-run")
        self.assertIsNone(outcome2.refusal)
        assert outcome2.presentation_path is not None

        review2 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome2.presentation_path,
            self.records,
            review_id="demo.shipping.rev2",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review2["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review2["savedState"], "actually-unresolved")
        self.assertIsNotNone(review2["savedUnresolvedExplanation"])
        self.assertTrue(any("gain or profit" in s for s in review2["savedUnresolvedExplanation"]["reasonSentences"]))

    def test_shipping_pass_through_supported_loss(self) -> None:
        """The same figures under platform pass-through still give the supported loss result."""
        # Price: 800.0, Buyer shipping: 100.0, Box 1a: 900.0, Purchase cost: 890.0
        # Platform kept shipping and supplied label -> seller paid 0.0
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=900.0,
            box4=0.0,
            submission_id="demo.pt.stmt",
            evidence_id="demo.pt.stmt.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = stmt_res["statement_keys"]
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.pt.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        # Verify the question does not ask the person to report the platform's label as their expense
        q_ship = rev["questions"]["seller-paid-shipping"]
        self.assertIn("do not include", q_ship["help"].lower())
        self.assertIn("provided and kept by the platform", q_ship["help"].lower())

        answers_pt = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 800.0,
            "shipping-arrangement": "platform-pass-through",
            "platform-fees": 0.0,
            "seller-paid-shipping": 0.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 100.0,
            "purchase-cost": 890.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev,
            answers=answers_pt,
            submission_id="demo.pt.ans",
            evidence_ids=_evidence_ids(answers_pt, prefix="demo.pt.ev"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "pt-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.pt.rev.outcome",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-supported-loss")
        self.assertIsNotNone(review["savedCalculation"])
        self.assertEqual(review["savedCalculation"]["box1a"], 900.0)
        self.assertIn("nondeductible personal loss", review["savedCalculation"]["sentence"])
        self.assertIsNone(review["savedUnresolvedExplanation"])

    def test_classification_supported_zero_admitted_statement(self) -> None:
        """An admitted $0 statement publishes supported-loss and is classified as supported zero."""
        # Statement with Box 1a = 0.0
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=0.0,
            box4=0.0,
            submission_id="demo.zero.stmt",
            evidence_id="demo.zero.stmt.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = stmt_res["statement_keys"]
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.zero.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        answers_zero = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 0.0,
            "shipping-arrangement": "none",
            "platform-fees": 0.0,
            "seller-paid-shipping": 0.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 0.0,
            "purchase-cost": 100.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev,
            answers=answers_zero,
            submission_id="demo.zero.ans",
            evidence_ids=_evidence_ids(answers_zero, prefix="demo.zero.ev"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "zero-stmt-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.zero.rev.outcome",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        # Saved state and wording - follows recorded outcome supported-loss (not amount > 0 proxy)
        self.assertEqual(review["savedCalculationState"], "current-supported-loss")
        self.assertEqual(review["savedState"], "supported-loss")
        self.assertIsNotNone(review["savedCalculation"])
        calc = review["savedCalculation"]
        self.assertEqual(calc["status"], "supported-loss")
        self.assertEqual(calc["box1a"], 0.0)
        self.assertEqual(calc["assumptions"], "none")
        self.assertIsNotNone(calc["computation"])
        self.assertIn("nondeductible personal loss", calc["sentence"])
        # No income warning
        self.assertIsNone(review["savedUnresolvedExplanation"])

    def test_classification_closed_empty_zero(self) -> None:
        """Closed-empty zero: the person said no Form 1099-K, so there is no statement and a $0 entry."""
        record_f1099k_no_statements_durably(
            self.log,
            self.registry,
            submission_id="demo.ce.no-stmts",
            evidence_id="demo.ce.no-stmts.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        outcome = _run_workspace(self.capability, self.log, "ce-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.ce.rev",
            shown_at="2026-10-16T12:01:00Z",
        )
        # Saved state and wording
        self.assertEqual(review["savedCalculationState"], "current-closed-empty-zero")
        self.assertEqual(review["savedState"], "closed-empty-zero")
        self.assertIsNotNone(review["savedCalculation"])
        calc = review["savedCalculation"]
        self.assertEqual(calc["status"], "closed-empty-zero")
        self.assertEqual(calc["box1a"], 0.0)
        self.assertIn("No Form 1099-K statements were received for 2025", calc["sentence"])
        # No income warning
        self.assertIsNone(review["savedUnresolvedExplanation"])

    def test_classification_missing_output(self) -> None:
        """Missing output: no top-entry or reason result in the saved run; neither supported nor unresolved."""
        stmt_keys = self._record_loss_statement()
        outcome = _run_workspace(self.capability, self.log, "missing-out-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        # Historical v1 permits a coherent missing-output view; a v2 file with
        # a stale root map is independently rejected by the saved-loader tests.
        from packages.derivation.presentation_projection import project_presentation_v1
        model = project_presentation_v1(json.loads(outcome.presentation_path.read_text("utf-8")))
        model["sections"] = [
            s for s in model["sections"]
            if (s.get("field") or {}).get("id") not in (
                "tax.us.2025.schedule1.top-entry.form-field",
                "tax.us.2025.form.f1099k.unresolved.form-field",
            )
        ]
        missing_p_path = Path(self.temp.name) / "missing.presentation.json"
        missing_p_path.write_text(json.dumps(model), encoding="utf-8")

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            missing_p_path,
            self.records,
            review_id="demo.missing.rev",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        # Saved state and wording
        self.assertEqual(review["savedCalculationState"], "current-missing-output")
        self.assertEqual(review["savedState"], "missing-output")
        self.assertIsNone(review["savedCalculation"])
        self.assertIsNone(review["savedUnresolvedExplanation"])
        self.assertIsNotNone(review["savedMissingOutput"])
        self.assertIn("No Form 1099-K top-entry or reason result", review["savedMissingOutput"]["sentence"])

    def test_classification_actually_unresolved(self) -> None:
        """Actually unresolved: a named stop with its reason sentence and the income sentence."""
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.unres.stmt",
            evidence_id="demo.unres.stmt.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = stmt_res["statement_keys"]
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.unres.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        # Answers that trigger unsupported gain ($800 price > $500 cost)
        answers_gain = copy.deepcopy(BASE_ANSWERS)
        answers_gain["purchase-cost"] = 500.0
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev,
            answers=answers_gain,
            submission_id="demo.unres.ans",
            evidence_ids=_evidence_ids(answers_gain, prefix="demo.unres.ev"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "unres-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.unres.rev.outcome",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        # Saved state and wording
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review["savedState"], "actually-unresolved")
        self.assertIsNone(review["savedCalculation"])
        self.assertIsNotNone(review["savedUnresolvedExplanation"])
        unres = review["savedUnresolvedExplanation"]
        self.assertTrue(any("gain or profit" in s for s in unres["reasonSentences"]))
        # Income warning appears only for the unresolved one
        self.assertIn("does not yet account for this Form 1099-K", unres["incomeSentence"])

    def test_box4_presented_as_supplied_by_person_or_none(self) -> None:
        """R4: Review presents Box 4 as what the person supplied, or None if absent."""
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id="demo.platform.box4test",
            statement_ref="stmt-box4",
            box1a=1000.0,
            box4=125.50,
            submission_id="demo.box4test.sub",
            evidence_id="demo.box4test.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = cast(dict[str, str], stmt_res["statement_keys"])
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.box4test.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(rev["statement"]["box4"], 125.50)
        self.assertIsNotNone(rev["statement"]["box4FindingId"])

        # Create workspace with Box 4 absent
        temp_dir = TemporaryDirectory(prefix="f1099k-nobox4-")
        self.addCleanup(temp_dir.cleanup)
        nobox4_ws = Path(temp_dir.name)
        nobox4_log = ActLog(nobox4_ws, self.registry)
        acts = list(self.log.read().acts)
        acts_no_box4 = [copy.deepcopy(a) for a in acts if "box4" not in str(a.get("payload", {}).get("finding", {}).get("fact_id", ""))]
        for idx, act in enumerate(acts_no_box4):
            act["committed_against"] = idx
        nobox4_log.append_batch(acts_no_box4, expected_revision=0)
        rev_nobox4 = prepare_f1099k_statement_review(
            nobox4_log,
            self.registry,
            review_id="demo.nobox4.rev",
            shown_at="2026-10-16T12:02:00Z",
            statement_keys=stmt_keys,
        )
        self.assertIsNone(rev_nobox4["statement"]["box4"])
        self.assertIsNone(rev_nobox4["statement"]["box4FindingId"])

    def test_owner_regression_platform_pass_through_additional_shipping(self) -> None:
        """Owner regression: platform pass-through with seller-paid shipping > 0.

        Exact figures:
        - item price: $900
        - purchase cost: $850
        - shipping arrangement: platform pass-through
        - buyer shipping: $100
        - additional seller-paid shipping: $100
        - platform fees: $0, platform sales tax: $0, refund: $0
        - Box 1a: $1,000, Box 4: $0
        """
        # 1. Discriminating proof on release v45:
        # Show that the same figures on release v45 gave the gain sentence.
        temp_dir_v45 = TemporaryDirectory(prefix="f1099k-v45-")
        self.addCleanup(temp_dir_v45.cleanup)
        ws_v45 = Path(temp_dir_v45.name)
        log_v45 = ActLog(ws_v45, self.registry)
        _seed_workspace_v45(log_v45)

        stmt_res_v45 = record_f1099k_statement_durably(
            log_v45,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=1000.0,
            box4=0.0,
            submission_id="demo.owner.v45.stmt",
            evidence_id="demo.owner.v45.stmt.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=log_v45.read().revision,
        )
        stmt_keys_v45 = cast(dict[str, str], stmt_res_v45["statement_keys"])
        rev_v45 = prepare_f1099k_statement_review(
            log_v45,
            self.registry,
            review_id="demo.owner.v45.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys_v45,
        )
        owner_answers = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 900.0,
            "shipping-arrangement": "platform-pass-through",
            "platform-fees": 0.0,
            "seller-paid-shipping": 100.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 100.0,
            "purchase-cost": 850.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        save_f1099k_statement_review(
            log_v45,
            self.registry,
            rev_v45,
            answers=owner_answers,
            submission_id="demo.owner.v45.ans",
            evidence_ids=_evidence_ids(owner_answers, prefix="demo.owner.v45.ev"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome_v45 = _run_workspace_v45(self.capability, log_v45, "owner-v45-run")
        self.assertIsNone(outcome_v45.refusal)
        assert outcome_v45.presentation_path is not None
        review_v45 = review_f1099k_statement_with_saved_presentation(
            log_v45,
            self.registry,
            outcome_v45.presentation_path,
            self.records,
            review_id="demo.owner.v45.outcome",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys_v45,
        )
        self.assertEqual(review_v45["savedCalculationState"], "current-unresolved-explanation")
        self.assertIsNotNone(review_v45["savedUnresolvedExplanation"])
        self.assertTrue(any("gain or profit" in s for s in review_v45["savedUnresolvedExplanation"]["reasonSentences"]))

        # 2. Owner regression on release v46:
        # Use the actual path: Track 2 recording operations, live_coordinate_run on release v46,
        # the saved presentation, and review reloaded from disk.
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=1000.0,
            box4=0.0,
            submission_id="demo.owner.v46.stmt",
            evidence_id="demo.owner.v46.stmt.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = cast(dict[str, str], stmt_res["statement_keys"])
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.owner.v46.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev,
            answers=owner_answers,
            submission_id="demo.owner.v46.ans",
            evidence_ids=_evidence_ids(owner_answers, prefix="demo.owner.v46.ev"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "owner-v46-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None

        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.owner.v46.outcome",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )

        assert outcome.publications is not None
        reason_pub = next(p for p in outcome.publications if p.finding.get("symbol", "").startswith("tax.us.2025.f1099k.statement-loss-reason"))
        self.assertEqual(reason_pub.finding.get("value"), "additional-seller-shipping-unsupported")

        # - there is no Schedule 1 top entry
        self.assertIsNone(review["savedCalculation"])
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review["savedState"], "actually-unresolved")

        # - the person's $100 answer is retained
        self.assertEqual(review["questions"]["seller-paid-shipping"]["answer"], 100.0)

        # - selling expenses and net proceeds are not-computed;
        # - amount realized $900 and adjusted basis $850 are shown
        unres = review["savedUnresolvedExplanation"]
        self.assertIsNotNone(unres)
        comp = unres["computation"]
        self.assertIsNotNone(comp)
        self.assertEqual(comp["sellingExpenses"], "not-computed")
        self.assertEqual(comp["netProceeds"], "not-computed")
        self.assertEqual(comp["amountRealized"], 900.0)
        self.assertEqual(comp["adjustedBasis"], 850.0)
        self.assertEqual(comp["expectedBox1aGrossAmount"], 1000.0)
        self.assertEqual(comp["comparison"], "not-computed")

        # - there is no gain, break-even or loss sentence
        self.assertFalse(any("gain or profit" in s for s in unres["reasonSentences"]))
        self.assertFalse(any("broke even" in s for s in unres["reasonSentences"]))
        self.assertFalse(any("nondeductible personal loss" in s for s in unres["reasonSentences"]))

        # - the named sentence and the income sentence are present
        named_sentence = "Shipping the person paid in addition to a platform-supplied label is not yet handled, so the route cannot tell whether the sale was a gain or a loss."
        self.assertTrue(any(named_sentence in s for s in unres["reasonSentences"]))
        self.assertIn("does not yet account for this Form 1099-K", unres["incomeSentence"])

    def test_correction_platform_pass_through_additional_shipping(self) -> None:
        """Correction in the owner regression workspace:
        - $100 -> $0 shipping: review says recalculation-needed.
        - Rerun gives genuine gain stop ($900 vs $850) with its figures.
        - Purchase cost -> $950 with shipping $0 gives supported loss with $1,000 entry.
        """
        # Setup owner regression workspace on v46
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=1000.0,
            box4=0.0,
            submission_id="demo.corr.stmt",
            evidence_id="demo.corr.stmt.ev",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = cast(dict[str, str], stmt_res["statement_keys"])
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.corr.rev",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        owner_answers = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 900.0,
            "shipping-arrangement": "platform-pass-through",
            "platform-fees": 0.0,
            "seller-paid-shipping": 100.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 100.0,
            "purchase-cost": 850.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev,
            answers=owner_answers,
            submission_id="demo.corr.ans",
            evidence_ids=_evidence_ids(owner_answers, prefix="demo.corr.ev"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "corr-init-run")
        assert outcome.presentation_path is not None
        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.corr.rev.init",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")

        # Step 1: Correct additional shipping from $100 to $0.
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            review,
            question="seller-paid-shipping",
            answer=0.0,
            submission_id="demo.corr.ship.zero",
            evidence_id="demo.corr.ship.zero.ev",
            actor=USER,
            at="2026-10-16T12:04:00Z",
        )
        # The review says recalculation-needed.
        review_recalc = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.corr.rev.recalc",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review_recalc["savedCalculationState"], "recalculation-needed")

        # Rerun then gives the genuine gain stop ($900 against $850) with its figures.
        outcome_gain = _run_workspace(self.capability, self.log, "corr-gain-run")
        assert outcome_gain.presentation_path is not None
        review_gain = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome_gain.presentation_path,
            self.records,
            review_id="demo.corr.rev.gain",
            shown_at="2026-10-16T12:06:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review_gain["savedCalculationState"], "current-unresolved-explanation")
        unres_gain = review_gain["savedUnresolvedExplanation"]
        self.assertIsNotNone(unres_gain)
        self.assertTrue(any("gain or profit" in s for s in unres_gain["reasonSentences"]))
        comp_gain = unres_gain["computation"]
        self.assertIsNotNone(comp_gain)
        self.assertEqual(comp_gain["amountRealized"], 900.0)
        self.assertEqual(comp_gain["sellingExpenses"], 0.0)
        self.assertEqual(comp_gain["netProceeds"], 900.0)
        self.assertEqual(comp_gain["adjustedBasis"], 850.0)
        self.assertEqual(comp_gain["expectedBox1aGrossAmount"], 1000.0)
        self.assertEqual(comp_gain["comparison"], "net proceeds > adjusted basis")

        # Step 2: Correcting purchase cost to $950 with shipping $0 gives a supported loss with the $1,000 entry.
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            review_gain,
            question="purchase-cost",
            answer=950.0,
            submission_id="demo.corr.cost.950",
            evidence_id="demo.corr.cost.950.ev",
            actor=USER,
            at="2026-10-16T12:07:00Z",
        )
        outcome_loss = _run_workspace(self.capability, self.log, "corr-loss-run")
        assert outcome_loss.presentation_path is not None
        review_loss = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome_loss.presentation_path,
            self.records,
            review_id="demo.corr.rev.loss",
            shown_at="2026-10-16T12:08:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review_loss["savedCalculationState"], "current-supported-loss")
        self.assertIsNotNone(review_loss["savedCalculation"])
        self.assertEqual(review_loss["savedCalculation"]["box1a"], 1000.0)
        self.assertIn("nondeductible personal loss", review_loss["savedCalculation"]["sentence"])
        comp_loss = review_loss["savedCalculation"]["computation"]
        self.assertIsNotNone(comp_loss)
        self.assertEqual(comp_loss["amountRealized"], 900.0)
        self.assertEqual(comp_loss["sellingExpenses"], 0.0)
        self.assertEqual(comp_loss["netProceeds"], 900.0)
        self.assertEqual(comp_loss["adjustedBasis"], 950.0)
        self.assertEqual(comp_loss["expectedBox1aGrossAmount"], 1000.0)
        self.assertEqual(comp_loss["comparison"], "net proceeds < adjusted basis")
