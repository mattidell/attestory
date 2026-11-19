"""Fast publication checks for core v98, registry v96 and release v96.

v98 admits exactly the vocabulary bundle with the two return-level answers,
the two input questions and the rule.dependents-worksheet-line-3 v2 successor
against v97, and changes nothing else in the package.
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

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
P = "tax.us.2025."
RULE = P + "rule.dependents-worksheet-line-3"
BUNDLE = P + "filing-status-tests.vocabulary"
QUESTIONS = (P + "input-question.hoh-tests-met", P + "input-question.qss-tests-met")
NEW = ((BUNDLE, "bundle.v2", "fact-type-bundle"), (QUESTIONS[0], "input-question.v1", "input-question"),
       (QUESTIONS[1], "input-question.v1", "input-question"))


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _file(citizen: str, version: str) -> Path:
    name = citizen.removeprefix(P)
    return CONTENT / ("filing-status-tests.bundle.json" if citizen == BUNDLE else f"{name}.{version}.json")


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def test_core_v98_admits_exactly_the_new_members_and_the_rule_successor() -> None:
    before = _read(CONTENT / "package.core-calculations.v97.json")
    after = _read(CONTENT / "package.core-calculations.v98.json")
    old = {row["id"]: row for row in before["members"]}
    assert old[RULE]["version"] == "v1" and old[RULE]["schema"] == "rule-artifact.v14"
    expected = {**old, RULE: {**old[RULE], "version": "v2", "schema": "rule-artifact.v17"}}
    for citizen, schema, role in NEW:
        assert citizen not in old
        expected[citizen] = {"id": citizen, "version": "v1", "schema": schema, "role": role}
    assert {row["id"]: row for row in after["members"]} == expected
    assert len(after["members"]) == len(before["members"]) + 3
    old_entries = {(row["id"], row["version"]) for row in before["entrypoints"]}
    new_entries = {(row["id"], row["version"]) for row in after["entrypoints"]}
    assert old_entries <= new_entries
    assert new_entries - old_entries == {(c, "v1") for c, _, _ in NEW}  # the rule is not an entrypoint
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v98")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_the_rule_successor_is_v1_with_the_two_tests_read_on_their_status() -> None:
    old, new = _read(CONTENT / "rule.dependents-worksheet-line-3.json"), _read(
        CONTENT / "rule.dependents-worksheet-line-3.v2.json")
    assert (old["version"], new["version"]) == ("v1", "v2")
    assert new["schema"] == "rule-artifact.v17"
    skip = ("schema", "version", "value", "notes")
    assert {k: v for k, v in new.items() if k not in skip} == {k: v for k, v in old.items() if k not in skip}
    text = json.dumps(new["value"])
    assert P + "hoh.tests-met" in text and P + "qss.tests-met" in text
    assert text.count(json.dumps(old["value"])) == 3  # v1's lookup on each branch that publishes
    assert P + "hoh.tests-met" not in json.dumps(old)


def test_registry_v96_is_add_only() -> None:
    before = _read(CONTENT / "published-packages.v95.json")
    after = _read(CONTENT / "published-packages.v96.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            expected = {(c, "v1"): {"id": c, "version": "v1", "checksum": citizen_checksum(_read(_file(c, "v1")))}
                        for c, _, _ in NEW}
            expected[(RULE, "v2")] = {"id": RULE, "version": "v2", "checksum": citizen_checksum(_read(_file(RULE, "v2")))}
            assert added == expected
        else:
            package = _read(CONTENT / "package.core-calculations.v98.json")
            assert added == {(CORE, "v98"): {"id": CORE, "version": "v98", "checksum": package["package_checksum"]}}


def test_release_v96_differs_from_v95_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v95.json")
    new = _read(RELEASES / f"{STEM}.v96.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v96.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v96", "package_registry_sha256": digest}


def test_v98_loader_entries_carry_v97_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v98")] == declarations[(CORE, "v97")]
    assert covered_flag_refusal_map(CORE, "v98") == covered_flag_refusal_map(CORE, "v97")
    assert covered_flag_refusal_map(CORE, "v98")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked,
                   unconfirmed_family_names_closure_question):
        assert switch(CORE, "v98") == switch(CORE, "v97") is True


def test_the_v1_rule_is_still_published_and_unchanged() -> None:
    registry = _index(_read(CONTENT / "published-packages.v96.json")["citizens"])
    assert registry[(RULE, "v1")]["checksum"] == citizen_checksum(_read(CONTENT / "rule.dependents-worksheet-line-3.json"))
