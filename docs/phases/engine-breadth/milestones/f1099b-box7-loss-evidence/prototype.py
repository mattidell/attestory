"""Scratch core v84: Form 1099-B box 7 refuses only a loss on that statement.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box7-loss.md.
Charter: docs/reviews/f1099b-box7-loss/charter-p0.md.

Builds a scratch core outside the repository. Does not edit packages/ or a
published schema. The box 7 question is not replaced.

    python3 prototype.py /path/outside/the/repo
"""

from __future__ import annotations

import copy
import json
import os
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
FROM = {"package": "v83", "registry": "v81", "release": "v81"}
TO = {"package": "v84", "registry": "v82", "release": "v82"}
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
VERDICT = P + "f1099b.box7-sale-verdict"
INERT = P + "f1099b.box7-loss-check-inert-path-unwritten"


def _smaller() -> str:
    """Decision 6 trial. Unset keeps the 16-rule shape. Never the default."""
    return os.environ.get("BOX7_SMALLER") or ""

# slug, family version, column (h) object fields added after proceeds.
# "basis_field" is subtracted. Extra fields are added (the wash).
FAMILIES: tuple[dict[str, Any], ...] = (
    {"slug": "covered-st", "family_version": "v1", "basis": "basis", "adds": ()},
    {"slug": "covered-lt", "family_version": "v1", "basis": "basis", "adds": ()},
    {"slug": "covered-w-st", "family_version": "v2", "basis": "basis",
     "adds": ("box_1g_wash_sale_disallowed_amount",)},
    {"slug": "covered-w-lt", "family_version": "v2", "basis": "basis",
     "adds": ("box_1g_wash_sale_disallowed_amount",)},
    {"slug": "noncovered-st", "family_version": "v1", "basis": "basis", "adds": ("wash_disallowed",)},
    {"slug": "noncovered-lt", "family_version": "v1", "basis": "basis", "adds": ("wash_disallowed",)},
    {"slug": "code-b-st", "family_version": "v1", "basis": "corrected_basis", "adds": ("wash_disallowed",)},
    {"slug": "code-b-lt", "family_version": "v1", "basis": "corrected_basis", "adds": ("wash_disallowed",)},
)


def _pin(fact_id: str, version: str = "v1") -> dict[str, str]:
    return {"id": fact_id, "version": version}


def _ref(name: str, field: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"op": "ref", "name": name}
    if field is not None:
        out["field"] = field
    return out


def _literal(fact_id: str, value: str, version: str = "v1") -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": _pin(fact_id, version), "value": value}


def _column_h(txn: str, basis: str, adds: tuple[str, ...]) -> dict[str, Any]:
    node: dict[str, Any] = {"op": "subtract", "left": _ref(txn, "proceeds"), "right": _ref(txn, basis)}
    for field in adds:
        node = {"op": "add", "args": [node, _ref(txn, field)]}
    return node


def _keys() -> list[dict[str, Any]]:
    return [
        {"name": "broker", "kind": "entity", "entity_kind": "tax.us.f1099b-broker"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.f1099b-statement"},
        {"name": "transaction", "kind": "entity", "entity_kind": "tax.us.f1099b-transaction"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _verdict_rule(family: dict[str, Any]) -> dict[str, Any]:
    slug = family["slug"]
    txn = P + f"f1099b.{slug}-txn"
    symbol = P + f"f1099b.{slug}-txn.box7-verdict"
    loss = {
        "op": "all",
        "args": [
            {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": _ref(BOX7),
                "right": _literal(BOX7, "yes"),
            },
            {"op": "compare", "cmp": "lt", "left": _column_h(txn, family["basis"], family["adds"]), "right": 0},
        ],
    }
    return {
        "schema": "rule-artifact.v15",
        "id": P + f"rule.f1099b.{slug}-txn.box7-verdict",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "subject": _pin(txn),
        "requires": [txn, BOX7],
        "pins": [],
        "when": True,
        "value": {
            "op": "choose",
            "when": loss,
            "then": _literal(VERDICT, "disallowed"),
            "else": _literal(VERDICT, "clear"),
        },
        "publishes": symbol,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": (
            "One verdict per sale. disallowed when this sale's statement has box 7 checked and "
            "column (h) is strictly below zero. clear for a gain, for zero, and when box 7 is no. "
            "An unanswered box 7 blocks this sale and names the box 7 fact. Column (h) is read "
            "from the sale object, including a wash amount of zero."
        ),
    }


def _check_rule(family: dict[str, Any]) -> dict[str, Any]:
    slug = family["slug"]
    txn = P + f"f1099b.{slug}-txn"
    family_id = P + f"f1099b.{slug}"
    symbol = P + f"f1099b.{slug}-txn.box7-verdict"
    return {
        "schema": "rule-artifact.v15",
        "id": P + f"rule.f1099b.{slug}-txn.box7-loss-check",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "selection": {
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [
                {
                    "id": "sales",
                    "activity": {
                        "kind": "source_nonempty",
                        "source_family": _pin(family_id, family["family_version"]),
                        "member_fact_types": [_pin(txn)],
                    },
                    "reads_subject_results": [{"symbol": symbol, "subject": _pin(txn)}],
                    "requires": [],
                    "pins": [],
                    "when": {
                        "op": "require_paired",
                        "key": "statement",
                        "withholding": BOX7,
                        "income": [txn],
                    },
                    "value": {
                        "op": "choose",
                        "when": {
                            "op": "collect_categorical_all_equal",
                            "name": symbol,
                            "value": _literal(VERDICT, "clear"),
                        },
                        "then": 0,
                        "else": {"op": "block", "code": "DEPENDENCY_ABSENT"},
                    },
                },
                {
                    "id": "inert",
                    "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(INERT)]},
                    "reads_subject_results": [],
                    "requires": [],
                    "pins": [],
                    "when": True,
                    "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
                },
            ],
            "default": {
                "id": "neither",
                "reads_subject_results": [],
                "requires": [],
                "pins": [],
                "when": True,
                "value": 0,
            },
            "refusal": {
                "code": "DEPENDENCY_INVALID",
                "missing": [f"f1099b.{slug}-box7-loss-check-conflict"],
                "pins": [],
            },
        },
        "publishes": P + f"f1099b.{slug}-txn.box7-loss-check",
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": [],
        "notes": (
            "Publishes 0 when every sale in this family is clear, and when the family is empty. "
            "Blocks with nothing missing when a sale is disallowed, so Schedule D line 16 stays "
            "unpublished and the form-field explanation is the sentence. An unanswered box 7 "
            "blocks here and names the box 7 fact, so the existing question is asked."
        ),
    }


def _line16() -> dict[str, Any]:
    """Decision 5: v4 keeps the eight v3 sale-count requirements, then the family checks.

    The any-yes block stays out of ``value``. Counts stay in v3 order so a blocked
    row names the same unpublished counts. A published check is 0 and is not missing.
    """
    rule = json.loads((CONTENT / "rule.schedule-d-line16.v3.json").read_text(encoding="utf-8"))
    line7 = P + "schedule-d.line-7"
    line15 = P + "schedule-d.line-15"
    counts = [item for item in rule["requires"] if item not in {line7, line15}]
    if _smaller() == "verdicts-only":
        checks = [P + f"f1099b.{family['slug']}-txn.box7-verdict" for family in FAMILIES]
    else:
        checks = [P + f"f1099b.{family['slug']}-txn.box7-loss-check" for family in FAMILIES]
    rule["version"] = "v4"
    rule["requires"] = [line7, line15, *counts, *checks]
    rule["blocked"] = {"code": "DEPENDENCY_ABSENT", "missing": list(rule["requires"])}
    rule["value"] = {
        "op": "add",
        "args": [_ref(line7), _ref(line15)],
    }
    rule["notes"] = (
        "Part III line 16 = line 7 + line 15, signed. v4 still requires the eight sale-count "
        "symbols, in the same order as v3, so a recorded v83 return names the same missing counts. "
        "A box 7 yes no longer blocks the line by itself. Each sale family publishes a loss check. "
        "The check is 0 when every sale on a box 7 statement is a gain or zero, and it blocks when "
        "box 7 is checked and column (h) on that statement is below zero. An unanswered box 7 still "
        "blocks and asks the same question. This return does not compute the disallowed loss."
    )
    return rule


def _field() -> dict[str, Any]:
    field = json.loads((CONTENT / "schedule-d.line-16.form-field.v3.json").read_text(encoding="utf-8"))
    field["version"] = "v4"
    field["description"] = (
        "Schedule D (2025) Part III line 16 equals line 7 plus line 15. "
        "It is blocked while a recorded Form 1099-B statement has no box 7 answer, and when "
        "box 7 is checked and a sale on that statement is at a loss."
    )
    field["dispositions"]["published_value"]["explain"] = (
        "A current derived finding publishes line 16 equal to line 7 plus line 15."
    )
    field["dispositions"]["blocked"]["explain"] = (
        "Schedule D line 16 has no value yet. It is waiting for line 7 or line 15. "
        "It is also blocked while a recorded Form 1099-B statement has no answer about box 7. "
        "It is blocked when box 7 is checked and a sale on that statement is at a loss: "
        "a loss based on the box 1d amount is not allowed, and this return does not compute it."
    )
    return field


def _bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": P + "f1099b.box7-sale-verdict.vocabulary",
        "version": "v1",
        "label": "Whether a Form 1099-B sale on a box 7 statement is clear or a disallowed loss",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": VERDICT,
                "version": "v1",
                "title": "Derived domain for a per-sale box 7 verdict. Nothing asks the filer to record it.",
                "nature": "determinable",
                "identity_keys": _keys(),
                "value_schema": {
                    "oneOf": [
                        {"const": "clear", "description": "Box 7 is no, or column (h) is zero or a gain."},
                        {"const": "disallowed", "description": "Box 7 is yes and column (h) is below zero."},
                    ]
                },
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": INERT,
                "version": "v1",
                "title": "Never recorded. The second selection path each box 7 loss check requires.",
                "nature": "determinable",
                "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
                "value_schema": {"type": "boolean"},
                "supersession": {"policy": "free"},
            },
        ],
    }


def artifacts() -> list[tuple[str, dict[str, Any]]]:
    out = [("f1099b-box7-sale-verdict.bundle.json", _bundle())]
    for family in FAMILIES:
        slug = family["slug"]
        out.append((f"rule.f1099b.{slug}-txn.box7-verdict.json", _verdict_rule(family)))
        if _smaller() != "verdicts-only":
            out.append((f"rule.f1099b.{slug}-txn.box7-loss-check.json", _check_rule(family)))
    out.append(("rule.schedule-d-line16.v4.json", _line16()))
    out.append(("schedule-d.line-16.form-field.v4.json", _field()))
    return out


def role_for(schema: str) -> str:
    return {
        "bundle.v2": "fact-type-bundle",
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
    summary = {
        "from": FROM,
        "to": TO,
        "package": report["package"]["version"],
        "registry": TO["registry"],
        "release": report["release"]["version"],
        "question_unchanged": P + "input-question.f1099b-statement-box7-loss-not-allowed",
        "smaller": _smaller() or None,
        "members_edited": len(members),
        "added": sum(1 for member in members if member["op"] == "add"),
        "replaced": sum(1 for member in members if member["op"] == "replace"),
        "new_rules": sum(
            1 for member in members
            if member["op"] == "add" and member["new"]["schema"] == "rule-artifact.v15"
        ),
        "members": [
            [member["op"], member["new"]["id"].removeprefix(P), member["new"]["version"]]
            for member in members
        ],
        "inherited_inconsistencies": [list(row) for row in report.get("inherited_inconsistencies") or ()],
    }
    return summary


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
            raise SystemExit(f"prototype-build contains {needle}")
    if _smaller():
        (scratch / "build-summary.json").write_text(text, encoding="utf-8")
    else:
        (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    print(json.dumps({"added": summary["added"], "replaced": summary["replaced"],
                      "new_rules": summary["new_rules"], "smaller": summary["smaller"],
                      "package": summary["package"]}, indent=2))


if __name__ == "__main__":
    main()
