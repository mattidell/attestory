"""Scratch core v92: line 6c draws "not checked", and Schedule 1 cites its top entry.

Evidence for docs/phases/engine-breadth/milestones/page-alerts.md.
Charter: docs/reviews/page-alerts/charter-p0.md.

Builds a scratch core v92 on published v91 in a directory outside the
repository. Does not edit packages/. Two content successors:

- rule.form1040-line6c v2 publishes not_checked, and form1040.line-6c v2
  renders that word, when the lump-sum election was not made.
- schedule1.top-entry.form-field v2 carries a new citation citizen.
  The publishing rule is unchanged.

    python3 prototype.py <scratch-directory-outside-the-repo>
"""

from __future__ import annotations

import json
import re
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
FROM = {"package": "v91", "registry": "v89", "release": "v89"}
TO = {"package": "v92", "registry": "v90", "release": "v90"}
TOP_CITATION = P + "citation.schedule1.top-entry"


def _load(name: str) -> dict[str, Any]:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def line6c_rule() -> dict[str, Any]:
    body = _load("rule.form1040-line6c.json")
    body["version"] = "v2"
    body["value"] = "not_checked"
    body["notes"] = (
        "Line 6c lump-sum election checkbox. When no-lump-sum-election is yes, "
        "the checkbox is not checked, so the rule publishes not_checked. "
        "The page already draws that word. An election made (the fact is no) "
        "stays outside this rule."
    )
    return body


def line6c_field() -> dict[str, Any]:
    body = _load("form1040.line-6c.form-field.json")
    body["version"] = "v2"
    published = body["dispositions"]["published_value"]
    published["render"] = "not_checked"
    published["explain"] = "The lump-sum election checkbox is not checked."
    return body


def top_citation() -> dict[str, Any]:
    return {
        "authority": {"family": "irs-instructions", "form_id": "1040-SCH-1", "tax_year": 2025},
        "id": TOP_CITATION,
        "schema": "citation.v1",
        "version": "v1",
    }


def top_field() -> dict[str, Any]:
    body = _load("schedule1.top-entry.form-field.json")
    body["version"] = "v2"
    body["citation"] = {"id": TOP_CITATION, "version": "v1"}
    return body


def artifacts() -> list[tuple[str, dict[str, Any]]]:
    return [
        ("rule.form1040-line6c.v2.json", line6c_rule()),
        ("form1040.line-6c.form-field.v2.json", line6c_field()),
        ("citation.schedule1.top-entry.json", top_citation()),
        ("schedule1.top-entry.form-field.v2.json", top_field()),
    ]


def _pin(body: dict[str, Any], role: str) -> dict[str, str]:
    return {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role}


def change_list() -> dict[str, Any]:
    package = _load(f"package.core-calculations.{FROM['package']}.json")
    members = {member["id"]: member for member in package["members"]}
    rule_old = members[P + "rule.form1040-line6c"]
    field_old = members[P + "form1040.line-6c"]
    top_old = members[P + "schedule1.top-entry.form-field"]
    rule = line6c_rule()
    field = line6c_field()
    citation = top_citation()
    top = top_field()
    return {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": [
            {"op": "replace", "old": rule_old, "new": _pin(rule, "computation")},
            {"op": "replace", "old": field_old, "new": _pin(field, "form-field")},
            {"op": "add", "new": _pin(citation, "citation")},
            {"op": "replace", "old": top_old, "new": _pin(top, "form-field")},
        ],
        "entrypoints": [
            {
                "op": "replace",
                "old": {"id": rule["id"], "version": "v1"},
                "new": {"id": rule["id"], "version": "v2"},
            },
            {
                "op": "replace",
                "old": {"id": top["id"], "version": "v1"},
                "new": {"id": top["id"], "version": "v2"},
            },
        ],
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }


def build(scratch: Path) -> dict[str, Any]:
    content = scratch / "content"
    releases = scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    for name, body in artifacts():
        (content / name).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes = change_list()
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
        "members": [
            ["computation", "rule.form1040-line6c", "v1", "v2", "value not_checked"],
            ["form-field", "form1040.line-6c", "v1", "v2", "render not_checked"],
            ["citation", "citation.schedule1.top-entry", None, "v1", "added"],
            ["form-field", "schedule1.top-entry.form-field", "v1", "v2", "citation added"],
        ],
        "entrypoints_replaced": [
            "rule.form1040-line6c v1 to v2",
            "schedule1.top-entry.form-field v1 to v2",
        ],
        "unchanged": [
            "rule.schedule1-top-entry stays v3",
            "form1040.line-6c stays a member, not an entrypoint",
            "citation.form1040.line-6c stays v1 and stays on the line 6c field",
        ],
        "inherited_inconsistencies": [
            list(row) for row in report.get("inherited_inconsistencies") or ()
        ],
        "design": (
            "Content successors only. Line 6c publishes and renders not_checked "
            "when the election was not made. The Schedule 1 top entry gains a "
            "citation. No engine, schema, projection, page or kernel change."
        ),
    }


def public_error(exc: BaseException) -> str:
    return re.sub(r"(?:/Users|/private|/tmp|/var)/\S+", "[path]", f"{type(exc).__name__}: {exc}")[:800]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    try:
        summary = build(scratch)
    except Exception as exc:  # noqa: BLE001 - a refused build is the finding
        summary = {"from": FROM, "to": TO, "refused": public_error(exc)}
    text = json.dumps(summary, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"prototype summary contains {needle}")
    (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    print(json.dumps(
        {k: summary.get(k) for k in ("package", "release", "refused", "design", "inherited_inconsistencies")},
        indent=2,
    ))


if __name__ == "__main__":
    main()
