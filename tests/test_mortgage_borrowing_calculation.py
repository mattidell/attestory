"""Admission and scoped vocabulary for connected mortgage calculations."""
from __future__ import annotations

import hashlib
import json
import copy
import re
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from typing import Any, Mapping, cast

import pytest

from packages.derivation.loader import DerivationSchemas
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.marshal import MortgagePaymentApplicabilityInvalid
from packages.derivation.package_validation import validate_package
from packages.derivation.presentation_projection import _validate_mortgage_borrowing_explanation, validate_presentation_model
from packages.derivation.projection import compute_derivation_currency
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import tax_registry
from packages.tax.mortgage_borrowing_recording import (
    clear_mortgage_borrowing_year_durably,
    correct_mortgage_borrowing_claim_durably,
    introduce_mortgage_borrowing_reference_durably,
    record_mortgage_borrowing_claim_durably,
    withdraw_mortgage_borrowing_claim_durably,
    current_mortgage_payment_comparison_support,
    current_mortgage_payment_comparison_applicability,
)
from packages.tax.f1098_statement_recording import answer_f1098_statement_answer_durably
from packages.tax.f1098_statement_review import (
    answer_f1098_statement_review_question, prepare_f1098_statement_review,
)
from packages.tax.mortgage_borrowing_review import (
    MortgageBorrowingReviewRefused, clear_mortgage_borrowing_review_account,
    correct_mortgage_borrowing_review_answer, prepare_mortgage_borrowing_review,
    record_mortgage_borrowing_review_answer,
)
from tests.test_f1098_mortgage_interest_line12e_track2 import _f1098_acts

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/demo.release.sli-worksheet-integration.2025.v55.json"
RELEASE_DIR = RELEASE.parent
PACKAGE = CONTENT / "package.core-calculations.v57.json"
REGISTRY = CONTENT / "published-packages.v55.json"
BORROWING_REF = "demo.mortgage.borrowing.shared"
LINK_TYPE = "tax.us.2025.f1098.borrowing-inclusion"
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


def _add_line12e_base_answers(acts: list[dict[str, Any]], *, missing_boundary: str | None = None) -> None:
    """Add explicit synthetic unrelated current-return declarations; infer no defaults."""
    adoption = acts.pop()
    acts.append({
        "schema": "act.v1", "act_id": "demo.mortgage.base-vocabulary", "kind": "bundle-adoption",
        "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:29Z",
        "committed_against": len(acts),
        "payload": {"bundle": _load(CONTENT / "senior-and-dependent-deductions.vocabulary.bundle.json")},
    })
    base_answers = (
        ("standard-deduction.can-be-claimed-as-dependent", "no"),
        ("schedule1a.no-parts-ii-iv-deductions-declared", "yes"),
    )
    for name, value in base_answers:
        acts.append({
            "schema": "act.v1", "act_id": f"demo.mortgage.base.{name}", "kind": "assertion",
            "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:30Z",
            "committed_against": len(acts),
            "payload": {"finding": _attested(f"demo.mortgage.base.{name}", f"tax.us.2025.{name}|tax-year=2025", value)},
        })
    if missing_boundary is not None:
        target = f"tax.us.2025.schedule-a-boundary.{missing_boundary}|tax-year=2025"
        acts[:] = [row for row in acts if not (
            row.get("kind") == "assertion"
            and row.get("payload", {}).get("finding", {}).get("fact_id") == target
        )]
    for index, row in enumerate(acts):
        row["committed_against"] = index
    adoption["committed_against"] = len(acts)
    acts.append(adoption)


def _has_transitive_pin(report: dict[str, Any], source_id: str, target_pins: set[str]) -> bool:
    """Follow real published disposition pins from a recorded source to a consumer."""
    reachable = {source_id}
    changed = True
    while changed:
        changed = False
        for row in report["dispositions"]:
            finding_id = row.get("finding_id")
            if not isinstance(finding_id, str) or finding_id in reachable:
                continue
            pin_ids = {pin.get("id") for pin in row.get("pins", []) if isinstance(pin, dict)}
            if reachable & pin_ids:
                reachable.add(finding_id)
                changed = True
    return bool(reachable & target_pins)


def _replace_recorded_source_value(acts: list[dict[str, Any]], fact_id: str, value: Any) -> None:
    matches = [row for row in acts if row.get("kind") == "assertion"
               and row.get("payload", {}).get("finding", {}).get("fact_id") == fact_id]
    if len(matches) != 1:
        raise AssertionError(f"expected one exact synthetic source assertion for {fact_id}")
    matches[0]["payload"]["finding"]["value"] = value


def _run_connected_case(*, uncertain_shared: str | None = None, unlinked_third_report: bool = False,
                       late_third_report: bool = False,
                       unconnected_singleton: bool = False, fully_supported_local: bool = False,
                       shared_only: bool = False,
                       first_box3: str = "2020-06-01",
                       second_interest: float = 3500.0,
                       filing_status: str | None = None,
                       shared_before_local: bool = False,
                       missing_local: str | None = None,
                       missing_shared: str | None = None,
                       correct_shared: str | None = None,
                       withdraw_shared: str | None = None,
                       root_outcome: str | None = None,
                       clear_account: bool = False,
                       single_current_report: bool = False,
                       annual_ceiling: float = 250000,
                       second_box2: float | None = None,
                       second_box3: str | None = None,
                       include_line12e_base_answers: bool = False,
                       missing_schedule_a_boundary: str | None = None,
                       shared_overrides: dict[str, str] | None = None,
                       local_overrides: dict[str, str] | None = None,
                       withdraw_link: int | None = None,
                       missing_link: int | None = None,
                       link_outcome: str | None = None,
                       second_active_borrowing: bool = False,
                       dormant_borrowing: bool = False,
                       missing_account_claim: str | None = None,
                       missing_second_account_claim: str | None = None,
                       through_reviews: bool = False,
                       retain_saved_to: Path | None = None,
                       remove_first_report: bool = False,
                       remove_only_report: bool = False,
                       rerecord_removed_source: bool = False,
                       post_run_currency_mutation: str | None = None,
                       observed_derived_currency: dict[str, Any] | None = None,
                       emit_test_candidate_pin: bool = False,
                       observed_current_claims: dict[str, Any] | None = None,
                       observed_publications: list[dict[str, Any]] | None = None,
                       direct_unresolved_comparison: bool = False,
                       asserted_payment_support_markers: bool = False,
                       unresolved_comparison_index: int | None = None,
                       payment_comparison: str | None = "different-payments") -> tuple[dict[str, Any], dict[str, Any], dict[str, str], dict[str, str]]:
    """Run the real recorder and coordinator against the successor package."""
    acts = cast(list[dict[str, Any]], _f1098_acts(
        interest=22000.0,
        box3=first_box3,
        second_statement_interest=None if unconnected_singleton or single_current_report else second_interest))
    if second_box2 is not None:
        _replace_recorded_source_value(
            acts, fact_id_for("tax.us.2025.f1098.box2-outstanding-principal", (
                ("payer", "demo.f1098.lender.b"), ("statement", "demo.f1098.stmt.b"), ("tax-year", "2025"))),
            second_box2,
        )
    if second_box3 is not None:
        _replace_recorded_source_value(
            acts, fact_id_for("tax.us.2025.f1098.box3-origination-date", (
                ("payer", "demo.f1098.lender.b"), ("statement", "demo.f1098.stmt.b"), ("tax-year", "2025"))),
            second_box3,
        )
    if filing_status is not None:
        _replace_recorded_source_value(
            acts, "tax.us.2025.filing-status|tax-year=2025", filing_status,
        )
    if include_line12e_base_answers:
        _add_line12e_base_answers(acts, missing_boundary=missing_schedule_a_boundary)
    late_member_acts: list[dict[str, Any]] = []
    late_reclose_act: dict[str, Any] | None = None
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
    if late_third_report:
        closure = next(row for row in acts if row.get("kind") == "assertion"
                       and str(row.get("payload", {}).get("finding", {}).get("fact_id", "")).startswith("tax.us.2025.f1098.source-closure|"))
        admission = copy.deepcopy(next(row for row in acts if row.get("kind") == "member-transition"
                                       and row.get("payload", {}).get("successor", {}).get("id") == "demo.f1098.h2"))
        admission["act_id"] = "demo.f1098.late-third-report-transition"
        admission["payload"]["member"]["finding"] = _attested(
            "demo.f1098.late-third-box1",
            fact_id_for("tax.us.2025.f1098.box1-mortgage-interest", (
                ("payer", "demo.f1098.lender.c"), ("statement", "demo.f1098.stmt.c"), ("tax-year", "2025"))),
            1900.0)
        admission["payload"]["successor"] = {"id": "demo.f1098.h3", "predecessor": "demo.f1098.h2"}
        companion_types = (
            ("box2-outstanding-principal", 200000.0), ("box3-origination-date", "2020-06-01"),
            ("box4-overpaid-refund", 0.0), ("box5-mortgage-insurance", 0.0),
            ("box6-points", 0.0), ("box9-number-of-properties", 1.0), ("box11-other", 0.0),
        )
        extension = [
            {"schema": "act.v1", "act_id": "demo.f1098.late-third-payer", "kind": "entity-introduced",
             "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:00Z", "committed_against": 0,
             "payload": {"entity": {"schema": "entity.v1", "id": "demo.f1098.lender.c", "kind": "tax.us.mortgage-lender", "label": "Synthetic lender"}}},
            {"schema": "act.v1", "act_id": "demo.f1098.late-third-statement", "kind": "entity-introduced",
             "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:00Z", "committed_against": 0,
             "payload": {"entity": {"schema": "entity.v1", "id": "demo.f1098.stmt.c", "kind": "tax.us.1098-statement", "label": "Synthetic Form 1098"}}},
            admission,
        ]
        for suffix, value in companion_types:
            fact_type = f"tax.us.2025.f1098.{suffix}"
            extension.append({"schema": "act.v1", "act_id": f"demo.f1098.late-third-{suffix}", "kind": "assertion",
                              "actor": "demo.user.filer-1", "at": "2026-10-23T16:00:00Z", "committed_against": 0,
                              "payload": {"finding": _attested(
                                  f"demo.f1098.late-third-{suffix}", fact_id_for(fact_type, (
                                      ("payer", "demo.f1098.lender.c"), ("statement", "demo.f1098.stmt.c"), ("tax-year", "2025"))), value)}})
        closure_h3 = copy.deepcopy(closure)
        closure_h3["act_id"] = "demo.f1098.late-third-reclose"
        closure_h3["payload"]["finding"] = _attested(
            "demo.f1098.late-third-closure",
            "tax.us.2025.f1098.source-closure|family-horizon=demo.f1098.h3,tax-year=2025", True)
        late_member_acts = extension
        late_reclose_act = closure_h3
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
        "version": "v55", "checksum": hashlib.sha256(release_bytes).hexdigest(),
    }
    adoption["payload"]["revision"] = len(acts) - 1
    report_keys_all = (
        {"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"},
        {"payer": "demo.f1098.lender.b", "statement": "demo.f1098.stmt.b", "tax-year": "2025"},
    ) + (({"payer": "demo.f1098.lender.c", "statement": "demo.f1098.stmt.c", "tax-year": "2025"},)
         if late_third_report else ())
    report_keys = report_keys_all[:1] if single_current_report else report_keys_all
    local_ids: dict[str, str] = {}
    root_ids: dict[str, str] = {}
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
        if late_member_acts:
            revision = log.read().revision
            for index, row in enumerate(late_member_acts):
                row["committed_against"] = revision + index
            log.append_batch(late_member_acts, expected_revision=revision)
            open_contents = log.read()
            open_horizon = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "run-open-horizon"), repo_root=ROOT,
                authoritative_acts=list(open_contents.acts), workspace_revision=open_contents.revision,
                run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"}, run_id="demo.mortgage.mapping.open-horizon",
                governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
                output_name="open-horizon.json")
            if open_horizon.refusal is not None or any(
                publication.finding.get("symbol") == "tax.us.2025.schedule-a.line8a"
                for publication in (open_horizon.publications or ())
            ):
                raise AssertionError("open late-member horizon must withhold, not reuse the old line-8a result")
            if late_reclose_act is None:
                raise AssertionError("late-member fixture lost its exact reclosure act")
            revision = log.read().revision
            late_reclose_act["committed_against"] = revision
            log.append(late_reclose_act, expected_revision=revision)
        if not unconnected_singleton:
            introduce_mortgage_borrowing_reference_durably(
                log, registry, reference_id=BORROWING_REF, description="Synthetic mortgage borrowing",
                actor="demo.user.filer-1", at="2026-10-23T16:01:00Z")
        if second_active_borrowing or dormant_borrowing:
            introduce_mortgage_borrowing_reference_durably(
                log, registry, reference_id="demo.mortgage.borrowing.other", description="Other synthetic mortgage borrowing",
                actor="demo.user.filer-1", at="2026-10-23T16:01:05Z")

        def record(claim: str, value: Any, statement: dict[str, str] | None = None,
                   borrowing_ref: str = BORROWING_REF,
                   peer_statement: dict[str, str] | None = None) -> str:
            if through_reviews:
                review = prepare_mortgage_borrowing_review(
                    log, registry, review_id=f"demo.mortgage.review.{log.read().revision}",
                    shown_at="2026-10-23T16:01:55Z", borrowing_ref=borrowing_ref)
                offered = next(row for row in review["questions"] if row["claim"] == claim)
                if offered["inputKind"] == "choice":
                    choices = {choice["value"]: choice["label"] for choice in offered["choices"]}
                    if value not in choices:
                        raise AssertionError(f"test requested an unoffered {claim} value: {value!r}")
                    value = next(choice["value"] for choice in offered["choices"] if choice["value"] == value)
                elif (offered["inputKind"] != "nonnegative-number" or not isinstance(value, (int, float))
                      or isinstance(value, bool) or value < offered["minimum"]):
                    raise AssertionError(f"test requested an invalid numeric {claim} value: {value!r}")
                result = record_mortgage_borrowing_review_answer(
                    log, registry, review, claim=claim, borrowing_ref=borrowing_ref, value=value,
                    submission_id=f"demo.mortgage.submission.{log.read().revision}",
                    evidence_id=f"demo.mortgage.evidence.{log.read().revision}",
                    actor="demo.user.filer-1", at="2026-10-23T16:02:00Z", statement_keys=statement,
                    peer_statement_keys=peer_statement)
                return cast(str, result["finding_id"])
            result = record_mortgage_borrowing_claim_durably(
                log, registry, claim=claim, borrowing_ref=borrowing_ref, value=value,
                submission_id=f"demo.mortgage.submission.{log.read().revision}",
                evidence_id=f"demo.mortgage.evidence.{log.read().revision}", actor="demo.user.filer-1",
                at="2026-10-23T16:02:00Z", statement_keys=statement,
                peer_statement_keys=peer_statement,
                comparison_support=(current_mortgage_payment_comparison_support(
                    log.read().acts, registry, borrowing_ref) if claim == "payment-comparison" else None),
                expected_revision=log.read().revision)
            return cast(str, result["finding_id"])

        def record_local(keys: dict[str, str], question: str, value: str, suffix: str) -> str:
            if through_reviews:
                review = prepare_f1098_statement_review(
                    log, registry, review_id=f"demo.f1098.review.{log.read().revision}",
                    shown_at="2026-10-23T16:01:55Z", bundle_version="v2", statement_keys=keys)
                result = answer_f1098_statement_review_question(
                    log, registry, review, question=question, answer=value,
                    submission_id=f"demo.mortgage.local.{suffix}",
                    evidence_id=f"demo.mortgage.local-evidence.{suffix}",
                    actor="demo.user.filer-1", at="2026-10-23T16:01:35Z")
                return cast(str, result["finding_ids"][0])
            result = answer_f1098_statement_answer_durably(
                log, registry, statement_keys=keys, question=question, answer=value,
                submission_id=f"demo.mortgage.local.{suffix}", evidence_id=f"demo.mortgage.local-evidence.{suffix}",
                actor="demo.user.filer-1", at="2026-10-23T16:01:35Z",
                expected_revision=log.read().revision, bundle_version="v2")
            return cast(str, result["finding_ids"][0])

        shared_ids: dict[str, str] = {}
        link_ids: dict[int, str] = {}
        payment_ids: dict[int, str] = {}

        def record_shared_claims() -> None:
            root_ids["recognition"] = record("continuing-borrowing", "yes")
            if missing_account_claim != "annual-ceiling":
                record("annual-ceiling", annual_ceiling)
            if missing_account_claim != "other-secured-home-debt":
                record("other-secured-home-debt", "no")
            shared_values = dict(values)
            if shared_overrides:
                shared_values.update(shared_overrides)
            for question, (claim, _default_value) in SHARED_CLAIMS.items():
                if missing_shared == question:
                    continue
                value = "cannot-tell" if uncertain_shared == question else shared_values[question]
                shared_ids[question] = record(claim, value)
            if second_active_borrowing:
                if len(report_keys) != 2:
                    raise AssertionError("two active borrowing roots require two current reports")
                first_report, second_report = report_keys
                link_ids[0] = record("report-inclusion", "affirmed", first_report)
                other_ref = "demo.mortgage.borrowing.other"
                record("continuing-borrowing", "yes", borrowing_ref=other_ref)
                if missing_second_account_claim != "annual-ceiling":
                    record("annual-ceiling", annual_ceiling, borrowing_ref=other_ref)
                if missing_second_account_claim != "other-secured-home-debt":
                    record("other-secured-home-debt", "no", borrowing_ref=other_ref)
                for claim, value in values.items():
                    record(claim, value, borrowing_ref=other_ref)
                link_ids[1] = record("report-inclusion", "affirmed", second_report, borrowing_ref=other_ref)
            else:
                for report_index, report in enumerate(report_keys):
                    if missing_link == report_index:
                        continue
                    link_ids[report_index] = record("report-inclusion", "affirmed", report)
                if (payment_comparison is not None and len(report_keys) == 2 and
                        all(index in link_ids for index in (0, 1))):
                    for index, report in enumerate(report_keys):
                        peer = report_keys[1 - index]
                        if unresolved_comparison_index == index:
                            comparison_fact = fact_id_for(
                                "tax.us.2025.mortgage.report-payment-comparison",
                                tuple((key, value) for key, value in (
                                    ("payer", report["payer"]), ("statement", report["statement"]),
                                    ("tax-year", report["tax-year"]), ("borrowing", BORROWING_REF))))
                            finding_id = f"demo.mortgage.unresolved-comparison.{index}"
                            revision = log.read().revision
                            log.append({
                                "schema": "act.v1", "act_id": f"{finding_id}.act", "kind": "assertion",
                                "actor": "demo.user.filer-1", "at": "2026-10-23T16:02:01Z",
                                "committed_against": revision,
                                "payload": {"finding": _attested(finding_id, comparison_fact, payment_comparison)},
                            }, expected_revision=revision)
                            payment_ids[index] = finding_id
                        else:
                            payment_ids[index] = record("payment-comparison", payment_comparison, report,
                                                         peer_statement=peer)
            if dormant_borrowing:
                dormant_ref = "demo.mortgage.borrowing.other"
                record("annual-ceiling", annual_ceiling, borrowing_ref=dormant_ref)
                record("other-secured-home-debt", "no", borrowing_ref=dormant_ref)

        if shared_before_local and not unconnected_singleton:
            record_shared_claims()

        for report_index, keys in enumerate(report_keys[:1] if unconnected_singleton else report_keys):
            for question in LOCAL_FACTS:
                if shared_only:
                    continue
                if missing_local == question and report_index == 0:
                    continue
                if (missing_local is None and report_index == 0 and uncertain_shared != question
                        and not fully_supported_local and not unconnected_singleton):
                    continue  # A demonstrates shared-only support except in the uncertainty mutation.
                local_value = (legacy_local_values[question] if unconnected_singleton
                               else values[question] if fully_supported_local
                               else "yes" if report_index == 0 else values[question])
                local_value = (local_overrides or {}).get(question, local_value)
                local_ids[f"{report_index}:{question}"] = record_local(
                    keys, question, local_value, f"{report_index}.{question}")

        if not unconnected_singleton and not fully_supported_local:
            report_indices = (0,) if single_current_report else ((0, 1) if shared_only or missing_local is not None else (1,))
            for report_index in report_indices:
                for question, value in {
                    "filing-unit-owns-home": "yes", "shared-main-home": "yes",
                    "home-is-collateral": "yes", "paid-the-interest": "yes",
                }.items():
                    if missing_local == question and report_index == 0:
                        continue
                    value = (local_overrides or {}).get(question, value)
                    local_ids[f"{report_index}:{question}"] = record_local(
                        report_keys[report_index], question, value, f"{report_index}.{question}")

        if fully_supported_local and not unconnected_singleton:
            for report_index, keys in enumerate(report_keys):
                for question in ("filing-unit-owns-home", "shared-main-home", "home-is-collateral", "paid-the-interest"):
                    if missing_local == question and report_index == 0:
                        continue
                    local_ids[f"{report_index}:{question}"] = record_local(
                        keys, question, (local_overrides or {}).get(question, "yes"),
                        f"{report_index}.{question}")

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

        saved_before_removal: tuple[bytes, bytes] | None = None
        saved_before_removal_paths: tuple[Path, Path] | None = None
        original_line8a_ids: set[str] = set()
        if remove_first_report or remove_only_report:
            if rerecord_removed_source:
                before_removal = log.read()
                prior_run = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "run-before-removal"), repo_root=ROOT,
                    authoritative_acts=list(before_removal.acts), workspace_revision=before_removal.revision,
                    run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
                    request={"schema": "run-request.v1"}, run_id="demo.mortgage.mapping.before-remove-rerecord",
                    governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
                    output_name="before-removal.json")
                if prior_run.refusal is not None or prior_run.output_path is None or prior_run.presentation_path is None:
                    raise AssertionError("baseline saved run failed before the removal lifecycle")
                saved_before_removal = (
                    prior_run.output_path.read_bytes(), prior_run.presentation_path.read_bytes(),
                )
                saved_before_removal_paths = (prior_run.output_path, prior_run.presentation_path)
                original_line8a_ids = {
                    publication.finding["id"]
                    for publication in (prior_run.publications or ())
                    if publication.finding.get("symbol") == "tax.us.2025.schedule-a.line8a"
                }
            transitions = [
                row for row in log.read().acts
                if row.get("kind") == "member-transition"
                and row.get("payload", {}).get("family", {}).get("id") == "tax.us.2025.f1098"
            ]
            expected_transitions = 1 if remove_only_report else 2
            if len(transitions) != expected_transitions:
                raise AssertionError("the removal probe has an unexpected source-member count")
            predecessor = transitions[-1]["payload"]["successor"]["id"]
            horizon = "demo.f1098.h3"
            removed_source = fact_id_for("tax.us.2025.f1098.box1-mortgage-interest", (
                ("payer", "demo.f1098.lender.a"), ("statement", "demo.f1098.stmt.a"), ("tax-year", "2025"),
            ))
            revision = log.read().revision
            revision = log.append({
                "schema": "act.v1", "act_id": "demo.f1098.remove-first-report",
                "kind": "member-transition", "actor": "demo.user.filer-1",
                "at": "2026-10-23T16:03:40Z", "committed_against": revision,
                "payload": {
                    "family": {"id": "tax.us.2025.f1098", "version": "v1"},
                    "scope": {"tax-year": "2025", "subject": "demo.primary"},
                    "member": {"action": "remove", "fact_id": removed_source},
                    "successor": {"id": horizon, "predecessor": predecessor},
                },
            }, expected_revision=revision)
            log.append({
                "schema": "act.v1", "act_id": "demo.f1098.reclose-after-removal",
                "kind": "assertion", "actor": "demo.user.filer-1",
                "at": "2026-10-23T16:03:41Z", "committed_against": revision,
                "payload": {"finding": _attested(
                    "demo.f1098.closure.after-removal",
                    f"tax.us.2025.f1098.source-closure|family-horizon={horizon},tax-year=2025",
                    True,
                )},
            }, expected_revision=revision)
            if rerecord_removed_source:
                intermediate = log.read()
                after_removal = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "run-after-removal"), repo_root=ROOT,
                    authoritative_acts=list(intermediate.acts), workspace_revision=intermediate.revision,
                    run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
                    request={"schema": "run-request.v1"}, run_id="demo.mortgage.mapping.after-removal",
                    governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
                    output_name="after-removal.json")
                if after_removal.refusal is not None or any(
                    publication.finding.get("symbol") == "tax.us.2025.schedule-a.line8a"
                    for publication in (after_removal.publications or ())
                ):
                    raise AssertionError("removed report was reused as a current line-8a result")
                revision = log.read().revision
                readded = log.append({
                    "schema": "act.v1", "act_id": "demo.f1098.rerecord-first-report",
                    "kind": "member-transition", "actor": "demo.user.filer-1",
                    "at": "2026-10-23T16:03:42Z", "committed_against": revision,
                    "payload": {
                        "family": {"id": "tax.us.2025.f1098", "version": "v1"},
                        "scope": {"tax-year": "2025", "subject": "demo.primary"},
                        "member": {"action": "assert", "finding": _attested(
                            "demo.f1098.rerecorded-box1", removed_source, 22000.0)},
                        "successor": {"id": "demo.f1098.h4", "predecessor": horizon},
                    },
                }, expected_revision=revision)
                log.append({
                    "schema": "act.v1", "act_id": "demo.f1098.reclose-after-rerecord",
                    "kind": "assertion", "actor": "demo.user.filer-1",
                    "at": "2026-10-23T16:03:43Z", "committed_against": readded,
                    "payload": {"finding": _attested(
                        "demo.f1098.closure.after-rerecord",
                        "tax.us.2025.f1098.source-closure|family-horizon=demo.f1098.h4,tax-year=2025", True)},
                }, expected_revision=readded)
                rerecorded_state = project(log.read().acts, registry)
                rerecorded_current = compute_currency(rerecorded_state).current_finding_ids
                rerecorded_finding = rerecorded_state.findings.get("demo.f1098.rerecorded-box1")
                old_source_findings = {
                    finding_id for finding_id, finding in rerecorded_state.findings.items()
                    if finding.get("fact_id") == removed_source
                    and finding_id != "demo.f1098.rerecorded-box1"
                }
                rerecorded_currency = compute_currency(rerecorded_state)
                preserved_local_ids = {
                    finding_id for key, finding_id in local_ids.items() if key.startswith("0:")
                }
                if (removed_source in rerecorded_state.withdrawn_fact_ids
                        or not isinstance(rerecorded_finding, Mapping)
                        or rerecorded_finding.get("fact_id") != removed_source
                        or "demo.f1098.rerecorded-box1" not in rerecorded_current
                        or not old_source_findings <= rerecorded_currency.displaced_finding_ids
                        or not preserved_local_ids <= rerecorded_current):
                    raise AssertionError("fresh source restoration must current only the new source finding and preserve independent local answers")
                review = prepare_mortgage_borrowing_review(
                    log, registry, review_id="demo.mortgage.review.rerecord-exact-link",
                    shown_at="2026-10-23T16:03:44Z", borrowing_ref=BORROWING_REF)
                corrected_link = correct_mortgage_borrowing_review_answer(
                    log, registry, review, claim="report-inclusion", borrowing_ref=BORROWING_REF,
                    finding_id=link_ids[0],
                    statement_keys={"payer": "demo.f1098.lender.a", "statement": "demo.f1098.stmt.a", "tax-year": "2025"},
                    value="affirmed", submission_id="demo.mortgage.reconfirm-restored-source-link",
                    evidence_id="demo.mortgage.reconfirm-restored-source-link.evidence",
                    actor="demo.user.filer-1", at="2026-10-23T16:03:45Z")
                link_ids[0] = corrected_link["finding_id"]
                prior_comparison_ids = dict(payment_ids)
                if observed_current_claims is not None:
                    observed_current_claims["prior_payment_comparison_ids"] = prior_comparison_ids
                for index in sorted(payment_ids):
                    comparison_review = prepare_mortgage_borrowing_review(
                        log, registry, review_id=f"demo.mortgage.review.reconfirm-comparison.{index}",
                        shown_at=f"2026-10-23T16:03:4{6 + index}Z", borrowing_ref=BORROWING_REF)
                    old_comparison_id = payment_ids[index]
                    offer = next(row for row in comparison_review["answers"]
                                 if row["claim"] == "payment-comparison"
                                 and row["findingId"] == old_comparison_id)
                    own_keys = {key: offer["scope"][key] for key in ("payer", "statement", "tax-year")}
                    reasserted = correct_mortgage_borrowing_review_answer(
                        log, registry, comparison_review, claim="payment-comparison",
                        borrowing_ref=BORROWING_REF, finding_id=old_comparison_id,
                        value="different-payments",
                        submission_id=f"demo.mortgage.reconfirm-restored-source-comparison.{index}",
                        evidence_id=f"demo.mortgage.reconfirm-restored-source-comparison.{index}.evidence",
                        statement_keys=own_keys, peer_statement_keys=offer["peerScope"],
                        actor="demo.user.filer-1", at=f"2026-10-23T16:03:4{8 + index}Z")
                    payment_ids[index] = reasserted["finding_id"]

        if correct_shared is not None:
            claim, favorable_value = SHARED_CLAIMS[correct_shared]
            shared_ids[f"previous:{correct_shared}"] = shared_ids[correct_shared]
            corrected = correct_mortgage_borrowing_claim_durably(
                log, registry, finding_id=shared_ids[correct_shared], claim=claim,
                borrowing_ref=BORROWING_REF, value=favorable_value,
                submission_id=f"demo.mortgage.correct.{correct_shared}",
                evidence_id=f"demo.mortgage.correct-evidence.{correct_shared}",
                actor="demo.user.filer-1", at="2026-10-23T16:03:00Z",
                expected_revision=log.read().revision,
            )
            shared_ids[correct_shared] = corrected["finding_id"]
        if withdraw_shared is not None:
            claim, _value = SHARED_CLAIMS[withdraw_shared]
            withdraw_mortgage_borrowing_claim_durably(
                log, registry, finding_id=shared_ids[withdraw_shared], claim=claim,
                borrowing_ref=BORROWING_REF, actor="demo.user.filer-1",
                at="2026-10-23T16:03:30Z", expected_revision=log.read().revision,
            )
        if withdraw_link is not None:
            withdraw_mortgage_borrowing_claim_durably(
                log, registry, finding_id=link_ids[withdraw_link], claim="report-inclusion",
                borrowing_ref=BORROWING_REF, actor="demo.user.filer-1",
                at="2026-10-23T16:03:45Z", expected_revision=log.read().revision,
                submission_id=f"demo.mortgage.withdraw-link.{withdraw_link}",
                evidence_id=f"demo.mortgage.withdraw-link-evidence.{withdraw_link}",
                statement_keys=report_keys[withdraw_link],
            )
        if link_outcome is not None:
            correct_mortgage_borrowing_claim_durably(
                log, registry, finding_id=link_ids[0], claim="report-inclusion",
                borrowing_ref=BORROWING_REF, value=link_outcome,
                submission_id=f"demo.mortgage.correct-link.{link_outcome}",
                evidence_id=f"demo.mortgage.correct-link-evidence.{link_outcome}",
                actor="demo.user.filer-1", at="2026-10-23T16:03:46Z",
                statement_keys=report_keys[0], expected_revision=log.read().revision,
            )
        if root_outcome is not None:
            correct_mortgage_borrowing_claim_durably(
                log, registry, finding_id=root_ids["recognition"], claim="continuing-borrowing",
                borrowing_ref=BORROWING_REF, value=root_outcome,
                submission_id="demo.mortgage.correct-root-outcome",
                evidence_id="demo.mortgage.correct-root-evidence", actor="demo.user.filer-1",
                at="2026-10-23T16:04:00Z", expected_revision=log.read().revision,
            )
        if clear_account:
            if through_reviews:
                review = prepare_mortgage_borrowing_review(
                    log, registry, review_id=f"demo.mortgage.review.clear.{log.read().revision}",
                    shown_at="2026-10-23T16:04:25Z", borrowing_ref=BORROWING_REF)
                clear_mortgage_borrowing_review_account(
                    log, registry, review, borrowing_ref=BORROWING_REF,
                    actor="demo.user.filer-1", at="2026-10-23T16:04:30Z")
            else:
                clear_mortgage_borrowing_year_durably(
                    log, registry, borrowing_ref=BORROWING_REF, actor="demo.user.filer-1",
                    at="2026-10-23T16:04:30Z", expected_revision=log.read().revision,
                )

        if observed_current_claims is not None:
            state = project(log.read().acts, registry)
            current_ids = compute_currency(state).current_finding_ids
            fact_lattice = facts_of(state.fact_state)
            for index, finding_id in link_ids.items():
                finding = state.findings[finding_id]
                observed_current_claims[f"report-inclusion:{index}"] = {
                    "finding_id": finding_id,
                    "fact_id": finding["fact_id"],
                    "fact_type": fact_lattice[finding["fact_id"]].fact_type_id,
                    "value": finding["value"],
                    "is_current": finding_id in current_ids,
                }
            for index, finding_id in payment_ids.items():
                finding = state.findings[finding_id]
                observed_current_claims[f"payment-comparison:{index}"] = {
                    "finding_id": finding_id,
                    "fact_id": finding["fact_id"],
                    "fact_type": fact_lattice[finding["fact_id"]].fact_type_id,
                    "value": finding["value"],
                    "is_current": finding_id in current_ids,
                }
            observed_current_claims["payment-comparison-applicability"] = (
                current_mortgage_payment_comparison_applicability(log.read().acts, registry))

        if direct_unresolved_comparison or asserted_payment_support_markers:
            required_bundles = []
            if direct_unresolved_comparison:
                required_bundles.append(("mortgage-borrowing.bundle.json",
                                         "tax.us.2025.mortgage.report-payment-comparison"))
            if asserted_payment_support_markers:
                required_bundles.append(("mortgage-borrowing-calculation.bundle.json",
                                         "tax.us.2025.mortgage.payment-comparison-support-marker"))
            state = project(log.read().acts, registry)
            for bundle_name, required_type in required_bundles:
                if required_type in state.fact_state.fact_types:
                    continue
                revision = log.read().revision
                log.append({
                    "schema": "act.v1", "act_id": f"demo.mortgage.raw-support-vocabulary.{len(required_bundles)}.{revision}",
                    "kind": "bundle-adoption", "actor": "demo.user.filer-1",
                    "at": "2026-10-23T16:04:57Z", "committed_against": revision,
                    "payload": {"bundle": _load(CONTENT / bundle_name)},
                }, expected_revision=revision)
                state = project(log.read().acts, registry)

        if direct_unresolved_comparison:
            own = report_keys[0]
            ordered_keys = tuple((key, value) for key, value in (
                ("payer", own["payer"]), ("statement", own["statement"]), ("tax-year", own["tax-year"]),
                ("borrowing", BORROWING_REF)))
            fact_id = fact_id_for("tax.us.2025.mortgage.report-payment-comparison", ordered_keys)
            revision = log.read().revision
            log.append({
                "schema": "act.v1", "act_id": "demo.mortgage.direct-unresolved-comparison",
                "kind": "assertion", "actor": "demo.user.filer-1",
                "at": "2026-10-23T16:04:58Z", "committed_against": revision,
                "payload": {"finding": _attested(
                    "demo.mortgage.direct-unresolved-comparison", fact_id, "different-payments")},
            }, expected_revision=revision)

        if asserted_payment_support_markers:
            marker_type = "tax.us.2025.mortgage.payment-comparison-support-marker"
            # Deliberately ordinary user assertions, including a wrong payer
            # for report B. They must not impersonate the marshal's derived
            # exact-pair support rows.
            for report_index, statement in enumerate(("demo.f1098.stmt.a", "demo.f1098.stmt.b")):
                for support_kind in ("comparison", "box1", "inclusion", "recognition"):
                    marker_identity = ("demo.f1098.lender.a", statement, "2025", BORROWING_REF, support_kind)
                    identity = tuple(zip(("payer", "statement", "tax-year", "borrowing", "support-kind"), marker_identity, strict=True))
                    fact_id = fact_id_for(marker_type, identity)
                    revision = log.read().revision
                    finding_id = f"demo.mortgage.asserted-payment-support.{report_index}.{support_kind}"
                    log.append({
                        "schema": "act.v1", "act_id": f"{finding_id}.act", "kind": "assertion",
                        "actor": "demo.user.filer-1", "at": "2026-10-23T16:04:59Z",
                        "committed_against": revision,
                        "payload": {"finding": _attested(finding_id, fact_id, "ready")},
                    }, expected_revision=revision)

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
        if emit_test_candidate_pin:
            state = project(log.read().acts, registry)
            current = compute_currency(state).current_finding_ids
            target_ids = [link_ids[0], link_ids[1], root_ids["recognition"]]
            for keys in report_keys[:2]:
                box1_id = fact_id_for(
                    "tax.us.2025.f1098.box1-mortgage-interest", tuple(sorted(keys.items()))
                )
                source_ids = [finding_id for finding_id, finding in state.findings.items()
                              if finding_id in current and finding.get("fact_id") == box1_id]
                if len(source_ids) != 1:
                    raise AssertionError(f"candidate pin probe expected one exact Box 1 finding: {source_ids}")
                target_ids.extend(source_ids)
            candidate = {
                "schema": "finding.v2", "id": "demo.test-only.candidate-pair-attestation",
                "fact_id": fact_id_for("tax.us.2025.f1098.this-is-the-original-loan", tuple(sorted({
                    "payer": "demo.test-only.candidate-payer",
                    "statement": "demo.test-only.candidate-statement", "tax-year": "2025",
                }.items()))),
                "value": "yes", "basis": "attested", "evidence_ids": [],
                "pins": {"finding_ids": sorted(set(target_ids)), "artifact_ids": []},
            }
            before_candidate_append = log.read().revision
            appended_revision = log.append({
                "schema": "act.v1", "act_id": "demo.test-only.candidate-pair-act",
                "kind": "assertion", "actor": "demo.user.filer-1",
                "at": "2026-10-23T16:04:59Z", "committed_against": before_candidate_append,
                "payload": {"finding": candidate},
            }, expected_revision=before_candidate_append)
            if appended_revision != before_candidate_append + 1:
                raise AssertionError("the schema-valid candidate act was not appended before projection")
            project(log.read().acts, registry)
            raise AssertionError("kernel unexpectedly projected an ordinary candidate finding with pins")
        if post_run_currency_mutation is not None:
            assert outcome.publications is not None
            old_publications = tuple(outcome.publications)
            if post_run_currency_mutation == "remove-box1":
                source_id = fact_id_for("tax.us.2025.f1098.box1-mortgage-interest", (
                    ("payer", "demo.f1098.lender.a"), ("statement", "demo.f1098.stmt.a"),
                    ("tax-year", "2025"),
                ))
                revision = log.read().revision
                revision = log.append({
                    "schema": "act.v1", "act_id": "demo.mortgage.withdraw-box1-membership",
                    "kind": "member-transition", "actor": "demo.user.filer-1",
                    "at": "2026-10-23T16:05:01Z", "committed_against": revision,
                    "payload": {
                        "family": {"id": "tax.us.2025.f1098", "version": "v1"},
                        "scope": {"tax-year": "2025", "subject": "demo.primary"},
                        "member": {"action": "remove", "fact_id": source_id},
                        "successor": {"id": "demo.f1098.currency-h3", "predecessor": "demo.f1098.h2"},
                    },
                }, expected_revision=revision)
                log.append({
                    "schema": "act.v1", "act_id": "demo.mortgage.currency-reclose",
                    "kind": "assertion", "actor": "demo.user.filer-1",
                    "at": "2026-10-23T16:05:02Z", "committed_against": revision,
                    "payload": {"finding": _attested(
                        "demo.f1098.currency-closure",
                        "tax.us.2025.f1098.source-closure|family-horizon=demo.f1098.currency-h3,tax-year=2025",
                        True,
                    )},
                }, expected_revision=revision)
            elif post_run_currency_mutation == "third-report-roundtrip":
                base = log.read()
                source_transition = next(row for row in base.acts
                                         if row.get("kind") == "member-transition"
                                         and row.get("payload", {}).get("successor", {}).get("id") == "demo.f1098.h2")
                add_third = copy.deepcopy(source_transition)
                add_third["act_id"] = "demo.f1098.roundtrip-add-c"
                add_third["payload"]["member"]["finding"] = _attested(
                    "demo.f1098.roundtrip-box1-c",
                    fact_id_for("tax.us.2025.f1098.box1-mortgage-interest", (
                        ("payer", "demo.f1098.lender.c"), ("statement", "demo.f1098.stmt.c"),
                        ("tax-year", "2025"))), 1900.0)
                add_third["payload"]["successor"] = {"id": "demo.f1098.h3", "predecessor": "demo.f1098.h2"}
                extension = [
                    {"schema": "act.v1", "act_id": "demo.f1098.roundtrip-payer-c", "kind": "entity-introduced",
                     "actor": "demo.user.filer-1", "at": "2026-10-23T16:05:01Z", "committed_against": 0,
                     "payload": {"entity": {"schema": "entity.v1", "id": "demo.f1098.lender.c",
                                  "kind": "tax.us.mortgage-lender", "label": "Synthetic lender C"}}},
                    {"schema": "act.v1", "act_id": "demo.f1098.roundtrip-statement-c", "kind": "entity-introduced",
                     "actor": "demo.user.filer-1", "at": "2026-10-23T16:05:02Z", "committed_against": 0,
                     "payload": {"entity": {"schema": "entity.v1", "id": "demo.f1098.stmt.c",
                                  "kind": "tax.us.1098-statement", "label": "Synthetic Form 1098 C"}}},
                    add_third,
                ]
                revision = base.revision
                for index, item in enumerate(extension):
                    item["committed_against"] = revision + index
                log.append_batch(extension, expected_revision=revision)
                open_contents = log.read()
                open_result = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "third-report-open"), repo_root=ROOT,
                    authoritative_acts=list(open_contents.acts), workspace_revision=open_contents.revision,
                    run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
                    request={"schema": "run-request.v1"}, run_id="demo.mortgage.third-report.open",
                    governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
                    output_name="third-open.json")
                if open_result.refusal is not None or any(
                    publication.finding.get("symbol") in {"tax.us.2025.schedule-a.line8a",
                                                            "tax.us.2025.deductions.line-12e"}
                    for publication in (open_result.publications or ())):
                    raise AssertionError("open third-report horizon must withhold both final mortgage lines")
                revision = log.read().revision
                close_third = {"schema": "act.v1", "act_id": "demo.f1098.roundtrip-close-h3",
                               "kind": "assertion", "actor": "demo.user.filer-1",
                               "at": "2026-10-23T16:05:03Z", "committed_against": revision,
                               "payload": {"finding": _attested(
                                   "demo.f1098.roundtrip-closure-h3",
                                   "tax.us.2025.f1098.source-closure|family-horizon=demo.f1098.h3,tax-year=2025",
                                   True)}}
                log.append(close_third, expected_revision=revision)
                closed_contents = log.read()
                closed_result = live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "third-report-closed"), repo_root=ROOT,
                    authoritative_acts=list(closed_contents.acts), workspace_revision=closed_contents.revision,
                    run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
                    request={"schema": "run-request.v1"}, run_id="demo.mortgage.third-report.closed",
                    governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
                    output_name="third-closed.json")
                if closed_result.refusal is not None or any(
                    publication.finding.get("symbol") in {"tax.us.2025.schedule-a.line8a",
                                                            "tax.us.2025.deductions.line-12e"}
                    for publication in (closed_result.publications or ())):
                    raise AssertionError("closed third-report family must not publish a partial mortgage result")
                assert observed_current_claims is not None
                closed_state = project(closed_contents.acts, registry)
                closed_readings = current_mortgage_payment_comparison_applicability(
                    closed_contents.acts, registry, state=closed_state,
                    currency=compute_currency(closed_state), lattice=facts_of(closed_state.fact_state))
                observed_current_claims["third-present-comparisons"] = closed_readings
                revision = log.read().revision
                remove_third = {"schema": "act.v1", "act_id": "demo.f1098.roundtrip-remove-c",
                                "kind": "member-transition", "actor": "demo.user.filer-1",
                                "at": "2026-10-23T16:05:04Z", "committed_against": revision,
                                "payload": {"family": {"id": "tax.us.2025.f1098", "version": "v1"},
                                            "scope": {"tax-year": "2025", "subject": "demo.primary"},
                                            "member": {"action": "remove", "fact_id": fact_id_for(
                                                "tax.us.2025.f1098.box1-mortgage-interest", (
                                                    ("payer", "demo.f1098.lender.c"),
                                                    ("statement", "demo.f1098.stmt.c"),
                                                    ("tax-year", "2025")))},
                                            "successor": {"id": "demo.f1098.h4", "predecessor": "demo.f1098.h3"}}}
                log.append(remove_third, expected_revision=revision)
                revision = log.read().revision
                close_fourth = {"schema": "act.v1", "act_id": "demo.f1098.roundtrip-close-h4",
                                "kind": "assertion", "actor": "demo.user.filer-1",
                                "at": "2026-10-23T16:05:05Z", "committed_against": revision,
                                "payload": {"finding": _attested(
                                    "demo.f1098.roundtrip-closure-h4",
                                    "tax.us.2025.f1098.source-closure|family-horizon=demo.f1098.h4,tax-year=2025",
                                    True)}}
                log.append(close_fourth, expected_revision=revision)
                roundtrip_contents = log.read()
                roundtrip_state = project(roundtrip_contents.acts, registry)
                observed_current_claims["third-removed-comparisons"] = (
                    current_mortgage_payment_comparison_applicability(
                        roundtrip_contents.acts, registry, state=roundtrip_state,
                        currency=compute_currency(roundtrip_state), lattice=facts_of(roundtrip_state.fact_state)))
            elif post_run_currency_mutation == "withdraw-proceeds-answer":
                withdraw_mortgage_borrowing_claim_durably(
                    log, registry, finding_id=shared_ids["what-the-money-paid-for"],
                    claim="what-the-money-paid-for", borrowing_ref=BORROWING_REF,
                    actor="demo.user.filer-1", at="2026-10-23T16:05:01Z",
                    expected_revision=log.read().revision,
                )
            elif post_run_currency_mutation == "correct-annual-ceiling":
                state = project(log.read().acts, registry)
                ceiling_fact_id = fact_id_for("tax.us.2025.f1098.borrowing-year-ceiling", (
                    ("borrowing", BORROWING_REF), ("tax-year", "2025"),
                ))
                current_ids = compute_currency(state).current_finding_ids
                ceiling_ids = [finding_id for finding_id, finding in state.findings.items()
                               if finding_id in current_ids and finding.get("fact_id") == ceiling_fact_id]
                if len(ceiling_ids) != 1:
                    raise AssertionError(f"expected one current exact annual ceiling, found {ceiling_ids}")
                correct_mortgage_borrowing_claim_durably(
                    log, registry, finding_id=ceiling_ids[0], claim="annual-ceiling",
                    borrowing_ref=BORROWING_REF, value=100000.0,
                    submission_id="demo.mortgage.currency-ceiling-correction",
                    evidence_id="demo.mortgage.currency-ceiling-correction.evidence",
                    actor="demo.user.filer-1", at="2026-10-23T16:05:01Z",
                    expected_revision=log.read().revision,
                )
            else:
                raise AssertionError(f"unknown post-run currency mutation {post_run_currency_mutation}")
            if observed_derived_currency is not None:
                kernel_currency = compute_currency(project(log.read().acts, registry))
                old_by_id = {publication.finding["id"]: publication.finding for publication in old_publications}
                derived_currency = compute_derivation_currency(kernel_currency, old_by_id)
                targets = {
                    "source_match": "tax.us.2025.f1098.affirmed-link-source-match|",
                    "witness": "tax.us.2025.mortgage.effective-proceeds-support-count|",
                    "coverage": "tax.us.2025.mortgage.report-effective-support-coverage|",
                    "reason": "tax.us.2025.f1098.residence-interest-reason|",
                    "line8a": "tax.us.2025.schedule-a.line8a",
                    "readiness": "tax.us.2025.mortgage.account-readiness|",
                    "line12e": "tax.us.2025.deductions.line-12e",
                }
                for label, symbol_prefix in targets.items():
                    matches = [finding for finding in old_by_id.values()
                               if str(finding.get("symbol", "")).startswith(symbol_prefix)]
                    observed_derived_currency[label] = [
                        {"id": finding["id"], "symbol": finding["symbol"],
                         "current": finding["id"] in derived_currency.current_derived_ids,
                         "pins": finding.get("pins", [])}
                        for finding in matches
                    ]
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "after-authority-change"), repo_root=ROOT,
                authoritative_acts=list(log.read().acts), workspace_revision=log.read().revision,
                run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"}, run_id="demo.mortgage.mapping.after-authority-change",
                governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
                output_name="after-authority-change.json")
            if outcome.refusal is not None:
                raise AssertionError(outcome.refusal)
            assert outcome.output_path is not None and outcome.presentation_path is not None
        if observed_publications is not None:
            assert outcome.publications is not None
            observed_publications.extend(dict(publication.finding) for publication in outcome.publications)
        if rerecord_removed_source and saved_before_removal is not None and saved_before_removal_paths is not None:
            assert outcome.output_path is not None and outcome.presentation_path is not None
            assert tuple(path.read_bytes() for path in saved_before_removal_paths) == saved_before_removal
            final_state = project(log.read().acts, registry)
            final_current = compute_currency(final_state).current_finding_ids
            if ("demo.f1098.rerecorded-box1" not in final_current
                    or link_ids[0] not in final_current):
                raise AssertionError("final coordinator inputs must include the restored source and explicitly corrected report link")
            final_line8a = [
                publication.finding for publication in (outcome.publications or ())
                if publication.finding.get("symbol") == "tax.us.2025.schedule-a.line8a"
            ]
            if len(final_line8a) != 1 or original_line8a_ids & {finding["id"] for finding in final_line8a}:
                raise AssertionError("restored coordinator result must be a new publication, with earlier saved artifacts unchanged")
            pins = final_line8a[0].get("pins", [])
            if not any(pin.get("id") == "demo.f1098.rerecorded-box1" for pin in pins):
                raise AssertionError("new coordinator publication must pin the fresh source finding")
        assert outcome.output_path is not None and outcome.presentation_path is not None
        report_model = _load(outcome.output_path)
        presentation_model = _load(outcome.presentation_path)
        if retain_saved_to is not None:
            retain_saved_to.mkdir(parents=True, exist_ok=False)
            (retain_saved_to / "report.json").write_bytes(outcome.output_path.read_bytes())
            (retain_saved_to / "presentation.json").write_bytes(outcome.presentation_path.read_bytes())
        return report_model, presentation_model, local_ids, shared_ids


def _run_empty_f1098_family(*, omit_closure: bool = False,
                            retained_borrowing: bool = False,
                            observed_publications: list[dict[str, Any]] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run the mortgage successor over a genuinely empty or unclosed source family."""
    acts = cast(list[dict[str, Any]], _f1098_acts(
        interest=None, itemized_assertion=1000.0, scope_flag_value=True,
    ))
    if omit_closure:
        acts = [row for row in acts if not (
            row.get("kind") == "assertion"
            and str(row.get("payload", {}).get("finding", {}).get("fact_id", "")).startswith(
                "tax.us.2025.f1098.source-closure|"
            )
        )]
    _add_line12e_base_answers(acts)
    adoption = acts[-1]
    package = _load(PACKAGE)
    adoption["payload"]["package"] = {
        "id": package["id"], "version": package["version"], "checksum": package["package_checksum"]
    }
    adoption["payload"]["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025", "version": "v55",
        "checksum": hashlib.sha256(RELEASE.read_bytes()).hexdigest(),
    }
    adoption["payload"]["revision"] = len(acts) - 1
    for index, row in enumerate(acts):
        row["committed_against"] = index
    with tempfile.TemporaryDirectory(prefix="mortgage-empty-family-") as tmp:
        if retained_borrowing:
            registry = tax_registry()
            log = ActLog(Path(tmp) / "recording", registry)
            log.append_batch(acts, expected_revision=0)
            introduce_mortgage_borrowing_reference_durably(
                log, registry, reference_id=BORROWING_REF, description="Synthetic retained mortgage borrowing",
                actor="demo.user.filer-1", at="2026-10-23T16:01:00Z",
            )
            for claim, value in (("annual-ceiling", 250000.0), ("other-secured-home-debt", "no")):
                record_mortgage_borrowing_claim_durably(
                    log, registry, claim=claim, borrowing_ref=BORROWING_REF, value=value,
                    submission_id=f"demo.mortgage.empty-retained.{claim}",
                    evidence_id=f"demo.mortgage.empty-retained-evidence.{claim}",
                    actor="demo.user.filer-1", at="2026-10-23T16:01:10Z",
                    expected_revision=log.read().revision,
                )
            acts = list(log.read().acts)
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "run"), repo_root=ROOT,
            authoritative_acts=acts, workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"}, scope_user="demo.user.filer-1",
            request={"schema": "run-request.v1"}, run_id=f"demo.mortgage.empty.{omit_closure}",
            governance_pins=[], surface=PublicationSurface(RELEASE_DIR, REGISTRY, CONTENT),
            output_name="report.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(outcome.refusal)
        assert outcome.output_path is not None and outcome.presentation_path is not None
        if observed_publications is not None:
            assert outcome.publications is not None
            observed_publications.extend(dict(publication.finding) for publication in outcome.publications)
        return _load(outcome.output_path), _load(outcome.presentation_path)


class MortgageBorrowingPackageTests(unittest.TestCase):
    def test_v57_admits_mortgage_successors_without_losing_main_v56_members(self) -> None:
        corpus = {}
        for path in CONTENT.glob("*.json"):
            citizen = _load(path)
            if isinstance(citizen, dict) and isinstance(citizen.get("id"), str) and isinstance(citizen.get("version"), str):
                corpus[(citizen["id"], citizen["version"])] = citizen

        base = _load(CONTENT / "package.core-calculations.v56.json")
        package = _load(PACKAGE)
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
        self.assertEqual(len(package["members"]), len(base["members"]) + 44)
        self.assertEqual(len(members - (base_members - expected_retired)), 48)
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
        coverage_position = member_order.index("tax.us.2025.rule.report-effective-support-coverage")
        witness_position = member_order.index(witness["id"])
        self.assertLess(reason_position, coverage_position)
        self.assertLess(coverage_position, witness_position)
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
        self.assertLess(resolved_coverage, resolved_witness)
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

        previous_registry = _load(CONTENT / "published-packages.v54.json")
        registry = _load(REGISTRY)
        self.assertTrue(set(map(json.dumps, previous_registry["packages"])) <= set(map(json.dumps, registry["packages"])))
        self.assertTrue(set(map(json.dumps, previous_registry["citizens"])) <= set(map(json.dumps, registry["citizens"])))
        entry = next(row for row in registry["packages"] if row["version"] == "v57")
        self.assertEqual(entry["checksum"], package["package_checksum"])
        self.assertEqual(
            _load(RELEASE)["package_registry_sha256"],
            hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
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
        for report_row in report_rows:
            observations = {item["factType"] for item in report_row["boxObservations"]}
            self.assertEqual(observations, {
                "tax.us.2025.f1098.box2-outstanding-principal",
                "tax.us.2025.f1098.box3-origination-date",
            })
            self.assertTrue(report_row["statementLabel"].get("statement"))
        legacy = copy.deepcopy(explanation)
        legacy["schema"] = "mortgage-borrowing-explanation.v1"
        legacy.pop("calculationChain")
        for row in legacy["reports"]:
            row.pop("answerConflicts")
            row.pop("paymentComparisons")
            row.pop("statementLabel")
            row.pop("boxObservations")
            for answer in [*row["localAnswers"], *row["effectiveAnswers"]]:
                answer.pop("title", None)
                answer.pop("valueLabel", None)
                answer.pop("consumption", None)
        for group_row in legacy["groups"]:
            group_row.pop("borrowingLabel")
            for claim in group_row["recordedApplicableClaims"].values():
                claim.pop("title", None)
                claim.pop("valueLabel", None)
        _validate_mortgage_borrowing_explanation(legacy)
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

    def test_offered_reviews_save_two_reports_and_reload_one_supported_result(self) -> None:
        retain_root = Path(tempfile.mkdtemp(prefix="mortgage-track3-offered-review-"))
        retained = retain_root / "saved"
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, through_reviews=True, include_line12e_base_answers=True,
            retain_saved_to=retained)
        self.assertEqual(_load(retained / "report.json"), report)
        self.assertEqual(_load(retained / "presentation.json"), model)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(report["authorization_status"], "AUTHORIZATION_ABSENT")
        self.assertEqual([row["reportedInterest"]["value"] for row in explanation["reports"]], [22000.0, 3500.0])
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500.0)
        chain = explanation["calculationChain"]
        self.assertTrue(any(pub["symbol"].startswith("tax.us.2025.f1098.principal-within-ceiling|")
                            for pub in chain["publications"]))
        self.assertTrue(any(row["artifact_id"] == "tax.us.2025.rule.f1098-line8a"
                            for row in chain["dispositions"]))
        line8a_rule = next(member for member in chain["resolvedContent"]
                           if member.get("id") == "tax.us.2025.rule.f1098-line8a")
        limit_parameter = next(member for member in chain["resolvedContent"]
                               if member.get("id") == "tax.us.2025.f1098.mortgage-interest-limit")
        self.assertEqual(line8a_rule["version"], "v5")
        self.assertTrue(any("1987-10-13" in str(member.get("value"))
                            for member in chain["resolvedContent"]))
        self.assertEqual(limit_parameter["values"]["single"], "750000")
        self.assertTrue(all(answer["consumption"] in {"consumed", "available-not-consumed"}
                            for row in explanation["reports"] for answer in row["effectiveAnswers"]))
        line12e = next(row for row in model["sections"] if row["id"] == "line-12e")
        self.assertEqual(line12e["resolved"]["disposition"], "published_value")
        self.assertEqual(line12e["resolved"]["value"], 25500.0)

    def test_offered_refinance_answers_save_truthful_recognition_and_withhold(self) -> None:
        retained = Path(tempfile.mkdtemp(prefix="mortgage-refinance-review-")) / "saved"
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, through_reviews=True, include_line12e_base_answers=True,
            local_overrides={"this-is-the-original-loan": "no"},
            shared_overrides={"this-is-the-original-loan": "no"},
            retain_saved_to=retained)
        self.assertEqual(_load(retained / "report.json"), report)
        self.assertEqual(_load(retained / "presentation.json"), model)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertTrue(all(row["reasonChain"]["value"] == "refinance"
                            for row in explanation["reports"]))
        claims = explanation["groups"][0]["recordedApplicableClaims"]
        recognition = claims["tax.us.2025.mortgage.continuing-borrowing"]
        self.assertEqual(recognition["value"], "yes")
        self.assertNotIn("original", recognition["title"].lower())
        originality = claims["tax.us.2025.mortgage.shared-original-loan"]
        self.assertEqual(originality["value"], "no")
        self.assertIn("original", originality["title"].lower())

    def test_late_member_is_reclosed_and_recorded_through_offered_review(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            late_third_report=True, fully_supported_local=True, through_reviews=True)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["reports"]), 3)
        late = next(row for row in explanation["reports"] if row["statement"] == "demo.f1098.stmt.c")
        self.assertEqual(late["reportedInterest"]["value"], 1900.0)
        self.assertEqual(len(late["relationships"]), 1)
        self.assertEqual(late["relationships"][0]["disposition"], "affirmed")
        self.assertEqual(len(late["localAnswers"]), 9)
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")

    def test_reviewed_clear_keeps_other_debt_and_two_reports_do_not_become_singleton(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, through_reviews=True, clear_account=True)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["reports"]), 2)
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        claims = explanation["groups"][0]["recordedApplicableClaims"]
        self.assertEqual(claims["tax.us.2025.mortgage.other-secured-home-debt"]["value"], "no")
        self.assertNotIn("tax.us.2025.mortgage.continuing-borrowing", claims)

    def test_removed_exact_source_restores_only_after_fresh_assertion_and_link_confirmation(self) -> None:
        observed: dict[str, Any] = {}
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, through_reviews=True, remove_first_report=True,
            rerecord_removed_source=True, observed_current_claims=observed)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["reports"]), 2)
        self.assertEqual({row["statement"] for row in explanation["reports"]},
                         {"demo.f1098.stmt.a", "demo.f1098.stmt.b"})
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "published")
        prior = set(observed["prior_payment_comparison_ids"].values())
        current = observed["payment-comparison-applicability"]
        self.assertEqual(len(current), 2)
        self.assertTrue(all(row["applicability"] == "current" for row in current))
        self.assertTrue(prior.isdisjoint({row["finding_id"] for row in current}))
        self.assertTrue(all(row["applicability"] == "current"
                            for report in explanation["reports"]
                            for row in report["paymentComparisons"]))

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
        observed: dict[str, Any] = {}
        report, model, _local_ids, _shared_ids = _run_connected_case(
            unlinked_third_report=True, fully_supported_local=True, include_line12e_base_answers=True,
            observed_current_claims=observed,
        )
        self.assertEqual(report["authorization_status"], "AUTHORIZATION_ABSENT")
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(explanation["line8aFindings"], [])
        line12e = next(row for row in model["sections"] if row["id"] == "line-12e")
        self.assertEqual(line12e["resolved"]["disposition"], "blocked")
        self.assertEqual(len(observed["payment-comparison-applicability"]), 2)
        self.assertTrue(all(row["applicability"] == "current"
                            for row in observed["payment-comparison-applicability"]))
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

    def test_connected_line12e_uses_schedule_a_and_saves_both_report_rows(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, include_line12e_base_answers=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        line8a = explanation["line8aFindings"][0]
        report_box1_ids = {row["reportedInterest"]["findingId"] for row in explanation["reports"]}
        self.assertEqual(line8a["value"], 25500.0)
        self.assertTrue(report_box1_ids <= {pin.get("id") for pin in line8a["pins"]})
        line12e = next(row for row in model["sections"] if row["id"] == "line-12e")
        self.assertEqual(line12e["resolved"]["disposition"], "published_value")
        self.assertEqual(line12e["resolved"]["value"], 25500.0)
        line12e_row = next(row for row in report["dispositions"]
                           if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e")
        self.assertEqual(line12e_row["disposition"], "published")
        schedule_total_row = next(row for row in report["dispositions"]
                                  if row.get("symbol") == "tax.us.2025.schedule-a.total")
        self.assertEqual(schedule_total_row["disposition"], "published")
        line12e_rule = _load(CONTENT / "rule.form1040-line12e.v2.json")
        self.assertIn("tax.us.2025.schedule-a.total", line12e_rule["requires"])
        self.assertIn("tax.us.2025.schedule-a.total", {pin["id"] for pin in line12e_rule["pins"]})
        attachment = next(row for row in model["attachments"]
                          if row["id"] == "tax.us.2025.rule.attachment.schedule-a")
        self.assertEqual(attachment["resolved"]["disposition"], "published")
        group = next(row for row in model["citationGroups"]
                     if row["id"] == "tax.us.2025.rule.attachment.schedule-a")
        attachment_source_ids = {site["pinId"] for site in group["parts"][0]["citationSites"]}
        self.assertTrue(report_box1_ids <= attachment_source_ids)
        tie_out = group["parts"][0]["tieOutText"]
        subtotal = re.search(r"Reported subtotal: ([0-9.]+)", tie_out)
        assert subtotal is not None, tie_out
        self.assertEqual(float(subtotal.group(1)), 25500.0)

    def test_equal_copy_reports_withhold_line8a_and_line12e(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, through_reviews=True, second_interest=22000.0,
            payment_comparison="copy-or-correction", include_line12e_base_answers=True)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual([row["reportedInterest"]["value"] for row in explanation["reports"]], [22000.0, 22000.0])
        for row in explanation["reports"]:
            comparison = row["paymentComparisons"][0]
            self.assertEqual(comparison["value"], "copy-or-correction")
            self.assertEqual(comparison["applicability"], "current")
            self.assertIn("correct the existing report", comparison["explanation"])
        self.assertEqual(explanation["line8aFindings"], [])
        line8a = next(row for row in report["dispositions"]
                      if row.get("artifact_id") == "tax.us.2025.rule.f1098-line8a")
        self.assertEqual(line8a["disposition"], "blocked")
        line12e = next(row for row in report["dispositions"]
                       if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e")
        self.assertEqual(line12e["disposition"], "blocked")
        self.assertNotEqual(line12e.get("value"), 0)

    def test_equal_distinct_payments_publish_both_lines_once(self) -> None:
        observed: dict[str, Any] = {}
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, through_reviews=True, second_interest=22000.0,
            payment_comparison="different-payments", include_line12e_base_answers=True,
            observed_current_claims=observed)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual([row["reportedInterest"]["value"] for row in explanation["reports"]], [22000.0, 22000.0])
        reloaded_model = json.loads(json.dumps(model))
        validate_presentation_model(reloaded_model)
        self.assertEqual(reloaded_model["mortgageBorrowingExplanation"]["schema"],
                         "mortgage-borrowing-explanation.v4")
        comparison_support_ids: set[str] = set()
        for row in reloaded_model["mortgageBorrowingExplanation"]["reports"]:
            comparisons = row["paymentComparisons"]
            self.assertEqual(len(comparisons), 1)
            self.assertEqual(comparisons[0]["value"], "different-payments")
            self.assertEqual(comparisons[0]["applicability"], "current")
            self.assertEqual(len(comparisons[0]["supportFindingIds"]), 5)
            comparison_support_ids.update(comparisons[0]["supportFindingIds"])
        prior_v3 = json.loads(json.dumps(reloaded_model))
        prior_v3["mortgageBorrowingExplanation"]["schema"] = "mortgage-borrowing-explanation.v3"
        for row in prior_v3["mortgageBorrowingExplanation"]["reports"]:
            for comparison in row["paymentComparisons"]:
                comparison.pop("peerIdentityStatus")
        validate_presentation_model(prior_v3)
        self.assertEqual(explanation["line8aFindings"][0]["value"], 44000.0)
        line12e = next(row for row in model["sections"] if row["id"] == "line-12e")
        self.assertEqual(line12e["resolved"]["disposition"], "published_value")
        self.assertEqual(line12e["resolved"]["value"], 44000.0)
        for symbol in ("tax.us.2025.schedule-a.line8a", "tax.us.2025.deductions.line-12e"):
            publication = next(row for row in report["dispositions"] if row.get("symbol") == symbol)
            self.assertEqual(publication["disposition"], "published")
        applicability = observed["payment-comparison-applicability"]
        self.assertEqual(len(applicability), 2)
        self.assertTrue(all(row["applicability"] == "current" for row in applicability))
        expected_support_ids: set[str] = set()
        for row in applicability:
            support = row["comparison_support"]
            expected_support_ids.add(support["recognition_finding_id"])
            for report_support in support["reports"]:
                expected_support_ids.add(report_support["box1_finding_id"])
                expected_support_ids.add(report_support["inclusion_finding_id"])
        self.assertEqual(comparison_support_ids, expected_support_ids)
        gate_rows = [row for row in report["dispositions"]
                     if row.get("artifact_id") == "tax.us.2025.rule.mortgage-payment-comparison-support-count"]
        self.assertEqual(len(gate_rows), 1)
        self.assertEqual(gate_rows[0]["disposition"], "published")
        self.assertTrue(expected_support_ids <= {pin.get("id") for pin in gate_rows[0].get("pins", [])})

    def test_missing_two_report_comparisons_withhold_both_final_lines(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_interest=22000.0, payment_comparison=None,
            include_line12e_base_answers=True)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        line8a = next(row for row in report["dispositions"]
                      if row.get("artifact_id") == "tax.us.2025.rule.f1098-line8a")
        self.assertEqual(line8a["disposition"], "blocked")
        line12e = next(row for row in report["dispositions"]
                       if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e")
        self.assertEqual(line12e["disposition"], "blocked")

    def test_ordinary_asserted_support_markers_cannot_publish_two_report_total(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_interest=22000.0, payment_comparison=None,
            asserted_payment_support_markers=True, include_line12e_base_answers=True)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        for artifact_id in ("tax.us.2025.rule.f1098-line8a", "tax.us.2025.rule.form1040-line12e"):
            row = next(row for row in report["dispositions"] if row.get("artifact_id") == artifact_id)
            self.assertEqual(row["disposition"], "blocked")

    def test_duplicate_current_reading_cannot_cover_unresolved_peer_report(self) -> None:
        from packages.derivation import live as live_module

        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_interest=22000.0,
            unresolved_comparison_index=1, include_line12e_base_answers=True)
        self.assertEqual(model["mortgageBorrowingExplanation"]["line8aFindings"], [])
        for artifact_id in ("tax.us.2025.rule.f1098-line8a", "tax.us.2025.rule.form1040-line12e"):
            self.assertEqual(next(row for row in report["dispositions"]
                                  if row.get("artifact_id") == artifact_id)["disposition"], "blocked")

        original_reader = live_module._mortgage_payment_comparison_applicability
        observed: list[dict[str, Any]] = []

        def duplicate_a(*args: Any, **kwargs: Any) -> list[dict[str, Any]]:
            readings = original_reader(*args, **kwargs)
            self.assertEqual(len(readings), 2)
            reading_a = next(row for row in readings if row["statement"]["payer"] == "demo.f1098.lender.a")
            reading_b = next(row for row in readings if row["statement"]["payer"] == "demo.f1098.lender.b")
            self.assertEqual(reading_a["applicability"], "current")
            self.assertEqual(reading_b["applicability"], "unresolved-applicability")
            observed.extend(readings)
            return [reading_a, dict(reading_a), reading_b]

        with patch.object(live_module, "_mortgage_payment_comparison_applicability", side_effect=duplicate_a):
            with self.assertRaisesRegex(MortgagePaymentApplicabilityInvalid,
                                        "repeats a current comparison"):
                _run_connected_case(fully_supported_local=True, second_interest=22000.0,
                                    unresolved_comparison_index=1, include_line12e_base_answers=True)

        self.assertEqual(len(observed), 2)

    def test_missing_peer_context_saves_a_blocked_comparison_explanation(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_interest=22000.0, payment_comparison=None,
            direct_unresolved_comparison=True, include_line12e_base_answers=True)
        explanation = model["mortgageBorrowingExplanation"]
        comparison = next(item for row in explanation["reports"] for item in row["paymentComparisons"])
        self.assertEqual(comparison["applicability"], "unresolved-applicability")
        self.assertIsNone(comparison["peer"])
        self.assertEqual(comparison["peerIdentityStatus"], "unavailable")
        self.assertIn("peer report identity is unavailable", comparison["explanation"])
        self.assertEqual(explanation["line8aFindings"], [])
        for artifact_id in ("tax.us.2025.rule.f1098-line8a", "tax.us.2025.rule.form1040-line12e"):
            self.assertEqual(next(row for row in report["dispositions"]
                                  if row.get("artifact_id") == artifact_id)["disposition"], "blocked")

    def test_link_correction_keeps_old_comparison_visible_but_unusable(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_interest=22000.0, payment_comparison="different-payments",
            link_outcome="affirmed", include_line12e_base_answers=True)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        old_comparisons = [comparison for row in explanation["reports"]
                           for comparison in row["paymentComparisons"]]
        self.assertEqual(len(old_comparisons), 2)
        self.assertTrue(all(row["value"] == "different-payments" for row in old_comparisons))
        self.assertTrue(all(row["applicability"] == "unresolved-applicability" for row in old_comparisons))
        self.assertTrue(all("not used" in row["explanation"] for row in old_comparisons))
        self.assertTrue(all(row["findingId"] for row in old_comparisons))
        self.assertEqual(next(row for row in report["dispositions"]
                              if row.get("artifact_id") == "tax.us.2025.rule.f1098-line8a")["disposition"], "blocked")

    def test_exact_pair_survives_third_report_roundtrip_but_old_derived_amount_does_not(self) -> None:
        observed_claims: dict[str, Any] = {}
        observed_derived: dict[str, Any] = {}
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_interest=22000.0, payment_comparison="different-payments",
            include_line12e_base_answers=True, observed_current_claims=observed_claims,
            observed_derived_currency=observed_derived,
            post_run_currency_mutation="third-report-roundtrip")
        self.assertEqual(len(observed_claims["third-present-comparisons"]), 2)
        self.assertTrue(all(row["applicability"] == "current"
                            for row in observed_claims["third-present-comparisons"]))
        self.assertEqual(len(observed_claims["third-removed-comparisons"]), 2)
        self.assertTrue(all(row["applicability"] == "current"
                            for row in observed_claims["third-removed-comparisons"]))
        for name in ("line8a", "line12e"):
            old_rows = observed_derived[name]
            self.assertEqual(len(old_rows), 1)
            self.assertFalse(old_rows[0]["current"])
        self.assertEqual(model["mortgageBorrowingExplanation"]["line8aFindings"][0]["value"], 44000.0)
        line12e = next(row for row in model["sections"] if row["id"] == "line-12e")
        self.assertEqual(line12e["resolved"]["disposition"], "published_value")
        self.assertEqual(line12e["resolved"]["value"], 44000.0)
        current_line8a = next(row for row in report["dispositions"]
                              if row.get("symbol") == "tax.us.2025.schedule-a.line8a")
        self.assertEqual(current_line8a["disposition"], "published")

    def test_connected_schedule_a_missing_one_boundary_blocks_attachment(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, include_line12e_base_answers=True,
            missing_schedule_a_boundary="no-charitable-declared",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500.0)
        attachment = next(row for row in model["attachments"]
                          if row["id"] == "tax.us.2025.rule.attachment.schedule-a")
        self.assertEqual(attachment["resolved"]["disposition"], "blocked")
        attachment_row = next(row for row in report["dispositions"]
                              if row.get("artifact_id") == "tax.us.2025.rule.attachment.schedule-a")
        self.assertEqual(attachment_row["disposition"], "blocked")
        self.assertIn("tax.us.2025.schedule-a-boundary.no-charitable-declared",
                      attachment_row.get("missing", []))

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
            shared_only=True, shared_overrides={question: value},
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        effective_type, reason_value = {
            "no-one-else-owes-it": (
                "tax.us.2025.f1098.effective-no-one-else-owes-it", "outside-co-obligor",
            ),
            "mortgage-credit-certificate-received": (
                "tax.us.2025.f1098.effective-credit-certificate", "certificate-received",
            ),
        }[question]
        rows = [row for row in report["dispositions"]
                if str(row.get("symbol", "")).startswith(f"{effective_type}|")]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["disposition"] == "published" for row in rows))
        for report_row in explanation["reports"]:
            effective = next(answer for answer in report_row["effectiveAnswers"]
                             if answer["factType"] == effective_type)
            self.assertEqual(effective["value"], value)
            self.assertEqual(report_row["reasonChain"]["value"], reason_value)

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

    def test_saved_original_loan_conflict_names_scopes_values_and_correction_path(self) -> None:
        _report, model, local_ids, shared_ids = _run_connected_case(
            fully_supported_local=True,
            local_overrides={"this-is-the-original-loan": "no"},
            shared_overrides={"this-is-the-original-loan": "yes"},
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        conflicts = [conflict for report in explanation["reports"]
                     for conflict in report["answerConflicts"]
                     if conflict["question"] == "Is this the original loan?"]
        self.assertEqual(len(conflicts), 2)
        for conflict in conflicts:
            self.assertEqual(conflict["local"]["scope"], "this exact Form 1098")
            self.assertEqual(conflict["local"]["value"], "no")
            self.assertIn(conflict["local"]["findingId"], local_ids.values())
            self.assertEqual(conflict["shared"]["scope"], "this named borrowing for 2025")
            self.assertEqual(conflict["shared"]["value"], "yes")
            self.assertEqual(conflict["shared"]["findingId"], shared_ids["this-is-the-original-loan"])
            self.assertIn("Correct the answer at the scope where it is wrong", conflict["correctionGuidance"])
            self.assertIn("does not choose", conflict["correctionGuidance"])

    def test_report_b_local_answer_cannot_fill_missing_a(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            missing_shared="owes-the-loan", missing_local="owes-the-loan", fully_supported_local=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        effective_type = "tax.us.2025.f1098.effective-owes-the-loan"
        rows = [row for row in report["dispositions"]
                if str(row.get("symbol", "")).startswith(f"{effective_type}|")]
        self.assertEqual(len(rows), 2)
        by_report = {"demo.f1098.stmt.a": None, "demo.f1098.stmt.b": None}
        for row in rows:
            symbol = str(row["symbol"])
            statement = next(name for name in by_report if f"statement={name}" in symbol)
            by_report[statement] = row["disposition"]
        self.assertEqual(by_report, {"demo.f1098.stmt.a": "blocked", "demo.f1098.stmt.b": "published"})
        saved_a, saved_b = explanation["reports"]
        self.assertFalse(any(answer["factType"] == LOCAL_FACTS["owes-the-loan"]
                             for answer in saved_a["localAnswers"]))
        saved_b_effective = next(answer for answer in saved_b["effectiveAnswers"]
                                 if answer["factType"] == effective_type)
        self.assertEqual(saved_b_effective["value"], "yes")
        self.assertIsNone(saved_a["reasonChain"])
        self.assertEqual(saved_b["reasonChain"]["value"], "qualified")

    def test_shared_correction_uses_only_current_favorable_finding(self) -> None:
        report, model, _local_ids, shared_ids = _run_connected_case(
            uncertain_shared="what-the-money-paid-for", correct_shared="what-the-money-paid-for",
            fully_supported_local=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500.0)
        claims = explanation["groups"][0]["recordedApplicableClaims"]
        proceeds = claims["tax.us.2025.mortgage.shared-proceeds-use"]
        self.assertEqual(proceeds["findingId"], shared_ids["what-the-money-paid-for"])
        self.assertEqual(proceeds["value"], "bought-the-home")
        self.assertNotIn("cannot-tell", {row.get("value") for row in claims.values()})
        old_id = shared_ids["previous:what-the-money-paid-for"]
        effective_type = "tax.us.2025.f1098.effective-proceeds-use"
        for report_row in explanation["reports"]:
            symbol = next(
                str(row["symbol"]) for row in report["dispositions"]
                if str(row.get("symbol", "")).startswith(f"{effective_type}|")
                and f"statement={report_row['statement']}" in str(row.get("symbol"))
            )
            effective_row = next(row for row in report["dispositions"] if row.get("symbol") == symbol)
            self.assertEqual(effective_row["disposition"], "published")
            effective_pins = {pin.get("id") for pin in effective_row["pins"]}
            self.assertIn(shared_ids["what-the-money-paid-for"], effective_pins)
            self.assertNotIn(old_id, effective_pins)
            self.assertIn(effective_row["finding_id"],
                          {pin.get("id") for pin in report_row["reasonChain"]["pins"]})

    def test_shared_withdrawal_leaves_independent_local_support(self) -> None:
        report, model, local_ids, _shared_ids = _run_connected_case(
            withdraw_shared="what-the-money-paid-for", fully_supported_local=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500.0)
        for report_index, row in enumerate(explanation["reports"]):
            self.assertEqual(row["reasonChain"]["value"], "qualified")
            local_fallback = next(
                answer for answer in row["effectiveAnswers"]
                if answer["factType"] == "tax.us.2025.f1098.effective-proceeds-use"
            )
            self.assertIn(local_ids[f"{report_index}:what-the-money-paid-for"],
                          {pin.get("id") for pin in local_fallback["pins"]})
            self.assertTrue(_has_transitive_pin(
                report, local_ids[f"{report_index}:what-the-money-paid-for"],
                {pin.get("id") for pin in row["reasonChain"]["pins"]},
            ))
        shared_proceeds = "tax.us.2025.mortgage.shared-proceeds-use"
        self.assertNotIn(shared_proceeds, explanation["groups"][0]["recordedApplicableClaims"])

    def test_kernel_rejects_test_only_candidate_finding_pins(self) -> None:
        with self.assertRaisesRegex(FindingModelError, "derived finding pins are not admitted"):
            _run_connected_case(fully_supported_local=True, post_run_currency_mutation="remove-box1",
                                emit_test_candidate_pin=True)

    def test_retained_source_match_and_downstream_currency_on_box1_withdrawal(self) -> None:
        retained: dict[str, Any] = {}
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, include_line12e_base_answers=True,
            post_run_currency_mutation="remove-box1", observed_derived_currency=retained,
        )
        self.assertEqual(len(retained["source_match"]), 2)
        source_a = [row for row in retained["source_match"] if "statement=demo.f1098.stmt.a" in row["symbol"]]
        source_b = [row for row in retained["source_match"] if "statement=demo.f1098.stmt.b" in row["symbol"]]
        self.assertEqual(len(source_a), 1)
        self.assertFalse(source_a[0]["current"], source_a)
        self.assertEqual(len(source_b), 1)
        self.assertTrue(source_b[0]["current"], source_b)
        self.assertFalse(any(
            row.get("symbol", "").startswith("tax.us.2025.f1098.affirmed-link-source-match|")
            and "statement=demo.f1098.stmt.a" in row.get("symbol", "")
            and row.get("disposition") == "published"
            for row in report["dispositions"]
        ))
        for key in ("line8a", "readiness", "line12e"):
            self.assertGreater(len(retained[key]), 0, retained)
            self.assertTrue(all(not row["current"] for row in retained[key]), retained[key])
        self.assertFalse(any(
            row.get("symbol") == "tax.us.2025.schedule-a.line8a" and row.get("disposition") == "published"
            for row in report["dispositions"]
        ))

    def test_retained_support_witness_currency_on_answer_withdrawal(self) -> None:
        retained: dict[str, Any] = {}
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, include_line12e_base_answers=True,
            post_run_currency_mutation="withdraw-proceeds-answer", observed_derived_currency=retained,
        )
        self.assertEqual(len(retained["witness"]), 2)
        for key in ("witness", "coverage", "reason"):
            self.assertEqual(len(retained[key]), 2, retained[key])
            self.assertTrue(all(not row["current"] for row in retained[key]), retained[key])
        for key in ("line8a", "line12e"):
            self.assertGreater(len(retained[key]), 0, retained)
            self.assertTrue(all(not row["current"] for row in retained[key]), retained[key])

    def test_readiness_and_line12e_currency_through_ceiling_and_line8a(self) -> None:
        retained: dict[str, Any] = {}
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, include_line12e_base_answers=True,
            post_run_currency_mutation="correct-annual-ceiling", observed_derived_currency=retained,
        )
        for key in ("readiness", "line8a", "line12e"):
            self.assertGreater(len(retained[key]), 0, retained)
            self.assertTrue(all(not row["current"] for row in retained[key]), retained[key])
        self.assertEqual(model["mortgageBorrowingExplanation"]["line8aFindings"], [])
        self.assertFalse(any(
            row.get("symbol") == "tax.us.2025.mortgage.account-readiness|"
            and row.get("disposition") == "published"
            for row in report["dispositions"]
        ))

    def test_root_withdrawal_with_affirmed_link_does_not_restore_singleton(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            single_current_report=True, fully_supported_local=True, root_outcome="withdrawn",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["reports"]), 1)
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(len(explanation["groups"]), 1)
        claims = explanation["groups"][0]["recordedApplicableClaims"]
        self.assertEqual(claims["tax.us.2025.mortgage.continuing-borrowing-withdrawn"]["value"], "withdrawn")
        self.assertEqual(explanation["reports"][0]["relationships"][0]["disposition"], "affirmed")

    def test_explicit_clear_single_report_allows_only_local_legacy_amount(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            single_current_report=True, fully_supported_local=True, clear_account=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["reports"]), 1)
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        self.assertEqual(explanation["line8aFindings"][0]["value"], 22000.0)
        self.assertEqual(explanation["reports"][0]["reasonChain"]["value"], "qualified")

    def test_explicit_clear_two_reports_blocks_subset_amount(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, clear_account=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["reports"]), 2)
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")

    def test_explicit_clear_single_report_unpaid_interest_is_known_zero(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            single_current_report=True, fully_supported_local=True, clear_account=True,
            local_overrides={"paid-the-interest": "no"},
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        self.assertEqual(explanation["line8aFindings"][0]["value"], 0)
        self.assertEqual(explanation["reports"][0]["reasonChain"]["value"], "not-paid")

    def test_explicit_clear_single_report_missing_local_answer_is_unresolved(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            single_current_report=True, fully_supported_local=True, clear_account=True,
            missing_local="paid-the-interest",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertIsNone(explanation["reports"][0]["reasonChain"])

    def test_withdrawn_final_report_link_does_not_restore_singleton(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            single_current_report=True, fully_supported_local=True, withdraw_link=0,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(explanation["reports"][0]["relationships"][0]["disposition"], "withdrawn")

    def test_missing_exact_report_link_blocks_connected_amount(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, missing_link=0,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(explanation["reports"][0]["relationships"], [])

    def test_denied_exact_report_link_blocks_without_becoming_withdrawn(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, link_outcome="denied",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(explanation["reports"][0]["relationships"][0]["disposition"], "denied")

    def test_cannot_tell_exact_report_link_blocks_without_becoming_denied(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, link_outcome="cannot-tell",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(explanation["reports"][0]["relationships"][0]["disposition"], "cannot-tell")

    def test_closed_empty_f1098_family_is_not_a_mortgage_subject(self) -> None:
        publications: list[dict[str, Any]] = []
        _report, model = _run_empty_f1098_family(observed_publications=publications)
        self.assertNotIn("mortgageBorrowingExplanation", model)
        rows = [row for row in _report["dispositions"]
                if row.get("artifact_id") == "tax.us.2025.rule.f1098-line8a"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "inapplicable")
        empty_total = [row for row in _report["dispositions"]
                       if row.get("artifact_id") == "tax.us.2025.rule.schedule-a-total-closed-empty"]
        self.assertEqual(len(empty_total), 1)
        self.assertEqual(empty_total[0]["disposition"], "published")
        schedule_total = next(row for row in publications if row["symbol"] == "tax.us.2025.schedule-a.total")
        self.assertEqual(float(schedule_total["value"]), 0.0)
        line12e = [row for row in _report["dispositions"]
                   if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e"]
        self.assertEqual(len(line12e), 1)
        self.assertEqual(line12e[0]["disposition"], "published")

    def test_missing_f1098_closure_does_not_become_closed_empty(self) -> None:
        _report, model = _run_empty_f1098_family(omit_closure=True)
        self.assertNotIn("mortgageBorrowingExplanation", model)
        rows = [row for row in _report["dispositions"]
                if row.get("artifact_id") == "tax.us.2025.rule.f1098-line8a"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(rows[0]["missing"], ["tax.us.2025.f1098"])
        self.assertNotIn("tax.us.2025.schedule-a.line8a", {row.get("symbol") for row in rows})
        line12e = [row for row in _report["dispositions"]
                   if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e"]
        self.assertEqual(len(line12e), 1)
        self.assertEqual(line12e[0]["disposition"], "blocked")

    def test_removing_sole_linked_report_keeps_zero_total_and_blocks_orphaned_line12e(self) -> None:
        publications: list[dict[str, Any]] = []
        current_claims: dict[str, Any] = {}
        report, model, _local_ids, _shared_ids = _run_connected_case(
            single_current_report=True, fully_supported_local=True,
            include_line12e_base_answers=True, remove_only_report=True,
            observed_current_claims=current_claims,
            observed_publications=publications,
        )
        self.assertEqual(current_claims["report-inclusion:0"]["value"], "affirmed")
        self.assertTrue(current_claims["report-inclusion:0"]["is_current"])
        self.assertEqual(current_claims["report-inclusion:0"]["fact_type"], LINK_TYPE)
        total = next(row for row in report["dispositions"]
                     if row.get("artifact_id") == "tax.us.2025.rule.schedule-a-total-closed-empty")
        self.assertEqual(total["disposition"], "published")
        schedule_total = next(row for row in publications if row["symbol"] == "tax.us.2025.schedule-a.total")
        self.assertEqual(float(schedule_total["value"]), 0.0)
        line12e = next(row for row in report["dispositions"]
                       if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e")
        self.assertEqual(line12e["disposition"], "blocked")
        self.assertEqual(line12e["code"], "DEPENDENCY_ABSENT")
        self.assertIn("tax.us.2025.f1098-inclusion-integrity", line12e["missing"])
        self.assertEqual(model["mortgageBorrowingExplanation"]["line8aFindings"], [])
        orphans = model["mortgageBorrowingExplanation"]["orphanRelationships"]
        self.assertEqual(len(orphans), 1)
        self.assertEqual(orphans[0]["factType"], LINK_TYPE)
        self.assertEqual(orphans[0]["response"], "affirmed")

    def test_closed_empty_retained_account_claims_add_no_mortgage_prerequisite(self) -> None:
        publications: list[dict[str, Any]] = []
        report, model = _run_empty_f1098_family(
            retained_borrowing=True, observed_publications=publications,
        )
        self.assertNotIn("mortgageBorrowingExplanation", model)
        line8a = next(row for row in report["dispositions"]
                      if row.get("artifact_id") == "tax.us.2025.rule.f1098-line8a")
        self.assertEqual(line8a["disposition"], "inapplicable")
        total = next(row for row in report["dispositions"]
                     if row.get("artifact_id") == "tax.us.2025.rule.schedule-a-total-closed-empty")
        self.assertEqual(total["disposition"], "published")
        schedule_total = next(row for row in publications if row["symbol"] == "tax.us.2025.schedule-a.total")
        self.assertEqual(float(schedule_total["value"]), 0.0)
        line12e = next(row for row in report["dispositions"]
                       if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e")
        self.assertEqual(line12e["disposition"], "published")

    def test_affirmed_link_to_removed_report_is_orphan(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, include_line12e_base_answers=True,
            remove_first_report=True,
        )
        line12e = [row for row in report["dispositions"]
                   if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e"]
        self.assertEqual(len(line12e), 1)
        self.assertEqual(line12e[0]["disposition"], "blocked")
        self.assertEqual(line12e[0]["code"], "DEPENDENCY_ABSENT")
        self.assertIn("tax.us.2025.f1098-inclusion-integrity", line12e[0]["missing"])
        self.assertEqual(model["mortgageBorrowingExplanation"]["line8aFindings"], [])

    def test_withdrawn_link_to_removed_report_is_not_affirmative_orphan(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, include_line12e_base_answers=True,
            remove_first_report=True, withdraw_link=0,
        )
        line12e = [row for row in report["dispositions"]
                   if row.get("artifact_id") == "tax.us.2025.rule.form1040-line12e"]
        self.assertEqual(len(line12e), 1)
        self.assertEqual(line12e[0]["disposition"], "published")
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        self.assertEqual(explanation["line8aFindings"][0]["value"], 3500)
        self.assertEqual(explanation["reports"][0]["relationships"][0]["disposition"], "affirmed")

    def test_two_active_borrowing_roots_do_not_merge_report_amounts(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_active_borrowing=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")

    def test_connected_mfs_ceiling_above_375k_limit_blocks(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, annual_ceiling=500000.0,
            filing_status="married_filing_separately",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")

    def test_connected_single_ceiling_500k_with_lower_principal_publishes(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, annual_ceiling=500000.0,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500)

    def test_connected_origination_on_1987_cutoff_blocks_amount(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, first_box3="1987-10-13",
            second_box3="1987-10-13",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")

    def test_connected_origination_after_1987_cutoff_remains_supported(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, first_box3="1987-10-14",
            second_box3="1987-10-14",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(len(explanation["line8aFindings"]), 1)
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500)

    def test_dormant_borrowing_cannot_supply_a_missing_a_account_answer(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, dormant_borrowing=True,
            missing_account_claim="other-secured-home-debt",
        )
        readiness_rows = [row for row in report["dispositions"]
                          if row.get("artifact_id") == "tax.us.2025.rule.mortgage-account-readiness"]
        self.assertFalse(any(row.get("disposition") == "published" and BORROWING_REF in str(row.get("symbol"))
                             for row in readiness_rows), readiness_rows)
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(len(explanation["line8aDispositions"]), 1)
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        a_group = next(group for group in explanation["groups"] if group["borrowing"] == BORROWING_REF)
        self.assertNotIn("tax.us.2025.mortgage.other-secured-home-debt",
                         a_group["recordedApplicableClaims"])

    def test_dormant_borrowing_with_complete_a_support_does_not_add_a_subject(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, dormant_borrowing=True,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"][0]["value"], 25500.0)
        readiness_rows = [row for row in report["dispositions"]
                          if row.get("artifact_id") == "tax.us.2025.rule.mortgage-account-readiness"
                          and row.get("disposition") == "published"]
        self.assertEqual(len(readiness_rows), 1)
        self.assertIn(BORROWING_REF, str(readiness_rows[0].get("symbol")))

    def test_dormant_borrowing_ceiling_cannot_supply_a_missing_a_ceiling(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, dormant_borrowing=True,
            missing_account_claim="annual-ceiling",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        readiness_rows = [row for row in report["dispositions"]
                          if row.get("artifact_id") == "tax.us.2025.rule.mortgage-account-readiness"]
        self.assertFalse(any(row.get("disposition") == "published" and BORROWING_REF in str(row.get("symbol"))
                             for row in readiness_rows), readiness_rows)

    def test_clear_a_does_not_transfer_its_other_debt_answer_to_b(self) -> None:
        report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_active_borrowing=True, clear_account=True,
            missing_second_account_claim="other-secured-home-debt",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        readiness_rows = [row for row in report["dispositions"]
                          if row.get("artifact_id") == "tax.us.2025.rule.mortgage-account-readiness"]
        self.assertFalse(any(row.get("disposition") == "published"
                             and "demo.mortgage.borrowing.other" in str(row.get("symbol"))
                             for row in readiness_rows), readiness_rows)

    def test_second_report_principal_above_ceiling_blocks_group_amount(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_box2=250001.0,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        report_b = next(row for row in explanation["reports"] if row["statement"] == "demo.f1098.stmt.b")
        self.assertEqual(report_b["reasonChain"]["value"], "qualified")
        principal_row = next(
            row for row in _report["dispositions"]
            if str(row.get("symbol", "")).startswith("tax.us.2025.f1098.principal-within-ceiling|")
            and "statement=demo.f1098.stmt.b" in str(row.get("symbol"))
        )
        self.assertEqual(principal_row["disposition"], "published")
        self.assertIn("demo.f1098.box2-outstanding-principal.1",
                      {pin.get("id") for pin in principal_row["pins"]})
        ceiling_row = next(
            row for row in _report["dispositions"]
            if str(row.get("symbol", "")).startswith("tax.us.2025.mortgage.account-ceiling-selected|")
        )
        self.assertIn(ceiling_row["finding_id"], {pin.get("id") for pin in principal_row["pins"]})

    def test_disagreeing_box3_dates_block_group_amount(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, second_box3="2020-06-02",
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(len(explanation["reports"]), 2)

    def test_ceiling_above_supported_cap_withholds_without_claiming_box2_excess(self) -> None:
        _report, model, _local_ids, _shared_ids = _run_connected_case(
            fully_supported_local=True, annual_ceiling=800000.0,
        )
        explanation = model["mortgageBorrowingExplanation"]
        self.assertEqual(explanation["line8aFindings"], [])
        self.assertEqual(explanation["line8aDispositions"][0]["disposition"], "blocked")
        self.assertEqual(explanation["groups"][0]["recordedApplicableClaims"]
                         ["tax.us.2025.f1098.borrowing-year-ceiling"]["value"], 800000.0)
        self.assertTrue(all(row["reasonChain"]["value"] == "qualified" for row in explanation["reports"]))

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
