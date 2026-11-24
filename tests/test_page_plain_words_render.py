"""Fast render-boundary checks for the saved page's own words.

A first-read text node or aria-label that holds a raw id fails. A badge
whose text is a disposition enum fails. Every line disposition, every
mapped blocked code, and one unmapped code are rendered from synthetic
models. The page under test is the product page unless PPW_PAGE names
another file (scratch mutants only).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGE = Path(os.environ.get("PPW_PAGE", ROOT / "packages/presentation/pages/citation-walk.v1.html"))
CHECKER = ROOT / "docs/phases/engine-breadth/milestones/page-plain-words-evidence/check_page_dom.mjs"

LINE_BADGES = {
    "published_value": "Amount",
    "computed_zero": "Zero",
    "closure_backed_zero": "Confirmed none",
    "published_categorical": "Determined",
    "blocked": "No result",
    "guard_inapplicable": "Not applicable",
}
ATTACHMENT_BADGES = {
    "published": "Complete",
    "blocked": "Not ready",
    "guard_inapplicable": "Not required",
}
LINE_CODES = {
    "DEPENDENCY_ABSENT": (
        "Required information is missing.",
        "This line is waiting on missing information.",
        "Add or confirm the missing information.",
    ),
    "DEPENDENCY_INVALID": (
        "Recorded information does not meet the requirements.",
        "Recorded information is not valid for this line.",
        "Correct the recorded information that does not meet the requirements.",
    ),
    "CATEGORICAL_DOMAIN_MISMATCH": (
        "A recorded answer is not one of the answers this line accepts.",
        "A recorded answer does not fit this line.",
        "Replace the answer with one this line accepts.",
    ),
    "SOURCE_SET_UNCLOSED": (
        "A set of tax forms has not been confirmed as complete.",
        "A set of forms has not been confirmed complete.",
        "Confirm whether this set of forms is complete.",
    ),
    "F1098_SCOPE_CONTRADICTION": (
        "A saved answer says there is no mortgage statement, but a mortgage statement is recorded.",
        "The mortgage statement answers disagree.",
        "Correct the no-statement answer, or remove the recorded mortgage statement.",
    ),
    "SLI_MFS_INELIGIBLE": (
        "The student-loan interest deduction is not available when the filing status is married filing separately.",
        "Married filing separately does not allow this deduction.",
        "This deduction stays unavailable while the filing status is married filing separately.",
    ),
    "SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE": (
        "This student-loan deduction is outside what Schedule 1, part II can include.",
        "This deduction is outside Schedule 1, part II.",
        "Review the student-loan answers. This deduction is outside Schedule 1, part II.",
    ),
    "SLI_UNIVERSAL_COMPONENT_VIOLATION": (
        "A condition the student-loan interest deduction requires on every return is not met.",
        "A required student-loan condition is not met.",
        "Review the student-loan conditions that apply to every return.",
    ),
    "ACCRUED_EXCEEDS_ASSOCIATED_REPORT": (
        "The accrued interest claimed is more than the associated report shows.",
        "Accrued interest is more than the associated report.",
        "Correct the accrued interest or the report it is tied to.",
    ),
    "AGGREGATE_ACCRUED_EXCEEDS_REPORT": (
        "The accrued interest claimed across the reports is more than the report shows.",
        "Combined accrued interest is more than the report.",
        "Correct the accrued amounts so they do not exceed the report.",
    ),
    "NOMINEE_ALLOCATIONS_EXCEED_REPORT": (
        "Nominee amounts add up to more than the report shows.",
        "Nominee amounts exceed the report.",
        "Correct the nominee amounts so they do not exceed the report.",
    ),
    "SUPPORTABILITY_NOT_ESTABLISHED": (
        "The records do not yet show that this adjustment is supported.",
        "Support for this adjustment is not established.",
        "Add the records that show this adjustment is supported.",
    ),
}
ATTACHMENT_CODES = {
    "DEPENDENCY_ABSENT": (
        "Required information is missing.",
        "This attachment is waiting on missing information.",
        "Add the missing information this attachment requires.",
    ),
    "DEPENDENCY_INVALID": (
        "Recorded information does not meet the requirements.",
        "Recorded information is not valid for this attachment.",
        "Correct the recorded information that does not meet the requirements.",
    ),
    "COMPLETENESS_VALUE_VIOLATION": (
        "A required confirmation answer does not match what this form needs.",
        "A required answer does not match what this form needs.",
        "Change the answer to the one this form requires.",
    ),
    "ITEMIZATION_TIE_OUT_VIOLATION": (
        "Itemized entries do not match the total.",
        "The itemized entries do not match the total.",
        "Correct the entries or the total so they match.",
    ),
    "EXCLUSIVE_PRESENCE_CONFLICT": (
        "Two records that cannot both apply are present.",
        "Conflicting records are both present.",
        "Keep only one of the conflicting records.",
    ),
}


def _field(line: str, dispositions: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": f"Synthetic line {line}",
        "line": line,
        "dispositions": dispositions,
        "citation": {"id": "demo.citation.line", "version": "v1"},
    }


def _section(section_id: str, disposition: str, **resolved_extra: object) -> dict[str, Any]:
    instruction_key = "published_value" if disposition == "published_categorical" else disposition
    instruction: dict[str, object] = {"explain": "Saved explanation for this line."}
    if disposition == "published_categorical":
        instruction["render"] = "checked"
    elif disposition in {"published_value", "computed_zero", "closure_backed_zero"}:
        instruction["render"] = "{value}"
    else:
        instruction["render"] = ""
        instruction["codes"] = list(LINE_CODES)
    resolved: dict[str, object] = {"disposition": disposition}
    resolved.update(resolved_extra)
    return {
        "id": section_id,
        "field": _field("11", {instruction_key: instruction}),
        "resolved": resolved,
        "citationSites": [],
    }


def _model(sections: list[dict[str, Any]], attachments: list[dict[str, Any]] | None = None, mortgage: dict[str, Any] | None = None) -> dict[str, Any]:
    model: dict[str, Any] = {
        "schema": "presentation-model.v1",
        "runId": "demo.run.ppw-render",
        "pinLabels": {},
        "questionGroups": [],
        "sections": sections,
        "attachments": attachments or [],
        "citationGroups": [],
        "diagnostics": [],
    }
    if mortgage is not None:
        model["mortgageBorrowingExplanation"] = mortgage
    return model


def _render(model: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({"key": "case", "model": model}) + "\n"
    env = os.environ.copy()
    env["PPW_CHECK_DETAIL"] = "1"
    proc = subprocess.run(
        ["node", str(CHECKER), str(PAGE)],
        input=payload,
        text=True,
        capture_output=True,
        timeout=30,
        check=True,
        env=env,
    )
    return dict(json.loads(proc.stdout)["case"])


def test_page_copy_covers_every_mapped_code() -> None:
    source = (ROOT / "packages/presentation/pages/citation-walk.v1.html").read_text(encoding="utf-8")
    for code in (*LINE_CODES, *ATTACHMENT_CODES):
        assert code in source


@pytest.mark.parametrize("disposition", list(LINE_BADGES))
def test_line_badge_is_plain_words(disposition: str) -> None:
    extra: dict[str, object] = {}
    if disposition in {"published_value", "computed_zero", "closure_backed_zero"}:
        extra["value"] = 0 if disposition != "published_value" else 42000
    if disposition == "blocked":
        extra["activeCodes"] = ["DEPENDENCY_ABSENT"]
    report = _render(_model([_section(f"line-{disposition}", disposition, **extra)]))
    assert report["section_errors"] == 0
    assert report["total_first_read_leaks"] == 0
    assert LINE_BADGES[disposition] in report["badge_texts"]
    assert disposition.replace("_", " ") not in report["first_read_text"]
    assert disposition not in report["badge_texts"]


@pytest.mark.parametrize("code", list(LINE_CODES))
def test_blocked_line_words_come_from_the_code(code: str) -> None:
    sentence, heading, remedy = LINE_CODES[code]
    report = _render(_model([
        _section("line-blocked", "blocked", activeCodes=[code], reasons=[]),
    ]))
    assert report["section_errors"] == 0, report["reason_codes"]
    text = report["first_read_text"]
    assert "This line has no result." in text
    assert sentence in text
    assert heading in text
    assert remedy in text
    assert "missing information" not in text or code == "DEPENDENCY_ABSENT"
    assert code not in text
    assert report["total_first_read_leaks"] == 0


def test_unmapped_line_code_fails_closed() -> None:
    report = _render(_model([
        _section("line-blocked", "blocked", activeCodes=["NOT_A_REAL_CODE"]),
    ]))
    assert report["section_errors"] == 1
    assert report["reason_codes"] == ["unmapped-blocked-code"]
    assert "NOT_A_REAL_CODE" not in report["first_read_text"]
    assert "This section reported a reason code this page does not recognize." in report["first_read_text"]


@pytest.mark.parametrize("disposition", list(ATTACHMENT_BADGES))
def test_attachment_badge_is_plain_words(disposition: str) -> None:
    resolved: dict[str, object] = {"disposition": disposition}
    if disposition == "blocked":
        resolved["activeCodes"] = ["DEPENDENCY_ABSENT"]
    report = _render(_model([], attachments=[{
        "id": "demo.attachment.one",
        "title": "Synthetic attachment",
        "resolved": resolved,
    }]))
    assert report["section_errors"] == 0
    assert report["total_first_read_leaks"] == 0
    assert ATTACHMENT_BADGES[disposition] in report["badge_texts"]


@pytest.mark.parametrize("code", list(ATTACHMENT_CODES))
def test_blocked_attachment_words_come_from_the_code(code: str) -> None:
    sentence, heading, remedy = ATTACHMENT_CODES[code]
    report = _render(_model([], attachments=[{
        "id": "demo.attachment.one",
        "title": "Synthetic attachment",
        "resolved": {"disposition": "blocked", "activeCodes": [code]},
    }]))
    assert report["section_errors"] == 0, report["reason_codes"]
    text = report["first_read_text"]
    assert heading in text
    assert sentence in text
    assert remedy in text
    assert "Not ready" in report["badge_texts"]
    assert code not in text
    if code != "DEPENDENCY_ABSENT":
        assert "missing" not in text.casefold()


def test_unmapped_attachment_code_fails_closed() -> None:
    report = _render(_model([], attachments=[{
        "id": "demo.attachment.one",
        "title": "Synthetic attachment",
        "resolved": {"disposition": "blocked", "activeCodes": ["NOT_A_REAL_CODE"]},
    }]))
    assert report["section_errors"] == 1
    assert report["reason_codes"] == ["unrecognized-attachment-code"]
    assert "NOT_A_REAL_CODE" not in report["first_read_text"]


def _mortgage(disposition: str) -> dict[str, Any]:
    return {
        "schema": "mortgage-borrowing-explanation.v1",
        "reports": [{
            "reportedInterest": {"value": 100},
            "localAnswers": [],
            "relationships": [{"disposition": disposition, "response": "yes"}],
            "effectiveAnswers": [],
        }],
        "groups": [],
        "line8aDispositions": [{
            "artifact_id": "tax.us.2025.rule.f1098-line8a",
            "disposition": "blocked",
        }],
        "line8aFindings": [],
        "orphanRelationships": [],
    }


def test_known_mortgage_link_disposition_stays_plain() -> None:
    report = _render(_model([], mortgage=_mortgage("affirmed")))
    assert report["section_errors"] == 0
    assert "Confirmed" in report["first_read_text"]
    assert report["total_first_read_leaks"] == 0


def test_unknown_mortgage_link_disposition_fails_closed() -> None:
    report = _render(_model([], mortgage=_mortgage("surprise-token")))
    assert report["section_errors"] == 1
    assert report["reason_codes"] == ["unrecognized-mortgage-link"]
    assert "surprise token" not in report["first_read_text"]
    assert "surprise-token" not in report["first_read_text"]


def test_first_read_rejects_a_raw_id() -> None:
    report = _render(_model([
        _section("line-published", "published_value", value=42000),
    ]))
    assert report["total_first_read_leaks"] == 0
    assert report["section_errors"] == 0
    assert "demo.citation.line" not in report["first_read_text"]
