"""Generate the Schedule D covered-LTCG Track 2 core-package v11 successor.

Deterministic, additive over the immutable v10 core-calculations package:
folds in Track 1's already-published covered-long-term-gain identity/family/
completeness citizens (never wired into a package by Track 1) plus Track 2's
own new content - the twin scalar collectible companions (ADR-0054), the
Schedule D attachment and line 8a/13/15/16 content (ADR-0052 Decision 3), the
selected-preferential-base rule (ADR-0052 Decision 4 / ADR-0053 Decision 2),
and the line 7a/9/16 successors (ADR-0052 Decision 5/7). v10 remains
historical; no existing citizen bytes are rewritten in place, only new
versions/citizens are added and a new package version references them.
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


# Track 1 citizens already published (checksums not yet in the registry -
# Track 1 established these citizens without wiring them into a package):
_TRACK1_CITIZEN_FILES = (
    "family.f1099b-covered-ltcg.json",
    "closure-mapping.f1099b-covered-ltcg.json",
    "f1099b-covered-ltcg.bundle.json",
    "schedule-d-boundary.bundle.json",
)

_TRACK1_MEMBERS = (
    {"role": "fact-type-bundle", "schema": "bundle.v2", "id": "tax.us.2025.f1099b.covered-ltcg.vocabulary", "version": "v1"},
    {"role": "fact-type-bundle", "schema": "bundle.v2", "id": "tax.us.2025.schedule-d-boundary.vocabulary", "version": "v1"},
    {"role": "source-family", "schema": "source-family.v1", "id": "tax.us.2025.f1099b.covered-ltcg", "version": "v1"},
    {"role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "id": "tax.us.2025.closure-mapping.f1099b-covered-ltcg", "version": "v1"},
)

# Track 2's own new content citizens.
_NEW_CITIZEN_FILES = (
    "quantity.covered-ltcg-proceeds.json",
    "quantity.covered-ltcg-basis.json",
    "family.f1099b-covered-ltcg-proceeds.json",
    "family.f1099b-covered-ltcg-basis.json",
    "closure-mapping.f1099b-covered-ltcg-proceeds.json",
    "closure-mapping.f1099b-covered-ltcg-basis.json",
    "f1099b-covered-ltcg-scalars.bundle.json",
    "rule.f1099b-covered-ltcg-proceeds-subtotal.json",
    "rule.f1099b-covered-ltcg-basis-subtotal.json",
    "rule.schedule-d-line8a-gain.json",
    "rule.schedule-d-line15.json",
    "rule.schedule-d-line16.json",
    "rule.selected-preferential-base.json",
    "rule.form1040-line7a.v2.json",
    "rule.form1040-line9.v4.json",
    "rule.form1040-line16.v4.json",
    "attachment.schedule-d.json",
    "citation.attachment.schedule-d.json",
    "citation.schedule-d.line-8a.json",
    "citation.schedule-d.line-13.json",
    "citation.schedule-d.line-15.json",
    "citation.schedule-d.line-16.json",
)

_NEW_MEMBERS = (
    {"role": "parameter", "schema": "quantity-vocabulary.v4", "id": "tax.us.2025.quantity.covered-ltcg-proceeds", "version": "v1"},
    {"role": "parameter", "schema": "quantity-vocabulary.v4", "id": "tax.us.2025.quantity.covered-ltcg-basis", "version": "v1"},
    {"role": "source-family", "schema": "source-family.v1", "id": "tax.us.2025.f1099b.covered-ltcg-proceeds", "version": "v1"},
    {"role": "source-family", "schema": "source-family.v1", "id": "tax.us.2025.f1099b.covered-ltcg-basis", "version": "v1"},
    {"role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "id": "tax.us.2025.closure-mapping.f1099b-covered-ltcg-proceeds", "version": "v1"},
    {"role": "source-closure-mapping", "schema": "source-closure-mapping.v2", "id": "tax.us.2025.closure-mapping.f1099b-covered-ltcg-basis", "version": "v1"},
    {"role": "fact-type-bundle", "schema": "bundle.v2", "id": "tax.us.2025.f1099b.covered-ltcg-scalars.vocabulary", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v2", "id": "tax.us.2025.rule.f1099b-covered-ltcg-proceeds-subtotal", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v2", "id": "tax.us.2025.rule.f1099b-covered-ltcg-basis-subtotal", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v3", "id": "tax.us.2025.rule.schedule-d-line8a-gain", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v3", "id": "tax.us.2025.rule.schedule-d-line15", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v3", "id": "tax.us.2025.rule.schedule-d-line16", "version": "v1"},
    {"role": "computation", "schema": "rule-artifact.v3", "id": "tax.us.2025.rule.selected-preferential-base", "version": "v1"},
    {"role": "attachment-rule", "schema": "attachment-rule.v3", "id": "tax.us.2025.rule.attachment.schedule-d", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.attachment.schedule-d", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.schedule-d.line-8a", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.schedule-d.line-13", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.schedule-d.line-15", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.schedule-d.line-16", "version": "v1"},
)

_VERSION_BUMPS = {
    "tax.us.2025.rule.form1040-line7a": "v2",
    "tax.us.2025.rule.form1040-line9": "v4",
    "tax.us.2025.rule.form1040-line16": "v4",
}

_NEW_ENTRYPOINTS = (
    {"id": "tax.us.2025.f1099b.covered-ltcg.vocabulary", "version": "v1"},
    {"id": "tax.us.2025.schedule-d-boundary.vocabulary", "version": "v1"},
    {"id": "tax.us.2025.f1099b.covered-ltcg-scalars.vocabulary", "version": "v1"},
    {"id": "tax.us.2025.f1099b.covered-ltcg", "version": "v1"},
    {"id": "tax.us.2025.f1099b.covered-ltcg-proceeds", "version": "v1"},
    {"id": "tax.us.2025.f1099b.covered-ltcg-basis", "version": "v1"},
    {"id": "tax.us.2025.rule.attachment.schedule-d", "version": "v1"},
    {"id": "tax.us.2025.citation.attachment.schedule-d", "version": "v1"},
    {"id": "tax.us.2025.citation.schedule-d.line-13", "version": "v1"},
    {"id": "tax.us.2025.rule.selected-preferential-base", "version": "v1"},
)


def render() -> dict[str, bytes]:
    rendered: dict[str, bytes] = {}

    package_v11 = _load("package.core-calculations.v10.json")
    package_v11["schema"] = "artifact-package.v7"
    package_v11["version"] = "v11"
    package_v11["members"] = [dict(member) for member in package_v11["members"]]
    for member in package_v11["members"]:
        bumped = _VERSION_BUMPS.get(member["id"])
        if bumped is not None:
            member["version"] = bumped
    package_v11["admitted_schemas"] = sorted(
        set(package_v11["admitted_schemas"]) | {"attachment-rule.v3", "quantity-vocabulary.v4"}
    )
    package_v11["members"].extend(dict(m) for m in _TRACK1_MEMBERS)
    package_v11["members"].extend(dict(m) for m in _NEW_MEMBERS)
    package_v11["entrypoints"] = [
        {"id": "tax.us.2025.rule.form1040-line16", "version": "v4"}
        if entry["id"] == "tax.us.2025.rule.form1040-line16"
        else {"id": "tax.us.2025.rule.form1040-line7a", "version": "v2"}
        if entry["id"] == "tax.us.2025.rule.form1040-line7a"
        else {"id": "tax.us.2025.rule.form1040-line9", "version": "v4"}
        if entry["id"] == "tax.us.2025.rule.form1040-line9"
        else dict(entry)
        for entry in package_v11["entrypoints"]
    ] + [dict(e) for e in _NEW_ENTRYPOINTS]
    package_v11["package_checksum"] = _checksum(package_v11)
    rendered["package.core-calculations.v11.json"] = _bytes(package_v11)

    registry = _load("published-packages.v5.json")
    package_entries = [
        dict(entry)
        for entry in registry["packages"]
        if (entry["id"], entry["version"]) != (package_v11["id"], package_v11["version"])
    ]
    package_entries.append(
        {"id": package_v11["id"], "version": package_v11["version"], "checksum": package_v11["package_checksum"]}
    )
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _TRACK1_CITIZEN_FILES + _NEW_CITIZEN_FILES:
        citizen = _load(name)
        citizen_entries = [
            entry for entry in citizen_entries
            if (entry["id"], entry["version"]) != (citizen["id"], citizen["version"])
        ]
        citizen_entries.append(
            {"id": citizen["id"], "version": citizen["version"], "checksum": _citizen_checksum(citizen)}
        )
    registry["packages"] = sorted(package_entries, key=lambda entry: (entry["id"], entry["version"]))
    registry["citizens"] = sorted(citizen_entries, key=lambda entry: (entry["id"], entry["version"]))
    rendered["published-packages.v6.json"] = _bytes(registry)
    return rendered


def main() -> None:
    for relative, content in render().items():
        (CONTENT / relative).write_bytes(content)
        print(f"wrote {relative}")


if __name__ == "__main__":
    main()
