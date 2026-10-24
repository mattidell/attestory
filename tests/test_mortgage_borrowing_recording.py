"""Mortgage borrowing recorder scope, lifecycle, and clear behavior."""
from __future__ import annotations

import json
import tempfile
import unittest
import pytest
from pathlib import Path
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.loader import load_mortgage_borrowing_bundle, tax_registry
from packages.tax.mortgage_borrowing_recording import (
    BORROWING_KIND, MortgageBorrowingRecordingRefused,
    clear_mortgage_borrowing_year_durably,
    correct_mortgage_borrowing_claim_durably,
    introduce_mortgage_borrowing_reference_durably,
    record_mortgage_borrowing_claim_durably,
    withdraw_mortgage_borrowing_claim_durably,
)
from tests.test_f1098_statement_review import _append_seed


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
