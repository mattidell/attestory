"""Fast publication checks for core v101, registry v99 and release v99 (eic-child-answers Track 1).

v101 admits exactly twenty-six input questions against v100, one for each
per-member answer of the four rosters that v100 never asks, each also an
entrypoint, and changes nothing else in the package. Each names an existing
fact type of its published roster or tie-breaker bundle that no v100 question
names, carries the wording track1_design.py gives it, and asks the thing the
fact's polarity says.
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-child-answers-evidence"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
P = "tax.us.2025."
FACTS = (
    *(P + f"eic.child.{n}" for n in ("age", "residency", "joint-return", "ssn")),
    *(P + f"dtb.child.{n}" for n in ("another-could-claim", "multiple-other-claimants", "filer-is-parent",
                                     "other-is-parent", "form-8332-released", "more-nights-with-filer", "same-nights",
                                     "filer-agi-higher", "same-agi", "other-will-claim")),
    *(P + f"ctc.child.{n}" for n in ("under-17", "lived-with-you", "no-over-half-support", "citizen-or-resident")),
    P + "odc.child.tin",
    *(P + f"odc.dependent.{n}" for n in ("relationship", "not-qualifying-child", "gross-income-under-limit",
                                         "over-half-support", "tin", "citizen-or-resident", "not-joint-return")),
)
QUESTIONS = {P + "input-question." + fact.removeprefix(P).replace(".", "-"): fact for fact in FACTS}


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _file(question: str) -> Path:
    return CONTENT / (question.removeprefix(P) + ".v1.json")


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    indexed = {(row["id"], row["version"]): row for row in rows}
    assert len(indexed) == len(rows)
    return indexed


def _design() -> Any:
    return evidence_loader.load(EVIDENCE / "track1_design.py", "eicc_t1_package_design")


def test_core_v101_admits_exactly_the_new_questions() -> None:
    assert len(QUESTIONS) == 26
    before = _read(CONTENT / "package.core-calculations.v100.json")
    after = _read(CONTENT / "package.core-calculations.v101.json")
    old = {row["id"]: row for row in before["members"]}
    expected = dict(old)
    for question in QUESTIONS:
        assert question not in old
        expected[question] = {"id": question, "version": "v1", "schema": "input-question.v1", "role": "input-question"}
    assert {row["id"]: row for row in after["members"]} == expected
    assert len(after["members"]) == len(before["members"]) + len(QUESTIONS)
    old_entries = {(row["id"], row["version"]) for row in before["entrypoints"]}
    new_entries = {(row["id"], row["version"]) for row in after["entrypoints"]}
    assert old_entries <= new_entries
    assert new_entries - old_entries == {(q, "v1") for q in QUESTIONS}
    skip = {"version", "members", "entrypoints", "package_checksum"}
    assert {k: v for k, v in after.items() if k not in skip} == {k: v for k, v in before.items() if k not in skip}
    assert (after["id"], after["version"]) == (CORE, "v101")
    assert after["package_checksum"] == package_instance_checksum(after)


def test_each_question_names_a_declared_member_fact_no_v100_question_names() -> None:
    package = _read(CONTENT / "package.core-calculations.v100.json")
    members = {(m["id"], m["version"]) for m in package["members"]}
    pins = {(m["id"], m["version"]) for m in package["members"] if m["role"] == "input-question"}
    asked = set()
    for path in CONTENT.glob("input-question.*.json"):
        body = _read(path)
        if (body["id"], body["version"]) in pins:
            asked.add(body["fact_type"]["id"])
    design = _design()
    assert set(design.QUESTIONS) == set(FACTS)
    for question, fact in QUESTIONS.items():
        bundle_id = design.BUNDLES[fact]
        assert (bundle_id, "v1") in members
        bundle = next(_read(p) for p in CONTENT.glob("*.bundle.json") if _read(p).get("id") == bundle_id)
        declared = {ft["id"]: ft for ft in bundle["fact_types"]}
        assert fact in declared and fact not in asked
        # Each is individuated on a roster member (a child or a dependent), so the page names that member.
        assert [k["name"] for k in declared[fact]["identity_keys"] if k["kind"] == "entity"] in (["child"], ["dependent"])
        body = _read(_file(question))
        assert body == {"fact_type": {"id": fact, "version": "v1"}, "id": question,
                        "question": design.QUESTIONS[fact], "schema": "input-question.v1", "version": "v1"}
        assert design.SOURCES[fact]


def test_each_question_says_what_yes_and_no_mean_and_its_polarity_follows_the_fact() -> None:
    design = _design()
    absent = {fact for fact in FACTS if fact.rsplit(".", 1)[1].startswith(("no-", "not-"))}
    assert absent == {P + "ctc.child.no-over-half-support", P + "odc.dependent.not-qualifying-child",
                      P + "odc.dependent.not-joint-return"}
    for question, fact in QUESTIONS.items():
        text = _read(_file(question))["question"]
        assert "Answer yes" in text and "Answer no" in text, fact
        assert design.POLARITY[fact] == ("abs" if fact in absent else "pos"), fact
    # A fact stated as an absence is asked about the thing itself, so the filer's yes records the fact's no.
    texts = {fact: _read(_file(q))["question"] for q, fact in QUESTIONS.items()}
    assert texts[P + "ctc.child.no-over-half-support"].startswith("Did this child provide over half of their own support")
    assert texts[P + "odc.dependent.not-qualifying-child"].startswith("Was this person a qualifying child of any taxpayer")
    assert texts[P + "odc.dependent.not-joint-return"].startswith("Did this person file a joint return for 2025")


def test_registry_v99_is_add_only() -> None:
    before = _read(CONTENT / "published-packages.v98.json")
    after = _read(CONTENT / "published-packages.v99.json")
    for kind in ("citizens", "packages"):
        old, new = _index(before[kind]), _index(after[kind])
        assert all(new[key] == row for key, row in old.items())
        added = {key: row for key, row in new.items() if key not in old}
        if kind == "citizens":
            assert added == {(q, "v1"): {"id": q, "version": "v1", "checksum": citizen_checksum(_read(_file(q)))}
                             for q in QUESTIONS}
        else:
            package = _read(CONTENT / "package.core-calculations.v101.json")
            assert added == {(CORE, "v101"): {"id": CORE, "version": "v101", "checksum": package["package_checksum"]}}


def test_release_v99_differs_from_v98_only_in_version_and_registry_digest() -> None:
    old = _read(RELEASES / f"{STEM}.v98.json")
    new = _read(RELEASES / f"{STEM}.v99.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v99.json").read_bytes()).hexdigest()
    assert new == {**old, "version": "v99", "package_registry_sha256": digest}


def test_v101_loader_entries_carry_v100_unchanged() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v101")] == declarations[(CORE, "v100")]
    assert covered_flag_refusal_map(CORE, "v101") == covered_flag_refusal_map(CORE, "v100")
    assert covered_flag_refusal_map(CORE, "v101")
    for switch in (selection_collect_satisfied_by_family, later_any_arm_refs_while_count_blocked,
                   unconfirmed_family_names_closure_question):
        assert switch(CORE, "v101") == switch(CORE, "v100") is True
