"""Scratch core v91: the preferential-base guard names its questions.

Published core v90 stays untouched. The scratch copy is a content successor
of ``rule.selected-preferential-base`` on ``rule-artifact.v17``, the same
shape Form 1040 line 16 has used since core v89. When Schedule D is required
and no sale is recorded, the guard blocks and names the four questions line
16 already names. Every other result of the guard is unchanged.

    python3 prototype.py <scratch-directory>
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
NAMED = [Q1, Q2, NO_8949, PATH_B]
RULE = "rule.selected-preferential-base.v10.json"
SUCCESSOR = "rule.selected-preferential-base.v11.json"


def _conclusion_is_no(node: Any) -> bool:
    return (
        isinstance(node, dict)
        and node.get("op") == "categorical_compare"
        and str((node.get("left") or {}).get("name", "")).endswith("schedule-d-required.conclusion")
        and (node.get("right") or {}).get("value") == "no"
    )


def name_the_question(when: dict[str, Any]) -> int:
    """The no-activity arm stays true when Schedule D is not required.

    When Schedule D is required, that arm blocks with line 16's four names
    instead of making the whole guard false.
    """
    found = 0

    def walk(node: Any) -> None:
        nonlocal found
        if isinstance(node, dict):
            if (
                node.get("op") == "choose"
                and node.get("then") is True
                and _conclusion_is_no(node.get("else"))
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


def successor_body() -> dict[str, Any]:
    body = json.loads((CONTENT / RULE).read_text(encoding="utf-8"))
    body["schema"] = "rule-artifact.v17"
    body["version"] = "v11"
    if name_the_question(body["when"]) != 1:
        raise SystemExit("the Schedule D required arm was not found exactly once")
    return body


def changes(body: dict[str, Any]) -> dict[str, Any]:
    package = json.loads((CONTENT / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
    current = {member["id"]: member for member in package["members"]}
    old = current[body["id"]]
    new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": "computation"}
    replaced = {"op": "replace", "old": {"id": old["id"], "version": old["version"]},
                "new": {"id": new["id"], "version": new["version"]}}
    return {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": [{"op": "replace", "old": dict(old), "new": new}],
        "entrypoints": [replaced],
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(scratch: Path) -> dict[str, Any]:
    if scratch.exists():
        raise SystemExit("scratch directory already exists")
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    body = successor_body()
    (content / SUCCESSOR).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes_path = scratch / "changes.json"
    changes_path.write_text(json.dumps(changes(body), indent=2) + "\n", encoding="utf-8")
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
    checksum = citizen_checksum(json.loads((content / SUCCESSOR).read_text(encoding="utf-8")))
    matched = False
    for citizen in registry["citizens"]:
        if citizen["id"] == body["id"] and citizen["version"] == body["version"]:
            citizen["checksum"] = checksum
            matched = True
    if not matched:
        raise SystemExit("successor is missing from the generated registry")
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
        "successor": SUCCESSOR,
        "schema": "rule-artifact.v17",
        "named_questions": [name.removeprefix(P) for name in NAMED],
        "guard": "no recorded sale and Schedule D required blocks with those names; Schedule D not required still publishes",
    }
    text = json.dumps(summary, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit("prototype summary contains a local path")
    (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    return summary


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py <scratch-directory>")
    summary = build(Path(sys.argv[1]))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
