"""Track 6: correction scope for a statement that already has an inclusion.

Each case uses the real recorder, a durable append, and a fresh ActLog read.
Applicability is the opt-in ``current_claim_applicability`` result. Case 6 is
the existing old-path file ``tests/test_f1098e_student_loan_interest_agi_track6.py``
and is not reimplemented here.
"""
from __future__ import annotations

import tempfile
import unittest
from typing import Any

from packages.kernel.act_log import ActLog
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.sli_relationship_recording import (
    STATEMENT_INCLUSION,
    RelationshipRecordingRefused,
    current_claim_applicability,
    record_submission_durably,
)
from packages.tax.sli_relationship_review import (
    _append_statement_source_correction_durably,
    apply_statement_correction_review,
    prepare_review,
)
import tests.test_sli_relationship_recording as track14
from tests.support import act, demo_entity

USER = "demo.user.filer"


def _affirmed_inclusion() -> tuple[tempfile.TemporaryDirectory[str], ActLog, Any, dict[str, str]]:
    """One current statement with one affirmed inclusion, through the real recorder."""
    raw, log, registry, refs = track14.OrdinaryRelationshipRecording()._workspace()
    saved = record_submission_durably(log, {
        "submission_id": "demo.track6.submission.inclusion",
        "evidence_id": "demo.evidence.track6.inclusion",
        "actor": USER,
        "at": "2026-10-02T12:00:00Z",
        "borrowing_ref": refs["borrowing"],
        "schooling_fact_id": refs["school"],
        "statement_fact_id": refs["statement"],
        "financing_response": "unanswered",
        "inclusion_response": "yes",
    }, registry)
    claim = saved["claims"]["statement-inclusion"]
    return raw, log, registry, {**refs, "inclusion_finding_id": claim["finding_id"],
                                "inclusion_fact_id": claim["fact_id"]}


def _recovered_acts(log: ActLog, registry: Any) -> tuple[dict[str, Any], ...]:
    """Reload the durable log from a fresh ActLog, then read its acts."""
    fresh = ActLog(log.path.parent, registry)
    return fresh.read().acts


def _applicability(acts: tuple[dict[str, Any], ...], registry: Any) -> dict[str, dict[str, str]]:
    return {row["finding_id"]: row for row in current_claim_applicability(acts, registry)}


class CorrectionEntryEnforcement(unittest.TestCase):
    def test_case_3_direct_same_identity_append_does_not_keep_inclusion_applicable(self) -> None:
        """Ordinary box-1 admission without scope evidence must not leave the old inclusion applicable."""
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            before = project(log.read().acts, registry)
            inclusion = before.findings[refs["inclusion_finding_id"]]
            self.assertEqual(
                facts_of(before.fact_state)[inclusion["fact_id"]].fact_type_id,
                STATEMENT_INCLUSION,
            )
            original = [
                (finding_id, finding) for finding_id, finding in before.findings.items()
                if finding_id in compute_currency(before).current_finding_ids
                and finding.get("fact_id") == refs["statement"]
            ]
            self.assertEqual(len(original), 1)
            keys = tuple(facts_of(before.fact_state)[refs["statement"]].keys)
            track14._append_source(
                log, registry, track14.STATEMENT_TYPE, keys, 1800.0, "track6-direct-box1",
            )
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            current_ids = compute_currency(state).current_finding_ids
            self.assertIn(refs["inclusion_finding_id"], state.findings)
            corrected = [
                finding for finding_id, finding in state.findings.items()
                if finding_id in current_ids and finding.get("fact_id") == refs["statement"]
            ]
            self.assertEqual(len(corrected), 1)
            self.assertEqual(corrected[0]["value"], 1800.0)
            self.assertNotEqual(corrected[0]["id"], original[0][0])
            rows = _applicability(acts, registry)
            self.assertEqual(
                rows[refs["inclusion_finding_id"]]["applicability"],
                "unresolved-applicability",
            )

    def test_case_1_reviewed_amount_only_keeps_inclusion_and_both_amounts(self) -> None:
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            before_acts = _recovered_acts(log, registry)
            before_state = project(before_acts, registry)
            original_value = next(
                finding["value"] for finding_id, finding in before_state.findings.items()
                if finding_id in compute_currency(before_state).current_finding_ids
                and finding.get("fact_id") == refs["statement"]
            )
            _reviewed_correction(
                log, registry, refs, scope="amount-only", amount=1775.0,
                correction_id="demo.track6.amount-only", borrowing_ref=None, finding_id=None,
                suffix="amount-only",
            )
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            values = [finding["value"] for finding in state.findings.values()
                      if finding.get("fact_id") == refs["statement"]]
            current = [
                finding["value"] for finding_id, finding in state.findings.items()
                if finding_id in compute_currency(state).current_finding_ids
                and finding.get("fact_id") == refs["statement"]
            ]
            self.assertEqual(current, [1775.0])
            self.assertIn(original_value, values)
            self.assertIn(1775.0, values)
            self.assertIn(refs["inclusion_finding_id"], state.findings)
            rows = _applicability(acts, registry)
            self.assertEqual(rows[refs["inclusion_finding_id"]]["applicability"], "current")
            self.assertEqual(rows[refs["inclusion_finding_id"]]["source_fact_id"], refs["statement"])

    def test_case_2_reviewed_removal_drops_applicability_and_keeps_affirmation(self) -> None:
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            _reviewed_correction(
                log, registry, refs, scope="inclusion-removed", amount=1660.0,
                correction_id="demo.track6.removal", borrowing_ref=refs["borrowing"],
                finding_id=refs["inclusion_finding_id"], suffix="removal",
            )
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            self.assertIn(refs["inclusion_finding_id"], state.findings)
            self.assertNotIn(refs["inclusion_finding_id"], compute_currency(state).current_finding_ids)
            self.assertEqual(
                state.evidence["demo.evidence.track6.inclusion"].evidence["content"]["responses"]
                ["inclusion_response"],
                "yes",
            )
            self.assertNotIn(refs["inclusion_finding_id"], _applicability(acts, registry))

    def test_case_4_direct_append_without_claims_is_admitted(self) -> None:
        raw, log, registry, refs = track14.OrdinaryRelationshipRecording()._workspace()
        with raw:
            before = log.read().revision
            keys = tuple(facts_of(project(log.read().acts, registry).fact_state)[refs["statement"]].keys)
            fact_id = track14._append_source(
                log, registry, track14.STATEMENT_TYPE, keys, 1410.0, "track6-no-claim-box1",
            )
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            current = [
                finding for finding_id, finding in state.findings.items()
                if finding_id in compute_currency(state).current_finding_ids
                and finding.get("fact_id") == refs["statement"]
            ]
            self.assertEqual(fact_id, refs["statement"])
            self.assertGreater(log.read().revision, before)
            self.assertEqual(len(current), 1)
            self.assertEqual(current[0]["value"], 1410.0)
            self.assertEqual(_applicability(acts, registry), {})

    def test_case_5_unrelated_statement_inclusion_stays_applicable(self) -> None:
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            other_fact = _append_other_statement(log, registry)
            other = record_submission_durably(log, {
                "submission_id": "demo.track6.submission.other-inclusion",
                "evidence_id": "demo.evidence.track6.other-inclusion",
                "actor": USER,
                "at": "2026-10-02T12:02:00Z",
                "borrowing_ref": refs["borrowing"],
                "schooling_fact_id": refs["school"],
                "statement_fact_id": other_fact,
                "financing_response": "unanswered",
                "inclusion_response": "yes",
            }, registry)
            other_id = other["claims"]["statement-inclusion"]["finding_id"]
            keys = tuple(facts_of(project(log.read().acts, registry).fact_state)[refs["statement"]].keys)
            track14._append_source(
                log, registry, track14.STATEMENT_TYPE, keys, 1800.0, "track6-direct-box1-beside-other",
            )
            acts = _recovered_acts(log, registry)
            rows = _applicability(acts, registry)
            self.assertEqual(rows[refs["inclusion_finding_id"]]["applicability"], "unresolved-applicability")
            self.assertEqual(rows[other_id]["applicability"], "current")
            self.assertEqual(rows[other_id]["source_fact_id"], other_fact)

    def test_case_7_reviewed_correction_restores_applicability_after_direct_append(self) -> None:
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            keys = tuple(facts_of(project(log.read().acts, registry).fact_state)[refs["statement"]].keys)
            track14._append_source(
                log, registry, track14.STATEMENT_TYPE, keys, 1800.0, "track6-direct-before-review",
            )
            after_direct = _recovered_acts(log, registry)
            direct_rows = _applicability(after_direct, registry)
            self.assertEqual(
                direct_rows[refs["inclusion_finding_id"]]["applicability"],
                "unresolved-applicability",
            )
            _reviewed_correction(
                log, registry, refs, scope="amount-only", amount=1900.0,
                correction_id="demo.track6.restore", borrowing_ref=None, finding_id=None,
                suffix="restore",
            )
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            values = {finding["value"] for finding in state.findings.values()
                      if finding.get("fact_id") == refs["statement"]}
            self.assertTrue({1250.0, 1800.0, 1900.0}.issubset(values))
            rows = _applicability(acts, registry)
            self.assertEqual(rows[refs["inclusion_finding_id"]]["applicability"], "current")
            self.assertIn(refs["inclusion_finding_id"], compute_currency(state).current_finding_ids)

    def test_unreviewed_2900_citing_reviewed_1775_scope_evidence_is_not_current(self) -> None:
        """Reviewed $1,775, then an unreviewed $2,900 that cites that same scope evidence.

        The recorder refuses the second write, so the log keeps $1,775 and the
        inclusion stays current against it. A log that already holds the $2,900
        citation does not report the inclusion current.
        """
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            scope_evidence_id = "demo.evidence.track6.reviewed-1775"
            _reviewed_correction(
                log, registry, refs, scope="amount-only", amount=1775.0,
                correction_id="demo.track1a3.reviewed-1775", borrowing_ref=None, finding_id=None,
                suffix="reviewed-1775",
            )
            reviewed_acts = _recovered_acts(log, registry)
            self.assertEqual(_current_box1_values(reviewed_acts, registry, refs["statement"]), [1775.0])
            self.assertEqual(
                _applicability(reviewed_acts, registry)[refs["inclusion_finding_id"]]["applicability"],
                "current",
            )
            revision = log.read().revision
            with self.assertRaises(RelationshipRecordingRefused):
                _append_statement_source_correction_durably(
                    log, registry, statement_fact_id=refs["statement"], corrected_total=2900.0,
                    correction_id="demo.track1a3.unreviewed-2900",
                    scope_evidence_id=scope_evidence_id, actor=USER, at="2026-10-02T12:06:00Z",
                )
            self.assertEqual(log.read().revision, revision)
            refused_acts = _recovered_acts(log, registry)
            self.assertEqual(_current_box1_values(refused_acts, registry, refs["statement"]), [1775.0])
            self.assertEqual(
                _applicability(refused_acts, registry)[refs["inclusion_finding_id"]]["applicability"],
                "current",
            )
            self.assertNotIn("demo.finding.track1a3.smuggle-2900", project(refused_acts, registry).findings)
            _smuggle_box1_citing_scope(
                log, registry, statement_fact_id=refs["statement"], value=2900.0,
                label="smuggle-2900", scope_evidence_id=scope_evidence_id,
                source_correction_id="demo.track1a3.smuggle-2900",
            )
            smuggled = _recovered_acts(log, registry)
            smuggled_state = project(smuggled, registry)
            current = _current_box1(smuggled_state, refs["statement"])
            self.assertEqual([finding["value"] for _finding_id, finding in current], [2900.0])
            self.assertIn(scope_evidence_id, current[0][1]["evidence_ids"])
            self.assertEqual(
                _applicability(smuggled, registry)[refs["inclusion_finding_id"]]["applicability"],
                "unresolved-applicability",
            )

    def test_same_amount_reuse_of_scope_evidence_is_refused(self) -> None:
        """A second update that repeats $1,775 and cites the same evidence is refused."""
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            scope_evidence_id = "demo.evidence.track6.same-amount"
            _reviewed_correction(
                log, registry, refs, scope="amount-only", amount=1775.0,
                correction_id="demo.track1a3.same-amount-review", borrowing_ref=None,
                finding_id=None, suffix="same-amount",
            )
            revision = log.read().revision
            with self.assertRaises(RelationshipRecordingRefused):
                _append_statement_source_correction_durably(
                    log, registry, statement_fact_id=refs["statement"], corrected_total=1775.0,
                    correction_id="demo.track1a3.same-amount-again",
                    scope_evidence_id=scope_evidence_id, actor=USER, at="2026-10-02T12:06:00Z",
                )
            self.assertEqual(log.read().revision, revision)
            acts = _recovered_acts(log, registry)
            self.assertEqual(_current_box1_values(acts, registry, refs["statement"]), [1775.0])
            self.assertEqual(
                _applicability(acts, registry)[refs["inclusion_finding_id"]]["applicability"],
                "current",
            )

    def test_reviewed_correction_against_a_changed_box1_is_refused(self) -> None:
        """A review prepared against one box 1 finding is refused after that finding changes."""
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            review = prepare_review(
                log, registry, review_id="demo.track1a3.review.stale",
                shown_at="2026-10-02T12:05:00Z", borrowing_refs=(refs["borrowing"],),
                schooling_fact_ids=(refs["school"],), statement_fact_ids=(refs["statement"],),
            )
            keys = tuple(facts_of(project(log.read().acts, registry).fact_state)[refs["statement"]].keys)
            track14._append_source(
                log, registry, track14.STATEMENT_TYPE, keys, 1640.0, "track1a3-stale-box1",
            )
            revision = log.read().revision
            with self.assertRaises(RelationshipRecordingRefused):
                apply_statement_correction_review(
                    log, registry, review=review, statement_fact_id=refs["statement"],
                    scope="amount-only", borrowing_ref=None, finding_id=None,
                    corrected_box1_total=1775.0, source_correction_id="demo.track1a3.stale",
                    actor=USER, at="2026-10-02T12:05:01Z",
                    submission_id="demo.track1a3.submission.stale",
                    evidence_id="demo.evidence.track1a3.stale",
                )
            self.assertEqual(log.read().revision, revision)
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            self.assertEqual(_current_box1_values(acts, registry, refs["statement"]), [1640.0])
            self.assertNotIn(1775.0, [finding["value"] for finding in state.findings.values()
                                      if finding.get("fact_id") == refs["statement"]])
            self.assertEqual(
                _applicability(acts, registry)[refs["inclusion_finding_id"]]["applicability"],
                "unresolved-applicability",
            )

    def test_scope_evidence_for_a_different_predecessor_does_not_refresh(self) -> None:
        """One citation is not enough when the finding is not the reviewed successor."""
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            before = project(log.read().acts, registry)
            original_id = next(
                finding_id for finding_id, finding in before.findings.items()
                if finding_id in compute_currency(before).current_finding_ids
                and finding.get("fact_id") == refs["statement"]
            )
            scope_evidence_id = "demo.evidence.track1a3.wrong-predecessor-scope"
            _submit_scope_evidence(
                log, evidence_id=scope_evidence_id, statement_fact_id=refs["statement"],
                reviewed_statement_finding_id="demo.finding.not-the-reviewed-box1",
                corrected_total=1888.0, correction_id="demo.track1a3.wrong-predecessor",
            )
            _smuggle_box1_citing_scope(
                log, registry, statement_fact_id=refs["statement"], value=1888.0,
                label="wrong-predecessor", scope_evidence_id=scope_evidence_id,
                source_correction_id="demo.track1a3.wrong-predecessor",
            )
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            current = _current_box1(state, refs["statement"])
            self.assertEqual(len(current), 1)
            self.assertNotEqual(current[0][0], original_id)
            self.assertEqual(current[0][1]["value"], 1888.0)
            self.assertIn(scope_evidence_id, current[0][1]["evidence_ids"])
            self.assertEqual(
                _applicability(acts, registry)[refs["inclusion_finding_id"]]["applicability"],
                "unresolved-applicability",
            )

    def test_wrong_kind_scope_evidence_does_not_refresh(self) -> None:
        """A perfect binding on the wrong evidence kind does not refresh the inclusion."""
        raw, log, registry, refs = _affirmed_inclusion()
        with raw:
            before = project(log.read().acts, registry)
            original_id = next(
                finding_id for finding_id, finding in before.findings.items()
                if finding_id in compute_currency(before).current_finding_ids
                and finding.get("fact_id") == refs["statement"]
            )
            scope_evidence_id = "demo.evidence.track1a3.wrong-kind-scope"
            _submit_scope_evidence(
                log, evidence_id=scope_evidence_id, statement_fact_id=refs["statement"],
                reviewed_statement_finding_id=original_id, corrected_total=1888.0,
                correction_id="demo.track1a3.wrong-kind",
                kind="tax.other-answer",
            )
            revision = log.read().revision
            with self.assertRaises(RelationshipRecordingRefused):
                _append_statement_source_correction_durably(
                    log, registry, statement_fact_id=refs["statement"], corrected_total=1888.0,
                    correction_id="demo.track1a3.wrong-kind",
                    scope_evidence_id=scope_evidence_id, actor=USER, at="2026-10-02T12:06:00Z",
                )
            self.assertEqual(log.read().revision, revision)
            _smuggle_box1_citing_scope(
                log, registry, statement_fact_id=refs["statement"], value=1888.0,
                label="wrong-kind", scope_evidence_id=scope_evidence_id,
                source_correction_id="demo.track1a3.wrong-kind",
            )
            acts = _recovered_acts(log, registry)
            state = project(acts, registry)
            current = _current_box1(state, refs["statement"])
            self.assertEqual(current[0][1]["value"], 1888.0)
            self.assertIn(scope_evidence_id, current[0][1]["evidence_ids"])
            self.assertEqual(
                _applicability(acts, registry)[refs["inclusion_finding_id"]]["applicability"],
                "unresolved-applicability",
            )


def _reviewed_correction(log: ActLog, registry: Any, refs: dict[str, str], *, scope: str,
                         amount: float, correction_id: str, borrowing_ref: str | None,
                         finding_id: str | None, suffix: str) -> dict[str, Any]:
    review = prepare_review(
        log, registry, review_id=f"demo.track6.review.{suffix}",
        shown_at="2026-10-02T12:05:00Z", borrowing_refs=(refs["borrowing"],),
        schooling_fact_ids=(refs["school"],), statement_fact_ids=(refs["statement"],),
    )
    return apply_statement_correction_review(
        log, registry, review=review, statement_fact_id=refs["statement"], scope=scope,
        borrowing_ref=borrowing_ref, finding_id=finding_id, corrected_box1_total=amount,
        source_correction_id=correction_id, actor=USER, at="2026-10-02T12:05:01Z",
        submission_id=f"demo.track6.submission.{suffix}",
        evidence_id=f"demo.evidence.track6.{suffix}",
    )


def _current_box1(state: Any, statement_fact_id: str) -> list[tuple[str, dict[str, Any]]]:
    current_ids = compute_currency(state).current_finding_ids
    return [
        (finding_id, finding) for finding_id, finding in state.findings.items()
        if finding_id in current_ids and finding.get("fact_id") == statement_fact_id
    ]


def _current_box1_values(acts: tuple[dict[str, Any], ...], registry: Any,
                         statement_fact_id: str) -> list[Any]:
    return [finding["value"] for _finding_id, finding in _current_box1(project(acts, registry), statement_fact_id)]


def _append_act(log: ActLog, item: dict[str, Any]) -> None:
    log.append(item, expected_revision=log.read().revision)


def _submit_scope_evidence(log: ActLog, *, evidence_id: str, statement_fact_id: str,
                           reviewed_statement_finding_id: str, corrected_total: float,
                           correction_id: str,
                           kind: str = "tax.student-loan.relationship-answer") -> None:
    """Record scope evidence directly. This is not the reviewed route."""
    revision = log.read().revision
    evidence = {
        "schema": "evidence.v1", "id": evidence_id,
        "kind": kind,
        "label": "Unreviewed reuse of correction scope",
        "content": {"recognition_context": {"statement_correction": {
            "statement_fact_id": statement_fact_id,
            "scope": "amount-only",
            "source_correction_id": correction_id,
            "corrected_box1_total": corrected_total,
            "reviewed_statement_finding_id": reviewed_statement_finding_id,
            "refreshes_inclusion_applicability": True,
        }}},
    }
    _append_act(log, {
        "schema": "act.v1", "act_id": f"track1a3.scope-evidence.{evidence_id}",
        "kind": "evidence-submitted", "actor": USER, "at": "2026-10-02T12:07:00Z",
        "committed_against": revision, "payload": {"evidence": evidence},
    })


def _smuggle_box1_citing_scope(log: ActLog, registry: Any, *, statement_fact_id: str, value: float,
                               label: str, scope_evidence_id: str, source_correction_id: str) -> None:
    """Admit a box 1 finding through the kernel, then persist it.

    The tax recorder's binding check does not run. ``ActLog.append`` does not
    run it either. ``project`` on the recovered log does run kernel admission,
    which has no Part 5 rule yet.
    """
    contents = log.read()
    source_evidence_id = f"demo.evidence.track1a3.{label}"
    contribution_id = f"demo.contribution.track1a3.{label}"
    finding_id = f"demo.finding.track1a3.{label}"
    revision = contents.revision
    evidence = {
        "schema": "evidence.v1", "id": source_evidence_id,
        "kind": "tax.form-1098e-corrected-statement-source",
        "label": "Smuggled Form 1098-E box-1 source",
        "content": {"source_correction_id": source_correction_id},
    }
    evidence_act = {
        "schema": "act.v1", "act_id": f"track1a3.smuggle.evidence.{label}",
        "kind": "evidence-submitted", "actor": USER, "at": "2026-10-02T12:08:00Z",
        "committed_against": revision, "payload": {"evidence": evidence},
    }
    contribution_act = {
        "schema": "act.v1", "act_id": f"track1a3.smuggle.contribution.{label}",
        "kind": "contribution", "actor": USER, "at": "2026-10-02T12:08:01Z",
        "committed_against": revision + 1,
        "payload": {"contribution": {
            "schema": "contribution.v1", "id": contribution_id, "evidence_id": source_evidence_id,
            "content": {"mode": "manual-entry", "source": "corrected-form-1098e"},
        }},
    }
    assertion = {
        "schema": "act.v1", "act_id": f"track1a3.smuggle.assertion.{label}",
        "kind": "assertion", "actor": USER, "at": "2026-10-02T12:08:02Z",
        "committed_against": revision + 2,
        "payload": {"finding": {
            "schema": "finding.v2", "id": finding_id, "fact_id": statement_fact_id,
            "value": value, "basis": "attested",
            "evidence_ids": [source_evidence_id, scope_evidence_id],
            "contribution_id": contribution_id,
        }},
    }
    staged = list(contents.acts) + [evidence_act]
    base = project(tuple(staged), registry)
    admitted = apply_contribution_batch(
        base, contribution_act=contribution_act, successor_acts=[assertion], registry=registry,
        record_id=f"track1a3.smuggle.record.{label}",
    )
    if admitted.terminal_record["phase"] != "completed":
        raise AssertionError(admitted.terminal_record)
    for item in (evidence_act, contribution_act, assertion):
        _append_act(log, item)


def _append_other_statement(log: ActLog, registry: Any) -> str:
    lender = "demo.track6.lender.other"
    statement = "demo.track6.statement.other"
    for identity, label, kind in (
        (lender, "Other Servicing", "tax.us.student-loan-lender"),
        (statement, "Other 2025 Form 1098-E", "tax.us.1098e-statement"),
    ):
        revision = log.read().revision
        log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                   expected_revision=revision)
    return track14._append_source(
        log, registry, track14.STATEMENT_TYPE,
        (("lender", lender), ("statement", statement), ("tax-year", "2025")),
        900.0, "track6-other-statement",
    )


if __name__ == "__main__":
    unittest.main()
