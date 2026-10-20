"""Tests for Track 1 Increment C: atomic Form 1099-K statement removal and fresh closure.

Tests:
1. Atomically removing a statement with a sibling standing:
   - Stages member-transition (action: "remove"), companion Box 4 retraction,
     and orphan answers retraction in a single ActLog.append_batch;
   - Sibling statement member fact, Box 4, and circumstance answers remain current;
   - Horizon advances, displacing predecessor closure.
2. Attesting fresh closure afterwards via close_f1099k_family_durably.
3. Removing the last remaining statement:
   - Family becomes empty of statements;
   - Fresh closure attested afterwards via record_f1099k_no_statements_durably.
4. Statement removal through the review save path (retract_f1099k_statement_review).
5. Fail-closed refusal boundaries (stale revision, non-existent statement, duplicate closure).
"""
from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    ALL_CIRCUMSTANCE_QUESTIONS,
    CLOSURE_TYPE,
    STATEMENT_BOX1A,
    STATEMENT_BOX4,
    F1099KRecordingRefused,
    close_f1099k_family_durably,
    record_f1099k_no_statements_durably,
    record_f1099k_statement_answers_durably,
    record_f1099k_statement_durably,
    retract_f1099k_statement_durably,
)
from packages.tax.f1099k_statement_review import (
    F1099KReviewRefused,
    prepare_f1099k_statement_review,
    retract_f1099k_statement_review,
)
from packages.tax.loader import tax_registry

USER = "demo.taxpayer"
PAYER_1 = "demo.platform.a"
STMT_1 = "demo.stmt.a"
PAYER_2 = "demo.platform.b"
STMT_2 = "demo.stmt.b"

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


class F1099KStatementRemovalIncrementCTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1099k-removal-inc-c-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)

    def test_atomic_statement_removal_with_sibling_standing(self) -> None:
        """Removing one statement atomically retracts its Box 1a, Box 4, and answers while sibling stands."""
        # Record Statement 1 ($880 Box 1a, $10 Box 4) + answers
        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_1,
            statement_ref=STMT_1,
            box1a=880.0,
            box4=10.0,
            submission_id="demo.sub.stmt1",
            evidence_id="demo.ev.stmt1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
        )
        ans_res1 = record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=res1["statement_keys"],
            answers=BASE_ANSWERS,
            submission_id="demo.sub.ans1",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.ev.ans1"),
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=res1["revision"],
        )

        # Record Statement 2 ($450 Box 1a, $5 Box 4) + answers
        res2 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_2,
            statement_ref=STMT_2,
            box1a=450.0,
            box4=5.0,
            submission_id="demo.sub.stmt2",
            evidence_id="demo.ev.stmt2",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=ans_res1["revision"],
        )
        ans_res2 = record_f1099k_statement_answers_durably(
            self.log,
            self.registry,
            statement_keys=res2["statement_keys"],
            answers=BASE_ANSWERS,
            submission_id="demo.sub.ans2",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.ev.ans2"),
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=res2["revision"],
        )

        # Confirm before removal: both statements and their answers are current
        state_before = project(self.log.read().acts, self.registry)
        current_ids_before = compute_currency(state_before).current_finding_ids
        lattice_before = facts_of(state_before.fact_state, include_displaced=True)

        stmt1_b1a_fids = [
            fid for fid in current_ids_before
            if lattice_before[state_before.findings[fid]["fact_id"]].fact_type_id == STATEMENT_BOX1A
            and dict(lattice_before[state_before.findings[fid]["fact_id"]].keys)["payer"] == PAYER_1
        ]
        stmt2_b1a_fids = [
            fid for fid in current_ids_before
            if lattice_before[state_before.findings[fid]["fact_id"]].fact_type_id == STATEMENT_BOX1A
            and dict(lattice_before[state_before.findings[fid]["fact_id"]].keys)["payer"] == PAYER_2
        ]
        self.assertEqual(len(stmt1_b1a_fids), 1)
        self.assertEqual(len(stmt2_b1a_fids), 1)

        # Now remove Statement 2 atomically
        rev_before = self.log.read().revision
        rem_res = retract_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_2,
            statement_ref=STMT_2,
            submission_id="demo.sub.rm.stmt2",
            actor=USER,
            at="2026-10-16T12:04:00Z",
            expected_revision=rev_before,
        )

        # The atomic append_batch added exactly 17 acts (1 MT + 1 Box 4 retract + 15 answer retracts)
        self.assertEqual(rem_res["revision"], rev_before + 17)
        self.assertEqual(self.log.read().revision, rev_before + 17)

        # Inspect the acts added in that atomic batch
        all_acts = self.log.read().acts
        new_acts = all_acts[rev_before:]
        self.assertEqual(len(new_acts), 17)
        kinds = [a["kind"] for a in new_acts]
        self.assertEqual(kinds.count("member-transition"), 1)
        self.assertEqual(kinds.count("finding-retracted"), 16)  # 1 Box 4 + 15 answers

        mt_act = next(a for a in new_acts if a["kind"] == "member-transition")
        self.assertEqual(mt_act["payload"]["member"]["action"], "remove")
        self.assertEqual(mt_act["payload"]["successor"]["id"], rem_res["horizon"])

        # Project state after removal
        state_after = project(all_acts, self.registry)
        current_ids_after = compute_currency(state_after).current_finding_ids
        lattice_after = facts_of(state_after.fact_state, include_displaced=True)

        # Statement 2 Box 1a is withdrawn
        stmt2_b1a_after = [
            fid for fid in current_ids_after
            if lattice_after[state_after.findings[fid]["fact_id"]].fact_type_id == STATEMENT_BOX1A
            and dict(lattice_after[state_after.findings[fid]["fact_id"]].keys)["payer"] == PAYER_2
        ]
        self.assertEqual(len(stmt2_b1a_after), 0)

        # Statement 2 Box 4 is withdrawn
        stmt2_b4_after = [
            fid for fid in current_ids_after
            if lattice_after[state_after.findings[fid]["fact_id"]].fact_type_id == STATEMENT_BOX4
            and dict(lattice_after[state_after.findings[fid]["fact_id"]].keys)["payer"] == PAYER_2
        ]
        self.assertEqual(len(stmt2_b4_after), 0)

        # Statement 2 answers are all withdrawn
        stmt2_ans_after = [
            fid for fid in current_ids_after
            if lattice_after[state_after.findings[fid]["fact_id"]].fact_type_id.startswith("tax.us.2025.f1099k.")
            and dict(lattice_after[state_after.findings[fid]["fact_id"]].keys).get("payer") == PAYER_2
        ]
        self.assertEqual(len(stmt2_ans_after), 0)

        # Statement 1 Box 1a, Box 4, and ALL 15 circumstance answers remain completely current!
        stmt1_b1a_after = [
            fid for fid in current_ids_after
            if lattice_after[state_after.findings[fid]["fact_id"]].fact_type_id == STATEMENT_BOX1A
            and dict(lattice_after[state_after.findings[fid]["fact_id"]].keys)["payer"] == PAYER_1
        ]
        stmt1_b4_after = [
            fid for fid in current_ids_after
            if lattice_after[state_after.findings[fid]["fact_id"]].fact_type_id == STATEMENT_BOX4
            and dict(lattice_after[state_after.findings[fid]["fact_id"]].keys)["payer"] == PAYER_1
        ]
        stmt1_ans_after = [
            fid for fid in current_ids_after
            if lattice_after[state_after.findings[fid]["fact_id"]].fact_type_id.startswith("tax.us.2025.f1099k.")
            and dict(lattice_after[state_after.findings[fid]["fact_id"]].keys).get("payer") == PAYER_1
            and lattice_after[state_after.findings[fid]["fact_id"]].fact_type_id not in (STATEMENT_BOX1A, STATEMENT_BOX4)
        ]
        self.assertEqual(len(stmt1_b1a_after), 1)
        self.assertEqual(len(stmt1_b4_after), 1)
        self.assertEqual(len(stmt1_ans_after), len(ALL_CIRCUMSTANCE_QUESTIONS))

    def test_close_f1099k_family_durably_after_removal(self) -> None:
        """After removing a statement, fresh closure can be recorded on the successor horizon."""
        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_1,
            statement_ref=STMT_1,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.sub.stmt1",
            evidence_id="demo.ev.stmt1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
            close_family=False,
        )
        res2 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_2,
            statement_ref=STMT_2,
            box1a=450.0,
            box4=0.0,
            submission_id="demo.sub.stmt2",
            evidence_id="demo.ev.stmt2",
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=res1["revision"],
        )

        rem_res = retract_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_2,
            statement_ref=STMT_2,
            submission_id="demo.sub.rm.stmt2",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=res2["revision"],
        )

        # Attest fresh closure on the post-removal horizon
        cl_res = close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="demo.sub.cl.after_rm",
            actor=USER,
            at="2026-10-16T12:03:00Z",
            expected_revision=rem_res["revision"],
        )
        self.assertEqual(cl_res["horizon"], rem_res["horizon"])

        # Check that closure finding is current
        state = project(self.log.read().acts, self.registry)
        current_ids = compute_currency(state).current_finding_ids
        closure_fid = cl_res["finding_ids"][0]
        self.assertIn(closure_fid, current_ids)
        self.assertEqual(
            state.findings[closure_fid]["fact_id"],
            f"{CLOSURE_TYPE}|family-horizon={rem_res['horizon']},tax-year=2025",
        )

    def test_removal_of_last_remaining_statement_and_no_statements_closure(self) -> None:
        """Removing the last remaining statement leaves an empty family that closes via record_f1099k_no_statements_durably."""
        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_1,
            statement_ref=STMT_1,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.sub.stmt1",
            evidence_id="demo.ev.stmt1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
            close_family=False,
        )

        # Retract Statement 1 (the only statement)
        rem_res = retract_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_1,
            statement_ref=STMT_1,
            submission_id="demo.sub.rm.last",
            actor=USER,
            at="2026-10-16T12:01:00Z",
            expected_revision=res1["revision"],
        )

        state = project(self.log.read().acts, self.registry)
        current_ids = compute_currency(state).current_finding_ids
        lattice = facts_of(state.fact_state, include_displaced=True)

        current_stmts = [
            fid for fid in current_ids
            if lattice[state.findings[fid]["fact_id"]].fact_type_id == STATEMENT_BOX1A
        ]
        self.assertEqual(len(current_stmts), 0)

        # Fresh closure afterwards on empty family
        no_stmt_res = record_f1099k_no_statements_durably(
            self.log,
            self.registry,
            submission_id="demo.sub.no_stmt.fresh",
            evidence_id="demo.ev.no_stmt.fresh",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=rem_res["revision"],
        )
        self.assertEqual(no_stmt_res["horizon"], rem_res["horizon"])

        state_final = project(self.log.read().acts, self.registry)
        current_final_ids = compute_currency(state_final).current_finding_ids
        closure_fid = no_stmt_res["finding_ids"][0]
        self.assertIn(closure_fid, current_final_ids)

    def test_save_path_removal_via_review(self) -> None:
        """Statement removal through the review save path (retract_f1099k_statement_review)."""
        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_1,
            statement_ref=STMT_1,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.sub.stmt1",
            evidence_id="demo.ev.stmt1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
            close_family=False,
        )

        review = prepare_f1099k_statement_review(
            self.log,
            self.registry,
            review_id="demo.rev.stmt1",
            shown_at="2026-10-16T12:01:00Z",
            statement_keys=res1["statement_keys"],
        )
        self.assertEqual(review["statement"]["box1a"], 880.0)

        # Remove statement through review save path
        rev_res = retract_f1099k_statement_review(
            self.log,
            self.registry,
            review,
            submission_id="demo.sub.rev_rm.1",
            actor=USER,
            at="2026-10-16T12:02:00Z",
        )
        self.assertGreater(rev_res["revision"], review["revision"])

        # Reviewing again now refuses because statement was removed
        with self.assertRaises(F1099KReviewRefused):
            prepare_f1099k_statement_review(
                self.log,
                self.registry,
                review_id="demo.rev.stmt1.after",
                shown_at="2026-10-16T12:03:00Z",
                statement_keys=res1["statement_keys"],
            )

    def test_removal_and_closure_refusals(self) -> None:
        """Fail-closed refusal boundaries for statement removal and family closure."""
        res1 = record_f1099k_statement_durably(
            self.log,
            self.registry,
            payer_id=PAYER_1,
            statement_ref=STMT_1,
            box1a=880.0,
            box4=0.0,
            submission_id="demo.sub.stmt1",
            evidence_id="demo.ev.stmt1",
            actor=USER,
            at="2026-10-16T12:00:00Z",
            expected_revision=0,
            close_family=False,
        )

        # 1. Non-existent statement
        with self.assertRaises(F1099KRecordingRefused):
            retract_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id="demo.unknown.platform",
                statement_ref="demo.unknown.stmt",
                submission_id="demo.sub.bad1",
                actor=USER,
                at="2026-10-16T12:01:00Z",
                expected_revision=res1["revision"],
            )

        # 2. Stale expected revision
        with self.assertRaises(F1099KRecordingRefused):
            retract_f1099k_statement_durably(
                self.log,
                self.registry,
                payer_id=PAYER_1,
                statement_ref=STMT_1,
                submission_id="demo.sub.bad2",
                actor=USER,
                at="2026-10-16T12:01:00Z",
                expected_revision=0,  # stale
            )

        # 3. Duplicate closure refusal
        cl_res = close_f1099k_family_durably(
            self.log,
            self.registry,
            submission_id="demo.sub.cl.1",
            actor=USER,
            at="2026-10-16T12:02:00Z",
            expected_revision=res1["revision"],
        )
        with self.assertRaises(F1099KRecordingRefused):
            close_f1099k_family_durably(
                self.log,
                self.registry,
                submission_id="demo.sub.cl.dup",
                actor=USER,
                at="2026-10-16T12:03:00Z",
                expected_revision=cl_res["revision"],
            )

        # 4. close_f1099k_family_durably refused when no statements exist
        empty_log = ActLog(Path(self.temp.name) / "empty_workspace", self.registry)
        with self.assertRaises(F1099KRecordingRefused):
            close_f1099k_family_durably(
                empty_log,
                self.registry,
                submission_id="demo.sub.cl.empty",
                actor=USER,
                at="2026-10-16T12:00:00Z",
                expected_revision=0,
            )


if __name__ == "__main__":
    unittest.main()
