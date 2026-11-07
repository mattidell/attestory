"""Live regression checks for the actual synthetic core-v79 saved-page path."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from tests.helpers.sale_page_observation import (
    PARKED_ALERTS,
    QUESTION,
    SCHEDULE_A,
    SCHEDULE_A_BOUNDARY,
    SCHEDULE1_TOP_FIELD,
    SCHEDULE1_TOP_ZERO_EXPLANATION,
    attachment_by_id,
    audit_observation,
    citation_part_text,
    collect,
    line_by_field,
    visible_question_state,
)


pytestmark = pytest.mark.live

EXPECTED_CASES = {
    "mortgage-1098",
    "covered-long-term-sale",
    "noncovered-box-e-sale",
    "wash-sale-code-w",
    "covered-basis-not-reported",
    "wage-single-noncovered-no",
    "wage-unanswered-question",
    "sale-answer-needs-reconfirmation",
    "mortgage-itemized-declared-boundaries",
    "mortgage-itemized-complete-scope",
}


@pytest.fixture(scope="module")
def observed() -> dict[str, Any]:
    return collect()


def _cases(batch: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cases = {row["spec"]["id"]: row for row in batch["cases"]}
    assert set(cases) == EXPECTED_CASES
    return cases


def _require_line(case: dict[str, Any], field_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    model, dom = line_by_field(case["model"], case["dom"], field_id)
    assert model is not None and dom is not None, field_id
    return model, dom


def _require_attachment(case: dict[str, Any], attachment_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    model, dom = attachment_by_id(case["model"], case["dom"], attachment_id)
    assert model is not None and dom is not None, attachment_id
    return model, dom


def _assert_published_line(case: dict[str, Any], field_id: str, value: int) -> None:
    model, dom = _require_line(case, field_id)
    assert model["resolved"]["disposition"] == "published_value"
    assert model["resolved"]["value"] == value
    assert dom["value"] == str(value)


def _schedule_a_report_row(case: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row for row in case["report"].get("dispositions", [])
        if isinstance(row, dict) and row.get("artifact_id") == SCHEDULE_A
    ]
    assert len(rows) == 1
    return rows[0]


def _assert_negative_instrument_mutations(cases: dict[str, dict[str, Any]]) -> None:
    """Instrument-only mutations are separate from the saved-page findings."""
    corrected = cases["covered-basis-not-reported"]
    model_line, _ = _require_line(corrected, "tax.us.2025.schedule-d.line-8a")
    section_id = str(model_line["id"])

    wrong_reason = deepcopy(corrected["dom"])
    reason_row = next(row for row in wrong_reason["lines"] if row.get("id") == section_id)
    reason_row["blocked_reasons"] = ["A different reason."]
    assert audit_observation(corrected["model"], wrong_reason)["unexpected"]

    empty_reason = deepcopy(corrected["dom"])
    reason_row = next(row for row in empty_reason["lines"] if row.get("id") == section_id)
    reason_row["blocked_reasons"] = [""]
    assert audit_observation(corrected["model"], empty_reason)["unexpected"]

    covered = cases["covered-long-term-sale"]
    covered_model, covered_dom = _require_line(covered, "tax.us.2025.schedule-d.line-8a")
    wrong_value = deepcopy(covered["dom"])
    value_row = next(row for row in wrong_value["lines"] if row.get("id") == covered_model["id"])
    value_row["value"] = "4001"
    assert audit_observation(covered["model"], wrong_value)["unexpected"]

    missing_row = deepcopy(covered["dom"])
    missing_row["lines"] = [row for row in missing_row["lines"] if row.get("id") != covered_model["id"]]
    assert audit_observation(covered["model"], missing_row)["unexpected"]
    assert covered_dom["value"] == "4000"

    one_question = deepcopy(covered["dom"])
    one_question["lines"][0]["blocked_reasons"] = [QUESTION]
    assert visible_question_state(one_question)["state"] == "once"
    duplicate_question = deepcopy(one_question)
    duplicate_question["lines"][1]["blocked_reasons"] = [QUESTION]
    assert visible_question_state(duplicate_question)["state"] == "duplicate"

    sch1 = cases["covered-long-term-sale"]
    sch1_line, sch1_dom = _require_line(sch1, SCHEDULE1_TOP_FIELD)
    alert = PARKED_ALERTS["line-sch1-top"]
    baseline_audit = audit_observation(sch1["model"], sch1["dom"])
    assert baseline_audit["unexpected"] == []
    assert any(
        row["section_id"] == "line-sch1-top"
        and row["alert"] == alert
        and "explicit no-Form-1099-K source closure" in row["source_cause"]
        for row in baseline_audit["renderer_diagnostics"]
    )
    assert sch1_dom["section_error"] == alert

    wrong_zero = deepcopy(sch1["model"])
    wrong_zero_line = next(row for row in wrong_zero["sections"] if row.get("id") == sch1_line["id"])
    wrong_zero_line["resolved"]["value"] = 999
    wrong_zero_audit = audit_observation(wrong_zero, sch1["dom"])
    assert any("model display value '999'" in difference for difference in wrong_zero_audit["unexpected"])
    assert any(row["section_id"] == "line-sch1-top" and row["alert"] == alert for row in wrong_zero_audit["renderer_diagnostics"])

    changed_explanation = deepcopy(sch1["model"])
    changed_explanation_line = next(
        row for row in changed_explanation["sections"] if row.get("id") == sch1_line["id"]
    )
    changed_explanation_line["field"]["dispositions"]["closure_backed_zero"]["explain"] = (
        "A different Form 1099-K closure explanation."
    )
    changed_explanation_audit = audit_observation(changed_explanation, sch1["dom"])
    assert any(
        "saved model no longer has the observed renderer source shape" in difference
        for difference in changed_explanation_audit["unexpected"]
    )
    assert any(
        row["section_id"] == "line-sch1-top" and row["alert"] == alert
        for row in changed_explanation_audit["renderer_diagnostics"]
    )

    changed_source = deepcopy(sch1["model"])
    changed_source_line = next(row for row in changed_source["sections"] if row.get("id") == sch1_line["id"])
    changed_source_line["resolved"]["act"]["finding"]["value"] = "999"
    changed_source_audit = audit_observation(changed_source, sch1["dom"])
    assert any(
        "saved model no longer has the observed renderer source shape" in difference
        for difference in changed_source_audit["unexpected"]
    )
    assert any(
        row["section_id"] == "line-sch1-top" and row["alert"] == alert
        for row in changed_source_audit["renderer_diagnostics"]
    )

    missing_closure_pin = deepcopy(sch1["model"])
    missing_closure_line = next(row for row in missing_closure_pin["sections"] if row.get("id") == sch1_line["id"])
    missing_closure_finding = missing_closure_line["resolved"]["act"]["finding"]
    missing_closure_finding["pins"] = [
        pin for pin in missing_closure_finding["pins"] if pin.get("id") != "demo.probe.f1099k.closure"
    ]
    missing_closure_audit = audit_observation(missing_closure_pin, sch1["dom"])
    assert any(
        "saved model no longer has the observed renderer source shape" in difference
        for difference in missing_closure_audit["unexpected"]
    )
    assert any(
        row["section_id"] == "line-sch1-top" and row["alert"] == alert
        for row in missing_closure_audit["renderer_diagnostics"]
    )
    assert sch1_line["field"]["dispositions"]["closure_backed_zero"]["explain"] == SCHEDULE1_TOP_ZERO_EXPLANATION


def test_real_chrome_cases_match_supported_model_and_dom_properties(observed: dict[str, Any]) -> None:
    """Real cases assert supported rows; two exact renderer alerts stay diagnostic."""
    cases = _cases(observed)
    browser = observed["browser"]
    assert isinstance(browser.get("browser_version"), str) and browser["browser_version"].startswith("Chrome/")
    assert isinstance(browser.get("node_version"), str) and browser["node_version"]
    assert browser.get("cleanup_completed") is True

    for case_id, case in cases.items():
        metadata = case["metadata"]
        adoption = metadata["selected_adoption"]
        assert case["dom"]["context_cleanup"] == {
            "target_closed": True,
            "browser_context_disposed": True,
        }, case_id
        assert adoption == {
            "package": "core-calculations@v79",
            "registry": "published-packages.v77.json",
            "release": "demo.release.sli-worksheet-integration.2025@v77",
            "coordinator_saved_page": True,
        }, case_id
        audit = audit_observation(case["model"], case["dom"])
        assert audit["unexpected"] == [], (case_id, audit["unexpected"])
        assert audit["blocked_reason_errors"] == [], (case_id, audit["blocked_reason_errors"])
        assert {row["section_id"]: row["alert"] for row in audit["renderer_diagnostics"]} == PARKED_ALERTS

        expected_question_state = (
            "duplicate"
            if case["spec"]["answered_noncovered_question"] in {"unanswered", "stale-no"}
            else "absent"
        )
        question = visible_question_state(case["dom"])
        assert question["state"] == expected_question_state, (case_id, question)

    mortgage = cases["mortgage-1098"]
    mortgage_line8a = mortgage["model"]["mortgageBorrowingExplanation"]["line8aFindings"]
    assert any(row.get("symbol") == "tax.us.2025.schedule-a.line8a" and row.get("value") == 4000 for row in mortgage_line8a)
    assert "group amount: 4000" in mortgage["dom"]["mortgage_explanation"]
    line12e, line12e_dom = _require_line(mortgage, "tax.us.2025.form1040.line-12e")
    assert line12e["resolved"]["value"] == 15750 and line12e_dom["value"] == "15750"
    mortgage_schedule_a, mortgage_schedule_a_dom = _require_attachment(mortgage, SCHEDULE_A)
    assert mortgage_schedule_a["resolved"]["disposition"] == "guard_inapplicable"
    assert mortgage_schedule_a_dom["disposition"] == "GUARD INAPPLICABLE"

    covered = cases["covered-long-term-sale"]
    _assert_published_line(covered, "tax.us.2025.schedule-d.line-8a", 4000)
    _, covered_schedule_d = _require_attachment(covered, "tax.us.2025.rule.attachment.schedule-d")
    assert covered_schedule_d["disposition"] == "PUBLISHED"

    noncovered = cases["noncovered-box-e-sale"]
    _assert_published_line(noncovered, "tax.us.2025.schedule-d.line-9", 4000)
    _, noncovered_f8949 = _require_attachment(noncovered, "tax.us.2025.rule.attachment.f8949")
    assert noncovered_f8949["disposition"] == "PUBLISHED"
    noncovered_parts = citation_part_text(noncovered["dom"])
    for heading_part, total in (("box e column (d)", "6000"), ("box e column (e)", "2000"), ("box e column (g)", "0")):
        assert any(heading_part in heading.casefold() and f"Reported subtotal: {total}" in text for heading, text in noncovered_parts)

    wash = cases["wash-sale-code-w"]
    _assert_published_line(wash, "tax.us.2025.schedule-d.line-9", -2000)
    wash_parts = citation_part_text(wash["dom"])
    for heading_part, total in (("box e column (d)", "4000"), ("box e column (e)", "7000"), ("box e column (g)", "1000")):
        assert any(heading_part in heading.casefold() and f"Reported subtotal: {total}" in text for heading, text in wash_parts)

    corrected = cases["covered-basis-not-reported"]
    blocked_line, blocked_dom = _require_line(corrected, "tax.us.2025.schedule-d.line-8a")
    assert blocked_line["resolved"]["disposition"] == "blocked"
    assert blocked_dom["value"] == "No value published — cannot compute."
    assert blocked_dom["blocked_reasons"] == [
        "Record this sale as a noncovered sale. The broker did not report its basis to the IRS."
    ]

    wage = cases["wage-single-noncovered-no"]
    wage_line, wage_dom = _require_line(wage, "tax.us.2025.schedule-d.line-9")
    assert wage_line["resolved"]["disposition"] == "closure_backed_zero"
    assert wage_line["resolved"]["value"] == 0 and wage_dom["value"] == "0"
    _, wage_schedule_d = _require_attachment(wage, "tax.us.2025.rule.attachment.schedule-d")
    assert wage_schedule_d["disposition"] == "GUARD INAPPLICABLE"
    closures = wage["metadata"]["noncovered_source_closures"]
    assert closures == [{
        "fact_id": "tax.us.2025.f1099b.noncovered-sold.source-closure|tax-year=2025",
        "value": "no",
    }]
    assert wage["metadata"]["noncovered_in_class_answers"] == []
    assert visible_question_state(wage["dom"])["state"] == "absent"

    missing = cases["mortgage-itemized-declared-boundaries"]
    complete = cases["mortgage-itemized-complete-scope"]
    assert "no-other-line16 is intentionally unanswered" in missing["spec"]["inputs"]
    assert "no-other-line16 is intentionally unanswered" not in complete["spec"]["inputs"]
    assert "no-other-line16 declaration is explicitly recorded" in complete["spec"]["inputs"]
    assert "exact missing Schedule A input is reported" not in complete["spec"]["inputs"]
    expected_boundaries = {
        "tax.us.2025.schedule-a-boundary.no-medical-declared",
        "tax.us.2025.schedule-a-boundary.no-salt-declared",
        "tax.us.2025.schedule-a-boundary.no-other-interest-declared",
        "tax.us.2025.schedule-a-boundary.no-investment-interest-declared",
        "tax.us.2025.schedule-a-boundary.no-charitable-declared",
        "tax.us.2025.schedule-a-boundary.no-casualty-theft-declared",
        "tax.us.2025.schedule-a-boundary.no-gambling-other-declared",
        "tax.us.2025.qbi.no-qbi-deduction-declared",
        "tax.us.2025.schedule1a.no-additional-deductions-declared",
    }
    for case in (missing, complete):
        observed_inputs = {row["fact_id"].split("|", maxsplit=1)[0] for row in case["metadata"]["source_scope_declarations"]}
        assert expected_boundaries <= observed_inputs
        assert "group amount: 20000" in case["dom"]["mortgage_explanation"]
        line12e_model, line12e_dom = _require_line(case, "tax.us.2025.form1040.line-12e")
        assert line12e_model["resolved"]["value"] == 20000 and line12e_dom["value"] == "20000"

    missing_schedule_a, missing_schedule_a_dom = _require_attachment(missing, SCHEDULE_A)
    assert missing_schedule_a["resolved"]["disposition"] == "blocked"
    assert missing_schedule_a_dom["disposition"] == "BLOCKED"
    missing_report = _schedule_a_report_row(missing)
    assert missing_report["code"] == "DEPENDENCY_ABSENT"
    assert missing_report["missing"] == [SCHEDULE_A_BOUNDARY]
    missing_inputs = {row["fact_id"].split("|", maxsplit=1)[0] for row in missing["metadata"]["source_scope_declarations"]}
    assert SCHEDULE_A_BOUNDARY not in missing_inputs

    complete_schedule_a, complete_schedule_a_dom = _require_attachment(complete, SCHEDULE_A)
    assert complete_schedule_a["resolved"]["disposition"] == "published"
    assert complete_schedule_a_dom["disposition"] == "PUBLISHED"
    complete_report = _schedule_a_report_row(complete)
    assert complete_report["disposition"] == "published" and complete_report.get("missing", []) == []
    complete_inputs = {row["fact_id"].split("|", maxsplit=1)[0] for row in complete["metadata"]["source_scope_declarations"]}
    assert SCHEDULE_A_BOUNDARY in complete_inputs
    _assert_negative_instrument_mutations(cases)
