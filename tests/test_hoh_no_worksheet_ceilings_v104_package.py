"""Publication checks for core v104, registry v102 and release v102.

v104 replaces the qualified-dividends worksheet ceilings with the successors
that read the head-of-household and qualifying-surviving-spouse answers.
The loader entries carry v103's maps. The published rule files are design.written.
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings-evidence"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
LINE6 = "tax.us.2025.rule.qdcg-worksheet.line-6"
LINE13 = "tax.us.2025.rule.qdcg-worksheet.line-13"
WORKSHEET_CAP = 6 * 1024


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def _design() -> Any:
    return evidence_loader.load(EVIDENCE / "design.py", "hnw_t1_package_design")


def test_published_ceiling_files_match_the_design() -> None:
    design = _design()
    bodies = design.written(CONTENT)
    assert set(bodies) == {design.LINE6_FILE, design.LINE13_FILE}
    for name, body in bodies.items():
        assert _read(CONTENT / name) == body
        assert (CONTENT / name).stat().st_size <= WORKSHEET_CAP
        assert body["schema"] == "rule-artifact.v17"
        assert body["version"] == "v2"
    assert bodies[design.LINE6_FILE]["publishes"] == "tax.us.2025.qdcg-worksheet.line-6"
    assert bodies[design.LINE13_FILE]["publishes"] == "tax.us.2025.qdcg-worksheet.line-13"


def test_core_v104_replaces_only_the_ceiling_rules() -> None:
    before = _read(CONTENT / "package.core-calculations.v103.json")
    after = _read(CONTENT / "package.core-calculations.v104.json")
    old = {row["id"]: row for row in before["members"]}
    new = {row["id"]: row for row in after["members"]}
    assert set(new) == set(old)
    assert old[LINE6] == {"id": LINE6, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"}
    assert old[LINE13] == {"id": LINE13, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"}
    assert new[LINE6] == {**old[LINE6], "version": "v2", "schema": "rule-artifact.v17"}
    assert new[LINE13] == {**old[LINE13], "version": "v2", "schema": "rule-artifact.v17"}
    for rule_id, row in old.items():
        if rule_id not in {LINE6, LINE13}:
            assert new[rule_id] == row
    assert after["entrypoints"] == before["entrypoints"]
    skip = {"version", "members", "package_checksum"}
    assert {key: value for key, value in after.items() if key not in skip} == {
        key: value for key, value in before.items() if key not in skip
    }
    assert (after["id"], after["version"]) == (CORE, "v104")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v102_is_add_only() -> None:
    design = _design()
    before = _read(CONTENT / "published-packages.v101.json")
    after = _read(CONTENT / "published-packages.v102.json")
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
            package = _read(CONTENT / "package.core-calculations.v104.json")
            assert added == {(CORE, "v104"): {"id": CORE, "version": "v104", "checksum": package["package_checksum"]}}


def test_release_v102_differs_from_v101_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v101.json")
    new = _read(RELEASES / f"{STEM}.v102.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v102.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v102", "package_registry_sha256": digest}


def test_v104_loader_entries_carry_v103_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v104")] == declarations[(CORE, "v103")]
    assert covered_flag_refusal_map(CORE, "v104") == covered_flag_refusal_map(CORE, "v103")
    assert covered_flag_refusal_map(CORE, "v104")
    for switch in (
        selection_collect_satisfied_by_family,
        later_any_arm_refs_while_count_blocked,
        unconfirmed_family_names_closure_question,
    ):
        assert switch(CORE, "v104") == switch(CORE, "v103") is True
