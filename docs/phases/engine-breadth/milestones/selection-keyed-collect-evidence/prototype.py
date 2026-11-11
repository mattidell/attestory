"""Scratch core v86: retire the box 4 stand-in symbol and the inert path.

Evidence for docs/phases/engine-breadth/milestones/selection-keyed-collect.md.
Charter: docs/reviews/selection-keyed-collect/charter-p0.md.

Applies engine.patch to a copy of packages/ outside the repository, lowers
the v15 path minimum only in that copy so the one-path subtotal can be
measured, and builds core v86 there. Production must publish a new schema
version instead of editing v15.

    python3 prototype.py /path/outside/the/repo
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"package": "v85", "registry": "v83", "release": "v83"}
TO = {"package": "v86", "registry": "v84", "release": "v84"}
SUBTOTAL = P + "rule.f1099b-b4-withholding-subtotal"
SYMBOL = P + "rule.f1099b-b4-amount-symbol"
AMOUNT = P + "f1099b.statement-box4-withholding"
FAMILY = P + "f1099b.b4"
PUBLISHES = P + "f1099b.b4-withholding-subtotal"


def _subtotal_v2() -> dict[str, Any]:
    body = json.loads((CONTENT / "rule.f1099b-b4-withholding-subtotal.json").read_text(encoding="utf-8"))
    amounts = copy.deepcopy(body["selection"]["paths"][0])
    amounts["requires"] = []
    amounts["pins"] = []
    body["version"] = "v2"
    body["selection"]["paths"] = [amounts]
    body["notes"] = (
        "Every current Form 1099-B box 4 amount, or zero when none is recorded. "
        "The amounts path collects the family directly. The zero is the default "
        "of this selection, so a return with no amount is not asked to close the family."
    )
    return body


def _pin(package: dict[str, Any], identity: str) -> dict[str, Any]:
    found = [member for member in package["members"] if member["id"] == identity]
    if len(found) != 1:
        raise SystemExit(f"member {identity} count {len(found)}")
    return dict(found[0])


def _entrypoint(package: dict[str, Any], identity: str) -> dict[str, str]:
    found = [entry for entry in package["entrypoints"] if entry["id"] == identity]
    if len(found) != 1:
        raise SystemExit(f"entrypoint {identity} count {len(found)}")
    return {"id": found[0]["id"], "version": found[0]["version"]}


def lower_path_minimum(packages: Path) -> str:
    """Prototype-only: v15 minItems 1 in this copy, with a matching checksum."""
    schema = packages / "schemas/derivation/rule-artifact.v15.schema.json"
    text = schema.read_text(encoding="utf-8")
    if text.count('"minItems": 2') != 1:
        raise SystemExit("v15 path minItems is not a single 2")
    schema.write_text(text.replace('"minItems": 2', '"minItems": 1', 1), encoding="utf-8")
    digest = hashlib.sha256(schema.read_bytes()).hexdigest()
    manifest_path = packages / "schemas/derivation/published.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    key = "rule-artifact.v15.schema.json"
    if key not in manifest:
        raise SystemExit("v15 schema is not in the derivation manifest")
    manifest[key] = digest
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return digest[:12]


def change_list(package: dict[str, Any]) -> dict[str, Any]:
    old = _pin(package, SUBTOTAL)
    new = {
        "id": SUBTOTAL,
        "version": "v2",
        "schema": "rule-artifact.v15",
        "role": "computation",
    }
    return {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": [
            {"op": "replace", "old": old, "new": new},
            {"op": "remove", "old": _pin(package, SYMBOL)},
        ],
        "entrypoints": [
            {
                "op": "replace",
                "old": _entrypoint(package, SUBTOTAL),
                "new": {"id": SUBTOTAL, "version": "v2"},
            },
            {"op": "remove", "value": _entrypoint(package, SYMBOL)},
        ],
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }


def build(scratch: Path) -> dict[str, Any]:
    packages = scratch / "packages"
    content = scratch / "content"
    releases = scratch / "releases"
    shutil.copytree(REPO / "packages", packages)
    subprocess.run(
        ["patch", "-p1", "-d", str(scratch), "-i", str(HERE / "engine.patch")],
        check=True, capture_output=True, text=True,
    )
    schema_digest = lower_path_minimum(packages)
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    (content / "rule.f1099b-b4-withholding-subtotal.v2.json").write_text(
        json.dumps(_subtotal_v2(), indent=2) + "\n", encoding="utf-8",
    )
    package = json.loads((content / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
    changes = change_list(package)
    changes_path = scratch / "changes.json"
    changes_path.write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    if str(scratch) not in sys.path:
        sys.path.insert(0, str(scratch))
    from tools.package_successor import generate_to_directory  # noqa: E402
    report = generate_to_directory(
        content / f"package.core-calculations.{FROM['package']}.json",
        content / f"published-packages.{FROM['registry']}.json",
        releases / f"{RELEASE_STEM}.{FROM['release']}.json",
        content,
        changes_path,
        scratch / "out",
    )
    for src, folder, target in (
        ("package.json", content, f"package.core-calculations.{TO['package']}.json"),
        ("registry.json", content, f"published-packages.{TO['registry']}.json"),
        ("release.json", releases, f"{RELEASE_STEM}.{TO['release']}.json"),
    ):
        shutil.copy(scratch / "out" / src, folder / target)
    core = {
        "version": TO["package"],
        "registry": TO["registry"],
        "release_version": TO["release"],
        "content": str(content),
        "releases": str(releases),
        "loader_from": FROM["package"],
        "packages": str(packages),
    }
    (scratch / "core.json").write_text(json.dumps(core, indent=2) + "\n", encoding="utf-8")
    return {
        "from": FROM,
        "to": TO,
        "package": report["package"]["version"],
        "registry": TO["registry"],
        "release": report["release"]["version"],
        "removed": SYMBOL.removeprefix(P),
        "replaced": [SUBTOTAL.removeprefix(P), "v1", "v2"],
        "paths": ["amounts"],
        "prototype_schema_minItems": 1,
        "prototype_schema_digest_prefix": schema_digest,
        "inherited_inconsistencies": [list(row) for row in report.get("inherited_inconsistencies") or ()],
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    summary = build(scratch)
    text = json.dumps(summary, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"prototype summary contains {needle}")
    (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    print(json.dumps({
        "package": summary["package"],
        "removed": summary["removed"],
        "replaced": summary["replaced"],
        "output": "prototype-build.json",
    }, indent=2))


if __name__ == "__main__":
    main()
