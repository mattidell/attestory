"""Generate the ADR-0055 core-package v12 successor.

Deterministic, additive over the immutable v11 core-calculations package:
swaps the Schedule D attachment member from attachment.schedule-d v1
(attachment-rule.v3, presence-only completeness) to attachment.schedule-d v2
(attachment-rule.v4, value-checked completeness for the seven boundary
declarations). v11 remains historical; no existing citizen bytes are
rewritten in place, only new versions/citizens are added and a new package
version references them.
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


_NEW_CITIZEN_FILES = (
    "attachment.schedule-d.v2.json",
)

_VERSION_BUMPS = {
    "tax.us.2025.rule.attachment.schedule-d": "v2",
}

_MEMBER_SCHEMA_BUMPS = {
    "tax.us.2025.rule.attachment.schedule-d": "attachment-rule.v4",
}


def render() -> dict[str, bytes]:
    rendered: dict[str, bytes] = {}

    package_v12 = _load("package.core-calculations.v11.json")
    package_v12["schema"] = "artifact-package.v8"
    package_v12["version"] = "v12"
    package_v12["members"] = [dict(member) for member in package_v12["members"]]
    for member in package_v12["members"]:
        bumped = _VERSION_BUMPS.get(member["id"])
        if bumped is not None:
            member["version"] = bumped
        schema_bump = _MEMBER_SCHEMA_BUMPS.get(member["id"])
        if schema_bump is not None:
            member["schema"] = schema_bump
    package_v12["admitted_schemas"] = sorted(
        (set(package_v12["admitted_schemas"]) | {"attachment-rule.v4"}) - {"attachment-rule.v3"}
    )
    package_v12["entrypoints"] = [
        {"id": "tax.us.2025.rule.attachment.schedule-d", "version": "v2"}
        if entry["id"] == "tax.us.2025.rule.attachment.schedule-d"
        else dict(entry)
        for entry in package_v12["entrypoints"]
    ]
    package_v12["package_checksum"] = _checksum(package_v12)
    rendered["package.core-calculations.v12.json"] = _bytes(package_v12)

    registry = _load("published-packages.v6.json")
    package_entries = [
        dict(entry)
        for entry in registry["packages"]
        if (entry["id"], entry["version"]) != (package_v12["id"], package_v12["version"])
    ]
    package_entries.append(
        {"id": package_v12["id"], "version": package_v12["version"], "checksum": package_v12["package_checksum"]}
    )
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _NEW_CITIZEN_FILES:
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
    rendered["published-packages.v7.json"] = _bytes(registry)
    return rendered


def main() -> None:
    for relative, content in render().items():
        (CONTENT / relative).write_bytes(content)
        print(f"wrote {relative}")


if __name__ == "__main__":
    main()
