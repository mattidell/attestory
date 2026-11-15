"""Trace how a categorical Form 1040 field is declared, published and rendered.

Evidence for docs/phases/engine-breadth/milestones/line12d-boxes.md.
Charter: docs/reviews/line12d-boxes/charter-p0.md.

Walks published core v89: form-field citizens, the rules that publish the
symbols they bind, the presentation model, and the saved citation-walk
renderer. The example is Form 1040 line 6d (the lived-apart checkbox and
its not-checked sibling). Also records whether any field already shows a
line 12d box, and the sha256 of the reused age-blindness law.json.

    python3 trace.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
LAW = REPO / "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence/law.json"
PACKAGE = CONTENT / "package.core-calculations.v89.json"


def _load(name: str) -> dict[str, Any]:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def _cite(path: str, start: int, end: int) -> dict[str, Any]:
    return {"file": path, "lines": f"{start}-{end}"}


def law() -> dict[str, Any]:
    raw = LAW.read_bytes()
    body = json.loads(raw)
    wanted = ("form1040-line12d", "age-65", "separate-return-spouse", "chart")
    quotes = {row["id"]: row for row in body["quotes"]}
    return {
        "path": str(LAW.relative_to(REPO)),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "quotes": {
            ident: {
                "source": quotes[ident]["source"],
                "extract_lines": quotes[ident]["extract_lines"],
                "text": quotes[ident]["text"],
            }
            for ident in wanted
        },
        "reading_spouse_boxes": next(
            line for line in body["reading"] if line.startswith("Spouse boxes:")
        ),
    }


def example_checkbox() -> dict[str, Any]:
    """Line 6d is the existing checkbox-like Form 1040 field."""
    checked = _load("form1040.line-6d.form-field.json")
    not_checked = _load("form1040.line-6d-not-checked.form-field.json")
    rule_checked = _load("rule.form1040-line6d.json")
    rule_not = _load("rule.form1040-line6d-not-checked.json")
    return {
        "why": (
            "Form 1040 line 6d is a checkbox. The package publishes the checked "
            "state and the not-checked state as two fields, each bound to a rule "
            "whose finding value is the field's published_value.render string."
        ),
        "checked_field": {
            "id": checked["id"].removeprefix(P),
            "schema": checked["schema"],
            "binds_symbol": checked["binds_symbol"].removeprefix(P),
            "line": checked["line"],
            "render": checked["dispositions"]["published_value"]["render"],
            "cite": _cite("packages/content/tax/2025/form1040.line-6d.form-field.json", 1, 47),
        },
        "not_checked_field": {
            "id": not_checked["id"].removeprefix(P),
            "binds_symbol": not_checked["binds_symbol"].removeprefix(P),
            "line": not_checked["line"],
            "render": not_checked["dispositions"]["published_value"]["render"],
            "cite": _cite(
                "packages/content/tax/2025/form1040.line-6d-not-checked.form-field.json", 1, 47
            ),
        },
        "checked_rule": {
            "id": rule_checked["id"].removeprefix(P),
            "schema": rule_checked["schema"],
            "role": rule_checked["role"],
            "publishes": rule_checked["publishes"].removeprefix(P),
            "value": rule_checked["value"],
            "cite": _cite("packages/content/tax/2025/rule.form1040-line6d.json", 1, 100),
        },
        "not_checked_rule": {
            "id": rule_not["id"].removeprefix(P),
            "publishes": rule_not["publishes"].removeprefix(P),
            "value": rule_not["value"],
            "cite": _cite(
                "packages/content/tax/2025/rule.form1040-line6d-not-checked.json", 1, 100
            ),
        },
        "section_id_is_line": _cite(
            "packages/derivation/presentation_projection.py", 3956, 3957
        ),
        "two_fields_need_two_line_values": (
            "The presentation section id is 'line-' plus field.line, so the "
            "checked and not-checked fields use line '6d' and '6d-not-checked'."
        ),
    }


def pipeline() -> dict[str, Any]:
    return {
        "declare": {
            "schema": "form-field.v3",
            "cite": _cite("packages/schemas/tax/form-field.v3.schema.json", 1, 6),
            "binds_symbol": (
                "A field names one binds_symbol. Package validation accepts a "
                "symbol a member rule publishes, or an input binding."
            ),
            "validation_cite": _cite(
                "packages/derivation/package_validation.py", 2595, 2601
            ),
            "reachability": (
                "Every form-field member is a reachability root, so the rule it "
                "binds is reached without listing the field as an entrypoint."
            ),
            "reachability_cite": _cite(
                "packages/derivation/package_validation.py", 3378, 3383
            ),
        },
        "publish": {
            "rule_role": (
                "Line 6d's publishers are computation rules (rule-artifact.v3), "
                "not field-mapping. field-mapping is the wages-to-line-1a role. "
                "A categorical checkbox uses a fixed string value equal to the "
                "field's published_value.render."
            ),
            "wages_field_mapping": {
                "id": "rule.w2-box1-to-line1a",
                "role": "field-mapping",
                "cite": _cite(
                    "packages/content/tax/2025/package.core-calculations.v89.json",
                    5897,
                    5901,
                ),
            },
        },
        "project": {
            "cite": _cite("packages/derivation/presentation_projection.py", 771, 806),
            "numeric": "published_value.render '{value}' copies the numeric finding.",
            "categorical": (
                "Any other render string is the affirmative checkbox form: the "
                "finding value must be that same string, and the source value is "
                "not copied onto the model. Disposition is published_categorical."
            ),
            "boolean_fact_cannot_bind_directly": (
                "taxpayer_over_65 is a boolean input. Binding a form field to it "
                "fails projection: the finding value is not the render string. A "
                "publishing rule is required."
            ),
            "one_field_one_render": (
                "published_value.render is one string, so one field shows one "
                "state. Line 6d therefore uses two fields for checked and not_checked."
            ),
        },
        "render": {
            "cite": _cite("packages/presentation/pages/citation-walk.v1.html", 1014, 1022),
            "accepts": "checked",
            "saved_page_observation": _cite(
                "docs/phases/engine-breadth/milestones/sale-page-observation-evidence/p0-observation.md",
                62,
                66,
            ),
            "note": (
                "The saved citation-walk page draws published_categorical only when "
                "render is 'checked'. Line 6c's not_elected and line 6d's "
                "not_checked hit missing-instruction on the page. The presentation "
                "model still carries those states."
            ),
        },
    }


def v89_line12d() -> dict[str, Any]:
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    fields = []
    for member in package["members"]:
        schema = str(member.get("schema") or "")
        ident = str(member.get("id") or "")
        if schema.startswith("form-field.") and "12d" in ident.lower():
            fields.append(ident)
        if schema.startswith("form-field.") and ident.endswith("line-12e"):
            body = _load("form1040.line-12e.form-field.json")
            line12e = {
                "id": body["id"].removeprefix(P),
                "binds": body["binds_symbol"].removeprefix(P),
                "render": body["dispositions"]["published_value"]["render"],
            }
    bindings = {
        row["symbol"]: row["mode"]
        for row in package["input_bindings"]
        if row["symbol"] in {
            "taxpayer_over_65",
            "taxpayer_blind",
            "spouse_over_65",
            "spouse_blind",
            "spouse_separate_condition",
        }
    }
    return {
        "package": "v89",
        "form_fields_named_12d": fields,
        "line_12e": line12e,
        "age_blind_bindings": bindings,
        "finding": (
            "No form field shows a line 12d box. The four age and blindness "
            "facts are required inputs; the page shows them through line 12e's "
            "amount and through the input questions while they are open."
        ),
    }


def main() -> None:
    payload = {
        "package": "v89",
        "law": law(),
        "example": example_checkbox(),
        "pipeline": pipeline(),
        "line12d_today": v89_line12d(),
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"trace output contains {needle}")
    (HERE / "trace.json").write_text(text, encoding="utf-8")
    print(json.dumps({
        "law_sha256": payload["law"]["sha256"],
        "example_checked_render": payload["example"]["checked_field"]["render"],
        "example_not_checked_render": payload["example"]["not_checked_field"]["render"],
        "renderer_accepts": payload["pipeline"]["render"]["accepts"],
        "line12d_fields": payload["line12d_today"]["form_fields_named_12d"],
        "bindings": payload["line12d_today"]["age_blind_bindings"],
    }, indent=2))


if __name__ == "__main__":
    main()
