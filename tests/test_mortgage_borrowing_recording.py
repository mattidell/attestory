"""Mortgage borrowing recorder scope, lifecycle, and clear behavior."""
from __future__ import annotations

import json
import copy
import tempfile
import unittest
import pytest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.derivation.marshal import (
    MortgagePaymentApplicabilityInvalid, MortgagePaymentApplicabilityMissing, marshal_run_context,
)
from packages.tax.loader import load_mortgage_borrowing_bundle, tax_registry
from packages.tax.mortgage_borrowing_recording import (
    BORROWING_KIND, MortgageBorrowingRecordingRefused,
    clear_mortgage_borrowing_year_durably,
    correct_mortgage_borrowing_claim_durably,
    introduce_mortgage_borrowing_reference_durably,
    current_mortgage_payment_comparison_applicability,
    current_mortgage_payment_comparison_support,
    record_mortgage_borrowing_claim_durably,
    withdraw_mortgage_borrowing_claim_durably,
)
from tests.test_f1098_statement_review import _append_seed
from packages.tax.mortgage_borrowing_review import (
    MortgageBorrowingReviewRefused, correct_mortgage_borrowing_review_answer,
    prepare_mortgage_borrowing_review,
    record_mortgage_borrowing_review_answer,
)


@pytest.mark.live(reason="Durable recorder stories exercise ActLog admission and recovery beyond the fast-lane budget")
class MortgageBorrowingRecordingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="mortgage-borrowing-recording-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)
        _append_seed(self.log, second_interest=5000)
        load_mortgage_borrowing_bundle(self.registry)
        self.actor = "demo.taxpayer"
        self.a = "demo.mortgage.borrowing.a"
        self.b = "demo.mortgage.borrowing.b"
        for reference in (self.a, self.b):
            introduce_mortgage_borrowing_reference_durably(
                self.log, self.registry, reference_id=reference, description="Same displayed lender",
                actor=self.actor, at="2026-10-23T12:00:00Z")

    def _record(self, claim: str, borrowing: str, value: Any, suffix: str,
                statement: str | None = None) -> dict[str, Any]:
        keys = None if statement is None else {
            "payer": "demo.f1098.lender.a" if statement.endswith("a") else "demo.f1098.lender.b",
            "statement": f"demo.f1098.stmt.{statement}", "tax-year": "2025",
        }
        return record_mortgage_borrowing_claim_durably(
            self.log, self.registry, claim=claim, borrowing_ref=borrowing, value=value,
            submission_id=f"demo.mortgage.submission.{suffix}",
            evidence_id=f"demo.mortgage.evidence.{suffix}", actor=self.actor,
            at="2026-10-23T12:01:00Z", statement_keys=keys,
            expected_revision=self.log.read().revision)

    def test_two_same_labeled_references_are_distinct_and_require_current_kind(self) -> None:
        state = project(self.log.read().acts, self.registry)
        self.assertNotEqual(self.a, self.b)
        self.assertEqual(state.fact_state.entities[self.a].entity["kind"], BORROWING_KIND)
        self.assertEqual(state.fact_state.entities[self.b].entity["kind"], BORROWING_KIND)
        revision = self.log.read().revision
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            self._record("continuing-borrowing", "demo.f1098.stmt.a", "yes", "wrong-kind")
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            self._record("continuing-borrowing", "demo.mortgage.borrowing.ended", "yes", "missing")
        self.log.append({"schema": "act.v1", "act_id": "demo.mortgage.borrowing.end-a",
                         "kind": "entity-superseded", "actor": self.actor,
                         "at": "2026-10-23T12:00:30Z", "committed_against": revision,
                         "payload": {"entity_id": self.a}}, expected_revision=revision)
        ended_revision = self.log.read().revision
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            self._record("continuing-borrowing", self.a, "yes", "ended")
        self.assertEqual(self.log.read().revision, ended_revision)

    def test_exact_report_outcomes_and_claim_correction_keep_other_pair(self) -> None:
        first = self._record("report-inclusion", self.a, "affirmed", "link-a", "a")
        second = self._record("report-inclusion", self.a, "affirmed", "link-b", "b")
        corrected = correct_mortgage_borrowing_claim_durably(
            self.log, self.registry, finding_id=first["finding_id"], claim="report-inclusion",
            borrowing_ref=self.a, value="cannot-tell", submission_id="demo.mortgage.submission.correct-a",
            evidence_id="demo.mortgage.evidence.correct-a", actor=self.actor,
            at="2026-10-23T12:02:00Z", statement_keys={"payer":"demo.f1098.lender.a",
            "statement":"demo.f1098.stmt.a", "tax-year":"2025"}, expected_revision=self.log.read().revision)
        state = project(self.log.read().acts, self.registry)
        current = compute_currency(state).current_finding_ids
        self.assertNotIn(first["finding_id"], current)
        self.assertIn(second["finding_id"], current)
        lattice = facts_of(state.fact_state, include_displaced=True)
        row = state.findings[corrected["finding_id"]]
        self.assertEqual(lattice[row["fact_id"]].fact_type_id, "tax.us.2025.f1098.borrowing-unresolved")

    def test_ceiling_validation_evidence_and_atomic_account_clear_preserve_other_debt(self) -> None:
        start = self.log.read().revision
        for invalid in (-1, True, float("inf"), float("nan")):
            with self.assertRaises(MortgageBorrowingRecordingRefused):
                self._record("annual-ceiling", self.a, invalid, f"invalid-{str(invalid)}")
        self.assertEqual(self.log.read().revision, start)
        recognition = self._record("continuing-borrowing", self.a, "yes", "recognition")
        link_a = self._record("report-inclusion", self.a, "affirmed", "clear-link-a", "a")
        link_b = self._record("report-inclusion", self.a, "affirmed", "clear-link-b", "b")
        ceiling = self._record("annual-ceiling", self.a, 240000, "ceiling")
        shared_answers = [
            self._record("owes-the-loan", self.a, "yes", "clear-shared-owes"),
            self._record("no-one-else-owes-it", self.a, "yes", "clear-shared-no-others"),
            self._record("what-the-money-paid-for", self.a, "bought-the-home", "clear-shared-proceeds"),
            self._record("this-is-the-original-loan", self.a, "yes", "clear-shared-original"),
            self._record("mortgage-credit-certificate-received", self.a, "received", "clear-shared-certificate"),
        ]
        shared_evidence = self.log.read().acts
        no_others_evidence = next(row["payload"]["evidence"] for row in shared_evidence
                                  if row.get("kind") == "evidence-submitted"
                                  and row.get("payload", {}).get("evidence", {}).get("id")
                                  == shared_answers[1]["evidence_id"])
        self.assertEqual(no_others_evidence["content"]["response_meaning"],
                         "no other obligor beyond the joint-filing spouses")
        other = self._record("other-secured-home-debt", self.a, "no", "other-debt")
        recognition_b = self._record("continuing-borrowing", self.b, "yes", "recognition-b")
        ceiling_b = self._record("annual-ceiling", self.b, 200000, "ceiling-b")
        shared_b = self._record("owes-the-loan", self.b, "yes", "shared-b")
        acts_before = self.log.read().acts
        state_before = project(acts_before, self.registry)
        current_before = compute_currency(state_before).current_finding_ids
        facts_before = facts_of(state_before.fact_state, include_displaced=True)
        protected_ids = {fid for fid, row in state_before.findings.items() if fid in current_before
                         and facts_before[row["fact_id"]].fact_type_id.startswith("tax.us.2025.f1098.")
                         and "borrowing-" not in facts_before[row["fact_id"]].fact_type_id}
        result = clear_mortgage_borrowing_year_durably(
            self.log, self.registry, borrowing_ref=self.a, actor=self.actor,
            at="2026-10-23T12:03:00Z", expected_revision=self.log.read().revision)
        self.assertEqual(set(result["ended_finding_ids"]),
                         {recognition["finding_id"], link_a["finding_id"], link_b["finding_id"],
                          ceiling["finding_id"], *(row["finding_id"] for row in shared_answers)})
        state = project(self.log.read().acts, self.registry)
        current = compute_currency(state).current_finding_ids
        self.assertIn(other["finding_id"], current)
        self.assertTrue({recognition_b["finding_id"], ceiling_b["finding_id"], shared_b["finding_id"]} <= current)
        self.assertTrue(protected_ids <= current)
        self.assertEqual({fid: state.findings[fid] for fid in protected_ids},
                         {fid: state_before.findings[fid] for fid in protected_ids})
        self.assertEqual(len(state.findings), len(project(acts_before, self.registry).findings))
        self.assertTrue(any(row.get("kind") == "finding-retracted"
                            for row in self.log.read().acts[len(acts_before):]))
        self.assertNotIn(fact_id_for("tax.us.2025.mortgage.other-secured-home-debt",
                                     (("borrowing", self.b), ("tax-year", "2025"))),
                         {finding["fact_id"] for finding in state.findings.values()})

    def test_retraction_and_stale_revision_are_scoped(self) -> None:
        answer = self._record("what-the-money-paid-for", self.a, "bought-the-home", "proceeds")
        revision = self.log.read().revision
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="annual-ceiling", borrowing_ref=self.a, value=100,
                submission_id="demo.mortgage.submission.stale", evidence_id="demo.mortgage.evidence.stale",
                actor=self.actor, at="2026-10-23T12:04:00Z", expected_revision=revision - 1)
        result = withdraw_mortgage_borrowing_claim_durably(
            self.log, self.registry, finding_id=answer["finding_id"], claim="what-the-money-paid-for",
            borrowing_ref=self.a, actor=self.actor, at="2026-10-23T12:05:00Z",
            expected_revision=self.log.read().revision)
        self.assertEqual(result["finding_id"], answer["finding_id"])
        self.assertNotIn(answer["finding_id"], compute_currency(result["state"]).current_finding_ids)

    def test_all_five_shared_answers_use_distinct_types_and_evidence(self) -> None:
        cases = (
            ("owes-the-loan", "yes"),
            ("no-one-else-owes-it", "yes"),
            ("what-the-money-paid-for", "bought-the-home"),
            ("this-is-the-original-loan", "yes"),
            ("mortgage-credit-certificate-received", "received"),
        )
        saved = [self._record(question, self.a, value, f"shared-{index}")
                 for index, (question, value) in enumerate(cases)]
        self.assertEqual(len({row["fact_type"] for row in saved}), 5)
        self.assertTrue(all(row["fact_type"].startswith("tax.us.2025.mortgage.shared-") for row in saved))
        state = project(self.log.read().acts, self.registry)
        lattice = facts_of(state.fact_state, include_displaced=True)
        for (question, value), row in zip(cases, saved, strict=True):
            evidence = state.evidence[row["evidence_id"]].evidence["content"]
            self.assertEqual(evidence["claim"], question)
            self.assertEqual(evidence["value"], value)
            self.assertEqual(row["fact_type"], lattice[state.findings[row["finding_id"]]["fact_id"]].fact_type_id)

    def test_payment_comparisons_bind_each_answer_to_the_exact_current_pair(self) -> None:
        self._record("continuing-borrowing", self.a, "yes", "comparison-recognition")
        self._record("report-inclusion", self.a, "affirmed", "comparison-link-a", "a")
        self._record("report-inclusion", self.a, "affirmed", "comparison-link-b", "b")
        review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.payment-comparison",
            shown_at="2026-10-23T12:10:00Z", borrowing_ref=self.a)
        offers = [row for row in review["answers"] if row["claim"] == "payment-comparison"]
        self.assertEqual(len(offers), 2)
        self.assertTrue(all(row["state"] == "absent" and row["comparisonSupport"] is not None for row in offers))
        recorded = []
        for index, offer in enumerate(offers):
            if index:
                review = prepare_mortgage_borrowing_review(
                    self.log, self.registry, review_id=f"demo.mortgage.review.payment-comparison.{index}",
                    shown_at="2026-10-23T12:10:02Z", borrowing_ref=self.a)
                offer = next(row for row in review["answers"] if row["claim"] == "payment-comparison"
                             and row["scope"]["statement"] == offer["scope"]["statement"])
            own = {key: offer["scope"][key] for key in ("payer", "statement", "tax-year")}
            recorded.append(record_mortgage_borrowing_review_answer(
                self.log, self.registry, review, claim="payment-comparison", borrowing_ref=self.a,
                value="different-payments", submission_id=f"demo.mortgage.payment-comparison.{index}",
                evidence_id=f"demo.mortgage.payment-comparison.{index}.evidence", actor=self.actor,
                at="2026-10-23T12:10:01Z", statement_keys=own, peer_statement_keys=offer["peerScope"]))
        state = project(self.log.read().acts, self.registry)
        current = compute_currency(state).current_finding_ids
        self.assertTrue(all(row["finding_id"] in current for row in recorded))
        applicable = current_mortgage_payment_comparison_applicability(self.log.read().acts, self.registry)
        self.assertEqual({row["finding_id"] for row in applicable if row["applicability"] == "current"},
                         {row["finding_id"] for row in recorded})
        current_state = project(self.log.read().acts, self.registry)
        current_currency = compute_currency(current_state)
        cold = current_mortgage_payment_comparison_applicability(self.log.read().acts, self.registry)
        same_projection = current_mortgage_payment_comparison_applicability(
            self.log.read().acts, self.registry, state=current_state, currency=current_currency,
            lattice=facts_of(current_state.fact_state))
        self.assertEqual(cold, same_projection)
        marshal_args: dict[str, Any] = dict(run_id="demo.mortgage.comparison.marshal", state=current_state,
                            currency=current_currency, rules=[], parameters={}, canon={},
                            adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
                            governance_pins=[])
        with self.assertRaises(MortgagePaymentApplicabilityMissing):
            marshal_run_context(**marshal_args)
        marshalled = marshal_run_context(**marshal_args, mortgage_payment_applicability=same_projection)
        markers = [source for source in marshalled.sources
                   if source.name == "tax.us.2025.mortgage.payment-comparison-support-marker"]
        self.assertEqual(len(markers), 8)
        malformed_readings: list[list[dict[str, Any]]] = [
            [same_projection[0], copy.deepcopy(same_projection[0]), same_projection[1]],
            [*same_projection, {**copy.deepcopy(same_projection[1]),
                                "finding_id": "demo.mortgage.comparison.extraneous"}],
        ]
        for index, field, value in (
            (0, "fact_id", "tax.us.2025.mortgage.report-payment-comparison|forged=true"),
            (0, "value", "copy-or-correction"),
            (0, "applicability", "unresolved-applicability"),
            (0, "borrowing", "demo.mortgage.borrowing.forged"),
            (0, "statement", {**same_projection[0]["statement"], "payer": "demo.f1098.lender.forged"}),
            (0, "peer_statement", {**same_projection[0]["peer_statement"],
                                    "statement": "demo.f1098.stmt.forged"}),
            (0, "comparison_support", {**same_projection[0]["comparison_support"],
                                        "recognition_finding_id": "demo.mortgage.recognition.forged"}),
        ):
            changed = copy.deepcopy(same_projection)
            changed[index][field] = value
            malformed_readings.append(changed)
        for readings in malformed_readings:
            with self.assertRaises(MortgagePaymentApplicabilityInvalid):
                marshal_run_context(**marshal_args, mortgage_payment_applicability=readings)
        for row in recorded:
            finding = state.findings[row["finding_id"]]
            evidence = state.evidence[row["evidence_id"]].evidence
            contribution = state.contributions[finding["contribution_id"]]
            self.assertEqual(finding["value"], "different-payments")
            self.assertEqual(evidence["content"]["value"], finding["value"])
            self.assertEqual(contribution["evidence_id"], row["evidence_id"])
            self.assertEqual(contribution["content"]["statement"], evidence["content"]["statement"])
            self.assertEqual(contribution["content"]["peer_statement"], evidence["content"]["peer_statement"])

    def test_payment_comparison_rejects_stale_or_foreign_pair_support(self) -> None:
        self._record("continuing-borrowing", self.a, "yes", "comparison-guard-recognition")
        self._record("report-inclusion", self.a, "affirmed", "comparison-guard-link-a", "a")
        self._record("report-inclusion", self.a, "affirmed", "comparison-guard-link-b", "b")
        review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.payment-comparison-guard",
            shown_at="2026-10-23T12:11:00Z", borrowing_ref=self.a)
        offer = next(row for row in review["answers"] if row["claim"] == "payment-comparison")
        own = {key: offer["scope"][key] for key in ("payer", "statement", "tax-year")}
        before = self.log.read().revision
        with self.assertRaises(MortgageBorrowingReviewRefused):
            record_mortgage_borrowing_review_answer(
                self.log, self.registry, review, claim="payment-comparison", borrowing_ref=self.a,
                value="different-payments", submission_id="demo.mortgage.payment-comparison.foreign",
                evidence_id="demo.mortgage.payment-comparison.foreign.evidence", actor=self.actor,
                at="2026-10-23T12:11:01Z", statement_keys=own,
                peer_statement_keys={"payer": "demo.f1098.lender.foreign", "statement": "demo.f1098.stmt.foreign",
                                     "tax-year": "2025"})
        self.assertEqual(self.log.read().revision, before)

    def test_unresolved_comparison_is_omitted_from_every_marshal_route(self) -> None:
        self._record("continuing-borrowing", self.a, "yes", "raw-comparison-recognition")
        self._record("report-inclusion", self.a, "affirmed", "raw-comparison-link-a", "a")
        self._record("report-inclusion", self.a, "affirmed", "raw-comparison-link-b", "b")
        comparison_type = "tax.us.2025.mortgage.report-payment-comparison"
        keys = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a",
                "tax-year": "2025", "borrowing": self.a}
        revision = self.log.read().revision
        self.log.append({
            "schema": "act.v1", "act_id": "demo.mortgage.raw-comparison-without-evidence.act",
            "kind": "assertion", "actor": self.actor, "at": "2026-10-23T12:11:30Z",
            "committed_against": revision,
            "payload": {"finding": {"schema": "finding.v2", "id": "demo.mortgage.raw-comparison-without-evidence",
                                      "fact_id": fact_id_for(comparison_type, tuple((key, keys[key]) for key in
                                                                                   ("payer", "statement", "tax-year", "borrowing"))),
                                      "value": "different-payments", "basis": "attested", "evidence_ids": []}},
        }, expected_revision=revision)
        state = project(self.log.read().acts, self.registry)
        currency = compute_currency(state)
        readings = current_mortgage_payment_comparison_applicability(
            self.log.read().acts, self.registry, state=state, currency=currency, lattice=facts_of(state.fact_state))
        self.assertEqual(len(readings), 1)
        self.assertEqual(readings[0]["applicability"], "unresolved-applicability")
        args: dict[str, Any] = {
            "run_id": "demo.mortgage.raw-comparison-marshal", "state": state, "currency": currency,
            "rules": [{"schema": "rule-artifact.v13", "requires": [comparison_type]}],
            "parameters": {}, "canon": {},
            "adoption_pin": {"role": "adoption", "id": "demo.package", "version": "v1"},
            "governance_pins": [],
            "input_bindings": [{"symbol": "demo.review.comparison-alias", "fact_type": {"id": comparison_type}}],
            "collect_source_names": [comparison_type],
            "mortgage_payment_applicability": readings,
        }
        marshalled = marshal_run_context(**args)
        self.assertNotIn("demo.review.comparison-alias", {item.symbol for item in marshalled.inputs})
        self.assertFalse(any(source.name == comparison_type for source in marshalled.sources))
        unresolved = [source for source in marshalled.sources
                      if source.name == "tax.us.2025.mortgage.payment-comparison-applicability-unresolved"]
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(unresolved[0].value, "unresolved-applicability")
        self.assertEqual(unresolved[0].finding_id, "demo.mortgage.raw-comparison-without-evidence")
        self.assertIsNotNone(unresolved[0].keys)
        self.assertEqual(dict(unresolved[0].keys or ()), keys)
        self.assertNotIn(comparison_type, {item.symbol for item in marshalled.inputs})

    def test_payment_comparison_requires_live_support_and_link_correction_ends_pair(self) -> None:
        recognition = self._record("continuing-borrowing", self.a, "yes", "comparison-lifecycle-recognition")
        link_rows = [self._record("report-inclusion", self.a, "affirmed", f"comparison-lifecycle-link-{suffix}", suffix)
                     for suffix in ("a", "b")]
        pair_support = current_mortgage_payment_comparison_support(self.log.read().acts, self.registry, self.a)
        self.assertIsNotNone(pair_support)
        before = self.log.read().revision
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="payment-comparison", borrowing_ref=self.a,
                value="different-payments", submission_id="demo.mortgage.comparison.lifecycle.unbound",
                evidence_id="demo.mortgage.comparison.lifecycle.unbound.evidence", actor=self.actor,
                at="2026-10-23T12:12:00Z", statement_keys={"payer": "demo.f1098.lender.a",
                "statement": "demo.f1098.stmt.a", "tax-year": "2025"},
                peer_statement_keys={"payer": "demo.f1098.lender.b", "statement": "demo.f1098.stmt.b",
                                     "tax-year": "2025"}, expected_revision=before)
        self.assertEqual(self.log.read().revision, before)

        comparison_ids = []
        for index, own, peer in ((0, "a", "b"), (1, "b", "a")):
            own_keys = {"payer": f"demo.f1098.lender.{own}", "statement": f"demo.f1098.stmt.{own}",
                        "tax-year": "2025"}
            peer_keys = {"payer": f"demo.f1098.lender.{peer}", "statement": f"demo.f1098.stmt.{peer}",
                         "tax-year": "2025"}
            saved = record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="payment-comparison", borrowing_ref=self.a,
                value="different-payments", submission_id=f"demo.mortgage.comparison.lifecycle.{index}",
                evidence_id=f"demo.mortgage.comparison.lifecycle.{index}.evidence", actor=self.actor,
                at=f"2026-10-23T12:12:0{index + 1}Z", statement_keys=own_keys,
                peer_statement_keys=peer_keys, comparison_support=pair_support,
                expected_revision=self.log.read().revision)
            comparison_ids.append(saved["finding_id"])

        correction = correct_mortgage_borrowing_claim_durably(
            self.log, self.registry, finding_id=link_rows[0]["finding_id"], claim="report-inclusion",
            borrowing_ref=self.a, value="affirmed", submission_id="demo.mortgage.comparison.lifecycle.relink",
            evidence_id="demo.mortgage.comparison.lifecycle.relink.evidence", actor=self.actor,
            at="2026-10-23T12:12:03Z", statement_keys={"payer": "demo.f1098.lender.a",
            "statement": "demo.f1098.stmt.a", "tax-year": "2025"}, expected_revision=self.log.read().revision)
        self.assertNotEqual(correction["finding_id"], link_rows[0]["finding_id"])
        readings = current_mortgage_payment_comparison_applicability(self.log.read().acts, self.registry)
        self.assertEqual({row["finding_id"] for row in readings}, set(comparison_ids))
        self.assertTrue(all(row["applicability"] == "unresolved-applicability" for row in readings))
        old_to_new: dict[str, str] = {}
        review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.payment-comparison.reconfirm",
            shown_at="2026-10-23T12:12:04Z", borrowing_ref=self.a)
        for index, old_id in enumerate(comparison_ids):
            offer = next(row for row in review["answers"] if row["claim"] == "payment-comparison"
                         and row["findingId"] == old_id)
            current_own_keys = {key: offer["scope"][key] for key in ("payer", "statement", "tax-year")}
            corrected_comparison = correct_mortgage_borrowing_review_answer(
                self.log, self.registry, review, claim="payment-comparison", borrowing_ref=self.a,
                finding_id=old_id, value="different-payments",
                submission_id=f"demo.mortgage.comparison.lifecycle.reconfirm.{index}",
                evidence_id=f"demo.mortgage.comparison.lifecycle.reconfirm.{index}.evidence",
                actor=self.actor, at=f"2026-10-23T12:12:0{4 + index}Z", statement_keys=current_own_keys,
                peer_statement_keys=offer["peerScope"])
            old_to_new[old_id] = corrected_comparison["finding_id"]
            if index + 1 < len(comparison_ids):
                review = prepare_mortgage_borrowing_review(
                    self.log, self.registry, review_id=f"demo.mortgage.review.payment-comparison.reconfirm.{index + 1}",
                    shown_at=f"2026-10-23T12:12:0{5 + index}Z", borrowing_ref=self.a)
        self.assertEqual(set(old_to_new), set(comparison_ids))
        self.assertTrue(set(old_to_new.values()).isdisjoint(set(comparison_ids)))
        current_readings = current_mortgage_payment_comparison_applicability(self.log.read().acts, self.registry)
        self.assertEqual({row["finding_id"] for row in current_readings}, set(old_to_new.values()))
        self.assertTrue(all(row["applicability"] == "current" for row in current_readings))

    def test_clear_ends_current_payment_comparison_answers(self) -> None:
        self._record("continuing-borrowing", self.a, "yes", "comparison-clear-recognition")
        self._record("report-inclusion", self.a, "affirmed", "comparison-clear-link-a", "a")
        self._record("report-inclusion", self.a, "affirmed", "comparison-clear-link-b", "b")
        review = prepare_mortgage_borrowing_review(
            self.log, self.registry, review_id="demo.mortgage.review.comparison-clear",
            shown_at="2026-10-23T12:13:00Z", borrowing_ref=self.a)
        comparison_ids = []
        offers = [row for row in review["answers"] if row["claim"] == "payment-comparison"]
        for index, initial_offer in enumerate(offers):
            offer = initial_offer
            if index:
                review = prepare_mortgage_borrowing_review(
                    self.log, self.registry, review_id="demo.mortgage.review.comparison-clear.second",
                    shown_at="2026-10-23T12:13:02Z", borrowing_ref=self.a)
                offer = next(row for row in review["answers"] if row["claim"] == "payment-comparison"
                             and row["scope"]["statement"] == initial_offer["scope"]["statement"])
            own = {key: offer["scope"][key] for key in ("payer", "statement", "tax-year")}
            saved = record_mortgage_borrowing_review_answer(
                self.log, self.registry, review, claim="payment-comparison", borrowing_ref=self.a,
                value="different-payments", submission_id=f"demo.mortgage.comparison.clear.{index}",
                evidence_id=f"demo.mortgage.comparison.clear.{index}.evidence", actor=self.actor,
                at=f"2026-10-23T12:13:0{index + 1}Z", statement_keys=own,
                peer_statement_keys=offer["peerScope"])
            comparison_ids.append(saved["finding_id"])
        result = clear_mortgage_borrowing_year_durably(
            self.log, self.registry, borrowing_ref=self.a, actor=self.actor,
            at="2026-10-23T12:13:03Z", expected_revision=self.log.read().revision)
        current = compute_currency(result["state"]).current_finding_ids
        self.assertTrue(set(comparison_ids).isdisjoint(current))

    def test_retracted_source_can_end_exact_orphan_link_but_cannot_create_affirmation(self) -> None:
        keys = {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"}
        link = self._record("report-inclusion", self.a, "affirmed", "orphan-link", "a")
        state = project(self.log.read().acts, self.registry)
        source_id = fact_id_for("tax.us.2025.f1098.box1-mortgage-interest", tuple(keys.items()))
        source_finding = next(fid for fid, finding in state.findings.items() if finding.get("fact_id") == source_id)
        revision = self.log.read().revision
        transitions = [row for row in self.log.read().acts if row.get("kind") == "member-transition"]
        predecessor_horizon = transitions[-1]["payload"]["successor"]["id"]
        self.log.append({"schema": "act.v1", "act_id": "demo.mortgage.source.remove-a",
                         "kind": "member-transition", "actor": self.actor,
                         "at": "2026-10-23T12:05:30Z", "committed_against": revision,
                         "payload": {"family": {"id": "tax.us.2025.f1098", "version": "v1"},
                                     "scope": {"tax-year": "2025", "subject": "demo.primary"},
                                     "member": {"action": "remove", "fact_id": source_id},
                                     "successor": {"id": "demo.f1098.h3", "predecessor": predecessor_horizon}}},
                        expected_revision=revision)
        self.assertNotIn(source_finding, compute_currency(
            project(self.log.read().acts, self.registry)).current_finding_ids)
        before_withdrawal = self.log.read().revision
        withdrawn = correct_mortgage_borrowing_claim_durably(
            self.log, self.registry, finding_id=link["finding_id"], claim="report-inclusion",
            borrowing_ref=self.a, value="withdrawn", submission_id="demo.mortgage.orphan.withdraw",
            evidence_id="demo.mortgage.orphan.withdraw.evidence", actor=self.actor,
            at="2026-10-23T12:06:00Z", statement_keys=keys, expected_revision=before_withdrawal)
        current = compute_currency(withdrawn["state"]).current_finding_ids
        self.assertNotIn(link["finding_id"], current)
        self.assertIn(withdrawn["finding_id"], current)
        finding = withdrawn["state"].findings[withdrawn["finding_id"]]
        contribution = withdrawn["state"].contributions[finding["contribution_id"]]
        self.assertNotIn("box1_finding_id", contribution["content"])
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="report-inclusion", borrowing_ref=self.a, value="affirmed",
                submission_id="demo.mortgage.orphan.reaffirm", evidence_id="demo.mortgage.orphan.reaffirm.evidence",
                actor=self.actor, at="2026-10-23T12:07:00Z", statement_keys=keys,
                expected_revision=self.log.read().revision)

    def test_incomplete_tail_and_reused_submission_or_evidence_refuse_atomically(self) -> None:
        saved = self._record("owes-the-loan", self.a, "yes", "identity")
        revision = self.log.read().revision
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="no-one-else-owes-it", borrowing_ref=self.a, value="yes",
                submission_id="demo.mortgage.submission.identity", evidence_id="demo.mortgage.new-evidence",
                actor=self.actor, at="2026-10-23T12:08:00Z", expected_revision=revision)
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="no-one-else-owes-it", borrowing_ref=self.a, value="yes",
                submission_id="demo.mortgage.submission.fresh", evidence_id=saved["evidence_id"],
                actor=self.actor, at="2026-10-23T12:08:01Z", expected_revision=revision)
        self.assertEqual(self.log.read().revision, revision)
        self.log.path.write_bytes(self.log.path.read_bytes() + b"{")
        with self.assertRaises(MortgageBorrowingRecordingRefused):
            record_mortgage_borrowing_claim_durably(
                self.log, self.registry, claim="no-one-else-owes-it", borrowing_ref=self.a, value="yes",
                submission_id="demo.mortgage.submission.torn", evidence_id="demo.mortgage.evidence.torn",
                actor=self.actor, at="2026-10-23T12:08:02Z")


if __name__ == "__main__":
    unittest.main()
