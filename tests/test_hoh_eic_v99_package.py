"""Fast publication checks for core v99, registry v97 and release v97.

v99 admits exactly the vocabulary bundle with the return-level marital-status
answer, the two input questions and the new rule.eic-answer.not-married
against v98, replaces rule.eic-status-class v1 and rule.eic-gate-result v2 by
their successors, replaces the five Step 4 question 2-6 answer rules by their
successors (a married "no" stops the questions, review EIC-R1), and changes
nothing else in the package.
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
BUNDLE = P + "eic-marital-status.vocabulary"
QUESTIONS = (P + "input-question.eic-not-married", P + "input-question.eic-separated-spouse")
ANSWER_RULE = P + "rule.eic-answer.not-married"
CLASS_RULE, GATE_RULE = P + "rule.eic-status-class", P + "rule.eic-gate-result"
STEP4 = ("age-25-under-65", "main-home-in-us", "not-claimable-as-dependent", "not-qualifying-child-of-another",
         "no-unsupported-situations")
STEP4_RULES = tuple(P + "rule.eic-answer." + name for name in STEP4)
SUCCESSORS = {CLASS_RULE: ("v1", "v2"), GATE_RULE: ("v2", "v3"), **{rule: ("v2", "v3") for rule in STEP4_RULES}}
NEW = ((BUNDLE, "bundle.v2", "fact-type-bundle"), (QUESTIONS[0], "input-question.v1", "input-question"),
       (QUESTIONS[1], "input-question.v1", "input-question"), (ANSWER_RULE, "rule-artifact.v14", "computation"))
FILES = {
    BUNDLE: "eic-marital-status.bundle.json",
    QUESTIONS[0]: "input-question.eic-not-married.v1.json",
    QUESTIONS[1]: "input-question.eic-separated-spouse.v1.json",
    ANSWER_RULE: "rule.eic-answer.not-married.json",
    CLASS_RULE + "|v1": "rule.eic-status-class.json",
    CLASS_RULE + "|v2": "rule.eic-status-class.v2.json",
    GATE_RULE + "|v2": "rule.eic-gate-result.v2.json",
    GATE_RULE + "|v3": "rule.eic-gate-result.v3.json",
}
for _name in STEP4:
    FILES[P + "rule.eic-answer." + _name + "|v2"] = "rule.eic-answer." + _name + ".v2.json"
    FILES[P + "rule.eic-answer." + _name + "|v3"] = "rule.eic-answer." + _name + ".v3.json"


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def test_core_v99_admits_exactly_the_new_members_and_the_seven_successors() -> None:
    before = _read(CONTENT / "package.core-calculations.v98.json")
    after = _read(CONTENT / "package.core-calculations.v99.json")
    old = {row["id"]: row for row in before["members"]}
    expected = dict(old)
    for rule, (v_old, v_new) in SUCCESSORS.items():
        assert old[rule]["version"] == v_old and old[rule]["schema"] == "rule-artifact.v14"
        expected[rule] = {**old[rule], "version": v_new}
    for citizen, schema, role in NEW:
        assert citizen not in old
        expected[citizen] = {"id": citizen, "version": "v1", "schema": schema, "role": role}
    assert {row["id"]: row for row in after["members"]} == expected
    assert len(after["members"]) == len(before["members"]) + len(NEW)
    old_entries = {(row["id"], row["version"]) for row in before["entrypoints"]}
    new_entries = {(row["id"], row["version"]) for row in after["entrypoints"]}
    assert old_entries <= new_entries
    # the bundle and the two questions are entrypoints; the rules are not
    assert new_entries - old_entries == {(BUNDLE, "v1"), (QUESTIONS[0], "v1"), (QUESTIONS[1], "v1")}
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v99")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_the_published_successors_replace_only_the_seven_rules() -> None:
    """No other v98 member pins a replaced rule version."""
    package = _read(CONTENT / "package.core-calculations.v98.json")
    targets = {(rule, v_old) for rule, (v_old, _) in SUCCESSORS.items()}
    found: list[tuple[Any, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if (node.get("id"), node.get("version")) in targets:
                found.append((node["id"], node["version"]))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for path in CONTENT.glob("rule.*.json"):
        body = _read(path)
        if (body.get("id") not in SUCCESSORS and isinstance(body, dict)
                and any(m["id"] == body.get("id") and m["version"] == body.get("version") for m in package["members"])):
            walk({k: v for k, v in body.items() if k != "id"})
    assert found == []


def test_the_new_answer_rule_reads_the_new_answer_and_the_successors_read_it() -> None:
    answer = _read(CONTENT / FILES[ANSWER_RULE])
    assert answer["publishes"] == P + "eic.answer.not-married"
    assert P + "eic.not-married" in json.dumps(answer)
    gate_old, gate_new = _read(CONTENT / FILES[GATE_RULE + "|v2"]), _read(CONTENT / FILES[GATE_RULE + "|v3"])
    assert P + "eic.answer.not-married" in gate_new["requires"]
    assert P + "eic.answer.not-married" not in json.dumps(gate_old)
    klass_old, klass_new = _read(CONTENT / FILES[CLASS_RULE + "|v1"]), _read(CONTENT / FILES[CLASS_RULE + "|v2"])
    assert P + "eic.column-count" in klass_new["requires"] and P + "eic.column-count" not in klass_old["requires"]
    pairs = [(klass_old, klass_new), (gate_old, gate_new)]
    for rule in STEP4_RULES:
        old, new = _read(CONTENT / FILES[rule + "|v2"]), _read(CONTENT / FILES[rule + "|v3"])
        assert old["publishes"] == new["publishes"] and old["version"] == "v2" and new["version"] == "v3"
        # each reads the not-married answer, and only that: the other requires and pins are v2's
        assert new["requires"] == [*old["requires"], P + "eic.answer.not-married"]
        assert [p["id"] for p in new["pins"]] == [*(p["id"] for p in old["pins"]), P + "eic.answer.not-married"]
        assert P + "eic.answer.not-married" not in json.dumps(old)
        pairs.append((old, new))
    for old, new in pairs:
        skip = ("version", "value", "notes", "requires", "pins", "blocked")
        assert {k: v for k, v in new.items() if k not in skip} == {k: v for k, v in old.items() if k not in skip}


def test_registry_v97_is_add_only() -> None:
    before = _read(CONTENT / "published-packages.v96.json")
    after = _read(CONTENT / "published-packages.v97.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            files = {(c, "v1"): FILES[c] for c, _, _ in NEW}
            files |= {(r, v): FILES[f"{r}|{v}"] for r, (_, v) in SUCCESSORS.items()}
            expected = {key: {"id": key[0], "version": key[1], "checksum": citizen_checksum(_read(CONTENT / name))}
                        for key, name in files.items()}
            assert added == expected
        else:
            package = _read(CONTENT / "package.core-calculations.v99.json")
            assert added == {(CORE, "v99"): {"id": CORE, "version": "v99", "checksum": package["package_checksum"]}}


def test_release_v97_differs_from_v96_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v96.json")
    new = _read(RELEASES / f"{STEM}.v97.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v97.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v97", "package_registry_sha256": digest}


def test_v99_loader_entries_carry_v98_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v99")] == declarations[(CORE, "v98")]
    assert covered_flag_refusal_map(CORE, "v99") == covered_flag_refusal_map(CORE, "v98")
    assert covered_flag_refusal_map(CORE, "v99")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked,
                   unconfirmed_family_names_closure_question):
        assert switch(CORE, "v99") == switch(CORE, "v98") is True


def test_the_replaced_rule_versions_are_still_published_and_unchanged() -> None:
    registry = _index(_read(CONTENT / "published-packages.v97.json")["citizens"])
    for rule, (v_old, _) in SUCCESSORS.items():
        key, name = (rule, v_old), FILES[f"{rule}|{v_old}"]
        assert registry[key]["checksum"] == citizen_checksum(_read(CONTENT / name))
