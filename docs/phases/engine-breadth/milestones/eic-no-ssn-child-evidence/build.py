"""Scratch core v102 from published v101: a qualifying child without a valid SSN still routes the credit.

Run: python3 build.py <new-directory-outside-repository>

Copies the published content and releases outside the repository, writes the
successors from design.py, and validates the package, registry and release
with tools/package_successor.generate_to_directory. Checks that no other v101
member pins a replaced rule by {"id", "version"}. Nothing in packages/ is edited.
Writes build.json beside this file. core.json in the scratch directory carries
local paths and is not committed.
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
FROM = {"core": "v101", "registry": "v99", "release": "v99"}
TO = {"core": "v102", "registry": "v100", "release": "v100"}


def _design():
    spec = importlib.util.spec_from_file_location("ens_p0_design", HERE / "design.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pinned(node, targets, found) -> None:
    if isinstance(node, dict):
        if (node.get("id"), node.get("version")) in targets:
            found.append((node["id"], node["version"]))
        for value in node.values():
            pinned(value, targets, found)
    elif isinstance(node, list):
        for value in node:
            pinned(value, targets, found)


def _scrub(text: str) -> str:
    return re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch")
    args = parser.parse_args()
    d = _design()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    written = d.written(source)
    skip = shutil.ignore_patterns(*sorted({
        *written,
        f"package.core-calculations.{TO['core']}.json",
        f"published-packages.{TO['registry']}.json",
        f"{STEM}.{TO['release']}.json",
    }))
    shutil.copytree(source, content, ignore=skip)
    shutil.copytree(releases, rel, ignore=skip)
    package = json.loads((source / f"package.core-calculations.{FROM['core']}.json").read_text())
    files = {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text())
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = body
    for rule_id, version in d.REPLACED.items():
        assert any(m["id"] == rule_id and m["version"] == version for m in package["members"]), rule_id
    found: list = []
    targets = set(d.REPLACED.items())
    for member in package["members"]:
        if member["id"] in d.REPLACED:
            continue
        body = files[(member["id"], member["version"])]
        pinned({k: v for k, v in body.items() if k != "id"}, targets, found)
    assert not found, found
    for name, body in written.items():
        assert not (content / name).exists(), name
        (content / name).write_text(d.dump(body))
    members = []
    for rule_id, new_file in (
        (d.CLASS_RULE, d.CLASS_FILE),
        (d.EARLY_RULE, d.EARLY_FILE),
        (d.QUESTIONS_RULE, d.QUESTIONS_FILE),
        (d.SEP_RULE, d.SEP_FILE),
        (d.NOT_MARRIED_RULE, d.NOT_MARRIED_FILE),
        (d.AGE_RULE, d.AGE_FILE),
        (d.HOME_RULE, d.HOME_FILE),
    ):
        old = next(m for m in package["members"] if m["id"] == rule_id)
        members.append({"op": "replace", "old": old, "new": {
            **old, "version": written[new_file]["version"], "schema": written[new_file]["schema"],
        }})
    added = [
        {"id": d.QUALIFIES_RULE, "version": "v1", "schema": written[d.QUALIFIES_FILE]["schema"], "role": "computation"},
        {"id": d.PRESENT_RULE, "version": "v1", "schema": written[d.PRESENT_FILE]["schema"], "role": "computation"},
    ]
    members += [{"op": "add", "new": pin} for pin in added]
    changes = {
        "package_version": TO["core"],
        "release_version": TO["release"],
        "members": members,
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    output = {
        "from": FROM, "to": TO, "changes": changes,
        "written": {name: hashlib.sha256(d.dump(body).encode()).hexdigest() for name, body in written.items()},
        "replaced_rules_pinned_by": found,
    }
    out_path = HERE / "build.json"
    try:
        report = generate_to_directory(
            content / f"package.core-calculations.{FROM['core']}.json",
            content / f"published-packages.{FROM['registry']}.json",
            rel / f"{STEM}.{FROM['release']}.json",
            content, scratch / "changes.json", scratch / "generated",
        )
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": _scrub(str(exc))[:2000]})
        text = json.dumps(output, indent=2) + "\n"
        assert not re.search(r"/(?:Users|private|tmp|var)/", text)
        out_path.write_text(text)
        raise SystemExit(output["failure"])
    for src, dst in (
        ("package.json", content / f"package.core-calculations.{TO['core']}.json"),
        ("registry.json", content / f"published-packages.{TO['registry']}.json"),
        ("release.json", rel / f"{STEM}.{TO['release']}.json"),
    ):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({
        "version": TO["core"], "registry": TO["registry"], "release_version": TO["release"],
        "content": str(content), "releases": str(rel), "loader_from": FROM["core"],
    }, indent=2) + "\n")
    generation = {}
    if isinstance(report, dict):
        for key, value in report.items():
            if isinstance(value, (str, int, bool)):
                generation[key] = value
            elif isinstance(value, dict):
                generation[key] = {k: v for k, v in value.items() if isinstance(v, (str, int, bool))}
            elif isinstance(value, list):
                generation[key + "_count"] = len(value)
    else:
        generation = {"report": _scrub(str(report))[:500]}
    output.update({
        "status": "valid",
        "validation": "generate_to_directory passed package, registry and release validation",
        "generation": generation,
    })
    text = json.dumps(output, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", text), "local path in build.json"
    out_path.write_text(text)
    print(json.dumps({k: v for k, v in output.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
