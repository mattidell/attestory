"""Scratch core v103 from published v102: Step 3 question 3 and the separated-spouse successor.

Run: python3 build.py <new-directory-outside-repository>

Copies published content and releases outside the repository, writes the
vocabulary bundle, the input question, the recorded-path rule, the answer
rule, and rule.eic-answer.separated-spouse v3 (design.py), and validates the
package, registry and release with tools/package_successor.generate_to_directory.
Nothing in packages/ is edited. Writes build-p0b.json beside this file.
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


def _design():
    spec = importlib.util.spec_from_file_location("esm_p0b_design", HERE / "design.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pinned(node, targets, found):
    if isinstance(node, dict):
        if (node.get("id"), node.get("version")) in targets:
            found.append((node["id"], node["version"]))
        for value in node.values():
            pinned(value, targets, found)
    elif isinstance(node, list):
        for value in node:
            pinned(value, targets, found)


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
    v2 = json.loads((source / "rule.eic-answer.separated-spouse.v2.json").read_text(encoding="utf-8"))
    bodies = d.written(v2)
    shutil.copytree(source, content)
    shutil.copytree(releases, rel)
    package = json.loads((source / "package.core-calculations.v102.json").read_text(encoding="utf-8"))
    files = {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = body
    found: list = []
    for member in package["members"]:
        if (member["id"], member["version"]) == (d.RULE_SEPARATED, "v2"):
            continue
        body = files.get((member["id"], member["version"]))
        if body is None:
            continue
        pinned({k: v for k, v in body.items() if k != "id"}, {(d.RULE_SEPARATED, "v2")}, found)
    assert not found, found
    for name, body in bodies.items():
        assert not (content / name).exists(), name
        (content / name).write_text(d.dump(body), encoding="utf-8")
    rule_pin = next(m for m in package["members"] if m["id"] == d.RULE_SEPARATED and m["version"] == "v2")
    new_rules = [
        {"id": d.RULE_RECORDED, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"},
        {"id": d.RULE_ANSWER, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"},
    ]
    new_vocab = [
        {"id": d.BUNDLE_ID, "version": "v1", "schema": "bundle.v2", "role": "fact-type-bundle"},
        {"id": d.question()["id"], "version": "v1", "schema": "input-question.v1", "role": "input-question"},
    ]
    changes = {
        "package_version": "v103",
        "release_version": "v101",
        "members": [
            {"op": "replace", "old": rule_pin, "new": {**rule_pin, "version": "v3"}},
            *[{"op": "add", "new": pin} for pin in new_rules + new_vocab],
        ],
        "entrypoints": [{"op": "add", "value": {"id": pin["id"], "version": pin["version"]}} for pin in new_vocab],
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    sizes = {name: (content / name).stat().st_size for name in bodies if name.startswith("rule.")}
    output = {
        "from": {"core": "v102", "registry": "v100", "release": "v100"},
        "to": {"core": "v103", "registry": "v101", "release": "v101"},
        "sizes": sizes,
        "cap": 5000,
        "over_cap": [name for name, size in sizes.items() if size > 5000],
        "written_sha256": {name: hashlib.sha256(d.dump(body).encode()).hexdigest() for name, body in bodies.items()},
        "replaced_rule_pinned_by": found,
    }
    out_path = HERE / "build-p0b.json"
    try:
        report = generate_to_directory(
            content / "package.core-calculations.v102.json",
            content / "published-packages.v100.json",
            rel / (STEM + ".v100.json"),
            content, scratch / "changes.json", scratch / "generated",
        )
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:2000]})
        out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
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
    output.update({
        "status": "valid",
        "validation": "generate_to_directory passed package, registry and release validation",
        "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))},
    })
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in output.items() if k != "written_sha256"}, indent=2))


if __name__ == "__main__":
    main()
