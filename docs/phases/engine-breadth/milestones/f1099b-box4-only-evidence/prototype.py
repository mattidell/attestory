"""Scratch core v85: ask for box 4 withholding on a Form 1099-B with no sale.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box4-only.md.
Charter: docs/reviews/f1099b-box4-only/charter-p0.md.

Builds a scratch core outside the repository. Does not edit packages/ or a
published schema.

    python3 prototype.py /path/outside/the/repo
"""

from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"package": "v84", "registry": "v82", "release": "v82"}
TO = {"package": "v85", "registry": "v83", "release": "v83"}
PRESENT = P + "f1099b.no-sale-box4-present"
AMOUNT = P + "f1099b.no-sale-box4-withholding"
SUBTOTAL = P + "f1099b.b4-withholding-subtotal"


def _pin(fact_id: str, version: str = "v1") -> dict[str, str]:
    return {"id": fact_id, "version": version}


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _literal(fact_id: str, value: str, version: str = "v1") -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": _pin(fact_id, version), "value": value}


def _eq(name: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": _ref(name),
        "right": _literal(name, value),
    }


def _bundle() -> dict[str, Any]:
    year_key = {"name": "tax-year", "kind": "literal", "values": ["2025"]}
    return {
        "schema": "bundle.v2",
        "id": P + "f1099b.no-sale-box4",
        "version": "v1",
        "label": "Form 1099-B box 4 withholding on a statement with no closed sale",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": PRESENT,
                "version": "v1",
                "title": (
                    "Whether the filer received a 2025 Form 1099-B or substitute statement "
                    "that shows federal income tax withheld in box 4 and reports no closed sale."
                ),
                "nature": "determinable",
                "identity_keys": [year_key],
                "value_schema": {
                    "oneOf": [
                        {"const": "yes", "description": "Such a statement was received."},
                        {"const": "no", "description": "No such statement was received."},
                    ]
                },
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": AMOUNT,
                "version": "v1",
                "title": (
                    "Federal income tax withheld in box 4 of 2025 Form 1099-B or substitute "
                    "statements that report no closed sale. One nonnegative total for the return."
                ),
                "nature": "determinable",
                "identity_keys": [year_key],
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
            },
        ],
    }


def _present_question() -> dict[str, Any]:
    return {
        "schema": "input-question.v1",
        "id": P + "input-question.f1099b-no-sale-box4-present",
        "version": "v1",
        "fact_type": _pin(PRESENT),
        "question": (
            "Did you receive a Form 1099-B or substitute statement that shows federal income "
            "tax withheld in box 4 and reports no closed sale (for example, a short sale still "
            "open at year end)?"
        ),
    }


def _amount_question() -> dict[str, Any]:
    return {
        "schema": "input-question.v1",
        "id": P + "input-question.f1099b-no-sale-box4-amount",
        "version": "v1",
        "fact_type": _pin(AMOUNT),
        "question": (
            "Enter the federal income tax withheld in box 4 of Form 1099-B or substitute "
            "statements that report no closed sale. If more than one such statement, enter "
            "the total. If box 4 is blank, enter $0."
        ),
    }


def _no_sale_addend() -> dict[str, Any]:
    return {
        "op": "choose",
        "when": _eq(PRESENT, "yes"),
        "then": _ref(AMOUNT),
        "else": 0,
    }


def _answered() -> dict[str, Any]:
    return {"op": "any", "args": [_eq(PRESENT, "yes"), _eq(PRESENT, "no")]}


def _line25b() -> dict[str, Any]:
    rule = json.loads((CONTENT / "rule.form1040-line25b.v7.json").read_text(encoding="utf-8"))
    rule["version"] = "v8"
    rule["notes"] = (
        rule["notes"]
        + " v8: also asks whether any Form 1099-B shows box 4 withholding and no closed sale. "
        "A yes adds that withholding to line 25b. A no adds nothing new. Line 25b cannot "
        "publish while that question is unanswered."
    )
    addend = _no_sale_addend()
    for arm in ("then", "else"):
        rule["value"][arm]["value"]["args"].append(copy.deepcopy(addend))
    when = rule["when"]
    assert when["op"] == "all"
    when["args"].append(_answered())
    return rule


def _field() -> dict[str, Any]:
    field = json.loads((CONTENT / "form1040.line-25b.form-field.v5.json").read_text(encoding="utf-8"))
    field["version"] = "v6"
    field["description"] = (
        field["description"]
        + " It also includes box 4 withholding from a Form 1099-B that reports no closed sale."
    )
    field["dispositions"]["blocked"]["explain"] = (
        "Form 1040 line 25b is blocked because an input it needs is missing or not yet closed. "
        "It is also blocked while a recorded sale's statement has no box 4 amount, and while "
        "it is unanswered whether a Form 1099-B shows box 4 withholding and no closed sale."
    )
    field["dispositions"]["published_value"]["explain"] = (
        field["dispositions"]["published_value"]["explain"]
        + " That total includes backup withholding from a Form 1099-B with no closed sale."
    )
    return field


def artifacts() -> list[tuple[str, dict[str, Any]]]:
    return [
        ("f1099b-no-sale-box4.bundle.json", _bundle()),
        ("input-question.f1099b-no-sale-box4-present.v1.json", _present_question()),
        ("input-question.f1099b-no-sale-box4-amount.v1.json", _amount_question()),
        ("rule.form1040-line25b.v8.json", _line25b()),
        ("form1040.line-25b.form-field.v6.json", _field()),
    ]


def role_for(schema: str) -> str:
    return {
        "bundle.v2": "fact-type-bundle",
        "input-question.v1": "input-question",
        "rule-artifact.v15": "computation",
        "form-field.v3": "form-field",
    }[schema]


def change_list() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    package = json.loads((CONTENT / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
    members_now = {member["id"]: member for member in package["members"]}
    entry_keys = {(entry["id"], entry["version"]) for entry in package["entrypoints"]}
    members: list[dict[str, Any]] = []
    entrypoints: list[dict[str, Any]] = []
    for _name, body in artifacts():
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role_for(body["schema"])}
        old = members_now.get(body["id"])
        if old is not None:
            members.append({"op": "replace", "old": dict(old), "new": new})
            if (old["id"], old["version"]) in entry_keys:
                entrypoints.append({
                    "op": "replace",
                    "old": {"id": old["id"], "version": old["version"]},
                    "new": {"id": new["id"], "version": new["version"]},
                })
        else:
            members.append({"op": "add", "new": new})
            entrypoints.append({"op": "add", "value": {"id": new["id"], "version": new["version"]}})
    changes = {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": members,
        "entrypoints": entrypoints,
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    return changes, members


def build(scratch: Path) -> dict[str, Any]:
    content = scratch / "content"
    releases = scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    for name, body in artifacts():
        (content / name).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes, members = change_list()
    changes_path = scratch / "changes.json"
    changes_path.write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / f"package.core-calculations.{FROM['package']}.json",
        content / f"published-packages.{FROM['registry']}.json",
        releases / f"{RELEASE_STEM}.{FROM['release']}.json",
        content,
        changes_path,
        scratch / "out",
    )
    for src, folder, target in (
        ("package.json", content, f"package.core-calculations.{TO['package']}.json"),
        ("registry.json", content, f"published-packages.{TO['registry']}.json"),
        ("release.json", releases, f"{RELEASE_STEM}.{TO['release']}.json"),
    ):
        shutil.copy(scratch / "out" / src, folder / target)
    core = {
        "version": TO["package"],
        "registry": TO["registry"],
        "release_version": TO["release"],
        "content": str(content),
        "releases": str(releases),
        "loader_from": FROM["package"],
    }
    (scratch / "core.json").write_text(json.dumps(core, indent=2) + "\n", encoding="utf-8")
    return {
        "from": FROM,
        "to": TO,
        "package": report["package"]["version"],
        "registry": TO["registry"],
        "release": report["release"]["version"],
        "members_edited": len(members),
        "added": sum(1 for member in members if member["op"] == "add"),
        "replaced": sum(1 for member in members if member["op"] == "replace"),
        "members": [
            [member["op"], member["new"]["id"].removeprefix(P), member["new"]["version"]]
            for member in members
        ],
        "inherited_inconsistencies": [list(row) for row in report.get("inherited_inconsistencies") or ()],
        "present_question": _present_question()["question"],
        "amount_question": _amount_question()["question"],
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    summary = build(scratch)
    text = json.dumps(summary, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"prototype summary contains {needle}")
    (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    print(json.dumps({
        "package": summary["package"],
        "added": summary["added"],
        "replaced": summary["replaced"],
        "output": "prototype-build.json",
    }, indent=2))


if __name__ == "__main__":
    main()
