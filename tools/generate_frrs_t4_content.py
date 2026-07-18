"""Generate the immutable, synthetic Track-4 core-package v2 publication set.

The script deliberately reads the published v1 surface and writes only new
``v2`` citizens.  It is deterministic so the package registry, Track-3
publication release, and adoption fixtures can be checked as bytes rather than
hand-maintained copies.  It never reads a workspace or any user data.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"


def _bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load(name: str) -> dict[str, Any]:
    value = json.loads((CONTENT / name).read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _checksum(value: dict[str, Any]) -> str:
    body = {key: item for key, item in value.items() if key != "package_checksum"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def render() -> dict[str, bytes]:
    """Return every Track-4 public content byte, addressed by content filename."""
    rendered: dict[str, bytes] = {}

    # The old W-2 vocabulary lacks a quantity on its source amount.  A new
    # bundle version supplies the exact versioned fact surface; it does not
    # rewrite the historical bundle or facts.
    w2_bundle = _load("w2.bundle.json")
    w2_bundle["version"] = "v2"
    for fact in w2_bundle["fact_types"]:
        fact["version"] = "v2"
        if fact["id"] == "tax.us.2025.w2.box1-wages":
            fact["source_amount"] = True
            fact["quantity"] = {"id": "tax.us.2025.quantity.taxable-interest", "version": "v1"}
    rendered["w2.bundle.v2.json"] = _bytes(w2_bundle)

    # The old mapping rule predates v2 rule artifacts.  Its successor has the
    # same tax expression plus the mandatory v2 metadata pin array.
    wages_rule = _load("rule.wages-line1a.json")
    wages_rule["schema"] = "rule-artifact.v2"
    wages_rule["version"] = "v2"
    wages_rule["pins"] = []
    wages_rule["value"].pop("stage", None)
    wages_rule["notes"] = (
        "Aggregates the adopted W-2 family through its adopted closure mapping; "
        "an empty source set publishes zero only on a current literal-true closure."
    )
    rendered["rule.wages-line1a.v2.json"] = _bytes(wages_rule)

    family = {
        "schema": "source-family.v1",
        "id": "tax.us.2025.w2",
        "version": "v2",
        "title": "Form W-2 box 1 statement items, tax year 2025",
        "scope": {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"},
        "closure_claim": "Every furnished Form W-2 box 1 item for tax year 2025 is recorded.",
        "member_predicate": {"fact_type": "tax.us.2025.w2.box1-wages"},
        "authorizes_subtotal": "tax.us.2025.wages.total-w2-box1",
    }
    rendered["family.w2.v2.json"] = _bytes(family)
    mapping = {
        "schema": "source-closure-mapping.v2",
        "id": "tax.us.2025.closure-mapping.w2",
        "version": "v2",
        "family": {"id": family["id"], "version": family["version"]},
        "member_fact_type": {"id": "tax.us.2025.w2.box1-wages", "version": "v2"},
        "closure_fact_type": {"id": "tax.us.2025.w2.source-closure", "version": "v2"},
        "closure_horizon_key": "family-horizon",
        "admits_symbol": "tax.us.2025.wages.total-w2-box1",
        "admission": {"condition": "current-literal-true"},
    }
    rendered["closure-mapping.w2.v2.json"] = _bytes(mapping)

    role_canon = {
        "schema": "role-canon.v1",
        "id": "tax.us.2025.role-canon",
        "version": "v1",
        "roles": {
            "parameter": "declared parameter", "computation": "rule", "applicability": "rule",
            "field-mapping": "rule", "cross-form-bridge": "rule", "input": "derivation edge",
            "choice": "derivation edge", "default": "default provenance", "composition": "composition provenance",
            "citation": "citation metadata", "adoption": "adoption", "governance": "governance",
            "engine": "engine", "package": "package", "operation-semantics": "operation",
            "form-field": "presentation", "source-family": "family",
            "source-closure-mapping": "closure mapping", "fact-type": "exact fact",
            "fact-type-bundle": "wholesale fact bundle",
        },
    }
    rendered["role-canon.v1.json"] = _bytes(role_canon)

    package = _load("package.core-calculations.json")
    package["version"] = "v2"
    package["members"] = [dict(member) for member in package["members"]]
    package["admitted_schemas"].append("role-canon.v1")
    for member in package["members"]:
        if member["id"] == wages_rule["id"]:
            member.update({"role": "field-mapping", "schema": "rule-artifact.v2", "version": "v2"})
        elif member["id"] == w2_bundle["id"]:
            member["version"] = "v2"
    package["members"].extend([
        {"role": "fact-type-bundle", "schema": "bundle.v2", "id": "tax.us.2025.f1099int.vocabulary", "version": "v1"},
        {"role": "source-family", "schema": "source-family.v1", "id": family["id"], "version": family["version"]},
        {"role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "id": mapping["id"], "version": mapping["version"]},
        {"role": "parameter", "schema": "role-canon.v1", "id": role_canon["id"], "version": role_canon["version"]},
    ])
    package["entrypoints"].append({"id": role_canon["id"], "version": role_canon["version"]})
    package["package_checksum"] = _checksum(package)
    rendered["package.core-calculations.v2.json"] = _bytes(package)

    # Publication keeps every historical registry entry and appends exact
    # checksums for the new immutable generation.  The registry itself is the
    # published release input, so it is rendered from content rather than
    # edited separately.
    registry = _load("published-packages.json")
    package_entries = [dict(entry) for entry in registry["packages"] if (entry["id"], entry["version"]) != (package["id"], package["version"])]
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    package_entries.append({"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]})
    for name in ("w2.bundle.v2.json", "rule.wages-line1a.v2.json", "family.w2.v2.json", "closure-mapping.w2.v2.json", "role-canon.v1.json"):
        citizen = json.loads(rendered[name])
        citizen_entries = [entry for entry in citizen_entries if (entry["id"], entry["version"]) != (citizen["id"], citizen["version"])]
        citizen_entries.append({"id": citizen["id"], "version": citizen["version"], "checksum": hashlib.sha256(json.dumps(citizen, sort_keys=True, separators=(",", ":")).encode()).hexdigest()})
    registry["packages"] = sorted(package_entries, key=lambda entry: (entry["id"], entry["version"]))
    registry["citizens"] = sorted(citizen_entries, key=lambda entry: (entry["id"], entry["version"]))
    rendered["published-packages.json"] = _bytes(registry)
    return rendered


def main() -> None:
    for relative, content in render().items():
        (CONTENT / relative).write_bytes(content)


if __name__ == "__main__":
    main()
