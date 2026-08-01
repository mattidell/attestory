"""Generate the additive 2025 Form-1065 Schedule K-1 box-5 successor route.

Historical schemas, citizens, packages, registries, releases, and adoptions are
read-only inputs.  This generator writes only the new K-1 breadth successors.
All fixture identities are obviously synthetic.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
SCHEMAS_DERIVATION = ROOT / "packages" / "schemas" / "derivation"
SCHEMAS_TAX = ROOT / "packages" / "schemas" / "tax"
FIXTURES = ROOT / "packages" / "sample_data" / "k1_interest_breadth"
FRRS_T3 = ROOT / "packages" / "sample_data" / "frrs_t3"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _canonical_checksum(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _package_checksum(package: dict[str, Any]) -> str:
    return _canonical_checksum(
        {key: value for key, value in package.items() if key != "package_checksum"}
    )


def render_schema_files() -> dict[Path, bytes]:
    attachment_v1 = _load(SCHEMAS_TAX / "attachment-rule.v1.schema.json")
    attachment_v2 = copy.deepcopy(attachment_v1)
    attachment_v2["$id"] = "tax/attachment-rule.v2"
    attachment_v2["title"] = "Schedule attachment rule with explicit itemization authority"
    attachment_v2["description"] = (
        "Additive successor to attachment-rule.v1. Each logical part declares "
        "single-family or composition authority, one or more same-family row "
        "sets with authorized subtotals, and one whole-part line tie-out."
    )
    attachment_v2["properties"]["schema"] = {"const": "attachment-rule.v2"}
    attachment_v2["properties"]["itemizations"] = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "part_id": {"type": "string", "minLength": 1},
                "label": {"type": "string", "minLength": 1},
                "authority": {"$ref": "#/$defs/itemization_authority"},
                "row_sets": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"$ref": "#/$defs/row_set"},
                },
                "tie_out": {
                    "type": "object",
                    "properties": {"line_symbol": {"type": "string", "minLength": 1}},
                    "required": ["line_symbol"],
                    "additionalProperties": False,
                },
            },
            "required": ["part_id", "label", "authority", "row_sets", "tie_out"],
            "additionalProperties": False,
        },
    }
    attachment_v2["$defs"]["itemization_authority"] = {
        "oneOf": [
            {
                "type": "object",
                "properties": {
                    "kind": {"const": "single_family"},
                    "source_family": {"$ref": "#/$defs/pin"},
                },
                "required": ["kind", "source_family"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {
                    "kind": {"const": "composition"},
                    "composition": {"$ref": "#/$defs/pin"},
                },
                "required": ["kind", "composition"],
                "additionalProperties": False,
            },
        ]
    }
    attachment_v2["$defs"]["row_set"] = {
        "type": "object",
        "properties": {
            "rows": {"$ref": "#/$defs/collect_members"},
            "subtotal_symbol": {"type": "string", "minLength": 1},
        },
        "required": ["rows", "subtotal_symbol"],
        "additionalProperties": False,
    }

    package_v5 = _load(SCHEMAS_DERIVATION / "artifact-package.v5.schema.json")
    package_v6 = copy.deepcopy(package_v5)
    package_v6["$id"] = "derivation/artifact-package.v6"
    package_v6["title"] = "Closed package admitting multi-family attachment successors"
    package_v6["description"] = (
        "artifact-package.v5 with attachment-rule.v2 admitted under the existing "
        "attachment-rule member role; every v5 schema and role remains admitted."
    )
    package_v6["properties"]["schema"] = {"const": "artifact-package.v6"}
    admitted = package_v6["properties"]["admitted_schemas"]["items"]["enum"]
    admitted.append("attachment-rule.v2")
    member_schemas = package_v6["$defs"]["member"]["properties"]["schema"]["enum"]
    member_schemas.append("attachment-rule.v2")
    package_v6["allOf"].extend([
        {
            "if": {"properties": {"members": {"contains": {"properties": {"schema": {"const": "attachment-rule.v2"}}, "required": ["schema"]}}}, "required": ["members"]},
            "then": {"properties": {"admitted_schemas": {"contains": {"const": "attachment-rule.v2"}}}},
        },
        {
            "if": {"properties": {"members": {"contains": {"properties": {"schema": {"const": "attachment-rule.v2"}}, "required": ["schema"]}}}, "required": ["members"]},
            "then": {"properties": {"members": {"items": {"if": {"properties": {"schema": {"const": "attachment-rule.v2"}}, "required": ["schema"]}, "then": {"properties": {"role": {"const": "attachment-rule"}}}}}}},
        },
    ])

    return {
        SCHEMAS_TAX / "attachment-rule.v2.schema.json": _document(attachment_v2),
        SCHEMAS_DERIVATION / "artifact-package.v6.schema.json": _document(package_v6),
    }


def _k1_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": "tax.us.2025.form1065-k1.vocabulary",
        "version": "v1",
        "label": "Schedule K-1 (Form 1065) box-5 taxable-interest vocabulary for tax year 2025",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.form1065-k1.box5-interest",
                "version": "v1",
                "title": "Taxable interest in box 5 of one logical 2025 Schedule K-1 (Form 1065); statement identity is peer to evidence and carries no file, upload, scan, document, or evidence key.",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "partnership", "kind": "entity", "entity_kind": "tax.us.partnership"},
                    {"name": "k1-statement", "kind": "entity", "entity_kind": "tax.us.form1065-k1-statement"},
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {"id": "tax.us.2025.quantity.taxable-interest", "version": "v1"},
            },
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.form1065-k1.box5.source-closure",
                "version": "v1",
                "title": "User-attested closure of the 2025 Form-1065 Schedule K-1 box-5 taxable-interest family on its current membership horizon.",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "boolean"},
                "supersession": {"policy": "free"},
            },
        ],
    }


def _k1_family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": "tax.us.2025.form1065-k1.box5",
        "version": "v1",
        "title": "Schedule K-1 (Form 1065) box-5 taxable-interest items, tax year 2025",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "closure_claim": "Every taxable-interest amount in box 5 of a 2025 Schedule K-1 (Form 1065) furnished to the return subject is recorded. This excludes other K-1 forms, boxes, attached statements, partnership basis, and total taxable-interest completeness.",
        "member_predicate": {"fact_type": "tax.us.2025.form1065-k1.box5-interest"},
        "authorizes_subtotal": "tax.us.2025.interest.form1065-k1-box5-subtotal",
    }


def _k1_mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.form1065-k1-box5",
        "version": "v1",
        "family": {"id": "tax.us.2025.form1065-k1.box5", "version": "v1"},
        "member_fact_type": {"id": "tax.us.2025.form1065-k1.box5-interest", "version": "v1"},
        "closure_fact_type": {"id": "tax.us.2025.form1065-k1.box5.source-closure", "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": "tax.us.2025.interest.form1065-k1-box5-subtotal",
        "admission": {"condition": "current-literal-true"},
    }


def _k1_citation() -> dict[str, Any]:
    return {
        "schema": "citation.v1",
        "id": "tax.us.2025.citation.form1065-k1.box5",
        "version": "v1",
        "authority": {"family": "irs-instructions", "form_id": "1065-SCHEDULE-K-1", "tax_year": 2025},
    }


def _k1_subtotal_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.form1065-k1-box5-subtotal",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": ["rounding.convention"],
        "pins": [{"role": "input", "id": "rounding.convention", "version": "v1", "origin": "assertion"}],
        "when": True,
        "value": {
            "op": "round",
            "value": {"op": "add", "args": [{"op": "collect", "name": "tax.us.2025.form1065-k1.box5-interest", "source_set": "tax.us.2025.form1065-k1.box5"}]},
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": "tax.us.2025.interest.form1065-k1-box5-subtotal",
        "citations": [{"id": "tax.us.2025.citation.form1065-k1.box5", "version": "v1"}],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": "Aggregates only current 2025 Schedule K-1 (Form 1065) box-5 members under the dedicated closed family.",
    }


def _composition_v2() -> dict[str, Any]:
    result = _load(CONTENT / "interest-composition.json")
    result["version"] = "v2"
    result["constituents"].append({
        "source_family": {"id": "tax.us.2025.form1065-k1.box5", "version": "v1"},
        "authorizes_subtotal": "tax.us.2025.interest.form1065-k1-box5-subtotal",
    })
    result["required_universe"]["claim"] = "Five declared positive taxable-interest families without adjustments, including 2025 Schedule K-1 (Form 1065) box 5."
    return result


def _line2b_v2() -> dict[str, Any]:
    result = _load(CONTENT / "rule.form1040-line2b.json")
    result["schema"] = "rule-artifact.v3"
    result["version"] = "v2"
    result["scope"].pop("effective_from", None)
    subtotal = "tax.us.2025.interest.form1065-k1-box5-subtotal"
    family = "tax.us.2025.form1065-k1.box5"
    result["requires"].append(subtotal)
    result["pins"].append({"role": "input", "id": subtotal, "version": "v1", "origin": "assertion"})
    result["when"]["args"].append({"op": "require_closed", "source_set": family})
    result["value"]["args"].append({"op": "ref", "name": subtotal})
    result["composition"]["version"] = "v2"
    result["citations"] = [{"id": "tax.us.2025.citation.form1040.line-2b", "version": "v1"}]
    result["blocked"]["missing"].append(subtotal)
    result["notes"] = "Computes Form 1040 line 2b from the exact five-family positive-interest composition, including only Form-1065 K-1 box 5 within the K-1 boundary."
    return result


def _line2b_field_v3() -> dict[str, Any]:
    result = _load(CONTENT / "form1040.line-2b.form-field.v2.json")
    result["version"] = "v3"
    result["description"] = "Form 1040 (2025), line 2b: total taxable interest from five declared positive source families: Form 1099-INT boxes 1 and 3, taxable Form 1099-OID box 1, enumerated non-form interest, and Schedule K-1 (Form 1065) box 5."
    result["dispositions"]["published_value"]["explain"] = "A current cited derived finding publishes taxable interest from the exact five-family composition, including any Form-1065 K-1 box-5 subtotal."
    return result


def _schedule_b_v2() -> dict[str, Any]:
    result = _load(CONTENT / "rule.attachment.schedule-b.json")
    result["schema"] = "attachment-rule.v2"
    result["version"] = "v2"
    result["title"] = "Schedule B (Interest and Ordinary Dividends): required when taxable interest or ordinary dividends exceed $1,500. Part I itemizes the exact five-family taxable-interest composition; Part II retains single-family ordinary-dividend authority; Part III and the named FinCEN-114 obligation are unchanged."
    families = [
        ("tax.us.2025.f1099int.b1", "tax.us.2025.f1099int.box1-interest", "tax.us.2025.interest.b1-subtotal"),
        ("tax.us.2025.f1099int.b3", "tax.us.2025.f1099int.box3-interest", "tax.us.2025.interest.b3-subtotal"),
        ("tax.us.2025.f1099oid.b1", "tax.us.2025.f1099oid.box1-interest-oid", "tax.us.2025.interest.oid-subtotal"),
        ("tax.us.2025.non-form-interest", "tax.us.2025.non-form-interest.amount", "tax.us.2025.interest.non-form-subtotal"),
        ("tax.us.2025.form1065-k1.box5", "tax.us.2025.form1065-k1.box5-interest", "tax.us.2025.interest.form1065-k1-box5-subtotal"),
    ]
    part_i = {
        "part_id": "part-i-interest",
        "label": "Part I: Taxable Interest",
        "authority": {"kind": "composition", "composition": {"id": "tax.us.2025.interest-composition", "version": "v2"}},
        "row_sets": [
            {
                "rows": {"op": "collect_members", "member_fact_type": {"id": fact_type, "version": "v1"}, "source_family": {"id": family, "version": "v1"}},
                "subtotal_symbol": subtotal,
            }
            for family, fact_type, subtotal in families
        ],
        "tie_out": {"line_symbol": "tax.us.2025.interest.taxable-total"},
    }
    part_ii_v1 = result["itemizations"][1]
    ordinary_subtotal = "tax.us.2025.dividends.1a-subtotal"
    part_ii = {
        "part_id": part_ii_v1["part_id"],
        "label": part_ii_v1["label"],
        "authority": {"kind": "single_family", "source_family": copy.deepcopy(part_ii_v1["rows"]["source_family"])},
        "row_sets": [{"rows": copy.deepcopy(part_ii_v1["rows"]), "subtotal_symbol": ordinary_subtotal}],
        "tie_out": {"line_symbol": ordinary_subtotal},
    }
    result["itemizations"] = [part_i, part_ii]
    return result


def render_content_files() -> dict[Path, bytes]:
    citizens = {
        "form1065-k1.bundle.json": _k1_bundle(),
        "family.form1065-k1-box5.json": _k1_family(),
        "closure-mapping.form1065-k1-box5.json": _k1_mapping(),
        "citation.form1065-k1.box5.json": _k1_citation(),
        "rule.form1065-k1-box5-subtotal.json": _k1_subtotal_rule(),
        "interest-composition.v2.json": _composition_v2(),
        "rule.form1040-line2b.v2.json": _line2b_v2(),
        "form1040.line-2b.form-field.v3.json": _line2b_field_v3(),
        "rule.attachment.schedule-b.v2.json": _schedule_b_v2(),
    }

    package = _load(CONTENT / "package.core-calculations.v8.json")
    package["schema"] = "artifact-package.v6"
    package["version"] = "v9"
    package["admitted_schemas"] = sorted(set(package["admitted_schemas"]) | {"attachment-rule.v2"})
    replacements = {
        "tax.us.2025.interest-composition": {"role": "composition", "schema": "taxable-interest-composition.v1", "version": "v2"},
        "tax.us.2025.rule.form1040-line2b": {"role": "computation", "schema": "rule-artifact.v3", "version": "v2"},
        "tax.us.2025.form1040.line-2b": {"role": "form-field", "schema": "form-field.v3", "version": "v3"},
        "tax.us.2025.rule.attachment.schedule-b": {"role": "attachment-rule", "schema": "attachment-rule.v2", "version": "v2"},
    }
    members: list[dict[str, Any]] = []
    for member in package["members"]:
        replacement = replacements.get(member["id"])
        members.append({"id": member["id"], **replacement} if replacement else dict(member))
    members.extend([
        {"id": "tax.us.2025.form1065-k1.vocabulary", "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"},
        {"id": "tax.us.2025.form1065-k1.box5", "role": "source-family", "schema": "source-family.v1", "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.form1065-k1-box5", "role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "version": "v1"},
        {"id": "tax.us.2025.citation.form1065-k1.box5", "role": "citation", "schema": "citation.v1", "version": "v1"},
        {"id": "tax.us.2025.rule.form1065-k1-box5-subtotal", "role": "computation", "schema": "rule-artifact.v3", "version": "v1"},
    ])
    package["members"] = sorted(members, key=lambda member: (member["id"], member["version"]))
    package["entrypoints"] = [
        ({"id": entry["id"], "version": "v2"} if entry["id"] == "tax.us.2025.rule.attachment.schedule-b" else dict(entry))
        for entry in package["entrypoints"]
    ]
    package["package_checksum"] = _package_checksum(package)
    citizens["package.core-calculations.v9.json"] = package

    registry = _load(CONTENT / "published-packages.v3.json")
    for citizen in citizens.values():
        if citizen.get("schema", "").startswith("artifact-package."):
            continue
        registry["citizens"].append({"id": citizen["id"], "version": citizen["version"], "checksum": _canonical_checksum(citizen)})
    registry["citizens"] = sorted(registry["citizens"], key=lambda row: (row["id"], row["version"]))
    registry["packages"].append({"id": package["id"], "version": "v9", "checksum": package["package_checksum"]})
    registry["packages"] = sorted(registry["packages"], key=lambda row: (row["id"], row["version"]))
    citizens["published-packages.v4.json"] = registry
    return {CONTENT / name: _document(value) for name, value in citizens.items()}


def render_fixture_files(content: dict[Path, bytes]) -> dict[Path, bytes]:
    registry_bytes = content[CONTENT / "published-packages.v4.json"]
    registry = json.loads(registry_bytes)
    package_entry = next(row for row in registry["packages"] if row["id"] == "tax.us.2025.package.core-calculations" and row["version"] == "v9")
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v4",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v9",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-07-31T12:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {"id": "tax.us.2025.package.core-calculations", "version": "v9", "checksum": package_entry["checksum"]},
            "release": {"id": "demo.release.2025", "version": "v4", "checksum": hashlib.sha256(release_bytes).hexdigest()},
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 9,
            "audit": {"note": "synthetic K-1 breadth adoption; non-authoritative"},
        },
    }
    attachment_example = _schedule_b_v2()
    package_example = json.loads(content[CONTENT / "package.core-calculations.v9.json"])
    malformed_attachment = copy.deepcopy(attachment_example)
    del malformed_attachment["itemizations"][0]["authority"]
    empty_rows = copy.deepcopy(attachment_example)
    empty_rows["itemizations"][0]["row_sets"] = []
    missing_subtotal = copy.deepcopy(attachment_example)
    del missing_subtotal["itemizations"][0]["row_sets"][0]["subtotal_symbol"]
    wrong_collect = copy.deepcopy(attachment_example)
    wrong_collect["itemizations"][0]["row_sets"][0]["rows"]["op"] = "collect"
    package_not_admitted = copy.deepcopy(package_example)
    package_not_admitted["admitted_schemas"].remove("attachment-rule.v2")
    package_wrong_role = copy.deepcopy(package_example)
    next(member for member in package_wrong_role["members"] if member["schema"] == "attachment-rule.v2")["role"] = "computation"
    return {
        FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v4.json": release_bytes,
        FIXTURES / "adoptions" / "adopt-core-v9-current.json": _document(adoption),
        FIXTURES / "schema" / "examples" / "attachment-rule.v2.json": _document(attachment_example),
        FIXTURES / "schema" / "examples" / "artifact-package.v6.json": _document(package_example),
        FIXTURES / "schema" / "negatives" / "attachment-rule.v2.missing-authority.json": _document(malformed_attachment),
        FIXTURES / "schema" / "negatives" / "attachment-rule.v2.empty-row-sets.json": _document(empty_rows),
        FIXTURES / "schema" / "negatives" / "attachment-rule.v2.missing-subtotal.json": _document(missing_subtotal),
        FIXTURES / "schema" / "negatives" / "attachment-rule.v2.wrong-collect-op.json": _document(wrong_collect),
        FIXTURES / "schema" / "negatives" / "artifact-package.v6.attachment-not-admitted.json": _document(package_not_admitted),
        FIXTURES / "schema" / "negatives" / "artifact-package.v6.attachment-wrong-role.json": _document(package_wrong_role),
    }


def main() -> None:
    schema_files = render_schema_files()
    content_files = render_content_files()
    fixture_files = render_fixture_files(content_files)
    for path, body in {**schema_files, **content_files, **fixture_files}.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
