"""Small assertions and loader for the real sale-page regression capture."""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import re
from typing import Any, cast

from tools.sale_page_observation import main


ROOT = Path(__file__).resolve().parents[2]
PARKED_ALERTS = {
    "line-6c": "This line is missing its rendering instruction for the declared disposition.",
    "line-sch1-top": "This line published a value with no citation attached. No value can be shown safely.",
}
QUESTION = "Did you sell any securities whose basis was not reported to the IRS?"
SCHEDULE_A = "tax.us.2025.rule.attachment.schedule-a"
SCHEDULE_A_BOUNDARY = "tax.us.2025.schedule-a-boundary.no-other-line16-declared"
SCHEDULE1_TOP_SYMBOL = "tax.us.2025.schedule1.top-entry"
SCHEDULE1_TOP_FIELD = "tax.us.2025.schedule1.top-entry.form-field"
SCHEDULE1_TOP_ZERO_EXPLANATION = "No Form 1099-K statements were received for 2025."

EXPECTED_PARKED_DIFFERENCES = {
    "line-6c": {
        "line-6c: model disposition 'published_categorical'; DOM badge ''",
        "line-6c: model display value 'checked'; DOM value ''",
        "line-6c: model explanation/reasons differ from the rendered DOM",
    },
    "line-sch1-top": {
        "line-sch1-top: model disposition 'closure_backed_zero'; DOM badge ''",
        "line-sch1-top: model display value '0'; DOM value ''",
        "line-sch1-top: model explanation/reasons differ from the rendered DOM",
    },
}


def _as_dict(value: object) -> dict[str, Any]:
    return cast(dict[str, Any], value) if isinstance(value, dict) else {}


def collect(*, core_version: str = "v79", case_id: str | None = None) -> dict[str, Any]:
    """Run the structured collector without writing tracked P0 reports."""
    output = io.StringIO()
    args = ["--track1-regression", "--structured-only", "--core-version", core_version]
    if case_id is not None:
        args.extend(("--case-id", case_id))
    with redirect_stdout(output):
        status = main(args)
    if status != 0:
        raise AssertionError("structured sale-page collector returned a failure status")
    match = re.search(r"scratch=(temp/sale-page-observation/[A-Za-z0-9TZ]+)/", output.getvalue())
    if match is None:
        raise AssertionError("structured sale-page collector did not identify its ignored scratch run")
    run_root = (ROOT / match.group(1)).resolve()
    scratch_root = (ROOT / "temp/sale-page-observation").resolve()
    if not run_root.is_relative_to(scratch_root):
        raise AssertionError("structured observation path escaped ignored scratch")
    path = run_root / "regression-observations.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError("structured sale-page observations must be an object")
    for case in payload.get("cases", []):
        for key in ("model_path", "report_path"):
            relative_path = case.get(key)
            if not isinstance(relative_path, str) or ".." in Path(relative_path).parts:
                raise AssertionError(f"unsafe structured observation {key}")
            resolved = (ROOT / relative_path).resolve()
            if not resolved.is_relative_to(run_root):
                raise AssertionError(f"structured observation {key} escaped its run")
            case[key.removesuffix("_path")] = json.loads(resolved.read_text(encoding="utf-8"))
    return cast(dict[str, Any], payload)


def line_by_id(model: dict[str, Any], dom: dict[str, Any], section_id: str) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    model_rows = [row for row in model.get("sections", []) if isinstance(row, dict) and row.get("id") == section_id]
    dom_rows = [row for row in dom.get("lines", []) if isinstance(row, dict) and row.get("id") == section_id]
    return (model_rows[0] if len(model_rows) == 1 else None, dom_rows[0] if len(dom_rows) == 1 else None)


def line_by_field(model: dict[str, Any], dom: dict[str, Any], field_id: str) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    model_rows = [
        row for row in model.get("sections", [])
        if isinstance(row, dict) and isinstance(row.get("field"), dict) and row["field"].get("id") == field_id
    ]
    if len(model_rows) != 1:
        return None, None
    return line_by_id(model, dom, str(model_rows[0].get("id") or ""))


def attachment_by_id(model: dict[str, Any], dom: dict[str, Any], attachment_id: str) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    model_rows = [row for row in model.get("attachments", []) if isinstance(row, dict) and row.get("id") == attachment_id]
    dom_rows = [
        row for row in dom.get("attachments", [])
        if isinstance(row, dict) and str(row.get("id", "")).removesuffix("-status") == attachment_id
    ]
    return (model_rows[0] if len(model_rows) == 1 else None, dom_rows[0] if len(dom_rows) == 1 else None)


def citation_part_text(dom: dict[str, Any]) -> list[tuple[str, str]]:
    return [
        (str(part.get("heading") or ""), str(part.get("tie_out_text") or ""))
        for group in dom.get("citation_groups", [])
        if isinstance(group, dict)
        for part in group.get("parts", [])
        if isinstance(part, dict)
    ]


def visible_question_state(dom: dict[str, Any], question: str = QUESTION) -> dict[str, Any]:
    """Classify only the visible line-local reason rows, not JSON or provenance."""
    occurrences: list[dict[str, Any]] = []
    for row in dom.get("lines", []):
        if not isinstance(row, dict):
            continue
        for reason in row.get("blocked_reasons", []):
            text = str(reason)
            count = text.count(question)
            if count:
                occurrences.append({"section_id": str(row.get("id") or ""), "count": count})
    total = sum(row["count"] for row in occurrences)
    state = "absent" if total == 0 else "once" if total == 1 else "duplicate"
    return {"state": state, "occurrences": occurrences, "total": total}


def audit_observation(model: dict[str, Any], dom: dict[str, Any]) -> dict[str, Any]:
    """Separate exact parked renderer diagnostics from unexpected parity failures."""
    from tools.sale_page_observation import _compare_model_and_dom

    differences, checks = _compare_model_and_dom(model, dom)
    model_rows = {str(row.get("id")): row for row in model.get("sections", []) if isinstance(row, dict)}
    dom_rows = {str(row.get("id")): row for row in dom.get("lines", []) if isinstance(row, dict)}
    diagnostics: list[dict[str, str]] = []
    unexpected: list[str] = []

    for section_id, alert in PARKED_ALERTS.items():
        source = model_rows.get(section_id)
        rendered = dom_rows.get(section_id)
        if source is None or rendered is None:
            unexpected.append(f"{section_id}: expected model and DOM rows are not uniquely present")
            continue
        field = _as_dict(source.get("field"))
        resolved = _as_dict(source.get("resolved"))
        if section_id == "line-6c":
            instruction = _as_dict(_as_dict(field.get("dispositions")).get("published_value"))
            act = _as_dict(resolved.get("act"))
            finding = _as_dict(act.get("finding"))
            cause_matches = (
                resolved.get("disposition") == "published_categorical"
                and finding.get("value") == "not_elected"
                and instruction.get("render") == "not_elected"
            )
            source_cause = "published_value render=not_elected is rejected by the categorical renderer"
        else:
            instruction = _as_dict(_as_dict(field.get("dispositions")).get("closure_backed_zero"))
            act = _as_dict(resolved.get("act"))
            finding = _as_dict(act.get("finding"))
            raw_pins = finding.get("pins")
            pins = [pin for pin in raw_pins if isinstance(pin, dict)] if isinstance(raw_pins, list) else []
            observed_source_pins = {
                (pin.get("id"), pin.get("role"), pin.get("version"), pin.get("origin"))
                for pin in pins
            }
            expected_source_pins = {
                ("tax.us.2025.package.core-calculations", "adoption", "v79", None),
                ("tax.us.2025.rule.schedule1-top-entry", "computation", "v3", None),
                ("demo.probe.f1099k.closure", "input", "v1", "assertion"),
                ("tax.us.2025.closure-mapping.f1099k", "package", "v3", None),
                ("tax.us.2025.f1099k", "package", "v2", None),
            }
            cause_matches = (
                field.get("id") == SCHEDULE1_TOP_FIELD
                and field.get("binds_symbol") == SCHEDULE1_TOP_SYMBOL
                and "citation" not in field
                and source.get("citationSites") == []
                and resolved.get("disposition") == "closure_backed_zero"
                and type(resolved.get("value")) is int
                and resolved.get("value") == 0
                and finding.get("symbol") == SCHEDULE1_TOP_SYMBOL
                and type(finding.get("value")) is str
                and finding.get("value") == "0"
                and instruction.get("explain") == SCHEDULE1_TOP_ZERO_EXPLANATION
                and instruction.get("render") == "{value}"
                and observed_source_pins == expected_source_pins
            )
            source_cause = (
                "value 0 is backed by the v79 Schedule 1 top-entry computation and the explicit "
                "no-Form-1099-K source closure; the projected field has no citation"
            )
        if not cause_matches:
            unexpected.append(f"{section_id}: saved model no longer has the observed renderer source shape")
        if rendered.get("section_error") != alert:
            unexpected.append(f"{section_id}: visible safe-renderer alert changed or disappeared")
        if any(rendered.get(key) for key in ("disposition", "value", "explain", "blocked_banner", "blocked_reasons")):
            unexpected.append(f"{section_id}: error boundary did not clear the adjacent value presentation")
        diagnostics.append({"section_id": section_id, "alert": alert, "source_cause": source_cause})

    for row in dom.get("lines", []):
        if isinstance(row, dict) and row.get("section_error") and row.get("id") not in PARKED_ALERTS:
            unexpected.append(f"{row.get('id')}: unexpected section-error alert")

    for difference in differences:
        if not any(difference in expected for expected in EXPECTED_PARKED_DIFFERENCES.values()):
            unexpected.append(difference)

    blocked_reason_errors: list[str] = []
    for section in model.get("sections", []):
        if not isinstance(section, dict):
            continue
        resolved = _as_dict(section.get("resolved"))
        if resolved.get("disposition") != "blocked":
            continue
        section_id = str(section.get("id") or "")
        rendered = dom_rows.get(section_id)
        if rendered is None:
            blocked_reason_errors.append(f"{section_id}: blocked line has no unique DOM row")
            continue
        reasons = resolved.get("reasons")
        if isinstance(reasons, list) and reasons:
            if any(not isinstance(reason, dict) or not str(reason.get("sentence") or "").strip() for reason in reasons):
                blocked_reason_errors.append(f"{section_id}: model blocker has an empty reason sentence")
        else:
            field = _as_dict(section.get("field"))
            instruction = _as_dict(_as_dict(field.get("dispositions")).get("blocked"))
            explanation = str(instruction.get("explain") or "").strip()
            if not explanation or explanation not in str(rendered.get("blocked_banner") or ""):
                blocked_reason_errors.append(f"{section_id}: blocked line has no nonempty model instruction in the DOM")

    return {
        "unexpected": unexpected,
        "blocked_reason_errors": blocked_reason_errors,
        "renderer_diagnostics": diagnostics,
        "comparison_checks": checks,
    }
