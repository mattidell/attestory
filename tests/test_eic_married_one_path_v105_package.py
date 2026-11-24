"""Publication checks for core v105, registry v103 and release v103.

v105 replaces the two married-taxpayer selection rules with one-path
successors. The loader entries carry v104's maps. The published rule files
are design.written.
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-married-one-path-evidence"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
RECORDED = "tax.us.2025.rule.eic-married-taxpayer-recorded"
FROM_SEPARATED = "tax.us.2025.rule.eic-married-taxpayer-from-separated"
EIC_CAP = 5000


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def _design() -> Any:
    return evidence_loader.load(EVIDENCE / "design.py", "emo_t1_package_design")


def test_published_one_path_files_match_the_design() -> None:
    design = _design()
    bodies = design.written(CONTENT)
    assert set(bodies) == {design.RECORDED_FILE, design.FROM_FILE}
    for name, body in bodies.items():
        assert _read(CONTENT / name) == body
        assert (CONTENT / name).stat().st_size <= EIC_CAP
        assert body["schema"] == "rule-artifact.v17"
        assert body["version"] == "v2"
        assert [path["id"] for path in body["selection"]["paths"]] == [design.PATH_ID]
        assert design.INERT not in json.dumps(body)
    assert bodies[design.RECORDED_FILE]["publishes"] == "tax.us.2025.eic.married-taxpayer-recorded"
    assert bodies[design.FROM_FILE]["publishes"] == "tax.us.2025.eic.married-taxpayer-from-separated"
    assert bodies[design.RECORDED_FILE]["id"] == RECORDED
    assert bodies[design.FROM_FILE]["id"] == FROM_SEPARATED


def test_core_v105_replaces_only_the_two_selection_rules() -> None:
    before = _read(CONTENT / "package.core-calculations.v104.json")
    after = _read(CONTENT / "package.core-calculations.v105.json")
    old = {row["id"]: row for row in before["members"]}
    new = {row["id"]: row for row in after["members"]}
    assert set(new) == set(old)
    for rule_id in (RECORDED, FROM_SEPARATED):
        assert old[rule_id] == {"id": rule_id, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"}
        assert new[rule_id] == {**old[rule_id], "version": "v2", "schema": "rule-artifact.v17"}
    for rule_id, row in old.items():
        if rule_id not in {RECORDED, FROM_SEPARATED}:
            assert new[rule_id] == row
    assert after["entrypoints"] == before["entrypoints"]
    skip = {"version", "members", "package_checksum"}
    assert {key: value for key, value in after.items() if key not in skip} == {
        key: value for key, value in before.items() if key not in skip
    }
    assert (after["id"], after["version"]) == (CORE, "v105")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v103_is_add_only() -> None:
    design = _design()
    before = _read(CONTENT / "published-packages.v102.json")
    after = _read(CONTENT / "published-packages.v103.json")
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
            package = _read(CONTENT / "package.core-calculations.v105.json")
            assert added == {(CORE, "v105"): {"id": CORE, "version": "v105", "checksum": package["package_checksum"]}}


def test_release_v103_differs_from_v102_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v102.json")
    new = _read(RELEASES / f"{STEM}.v103.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v103.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v103", "package_registry_sha256": digest}


def test_v105_loader_entries_carry_v104_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v105")] == declarations[(CORE, "v104")]
    assert covered_flag_refusal_map(CORE, "v105") == covered_flag_refusal_map(CORE, "v104")
    assert covered_flag_refusal_map(CORE, "v105")
    for switch in (
        selection_collect_satisfied_by_family,
        later_any_arm_refs_while_count_blocked,
        unconfirmed_family_names_closure_question,
    ):
        assert switch(CORE, "v105") == switch(CORE, "v104") is True
