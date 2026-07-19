"""Generate the DSBS Track 2 core-package v5 successor set.

Deterministic, additive over the immutable v4 core-calculations package
(tools/generate_dsbs_t2_content.py): v5 folds in deliverables 5-8 - the
Schedule B attachment citizen (existence conditional, collect_members
itemization rows, tie-out, Part III completeness), its three new taxpayer-
assertion fact types, its own citation and threshold parameter. v4 remains
historical; no existing citizen bytes are rewritten in place, only new
citizens are added and a new package version references them.
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


# New citizens introduced directly as committed files (not generated).
_NEW_CITIZEN_FILES = (
    "scheduleb.bundle.json",
    "citation.schedule-b.json",
    "parameter.schedule-b-threshold.json",
    "rule.attachment.schedule-b.json",
)

_NEW_MEMBERS = (
    {"role": "fact-type-bundle", "schema": "bundle.v2", "id": "tax.us.2025.scheduleb.vocabulary", "version": "v1"},
    {"role": "citation", "schema": "citation.v1", "id": "tax.us.2025.citation.schedule-b", "version": "v1"},
    {"role": "parameter", "schema": "parameter-declaration.v1", "id": "tax.us.2025.parameter.schedule-b-threshold", "version": "v1"},
    {"role": "attachment-rule", "schema": "attachment-rule.v1", "id": "tax.us.2025.rule.attachment.schedule-b", "version": "v1"},
)


def render() -> dict[str, bytes]:
    rendered: dict[str, bytes] = {}

    package_v5 = _load("package.core-calculations.v4.json")
    package_v5["schema"] = "artifact-package.v4"
    package_v5["version"] = "v5"
    package_v5["members"] = [dict(member) for member in package_v5["members"]]
    package_v5["admitted_schemas"] = sorted(
        set(package_v5["admitted_schemas"]) | {"attachment-rule.v1"}
    )
    package_v5["members"].extend(dict(m) for m in _NEW_MEMBERS)
    # The package-graph reachability walker (package_validation.py) has no
    # adjacency case for attachment-rule.v1's requirement/itemizations/
    # completeness structure, nor for a bare fact-type.v2 member outside a
    # bundle (the same situation dividend-universe.v1 was in at v4) - every
    # new member this schedule needs is therefore its own declared root,
    # the same sanctioned mechanism v4 already used.
    package_v5["entrypoints"] = list(package_v5["entrypoints"]) + [
        {"id": "tax.us.2025.rule.attachment.schedule-b", "version": "v1"},
        {"id": "tax.us.2025.citation.schedule-b", "version": "v1"},
        {"id": "tax.us.2025.parameter.schedule-b-threshold", "version": "v1"},
        {"id": "tax.us.2025.scheduleb.vocabulary", "version": "v1"},
    ]
    package_v5["package_checksum"] = _checksum(package_v5)
    rendered["package.core-calculations.v5.json"] = _bytes(package_v5)

    registry = _load("published-packages.json")
    package_entries = [
        dict(entry)
        for entry in registry["packages"]
        if (entry["id"], entry["version"]) != (package_v5["id"], package_v5["version"])
    ]
    package_entries.append(
        {"id": package_v5["id"], "version": package_v5["version"], "checksum": package_v5["package_checksum"]}
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
