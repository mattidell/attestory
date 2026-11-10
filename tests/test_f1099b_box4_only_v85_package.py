"""Core v85 is the decided Form 1099-B no-sale box 4 design, published as successors only.

Static checks on the published package, registry, release and loader entries,
and on the sale-fact audit: line 25b v8 still reads the per-statement box 4
amount. The coordinator runs live in tests/test_f1099b_box4_only_v85.py.

The successor bodies are rebuilt from the evidence prototype
(``prototype.artifacts``) and compared byte for byte. The audit is the
evidence ``tables.py``. Both are loaded under names no other module uses, and
no attribute of either is assigned.
"""

from __future__ import annotations

import hashlib
import importlib.util
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

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence"
TABLES = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence"
RECORDED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."
PRESENT = P + "f1099b.no-sale-box4-present"
AMOUNT = P + "f1099b.no-sale-box4-withholding"
LINE25B = P + "rule.form1040-line25b"
FIELD = P + "form1040.line-25b"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _module(name: str, path: Path) -> ModuleType:
    """An evidence module under its own name, loaded fresh and never registered or modified."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    module = _module("f1099b_box4_only_v85_package_prototype", EVIDENCE / "prototype.py")
    assert module.FROM == {"package": "v84", "registry": "v82", "release": "v82"}
    assert module.TO == {"package": "v85", "registry": "v83", "release": "v83"}
    return module


@pytest.fixture(scope="module")
def bodies(prototype: ModuleType) -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = prototype.artifacts()
    assert len(found) == 5
    return found


@pytest.fixture(scope="module")
def tables() -> ModuleType:
    return _module("f1099b_box4_only_v85_package_tables", TABLES / "tables.py")


def test_every_successor_is_the_prototype_byte_for_byte(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    for name, body in bodies:
        assert (CONTENT / name).read_bytes() == (json.dumps(body, indent=2) + "\n").encode("utf-8"), name


def test_core_v85_is_v84_with_exactly_the_prototype_member_edits(
        prototype: ModuleType, bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v84 = _load_json(CONTENT / "package.core-calculations.v84.json")
    v85 = _load_json(CONTENT / "package.core-calculations.v85.json")
    assert (v85["id"], v85["version"]) == (CORE, "v85")
    assert {k: v for k, v in v85.items() if k not in ("version", "package_checksum", "members", "entrypoints")} == {
        k: v for k, v in v84.items() if k not in ("version", "package_checksum", "members", "entrypoints")}
    members = {m["id"]: m for m in v84["members"]}
    entrypoints = {(e["id"], e["version"]) for e in v84["entrypoints"]}
    adds = replaces = 0
    for _name, body in bodies:
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"],
               "role": prototype.role_for(body["schema"])}
        old = members.get(body["id"])
        if old is None:
            adds += 1
            entrypoints.add((body["id"], body["version"]))
        else:
            replaces += 1
            assert old["version"] != body["version"]
            if (old["id"], old["version"]) in entrypoints:
                entrypoints.remove((old["id"], old["version"]))
                entrypoints.add((body["id"], body["version"]))
        members[body["id"]] = new
    assert (adds, replaces) == (3, 2)
    assert sorted(v85["members"], key=lambda m: m["id"]) == sorted(members.values(), key=lambda m: m["id"])
    assert {(e["id"], e["version"]) for e in v85["entrypoints"]} == entrypoints
    assert members[LINE25B]["version"] == "v8"
    assert members[FIELD]["version"] == "v6"
    v84_members = {m["id"]: m["version"] for m in v84["members"]}
    assert v84_members[LINE25B] == "v7"
    assert v84_members[FIELD] == "v5"
    assert P + "f1099b.no-sale-box4" not in v84_members


def test_registry_v83_only_adds_v85_and_its_new_citizens(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v82 = _load_json(CONTENT / "published-packages.v82.json")
    v83 = _load_json(CONTENT / "published-packages.v83.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v82[key]}
        after = {(e["id"], e["version"]): e for e in v83[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    packages = {(e["id"], e["version"]) for e in v83["packages"]} - {(e["id"], e["version"]) for e in v82["packages"]}
    assert packages == {(CORE, "v85")}
    assert (CORE, "v84") in {(e["id"], e["version"]) for e in v82["packages"]}
    added = {(e["id"], e["version"]): e["checksum"] for e in v83["citizens"]}
    for identity in {(e["id"], e["version"]) for e in v82["citizens"]}:
        del added[identity]
    assert added == {(body["id"], body["version"]): citizen_checksum(body) for _name, body in bodies}


def test_release_v83_pins_registry_v83() -> None:
    release = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v83.json")
    previous = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v82.json")
    assert release["version"] == "v83"
    registry = (CONTENT / "published-packages.v83.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()
    assert {k: v for k, v in release.items() if k not in ("version", "package_registry_sha256")} == {
        k: v for k, v in previous.items() if k not in ("version", "package_registry_sha256")}


def test_core_v85_carries_v84_loader_entries_and_no_new_pair() -> None:
    """The no-sale facts are return-keyed. They take no presence pair of their own."""
    declarations = domain_package_companion_declarations()
    v84, v85 = declarations[(CORE, "v84")], declarations[(CORE, "v85")]
    assert v85["presence_pairs"] == v84["presence_pairs"]
    assert v85["value_domains"] == v84["value_domains"]
    assert PRESENT not in v85["presence_pairs"]
    assert AMOUNT not in v85["presence_pairs"]
    assert covered_flag_refusal_map(CORE, "v85") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v85") == covered_flag_refusal_map(CORE, "v84")


def test_core_v84_and_earlier_stay_on_line_25b_v7() -> None:
    v84 = _load_json(CONTENT / "package.core-calculations.v84.json")
    members = {m["id"]: m["version"] for m in v84["members"]}
    assert members[LINE25B] == "v7"
    assert members[FIELD] == "v5"
    v83 = _load_json(CONTENT / "package.core-calculations.v83.json")
    earlier = {m["id"]: m["version"] for m in v83["members"]}
    assert earlier[LINE25B] == "v7"
    assert earlier[FIELD] == "v5"


def test_line_25b_v8_still_reads_the_box4_amount(tables: ModuleType) -> None:
    members = tables.members(CONTENT, "v85")
    assert tables.line25b_reads_amount(members) is True
    line25b = next(body for body in members if body.get("id") == LINE25B)
    assert line25b["version"] == "v8"
    reads = tables.value_side_reads(line25b)
    assert P + "f1099b.b4-withholding-subtotal" in reads
    assert AMOUNT in reads
    assert PRESENT in reads
    assert tables.audit(members, tables.field_table(members)) == []
    assert tables.row_audit(tables.row_table(members, tables.loader_pairs("v85"))) == []
    assert tables.consumer_audit(members) == []
    v84 = tables.members(CONTENT, "v84")
    assert tables.line25b_reads_amount(v84) is True
    earlier = tables.members(CONTENT, "v82")
    assert tables.line25b_reads_amount(earlier) is False
    assert tables.audit(v84, tables.field_table(v84)) == []


def test_the_committed_v85_tables_are_the_published_v85s(tables: ModuleType) -> None:
    members = tables.members(CONTENT, "v85")
    committed = _load_json(TABLES / "tables-v85.json")
    assert committed["package"] == "core-calculations v85"
    assert committed["fields"] == tables.field_table(members)
    assert committed["rows"] == tables.row_table(members, tables.loader_pairs("v85"))
    assert committed["consumers"] == tables.consumer_table(members)
    assert committed["audit_failures"] == []
    text = (TABLES / "tables-v85.json").read_text(encoding="utf-8")
    assert "/Users/" not in text and "/private/" not in text and "/tmp/" not in text and "/var/" not in text


def test_the_recorded_v83_fixture_holds_298_runs() -> None:
    """The live module compares published v85 to this file in place. It is not copied."""
    table = _load_json(RECORDED)
    assert len(table["track0"]) == 79
    assert len(table["returns"]) == 213
    assert len(table["zero_sample"]) == 6
    assert len(table["track0"]) + len(table["returns"]) + len(table["zero_sample"]) == 298
