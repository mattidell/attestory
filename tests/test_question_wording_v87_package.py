"""Core v87 is the decided question wording, published as successors only.

Static checks on the seven successor citizens, the package, registry,
release and loader entries. The coordinator runs live in
tests/test_question_wording_v87.py.

Each successor is rebuilt from the evidence prototype
(``prototype.artifacts``) and compared byte for byte. The prototype is
loaded under a name no other module uses, and no attribute of it is
assigned.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    selection_collect_satisfied_by_family,
)
from tests import evidence_loader

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."

# (member id, v86 version, v87 version, successor file, v86 file)
EDITS = (
    (P + "closure-mapping.f1099b-covered-w-st-adjustment", "v3", "v4",
     "closure-mapping.f1099b-covered-w-st-adjustment.v4.json",
     "closure-mapping.f1099b-covered-w-st-adjustment.v3.json"),
    (P + "closure-mapping.f1099b-covered-w-lt-adjustment", "v3", "v4",
     "closure-mapping.f1099b-covered-w-lt-adjustment.v4.json",
     "closure-mapping.f1099b-covered-w-lt-adjustment.v3.json"),
    (P + "input-question.exception1-only-box2a-capital-gains", "v2", "v3",
     "input-question.exception1-only-box2a-capital-gains.v3.json",
     "input-question.exception1-only-box2a-capital-gains.v2.json"),
    (P + "input-question.sli-scope-not-claimed-as-dependent", "v1", "v2",
     "input-question.sli-scope-not-claimed-as-dependent.v2.json",
     "input-question.sli-scope-not-claimed-as-dependent.v1.json"),
    (P + "exception1.vocabulary", "v1", "v2", "exception1.bundle.v2.json", "exception1.bundle.json"),
    (P + "sli-scope.vocabulary", "v1", "v2", "sli-scope.bundle.v2.json", "sli-scope.bundle.json"),
    (P + "core_calculations.vocabulary", "v2", "v3",
     "core_calculations.bundle.v3.json", "core_calculations.bundle.v2.json"),
)

WASH = (
    "Have you recorded the wash-sale loss adjustment amount of every covered {term} sale "
    "with a wash-sale loss adjustment (a loss disallowed because you bought the same "
    "investment within 30 days before or after the sale) on every Form 1099-B you or "
    "your spouse received for 2025?"
)
ONLY_BOX2A = (
    "Is it true that you had no capital gains in 2025 other than capital gain "
    "distributions in box 2a of Form 1099-DIV, and that you had no sale in 2025 of "
    "stock, bonds, funds or other property that you must report on Form 8949 or "
    "Schedule D (even one with no gain or loss)? Sales inside an IRA or 401(k) and "
    "losses on personal items do not count."
)
SLI = (
    "Is someone else claiming you (or your spouse, on a joint return) as a dependent "
    "on their 2025 return?"
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    module = evidence_loader.load(EVIDENCE / "prototype.py", "qw_t1_v87_package_prototype")
    assert module.FROM == {"package": "v86", "registry": "v84", "release": "v84"}
    assert module.TO == {"package": "v87", "registry": "v85", "release": "v85"}
    return module


def test_successors_are_the_prototype_byte_for_byte(prototype: ModuleType) -> None:
    rows = prototype.artifacts(True)
    assert [name for name, _body in rows] == [edit[3] for edit in EDITS]
    for name, body in rows:
        assert (CONTENT / name).read_bytes() == (json.dumps(body, indent=2) + "\n").encode("utf-8"), name


def test_successor_questions_carry_the_decided_words() -> None:
    st = _load_json(CONTENT / "closure-mapping.f1099b-covered-w-st-adjustment.v4.json")
    lt = _load_json(CONTENT / "closure-mapping.f1099b-covered-w-lt-adjustment.v4.json")
    only = _load_json(CONTENT / "input-question.exception1-only-box2a-capital-gains.v3.json")
    sli = _load_json(CONTENT / "input-question.sli-scope-not-claimed-as-dependent.v2.json")
    assert st["closure_question"] == WASH.format(term="short-term")
    assert lt["closure_question"] == WASH.format(term="long-term")
    assert only["question"] == ONLY_BOX2A
    assert sli["question"] == SLI


def _title(name: str, fact_id: str) -> str:
    hits = [f["title"] for f in _load_json(CONTENT / name)["fact_types"] if f["id"] == fact_id]
    assert len(hits) == 1, fact_id
    return str(hits[0])


def test_successor_titles_carry_the_repaired_scope() -> None:
    """Review F1: the Exception 1 title has the question's scope. Review F4: blindness is dated."""
    title = _title("exception1.bundle.v2.json", P + "exception1.only-box2a-capital-gains")
    assert "no 2025 sale of stock, bonds, funds or other property that must be reported on Form 8949 or Schedule D" in title
    assert "sales inside an IRA or 401(k) and losses on personal-use property do not count" in title
    for fact in ("taxpayer-blind", "spouse-blind"):
        assert "or as of December 31, 2025 could not see better than 20/200" in _title(
            "core_calculations.bundle.v3.json", P + fact)


def test_each_successor_differs_from_its_predecessor_only_in_words_and_version() -> None:
    """Fact type versions, ids, domains and bindings do not change; only text and the citizen version."""
    for member, old, new, name, previous in EDITS:
        before = _load_json(CONTENT / previous)
        after = _load_json(CONTENT / name)
        assert (before["id"], before["version"]) == (member, old)
        assert (after["id"], after["version"]) == (member, new)
        if "fact_types" in after:
            assert [f["id"] for f in after["fact_types"]] == [f["id"] for f in before["fact_types"]]
            for left, right in zip(before["fact_types"], after["fact_types"], strict=True):
                assert {k: v for k, v in left.items() if k != "title"} == {
                    k: v for k, v in right.items() if k != "title"}, right["id"]
            skip: tuple[str, ...] = ("version", "fact_types")
        else:
            skip = ("version", "closure_question", "question")
        assert {k: v for k, v in after.items() if k not in skip} == {
            k: v for k, v in before.items() if k not in skip}, name


def test_core_v87_is_v86_with_exactly_the_seven_member_edits() -> None:
    v86 = _load_json(CONTENT / "package.core-calculations.v86.json")
    v87 = _load_json(CONTENT / "package.core-calculations.v87.json")
    assert (v87["id"], v87["version"]) == (CORE, "v87")
    assert v87["schema"] == v86["schema"]
    assert v87["admitted_schemas"] == v86["admitted_schemas"]
    skip = ("version", "package_checksum", "members", "entrypoints")
    assert {k: v for k, v in v87.items() if k not in skip} == {k: v for k, v in v86.items() if k not in skip}
    members = {m["id"]: m for m in v86["members"]}
    entrypoints = {(e["id"], e["version"]) for e in v86["entrypoints"]}
    for member, old, new, _name, _previous in EDITS:
        assert members[member]["version"] == old
        members[member] = {**members[member], "version": new}
        if (member, old) in entrypoints:
            entrypoints.remove((member, old))
            entrypoints.add((member, new))
    after = {m["id"]: m for m in v87["members"]}
    assert after == members
    assert len(v87["members"]) == len(v86["members"])
    assert {(e["id"], e["version"]) for e in v87["entrypoints"]} == entrypoints
    changed = {m for m, entry in after.items() if entry != {x["id"]: x for x in v86["members"]}[m]}
    assert changed == {edit[0] for edit in EDITS}
    assert v87["package_checksum"] == package_instance_checksum(v87)


def test_registry_v85_only_adds_v87_and_the_seven_successors() -> None:
    v84 = _load_json(CONTENT / "published-packages.v84.json")
    v85 = _load_json(CONTENT / "published-packages.v85.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v84[key]}
        after = {(e["id"], e["version"]): e for e in v85[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    packages = {(e["id"], e["version"]): e["checksum"] for e in v85["packages"]}
    for identity in {(e["id"], e["version"]) for e in v84["packages"]}:
        del packages[identity]
    v87 = _load_json(CONTENT / "package.core-calculations.v87.json")
    assert packages == {(CORE, "v87"): v87["package_checksum"]}
    added = {(e["id"], e["version"]): e["checksum"] for e in v85["citizens"]}
    for identity in {(e["id"], e["version"]) for e in v84["citizens"]}:
        del added[identity]
    assert added == {
        (member, new): citizen_checksum(_load_json(CONTENT / name))
        for member, _old, new, name, _previous in EDITS
    }


def test_release_v85_pins_registry_v85() -> None:
    release = _load_json(RELEASES / f"{RELEASE_STEM}.v85.json")
    previous = _load_json(RELEASES / f"{RELEASE_STEM}.v84.json")
    assert release["version"] == "v85"
    registry = (CONTENT / "published-packages.v85.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()
    assert {k: v for k, v in release.items() if k not in ("version", "package_registry_sha256")} == {
        k: v for k, v in previous.items() if k not in ("version", "package_registry_sha256")}


def test_core_v87_carries_v86_loader_entries() -> None:
    declarations = domain_package_companion_declarations()
    v86, v87 = declarations[(CORE, "v86")], declarations[(CORE, "v87")]
    assert v87["presence_pairs"] == v86["presence_pairs"]
    assert v87["value_domains"] == v86["value_domains"]
    assert covered_flag_refusal_map(CORE, "v87") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v87") == covered_flag_refusal_map(CORE, "v86")
    assert selection_collect_satisfied_by_family(CORE, "v87") is True
    assert selection_collect_satisfied_by_family(CORE, "v86") is True


def test_core_v86_and_earlier_are_unchanged() -> None:
    """v86 and earlier keep the predecessor members, and their published checksums still hold."""
    registry = _load_json(CONTENT / "published-packages.v85.json")
    packages = {(e["id"], e["version"]): e["checksum"] for e in registry["packages"]}
    citizens = {(e["id"], e["version"]): e["checksum"] for e in registry["citizens"]}
    for version in ("v86", "v85", "v84", "v83"):
        package = _load_json(CONTENT / f"package.core-calculations.{version}.json")
        assert packages[(CORE, version)] == package_instance_checksum(package) == package["package_checksum"]
    v86 = {m["id"]: m["version"] for m in _load_json(CONTENT / "package.core-calculations.v86.json")["members"]}
    for member, old, new, _name, previous in EDITS:
        assert v86[member] == old
        assert citizens[(member, old)] == citizen_checksum(_load_json(CONTENT / previous))
        assert (member, new) not in {
            (e["id"], e["version"]) for e in _load_json(CONTENT / "published-packages.v84.json")["citizens"]}
