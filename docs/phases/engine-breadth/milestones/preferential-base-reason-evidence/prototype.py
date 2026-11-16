"""Scratch core v91: the preferential-base guard names eight questions.

Published core v90 stays untouched. The scratch copy is a content successor
of ``rule.selected-preferential-base`` on ``rule-artifact.v17``. When
Schedule D is required and no sale is recorded, the guard blocks and names
the four sale questions and the four Exception 1 questions. Every other
result of the guard is unchanged.

``rule.form1040-line16`` v9 names those eight questions only in that same
state. Every other line 16 block keeps the four sale questions.

    python3 prototype.py <scratch-directory>
    python3 prototype.py line16 <scratch-directory>
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation.package_validation import citizen_checksum  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"package": "v90", "registry": "v88", "release": "v88"}
TO = {"package": "v91", "registry": "v89", "release": "v89"}
Q1 = P + "f1099b.noncovered-sold.source-closure"
Q2 = P + "f8949.no1099b-sold.source-closure"
NO_8949 = P + "schedule-d-boundary.no-form8949-sources"
PATH_B = P + "schedule-d-boundary.no-other-form8949-adjustments"
FOUR = [Q1, Q2, NO_8949, PATH_B]
EXC = [
    P + "exception1.only-box2a-capital-gains",
    P + "exception1.no-capital-losses",
    P + "exception1.no-qof-deferral",
    P + "exception1.no-boxes-2b-2c-2d",
]
NAMED = FOUR + EXC
RULE = "rule.selected-preferential-base.v10.json"
SUCCESSOR = "rule.selected-preferential-base.v11.json"
LINE16_RULE = "rule.form1040-line16.v8.json"
LINE16_SUCCESSOR = "rule.form1040-line16.v9.json"
CONCLUSION = P + "schedule-d-required.conclusion"


def _conclusion_eq(node: Any, value: str) -> bool:
    return (
        isinstance(node, dict)
        and node.get("op") == "categorical_compare"
        and str((node.get("left") or {}).get("name", "")).endswith("schedule-d-required.conclusion")
        and (node.get("right") or {}).get("value") == value
    )


def _four_block(node: Any) -> bool:
    return (
        isinstance(node, dict)
        and node.get("op") == "block"
        and node.get("code") == "DEPENDENCY_ABSENT"
        and node.get("missing") == FOUR
    )


def name_the_question(when: dict[str, Any]) -> int:
    """The no-activity arm stays true when Schedule D is not required.

    When Schedule D is required, that arm blocks with the eight names
    instead of making the whole guard false.
    """
    found = 0

    def walk(node: Any) -> None:
        nonlocal found
        if isinstance(node, dict):
            if (
                node.get("op") == "choose"
                and node.get("then") is True
                and _conclusion_eq(node.get("else"), "no")
            ):
                node["else"] = {
                    "op": "choose",
                    "when": node["else"],
                    "then": True,
                    "else": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": list(NAMED)},
                }
                found += 1
                return
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(when)
    return found


def name_line16(when: dict[str, Any]) -> int:
    """Eight names only when the published four-name block is Schedule D required.

    The published else stays the four sale questions on every other result.
    """
    found = 0

    def walk(node: Any) -> None:
        nonlocal found
        if isinstance(node, dict):
            if node.get("op") == "choose" and _four_block(node.get("else")):
                node["else"] = {
                    "op": "choose",
                    "when": {
                        "op": "categorical_compare",
                        "cmp": "eq",
                        "left": {"op": "ref", "name": CONCLUSION},
                        "right": {
                            "op": "category_literal",
                            "fact_type": {"id": CONCLUSION, "version": "v1"},
                            "value": "yes",
                        },
                    },
                    "then": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": list(NAMED)},
                    "else": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": list(FOUR)},
                }
                found += 1
                return
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(when)
    return found


def successor_body() -> dict[str, Any]:
    body = json.loads((CONTENT / RULE).read_text(encoding="utf-8"))
    body["schema"] = "rule-artifact.v17"
    body["version"] = "v11"
    if name_the_question(body["when"]) != 1:
        raise SystemExit("the Schedule D required arm was not found exactly once")
    return body


def line16_body() -> dict[str, Any]:
    body = json.loads((CONTENT / LINE16_RULE).read_text(encoding="utf-8"))
    body["version"] = "v9"
    note = str(body.get("notes") or "")
    body["notes"] = note + (
        " v9: where Schedule D is required and no sale is recorded, the block names"
        " the four sale questions and the four Exception 1 questions. Every other"
        " block keeps the four sale questions."
    )
    if name_line16(body["when"]) != 1:
        raise SystemExit("line 16's four-name block was not found exactly once")
    return body


def artifacts() -> list[tuple[str, dict[str, Any]]]:
    """The published successor. Line 16 v9 stays out: the gate parks it."""
    return [(SUCCESSOR, successor_body())]


def changes(bodies: list[dict[str, Any]]) -> dict[str, Any]:
    package = json.loads((CONTENT / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
    current = {member["id"]: member for member in package["members"]}
    members = []
    entrypoints = []
    for body in bodies:
        old = current[body["id"]]
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": "computation"}
        members.append({"op": "replace", "old": dict(old), "new": new})
        entrypoints.append({
            "op": "replace",
            "old": {"id": old["id"], "version": old["version"]},
            "new": {"id": new["id"], "version": new["version"]},
        })
    return {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": members,
        "entrypoints": entrypoints,
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(scratch: Path, written: list[tuple[str, dict[str, Any]]], *, record: bool) -> dict[str, Any]:
    if scratch.exists():
        raise SystemExit("scratch directory already exists")
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    for name, body in written:
        (content / name).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes_path = scratch / "changes.json"
    changes_path.write_text(json.dumps(changes([body for _name, body in written]), indent=2) + "\n", encoding="utf-8")
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
    registry_path = content / f"published-packages.{TO['registry']}.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for name, body in written:
        checksum = citizen_checksum(json.loads((content / name).read_text(encoding="utf-8")))
        matched = False
        for citizen in registry["citizens"]:
            if citizen["id"] == body["id"] and citizen["version"] == body["version"]:
                citizen["checksum"] = checksum
                matched = True
        if not matched:
            raise SystemExit("successor is missing from the generated registry: " + name)
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    release_path = releases / f"{RELEASE_STEM}.{TO['release']}.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release["package_registry_sha256"] = sha(registry_path)
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
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
        "successors": [name for name, _body in written],
        "schema": "rule-artifact.v17",
        "named_questions": [name.removeprefix(P) for name in NAMED],
        "guard": "no recorded sale and Schedule D required blocks with the eight names; every other guard result is unchanged",
        "line16": (
            "included"
            if any(name == LINE16_SUCCESSOR for name, _body in written)
            else "parked; line16-gate.json shows v9 changes exception1_personal_loss_8949"
        ),
    }
    if record:
        text = json.dumps(summary, indent=2) + "\n"
        for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
            if needle in text:
                raise SystemExit("prototype summary contains a local path")
        (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    return summary


def main() -> None:
    if len(sys.argv) == 2:
        summary = build(Path(sys.argv[1]), artifacts(), record=True)
    elif len(sys.argv) == 3 and sys.argv[1] == "line16":
        summary = build(Path(sys.argv[2]), [(LINE16_SUCCESSOR, line16_body())], record=False)
    else:
        raise SystemExit("usage: prototype.py <scratch-directory> | prototype.py line16 <scratch-directory>")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
