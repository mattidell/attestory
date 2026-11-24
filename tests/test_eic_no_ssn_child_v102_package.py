"""Publication checks for core v102, registry v100 and release v100.

v102 replaces eight earned-income-credit rules and adds the qualifying-child
test and the present count. The loader entries carry v101's maps. The
published rule files are the widened successors from track1_design.py.
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-no-ssn-child-evidence"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def _design() -> Any:
    return evidence_loader.load(EVIDENCE / "track1_design.py", "ens_t1_package_design")


def test_published_rules_are_the_widened_design() -> None:
    design = _design()
    bodies = design.written(CONTENT)
    assert set(bodies) == {
        "rule.eic-child.qualifies.json",
        "rule.eic-qualifying-child-present.json",
        "rule.eic-status-class.v3.json",
        "rule.eic-early-stop.v3.json",
        "rule.eic-questions-required.v3.json",
        "rule.eic-answer.separated-spouse.v2.json",
        "rule.eic-answer.not-married.v2.json",
        "rule.eic-answer.age-25-under-65.v4.json",
        "rule.eic-answer.main-home-in-us.v4.json",
        "rule.eic-answer.not-claimable-as-dependent.v4.json",
    }
    for name, body in bodies.items():
        assert _read(CONTENT / name) == body
    assert "tax.us.2025.eic.status-class" not in bodies["rule.eic-answer.age-25-under-65.v4.json"]["requires"]
    assert "tax.us.2025.eic.status-class" not in bodies["rule.eic-answer.main-home-in-us.v4.json"]["requires"]
    counts = _read(CONTENT / "rule.eic-child.counts.v2.json")
    qualifies = bodies["rule.eic-child.qualifies.json"]
    assert "tax.us.2025.eic.child.ssn-met" in counts["requires"]
    assert "tax.us.2025.eic.child.ssn-met" not in qualifies["requires"]


def test_core_v102_replaces_eight_rules_and_adds_two() -> None:
    design = _design()
    before = _read(CONTENT / "package.core-calculations.v101.json")
    after = _read(CONTENT / "package.core-calculations.v102.json")
    bodies = design.written(CONTENT)
    old = {row["id"]: row for row in before["members"]}
    expected = dict(old)
    for rule_id, version in design.REPLACED.items():
        assert old[rule_id]["version"] == version
        successor = next(body for body in bodies.values() if body["id"] == rule_id)
        expected[rule_id] = {**old[rule_id], "version": successor["version"], "schema": successor["schema"]}
    for rule_id in (design.QUALIFIES_RULE, design.PRESENT_RULE):
        assert rule_id not in old
        body = next(item for item in bodies.values() if item["id"] == rule_id)
        expected[rule_id] = {"id": rule_id, "version": "v1", "schema": body["schema"], "role": "computation"}
    assert {row["id"]: row for row in after["members"]} == expected
    assert {(row["id"], row["version"]) for row in after["entrypoints"]} == {
        (row["id"], row["version"]) for row in before["entrypoints"]
    }
    skip = {"version", "members", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v102")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v100_is_add_only() -> None:
    design = _design()
    before = _read(CONTENT / "published-packages.v99.json")
    after = _read(CONTENT / "published-packages.v100.json")
    bodies = design.written(CONTENT)
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
            package = _read(CONTENT / "package.core-calculations.v102.json")
            assert added == {(CORE, "v102"): {"id": CORE, "version": "v102", "checksum": package["package_checksum"]}}


def test_release_v100_differs_from_v99_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v99.json")
    new = _read(RELEASES / f"{STEM}.v100.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v100.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v100", "package_registry_sha256": digest}


def test_v102_loader_entries_carry_v101_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v102")] == declarations[(CORE, "v101")]
    assert covered_flag_refusal_map(CORE, "v102") == covered_flag_refusal_map(CORE, "v101")
    assert covered_flag_refusal_map(CORE, "v102")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked,
                   unconfirmed_family_names_closure_question):
        assert switch(CORE, "v102") == switch(CORE, "v101") is True
