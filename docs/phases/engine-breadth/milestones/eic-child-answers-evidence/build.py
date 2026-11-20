"""Scratch core v101 from published v100: the content routes P0 tries (design.py).

Run: python3 build.py <new-directory-outside-repository> --variant q|g

Copies the published content and releases outside the repository, writes the
variant's new files (design.py) and validates the package, registry and
release with tools/package_successor.generate_to_directory. ``q`` only adds
input questions (each also an entrypoint, as v100's questions are). ``g`` also
replaces the two roster count rules; the build checks that no other v100
member pins either by {"id", "version"}, so the replacement cascades to
nothing. Nothing in packages/ is edited. Writes build-<variant>.json beside
this file and core.json into the scratch directory (loader entries carried
from v100).
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
FROM = {"core": "v100", "registry": "v98", "release": "v98"}
TO = {"core": "v101", "registry": "v99", "release": "v99"}


def _design():
    spec = importlib.util.spec_from_file_location("eicc_p0_design", HERE / "design.py")
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
    parser.add_argument("--variant", choices=("q", "g"), required=True)
    args = parser.parse_args()
    d = _design()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    written = d.written(source, args.variant)
    skip = shutil.ignore_patterns(*sorted({*written, f"package.core-calculations.{TO['core']}.json",
                                           f"published-packages.{TO['registry']}.json",
                                           f"{STEM}.{TO['release']}.json"}))
    shutil.copytree(source, content, ignore=skip)
    shutil.copytree(releases, rel, ignore=skip)
    package = json.loads((source / f"package.core-calculations.{FROM['core']}.json").read_text())
    member_keys = {(m["id"], m["version"]) for m in package["members"]}
    files = {}
    for path in source.glob("*.json"):
        try:
            body = json.loads(path.read_text())
        except ValueError:
            continue
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = body
    asked = {files[(m["id"], m["version"])]["fact_type"]["id"] for m in package["members"] if m["role"] == "input-question"}
    for bundle in set(d.FACTS.values()):
        assert (bundle, "v1") in member_keys, bundle
    replaced = {rule_id: "v1" for rule_id in d.COUNT_FILES} if args.variant == "g" else {}
    for rule_id, version in replaced.items():
        assert (rule_id, version) in member_keys, rule_id
    found: list = []
    for member in package["members"]:
        if member["id"] not in replaced:
            body = files[(member["id"], member["version"])]
            pinned({k: v for k, v in body.items() if k != "id"}, set(replaced.items()), found)
    assert not found, found
    members: list = []
    added = []
    for name, body in written.items():
        assert not (content / name).exists(), name
        (content / name).write_text(d.dump(body))
        if body["schema"] == "input-question.v1":
            assert body["fact_type"]["id"] not in asked, f"already asked on {FROM['core']}: {name}"
            assert not any(k[0] == body["id"] for k in member_keys), name
            added.append({"id": body["id"], "version": "v1", "schema": "input-question.v1", "role": "input-question"})
        else:
            old = next(m for m in package["members"] if m["id"] == body["id"])
            members.append({"op": "replace", "old": old, "new": {**old, "version": body["version"], "schema": body["schema"]}})
    members += [{"op": "add", "new": pin} for pin in added]
    changes = {
        "package_version": TO["core"], "release_version": TO["release"],
        "members": members,
        "entrypoints": [{"op": "add", "value": {"id": pin["id"], "version": pin["version"]}} for pin in added],
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    output = {"variant": args.variant, "from": FROM, "to": TO, "changes": changes,
              "written": {name: hashlib.sha256(d.dump(body).encode()).hexdigest() for name, body in written.items()},
              "replaced_rules_pinned_by": found}
    out_path = HERE / f"build-{args.variant}.json"
    try:
        report = generate_to_directory(content / f"package.core-calculations.{FROM['core']}.json",
                                       content / f"published-packages.{FROM['registry']}.json",
                                       rel / f"{STEM}.{FROM['release']}.json",
                                       content, scratch / "changes.json", scratch / "generated")
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:2000]})
        out_path.write_text(json.dumps(output, indent=2) + "\n")
        raise SystemExit(output["failure"])
    for src, dst in (("package.json", content / f"package.core-calculations.{TO['core']}.json"),
                     ("registry.json", content / f"published-packages.{TO['registry']}.json"),
                     ("release.json", rel / f"{STEM}.{TO['release']}.json")):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({"version": TO["core"], "registry": TO["registry"],
                                                   "release_version": TO["release"], "content": str(content),
                                                   "releases": str(rel), "loader_from": FROM["core"]}, indent=2) + "\n")
    output.update({"status": "valid", "validation": "generate_to_directory passed package, registry and release validation",
                   "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))}
                   if isinstance(report, dict) else str(report)})
    text = json.dumps(output, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", text), "local path in build json"
    out_path.write_text(text)
    print(json.dumps({k: v for k, v in output.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
