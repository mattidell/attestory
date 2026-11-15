"""Core v90 publishes line 12d's boxes as successors of v89.

Static checks: byte identity with the prototype, the seventeen member
additions, registry v88 add-only, release v88, and the loader entries.
v89 and earlier stay as they were. The coordinate runs live in
tests/test_line12d_boxes_v90.py.

The prototype is loaded under a name no other module uses, and no attribute
of it is assigned.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    selection_collect_satisfied_by_family,
)
from tests import evidence_loader


REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/line12d-boxes-evidence"
CORE = "tax.us.2025.package.core-calculations"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
EARLIER = ("v89", "v88", "v87", "v86", "v85", "v84", "v83")


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _bytes(body: Any) -> bytes:
    return (json.dumps(body, indent=2) + "\n").encode("utf-8")


def _kept(body: dict[str, Any]) -> dict[str, Any]:
    skip = ("version", "members", "entrypoints", "package_checksum")
    return {key: value for key, value in body.items() if key not in skip}


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    return evidence_loader.load(EVIDENCE / "prototype.py", "l12d_t1_v90_package_prototype")


def test_citizens_match_the_prototype(prototype: ModuleType) -> None:
    written = cast(list[tuple[str, dict[str, Any]]], prototype.artifacts())
    assert len(written) == 17
    for name, source in written:
        assert (CONTENT / name).read_bytes() == _bytes(source), name


def test_core_v90_adds_exactly_those_members(prototype: ModuleType) -> None:
    before = _load(CONTENT / "package.core-calculations.v89.json")
    after = _load(CONTENT / "package.core-calculations.v90.json")
    assert (after["id"], after["version"], after["schema"]) == (CORE, "v90", before["schema"])
    assert _kept(after) == _kept(before)

    members = {row["id"]: row for row in cast(list[dict[str, Any]], before["members"])}
    entrypoints = {(row["id"], row["version"]) for row in cast(list[dict[str, Any]], before["entrypoints"])}
    added: set[str] = set()
    rule_ids: set[str] = set()
    for name, _source in cast(list[tuple[str, dict[str, Any]]], prototype.artifacts()):
        body = _load(CONTENT / name)
        new = {
            "id": body["id"],
            "version": body["version"],
            "schema": body["schema"],
            "role": prototype.role_for(body["schema"]),
        }
        assert body["id"] not in members
        members[body["id"]] = new
        if body["schema"] == "rule-artifact.v3":
            entrypoints.add((new["id"], new["version"]))
            rule_ids.add(str(body["id"]))
        added.add(str(body["id"]))
    assert {row["id"]: row for row in cast(list[dict[str, Any]], after["members"])} == members
    assert {(row["id"], row["version"]) for row in cast(list[dict[str, Any]], after["entrypoints"])} == entrypoints
    prior_ids = {row["id"] for row in cast(list[dict[str, Any]], before["members"])}
    prior_entrypoints = {(row["id"], row["version"]) for row in cast(list[dict[str, Any]], before["entrypoints"])}
    assert added - prior_ids == added
    assert {row[0] for row in entrypoints - prior_entrypoints} == rule_ids
    assert len(added) == 17
    assert len(rule_ids) == 8
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v88_is_add_only(prototype: ModuleType) -> None:
    before = _load(CONTENT / "published-packages.v87.json")
    after = _load(CONTENT / "published-packages.v88.json")
    for key in ("citizens", "packages"):
        old = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], before[key])}
        new = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], after[key])}
        assert all(new[identity] == row for identity, row in old.items())
    added_citizens = {
        (row["id"], row["version"]): row["checksum"]
        for row in cast(list[dict[str, Any]], after["citizens"])
        if (row["id"], row["version"]) not in {
            (old["id"], old["version"]) for old in cast(list[dict[str, Any]], before["citizens"])
        }
    }
    expected: dict[tuple[str, str], str] = {}
    for name, _source in cast(list[tuple[str, dict[str, Any]]], prototype.artifacts()):
        body = _load(CONTENT / name)
        expected[(str(body["id"]), str(body["version"]))] = citizen_checksum(body)
    assert added_citizens == expected
    added_packages = [
        row for row in cast(list[dict[str, Any]], after["packages"])
        if (row["id"], row["version"]) not in {
            (old["id"], old["version"]) for old in cast(list[dict[str, Any]], before["packages"])
        }
    ]
    package = _load(CONTENT / "package.core-calculations.v90.json")
    assert added_packages == [{"checksum": package["package_checksum"], "id": CORE, "version": "v90"}]


def test_release_v88_and_loader_entries_carry_v89() -> None:
    release = _load(RELEASES / f"{RELEASE_STEM}.v88.json")
    previous = _load(RELEASES / f"{RELEASE_STEM}.v87.json")
    assert release["version"] == "v88"
    assert release["package_registry_sha256"] == hashlib.sha256(
        (CONTENT / "published-packages.v88.json").read_bytes()
    ).hexdigest()
    assert {key: value for key, value in release.items() if key not in ("version", "package_registry_sha256")} == {
        key: value for key, value in previous.items() if key not in ("version", "package_registry_sha256")
    }

    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v90")] == declarations[(CORE, "v89")]
    assert covered_flag_refusal_map(CORE, "v90") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v90") == covered_flag_refusal_map(CORE, "v89")
    assert selection_collect_satisfied_by_family(CORE, "v90") is True
    assert selection_collect_satisfied_by_family(CORE, "v89") is True


def test_v89_and_earlier_are_unchanged() -> None:
    before = _load(CONTENT / "published-packages.v87.json")
    after = _load(CONTENT / "published-packages.v88.json")
    old_packages = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], before["packages"])}
    new_packages = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], after["packages"])}
    old_citizens = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], before["citizens"])}
    new_citizens = {(row["id"], row["version"]): row for row in cast(list[dict[str, Any]], after["citizens"])}
    assert all(new_packages[key] == value for key, value in old_packages.items())
    assert all(new_citizens[key] == value for key, value in old_citizens.items())
    for version in EARLIER:
        package = _load(CONTENT / f"package.core-calculations.{version}.json")
        assert package["package_checksum"] == package_instance_checksum(package)
        assert old_packages[(CORE, version)]["checksum"] == package["package_checksum"]
        assert new_packages[(CORE, version)]["checksum"] == package["package_checksum"]
