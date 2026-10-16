"""Production-shaped regression evidence for mortgage explanation successors.

Every case in this module begins with the durable ordinary-answer recorder and
uses the adopted package through the live coordinator. Completed and unresolved
views are reloaded from the saved presentation JSON.
"""
from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.presentation_projection import PresentationModelError, _mortgage_basis_answers
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.f1098_statement_review import (
    F1098ReviewRefused,
    answer_f1098_statement_review_question,
    correct_f1098_statement_review_answer,
    prepare_f1098_statement_review,
    review_f1098_statement_with_saved_presentation,
    save_f1098_statement_review,
)
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry
from tests.test_f1098_statement_review import (  # type: ignore[attr-defined]
    BASE_ANSWERS,
    CONTENT,
    RELEASE_DIR,
    ROOT,
    SCOPE,
    USER,
    _base_acts,
    _evidence_ids,
)
from tests.test_f1098_circumstances_calculation import USER as RUN_USER  # type: ignore[attr-defined]


PACKAGE_PATH = CONTENT / "package.core-calculations.v45.json"
REGISTRY_PATH = CONTENT / "published-packages.v43.json"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v43.json"
REASON_SYMBOL = "tax.us.2025.f1098.residence-interest-reason"
AMOUNT_SYMBOL = "tax.us.2025.schedule-a.line8a"
REASON_RULE = "tax.us.2025.rule.f1098-residence-interest-reason"
AMOUNT_RULE = "tax.us.2025.rule.f1098-line8a"
UNRESOLVED_RULE = "tax.us.2025.rule.f1098-residence-interest-unresolved"
UNRESOLVED_FIELD = "tax.us.2025.form.f1098.residence-interest-unresolved"
FACT_PREFIX = "tax.us.2025.f1098."
ACTOR = USER

V2_ANSWERS = {
    "filing-unit-owns-home": "yes",
    "shared-main-home": "yes",
    "home-is-collateral": "yes",
    "owes-the-loan": "yes",
    "paid-the-interest": "yes",
    "no-one-else-owes-it": "yes",
    "what-the-money-paid-for": "bought-the-home",
    "this-is-the-original-loan": "yes",
    "mortgage-credit-certificate-received": "not-received",
}


def _read(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _v45_seed(*, filing_status: str | None = None, box2: float = 200000.0,
              box9: float = 1.0, box3: str = "2020-06-01",
              omit_box9: bool = False) -> list[dict[str, Any]]:
    """Use the established native closed-empty SLI return, pinned to v45/v43."""
    acts = _base_acts(filing_status=filing_status)
    if omit_box9:
        acts = [row for row in acts if not (
            row.get("kind") == "assertion"
            and isinstance(row.get("payload"), dict)
            and isinstance(row["payload"].get("finding"), dict)
            and str(row["payload"]["finding"].get("fact_id", "")).startswith(FACT_PREFIX + "box9-number-of-properties|")
        )]
    for row in acts:
        payload = row.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        fact_id = finding.get("fact_id") if isinstance(finding, dict) else None
        if isinstance(finding, dict) and isinstance(fact_id, str):
            if fact_id.startswith(FACT_PREFIX + "box2-outstanding-principal|"):
                finding["value"] = box2
            elif fact_id.startswith(FACT_PREFIX + "box9-number-of-properties|"):
                finding["value"] = box9
            elif fact_id.startswith(FACT_PREFIX + "box3-origination-date|"):
                finding["value"] = box3
        if row.get("kind") == "package-adoption":
            package = _read(PACKAGE_PATH)
            release = _read(RELEASE_PATH)
            payload = cast(dict[str, Any], payload)
            payload["package"] = {"id": package["id"], "version": package["version"],
                                  "checksum": package["package_checksum"]}
            payload["release"] = {"id": release["id"], "version": release["version"],
                                  "checksum": hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest()}
            payload["audit"] = {"note": "synthetic production-review successor regression"}
    for index, row in enumerate(acts):
        row["committed_against"] = index
        row["act_id"] = f"demo.f1098.production-repair.seed.{index:04d}"
        if row.get("kind") == "package-adoption":
            cast(dict[str, Any], row["payload"])["revision"] = index
    return acts


def _new_account(root: Path, *, answers: dict[str, str] | None = None,
                 filing_status: str | None = None, box2: float = 200000.0,
                 box9: float = 1.0, box3: str = "2020-06-01",
                 omit_box9: bool = False) -> tuple[Any, ActLog, dict[str, Any]]:
    registry = tax_registry()
    log = ActLog(root / "workspace", registry)
    log.append_batch(_v45_seed(filing_status=filing_status, box2=box2, box9=box9, box3=box3,
                               omit_box9=omit_box9), expected_revision=0)
    review = prepare_f1098_statement_review(
        log, registry, review_id="demo.f1098.production-repair.preview.v2",
        shown_at="2026-10-15T12:00:00Z", bundle_version="v2",
    )
    if review.get("bundleVersion") != "v2":
        raise AssertionError(f"v2 selection was not retained in the review snapshot: {review!r}")
    questions = review["questions"]
    if "filing-unit-owns-home" not in questions or "shared-main-home" not in questions:
        raise AssertionError("v2 preview did not offer the broader filing-unit questions")
    submitted = dict(V2_ANSWERS)
    submitted.update(answers or {})
    save_f1098_statement_review(
        log, registry, review, answers=submitted,
        submission_id="demo.f1098.production-repair.initial-v2",
        evidence_ids=_evidence_ids(submitted, "demo.f1098.production-repair.evidence"),
        actor=ACTOR, at="2026-10-15T12:01:00Z", bundle_version="v2",
    )
    return registry, log, review


def _run_and_reload(root: Path, registry: Any, log: ActLog, name: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Any]:
    capability = WorkspaceCapability(root / "workspace")
    contents = log.read()
    outcome = live_coordinate_run(
        capability, repo_root=ROOT, authoritative_acts=contents.acts,
        workspace_revision=contents.revision, run_scope=SCOPE, scope_user=RUN_USER,
        request={"schema": "run-request.v1"}, run_id=f"demo.f1098.production-repair.{name}",
        governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT),
        output_name=f"{name}.json",
    )
    if outcome.refusal is not None:
        raise AssertionError(f"adopted v45 run refused: {outcome.refusal!r}")
    if outcome.output_path is None or outcome.presentation_path is None:
        raise AssertionError("coordinator did not save output and presentation")
    report = _read(outcome.output_path)
    presentation = _read(outcome.presentation_path)
    records = RecordStream(capability.location / "records", DerivationSchemas())
    saved = review_f1098_statement_with_saved_presentation(
        log, registry, outcome.presentation_path, records,
        review_id=f"demo.f1098.production-repair.saved.{name}",
        shown_at="2026-10-15T12:02:00Z",
    )
    return report, presentation, saved, outcome


def _dispositions(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report.get("dispositions", [])}


def _publication_value(outcome: Any, symbol: str) -> Any:
    rows = [row.finding.get("value") for row in outcome.publications or ()
            if row.finding.get("symbol") == symbol or str(row.finding.get("symbol", "")).startswith(symbol + "|")]
    return rows[0] if rows else None


class F1098ProductionReviewRepairTests(unittest.TestCase):
    def test_v2_timing_defaults_remain_structural_and_cannot_be_submitted(self) -> None:
        bundle = _read(CONTENT / "f1098-circumstances.bundle.v2.json")
        timing_ids = (
            FACT_PREFIX + "loan-timing-relative-to-purchase",
            FACT_PREFIX + "loan-timing-relative-to-building-or-improving",
        )
        fact_types = {row["id"]: row for row in bundle["fact_types"]}
        for fact_id in timing_ids:
            with self.subTest(fact_id=fact_id):
                fact_type = fact_types[fact_id]
                values = fact_type["value_schema"]["enum"]
                self.assertIn("not-asked", values)
                self.assertIn("not-asked", [row["const"] for row in fact_type["value_schema"]["oneOf"]])
                self.assertTrue(fact_type.get("optional_default"))

        with TemporaryDirectory(prefix="f1098-repair-structural-default-") as directory:
            root = Path(directory)
            registry, log, _ = _new_account(
                root, answers={"what-the-money-paid-for": "unrelated-personal-expense"},
            )
            review = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.not-asked-preview",
                shown_at="2026-10-15T12:02:00Z", bundle_version="v2",
            )
            self.assertTrue(review["timingRelevant"])
            self.assertTrue(all(review["questions"][question]["relevance"] == "relevant"
                                for question in ("loan-timing-relative-to-purchase",
                                                 "loan-timing-relative-to-building-or-improving")))
            self.assertTrue(all("not-asked" not in review["questions"][question]["labels"]
                                for question in ("loan-timing-relative-to-purchase",
                                                 "loan-timing-relative-to-building-or-improving")))
            before = log.path.read_bytes()
            for timing_question in (
                "loan-timing-relative-to-purchase",
                "loan-timing-relative-to-building-or-improving",
            ):
                with self.subTest(question=timing_question), self.assertRaisesRegex(
                    F1098ReviewRefused, f"not an offered value for {timing_question}"
                ):
                    answer_f1098_statement_review_question(
                        log, registry, review, question=timing_question, answer="not-asked",
                        submission_id="demo.f1098.production-repair.not-asked",
                        evidence_id="demo.f1098.production-repair.not-asked.evidence",
                        actor=ACTOR, at="2026-10-15T12:01:00Z",
                    )
                self.assertEqual(log.path.read_bytes(), before)

            answered = answer_f1098_statement_review_question(
                log, registry, review, question="loan-timing-relative-to-purchase", answer="no",
                submission_id="demo.f1098.production-repair.timing-offered",
                evidence_id="demo.f1098.production-repair.timing-offered.evidence",
                actor=ACTOR, at="2026-10-15T12:03:00Z",
            )
            self.assertEqual(len(answered["finding_ids"]), 1)
            refreshed = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.timing-refreshed",
                shown_at="2026-10-15T12:04:00Z", bundle_version="v2",
            )
            self.assertEqual(refreshed["questions"]["loan-timing-relative-to-purchase"]["answer"], "no")

    def test_v2_recorder_uncertainty_correction_and_saved_statement_reasons(self) -> None:
        cases = (
            ("liability", "owes-the-loan", "cannot-tell-liability", None),
            ("certificate", "mortgage-credit-certificate-received", "cannot-tell-certificate", None),
            ("original-loan-purchase", "this-is-the-original-loan", "cannot-tell-original-loan", "bought-the-home"),
            ("original-loan-personal-expense", "this-is-the-original-loan", "cannot-tell-original-loan",
             "unrelated-personal-expense"),
        )
        for case_name, question, expected_reason, use in cases:
            with self.subTest(case=case_name), TemporaryDirectory(prefix="f1098-repair-uncertain-") as directory:
                root = Path(directory)
                answers = {question: "cannot-tell"}
                if use is not None:
                    answers["what-the-money-paid-for"] = use
                if use == "unrelated-personal-expense":
                    answers.update({
                        "loan-timing-relative-to-purchase": "no",
                        "loan-timing-relative-to-building-or-improving": "no",
                    })
                registry, log, _ = _new_account(root, answers=answers)
                report, presentation, saved, outcome = _run_and_reload(root, registry, log, case_name)
                rows = _dispositions(report)
                self.assertEqual(_publication_value(outcome, REASON_SYMBOL), expected_reason)
                self.assertEqual(rows[AMOUNT_RULE]["disposition"], "blocked")
                self.assertEqual(rows[UNRESOLVED_RULE]["disposition"], "blocked")
                self.assertEqual(rows[UNRESOLVED_RULE]["code"], "DEPENDENCY_ABSENT")
                reason_field = next(row for row in presentation["sections"]
                                    if row["field"].get("id") == UNRESOLVED_FIELD)
                rendered = json.dumps(reason_field["resolved"].get("reasons", []), sort_keys=True)
                self.assertIn("Synthetic lender", rendered)
                expected_condition = {
                    "owes-the-loan": "owe this loan",
                    "mortgage-credit-certificate-received": "certificate was received",
                    "this-is-the-original-loan": "original loan or a refinance",
                }[question]
                self.assertIn(expected_condition, rendered)
                self.assertEqual(saved["calculationAssociation"]["state"], "current")
                self.assertEqual(saved["savedCalculationState"], "current-unresolved-explanation")
                self.assertEqual(saved["savedUnresolvedExplanation"]["reasons"], reason_field["resolved"]["reasons"])

        with TemporaryDirectory(prefix="f1098-repair-unknown-correction-") as directory:
            root = Path(directory)
            registry, log, _ = _new_account(root, answers={"owes-the-loan": "cannot-tell"})
            before = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.correction.before",
                shown_at="2026-10-15T12:03:00Z", bundle_version="v2",
            )
            previous_id = before["questions"]["owes-the-loan"]["finding_id"]
            correct_f1098_statement_review_answer(
                log, registry, before, question="owes-the-loan", answer="yes",
                submission_id="demo.f1098.production-repair.correction.liability",
                evidence_id="demo.f1098.production-repair.evidence.liability-corrected",
                actor=ACTOR, at="2026-10-15T12:04:00Z",
            )
            corrected = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.correction.after",
                shown_at="2026-10-15T12:04:30Z", bundle_version="v2",
            )
            replacement_id = corrected["questions"]["owes-the-loan"]["finding_id"]
            self.assertNotEqual(replacement_id, previous_id)
            report, presentation, saved, outcome = _run_and_reload(root, registry, log, "liability-corrected")
            rows = _dispositions(report)
            self.assertEqual(_publication_value(outcome, REASON_SYMBOL), "qualified")
            self.assertEqual(rows[AMOUNT_RULE]["disposition"], "published")
            reason = next(pub.finding for pub in outcome.publications or ()
                          if str(pub.finding.get("symbol", "")).startswith(REASON_SYMBOL + "|"))
            current_pin_ids = {pin["id"] for pin in reason.get("pins", []) if pin.get("role") == "input"}
            self.assertNotIn(previous_id, current_pin_ids)
            self.assertIn(replacement_id, current_pin_ids)
            self.assertEqual(saved["calculationAssociation"]["state"], "current")
            answer = next(item for item in presentation["mortgageInterestExplanation"]["accounts"][0]["personAnswers"]
                          if item["factType"] == FACT_PREFIX + "owes-the-loan")
            self.assertEqual(answer["response"], "yes")
            self.assertIn("joint-filing spouse", answer["responseLabel"].lower())

    def test_named_outside_cases_and_three_justified_zeros_keep_their_dispositions(self) -> None:
        unsupported: tuple[tuple[str, dict[str, str], float, str], ...] = (
            ("refinance", {"this-is-the-original-loan": "no"}, 1.0, "refinance"),
            ("multiple-properties", {}, 2.0, "property-count-outside-coverage"),
            ("other-use", {"what-the-money-paid-for": "other"}, 1.0, "other-use-outside-coverage"),
            ("filing-unit-not-owner", {"filing-unit-owns-home": "no"}, 1.0, "non-owner-outside-coverage"),
            ("not-shared-main-home", {"shared-main-home": "no"}, 1.0, "non-main-home-outside-coverage"),
            ("outside-co-obligor", {"no-one-else-owes-it": "no"}, 1.0, "outside-co-obligor"),
        )
        for name, answers, box9, reason in unsupported:
            with self.subTest(name=name), TemporaryDirectory(prefix="f1098-repair-limit-") as directory:
                root = Path(directory)
                registry, log, _ = _new_account(root, answers=answers, box9=box9)
                report, presentation, saved, outcome = _run_and_reload(root, registry, log, name)
                rows = _dispositions(report)
                self.assertEqual(_publication_value(outcome, REASON_SYMBOL), reason)
                self.assertEqual(rows[AMOUNT_RULE]["disposition"], "blocked")
                self.assertIsNone(_publication_value(outcome, AMOUNT_SYMBOL))
                reason_field = next(row for row in presentation["sections"]
                                    if row["field"].get("id") == UNRESOLVED_FIELD)
                reasons = reason_field["resolved"].get("reasons", [])
                encoded = json.dumps(reasons, sort_keys=True)
                descriptions = [(row.get("factId"), row.get("message", row.get("text", "")))
                                for row in reasons if isinstance(row, dict)]
                self.assertTrue(descriptions)
                self.assertEqual(_publication_value(outcome, REASON_SYMBOL), reason)
                self.assertIn({"refinance": "refinance", "multiple-properties": "property count other than one",
                               "other-use": "another use", "filing-unit-not-owner": "you do not own the home",
                               "not-shared-main-home": "not the main home shared by the filing unit",
                               "outside-co-obligor": "someone outside the joint-filing spouses"}[name],
                              encoded.lower())
                self.assertEqual(saved["calculationAssociation"]["state"], "current")

        zeros = (
            ("collateral-zero", {"home-is-collateral": "no"}, 1.0, "not-collateral"),
            ("no-payment-zero", {"paid-the-interest": "no"}, 1.0, "not-paid"),
            ("personal-expense-zero", {
                "what-the-money-paid-for": "unrelated-personal-expense",
                "loan-timing-relative-to-purchase": "no",
                "loan-timing-relative-to-building-or-improving": "no",
            }, 1.0, "use-unrelated-personal-expense"),
        )
        for name, answers, box9, reason in zeros:
            with self.subTest(name=name), TemporaryDirectory(prefix="f1098-repair-zero-") as directory:
                root = Path(directory)
                registry, log, _ = _new_account(root, answers=answers, box9=box9)
                report, presentation, saved, outcome = _run_and_reload(root, registry, log, name)
                rows = _dispositions(report)
                account = presentation["mortgageInterestExplanation"]["accounts"][0]
                self.assertEqual(_publication_value(outcome, REASON_SYMBOL), reason)
                self.assertEqual(rows[AMOUNT_RULE]["disposition"], "published")
                self.assertEqual(float(_publication_value(outcome, AMOUNT_SYMBOL)), 0.0)
                self.assertEqual(account["deductibleAmount"], 0)
                self.assertEqual(account["reason"], reason)
                self.assertNotIn("basis", account)
                self.assertEqual(saved["calculationAssociation"]["state"], "current")
                if name == "personal-expense-zero":
                    self.assertIn("original loan", account["description"].lower())
                    self.assertIn("one property", account["description"].lower())
                    self.assertIn("october 13, 1987", account["description"].lower())
                    self.assertIn("refinanc", account["description"].lower())
                    self.assertIn("both timing exceptions", account["description"].lower())
                    self.assertIn("does not verify continuous security", account["description"].lower())
                elif name == "collateral-zero":
                    self.assertIn("not collateral", account["description"].lower())
                    self.assertNotIn("acquisition", account["description"].lower())
                else:
                    self.assertIn("neither spouse paid", account["description"].lower())
                    self.assertNotIn("1987-10-13", account["description"])

        # New uncertainty reasons must not outrank a decisive zero or the
        # selected personal-expense zero. This is an explicit preservation of
        # the condition table's precedence, not a tax conclusion added here.
        precedence = (
            ("liability-unknown-beside-personal-zero", {
                "owes-the-loan": "cannot-tell",
                "what-the-money-paid-for": "unrelated-personal-expense",
                "loan-timing-relative-to-purchase": "no",
                "loan-timing-relative-to-building-or-improving": "no",
            }, "use-unrelated-personal-expense"),
            ("liability-unknown-beside-collateral-zero", {
                "owes-the-loan": "cannot-tell", "home-is-collateral": "no",
            }, "not-collateral"),
            ("certificate-unknown-beside-no-payment-zero", {
                "mortgage-credit-certificate-received": "cannot-tell", "paid-the-interest": "no",
            }, "not-paid"),
        )
        for name, answers, reason in precedence:
            with self.subTest(name=name), TemporaryDirectory(prefix="f1098-repair-precedence-") as directory:
                root = Path(directory)
                registry, log, _ = _new_account(root, answers=answers)
                report, presentation, saved, outcome = _run_and_reload(root, registry, log, name)
                self.assertEqual(_publication_value(outcome, REASON_SYMBOL), reason)
                self.assertEqual(float(_publication_value(outcome, AMOUNT_SYMBOL)), 0.0)
                self.assertEqual(_dispositions(report)[AMOUNT_RULE]["disposition"], "published")
                self.assertEqual(presentation["mortgageInterestExplanation"]["accounts"][0]["reason"], reason)
                self.assertEqual(saved["savedCalculationState"], "current-explanation")

    def test_v2_labels_defaults_joint_return_debt_limit_and_append_only_registry(self) -> None:
        with TemporaryDirectory(prefix="f1098-repair-joint-labels-") as directory:
            root = Path(directory)
            registry, log, preview = _new_account(
                root, filing_status="married_filing_jointly", omit_box9=True,
            )
            self.assertIn("either spouse", preview["questions"]["filing-unit-owns-home"]["help"].lower())
            self.assertIn("main home shared", preview["questions"]["shared-main-home"]["question"].lower())
            report, presentation, saved, outcome = _run_and_reload(root, registry, log, "joint-qualified")
            account = presentation["mortgageInterestExplanation"]["accounts"][0]
            by_fact = {row["factType"]: row for row in account["personAnswers"]}
            owner = by_fact[FACT_PREFIX + "filing-unit-owns-home"]
            self.assertEqual(owner["response"], "yes")
            self.assertIn("spouse", owner["responseLabel"].lower())
            self.assertIn("if we file jointly", owner["responseLabel"].lower())
            self.assertNotIn(FACT_PREFIX + "owns-the-home", by_fact)
            self.assertNotIn(FACT_PREFIX + "lives-there-most-of-the-time", by_fact)
            self.assertIn("either spouse", preview["questions"]["filing-unit-owns-home"]["help"].lower())
            self.assertEqual(by_fact[FACT_PREFIX + "shared-main-home"]["response"], "yes")
            self.assertIn("filing unit", by_fact[FACT_PREFIX + "shared-main-home"]["responseLabel"].lower())
            self.assertEqual(by_fact[FACT_PREFIX + "paid-the-interest"]["response"], "yes")
            self.assertIn("My filing unit", by_fact[FACT_PREFIX + "paid-the-interest"]["responseLabel"])
            self.assertEqual(by_fact[FACT_PREFIX + "no-one-else-owes-it"]["response"], "yes")
            sole_obligor_label = by_fact[FACT_PREFIX + "no-one-else-owes-it"]["responseLabel"].lower()
            self.assertIn("joint-filing spouse", sole_obligor_label)
            self.assertIn("owes this loan", sole_obligor_label)
            self.assertTrue(any(row["factType"] == FACT_PREFIX + "box9-number-of-properties"
                                for row in account["declaredDefaults"]))
            self.assertFalse(any(row["factType"] == FACT_PREFIX + "box9-number-of-properties"
                                 for row in account["personAnswers"]))
            self.assertTrue(all(row["origin"]["kind"] == "recorded" for row in account["personAnswers"]))
            self.assertEqual(saved["savedCalculationState"], "current-explanation")
            self.assertEqual(_dispositions(report)[AMOUNT_RULE]["disposition"], "published")
            basis_said = json.dumps(account.get("basis", {}).get("said", []), sort_keys=True).lower()
            self.assertIn("filing unit", basis_said)
            self.assertIn("shared", basis_said)
            self.assertNotIn("you own and live", basis_said)
            status_finding = next(row["payload"]["finding"] for row in log.read().acts
                                  if row.get("kind") == "assertion" and isinstance(row.get("payload"), dict)
                                  and isinstance(row["payload"].get("finding"), dict)
                                  and row["payload"]["finding"].get("fact_id") == "tax.us.2025.filing-status|tax-year=2025")
            self.assertEqual(status_finding["value"], "married_filing_jointly")

        with TemporaryDirectory(prefix="f1098-repair-over-limit-") as directory:
            root = Path(directory)
            registry, log, _ = _new_account(root, box2=800000.0)
            report, presentation, saved, outcome = _run_and_reload(root, registry, log, "over-limit")
            self.assertEqual(_publication_value(outcome, REASON_SYMBOL), "debt-limit-over")
            field = next(row for row in presentation["sections"]
                         if row["field"].get("id") == UNRESOLVED_FIELD)
            text = json.dumps(field["resolved"].get("reasons", []), sort_keys=True).lower()
            self.assertIn("older debt", text)
            self.assertEqual(_dispositions(report)[AMOUNT_RULE]["disposition"], "blocked")
            self.assertEqual(saved["calculationAssociation"]["state"], "current")

        package = _read(PACKAGE_PATH)
        release = _read(RELEASE_PATH)
        manifest = _read(REGISTRY_PATH)
        prior_manifest = _read(CONTENT / "published-packages.v42.json")
        self.assertEqual(package["version"], "v45")
        self.assertEqual(package["package_checksum"], package_instance_checksum(package))
        self.assertEqual(release["version"], "v43")
        self.assertEqual(manifest["packages"][:len(prior_manifest["packages"])], prior_manifest["packages"])
        self.assertEqual(manifest["citizens"][:len(prior_manifest["citizens"])], prior_manifest["citizens"])
        self.assertIn({"id": package["id"], "version": package["version"],
                       "checksum": package["package_checksum"]}, manifest["packages"])
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(REGISTRY_PATH.read_bytes()).hexdigest())
        prior_package = _read(CONTENT / "package.core-calculations.v44.json")
        self.assertEqual(prior_package["package_checksum"], package_instance_checksum(prior_package))
        for filename in (
            "f1098-circumstances.bundle.v2.json", "rule.f1098-line8a.v2.json",
            "rule.f1098-residence-interest-reason.v2.json", "rule.f1098-residence-interest-unresolved.v2.json",
        ):
            citizen = _read(CONTENT / filename)
            key = (citizen["id"], citizen["version"])
            registry_row = next(row for row in manifest["citizens"]
                                if (row["id"], row["version"]) == key)
            package_row = next(row for row in package["members"]
                               if (row["id"], row["version"]) == key)
            self.assertEqual(registry_row["checksum"], citizen_checksum(citizen))
            self.assertEqual(package_row["schema"], citizen["schema"])
            self.assertEqual(package_row["role"],
                             "fact-type-bundle" if citizen["schema"] == "bundle.v2" else "computation")

    def test_personal_v1_tokens_do_not_satisfy_v2_and_v44_remains_available(self) -> None:
        # A v1-only ordinary account is deliberately run against the v45 package.
        # The two new filing-unit inputs must remain absent, not inferred from
        # similarly shaped personal yes/no answers.
        with TemporaryDirectory(prefix="f1098-repair-v1-blocked-") as directory:
            root = Path(directory)
            registry = tax_registry()
            log = ActLog(root / "workspace", registry)
            log.append_batch(_v45_seed(), expected_revision=0)
            preview = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.v1-preview",
                shown_at="2026-10-15T12:05:00Z", bundle_version="v1",
            )
            self.assertIn("owns-the-home", preview["questions"])
            self.assertNotIn("filing-unit-owns-home", preview["questions"])
            self.assertNotIn("shared-main-home", preview["questions"])
            save_f1098_statement_review(
                log, registry, preview, answers=BASE_ANSWERS,
                submission_id="demo.f1098.production-repair.legacy-v1-answers",
                evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.f1098.production-repair.v1-evidence"),
                actor=ACTOR, at="2026-10-15T12:06:00Z", bundle_version="v1",
            )
            report, presentation, saved, outcome = _run_and_reload(root, registry, log, "v1-only-v45")
            line8a = _dispositions(report)[AMOUNT_RULE]
            self.assertEqual(line8a["disposition"], "blocked")
            missing = line8a.get("missing", [])
            self.assertTrue(any(str(item) == FACT_PREFIX + "filing-unit-owns-home" for item in missing),
                            f"expected filing-unit ownership input missing, got {line8a!r}")
            self.assertTrue(any(str(item) == FACT_PREFIX + "shared-main-home" for item in missing),
                            f"expected shared-main-home input missing, got {line8a!r}")
            state = saved["questions"]
            self.assertEqual(state["owns-the-home"]["answer"], "yes")
            self.assertEqual(state["lives-there-most-of-the-time"]["answer"], "yes")

        # Historical v44 remains runnable with its explicitly selected v1
        # account and its own publication registry/release.
        with TemporaryDirectory(prefix="f1098-repair-v44-preserved-") as directory:
            root = Path(directory)
            registry = tax_registry()
            log = ActLog(root / "workspace", registry)
            log.append_batch(_base_acts(), expected_revision=0)
            preview = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.v44-preview",
                shown_at="2026-10-15T12:07:00Z", bundle_version="v1",
            )
            save_f1098_statement_review(
                log, registry, preview, answers=BASE_ANSWERS,
                submission_id="demo.f1098.production-repair.v44-v1-answers",
                evidence_ids=_evidence_ids(BASE_ANSWERS, "demo.f1098.production-repair.v44-evidence"),
                actor=ACTOR, at="2026-10-15T12:08:00Z", bundle_version="v1",
            )
            contents = log.read()
            outcome = live_coordinate_run(
                WorkspaceCapability(root / "workspace"), repo_root=ROOT,
                authoritative_acts=contents.acts, workspace_revision=contents.revision,
                run_scope=SCOPE, scope_user=RUN_USER, request={"schema": "run-request.v1"},
                run_id="demo.f1098.production-repair.v44-v1", governance_pins=[],
                surface=PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v42.json", CONTENT),
                output_name="v44.json",
            )
            self.assertIsNone(outcome.refusal, f"historical v44 route refused: {outcome.refusal!r}")
            self.assertIsNotNone(outcome.presentation_path)
            presentation = _read(cast(Path, outcome.presentation_path))
            self.assertEqual(presentation["mortgageInterestExplanation"]["accounts"][0]["reason"], "qualified")

    def test_v2_versioned_answer_metadata_never_falls_back_or_depends_on_resolution_order(self) -> None:
        with TemporaryDirectory(prefix="f1098-repair-versioned-labels-") as directory:
            root = Path(directory)
            registry, log, _ = _new_account(root)
            _, _, _, outcome = _run_and_reload(root, registry, log, "metadata-version-order")
            publications = outcome.publications or ()
            reason_finding = next(pub.finding for pub in publications
                                  if str(pub.finding.get("symbol", "")).startswith(REASON_SYMBOL + "|"))
            publications_by_id = {pub.finding["id"]: pub.finding for pub in publications
                                  if isinstance(pub.finding.get("id"), str)}
            state = project(log.read().acts, registry)
            fact_map = facts_of(state.fact_state)
        v1 = _read(CONTENT / "f1098-circumstances.bundle.json")
        v2 = _read(CONTENT / "f1098-circumstances.bundle.v2.json")
        rule = _read(CONTENT / "rule.f1098-residence-interest-reason.v2.json")
        args = {
            "finding": reason_finding,
            "publications_by_id": publications_by_id, "state": state, "fact_map": fact_map,
            "reason_rule": rule,
        }
        first = _mortgage_basis_answers(resolved_members=[v1, v2], **args)
        reversed_order = _mortgage_basis_answers(resolved_members=[v2, v1], **args)
        self.assertEqual(first, reversed_order)
        answers_by_type = {item["factType"]: item for item in first["personAnswers"]}
        for suffix in ("paid-the-interest", "no-one-else-owes-it"):
            row = answers_by_type[FACT_PREFIX + suffix]
            self.assertEqual(row["response"], "yes")
            self.assertEqual(row["origin"], {"kind": "recorded", "findingId": row["findingId"]})
            definition = next(item for item in v2["fact_types"] if item["id"] == FACT_PREFIX + suffix)
            expected_label = next(item["description"] for item in definition["value_schema"]["oneOf"]
                                  if item["const"] == "yes")
            self.assertEqual(row["responseLabel"], expected_label)
        without_paid_v2 = copy.deepcopy(v2)
        without_paid_v2["fact_types"] = [item for item in v2["fact_types"]
                                           if item["id"] != FACT_PREFIX + "paid-the-interest"]
        with self.assertRaisesRegex(PresentationModelError, r"paid-the-interest@v2 is not uniquely resolved"):
            _mortgage_basis_answers(resolved_members=[v1, without_paid_v2], **args)

    def test_v2_single_answer_adopts_selected_questions_and_conflicting_save_is_atomic(self) -> None:
        with TemporaryDirectory(prefix="f1098-repair-v2-incremental-") as directory:
            root = Path(directory)
            registry = tax_registry()
            log = ActLog(root / "workspace", registry)
            log.append_batch(_v45_seed(), expected_revision=0)
            preview = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.incremental-preview",
                shown_at="2026-10-15T12:09:00Z", bundle_version="v2",
            )
            before = log.read().revision
            with self.assertRaises(F1098ReviewRefused):
                save_f1098_statement_review(
                    log, registry, preview, answers=V2_ANSWERS,
                    submission_id="demo.f1098.production-repair.conflicting-save",
                    evidence_ids=_evidence_ids(V2_ANSWERS, "demo.f1098.production-repair.conflict-evidence"),
                    actor=ACTOR, at="2026-10-15T12:09:30Z", bundle_version="v1",
                )
            self.assertEqual(log.read().revision, before)
            answer_f1098_statement_review_question(
                log, registry, preview, question="filing-unit-owns-home", answer="yes",
                submission_id="demo.f1098.production-repair.incremental-owner",
                evidence_id="demo.f1098.production-repair.incremental-owner.evidence",
                actor=ACTOR, at="2026-10-15T12:10:00Z",
            )
            fresh = prepare_f1098_statement_review(
                log, registry, review_id="demo.f1098.production-repair.incremental-fresh",
                shown_at="2026-10-15T12:10:30Z",
            )
            self.assertEqual(fresh["bundleAdoption"], {"id": "tax.us.2025.f1098-successor.vocabulary", "version": "v2"})
            self.assertEqual(fresh["questions"]["filing-unit-owns-home"]["answer"], "yes")
            self.assertEqual(fresh["questions"]["shared-main-home"]["state"], "absent")
            contents = log.read()
            outcome = live_coordinate_run(
                WorkspaceCapability(root / "workspace"), repo_root=ROOT,
                authoritative_acts=contents.acts, workspace_revision=contents.revision,
                run_scope=SCOPE, scope_user=RUN_USER, request={"schema": "run-request.v1"},
                run_id="demo.f1098.production-repair.incremental-v2", governance_pins=[],
                surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT),
                output_name="incremental-v2.json",
            )
            self.assertIsNone(outcome.refusal)
            self.assertIsNotNone(outcome.output_path)
            dispositions = _dispositions(_read(cast(Path, outcome.output_path)))
            self.assertEqual(dispositions[AMOUNT_RULE]["disposition"], "blocked")
            self.assertIn("shared-main-home", json.dumps(dispositions[AMOUNT_RULE].get("missing", [])))
