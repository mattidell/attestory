"""Build scratch v96 from published v95 and the explicit wording manifest.

Run: python3 p0b_build.py <new-directory-outside-repository>
Every predecessor byte is recoverable by undoing the declared prose and
root-version replacements. No production content or published bytes change.
"""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools.package_successor import generate_to_directory, SuccessorError


def property_at(body, path, value=None, *, put=False):
    keys = path.split(".")
    for key in keys[:-1]: body = body[key]
    if put: body[keys[-1]] = value
    return body[keys[-1]]


def literal_replace(raw, old, new):
    for ascii_only in (False, True):
        before, after = json.dumps(old, ensure_ascii=ascii_only), json.dumps(new, ensure_ascii=ascii_only)
        if before in raw:
            assert raw.count(before) == 1, "ambiguous prose literal"
            return raw.replace(before, after, 1), before, after
    raise AssertionError("declared prose literal not in predecessor bytes")


def main():
    scratch = Path(sys.argv[1]).resolve()
    assert scratch != REPO and REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content = scratch / "content"; rel = scratch / "releases"
    shutil.copytree(source, content); shutil.copytree(releases, rel)
    manifest = json.loads((HERE / "p0b-wording.json").read_text())
    package = json.loads((source / "package.core-calculations.v95.json").read_text())
    pins = {m["id"]: m for m in package["members"]}
    existing = {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text())
        if re.fullmatch(r"v\d+", str(body.get("version"))):
            existing.setdefault(body.get("id"), set()).add(int(body["version"][1:]))
    grouped = {}
    for row in manifest["replacements"]: grouped.setdefault(row["file"], []).append(row)
    members, entries, successors = [], [], []
    for filename, replacements in sorted(grouped.items()):
        old_path = REPO / filename
        raw = old_raw = old_path.read_text()
        old = json.loads(raw)
        new_version = "v" + str(max(existing[old["id"]]) + 1)
        normalized = copy.deepcopy(old)
        undo = []
        for row in replacements:
            assert property_at(old, row["property"]) == row["old"]
            property_at(normalized, row["property"], row["new"], put=True)
            raw, before, after = literal_replace(raw, row["old"], row["new"])
            undo.append((after, before))
        # Root-version line only; nested schema/citation/fact versions stay exact.
        pattern = re.compile(r'(?m)^(  "version": ")' + re.escape(old["version"]) + r'("[,]?)$')
        raw, count = pattern.subn(lambda m: m[1] + new_version + m[2], raw)
        assert count == 1
        normalized["version"] = new_version
        assert json.loads(raw) == normalized
        recovered = raw
        recovered, count = re.subn(r'(?m)^(  "version": ")' + re.escape(new_version) + r'("[,]?)$',
                                  lambda m: m[1] + old["version"] + m[2], recovered)
        assert count == 1
        for after, before in reversed(undo): recovered = recovered.replace(after, before, 1)
        assert recovered == old_raw, "non-prose predecessor bytes changed"
        next_name = re.sub(r"(?:\.v\d+)?\.json$", "." + new_version + ".json", old_path.name)
        assert not (content / next_name).exists()
        (content / next_name).write_text(raw)
        old_pin = pins[old["id"]]
        assert old_pin["version"] == old["version"]
        new_pin = {**old_pin, "version": new_version}
        members.append({"op": "replace", "old": old_pin, "new": new_pin})
        if any(e == {"id": old["id"], "version": old["version"]} for e in package["entrypoints"]):
            entries.append({"op": "replace", "old": {"id": old["id"], "version": old["version"]},
                            "new": {"id": old["id"], "version": new_version}})
        successors.append({"id": old["id"], "old_version": old["version"], "new_version": new_version,
            "predecessor": filename, "successor_filename": next_name,
            "changed_properties": [r["property"] for r in replacements],
            "predecessor_sha256": hashlib.sha256(old_path.read_bytes()).hexdigest(),
            "successor_sha256": hashlib.sha256(raw.encode()).hexdigest(), "byte_undo_proof": True})
    assert len(successors) == manifest["citizens"] == 50
    changes = {"package_version": "v96", "release_version": "v94", "members": members,
               "entrypoints": entries, "registry_sort": "id_version"}
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    stem = "demo.release.sli-worksheet-integration.2025"
    try:
        report = generate_to_directory(content / "package.core-calculations.v95.json",
            content / "published-packages.v93.json", rel / (stem + ".v93.json"),
            content, scratch / "changes.json", scratch / "generated")
    except SuccessorError as exc:
        output = {"status": "stopped", "source": "published v95", "proposed_core": "v96",
            "citizens_prepared": len(successors), "replaced_properties": len(manifest["replacements"]),
            "member_replacements": len(members), "entrypoint_replacements": len(entries),
            "byte_undo_proofs": len(successors), "successors": successors,
            "failure": str(exc), "valid_successor": False,
            "gate": "packages/derivation/package_validation.py:2884; inherited v68 successor graph requires line-2b@v6",
            "replay": "not run: charter requires stop for an engine change"}
        (HERE / "p0b-build.json").write_text(json.dumps(output, indent=2) + "\n")
        raise SystemExit(str(exc)) from None
    for src, dst in (("package.json", content / "package.core-calculations.v96.json"),
                     ("registry.json", content / "published-packages.v94.json"),
                     ("release.json", rel / (stem + ".v94.json"))):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({"version": "v96", "registry": "v94", "release_version": "v94",
        "content": str(content), "releases": str(rel), "loader_from": "v95"}, indent=2) + "\n")
    output = {"from": {"core": "v95", "registry": "v93", "release": "v93"},
        "to": {"core": "v96", "registry": "v94", "release": "v94"}, "citizens": len(successors),
        "replaced_properties": len(manifest["replacements"]), "member_replacements": len(members),
        "entrypoint_replacements": len(entries), "new_files": len(successors) + 3,
        "validation": "generate_to_directory passed package, registry and release integrity validation",
        "unchanged_bytes": "Undo only declared prose and the root citizen version recovers each exact predecessor; values, requires, pins, guards, missing names, question identities, codes and every other byte are preserved.",
        "successors": successors}
    (HERE / "p0b-build.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "successors"}, indent=2))


if __name__ == "__main__": main()
