"""Core v101 (registry v99, release v99) from published v100: the Track 1 member questions (track1_design.py).

Run: python3 track1_build.py <new-directory-outside-repository> [--publish]

Copies the published content and releases outside the repository, writes the
twenty-six input questions and validates the package, registry and release
with tools/package_successor.generate_to_directory. Only members are added
(each question also an entrypoint, as v100's questions are); no member is
replaced, so nothing cascades. Each question names a fact type declared by a
v100 bundle that no v100 question names. With ``--publish`` the new files are
copied into packages/ (new files only; the script refuses to overwrite).
Writes track1-build.json beside this file and core.json into the scratch
directory.
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
SOURCE = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"


def _design():
    spec = importlib.util.spec_from_file_location("eicc_t1_design", HERE / "track1_design.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _versioned(directory: Path) -> dict[tuple[str, str], dict]:
    files = {}
    for path in directory.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = body
    return files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    d = _design()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    content, rel = scratch / "content", scratch / "releases"
    written = d.written()
    outputs = {f"package.core-calculations.{TO['core']}.json", f"published-packages.{TO['registry']}.json",
               f"{STEM}.{TO['release']}.json"}
    skip = shutil.ignore_patterns(*sorted({*written, *outputs}))
    shutil.copytree(SOURCE, content, ignore=skip)
    shutil.copytree(RELEASES, rel, ignore=skip)
    package = json.loads((SOURCE / f"package.core-calculations.{FROM['core']}.json").read_text(encoding="utf-8"))
    members = {(m["id"], m["version"]) for m in package["members"]}
    files = _versioned(SOURCE)
    asked = {files[(m["id"], m["version"])]["fact_type"]["id"] for m in package["members"]
             if m["role"] == "input-question"}
    declared: dict[str, set[str]] = {}
    for bundle in set(d.BUNDLES.values()):
        assert (bundle, "v1") in members, bundle
        declared[bundle] = {ft["id"] for ft in files[(bundle, "v1")]["fact_types"]}
    for name, body in written.items():
        fact = body["fact_type"]["id"]
        assert fact in declared[d.BUNDLES[fact]], name
        assert fact not in asked, f"already asked on {FROM['core']}: {name}"
        assert not any(m[0] == body["id"] for m in members), name
        assert not (content / name).exists(), name
        (content / name).write_text(d.dump(body), encoding="utf-8")
    added = [{"id": body["id"], "version": "v1", "schema": "input-question.v1", "role": "input-question"}
             for body in written.values()]
    changes = {
        "package_version": TO["core"], "release_version": TO["release"],
        "members": [{"op": "add", "new": pin} for pin in added],
        "entrypoints": [{"op": "add", "value": {"id": pin["id"], "version": pin["version"]}} for pin in added],
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    output = {"from": FROM, "to": TO, "changes": changes,
              "written": {name: hashlib.sha256(d.dump(body).encode()).hexdigest() for name, body in written.items()},
              "replaced_members": []}
    out_path = HERE / "track1-build.json"
    try:
        report = generate_to_directory(content / f"package.core-calculations.{FROM['core']}.json",
                                       content / f"published-packages.{FROM['registry']}.json",
                                       rel / f"{STEM}.{FROM['release']}.json",
                                       content, scratch / "changes.json", scratch / "generated")
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:2000]})
        out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
        raise SystemExit(output["failure"])
    generated = {"package.json": content / f"package.core-calculations.{TO['core']}.json",
                 "registry.json": content / f"published-packages.{TO['registry']}.json",
                 "release.json": rel / f"{STEM}.{TO['release']}.json"}
    for src, dst in generated.items():
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({"version": TO["core"], "registry": TO["registry"],
                                                   "release_version": TO["release"], "content": str(content),
                                                   "releases": str(rel), "loader_from": FROM["core"]}, indent=2) + "\n",
                                       encoding="utf-8")
    output.update({"status": "valid", "validation": "generate_to_directory passed package, registry and release validation",
                   "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))}
                   if isinstance(report, dict) else str(report)})
    if args.publish:
        targets = [(content / name, SOURCE / name) for name in written]
        targets += [(generated["package.json"], SOURCE / generated["package.json"].name),
                    (generated["registry.json"], SOURCE / generated["registry.json"].name),
                    (generated["release.json"], RELEASES / generated["release.json"].name)]
        for _, dst in targets:
            assert not dst.exists(), f"refusing to overwrite {dst.name}"
        for src, dst in targets:
            shutil.copyfile(src, dst)
        output["published"] = sorted(dst.name for _, dst in targets)
    text = json.dumps(output, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", text), "local path in track1-build.json"
    out_path.write_text(text, encoding="utf-8")
    print(json.dumps({k: v for k, v in output.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
