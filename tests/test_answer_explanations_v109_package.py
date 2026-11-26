"""Fast publication tests for core v109 (line16-next-step, ADR 0091).

Core v109 adds four answer-explanation.v1 citizens, one for each Exception 1
question answered no, under the new artifact-package.v45. answer-explanation.v1
and artifact-package.v45 are new schema files; v45 is v44 plus that one
schema and role. Nothing else in the package moves. The live checks (full
package validation and the drawn reasons) are in
test_answer_explanations_v109_live.py.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.authorization_closure import build_dependency_edges
from packages.derivation.loader import DerivationSchemas, ROLE_VOCABULARY
from packages.derivation.package_validation import (
    ANSWER_EXPLANATION_SCHEMAS,
    citizen_checksum,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.schema_capabilities import artifact_package_caps
from packages.derivation.presentation_projection import _answer_explanation_sentences
from packages.kernel.facts import KernelState
from packages.kernel.findings import FindingState
from packages.tax.loader import (
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    explains_identity_exclusivity_collision,
    later_any_arm_refs_while_count_blocked,
    selection_collect_satisfied_by_family,
    unconfirmed_family_names_closure_question,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
SCHEMAS = ROOT / "packages" / "schemas" / "derivation"
RELEASES = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
P = "tax.us.2025."

# ADR 0091 Decision 4 and line16-next-step Decision 3: the four sentences as accepted.
SENTENCES = {
    "only-box2a-capital-gains": (
        "You answered no to the question about capital gains and sales other than box 2a of Form 1099-DIV, "
        "so you must file Schedule D. If that is wrong, change your answer. If it is right, record each sale "
        "you must report; if you have no sale to record, this calculation does not cover your return."),
    "no-capital-losses": (
        "You answered no to the question about capital losses, so you must file Schedule D. If that is wrong, "
        "change your answer. If it is right, record each sale you must report; if you have no sale to record, "
        "this calculation does not cover your return."),
    "no-qof-deferral": (
        "You answered no to the question about deferring a gain in a qualified opportunity fund, so you must "
        "file Form 8949 and Schedule D. If that is wrong, change your answer. If it is right, this calculation "
        "does not cover your return."),
    "no-boxes-2b-2c-2d": (
        "You answered no to the question about boxes 2b, 2c and 2d of Form 1099-DIV, so you must file "
        "Schedule D. If that is wrong, change your answer. If it is right, this calculation does not cover "
        "your return."),
}


def _read(path: Path) -> dict[str, Any]:
    return dict(json.loads(path.read_text(encoding="utf-8")))


def _citizen_path(slug: str) -> Path:
    return CONTENT / f"answer-explanation.exception1-{slug}-no.v1.json"


def _pins(package: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    return [(m["id"], m["version"], m["schema"], m["role"]) for m in package["members"]]


def test_the_two_schemas_are_new_published_files() -> None:
    manifest = _read(SCHEMAS / "published.json")
    for name in ("answer-explanation.v1.schema.json", "artifact-package.v45.schema.json"):
        assert manifest[name] == hashlib.sha256((SCHEMAS / name).read_bytes()).hexdigest()
    schema = _read(SCHEMAS / "answer-explanation.v1.schema.json")
    assert schema["$id"] == "derivation/answer-explanation.v1"
    assert schema["required"] == ["schema", "id", "version", "fact_type", "value", "explanation"]
    assert schema["additionalProperties"] is False
    assert ANSWER_EXPLANATION_SCHEMAS == frozenset({"answer-explanation.v1"})
    assert "answer-explanation" in ROLE_VOCABULARY


def test_artifact_package_v45_is_v44_plus_the_one_schema_and_role() -> None:
    v44 = _read(SCHEMAS / "artifact-package.v44.schema.json")
    v45 = _read(SCHEMAS / "artifact-package.v45.schema.json")
    expected = copy.deepcopy(v44)
    member = expected["$defs"]["member"]["properties"]
    member["role"]["enum"].append("answer-explanation")
    member["schema"]["enum"].append("answer-explanation.v1")
    expected["properties"]["admitted_schemas"]["items"]["enum"].append("answer-explanation.v1")
    gates = [gate for gate in expected["allOf"] if "family-block-explanation.v1" in json.dumps(gate.get("if", {}))]
    assert len(gates) == 1
    expected["allOf"].append(json.loads(json.dumps(gates[0]).replace("family-block-explanation.v1", "answer-explanation.v1")))
    expected["$id"] = "derivation/artifact-package.v45"
    expected["properties"]["schema"]["const"] = "artifact-package.v45"
    expected["description"] = ("Artifact package v45: additive successor to v44, admitting answer-explanation.v1 in "
                               "both closed member and admitted-schema sets. v44 remains immutable history.")
    expected["title"] = "Closed package admitting answer-explanation.v1"
    assert v45 == expected
    v44_caps = artifact_package_caps("artifact-package.v44")
    assert v44_caps is not None
    assert artifact_package_caps("artifact-package.v45") == dataclasses.replace(v44_caps, schema="artifact-package.v45")


@pytest.mark.parametrize("slug", sorted(SENTENCES))
def test_each_citizen_declares_the_accepted_sentence_for_a_no_answer(slug: str) -> None:
    body = _read(_citizen_path(slug))
    assert body == {
        "schema": "answer-explanation.v1",
        "id": f"{P}answer-explanation.exception1-{slug}-no",
        "version": "v1",
        "fact_type": {"id": f"{P}exception1.{slug}", "version": "v1"},
        "value": "no",
        "explanation": SENTENCES[slug],
    }
    text = body["explanation"]
    assert text.startswith("You answered no to the question about ")
    assert "If that is wrong, change your answer. If it is right, " in text
    assert "this calculation does not cover your return." in text


def test_core_v109_adds_exactly_the_four_citizens_on_artifact_package_v45() -> None:
    v108 = _read(CONTENT / "package.core-calculations.v108.json")
    v109 = _read(CONTENT / "package.core-calculations.v109.json")
    assert (v109["id"], v109["version"], v109["schema"]) == (CORE, "v109", "artifact-package.v45")
    assert v108["schema"] == "artifact-package.v44"
    assert v109["package_checksum"] == package_instance_checksum(v109)
    assert {k for k in v109 if v109[k] != v108[k]} == {
        "version", "schema", "members", "entrypoints", "admitted_schemas", "package_checksum"}
    four = [(f"{P}answer-explanation.exception1-{slug}-no", "v1") for slug in
            ("only-box2a-capital-gains", "no-capital-losses", "no-qof-deferral", "no-boxes-2b-2c-2d")]
    assert _pins(v109) == _pins(v108) + [(i, v, "answer-explanation.v1", "answer-explanation") for i, v in four]
    assert [(e["id"], e["version"]) for e in v109["entrypoints"]] == [
        (e["id"], e["version"]) for e in v108["entrypoints"]] + four
    assert v109["admitted_schemas"] == v108["admitted_schemas"] + ["answer-explanation.v1"]


def test_registry_v107_is_add_only_and_release_v107_moves_only_the_registry() -> None:
    reg106 = _read(CONTENT / "published-packages.v106.json")
    reg107 = _read(CONTENT / "published-packages.v107.json")
    assert {k for k in reg107 if reg107[k] != reg106[k]} == {"citizens", "packages"}
    assert reg107["citizens"][: len(reg106["citizens"])] == reg106["citizens"]
    assert reg107["packages"][: len(reg106["packages"])] == reg106["packages"]
    added = reg107["citizens"][len(reg106["citizens"]):]
    assert [(e["id"], e["version"]) for e in added] == [
        (f"{P}answer-explanation.exception1-{slug}-no", "v1") for slug in
        ("only-box2a-capital-gains", "no-capital-losses", "no-qof-deferral", "no-boxes-2b-2c-2d")]
    for entry in added:
        slug = entry["id"].removeprefix(f"{P}answer-explanation.exception1-").removesuffix("-no")
        assert entry["checksum"] == citizen_checksum(_read(_citizen_path(slug)))
    v109 = _read(CONTENT / "package.core-calculations.v109.json")
    assert reg107["packages"][len(reg106["packages"]):] == [
        {"id": CORE, "version": "v109", "checksum": v109["package_checksum"]}]
    rel106 = _read(RELEASES / f"{STEM}.v106.json")
    rel107 = _read(RELEASES / f"{STEM}.v107.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v107.json").read_bytes()).hexdigest()
    assert rel107 == {**rel106, "version": "v107", "package_registry_sha256": digest}


def test_v109_loader_entries_carry_v108() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v109")] == declarations[(CORE, "v108")]
    assert covered_flag_refusal_map(CORE, "v109") == covered_flag_refusal_map(CORE, "v108")
    for switch in (
        selection_collect_satisfied_by_family,
        later_any_arm_refs_while_count_blocked,
        unconfirmed_family_names_closure_question,
        explains_identity_exclusivity_collision,
    ):
        assert switch(CORE, "v109") == switch(CORE, "v108") is True


@pytest.mark.parametrize(("case", "codes"), [
    ("bundle", set()),
    ("standalone", set()),
    ("outside-domain", {"ANSWER_EXPLANATION_VALUE_OUTSIDE_DOMAIN"}),
    ("missing-question", {"ANSWER_EXPLANATION_QUESTION_ABSENT"}),
    ("outside-surface", {"ANSWER_EXPLANATION_FACT_TYPE_NOT_ADMITTED",
                         "ANSWER_EXPLANATION_QUESTION_ABSENT",
                         "ANSWER_EXPLANATION_VALUE_OUTSIDE_DOMAIN"}),
    ("duplicate", {"ANSWER_EXPLANATION_DUPLICATE"}),
    ("wrong-role", {"ROLE_MISMATCH"}),
    ("old-schema", {"PACKAGE_SCHEMA_INVALID"}),
])
def test_answer_explanation_package_validation_controls(case: str, codes: set[str]) -> None:
    role_canon = _read(next(CONTENT.glob("*role-canon*.json")))
    fact_type: dict[str, Any] = {
        "schema": "fact-type.v2", "id": "demo.fact.answer", "version": "v1",
        "title": "Demo answer", "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "supersession": {"policy": "free"}, "value_schema": {"type": "string", "enum": ["yes", "no"]},
    }
    fact_pin = {"id": "demo.fact.answer", "version": "v1"}
    bundle = {"schema": "bundle.v2", "id": "demo.bundle.answers", "version": "v1",
              "label": "Demo answers", "fact_types": [fact_type]}
    question = {"schema": "input-question.v1", "id": "demo.input-question.answer", "version": "v1",
                "fact_type": fact_pin, "question": "Was the demo item recorded?"}
    answer = {
        "schema": "answer-explanation.v1", "id": "demo.answer-explanation.answer-no", "version": "v1",
        "fact_type": {**fact_pin, "version": "v2"} if case == "outside-surface" else fact_pin,
        "value": "maybe" if case == "outside-domain" else "no",
        "explanation": "You said the demo item has yet to be recorded. Record it to proceed.",
    }
    docs: list[tuple[dict[str, Any], str]] = [
        (role_canon, "parameter"), (answer, "input-question" if case == "wrong-role" else "answer-explanation"),
    ]
    docs.append((fact_type, "fact-type") if case == "standalone" else (bundle, "fact-type-bundle"))
    if case != "missing-question":
        docs.append((question, "input-question"))
    if case == "duplicate":
        docs.append(({**answer, "id": "demo.answer-explanation.duplicate"}, "answer-explanation"))
    members = [{"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role}
               for body, role in docs]
    package: dict[str, Any] = {
        "schema": "artifact-package.v44" if case == "old-schema" else "artifact-package.v45",
        "id": "demo.package.answers", "version": "v2",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"},
        "admitted_schemas": sorted({member["schema"] for member in members}),
        "members": members, "input_bindings": [], "composition_obligations": [],
        # The answer and question each root the reachability walk to the adopted fact.
        "entrypoints": [{"id": member["id"], "version": member["version"]} for member in members
                        if member["role"] not in {"fact-type", "fact-type-bundle"}],
    }
    package["package_checksum"] = package_instance_checksum(package)
    corpus = {(body["id"], body["version"]): body for body, _ in docs}
    outcome = validate_package(package, corpus, DerivationSchemas())
    assert outcome.ok is (not codes), outcome.issues
    assert {issue.code for issue in outcome.issues} == codes
    if case in {"bundle", "standalone"}:
        edges = build_dependency_edges({body["id"]: body for body, _ in docs}, package=package)
        target = bundle if case == "bundle" else fact_type
        assert edges[str(answer["id"])] == {str(target["id"]), role_canon["id"]}


def test_answer_explanations_require_a_single_current_finding_per_fact() -> None:
    fact_type = "demo.fact.answer"
    first = fact_type + "|item=demo.a"
    second = fact_type + "|item=demo.b"
    state = FindingState(
        fact_state=KernelState(fact_types={fact_type: {
            "id": fact_type, "version": "v1", "nature": "determinable",
            "identity_keys": [{"name": "item", "kind": "literal", "values": ["demo.a", "demo.b"]}],
        }}),
        findings={
            "demo.first": {"fact_id": first, "value": "no"},
            "demo.first-again": {"fact_id": first, "value": "no"},
            "demo.second": {"fact_id": second, "value": "no"},
        },
    )
    explanation = "Record the demo item."
    members = [{"schema": "answer-explanation.v1", "fact_type": {"id": fact_type, "version": "v1"},
                "value": "no", "explanation": explanation}]
    assert _answer_explanation_sentences(
        members, state, current_finding_ids=frozenset(state.findings),
    ) == {second: explanation, fact_type: explanation}
    assert _answer_explanation_sentences(
        members, state, current_finding_ids=frozenset({"demo.first", "demo.second"}),
    ) == {first: explanation, second: explanation}
