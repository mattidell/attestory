"""Fast publication checks for core v96, registry v94 and release v94.

The 50 successor citizens carry the accepted Track 0 manifest texts and
nothing else. v95 and earlier stay as published.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, cast

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import (
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    later_any_arm_refs_while_count_blocked,
    selection_collect_satisfied_by_family,
    unconfirmed_family_names_closure_question,
)

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/plain-line-texts-evidence"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _successors() -> list[dict[str, Any]]:
    rows = cast(list[dict[str, Any]], _read(EVIDENCE / "track0-validation.json")["successors"])
    assert len(rows) == 50
    return rows


def _manifest() -> list[dict[str, Any]]:
    rows = cast(list[dict[str, Any]], _read(EVIDENCE / "track0-wording.json")["replacements"])
    assert len(rows) == 57
    return rows


def _at(body: dict[str, Any], path: str) -> Any:
    node: Any = body
    for part in path.split("."):
        node = node[part]
    return node


def _put(body: dict[str, Any], path: str, value: str) -> None:
    *parents, last = path.split(".")
    node: Any = body
    for part in parents:
        node = node[part]
    node[last] = value


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def test_successor_bytes_match_the_accepted_digests() -> None:
    for row in _successors():
        path = CONTENT / row["successor_filename"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["successor_sha256"], row["id"]
        assert hashlib.sha256((REPO / row["predecessor"]).read_bytes()).hexdigest() == row["predecessor_sha256"]


def test_successors_carry_exactly_the_manifest_texts() -> None:
    by_file: dict[str, list[dict[str, Any]]] = {}
    for row in _manifest():
        by_file.setdefault(row["file"], []).append(row)
    assert len(by_file) == 50
    for row in _successors():
        old = _read(REPO / row["predecessor"])
        new = _read(CONTENT / row["successor_filename"])
        expected = copy.deepcopy(old)
        for item in by_file[row["predecessor"]]:
            assert _at(old, item["property"]) == item["old"]
            assert _at(new, item["property"]) == item["new"]
            _put(expected, item["property"], item["new"])
        expected["version"] = row["new_version"]
        assert new == expected, row["id"]
        assert [item["property"] for item in by_file[row["predecessor"]]] == row["changed_properties"]


def test_core_v96_replaces_exactly_the_50_members_and_entrypoints() -> None:
    before = _read(CONTENT / "package.core-calculations.v95.json")
    after = _read(CONTENT / "package.core-calculations.v96.json")
    old = {row["id"]: row for row in before["members"]}
    expected = dict(old)
    for row in _successors():
        assert old[row["id"]]["version"] == row["old_version"]
        expected[row["id"]] = {**old[row["id"]], "version": row["new_version"]}
    assert {row["id"]: row for row in after["members"]} == expected
    assert len(after["members"]) == len(before["members"])
    old_entries = {(row["id"], row["version"]) for row in before["entrypoints"]}
    new_entries = {(row["id"], row["version"]) for row in after["entrypoints"]}
    ids = {row["id"]: row for row in _successors()}
    assert old_entries - new_entries == {(i, r["old_version"]) for i, r in ids.items() if (i, r["old_version"]) in old_entries}
    assert new_entries - old_entries == {(i, r["new_version"]) for i, r in ids.items() if (i, r["old_version"]) in old_entries}
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v96")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v94_is_add_only() -> None:
    before = _read(CONTENT / "published-packages.v93.json")
    after = _read(CONTENT / "published-packages.v94.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            assert added == {(r["id"], r["new_version"]): {
                "id": r["id"], "version": r["new_version"],
                "checksum": citizen_checksum(_read(CONTENT / r["successor_filename"]))} for r in _successors()}
        else:
            package = _read(CONTENT / "package.core-calculations.v96.json")
            assert added == {(CORE, "v96"): {"id": CORE, "version": "v96", "checksum": package["package_checksum"]}}


def test_release_v94_differs_from_v93_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v93.json")
    new = _read(RELEASES / f"{STEM}.v94.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v94.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v94", "package_registry_sha256": digest}


def test_v96_loader_entries_carry_v95_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v96")] == declarations[(CORE, "v95")]
    assert covered_flag_refusal_map(CORE, "v96") == covered_flag_refusal_map(CORE, "v95")
    assert covered_flag_refusal_map(CORE, "v96")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked,
                   unconfirmed_family_names_closure_question):
        assert switch(CORE, "v96") == switch(CORE, "v95") is True


def test_every_earlier_published_citizen_is_untouched() -> None:
    # Published v95 and earlier members still exist byte-for-byte: each
    # predecessor file keeps the digest recorded when it was replaced.
    for row in _successors():
        assert hashlib.sha256((REPO / row["predecessor"]).read_bytes()).hexdigest() == row["predecessor_sha256"]
    registry = _index(_read(CONTENT / "published-packages.v94.json")["citizens"])
    for row in _successors():
        old = _read(REPO / row["predecessor"])
        assert registry[(row["id"], row["old_version"])]["checksum"] == citizen_checksum(old)
