"""Core v91 publishes the eight-name preferential base as the successor of v90.

Static checks: byte identity with the prototype, the one member replacement,
registry v89 add-only, release v89, and the loader entries. v90 and earlier
stay as they were. Line 16 v9 is parked, so the published package changes
one member. The coordinate runs live in
tests/test_preferential_base_reason_v91.py.

The prototype is loaded under a name no other module uses, and no attribute
of it is assigned.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any, cast

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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/preferential-base-reason-evidence"
CORE = "tax.us.2025.package.core-calculations"
PREFERENTIAL = "tax.us.2025.rule.selected-preferential-base"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
EARLIER = ("v90", "v89", "v88", "v87", "v86", "v85", "v84")


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _bytes(body: Any) -> bytes:
    return (json.dumps(body, indent=2) + "\n").encode("utf-8")


def _kept(body: dict[str, Any]) -> dict[str, Any]:
    skip = ("version", "members", "entrypoints", "package_checksum")
    return {key: value for key, value in body.items() if key not in skip}


def prototype() -> ModuleType:
    return evidence_loader.load(EVIDENCE / "prototype.py", "pbr_t1_v91_package_prototype")


def test_citizen_matches_the_prototype() -> None:
    written = cast(list[tuple[str, dict[str, Any]]], prototype().artifacts())
    assert len(written) == 1
    name, source = written[0]
    assert name == "rule.selected-preferential-base.v11.json"
    assert (CONTENT / name).read_bytes() == _bytes(source)


def test_core_v91_replaces_exactly_one_member() -> None:
    before = _load(CONTENT / "package.core-calculations.v90.json")
    after = _load(CONTENT / "package.core-calculations.v91.json")
    assert (after["id"], after["version"], after["schema"]) == (CORE, "v91", before["schema"])
    assert _kept(after) == _kept(before)

    old_members = {row["id"]: row for row in cast(list[dict[str, Any]], before["members"])}
    new_members = {row["id"]: row for row in cast(list[dict[str, Any]], after["members"])}
    assert set(old_members) == set(new_members)
    changed = [member_id for member_id, row in new_members.items() if old_members[member_id] != row]
    assert changed == [PREFERENTIAL]
    assert old_members[PREFERENTIAL]["version"] == "v10"
    assert new_members[PREFERENTIAL] == {
        "id": PREFERENTIAL,
        "version": "v11",
        "schema": "rule-artifact.v17",
        "role": "computation",
    }

    old_entrypoints = {(row["id"], row["version"]) for row in cast(list[dict[str, Any]], before["entrypoints"])}
    new_entrypoints = {(row["id"], row["version"]) for row in cast(list[dict[str, Any]], after["entrypoints"])}
    assert old_entrypoints - new_entrypoints == {(PREFERENTIAL, "v10")}
    assert new_entrypoints - old_entrypoints == {(PREFERENTIAL, "v11")}
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v89_is_add_only() -> None:
    before = _load(CONTENT / "published-packages.v88.json")
    after = _load(CONTENT / "published-packages.v89.json")
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
    body = _load(CONTENT / "rule.selected-preferential-base.v11.json")
    assert added_citizens == {(PREFERENTIAL, "v11"): citizen_checksum(body)}
    added_packages = [
        row for row in cast(list[dict[str, Any]], after["packages"])
        if (row["id"], row["version"]) not in {
            (old["id"], old["version"]) for old in cast(list[dict[str, Any]], before["packages"])
        }
    ]
    package = _load(CONTENT / "package.core-calculations.v91.json")
    assert added_packages == [{"checksum": package["package_checksum"], "id": CORE, "version": "v91"}]


def test_release_v89_and_loader_entries_carry_v90() -> None:
    release = _load(RELEASES / f"{RELEASE_STEM}.v89.json")
    previous = _load(RELEASES / f"{RELEASE_STEM}.v88.json")
    assert release["version"] == "v89"
    assert release["package_registry_sha256"] == hashlib.sha256(
        (CONTENT / "published-packages.v89.json").read_bytes()
    ).hexdigest()
    assert {key: value for key, value in release.items() if key not in ("version", "package_registry_sha256")} == {
        key: value for key, value in previous.items() if key not in ("version", "package_registry_sha256")
    }

    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v91")] == declarations[(CORE, "v90")]
    assert covered_flag_refusal_map(CORE, "v91") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v91") == covered_flag_refusal_map(CORE, "v90")
    assert selection_collect_satisfied_by_family(CORE, "v91") is True
    assert selection_collect_satisfied_by_family(CORE, "v90") is True


def test_v90_and_earlier_are_unchanged() -> None:
    before = _load(CONTENT / "published-packages.v88.json")
    after = _load(CONTENT / "published-packages.v89.json")
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
