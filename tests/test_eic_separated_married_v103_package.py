"""Publication checks for core v103, registry v101 and release v101.

v103 replaces the separated-spouse answer with v3 and adds Step 3 question 3:
the vocabulary bundle, the input question, and three computation rules. The
loader entries carry v102's maps. The published files are design.written.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import (
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    later_any_arm_refs_while_count_blocked,
    selection_collect_satisfied_by_family,
    unconfirmed_family_names_closure_question,
)
from tests import evidence_loader

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-separated-married-evidence"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
SEPARATED = "tax.us.2025.rule.eic-answer.separated-spouse"
CAP = 5000


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def _design() -> Any:
    return evidence_loader.load(EVIDENCE / "design.py", "esm_t1_package_design")


def test_published_files_match_the_design() -> None:
    design = _design()
    v2 = _read(CONTENT / "rule.eic-answer.separated-spouse.v2.json")
    bodies = design.written(v2)
    assert set(bodies) == {
        "eic-married-taxpayer.bundle.json",
        "input-question.eic-married-taxpayer.v1.json",
        "rule.eic-married-taxpayer-recorded.v1.json",
        "rule.eic-married-taxpayer-from-separated.v1.json",
        "rule.eic-answer.married-taxpayer.v1.json",
        "rule.eic-answer.separated-spouse.v3.json",
    }
    for name, body in bodies.items():
        assert _read(CONTENT / name) == body
        if name.startswith("rule."):
            assert (CONTENT / name).stat().st_size <= CAP
    question = bodies["input-question.eic-married-taxpayer.v1.json"]
    assert question["fact_type"]["id"] == design.MARRIED
    married = next(fact for fact in bodies["eic-married-taxpayer.bundle.json"]["fact_types"] if fact["id"] == design.MARRIED)
    inert = next(fact for fact in bodies["eic-married-taxpayer.bundle.json"]["fact_types"] if fact["id"] == design.INERT)
    for text in (question["question"], married["title"]):
        assert "interlocutory decree" in text
        assert "final decree of divorce or of separate maintenance" in text
        assert "considered unmarried" in text
        assert "Rule 3" in text
        assert "continues to question 6" in text
        assert "keep the credit" not in text
    assert inert["value_schema"] == {"not": {}}
    fact_ids = {fact["id"] for fact in bodies["eic-married-taxpayer.bundle.json"]["fact_types"]}
    assert fact_ids == {design.MARRIED, design.INERT}
    for path in CONTENT.glob("input-question*.json"):
        offered = (_read(path).get("fact_type") or {}).get("id")
        assert offered != design.INERT


def test_core_v103_replaces_separated_spouse_and_adds_the_question() -> None:
    design = _design()
    before = _read(CONTENT / "package.core-calculations.v102.json")
    after = _read(CONTENT / "package.core-calculations.v103.json")
    bodies = design.written(_read(CONTENT / "rule.eic-answer.separated-spouse.v2.json"))
    old = {row["id"]: row for row in before["members"]}
    new = {row["id"]: row for row in after["members"]}
    added = {
        design.RULE_RECORDED: {"id": design.RULE_RECORDED, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"},
        design.RULE_FROM: {"id": design.RULE_FROM, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"},
        design.RULE_ANSWER: {"id": design.RULE_ANSWER, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"},
        design.BUNDLE_ID: {"id": design.BUNDLE_ID, "version": "v1", "schema": "bundle.v2", "role": "fact-type-bundle"},
        design.MARRIED.replace(".eic.married-taxpayer", ".input-question.eic-married-taxpayer"): {
            "id": bodies["input-question.eic-married-taxpayer.v1.json"]["id"],
            "version": "v1",
            "schema": "input-question.v1",
            "role": "input-question",
        },
    }
    assert set(new) - set(old) == set(added)
    assert set(old) - set(new) == set()
    assert old[SEPARATED]["version"] == "v2"
    assert new[SEPARATED] == {**old[SEPARATED], "version": "v3"}
    for rule_id, row in old.items():
        if rule_id != SEPARATED:
            assert new[rule_id] == row
    for rule_id, row in added.items():
        assert new[rule_id] == row
    old_entries = {row["id"]: row for row in before["entrypoints"]}
    new_entries = {row["id"]: row for row in after["entrypoints"]}
    assert set(new_entries) - set(old_entries) == {design.BUNDLE_ID, added_question_id(bodies)}
    assert new_entries[design.BUNDLE_ID] == {"id": design.BUNDLE_ID, "version": "v1"}
    assert new_entries[added_question_id(bodies)] == {"id": added_question_id(bodies), "version": "v1"}
    for rule_id, row in old_entries.items():
        assert new_entries[rule_id] == row
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v103")
    assert after["package_checksum"] == package_instance_checksum(after)


def added_question_id(bodies: dict[str, Any]) -> str:
    return str(bodies["input-question.eic-married-taxpayer.v1.json"]["id"])


def test_registry_v101_is_add_only() -> None:
    design = _design()
    before = _read(CONTENT / "published-packages.v100.json")
    after = _read(CONTENT / "published-packages.v101.json")
    bodies = design.written(_read(CONTENT / "rule.eic-answer.separated-spouse.v2.json"))
    expected = {
        (body["id"], body["version"]): {
            "id": body["id"], "version": body["version"], "checksum": citizen_checksum(_read(CONTENT / name)),
        }
        for name, body in bodies.items()
    }
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            assert added == expected
        else:
            package = _read(CONTENT / "package.core-calculations.v103.json")
            assert added == {(CORE, "v103"): {"id": CORE, "version": "v103", "checksum": package["package_checksum"]}}


def test_release_v101_differs_from_v100_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v100.json")
    new = _read(RELEASES / f"{STEM}.v101.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v101.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v101", "package_registry_sha256": digest}


def test_v103_loader_entries_carry_v102_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v103")] == declarations[(CORE, "v102")]
    assert covered_flag_refusal_map(CORE, "v103") == covered_flag_refusal_map(CORE, "v102")
    assert covered_flag_refusal_map(CORE, "v103")
    for switch in (
        selection_collect_satisfied_by_family,
        later_any_arm_refs_while_count_blocked,
        unconfirmed_family_names_closure_question,
    ):
        assert switch(CORE, "v103") == switch(CORE, "v102") is True
