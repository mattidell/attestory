"""End-to-end demonstration test for Form 1099-K personal item sale loss route.

Exercises the complete lifecycle from charter-track3-demonstration.md:
1. Person with W-2 ($90k) and unemployment ($3k) records 'no Form 1099-K'.
   Schedule 1 attaches, top entry is 0, Form 1040 line 8 is $3,000, line 9 is $93,000.
2. Form 1099-K arrives. Recorded and fully answered for a loss.
   Top entry enters Box 1a ($880.00) exactly once. Form 1040 lines 8 and 9 are unchanged.
3. Correct purchase cost so sale is a gain.
   Review says recalculation-needed. Rerun shows gain stop, no top entry,
   and explanation states income does not yet account for statement.
4. Withdraw platform fees.
   Rerun shows platform fees unanswered stop and not-computed figures.
5. Re-answer platform fees and correct purchase cost back to original loss figures.
   Top entry returns. Lines 8 and 9 remain unchanged.

At each step, saved artifacts are read from disk and assert what the explanation retains:
report, answers, assumptions ("none"), computation (5 figures + comparison), and reasons.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, cast
import unittest

from packages.derivation.live import LiveCoordinatorOutcome, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.tax.f1099k_statement_recording import (
    record_f1099k_no_statements_durably,
    record_f1099k_statement_durably,
)
from packages.tax.f1099k_statement_review import (
    answer_f1099k_statement_review_question,
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
    TOP_ENTRY_SYMBOL,
    UNRESOLVED_SYMBOL,
    USER,
    _finish_acts,
    _make_base_acts,
)
from tests.test_f1099k_statement_recording import BASE_ANSWERS, PAYER, STMT, _evidence_ids


def _published_field_value(model: dict[str, Any], field_id: str) -> Any:
    for sec in model.get("sections", []):
        field = sec.get("field") or {}
        if field.get("id") == field_id:
            resolved = sec.get("resolved") or {}
            if resolved.get("disposition") in ("published_value", "published", "computed_zero", "closure_backed_zero"):
                return resolved.get("value")
    return None


class Form1099KPersonalItemSaleDemonstrationTests(unittest.TestCase):
    """End-to-end synthetic story demonstrating the Form 1099-K loss route lifecycle."""

    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1099k-demo-e2e-")
        self.addCleanup(self.temp.cleanup)
        self.workspace_dir = Path(self.temp.name) / "workspace"
        self.capability = WorkspaceCapability(self.workspace_dir)
        self.registry = tax_registry()
        self.log = ActLog(self.workspace_dir, self.registry)
        # Seed workspace with W-2 ($90,000) and Unemployment ($3,000)
        seed_acts = _finish_acts(_make_base_acts(wages=90000.0, unemployment=3000.0))
        self.log.append_batch(seed_acts, expected_revision=0)
        self.records = RecordStream(self.workspace_dir / "records", DerivationSchemas())

    def _run(self, run_id: str) -> LiveCoordinatorOutcome:
        contents = self.log.read()
        return live_coordinate_run(
            self.capability,
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

    def test_complete_demonstration_story(self) -> None:
        """Execute the 5-step lifecycle and verify exit criteria at every step."""

        # =========================================================================
        # STEP 1: A person with W-2 and unemployment records 'no Form 1099-K'.
        # Schedule 1 attaches as before and the top entry is 0.
        # =========================================================================
        step1_rev_before = self.log.read().revision
        record_f1099k_no_statements_durably(
            self.log,
            self.registry,
            submission_id="demo.f1099k.sub.step1-no-1099k",
            evidence_id="demo.f1099k.ev.step1-no-1099k",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=step1_rev_before,
        )

        outcome1 = self._run("step1-no-1099k")
        self.assertIsNone(outcome1.refusal)
        assert outcome1.presentation_path is not None
        self.assertTrue(outcome1.presentation_path.exists())

        # Read saved presentation artifact from disk
        saved_pres1 = json.loads(outcome1.presentation_path.read_text("utf-8"))
        review1 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome1.presentation_path,
            self.records,
            review_id="demo.f1099k.rev.step1",
            shown_at="2026-10-16T12:01:00Z",
        )

        # Assert Step 1 outcome:
        # Schedule 1 top entry is 0
        self.assertEqual(review1["savedCalculationState"], "current-closed-empty-zero")
        calc1 = review1["savedCalculation"]
        self.assertIsNotNone(calc1)
        self.assertEqual(calc1["status"], "closed-empty-zero")
        self.assertEqual(calc1["box1a"], 0.0)
        self.assertEqual(calc1["assumptions"], "none")
        self.assertIsNone(calc1["computation"])

        # Form 1040 Line 8 (Schedule 1 unemployment $3,000) and Line 9 ($93,000)
        line8_step1 = _published_field_value(saved_pres1, "tax.us.2025.form1040.line-8")
        line9_step1 = _published_field_value(saved_pres1, "tax.us.2025.form1040.line-9")
        self.assertEqual(float(str(line8_step1)), 3000.0)
        self.assertEqual(float(str(line9_step1)), 93000.0)

        # =========================================================================
        # STEP 2: A Form 1099-K arrives. Recorded and answered for a loss.
        # Box 1a ($880) appears in top entry exactly once; lines 8 and 9 unchanged.
        # =========================================================================
        stmt_res2 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref=STMT,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.f1099k.sub.step2-stmt",
            evidence_id="demo.f1099k.ev.step2-stmt",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys2 = cast(dict[str, str], stmt_res2["statement_keys"])

        rev2_prep = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.step2-prep",
            shown_at="2026-10-16T12:02:30Z",
            statement_keys=stmt_keys2,
        )

        loss_answers = {
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
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev2_prep,
            answers=loss_answers,
            submission_id="demo.f1099k.sub.step2-ans",
            evidence_ids=_evidence_ids(loss_answers, prefix="demo.f1099k.ev.step2"),
            actor=USER,
            at="2026-10-16T12:03:00Z",
        )

        outcome2 = self._run("step2-loss")
        self.assertIsNone(outcome2.refusal)
        assert outcome2.presentation_path is not None
        saved_pres2 = json.loads(outcome2.presentation_path.read_text("utf-8"))

        review2 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome2.presentation_path,
            self.records,
            review_id="demo.f1099k.rev.step2",
            shown_at="2026-10-16T12:04:00Z",
            statement_keys=stmt_keys2,
        )

        # Assert Step 2 outcome:
        # Top entry is Box 1a ($880.00) entered exactly once
        self.assertEqual(review2["savedCalculationState"], "current-supported-loss")
        calc2 = review2["savedCalculation"]
        self.assertIsNotNone(calc2)
        self.assertEqual(calc2["status"], "supported-loss")
        self.assertEqual(calc2["box1a"], 880.0)

        top_pubs2 = [p.finding for p in (outcome2.publications or ()) if p.finding.get("symbol") == TOP_ENTRY_SYMBOL]
        self.assertEqual(len(top_pubs2), 1)
        self.assertEqual(float(str(top_pubs2[0]["value"])), 880.0)

        # Lines 8 and 9 UNCHANGED from step 1
        line8_step2 = _published_field_value(saved_pres2, "tax.us.2025.form1040.line-8")
        line9_step2 = _published_field_value(saved_pres2, "tax.us.2025.form1040.line-9")
        self.assertEqual(float(str(line8_step2)), float(str(line8_step1)))
        self.assertEqual(float(str(line9_step2)), float(str(line9_step1)))

        # Assert explanation retention:
        # report: payer label and Box 1a
        self.assertEqual(review2["statement"]["payerLabel"], "Synthetic platform")
        self.assertEqual(review2["statement"]["box1a"], 880.0)
        # answers: chosen answers and labels
        self.assertEqual(review2["questions"]["agreed-item-price"]["answer"], 800.0)
        self.assertEqual(review2["questions"]["agreed-item-price"]["label"], "$800.00")
        self.assertEqual(review2["questions"]["purchase-cost"]["answer"], 1000.0)
        self.assertEqual(review2["questions"]["purchase-cost"]["label"], "$1,000.00")
        # assumptions: "none"
        self.assertEqual(calc2["assumptions"], "none")
        # computation: 5 figures + comparison
        comp2 = calc2["computation"]
        self.assertIsNotNone(comp2)
        self.assertEqual(comp2["amountRealized"], 800.0)
        self.assertEqual(comp2["sellingExpenses"], 80.0)
        self.assertEqual(comp2["netProceeds"], 720.0)
        self.assertEqual(comp2["adjustedBasis"], 1000.0)
        self.assertEqual(comp2["expectedBox1aGrossAmount"], 880.0)
        self.assertEqual(comp2["comparison"], "net proceeds < adjusted basis")

        # =========================================================================
        # STEP 3: Correct purchase cost so sale is a gain.
        # Review says recalculation-needed. Rerun shows gain stop, no top entry,
        # and income sentence states return's income does not yet account for statement.
        # =========================================================================
        rev3_prep = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.step3-prep",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys2,
        )

        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            rev3_prep,
            question="purchase-cost",
            answer=500.0,
            submission_id="demo.f1099k.sub.step3-corr-cost",
            evidence_id="demo.f1099k.ev.step3-corr-cost",
            actor=USER,
            at="2026-10-16T12:06:00Z",
        )

        # Before rerun: reload review with the previous presentation -> recalculation-needed!
        rev3_stale = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome2.presentation_path,
            self.records,
            review_id="demo.f1099k.rev.step3-stale",
            shown_at="2026-10-16T12:06:30Z",
            statement_keys=stmt_keys2,
        )
        self.assertEqual(rev3_stale["savedCalculationState"], "recalculation-needed")

        outcome3 = self._run("step3-gain")
        self.assertIsNone(outcome3.refusal)
        assert outcome3.presentation_path is not None
        saved_pres3 = json.loads(outcome3.presentation_path.read_text("utf-8"))

        review3 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome3.presentation_path,
            self.records,
            review_id="demo.f1099k.rev.step3",
            shown_at="2026-10-16T12:07:00Z",
            statement_keys=stmt_keys2,
        )

        # Assert Step 3 outcome:
        # Gain stop, no top entry
        self.assertEqual(review3["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review3["savedState"], "actually-unresolved")
        self.assertIsNone(review3["savedCalculation"])

        top_pubs3 = [p.finding for p in (outcome3.publications or ()) if p.finding.get("symbol") == TOP_ENTRY_SYMBOL]
        self.assertEqual(len(top_pubs3), 0)

        # Assert explanation retention:
        unres3 = review3["savedUnresolvedExplanation"]
        self.assertIsNotNone(unres3)
        self.assertEqual(unres3["assumptions"], "none")
        self.assertIn("does not yet account for this Form 1099-K", unres3["incomeSentence"])
        self.assertTrue(any("gain or profit" in s for s in unres3["reasonSentences"]))

        comp3 = unres3["computation"]
        self.assertIsNotNone(comp3)
        self.assertEqual(comp3["amountRealized"], 800.0)
        self.assertEqual(comp3["sellingExpenses"], 80.0)
        self.assertEqual(comp3["netProceeds"], 720.0)
        self.assertEqual(comp3["adjustedBasis"], 500.0)
        self.assertEqual(comp3["expectedBox1aGrossAmount"], 880.0)
        self.assertEqual(comp3["comparison"], "net proceeds > adjusted basis")

        # =========================================================================
        # STEP 4: Withdraw an amount (platform-fees).
        # Rerun shows that amount's unanswered stop and not-computed figures.
        # =========================================================================
        rev4_prep = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.step4-prep",
            shown_at="2026-10-16T12:08:00Z",
            statement_keys=stmt_keys2,
        )

        withdraw_f1099k_statement_review_answers(
            self.log,
            self.registry,
            rev4_prep,
            questions=["platform-fees"],
            submission_id="demo.f1099k.sub.step4-withdraw-fees",
            actor=USER,
            at="2026-10-16T12:09:00Z",
        )

        outcome4 = self._run("step4-withdrawn")
        self.assertIsNone(outcome4.refusal)
        assert outcome4.presentation_path is not None

        review4 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome4.presentation_path,
            self.records,
            review_id="demo.f1099k.rev.step4",
            shown_at="2026-10-16T12:10:00Z",
            statement_keys=stmt_keys2,
        )

        # Assert Step 4 outcome:
        self.assertEqual(review4["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review4["savedState"], "actually-unresolved")
        unres4 = review4["savedUnresolvedExplanation"]
        self.assertIsNotNone(unres4)
        self.assertEqual(unres4["assumptions"], "none")
        self.assertTrue(any("platform selling fees" in s for s in unres4["reasonSentences"]))

        comp4 = unres4["computation"]
        # Expected values derived from scenario's recorded answers per track3-computation.md Case 4:
        # agreed-item-price ($800) - refunds ($0) = $800
        # platform-fees is unanswered -> selling expenses and net proceeds are not-computed
        # purchase-cost ($500 corrected in step 3) = $500
        # expected Box 1a is $880
        self.assertEqual(comp4["amountRealized"], 800.0)
        self.assertEqual(comp4["sellingExpenses"], "not-computed")
        self.assertEqual(comp4["netProceeds"], "not-computed")
        self.assertEqual(comp4["adjustedBasis"], 500.0)
        self.assertEqual(comp4["expectedBox1aGrossAmount"], 880.0)
        self.assertEqual(comp4["comparison"], "not-computed")
        assert outcome4.publications is not None
        step4_pubs = {
            str(pub.finding.get("symbol", "")).split("|")[0]: pub.finding.get("value")
            for pub in outcome4.publications
            if isinstance(getattr(pub, "finding", None), Mapping)
            and f"statement={stmt_keys2['statement']}" in str(pub.finding.get("symbol", ""))
        }
        self.assertEqual(comp4["amountRealized"], float(str(step4_pubs["tax.us.2025.f1099k.amount-realized"])))
        self.assertEqual(comp4["sellingExpenses"], step4_pubs["tax.us.2025.f1099k.selling-expenses"])
        self.assertEqual(comp4["netProceeds"], step4_pubs["tax.us.2025.f1099k.net-proceeds"])
        self.assertEqual(comp4["adjustedBasis"], float(str(step4_pubs["tax.us.2025.f1099k.adjusted-basis"])))
        self.assertEqual(comp4["expectedBox1aGrossAmount"], float(str(step4_pubs["tax.us.2025.f1099k.expected-box1a-gross-amount"])))

        # =========================================================================
        # STEP 5: Answer again with original loss figures.
        # Top entry returns. Lines 8 and 9 remain unchanged.
        # =========================================================================
        rev5_prep = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.step5-prep",
            shown_at="2026-10-16T12:11:00Z",
            statement_keys=stmt_keys2,
        )
        answer_f1099k_statement_review_question(
            self.log,
            self.registry,
            rev5_prep,
            question="platform-fees",
            answer=80.0,
            submission_id="demo.f1099k.sub.step5-reans-fees",
            evidence_id="demo.f1099k.ev.step5-reans-fees",
            actor=USER,
            at="2026-10-16T12:12:00Z",
        )

        rev5b_prep = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.f1099k.rev.step5b-prep",
            shown_at="2026-10-16T12:13:00Z",
            statement_keys=stmt_keys2,
        )
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            rev5b_prep,
            question="purchase-cost",
            answer=1000.0,
            submission_id="demo.f1099k.sub.step5-recorr-cost",
            evidence_id="demo.f1099k.ev.step5-recorr-cost",
            actor=USER,
            at="2026-10-16T12:14:00Z",
        )

        outcome5 = self._run("step5-loss-restored")
        self.assertIsNone(outcome5.refusal)
        assert outcome5.presentation_path is not None
        saved_pres5 = json.loads(outcome5.presentation_path.read_text("utf-8"))

        review5 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome5.presentation_path,
            self.records,
            review_id="demo.f1099k.rev.step5",
            shown_at="2026-10-16T12:15:00Z",
            statement_keys=stmt_keys2,
        )

        # Assert Step 5 outcome:
        # Top entry returns with 880.0
        self.assertEqual(review5["savedCalculationState"], "current-supported-loss")
        calc5 = review5["savedCalculation"]
        self.assertIsNotNone(calc5)
        self.assertEqual(calc5["status"], "supported-loss")
        self.assertEqual(calc5["box1a"], 880.0)

        top_pubs5 = [p.finding for p in (outcome5.publications or ()) if p.finding.get("symbol") == TOP_ENTRY_SYMBOL]
        self.assertEqual(len(top_pubs5), 1)
        self.assertEqual(float(str(top_pubs5[0]["value"])), 880.0)

        # Lines 8 and 9 remain unchanged
        line8_step5 = _published_field_value(saved_pres5, "tax.us.2025.form1040.line-8")
        line9_step5 = _published_field_value(saved_pres5, "tax.us.2025.form1040.line-9")
        self.assertEqual(float(str(line8_step5)), float(str(line8_step1)))
        self.assertEqual(float(str(line9_step5)), float(str(line9_step1)))

        # Explanation retained
        comp5 = calc5["computation"]
        self.assertIsNotNone(comp5)
        self.assertEqual(comp5["netProceeds"], 720.0)
        self.assertEqual(comp5["adjustedBasis"], 1000.0)
        self.assertEqual(comp5["comparison"], "net proceeds < adjusted basis")
        self.assertEqual(calc5["assumptions"], "none")


if __name__ == "__main__":
    unittest.main()
