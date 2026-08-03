"""Generate the Track 3 core-package v13 successor: Schedule D form-field citizens.

Deterministic, additive over the immutable v12 core-calculations package: adds
form-field citizens binding Schedule D line 8a column (h), line 13, line 15,
and line 16 (ADR-0052 Decision 3). Line 7a/9/16 (Form 1040) field citizens
are unchanged - they already bind tax.us.2025.capital-gains.line7a-total,
tax.us.2025.income.total-income, and tax.us.2025.tax.total-tax, exactly the
symbols the Track-2/ADR-0055 producers still publish. v12 remains historical;
only new versions/citizens are added and a new package version references
them.
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
    "schedule-d.line-8a.form-field.json",
    "schedule-d.line-13.form-field.json",
    "schedule-d.line-15.form-field.json",
    "schedule-d.line-16.form-field.json",
)

_NEW_MEMBERS = (
    {"role": "form-field", "schema": "form-field.v3", "id": "tax.us.2025.schedule-d.line-8a", "version": "v1"},
    {"role": "form-field", "schema": "form-field.v3", "id": "tax.us.2025.schedule-d.line-13", "version": "v1"},
    {"role": "form-field", "schema": "form-field.v3", "id": "tax.us.2025.schedule-d.line-15", "version": "v1"},
    {"role": "form-field", "schema": "form-field.v3", "id": "tax.us.2025.schedule-d.line-16", "version": "v1"},
)


def render() -> dict[str, bytes]:
    rendered: dict[str, bytes] = {}

    package_v13 = _load("package.core-calculations.v12.json")
    package_v13["version"] = "v13"
    package_v13["members"] = [dict(member) for member in package_v13["members"]] + [
        dict(m) for m in _NEW_MEMBERS
    ]
    package_v13["package_checksum"] = _checksum(package_v13)
    rendered["package.core-calculations.v13.json"] = _bytes(package_v13)

    registry = _load("published-packages.v7.json")
    package_entries = [
        dict(entry)
        for entry in registry["packages"]
        if (entry["id"], entry["version"]) != (package_v13["id"], package_v13["version"])
    ]
    package_entries.append(
        {"id": package_v13["id"], "version": package_v13["version"], "checksum": package_v13["package_checksum"]}
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
    rendered["published-packages.v8.json"] = _bytes(registry)
    return rendered


def main() -> None:
    for relative, content in render().items():
        (CONTENT / relative).write_bytes(content)
        print(f"wrote {relative}")


if __name__ == "__main__":
    main()
