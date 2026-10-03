"""Track 14 ordinary relationship input through content and ActLog recovery."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import install_domain_scoped_supersession
from packages.tax.sli_relationship_recording import (
    FINANCING, SCHOOLING, STATEMENT_INCLUSION, RelationshipRecordingRefused,
    current_claim_applicability,
    introduce_borrowing_reference_durably, record_submission_durably,
)
from tests.support import act, demo_entity, demo_evidence


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
STATEMENT_TYPE = "tax.us.2025.f1098e.box1-student-loan-interest"


def _append_source(log: ActLog, registry: Any, fact_type: str, keys: tuple[tuple[str, str], ...],
                   value: Any, label: str) -> str:
    before = log.read()
    evidence_id = f"demo.evidence.track14.{label}"
    contribution_id = f"demo.contribution.track14.{label}"
    finding = {"schema": "finding.v2", "id": f"demo.finding.track14.{label}",
               "fact_id": fact_id_for(fact_type, keys), "value": value, "basis": "attested",
               "evidence_ids": [evidence_id], "contribution_id": contribution_id}
    staged = list(before.acts)
    staged.append(act(len(staged), "evidence-submitted", {"evidence": demo_evidence(
        evidence_id, "Synthetic Track 14 answer", {"label": label})}))
    contribution = act(len(staged), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "synthetic": True},
    }})
    assertion = act(len(staged) + 1, "assertion", {"finding": finding})
    base = project(tuple(staged), registry)
    admitted = apply_contribution_batch(base, contribution_act=contribution,
                                        successor_acts=[assertion], registry=registry,
                                        record_id=f"demo.contribution-record.track14.{label}")
    if admitted.terminal_record["phase"] != "completed":
        raise AssertionError(admitted.terminal_record)
    for item in (staged[-1], contribution, assertion):
        log.append(item, expected_revision=log.read().revision)
    return cast(str, finding["fact_id"])


class OrdinaryRelationshipRecording(unittest.TestCase):
    def _workspace(self) -> tuple[tempfile.TemporaryDirectory[str], ActLog, Any, dict[str, str]]:
        raw = tempfile.TemporaryDirectory(prefix="sli-track14-")
        schemas = DerivationSchemas()
        install_domain_scoped_supersession(schemas.registry)
        log = ActLog(Path(raw.name) / "workspace", schemas.registry)
        fact_bundle = json.loads((CONTENT / "sli-relationship-source.bundle.json").read_text("utf-8"))
        form_bundle = json.loads((CONTENT / "f1098e.bundle.json").read_text("utf-8"))
        log.append(act(0, "bundle-adoption", {"bundle": form_bundle}), expected_revision=0)
        log.append(act(1, "bundle-adoption", {"bundle": fact_bundle}), expected_revision=1)
        borrowing_ref = "demo.track14.borrowing.autumn"
        introduce_borrowing_reference_durably(
            log, schemas.registry, reference_id=borrowing_ref, description="Autumn borrowing",
            actor="demo.user.filer", at="2026-09-29T11:59:00Z",
        )
        entities = [
            ("demo.track14.period.autumn24", "Autumn 2024", "tax.us.educational-period"),
            ("demo.track14.institution.river", "Riverside College", "tax.us.educational-institution"),
            ("demo.track14.programme.bsc", "BSc", "tax.us.educational-programme"),
            ("demo.track14.lender.cedar", "Cedar Servicing", "tax.us.student-loan-lender"),
            ("demo.track14.statement.2025", "2025 Form 1098-E", "tax.us.1098e-statement"),
        ]
        for identity, label, kind in entities:
            revision = log.read().revision
            log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                       expected_revision=revision)
        school_keys = (("period", entities[0][0]), ("institution", entities[1][0]),
                       ("programme", entities[2][0]))
        school_id = _append_source(log, schemas.registry, SCHOOLING, school_keys,
                                   "Riverside College, BSc, autumn 2024", "school")
        statement_keys = (("lender", entities[3][0]), ("statement", entities[4][0]),
                          ("tax-year", "2025"))
        statement_id = _append_source(log, schemas.registry, STATEMENT_TYPE, statement_keys,
                                      1250.0, "statement-box1")
        return raw, log, schemas.registry, {"borrowing": borrowing_ref,
                                           "school": school_id, "statement": statement_id}

    def test_one_answer_admits_two_distinct_claims_and_unknown_portion(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            result = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.both",
                "evidence_id": "demo.evidence.track14.submission.both",
                "actor": "demo.user.filer", "at": "2026-09-29T12:00:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes", "interest_portion_response": "unknown",
                "recognition_context": {"borrowing_label": "Autumn borrowing"},
            }, registry)
            reopened_log = ActLog(log.path.parent, registry)
            del log
            recovered_acts = reopened_log.read().acts
            self.assertEqual(set(result["claims"]), {"financing", "statement-inclusion"})
            self.assertNotEqual(result["claims"]["financing"]["finding_id"],
                                result["claims"]["statement-inclusion"]["finding_id"])
            recovered = project(recovered_acts, registry)
            self.assertIn(result["claims"]["financing"]["finding_id"], recovered.findings)
            self.assertIn(result["claims"]["statement-inclusion"]["finding_id"], recovered.findings)
            evidence = recovered.evidence["demo.evidence.track14.submission.both"].evidence
            self.assertEqual(evidence["content"]["responses"],
                             {"financing_response": "yes", "inclusion_response": "yes"})
            self.assertEqual(evidence["content"]["interest_portion_response"], "unknown")
            self.assertEqual(recovered.findings[result["claims"]["statement-inclusion"]["finding_id"]]
                             ["value"], "sli.statement-inclusion.affirmed")

    def test_fresh_actlog_reopen_recovers_claims_and_projection(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            result = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.reopen",
                "evidence_id": "demo.evidence.track14.submission.reopen",
                "actor": "demo.user.filer", "at": "2026-09-29T12:00:30Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes", "interest_portion_response": "unknown",
            }, registry)
            log_path = log.path.parent
            del log

            reopened = ActLog(log_path, registry)
            durable_acts = reopened.read().acts
            recovered_state = project(durable_acts, registry)
            current_ids = compute_currency(recovered_state).current_finding_ids
            self.assertEqual(set(result["claims"]), {"financing", "statement-inclusion"})
            self.assertTrue({claim["finding_id"] for claim in result["claims"].values()}
                            <= current_ids)
            self.assertEqual(len(recovered_state.evidence), 3)
            answers = recovered_state.evidence["demo.evidence.track14.submission.reopen"].evidence
            self.assertEqual(answers["content"]["interest_portion_response"], "unknown")

    def test_unresolved_equal_looking_candidates_reopen_without_selection(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            candidates = {
                "borrowings": [refs["borrowing"], "demo.track14.borrowing.autumn-twin"],
                "schooling_situations": [refs["school"]],
                "statements": [refs["statement"]],
            }
            introduce_borrowing_reference_durably(
                log, registry, reference_id=candidates["borrowings"][1],
                description="Autumn borrowing", actor="demo.user.filer",
                at="2026-09-29T12:00:40Z",
            )
            period = "demo.track14.period.autumn-twin"
            lender = "demo.track14.lender.cedar-twin"
            statement = "demo.track14.statement.autumn-twin"
            for identity, label, kind in (
                (period, "Autumn 2024", "tax.us.educational-period"),
                (lender, "Cedar Servicing", "tax.us.student-loan-lender"),
                (statement, "2025 Form 1098-E", "tax.us.1098e-statement"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            second_school = _append_source(
                log, registry, SCHOOLING,
                (("period", period), ("institution", "demo.track14.institution.river"),
                 ("programme", "demo.track14.programme.bsc")),
                "Riverside College, BSc, autumn 2024", "unresolved-equal-school",
            )
            second_statement = _append_source(
                log, registry, STATEMENT_TYPE,
                (("lender", lender), ("statement", statement), ("tax-year", "2025")),
                1250.0, "unresolved-equal-statement",
            )
            candidates["schooling_situations"].append(second_school)
            candidates["statements"].append(second_statement)

            result = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.unresolved-candidates",
                "evidence_id": "demo.evidence.track14.submission.unresolved-candidates",
                "actor": "demo.user.filer", "at": "2026-09-29T12:00:50Z",
                "borrowing_ref": None, "schooling_fact_id": None, "statement_fact_id": None,
                "financing_response": "cannot-tell", "inclusion_response": "unanswered",
                "recognition_context": {"unresolved_candidates": candidates},
            }, registry)
            self.assertEqual(result["claims"], {})
            reopened = ActLog(log.path.parent, registry)
            recovered = project(reopened.read().acts, registry)
            evidence = recovered.evidence["demo.evidence.track14.submission.unresolved-candidates"].evidence
            self.assertEqual(evidence["content"]["references"], {
                "borrowing_ref": None, "schooling_fact_id": None, "statement_fact_id": None,
            })
            self.assertEqual(evidence["content"]["recognition_context"]["unresolved_candidates"], candidates)
            self.assertEqual(evidence["content"]["responses"], {
                "financing_response": "cannot-tell", "inclusion_response": "unanswered",
            })
            current_ids = compute_currency(recovered).current_finding_ids
            current_facts = facts_of(recovered.fact_state)
            current_types = {
                current_facts[finding["fact_id"]].fact_type_id
                for finding_id, finding in recovered.findings.items()
                if finding_id in current_ids and finding["fact_id"] in current_facts
            }
            self.assertNotIn(FINANCING, current_types)
            self.assertNotIn(STATEMENT_INCLUSION, current_types)

    def test_no_answers_are_preserved_without_affirmative_relationships(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            result = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.no-answers",
                "evidence_id": "demo.evidence.track14.submission.no-answers",
                "actor": "demo.user.filer", "at": "2026-09-29T12:00:55Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "no",
                "inclusion_response": "no",
            }, registry)
            self.assertEqual(result["claims"], {})
            reopened = ActLog(log.path.parent, registry)
            recovered = project(reopened.read().acts, registry)
            answers = recovered.evidence["demo.evidence.track14.submission.no-answers"].evidence
            self.assertEqual(answers["content"]["responses"], {
                "financing_response": "no", "inclusion_response": "no",
            })
            current_ids = compute_currency(recovered).current_finding_ids
            current_facts = facts_of(recovered.fact_state)
            relationship_types = {
                current_facts[finding["fact_id"]].fact_type_id
                for finding_id, finding in recovered.findings.items()
                if finding_id in current_ids and finding["fact_id"] in current_facts
            }
            self.assertNotIn(FINANCING, relationship_types)
            self.assertNotIn(STATEMENT_INCLUSION, relationship_types)

    def test_known_financing_and_unresolved_inclusion_creates_no_membership(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            result = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.uncertain",
                "evidence_id": "demo.evidence.track14.submission.uncertain",
                "actor": "demo.user.filer", "at": "2026-09-29T12:01:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": "", "financing_response": "yes",
                "inclusion_response": "cannot-tell",
            }, registry)
            self.assertEqual(set(result["claims"]), {"financing"})
            state = project(log.read().acts, registry)
            current_ids = compute_currency(state).current_finding_ids
            current_types = {facts_of(state.fact_state)[row["fact_id"]].fact_type_id
                             for fid, row in state.findings.items()
                             if fid in current_ids and row["fact_id"] in facts_of(state.fact_state)}
            self.assertIn(FINANCING, current_types)
            self.assertNotIn(STATEMENT_INCLUSION, current_types)

    def test_ambiguous_or_stale_statement_reference_refuses_before_append(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            before = log.read().revision
            with self.assertRaises(RelationshipRecordingRefused):
                record_submission_durably(log, {
                    "submission_id": "demo.track14.submission.stale",
                    "evidence_id": "demo.evidence.track14.submission.stale",
                    "actor": "demo.user.filer", "at": "2026-09-29T12:02:00Z",
                    "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                    "statement_fact_id": "demo.stale.statement", "financing_response": "yes",
                    "inclusion_response": "yes",
                }, registry)
            self.assertEqual(log.read().revision, before)

    def test_financing_correction_and_withdrawal_leave_statement_claim_current(self) -> None:
        from packages.tax.sli_relationship_recording import (
            correct_relationship_claim_durably, withdraw_relationship_claim_durably,
        )

        raw, log, registry, refs = self._workspace()
        with raw:
            initial = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.lifecycle.initial",
                "evidence_id": "demo.evidence.track14.submission.lifecycle.initial",
                "actor": "demo.user.filer", "at": "2026-09-29T12:03:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes",
            }, registry)
            original_school_fact_id = refs["school"]
            school_keys = (("period", "demo.track14.period.autumn24"),
                           ("institution", "demo.track14.institution.river"),
                           ("programme", "demo.track14.programme.bsc"))
            _append_source(log, registry, SCHOOLING, school_keys,
                           "Riverside College, BSc, autumn 2024, corrected course description",
                           "school-corrected")
            corrected_school_state = project(log.read().acts, registry)
            corrected_school_finding = next(
                fid for fid, row in corrected_school_state.findings.items()
                if row["fact_id"] == original_school_fact_id and
                row["value"] == "Riverside College, BSc, autumn 2024, corrected course description"
            )
            current_after_school_correction = compute_currency(corrected_school_state).current_finding_ids
            self.assertIn(corrected_school_finding, current_after_school_correction)
            self.assertIn(initial["claims"]["financing"]["finding_id"], current_after_school_correction)
            self.assertIn(initial["claims"]["statement-inclusion"]["finding_id"], current_after_school_correction)
            school_withdrawal = act(log.read().revision, "finding-retracted",
                                    {"finding_id": corrected_school_finding})
            from packages.kernel.findings import apply_act
            apply_act(corrected_school_state, school_withdrawal, registry)
            log.append(school_withdrawal, expected_revision=log.read().revision)
            after_school_withdrawal = project(log.read().acts, registry)
            current_after_withdrawal = compute_currency(after_school_withdrawal).current_finding_ids
            self.assertNotIn(corrected_school_finding, current_after_withdrawal)
            self.assertIn(initial["claims"]["financing"]["finding_id"], current_after_withdrawal)
            self.assertIn(initial["claims"]["statement-inclusion"]["finding_id"], current_after_withdrawal)
            applicability = {row["finding_id"]: row["applicability"]
                             for row in current_claim_applicability(log.read().acts, registry)}
            self.assertEqual(applicability[initial["claims"]["financing"]["finding_id"]],
                             "unresolved-applicability")
            self.assertEqual(applicability[initial["claims"]["statement-inclusion"]["finding_id"]],
                             "current")
            successor_period = "demo.track14.period.spring25"
            successor_institution = "demo.track14.institution.metro"
            successor_programme = "demo.track14.programme.certificate"
            for identity, label, kind in (
                (successor_period, "Spring 2025", "tax.us.educational-period"),
                (successor_institution, "Metro College", "tax.us.educational-institution"),
                (successor_programme, "Certificate", "tax.us.educational-programme"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            alternate_school = _append_source(
                log, registry, SCHOOLING,
                (("period", successor_period), ("institution", successor_institution),
                 ("programme", successor_programme)),
                "Metro College, certificate, spring 2025", "school-successor",
            )
            corrected = correct_relationship_claim_durably(
                log, registry, finding_id=initial["claims"]["financing"]["finding_id"],
                actor="demo.user.filer", at="2026-09-29T12:04:00Z", successor={
                    "submission_id": "demo.track14.submission.lifecycle.corrected",
                    "evidence_id": "demo.evidence.track14.submission.lifecycle.corrected",
                    "actor": "demo.user.filer", "at": "2026-09-29T12:04:00Z",
                    "borrowing_ref": refs["borrowing"], "schooling_fact_id": alternate_school,
                    "statement_fact_id": refs["statement"], "financing_response": "yes",
                    "inclusion_response": "unanswered",
                },
            )
            corrected_finance = corrected["claims"]["financing"]["finding_id"]
            current_ids = compute_currency(corrected["state"]).current_finding_ids
            self.assertIn(corrected_finance, current_ids)
            self.assertNotIn(initial["claims"]["financing"]["finding_id"], current_ids)
            self.assertIn(initial["claims"]["statement-inclusion"]["finding_id"], current_ids)
            withdrawn = withdraw_relationship_claim_durably(
                log, registry, finding_id=corrected_finance, actor="demo.user.filer",
                at="2026-09-29T12:05:00Z",
            )
            current_ids = compute_currency(withdrawn["state"]).current_finding_ids
            self.assertNotIn(corrected_finance, current_ids)
            self.assertIn(initial["claims"]["statement-inclusion"]["finding_id"], current_ids)

    def test_unanswered_only_submission_is_inspectable_and_cannot_be_replayed(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            original = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.unanswered",
                "evidence_id": "demo.evidence.track14.submission.unanswered",
                "actor": "demo.user.filer", "at": "2026-09-29T12:06:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "unanswered",
                "inclusion_response": "cannot-tell",
            }, registry)
            self.assertEqual(original["claims"], {})
            before = log.read().revision
            with self.assertRaisesRegex(RelationshipRecordingRefused, "submission identity"):
                record_submission_durably(log, {
                    "submission_id": "demo.track14.submission.unanswered",
                    "evidence_id": "demo.evidence.track14.submission.unanswered-replay",
                    "actor": "demo.user.filer", "at": "2026-09-29T12:07:00Z",
                    "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                    "statement_fact_id": refs["statement"], "financing_response": "unanswered",
                    "inclusion_response": "unanswered",
                }, registry)
            self.assertEqual(log.read().revision, before)

    def test_normal_submission_cannot_forge_correction_lineage(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            before = log.read().revision
            with self.assertRaisesRegex(RelationshipRecordingRefused, "assigned by the correction"):
                record_submission_durably(log, {
                    "submission_id": "demo.track14.submission.forged-correction",
                    "evidence_id": "demo.evidence.track14.submission.forged-correction",
                    "actor": "demo.user.filer", "at": "2026-09-29T12:12:00Z",
                    "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                    "statement_fact_id": refs["statement"], "financing_response": "unanswered",
                    "inclusion_response": "unanswered",
                    "correction_of_finding_id": "demo.finding.someone-elses-claim",
                }, registry)
            self.assertEqual(log.read().revision, before)

    def test_equal_looking_subjects_remain_distinct_and_missing_choice_refuses(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            # Equal display text and equal statement amount do not merge or
            # select either subject; the opaque handles remain distinct.
            borrower2 = "demo.track14.borrowing.autumn-copy"
            introduce_borrowing_reference_durably(
                log, registry, reference_id=borrower2, description="Autumn borrowing",
                actor="demo.user.filer", at="2026-09-29T12:13:00Z",
            )
            period2 = "demo.track14.period.autumn24-copy"
            revision = log.read().revision
            log.append(act(revision, "entity-introduced", {"entity": demo_entity(
                period2, "Autumn 2024", "tax.us.educational-period")} ), expected_revision=revision)
            second_school = _append_source(
                log, registry, SCHOOLING,
                (("period", period2),
                 ("institution", "demo.track14.institution.river"),
                 ("programme", "demo.track14.programme.bsc")),
                "Riverside College, BSc, autumn 2024", "school-equal-valued-distinct-situation",
            )
            self.assertNotEqual(second_school, refs["school"])
            lender2, statement2 = "demo.track14.lender.equal", "demo.track14.statement.equal"
            for identity, label, kind in (
                (lender2, "Cedar Servicing", "tax.us.student-loan-lender"),
                (statement2, "2025 Form 1098-E", "tax.us.1098e-statement"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            _append_source(log, registry, STATEMENT_TYPE,
                           (("lender", lender2), ("statement", statement2), ("tax-year", "2025")),
                           1250.0, "statement-equal")
            before = log.read().revision
            for submission_id, override in (
                ("demo.track14.submission.no-borrowing", {"borrowing_ref": None,
                    "schooling_fact_id": refs["school"], "statement_fact_id": refs["statement"],
                    "financing_response": "yes", "inclusion_response": "unanswered"}),
                ("demo.track14.submission.no-school", {"borrowing_ref": refs["borrowing"],
                    "schooling_fact_id": None, "statement_fact_id": refs["statement"],
                    "financing_response": "yes", "inclusion_response": "unanswered"}),
                ("demo.track14.submission.no-statement", {"borrowing_ref": refs["borrowing"],
                    "schooling_fact_id": refs["school"], "statement_fact_id": None,
                    "financing_response": "unanswered", "inclusion_response": "yes"}),
            ):
                with self.assertRaises(RelationshipRecordingRefused):
                    record_submission_durably(log, {
                        "submission_id": submission_id,
                        "evidence_id": f"demo.evidence.{submission_id}",
                        "actor": "demo.user.filer", "at": "2026-09-29T12:14:00Z",
                        **override,
                    }, registry)
            self.assertEqual(log.read().revision, before)
            first = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.matrix.a",
                "evidence_id": "demo.evidence.track14.submission.matrix.a",
                "actor": "demo.user.filer", "at": "2026-09-29T12:15:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes",
            }, registry)
            second = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.matrix.b",
                "evidence_id": "demo.evidence.track14.submission.matrix.b",
                "actor": "demo.user.filer", "at": "2026-09-29T12:16:00Z",
                "borrowing_ref": borrower2, "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes",
            }, registry)
            separate_situation = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.matrix.c",
                "evidence_id": "demo.evidence.track14.submission.matrix.c",
                "actor": "demo.user.filer", "at": "2026-09-29T12:17:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": second_school,
                "statement_fact_id": None, "financing_response": "yes",
                "inclusion_response": "unanswered",
            }, registry)
            self.assertNotEqual(first["claims"]["financing"]["fact_id"],
                                second["claims"]["financing"]["fact_id"])
            self.assertNotEqual(first["claims"]["financing"]["fact_id"],
                                separate_situation["claims"]["financing"]["fact_id"])
            self.assertNotEqual(first["claims"]["statement-inclusion"]["fact_id"],
                                second["claims"]["statement-inclusion"]["fact_id"])

    def test_statement_inclusion_correction_and_withdrawal_are_independent(self) -> None:
        from packages.tax.sli_relationship_recording import (
            correct_relationship_claim_durably, withdraw_relationship_claim_durably,
        )

        raw, log, registry, refs = self._workspace()
        with raw:
            initial = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.statement.initial",
                "evidence_id": "demo.evidence.track14.submission.statement.initial",
                "actor": "demo.user.filer", "at": "2026-09-29T12:08:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes",
            }, registry)
            source_statement_keys = (("lender", "demo.track14.lender.cedar"),
                                     ("statement", "demo.track14.statement.2025"),
                                     ("tax-year", "2025"))
            membership_before_amount_correction = initial["claims"]["statement-inclusion"]["finding_id"]
            # ADR 0077 Part 5: a direct unscoped box 1 append while the inclusion is
            # current is refused at ActLog.append and not recorded.
            with self.assertRaisesRegex(FindingModelError, "scoped supersession violated"):
                _append_source(log, registry, STATEMENT_TYPE, source_statement_keys, 1999.0,
                               "statement-box1-corrected")
            corrected_source_state = project(log.read().acts, registry)
            self.assertNotIn("demo.finding.track14.statement-box1-corrected",
                             corrected_source_state.findings)
            after_amount_correction = compute_currency(corrected_source_state).current_finding_ids
            self.assertIn(membership_before_amount_correction, after_amount_correction)
            self.assertIn(initial["claims"]["financing"]["finding_id"], after_amount_correction)
            amount_applicability = {row["finding_id"]: row["applicability"]
                                    for row in current_claim_applicability(log.read().acts, registry)}
            self.assertEqual(amount_applicability[membership_before_amount_correction], "current")
            before = log.read().revision
            with self.assertRaisesRegex(RelationshipRecordingRefused, "exactly the predecessor"):
                correct_relationship_claim_durably(
                    log, registry, finding_id=initial["claims"]["financing"]["finding_id"],
                    actor="demo.user.filer", at="2026-09-29T12:09:00Z", successor={
                        "submission_id": "demo.track14.submission.statement.wrong-kind",
                        "evidence_id": "demo.evidence.track14.submission.statement.wrong-kind",
                        "actor": "demo.user.filer", "at": "2026-09-29T12:09:00Z",
                        "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                        "statement_fact_id": refs["statement"], "financing_response": "unanswered",
                        "inclusion_response": "yes",
                    },
                )
            self.assertEqual(log.read().revision, before)

            lender2 = "demo.track14.lender.other"
            statement2 = "demo.track14.statement.other"
            for identity, label, kind in (
                (lender2, "Other lender", "tax.us.student-loan-lender"),
                (statement2, "Other 2025 Form 1098-E", "tax.us.1098e-statement"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            second_statement = _append_source(
                log, registry, STATEMENT_TYPE,
                (("lender", lender2), ("statement", statement2), ("tax-year", "2025")),
                1250.0, "statement-box1-equal",
            )
            corrected = correct_relationship_claim_durably(
                log, registry, finding_id=initial["claims"]["statement-inclusion"]["finding_id"],
                actor="demo.user.filer", at="2026-09-29T12:10:00Z", successor={
                    "submission_id": "demo.track14.submission.statement.corrected",
                    "evidence_id": "demo.evidence.track14.submission.corrected",
                    "actor": "demo.user.filer", "at": "2026-09-29T12:10:00Z",
                    "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                    "statement_fact_id": second_statement, "financing_response": "unanswered",
                    "inclusion_response": "yes",
                },
            )
            new_membership = corrected["claims"]["statement-inclusion"]["finding_id"]
            current_ids = compute_currency(corrected["state"]).current_finding_ids
            self.assertIn(new_membership, current_ids)
            self.assertNotIn(initial["claims"]["statement-inclusion"]["finding_id"], current_ids)
            self.assertIn(initial["claims"]["financing"]["finding_id"], current_ids)
            withdrawn = withdraw_relationship_claim_durably(
                log, registry, finding_id=new_membership, actor="demo.user.filer",
                at="2026-09-29T12:11:00Z",
            )
            current_ids = compute_currency(withdrawn["state"]).current_finding_ids
            self.assertNotIn(new_membership, current_ids)
            self.assertIn(initial["claims"]["financing"]["finding_id"], current_ids)

    def test_retracting_named_statement_target_marks_only_inclusion_unresolved(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            initial = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.statement-target",
                "evidence_id": "demo.evidence.track14.submission.statement-target",
                "actor": "demo.user.filer", "at": "2026-09-29T12:18:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes",
            }, registry)
            statement_source = next(
                fid for fid, finding in initial["state"].findings.items()
                if finding["fact_id"] == refs["statement"]
            )
            retraction = act(log.read().revision, "finding-retracted", {"finding_id": statement_source})
            log.append(retraction, expected_revision=log.read().revision)
            state = project(log.read().acts, registry)
            current_ids = compute_currency(state).current_finding_ids
            self.assertIn(initial["claims"]["financing"]["finding_id"], current_ids)
            self.assertIn(initial["claims"]["statement-inclusion"]["finding_id"], current_ids)
            applicability = {row["finding_id"]: row["applicability"]
                             for row in current_claim_applicability(log.read().acts, registry)}
            self.assertEqual(applicability[initial["claims"]["financing"]["finding_id"]], "current")
            self.assertEqual(applicability[initial["claims"]["statement-inclusion"]["finding_id"]],
                             "unresolved-applicability")

    def test_superseded_borrowing_displaces_claims_from_current_projection(self) -> None:
        raw, log, registry, refs = self._workspace()
        with raw:
            initial = record_submission_durably(log, {
                "submission_id": "demo.track14.submission.borrowing-superseded",
                "evidence_id": "demo.evidence.track14.submission.borrowing-superseded",
                "actor": "demo.user.filer", "at": "2026-09-29T12:19:00Z",
                "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
                "statement_fact_id": refs["statement"], "financing_response": "yes",
                "inclusion_response": "yes",
            }, registry)
            before = log.read().revision
            log.append(act(before, "entity-superseded", {"entity_id": refs["borrowing"]}),
                       expected_revision=before)
            recovered = project(log.read().acts, registry)
            current_ids = compute_currency(recovered).current_finding_ids
            claim_ids = {claim["finding_id"] for claim in initial["claims"].values()}
            self.assertFalse(claim_ids & current_ids)
            self.assertTrue(claim_ids <= recovered.findings.keys())
            self.assertFalse(claim_ids & {
                row["finding_id"] for row in current_claim_applicability(log.read().acts, registry)
            })
