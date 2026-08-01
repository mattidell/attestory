"""Generate the additive 2025 payer-reported market-discount successor route.

Historical schemas, citizens, packages, registries, releases, and adoptions are
read-only inputs.  This generator writes only the new market-discount
successors: two source families (Form 1099-INT box 10 and Form 1099-OID box 5),
the seven-family interest composition, the line-2b and Schedule B successors,
and the next package/release/adoption route.  All fixture identities are
obviously synthetic.  No new schema is introduced (MD-C5): every citizen below
targets an already-published schema generation.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "market_discount_interest"


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


def _b10_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": "tax.us.2025.f1099int-b10.vocabulary",
        "version": "v1",
        "label": "Form 1099-INT box-10 market-discount vocabulary for tax year 2025",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.f1099int.box10-market-discount",
                "version": "v1",
                "title": "Market discount reported in box 10 of one logical Form 1099-INT statement instance furnished by a payer for 2025 under the recipient's section 1278(b) current-inclusion election; statement identity is peer to evidence and carries no file, upload, scan, document, or evidence key (ADR-0015). This claim covers Form 1099-INT box 10 only, never Form 1099-OID box 5, other 1099-INT boxes, or disposition-time market discount.",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "payer", "kind": "entity", "entity_kind": "tax.us.interest-payer"},
                    {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1099int-statement"},
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {"id": "tax.us.2025.quantity.taxable-interest", "version": "v1"},
            },
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.f1099int.b10.source-closure",
                "version": "v1",
                "title": "User-attested closure of the 2025 Form 1099-INT box-10 market-discount family on its current membership horizon.",
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


def _oid_b5_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": "tax.us.2025.f1099oid-b5.vocabulary",
        "version": "v1",
        "label": "Form 1099-OID box-5 market-discount vocabulary for tax year 2025",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.f1099oid.box5-market-discount",
                "version": "v1",
                "title": "Market discount reported in box 5 of one logical Form 1099-OID statement instance furnished by a payer for 2025 for a covered security acquired with OID, under the recipient's section 1278(b) current-inclusion election; statement identity is peer to evidence and carries no file, upload, scan, document, or evidence key (ADR-0015). This claim covers Form 1099-OID box 5 only, never Form 1099-INT box 10, Form 1099-OID box 1, or disposition-time market discount.",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "payer", "kind": "entity", "entity_kind": "tax.us.interest-payer"},
                    {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1099oid-statement"},
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                ],
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {"id": "tax.us.2025.quantity.taxable-interest", "version": "v1"},
            },
            {
                "schema": "fact-type.v2",
                "id": "tax.us.2025.f1099oid.b5.source-closure",
                "version": "v1",
                "title": "User-attested closure of the 2025 Form 1099-OID box-5 market-discount family on its current membership horizon.",
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


def _b10_family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": "tax.us.2025.f1099int.b10",
        "version": "v1",
        "title": "Form 1099-INT box-10 market-discount statement items, tax year 2025",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "closure_claim": "Every market-discount amount reported in box 10 of a 2025 Form 1099-INT furnished to the taxpayer under a section 1278(b) current-inclusion election is recorded as a statement item. This claim covers Form 1099-INT box 10 only: it says nothing about Form 1099-OID box 5, other 1099-INT boxes, disposition-time market discount, basis, or total taxable interest.",
        "member_predicate": {"fact_type": "tax.us.2025.f1099int.box10-market-discount"},
        "authorizes_subtotal": "tax.us.2025.interest.b10-market-discount-subtotal",
    }


def _oid_b5_family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": "tax.us.2025.f1099oid.b5",
        "version": "v1",
        "title": "Form 1099-OID box-5 market-discount statement items, tax year 2025",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "closure_claim": "Every market-discount amount reported in box 5 of a 2025 Form 1099-OID furnished to the taxpayer under a section 1278(b) current-inclusion election is recorded as a statement item. This claim covers Form 1099-OID box 5 only: it says nothing about Form 1099-INT box 10, Form 1099-OID box 1, disposition-time market discount, basis, or total taxable interest.",
        "member_predicate": {"fact_type": "tax.us.2025.f1099oid.box5-market-discount"},
        "authorizes_subtotal": "tax.us.2025.interest.oid-b5-market-discount-subtotal",
    }


def _b10_mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.f1099int-b10",
        "version": "v1",
        "family": {"id": "tax.us.2025.f1099int.b10", "version": "v1"},
        "member_fact_type": {"id": "tax.us.2025.f1099int.box10-market-discount", "version": "v1"},
        "closure_fact_type": {"id": "tax.us.2025.f1099int.b10.source-closure", "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": "tax.us.2025.interest.b10-market-discount-subtotal",
        "admission": {"condition": "current-literal-true"},
    }


def _oid_b5_mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.f1099oid-b5",
        "version": "v1",
        "family": {"id": "tax.us.2025.f1099oid.b5", "version": "v1"},
        "member_fact_type": {"id": "tax.us.2025.f1099oid.box5-market-discount", "version": "v1"},
        "closure_fact_type": {"id": "tax.us.2025.f1099oid.b5.source-closure", "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": "tax.us.2025.interest.oid-b5-market-discount-subtotal",
        "admission": {"condition": "current-literal-true"},
    }


def _b10_citation() -> dict[str, Any]:
    return {
        "schema": "citation.v1",
        "id": "tax.us.2025.citation.f1099int.box10",
        "version": "v1",
        "authority": {"family": "irs-instructions", "form_id": "1099-INT", "tax_year": 2025},
    }


def _oid_b5_citation() -> dict[str, Any]:
    return {
        "schema": "citation.v1",
        "id": "tax.us.2025.citation.f1099oid.box5",
        "version": "v1",
        "authority": {"family": "irs-instructions", "form_id": "1099-OID", "tax_year": 2025},
    }


def _b10_subtotal_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.f1099int-b10-subtotal",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": ["rounding.convention"],
        "pins": [{"role": "input", "id": "rounding.convention", "version": "v1", "origin": "assertion"}],
        "when": True,
        "value": {
            "op": "round",
            "value": {"op": "add", "args": [{"op": "collect", "name": "tax.us.2025.f1099int.box10-market-discount", "source_set": "tax.us.2025.f1099int.b10"}]},
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": "tax.us.2025.interest.b10-market-discount-subtotal",
        "citations": [{"id": "tax.us.2025.citation.f1099int.box10", "version": "v1"}],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": "Aggregates only current 2025 Form 1099-INT box-10 market-discount members under the dedicated closed family. This symbol never publishes to, or stands behind, Form 1099-OID box 5, other 1099-INT boxes, or total taxable interest.",
    }


def _oid_b5_subtotal_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.f1099oid-b5-subtotal",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": ["rounding.convention"],
        "pins": [{"role": "input", "id": "rounding.convention", "version": "v1", "origin": "assertion"}],
        "when": True,
        "value": {
            "op": "round",
            "value": {"op": "add", "args": [{"op": "collect", "name": "tax.us.2025.f1099oid.box5-market-discount", "source_set": "tax.us.2025.f1099oid.b5"}]},
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": "tax.us.2025.interest.oid-b5-market-discount-subtotal",
        "citations": [{"id": "tax.us.2025.citation.f1099oid.box5", "version": "v1"}],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": "Aggregates only current 2025 Form 1099-OID box-5 market-discount members under the dedicated closed family. This symbol never publishes to, or stands behind, Form 1099-INT box 10, Form 1099-OID box 1, or total taxable interest.",
    }


def _composition_v3() -> dict[str, Any]:
    result = _load(CONTENT / "interest-composition.v2.json")
    result["version"] = "v3"
    result["constituents"].extend([
        {
            "source_family": {"id": "tax.us.2025.f1099int.b10", "version": "v1"},
            "authorizes_subtotal": "tax.us.2025.interest.b10-market-discount-subtotal",
        },
        {
            "source_family": {"id": "tax.us.2025.f1099oid.b5", "version": "v1"},
            "authorizes_subtotal": "tax.us.2025.interest.oid-b5-market-discount-subtotal",
        },
    ])
    result["required_universe"]["claim"] = (
        "Seven declared positive taxable-interest families without adjustments, "
        "including 2025 Schedule K-1 (Form 1065) box 5 and payer-reported "
        "current-inclusion market discount from Form 1099-INT box 10 and Form "
        "1099-OID box 5."
    )
    return result


def _line2b_v3() -> dict[str, Any]:
    result = _load(CONTENT / "rule.form1040-line2b.v2.json")
    result["version"] = "v3"
    for subtotal, family in (
        ("tax.us.2025.interest.b10-market-discount-subtotal", "tax.us.2025.f1099int.b10"),
        ("tax.us.2025.interest.oid-b5-market-discount-subtotal", "tax.us.2025.f1099oid.b5"),
    ):
        result["requires"].append(subtotal)
        result["pins"].append({"role": "input", "id": subtotal, "version": "v1", "origin": "assertion"})
        result["when"]["args"].append({"op": "require_closed", "source_set": family})
        result["value"]["args"].append({"op": "ref", "name": subtotal})
        result["blocked"]["missing"].append(subtotal)
    result["composition"]["version"] = "v3"
    result["notes"] = (
        "Computes Form 1040 line 2b from the exact seven-family positive-interest "
        "composition, including payer-reported current-inclusion market discount "
        "from Form 1099-INT box 10 and Form 1099-OID box 5 within the payer-"
        "reported boundary."
    )
    return result


def _line2b_field_v4() -> dict[str, Any]:
    result = _load(CONTENT / "form1040.line-2b.form-field.v3.json")
    result["version"] = "v4"
    result["description"] = (
        "Form 1040 (2025), line 2b: total taxable interest from seven declared "
        "positive source families: Form 1099-INT boxes 1 and 3, taxable Form "
        "1099-OID box 1, enumerated non-form interest, Schedule K-1 (Form 1065) "
        "box 5, and payer-reported current-inclusion market discount from Form "
        "1099-INT box 10 and Form 1099-OID box 5."
    )
    result["dispositions"]["published_value"]["explain"] = (
        "A current cited derived finding publishes taxable interest from the "
        "exact seven-family composition, including any payer-reported current-"
        "inclusion market-discount subtotal."
    )
    return result


def _schedule_b_v3() -> dict[str, Any]:
    result = _load(CONTENT / "rule.attachment.schedule-b.v2.json")
    result["version"] = "v3"
    result["title"] = (
        "Schedule B (Interest and Ordinary Dividends): required when taxable "
        "interest or ordinary dividends exceed $1,500. Part I itemizes the "
        "exact seven-family taxable-interest composition, including "
        "payer-reported current-inclusion market discount; Part II retains "
        "single-family ordinary-dividend authority; Part III and the named "
        "FinCEN-114 obligation are unchanged."
    )
    result["itemizations"][0]["authority"]["composition"]["version"] = "v3"
    result["itemizations"][0]["row_sets"].extend([
        {
            "rows": {
                "op": "collect_members",
                "member_fact_type": {"id": "tax.us.2025.f1099int.box10-market-discount", "version": "v1"},
                "source_family": {"id": "tax.us.2025.f1099int.b10", "version": "v1"},
            },
            "subtotal_symbol": "tax.us.2025.interest.b10-market-discount-subtotal",
        },
        {
            "rows": {
                "op": "collect_members",
                "member_fact_type": {"id": "tax.us.2025.f1099oid.box5-market-discount", "version": "v1"},
                "source_family": {"id": "tax.us.2025.f1099oid.b5", "version": "v1"},
            },
            "subtotal_symbol": "tax.us.2025.interest.oid-b5-market-discount-subtotal",
        },
    ])
    return result


def render_content_files() -> dict[str, dict[str, Any]]:
    citizens: dict[str, dict[str, Any]] = {
        "f1099int-b10.bundle.json": _b10_bundle(),
        "f1099oid-b5.bundle.json": _oid_b5_bundle(),
        "family.f1099int-b10.json": _b10_family(),
        "family.f1099oid-b5.json": _oid_b5_family(),
        "closure-mapping.f1099int-b10.json": _b10_mapping(),
        "closure-mapping.f1099oid-b5.json": _oid_b5_mapping(),
        "citation.f1099int.box10.json": _b10_citation(),
        "citation.f1099oid.box5.json": _oid_b5_citation(),
        "rule.f1099int-b10-subtotal.json": _b10_subtotal_rule(),
        "rule.f1099oid-b5-subtotal.json": _oid_b5_subtotal_rule(),
        "interest-composition.v3.json": _composition_v3(),
        "rule.form1040-line2b.v3.json": _line2b_v3(),
        "form1040.line-2b.form-field.v4.json": _line2b_field_v4(),
        "rule.attachment.schedule-b.v3.json": _schedule_b_v3(),
    }

    package = _load(CONTENT / "package.core-calculations.v9.json")
    package["version"] = "v10"
    replacements = {
        "tax.us.2025.interest-composition": {"role": "composition", "schema": "taxable-interest-composition.v1", "version": "v3"},
        "tax.us.2025.rule.form1040-line2b": {"role": "computation", "schema": "rule-artifact.v3", "version": "v3"},
        "tax.us.2025.form1040.line-2b": {"role": "form-field", "schema": "form-field.v3", "version": "v4"},
        "tax.us.2025.rule.attachment.schedule-b": {"role": "attachment-rule", "schema": "attachment-rule.v2", "version": "v3"},
    }
    members: list[dict[str, Any]] = []
    for member in package["members"]:
        replacement = replacements.get(member["id"])
        members.append({"id": member["id"], **replacement} if replacement else dict(member))
    members.extend([
        {"id": "tax.us.2025.f1099int-b10.vocabulary", "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"},
        {"id": "tax.us.2025.f1099oid-b5.vocabulary", "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"},
        {"id": "tax.us.2025.f1099int.b10", "role": "source-family", "schema": "source-family.v1", "version": "v1"},
        {"id": "tax.us.2025.f1099oid.b5", "role": "source-family", "schema": "source-family.v1", "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.f1099int-b10", "role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.f1099oid-b5", "role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "version": "v1"},
        {"id": "tax.us.2025.citation.f1099int.box10", "role": "citation", "schema": "citation.v1", "version": "v1"},
        {"id": "tax.us.2025.citation.f1099oid.box5", "role": "citation", "schema": "citation.v1", "version": "v1"},
        {"id": "tax.us.2025.rule.f1099int-b10-subtotal", "role": "computation", "schema": "rule-artifact.v3", "version": "v1"},
        {"id": "tax.us.2025.rule.f1099oid-b5-subtotal", "role": "computation", "schema": "rule-artifact.v3", "version": "v1"},
    ])
    package["members"] = sorted(members, key=lambda member: (member["id"], member["version"]))
    package["entrypoints"] = [
        ({"id": entry["id"], "version": "v3"} if entry["id"] == "tax.us.2025.rule.attachment.schedule-b" else dict(entry))
        for entry in package["entrypoints"]
    ]
    package["package_checksum"] = _package_checksum(package)
    citizens["package.core-calculations.v10.json"] = package

    registry = _load(CONTENT / "published-packages.v4.json")
    for citizen in citizens.values():
        if citizen.get("schema", "").startswith("artifact-package."):
            continue
        registry["citizens"].append({"id": citizen["id"], "version": citizen["version"], "checksum": _canonical_checksum(citizen)})
    registry["citizens"] = sorted(registry["citizens"], key=lambda row: (row["id"], row["version"]))
    registry["packages"].append({"id": package["id"], "version": "v10", "checksum": package["package_checksum"]})
    registry["packages"] = sorted(registry["packages"], key=lambda row: (row["id"], row["version"]))
    citizens["published-packages.v5.json"] = registry
    return citizens


def render_fixture_files(citizens: dict[str, dict[str, Any]]) -> dict[Path, bytes]:
    registry_bytes = _document(citizens["published-packages.v5.json"])
    registry = json.loads(registry_bytes)
    package_entry = next(row for row in registry["packages"] if row["id"] == "tax.us.2025.package.core-calculations" and row["version"] == "v10")
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v5",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v10",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-01T12:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {"id": "tax.us.2025.package.core-calculations", "version": "v10", "checksum": package_entry["checksum"]},
            "release": {"id": "demo.release.2025", "version": "v5", "checksum": hashlib.sha256(release_bytes).hexdigest()},
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 10,
            "audit": {"note": "synthetic market-discount breadth adoption; non-authoritative"},
        },
    }
    return {
        FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v5.json": release_bytes,
        FIXTURES / "adoptions" / "adopt-core-v10-current.json": _document(adoption),
    }


def render_all() -> dict[Path, bytes]:
    citizens = render_content_files()
    content_files = {CONTENT / name: _document(value) for name, value in citizens.items()}
    fixture_files = render_fixture_files(citizens)
    return {**content_files, **fixture_files}


def main() -> None:
    for path, body in render_all().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
