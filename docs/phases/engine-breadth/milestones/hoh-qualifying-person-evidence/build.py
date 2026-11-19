"""Scratch core v98 from published v97: head of household and qualifying surviving spouse ask their tests.

Run: python3 build.py <new-directory-outside-repository> [--variant q]

Copies the published content and releases outside the repository, writes the
new vocabulary bundle, the two input questions and the
rule.dependents-worksheet-line-3 v2 successor (design.py), and validates the
package, registry and release with tools/package_successor.generate_to_directory.
Nothing pins rule.dependents-worksheet-line-3 v1 by {"id", "version"}, so the
replacement cascades to nothing. Nothing in packages/ is edited. Writes
build-<variant>.json beside this file.
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
    spec = importlib.util.spec_from_file_location("hoh_p0_design", HERE / "design.py")
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
    parser.add_argument("--variant", choices=("q",), default="q")
    args = parser.parse_args()
    d = _design()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    # Rebuilding on a branch that already carries v98: start from v97 content only.
    skip = shutil.ignore_patterns(*sorted({d.BUNDLE_FILE, "package.core-calculations.v98.json",
                                           "published-packages.v96.json", STEM + ".v96.json",
                                           "rule.dependents-worksheet-line-3.v2.json",
                                           *d.questions()}))
    shutil.copytree(source, content, ignore=skip)
    shutil.copytree(releases, rel, ignore=skip)
    package = json.loads((source / "package.core-calculations.v97.json").read_text())
    # No other v97 member pins the rule being replaced.
    files = {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text())
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = body
    found: list = []
    for member in package["members"]:
        if member["id"] != d.RULE_ID:
            body = files[(member["id"], member["version"])]
            pinned({k: v for k, v in body.items() if k != "id"}, {(d.RULE_ID, "v1")}, found)
    assert not found, found
    v1_path = source / "rule.dependents-worksheet-line-3.json"
    v1 = json.loads(v1_path.read_text())
    written = {d.BUNDLE_FILE: d.bundle(), "rule.dependents-worksheet-line-3.v2.json": d.rule_successor(v1),
               **d.questions()}
    for name, body in written.items():
        assert not (content / name).exists(), name
        (content / name).write_text(d.dump(body))
    rule_pin = next(m for m in package["members"] if m["id"] == d.RULE_ID)
    new = [{"id": d.BUNDLE_ID, "version": "v1", "schema": "bundle.v2", "role": "fact-type-bundle"}]
    new += [{"id": q["id"], "version": "v1", "schema": "input-question.v1", "role": "input-question"}
            for q in d.questions().values()]
    changes = {
        "package_version": "v98", "release_version": "v96",
        "members": [{"op": "replace", "old": rule_pin, "new": {**rule_pin, "version": "v2", "schema": written["rule.dependents-worksheet-line-3.v2.json"]["schema"]}}]
        + [{"op": "add", "new": pin} for pin in new],
        "entrypoints": [{"op": "add", "value": {"id": pin["id"], "version": pin["version"]}} for pin in new],
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    output = {"variant": args.variant, "from": {"core": "v97", "registry": "v95", "release": "v95"},
              "to": {"core": "v98", "registry": "v96", "release": "v96"}, "changes": changes,
              "written": {name: hashlib.sha256(d.dump(body).encode()).hexdigest() for name, body in written.items()},
              "replaced_rule_pinned_by": found}
    out_path = HERE / f"build-{args.variant}.json"
    try:
        report = generate_to_directory(content / "package.core-calculations.v97.json",
                                       content / "published-packages.v95.json", rel / (STEM + ".v95.json"),
                                       content, scratch / "changes.json", scratch / "generated")
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:2000]})
        out_path.write_text(json.dumps(output, indent=2) + "\n")
        raise SystemExit(output["failure"])
    for src, dst in (("package.json", content / "package.core-calculations.v98.json"),
                     ("registry.json", content / "published-packages.v96.json"),
                     ("release.json", rel / (STEM + ".v96.json"))):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({"version": "v98", "registry": "v96", "release_version": "v96",
                                                   "content": str(content), "releases": str(rel), "loader_from": "v97"},
                                                  indent=2) + "\n")
    output.update({"status": "valid", "validation": "generate_to_directory passed package, registry and release validation",
                   "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))}
                   if isinstance(report, dict) else str(report)})
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
