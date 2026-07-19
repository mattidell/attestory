"""Generate the DSBS Track 2 core-package v4 successor set.

Deterministic, additive over the immutable v3 core-calculations package
(tools/generate_frrs_t4_content.py): v4 folds in the Track 1 1099-DIV
schema citizens (family/closure-mapping/bundle/universe/quantities, already
published) plus Track 2's own new content - the box 1a/1b subtotal rules,
lines 3a/3b, the line-9 v2 extension, and their form-fields/citations. v3
remains historical; no existing citizen bytes are rewritten in place, only
new versions/citizens are added and a new package version references them.
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


def _citizen_checksum(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# New citizens introduced directly as committed files (not generated): the
# rule artifacts, form-fields, and citations already exist on disk under
# packages/content/tax/2025/. This script only assembles the new package
# version and the extended publication registry around them.
_NEW_CITIZEN_FILES = (
    "rule.f1099div-1a-subtotal.json",
    "rule.f1099div-1b-subtotal.json",
    "rule.form1040-line3a.json",
    "rule.form1040-line3b.json",
    "rule.form1040-line9.v2.json",
    "citation.form1040.line-3a.json",
    "citation.form1040.line-3b.json",
    "form1040.line-3a.form-field.json",
    "form1040.line-3b.form-field.json",
)

# Track 1 citizens already published (checksums already in the registry):
# reused as package members by pin only, never re-rendered.
_TRACK1_MEMBERS = (
    {"role": "fact-type-bundle", "schema": "bundle.v2", "id": "tax.us.2025.f1099div.vocabulary", "version": "v1"},
    {"role": "source-family", "schema": "source-family.v1", "id": "tax.us.2025.f1099div.1a", "version": "v1"},
    {"role": "source-family", "schema": "source-family.v1", "id": "tax.us.2025.f1099div.1b", "version": "v1"},
    {"role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "id": "tax.us.2025.closure-mapping.f1099div-1a", "version": "v1"},
    {"role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "id": "tax.us.2025.closure-mapping.f1099div-1b", "version": "v1"},
    {"role": "parameter", "schema": "quantity-vocabulary.v2", "id": "tax.us.2025.quantity.ordinary-dividends", "version": "v1"},
    {"role": "parameter", "schema": "quantity-vocabulary.v2", "id": "tax.us.2025.quantity.qualified-dividends", "version": "v1"},
    {"role": "dividend-universe", "schema": "dividend-universe.v1", "id": "tax.us.2025.dividend-universe", "version": "v1"},
)

_NEW_MEMBERS = (
    {"role": "computation", "schema": "rule-artifact.v2", "id": "tax.us.2025.rule.f1099div-1a-subtotal", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v2", "id": "tax.us.2025.rule.f1099div-1b-subtotal", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v2", "id": "tax.us.2025.rule.form1040-line3a", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v2", "id": "tax.us.2025.rule.form1040-line3b", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.form1040.line-3a", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.form1040.line-3b", "version": "v1"},
    {"role": "form-field", "schema": "form-field.v3", "id": "tax.us.2025.form1040.line-3a", "version": "v1"},
    {"role": "form-field", "schema": "form-field.v3", "id": "tax.us.2025.form1040.line-3b", "version": "v1"},
)


def render() -> dict[str, bytes]:
    rendered: dict[str, bytes] = {}

    package_v4 = _load("package.core-calculations.v3.json")
    package_v4["schema"] = "artifact-package.v4"
    package_v4["version"] = "v4"
    package_v4["members"] = [dict(member) for member in package_v4["members"]]
    for member in package_v4["members"]:
        if member["id"] == "tax.us.2025.rule.form1040-line9":
            member["version"] = "v2"
    package_v4["admitted_schemas"] = sorted(
        set(package_v4["admitted_schemas"]) | {"quantity-vocabulary.v2", "dividend-universe.v1", "form-field.v3"}
    )
    package_v4["members"].extend(dict(m) for m in _TRACK1_MEMBERS)
    package_v4["members"].extend(dict(m) for m in _NEW_MEMBERS)
    package_v4["entrypoints"] = list(package_v4["entrypoints"]) + [
        {"id": "tax.us.2025.dividend-universe", "version": "v1"},
    ]
    package_v4["package_checksum"] = _checksum(package_v4)
    rendered["package.core-calculations.v4.json"] = _bytes(package_v4)

    registry = _load("published-packages.json")
    package_entries = [
        dict(entry)
        for entry in registry["packages"]
        if (entry["id"], entry["version"]) != (package_v4["id"], package_v4["version"])
    ]
    package_entries.append(
        {"id": package_v4["id"], "version": package_v4["version"], "checksum": package_v4["package_checksum"]}
    )
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _NEW_CITIZEN_FILES:
        citizen = _load(name)
        citizen_entries = [
            entry for entry in citizen_entries if (entry["id"], entry["version"]) != (citizen["id"], citizen["version"])
        ]
        citizen_entries.append(
            {"id": citizen["id"], "version": citizen["version"], "checksum": _citizen_checksum(citizen)}
        )
    registry["packages"] = sorted(package_entries, key=lambda entry: (entry["id"], entry["version"]))
    registry["citizens"] = sorted(citizen_entries, key=lambda entry: (entry["id"], entry["version"]))
    rendered["published-packages.json"] = _bytes(registry)
    return rendered


def main() -> None:
    for relative, content in render().items():
        (CONTENT / relative).write_bytes(content)


if __name__ == "__main__":
    main()
