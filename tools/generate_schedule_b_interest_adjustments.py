"""Generate the additive Schedule B interest-adjustment publication chain.

This generator discovers the latest same-ID core package and published-registry
predecessors on the content tree (currently package v14 / registry v9), then
writes only the Schedule B interest-adjustment content citizens plus package
v15, published registry v10, release v8, and synthetic v15 adoption. It
introduces no evaluator operation; attachment-rule.v6 / artifact-package.v12
are the milestone-admitted schema successors already published on this branch.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "schedule_b_interest_adjustments"

CORE_PACKAGE_ID = "tax.us.2025.package.core-calculations"
SUCCESSOR_PACKAGE_VERSION = 15
SUCCESSOR_REGISTRY_VERSION = 10
SUCCESSOR_PACKAGE_SCHEMA = "artifact-package.v12"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _checksum(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _package_checksum(package: dict[str, Any]) -> str:
    return _checksum({key: value for key, value in package.items() if key != "package_checksum"})


def _latest_versioned_path(prefix: str, *, below: int) -> Path:
    """Return the highest ``{prefix}.vN.json`` path with N < below."""
    found: list[tuple[int, Path]] = []
    pattern = re.compile(rf"^{re.escape(prefix)}\.v(\d+)\.json$")
    for path in CONTENT.glob(f"{prefix}.v*.json"):
        match = pattern.fullmatch(path.name)
        if match is None:
            continue
        version = int(match.group(1))
        if version < below:
            found.append((version, path))
    if not found:
        raise RuntimeError(f"no {prefix}.vN.json predecessor with N < {below} under {CONTENT}")
    found.sort(key=lambda item: item[0])
    return found[-1][1]


def _load_core_predecessor() -> dict[str, Any]:
    path = _latest_versioned_path("package.core-calculations", below=SUCCESSOR_PACKAGE_VERSION)
    package = _load(path)
    if package.get("id") != CORE_PACKAGE_ID:
        raise RuntimeError(f"{path} id {package.get('id')!r} is not {CORE_PACKAGE_ID}")
    return package


def _load_registry_predecessor() -> dict[str, Any]:
    return _load(_latest_versioned_path("published-packages", below=SUCCESSOR_REGISTRY_VERSION))


CLASSES: tuple[tuple[str, str, str, str], ...] = (
    (
        "nominee",
        "nominee_distribution",
        "Nominee Distribution",
        "a nominee distribution adjustment reported for one logical Schedule B interest-adjustment instance",
    ),
    (
        "accrued-interest",
        "accrued_interest",
        "Accrued Interest",
        "an accrued-interest-paid-to-seller adjustment reported for one logical Schedule B interest-adjustment instance",
    ),
    (
        "abp-adjustment",
        "abp_adjustment",
        "ABP Adjustment",
        "a taxable amortizable bond premium adjustment reported for one logical Schedule B interest-adjustment instance where the payer did not already net the amount",
    ),
)
POSITIVE_TOTAL = "tax.us.2025.interest.positive-total"


def _ids(token: str) -> dict[str, str]:
    prefix = f"tax.us.2025.scheduleb.adjustment.{token}"
    return {
        "family": prefix,
        "amount": f"{prefix}.amount",
        "closure": f"{prefix}.source-closure",
        "bundle": f"{prefix}.vocabulary",
        "mapping": f"tax.us.2025.closure-mapping.scheduleb-adjustment.{token}",
        "citation": f"tax.us.2025.citation.scheduleb-adjustment.{token}",
        "rule": f"tax.us.2025.rule.scheduleb-adjustment.{token}-subtotal",
        "subtotal": f"tax.us.2025.interest.scheduleb-{token}-subtotal",
    }


def _bundle(token: str, kind: str, label: str, boundary: str) -> dict[str, Any]:
    ids = _ids(token)
    return {
        "schema": "bundle.v2",
        "id": ids["bundle"],
        "version": "v1",
        "label": f"Synthetic 2025 Schedule B {label} adjustment vocabulary",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": ids["amount"],
                "version": "v1",
                "title": f"A nonnegative contributed {label.lower()} amount for {boundary}; identity is exactly the tax year plus logical adjustment instance and never an evidence, file, upload, scan, or document identifier.",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
                    {"name": "adjustment-instance", "kind": "entity", "entity_kind": "tax.us.scheduleb-adjustment-instance"},
                ],
                "value_schema": {"type": "number", "minimum": 0},
                "supersession": {"policy": "free"},
                "source_amount": True,
                "quantity": {"id": "tax.us.2025.quantity.taxable-interest", "version": "v1"},
            },
            {
                "schema": "fact-type.v2",
                "id": ids["closure"],
                "version": "v1",
                "title": f"Synthetic user-attested closure of the 2025 {label} adjustment class on its current membership horizon; it makes no claim about other interest, investments, transactions, or Schedule D.",
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


def _family(token: str, kind: str, label: str, boundary: str) -> dict[str, Any]:
    ids = _ids(token)
    return {
        "schema": "source-family.v1",
        "id": ids["family"],
        "version": "v1",
        "title": f"Synthetic {label} adjustment instances, tax year 2025",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "closure_claim": f"Every contributed {label.lower()} amount within the bounded Schedule B interest-adjustment surface is recorded as a logical adjustment instance for 2025. This claim covers {boundary} only; it says nothing about other adjustment classes, total interest, investment calculations, tax-exempt interest, frozen deposits, savings bonds, transactions, or Schedule D.",
        "member_predicate": {"fact_type": ids["amount"]},
        "authorizes_subtotal": ids["subtotal"],
    }


def _mapping(token: str) -> dict[str, Any]:
    ids = _ids(token)
    return {
        "schema": "source-closure-mapping.v2",
        "id": ids["mapping"],
        "version": "v1",
        "family": {"id": ids["family"], "version": "v1"},
        "member_fact_type": {"id": ids["amount"], "version": "v1"},
        "closure_fact_type": {"id": ids["closure"], "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": ids["subtotal"],
        "admission": {"condition": "current-literal-true"},
    }


def _citation(token: str, label: str) -> dict[str, Any]:
    ids = _ids(token)
    return {
        "schema": "citation.v1",
        "id": ids["citation"],
        "version": "v1",
        "authority": {"family": "irs-instructions", "form_id": "1040-SCH-B", "tax_year": 2025},
    }


def _subtotal_rule(token: str, label: str) -> dict[str, Any]:
    ids = _ids(token)
    return {
        "schema": "rule-artifact.v3",
        "id": ids["rule"],
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "role": "computation",
        "requires": ["rounding.convention"],
        "pins": [{"role": "input", "id": "rounding.convention", "version": "v1", "origin": "assertion"}],
        "when": True,
        "value": {
            "op": "round",
            "value": {"op": "add", "args": [{"op": "collect", "name": ids["amount"], "source_set": ids["family"]}]},
            "mode": {"op": "ref", "name": "rounding.convention"},
        },
        "publishes": ids["subtotal"],
        "citations": [{"id": ids["citation"], "version": "v1"}],
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": ["rounding.convention"]},
        "notes": f"Aggregates only the current closed {label} adjustment family. It never infers, calculates, or broadens any neighboring interest or transaction surface.",
    }


def _line2b_v4() -> dict[str, Any]:
    result = _load(CONTENT / "rule.form1040-line2b.v3.json")
    result["version"] = "v4"
    result["composition"] = {"id": "tax.us.2025.interest-composition", "version": "v4"}
    positive_args = copy.deepcopy(result["value"]["args"])
    positive_refs = [copy.deepcopy(arg) for arg in positive_args]
    adjustment_refs = [{"op": "ref", "name": _ids(token)["subtotal"]} for token, *_ in CLASSES]
    adjustment_symbols = [_ids(token)["subtotal"] for token, *_ in CLASSES]
    adjustment_families = [_ids(token)["family"] for token, *_ in CLASSES]
    result["requires"].extend(adjustment_symbols)
    result["pins"].extend({"role": "input", "id": symbol, "version": "v1", "origin": "assertion"} for symbol in adjustment_symbols)
    result["when"]["args"].extend({"op": "require_closed", "source_set": family} for family in adjustment_families)
    result["when"]["args"].append({
        "op": "compare",
        "left": {"op": "add", "args": positive_refs},
        "right": {"op": "add", "args": adjustment_refs},
        "cmp": "gte",
    })
    result["value"] = {
        "op": "subtract",
        "left": {"op": "add", "args": positive_refs},
        "right": {"op": "add", "args": adjustment_refs},
    }
    result["blocked"]["missing"].extend(adjustment_symbols)
    result["notes"] = (
        "Computes Form 1040 line 2b from the exact seven-family positive-interest "
        "composition less the three exact closed Schedule B adjustment classes. "
        "The existing subtract vocabulary is used; the comparison guard refuses "
        "to publish a negative taxable-interest result when adjustments exceed "
        "the positive basis."
    )
    return result


def _positive_total_rule() -> dict[str, Any]:
    result = _load(CONTENT / "rule.form1040-line2b.v3.json")
    result["id"] = "tax.us.2025.rule.interest-positive-total"
    result["version"] = "v1"
    result["composition"]["version"] = "v4"
    result["publishes"] = POSITIVE_TOTAL
    result["notes"] = (
        "Publishes the exact seven-family positive-interest line-1 basis for "
        "Schedule B threshold admission. It is not taxable interest after the "
        "three explicit adjustment classes and makes no broader completeness claim."
    )
    return result


def _positive_composition_v4() -> dict[str, Any]:
    result = _load(CONTENT / "interest-composition.v3.json")
    result["version"] = "v4"
    result["publishes"] = POSITIVE_TOTAL
    result["required_universe"]["claim"] = (
        "Seven declared positive taxable-interest families forming the gross "
        "Schedule B Part I line-1 basis, without subtractive adjustments."
    )
    return result


def _line2b_field_v5() -> dict[str, Any]:
    result = _load(CONTENT / "form1040.line-2b.form-field.v4.json")
    result["version"] = "v5"
    result["description"] = (
        "Form 1040 (2025), line 2b: exact seven-family positive taxable interest "
        "less the three separately closed Schedule B adjustment classes: Nominee "
        "Distribution, Accrued Interest, and ABP Adjustment."
    )
    result["dispositions"]["published_value"]["explain"] = (
        "A current cited derived finding publishes the seven-family positive "
        "interest total less the exact contributed and closed Schedule B "
        "adjustment classes."
    )
    result["dispositions"]["guard_inapplicable"]["explain"] = (
        "No taxable-interest value is published because the explicit adjustment "
        "classes exceed the positive-interest basis."
    )
    return result


def _schedule_b_v4() -> dict[str, Any]:
    result = _load(CONTENT / "rule.attachment.schedule-b.v3.json")
    result["version"] = "v4"
    result["schema"] = "attachment-rule.v6"
    result["title"] = (
        "Schedule B (Interest and Ordinary Dividends): Part I lists the exact "
        "seven-family positive interest sources, then the exact adjustment rows "
        "Nominee Distribution, Accrued Interest, and ABP Adjustment; the final "
        "Part I result subtracts those rows and ties to line 2b. Part II, Part "
        "III, threshold, and citation contracts are unchanged."
    )
    result["requirement"]["subtotals"] = [POSITIVE_TOTAL, "tax.us.2025.dividends.ordinary-total"]
    part_i = result["itemizations"][0]
    part_i["authority"]["composition"]["version"] = "v4"
    positive_symbols = [row["subtotal_symbol"] for row in part_i["row_sets"]]
    part_i["adjustment_rows"] = []
    for token, kind, label, _boundary in CLASSES:
        ids = _ids(token)
        part_i["adjustment_rows"].append({
            "kind": kind,
            "label": label,
            "rows": {
                "op": "collect_members",
                "member_fact_type": {"id": ids["amount"], "version": "v1"},
                "source_family": {"id": ids["family"], "version": "v1"},
            },
            "subtotal_symbol": ids["subtotal"],
            "sign": "negative",
        })
    adjustment_symbols = [row["subtotal_symbol"] for row in part_i["adjustment_rows"]]
    part_i["tie_out"] = {
        "line_symbol": "tax.us.2025.interest.taxable-total",
        "operation": "subtract",
        "positive_subtotals": positive_symbols,
        "adjustment_subtotals": adjustment_symbols,
    }
    part_ii = result["itemizations"][1]
    part_ii["adjustment_rows"] = []
    part_ii["tie_out"] = {
        "line_symbol": part_ii["tie_out"]["line_symbol"],
        "operation": "subtract",
        "positive_subtotals": [row["subtotal_symbol"] for row in part_ii["row_sets"]],
        "adjustment_subtotals": [],
    }
    return result


def render_content_files() -> dict[str, dict[str, Any]]:
    citizens: dict[str, dict[str, Any]] = {}
    for token, kind, label, boundary in CLASSES:
        citizens[f"scheduleb-adjustment.{token}.bundle.json"] = _bundle(token, kind, label, boundary)
        citizens[f"family.scheduleb-adjustment.{token}.json"] = _family(token, kind, label, boundary)
        citizens[f"closure-mapping.scheduleb-adjustment.{token}.json"] = _mapping(token)
        citizens[f"citation.scheduleb-adjustment.{token}.json"] = _citation(token, label)
        citizens[f"rule.scheduleb-adjustment.{token}-subtotal.json"] = _subtotal_rule(token, label)

    citizens["rule.form1040-line2b.v4.json"] = _line2b_v4()
    citizens["interest-composition.v4.json"] = _positive_composition_v4()
    citizens["rule.interest-positive-total.json"] = _positive_total_rule()
    citizens["form1040.line-2b.form-field.v5.json"] = _line2b_field_v5()
    citizens["rule.attachment.schedule-b.v4.json"] = _schedule_b_v4()

    package = _load_core_predecessor()
    package["schema"] = SUCCESSOR_PACKAGE_SCHEMA
    package["version"] = f"v{SUCCESSOR_PACKAGE_VERSION}"
    package["admitted_schemas"] = sorted(set(package["admitted_schemas"]) | {"attachment-rule.v6"})
    package["composition_obligations"] = sorted(set(package["composition_obligations"]) | {POSITIVE_TOTAL, "tax.us.2025.interest.taxable-total"})
    replacements = {
        "tax.us.2025.rule.form1040-line2b": {"role": "computation", "schema": "rule-artifact.v3", "version": "v4"},
        "tax.us.2025.form1040.line-2b": {"role": "form-field", "schema": "form-field.v3", "version": "v5"},
        "tax.us.2025.rule.attachment.schedule-b": {"role": "attachment-rule", "schema": "attachment-rule.v6", "version": "v4"},
        # Forward replacement: select only composition v4. Published v3 remains in
        # the registry; it must not remain a selected package member.
        "tax.us.2025.interest-composition": {
            "role": "composition",
            "schema": "taxable-interest-composition.v1",
            "version": "v4",
        },
    }
    members: list[dict[str, Any]] = []
    for member in package["members"]:
        replacement = replacements.get(member["id"])
        members.append({"id": member["id"], **replacement} if replacement else dict(member))
    members.append({
        "id": "tax.us.2025.rule.interest-positive-total",
        "role": "computation",
        "schema": "rule-artifact.v3",
        "version": "v1",
    })
    for token, _kind, _label, _boundary in CLASSES:
        ids = _ids(token)
        members.extend([
            {"id": ids["bundle"], "role": "fact-type-bundle", "schema": "bundle.v2", "version": "v1"},
            {"id": ids["family"], "role": "source-family", "schema": "source-family.v1", "version": "v1"},
            {"id": ids["mapping"], "role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "version": "v1"},
            {"id": ids["citation"], "role": "citation", "schema": "citation.v1", "version": "v1"},
            {"id": ids["rule"], "role": "computation", "schema": "rule-artifact.v3", "version": "v1"},
        ])
    package["members"] = sorted(members, key=lambda member: (member["id"], member["version"]))
    package["entrypoints"] = [
        ({"id": entry["id"], "version": "v4"} if entry["id"] == "tax.us.2025.rule.attachment.schedule-b" else dict(entry))
        for entry in package["entrypoints"]
    ]
    package["package_checksum"] = _package_checksum(package)
    citizens["package.core-calculations.v15.json"] = package

    registry = _load_registry_predecessor()
    existing_citizens = {(c["id"], c["version"]) for c in registry["citizens"]}
    for citizen in citizens.values():
        if citizen.get("schema", "").startswith("artifact-package."):
            continue
        key = (citizen["id"], citizen["version"])
        if key not in existing_citizens:
            registry["citizens"].append({"id": citizen["id"], "version": citizen["version"], "checksum": _checksum(citizen)})
            existing_citizens.add(key)
    registry["citizens"] = sorted(registry["citizens"], key=lambda row: (row["id"], row["version"]))
    existing_pkgs = {(p["id"], p["version"]) for p in registry["packages"]}
    if (package["id"], "v15") not in existing_pkgs:
        registry["packages"].append({"id": package["id"], "version": "v15", "checksum": package["package_checksum"]})
    registry["packages"] = sorted(registry["packages"], key=lambda row: (row["id"], row["version"]))
    citizens["published-packages.v10.json"] = registry
    return citizens


def render_fixture_files(citizens: dict[str, dict[str, Any]]) -> dict[Path, bytes]:
    registry_bytes = _document(citizens["published-packages.v10.json"])
    package = citizens["package.core-calculations.v15.json"]
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v8",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v15",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-03T12:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {"id": package["id"], "version": "v15", "checksum": package["package_checksum"]},
            "release": {"id": "demo.release.2025", "version": "v8", "checksum": hashlib.sha256(release_bytes).hexdigest()},
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 15,
            "supersedes": "demo.act.adopt.core.v14",
            "audit": {"note": "synthetic Schedule B interest-adjustment successor adoption; non-authoritative"},
        },
    }
    return {
        FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v8.json": release_bytes,
        FIXTURES / "adoptions" / "adopt-core-v15-current.json": _document(adoption),
    }


def render_all() -> dict[Path, bytes]:
    citizens = render_content_files()
    content_files = {CONTENT / name: _document(value) for name, value in citizens.items()}
    return {**content_files, **render_fixture_files(citizens)}


def main() -> None:
    for path, body in render_all().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
