"""Scratch core v103 from published v102: worksheet lines 6 and 13 read the status tests.

Run: python3 build.py <new-directory-outside-repository>

Copies published content and releases outside the repository, writes the two
successor rules from design.py, and validates the package, registry and
release with tools.package_successor.generate_to_directory. Nothing under
packages/ is edited. Writes build.json beside this file.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools.package_successor import SuccessorError, generate_to_directory  # noqa: E402

STEM = "demo.release.sli-worksheet-integration.2025"
PATH_IN_TEXT = re.compile(r"/(?:Users|private|tmp|var)/\S+")


def _design():
    spec = importlib.util.spec_from_file_location("hnw_p0_design", HERE / "design.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pinned(node: object, targets: set[tuple[str, str]], found: list[tuple[str, str]]) -> None:
    if isinstance(node, dict):
        if (node.get("id"), node.get("version")) in targets:
            found.append((node["id"], node["version"]))
        for value in node.values():
            _pinned(value, targets, found)
    elif isinstance(node, list):
        for value in node:
            _pinned(value, targets, found)


def _scrub(text: str) -> str:
    return PATH_IN_TEXT.sub("<path>", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch")
    args = parser.parse_args()
    design = _design()
    scratch = Path(args.scratch).resolve()
    if REPO in scratch.parents or scratch == REPO or scratch.exists():
        raise SystemExit("scratch must be a new directory outside the repository")
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    written = design.written(source)
    shutil.copytree(source, content)
    shutil.copytree(releases, rel)
    package = json.loads((source / "package.core-calculations.v102.json").read_text(encoding="utf-8"))
    files: dict[tuple[str, str], dict] = {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = body
    replaced = {design.LINE6: "v1", design.LINE13: "v1"}
    for rule_id, version in replaced.items():
        assert any(member["id"] == rule_id and member["version"] == version for member in package["members"]), rule_id
    found: list[tuple[str, str]] = []
    for member in package["members"]:
        if member["id"] not in replaced:
            body = files[(member["id"], member["version"])]
            _pinned({key: value for key, value in body.items() if key != "id"}, set(replaced.items()), found)
    if found:
        raise SystemExit(f"another member pins a replaced rule: {found}")
    for name, body in written.items():
        target = content / name
        if target.exists():
            raise SystemExit(f"successor file already in the copy: {name}")
        target.write_text(design.dump(body), encoding="utf-8")
    members = []
    for rule_id, filename in ((design.LINE6, design.LINE6_FILE), (design.LINE13, design.LINE13_FILE)):
        old = next(member for member in package["members"] if member["id"] == rule_id)
        new_body = written[filename]
        members.append({"op": "replace", "old": old, "new": {**old, "version": new_body["version"], "schema": new_body["schema"]}})
    changes = {
        "package_version": "v103",
        "release_version": "v101",
        "members": members,
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    output: dict = {
        "from": {"core": "v102", "registry": "v100", "release": "v100"},
        "to": {"core": "v103", "registry": "v101", "release": "v101"},
        "label": "scratch successor of published v102; the published number waits on the foreman because eic-separated-married is using v103",
        "replaced_rules_pinned_by": found,
        "written": {name: hashlib.sha256(design.dump(body).encode()).hexdigest() for name, body in written.items()},
        "bytes": {name: len(design.dump(body).encode()) for name, body in written.items()},
    }
    out_path = HERE / "build.json"
    try:
        report = generate_to_directory(
            content / "package.core-calculations.v102.json",
            content / "published-packages.v100.json",
            rel / (STEM + ".v100.json"),
            content,
            scratch / "changes.json",
            scratch / "generated",
        )
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": _scrub(str(exc))[:2000]})
        text = json.dumps(output, indent=2) + "\n"
        if PATH_IN_TEXT.search(text):
            raise SystemExit("build.json would contain a local path")
        out_path.write_text(text, encoding="utf-8")
        raise SystemExit(output["failure"])
    for src, dst in (
        ("package.json", content / "package.core-calculations.v103.json"),
        ("registry.json", content / "published-packages.v101.json"),
        ("release.json", rel / (STEM + ".v101.json")),
    ):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({
        "version": "v103", "registry": "v101", "release_version": "v101",
        "content": str(content), "releases": str(rel), "loader_from": "v102",
    }, indent=2) + "\n", encoding="utf-8")
    generation = {key: value for key, value in report.items() if isinstance(value, (str, int, bool))} if isinstance(report, dict) else {}
    output.update({
        "status": "valid",
        "validation": "generate_to_directory passed package, registry and release validation",
        "generation": {key: _scrub(value) if isinstance(value, str) else value for key, value in generation.items()},
    })
    text = json.dumps(output, indent=2) + "\n"
    if PATH_IN_TEXT.search(text):
        raise SystemExit("build.json would contain a local path")
    out_path.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
