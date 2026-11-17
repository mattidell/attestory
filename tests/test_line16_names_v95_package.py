"""Fast publication checks for the two accepted failing-criterion citizens."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, cast

import pytest

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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/line16-names-evidence"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"


def _read(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _artifacts() -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], _read(EVIDENCE / "track1-content.json")["artifacts"])


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def test_citizens_match_the_accepted_prototype_bytes() -> None:
    artifacts = _artifacts()
    assert {row["filename"] for row in artifacts} == {
        "rule.form1040-line16.v9.json", "rule.selected-preferential-base.v12.json"
    }
    predecessors = {"v9": "rule.form1040-line16.v8.json", "v12": "rule.selected-preferential-base.v11.json"}
    for row in artifacts:
        path = CONTENT / row["filename"]
        assert path.stat().st_size == row["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        body = _read(path)
        assert all(body[key] == row[key] for key in ("id", "version", "schema"))
        assert body["schema"] == "rule-artifact.v17"
        before = _read(CONTENT / predecessors[body["version"]])
        changed = {"when", "version", "notes"}
        assert {key: value for key, value in body.items() if key not in changed} == {
            key: value for key, value in before.items() if key not in changed
        }, row["filename"]


def test_core_v95_replaces_exactly_the_two_members_and_entrypoints() -> None:
    before = _read(CONTENT / "package.core-calculations.v94.json")
    after = _read(CONTENT / "package.core-calculations.v95.json")
    old = {row["id"]: row for row in before["members"]}
    expected = dict(old)
    for row in _artifacts():
        expected[row["id"]] = {key: row[key] for key in ("id", "version", "schema", "role")}
    assert {row["id"]: row for row in after["members"]} == expected
    assert len(after["members"]) == len(before["members"]) == len(old)
    old_entries = {(row["id"], row["version"]) for row in before["entrypoints"]}
    new_entries = {(row["id"], row["version"]) for row in after["entrypoints"]}
    assert old_entries - new_entries == {(row["id"], old[row["id"]]["version"]) for row in _artifacts()}
    assert new_entries - old_entries == {(row["id"], row["version"]) for row in _artifacts()}
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v95")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v93_is_add_only() -> None:
    before = _read(CONTENT / "published-packages.v92.json")
    after = _read(CONTENT / "published-packages.v93.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            assert added == {(row["id"], row["version"]): {
                "id": row["id"], "version": row["version"],
                "checksum": citizen_checksum(_read(CONTENT / row["filename"]))
            } for row in _artifacts()}
        else:
            package = _read(CONTENT / "package.core-calculations.v95.json")
            assert added == {(CORE, "v95"): {"id": CORE, "version": "v95", "checksum": package["package_checksum"]}}


def test_release_and_publication_bytes_match_the_generated_prototype() -> None:
    for row in _read(EVIDENCE / "track1-publication.json")["files"]:
        parent = RELEASES if row["filename"].startswith("demo.release.") else CONTENT
        assert hashlib.sha256((parent / row["filename"]).read_bytes()).hexdigest() == row["sha256"]
    old = _read(RELEASES / f"{STEM}.v92.json")
    new = _read(RELEASES / f"{STEM}.v93.json")
    assert new == {**old, "version": "v93", "package_registry_sha256": hashlib.sha256((CONTENT / "published-packages.v93.json").read_bytes()).hexdigest()}


def test_v95_loader_entries_carry_v94_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v95")] == declarations[(CORE, "v94")]
    assert covered_flag_refusal_map(CORE, "v95") == covered_flag_refusal_map(CORE, "v94")
    assert covered_flag_refusal_map(CORE, "v95")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked, unconfirmed_family_names_closure_question):
        assert switch(CORE, "v95") == switch(CORE, "v94") is True


def test_line16_required_symbol_allowlist_carries_the_existing_rationales() -> None:
    transfers = _read(EVIDENCE / "track1-publication.json")["required_versus_read_allowlist_transfers"]
    assert len(transfers) == 2
    entries = _read(REPO / "tools/required_versus_read_allowlist.json")["entries"]
    assert {row["after"]["symbol"] for row in transfers} == {"filing_status", "tax.us.2025.income.taxable-income"}
    for row in transfers:
        assert row["before"]["version"] == "v8"
        assert row["after"] == {**row["before"], "version": "v9"}
        assert row["after"] in entries
        assert row["before"] not in entries


@pytest.mark.parametrize("shard", range(8))
def test_v94_and_earlier_bytes_are_unchanged(shard: int) -> None:
    # Bounded shards keep the full 1,801-file integrity witness in the fast lane.
    files = _read(EVIDENCE / "track1-historical-hashes.json")["files"]
    assert len(files) == 1801
    for relative, sha in list(files.items())[shard::8]:
        assert hashlib.sha256((REPO / relative).read_bytes()).hexdigest() == sha, relative
