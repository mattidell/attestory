"""Track 16 one-review contract through the real Track 14 recorder and recovery."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas
from packages.tax.loader import install_domain_scoped_supersession
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.sli_relationship_recording import (
    FINANCING, STATEMENT_INCLUSION, RelationshipRecordingRefused,
)
from packages.tax.sli_relationship_review import (
    correct_review_claim, prepare_review, save_review, withdraw_review_claim,
)
from tests.support import act, demo_entity
import tests.test_sli_relationship_recording as track14

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
REGISTRY = install_domain_scoped_supersession(DerivationSchemas().registry)
USER = "demo.user.filer"


class OneReviewInput(unittest.TestCase):
    def _workspace(self) -> tuple[tempfile.TemporaryDirectory[str], ActLog, dict[str, str]]:
        raw = tempfile.TemporaryDirectory(prefix="sli-track16-")
        log = ActLog(Path(raw.name) / "workspace", REGISTRY)
        log.append(act(0, "bundle-adoption", {"bundle": json.loads((CONTENT / "f1098e.bundle.json").read_text())}),
                   expected_revision=0)
        log.append(act(1, "bundle-adoption", {"bundle": json.loads((CONTENT / "sli-relationship-source.bundle.json").read_text())}),
                   expected_revision=1)
        borrowing = "demo.track16.borrowing.autumn"
        from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably
        introduce_borrowing_reference_durably(log, REGISTRY, reference_id=borrowing,
                                               description="Autumn study borrowing", actor=USER,
                                               at="2026-09-30T10:00:00Z")
        entities = [
            ("demo.track16.period.autumn", "Autumn 2024", "tax.us.educational-period"),
            ("demo.track16.institution.river", "Riverside College", "tax.us.educational-institution"),
            ("demo.track16.programme.bsc", "BSc", "tax.us.educational-programme"),
            ("demo.track16.lender.cedar", "Cedar Servicing", "tax.us.student-loan-lender"),
            ("demo.track16.statement.2025", "2025 Form 1098-E", "tax.us.1098e-statement"),
        ]
        for identity, label, kind in entities:
            revision = log.read().revision
            log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                       expected_revision=revision)
        school = track14._append_source(
            log, REGISTRY, "tax.us.2025.sli.schooling-situation",
            (("period", entities[0][0]), ("institution", entities[1][0]), ("programme", entities[2][0])),
            "Riverside College, BSc, autumn 2024", "track16-school-a",
        )
        statement = track14._append_source(
            log, REGISTRY, "tax.us.2025.f1098e.box1-student-loan-interest",
            (("lender", entities[3][0]), ("statement", entities[4][0]), ("tax-year", "2025")),
            1200.0, "track16-statement-a",
        )
        return raw, log, {"borrowing": borrowing, "school": school, "statement": statement}

    def _review(self, log: ActLog, refs: dict[str, str], name: str,
                schools: tuple[str, ...] | None = None,
                statements: tuple[str, ...] | None = None) -> dict[str, Any]:
        return prepare_review(log, REGISTRY, review_id=f"demo.track16.review.{name}",
                              shown_at="2026-09-30T10:10:00Z",
                              borrowing_refs=(refs["borrowing"],),
                              schooling_fact_ids=(schools if schools is not None else (refs["school"],)),
                              statement_fact_ids=(statements if statements is not None else (refs["statement"],)))

    def _save(self, log: ActLog, refs: dict[str, str], review: dict[str, Any], name: str,
              **overrides: Any) -> dict[str, Any]:
        values: dict[str, Any] = {
            "borrowing_ref": refs["borrowing"], "schooling_fact_id": refs["school"],
            "statement_fact_id": refs["statement"], "financing_response": "yes",
            "inclusion_response": "yes", "actor": USER,
            "at": "2026-09-30T10:11:00Z", "submission_id": f"demo.track16.submission.{name}",
            "evidence_id": f"demo.evidence.track16.submission.{name}",
            "interest_portion_response": "unknown",
        }
        values.update(overrides)
        return save_review(log, REGISTRY, review, **values)

    def test_one_save_records_two_meanings_and_fresh_recovery(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            review = self._review(log, refs, "both")
            self.assertEqual(review["selections"], {"borrowing_ref": None,
                                                    "schooling_fact_id": None,
                                                    "statement_fact_id": None})
            self.assertEqual(review["propositions"]["financing"],
                             "Some of this borrowing financed these studies.")
            self.assertEqual(review["propositions"]["statement_inclusion"],
                             "This statement includes interest on this borrowing.")
            statement_card = review["statement_choices"][0]
            self.assertEqual((statement_card["tax_year"], statement_card["issuer_as_printed"],
                              statement_card["box_1_reported_total"]),
                             ("2025", "Cedar Servicing", 1200.0))
            self.assertNotEqual(statement_card["shown_as"], statement_card["choice_ref"])
            result = self._save(log, refs, review, "both")
            reopened = ActLog(log.path.parent, REGISTRY)
            state = project(reopened.read().acts, REGISTRY)
            current = compute_currency(state).current_finding_ids
            self.assertEqual(set(result["claims"]), {"financing", "statement-inclusion"})
            claims = result["claims"]
            self.assertTrue({row["finding_id"] for row in claims.values()} <= current)
            evidence = state.evidence[result["evidence_id"]].evidence["content"]
            context = evidence["recognition_context"]
            expected_fact_ids = {
                "financing": "tax.us.2025.sli.financing-relationship|borrowing=demo.track16.borrowing.autumn,period=demo.track16.period.autumn,institution=demo.track16.institution.river,programme=demo.track16.programme.bsc",
                "statement-inclusion": "tax.us.2025.sli.statement-inclusion-relationship|lender=demo.track16.lender.cedar,statement=demo.track16.statement.2025,tax-year=2025,borrowing=demo.track16.borrowing.autumn",
            }
            expected_finding_ids = {
                "financing": "sli.relationship.finding.43f808001ac5e38a6ded6962",
                "statement-inclusion": "sli.relationship.finding.fde2a64725f8195d1b9e2064",
            }
            expected_values = {"financing": "sli.financing.affirmed",
                               "statement-inclusion": "sli.statement-inclusion.affirmed"}
            self.assertEqual(context["responses"], {"financing": "yes", "statement_inclusion": "yes"})
            self.assertEqual(context["selections"], {"borrowing_ref": refs["borrowing"],
                                                      "schooling_fact_id": refs["school"],
                                                      "statement_fact_id": refs["statement"]})
            self.assertEqual(context["choices_shown"]["statement_choices"][0]["box_1_reported_total"], 1200.0)
            self.assertEqual(evidence["interest_portion_response"], "unknown")
            for kind, claim in claims.items():
                finding = state.findings[claim["finding_id"]]
                self.assertEqual(claim["fact_id"], expected_fact_ids[kind])
                self.assertEqual(claim["finding_id"], expected_finding_ids[kind])
                self.assertEqual(finding["value"], expected_values[kind])
                self.assertEqual(finding["fact_id"], expected_fact_ids[kind])
                self.assertEqual(finding["contribution_id"],
                                 expected_finding_ids[kind].replace("sli.relationship.finding.",
                                                                    "sli.relationship.contribution."))
                self.assertEqual(finding["evidence_ids"], [result["evidence_id"]])

    def test_equal_descriptions_need_explicit_selection_and_uncertainty_is_saved(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably
            twin_borrowing = "demo.track16.borrowing.autumn-copy"
            introduce_borrowing_reference_durably(log, REGISTRY, reference_id=twin_borrowing,
                                                   description="Autumn study borrowing", actor=USER,
                                                   at="2026-09-30T10:09:00Z")
            period = "demo.track16.period.twin"
            revision = log.read().revision
            log.append(act(revision, "entity-introduced", {"entity": demo_entity(
                period, "Autumn 2024", "tax.us.educational-period")}), expected_revision=revision)
            second_school = track14._append_source(
                log, REGISTRY, "tax.us.2025.sli.schooling-situation",
                (("period", period), ("institution", "demo.track16.institution.river"),
                 ("programme", "demo.track16.programme.bsc")),
                "Riverside College, BSc, autumn 2024", "track16-school-twin",
            )
            twin_lender = "demo.track16.lender.cedar-copy"
            twin_statement = "demo.track16.statement.2025-copy"
            for identity, label, kind in (
                (twin_lender, "Cedar Servicing", "tax.us.student-loan-lender"),
                (twin_statement, "2025 Form 1098-E", "tax.us.1098e-statement"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            second_statement = track14._append_source(
                log, REGISTRY, "tax.us.2025.f1098e.box1-student-loan-interest",
                (("lender", twin_lender), ("statement", twin_statement), ("tax-year", "2025")),
                1200.0, "track16-statement-twin",
            )
            review = prepare_review(
                log, REGISTRY, review_id="demo.track16.review.ambiguous-all",
                shown_at="2026-09-30T10:10:00Z",
                borrowing_refs=(refs["borrowing"], twin_borrowing),
                schooling_fact_ids=(refs["school"], second_school),
                statement_fact_ids=(refs["statement"], second_statement),
            )
            self.assertEqual([card["shown_as"] for card in review["borrowing_choices"]],
                             ["Autumn study borrowing"] * 2)
            self.assertEqual([card["shown_as"] for card in review["schooling_choices"]],
                             ["Riverside College, BSc, autumn 2024"] * 2)
            self.assertEqual([card["shown_as"] for card in review["statement_choices"]],
                             ["2025 Form 1098-E"] * 2)
            self.assertEqual([card["box_1_reported_total"] for card in review["statement_choices"]],
                             [1200.0, 1200.0])
            with self.assertRaisesRegex(RelationshipRecordingRefused, "financing yes/no requires explicit"):
                self._save(log, refs, review, "no-selection", borrowing_ref=None,
                           schooling_fact_id=None, financing_response="no", inclusion_response="unanswered")
            # Opaque handles cannot resolve cards whose complete visible content
            # is identical. Check each subject kind with the others unique.
            borrower_ambiguous = prepare_review(
                log, REGISTRY, review_id="demo.track16.review.borrower-ambiguous",
                shown_at="2026-09-30T10:10:00Z",
                borrowing_refs=(refs["borrowing"], twin_borrowing),
                schooling_fact_ids=(refs["school"],), statement_fact_ids=(),
            )
            with self.assertRaisesRegex(RelationshipRecordingRefused, "indistinguishable"):
                self._save(log, refs, borrower_ambiguous, "borrower-ambiguous",
                           borrowing_ref=refs["borrowing"], statement_fact_id=None,
                           financing_response="yes", inclusion_response="unanswered")
            school_ambiguous = prepare_review(
                log, REGISTRY, review_id="demo.track16.review.school-ambiguous",
                shown_at="2026-09-30T10:10:00Z",
                borrowing_refs=(refs["borrowing"],),
                schooling_fact_ids=(refs["school"], second_school), statement_fact_ids=(),
            )
            with self.assertRaisesRegex(RelationshipRecordingRefused, "indistinguishable"):
                self._save(log, refs, school_ambiguous, "school-ambiguous",
                           statement_fact_id=None, financing_response="no",
                           inclusion_response="unanswered")
            statement_ambiguous = prepare_review(
                log, REGISTRY, review_id="demo.track16.review.statement-ambiguous",
                shown_at="2026-09-30T10:10:00Z",
                borrowing_refs=(refs["borrowing"],), schooling_fact_ids=(),
                statement_fact_ids=(refs["statement"], second_statement),
            )
            with self.assertRaisesRegex(RelationshipRecordingRefused, "indistinguishable"):
                self._save(log, refs, statement_ambiguous, "statement-ambiguous",
                           schooling_fact_id=None, financing_response="unanswered",
                           inclusion_response="no")
            saved = self._save(log, refs, review, "cannot-tell", borrowing_ref=None,
                               schooling_fact_id=None, statement_fact_id=None,
                               financing_response="cannot-tell", inclusion_response="unanswered")
            reopened = ActLog(log.path.parent, REGISTRY)
            state = project(reopened.read().acts, REGISTRY)
            evidence = state.evidence[saved["evidence_id"]].evidence["content"]
            self.assertEqual(evidence["recognition_context"]["choices_shown"]["schooling_choices"][0]["shown_as"],
                             evidence["recognition_context"]["choices_shown"]["schooling_choices"][1]["shown_as"])
            self.assertEqual(evidence["recognition_context"]["responses"],
                             {"financing": "cannot-tell", "statement_inclusion": "unanswered"})
            self.assertEqual(saved["claims"], {})
            self.assertNotIn(FINANCING, {facts_of(state.fact_state)[row["fact_id"]].fact_type_id
                                         for fid, row in state.findings.items() if fid in compute_currency(state).current_finding_ids
                                         and row["fact_id"] in facts_of(state.fact_state)})

    def test_explicit_single_clause_and_stale_selection(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            review = self._review(log, refs, "single")
            saved = self._save(log, refs, review, "single", inclusion_response="unanswered")
            self.assertEqual(set(saved["claims"]), {"financing"})
            negative = self._save(log, refs, self._review(log, refs, "identified-no"),
                                  "identified-no", financing_response="no", inclusion_response="no")
            self.assertEqual(negative["claims"], {})
            no_state = project(ActLog(log.path.parent, REGISTRY).read().acts, REGISTRY)
            no_context = no_state.evidence[negative["evidence_id"]].evidence["content"]["recognition_context"]
            self.assertEqual(no_context["selections"], {"borrowing_ref": refs["borrowing"],
                                                         "schooling_fact_id": refs["school"],
                                                         "statement_fact_id": refs["statement"]})
            self.assertEqual(no_context["responses"], {"financing": "no", "statement_inclusion": "no"})
            stale_review = self._review(log, refs, "stale")
            inclusion_source = next(fid for fid, row in saved["state"].findings.items()
                                    if row["fact_id"] == refs["statement"])
            log.append(act(log.read().revision, "finding-retracted", {"finding_id": inclusion_source}),
                       expected_revision=log.read().revision)
            before = log.read().revision
            with self.assertRaisesRegex(RelationshipRecordingRefused, "reviewed choice is no longer current"):
                self._save(log, refs, stale_review, "stale", statement_fact_id=refs["statement"],
                           financing_response="unanswered", inclusion_response="yes")
            self.assertEqual(log.read().revision, before)

    def test_same_fact_id_value_correction_invalidates_the_shown_review(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            review = self._review(log, refs, "before-source-correction")
            track14._append_source(
                log, REGISTRY, "tax.us.2025.sli.schooling-situation",
                (("period", "demo.track16.period.autumn"),
                 ("institution", "demo.track16.institution.river"),
                 ("programme", "demo.track16.programme.bsc")),
                "Riverside College, BSc, autumn 2024 — corrected course description",
                "track16-school-description-correction",
            )
            track14._append_source(
                log, REGISTRY, "tax.us.2025.f1098e.box1-student-loan-interest",
                (("lender", "demo.track16.lender.cedar"),
                 ("statement", "demo.track16.statement.2025"), ("tax-year", "2025")),
                1350.0, "track16-statement-amount-correction",
            )
            corrected_state = project(log.read().acts, REGISTRY)
            corrected_current = compute_currency(corrected_state).current_finding_ids
            for fact_id, expected_type, expected_value, old_card in (
                (refs["school"], "tax.us.2025.sli.schooling-situation",
                 "Riverside College, BSc, autumn 2024 — corrected course description",
                 review["schooling_choices"][0]),
                (refs["statement"], "tax.us.2025.f1098e.box1-student-loan-interest",
                 1350.0, review["statement_choices"][0]),
            ):
                self.assertEqual(facts_of(corrected_state.fact_state)[fact_id].fact_type_id, expected_type)
                current_rows = [(finding_id, row) for finding_id, row in corrected_state.findings.items()
                                if finding_id in corrected_current and row["fact_id"] == fact_id]
                self.assertEqual(len(current_rows), 1)
                current_finding_id, current_finding = current_rows[0]
                self.assertEqual(current_finding["value"], expected_value)
                self.assertNotEqual(current_finding_id, old_card["support"][0]["finding_id"])
                self.assertNotEqual(current_finding["evidence_ids"],
                                    old_card["support"][0]["evidence_ids"])
            before = log.read().revision
            with self.assertRaisesRegex(RelationshipRecordingRefused, "prepared review changed"):
                self._save(log, refs, review, "old-display")
            self.assertEqual(log.read().revision, before)

    def test_source_change_after_review_before_submission_recorder_read_refuses_save(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            review = self._review(log, refs, "handoff-submission")
            reviewed_revision = log.read().revision
            original = track14._append_source
            injected = False
            import packages.tax.sli_relationship_review as review_module
            recorder = getattr(review_module, "record_submission_durably")

            def interleaved_recorder(target: ActLog, submission: dict[str, Any], registry: Any,
                                     *, expected_revision: int | None = None) -> dict[str, Any]:
                nonlocal injected
                if not injected:
                    injected = True
                    original(target, registry, "tax.us.2025.sli.schooling-situation",
                             (("period", "demo.track16.period.autumn"),
                              ("institution", "demo.track16.institution.river"),
                              ("programme", "demo.track16.programme.bsc")),
                             "Corrected after display", "handoff-school-correction")
                return cast(dict[str, Any], recorder(target, submission, registry,
                                                     expected_revision=expected_revision))

            setattr(review_module, "record_submission_durably", interleaved_recorder)
            try:
                with self.assertRaisesRegex(RelationshipRecordingRefused, "revision changed"):
                    self._save(log, refs, review, "handoff-submission")
            finally:
                setattr(review_module, "record_submission_durably", recorder)
            contents = log.read()
            state = project(contents.acts, REGISTRY)
            current = compute_currency(state).current_finding_ids
            school_id, school = next((fid, row) for fid, row in state.findings.items()
                                      if fid in current and row["fact_id"] == refs["school"])
            self.assertEqual(school["value"], "Corrected after display")
            self.assertEqual(school_id, "demo.finding.track14.handoff-school-correction")
            self.assertEqual(contents.revision, reviewed_revision + 3)
            self.assertNotIn("demo.evidence.track16.submission.handoff-submission", state.evidence)
            self.assertFalse(any(row.get("kind") == "evidence-submitted" and
                                 row.get("payload", {}).get("evidence", {}).get("id") ==
                                 "demo.evidence.track16.submission.handoff-submission"
                                 for row in contents.acts))
            self.assertFalse(any(row.get("kind") == "contribution" and
                                 row.get("payload", {}).get("contribution", {}).get("evidence_id") ==
                                 "demo.evidence.track16.submission.handoff-submission"
                                 for row in contents.acts))
            self.assertFalse(any(row.get("kind") == "assertion" and
                                 row.get("payload", {}).get("finding", {}).get("evidence_ids") ==
                                 ["demo.evidence.track16.submission.handoff-submission"]
                                 for row in contents.acts))

    def test_source_change_after_review_before_correction_recorder_read_refuses(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            initial = self._save(log, refs, self._review(log, refs, "handoff-correction-read-source"),
                                 "handoff-correction-read-source")
            predecessor = initial["claims"]["financing"]["finding_id"]
            review = self._review(log, refs, "handoff-correction-read")
            reviewed_revision = log.read().revision
            import packages.tax.sli_relationship_review as review_module
            recorder = getattr(review_module, "correct_relationship_claim_durably")
            injected = False

            def interleaved_recorder(target: ActLog, registry: Any, **kwargs: Any) -> dict[str, Any]:
                nonlocal injected
                if not injected:
                    injected = True
                    track14._append_source(
                        target, registry, "tax.us.2025.sli.schooling-situation",
                        (("period", "demo.track16.period.autumn"),
                         ("institution", "demo.track16.institution.river"),
                         ("programme", "demo.track16.programme.bsc")),
                        "Corrected after correction review", "handoff-correction-read-school",
                    )
                return cast(dict[str, Any], recorder(target, registry, **kwargs))

            setattr(review_module, "correct_relationship_claim_durably", interleaved_recorder)
            try:
                with self.assertRaisesRegex(RelationshipRecordingRefused, "revision changed"):
                    correct_review_claim(
                        log, REGISTRY, finding_id=predecessor, review=review,
                        borrowing_ref=refs["borrowing"], schooling_fact_id=refs["school"],
                        statement_fact_id=None, financing_response="yes", inclusion_response="unanswered",
                        actor=USER, at="2026-09-30T10:35:00Z",
                        submission_id="demo.track16.submission.handoff-correction-read",
                        evidence_id="demo.evidence.track16.handoff-correction-read",
                    )
            finally:
                setattr(review_module, "correct_relationship_claim_durably", recorder)
            contents = log.read()
            state = project(contents.acts, REGISTRY)
            current = compute_currency(state).current_finding_ids
            self.assertEqual(contents.revision, reviewed_revision + 3)
            self.assertIn(predecessor, current)
            self.assertNotIn("demo.evidence.track16.handoff-correction-read", state.evidence)
            self.assertFalse(any(row.get("kind") == "evidence-submitted" and
                                 row.get("payload", {}).get("evidence", {}).get("id") ==
                                 "demo.evidence.track16.handoff-correction-read" for row in contents.acts))
            self.assertFalse(any(row.get("kind") == "finding-retracted" and
                                 row.get("payload", {}).get("finding_id") == predecessor
                                 for row in contents.acts))
            self.assertFalse(any(row.get("evidence_ids") ==
                                 ["demo.evidence.track16.handoff-correction-read"]
                                 for row in state.findings.values()))
            school_id, school = next((fid, row) for fid, row in state.findings.items()
                                      if fid in current and row["fact_id"] == refs["school"])
            self.assertEqual(school_id, "demo.finding.track14.handoff-correction-read-school")
            self.assertEqual(school["value"], "Corrected after correction review")

    def test_source_change_before_correction_first_append_keeps_predecessor(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            initial = self._save(log, refs, self._review(log, refs, "handoff-correction-source"),
                                 "handoff-correction-source")
            predecessor = initial["claims"]["financing"]["finding_id"]
            review = self._review(log, refs, "handoff-correction")
            reviewed_revision = log.read().revision
            original_append = log.append
            injected = False
            source_appending = False

            def interleaved_append(item: dict[str, Any], expected_revision: int) -> int:
                nonlocal injected, source_appending
                if not injected and not source_appending and item.get("kind") == "finding-retracted" and \
                        item.get("payload", {}).get("finding_id") == predecessor:
                    injected = True
                    source_appending = True
                    try:
                        track14._append_source(
                            log, REGISTRY, "tax.us.2025.sli.schooling-situation",
                            (("period", "demo.track16.period.autumn"),
                             ("institution", "demo.track16.institution.river"),
                             ("programme", "demo.track16.programme.bsc")),
                            "Corrected before first append", "handoff-correction-school",
                        )
                    finally:
                        source_appending = False
                return original_append(item, expected_revision)

            setattr(log, "append", interleaved_append)
            try:
                with self.assertRaisesRegex(RelationshipRecordingRefused, "first append"):
                    correct_review_claim(
                        log, REGISTRY, finding_id=predecessor, review=review,
                        borrowing_ref=refs["borrowing"], schooling_fact_id=refs["school"],
                        statement_fact_id=None, financing_response="yes", inclusion_response="unanswered",
                        actor=USER, at="2026-09-30T10:40:00Z",
                        submission_id="demo.track16.submission.handoff-correction",
                        evidence_id="demo.evidence.track16.handoff-correction",
                    )
            finally:
                setattr(log, "append", original_append)
            contents = log.read()
            state = project(contents.acts, REGISTRY)
            current = compute_currency(state).current_finding_ids
            self.assertIn(predecessor, current)
            self.assertEqual(contents.revision, reviewed_revision + 3)
            self.assertNotIn("demo.evidence.track16.handoff-correction", state.evidence)
            self.assertFalse(any(row.get("kind") == "finding-retracted" and
                                 row.get("payload", {}).get("finding_id") == predecessor
                                 for row in contents.acts))
            school = next(row for fid, row in state.findings.items()
                          if fid in current and row["fact_id"] == refs["school"])
            self.assertEqual(school["value"], "Corrected before first append")

    def test_mutated_review_proposition_is_not_saved_as_shown(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            review = self._review(log, refs, "mutated-copy")
            review["propositions"]["financing"] = "A different claim the person did not see."
            before = log.read().revision
            with self.assertRaisesRegex(RelationshipRecordingRefused, "prepared review changed"):
                self._save(log, refs, review, "mutated-copy")
            self.assertEqual(log.read().revision, before)

    def test_correction_and_withdrawal_are_claim_specific_and_recoverable(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            extra_period = "demo.track16.period.metro"
            extra_institution = "demo.track16.institution.metro"
            extra_programme = "demo.track16.programme.certificate"
            other_lender = "demo.track16.lender.other"
            other_statement = "demo.track16.statement.other"
            for identity, label, kind in (
                (extra_period, "Spring 2025", "tax.us.educational-period"),
                (extra_institution, "Metro College", "tax.us.educational-institution"),
                (extra_programme, "Certificate", "tax.us.educational-programme"),
                (other_lender, "Pine Servicing", "tax.us.student-loan-lender"),
                (other_statement, "Other 2025 Form 1098-E", "tax.us.1098e-statement"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            metro_school = track14._append_source(
                log, REGISTRY, "tax.us.2025.sli.schooling-situation",
                (("period", extra_period), ("institution", extra_institution), ("programme", extra_programme)),
                "Metro College, Certificate, spring 2025", "track16-school-metro",
            )
            other_statement_id = track14._append_source(
                log, REGISTRY, "tax.us.2025.f1098e.box1-student-loan-interest",
                (("lender", other_lender), ("statement", other_statement), ("tax-year", "2025")),
                800.0, "track16-statement-other",
            )
            initial_review = self._review(log, refs, "lifecycle")
            initial = self._save(log, refs, initial_review, "lifecycle-initial")
            finance_id = initial["claims"]["financing"]["finding_id"]
            inclusion_id = initial["claims"]["statement-inclusion"]["finding_id"]
            second_borrowing = "demo.track16.borrowing.second"
            from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably
            introduce_borrowing_reference_durably(log, REGISTRY, reference_id=second_borrowing,
                                                   description="Campus borrowing", actor=USER,
                                                   at="2026-09-30T10:20:00Z")
            second_review = prepare_review(log, REGISTRY, review_id="demo.track16.review.second-statement",
                                           shown_at="2026-09-30T10:20:00Z",
                                           borrowing_refs=(second_borrowing,),
                                           schooling_fact_ids=(refs["school"],),
                                           statement_fact_ids=(other_statement_id,))
            other = self._save(log, {**refs, "borrowing": second_borrowing,
                                     "school": refs["school"], "statement": other_statement_id},
                               second_review, "other-subject")
            other_ids = {row["finding_id"] for row in other["claims"].values()}
            other_support = {
                finding_id: {key: other["state"].findings[finding_id][key]
                             for key in ("fact_id", "value", "evidence_ids", "contribution_id")}
                for finding_id in other_ids
            }

            correction_review = self._review(log, refs, "finance-correction", schools=(metro_school,))
            corrected = correct_review_claim(
                log, REGISTRY, finding_id=finance_id, review=correction_review,
                borrowing_ref=refs["borrowing"], schooling_fact_id=metro_school,
                statement_fact_id=None, financing_response="yes", inclusion_response="unanswered",
                actor=USER, at="2026-09-30T10:30:00Z",
                submission_id="demo.track16.submission.finance-correction",
                evidence_id="demo.evidence.track16.finance-correction",
            )
            successor_finance = corrected["claims"]["financing"]["finding_id"]
            withdraw_review_claim(log, REGISTRY, finding_id=inclusion_id, actor=USER,
                                 at="2026-09-30T10:31:00Z")
            reopened = ActLog(log.path.parent, REGISTRY)
            recovered = project(reopened.read().acts, REGISTRY)
            current = compute_currency(recovered).current_finding_ids
            self.assertIn(successor_finance, current)
            self.assertNotIn(finance_id, current)
            self.assertNotIn(inclusion_id, current)
            # The other borrowing and its second statement remain supported.
            self.assertTrue(other_ids <= current)
            for finding_id, expected in other_support.items():
                self.assertEqual({key: recovered.findings[finding_id][key] for key in expected}, expected)
            self.assertIn(initial["evidence_id"], recovered.evidence)
            self.assertIn(corrected["evidence_id"], recovered.evidence)


    def test_reverse_lifecycle_corrects_inclusion_then_withdraws_financing(self) -> None:
        raw, log, refs = self._workspace()
        with raw:
            lender = "demo.track16.lender.replacement"
            statement = "demo.track16.statement.replacement"
            for identity, label, kind in (
                (lender, "Maple Servicing", "tax.us.student-loan-lender"),
                (statement, "Replacement 2025 Form 1098-E", "tax.us.1098e-statement"),
            ):
                revision = log.read().revision
                log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=revision)
            replacement_statement = track14._append_source(
                log, REGISTRY, "tax.us.2025.f1098e.box1-student-loan-interest",
                (("lender", lender), ("statement", statement), ("tax-year", "2025")),
                600.0, "track16-statement-replacement",
            )
            review = self._review(log, refs, "reverse-initial")
            initial = self._save(log, refs, review, "reverse-initial")
            finance_id = initial["claims"]["financing"]["finding_id"]
            inclusion_id = initial["claims"]["statement-inclusion"]["finding_id"]
            corrected_review = self._review(log, refs, "reverse-correction",
                                            statements=(replacement_statement,))
            corrected = correct_review_claim(
                log, REGISTRY, finding_id=inclusion_id, review=corrected_review,
                borrowing_ref=refs["borrowing"], schooling_fact_id=None,
                statement_fact_id=replacement_statement, financing_response="unanswered",
                inclusion_response="yes", actor=USER, at="2026-09-30T10:50:00Z",
                submission_id="demo.track16.submission.reverse-correction",
                evidence_id="demo.evidence.track16.reverse-correction",
            )
            successor = corrected["claims"]["statement-inclusion"]["finding_id"]
            withdraw_review_claim(log, REGISTRY, finding_id=finance_id, actor=USER,
                                 at="2026-09-30T10:51:00Z")
            recovered = project(ActLog(log.path.parent, REGISTRY).read().acts, REGISTRY)
            current = compute_currency(recovered).current_finding_ids
            self.assertIn(successor, current)
            self.assertNotIn(inclusion_id, current)
            self.assertNotIn(finance_id, current)
            self.assertIn(initial["evidence_id"], recovered.evidence)
            self.assertIn(corrected["evidence_id"], recovered.evidence)


if __name__ == "__main__":
    unittest.main()
