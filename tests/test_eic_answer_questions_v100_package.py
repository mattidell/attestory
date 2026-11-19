"""Fast publication checks for core v100, registry v98 and release v98.

v100 admits exactly four input questions against v99, one for each earned
income credit answer that had none (age, main home, not claimable as a
dependent, spouse Social Security number), each also an entrypoint, and
changes nothing else in the package. Each names an existing fact type of the
published eic-questions vocabulary that no v99 question names, and carries
the wording P0 designed.
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-answer-questions-evidence"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
P = "tax.us.2025."
NAMES = ("age-25-under-65", "main-home-in-us", "not-claimable-as-dependent", "spouse-valid-ssn")
QUESTIONS = tuple(P + "input-question.eic-" + name for name in NAMES)
FILES = {P + "input-question.eic-" + name: "input-question.eic-" + name + ".v1.json" for name in NAMES}


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def test_core_v100_admits_exactly_the_four_questions() -> None:
    before = _read(CONTENT / "package.core-calculations.v99.json")
    after = _read(CONTENT / "package.core-calculations.v100.json")
    old = {row["id"]: row for row in before["members"]}
    expected = dict(old)
    for question in QUESTIONS:
        assert question not in old
        expected[question] = {"id": question, "version": "v1", "schema": "input-question.v1", "role": "input-question"}
    assert {row["id"]: row for row in after["members"]} == expected
    assert len(after["members"]) == len(before["members"]) + 4
    old_entries = {(row["id"], row["version"]) for row in before["entrypoints"]}
    new_entries = {(row["id"], row["version"]) for row in after["entrypoints"]}
    assert old_entries <= new_entries
    assert new_entries - old_entries == {(q, "v1") for q in QUESTIONS}
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v100")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_each_question_names_an_existing_fact_no_v99_question_names() -> None:
    package = _read(CONTENT / "package.core-calculations.v99.json")
    bundle = _read(CONTENT / "eic-questions.bundle.json")
    assert (bundle["id"], bundle["version"]) in {(m["id"], m["version"]) for m in package["members"]}
    declared = {fact["id"] for fact in bundle["fact_types"]}
    pins = {(m["id"], m["version"]) for m in package["members"] if m["role"] == "input-question"}
    asked = set()
    found = set()
    for path in CONTENT.glob("input-question.*.json"):  # file names are not uniform, so match by id and version
        body = _read(path)
        if (body["id"], body["version"]) in pins:
            found.add((body["id"], body["version"]))
            asked.add(body["fact_type"]["id"])
    assert found == pins
    design = evidence_loader.load(EVIDENCE / "design.py", "eicq_t1_package_design")
    for name in NAMES:
        body = _read(CONTENT / FILES[P + "input-question.eic-" + name])
        assert body == {"fact_type": {"id": P + "eic." + name, "version": "v1"}, "id": P + "input-question.eic-" + name,
                        "question": design.QUESTIONS[name], "schema": "input-question.v1", "version": "v1"}
        assert body["fact_type"]["id"] in declared and body["fact_type"]["id"] not in asked


def test_registry_v98_is_add_only() -> None:
    before = _read(CONTENT / "published-packages.v97.json")
    after = _read(CONTENT / "published-packages.v98.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            assert added == {(q, "v1"): {"id": q, "version": "v1", "checksum": citizen_checksum(_read(CONTENT / FILES[q]))}
                             for q in QUESTIONS}
        else:
            package = _read(CONTENT / "package.core-calculations.v100.json")
            assert added == {(CORE, "v100"): {"id": CORE, "version": "v100", "checksum": package["package_checksum"]}}


def test_release_v98_differs_from_v97_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v97.json")
    new = _read(RELEASES / f"{STEM}.v98.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v98.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v98", "package_registry_sha256": digest}


def test_v100_loader_entries_carry_v99_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v100")] == declarations[(CORE, "v99")]
    assert covered_flag_refusal_map(CORE, "v100") == covered_flag_refusal_map(CORE, "v99")
    assert covered_flag_refusal_map(CORE, "v100")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked,
                   unconfirmed_family_names_closure_question):
        assert switch(CORE, "v100") == switch(CORE, "v99") is True
