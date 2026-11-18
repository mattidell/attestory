"""Adopt P0b's 50 prepared citizens, refine prose, validate Decision 5.

Run: python3 p0c_validate.py <prepared-p0b-directory> <new-p0c-directory>
All runtime content and controls stay outside the repository.
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

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return module

runtime = load("plt_p0c_validation_runtime", HERE / "p0c_runtime.py")
prior = load("plt_p0c_byte_helpers", HERE / "p0b_build.py")
from tools.package_successor import generate_to_directory, load_corpus
from packages.derivation.package_validation import (validate_package, package_instance_checksum,
    load_published_citizen_checksums)
from packages.derivation.loader import DerivationSchemas


def main():
    prepared, scratch = (Path(p).resolve() for p in sys.argv[1:])
    assert REPO not in prepared.parents and REPO not in scratch.parents and not scratch.exists()
    recorded = json.loads((HERE / "p0b-build.json").read_text())
    old_manifest = json.loads((HERE / "p0b-wording.json").read_text())["replacements"]
    manifest = json.loads((HERE / "p0c-wording.json").read_text())["replacements"]
    assert len(manifest) == len(old_manifest) == 57
    for row in recorded["successors"]:
        assert hashlib.sha256((prepared / "content" / row["successor_filename"]).read_bytes()).hexdigest() == row["successor_sha256"]
    shutil.copytree(prepared, scratch)
    content, releases = scratch / "content", scratch / "releases"
    rows = []
    for row in recorded["successors"]:
        path = content / row["successor_filename"]
        raw = path.read_text()
        for before, after in zip(old_manifest, manifest):
            assert (before["id"], before["property"], before["old"]) == (after["id"], after["property"], after["old"])
            if before["id"] == row["id"] and before["new"] != after["new"]:
                raw, _, _ = prior.literal_replace(raw, before["new"], after["new"])
        path.write_text(raw)
        recovered = raw
        for change in reversed([r for r in manifest if r["id"] == row["id"]]):
            assert prior.property_at(json.loads(raw), change["property"]) == change["new"]
            recovered, _, _ = prior.literal_replace(recovered, change["new"], change["old"])
        recovered, count = re.subn(r'(?m)^(  "version": ")' + re.escape(row["new_version"]) + r'("[,]?)$',
            lambda m: m[1] + row["old_version"] + m[2], recovered)
        assert count == 1 and recovered == (REPO / row["predecessor"]).read_text()
        rows.append({**row, "successor_sha256": hashlib.sha256(raw.encode()).hexdigest(), "byte_undo_proof": True})
    schemas = DerivationSchemas()
    corpus, _ = load_corpus(content)
    v95 = json.loads((content / "package.core-calculations.v95.json").read_text())
    old_checks = load_published_citizen_checksums(content / "published-packages.v93.json")
    before = validate_package(v95, corpus, schemas, old_checks)
    assert before.ok, before.issues
    stem = "demo.release.sli-worksheet-integration.2025"
    with runtime.injected_graph() as injection:
        report = generate_to_directory(content / "package.core-calculations.v95.json",
            content / "published-packages.v93.json", releases / (stem + ".v93.json"),
            content, scratch / "changes.json", scratch / "generated")
        for source, dest in (("package.json", content / "package.core-calculations.v96.json"),
            ("registry.json", content / "published-packages.v94.json"),
            ("release.json", releases / (stem + ".v94.json"))):
            shutil.copyfile(scratch / "generated" / source, dest)
        checks = load_published_citizen_checksums(content / "published-packages.v94.json")
        v96 = json.loads((content / "package.core-calculations.v96.json").read_text())
        valid = validate_package(v96, corpus, schemas, checks)
        assert valid.ok, valid.issues
        controls = {}
        for name, package, field_version, expected_ok in (
            ("v96_with_v6_rejected", v96, "v6", False),
            ("v95_with_v7_rejected", v95, "v7", False),
            ("v95_unchanged_under_injection", v95, "v6", True)):
            changed = copy.deepcopy(package)
            pin = next(p for p in changed["members"] if p["id"] == runtime.FIELD)
            pin["version"] = field_version
            changed["package_checksum"] = package_instance_checksum(changed)
            result = validate_package(changed, corpus, schemas, checks)
            codes = [i.code for i in result.issues]
            assert result.ok == expected_ok, (name, result.issues)
            if not expected_ok: assert codes == ["NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED"], (name, codes)
            controls[name] = {"passed": True, "ok": result.ok, "codes": codes}
    assert validate_package(v95, corpus, schemas, old_checks).ok
    (scratch / "core.json").write_text(json.dumps({"version": "v96", "registry": "v94", "release_version": "v94",
        "content": str(content), "releases": str(releases), "loader_from": "v95"}, indent=2) + "\n")
    output = {"status": "pass", "source": "published core v95 / registry v93 / release v93",
        "scratch": "core v96 / registry v94 / release v94", "injection": injection,
        "controls": controls, "v95_before_and_after_injection": "valid",
        "citizens": len(rows), "replacements": len(manifest), "byte_undo_proofs": len(rows),
        "generation": report, "successors": rows}
    (HERE / "p0c-validation.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k:v for k,v in output.items() if k != "successors"}, indent=2))


if __name__ == "__main__": main()
