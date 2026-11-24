"""Publish core v102 from published v101, with the widened Step 4 skip.

Run: python3 track1_build.py <new-directory-outside-repository>

Copies published content outside the repository, writes the successors from
track1_design.py, and validates the package, registry and release. Nothing
under packages/ is edited. Writes track1-build.json beside this file. The
scratch core.json carries local paths and is not committed.
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
    spec = importlib.util.spec_from_file_location("ens_t1_design", HERE / "track1_design.py")
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
    design = _design()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    written = design.written(source)
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
    for rule_id, version in design.REPLACED.items():
        assert any(m["id"] == rule_id and m["version"] == version for m in package["members"]), rule_id
    found: list = []
    targets = set(design.REPLACED.items())
    for member in package["members"]:
        if member["id"] in design.REPLACED:
            continue
        body = files[(member["id"], member["version"])]
        pinned({k: v for k, v in body.items() if k != "id"}, targets, found)
    assert not found, found
    for name, body in written.items():
        assert not (content / name).exists(), name
        (content / name).write_text(design.dump(body))
    order = (
        (design.CLASS_RULE, design.CLASS_FILE),
        (design.EARLY_RULE, design.EARLY_FILE),
        (design.QUESTIONS_RULE, design.QUESTIONS_FILE),
        (design.SEP_RULE, design.SEP_FILE),
        (design.NOT_MARRIED_RULE, design.NOT_MARRIED_FILE),
        (design.AGE_RULE, design.AGE_FILE),
        (design.HOME_RULE, design.HOME_FILE),
        (design.NOT_CLAIMABLE_RULE, design.NOT_CLAIMABLE_FILE),
    )
    members = []
    for rule_id, new_file in order:
        old = next(m for m in package["members"] if m["id"] == rule_id)
        members.append({"op": "replace", "old": old, "new": {
            **old, "version": written[new_file]["version"], "schema": written[new_file]["schema"],
        }})
    added = [
        {"id": design.QUALIFIES_RULE, "version": "v1", "schema": written[design.QUALIFIES_FILE]["schema"], "role": "computation"},
        {"id": design.PRESENT_RULE, "version": "v1", "schema": written[design.PRESENT_FILE]["schema"], "role": "computation"},
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
        "written": {name: hashlib.sha256(design.dump(body).encode()).hexdigest() for name, body in written.items()},
        "replaced_rules_pinned_by": found,
    }
    out_path = HERE / "track1-build.json"
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
    assert not re.search(r"/(?:Users|private|tmp|var)/", text), "local path in track1-build.json"
    out_path.write_text(text)
    print(json.dumps({k: v for k, v in output.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
