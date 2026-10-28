"""Same-state projection reuse inside mortgage and Form 1098 operations.

A returned durable state is compared with an independent ``project`` of the
acts actually written. Call counts wrap each module's own ``project`` binding
for one operation. Reuse is inside that operation: a public call that is not
given a projection still folds, and an append refreshes the next read.
"""
from __future__ import annotations

import unittest
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable
from unittest.mock import patch

import pytest

import packages.tax.f1098_statement_recording as f1098_recording
import packages.tax.mortgage_borrowing_recording as mortgage_recording
import packages.tax.mortgage_borrowing_review as mortgage_review
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from packages.tax.f1098_statement_recording import (
    BUNDLE_ID, F1098RecordingRefused, _ensure_bundle,
    answer_f1098_statement_answer_durably, correct_f1098_statement_answer_durably,
    record_f1098_statement_answers_durably, withdraw_f1098_statement_answer_durably,
)
from packages.tax.loader import load_mortgage_borrowing_bundle, tax_registry
from packages.tax.mortgage_borrowing_recording import (
    BUNDLE_ID as MORTGAGE_BUNDLE_ID, MortgageBorrowingRecordingRefused,
    correct_mortgage_borrowing_claim_durably, current_mortgage_payment_comparison_support,
    introduce_mortgage_borrowing_reference_durably, record_mortgage_borrowing_claim_durably,
    withdraw_mortgage_borrowing_claim_durably,
)
from packages.tax.mortgage_borrowing_review import prepare_mortgage_borrowing_review
from tests.test_f1098_statement_review import BASE_ANSWERS, USER, _append_seed, _evidence_ids

KEYS_A = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
KEYS_B = {"payer": "demo.f1098.lender.b", "statement": "demo.f1098.stmt.b", "tax-year": "2025"}


def _counted(modules: list[Any], call: Callable[[], Any]) -> tuple[Any, dict[str, list[int]]]:
    """Run ``call`` and record each wrapped module's ``project`` act counts."""
    calls: dict[str, list[int]] = {}
    with ExitStack() as stack:
        for module in modules:
            original = module.project
            name = module.__name__
            calls[name] = []

            def wrapped(acts: Any, registry: Any, *, _original: Any = original, _name: str = name) -> Any:
                calls[_name].append(len(tuple(acts)))
                return _original(acts, registry)

            stack.enter_context(patch.object(module, "project", wrapped))
        return call(), calls


def _bundle_count(acts: list[dict[str, Any]] | tuple[dict[str, Any], ...], bundle_id: str) -> int:
    return sum(
        1 for row in acts
        if row.get("kind") == "bundle-adoption"
        and row.get("payload", {}).get("bundle", {}).get("id") == bundle_id
    )


@pytest.mark.live(reason="durable Form 1098 and mortgage recording over a synthetic workspace exceeds the fast-lane budget")
class F1098ProjectionReuseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1098-projection-reuse-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)
        _append_seed(self.log)

    def _answer(self, question: str, answer: str, suffix: str) -> dict[str, Any]:
        return answer_f1098_statement_answer_durably(
            self.log, self.registry, statement_keys=KEYS_A, question=question, answer=answer,
            submission_id=f"demo.f1098.reuse.{suffix}", evidence_id=f"demo.f1098.reuse.{suffix}.evidence",
            actor=USER, at="2026-10-27T12:00:00Z", expected_revision=self.log.read().revision,
        )

    def test_ensure_bundle_matches_a_fresh_fold_after_append_and_without_one(self) -> None:
        staged = list(self.log.read().acts)
        before = len(staged)
        adopted = _ensure_bundle(staged, self.registry, USER, "2026-10-27T12:00:00Z", "demo.f1098.ensure")
        self.assertEqual(len(staged), before + 1)
        self.assertEqual(adopted, project(tuple(staged), self.registry))
        again = _ensure_bundle(staged, self.registry, USER, "2026-10-27T12:00:01Z", "demo.f1098.ensure.again")
        self.assertEqual(len(staged), before + 1)
        self.assertEqual(again, project(tuple(staged), self.registry))

    def test_separate_calls_do_not_share_a_projection(self) -> None:
        other_registry = tax_registry()
        staged_a: list[dict[str, Any]] = []
        staged_b: list[dict[str, Any]] = []
        state_a = _ensure_bundle(staged_a, self.registry, USER, "2026-10-27T12:00:00Z", "demo.f1098.a")
        state_b = _ensure_bundle(staged_b, other_registry, USER, "2026-10-27T12:00:00Z", "demo.f1098.b")
        self.assertEqual(state_a, project(tuple(staged_a), self.registry))
        self.assertEqual(state_b, project(tuple(staged_b), other_registry))
        self.assertEqual(len(staged_a), 1)
        self.assertEqual(len(staged_b), 1)

    def test_first_answer_adopts_the_bundle_and_folds_twice(self) -> None:
        # Before: bundle fold, the answer's own fold, validation's fold, and
        # the post-save read. After: the bundle fold (advanced through the
        # appended act) and the post-save read.
        result, counts = _counted([f1098_recording], lambda: self._answer("paid-the-interest", "yes", "first"))
        folds = counts[f1098_recording.__name__]
        self.assertEqual(len(folds), 2)
        self.assertEqual(result["state"], project(self.log.read().acts, self.registry))
        self.assertEqual(_bundle_count(self.log.read().acts, BUNDLE_ID), 1)
        self.assertIn(result["finding_ids"][0], compute_currency(result["state"]).current_finding_ids)
        self.assertEqual(result["state"].findings[result["finding_ids"][0]]["value"], "yes")

    def test_later_answer_reuses_the_adopted_bundle_projection(self) -> None:
        self._answer("paid-the-interest", "yes", "first")
        bundles = _bundle_count(self.log.read().acts, BUNDLE_ID)
        result, counts = _counted([f1098_recording], lambda: self._answer("owes-the-loan", "yes", "second"))
        self.assertEqual(len(counts[f1098_recording.__name__]), 2)
        self.assertEqual(_bundle_count(self.log.read().acts, BUNDLE_ID), bundles)
        self.assertEqual(result["state"], project(self.log.read().acts, self.registry))
        current = compute_currency(result["state"]).current_finding_ids
        self.assertIn(result["finding_ids"][0], current)

    def test_incomplete_record_refuses_without_writing(self) -> None:
        revision = self.log.read().revision

        def _call() -> F1098RecordingRefused:
            try:
                record_f1098_statement_answers_durably(
                    self.log, self.registry, statement_keys=KEYS_A, answers={"paid-the-interest": "yes"},
                    submission_id="demo.f1098.reuse.incomplete",
                    evidence_ids={"paid-the-interest": "demo.f1098.reuse.incomplete.evidence"},
                    actor=USER, at="2026-10-27T12:01:00Z", expected_revision=revision,
                )
            except F1098RecordingRefused as exc:
                return exc
            raise AssertionError("incomplete answers were admitted")

        refused, counts = _counted([f1098_recording], _call)
        self.assertIsInstance(refused, F1098RecordingRefused)
        self.assertEqual(len(counts[f1098_recording.__name__]), 1)
        self.assertEqual(self.log.read().revision, revision)
        self.assertEqual(_bundle_count(self.log.read().acts, BUNDLE_ID), 0)

    def test_stale_revision_refuses_before_any_fold(self) -> None:
        revision = self.log.read().revision

        def _call() -> F1098RecordingRefused:
            try:
                answer_f1098_statement_answer_durably(
                    self.log, self.registry, statement_keys=KEYS_A, question="paid-the-interest",
                    answer="yes", submission_id="demo.f1098.reuse.stale",
                    evidence_id="demo.f1098.reuse.stale.evidence", actor=USER,
                    at="2026-10-27T12:02:00Z", expected_revision=revision + 1,
                )
            except F1098RecordingRefused as exc:
                return exc
            raise AssertionError("stale revision was admitted")

        refused, counts = _counted([f1098_recording], _call)
        self.assertIsInstance(refused, F1098RecordingRefused)
        self.assertEqual(counts[f1098_recording.__name__], [])
        self.assertEqual(self.log.read().revision, revision)

    def test_correction_and_withdrawal_keep_current_support(self) -> None:
        first = self._answer("paid-the-interest", "yes", "correct-base")

        def _correct() -> dict[str, Any]:
            return correct_f1098_statement_answer_durably(
                self.log, self.registry, statement_keys=KEYS_A, question="paid-the-interest", answer="no",
                predecessor_finding_id=first["finding_ids"][0], submission_id="demo.f1098.reuse.correct",
                evidence_id="demo.f1098.reuse.correct.evidence", actor=USER, at="2026-10-27T12:03:00Z",
                expected_revision=self.log.read().revision,
            )

        corrected, counts = _counted([f1098_recording], _correct)
        self.assertEqual(len(counts[f1098_recording.__name__]), 2)
        self.assertEqual(corrected["state"], project(self.log.read().acts, self.registry))
        current = compute_currency(corrected["state"]).current_finding_ids
        self.assertNotIn(first["finding_ids"][0], current)
        self.assertIn(corrected["finding_ids"][0], current)
        self.assertEqual(corrected["state"].findings[corrected["finding_ids"][0]]["value"], "no")
        held = self.log.read().revision
        with self.assertRaises(F1098RecordingRefused):
            correct_f1098_statement_answer_durably(
                self.log, self.registry, statement_keys=KEYS_A, question="paid-the-interest", answer="yes",
                predecessor_finding_id=first["finding_ids"][0], submission_id="demo.f1098.reuse.stale-target",
                evidence_id="demo.f1098.reuse.stale-target.evidence", actor=USER, at="2026-10-27T12:03:30Z",
                expected_revision=held,
            )
        self.assertEqual(self.log.read().revision, held)

        withdrawn = withdraw_f1098_statement_answer_durably(
            self.log, self.registry, current_findings=[corrected["finding_ids"][0]],
            submission_id="demo.f1098.reuse.withdraw", actor=USER, at="2026-10-27T12:04:00Z",
            expected_revision=self.log.read().revision,
        )
        self.assertEqual(withdrawn["state"], project(self.log.read().acts, self.registry))
        after_withdrawal = compute_currency(withdrawn["state"]).current_finding_ids
        self.assertNotIn(corrected["finding_ids"][0], after_withdrawal)
        restored, restore_counts = _counted(
            [f1098_recording], lambda: self._answer("paid-the-interest", "yes", "restored"))
        self.assertEqual(len(restore_counts[f1098_recording.__name__]), 2)
        restored_current = compute_currency(restored["state"]).current_finding_ids
        self.assertIn(restored["finding_ids"][0], restored_current)
        self.assertNotIn(corrected["finding_ids"][0], restored_current)
        self.assertEqual(restored["state"], project(self.log.read().acts, self.registry))

    def test_nine_answer_record_folds_twice_when_the_bundle_is_appended(self) -> None:
        revision = self.log.read().revision
        result, counts = _counted([f1098_recording], lambda: record_f1098_statement_answers_durably(
            self.log, self.registry, statement_keys=KEYS_A, answers=BASE_ANSWERS,
            submission_id="demo.f1098.reuse.nine", evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.f1098.reuse.nine"),
            actor=USER, at="2026-10-27T12:05:00Z", expected_revision=revision,
        ))
        self.assertEqual(len(counts[f1098_recording.__name__]), 2)
        self.assertEqual(result["state"], project(self.log.read().acts, self.registry))
        current = compute_currency(result["state"]).current_finding_ids
        self.assertTrue(all(finding_id in current for finding_id in result["finding_ids"]))
        self.assertEqual(len(result["finding_ids"]), 9)


@pytest.mark.live(reason="durable mortgage review and comparison recording over a synthetic workspace exceeds the fast-lane budget")
class MortgageProjectionReuseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="mortgage-projection-reuse-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)
        _append_seed(self.log, second_interest=5000)
        load_mortgage_borrowing_bundle(self.registry)
        self.actor = USER
        self.borrowing_a = "demo.mortgage.reuse.a"
        self.borrowing_b = "demo.mortgage.reuse.b"
        for reference in (self.borrowing_a, self.borrowing_b):
            introduce_mortgage_borrowing_reference_durably(
                self.log, self.registry, reference_id=reference, description="Displayed lender",
                actor=self.actor, at="2026-10-27T13:00:00Z",
            )

    def _record(self, claim: str, borrowing: str, value: Any, suffix: str,
                statement: str | None = None, **extra: Any) -> dict[str, Any]:
        keys = None if statement is None else (KEYS_A if statement == "a" else KEYS_B)
        return record_mortgage_borrowing_claim_durably(
            self.log, self.registry, claim=claim, borrowing_ref=borrowing, value=value,
            submission_id=f"demo.mortgage.reuse.{suffix}", evidence_id=f"demo.mortgage.reuse.{suffix}.evidence",
            actor=self.actor, at="2026-10-27T13:01:00Z", statement_keys=keys,
            expected_revision=self.log.read().revision, **extra,
        )

    def _pair(self) -> dict[str, Any]:
        self._record("continuing-borrowing", self.borrowing_a, "yes", "recognition")
        self._record("report-inclusion", self.borrowing_a, "affirmed", "link-a", "a")
        self._record("report-inclusion", self.borrowing_a, "affirmed", "link-b", "b")
        support = current_mortgage_payment_comparison_support(
            self.log.read().acts, self.registry, self.borrowing_a)
        self.assertIsNotNone(support)
        assert support is not None
        return support

    def test_support_called_alone_still_folds(self) -> None:
        self._pair()
        result, counts = _counted([mortgage_recording], lambda: current_mortgage_payment_comparison_support(
            self.log.read().acts, self.registry, self.borrowing_a))
        self.assertEqual(len(counts[mortgage_recording.__name__]), 1)
        self.assertIsNotNone(result)

    def test_review_reuses_one_projection_for_both_borrowings(self) -> None:
        support = self._pair()

        def _call() -> dict[str, Any]:
            return prepare_mortgage_borrowing_review(
                self.log, self.registry, review_id="demo.mortgage.reuse.review",
                shown_at="2026-10-27T13:02:00Z",
            )

        review, counts = _counted([mortgage_review, mortgage_recording], _call)
        self.assertEqual(len(counts[mortgage_review.__name__]), 1)
        self.assertEqual(counts[mortgage_recording.__name__], [])
        offer = next(row for row in review["answers"]
                     if row["claim"] == "payment-comparison" and row["scope"]["borrowing"] == self.borrowing_a
                     and row["scope"]["statement"] == KEYS_A["statement"])
        self.assertEqual(offer["state"], "absent")
        self.assertEqual(offer["comparisonSupport"], support)
        other = next(row for row in review["answers"]
                     if row["claim"] == "payment-comparison" and row["scope"]["borrowing"] == self.borrowing_b
                     and row["scope"]["statement"] == KEYS_A["statement"])
        self.assertEqual(other["state"], "unavailable")
        self.assertIsNone(other["comparisonSupport"])

    def test_comparison_save_without_an_append_skips_the_repeated_fold(self) -> None:
        support = self._pair()
        before = len(self.log.read().acts)
        own = {key: support["reports"][0]["keys"][key] for key in ("payer", "statement", "tax-year")}
        peer = {key: support["reports"][1]["keys"][key] for key in ("payer", "statement", "tax-year")}

        def _call() -> dict[str, Any]:
            return record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="payment-comparison", borrowing_ref=self.borrowing_a,
                value="different-payments", submission_id="demo.mortgage.reuse.comparison",
                evidence_id="demo.mortgage.reuse.comparison.evidence", actor=self.actor,
                at="2026-10-27T13:03:00Z", statement_keys=own, peer_statement_keys=peer,
                comparison_support=support, expected_revision=self.log.read().revision,
            )

        saved, counts = _counted([mortgage_recording], _call)
        folds = counts[mortgage_recording.__name__]
        self.assertEqual(len(folds), 2)
        self.assertEqual(folds[0], before)
        self.assertEqual(folds[1], len(self.log.read().acts))
        self.assertGreater(folds[1], folds[0])
        self.assertEqual(saved["state"], project(self.log.read().acts, self.registry))
        self.assertEqual(saved["state"].findings[saved["finding_id"]]["value"], "different-payments")

    def test_comparison_before_bundle_adoption_refreshes_after_the_append(self) -> None:
        before_acts = len(self.log.read().acts)
        revision = self.log.read().revision

        def _call() -> MortgageBorrowingRecordingRefused:
            try:
                record_mortgage_borrowing_claim_durably(
                    self.log, self.registry, claim="payment-comparison", borrowing_ref=self.borrowing_a,
                    value="different-payments", submission_id="demo.mortgage.reuse.early-comparison",
                    evidence_id="demo.mortgage.reuse.early-comparison.evidence", actor=self.actor,
                    at="2026-10-27T13:04:00Z", statement_keys=KEYS_A, peer_statement_keys=KEYS_B,
                    comparison_support=None, expected_revision=revision,
                )
            except MortgageBorrowingRecordingRefused as exc:
                return exc
            raise AssertionError("unbound comparison was admitted")

        refused, counts = _counted([mortgage_recording], _call)
        self.assertIsInstance(refused, MortgageBorrowingRecordingRefused)
        self.assertEqual(counts[mortgage_recording.__name__], [before_acts, before_acts])
        self.assertEqual(self.log.read().revision, revision)
        self.assertEqual(_bundle_count(self.log.read().acts, MORTGAGE_BUNDLE_ID), 0)

    def test_correction_and_withdrawal_change_the_next_support_read(self) -> None:
        support = self._pair()
        link = next(row for row in support["reports"] if row["keys"]["statement"] == KEYS_A["statement"])
        corrected = correct_mortgage_borrowing_claim_durably(
            self.log, self.registry, finding_id=link["inclusion_finding_id"], claim="report-inclusion",
            borrowing_ref=self.borrowing_a, value="denied", submission_id="demo.mortgage.reuse.deny",
            evidence_id="demo.mortgage.reuse.deny.evidence", actor=self.actor, at="2026-10-27T13:05:00Z",
            statement_keys=KEYS_A, expected_revision=self.log.read().revision,
        )
        denied_state = project(self.log.read().acts, self.registry)
        denied_current = compute_currency(denied_state).current_finding_ids
        self.assertNotIn(link["inclusion_finding_id"], denied_current)
        self.assertIn(corrected["finding_id"], denied_current)
        self.assertEqual(denied_state.findings[corrected["finding_id"]]["value"], "denied")
        self.assertIsNone(current_mortgage_payment_comparison_support(
            self.log.read().acts, self.registry, self.borrowing_a))
        held = self.log.read().revision
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="payment-comparison", borrowing_ref=self.borrowing_a,
                value="different-payments", submission_id="demo.mortgage.reuse.stale-support",
                evidence_id="demo.mortgage.reuse.stale-support.evidence", actor=self.actor,
                at="2026-10-27T13:05:30Z", statement_keys=KEYS_A, peer_statement_keys=KEYS_B,
                comparison_support=support, expected_revision=held,
            )
        self.assertEqual(self.log.read().revision, held)
        denied_review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.reuse.denied",
            shown_at="2026-10-27T13:05:31Z", borrowing_ref=self.borrowing_a,
        )
        denied_offer = next(row for row in denied_review["answers"]
                            if row["claim"] == "payment-comparison" and row["scope"]["statement"] == KEYS_A["statement"])
        self.assertEqual(denied_offer["state"], "unavailable")
        self.assertIsNone(denied_offer["comparisonSupport"])
        denied_link = next(row for row in denied_review["answers"]
                           if row["claim"] == "report-inclusion" and row["scope"]["statement"] == KEYS_A["statement"])
        self.assertEqual(denied_link["value"], "denied")
        self.assertEqual(denied_link["findingId"], corrected["finding_id"])

        other_link = next(row for row in support["reports"] if row["keys"]["statement"] == KEYS_B["statement"])
        withdrawn = withdraw_mortgage_borrowing_claim_durably(
            self.log, self.registry, finding_id=other_link["inclusion_finding_id"],
            claim="report-inclusion", borrowing_ref=self.borrowing_a, actor=self.actor,
            at="2026-10-27T13:06:00Z", statement_keys=KEYS_B,
            submission_id="demo.mortgage.reuse.withdraw-link",
            evidence_id="demo.mortgage.reuse.withdraw-link.evidence",
            expected_revision=self.log.read().revision,
        )
        withdrawn_current = compute_currency(withdrawn["state"]).current_finding_ids
        self.assertNotIn(other_link["inclusion_finding_id"], withdrawn_current)
        self.assertEqual(withdrawn["state"], project(self.log.read().acts, self.registry))
        self.assertIsNone(current_mortgage_payment_comparison_support(
            self.log.read().acts, self.registry, self.borrowing_a))
        withdrawn_review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.reuse.withdrawn",
            shown_at="2026-10-27T13:06:01Z", borrowing_ref=self.borrowing_a,
        )
        withdrawn_offer = next(row for row in withdrawn_review["answers"]
                               if row["claim"] == "payment-comparison"
                               and row["scope"]["statement"] == KEYS_B["statement"])
        self.assertEqual(withdrawn_offer["state"], "unavailable")
        self.assertIsNone(withdrawn_offer["comparisonSupport"])
        self.assertNotEqual(withdrawn_offer["comparisonSupport"], support)
