"""Scratch core v99 from published v98: the earned income credit asks a head of household with no qualifying child whether they were married.

Run: python3 build.py <new-directory-outside-repository> [--variant m]

Copies the published content and releases outside the repository, writes the
new vocabulary bundle, input question and answer rule and the
rule.eic-status-class v2, rule.eic-gate-result v3 and the five Step 4 answer-rule v3 successors (design.py,
each built from the published v98 member it succeeds), and validates the
package, registry and release with tools/package_successor.generate_to_directory.
Checks that no other v98 member pins either replaced rule by {"id", "version"},
so the replacements cascade to nothing. Nothing in packages/ is edited.
Writes build-<variant>.json beside this file.
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
    spec = importlib.util.spec_from_file_location("hoh_eic_p0_design", HERE / "design.py")
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
    parser.add_argument("--variant", choices=("m",), default="m")
    args = parser.parse_args()
    d = _design()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    written = d.written(source)
    # Rebuilding on a branch that already carries v99: start from v98 content only.
    skip = shutil.ignore_patterns(*sorted({*written, "package.core-calculations.v99.json",
                                           "published-packages.v97.json", STEM + ".v97.json"}))
    shutil.copytree(source, content, ignore=skip)
    shutil.copytree(releases, rel, ignore=skip)
    package = json.loads((source / "package.core-calculations.v98.json").read_text())
    files = {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text())
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = body
    replaced = {d.CLASS_RULE: "v1", d.GATE_RULE: "v2", **{rule: "v2" for rule in d.STEP4_RULES}}
    for rule_id, version in replaced.items():
        assert any(m["id"] == rule_id and m["version"] == version for m in package["members"]), rule_id
    found: list = []
    for member in package["members"]:
        if member["id"] not in replaced:
            body = files[(member["id"], member["version"])]
            pinned({k: v for k, v in body.items() if k != "id"}, set(replaced.items()), found)
    assert not found, found
    for name, body in written.items():
        assert not (content / name).exists(), name
        (content / name).write_text(d.dump(body))
    members = []
    for rule_id, new_file in ((d.CLASS_RULE, d.CLASS_FILE), (d.GATE_RULE, d.GATE_FILE), *d.STEP4_RULES.items()):
        old = next(m for m in package["members"] if m["id"] == rule_id)
        members.append({"op": "replace", "old": old, "new": {**old, "version": written[new_file]["version"],
                                                             "schema": written[new_file]["schema"]}})
    added = [{"id": d.ANSWER_RULE, "version": "v1", "schema": written[d.ANSWER_RULE_FILE]["schema"], "role": "computation"},
             {"id": d.BUNDLE_ID, "version": "v1", "schema": "bundle.v2", "role": "fact-type-bundle"},
             {"id": d.QUESTION_ID, "version": "v1", "schema": "input-question.v1", "role": "input-question"},
             {"id": d.SEP_QUESTION_ID, "version": "v1", "schema": "input-question.v1", "role": "input-question"}]
    members += [{"op": "add", "new": pin} for pin in added]
    changes = {
        "package_version": "v99", "release_version": "v97",
        "members": members,
        "entrypoints": [{"op": "add", "value": {"id": pin["id"], "version": pin["version"]}} for pin in added[1:]],
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    output = {"variant": args.variant, "from": {"core": "v98", "registry": "v96", "release": "v96"},
              "to": {"core": "v99", "registry": "v97", "release": "v97"}, "changes": changes,
              "written": {name: hashlib.sha256(d.dump(body).encode()).hexdigest() for name, body in written.items()},
              "replaced_rules_pinned_by": found}
    out_path = HERE / f"build-{args.variant}.json"
    try:
        report = generate_to_directory(content / "package.core-calculations.v98.json",
                                       content / "published-packages.v96.json", rel / (STEM + ".v96.json"),
                                       content, scratch / "changes.json", scratch / "generated")
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:2000]})
        out_path.write_text(json.dumps(output, indent=2) + "\n")
        raise SystemExit(output["failure"])
    for src, dst in (("package.json", content / "package.core-calculations.v99.json"),
                     ("registry.json", content / "published-packages.v97.json"),
                     ("release.json", rel / (STEM + ".v97.json"))):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({"version": "v99", "registry": "v97", "release_version": "v97",
                                                   "content": str(content), "releases": str(rel), "loader_from": "v98"},
                                                  indent=2) + "\n")
    output.update({"status": "valid", "validation": "generate_to_directory passed package, registry and release validation",
                   "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))}
                   if isinstance(report, dict) else str(report)})
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
