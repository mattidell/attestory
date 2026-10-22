"""Track 2 regressions: one-projection-per-operation reuse changes nothing observable.

Every differential check compares a changed operation's own returned state
against an independent fresh fold of the acts it actually wrote
(``project(log.read().acts, registry)``) -- the concrete form, here, of
"equal the current implementation's" result: a wrong reuse is exactly a
state that disagrees with a fresh fold of what was actually committed.
``findings.project`` itself is unchanged by this track, so that independent
fold is a faithful reference.

Call-count checks wrap each module's own ``project`` binding (the same
technique ``temp/projection-reuse/measure_p0.py`` uses) for the duration of
one operation and assert the count dropped to the one necessarily-cold fold
that remains.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable
from unittest.mock import patch

import pytest

import packages.derivation.correction_session as cs
import packages.tax.f1099k_statement_recording as f1099k_rec
import packages.tax.f1099k_statement_review as f1099k_review
import packages.tax.sli_relationship_recording as sli_rec
import packages.tax.sli_relationship_review as sli_review
from packages.derivation.correction_session import _entity_label, _opened_loan_answers
from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    _ensure_bundles,
    record_f1099k_statement_durably,
)
from packages.tax.f1099k_statement_review import (
    correct_f1099k_statement_review_answer,
    prepare_f1099k_statement_review,
)
from packages.tax.loader import install_domain_scoped_supersession, tax_registry
from packages.tax.sli_relationship_recording import (
    correct_borrowing_answer_durably,
    introduce_borrowing_reference_durably,
    record_borrowing_answer_durably,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
USER = "demo.taxpayer"


def _project_call_count(module: Any, call: Callable[[], Any]) -> tuple[Any, list[int]]:
    """Run ``call`` with ``module.project`` wrapped; return (result, per-call act counts)."""
    original = module.project
    calls: list[int] = []

    def wrapped(acts: Any, registry: Any) -> Any:
        calls.append(len(tuple(acts)))
        return original(acts, registry)

    with patch.object(module, "project", wrapped):
        result = call()
    return result, calls


def _sli_workspace(suffix: str = "a") -> tuple[TemporaryDirectory[str], ActLog, Any, str]:
    """A tiny workspace with relationship bundle v1 adopted and one borrowing.

    Matches the P0 short history's own setup: v1 adopted, no v2 fact types,
    so the first borrowing answer exercises ``_stage_relationship_v2_adoption``'s
    adoption branch. ``suffix`` keeps two workspaces' borrowing references
    distinct, so a cross-call-leak check can tell them apart.
    """
    raw: TemporaryDirectory[str] = TemporaryDirectory(prefix=f"projection-reuse-sli-{suffix}-")
    schemas = DerivationSchemas()
    install_domain_scoped_supersession(schemas.registry)
    log = ActLog(Path(raw.name) / "workspace", schemas.registry)
    fact_bundle = json.loads((CONTENT / "sli-relationship-source.bundle.json").read_text("utf-8"))
    log.append(
        {"schema": "act.v1", "act_id": f"demo.track2.bundle.{suffix}.0", "kind": "bundle-adoption",
         "actor": USER, "at": "2026-10-21T00:00:00Z", "committed_against": 0,
         "payload": {"bundle": fact_bundle}},
        expected_revision=0,
    )
    borrowing_ref = f"demo.track2.borrowing.{suffix}"
    introduce_borrowing_reference_durably(
        log, schemas.registry, reference_id=borrowing_ref, description=f"Borrowing {suffix}",
        actor=USER, at="2026-10-21T00:00:01Z",
    )
    return raw, log, schemas.registry, borrowing_ref


BASE_ANSWERS: dict[str, Any] = {
    "covers-only-single-item": "yes",
    "acquired-by-purchase": "yes",
    "primary-purpose-at-acquisition": "personal-use",
    "exclusive-personal-use": "yes",
    "digital-asset-involvement": "no",
    "agreed-item-price": 800.0,
    "shipping-arrangement": "platform-pass-through",
    "platform-fees": 80.0,
    "seller-paid-shipping": 0.0,
    "sales-tax-collected-by-platform": 56.0,
    "refund-amount": 0.0,
    "buyer-paid-shipping": 24.0,
    "purchase-cost": 1000.0,
    "cost-basis-known": "yes",
    "lasting-improvements-or-adjustments": "no",
}


@pytest.mark.live(reason="durable recording and review over synthetic workspaces exceeds the fast-lane budget")
class F1099KReuseTests(unittest.TestCase):
    """``_ensure_bundles``, ``_commit`` and the review-to-record reuse."""

    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="projection-reuse-f1099k-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)

    def _record(self, **overrides: Any) -> dict[str, Any]:
        kwargs: dict[str, Any] = dict(
            payer_id="demo.platform.a", statement_ref="demo.stmt.a", box1a=880.0, box4=0.0,
            submission_id="demo.sub.record", evidence_id="demo.ev.record", actor=USER,
            at="2026-10-21T00:00:00Z", expected_revision=0, close_family=False,
        )
        kwargs.update(overrides)
        return record_f1099k_statement_durably(self.log, self.registry, **kwargs)

    def test_record_statement_state_matches_fresh_fold(self) -> None:
        result = self._record()
        fresh = project(self.log.read().acts, self.registry)
        self.assertEqual(result["state"], fresh)

    def test_record_statement_folds_fewer_times_than_before(self) -> None:
        # Before Track 2: _ensure_bundles's own fold, the caller's re-fold
        # right after it, and _commit's post-write fold -- three. After:
        # only _ensure_bundles's own (necessarily cold) fold.
        _result, calls = _project_call_count(f1099k_rec, self._record)
        self.assertEqual(len(calls), 1)

    def test_save_review_reuses_prepare_review_fold_across_modules(self) -> None:
        first = self._record(answers=BASE_ANSWERS,
                             answer_evidence_ids={q: f"demo.ev.{q}" for q in BASE_ANSWERS})
        keys = first["statement_keys"]
        review = prepare_f1099k_statement_review(
            self.log, self.registry, review_id="demo.review", shown_at="2026-10-21T00:01:00Z",
            statement_keys=keys,
        )
        self.assertEqual(review["questions"]["purchase-cost"]["answer"], 1000.0)

        def _call() -> dict[str, Any]:
            return correct_f1099k_statement_review_answer(
                self.log, self.registry, review, question="purchase-cost", answer=1050.0,
                submission_id="demo.sub.correct", evidence_id="demo.ev.correct",
                actor=USER, at="2026-10-21T00:02:00Z",
            )

        result, record_calls = _project_call_count(f1099k_rec, _call)
        # Bundles are already adopted (from the first record), and the
        # review's own fold -- in the other module -- is reused throughout:
        # zero folds left inside f1099k_statement_recording for this call.
        self.assertEqual(len(record_calls), 0)
        fresh = project(self.log.read().acts, self.registry)
        self.assertEqual(result["state"], fresh)

    def test_prepare_review_called_alone_still_folds_fresh(self) -> None:
        first = self._record(answers=BASE_ANSWERS,
                             answer_evidence_ids={q: f"demo.ev.{q}" for q in BASE_ANSWERS})
        keys = first["statement_keys"]

        def _call() -> dict[str, Any]:
            return prepare_f1099k_statement_review(
                self.log, self.registry, review_id="demo.review.alone",
                shown_at="2026-10-21T00:03:00Z", statement_keys=keys,
            )

        result, calls = _project_call_count(f1099k_review, _call)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["statement"]["box1a"], 880.0)

    def test_ensure_bundles_no_cross_call_leak(self) -> None:
        registry_a = tax_registry()
        registry_b = tax_registry()
        staged_a: list[dict[str, Any]] = []
        staged_b: list[dict[str, Any]] = []
        state_a = _ensure_bundles(staged_a, registry_a, USER, "2026-10-21T00:00:00Z", "a")
        state_b = _ensure_bundles(staged_b, registry_b, USER, "2026-10-21T00:00:00Z", "b")
        self.assertEqual(len(staged_a), 2)
        self.assertEqual(len(staged_b), 2)
        self.assertEqual(state_a, project(tuple(staged_a), registry_a))
        self.assertEqual(state_b, project(tuple(staged_b), registry_b))


@pytest.mark.live(reason="durable relationship recording over a synthetic workspace exceeds the fast-lane budget")
class SLIReuseTests(unittest.TestCase):
    """``_record_borrowing_answer_durably`` and ``borrowing_recognition_clues``."""

    def test_record_borrowing_answer_adopts_v2_and_matches_fresh_fold(self) -> None:
        raw, log, registry, borrowing_ref = _sli_workspace()
        with raw:
            result = record_borrowing_answer_durably(
                log, registry, question="loan-paid-only-school-costs", borrowing_ref=borrowing_ref,
                response="yes", submission_id="demo.sub.answer", evidence_id="demo.ev.answer",
                actor=USER, at="2026-10-21T00:00:02Z",
            )
            self.assertEqual(result["adopted_bundle_version"], "v2")
            fresh = project(log.read().acts, registry)
            self.assertEqual(result["state"], fresh)
            self.assertEqual(result["state"].findings[result["finding_id"]]["value"], "yes")

    def test_record_borrowing_answer_folds_once(self) -> None:
        raw, log, registry, borrowing_ref = _sli_workspace()
        with raw:
            def _call() -> dict[str, Any]:
                return record_borrowing_answer_durably(
                    log, registry, question="loan-paid-only-school-costs", borrowing_ref=borrowing_ref,
                    response="yes", submission_id="demo.sub.answer", evidence_id="demo.ev.answer",
                    actor=USER, at="2026-10-21T00:00:02Z",
                )
            # Before Track 2: _stage_relationship_v2_adoption, _current, the
            # base fold before the contribution batch, and the final fold --
            # four, plus _stage_enrollment_follows_schooling's own fold
            # inside _commit_save (untouched; not a named site; shared by
            # other _commit_save callers this track does not charter) --
            # five. After: _stage_relationship_v2_adoption's own fold (the
            # first, necessarily cold, bundle check) plus that same untouched
            # enrollment-follows-schooling fold -- two.
            _result, calls = _project_call_count(sli_rec, _call)
            self.assertEqual(len(calls), 2)

    def test_correct_borrowing_answer_reuses_state_without_extra_fold(self) -> None:
        raw, log, registry, borrowing_ref = _sli_workspace()
        with raw:
            first = record_borrowing_answer_durably(
                log, registry, question="loan-paid-only-school-costs", borrowing_ref=borrowing_ref,
                response="yes", submission_id="demo.sub.answer", evidence_id="demo.ev.answer",
                actor=USER, at="2026-10-21T00:00:02Z",
            )

            def _call() -> dict[str, Any]:
                return correct_borrowing_answer_durably(
                    log, registry, finding_id=first["finding_id"],
                    question="loan-paid-only-school-costs", borrowing_ref=borrowing_ref,
                    response="no", submission_id="demo.sub.correct", evidence_id="demo.ev.correct",
                    actor=USER, at="2026-10-21T00:00:03Z",
                )

            # Bundle v2 is already adopted: one fold inside
            # _stage_relationship_v2_adoption (a no-op check) plus the
            # untouched enrollment-follows-schooling fold inside
            # _commit_save -- two.
            result, calls = _project_call_count(sli_rec, _call)
            self.assertEqual(len(calls), 2)
            fresh = project(log.read().acts, registry)
            self.assertEqual(result["state"], fresh)

    def test_borrowing_recognition_clues_called_alone_still_folds_fresh(self) -> None:
        raw, log, registry, borrowing_ref = _sli_workspace()
        with raw:
            record_borrowing_answer_durably(
                log, registry, question="loan-paid-only-school-costs", borrowing_ref=borrowing_ref,
                response="yes", submission_id="demo.sub.answer", evidence_id="demo.ev.answer",
                actor=USER, at="2026-10-21T00:00:02Z",
            )
            contents = log.read()
            clues = sli_review.borrowing_recognition_clues(contents, registry, borrowing_ref)
            self.assertEqual(clues["borrowing_ref"], borrowing_ref)

    def test_borrowing_recognition_clues_no_cross_call_leak(self) -> None:
        raw_a, log_a, registry_a, ref_a = _sli_workspace("a")
        raw_b, log_b, registry_b, ref_b = _sli_workspace("b")
        with raw_a, raw_b:
            record_borrowing_answer_durably(
                log_a, registry_a, question="loan-paid-only-school-costs", borrowing_ref=ref_a,
                response="yes", submission_id="demo.sub.a", evidence_id="demo.ev.a",
                actor=USER, at="2026-10-21T00:00:02Z",
            )
            state_a = project(log_a.read().acts, registry_a)
            clues_a = sli_review.borrowing_recognition_clues(
                log_a.read(), registry_a, ref_a, _state=state_a)
            self.assertEqual(clues_a["forms"], [])
            # A different workspace, registry and borrowing -- called cold,
            # without _state -- must not see anything from the first call.
            clues_b = sli_review.borrowing_recognition_clues(log_b.read(), registry_b, ref_b)
            self.assertEqual(clues_b["borrowing_ref"], ref_b)
            self.assertEqual(clues_b["forms"], [])
            self.assertEqual(clues_b["financing"], [])


@pytest.mark.live(reason="durable relationship recording over a synthetic workspace exceeds the fast-lane budget")
class CorrectionSessionReuseTests(unittest.TestCase):
    """``_entity_label``, reused inside ``_opened_loan_answers``."""

    def test_opened_loan_answers_folds_once(self) -> None:
        raw, log, registry, borrowing_ref = _sli_workspace()
        with raw:
            record_borrowing_answer_durably(
                log, registry, question="loan-paid-only-school-costs", borrowing_ref=borrowing_ref,
                response="yes", submission_id="demo.sub.answer", evidence_id="demo.ev.answer",
                actor=USER, at="2026-10-21T00:00:02Z",
            )
            contents = log.read()
            result, calls = _project_call_count(cs, lambda: _opened_loan_answers(contents, registry))
            self.assertEqual(len(calls), 1)
            [row] = result
            self.assertEqual(row["borrowing_label"], "Borrowing a")

    def test_entity_label_called_alone_still_folds_fresh(self) -> None:
        raw, log, registry, borrowing_ref = _sli_workspace()
        with raw:
            contents = log.read()
            self.assertEqual(_entity_label(contents, registry, borrowing_ref), "Borrowing a")

    def test_entity_label_no_cross_call_leak(self) -> None:
        raw_a, log_a, registry_a, ref_a = _sli_workspace("a")
        raw_b, log_b, registry_b, _ref_b = _sli_workspace("b")
        with raw_a, raw_b:
            state_a = project(log_a.read().acts, registry_a)
            label_a = _entity_label(log_a.read(), registry_a, ref_a, _state=state_a)
            # A different workspace, called cold, looking up a reference that
            # exists only in the first workspace -- confirms nothing from the
            # first call's state leaked into the second's cold fold.
            label_b = _entity_label(log_b.read(), registry_b, ref_a)
            self.assertEqual(label_a, "Borrowing a")
            self.assertIsNone(label_b)


if __name__ == "__main__":
    unittest.main()
