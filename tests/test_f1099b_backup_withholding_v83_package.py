"""Core v83 is the decided Form 1099-B box 4 design, published as successors only.

Static checks on the published package, registry, release and loader entries,
on the words of the new box 4 question, and on the sale-fact audit: core v83
counts the box 4 amount as read and does not require the retired yes/no.
The coordinator runs live in tests/test_f1099b_backup_withholding_v83.py.

The successor bodies are rebuilt from the evidence prototype
(``prototype.artifacts`` with the decided switches only; the bridge repair is
not taken) and compared byte for byte. The audit is the evidence ``tables.py``.
Both are loaded under names no other module uses, and no attribute of either
is assigned.
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence"
TABLES = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence"
CORE = "tax.us.2025.package.core-calculations"
FIXTURE = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
CLASSES = {"box4_unanswered_asks_amount": 150, "identical": 63}
P = "tax.us.2025."
QUESTION = (
    "Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a "
    "sale from. If box 4 is blank, enter $0."
)
AMOUNT = P + "f1099b.statement-box4-withholding"
YES_NO = P + "f1099b.statement-box4-withholding-reported"
BOX4 = "box 4 federal income tax withheld"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _module(name: str, path: Path) -> ModuleType:
    """An evidence module under its own name, loaded fresh and never registered or modified."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _bodies_by_identity() -> dict[tuple[str, str], str]:
    found: dict[tuple[str, str], str] = {}
    for path in CONTENT.glob("*.json"):
        text = path.read_text(encoding="utf-8")
        try:
            body = json.loads(text)
        except ValueError:
            continue
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            found[(body["id"], body["version"])] = text
    return found


def _rule_texts(package_version: str) -> list[str]:
    package = _load_json(CONTENT / f"package.core-calculations.{package_version}.json")
    bodies = _bodies_by_identity()
    texts: list[str] = []
    for member in package["members"]:
        if member["role"] not in ("computation", "attachment-rule"):
            continue
        texts.append(bodies[(member["id"], member["version"])])
    return texts


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    module = _module("f1099b_b4_v83_package_prototype", EVIDENCE / "prototype.py")
    assert module.FIXES == ("box4_amount",)
    assert module.REPAIRS == ("bridge_v82_no",)
    assert module.SWITCHES == {"box4_amount"}
    assert module.FROM == {"package": "v82", "registry": "v80", "release": "v80"}
    assert module.TO == {"package": "v83", "registry": "v81", "release": "v81"}
    return module


@pytest.fixture(scope="module")
def bodies(prototype: ModuleType) -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = prototype.artifacts(set(prototype.SWITCHES))
    assert len(found) == 7
    return found


@pytest.fixture(scope="module")
def tables() -> ModuleType:
    return _module("f1099b_b4_v83_package_tables", TABLES / "tables.py")


# ---- the package, registry, release and loader ------------------------------------


def test_every_successor_is_the_prototype_byte_for_byte(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    for name, body in bodies:
        assert "bridge_v82_no" not in json.dumps(body)
        assert (CONTENT / name).read_bytes() == (json.dumps(body, indent=2) + "\n").encode("utf-8"), name


def test_core_v83_is_v82_with_exactly_the_prototype_member_edits(
        prototype: ModuleType, bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v82 = _load_json(CONTENT / "package.core-calculations.v82.json")
    v83 = _load_json(CONTENT / "package.core-calculations.v83.json")
    assert (v83["id"], v83["version"]) == (CORE, "v83")
    assert {k: v for k, v in v83.items() if k not in ("version", "package_checksum", "members", "entrypoints")} == {
        k: v for k, v in v82.items() if k not in ("version", "package_checksum", "members", "entrypoints")}
    members = {m["id"]: m for m in v82["members"]}
    entrypoints = {(e["id"], e["version"]) for e in v82["entrypoints"]}
    adds = replaces = 0
    for _name, body in bodies:
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": prototype.role_for(body["schema"])}
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
    assert (adds, replaces) == (5, 2)
    assert sorted(v83["members"], key=lambda m: m["id"]) == sorted(members.values(), key=lambda m: m["id"])
    assert {(e["id"], e["version"]) for e in v83["entrypoints"]} == entrypoints
    assert members[P + "rule.form1040-line25b"]["version"] == "v7"
    assert members[P + "form1040.line-25b"]["version"] == "v5"
    v82_members = {m["id"]: m["version"] for m in v82["members"]}
    assert v82_members[P + "rule.form1040-line25b"] == "v6"
    assert v82_members[P + "form1040.line-25b"] == "v4"


def test_registry_v81_only_adds_v83_and_its_new_citizens(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v80 = _load_json(CONTENT / "published-packages.v80.json")
    v81 = _load_json(CONTENT / "published-packages.v81.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v80[key]}
        after = {(e["id"], e["version"]): e for e in v81[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    packages = {(e["id"], e["version"]) for e in v81["packages"]} - {(e["id"], e["version"]) for e in v80["packages"]}
    assert packages == {(CORE, "v83")}
    assert (CORE, "v83") not in {(e["id"], e["version"]) for e in v80["packages"]}
    assert (CORE, "v82") in {(e["id"], e["version"]) for e in v80["packages"]}
    added = {(e["id"], e["version"]): e["checksum"] for e in v81["citizens"]}
    for identity in {(e["id"], e["version"]) for e in v80["citizens"]}:
        del added[identity]
    assert added == {(body["id"], body["version"]): citizen_checksum(body) for _name, body in bodies}


def test_release_v81_pins_registry_v81() -> None:
    release = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v81.json")
    previous = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v80.json")
    assert release["version"] == "v81"
    registry = (CONTENT / "published-packages.v81.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()
    assert {k: v for k, v in release.items() if k not in ("version", "package_registry_sha256")} == {
        k: v for k, v in previous.items() if k not in ("version", "package_registry_sha256")}


def test_core_v83_carries_v82_loader_entries_and_no_box4_pair() -> None:
    """The box 4 amount is statement-keyed. It takes no presence pair of its own."""
    declarations = domain_package_companion_declarations()
    v82, v83 = declarations[(CORE, "v82")], declarations[(CORE, "v83")]
    assert v83["presence_pairs"] == v82["presence_pairs"]
    assert v83["value_domains"] == v82["value_domains"]
    assert AMOUNT not in v83["presence_pairs"]
    assert covered_flag_refusal_map(CORE, "v83") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v83") == covered_flag_refusal_map(CORE, "v82")


def test_v82_still_reads_the_yes_no_and_v83_does_not() -> None:
    (v6,) = [text for text in _rule_texts("v82") if '"version": "v6"' in text and "rule.form1040-line25b" in text]
    assert v6.count("statement-box4-withholding") == v6.count("statement-box4-withholding-reported")
    assert "statement-box4-withholding-reported" in v6
    rules = _rule_texts("v83")
    (v7,) = [text for text in rules if '"version": "v7"' in text and "rule.form1040-line25b" in text]
    assert "statement-box4-withholding-reported" not in v7
    assert "f1099b.statement-box4-withholding" in v7
    assert all("statement-box4-withholding-reported" not in text for text in rules)


# ---- the question against its proposition --------------------------------------------


def test_the_box4_question_states_the_amount_proposition() -> None:
    question = _load_json(CONTENT / "input-question.f1099b-box4.v1.json")
    bundle = _load_json(CONTENT / "f1099b-box4.bundle.json")
    (fact,) = [item for item in bundle["fact_types"] if item["id"] == AMOUNT]
    assert question["question"] == QUESTION
    assert fact["title"] == (
        "Federal income tax withheld in box 4 of one recorded 2025 Form 1099-B statement. "
        "Nonnegative source amount only.")
    assert "If box 4 is blank, enter $0." in question["question"]
    assert question["fact_type"] == {"id": fact["id"], "version": fact["version"]} == {"id": AMOUNT, "version": "v1"}
    assert question["schema"] == "input-question.v1" and question["version"] == "v1"
    retired = _load_json(CONTENT / "input-question.f1099b-statement-box4-withholding-reported.json")
    assert retired["question"] != question["question"]
    assert "does it show federal income tax withheld in box 4" in retired["question"]
    assert retired["fact_type"]["id"] == YES_NO


# ---- the audit -----------------------------------------------------------------------


def _drop_amount_collect(node: Any) -> None:
    if isinstance(node, dict):
        for key, value in list(node.items()):
            if isinstance(value, list):
                node[key] = [
                    item for item in value
                    if not (
                        isinstance(item, dict)
                        and item.get("op") == "collect"
                        and item.get("name") == AMOUNT
                    )
                ]
                for item in node[key]:
                    _drop_amount_collect(item)
            else:
                _drop_amount_collect(value)
    elif isinstance(node, list):
        for item in node:
            _drop_amount_collect(item)


def test_v83_counts_the_box4_amount_as_read(tables: ModuleType) -> None:
    members = tables.members(CONTENT, "v83")
    assert tables.line25b_reads_amount(members) is True
    assert tables.accounted_boxes(members)[BOX4] == ["f1099b.statement-box4-withholding"]
    read = tables.read_by_rules(members)
    assert AMOUNT in read and YES_NO not in read
    assert tables.audit(members, tables.field_table(members)) == []
    assert tables.row_audit(tables.row_table(members, tables.loader_pairs("v83"))) == []
    earlier = tables.members(CONTENT, "v82")
    assert tables.line25b_reads_amount(earlier) is False
    assert tables.accounted_boxes(earlier)[BOX4] == ["f1099b.statement-box4-withholding-reported"]
    read_earlier = tables.read_by_rules(earlier)
    assert YES_NO in read_earlier and AMOUNT not in read_earlier


def test_removing_the_value_collect_fails_the_audit(tables: ModuleType) -> None:
    members = copy.deepcopy(tables.members(CONTENT, "v83"))
    assert AMOUNT in tables.read_by_rules(members)
    _drop_amount_collect(members)
    assert AMOUNT not in tables.read_by_rules(members)
    failures = tables.audit(members, tables.field_table(members))
    assert any("no rule reads the answer f1099b.statement-box4-withholding" in item for item in failures)


def test_the_committed_v83_tables_are_the_published_v83s(tables: ModuleType) -> None:
    members = tables.members(CONTENT, "v83")
    committed = _load_json(TABLES / "tables-v83.json")
    assert committed["package"] == "core-calculations v83"
    assert committed["fields"] == tables.field_table(members)
    assert committed["rows"] == tables.row_table(members, tables.loader_pairs("v83"))
    assert committed["consumers"] == tables.consumer_table(members)
    assert committed["audit_failures"] == []


def test_the_measured_return_classes_match_the_decided_design() -> None:
    """The live module pins each return. This locks the class counts without a run."""
    table = _load_json(FIXTURE)
    assert table["classes"] == CLASSES
    assert table["no_sales_changed"] == []
    assert len(table["track0"]) == 79
    assert len(table["returns"]) == 213
    assert sum(1 for entry in table["returns"].values() if not entry["has_sales"]) == 39
    assert "case/a_8949_yes/recorded" in table["zero_sample"]
    assert all(entry["restores_v82_lines"] is True for entry in table["zero_sample"].values())
    text = FIXTURE.read_text(encoding="utf-8")
    assert "/Users/" not in text and "/private/" not in text and "/tmp/" not in text and "/var/" not in text
