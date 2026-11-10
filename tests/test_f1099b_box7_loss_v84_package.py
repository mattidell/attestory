"""Core v84 is the decided Form 1099-B box 7 design, published as successors only.

Static checks on the published package, registry, release and loader entries,
and on the sale-fact audit: the box 7 answer is a value-side read of the eight
verdict rules and of nothing else. The coordinator runs live in
tests/test_f1099b_box7_loss_v84.py.

The successor bodies are rebuilt from the evidence prototype
(``prototype.artifacts`` with the smaller switch unset) and compared byte for
byte. The audit is the evidence ``tables.py``. Both are loaded under names no
other module uses, and no attribute of either is assigned.
"""

from __future__ import annotations

import copy
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-box7-loss-evidence"
TABLES = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence"
RECORDED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
VERDICTS = (
    "rule.f1099b.covered-st-txn.box7-verdict",
    "rule.f1099b.covered-lt-txn.box7-verdict",
    "rule.f1099b.covered-w-st-txn.box7-verdict",
    "rule.f1099b.covered-w-lt-txn.box7-verdict",
    "rule.f1099b.noncovered-st-txn.box7-verdict",
    "rule.f1099b.noncovered-lt-txn.box7-verdict",
    "rule.f1099b.code-b-st-txn.box7-verdict",
    "rule.f1099b.code-b-lt-txn.box7-verdict",
)


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
    module = _module("f1099b_box7_v84_package_prototype", EVIDENCE / "prototype.py")
    assert module._smaller() == ""
    assert module.FROM == {"package": "v83", "registry": "v81", "release": "v81"}
    assert module.TO == {"package": "v84", "registry": "v82", "release": "v82"}
    return module


@pytest.fixture(scope="module")
def bodies(prototype: ModuleType) -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = prototype.artifacts()
    assert len(found) == 19
    return found


@pytest.fixture(scope="module")
def tables() -> ModuleType:
    return _module("f1099b_box7_v84_package_tables", TABLES / "tables.py")


def test_every_successor_is_the_prototype_byte_for_byte(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    for name, body in bodies:
        assert (CONTENT / name).read_bytes() == (json.dumps(body, indent=2) + "\n").encode("utf-8"), name


def test_core_v84_is_v83_with_exactly_the_prototype_member_edits(
        prototype: ModuleType, bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v83 = _load_json(CONTENT / "package.core-calculations.v83.json")
    v84 = _load_json(CONTENT / "package.core-calculations.v84.json")
    assert (v84["id"], v84["version"]) == (CORE, "v84")
    assert {k: v for k, v in v84.items() if k not in ("version", "package_checksum", "members", "entrypoints")} == {
        k: v for k, v in v83.items() if k not in ("version", "package_checksum", "members", "entrypoints")}
    members = {m["id"]: m for m in v83["members"]}
    entrypoints = {(e["id"], e["version"]) for e in v83["entrypoints"]}
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
    assert (adds, replaces) == (17, 2)
    assert sorted(v84["members"], key=lambda m: m["id"]) == sorted(members.values(), key=lambda m: m["id"])
    assert {(e["id"], e["version"]) for e in v84["entrypoints"]} == entrypoints
    assert members[P + "rule.schedule-d-line16"]["version"] == "v4"
    assert members[P + "schedule-d.line-16"]["version"] == "v4"
    v83_members = {m["id"]: m["version"] for m in v83["members"]}
    assert v83_members[P + "rule.schedule-d-line16"] == "v3"
    assert v83_members[P + "schedule-d.line-16"] == "v3"
    assert all(rule_id not in v83_members for rule_id in (P + name for name in VERDICTS))


def test_registry_v82_only_adds_v84_and_its_new_citizens(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v81 = _load_json(CONTENT / "published-packages.v81.json")
    v82 = _load_json(CONTENT / "published-packages.v82.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v81[key]}
        after = {(e["id"], e["version"]): e for e in v82[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    packages = {(e["id"], e["version"]) for e in v82["packages"]} - {(e["id"], e["version"]) for e in v81["packages"]}
    assert packages == {(CORE, "v84")}
    assert (CORE, "v83") in {(e["id"], e["version"]) for e in v81["packages"]}
    added = {(e["id"], e["version"]): e["checksum"] for e in v82["citizens"]}
    for identity in {(e["id"], e["version"]) for e in v81["citizens"]}:
        del added[identity]
    assert added == {(body["id"], body["version"]): citizen_checksum(body) for _name, body in bodies}


def test_release_v82_pins_registry_v82() -> None:
    release = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v82.json")
    previous = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v81.json")
    assert release["version"] == "v82"
    registry = (CONTENT / "published-packages.v82.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()
    assert {k: v for k, v in release.items() if k not in ("version", "package_registry_sha256")} == {
        k: v for k, v in previous.items() if k not in ("version", "package_registry_sha256")}


def test_core_v84_carries_v83_loader_entries_and_no_box7_pair() -> None:
    """The box 7 answer stays statement-keyed. It takes no presence pair of its own."""
    declarations = domain_package_companion_declarations()
    v83, v84 = declarations[(CORE, "v83")], declarations[(CORE, "v84")]
    assert v84["presence_pairs"] == v83["presence_pairs"]
    assert v84["value_domains"] == v83["value_domains"]
    assert BOX7 not in v84["presence_pairs"]
    assert covered_flag_refusal_map(CORE, "v84") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v84") == covered_flag_refusal_map(CORE, "v83")


def test_box7_is_read_only_on_the_verdict_value_side(tables: ModuleType) -> None:
    members = tables.members(CONTENT, "v84")
    assert [tables.short(item) for item in tables.box7_value_readers(members)] == list(VERDICTS)
    assert tables.BOX7_FACT in tables.read_by_rules(members)
    checks = [body for body in members if str(body["id"]).endswith(".box7-loss-check")]
    assert len(checks) == 8
    assert all(tables.BOX7_FACT not in tables.value_side_reads(body) for body in checks)
    line16 = next(body for body in members if str(body["id"]).endswith("rule.schedule-d-line16"))
    assert line16["version"] == "v4"
    assert tables.BOX7_FACT not in tables.value_side_reads(line16)
    assert tables.audit(members, tables.field_table(members)) == []
    assert tables.row_audit(tables.row_table(members, tables.loader_pairs("v84"))) == []
    assert tables.consumer_audit(members) == []
    earlier = tables.members(CONTENT, "v83")
    assert [tables.short(item) for item in tables.box7_value_readers(earlier)] == ["rule.schedule-d-line16"]
    assert tables.audit(earlier, tables.field_table(earlier)) == []


def _replace_box7_ref(node: Any) -> int:
    """Replace one box 7 value-side ref with a category literal. Requires are left alone."""
    if isinstance(node, dict):
        if node.get("op") == "ref" and node.get("name") == BOX7:
            node.clear()
            node.update({
                "op": "category_literal",
                "fact_type": {"id": BOX7, "version": "v1"},
                "value": "yes",
            })
            return 1
        return sum(_replace_box7_ref(value) for value in node.values())
    if isinstance(node, list):
        return sum(_replace_box7_ref(value) for value in node)
    return 0


def test_one_blind_verdict_fails_the_sale_fact_audit(tables: ModuleType) -> None:
    """One family that drops its value-side read of box 7 fails the audit by name."""
    members = copy.deepcopy(tables.members(CONTENT, "v84"))
    target = P + VERDICTS[0]
    (rule,) = [body for body in members if body.get("id") == target]
    assert _replace_box7_ref(rule["value"]) == 1
    assert tables.BOX7_FACT not in tables.value_side_reads(rule)
    assert BOX7 in rule["requires"]
    failures = tables.audit(members, tables.field_table(members))
    assert failures == [
        "box 7 loss not allowed: rule.f1099b.covered-st-txn.box7-verdict does not read "
        "the answer f1099b.statement-box7-loss-not-allowed"
    ]
    assert [tables.short(item) for item in tables.box7_value_readers(members)] == list(VERDICTS[1:])


def test_the_committed_v84_tables_are_the_published_v84s(tables: ModuleType) -> None:
    members = tables.members(CONTENT, "v84")
    committed = _load_json(TABLES / "tables-v84.json")
    assert committed["package"] == "core-calculations v84"
    assert committed["fields"] == tables.field_table(members)
    assert committed["rows"] == tables.row_table(members, tables.loader_pairs("v84"))
    assert committed["consumers"] == tables.consumer_table(members)
    assert committed["audit_failures"] == []
    text = (TABLES / "tables-v84.json").read_text(encoding="utf-8")
    assert "/Users/" not in text and "/private/" not in text and "/tmp/" not in text and "/var/" not in text


def test_the_recorded_v83_fixture_holds_298_runs() -> None:
    """The live module compares published v84 to this file in place. It is not copied."""
    table = _load_json(RECORDED)
    assert len(table["track0"]) == 79
    assert len(table["returns"]) == 213
    assert len(table["zero_sample"]) == 6
    assert len(table["track0"]) + len(table["returns"]) + len(table["zero_sample"]) == 298
