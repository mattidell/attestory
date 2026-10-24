"""Build the additive mortgage Track 2 consumer package/release successor."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages/content/tax/2025"
RELEASES = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
NEW_CITIZENS = ("rule.form1040-line12e.v2.json", "attachment.schedule-a.v2.json")


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _checksum(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build() -> dict[Path, bytes]:
    package = _load(CONTENT / "package.core-calculations.v54.json")
    package["version"] = "v55"
    new_citizens = [_load(CONTENT / name) for name in NEW_CITIZENS]
    new_versions = {(citizen["id"], citizen["version"]): citizen for citizen in new_citizens}
    package["members"] = [
        member for member in package["members"]
        if (member["id"], member["version"]) not in {
            ("tax.us.2025.rule.form1040-line12e", "v1"),
            ("tax.us.2025.rule.attachment.schedule-a", "v1"),
        }
    ]
    for citizen in new_citizens:
        schema = citizen["schema"]
        role = citizen.get("role", "attachment-rule" if schema.startswith("attachment-rule.") else None)
        assert isinstance(role, str)
        package["members"].append({"id": citizen["id"], "role": role, "schema": schema, "version": citizen["version"]})
    package["members"] = sorted(package["members"], key=lambda member: (member["id"], member["version"]))
    entries = {(entry["id"], entry["version"]) for entry in package["entrypoints"]}
    entries.discard(("tax.us.2025.rule.form1040-line12e", "v1"))
    entries.discard(("tax.us.2025.rule.attachment.schedule-a", "v1"))
    entries.update(new_versions)
    package["entrypoints"] = [{"id": identifier, "version": version} for identifier, version in sorted(entries)]
    package.pop("package_checksum", None)
    package["package_checksum"] = _checksum(package)

    registry = _load(CONTENT / "published-packages.v52.json")
    citizen_entries = list(registry["citizens"])
    for citizen in new_citizens:
        citizen_entries.append({"id": citizen["id"], "version": citizen["version"], "checksum": _checksum(citizen)})
    registry["citizens"] = sorted(citizen_entries, key=lambda entry: (entry["id"], entry["version"]))
    registry["packages"] = sorted(
        list(registry["packages"]) + [{"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]}],
        key=lambda entry: (entry["id"], entry["version"]),
    )
    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": "v53",
        "package_registry_sha256": hashlib.sha256(_document(registry)).hexdigest(),
    }
    return {
        CONTENT / "package.core-calculations.v55.json": _document(package),
        CONTENT / "published-packages.v53.json": _document(registry),
        RELEASES / "demo.release.sli-worksheet-integration.2025.v53.json": _document(release),
    }


if __name__ == "__main__":
    for path, content in build().items():
        path.write_bytes(content)
