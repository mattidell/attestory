"""Generate the Track 1 Schedule 1 absence-succession publication chain.

Produces the successor vocabulary bundle, the migration artifact, worksheet
v3 (nonempty CDS retargeted; empty-route contract unchanged), package
core-calculations v31, published-packages v26, release v24, and the
adopt-core-v31 fixture. Lowest free versions on the ratified line at
implementation time.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from packages.tax.schedule1_adjustments_succession import (
    MIGRATION_ID,
    MIGRATION_VERSION,
    PAIRS,
    PREDECESSOR_IDS,
    SUCCESSOR_BUNDLE_ID,
    SUCCESSOR_BUNDLE_VERSION,
    SUCCESSOR_IDS,
    SUCCESSOR_TITLES,
)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "ssa1099_benefits_line6"

YES_NO = {"type": "string", "enum": ["yes", "no"]}
IDENTITY = [{"kind": "literal", "name": "tax-year", "values": ["2025"]}]

SUCCESSOR_BUNDLE_FILE = "schedule1-adjustments-scope.bundle.json"
MIGRATION_FILE = "schedule1-adjustments-scope.succession.json"
WORKSHEET_FILE = "rule.ss-benefits-worksheet.v3.json"
PACKAGE_FILE = "package.core-calculations.v31.json"
REGISTRY_FILE = "published-packages.v26.json"
RELEASE_FILE = "demo.release.2025.v24.json"
ADOPTION_FILE = "adopt-core-v31-current.json"


def _bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load(name: str) -> dict[str, Any]:
    value = json.loads((CONTENT / name).read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _checksum(value: dict[str, Any]) -> str:
    body = {key: item for key, item in value.items() if key != "package_checksum"}
    return hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _citizen_checksum(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build_successor_bundle() -> dict[str, Any]:
    fact_types = []
    for successor_id, title in zip(SUCCESSOR_IDS, SUCCESSOR_TITLES, strict=True):
        fact_types.append(
            {
                "id": successor_id,
                "identity_keys": copy.deepcopy(IDENTITY),
                "nature": "determinable",
                "schema": "fact-type.v2",
                "supersession": {"policy": "free"},
                "title": title,
                "value_schema": copy.deepcopy(YES_NO),
                "version": "v1",
            }
        )
    return {
        "schema": "bundle.v2",
        "id": SUCCESSOR_BUNDLE_ID,
        "version": SUCCESSOR_BUNDLE_VERSION,
        "label": (
            "Schedule 1 Part II adjustment-absence vocabulary for tax year 2025. "
            "Thirteen Schedule-1-native {yes, no} declarations; not a successor "
            "version of ss-benefits-scope.vocabulary."
        ),
        "fact_types": fact_types,
    }


def build_migration() -> dict[str, Any]:
    return {
        "schema": "migration-artifact.v1",
        "id": MIGRATION_ID,
        "version": MIGRATION_VERSION,
        "title": (
            "Succeed the thirteen Schedule 1 Part II absence facts from the "
            "Social Security worksheet vocabulary onto Schedule-1-native ids. "
            "Adoption is a direct supersession root. Finding half is a "
            "presented successor claim."
        ),
        "finding_mapping": {"policy": "presented-claim"},
        "pairs": [
            {"predecessor": predecessor, "successor": successor}
            for predecessor, successor in PAIRS
        ],
    }


def build_worksheet() -> dict[str, Any]:
    rule = _load("rule.ss-benefits-worksheet.v2.json")
    mapping = dict(PAIRS)
    text = json.dumps(rule)
    for predecessor, successor in mapping.items():
        text = text.replace(predecessor, successor)
    rule = json.loads(text)
    assert isinstance(rule, dict)
    dumped = json.dumps(rule)
    for predecessor in PREDECESSOR_IDS:
        assert predecessor not in dumped, predecessor
    for successor in SUCCESSOR_IDS:
        assert successor in dumped, successor
    rule["version"] = "v3"
    rule["notes"] = (
        rule["notes"]
        + " Nonempty-route Schedule 1 Part II absences retargeted onto the "
        "schedule1-adjustments-scope successors. Empty-route contract is the "
        "Milestone 1 contract: eleven requires including "
        "no-rrb-or-foreign-social-benefit, require_closed, count, the no-rrb "
        "conjunct, and choose(count==0 → 0)."
    )
    return rule


def _member_pin(citizen: dict[str, Any], role: str) -> dict[str, Any]:
    return {
        "id": citizen["id"],
        "role": role,
        "schema": citizen["schema"],
        "version": citizen["version"],
    }


def build_package(citizens: dict[str, dict[str, Any]]) -> dict[str, Any]:
    package = _load("package.core-calculations.v30.json")
    package["schema"] = "artifact-package.v23"
    package["version"] = "v31"
    admitted = list(package["admitted_schemas"])
    if "migration-artifact.v1" not in admitted:
        admitted.append("migration-artifact.v1")
        admitted.sort()
    package["admitted_schemas"] = admitted
    members = [
        dict(member)
        for member in package["members"]
        if member["id"] != "tax.us.2025.rule.ss-benefits-worksheet"
    ]
    members.append(_member_pin(citizens[WORKSHEET_FILE], "computation"))
    members.append(_member_pin(citizens[SUCCESSOR_BUNDLE_FILE], "fact-type-bundle"))
    members.append(_member_pin(citizens[MIGRATION_FILE], "migration-artifact"))
    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))
    entrypoints = [
        dict(entry)
        for entry in package["entrypoints"]
        if entry["id"] != "tax.us.2025.rule.ss-benefits-worksheet"
    ]
    entrypoints.append({"id": "tax.us.2025.rule.ss-benefits-worksheet", "version": "v3"})
    entrypoints.append({"id": SUCCESSOR_BUNDLE_ID, "version": SUCCESSOR_BUNDLE_VERSION})
    entrypoints.append({"id": MIGRATION_ID, "version": MIGRATION_VERSION})
    package["entrypoints"] = [
        {"id": eid, "version": ver}
        for eid, ver in sorted({(e["id"], e["version"]) for e in entrypoints})
    ]
    package["package_checksum"] = _checksum(package)
    return package


def build_registry(package: dict[str, Any], citizens: dict[str, dict[str, Any]]) -> dict[str, Any]:
    registry = _load("published-packages.v25.json")
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for citizen in citizens.values():
        key = (citizen["id"], citizen["version"])
        citizen_entries = [e for e in citizen_entries if (e["id"], e["version"]) != key]
        citizen_entries.append(
            {
                "id": citizen["id"],
                "version": citizen["version"],
                "checksum": _citizen_checksum(citizen),
            }
        )
    registry["citizens"] = sorted(citizen_entries, key=lambda e: (e["id"], e["version"]))
    package_entries = [dict(entry) for entry in registry["packages"]]
    package_entries.append(
        {
            "id": package["id"],
            "version": package["version"],
            "checksum": package["package_checksum"],
        }
    )
    registry["packages"] = sorted(package_entries, key=lambda e: (e["id"], e["version"]))
    return registry


def build_release(registry_bytes: bytes) -> dict[str, Any]:
    return {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v24",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }


def build_adoption(
    package: dict[str, Any],
    registry: dict[str, Any],
    release: dict[str, Any],
    release_bytes: bytes,
) -> dict[str, Any]:
    package_entry = next(
        e
        for e in registry["packages"]
        if e["id"] == package["id"] and e["version"] == package["version"]
    )
    return {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v31",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-14T12:00:00Z",
        "committed_against": 0,
        "payload": {
            "package": {
                "id": package["id"],
                "version": package["version"],
                "checksum": package_entry["checksum"],
            },
            "release": {
                "id": release["id"],
                "version": release["version"],
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 31,
            "audit": {
                "note": "synthetic Schedule 1 absence succession adoption; non-authoritative"
            },
        },
    }


def render_all(
    content_dir: Path | None = None,
    fixtures_dir: Path | None = None,
) -> dict[Path, bytes]:
    content = CONTENT if content_dir is None else content_dir
    fixtures = FIXTURES if fixtures_dir is None else fixtures_dir
    citizens = {
        SUCCESSOR_BUNDLE_FILE: build_successor_bundle(),
        MIGRATION_FILE: build_migration(),
        WORKSHEET_FILE: build_worksheet(),
    }
    package = build_package(citizens)
    registry = build_registry(package, citizens)
    out: dict[Path, bytes] = {
        content / name: _bytes(citizen) for name, citizen in citizens.items()
    }
    out[content / PACKAGE_FILE] = _bytes(package)
    out[content / REGISTRY_FILE] = _bytes(registry)
    registry_bytes = out[content / REGISTRY_FILE]
    release = build_release(registry_bytes)
    release_bytes = _bytes(release)
    adoption = build_adoption(package, registry, release, release_bytes)
    out[fixtures / "publication_surface" / "releases" / RELEASE_FILE] = release_bytes
    out[fixtures / "adoptions" / ADOPTION_FILE] = _bytes(adoption)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-dir", type=Path, default=None)
    parser.add_argument("--fixtures-dir", type=Path, default=None)
    args = parser.parse_args()
    for path, body in render_all(args.content_dir, args.fixtures_dir).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
