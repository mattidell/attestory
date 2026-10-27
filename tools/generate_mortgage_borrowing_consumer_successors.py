"""Rebuild the reviewed mortgage package delta on the selected ratified base."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = "packages/content/tax/2025"
RELEASES = "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
BASE_PACKAGE_REL = f"{CONTENT}/package.core-calculations.v56.json"
BASE_REGISTRY_REL = f"{CONTENT}/published-packages.v54.json"
BASE_RELEASE_REL = f"{RELEASES}/demo.release.sli-worksheet-integration.2025.v54.json"
DELTA_REL = "tools/data/mortgage_borrowing_core55_delta.json"
PACKAGE_REL = f"{CONTENT}/package.core-calculations.v57.json"
REGISTRY_REL = f"{CONTENT}/published-packages.v55.json"
RELEASE_REL = f"{RELEASES}/demo.release.sli-worksheet-integration.2025.v55.json"
OUTPUT_RELS = (PACKAGE_REL, REGISTRY_REL, RELEASE_REL)
SUCCESSOR_IDS = {
    "tax.us.2025.rule.attachment.schedule-a": ("v1", "v2"),
    "tax.us.2025.rule.f1098-line8a": ("v2", "v5"),
    "tax.us.2025.rule.f1098-residence-interest-reason": ("v2", "v5"),
    "tax.us.2025.rule.form1040-line12e": ("v1", "v2"),
}
BASE_SHA256 = {
    BASE_PACKAGE_REL: "6e8a5ec5e47afaaf8c1319fa9ac63361b6cda1a7fdd78f4e8e84635c6d9737ba",
    BASE_REGISTRY_REL: "1de1df059988afd56fd72e731743380f33e730b85e2145bbb420e28c8d2e68e7",
    BASE_RELEASE_REL: "30fbccd842b07ac4747e08a1cc20bd270628704320db7141126d87ed03a6086b",
}


class GenerationGuardError(ValueError):
    """A frozen source, candidate identity, or publication guard failed."""


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _checksum(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _pinned_json(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise GenerationGuardError(f"cannot read pinned base artifact {relative}: {exc}") from exc
    if hashlib.sha256(raw).hexdigest() != BASE_SHA256[relative]:
        raise GenerationGuardError(f"pinned base bytes changed: {relative}")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise GenerationGuardError(f"expected object at pinned path {relative}")
    return value


def _identity(row: dict[str, Any]) -> tuple[str, str]:
    identifier, version = row.get("id"), row.get("version")
    if not isinstance(identifier, str) or not isinstance(version, str):
        raise GenerationGuardError("publication row lacks an id/version identity")
    return identifier, version


def _index(rows: list[dict[str, Any]], label: str) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = _identity(row)
        if key in result:
            raise GenerationGuardError(f"duplicate {label} identity: {key}")
        result[key] = row
    return result


def _members(package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = package.get("members")
    if not isinstance(rows, list):
        raise GenerationGuardError("package members are malformed")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise GenerationGuardError("package member is malformed")
        if row["id"] in result:
            raise GenerationGuardError(f"duplicate package member id: {row['id']}")
        result[row["id"]] = row
    return result


def _mortgage_delta(delta: dict[str, Any], base: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    added, new_entrypoints = delta.get("members"), delta.get("entrypoints")
    successors = delta.get("successors")
    anchors = delta.get("member_anchors")
    if (not isinstance(added, list) or not isinstance(new_entrypoints, list)
            or not isinstance(successors, list) or not isinstance(anchors, dict)):
        raise GenerationGuardError("durable mortgage delta is malformed")
    current = _members(base)
    if len(added) != 44 or len(_members({"members": added})) != 44:
        raise GenerationGuardError("frozen mortgage package delta is not the reviewed 44-addition/four-successor contract")
    if set(anchors) != {row["id"] for row in added} or not set(anchors.values()) <= set(current):
        raise GenerationGuardError("durable member placement anchors do not match the selected base")
    for identifier, (prior_version, successor_version) in SUCCESSOR_IDS.items():
        if current.get(identifier, {}).get("version") != prior_version:
            raise GenerationGuardError(f"selected base predecessor differs from frozen source: {identifier}")
    collisions = sorted(set(current) & {row["id"] for row in added})
    if collisions:
        raise GenerationGuardError(f"new mortgage member id collides with selected base: {collisions[0]}")
    if {_identity(row) for row in successors} != {
        (identifier, successor) for identifier, (_prior, successor) in SUCCESSOR_IDS.items()
    }:
        raise GenerationGuardError("durable successor selections differ from the reviewed four-version contract")
    return [*added, *successors], new_entrypoints


def _merge_package(base: dict[str, Any], delta: dict[str, Any]) -> dict[str, Any]:
    delta_members, new_entrypoints = _mortgage_delta(delta, base)
    successors = [row for row in delta_members if row["id"] in SUCCESSOR_IDS]
    added = [row for row in delta_members if row["id"] not in SUCCESSOR_IDS]
    result = dict(base)
    result["version"] = "v57"
    base_rows = list(base["members"])
    successor_by_id = {row["id"]: row for row in successors}
    rows = [successor_by_id.get(row["id"], row) for row in base_rows]
    # Keep the complete selected-base order. Add mortgage-only declarations in
    # their reviewed source order after the last shared source-base anchor.
    anchor_map = delta["member_anchors"]
    pending: dict[str, list[dict[str, Any]]] = {}
    for row in added:
        pending.setdefault(anchor_map[row["id"]], []).append(row)
    ordered: list[dict[str, Any]] = []
    for row in rows:
        ordered.append(row)
        ordered.extend(pending.pop(row["id"], []))
    if pending:
        raise GenerationGuardError("durable member placement references a missing base anchor")
    result["members"] = ordered
    added_ep = {_identity(row) for row in new_entrypoints}
    removed_ep = {(identifier, prior) for identifier, (prior, _) in SUCCESSOR_IDS.items()}
    expected_removed = {(identifier, prior) for identifier, (prior, _) in SUCCESSOR_IDS.items()}
    if removed_ep != expected_removed or len(added_ep) != 23:
        raise GenerationGuardError("frozen mortgage entrypoint delta differs from the reviewed selection")
    entrypoints = list(base["entrypoints"])
    for identity in removed_ep:
        if identity not in {_identity(row) for row in entrypoints}:
            raise GenerationGuardError(f"selected base lacks superseded entrypoint: {identity}")
    entrypoints = [row for row in entrypoints if _identity(row) not in removed_ep]
    entry_index = {_identity(row) for row in entrypoints}
    new_rows = new_entrypoints
    for row in new_rows:
        identity = _identity(row)
        if identity in entry_index:
            raise GenerationGuardError(f"mortgage entrypoint collides with selected base: {identity}")
        entry_index.add(identity)
    entrypoints.extend(new_rows)
    result["entrypoints"] = entrypoints
    result.pop("package_checksum", None)
    result["package_checksum"] = _checksum(result)
    return result


def _resolve_citizens(root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted((root / CONTENT).glob("*.json")):
        try:
            citizen = json.loads(path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GenerationGuardError(f"cannot read candidate citizen {path.name}: {exc}") from exc
        if isinstance(citizen, dict) and isinstance(citizen.get("id"), str) and isinstance(citizen.get("version"), str):
            key = (citizen["id"], citizen["version"])
            if key in result:
                raise GenerationGuardError(f"ambiguous candidate citizen identity: {key}")
            result[key] = citizen
    return result


def build(root: Path = ROOT) -> dict[str, bytes]:
    base = _pinned_json(root, BASE_PACKAGE_REL)
    registry = _pinned_json(root, BASE_REGISTRY_REL)
    release = _pinned_json(root, BASE_RELEASE_REL)
    delta = json.loads((root / DELTA_REL).read_text("utf-8"))
    if base.get("version") != "v56" or not isinstance(registry.get("citizens"), list):
        raise GenerationGuardError("selected ratified base package/registry changed shape")
    package = _merge_package(base, delta)
    citizens = registry.get("citizens")
    packages = registry.get("packages")
    if not isinstance(citizens, list) or not isinstance(packages, list):
        raise GenerationGuardError("selected base registry arrays are malformed")
    citizen_index = _index(citizens, "base citizen")
    package_index = _index(packages, "base package")
    local_citizens = _resolve_citizens(root)
    base_member_index = _index(base["members"], "selected-base member")
    for key, row in base_member_index.items():
        frozen = citizen_index.get(key)
        local = local_citizens.get(key)
        if frozen is None or local is None:
            raise GenerationGuardError(f"selected-base member lacks a frozen registry/citizen: {key}")
        if _checksum(local) != frozen.get("checksum"):
            raise GenerationGuardError(f"ratified citizen checksum changed: {key}")
    members = package["members"]
    additions = [row for row in members if (row["id"], row["version"]) not in base_member_index]
    for row in additions:
        key = _identity(row)
        citizen = local_citizens.get(key)
        if citizen is None:
            raise GenerationGuardError(f"missing exact citizen: {key}")
        if citizen.get("schema") != row.get("schema"):
            raise GenerationGuardError(f"citizen schema mismatch: {key}")
        if key in citizen_index:
            raise GenerationGuardError(f"candidate citizen identity already exists in selected base: {key}")
        citizen_index[key] = {"id": key[0], "version": key[1], "checksum": _checksum(citizen)}
    package_key = (package["id"], package["version"])
    if package_key in package_index:
        raise GenerationGuardError("new package identity already exists in selected base")
    package_index[package_key] = {"id": package_key[0], "version": package_key[1], "checksum": package["package_checksum"]}
    new_registry = dict(registry)
    new_registry["citizens"] = [*citizens, *sorted((row for key, row in citizen_index.items() if key not in _index(citizens, "base citizen")), key=_identity)]
    new_registry["packages"] = [*packages, package_index[package_key]]
    new_release = dict(release)
    new_release["version"] = "v55"
    new_release["package_registry_sha256"] = hashlib.sha256(_document(new_registry)).hexdigest()
    return {
        PACKAGE_REL: _document(package),
        REGISTRY_REL: _document(new_registry),
        RELEASE_REL: _document(new_release),
    }


def _write_outputs(root: Path, outputs: dict[str, bytes]) -> None:
    paths = {root / relative: content for relative, content in outputs.items()}
    collisions = [path.name for path in paths if path.exists()]
    if collisions:
        raise GenerationGuardError("refusing to overwrite candidate output: " + ", ".join(collisions))
    for path, content in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare existing candidate bytes with the pinned rebuild")
    args = parser.parse_args(argv)
    try:
        outputs = build()
        paths = {ROOT / relative: content for relative, content in outputs.items()}
        if args.check:
            stale = [path.name for path, content in paths.items() if not path.exists() or path.read_bytes() != content]
            if stale:
                print("stale candidate outputs: " + ", ".join(sorted(stale)))
                return 1
            print("pinned mortgage package/registry/release bytes are reproducible (3 files)")
            return 0
        _write_outputs(ROOT, outputs)
        print("generated additive mortgage package v57 / registry v55 / release v55")
        return 0
    except (GenerationGuardError, OSError, json.JSONDecodeError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
