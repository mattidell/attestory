"""Core v82 is the final scratch v82 of the sale family audit, published as successors only.

Static checks on the published package, registry, release and loader entries,
on the words of each new or reworded input question, and the audit itself:
every field a sale record carries is read by a rule, or has a recorded reason
it cannot change the return, or is refused by an answer some rule reads. The
cases run through the coordinator in tests/test_sale_family_audit_v82.py.

The successor bodies are rebuilt from the evidence prototype
(``prototype.artifacts`` with every switch on), which reads only the published
predecessors, and compared byte for byte. The audit is the evidence
``tables.py``. Both are loaded under names no other module uses, and no
attribute of either is assigned.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from packages.derivation.package_validation import citizen_checksum
from packages.tax.loader import (
    COVERED_FLAG_REFUSAL_OBJECTS,
    code_b_scalar_presence_pairs,
    covered_flag_refusal_map,
    covered_scalar_presence_pairs,
    domain_package_companion_declarations,
)
from tests import evidence_loader

REPO = Path(__file__).resolve().parents[1]
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence"
CORE = "tax.us.2025.package.core-calculations"
P = "tax.us.2025."


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _module(name: str, path: Path) -> ModuleType:
    """An evidence module under its own name. Nothing on it is assigned."""
    return evidence_loader.load(path, name)


@pytest.fixture(scope="module")
def prototype() -> ModuleType:
    module = _module("sale_family_audit_v82_package_prototype", EVIDENCE / "prototype.py")
    assert module.REPAIRS == ("statement_box4", "statement_box7", "field_words", "exception1_words", "row_needs_sale",
                              "line7b_activity", "field_truth")
    assert module.FROM == {"package": "v81", "registry": "v79", "release": "v79"}
    assert module.TO == {"package": "v82", "registry": "v80", "release": "v80"}
    return module


@pytest.fixture(scope="module")
def bodies(prototype: ModuleType) -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = prototype.artifacts(set(prototype.SWITCHES))
    return out


@pytest.fixture(scope="module")
def tables() -> ModuleType:
    return _module("sale_family_audit_v82_package_tables", EVIDENCE / "tables.py")


# ---- the package, registry, release and loader ------------------------------------


def test_every_successor_is_the_prototype_byte_for_byte(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    assert len(bodies) == 35
    for name, body in bodies:
        assert (CONTENT / name).read_bytes() == (json.dumps(body, indent=2) + "\n").encode("utf-8"), name


def test_core_v82_is_v81_with_exactly_the_prototype_member_edits(
        prototype: ModuleType, bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v81 = _load_json(CONTENT / "package.core-calculations.v81.json")
    v82 = _load_json(CONTENT / "package.core-calculations.v82.json")
    assert (v82["id"], v82["version"]) == (CORE, "v82")
    assert {k: v for k, v in v82.items() if k not in ("version", "package_checksum", "members", "entrypoints")} == {
        k: v for k, v in v81.items() if k not in ("version", "package_checksum", "members", "entrypoints")}
    members = {m["id"]: m for m in v81["members"]}
    entrypoints = {(e["id"], e["version"]) for e in v81["entrypoints"]}
    adds = replaces = 0
    for _name, body in bodies:
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": prototype.role(body)}
        old = members.get(body["id"])
        if old is None:
            adds += 1
            entrypoints.add((body["id"], body["version"]))
        else:
            replaces += 1
            assert old["version"] != body["version"]
            if (old["id"], old["version"]) in entrypoints:
                entrypoints.remove((old["id"], old["version"]))
                entrypoints.add((body["id"], body["version"]))
        members[body["id"]] = new
    assert (adds, replaces) == (5, 30)
    assert sorted(v82["members"], key=lambda m: m["id"]) == sorted(members.values(), key=lambda m: m["id"])
    assert {(e["id"], e["version"]) for e in v82["entrypoints"]} == entrypoints
    assert len(v82["entrypoints"]) == len(entrypoints)


def test_registry_v80_only_adds_v82_and_its_new_citizens(bodies: list[tuple[str, dict[str, Any]]]) -> None:
    v79 = _load_json(CONTENT / "published-packages.v79.json")
    v80 = _load_json(CONTENT / "published-packages.v80.json")
    for key in ("citizens", "packages"):
        before = {(e["id"], e["version"]): e for e in v79[key]}
        after = {(e["id"], e["version"]): e for e in v80[key]}
        for identity, entry in before.items():
            assert after[identity] == entry, identity
    packages = {(e["id"], e["version"]) for e in v80["packages"]} - {(e["id"], e["version"]) for e in v79["packages"]}
    assert packages == {(CORE, "v82")}
    added = {(e["id"], e["version"]): e["checksum"] for e in v80["citizens"]}
    for identity in {(e["id"], e["version"]) for e in v79["citizens"]}:
        del added[identity]
    assert added == {(body["id"], body["version"]): citizen_checksum(body) for _name, body in bodies}


def test_release_v80_pins_registry_v80() -> None:
    release = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v80.json")
    previous = _load_json(RELEASES / "demo.release.sli-worksheet-integration.2025.v79.json")
    assert release["version"] == "v80"
    registry = (CONTENT / "published-packages.v80.json").read_bytes()
    assert release["package_registry_sha256"] == hashlib.sha256(registry).hexdigest()
    assert {k: v for k, v in release.items() if k not in ("version", "package_registry_sha256")} == {
        k: v for k, v in previous.items() if k not in ("version", "package_registry_sha256")}


def test_core_v82_carries_v81s_loader_entries_and_the_covered_row_pairs(prototype: ModuleType) -> None:
    """Review F1: every covered and code W amount row requires its own sale, as the other kinds' rows do."""
    declarations = domain_package_companion_declarations()
    v81, v82 = declarations[(CORE, "v81")], declarations[(CORE, "v82")]
    pairs = covered_scalar_presence_pairs()
    assert pairs == prototype.presence_pairs(set(prototype.SWITCHES))
    assert len(pairs) == 10
    assert v82["presence_pairs"] == {**v81["presence_pairs"], **pairs}
    assert v82["value_domains"] == v81["value_domains"]
    for scalar, sale in pairs.items():
        assert scalar.startswith(sale + ".") and "covered" in sale
        assert scalar not in v81["presence_pairs"]
    assert code_b_scalar_presence_pairs().items() <= v82["presence_pairs"].items()
    assert covered_flag_refusal_map(CORE, "v82") == COVERED_FLAG_REFUSAL_OBJECTS == covered_flag_refusal_map(CORE, "v81")


# ---- Form 1040 line 7b (review F2) ---------------------------------------------------


def test_line_7b_is_checked_only_when_no_sale_is_recorded() -> None:
    """Line 7b v2 reads every sale count and covered proceeds subtotal line 16 v7 reads, and is inapplicable
    when any is above zero; the Schedule-D-required conclusion decides it only when no sale is recorded."""
    rule = _load_json(CONTENT / "rule.form1040-line7b.v2.json")
    v1 = _load_json(CONTENT / "rule.form1040-line7b.json")
    line16 = _load_json(CONTENT / "rule.form1040-line16.v7.json")
    assert _v82_pins()[rule["id"]] == "v2"
    conclusion, no_sale = rule["when"]["args"]
    assert rule["when"]["op"] == "all" and conclusion == v1["when"]
    assert no_sale["op"] == "not" and no_sale["value"]["op"] == "any"
    read = [arm["left"]["name"] for arm in no_sale["value"]["args"]]
    assert all(arm["op"] == "compare" and arm["cmp"] == "gt" and arm["right"] == 0 for arm in no_sale["value"]["args"])
    (route,) = line16["when"]["args"]
    activity = route["when"]["args"]
    assert read == [arm["left"]["name"] for arm in activity]
    assert set(read) <= set(rule["requires"]) and rule["blocked"]["missing"] == rule["requires"]
    assert (rule["value"], rule["publishes"]) == (v1["value"], v1["publishes"])
    field = _load_json(CONTENT / "form1040.line-7b.form-field.v3.json")
    assert _v82_pins()[field["id"]] == "v3"
    words = {k: v["explain"] for k, v in field["dispositions"].items()}
    assert words["published_value"].startswith("No sale is recorded and the checked Schedule-D-required conclusion is no")
    assert "you recorded a sale" in words["guard_inapplicable"]
    assert "whether you recorded any sale decides" in words["blocked"]


# ---- review F3: two field sentences true of their rules ---------------------------------


def test_the_line_16_and_line_7a_sentences_are_true_of_their_rules() -> None:
    """Line 16 v7 takes the Schedule D route for any recorded sale; line 7a v9 does not read Exception 1 beside one."""
    line16 = _load_json(CONTENT / "form1040.line-16.form-field.v3.json")["dispositions"]
    assert line16["guard_inapplicable"]["explain"].startswith("Line 16 is computed here only when you recorded a sale, ")
    assert "covered securities" not in line16["guard_inapplicable"]["explain"]
    line7a = _load_json(CONTENT / "form1040.line-7a.form-field.v2.json")["dispositions"]["blocked"]["explain"]
    assert line7a.startswith("Line 7a has no value yet. Whether you recorded any sale decides its route")
    assert "because Exception-1 authority" not in line7a
    for words in ("With a sale recorded", "Schedule D", "With none", "Exception 1 answers", "box 2a"):
        assert words in line7a, words


# ---- each new or reworded input question against its proposition --------------------

# The v1 sentence the four Exception 1 facts shared: its "yes" meant each fact's "no".
EXCEPTION1_V1 = ("Besides capital gain distributions in box 2a of Form 1099-DIV, did you have any other capital gain "
                 "or loss in 2025 (including any capital loss, any amount in Form 1099-DIV box 2b, 2c or 2d, or a gain "
                 "deferred through a qualified opportunity fund)?")
# Fact -> (the v2 question, the proposition in the fact's title that the question's "yes" asserts).
EXCEPTION1_V2 = {
    "exception1.only-box2a-capital-gains": (
        "Is it true that you had no capital gains in 2025 other than capital gain distributions in box 2a of Form "
        "1099-DIV (for example, no gain from selling stock, funds or other property)?",
        "whether the return's only capital gains are Form 1099-DIV box-2a capital-gain distributions"),
    "exception1.no-capital-losses": (
        "Is it true that you had no capital losses in 2025 (for example, no loss from selling stock, funds or other "
        "property)?",
        "whether the return has no capital losses"),
    "exception1.no-qof-deferral": (
        "Is it true that you did not defer any capital gain in 2025 by investing in a qualified opportunity fund?",
        "whether no capital gain is being deferred through a qualified opportunity fund"),
    "exception1.no-boxes-2b-2c-2d": (
        "Is it true that none of your 2025 Forms 1099-DIV or substitute statements shows an amount in box 2b, 2c "
        "or 2d?",
        "whether no Form 1099-DIV or substitute statement has an amount in box 2b, 2c, or 2d"),
}


def _fact(bundle: str, fact_id: str) -> dict[str, Any]:
    (fact,) = [f for f in _load_json(CONTENT / bundle)["fact_types"] if f["id"] == fact_id]
    found: dict[str, Any] = fact
    return found


def _v82_pins() -> dict[str, str]:
    return {m["id"]: m["version"] for m in _load_json(CONTENT / "package.core-calculations.v82.json")["members"]}


@pytest.mark.parametrize("fact", sorted(EXCEPTION1_V2))
def test_each_exception1_question_says_yes_when_its_fact_is_yes(prototype: ModuleType, fact: str) -> None:
    """Decision 2: a reply recorded literally is the fact's value."""
    text, proposition = EXCEPTION1_V2[fact]
    slug = fact.replace(".", "-", 1)
    v1 = _load_json(CONTENT / f"input-question.{slug}.v1.json")
    v2 = _load_json(CONTENT / f"input-question.{slug}.v2.json")
    assert v1["question"] == EXCEPTION1_V1
    assert v2["question"] == text == prototype.EXCEPTION1_QUESTIONS[fact]
    assert v2["id"] == v1["id"] == P + f"input-question.{slug}"
    assert v2["version"] == "v2" and v2["schema"] == v1["schema"] == "input-question.v1"
    fact_body = _fact("exception1.bundle.json", P + fact)
    assert v2["fact_type"] == v1["fact_type"] == {"id": P + fact, "version": fact_body["version"]}
    assert fact_body["value_schema"] == {"enum": ["yes", "no"]}
    assert proposition in fact_body["title"].split(" Contributed categorical")[0].split(" Return-level")[0], fact
    # The question asserts the proposition, so "yes" is the fact's "yes".
    assert text.startswith("Is it true that ")
    pins = _v82_pins()
    assert pins[v2["id"]] == "v2"
    assert pins[P + "exception1.vocabulary"] == "v1"


def test_the_four_exception1_questions_are_distinct_and_yes_means_exception1_holds() -> None:
    """The conclusion rule treats all four "yes" as Exception 1 holding (Schedule D not required)."""
    texts = [text for text, _ in EXCEPTION1_V2.values()]
    assert len(set(texts)) == 4 and EXCEPTION1_V1 not in texts
    rule = _load_json(CONTENT / "rule.schedule-d-required.conclusion.json")
    assert _v82_pins()[rule["id"]] == rule["version"] == "v1"
    assert rule["value"]["then"] == "no" and rule["value"]["else"] == "yes"
    arms = rule["value"]["when"]["args"]
    assert sorted(arm["left"]["name"].removeprefix(P) for arm in arms) == sorted(EXCEPTION1_V2)
    for arm in arms:
        assert (arm["op"], arm["cmp"], arm["right"]["value"]) == ("categorical_compare", "eq", "yes")


STATEMENT_KEYS = [{"name": "statement", "kind": "entity", "entity_kind": "tax.us.f1099b-statement"},
                  {"name": "tax-year", "kind": "literal", "values": ["2025"]}]
# Fact -> (question, title, the rule that reads it).
STATEMENT_QUESTIONS = {
    "f1099b.statement-box4-withholding-reported": (
        "For each Form 1099-B or substitute statement you recorded a sale from, does it show federal income tax "
        "withheld in box 4?",
        "Whether one recorded 2025 Form 1099-B statement shows federal income tax withheld (backup withholding) in "
        "box 4. yes or no.",
        "rule.form1040-line25b.v6.json"),
    "f1099b.statement-box7-loss-not-allowed": (
        "For each Form 1099-B or substitute statement you recorded a sale from, is box 7 (\"If checked, loss is not "
        "allowed based on amount in 1d\") checked for any sale on it?",
        "Whether box 7 (loss not allowed based on the box 1d amount) is checked for any sale on one recorded 2025 "
        "Form 1099-B statement. yes or no.",
        "rule.schedule-d-line16.v3.json"),
}


@pytest.mark.parametrize("fact", sorted(STATEMENT_QUESTIONS))
def test_each_statement_question_asks_one_statement_and_yes_refuses(fact: str) -> None:
    """Asked once per recorded Form 1099-B statement; "yes" is the box shown, and the reading rule refuses it."""
    text, title, rule_name = STATEMENT_QUESTIONS[fact]
    question = _load_json(CONTENT / f"input-question.{fact.replace('.', '-', 1)}.json")
    body = _fact("f1099b-statement-boxes.bundle.json", P + fact)
    assert question["question"] == text
    assert question["fact_type"] == {"id": P + fact, "version": body["version"]} == {"id": P + fact, "version": "v1"}
    assert body["title"] == title
    assert body["identity_keys"] == STATEMENT_KEYS
    assert body["value_schema"] == {"enum": ["yes", "no"]}
    assert body["supersession"] == {"policy": "free"}
    rule = _load_json(CONTENT / rule_name)
    assert _v82_pins()[rule["id"]] == rule["version"]
    text_of = json.dumps(rule)
    # Every recorded Form 1099-B sale's statement needs an answer, and anything but "no" on any statement blocks.
    assert rule["when"]["args"][-1] == {
        "op": "require_paired", "key": "statement", "withholding": P + fact,
        "income": [P + f"f1099b.{k}-{t}-txn" for k in ("covered", "covered-w", "noncovered", "code-b")
                   for t in ("st", "lt")]}
    assert rule["value"]["then"] == {"op": "block", "code": "DEPENDENCY_ABSENT"}
    (every_no,) = [arg["value"] for arg in rule["value"]["when"]["args"] if arg.get("op") == "not"]
    assert every_no == {"op": "collect_categorical_all_equal", "name": P + fact, "value": {
        "op": "category_literal", "fact_type": {"id": P + fact, "version": "v1"}, "value": "no"}}
    assert text_of.count(f'"{P}{fact}"') == 3


def test_the_return_level_box_answers_are_not_declared() -> None:
    """Track 0's counterexample: one answer per return stayed current beside a sale from a new statement."""
    declared = {f["id"] for f in _load_json(CONTENT / "f1099b-statement-boxes.bundle.json")["fact_types"]}
    assert declared == {P + fact for fact in STATEMENT_QUESTIONS}


# ---- the audit: every sale field is read, has a reason, or is refused by an answer ----


def _members(tables: ModuleType, version: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = tables.members(CONTENT, version)
    return found


def test_every_sale_field_on_v82_is_read_or_has_a_recorded_reason(tables: ModuleType) -> None:
    members = _members(tables, "v82")
    fields = tables.field_table(members)
    assert sorted(fields) == sorted(name.removeprefix(P) for name in tables.SALE_OBJECTS)
    assert tables.audit(members, fields) == []
    assert tables.consumer_audit(members) == []


def test_every_amount_row_on_v82_is_tied_to_its_sale(tables: ModuleType) -> None:
    """Review F1: each proceeds, basis and column (g) row requires its own sale (a loader presence pair)."""
    rows = tables.row_table(_members(tables, "v82"), tables.loader_pairs("v82"))
    assert len(rows) == 28
    assert all(sale == row.rsplit(".", 1)[0] for row, sale in rows.items())
    assert tables.row_audit(rows) == []
    pairs = dict(tables.loader_pairs("v82"))
    del pairs[P + "f1099b.covered-w-lt-txn.adjustment"]
    assert tables.row_audit(tables.row_table(_members(tables, "v82"), pairs)) == [
        "f1099b.covered-w-lt-txn.adjustment is not tied to its sale: a row with no sale of its own is summed on its "
        "line"]


def test_the_committed_v82_tables_are_the_published_v82s(tables: ModuleType) -> None:
    members = _members(tables, "v82")
    fields = tables.field_table(members)
    committed = _load_json(EVIDENCE / "tables-v82.json")
    assert committed["fields"] == fields
    assert committed["rows"] == tables.row_table(members, tables.loader_pairs("v82"))
    assert committed["consumers"] == tables.consumer_table(members)
    assert committed["audit_failures"] == []


def test_the_audit_fails_on_v81(tables: ModuleType) -> None:
    """The check bites: on v81 it names every defect P0 and the review found in the tables (56 failures)."""
    members = _members(tables, "v81")
    failures = (tables.audit(members, tables.field_table(members)) +
                tables.row_audit(tables.row_table(members, tables.loader_pairs("v81"))) + tables.consumer_audit(members))
    assert len(failures) == 56
    assert sum("is not tied to its sale" in failure for failure in failures) == 10
    for words in ("f1099b.covered-st-txn.proceeds is not tied to its sale","f1099b.covered-st-count is not read by form1040.line7b-schedule-d-not-required","f1099b.covered-st-txn.long_term is read by no rule",
                  "f1099b.covered-lt-txn.box_1g_wash_sale_adjustment is read by no rule",
                  "f8949.no1099b-st-count: no rule publishes the count",
                  "f1099b.covered-w-st-count is not read by tax.total-tax",
                  "the answer f1099b.statement-box4-withholding-reported is not declared"):
        assert any(words in failure for failure in failures), words


def test_a_new_unread_sale_field_fails_the_audit(tables: ModuleType) -> None:
    members = copy.deepcopy(_members(tables, "v82"))
    (bundle,) = [m for m in members if m["_role"] == "fact-type-bundle"
                 and any(f["id"] == P + "f1099b.noncovered-st-txn" for f in m["fact_types"])]
    (sale,) = [f for f in bundle["fact_types"] if f["id"] == P + "f1099b.noncovered-st-txn"]
    sale["value_schema"]["properties"]["box_99_new_amount"] = {"type": "number"}
    failures = tables.audit(members, tables.field_table(members))
    assert failures == ["f1099b.noncovered-st-txn.box_99_new_amount is read by no rule and has no reason it cannot "
                        "change the return"]


def test_a_no_effect_reason_covers_only_its_own_objects(tables: ModuleType) -> None:
    """Review N1: the box 5 reason is keyed by (object, field), so the same field on another sale object fails."""
    members = copy.deepcopy(_members(tables, "v82"))
    (bundle,) = [m for m in members if m["_role"] == "fact-type-bundle"
                 and any(f["id"] == P + "f1099b.noncovered-st-txn" for f in m["fact_types"])]
    (sale,) = [f for f in bundle["fact_types"] if f["id"] == P + "f1099b.noncovered-st-txn"]
    sale["value_schema"]["properties"]["covered_security"] = {"enum": ["yes", "no"]}
    assert tables.audit(members, tables.field_table(members)) == [
        "f1099b.noncovered-st-txn.covered_security is read by no rule and has no reason it cannot change the return"]
    assert sorted(obj for obj, _field in tables.NO_EFFECT) == sorted(
        f"f1099b.{k}-txn" for k in ("covered-st", "covered-lt", "covered-w-st", "covered-w-lt"))


def test_each_sale_line_names_only_its_own_admission_reasons() -> None:
    """Review N4: only lines 1a and 8a refuse a box 1g sale, and they have no wash-sale row."""
    for name in ("schedule-d.line-1a.form-field.v4.json", "schedule-d.line-8a.form-field.v3.json"):
        words = _load_json(CONTENT / name)["dispositions"]["blocked"]["explain"]
        assert "box 1g (record it as a code W sale)" in words and "wash-sale row" not in words, name
    for name in ("schedule-d.line-1b.form-field.v4.json", "schedule-d.line-8b.form-field.v4.json"):
        words = _load_json(CONTENT / name)["dispositions"]["blocked"]["explain"]
        assert "box 1g" not in words and "wash-sale row is missing" in words, name


def test_a_refusing_answer_no_rule_reads_fails_the_audit(tables: ModuleType) -> None:
    members = copy.deepcopy(_members(tables, "v82"))
    kept = [m for m in members if not (m["_role"] == "computation" and m["id"] == P + "rule.form1040-line25b")]
    assert len(kept) == len(members) - 1
    failures = tables.audit(kept, tables.field_table(kept))
    assert failures == ["box 4 federal income tax withheld: no rule reads the answer "
                        "f1099b.statement-box4-withholding-reported"]
