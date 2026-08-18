"""Generate the Form 1098-E / Student Loan Interest Deduction Track 6
package/publication set.

Deterministic, additive over the ratified v32 core-calculations package
(main's own concurrently-adopted content as of this build): v33 wires in
Tracks 1-5's already-committed Form 1098-E / SLI citizens (never before an
actual package member) plus Track 6's own two new mints -- the Schedule 1
line-21 form-field and the Form 1098-E box-1 closure mapping -- so the ten
synthetic end-to-end disposition-path models
(docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md,
Track 6) can be run for real through ``live_coordinate_run``. No existing
citizen bytes are rewritten in place: the historical
rule.form1040-line11.json (v1), form1040.line-11.form-field.json, and
rule.attachment.schedule-1.json (v1) remain untouched on disk and simply
stop being v33 package members, mirroring this corpus's established
successor-version precedent (rule.form1040-line15 v1 -> v2 at v29).

Track 6 also required two additive substrate repairs, recorded here rather
than in this generator: rule-artifact.v6 (Track 1's multiply/divide
successor schema) was minted by Track 1 but never wired into
artifact-package's own schema chain or the runner/marshal/package_validation
rule-artifact.v4-shaped call sites -- see artifact-package.v25.schema.json
(v24's own true additive successor, since v24 itself is already claimed by
main's own concurrent content) and the accompanying edits to
packages/derivation/{live,marshal,package_validation}.py.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "f1098e_student_loan_interest_track6"

# Tracks 1-5 citizens: already committed on disk, never before a real
# package member.
_TRACKS_1_5_MEMBER_FILES = (
    "f1098e.bundle.json",
    "family.f1098e-1.json",
    "sli-scope.bundle.json",
    "parameter.sli-interest-cap.json",
    "parameter.sli-magi-phase-range.json",
    "parameter.sli-magi-threshold.json",
    "citation.form1040.sli-worksheet.json",
    "rule.sli-worksheet-line1-subtotal.json",
    "rule.sli-worksheet.json",
    "rule.schedule1-line26.json",
    "citation.schedule1.line-26.json",
    "citation.schedule1.line-21.json",
    "rule.attachment.schedule-1.v2.json",
    "rule.form1040-line10.json",
    "citation.form1040.line-10.json",
    "form1040.line-10.form-field.json",
    "rule.form1040-line11.v2.json",
    "citation.form1040.line-11a.json",
    "citation.form1040.line-11b.json",
    "form1040.line-11a.form-field.json",
    "form1040.line-11b.form-field.json",
)

# Track 6's own two new mints.
_TRACK6_MEMBER_FILES = (
    "closure-mapping.f1098e.1.json",
    "schedule1.line-21.form-field.json",
)

_ALL_NEW_MEMBER_FILES = _TRACKS_1_5_MEMBER_FILES + _TRACK6_MEMBER_FILES

# Historical citizens dropped from v32 membership (bytes untouched on disk;
# remain reachable through package versions v1-v31). Fully superseded:
# rule.form1040-line11 v2 replaces v1; form1040.line-11a/line-11b (both
# binding the same tax.us.2025.income.agi symbol, by T0-8 design) replace
# form1040.line-11; rule.attachment.schedule-1 v2 replaces v1.
_DROPPED_MEMBER_IDS = (
    "tax.us.2025.form1040.line-11",
    "tax.us.2025.citation.form1040.line-11",
)


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


def _member_pin(citizen: dict[str, Any]) -> dict[str, Any]:
    schema = citizen["schema"]
    if schema.startswith("rule-artifact."):
        role = citizen["role"]
    elif schema in ("form-field.v1", "form-field.v2", "form-field.v3"):
        role = "form-field"
    elif schema == "citation.v1":
        role = "citation"
    elif schema == "source-family.v1":
        role = "source-family"
    elif schema == "source-closure-mapping.v2":
        role = "source-closure-mapping"
    elif schema in ("bundle.v1", "bundle.v2"):
        role = "fact-type-bundle"
    elif schema == "parameter-declaration.v1":
        role = "parameter"
    elif schema.startswith("attachment-rule."):
        role = "attachment-rule"
    else:
        raise AssertionError(f"unhandled schema for member pin: {schema}")
    return {"id": citizen["id"], "role": role, "schema": schema, "version": citizen["version"]}


def build_package() -> dict[str, Any]:
    package = _load("package.core-calculations.v32.json")
    # rule-artifact.v6 (Track 1's multiply/divide successor) is new to this
    # package's own admitted-schema chain: artifact-package.v25 is v24's own
    # additive successor admitting it.
    package["schema"] = "artifact-package.v25"
    package["version"] = "v33"

    members = [dict(member) for member in package["members"] if member["id"] not in _DROPPED_MEMBER_IDS]
    # Drop the v1 line-11 and v1 attachment.schedule-1 members; their
    # successors are added below by (id, version)-unique replacement.
    members = [
        m for m in members
        if not (m["id"] == "tax.us.2025.rule.form1040-line11" and m["version"] == "v1")
        and not (m["id"] == "tax.us.2025.rule.attachment.schedule-1" and m["version"] == "v1")
    ]

    for name in _ALL_NEW_MEMBER_FILES:
        citizen = _load(name)
        members.append(_member_pin(citizen))

    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))
    package["admitted_schemas"] = sorted(set(package["admitted_schemas"]) | {"rule-artifact.v6"})

    entrypoints = [dict(e) for e in package["entrypoints"] if e["id"] not in _DROPPED_MEMBER_IDS]
    entrypoints = [
        e for e in entrypoints
        if not (e["id"] == "tax.us.2025.rule.form1040-line11")
        and not (e["id"] == "tax.us.2025.rule.attachment.schedule-1")
    ]
    new_entrypoint_ids = (
        "tax.us.2025.rule.form1040-line11",
        "tax.us.2025.rule.attachment.schedule-1",
        "tax.us.2025.rule.form1040-line10",
        "tax.us.2025.rule.sli-worksheet",
        "tax.us.2025.rule.sli-worksheet-line1-subtotal",
        "tax.us.2025.rule.schedule1-line26",
        "tax.us.2025.form1040.line-10",
        "tax.us.2025.form1040.line-11a",
        "tax.us.2025.form1040.line-11b",
        "tax.us.2025.schedule1.line-21",
        "tax.us.2025.f1098e.1",
        "tax.us.2025.closure-mapping.f1098e.1",
        "tax.us.2025.f1098e.vocabulary",
        "tax.us.2025.sli-scope.vocabulary",
    )
    members_by_id = {m["id"]: m for m in package["members"]}
    for entry_id in new_entrypoint_ids:
        member = members_by_id[entry_id]
        entrypoints.append({"id": entry_id, "version": member["version"]})
    package["entrypoints"] = sorted({(e["id"], e["version"]) for e in entrypoints})
    package["entrypoints"] = [{"id": eid, "version": ver} for eid, ver in package["entrypoints"]]

    package["package_checksum"] = _checksum(package)
    return package


def build_registry(package: dict[str, Any]) -> dict[str, Any]:
    registry = _load("published-packages.v27.json")
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _ALL_NEW_MEMBER_FILES:
        citizen = _load(name)
        key = (citizen["id"], citizen["version"])
        citizen_entries = [e for e in citizen_entries if (e["id"], e["version"]) != key]
        citizen_entries.append(
            {"id": citizen["id"], "version": citizen["version"], "checksum": _citizen_checksum(citizen)}
        )
    registry["citizens"] = sorted(citizen_entries, key=lambda e: (e["id"], e["version"]))

    package_entries = [dict(entry) for entry in registry["packages"]]
    package_entries.append(
        {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]}
    )
    registry["packages"] = sorted(package_entries, key=lambda e: (e["id"], e["version"]))
    return registry


def build_release(registry_bytes: bytes) -> dict[str, Any]:
    return {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v26",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }


def build_adoption(
    package: dict[str, Any], registry: dict[str, Any], release: dict[str, Any], release_bytes: bytes
) -> dict[str, Any]:
    package_entry = next(
        e for e in registry["packages"] if e["id"] == package["id"] and e["version"] == package["version"]
    )
    return {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v33",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-15T12:00:00Z",
        "committed_against": 0,
        "payload": {
            "package": {"id": package["id"], "version": package["version"], "checksum": package_entry["checksum"]},
            "release": {"id": release["id"], "version": release["version"], "checksum": hashlib.sha256(release_bytes).hexdigest()},
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 33,
            "audit": {"note": "synthetic Form 1098-E Student Loan Interest Deduction Track 6 adoption; non-authoritative"},
        },
    }


def render_all() -> dict[Path, bytes]:
    package = build_package()
    registry = build_registry(package)

    out: dict[Path, bytes] = {
        CONTENT / "package.core-calculations.v33.json": _bytes(package),
        CONTENT / "published-packages.v28.json": _bytes(registry),
    }

    registry_bytes = out[CONTENT / "published-packages.v28.json"]
    release = build_release(registry_bytes)
    release_bytes = _bytes(release)
    adoption = build_adoption(package, registry, release, release_bytes)

    out[FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v26.json"] = release_bytes
    out[FIXTURES / "adoptions" / "adopt-core-v33-current.json"] = _bytes(adoption)
    return out


def main() -> None:
    for path, body in render_all().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
