"""Fast publication checks for core v97, registry v95 and release v95.

v97 admits exactly the five Schedule 1 lines 2a-6 input-question successors
of variant q and changes nothing else in the package against v96.
"""
from __future__ import annotations

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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-bartering-evidence"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
SENTENCE = (" Also answer yes if a Form 1099-B you received shows an amount above zero in box 13 (Bartering), "
            "even if you do not think of it as a business.")
IDS = tuple("tax.us.2025.input-question.schedule1-part1-scope-" + s for s in (
    "no-sch1-line2a-alimony", "no-sch1-line3-business", "no-sch1-line4-other-gains", "no-sch1-line5-rental",
    "no-sch1-line6-farm"))


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _file(citizen: str, version: str) -> Path:
    return CONTENT / (citizen.removeprefix("tax.us.2025.") + f".{version}.json")


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def test_the_wording_manifest_is_exactly_the_five_questions() -> None:
    rows = [r for r in _read(EVIDENCE / "wording.json")["replacements"] if "q" in r["variants"]]
    assert sorted(r["id"] for r in rows) == sorted(IDS)
    assert {r["new"] for r in rows} == {next(iter({r["old"] for r in rows})) + SENTENCE}


def test_each_successor_is_its_predecessor_plus_the_sentence_and_a_version() -> None:
    for citizen in IDS:
        old, new = _read(_file(citizen, "v1")), _read(_file(citizen, "v2"))
        assert old["version"] == "v1" and new["version"] == "v2"
        assert new["question"] == old["question"] + SENTENCE
        assert {k: v for k, v in new.items() if k not in ("version", "question")} == \
            {k: v for k, v in old.items() if k not in ("version", "question")}


def test_core_v97_replaces_exactly_the_five_members_and_entrypoints() -> None:
    before = _read(CONTENT / "package.core-calculations.v96.json")
    after = _read(CONTENT / "package.core-calculations.v97.json")
    old = {row["id"]: row for row in before["members"]}
    expected = dict(old)
    for citizen in IDS:
        assert old[citizen]["version"] == "v1"
        expected[citizen] = {**old[citizen], "version": "v2"}
    assert {row["id"]: row for row in after["members"]} == expected
    assert len(after["members"]) == len(before["members"])
    old_entries = {(row["id"], row["version"]) for row in before["entrypoints"]}
    new_entries = {(row["id"], row["version"]) for row in after["entrypoints"]}
    assert old_entries - new_entries == {(c, "v1") for c in IDS}
    assert new_entries - old_entries == {(c, "v2") for c in IDS}
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v97")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_registry_v95_is_add_only() -> None:
    before = _read(CONTENT / "published-packages.v94.json")
    after = _read(CONTENT / "published-packages.v95.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            assert added == {(c, "v2"): {"id": c, "version": "v2",
                                         "checksum": citizen_checksum(_read(_file(c, "v2")))} for c in IDS}
        else:
            package = _read(CONTENT / "package.core-calculations.v97.json")
            assert added == {(CORE, "v97"): {"id": CORE, "version": "v97", "checksum": package["package_checksum"]}}


def test_release_v95_differs_from_v94_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v94.json")
    new = _read(RELEASES / f"{STEM}.v95.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v95.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v95", "package_registry_sha256": digest}


def test_v97_loader_entries_carry_v96_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v97")] == declarations[(CORE, "v96")]
    assert covered_flag_refusal_map(CORE, "v97") == covered_flag_refusal_map(CORE, "v96")
    assert covered_flag_refusal_map(CORE, "v97")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked,
                   unconfirmed_family_names_closure_question):
        assert switch(CORE, "v97") == switch(CORE, "v96") is True


def test_the_v1_predecessors_are_still_published_and_unchanged() -> None:
    registry = _index(_read(CONTENT / "published-packages.v95.json")["citizens"])
    for citizen in IDS:
        assert registry[(citizen, "v1")]["checksum"] == citizen_checksum(_read(_file(citizen, "v1")))
    assert cast(str, _read(_file(IDS[0], "v1"))["question"]).endswith("Schedule 1 lines 2a through 6?")
