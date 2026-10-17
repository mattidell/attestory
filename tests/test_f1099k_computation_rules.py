"""Focused tests for Form 1099-K five computation rules.

Covers:
- The 5 figures across shipping arrangements (platform-pass-through, seller-received-shipping, none)
- Refunds reducing amount realized
- The not-computed paths for omitted or uncertain answers
- Reconciliation stop publishing expected Box 1a and showing mismatched figures
- Owner Standard 1: All answers driven through Track 2 review operations (prepare_f1099k_statement_review,
  save_f1099k_statement_review, answer_f1099k_statement_review_question)
- Owner Standard 2: Displayed status follows recorded outcome (e.g. supported-loss)
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, cast

from packages.derivation.live import LiveCoordinatorOutcome, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.tax.f1099k_statement_recording import record_f1099k_statement_durably
from packages.tax.f1099k_statement_review import (
    answer_f1099k_statement_review_question,
    correct_f1099k_statement_review_answer,
    prepare_f1099k_statement_review,
    review_f1099k_statement_with_saved_presentation,
    save_f1099k_statement_review,
    withdraw_f1099k_statement_review_answers,
)
from packages.tax.loader import tax_registry
import json
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested
from tests.test_f1099k_personal_item_sale_track1 import (
    BOX1A,
    BOX4,
    FAMILY_ID,
    Q1,
    Q3,
    Q4,
    Q5,
    Q7,
    Q8_PRICE,
    Q8_SHIP,
    Q9_FEES,
    Q9_SELLER_SHIP,
    Q10_REFUND,
    Q10_TAX,
    Q11_BUYER_SHIP,
    Q12_COST,
    Q12_GATE,
    Q13,
    ROOT,
    SCOPE,
    SURFACE,
    USER,
    _add_family_closure,
    _add_statement_assertions,
    _add_statement_entities,
    _finish_acts,
    _make_base_acts,
    _statement_fact_id,
)
from tests.test_f1099k_statement_recording import PAYER, STMT, _evidence_ids


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


class Form1099KComputationRulesTests(unittest.TestCase):
    """Focused tests for the 5 Form 1099-K computation rules and recorded presentation."""

    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1099k-comp-test-")
        self.addCleanup(self.temp.cleanup)
        self.workspace_dir = Path(self.temp.name) / "workspace"
        self.capability = WorkspaceCapability(self.workspace_dir)
        self.registry = tax_registry()
        self.log = ActLog(self.workspace_dir, self.registry)
        _seed_workspace(self.log)
        self.records = RecordStream(self.workspace_dir / "records", DerivationSchemas())

    def _record_and_review(
        self,
        *,
        box1a: float,
        answers: dict[str, Any],
        run_id: str,
        payer: str = PAYER,
        stmt: str = STMT,
    ) -> dict[str, Any]:
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=payer,
            statement_ref=stmt,
            box1a=box1a,
            box4=0.0,
            submission_id=f"demo.stmt.{run_id}",
            evidence_id=f"demo.stmt.ev.{run_id}",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = cast(dict[str, str], stmt_res["statement_keys"])
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id=f"demo.rev.{run_id}",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        save_f1099k_statement_review(
            self.log,
            self.registry,
            rev,
            answers=answers,
            submission_id=f"demo.ans.{run_id}",
            evidence_ids=_evidence_ids(answers, prefix=f"demo.ans.ev.{run_id}"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, run_id)
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        return review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id=f"demo.outcome.rev.{run_id}",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )

    def test_figures_platform_pass_through_shipping(self) -> None:
        """Platform pass-through: buyer shipping passes through Box 1a; seller paid $0 shipping."""
        answers = {
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
        review = self._record_and_review(box1a=880.0, answers=answers, run_id="pt-shipping")
        self.assertEqual(review["savedCalculationState"], "current-supported-loss")
        self.assertEqual(review["savedState"], "supported-loss")
        calc = review["savedCalculation"]
        self.assertEqual(calc["status"], "supported-loss")
        self.assertEqual(calc["box1a"], 880.0)
        self.assertEqual(calc["assumptions"], "none")
        comp = calc["computation"]
        self.assertIsNotNone(comp)
        self.assertEqual(comp["amountRealized"], 800.0)
        self.assertEqual(comp["sellingExpenses"], 80.0)
        self.assertEqual(comp["netProceeds"], 720.0)
        self.assertEqual(comp["adjustedBasis"], 1000.0)
        self.assertEqual(comp["expectedBox1aGrossAmount"], 880.0)
        self.assertEqual(comp["comparison"], "net proceeds < adjusted basis")

    def test_figures_seller_received_shipping(self) -> None:
        """Seller received shipping: buyer-paid shipping adds to amount realized; seller-paid shipping adds to expenses."""
        answers = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 500.0,
            "shipping-arrangement": "seller-received-shipping",
            "platform-fees": 50.0,
            "seller-paid-shipping": 25.0,
            "sales-tax-collected-by-platform": 40.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 30.0,
            "purchase-cost": 700.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        # Box 1a = $500 (price) + $40 (tax) + $30 (buyer ship) = $570
        review = self._record_and_review(box1a=570.0, answers=answers, run_id="sr-shipping")
        self.assertEqual(review["savedCalculationState"], "current-supported-loss")
        calc = review["savedCalculation"]
        self.assertEqual(calc["status"], "supported-loss")
        self.assertEqual(calc["assumptions"], "none")
        comp = calc["computation"]
        self.assertEqual(comp["amountRealized"], 530.0)  # $500 + $30
        self.assertEqual(comp["sellingExpenses"], 75.0)   # $50 + $25
        self.assertEqual(comp["netProceeds"], 455.0)       # $530 - $75
        self.assertEqual(comp["adjustedBasis"], 700.0)
        self.assertEqual(comp["expectedBox1aGrossAmount"], 570.0)
        self.assertEqual(comp["comparison"], "net proceeds < adjusted basis")

    def test_figures_with_refunds(self) -> None:
        """Refunds given back reduce the amount realized."""
        answers = {
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
            "refund-amount": 50.0,  # $50 refund given back
            "buyer-paid-shipping": 24.0,
            "purchase-cost": 1000.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        review = self._record_and_review(box1a=880.0, answers=answers, run_id="refund-sale")
        self.assertEqual(review["savedCalculationState"], "current-supported-loss")
        comp = review["savedCalculation"]["computation"]
        self.assertEqual(comp["amountRealized"], 750.0)  # $800 - $50
        self.assertEqual(comp["sellingExpenses"], 80.0)
        self.assertEqual(comp["netProceeds"], 670.0)      # $750 - $80
        self.assertEqual(comp["adjustedBasis"], 1000.0)
        self.assertEqual(comp["comparison"], "net proceeds < adjusted basis")

    def test_figures_shipping_none_arrangement(self) -> None:
        """Local pickup / digital delivery: shipping arrangement 'none', no shipping amounts."""
        answers = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "personal-use",
            "exclusive-personal-use": "yes",
            "digital-asset-involvement": "no",
            "agreed-item-price": 300.0,
            "shipping-arrangement": "none",
            "platform-fees": 30.0,
            "seller-paid-shipping": 0.0,
            "sales-tax-collected-by-platform": 0.0,
            "refund-amount": 0.0,
            "buyer-paid-shipping": 0.0,
            "purchase-cost": 400.0,
            "cost-basis-known": "yes",
            "lasting-improvements-or-adjustments": "no",
        }
        review = self._record_and_review(box1a=300.0, answers=answers, run_id="none-shipping")
        self.assertEqual(review["savedCalculationState"], "current-supported-loss")
        comp = review["savedCalculation"]["computation"]
        self.assertEqual(comp["amountRealized"], 300.0)
        self.assertEqual(comp["sellingExpenses"], 30.0)
        self.assertEqual(comp["netProceeds"], 270.0)
        self.assertEqual(comp["adjustedBasis"], 400.0)
        self.assertEqual(comp["expectedBox1aGrossAmount"], 300.0)
        self.assertEqual(comp["comparison"], "net proceeds < adjusted basis")

    def test_not_computed_paths(self) -> None:
        """When an amount or gate is omitted or unknown, dependent figures publish 'not-computed'."""
        # 1. Unanswered platform fees: withdrawal via Track 2 review operations
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref="stmt-notcomp-1",
            box1a=880.0,
            box4=0.0,
            submission_id="demo.stmt.notcomp1",
            evidence_id="demo.stmt.ev.notcomp1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = cast(dict[str, str], stmt_res["statement_keys"])
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.rev.notcomp1",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        answers = {
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
            rev,
            answers=answers,
            submission_id="demo.ans.notcomp1",
            evidence_ids=_evidence_ids(answers, prefix="demo.ans.ev.notcomp1"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        # Prepare fresh review reflecting saved revision before withdrawal
        rev_to_withdraw = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.rev.notcomp1-withdraw",
            shown_at="2026-10-16T12:02:30Z",
            statement_keys=stmt_keys,
        )
        withdraw_f1099k_statement_review_answers(
            self.log,
            self.registry,
            rev_to_withdraw,
            questions=["platform-fees"],
            submission_id="demo.ans.withdraw-fees",
            actor=USER,
            at="2026-10-16T12:03:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "notcomp1-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.outcome.rev.notcomp1",
            shown_at="2026-10-16T12:04:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review["savedState"], "actually-unresolved")
        unres = review["savedUnresolvedExplanation"]
        self.assertEqual(unres["assumptions"], "none")
        comp = unres["computation"]
        # When platform-fees is unanswered, computation figures are unpinned but published figures are retained (Finding 1)
        # Expected values derived from scenario's recorded answers per track3-computation.md Case 4:
        # agreed-item-price ($800) - refunds ($0) = $800
        # platform-fees is unanswered -> selling expenses and net proceeds are not-computed
        # purchase-cost ($1,000) + improvements ($0) = $1,000
        # expected Box 1a is $880
        self.assertEqual(comp["amountRealized"], 800)
        self.assertEqual(comp["sellingExpenses"], "not-computed")
        self.assertEqual(comp["netProceeds"], "not-computed")
        self.assertEqual(comp["adjustedBasis"], 1000)
        self.assertEqual(comp["expectedBox1aGrossAmount"], 880)
        self.assertEqual(comp["comparison"], "not-computed")
        assert outcome.publications is not None
        stmt_pubs = {
            str(pub.finding.get("symbol", "")).split("|")[0]: pub.finding.get("value")
            for pub in outcome.publications
            if isinstance(getattr(pub, "finding", None), Mapping)
            and f"statement={stmt_keys['statement']}" in str(pub.finding.get("symbol", ""))
        }
        self.assertEqual(comp["amountRealized"], float(str(stmt_pubs["tax.us.2025.f1099k.amount-realized"])))
        self.assertEqual(comp["sellingExpenses"], stmt_pubs["tax.us.2025.f1099k.selling-expenses"])
        self.assertEqual(comp["netProceeds"], stmt_pubs["tax.us.2025.f1099k.net-proceeds"])
        self.assertEqual(comp["adjustedBasis"], float(str(stmt_pubs["tax.us.2025.f1099k.adjusted-basis"])))
        self.assertEqual(comp["expectedBox1aGrossAmount"], float(str(stmt_pubs["tax.us.2025.f1099k.expected-box1a-gross-amount"])))
        self.assertTrue(any("platform selling fees" in s for s in unres["reasonSentences"]))

        # 2. Answer platform-fees back so fees are known
        rev_before_reans = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.rev.notcomp-reans",
            shown_at="2026-10-16T12:04:30Z",
            statement_keys=stmt_keys,
        )
        answer_f1099k_statement_review_question(
            self.log,
            self.registry,
            rev_before_reans,
            question="platform-fees",
            answer=80.0,
            submission_id="demo.ans.reans-fees",
            evidence_id="demo.ans.ev.reans-fees",
            actor=USER,
            at="2026-10-16T12:04:45Z",
        )

        # 3. Correct cost-basis-known to cannot-tell
        rev_before_corr = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.rev.notcomp2",
            shown_at="2026-10-16T12:05:00Z",
            statement_keys=stmt_keys,
        )
        correct_f1099k_statement_review_answer(
            self.log,
            self.registry,
            rev_before_corr,
            question="cost-basis-known",
            answer="cannot-tell",
            submission_id="demo.ans.corr-basis",
            evidence_id="demo.ans.ev.corr-basis",
            actor=USER,
            at="2026-10-16T12:06:00Z",
        )
        outcome2 = _run_workspace(self.capability, self.log, "notcomp2-run")
        self.assertIsNone(outcome2.refusal)
        assert outcome2.presentation_path is not None
        review2 = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome2.presentation_path,
            self.records,
            review_id="demo.outcome.rev.notcomp2",
            shown_at="2026-10-16T12:07:00Z",
            statement_keys=stmt_keys,
        )
        unres2 = review2["savedUnresolvedExplanation"]
        comp2 = unres2["computation"]
        self.assertEqual(comp2["adjustedBasis"], "not-computed")
        self.assertEqual(comp2["amountRealized"], 800)
        self.assertEqual(comp2["sellingExpenses"], 80)
        self.assertEqual(comp2["netProceeds"], 720)
        self.assertEqual(comp2["expectedBox1aGrossAmount"], 880)
        self.assertEqual(comp2["comparison"], "not-computed")
        self.assertTrue(any("purchase cost of the item is unknown" in s for s in unres2["reasonSentences"]))

    def test_reconciliation_stop_shows_mismatched_figures(self) -> None:
        """When Box 1a does not reconcile with price + tax + shipping, reconciliation stop retains expected Box 1a."""
        answers = {
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
        # Expected Box 1a is $880.0 ($800 price + $56 tax + $24 buyer ship).
        # Report $950.0 on the Form 1099-K -> reconciliation discrepancy!
        review = self._record_and_review(box1a=950.0, answers=answers, run_id="recon-mismatch")
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review["savedState"], "actually-unresolved")
        unres = review["savedUnresolvedExplanation"]
        self.assertEqual(unres["assumptions"], "none")
        comp = unres["computation"]
        # All 5 published figures are retained on reconciliation discrepancy stop (Finding 1)
        self.assertEqual(comp["expectedBox1aGrossAmount"], 880.0)
        self.assertEqual(comp["amountRealized"], 800)
        self.assertEqual(comp["sellingExpenses"], 80)
        self.assertEqual(comp["netProceeds"], 720)
        self.assertEqual(comp["adjustedBasis"], 1000)
        self.assertEqual(comp["comparison"], "not-computed")
        self.assertTrue(any("reconcile" in s.lower() for s in unres["reasonSentences"]))

    def test_absent_box4_reports_declared_default_assumption(self) -> None:
        """R1: A run whose Box 4 finding is absent reports the Box 4 declared default as an assumption actually used."""
        acts = _make_base_acts(wages=90000.0)
        payer = "demo.platform.nobox4"
        stmt = "demo.stmt.nobox4"
        _add_statement_entities(acts, payer, stmt)
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.nobox4", _statement_fact_id(BOX1A, payer, stmt), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        # Circumstance answers for supported loss, but Box 4 finding is omitted
        ans = {
            Q1: "yes", Q3: "yes", Q4: "personal-use", Q5: "yes", Q7: "no",
            Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
            Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0,
            Q11_BUYER_SHIP: 24.0, Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
        }
        for fact_id, val in ans.items():
            short = fact_id.rsplit(".", 1)[-1]
            acts.append(_act(len(acts), "assertion", {"finding": _attested(f"f.{short}.{stmt}", _statement_fact_id(fact_id, payer, stmt), val)}))
        _add_family_closure(acts, "demo.f1099k.h1", closed=True)
        finished_acts = _finish_acts(acts)

        ws_dir = Path(self.temp.name) / "ws-nobox4"
        cap = WorkspaceCapability(ws_dir)
        log = ActLog(ws_dir, self.registry)
        log.append_batch(finished_acts, expected_revision=0)
        outcome = _run_workspace(cap, log, "run-nobox4")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        expl = model["f1099kStatementExplanation"][stmt]
        self.assertEqual(expl["reason"], "supported-loss")
        self.assertIsInstance(expl["assumptions"], list)
        self.assertEqual(len(expl["assumptions"]), 1)
        self.assertEqual(expl["assumptions"][0]["factId"], BOX4)
        self.assertEqual(expl["assumptions"][0]["declaredDefault"], 0)

        # Review with saved presentation carries the assumptions list
        stmt_keys = {"payer": payer, "statement": stmt, "tax-year": "2025"}
        rev = review_f1099k_statement_with_saved_presentation(
            log,
            self.registry,
            outcome.presentation_path,
            RecordStream(ws_dir / "records", DerivationSchemas()),
            review_id="demo.outcome.rev.nobox4",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(rev["savedCalculationState"], "current-supported-loss")
        calc = rev["savedCalculation"]
        self.assertEqual(calc["assumptions"], expl["assumptions"])

    def test_two_statements_per_statement_explanation(self) -> None:
        """R3: Two statements (out of scope) each show their own recorded figures and reason."""
        acts = _make_base_acts(wages=90000.0)
        payer_a, stmt_a = "demo.platform.a", "demo.stmt.a"
        payer_b, stmt_b = "demo.platform.b", "demo.stmt.b"
        _add_statement_entities(acts, payer_a, stmt_a)
        _add_statement_entities(acts, payer_b, stmt_b)
        acts.append(_act(len(acts), "horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": {"tax-year": "2025", "subject": "demo.primary"}, "horizon_id": "demo.f1099k.h0"}))
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.a", _statement_fact_id(BOX1A, payer_a, stmt_a), 880.0)},
            "successor": {"id": "demo.f1099k.h1", "predecessor": "demo.f1099k.h0"},
        }))
        _add_statement_assertions(
            acts, payer=payer_a, stmt=stmt_a, box1a=880.0, box4=0.0,
            answers={
                Q8_PRICE: 800.0, Q8_SHIP: "platform-pass-through", Q9_FEES: 80.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 56.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 24.0,
                Q12_COST: 1000.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        acts.append(_act(len(acts), "member-transition", {
            "family": {"id": FAMILY_ID, "version": "v1"},
            "scope": {"tax-year": "2025", "subject": "demo.primary"},
            "member": {"action": "assert", "finding": _attested("f.b1a.stmt.b", _statement_fact_id(BOX1A, payer_b, stmt_b), 400.0)},
            "successor": {"id": "demo.f1099k.h2", "predecessor": "demo.f1099k.h1"},
        }))
        _add_statement_assertions(
            acts, payer=payer_b, stmt=stmt_b, box1a=400.0, box4=0.0,
            answers={
                Q8_PRICE: 400.0, Q8_SHIP: "none", Q9_FEES: 50.0,
                Q9_SELLER_SHIP: 0.0, Q10_TAX: 0.0, Q10_REFUND: 0.0, Q11_BUYER_SHIP: 0.0,
                Q12_COST: 500.0, Q12_GATE: "yes", Q13: "no",
            },
        )
        _add_family_closure(acts, "demo.f1099k.h2", closed=True)
        finished_acts = _finish_acts(acts)

        ws_dir = Path(self.temp.name) / "ws-twostmts"
        cap = WorkspaceCapability(ws_dir)
        log = ActLog(ws_dir, self.registry)
        log.append_batch(finished_acts, expected_revision=0)
        outcome = _run_workspace(cap, log, "run-twostmts")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        f1099k_expl = model["f1099kStatementExplanation"]
        self.assertIn(stmt_a, f1099k_expl)
        self.assertIn(stmt_b, f1099k_expl)

        expl_a = f1099k_expl[stmt_a]
        self.assertEqual(expl_a["reason"], "multiple-f1099k-out-of-scope")
        self.assertEqual(expl_a["statementKeys"]["statement"], stmt_a)
        self.assertEqual(expl_a["statementKeys"]["payer"], payer_a)

        expl_b = f1099k_expl[stmt_b]
        self.assertEqual(expl_b["reason"], "multiple-f1099k-out-of-scope")
        self.assertEqual(expl_b["statementKeys"]["statement"], stmt_b)
        self.assertEqual(expl_b["statementKeys"]["payer"], payer_b)

        # Both statements are reviewed separately and resolve their respective explanation
        records = RecordStream(ws_dir / "records", DerivationSchemas())
        rev_a = review_f1099k_statement_with_saved_presentation(
            log,
            self.registry,
            outcome.presentation_path,
            records,
            review_id="demo.outcome.rev.stmt-a",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys={"payer": payer_a, "statement": stmt_a, "tax-year": "2025"},
        )
        self.assertEqual(rev_a["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(rev_a["savedUnresolvedExplanation"]["statementKeys"]["statement"], stmt_a)
        self.assertTrue(any("multiple" in s.lower() for s in rev_a["savedUnresolvedExplanation"]["reasonSentences"]))

        rev_b = review_f1099k_statement_with_saved_presentation(
            log,
            self.registry,
            outcome.presentation_path,
            records,
            review_id="demo.outcome.rev.stmt-b",
            shown_at="2026-10-16T12:04:00Z",
            statement_keys={"payer": payer_b, "statement": stmt_b, "tax-year": "2025"},
        )
        self.assertEqual(rev_b["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(rev_b["savedUnresolvedExplanation"]["statementKeys"]["statement"], stmt_b)
        self.assertTrue(any("multiple" in s.lower() for s in rev_b["savedUnresolvedExplanation"]["reasonSentences"]))

    def test_exclusion_stop_retains_published_figures_and_missing_fallback(self) -> None:
        """An early exclusion stop (investment-purpose-excluded) retains published figures.

        Also asserts that a figure absent from publications stays 'missing',
        and a second statement's figures are never matched.
        """
        stmt_res = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER,
            statement_ref="stmt-exclusion-1",
            box1a=880.0,
            box4=0.0,
            submission_id="demo.stmt.excl1",
            evidence_id="demo.stmt.ev.excl1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=self.log.read().revision,
        )
        stmt_keys = cast(dict[str, str], stmt_res["statement_keys"])
        rev = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.rev.excl1",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=stmt_keys,
        )
        answers = {
            "covers-only-single-item": "yes",
            "acquired-by-purchase": "yes",
            "primary-purpose-at-acquisition": "investment-or-profit",
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
            rev,
            answers=answers,
            submission_id="demo.ans.excl1",
            evidence_ids=_evidence_ids(answers, prefix="demo.ans.ev.excl1"),
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        outcome = _run_workspace(self.capability, self.log, "excl1-run")
        self.assertIsNone(outcome.refusal)
        assert outcome.presentation_path is not None
        review = review_f1099k_statement_with_saved_presentation(
            self.log,
            self.registry,
            outcome.presentation_path,
            self.records,
            review_id="demo.outcome.rev.excl1",
            shown_at="2026-10-16T12:03:00Z",
            statement_keys=stmt_keys,
        )
        self.assertEqual(review["savedCalculationState"], "current-unresolved-explanation")
        self.assertEqual(review["savedState"], "actually-unresolved")
        unres = review["savedUnresolvedExplanation"]
        self.assertEqual(unres["assumptions"], "none")
        self.assertTrue(any("investment" in s.lower() for s in unres["reasonSentences"]))

        comp = unres["computation"]
        self.assertEqual(comp["amountRealized"], 800)
        self.assertEqual(comp["sellingExpenses"], 80)
        self.assertEqual(comp["netProceeds"], 720)
        self.assertEqual(comp["adjustedBasis"], 1000)
        self.assertEqual(comp["expectedBox1aGrossAmount"], 880)
        self.assertEqual(comp["comparison"], "not-computed")

        assert outcome.publications is not None
        stmt_pubs = {
            str(pub.finding.get("symbol", "")).split("|")[0]: pub.finding.get("value")
            for pub in outcome.publications
            if isinstance(getattr(pub, "finding", None), Mapping)
            and f"statement={stmt_keys['statement']}" in str(pub.finding.get("symbol", ""))
        }
        self.assertEqual(comp["amountRealized"], float(str(stmt_pubs["tax.us.2025.f1099k.amount-realized"])))
        self.assertEqual(comp["sellingExpenses"], float(str(stmt_pubs["tax.us.2025.f1099k.selling-expenses"])))
        self.assertEqual(comp["netProceeds"], float(str(stmt_pubs["tax.us.2025.f1099k.net-proceeds"])))
        self.assertEqual(comp["adjustedBasis"], float(str(stmt_pubs["tax.us.2025.f1099k.adjusted-basis"])))
        self.assertEqual(comp["expectedBox1aGrossAmount"], float(str(stmt_pubs["tax.us.2025.f1099k.expected-box1a-gross-amount"])))

        # Unit assertion on _f1099k_statement_computation:
        # 1. Figure absent from publications stays "missing"
        # 2. Second statement's figures are never matched
        from packages.derivation.presentation_projection import _f1099k_statement_computation
        reason_finding = next(
            pub.finding for pub in outcome.publications
            if isinstance(getattr(pub, "finding", None), Mapping)
            and "tax.us.2025.f1099k.statement-loss-reason" in str(pub.finding.get("symbol", ""))
        )
        partial_pubs = [
            pub for pub in outcome.publications
            if isinstance(getattr(pub, "finding", None), Mapping)
            and "tax.us.2025.f1099k.adjusted-basis" not in str(pub.finding.get("symbol", ""))
        ]
        comp_partial = _f1099k_statement_computation(
            reason_finding,
            {},
            publications=partial_pubs,
            statement_keys=stmt_keys,
        )
        self.assertEqual(comp_partial["amountRealized"], 800)
        self.assertEqual(comp_partial["adjustedBasis"], "missing")

        second_stmt_pubs = [
            {
                "finding": {
                    "symbol": "tax.us.2025.f1099k.adjusted-basis|tax.us.2025.f1099k.box1a-gross-amount|payer=demo.platform.a,statement=stmt.other.stmt-2,tax-year=2025",
                    "value": "999.0",
                }
            }
        ]
        comp_second_stmt = _f1099k_statement_computation(
            reason_finding,
            {},
            publications=second_stmt_pubs,
            statement_keys=stmt_keys,
        )
        self.assertEqual(comp_second_stmt["adjustedBasis"], "missing")


if __name__ == "__main__":
    unittest.main()
