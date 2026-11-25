"""Fast publication, validation, closure, and coverage tests for ADR 0088 (core v106)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.authorization_closure import build_dependency_edges
from packages.derivation.loader import DerivationSchemas, ROLE_VOCABULARY
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum, validate_package
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.loader import (
    covered_flag_refusal_map,
    domain_package_companion_declarations,
    later_any_arm_refs_while_count_blocked,
    selection_collect_satisfied_by_family,
    unconfirmed_family_names_closure_question,
)
from tools.sale_page_observation import _compare_model_and_dom, _expected_blocked_reason_texts

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASES = ROOT / "packages" / "sample_data" / "student_loan_worksheet_integration" / "publication_surface" / "releases"
WORDING_PATH = ROOT / "docs" / "phases" / "engine-breadth" / "milestones" / "sale-block-explanations-evidence" / "wording.json"
CORE = "tax.us.2025.package.core-calculations"
STEM = "demo.release.sli-worksheet-integration.2025"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"}


def _read(path: Path) -> dict[str, Any]:
    return dict(json.loads(path.read_text(encoding="utf-8")))


def _index_by_id_ver(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(str(row["id"]), str(row["version"])): row for row in rows}


def _build_minimal_package(
    *,
    schema: str = "artifact-package.v44",
    members: list[dict[str, Any]],
    corpus_docs: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[tuple[str, str], dict[str, Any]]]:
    role_canon = _read(next(CONTENT.glob("*role-canon*.json")))
    docs = [role_canon, *corpus_docs]
    all_members = [
        {"id": str(role_canon["id"]), "version": str(role_canon["version"]), "schema": "role-canon.v1", "role": "parameter"},
        *members,
    ]
    admitted = sorted({str(m["schema"]) for m in all_members})
    package: dict[str, Any] = {
        "schema": schema,
        "id": "demo.package.fbe",
        "version": "v1",
        "scope": dict(SCOPE),
        "admitted_schemas": admitted,
        "members": all_members,
        "input_bindings": [],
        "entrypoints": [{"id": str(m["id"]), "version": str(m["version"])} for m in all_members],
        "composition_obligations": [],
    }
    package["package_checksum"] = package_instance_checksum(package)
    corpus = {(str(d["id"]), str(d["version"])): d for d in docs}
    return package, corpus


def _base_sale_fixtures() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fact_type = {
        "schema": "fact-type.v2",
        "id": "demo.fact.sale",
        "version": "v1",
        "title": "Demo sale",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "value_schema": {"type": "object", "properties": {"proceeds": {"type": "number"}}},
        "supersession": {"policy": "free"},
    }
    adj_fact = {
        "schema": "fact-type.v2",
        "id": "demo.fact.sale.adjustment",
        "version": "v1",
        "title": "Demo sale adjustment",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
    }
    bundle = {
        "schema": "bundle.v2",
        "id": "demo.bundle.sales",
        "version": "v1",
        "label": "Demo sales bundle",
        "fact_types": [fact_type, adj_fact],
    }
    family = {
        "schema": "source-family.v2",
        "id": "demo.family.sales",
        "version": "v1",
        "scope": dict(SCOPE),
        "title": "Demo sales",
        "closure_claim": "Demo sales recorded for 2025.",
        "member_predicate": {"fact_type": "demo.fact.sale"},
        "authorizes_subtotal": "demo.sales.subtotal",
        "member_constraints": [
            {
                "id": "demo.constraint.code-w-on-gain",
                "block_code": "CODE_W_ON_GAIN",
                "meaning": "Engine text.",
                "violated_when": {
                    "op": "field_equals",
                    "field": "proceeds",
                    "arg": "bad",
                },
            }
        ],
    }
    input_q = {
        "schema": "input-question.v1",
        "id": "demo.input-question.adj",
        "version": "v1",
        "fact_type": {"id": "demo.fact.sale.adjustment", "version": "v1"},
        "question": "What is the disallowed wash-sale loss?",
    }
    pins: list[dict[str, Any]] = [
        {"id": "demo.fact.sale", "version": "v1", "schema": "fact-type.v2", "role": "fact-type"},
        {"id": "demo.fact.sale.adjustment", "version": "v1", "schema": "fact-type.v2", "role": "fact-type"},
        {"id": "demo.bundle.sales", "version": "v1", "schema": "bundle.v2", "role": "fact-type-bundle"},
        {"id": "demo.family.sales", "version": "v1", "schema": "source-family.v2", "role": "source-family"},
        {"id": "demo.input-question.adj", "version": "v1", "schema": "input-question.v1", "role": "input-question"},
    ]
    docs: list[dict[str, Any]] = [fact_type, adj_fact, bundle, family, input_q]
    return pins, docs


def test_core_v106_adds_only_6_questions_and_30_explanations_on_v44() -> None:
    v105 = _read(CONTENT / "package.core-calculations.v105.json")
    v106 = _read(CONTENT / "package.core-calculations.v106.json")
    assert (v106["id"], v106["version"], v106["schema"]) == (CORE, "v106", "artifact-package.v44")
    assert set(v106["admitted_schemas"]) - set(v105["admitted_schemas"]) == {"family-block-explanation.v1"}
    assert v106["package_checksum"] == package_instance_checksum(v106)

    v105_pins = {(m["id"], m["version"], m["schema"], m["role"]) for m in v105["members"]}
    v106_pins = {(m["id"], m["version"], m["schema"], m["role"]) for m in v106["members"]}
    assert v105_pins.issubset(v106_pins)
    added = v106_pins - v105_pins
    added_iq = {pin for pin in added if pin[2] == "input-question.v1"}
    added_fbe = {pin for pin in added if pin[2] == "family-block-explanation.v1"}
    assert len(added) == 36
    assert len(added_iq) == 6
    assert len(added_fbe) == 30

    # Zero source-family pins changed.
    v105_fams = {pin for pin in v105_pins if pin[2].startswith("source-family.")}
    v106_fams = {pin for pin in v106_pins if pin[2].startswith("source-family.")}
    assert v105_fams == v106_fams


def test_registry_v104_and_release_v104_only_advance_core() -> None:
    reg103 = _read(CONTENT / "published-packages.v103.json")
    reg104 = _read(CONTENT / "published-packages.v104.json")

    old_cit = _index_by_id_ver(reg103["citizens"])
    new_cit = _index_by_id_ver(reg104["citizens"])
    assert all(new_cit[k] == v for k, v in old_cit.items())
    added_cit = {k: new_cit[k] for k in set(new_cit) - set(old_cit)}
    assert len(added_cit) == 36
    for p in list(CONTENT.glob("family-block-explanation.*.v1.json")) + list(CONTENT.glob("input-question.*adjustment*.v1.json")):
        doc = _read(p)
        key = (doc["id"], doc["version"])
        if key in added_cit:
            assert added_cit[key]["checksum"] == citizen_checksum(doc)

    old_pkg = _index_by_id_ver(reg103["packages"])
    new_pkg = _index_by_id_ver(reg104["packages"])
    assert all(new_pkg[k] == v for k, v in old_pkg.items())
    pkg106 = _read(CONTENT / "package.core-calculations.v106.json")
    assert {k: new_pkg[k] for k in set(new_pkg) - set(old_pkg)} == {
        (CORE, "v106"): {"id": CORE, "version": "v106", "checksum": pkg106["package_checksum"]}
    }

    rel103 = _read(RELEASES / f"{STEM}.v103.json")
    rel104 = _read(RELEASES / f"{STEM}.v104.json")
    digest = hashlib.sha256((CONTENT / "published-packages.v104.json").read_bytes()).hexdigest()
    assert rel104 == {**rel103, "version": "v104", "package_registry_sha256": digest}


def test_v106_loader_entries_carry_v105() -> None:
    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v106")] == declarations[(CORE, "v105")]
    assert covered_flag_refusal_map(CORE, "v106") == covered_flag_refusal_map(CORE, "v105")
    for switch in (
        selection_collect_satisfied_by_family,
        later_any_arm_refs_while_count_blocked,
        unconfirmed_family_names_closure_question,
    ):
        assert switch(CORE, "v106") == switch(CORE, "v105") is True


def test_every_current_core_member_constraint_has_family_block_explanation() -> None:
    """ADR 0088 Decision 5: every member_constraints entry on v106 has a matching explanation."""
    v106 = _read(CONTENT / "package.core-calculations.v106.json")
    wording = _read(WORDING_PATH)
    expected_by_key = {(r["family_id"], r["block_code"]): r for r in wording["replacements"]}

    explanations: dict[tuple[str, str], dict[str, Any]] = {}
    for p in sorted(CONTENT.glob("family-block-explanation.*.v1.json")):
        doc = _read(p)
        explanations[(doc["family_id"], doc["block_code"])] = doc

    families_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for p in sorted(CONTENT.glob("family.*.json")):
        doc = _read(p)
        families_by_key[(doc["id"], doc["version"])] = doc

    v106_fbe_ids = {(m["id"], m["version"]) for m in v106["members"] if m["schema"] == "family-block-explanation.v1"}
    checked = 0
    for pin in v106["members"]:
        if not pin["schema"].startswith("source-family."):
            continue
        fam = families_by_key[(pin["id"], pin["version"])]
        for mc in fam.get("member_constraints", []):
            key = (fam["id"], mc["block_code"])
            assert key in explanations, f"Missing family-block-explanation.v1 for {key}"
            doc = explanations[key]
            assert (doc["id"], doc["version"]) in v106_fbe_ids
            assert doc["explanation"] == expected_by_key[key]["new"]
            checked += 1
    assert checked == 30


def test_package_validation_and_schema_reject_invalid_family_block_explanations() -> None:
    schemas = DerivationSchemas()

    pins, docs = _base_sale_fixtures()
    good_fbe = {
        "schema": "family-block-explanation.v1",
        "id": "demo.fbe.code-w",
        "version": "v1",
        "family_id": "demo.family.sales",
        "block_code": "CODE_W_ON_GAIN",
        "explanation": "Plain wash-sale sentence.",
        "fact_type": {"id": "demo.fact.sale.adjustment", "version": "v1"},
    }
    good_pin = {"id": "demo.fbe.code-w", "version": "v1", "schema": "family-block-explanation.v1", "role": "family-block-explanation"}
    pkg_ok, corp_ok = _build_minimal_package(members=[*pins, good_pin], corpus_docs=[*docs, good_fbe])
    res_ok = validate_package(pkg_ok, corp_ok, schemas)
    assert res_ok.ok, res_ok.issues

    # v43 rejects family-block-explanation.v1 at schema level.
    pkg_v43, _ = _build_minimal_package(schema="artifact-package.v43", members=[*pins, good_pin], corpus_docs=[*docs, good_fbe])
    with pytest.raises(SchemaValidationError):
        schemas.validate_declared(pkg_v43)

    # 1. ROLE_MISMATCH
    bad_role_pin = {**good_pin, "role": "input-question"}
    pkg, corp = _build_minimal_package(members=[*pins, bad_role_pin], corpus_docs=[*docs, good_fbe])
    assert "ROLE_MISMATCH" in [i.code for i in validate_package(pkg, corp, schemas).issues]

    # 2. FAMILY_BLOCK_EXPLANATION_FAMILY_ABSENT
    bad_fam = {**good_fbe, "family_id": "demo.family.missing"}
    pkg, corp = _build_minimal_package(members=[*pins, good_pin], corpus_docs=[*docs, bad_fam])
    assert "FAMILY_BLOCK_EXPLANATION_FAMILY_ABSENT" in [i.code for i in validate_package(pkg, corp, schemas).issues]

    # 3. FAMILY_BLOCK_EXPLANATION_CODE_ABSENT
    bad_code = {**good_fbe, "block_code": "NO_SUCH_CODE"}
    pkg, corp = _build_minimal_package(members=[*pins, good_pin], corpus_docs=[*docs, bad_code])
    assert "FAMILY_BLOCK_EXPLANATION_CODE_ABSENT" in [i.code for i in validate_package(pkg, corp, schemas).issues]

    # 4. FAMILY_BLOCK_EXPLANATION_DUPLICATE
    dup_fbe = {**good_fbe, "id": "demo.fbe.code-w-dup"}
    dup_pin = {**good_pin, "id": "demo.fbe.code-w-dup"}
    pkg, corp = _build_minimal_package(members=[*pins, good_pin, dup_pin], corpus_docs=[*docs, good_fbe, dup_fbe])
    assert "FAMILY_BLOCK_EXPLANATION_DUPLICATE" in [i.code for i in validate_package(pkg, corp, schemas).issues]

    # 5. FAMILY_BLOCK_EXPLANATION_FACT_TYPE_NOT_ADMITTED
    unadmitted_ft = {**good_fbe, "fact_type": {"id": "demo.fact.unknown", "version": "v1"}}
    pkg, corp = _build_minimal_package(members=[*pins, good_pin], corpus_docs=[*docs, unadmitted_ft])
    assert "FAMILY_BLOCK_EXPLANATION_FACT_TYPE_NOT_ADMITTED" in [i.code for i in validate_package(pkg, corp, schemas).issues]

    # 6. FAMILY_BLOCK_EXPLANATION_QUESTION_ABSENT
    pins_no_iq = [p for p in pins if p["id"] != "demo.input-question.adj"]
    docs_no_iq = [d for d in docs if d["id"] != "demo.input-question.adj"]
    pkg, corp = _build_minimal_package(members=[*pins_no_iq, good_pin], corpus_docs=[*docs_no_iq, good_fbe])
    assert "FAMILY_BLOCK_EXPLANATION_QUESTION_ABSENT" in [i.code for i in validate_package(pkg, corp, schemas).issues]


def test_authorization_closure_links_family_and_explanation_edges() -> None:
    pins, docs = _base_sale_fixtures()
    fbe = {
        "schema": "family-block-explanation.v1",
        "id": "demo.fbe.code-w",
        "version": "v1",
        "family_id": "demo.family.sales",
        "block_code": "CODE_W_ON_GAIN",
        "explanation": "Plain wash-sale sentence.",
        "fact_type": {"id": "demo.fact.sale.adjustment", "version": "v1"},
    }
    pkg, _ = _build_minimal_package(
        members=[
            *pins,
            {"id": "demo.fbe.code-w", "version": "v1", "schema": "family-block-explanation.v1", "role": "family-block-explanation"},
        ],
        corpus_docs=[*docs, fbe],
    )
    corpus_by_id = {d["id"]: d for d in [*docs, fbe]}
    edges = build_dependency_edges(corpus_by_id, package=pkg)
    assert "demo.fbe.code-w" in edges["demo.family.sales"]
    assert "demo.family.sales" in edges["demo.fbe.code-w"]
    assert "demo.fact.sale.adjustment" in edges["demo.fbe.code-w"]


def test_sale_page_observation_matches_two_reason_wash_sale_model() -> None:
    plain = "A wash-sale loss disallowed in box 1g of this Form 1099-B was entered on a sale that is not a loss."
    question = "What is the nondeductible wash-sale loss in box 1g of Form 1099-B (or 0 if none)?"
    model: dict[str, Any] = {
        "schema": "presentation-model.v3",
        "questionGroups": [{"id": "q-group-1", "question": question}],
        "sections": [{
            "id": "demo-line",
            "field": {"id": "demo.field.line", "dispositions": {"blocked": {"explain": "Demo explain."}}},
            "resolved": {
                "disposition": "blocked",
                "reasons": [{"sentence": plain}, {"sentence": question}],
                "questionRefs": [{
                    "groupId": "q-group-1",
                    "reasonIndices": [1],
                    "scopes": [{"kind": "fact", "id": "demo.fact.adj", "status": "current"}],
                }],
            },
        }],
        "attachments": [],
    }
    dom: dict[str, Any] = {
        "lines": [{
            "id": "demo-line",
            "disposition": "No result",
            "disposition_raw": "blocked",
            "value": "This line has no result.",
            "blocked_reasons": [plain, "See the question and affected lines above"],
        }],
        "attachments": [],
    }
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [
        plain,
        "See the question and affected lines above",
    ]
    differences, _checks = _compare_model_and_dom(model, dom)
    assert differences == []
