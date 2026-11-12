"""Core v88 is the decided age and blindness content, published as successors only.

Static checks: byte identity with the prototype, the member and binding edits,
registry v86 add-only, release v86, and the loader entries. The coordinator
runs live in tests/test_age_blindness_v88.py.

The prototype is loaded under a name no other module uses, and no attribute
of it is assigned.
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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/age-blindness-asked-evidence"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."

# (member id, v87 version, v88 version)
BUMPS = (
    (P + "rule.dependents-worksheet-line-1", "v1", "v2"),
    (P + "rule.schedule1a-part-v-line-36b", "v1", "v2"),
    (P + "core_calculations.vocabulary", "v3", "v4"),
)
QUESTION_SLUGS = (
    "taxpayer-over-65",
    "taxpayer-blind",
    "spouse-over-65",
    "spouse-blind",
    "standard-deduction.spouse-separate-condition",
)
REQUIRED_SYMBOLS = (
    "taxpayer_over_65",
    "taxpayer_blind",
    "spouse_over_65",
    "spouse_blind",
)
COND_SYMBOL = "spouse_separate_condition"
COND_FACT = P + "standard-deduction.spouse-separate-condition"

TAXPAYER_AGE = (
    "Were you born before January 2, 1961? A person reaches age 65 on the day before "
    "their 65th birthday, so a birthday of January 1, 1961 counts and January 2, 1961 "
    "does not. If this return is for someone who died in 2025 before reaching age 65, "
    "answer no."
)
TAXPAYER_BLIND = (
    "Were you totally blind on December 31, 2025, or do you have a statement certified "
    "by your eye doctor (ophthalmologist or optometrist) that you can't see better than "
    "20/200 in your better eye with glasses or contact lenses, or that your field of "
    "vision is 20 degrees or less?"
)
SPOUSE_AGE = (
    "Was your spouse born before January 2, 1961? A person reaches age 65 on the day "
    "before their 65th birthday. If your spouse died in 2025 before reaching age 65, "
    "answer no."
)
SPOUSE_BLIND = (
    "Was your spouse totally blind on December 31, 2025, or does your spouse have a "
    "statement certified by an eye doctor (ophthalmologist or optometrist) that they "
    "can't see better than 20/200 in the better eye with glasses or contact lenses, or "
    "that their field of vision is 20 degrees or less?"
)
# Decision 10.
COND_QUESTION = (
    "Is it true that your spouse had no income, isn't filing a return, and can't be claimed "
    "as a dependent on another person's return?"
)
SENTENCES = {
    "taxpayer-over-65": TAXPAYER_AGE,
    "taxpayer-blind": TAXPAYER_BLIND,
    "spouse-over-65": SPOUSE_AGE,
    "spouse-blind": SPOUSE_BLIND,
    "standard-deduction.spouse-separate-condition": COND_QUESTION,
}
COND_TITLE = (
    "The spouse had no income, isn't filing a return, and can't be claimed as a dependent "
    "on another person's return."
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _bytes(body: Any) -> bytes:
    return (json.dumps(body, indent=2) + "\n").encode("utf-8")


def _bindings(package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["symbol"]): row for row in package["input_bindings"]}


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    return evidence_loader.load(EVIDENCE / "prototype.py", "aba_t1_v88_package_prototype")


def test_successors_are_the_prototype_byte_for_byte(prototype: ModuleType) -> None:
    for slug in QUESTION_SLUGS:
        name = f"input-question.{slug}.v1.json"
        assert (CONTENT / name).read_bytes() == _bytes(prototype.question(slug)), name
    assert (CONTENT / "rule.dependents-worksheet-line-1.v2.json").read_bytes() == _bytes(
        prototype.line1(CONTENT))
    assert (CONTENT / "rule.schedule1a-part-v-line-36b.v2.json").read_bytes() == _bytes(
        prototype.line36b(CONTENT))
    bundle, titles = prototype.vocabulary_v4(CONTENT)
    assert (CONTENT / "core_calculations.bundle.v4.json").read_bytes() == _bytes(bundle)
    published = {
        str(fact["id"]): str(fact["title"])
        for fact in _load_json(CONTENT / "core_calculations.bundle.v3.json")["fact_types"]
        if fact["id"] in (P + "spouse-over-65", P + "spouse-blind")
    }
    assert titles == published


def test_questions_carry_the_decided_sentences() -> None:
    for slug, sentence in SENTENCES.items():
        body = _load_json(CONTENT / f"input-question.{slug}.v1.json")
        assert body["question"] == sentence
        assert (body["id"], body["version"], body["schema"]) == (
            P + "input-question." + slug, "v1", "input-question.v1")
    bundle = _load_json(CONTENT / "core_calculations.bundle.v4.json")
    facts = [fact for fact in bundle["fact_types"] if fact["id"] == COND_FACT]
    assert len(facts) == 1
    assert facts[0]["schema"] == "fact-type.v2"
    assert facts[0]["title"] == COND_TITLE
    assert facts[0]["version"] == "v1"
    names = sorted(path.name for path in CONTENT.glob("*spouse-separate-condition*"))
    assert names == ["input-question.standard-deduction.spouse-separate-condition.v1.json"]


def test_line_successors_ask_what_decision_9_decided() -> None:
    line1 = _load_json(CONTENT / "rule.dependents-worksheet-line-1.v2.json")
    previous = _load_json(CONTENT / "rule.dependents-worksheet-line-1.json")
    assert (line1["id"], line1["version"]) == (P + "rule.dependents-worksheet-line-1", "v2")
    assert previous["version"] == "v1"
    assert line1["requires"] == ["filing_status"]
    assert COND_SYMBOL in json.dumps(line1["value"])
    assert COND_SYMBOL not in json.dumps(previous)
    line36b = _load_json(CONTENT / "rule.schedule1a-part-v-line-36b.v2.json")
    assert (line36b["id"], line36b["version"]) == (P + "rule.schedule1a-part-v-line-36b", "v2")
    assert line36b["requires"] == ["filing_status", P + "schedule1a.line35-per-person-amount"]
    assert line36b["value"]["op"] == "choose"


def test_core_v88_is_v87_with_exactly_the_eight_member_edits() -> None:
    v87 = _load_json(CONTENT / "package.core-calculations.v87.json")
    v88 = _load_json(CONTENT / "package.core-calculations.v88.json")
    assert (v88["id"], v88["version"], v88["schema"]) == (CORE, "v88", v87["schema"])
    skip = ("version", "package_checksum", "members", "entrypoints", "input_bindings")
    assert {k: v for k, v in v88.items() if k not in skip} == {k: v for k, v in v87.items() if k not in skip}
    members = {m["id"]: m for m in v87["members"]}
    entrypoints = {(e["id"], e["version"]) for e in v87["entrypoints"]}
    for member, old, new in BUMPS:
        assert members[member]["version"] == old
        members[member] = {**members[member], "version": new}
    for slug in QUESTION_SLUGS:
        member_id = P + "input-question." + slug
        assert member_id not in members
        members[member_id] = {
            "id": member_id, "version": "v1", "schema": "input-question.v1", "role": "input-question",
        }
        entrypoints.add((member_id, "v1"))
    after = {m["id"]: m for m in v88["members"]}
    assert after == members
    assert {(e["id"], e["version"]) for e in v88["entrypoints"]} == entrypoints
    before = {m["id"]: m for m in v87["members"]}
    changed = {member for member, body in after.items() if body != before.get(member)}
    assert changed == {member for member, _old, _new in BUMPS} | {
        P + "input-question." + slug for slug in QUESTION_SLUGS}
    bindings = _bindings(v88)
    previous_bindings = _bindings(v87)
    for symbol in REQUIRED_SYMBOLS:
        assert {**previous_bindings[symbol], "mode": "required"} == bindings[symbol]
        assert previous_bindings[symbol]["mode"] == "optional_default"
    assert bindings[COND_SYMBOL] == {
        "fact_type": {"id": COND_FACT, "version": "v1"},
        "mode": "required",
        "symbol": COND_SYMBOL,
    }
    assert COND_SYMBOL not in previous_bindings
    untouched = set(previous_bindings) - set(REQUIRED_SYMBOLS)
    assert {symbol: bindings[symbol] for symbol in untouched} == {
        symbol: previous_bindings[symbol] for symbol in untouched}
    assert v88["package_checksum"] == package_instance_checksum(v88)


def test_registry_v86_only_adds_v88_and_the_eight_successors() -> None:
    v85 = _load_json(CONTENT / "published-packages.v85.json")
    v86 = _load_json(CONTENT / "published-packages.v86.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v85[key]}
        after = {(e["id"], e["version"]): e for e in v86[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    packages = {(e["id"], e["version"]): e["checksum"] for e in v86["packages"]}
    for identity in {(e["id"], e["version"]) for e in v85["packages"]}:
        del packages[identity]
    v88 = _load_json(CONTENT / "package.core-calculations.v88.json")
    assert packages == {(CORE, "v88"): v88["package_checksum"]}
    added = {(e["id"], e["version"]): e["checksum"] for e in v86["citizens"]}
    for identity in {(e["id"], e["version"]) for e in v85["citizens"]}:
        del added[identity]
    expected = {
        (P + "input-question." + slug, "v1"): citizen_checksum(
            _load_json(CONTENT / f"input-question.{slug}.v1.json"))
        for slug in QUESTION_SLUGS
    }
    expected[(P + "rule.dependents-worksheet-line-1", "v2")] = citizen_checksum(
        _load_json(CONTENT / "rule.dependents-worksheet-line-1.v2.json"))
    expected[(P + "rule.schedule1a-part-v-line-36b", "v2")] = citizen_checksum(
        _load_json(CONTENT / "rule.schedule1a-part-v-line-36b.v2.json"))
    expected[(P + "core_calculations.vocabulary", "v4")] = citizen_checksum(
        _load_json(CONTENT / "core_calculations.bundle.v4.json"))
    assert added == expected


def test_release_v86_pins_registry_v86() -> None:
    release = _load_json(RELEASES / f"{RELEASE_STEM}.v86.json")
    previous = _load_json(RELEASES / f"{RELEASE_STEM}.v85.json")
    assert release["version"] == "v86"
    registry = (CONTENT / "published-packages.v86.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()
    assert {k: v for k, v in release.items() if k not in ("version", "package_registry_sha256")} == {
        k: v for k, v in previous.items() if k not in ("version", "package_registry_sha256")}


def test_core_v88_carries_v87_loader_entries() -> None:
    declarations = domain_package_companion_declarations()
    v87, v88 = declarations[(CORE, "v87")], declarations[(CORE, "v88")]
    assert v88["presence_pairs"] == v87["presence_pairs"]
    assert v88["value_domains"] == v87["value_domains"]
    assert covered_flag_refusal_map(CORE, "v88") == COVERED_FLAG_REFUSAL_OBJECTS
    assert covered_flag_refusal_map(CORE, "v88") == covered_flag_refusal_map(CORE, "v87")
    assert selection_collect_satisfied_by_family(CORE, "v88") is True
    assert selection_collect_satisfied_by_family(CORE, "v87") is True


def test_core_v87_and_earlier_are_unchanged() -> None:
    """v87 and earlier keep their published checksums, and v86 copies those registry entries."""
    current = _load_json(CONTENT / "published-packages.v86.json")
    previous = _load_json(CONTENT / "published-packages.v85.json")
    current_packages = {(e["id"], e["version"]): e["checksum"] for e in current["packages"]}
    previous_packages = {(e["id"], e["version"]): e["checksum"] for e in previous["packages"]}
    current_citizens = {(e["id"], e["version"]): e["checksum"] for e in current["citizens"]}
    previous_citizens = {(e["id"], e["version"]): e["checksum"] for e in previous["citizens"]}
    for version in ("v87", "v86", "v85", "v84", "v83"):
        package = _load_json(CONTENT / f"package.core-calculations.{version}.json")
        checksum = package_instance_checksum(package)
        assert checksum == package["package_checksum"]
        assert current_packages[(CORE, version)] == checksum
        assert previous_packages[(CORE, version)] == checksum
    v87_members = {
        m["id"]: m["version"] for m in _load_json(CONTENT / "package.core-calculations.v87.json")["members"]}
    for member, old, new in BUMPS:
        assert v87_members[member] == old
        assert (member, new) not in previous_citizens
        assert current_citizens[(member, old)] == previous_citizens[(member, old)]
    for slug in QUESTION_SLUGS:
        assert (P + "input-question." + slug, "v1") not in previous_citizens
        assert P + "input-question." + slug not in v87_members
