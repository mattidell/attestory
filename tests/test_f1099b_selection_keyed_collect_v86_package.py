"""Core v86 is the decided family-collect selection, published as successors only.

Static checks on the published package, registry, release and loader entries.
The coordinator runs live in tests/test_f1099b_selection_keyed_collect_v86.py.

The subtotal successor is rebuilt from the evidence prototype
(``prototype._subtotal_v2``) with schema rule-artifact.v16 and compared byte
for byte. The prototype is loaded under a name no other module uses, and no
attribute of it is assigned.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from packages.derivation.package_validation import citizen_checksum
from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    covered_flag_refusal_map,
    domain_package_companion_declarations,
)
from tests import evidence_loader

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence"
RECORDED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."
SUBTOTAL = P + "rule.f1099b-b4-withholding-subtotal"
SYMBOL = P + "rule.f1099b-b4-amount-symbol"
SUBTOTAL_FILE = "rule.f1099b-b4-withholding-subtotal.v2.json"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    module = evidence_loader.load(EVIDENCE / "prototype.py", "skc_t1_v86_package_prototype")
    assert module.FROM == {"package": "v85", "registry": "v83", "release": "v83"}
    assert module.TO == {"package": "v86", "registry": "v84", "release": "v84"}
    return module


def test_subtotal_v2_is_the_prototype_on_rule_artifact_v16(prototype: ModuleType) -> None:
    body = prototype._subtotal_v2()
    body["schema"] = "rule-artifact.v16"
    assert (CONTENT / SUBTOTAL_FILE).read_bytes() == (json.dumps(body, indent=2) + "\n").encode("utf-8")


def test_core_v86_is_v85_with_exactly_the_prototype_member_edits() -> None:
    v85 = _load_json(CONTENT / "package.core-calculations.v85.json")
    v86 = _load_json(CONTENT / "package.core-calculations.v86.json")
    assert (v86["id"], v86["version"]) == (CORE, "v86")
    assert v85["schema"] == "artifact-package.v41"
    assert v86["schema"] == "artifact-package.v42"
    assert "rule-artifact.v16" not in v85["admitted_schemas"]
    assert set(v86["admitted_schemas"]) == set(v85["admitted_schemas"]) | {"rule-artifact.v16"}
    skip = ("version", "package_checksum", "members", "entrypoints", "schema", "admitted_schemas")
    assert {k: v for k, v in v86.items() if k not in skip} == {k: v for k, v in v85.items() if k not in skip}
    members = {m["id"]: m for m in v85["members"]}
    entrypoints = {(e["id"], e["version"]) for e in v85["entrypoints"]}
    old = members[SUBTOTAL]
    assert old["version"] == "v1"
    if (old["id"], old["version"]) in entrypoints:
        entrypoints.remove((old["id"], old["version"]))
        entrypoints.add((SUBTOTAL, "v2"))
    members[SUBTOTAL] = {"id": SUBTOTAL, "version": "v2", "schema": "rule-artifact.v16", "role": "computation"}
    removed = members.pop(SYMBOL)
    if (removed["id"], removed["version"]) in entrypoints:
        entrypoints.remove((removed["id"], removed["version"]))
    assert sorted(v86["members"], key=lambda m: m["id"]) == sorted(members.values(), key=lambda m: m["id"])
    assert {(e["id"], e["version"]) for e in v86["entrypoints"]} == entrypoints
    assert len(v86["members"]) == 998
    assert len(v85["members"]) == 999
    assert SYMBOL not in {m["id"] for m in v86["members"]}
    assert members[SUBTOTAL]["schema"] == "rule-artifact.v16"


def test_registry_v84_only_adds_v86_and_the_subtotal_successor() -> None:
    v83 = _load_json(CONTENT / "published-packages.v83.json")
    v84 = _load_json(CONTENT / "published-packages.v84.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v83[key]}
        after = {(e["id"], e["version"]): e for e in v84[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    packages = {(e["id"], e["version"]) for e in v84["packages"]} - {(e["id"], e["version"]) for e in v83["packages"]}
    assert packages == {(CORE, "v86")}
    assert (CORE, "v85") in {(e["id"], e["version"]) for e in v83["packages"]}
    added = {(e["id"], e["version"]): e["checksum"] for e in v84["citizens"]}
    for identity in {(e["id"], e["version"]) for e in v83["citizens"]}:
        del added[identity]
    body = _load_json(CONTENT / SUBTOTAL_FILE)
    assert added == {(SUBTOTAL, "v2"): citizen_checksum(body)}


def test_release_v84_pins_registry_v84() -> None:
    release = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v84.json")
    previous = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v83.json")
    assert release["version"] == "v84"
    registry = (CONTENT / "published-packages.v84.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()
    assert {k: v for k, v in release.items() if k not in ("version", "package_registry_sha256")} == {
        k: v for k, v in previous.items() if k not in ("version", "package_registry_sha256")}


def test_core_v86_carries_v85_loader_entries() -> None:
    declarations = domain_package_companion_declarations()
    v85, v86 = declarations[(CORE, "v85")], declarations[(CORE, "v86")]
    assert v86["presence_pairs"] == v85["presence_pairs"]
    assert v86["value_domains"] == v85["value_domains"]
    assert covered_flag_refusal_map(CORE, "v86") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v86") == covered_flag_refusal_map(CORE, "v85")


def test_core_v85_and_earlier_keep_the_stand_in() -> None:
    for version in ("v85", "v84", "v83"):
        package = _load_json(CONTENT / f"package.core-calculations.{version}.json")
        members = {m["id"]: m for m in package["members"]}
        assert members[SYMBOL]["version"] == "v1"
        assert members[SUBTOTAL]["version"] == "v1"
        assert members[SUBTOTAL]["schema"] == "rule-artifact.v15"


def test_the_recorded_v83_fixture_holds_298_runs() -> None:
    """The live module compares published v86 to this file in place. It is not copied."""
    table = _load_json(RECORDED)
    assert len(table["track0"]) == 79
    assert len(table["returns"]) == 213
    assert len(table["zero_sample"]) == 6
    assert len(table["track0"]) + len(table["returns"]) + len(table["zero_sample"]) == 298
