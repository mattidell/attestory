"""Static publication checks for blocked-question core v89."""

from __future__ import annotations

import copy
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"
CORE = "tax.us.2025.package.core-calculations"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _bytes(body: Any) -> bytes:
    return (json.dumps(body, indent=2) + "\n").encode("utf-8")


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    evidence_loader.load(EVIDENCE / "common.py", "common")
    evidence_loader.load(EVIDENCE / "probe.py", "probe")
    return evidence_loader.load(EVIDENCE / "prototype.py", "bnq_t1_v89_package_prototype")


def test_successors_are_the_prototype_on_rule_artifact_v17(prototype: ModuleType) -> None:
    for name, source in prototype.artifacts():
        body = copy.deepcopy(source)
        if body["schema"] != "input-question.v1":
            prototype.inject(body)
            body["schema"] = "rule-artifact.v17"
        assert (CONTENT / name).read_bytes() == _bytes(body), name


def test_core_v89_is_v88_with_exactly_the_decided_member_edits(prototype: ModuleType) -> None:
    before = _load(CONTENT / "package.core-calculations.v88.json")
    after = _load(CONTENT / "package.core-calculations.v89.json")
    assert (after["id"], after["version"], after["schema"]) == (CORE, "v89", "artifact-package.v43")
    assert set(after["admitted_schemas"]) == set(before["admitted_schemas"]) | {"rule-artifact.v17"}
    skip = ("version", "schema", "admitted_schemas", "members", "entrypoints", "package_checksum")
    assert {key: value for key, value in after.items() if key not in skip} == {
        key: value for key, value in before.items() if key not in skip}

    members = {row["id"]: row for row in before["members"]}
    entrypoints = {(row["id"], row["version"]) for row in before["entrypoints"]}
    changed: set[str] = set()
    for name, _source in prototype.artifacts():
        body = _load(CONTENT / name)
        role = "input-question" if body["schema"] == "input-question.v1" else "computation"
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role}
        old = members.get(body["id"])
        was_entrypoint = old is None or (old["id"], old["version"]) in entrypoints
        if old is not None and was_entrypoint:
            entrypoints.discard((old["id"], old["version"]))
        members[body["id"]] = new
        if was_entrypoint:
            entrypoints.add((new["id"], new["version"]))
        changed.add(body["id"])
    assert {row["id"]: row for row in after["members"]} == members
    assert {(row["id"], row["version"]) for row in after["entrypoints"]} == entrypoints
    prior = {row["id"]: row for row in before["members"]}
    observed = {member for member, row in members.items() if row != prior.get(member)}
    assert observed == changed
    assert len(changed) == 13
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v87_is_add_only() -> None:
    before = _load(CONTENT / "published-packages.v86.json")
    after = _load(CONTENT / "published-packages.v87.json")
    for key in ("citizens", "packages"):
        old = {(row["id"], row["version"]): row for row in before[key]}
        new = {(row["id"], row["version"]): row for row in after[key]}
        assert all(new[identity] == row for identity, row in old.items())
    added_citizens = {
        (row["id"], row["version"]): row["checksum"] for row in after["citizens"]
        if (row["id"], row["version"]) not in {
            (old["id"], old["version"]) for old in before["citizens"]}
    }
    expected = {}
    evidence_loader.load(EVIDENCE / "common.py", "common")
    evidence_loader.load(EVIDENCE / "probe.py", "probe")
    prototype = evidence_loader.load(EVIDENCE / "prototype.py", "bnq_t1_v89_registry_prototype")
    for name, _source in prototype.artifacts():
        body = _load(CONTENT / name)
        expected[(body["id"], body["version"])] = citizen_checksum(body)
    assert added_citizens == expected
    added_packages = [row for row in after["packages"] if (row["id"], row["version"]) not in {
        (old["id"], old["version"]) for old in before["packages"]}]
    package = _load(CONTENT / "package.core-calculations.v89.json")
    assert added_packages == [{"checksum": package["package_checksum"], "id": CORE, "version": "v89"}]


def test_release_v87_and_loader_entries_carry_v88() -> None:
    release = _load(RELEASES / f"{RELEASE_STEM}.v87.json")
    previous = _load(RELEASES / f"{RELEASE_STEM}.v86.json")
    assert release["version"] == "v87"
    assert release["package_registry_sha256"] == hashlib.sha256(
        (CONTENT / "published-packages.v87.json").read_bytes()).hexdigest()
    assert {key: value for key, value in release.items()
            if key not in ("version", "package_registry_sha256")} == {
                key: value for key, value in previous.items()
                if key not in ("version", "package_registry_sha256")}

    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v89")] == declarations[(CORE, "v88")]
    assert covered_flag_refusal_map(CORE, "v89") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v89") == covered_flag_refusal_map(CORE, "v88")
    assert selection_collect_satisfied_by_family(CORE, "v89") is True
    assert selection_collect_satisfied_by_family(CORE, "v88") is True


def test_v88_and_earlier_registry_entries_are_unchanged() -> None:
    before = _load(CONTENT / "published-packages.v86.json")
    after = _load(CONTENT / "published-packages.v87.json")
    old_packages = {(row["id"], row["version"]): row for row in before["packages"]}
    new_packages = {(row["id"], row["version"]): row for row in after["packages"]}
    old_citizens = {(row["id"], row["version"]): row for row in before["citizens"]}
    new_citizens = {(row["id"], row["version"]): row for row in after["citizens"]}
    assert all(new_packages[key] == value for key, value in old_packages.items())
    assert all(new_citizens[key] == value for key, value in old_citizens.items())
    for version in ("v88", "v87", "v86", "v85", "v84", "v83"):
        package = _load(CONTENT / f"package.core-calculations.{version}.json")
        assert package["package_checksum"] == package_instance_checksum(package)
        assert old_packages[(CORE, version)]["checksum"] == package["package_checksum"]

