"""Admission and scoped vocabulary for connected mortgage calculations."""
from __future__ import annotations

import hashlib
import json
import copy
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

import pytest

from packages.derivation.loader import DerivationSchemas
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.act_log import ActLog
from packages.kernel.facts import fact_id_for
from packages.tax.loader import tax_registry
from packages.tax.mortgage_borrowing_recording import (
    introduce_mortgage_borrowing_reference_durably,
    record_mortgage_borrowing_claim_durably,
)
from packages.tax.f1098_statement_recording import answer_f1098_statement_answer_durably
from tests.test_f1098_mortgage_interest_line12e_track2 import _f1098_acts

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/demo.release.sli-worksheet-integration.2025.v53.json"
RELEASE_DIR = RELEASE.parent
PACKAGE = CONTENT / "package.core-calculations.v55.json"
REGISTRY = CONTENT / "published-packages.v53.json"
BORROWING_REF = "demo.mortgage.borrowing.shared"
LINK_TYPE = "tax.us.2025.f1098.borrowing-inclusion"
ROOT_TYPE = "tax.us.2025.mortgage.continuing-borrowing"
LOCAL_FACTS = {
    "owes-the-loan": "tax.us.2025.f1098.owes-the-loan",
    "no-one-else-owes-it": "tax.us.2025.f1098.no-one-else-owes-it",
    "what-the-money-paid-for": "tax.us.2025.f1098.what-the-money-paid-for",
    "this-is-the-original-loan": "tax.us.2025.f1098.this-is-the-original-loan",
    "mortgage-credit-certificate-received": "tax.us.2025.f1098.mortgage-credit-certificate-received",
}
SHARED_CLAIMS = {
    "owes-the-loan": ("owes-the-loan", "yes"),
    "no-one-else-owes-it": ("no-one-else-owes-it", "no"),
    "what-the-money-paid-for": ("what-the-money-paid-for", "bought-the-home"),
    "this-is-the-original-loan": ("this-is-the-original-loan", "yes"),
    "mortgage-credit-certificate-received": ("mortgage-credit-certificate-received", "not-received"),
}

pytestmark = pytest.mark.live


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, Any]:
    return {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id, "value": value,
            "basis": "attested", "evidence_ids": []}


def _run_connected_case(*, uncertain_shared: str | None = None, unlinked_third_report: bool = False,
                       unconnected_singleton: bool = False, fully_supported_local: bool = False,
                       shared_only: bool = False,
                       shared_before_local: bool = False,
                       shared_overrides: dict[str, str] | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, str], dict[str, str]]:
    """Run the real recorder and coordinator against the successor package."""
    acts = cast(list[dict[str, Any]], _f1098_acts(
        interest=22000.0, second_statement_interest=None if unconnected_singleton else 3500.0))
    if unlinked_third_report:
        previous = next(row for row in acts if row.get("kind") == "member-transition"
                        and row["payload"]["successor"]["id"] == "demo.f1098.h2")
        transition = copy.deepcopy(previous)
        transition["act_id"] = "demo.f1098.third-report-transition"
        transition["payload"]["member"]["finding"] = _attested(
            "demo.f1098.box1.2", fact_id_for("tax.us.2025.f1098.box1-mortgage-interest", (
                ("payer", "demo.f1098.lender.c"), ("statement", "demo.f1098.stmt.c"), ("tax-year", "2025"))), 1900.0)
        transition["payload"]["successor"] = {"id": "demo.f1098.h3", "predecessor": "demo.f1098.h2"}
        closure = next(row for row in acts if row.get("kind") == "assertion"
                       and str(row.get("payload", {}).get("finding", {}).get("fact_id", "")).startswith("tax.us.2025.f1098.source-closure|"))
        closure["payload"]["finding"] = _attested(
            "demo.f1098.closure", "tax.us.2025.f1098.source-closure|family-horizon=demo.f1098.h3,tax-year=2025", True)
        close_index = acts.index(closure)
        acts[close_index:close_index] = [
            {"schema": "act.v1", "act_id": "demo.f1098.third-payer", "kind": "entity-introduced",
             "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:00Z", "committed_against": 0,
             "payload": {"entity": {"schema": "entity.v1", "id": "demo.f1098.lender.c", "kind": "tax.us.mortgage-lender", "label": "Synthetic lender"}}},
            {"schema": "act.v1", "act_id": "demo.f1098.third-statement", "kind": "entity-introduced",
             "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:00Z", "committed_against": 0,
             "payload": {"entity": {"schema": "entity.v1", "id": "demo.f1098.stmt.c", "kind": "tax.us.1098-statement", "label": "Synthetic Form 1098"}}},
            transition,
        ]
        for index, row in enumerate(acts):
            row["committed_against"] = index
    old_adoption = acts.pop()
    acts.append({"schema": "act.v1", "act_id": old_adoption["act_id"],
                 "kind": old_adoption["kind"], "actor": old_adoption["actor"],
                 "at": old_adoption["at"], "committed_against": len(acts),
                 "payload": copy.deepcopy(old_adoption["payload"])})
    adoption = acts[-1]
    package = _load(PACKAGE)
    release_bytes = RELEASE.read_bytes()
    adoption["payload"]["package"] = {
        "id": package["id"], "version": package["version"], "checksum": package["package_checksum"]
    }
    adoption["payload"]["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": "v53", "checksum": hashlib.sha256(release_bytes).hexdigest(),
    }
    adoption["payload"]["revision"] = len(acts) - 1
    report_keys = (
        {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"},
        {"payer": "demo.f1098.lender.b", "statement": "demo.f1098.stmt.b", "tax-year": "2025"},
    )
    local_ids: dict[str, str] = {}
    values = {key: value for key, (_, value) in SHARED_CLAIMS.items()}
    if shared_only:
        values["no-one-else-owes-it"] = "yes"
    if fully_supported_local:
        values["no-one-else-owes-it"] = "yes"
    legacy_local_values = {**values, "no-one-else-owes-it": "yes"}
    with tempfile.TemporaryDirectory(prefix="mortgage-calculation-") as tmp:
        registry = tax_registry()
        log = ActLog(Path(tmp) / "workspace", registry)
        log.append_batch(acts, expected_revision=0)
        if not unconnected_singleton:
            introduce_mortgage_borrowing_reference_durably(
                log, registry, reference_id=BORROWING_REF, description="Synthetic mortgage borrowing",
                actor="demo.user.filer-1", at="2026-10-23T16:01:00Z")

        def record(claim: str, value: Any, statement: dict[str, str] | None = None) -> str:
            result = record_mortgage_borrowing_claim_durably(
                log, registry, claim=claim, borrowing_ref=BORROWING_REF, value=value,
                submission_id=f"demo.mortgage.submission.{log.read().revision}",
                evidence_id=f"demo.mortgage.evidence.{log.read().revision}", actor="demo.user.filer-1",
                at="2026-10-23T16:02:00Z", statement_keys=statement,
                expected_revision=log.read().revision)
            return cast(str, result["finding_id"])

        shared_ids: dict[str, str] = {}

        def record_shared_claims() -> None:
            record("continuing-borrowing", "yes")
            record("annual-ceiling", 250000)
            record("other-secured-home-debt", "no")
            shared_values = dict(values)
            if shared_overrides:
                shared_values.update(shared_overrides)
            for question, (claim, _default_value) in SHARED_CLAIMS.items():
                value = "cannot-tell" if uncertain_shared == question else shared_values[question]
                shared_ids[question] = record(claim, value)
            for report in report_keys:
                record("report-inclusion", "affirmed", report)

        if shared_before_local and not unconnected_singleton:
            record_shared_claims()

        for report_index, keys in enumerate(report_keys[:1] if unconnected_singleton else report_keys):
            for question in LOCAL_FACTS:
                if shared_only:
                    continue
                if (report_index == 0 and uncertain_shared != question and not fully_supported_local
                        and not unconnected_singleton):
                    continue  # A demonstrates shared-only support except in the uncertainty mutation.
                local_value = (legacy_local_values[question] if unconnected_singleton
                               else values[question] if fully_supported_local
                               else "yes" if report_index == 0 else values[question])
                result = answer_f1098_statement_answer_durably(
                    log, registry, statement_keys=keys, question=question, answer=local_value,
                    submission_id=f"demo.mortgage.local.{report_index}.{question}",
                    evidence_id=f"demo.mortgage.local-evidence.{report_index}.{question}",
                    actor="demo.user.filer-1", at="2026-10-23T16:01:30Z",
                    expected_revision=log.read().revision, bundle_version="v2",
                )
                local_ids[f"{report_index}:{question}"] = result["finding_ids"][0]

        if not unconnected_singleton and not fully_supported_local:
            report_indices = (0, 1) if shared_only else (1,)
            for report_index in report_indices:
                for question, value in {
                    "filing-unit-owns-home": "yes", "shared-main-home": "yes",
                    "home-is-collateral": "yes", "paid-the-interest": "yes",
                }.items():
                    result = answer_f1098_statement_answer_durably(
                        log, registry, statement_keys=report_keys[report_index], question=question, answer=value,
                        submission_id=f"demo.mortgage.local.{report_index}.{question}",
                        evidence_id=f"demo.mortgage.local-evidence.{report_index}.{question}",
                        actor="demo.user.filer-1", at="2026-10-23T16:01:35Z",
                        expected_revision=log.read().revision, bundle_version="v2",
                    )
                    local_ids[f"{report_index}:{question}"] = result["finding_ids"][0]

        if fully_supported_local and not unconnected_singleton:
            for report_index, keys in enumerate(report_keys):
                for question in ("filing-unit-owns-home", "shared-main-home", "home-is-collateral", "paid-the-interest"):
                    result = answer_f1098_statement_answer_durably(
                        log, registry, statement_keys=keys, question=question, answer="yes",
                        submission_id=f"demo.mortgage.local.{report_index}.{question}",
                        evidence_id=f"demo.mortgage.local-evidence.{report_index}.{question}",
                        actor="demo.user.filer-1", at="2026-10-23T16:01:35Z",
                        expected_revision=log.read().revision, bundle_version="v2",
                    )
                    local_ids[f"{report_index}:{question}"] = result["finding_ids"][0]

        if unconnected_singleton:
            additional_answers = {
                "filing-unit-owns-home": "yes", "shared-main-home": "yes",
                "home-is-collateral": "yes", "paid-the-interest": "yes",
            }
            for question, value in additional_answers.items():
                result = answer_f1098_statement_answer_durably(
                    log, registry, statement_keys=report_keys[0], question=question, answer=value,
                    submission_id=f"demo.mortgage.singleton.{question}",
                    evidence_id=f"demo.mortgage.singleton.evidence.{question}",
                    actor="demo.user.filer-1", at="2026-10-23T16:01:40Z",
                    expected_revision=log.read().revision, bundle_version="v2",
                )
                local_ids[f"0:{question}"] = result["finding_ids"][0]

        if not shared_before_local and not unconnected_singleton:
            record_shared_claims()

        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "run"), repo_root=ROOT,
            authoritative_acts=list(log.read().acts), workspace_revision=log.read().revision,
            run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
            request={"schema": "run-request.v1"}, run_id=f"demo.mortgage.mapping.{uncertain_shared or 'supported'}",
            governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
            output_name="report.json")
        if outcome.refusal is not None:
            raise AssertionError(outcome.refusal)
        assert outcome.output_path is not None and outcome.presentation_path is not None
        return _load(outcome.output_path), _load(outcome.presentation_path), local_ids, shared_ids


class MortgageBorrowingPackageTests(unittest.TestCase):
    def test_v55_admits_consumer_successors_without_losing_v54_members(self) -> None:
        corpus = {}
        for path in CONTENT.glob("*.json"):
            citizen = _load(path)
            if isinstance(citizen, dict) and isinstance(citizen.get("id"), str) and isinstance(citizen.get("version"), str):
                corpus[(citizen["id"], citizen["version"])] = citizen

        base = _load(CONTENT / "package.core-calculations.v54.json")
        package = _load(CONTENT / "package.core-calculations.v55.json")
        result = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(result.ok, [issue.code for issue in result.issues])
        self.assertEqual(package["input_bindings"], base["input_bindings"])
        members = {(row["id"], row["version"], row["schema"], row["role"]) for row in package["members"]}
        base_members = {(row["id"], row["version"], row["schema"], row["role"]) for row in base["members"]}
        expected_retired = {
            ("tax.us.2025.rule.form1040-line12e", "v1", "rule-artifact.v4", "computation"),
            ("tax.us.2025.rule.attachment.schedule-a", "v1", "attachment-rule.v4", "attachment-rule"),
            ("tax.us.2025.rule.f1098-line8a", "v2", "rule-artifact.v14", "computation"),
            ("tax.us.2025.rule.f1098-residence-interest-reason", "v2", "rule-artifact.v14", "computation"),
        }
        self.assertTrue(expected_retired <= base_members)
        self.assertTrue((base_members - expected_retired) <= members)
        self.assertEqual(len(package["members"]), 623)
        self.assertEqual(len(members - (base_members - expected_retired)), 30)
        self.assertIn(("tax.us.2025.rule.f1098-line8a", "v5", "rule-artifact.v14", "computation"), members)
        self.assertIn(("tax.us.2025.rule.f1098-residence-interest-reason", "v5", "rule-artifact.v14", "computation"), members)
        self.assertIn(("tax.us.2025.rule.form1040-line12e", "v2", "rule-artifact.v4", "computation"), members)
        self.assertIn(("tax.us.2025.rule.attachment.schedule-a", "v2", "attachment-rule.v4", "attachment-rule"), members)
        reason = corpus[("tax.us.2025.rule.f1098-residence-interest-reason", "v5")]
        witness = corpus[("tax.us.2025.rule.effective-proceeds-support-count", "v1")]
        connected_outputs = {
            "tax.us.2025.f1098.effective-owes-the-loan",
            "tax.us.2025.f1098.effective-no-one-else-owes-it",
            "tax.us.2025.f1098.effective-proceeds-use",
            "tax.us.2025.f1098.effective-original-loan",
            "tax.us.2025.f1098.effective-credit-certificate",
        }
        self.assertIn("tax.us.2025.mortgage.report-effective-support-coverage", reason["requires"])
        self.assertFalse(connected_outputs & set(reason["requires"]))
        self.assertTrue(connected_outputs <= set(witness["requires"]))
        member_order = [row["id"] for row in package["members"]]
        reason_position = member_order.index(reason["id"])
        for mapping in (
            "tax.us.2025.rule.owes-the-loan-effective-answer",
            "tax.us.2025.rule.no-one-else-owes-it-effective-answer",
            "tax.us.2025.rule.what-the-money-paid-for-effective-answer",
            "tax.us.2025.rule.this-is-the-original-loan-effective-answer",
            "tax.us.2025.rule.mortgage-credit-certificate-received-effective-answer",
        ):
            self.assertLess(reason_position, member_order.index(mapping))
        resolved_order = [row["id"] for row in result.resolved_members]
        resolved_reason = resolved_order.index(reason["id"])
        resolved_coverage = resolved_order.index("tax.us.2025.rule.report-effective-support-coverage")
        resolved_witness = resolved_order.index(witness["id"])
        self.assertLess(resolved_reason, resolved_coverage)
        self.assertLess(resolved_witness, resolved_coverage)
        for mapping in (
            "tax.us.2025.rule.owes-the-loan-effective-answer",
            "tax.us.2025.rule.no-one-else-owes-it-effective-answer",
            "tax.us.2025.rule.what-the-money-paid-for-effective-answer",
            "tax.us.2025.rule.this-is-the-original-loan-effective-answer",
            "tax.us.2025.rule.mortgage-credit-certificate-received-effective-answer",
        ):
            self.assertLess(resolved_reason, resolved_order.index(mapping))
        line12e = corpus[("tax.us.2025.rule.form1040-line12e", "v2")]
        self.assertIn("tax.us.2025.schedule-a.total", line12e["requires"])
        self.assertIn("tax.us.2025.schedule-a.total", {pin["id"] for pin in line12e["pins"]})
        attachment = corpus[("tax.us.2025.rule.attachment.schedule-a", "v2")]
        required = attachment["completeness"]["required_answers"]
        self.assertEqual(len(required), 7)
        self.assertTrue(all(row["check"] == "value" and row["equals"] == "yes" for row in required))
        self.assertNotIn("tax.us.2025.f1098.liable-and-paid", {row["symbol"] for row in required})

        calculation = corpus[("tax.us.2025.mortgage-borrowing-calculation", "v1")]
        linked = [fact for fact in calculation["fact_types"] if fact["id"].startswith("tax.us.2025.f1098.effective-")]
        self.assertEqual(len(linked), 5)
        expected_keys = ["payer", "statement", "tax-year", "borrowing"]
        self.assertTrue(all([key["name"] for key in fact["identity_keys"]] == expected_keys for fact in linked))

        initial_registry = _load(CONTENT / "published-packages.v51.json")
        previous_registry = _load(CONTENT / "published-packages.v52.json")
        registry = _load(CONTENT / "published-packages.v53.json")
        self.assertTrue(set(map(json.dumps, initial_registry["packages"])) <= set(map(json.dumps, previous_registry["packages"])))
        self.assertTrue(set(map(json.dumps, initial_registry["citizens"])) <= set(map(json.dumps, previous_registry["citizens"])))
        self.assertTrue(set(map(json.dumps, previous_registry["packages"])) <= set(map(json.dumps, registry["packages"])))
        self.assertTrue(set(map(json.dumps, previous_registry["citizens"])) <= set(map(json.dumps, registry["citizens"])))
        entry = next(row for row in registry["packages"] if row["version"] == "v55")
        self.assertEqual(entry["checksum"], package["package_checksum"])
        self.assertEqual(
            _load(RELEASE)["package_registry_sha256"],
            hashlib.sha256((CONTENT / "published-packages.v53.json").read_bytes()).hexdigest(),
        )

    def test_five_effective_mappings_use_exact_real_recorded_links(self) -> None:
        report, model, local_ids, shared_ids = _run_connected_case()
        self.assertEqual(report["authorization_status"], "AUTHORIZATION_ABSENT")
        explanation = model["mortgageBorrowingExplanation"]
        group = explanation["groups"][0]
        report_rows = explanation["reports"]
        self.assertEqual(explanation["runId"], report["run_id"])
        self.assertGreater(explanation["workspaceRevision"], 0)
        self.assertEqual(len(report_rows), 2)
        self.assertEqual([item["reportedInterest"]["value"] for item in report_rows], [22000.0, 3500.0])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["artifact_id"], "tax.us.2025.rule.f1098-line8a")
        self.assertEqual(explanation["line8aFindings"], [])
        local_types = {
            "tax.us.2025.f1098.filing-unit-owns-home", "tax.us.2025.f1098.shared-main-home",
            "tax.us.2025.f1098.home-is-collateral", "tax.us.2025.f1098.paid-the-interest",
        }
        self.assertTrue(local_types <= {answer["factType"] for answer in report_rows[1]["localAnswers"]})
        self.assertIsNone(report_rows[0]["reasonChain"])
        self.assertIsNotNone(report_rows[1]["reasonChain"])
        self.assertTrue(
            {local_ids[f"1:{question}"] for question in LOCAL_FACTS}
            <= {answer["findingId"] for answer in report_rows[1]["localAnswers"]}
        )
        self.assertEqual(group["recordedApplicableClaims"]["tax.us.2025.mortgage.shared-no-one-else-owes-it"]["value"], "no")
        self.assertEqual(group["recordedApplicableClaims"]["tax.us.2025.mortgage.shared-credit-certificate"]["value"], "not-received")
        self.assertEqual(group["recordedApplicableClaims"]["tax.us.2025.f1098.borrowing-year-ceiling"]["value"], 250000)
        self.assertEqual(explanation["line8aDispositions"][0]["artifact_id"], "tax.us.2025.rule.f1098-line8a")
        rows = {row["symbol"]: row for row in report["dispositions"]
                if row.get("symbol", "").startswith("tax.us.2025.f1098.effective-")}
        expected_keys = (
            ("demo.f1098.lender.a", "demo.f1098.stmt.a"),
            ("demo.f1098.lender.b", "demo.f1098.stmt.b"),
        )
        shared_values = {question: value for question, (_, value) in SHARED_CLAIMS.items()}
        for question, effective_type in (
            ("owes-the-loan", "tax.us.2025.f1098.effective-owes-the-loan"),
            ("no-one-else-owes-it", "tax.us.2025.f1098.effective-no-one-else-owes-it"),
            ("what-the-money-paid-for", "tax.us.2025.f1098.effective-proceeds-use"),
            ("this-is-the-original-loan", "tax.us.2025.f1098.effective-original-loan"),
            ("mortgage-credit-certificate-received", "tax.us.2025.f1098.effective-credit-certificate"),
        ):
            for report_index, (payer, statement) in enumerate(expected_keys):
                fact_id = fact_id_for(effective_type, (("payer", payer), ("statement", statement),
                                                       ("tax-year", "2025"), ("borrowing", BORROWING_REF)))
                symbol = f"{effective_type}|tax.us.2025.f1098.borrowing-inclusion|payer={payer},statement={statement},tax-year=2025,borrowing={BORROWING_REF}"
                self.assertIn(symbol, rows, (question, report_index))
                self.assertEqual(rows[symbol]["disposition"], "published")
                pins = {pin.get("id") for pin in rows[symbol].get("pins", []) if isinstance(pin, dict)}
                self.assertIn(shared_ids[question], pins)
                answer = next(item for item in report_rows[report_index]["effectiveAnswers"]
                              if item["factType"] == effective_type)
                self.assertEqual(answer["value"], shared_values[question])
                self.assertIn(shared_ids[question], {pin.get("id") for pin in answer["pins"]})
                if report_index == 1:
                    self.assertIn(local_ids[f"1:{question}"], pins)
                    self.assertIn(local_ids[f"1:{question}"], {pin.get("id") for pin in answer["pins"]})
                else:
                    self.assertNotIn(local_ids.get(f"0:{question}"), pins)

    def test_cannot_tell_shared_claim_withholds_favorable_local_value(self) -> None:
        report, model, local_ids, shared_ids = _run_connected_case(uncertain_shared="no-one-else-owes-it")
        target_type = "tax.us.2025.f1098.effective-no-one-else-owes-it"
        target_id = fact_id_for(target_type, (("payer", "demo.f1098.lender.a"),
            ("statement", "demo.f1098.stmt.a"), ("tax-year", "2025"), ("borrowing", BORROWING_REF)))
        symbol = f"{target_type}|tax.us.2025.f1098.borrowing-inclusion|payer=demo.f1098.lender.a,statement=demo.f1098.stmt.a,tax-year=2025,borrowing={BORROWING_REF}"
        rows = {row["symbol"]: row for row in report["dispositions"] if row.get("symbol")}
        self.assertEqual(rows[symbol]["disposition"], "blocked")
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        group = explanation["groups"][0]
        self.assertEqual(group["recordedApplicableClaims"]["tax.us.2025.mortgage.shared-no-one-else-owes-it"]["value"], "cannot-tell")
        local = next(answer for answer in explanation["reports"][0]["localAnswers"]
                     if answer["factType"] == LOCAL_FACTS["no-one-else-owes-it"])
        self.assertEqual(local["value"], "yes")
        self.assertFalse(any(answer["factType"] == target_type for answer in explanation["reports"][0]["effectiveAnswers"]))
        self.assertTrue(local_ids["0:no-one-else-owes-it"])
        self.assertTrue(shared_ids["no-one-else-owes-it"])

    def test_two_supported_reports_publish_and_save_the_full_line8a_sum(self) -> None:
        report, model, local_ids, _shared_ids = _run_connected_case(fully_supported_local=True)
        explanation = model["mortgageBorrowingExplanation"]
        rows = [row for row in report["dispositions"]
                if row.get("symbol") == "tax.us.2025.schedule-a.line8a"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        line8a = explanation["line8aFindings"][0]
        self.assertEqual(line8a["symbol"], "tax.us.2025.schedule-a.line8a")
        self.assertEqual(line8a["value"], 25500.0)
        self.assertTrue(line8a["id"])
        self.assertTrue(line8a["pins"])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "published")
        self.assertEqual(len(explanation["reports"]), 2)
        box1_finding_ids = {report_row["reportedInterest"]["findingId"] for report_row in explanation["reports"]}
        line8a_pin_ids = {pin.get("id") for pin in line8a["pins"] if isinstance(pin, dict)}
        self.assertTrue(box1_finding_ids <= line8a_pin_ids)
        for index, report_row in enumerate(explanation["reports"]):
            self.assertIsNotNone(report_row["reasonChain"])
            self.assertEqual(report_row["reasonChain"]["value"], "qualified")
            reason_pin_ids = {pin.get("id") for pin in report_row["reasonChain"]["pins"]
                              if isinstance(pin, dict)}
            self.assertIn(report_row["reportedInterest"]["findingId"], reason_pin_ids)
            recorded = {answer["findingId"] for answer in report_row["localAnswers"]}
            self.assertEqual(recorded, {local_ids[f"{index}:{question}"] for question in LOCAL_FACTS} |
                             {local_ids[f"{index}:{question}"] for question in
                              ("filing-unit-owns-home", "shared-main-home", "home-is-collateral", "paid-the-interest")})

    def test_projection_keeps_unlinked_current_report_once(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(unlinked_third_report=True)
        self.assertEqual(report["authorization_status"], "AUTHORIZATION_ABSENT")
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(len(explanation["reports"]), 3)
        third = next(row for row in explanation["reports"] if row["statement"] == "demo.f1098.stmt.c")
        self.assertEqual(third["reportedInterest"]["value"], 1900.0)
        self.assertEqual(third["relationships"], [])
        self.assertEqual(len(explanation["groups"][0]["reportKeys"]), 2)

    def test_shared_only_claims_feed_both_report_reasons_and_full_line8a_sum(self) -> None:
        report, model, local_ids, _shared_ids = _run_connected_case(shared_only=True)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(report["authorization_status"], "AUTHORIZATION_ABSENT")
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        line8a = explanation["line8aFindings"][0]
        self.assertEqual(line8a["value"], 25500.0)
        line8a_pin_ids = {pin.get("id") for pin in line8a["pins"] if isinstance(pin, dict)}
        report_box1_ids = {row["reportedInterest"]["findingId"] for row in explanation["reports"]}
        self.assertTrue(report_box1_ids <= line8a_pin_ids)
        expected_local_types = {
            "tax.us.2025.f1098.filing-unit-owns-home", "tax.us.2025.f1098.shared-main-home",
            "tax.us.2025.f1098.home-is-collateral", "tax.us.2025.f1098.paid-the-interest",
        }
        expected_effective_types = {
            "tax.us.2025.f1098.effective-owes-the-loan",
            "tax.us.2025.f1098.effective-no-one-else-owes-it",
            "tax.us.2025.f1098.effective-proceeds-use",
            "tax.us.2025.f1098.effective-original-loan",
            "tax.us.2025.f1098.effective-credit-certificate",
        }
        for index, report_row in enumerate(explanation["reports"]):
            self.assertIsNotNone(report_row["reasonChain"])
            self.assertEqual(report_row["reasonChain"]["value"], "qualified")
            self.assertEqual({answer["factType"] for answer in report_row["localAnswers"]}, expected_local_types)
            self.assertEqual(
                {answer["findingId"] for answer in report_row["localAnswers"]},
                {local_ids[f"{index}:{question}"] for question in
                 ("filing-unit-owns-home", "shared-main-home", "home-is-collateral", "paid-the-interest")},
            )
            effective = [answer for answer in report_row["effectiveAnswers"]
                         if answer["factType"] in expected_effective_types]
            self.assertEqual({answer["factType"] for answer in effective}, expected_effective_types)
            reason_pin_ids = {pin.get("id") for pin in report_row["reasonChain"]["pins"]
                              if isinstance(pin, dict)}
            self.assertIn(report_row["reportedInterest"]["findingId"], reason_pin_ids)
            self.assertTrue({answer["findingId"] for answer in effective} <= reason_pin_ids)

    def _assert_uncertain_shared_claim_withholds_line8a(self, question: str) -> None:
        report, model, _local_ids, shared_ids = _run_connected_case(
            uncertain_shared=question, fully_supported_local=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        effective_type = {
            "owes-the-loan": "tax.us.2025.f1098.effective-owes-the-loan",
            "no-one-else-owes-it": "tax.us.2025.f1098.effective-no-one-else-owes-it",
            "what-the-money-paid-for": "tax.us.2025.f1098.effective-proceeds-use",
            "this-is-the-original-loan": "tax.us.2025.f1098.effective-original-loan",
            "mortgage-credit-certificate-received": "tax.us.2025.f1098.effective-credit-certificate",
        }[question]
        effective_rows = [row for row in report["dispositions"]
                          if str(row.get("symbol", "")).startswith(f"{effective_type}|")]
        self.assertEqual(len(effective_rows), 2)
        self.assertTrue(all(row["disposition"] == "blocked" for row in effective_rows))
        self.assertTrue(all(not any(answer["factType"] == effective_type
                                    for answer in report_row["effectiveAnswers"])
                            for report_row in explanation["reports"]))
        applicable = explanation["groups"][0]["recordedApplicableClaims"]
        self.assertTrue(any(claim["findingId"] == shared_ids[question] and claim["value"] == "cannot-tell"
                            for claim in applicable.values()))

    def test_uncertain_shared_owes_claim_with_favorable_local_withholds_line8a(self) -> None:
        self._assert_uncertain_shared_claim_withholds_line8a("owes-the-loan")

    def test_uncertain_shared_no_other_obligor_with_favorable_local_withholds_line8a(self) -> None:
        self._assert_uncertain_shared_claim_withholds_line8a("no-one-else-owes-it")

    def test_uncertain_shared_proceeds_with_favorable_local_withholds_line8a(self) -> None:
        self._assert_uncertain_shared_claim_withholds_line8a("what-the-money-paid-for")

    def test_uncertain_shared_original_loan_with_favorable_local_withholds_line8a(self) -> None:
        self._assert_uncertain_shared_claim_withholds_line8a("this-is-the-original-loan")

    def test_uncertain_shared_certificate_with_favorable_local_withholds_line8a(self) -> None:
        self._assert_uncertain_shared_claim_withholds_line8a("mortgage-credit-certificate-received")

    def _assert_contrary_shared_claim_withholds_line8a(self, question: str, value: str) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, shared_overrides={question: value},
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        effective_type = {
            "no-one-else-owes-it": "tax.us.2025.f1098.effective-no-one-else-owes-it",
            "mortgage-credit-certificate-received": "tax.us.2025.f1098.effective-credit-certificate",
        }[question]
        rows = [row for row in report["dispositions"]
                if str(row.get("symbol", "")).startswith(f"{effective_type}|")]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["disposition"] == "blocked" for row in rows))

    def test_shared_no_other_obligor_answer_is_not_favorable(self) -> None:
        self._assert_contrary_shared_claim_withholds_line8a("no-one-else-owes-it", "no")

    def test_shared_received_certificate_answer_is_not_favorable(self) -> None:
        self._assert_contrary_shared_claim_withholds_line8a("mortgage-credit-certificate-received", "received")

    def _assert_disagreement_withholds_line8a(self, *, shared_before_local: bool) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, shared_before_local=shared_before_local,
            shared_overrides={"owes-the-loan": "no"},
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        rows = [row for row in report["dispositions"]
                if str(row.get("symbol", "")).startswith("tax.us.2025.f1098.effective-owes-the-loan|")]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["disposition"] == "blocked" for row in rows))

    def test_disagreeing_local_and_shared_answers_block_local_first(self) -> None:
        self._assert_disagreement_withholds_line8a(shared_before_local=False)

    def test_disagreeing_local_and_shared_answers_block_shared_first(self) -> None:
        self._assert_disagreement_withholds_line8a(shared_before_local=True)

    def test_new_package_without_borrowing_activity_does_not_fabricate_completed_legacy_result(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(unconnected_singleton=True)
        self.assertEqual(report["authorization_status"], "AUTHORIZATION_ABSENT")
        self.assertIn("mortgageInterestExplanation", model)
        projection = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(projection["line8aDispositions"]), 1)
        self.assertEqual(len(projection["line8aFindings"]), 1)
        self.assertEqual(projection["line8aFindings"][0]["value"], 22000.0)
        self.assertEqual(len(projection["reports"]), 1)
        self.assertEqual(len(projection["groups"]), 0)
        legacy = model["mortgageInterestExplanation"]["accounts"][0]
        self.assertEqual(legacy["deductibleAmount"], 22000.0)
        self.assertEqual(legacy["reason"], "qualified")
        self.assertTrue(legacy["basis"]["derived"])
        self.assertTrue(legacy["personAnswers"])
        row = next(item for item in report["dispositions"] if item.get("artifact_id") == "tax.us.2025.rule.f1098-residence-interest-reason")
        self.assertEqual(row["disposition"], "published")


if __name__ == "__main__":
    unittest.main()
