"""Track 4 Form 1098 answer review, atomic recording, and saved run association."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
from unittest.mock import patch

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.f1098_statement_recording import F1098RecordingRefused
from packages.tax.f1098_statement_review import (
    F1098ReviewRefused, QUESTIONS, answer_f1098_statement_review_question,
    answer_f1098_statement_review_timing, associate_saved_run,
    correct_f1098_statement_review_answer,
    prepare_f1098_statement_review, save_f1098_statement_review,
    review_f1098_statement_with_saved_presentation, withdraw_f1098_statement_review_answers,
)
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry
from tests.test_f1098_circumstances_calculation import (  # type: ignore[attr-defined]
    CONTENT, RELEASE_DIR, ROOT, SCOPE, USER as RUN_USER, _acts,
    F1098E_CLOSURE_TYPE,
)


REGISTRY_PATH = CONTENT / "published-packages.v42.json"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v42.json"
RELEASE_ID = "demo.release.sli-worksheet-integration.2025"
ANSWER_SUFFIXES = (
    "owns-the-home", "lives-there-most-of-the-time", "home-is-collateral", "owes-the-loan",
    "paid-the-interest", "no-one-else-owes-it", "what-the-money-paid-for", "this-is-the-original-loan",
    "mortgage-credit-certificate-received",
)
BASE_ANSWERS = {
    "owns-the-home": "yes", "lives-there-most-of-the-time": "yes", "home-is-collateral": "yes",
    "owes-the-loan": "yes", "paid-the-interest": "yes", "no-one-else-owes-it": "yes",
    "what-the-money-paid-for": "bought-the-home", "this-is-the-original-loan": "yes",
    "mortgage-credit-certificate-received": "not-received",
}
USER = "demo.taxpayer"


def _base_acts(*, filing_status: str | None = None, second_interest: int | None = None) -> list[dict[str, Any]]:
    rows = _acts(20000, filing_status=filing_status, second_interest=second_interest)
    answer_prefix = "tax.us.2025.f1098."
    filtered: list[dict[str, Any]] = []
    for row in rows:
        if row.get("kind") == "bundle-adoption":
            payload = row.get("payload")
            bundle = payload.get("bundle", {}) if isinstance(payload, dict) else {}
            if isinstance(bundle, dict) and bundle.get("id") == "tax.us.2025.f1098-successor.vocabulary":
                continue
        payload = row.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        fact_id = finding.get("fact_id", "") if isinstance(finding, dict) else ""
        if row.get("kind") == "assertion" and fact_id.startswith(answer_prefix) and any(
            f"{answer_prefix}{suffix}|" in fact_id for suffix in ANSWER_SUFFIXES + (
                "loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving",
            )
        ):
            continue
        filtered.append(copy.deepcopy(row))
    for index, row in enumerate(filtered):
        row["committed_against"] = index
        row["act_id"] = f"demo.f1098.track4.seed.act.{index:04d}"
    return filtered


def _append_seed(log: ActLog, *, filing_status: str | None = None, second_interest: int | None = None) -> None:
    acts = _base_acts(filing_status=filing_status, second_interest=second_interest)
    log.append_batch(acts, expected_revision=0)


def _evidence_ids(answers: dict[str, str], prefix: str = "demo.f1098.evidence") -> dict[str, str]:
    return {question: f"{prefix}.{question}" for question in answers}


def _review(log: ActLog, registry: Any) -> dict[str, Any]:
    return prepare_f1098_statement_review(log, registry, review_id=f"demo.review.{log.read().revision}",
                                         shown_at="2026-10-15T12:00:00Z")


def _save(log: ActLog, registry: Any, answers: dict[str, str], submission: str = "demo.f1098.first") -> dict[str, Any]:
    review = _review(log, registry)
    return save_f1098_statement_review(
        log, registry, review, answers=answers, submission_id=submission,
        evidence_ids=_evidence_ids(answers), actor=USER, at="2026-10-15T12:01:00Z",
    )


class F1098StatementReviewTests(unittest.TestCase):
    def test_local_no_one_else_owes_wording_matches_yes_choice(self) -> None:
        question = QUESTIONS["no-one-else-owes-it"]
        self.assertEqual(question["question"], "Do only you and, if filing jointly, your spouse owe this loan?")
        self.assertEqual(question["labels"]["yes"], "No one else owes it")
        self.assertEqual(question["labels"]["no"], "Someone else owes it")
        self.assertIn("Only when you file jointly", question["help"])
        self.assertIn("If you file separately", question["help"])
        original = QUESTIONS["this-is-the-original-loan"]
        self.assertIn("change in the company collecting payments does not", original["help"])

    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="f1098-answer-review-")
        self.addCleanup(self.temp.cleanup)
        self.registry = tax_registry()
        self.log = ActLog(Path(self.temp.name) / "workspace", self.registry)
        _append_seed(self.log)

    def test_real_account_admission_and_one_atomic_nine_answer_save(self) -> None:
        review = _review(self.log, self.registry)
        self.assertEqual(review["statement"]["payerLabel"], "Synthetic lender")
        self.assertEqual(review["statement"]["taxYear"], "2025")
        self.assertEqual(review["statement"]["box1"], 20000)
        self.assertEqual(len(review["questions"]), 11)
        self.assertIn("nobody paid any for you", review["questions"]["paid-the-interest"]["help"])
        self.assertEqual(review["questions"]["loan-timing-relative-to-purchase"]["state"], "absent")
        self.assertEqual(review["questions"]["loan-timing-relative-to-purchase"]["defaultPolicy"], {
            "parameterId": "tax.us.2025.parameter.f1098-timing-purchase-structural-default",
            "parameterVersion": "v1", "value": "not-asked", "status": "proposed-until-bundle-adoption",
        })
        before = self.log.read().revision
        saved = save_f1098_statement_review(
            self.log, self.registry, review, answers=BASE_ANSWERS, submission_id="demo.f1098.nine",
            evidence_ids=_evidence_ids(BASE_ANSWERS), actor=USER, at="2026-10-15T12:02:00Z",
        )
        self.assertEqual(len(saved["finding_ids"]), 9)
        self.assertGreater(saved["revision"], before)
        acts = self.log.read().acts[before:]
        self.assertEqual(sum(row["kind"] == "bundle-adoption" for row in acts), 1)
        self.assertEqual(sum(row["kind"] == "evidence-submitted" for row in acts), 9)
        self.assertEqual(sum(row["kind"] == "contribution" for row in acts), 9)
        self.assertEqual(sum(row["kind"] == "assertion" for row in acts), 9)
        fresh = _review(self.log, self.registry)
        self.assertEqual(fresh["questions"]["paid-the-interest"]["answer"], "yes")

    def test_explicit_selection_reviews_one_of_two_current_statements(self) -> None:
        log = ActLog(Path(self.temp.name) / "two-statements", self.registry)
        _append_seed(log, second_interest=3500)
        state = project(log.read().acts, self.registry)
        lattice = facts_of(state.fact_state)
        current_ids = compute_currency(state).current_finding_ids
        sources = [lattice[finding["fact_id"]] for finding_id, finding in state.findings.items()
                   if finding_id in current_ids and finding["fact_id"] in lattice
                   and lattice[finding["fact_id"]].fact_type_id == "tax.us.2025.f1098.box1-mortgage-interest"]
        sources = list({fact.fact_id: fact for fact in sources}.values())
        self.assertEqual(len(sources), 2)
        with self.assertRaises(F1098ReviewRefused):
            _review(log, self.registry)
        selected_keys = dict(sources[1].keys)
        selected = prepare_f1098_statement_review(
            log, self.registry, review_id="demo.review.selected-b",
            shown_at="2026-10-15T12:00:00Z", statement_keys=selected_keys,
        )
        self.assertEqual(selected["statement"]["keys"], selected_keys)
        saved = save_f1098_statement_review(
            log, self.registry, selected, answers=BASE_ANSWERS,
            submission_id="demo.f1098.selected-b", evidence_ids=_evidence_ids(BASE_ANSWERS),
            actor=USER, at="2026-10-15T12:01:00Z",
        )
        self.assertEqual(len(saved["finding_ids"]), 9)
        fresh = prepare_f1098_statement_review(
            log, self.registry, review_id="demo.review.selected-b.fresh",
            shown_at="2026-10-15T12:02:00Z", statement_keys=selected_keys,
        )
        self.assertEqual(fresh["questions"]["paid-the-interest"]["answer"], "yes")
        self.assertEqual(fresh["revision"], saved["revision"])

    def test_first_save_interruption_leaves_no_adoption_or_partial_answers(self) -> None:
        review = _review(self.log, self.registry)
        before = self.log.path.read_bytes()
        with patch("packages.kernel.act_log.os.replace", side_effect=OSError("simulated interruption before batch rename")):
            with self.assertRaises(OSError):
                save_f1098_statement_review(
                    self.log, self.registry, review, answers=BASE_ANSWERS,
                    submission_id="demo.f1098.interrupted-first-save", evidence_ids=_evidence_ids(BASE_ANSWERS),
                    actor=USER, at="2026-10-15T12:03:00Z",
                )
        self.assertEqual(self.log.path.read_bytes(), before)
        self.assertEqual(self.log.read().revision, review["revision"])

    def test_forged_readonly_snapshot_and_directly_malformed_presentation_fail_closed(self) -> None:
        review = _review(self.log, self.registry)
        forged = copy.deepcopy(review)
        forged["statement"]["box1"] = 1
        before = self.log.read().revision
        with self.assertRaises(F1098ReviewRefused):
            save_f1098_statement_review(
                self.log, self.registry, forged, answers=BASE_ANSWERS,
                submission_id="demo.f1098.forged", evidence_ids=_evidence_ids(BASE_ANSWERS),
                actor=USER, at="2026-10-15T12:04:00Z",
            )
        self.assertEqual(self.log.read().revision, before)
        records = RecordStream(Path(self.temp.name) / "records", DerivationSchemas())
        malformed = Path(self.temp.name) / "malformed-presentation.json"
        malformed.write_text('{"runId": "forged", "mortgageInterestExplanation": {}}', encoding="utf-8")
        combined = review_f1098_statement_with_saved_presentation(
            self.log, self.registry, malformed, records, review_id="demo.review.malformed",
            shown_at="2026-10-15T12:04:30Z",
        )
        self.assertEqual(combined["calculationAssociation"]["state"], "recalculation-needed")
        self.assertIsNone(combined["savedCalculation"])

    def test_timing_zero_one_two_and_reserved_default_are_distinct(self) -> None:
        answers = {**BASE_ANSWERS, "what-the-money-paid-for": "unrelated-personal-expense"}
        _save(self.log, self.registry, answers, "demo.f1098.personal.zero")
        review = _review(self.log, self.registry)
        self.assertEqual(review["questions"]["loan-timing-relative-to-building-or-improving"]["state"], "absent")
        first = answer_f1098_statement_review_timing(
            self.log, self.registry, review, question="loan-timing-relative-to-purchase", answer="no",
            submission_id="demo.f1098.timing.one", evidence_id="demo.f1098.evidence.timing.one",
            actor=USER, at="2026-10-15T12:05:00Z",
        )
        self.assertEqual(len(first["finding_ids"]), 1)
        one = _review(self.log, self.registry)
        self.assertEqual(one["questions"]["loan-timing-relative-to-purchase"]["answer"], "no")
        self.assertEqual(one["questions"]["loan-timing-relative-to-building-or-improving"]["state"], "absent")
        second = answer_f1098_statement_review_timing(
            self.log, self.registry, one, question="loan-timing-relative-to-building-or-improving", answer="no",
            submission_id="demo.f1098.timing.two", evidence_id="demo.f1098.evidence.timing.two",
            actor=USER, at="2026-10-15T12:06:00Z",
        )
        self.assertEqual(len(second["finding_ids"]), 1)
        two = _review(self.log, self.registry)
        self.assertEqual(two["questions"]["loan-timing-relative-to-building-or-improving"]["answer"], "no")

    def test_irrelevant_timing_submission_unknown_and_not_asked_refuse_without_write(self) -> None:
        before = self.log.path.read_bytes() if self.log.path.exists() else b""
        answers = {**BASE_ANSWERS, "loan-timing-relative-to-purchase": "no"}
        for bad in (answers, {**BASE_ANSWERS, "unknown-question": "yes"},
                    {**BASE_ANSWERS, "what-the-money-paid-for": "not-asked"}):
            with self.subTest(bad=bad), self.assertRaises(F1098ReviewRefused):
                _save(self.log, self.registry, bad, "demo.f1098.invalid")
            self.assertEqual(self.log.path.read_bytes(), before)

    def test_correction_payment_replaces_current_answer_and_withdrawal_never_asserts_opposite(self) -> None:
        _save(self.log, self.registry, BASE_ANSWERS, "demo.f1098.payment.start")
        review = _review(self.log, self.registry)
        correct_f1098_statement_review_answer(
            self.log, self.registry, review, question="paid-the-interest", answer="paid-by-others-or-partial",
            submission_id="demo.f1098.payment.partial", evidence_id="demo.f1098.payment.partial.evidence",
            actor=USER, at="2026-10-15T12:10:00Z",
        )
        partial = _review(self.log, self.registry)
        self.assertEqual(partial["questions"]["paid-the-interest"]["answer"], "paid-by-others-or-partial")
        with self.assertRaises(F1098ReviewRefused):
            correct_f1098_statement_review_answer(
                self.log, self.registry, review, question="paid-the-interest", answer="yes",
                submission_id="demo.f1098.payment.stale", evidence_id="demo.f1098.payment.stale.evidence",
                actor=USER, at="2026-10-15T12:11:00Z",
            )
        target = partial["questions"]["paid-the-interest"]["finding_id"]
        withdraw_f1098_statement_review_answers(
            self.log, self.registry, partial, questions=["paid-the-interest"], submission_id="demo.f1098.payment.withdraw",
            actor=USER, at="2026-10-15T12:12:00Z",
        )
        after = _review(self.log, self.registry)
        self.assertEqual(after["questions"]["paid-the-interest"]["state"], "absent")
        state = project(self.log.read().acts, self.registry)
        self.assertNotIn(target, compute_currency(state).current_finding_ids)
        self.assertEqual(self.log.read().acts[-1]["kind"], "finding-retracted")
        reanswered = answer_f1098_statement_review_question(
            self.log, self.registry, after, question="paid-the-interest", answer="yes",
            submission_id="demo.f1098.payment.reanswered", evidence_id="demo.f1098.payment.reanswered.evidence",
            actor=USER, at="2026-10-15T12:13:00Z",
        )
        self.assertNotEqual(reanswered["finding_ids"][0], target)
        self.assertNotIn(target, compute_currency(project(self.log.read().acts, self.registry)).current_finding_ids)

    def test_withdrawing_both_timing_answers_is_one_batch_and_use_correction_retains_them(self) -> None:
        answers = {**BASE_ANSWERS, "what-the-money-paid-for": "unrelated-personal-expense",
                   "loan-timing-relative-to-purchase": "no",
                   "loan-timing-relative-to-building-or-improving": "no"}
        _save(self.log, self.registry, answers, "demo.f1098.timing.pair")
        review = _review(self.log, self.registry)
        correction = correct_f1098_statement_review_answer(
            self.log, self.registry, review, question="what-the-money-paid-for", answer="other",
            submission_id="demo.f1098.use.other", evidence_id="demo.f1098.use.other.evidence",
            actor=USER, at="2026-10-15T12:20:00Z",
        )
        self.assertEqual(len(correction["finding_ids"]), 1)
        irrelevant = _review(self.log, self.registry)
        self.assertEqual(irrelevant["questions"]["loan-timing-relative-to-purchase"]["state"], "answered")
        self.assertEqual(irrelevant["questions"]["loan-timing-relative-to-purchase"]["relevance"], "retained-but-irrelevant")
        retained_ids = [irrelevant["questions"][question]["finding_id"] for question in (
            "loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving")]
        correct_f1098_statement_review_answer(
            self.log, self.registry, irrelevant, question="what-the-money-paid-for",
            answer="unrelated-personal-expense", submission_id="demo.f1098.use.personal-again",
            evidence_id="demo.f1098.use.personal-again.evidence", actor=USER,
            at="2026-10-15T12:20:30Z",
        )
        restored = _review(self.log, self.registry)
        self.assertEqual([restored["questions"][question]["finding_id"] for question in (
            "loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving")], retained_ids)
        self.assertTrue(all(restored["questions"][question]["relevance"] == "relevant" for question in (
            "loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving")))
        start = self.log.read().revision
        before_bytes = self.log.path.read_bytes()
        with patch("packages.kernel.act_log.os.replace", side_effect=OSError("simulated interruption before batch rename")):
            with self.assertRaises(OSError):
                withdraw_f1098_statement_review_answers(
                    self.log, self.registry, restored,
                    questions=["loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving"],
                    submission_id="demo.f1098.timing.interrupted", actor=USER, at="2026-10-15T12:21:00Z",
                )
        self.assertEqual(self.log.path.read_bytes(), before_bytes)
        self.assertEqual(self.log.read().revision, start)
        withdraw_f1098_statement_review_answers(
            self.log, self.registry, restored,
            questions=["loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving"],
            submission_id="demo.f1098.timing.withdraw-pair", actor=USER, at="2026-10-15T12:21:00Z",
        )
        withdrawal = self.log.read().acts[start:]
        self.assertEqual(len(withdrawal), 3)
        self.assertEqual(withdrawal[0]["kind"], "evidence-submitted")
        self.assertTrue(all(row["kind"] == "finding-retracted" for row in withdrawal[1:]))
        self.assertEqual(withdrawal[0]["payload"]["evidence"]["content"]["target_finding_ids"],
                         [restored["questions"][q]["finding_id"] for q in (
                             "loan-timing-relative-to-purchase", "loan-timing-relative-to-building-or-improving")])


class F1098SavedRunAssociationTests(unittest.TestCase):
    def test_incomplete_first_answer_stays_unresolved_on_real_coordinator(self) -> None:
        with TemporaryDirectory(prefix="f1098-live-incomplete-answer-") as temp:
            registry = tax_registry()
            capability = WorkspaceCapability(Path(temp) / "workspace")
            log = ActLog(Path(temp) / "workspace", registry)
            _append_seed(log)
            review = _review(log, registry)
            answer_f1098_statement_review_question(
                log, registry, review, question="paid-the-interest", answer="yes",
                submission_id="demo.f1098.incomplete.first-answer",
                evidence_id="demo.f1098.incomplete.first-answer.evidence", actor=USER,
                at="2026-10-15T12:49:00Z",
            )
            current = _review(log, registry)
            self.assertEqual(current["questions"]["paid-the-interest"]["answer"], "yes")
            self.assertTrue(all(
                current["questions"][question]["state"] == "absent"
                for question in BASE_ANSWERS if question != "paid-the-interest"
            ))
            contents = log.read()
            outcome = live_coordinate_run(
                capability, repo_root=ROOT, authoritative_acts=contents.acts,
                workspace_revision=contents.revision, run_scope=SCOPE, scope_user=RUN_USER,
                request={"schema": "run-request.v1"},
                run_id="demo.f1098.track4.incomplete-first-answer", governance_pins=[],
                surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT),
                output_name="demo.f1098.track4.incomplete-first-answer.json",
            )
            self.assertIsNone(outcome.refusal)
            self.assertIsNotNone(outcome.presentation_path)
            presentation = cast(dict[str, Any], json.loads(
                cast(Path, outcome.presentation_path).read_text("utf-8")
            ))
            self.assertNotIn("mortgageInterestExplanation", presentation)
            unresolved = next(
                row for row in presentation["sections"]
                if row["field"].get("id") == "tax.us.2025.form.f1098.residence-interest-unresolved"
            )
            self.assertTrue(unresolved["resolved"]["reasons"])
            self.assertIsNotNone(outcome.output_path)
            report = cast(dict[str, Any], json.loads(
                cast(Path, outcome.output_path).read_text("utf-8")
            ))
            line8a_disposition = next(
                row for row in report["dispositions"]
                if row["artifact_id"] == "tax.us.2025.rule.f1098-line8a"
            )
            self.assertEqual(line8a_disposition["disposition"], "blocked")

    def test_recorder_timing_zero_one_two_has_distinct_live_outcomes(self) -> None:
        with TemporaryDirectory(prefix="f1098-live-timing-answer-") as temp:
            registry = tax_registry()
            capability = WorkspaceCapability(Path(temp) / "workspace")
            log = ActLog(Path(temp) / "workspace", registry)
            _append_seed(log)
            personal = {**BASE_ANSWERS, "what-the-money-paid-for": "unrelated-personal-expense"}
            _save(log, registry, personal, "demo.f1098.live-timing-zero")
            records = RecordStream(capability.location / "records", DerivationSchemas())

            def run(run_id: str) -> dict[str, Any]:
                contents = log.read()
                outcome = live_coordinate_run(
                    capability, repo_root=ROOT, authoritative_acts=contents.acts,
                    workspace_revision=contents.revision, run_scope=SCOPE, scope_user=RUN_USER,
                    request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
                    surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT), output_name=f"{run_id}.json",
                )
                self.assertIsNone(outcome.refusal)
                self.assertIsNotNone(outcome.presentation_path)
                presentation_path = cast(Path, outcome.presentation_path)
                return cast(dict[str, Any], json.loads(presentation_path.read_text("utf-8")))

            zero = run("demo.f1098.track4.timing-zero")
            zero_field = next(row for row in zero["sections"]
                              if row["field"].get("id") == "tax.us.2025.form.f1098.residence-interest-unresolved")
            self.assertTrue(zero_field["resolved"]["reasons"])

            review = _review(log, registry)
            answer_f1098_statement_review_timing(
                log, registry, review, question="loan-timing-relative-to-purchase", answer="no",
                submission_id="demo.f1098.live-timing-one", evidence_id="demo.f1098.live-timing-one.evidence",
                actor=USER, at="2026-10-15T12:50:00Z",
            )
            one = run("demo.f1098.track4.timing-one")
            one_field = next(row for row in one["sections"]
                             if row["field"].get("id") == "tax.us.2025.form.f1098.residence-interest-unresolved")
            self.assertTrue(one_field["resolved"]["reasons"])
            self.assertTrue(one_field["resolved"]["reasons"])

            review = _review(log, registry)
            answer_f1098_statement_review_timing(
                log, registry, review, question="loan-timing-relative-to-building-or-improving", answer="no",
                submission_id="demo.f1098.live-timing-two", evidence_id="demo.f1098.live-timing-two.evidence",
                actor=USER, at="2026-10-15T12:51:00Z",
            )
            two = run("demo.f1098.track4.timing-two")
            two_field = next(row for row in two["sections"]
                             if row["field"].get("id") == "tax.us.2025.form.f1098.residence-interest-unresolved")
            self.assertIn("mortgageInterestExplanation", two,
                          json.dumps({"review": _review(log, registry)["questions"],
                                      "unresolvedField": two_field["resolved"],
                                      "sections": [(row["field"].get("id"), row["field"].get("binds_symbol"),
                                                    row["resolved"]) for row in two["sections"]]},
                                     sort_keys=True))
            self.assertEqual(two["mortgageInterestExplanation"]["accounts"][0]["reason"],
                             "use-unrelated-personal-expense")

    def test_actual_v44_live_run_is_associated_only_at_its_recorded_revision(self) -> None:
        with TemporaryDirectory(prefix="f1098-live-answer-") as temp:
            registry = tax_registry()
            capability = WorkspaceCapability(Path(temp) / "workspace")
            log = ActLog(Path(temp) / "workspace", registry)
            _append_seed(log, filing_status="married_filing_jointly")
            seed_revision = log.read().revision
            seed_state = project(log.read().acts, registry)
            seed_lattice = facts_of(seed_state.fact_state, include_displaced=True)
            closed_empty_history = sorted(
                (fid, row["fact_id"], row["value"])
                for fid, row in seed_state.findings.items()
                if row["fact_id"] in seed_lattice
                and seed_lattice[row["fact_id"]].fact_type_id == F1098E_CLOSURE_TYPE
            )
            self.assertTrue(closed_empty_history, "fixture must retain its native closed-empty Form 1098-E account")
            _save(log, registry, BASE_ANSWERS, "demo.f1098.live-save")

            def run(run_id: str) -> Any:
                contents = log.read()
                outcome = live_coordinate_run(
                    capability, repo_root=ROOT, authoritative_acts=contents.acts,
                    workspace_revision=contents.revision, run_scope=SCOPE, scope_user=RUN_USER,
                    request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
                    surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT), output_name=f"{run_id}.json",
                )
                self.assertIsNone(outcome.refusal)
                self.assertIsNotNone(outcome.presentation_path)
                return outcome

            result = run("demo.f1098.track4.run1")
            first_contents = log.read()
            presentation = json.loads(result.presentation_path.read_text("utf-8"))
            saved_presentation_bytes = result.presentation_path.read_bytes()
            records = RecordStream(capability.location / "records", DerivationSchemas())
            self.assertEqual(associate_saved_run(presentation, records, first_contents.revision)["state"], "current")
            combined = review_f1098_statement_with_saved_presentation(
                log, registry, result.presentation_path, records, review_id="demo.review.saved",
                shown_at="2026-10-15T12:29:00Z",
            )
            self.assertEqual(combined["calculationAssociation"]["state"], "current")
            self.assertTrue(combined["savedCalculation"]["accounts"])
            self.assertEqual(combined["savedCalculation"]["accounts"][0]["reason"], "qualified")
            updated = _review(log, registry)
            correct_f1098_statement_review_answer(
                log, registry, updated, question="paid-the-interest", answer="paid-by-others-or-partial",
                submission_id="demo.f1098.live-partial", evidence_id="demo.f1098.live-partial.evidence",
                actor=USER, at="2026-10-15T12:30:00Z",
            )
            changed_contents = log.read()
            stale_association = associate_saved_run(presentation, records, changed_contents.revision)
            self.assertEqual(stale_association["state"], "recalculation-needed")
            self.assertEqual(stale_association["runRevision"], first_contents.revision)
            self.assertEqual(stale_association["currentRevision"], changed_contents.revision)
            # The saved artifact remains reviewable as the historical run; it is not
            # silently relabeled as a calculation of the corrected source.
            presentation_after_correction = json.loads(result.presentation_path.read_text("utf-8"))
            self.assertEqual(result.presentation_path.read_bytes(), saved_presentation_bytes)
            self.assertEqual(presentation_after_correction["runId"], presentation["runId"])
            partial = run("demo.f1098.track4.run2")
            partial_presentation = json.loads(partial.presentation_path.read_text("utf-8"))
            self.assertFalse(any(pub.finding.get("symbol") == "tax.us.2025.schedule-a.line8a"
                                 for pub in partial.publications))
            partial_review = review_f1098_statement_with_saved_presentation(
                log, registry, partial.presentation_path, records, review_id="demo.review.partial",
                shown_at="2026-10-15T12:31:00Z",
            )
            self.assertEqual(partial_review["questions"]["paid-the-interest"]["answer"], "paid-by-others-or-partial")
            self.assertEqual(partial_review["savedCalculationState"], "current-unresolved-explanation")
            self.assertIsNone(partial_review["savedCalculation"])
            self.assertTrue(partial_review["savedUnresolvedExplanation"]["reasons"])
            self.assertEqual(partial_review["savedUnresolvedExplanation"]["statementLabel"], "Synthetic Form 1098")
            updated = _review(log, registry)
            correct_f1098_statement_review_answer(
                log, registry, updated, question="paid-the-interest", answer="yes",
                submission_id="demo.f1098.live-yes-again", evidence_id="demo.f1098.live-yes-again.evidence",
                actor=USER, at="2026-10-15T12:32:00Z",
            )
            final = run("demo.f1098.track4.run3")
            final_presentation = json.loads(final.presentation_path.read_text("utf-8"))
            self.assertEqual(final_presentation["mortgageInterestExplanation"]["accounts"][0]["reason"], "qualified")
            final_review = review_f1098_statement_with_saved_presentation(
                log, registry, final.presentation_path, records, review_id="demo.review.qualified-again",
                shown_at="2026-10-15T12:32:30Z",
            )
            self.assertEqual(final_review["savedCalculationState"], "current-explanation")
            self.assertEqual(final_review["savedCalculation"]["accounts"][0]["reason"], "qualified")
            withdrawal_review = _review(log, registry)
            withdraw_f1098_statement_review_answers(
                log, registry, withdrawal_review, questions=["paid-the-interest"],
                submission_id="demo.f1098.live-payment-withdrawal", actor=USER,
                at="2026-10-15T12:33:00Z",
            )
            withdrawn_run = run("demo.f1098.track4.payment-withdrawn")
            withdrawn_presentation = json.loads(withdrawn_run.presentation_path.read_text("utf-8"))
            self.assertNotIn("mortgageInterestExplanation", withdrawn_presentation)
            self.assertFalse(any(pub.finding.get("symbol") == "tax.us.2025.schedule-a.line8a"
                                 for pub in withdrawn_run.publications))
            withdrawn_report = json.loads(withdrawn_run.output_path.read_text("utf-8"))
            line8a_disposition = next(row for row in withdrawn_report["dispositions"]
                                      if row["artifact_id"] == "tax.us.2025.rule.f1098-line8a")
            self.assertEqual(line8a_disposition["disposition"], "blocked")
            current = _review(log, registry)
            answer_f1098_statement_review_question(
                log, registry, current, question="paid-the-interest", answer="yes",
                submission_id="demo.f1098.live-payment-reanswer", evidence_id="demo.f1098.live-payment-reanswer.evidence",
                actor=USER, at="2026-10-15T12:34:00Z",
            )
            reanswered_run = run("demo.f1098.track4.payment-reanswered")
            reanswered_presentation = json.loads(reanswered_run.presentation_path.read_text("utf-8"))
            self.assertEqual(reanswered_presentation["mortgageInterestExplanation"]["accounts"][0]["reason"], "qualified")
            association = review_f1098_statement_with_saved_presentation(
                log, registry, result.presentation_path, records, review_id="demo.review.stale",
                shown_at="2026-10-15T12:33:00Z",
            )["calculationAssociation"]
            self.assertEqual(association["state"], "recalculation-needed")
            stale_review = review_f1098_statement_with_saved_presentation(
                log, registry, result.presentation_path, records, review_id="demo.review.stale-result",
                shown_at="2026-10-15T12:34:00Z",
            )
            self.assertIsNone(stale_review["savedCalculation"])
            self.assertEqual(stale_review["savedCalculationState"], "recalculation-needed")

            current = _review(log, registry)
            correct_f1098_statement_review_answer(
                log, registry, current, question="paid-the-interest", answer="no",
                submission_id="demo.f1098.live-no-payment", evidence_id="demo.f1098.live-no-payment.evidence",
                actor=USER, at="2026-10-15T12:35:00Z",
            )
            no_payment = run("demo.f1098.track4.no-payment")
            no_payment_model = json.loads(no_payment.presentation_path.read_text("utf-8"))
            no_payment_account = no_payment_model["mortgageInterestExplanation"]["accounts"][0]
            self.assertEqual(no_payment_account["reason"], "not-paid")
            self.assertEqual(no_payment_account["reportedInterest"]["value"], 20000)
            self.assertEqual(no_payment_account["deductibleAmount"], 0)

            current = _review(log, registry)
            correct_f1098_statement_review_answer(
                log, registry, current, question="paid-the-interest", answer="yes",
                submission_id="demo.f1098.live-payment-restore", evidence_id="demo.f1098.live-payment-restore.evidence",
                actor=USER, at="2026-10-15T12:36:00Z",
            )
            current = _review(log, registry)
            correct_f1098_statement_review_answer(
                log, registry, current, question="home-is-collateral", answer="no",
                submission_id="demo.f1098.live-not-collateral", evidence_id="demo.f1098.live-not-collateral.evidence",
                actor=USER, at="2026-10-15T12:37:00Z",
            )
            no_collateral = run("demo.f1098.track4.no-collateral")
            no_collateral_model = json.loads(no_collateral.presentation_path.read_text("utf-8"))
            no_collateral_account = no_collateral_model["mortgageInterestExplanation"]["accounts"][0]
            self.assertEqual(no_collateral_account["reason"], "not-collateral")
            self.assertEqual(no_collateral_account["reportedInterest"]["value"], 20000)
            self.assertEqual(no_collateral_account["deductibleAmount"], 0)
            mortgage_additions = log.read().acts[seed_revision:]
            self.assertFalse(any(
                str(row.get("payload", {}).get("finding", {}).get("fact_id", "")).startswith("tax.us.2025.f1098e.")
                for row in mortgage_additions
            ), "mortgage answer operations must not introduce student-loan findings")
            final_state = project(log.read().acts, registry)
            final_lattice = facts_of(final_state.fact_state, include_displaced=True)
            self.assertEqual(sorted(
                (fid, row["fact_id"], row["value"])
                for fid, row in final_state.findings.items()
                if row["fact_id"] in final_lattice
                and final_lattice[row["fact_id"]].fact_type_id == F1098E_CLOSURE_TYPE
            ), closed_empty_history)
