"""Scratch core v83 prototype for Form 1099-B backup withholding.

Evidence for docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md.
Charter: docs/reviews/f1099b-backup-withholding/charter-p0.md (Scope 4).

Builds a scratch core v83 in a temporary directory outside the repository:
- Fact type: tax.us.2025.f1099b.statement-box4-withholding (number, min 0, keys: statement, tax-year)
- Bundle: f1099b.statement-boxes.vocabulary v2
- Input question: input-question.f1099b-box4 v1
- Rule: rule.form1040-line25b v7 (require_paired on statement key, adds box 4 to line 25b)
- Form field: form1040.line-25b v5 (updated descriptions, retires temporary refusal sentence)

Generates package v83, registry v81, and release v81 from core v82 with tools.package_successor.
Writes prototype-build.json beside this file.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
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

FROM = {"package": "v82", "registry": "v80", "release": "v80"}
TO = {"package": "v83", "registry": "v81", "release": "v81"}


def artifacts() -> list[tuple[str, dict[str, Any]]]:
    """Successor artifacts for scratch core v83."""
    out: list[tuple[str, dict[str, Any]]] = []

    # 1. Bundle: f1099b-box4.bundle.json
    bundle_b4 = {
        "schema": "bundle.v2",
        "id": P + "f1099b.box4",
        "version": "v1",
        "label": "Form 1099-B box 4 federal income tax withheld vocabulary",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": P + "f1099b.statement-box4-withholding",
                "version": "v1",
                "title": "Federal income tax withheld in box 4 of one recorded 2025 Form 1099-B statement. Nonnegative source amount only.",
                "nature": "determinable",
                "identity_keys": [
                    {
                        "name": "statement",
                        "kind": "entity",
                        "entity_kind": "tax.us.f1099b-statement",
                    },
                    {
                        "name": "tax-year",
                        "kind": "literal",
                        "values": ["2025"],
                    },
                ],
                "value_schema": {
                    "type": "number",
                    "minimum": 0,
                },
                "supersession": {
                    "policy": "free",
                },
            }
        ],
    }
    out.append(("f1099b-box4.bundle.json", bundle_b4))

    # 2. Input question: input-question.f1099b-box4.v1.json
    q_b4 = {
        "schema": "input-question.v1",
        "id": P + "input-question.f1099b-box4",
        "version": "v1",
        "fact_type": {
            "id": P + "f1099b.statement-box4-withholding",
            "version": "v1",
        },
        "question": "Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from. If box 4 is blank, enter $0.",
    }
    out.append(("input-question.f1099b-box4.v1.json", q_b4))

    # 3. Family: family.f1099b-b4.v1.json
    family_b4 = {
        "schema": "source-family.v1",
        "id": P + "f1099b.b4",
        "version": "v1",
        "title": "Form 1099-B box 4 statement items, tax year 2025",
        "scope": {
            "family": "individual-income-tax",
            "jurisdiction": "US-federal",
            "tax_year": 2025,
        },
        "member_predicate": {
            "fact_type": P + "f1099b.statement-box4-withholding",
        },
        "authorizes_subtotal": P + "payments.line25b",
        "closure_claim": (
            "Every federal income tax withheld amount reported in box 4 of a Form 1099-B furnished "
            "to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon. "
            "Closed with members authorizes the sum of current members; closed-empty authorizes subtotal 0."
        ),
    }
    out.append(("family.f1099b-b4.json", family_b4))

    # 4. Rule: rule.form1040-line25b.v7.json
    rule_v6 = json.loads((CONTENT / "rule.form1040-line25b.v6.json").read_text(encoding="utf-8"))
    rule_v7 = copy.deepcopy(rule_v6)
    rule_v7["version"] = "v7"
    rule_v7["notes"] = (
        "Form 1040 line 25b: 'Add the amounts shown as federal income tax withheld' on Forms 1099-INT, "
        "1099-DIV, 1099-R box 4, 1099-G box 4, SSA-1099 box 6, and Form 1099-B box 4 backup withholding "
        "(i1040gi-2025 line 25b). Each document's own subtotal rule is pinned and added here, one addend per "
        "document. v7: pairs Form 1099-B statements with statement-box4-withholding via require_paired; "
        "when sales exist, collects and sums statement-box4-withholding into line 25b; when no sales exist, "
        "sums the five 1099 subtotals."
    )

    # In when: replace statement-box4-withholding-reported with statement-box4-withholding in require_paired
    when_all = rule_v7["when"]["args"]
    for i, node in enumerate(when_all):
        if isinstance(node, dict) and node.get("op") == "require_paired" and "f1099b.statement-box4" in str(node.get("withholding")):
            when_all[i] = {
                "op": "require_paired",
                "key": "statement",
                "withholding": P + "f1099b.statement-box4-withholding",
                "income": node["income"],
            }

    # In value: choose when sale counts > 0 then sum 5 subtotals + collect(statement-box4-withholding) else sum 5 subtotals
    five_subtotals = [
        {"name": P + "interest.b4-withholding-subtotal", "op": "ref"},
        {"name": P + "dividends.b4-withholding-subtotal", "op": "ref"},
        {"name": P + "ira.box4-withholding-subtotal", "op": "ref"},
        {"name": P + "unemployment.b4-withholding-subtotal", "op": "ref"},
        {"name": P + "ssa1099.b6-withholding-subtotal", "op": "ref"},
    ]
    six_addends = [
        *five_subtotals,
        {
            "op": "add",
            "args": [
                {
                    "op": "collect",
                    "name": P + "f1099b.statement-box4-withholding",
                    "source_set": P + "f1099b.b4",
                }
            ],
        },
    ]

    sale_count_checks = [
        {"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": P + f"f1099b.{fam}-count"}, "right": 0}
        for fam in (
            "covered-st", "covered-lt", "covered-w-st", "covered-w-lt",
            "noncovered-st", "noncovered-lt", "code-b-st", "code-b-lt",
        )
    ]

    rule_v7["value"] = {
        "op": "choose",
        "when": {
            "op": "any",
            "args": sale_count_checks,
        },
        "then": {
            "op": "round",
            "mode": {"name": "rounding.convention", "op": "ref"},
            "value": {
                "op": "add",
                "args": six_addends,
            },
        },
        "else": {
            "op": "round",
            "mode": {"name": "rounding.convention", "op": "ref"},
            "value": {
                "op": "add",
                "args": five_subtotals,
            },
        },
    }
    out.append(("rule.form1040-line25b.v7.json", rule_v7))

    # 4. Form field: form1040.line-25b.form-field.v5.json
    field_v4 = json.loads((CONTENT / "form1040.line-25b.form-field.v4.json").read_text(encoding="utf-8"))
    field_v5 = copy.deepcopy(field_v4)
    field_v5["version"] = "v5"
    field_v5["description"] = (
        "Form 1040 line 25b: federal income tax withheld from Form(s) 1099 "
        "(Forms 1099-INT, 1099-DIV and 1099-R box 4, Form 1099-G box 4, Form SSA-1099 box 6, and Form 1099-B box 4 backup withholding)."
    )
    field_v5["dispositions"]["blocked"]["explain"] = (
        "Form 1040 line 25b is blocked because an input it needs is missing or not yet closed. "
        "It is also blocked while a recorded Form 1099-B statement has no answer about box 4."
    )
    field_v5["dispositions"]["published_value"]["explain"] = (
        "Form 1040 line 25b is the total of the 1099-document withholding amounts, with cents included, "
        "rounded once to whole dollars: Forms 1099-INT, 1099-DIV and 1099-R box 4, Form 1099-G box 4, "
        "Form SSA-1099 box 6, and Form 1099-B box 4 backup withholding."
    )
    out.append(("form1040.line-25b.form-field.v5.json", field_v5))

    return out


def role_for(schema: str) -> str:
    roles = {
        "bundle.v2": "fact-type-bundle",
        "input-question.v1": "input-question",
        "source-family.v1": "source-family",
        "rule-artifact.v15": "computation",
        "form-field.v3": "form-field",
    }
    return roles[schema]


def change_list() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    pkg_v82 = json.loads((CONTENT / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
    members_v82 = {m["id"]: m for m in pkg_v82["members"]}
    entry_keys = {(e["id"], e["version"]) for e in pkg_v82["entrypoints"]}

    members: list[dict[str, Any]] = []
    entrypoints: list[dict[str, Any]] = []

    for _name, body in artifacts():
        cid = body["id"]
        cver = body["version"]
        cschema = body["schema"]
        new_m = {"id": cid, "version": cver, "schema": cschema, "role": role_for(cschema)}
        old_m = members_v82.get(cid)
        if old_m is not None:
            members.append({"op": "replace", "old": dict(old_m), "new": new_m})
            if (old_m["id"], old_m["version"]) in entry_keys:
                entrypoints.append({
                    "op": "replace",
                    "old": {"id": old_m["id"], "version": old_m["version"]},
                    "new": {"id": cid, "version": cver},
                })
        else:
            members.append({"op": "add", "new": new_m})
            entrypoints.append({"op": "add", "value": {"id": cid, "version": cver}})

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

    # Write new successor artifacts to content
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

    summary = {
        "from": FROM,
        "to": TO,
        "package": report["package"]["version"],
        "registry": TO["registry"],
        "release": report["release"]["version"],
        "members_edited": len(members),
        "added": sum(1 for m in members if m["op"] == "add"),
        "replaced": sum(1 for m in members if m["op"] == "replace"),
        "members": [
            [m["op"], m["new"]["id"].removeprefix(P), m["new"]["version"]]
            for m in members
        ],
        "inherited_inconsistencies": [list(r) for r in report.get("inherited_inconsistencies") or ()],
    }
    return summary


def main() -> None:
    scratch = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (Path(tempfile.gettempdir()) / "scratch-core-v83").resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")

    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)

    print(f"Building scratch core v83 in {scratch}...")
    summary = build(scratch)

    out_file = HERE / "prototype-build.json"
    out_file.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_file.name}")

    core = {
        "version": TO["package"],
        "registry": TO["registry"],
        "release_version": TO["release"],
        "content": str(scratch / "content"),
        "releases": str(scratch / "releases"),
        "loader_from": FROM["package"],
    }
    (scratch / "core.json").write_text(json.dumps(core) + "\n", encoding="utf-8")
    print("core:", json.dumps(core, indent=2))


if __name__ == "__main__":
    main()
