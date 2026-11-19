"""Scratch core v100 from published v99: an input question for each earned income credit answer that has none.

Run: python3 build.py <new-directory-outside-repository>

Copies the published content and releases outside the repository, writes the
four input questions (design.py) and validates the package, registry and
release with tools/package_successor.generate_to_directory. Only members are
added (four input questions, each also an entrypoint, as v99's questions
are); no member is replaced, so nothing cascades. Nothing in packages/ is
edited. Writes build.json beside this file and core.json into the scratch
directory (loader entries carried from v99).
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
FROM = {"core": "v99", "registry": "v97", "release": "v97"}
TO = {"core": "v100", "registry": "v98", "release": "v98"}


def _design():
    spec = importlib.util.spec_from_file_location("eicq_p0_design", HERE / "design.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    written = d.written()
    skip = shutil.ignore_patterns(*sorted({*written, f"package.core-calculations.{TO['core']}.json",
                                           f"published-packages.{TO['registry']}.json",
                                           f"{STEM}.{TO['release']}.json"}))
    shutil.copytree(source, content, ignore=skip)
    shutil.copytree(releases, rel, ignore=skip)
    package = json.loads((source / f"package.core-calculations.{FROM['core']}.json").read_text())
    members = {(m["id"], m["version"]) for m in package["members"]}
    bundle = json.loads((source / "eic-questions.bundle.json").read_text())
    assert (bundle["id"], bundle["version"]) == (d.BUNDLE["id"], d.BUNDLE["version"]) and (bundle["id"], bundle["version"]) in members
    declared = {ft["id"] for ft in bundle["fact_types"]}
    asked = set()
    for member in package["members"]:
        if member["role"] == "input-question":
            path = next(p for p in source.glob("input-question.*.json")
                        if json.loads(p.read_text()).get("id") == member["id"]
                        and json.loads(p.read_text()).get("version") == member["version"])
            asked.add(json.loads(path.read_text())["fact_type"]["id"])
    for name, body in written.items():
        assert body["fact_type"]["id"] in declared, name
        assert body["fact_type"]["id"] not in asked, f"already asked on {FROM['core']}: {name}"
        assert not any(m[0] == body["id"] for m in members), name
        assert not (content / name).exists(), name
        (content / name).write_text(d.dump(body))
    added = [{"id": body["id"], "version": "v1", "schema": "input-question.v1", "role": "input-question"}
             for body in written.values()]
    changes = {
        "package_version": TO["core"], "release_version": TO["release"],
        "members": [{"op": "add", "new": pin} for pin in added],
        "entrypoints": [{"op": "add", "value": {"id": pin["id"], "version": pin["version"]}} for pin in added],
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    output = {"from": FROM, "to": TO, "changes": changes,
              "written": {name: hashlib.sha256(d.dump(body).encode()).hexdigest() for name, body in written.items()},
              "replaced_members": []}
    out_path = HERE / "build.json"
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
    assert not re.search(r"/(?:Users|private|tmp|var)/", text), "local path in build.json"
    out_path.write_text(text)
    print(json.dumps({k: v for k, v in output.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
