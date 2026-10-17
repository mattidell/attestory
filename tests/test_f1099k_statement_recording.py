"""Track 2 direct durable-recorder admission and refusal checks for Form 1099-K."""
from __future__ import annotations

import copy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import unittest
import pytest

from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    F1099KRecordingRefused,
    answer_f1099k_statement_answer_durably,
    correct_f1099k_statement_answer_durably,
    record_f1099k_no_statements_durably,
    record_f1099k_statement_answers_durably,
    record_f1099k_statement_durably,
    withdraw_f1099k_statement_answer_durably,
)
from packages.tax.loader import tax_registry

USER = "demo.taxpayer"
PAYER = "demo.platform.a"
STMT = "demo.stmt.a"

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


def _evidence_ids(answers: dict[str, Any], prefix: str = "demo.f1099k.evidence") -> dict[str, str]:
    return {question: f"{prefix}.{question}" for question in answers}


@pytest.mark.live(reason="durable admission over synthetic Form 1099-K workspaces exceeds the fast-lane budget")
class F1099KStatementRecordingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1099k-answer-recording-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)

    def test_record_statement_and_answers_durably(self) -> None:
        res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.stmt1",
            evidence_id="demo.f1099k.ev.stmt1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        self.assertEqual(len(res["finding_ids"]), 3)
        self.assertIn("statement_keys", res)
        stmt_keys = res["statement_keys"]
        self.assertEqual(stmt_keys["payer"], PAYER)
        self.assertEqual(stmt_keys["tax-year"], "2025")

        ans_res = record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=stmt_keys,
            answers=BASE_ANSWERS,
            submission_id="demo.f1099k.sub.ans1",
            evidence_ids=_evidence_ids(BASE_ANSWERS),
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=res["revision"],
        )
        self.assertEqual(len(ans_res["finding_ids"]), 15)

        acts = self.log.read().acts
        saved_evidence = [
            row["payload"]["evidence"] for row in acts
            if row["kind"] == "evidence-submitted" and row["payload"]["evidence"].get("kind") == "tax.personal-item-sale.f1099k-statement-answer"
        ]
        q1_ev = next(row for row in saved_evidence if row["content"]["question"].endswith("covers-only-single-item"))
        self.assertEqual(q1_ev["kind"], "tax.personal-item-sale.f1099k-statement-answer")
        self.assertEqual(q1_ev["content"]["answer"], "yes")
        self.assertEqual(q1_ev["content"]["statement"], stmt_keys)

    def test_record_statement_corrected(self) -> None:
        first = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.stmt-first",
            evidence_id="demo.f1099k.ev.stmt-first",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        # Duplicate without corrected=True is refused
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id=PAYER,
                statement_ref=STMT,
                box1a=900.0,
                box4=0.0,
                submission_id="demo.f1099k.sub.stmt-dup",
                evidence_id="demo.f1099k.ev.stmt-dup",
                actor=USER,
                at="2026-10-16T12:01:00Z",
                expected_revision=first["revision"],
            )

        # Corrected statement succeeds
        corrected = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=900.0,
            box4=0.0,
            corrected=True,
            submission_id="demo.f1099k.sub.stmt-corrected",
            evidence_id="demo.f1099k.ev.stmt-corrected",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=first["revision"],
        )
        self.assertGreater(corrected["revision"], first["revision"])

        # Check that Box 1a finding was asserted, not member-transition
        new_acts = self.log.read().acts[first["revision"]:]
        b1a_acts = [
            a for a in new_acts
            if a["kind"] in ("assertion", "member-transition")
            and "box1a-gross-amount" in a["payload"]["finding"]["fact_id"]
        ]
        self.assertEqual(len(b1a_acts), 1)
        self.assertEqual(b1a_acts[0]["kind"], "assertion")
        self.assertEqual(b1a_acts[0]["payload"]["finding"]["value"], 900.0)

    def test_record_no_statements_durably_and_subsequent_statement(self) -> None:
        closed = record_f1099k_no_statements_durably(
            self.log,
            self.registry,
            submission_id="demo.f1099k.no-stmts",
            evidence_id="demo.f1099k.ev.no-stmts",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        self.assertEqual(len(closed["finding_ids"]), 1)
        closure_fid = closed["finding_ids"][0]

        state = project(self.log.read().acts, self.registry)
        current_fids = compute_currency(state).current_finding_ids
        self.assertIn(closure_fid, current_fids)

        # Recording a statement after no statements advances horizon
        subsequent = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.subsequent-stmt",
            evidence_id="demo.f1099k.ev.subsequent-stmt",
            actor=USER,
            at="2026-10-16T12:05:00Z",
            expected_revision=closed["revision"],
        )
        self.assertGreater(subsequent["revision"], closed["revision"])

    def test_record_no_statements_refuses_when_statements_exist(self) -> None:
        first = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.first",
            evidence_id="demo.f1099k.ev.first",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_no_statements_durably(
                self.log,
                self.registry,
                submission_id="demo.f1099k.sub.no-stmts-bad",
                evidence_id="demo.f1099k.ev.no-stmts-bad",
                actor=USER,
                at="2026-10-16T12:01:00Z",
                expected_revision=first["revision"],
            )

    def test_stale_expected_revision_refuses_log_unchanged(self) -> None:
        first = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.stale1",
            evidence_id="demo.f1099k.ev.stale1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        rev = first["revision"]
        content_bytes = self.log.path.read_bytes()

        # Stale revision for record_f1099k_statement_durably
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id="demo.platform.b",
                statement_ref="demo.stmt.b",
                box1a=500.0,
                box4=0.0,
                submission_id="demo.f1099k.sub.stale2",
                evidence_id="demo.f1099k.ev.stale2",
                actor=USER,
                at="2026-10-16T12:01:00Z",
                expected_revision=0,  # Stale!
            )
        self.assertEqual(self.log.read().revision, rev)
        self.assertEqual(self.log.path.read_bytes(), content_bytes)

        # Stale revision for record_f1099k_statement_answers_durably
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_answers_durably(
                self.log,
                self.registry,
                statement_keys=first["statement_keys"],
                answers=BASE_ANSWERS,
                submission_id="demo.f1099k.sub.ans-stale",
                evidence_ids=_evidence_ids(BASE_ANSWERS),
                actor=USER,
                at="2026-10-16T12:02:00Z",
                expected_revision=0,  # Stale!
            )
        self.assertEqual(self.log.read().revision, rev)
        self.assertEqual(self.log.path.read_bytes(), content_bytes)

        # Save answers to test answer/correct/withdraw stale checks
        ans_res = record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=first["statement_keys"],
            answers=BASE_ANSWERS,
            submission_id="demo.f1099k.sub.ans-ok",
            evidence_ids=_evidence_ids(BASE_ANSWERS),
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=rev,
        )
        new_rev = ans_res["revision"]
        new_bytes = self.log.path.read_bytes()

        with self.assertRaises(F1099KRecordingRefused):
            answer_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                statement_keys=first["statement_keys"],
                question="covers-only-single-item",
                answer="yes",
                submission_id="demo.f1099k.single-stale",
                evidence_id="demo.f1099k.single-stale.ev",
                actor=USER,
                at="2026-10-16T12:04:00Z",
                expected_revision=rev,  # Stale!
            )
        self.assertEqual(self.log.read().revision, new_rev)
        self.assertEqual(self.log.path.read_bytes(), new_bytes)

        cost_fid = ans_res["finding_ids"][12]  # purchase-cost finding id
        with self.assertRaises(F1099KRecordingRefused):
            correct_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                statement_keys=first["statement_keys"],
                question="purchase-cost",
                answer=1200.0,
                predecessor_finding_id=cost_fid,
                submission_id="demo.f1099k.correct-stale",
                evidence_id="demo.f1099k.correct-stale.ev",
                actor=USER,
                at="2026-10-16T12:05:00Z",
                expected_revision=rev,  # Stale!
            )
        self.assertEqual(self.log.read().revision, new_rev)
        self.assertEqual(self.log.path.read_bytes(), new_bytes)

        with self.assertRaises(F1099KRecordingRefused):
            withdraw_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                current_findings=[cost_fid],
                submission_id="demo.f1099k.withdraw-stale",
                actor=USER,
                at="2026-10-16T12:06:00Z",
                expected_revision=rev,  # Stale!
            )
        self.assertEqual(self.log.read().revision, new_rev)
        self.assertEqual(self.log.path.read_bytes(), new_bytes)

    def test_invalid_choice_or_not_asked_refused_before_write(self) -> None:
        first = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.vocab",
            evidence_id="demo.f1099k.ev.vocab",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        rev = first["revision"]
        content_bytes = self.log.path.read_bytes()

        # Choice outside vocabulary
        with self.assertRaises(F1099KRecordingRefused):
            answer_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                statement_keys=first["statement_keys"],
                question="covers-only-single-item",
                answer="maybe",
                submission_id="demo.f1099k.bad-choice",
                evidence_id="demo.f1099k.bad-choice.ev",
                actor=USER,
                at="2026-10-16T12:01:00Z",
                expected_revision=rev,
            )
        self.assertEqual(self.log.read().revision, rev)
        self.assertEqual(self.log.path.read_bytes(), content_bytes)

        # "not-asked" submitted
        with self.assertRaises(F1099KRecordingRefused):
            answer_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                statement_keys=first["statement_keys"],
                question="shipping-arrangement",
                answer="not-asked",
                submission_id="demo.f1099k.not-asked-ans",
                evidence_id="demo.f1099k.not-asked-ans.ev",
                actor=USER,
                at="2026-10-16T12:02:00Z",
                expected_revision=rev,
            )
        self.assertEqual(self.log.read().revision, rev)
        self.assertEqual(self.log.path.read_bytes(), content_bytes)

        # Negative amount
        with self.assertRaises(F1099KRecordingRefused):
            answer_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                statement_keys=first["statement_keys"],
                question="agreed-item-price",
                answer=-50.0,
                submission_id="demo.f1099k.negative-price",
                evidence_id="demo.f1099k.negative-price.ev",
                actor=USER,
                at="2026-10-16T12:03:00Z",
                expected_revision=rev,
            )
        self.assertEqual(self.log.read().revision, rev)
        self.assertEqual(self.log.path.read_bytes(), content_bytes)

        # String for numeric question
        with self.assertRaises(F1099KRecordingRefused):
            answer_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                statement_keys=first["statement_keys"],
                question="purchase-cost",
                answer="one-thousand",
                submission_id="demo.f1099k.str-cost",
                evidence_id="demo.f1099k.str-cost.ev",
                actor=USER,
                at="2026-10-16T12:04:00Z",
                expected_revision=rev,
            )
        self.assertEqual(self.log.read().revision, rev)
        self.assertEqual(self.log.path.read_bytes(), content_bytes)

    def test_statement_identity_validation(self) -> None:
        # Empty payer
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id="",
                statement_ref=STMT,
                box1a=880.0,
                box4=0.0,
                submission_id="demo.f1099k.bad-payer",
                evidence_id="demo.f1099k.bad-payer.ev",
                actor=USER,
                at="2026-10-16T12:00:00Z",
                expected_revision=0,
            )

        # Empty statement ref
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id=PAYER,
                statement_ref="",
                box1a=880.0,
                box4=0.0,
                submission_id="demo.f1099k.bad-ref-empty",
                evidence_id="demo.f1099k.bad-ref-empty.ev",
                actor=USER,
                at="2026-10-16T12:00:00Z",
                expected_revision=0,
            )

        # Forbidden marker in statement ref
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id=PAYER,
                statement_ref="statement.pdf",
                box1a=880.0,
                box4=0.0,
                submission_id="demo.f1099k.bad-ref-marker",
                evidence_id="demo.f1099k.bad-ref-marker.ev",
                actor=USER,
                at="2026-10-16T12:00:00Z",
                expected_revision=0,
            )

        # Negative box1a
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id=PAYER,
                statement_ref=STMT,
                box1a=-100.0,
                box4=0.0,
                submission_id="demo.f1099k.neg-box1a",
                evidence_id="demo.f1099k.neg-box1a.ev",
                actor=USER,
                at="2026-10-16T12:00:00Z",
                expected_revision=0,
            )

        # Negative box4
        with self.assertRaises(F1099KRecordingRefused):
            record_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id=PAYER,
                statement_ref=STMT,
                box1a=880.0,
                box4=-5.0,
                submission_id="demo.f1099k.neg-box4",
                evidence_id="demo.f1099k.neg-box4.ev",
                actor=USER,
                at="2026-10-16T12:00:00Z",
                expected_revision=0,
            )

        # Omitted box4 raises TypeError (R4: explicit required argument)
        with self.assertRaises(TypeError):
            record_f1099k_statement_durably(  # type: ignore[call-arg]
                self.log,
                self.registry,
                payer_id=PAYER,
                statement_ref=STMT,
                box1a=880.0,
                submission_id="demo.f1099k.omitted-box4",
                evidence_id="demo.f1099k.omitted-box4.ev",
                actor=USER,
                at="2026-10-16T12:00:00Z",
                expected_revision=0,
            )

    def test_answer_correction_and_history_preservation(self) -> None:
        first = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.hist",
            evidence_id="demo.f1099k.ev.hist",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        ans_res = record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=first["statement_keys"],
            answers=BASE_ANSWERS,
            submission_id="demo.f1099k.sub.ans-hist",
            evidence_ids=_evidence_ids(BASE_ANSWERS),
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=first["revision"],
        )
        state_before = project(self.log.read().acts, self.registry)
        cost_fid = next(
            fid for fid, finding in state_before.findings.items()
            if "purchase-cost" in finding["fact_id"] and fid in compute_currency(state_before).current_finding_ids
        )

        # Correct cost from 1000.0 to 500.0
        corr = correct_f1099k_statement_answer_durably(
            self.log,
            self.registry,
            statement_keys=first["statement_keys"],
            question="purchase-cost",
            answer=500.0,
            predecessor_finding_id=cost_fid,
            submission_id="demo.f1099k.corr-cost",
            evidence_id="demo.f1099k.corr-cost.ev",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=ans_res["revision"],
        )
        self.assertEqual(len(corr["finding_ids"]), 1)
        new_cost_fid = corr["finding_ids"][0]

        state_after = project(self.log.read().acts, self.registry)
        current_fids = compute_currency(state_after).current_finding_ids
        # Old finding retracted
        self.assertNotIn(cost_fid, current_fids)
        # New finding current
        self.assertIn(new_cost_fid, current_fids)
        # Both exist in history
        self.assertIn(cost_fid, state_after.findings)
        self.assertIn(new_cost_fid, state_after.findings)
        self.assertEqual(state_after.findings[cost_fid]["value"], 1000.0)
        self.assertEqual(state_after.findings[new_cost_fid]["value"], 500.0)

    def test_withdrawal_refuses_non_answer_and_non_current(self) -> None:
        first = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.withdr",
            evidence_id="demo.f1099k.ev.withdr",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        ans_res = record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=first["statement_keys"],
            answers=BASE_ANSWERS,
            submission_id="demo.f1099k.sub.ans-withdr",
            evidence_ids=_evidence_ids(BASE_ANSWERS),
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=first["revision"],
        )
        state = project(self.log.read().acts, self.registry)
        # Try to withdraw Box 1a (not a circumstance answer)
        b1a_fid = next(
            fid for fid, finding in state.findings.items()
            if "box1a-gross-amount" in finding["fact_id"]
        )
        with self.assertRaises(F1099KRecordingRefused):
            withdraw_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                current_findings=[b1a_fid],
                submission_id="demo.f1099k.bad-withdraw-b1a",
                actor=USER,
                at="2026-10-16T12:02:00Z",
                expected_revision=ans_res["revision"],
            )

        # Withdraw personal use answer
        q5_fid = next(
            fid for fid, finding in state.findings.items()
            if "exclusive-personal-use" in finding["fact_id"]
        )
        w_res = withdraw_f1099k_statement_answer_durably(
            self.log,
            self.registry,
            current_findings=[q5_fid],
            submission_id="demo.f1099k.withdraw-q5",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=ans_res["revision"],
        )
        self.assertGreater(w_res["revision"], ans_res["revision"])

        # Retrying to withdraw the retracted finding raises
        with self.assertRaises(F1099KRecordingRefused):
            withdraw_f1099k_statement_answer_durably(
                self.log,
                self.registry,
                current_findings=[q5_fid],
                submission_id="demo.f1099k.withdraw-q5-again",
                actor=USER,
                at="2026-10-16T12:04:00Z",
                expected_revision=w_res["revision"],
            )

    def test_two_statements_recorded_advances_horizons(self) -> None:
        first = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.stmt-1",
            evidence_id="demo.f1099k.ev.stmt-1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        second = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id="demo.platform.b",
            statement_ref="demo.stmt.b",
            box1a=450.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.stmt-2",
            evidence_id="demo.f1099k.ev.stmt-2",
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=first["revision"],
        )
        self.assertGreater(second["revision"], first["revision"])
        state = project(self.log.read().acts, self.registry)
        current_b1a = [
            f["value"] for fid, f in state.findings.items()
            if "box1a-gross-amount" in f["fact_id"] and fid in compute_currency(state).current_finding_ids
        ]
        self.assertEqual(sorted(current_b1a), [450.0, 880.0])
