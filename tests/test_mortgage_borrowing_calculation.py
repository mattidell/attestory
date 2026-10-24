"""Admission and scoped vocabulary for connected mortgage calculations."""
from __future__ import annotations

import hashlib
import json
import copy
import tempfile
import unittest
from pathlib import Path
from typing import Any

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
from tests.test_f1098_mortgage_interest_line12e_track2 import _attested, _f1098_acts

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/demo.release.sli-worksheet-integration.2025.v52.json"
RELEASE_DIR = RELEASE.parent
PACKAGE = CONTENT / "package.core-calculations.v54.json"
REGISTRY = CONTENT / "published-packages.v52.json"
BORROWING_REF = "demo.mortgage.borrowing.shared"
LINK_TYPE = "tax.us.2025.f1098.borrowing-inclusion"
ROOT_TYPE = "tax.us.2025.mortgage.continuing-borrowing"
LOCAL_BUNDLE = "f1098-circumstances.bundle.v2.json"
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


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _run_connected_case(*, uncertain_shared: str | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, str], dict[str, str]]:
    """Run the real recorder and coordinator against the successor package."""
    acts = _f1098_acts(interest=22000.0, second_statement_interest=3500.0)
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
        "version": "v52", "checksum": hashlib.sha256(release_bytes).hexdigest(),
    }
    adoption["payload"]["revision"] = len(acts) - 1
    acts.insert(len(acts) - 1, {"schema": "act.v1", "act_id": "demo.mortgage.local-bundle",
        "kind": "bundle-adoption", "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:00Z",
        "committed_against": len(acts) - 1, "payload": {"bundle": _load(CONTENT / LOCAL_BUNDLE)}})
    for index, row in enumerate(acts):
        row["committed_against"] = index
    adoption["payload"]["revision"] = len(acts) - 1

    report_keys = (
        {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"},
        {"payer": "demo.f1098.lender.b", "statement": "demo.f1098.stmt.b", "tax-year": "2025"},
    )
    local_ids: dict[str, str] = {}
    values = {key: value for key, (_, value) in SHARED_CLAIMS.items()}
    for report_index, keys in enumerate(report_keys):
        for question, fact_type in LOCAL_FACTS.items():
            if report_index == 0 and uncertain_shared == question:
                local_value = "yes"
            elif report_index == 0:
                continue  # A demonstrates shared-only support.
            else:
                local_value = values[question]
            finding_id = f"demo.mortgage.local.{report_index}.{question}"
            fact_id = fact_id_for(fact_type, tuple((key, keys[key]) for key in ("payer", "statement", "tax-year")))
            local_ids[f"{report_index}:{question}"] = finding_id
            acts.insert(len(acts) - 1, {"schema": "act.v1", "act_id": f"demo.mortgage.local-act.{report_index}.{question}",
                "kind": "assertion", "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:01Z",
                "committed_against": 0, "payload": {"finding": _attested(finding_id, fact_id, local_value)}})
    for index, row in enumerate(acts):
        row["committed_against"] = index
    adoption["payload"]["revision"] = len(acts) - 1

    with tempfile.TemporaryDirectory(prefix="mortgage-calculation-") as tmp:
        registry = tax_registry()
        log = ActLog(Path(tmp) / "workspace", registry)
        log.append_batch(acts, expected_revision=0)
        introduce_mortgage_borrowing_reference_durably(
            log, registry, reference_id=BORROWING_REF, description="Synthetic mortgage borrowing",
            actor="demo.user.filer-1", at="2026-10-23T16:01:00Z")

        def record(claim: str, value: str, statement: dict[str, str] | None = None) -> str:
            result = record_mortgage_borrowing_claim_durably(
                log, registry, claim=claim, borrowing_ref=BORROWING_REF, value=value,
                submission_id=f"demo.mortgage.submission.{log.read().revision}",
                evidence_id=f"demo.mortgage.evidence.{log.read().revision}", actor="demo.user.filer-1",
                at="2026-10-23T16:02:00Z", statement_keys=statement,
                expected_revision=log.read().revision)
            return result["finding_id"]

        record("continuing-borrowing", "yes")
        record("annual-ceiling", 250000)
        record("other-secured-home-debt", "no")
        shared_ids: dict[str, str] = {}
        for question, (claim, value) in SHARED_CLAIMS.items():
            if uncertain_shared == question:
                value = "cannot-tell"
            shared_ids[question] = record(claim, value)
        for report in report_keys:
            record("report-inclusion", "affirmed", report)

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
    def test_v54_admits_recording_and_calculation_vocab_without_losing_core_members(self) -> None:
        corpus = {}
        for path in CONTENT.glob("*.json"):
            citizen = _load(path)
            if isinstance(citizen, dict) and isinstance(citizen.get("id"), str) and isinstance(citizen.get("version"), str):
                corpus[(citizen["id"], citizen["version"])] = citizen

        base = _load(CONTENT / "package.core-calculations.v53.json")
        package = _load(CONTENT / "package.core-calculations.v54.json")
        result = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(result.ok, [issue.code for issue in result.issues])
        self.assertEqual(package["input_bindings"], base["input_bindings"])
        members = {(row["id"], row["version"], row["schema"], row["role"]) for row in package["members"]}
        base_members = {(row["id"], row["version"], row["schema"], row["role"]) for row in base["members"]}
        self.assertTrue(base_members <= members)
        self.assertEqual(len(package["members"]), 597)
        self.assertEqual(len(members - base_members), 17)

        calculation = corpus[("tax.us.2025.mortgage-borrowing-calculation", "v1")]
        linked = [fact for fact in calculation["fact_types"] if fact["id"].startswith("tax.us.2025.f1098.effective-")]
        self.assertEqual(len(linked), 5)
        expected_keys = ["payer", "statement", "tax-year", "borrowing"]
        self.assertTrue(all([key["name"] for key in fact["identity_keys"]] == expected_keys for fact in linked))

        base_registry = _load(CONTENT / "published-packages.v51.json")
        registry = _load(CONTENT / "published-packages.v52.json")
        self.assertTrue(set(map(json.dumps, base_registry["packages"])) <= set(map(json.dumps, registry["packages"])))
        self.assertTrue(set(map(json.dumps, base_registry["citizens"])) <= set(map(json.dumps, registry["citizens"])))
        entry = next(row for row in registry["packages"] if row["version"] == "v54")
        self.assertEqual(entry["checksum"], package["package_checksum"])
        self.assertEqual(
            _load(RELEASE)["package_registry_sha256"],
            hashlib.sha256((CONTENT / "published-packages.v52.json").read_bytes()).hexdigest(),
        )

    def test_five_effective_mappings_use_exact_real_recorded_links(self) -> None:
        report, model, local_ids, shared_ids = _run_connected_case()
        self.assertEqual(report["authorization_status"], "AUTHORIZATION_ABSENT")
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
                if report_index == 1:
                    self.assertIn(local_ids[f"1:{question}"], pins)
                else:
                    self.assertNotIn(local_ids.get(f"0:{question}"), pins)

    def test_cannot_tell_shared_claim_withholds_favorable_local_value(self) -> None:
        report, _model, local_ids, shared_ids = _run_connected_case(uncertain_shared="no-one-else-owes-it")
        target_type = "tax.us.2025.f1098.effective-no-one-else-owes-it"
        target_id = fact_id_for(target_type, (("payer", "demo.f1098.lender.a"),
            ("statement", "demo.f1098.stmt.a"), ("tax-year", "2025"), ("borrowing", BORROWING_REF)))
        symbol = f"{target_type}|tax.us.2025.f1098.borrowing-inclusion|payer=demo.f1098.lender.a,statement=demo.f1098.stmt.a,tax-year=2025,borrowing={BORROWING_REF}"
        rows = {row["symbol"]: row for row in report["dispositions"] if row.get("symbol")}
        self.assertEqual(rows[symbol]["disposition"], "blocked")
        self.assertTrue(local_ids["0:no-one-else-owes-it"])
        self.assertTrue(shared_ids["no-one-else-owes-it"])


if __name__ == "__main__":
    unittest.main()
