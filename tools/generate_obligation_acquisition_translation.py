"""Generate the Document and Ordinary-Fact Translation Vertical package set.

Deterministic and additive over the ratified v33 core-calculations package:
v34 admits ``source-family.v3`` (the required cross-family
``identity_association`` successor minted by this milestone's Track 2) and
wires in the canonical obligation-acquisition slice --- the ordinary-fact
bundle, the canonical and scalar families, their closure mappings, the adopted
subtotal rule, and the line-2b and Schedule B successors that consume them.

No existing citizen bytes are rewritten in place. ``rule.form1040-line2b``
v4, ``form1040.line-2b.form-field`` v5, and ``rule.attachment.schedule-b`` v4
remain untouched on disk and simply stop being v34 package members, following
this corpus's established successor-version precedent.

The Schedule B successor is not optional presentation polish. Its Part I
tie-out declaration must list exactly the adjustment subtotals its own
adjustment rows carry (``runner.py`` ``tie_out_declaration``), so line 2b
cannot subtract a fourth adjustment class without Schedule B rendering it.

Every identity here is obviously synthetic (``demo.*``) and every amount is
invented. Nothing in this generator, the content it emits, or the fixtures it
writes derives from a real document or a real return.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "obligation_acquisition_translation"

# The canonical slice's own new citizens.
_NEW_MEMBER_FILES = (
    "obligation-acquisition.bundle.json",
    "family.obligation-acquisition.json",
    "family.obligation-accrued-interest-paid.json",
    "closure-mapping.obligation-acquisition.json",
    "closure-mapping.obligation-accrued-interest-paid.json",
    "rule.obligation-accrued-interest-subtotal.json",
    "rule.form1040-line2b.v5.json",
    "form1040.line-2b.form-field.v6.json",
    "rule.attachment.schedule-b.v5.json",
)

# (id, version) pairs superseded by the members above.
_SUPERSEDED = (
    ("tax.us.2025.rule.form1040-line2b", "v4"),
    ("tax.us.2025.form1040.line-2b", "v5"),
    ("tax.us.2025.rule.attachment.schedule-b", "v4"),
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
    elif schema.startswith("form-field."):
        role = "form-field"
    elif schema == "citation.v1":
        role = "citation"
    elif schema.startswith("source-family."):
        role = "source-family"
    elif schema == "source-closure-mapping.v2":
        role = "source-closure-mapping"
    elif schema.startswith("bundle."):
        role = "fact-type-bundle"
    elif schema == "parameter-declaration.v1":
        role = "parameter"
    elif schema.startswith("attachment-rule."):
        role = "attachment-rule"
    else:
        raise AssertionError(f"unhandled schema for member pin: {schema}")
    return {"id": citizen["id"], "role": role, "schema": schema, "version": citizen["version"]}


def build_package() -> dict[str, Any]:
    package = _load("package.core-calculations.v33.json")
    package["schema"] = "artifact-package.v26"
    package["version"] = "v34"

    superseded = set(_SUPERSEDED)
    members = [
        dict(member)
        for member in package["members"]
        if (member["id"], member["version"]) not in superseded
    ]
    for name in _NEW_MEMBER_FILES:
        members.append(_member_pin(_load(name)))
    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))
    package["admitted_schemas"] = sorted(
        set(package["admitted_schemas"]) | {"source-family.v3", "attachment-rule.v9"}
    )

    members_by_id = {m["id"]: m for m in package["members"]}
    superseded_ids = {member_id for member_id, _ in _SUPERSEDED}
    entrypoints = [
        dict(entry) for entry in package["entrypoints"] if entry["id"] not in superseded_ids
    ]
    new_entrypoint_ids = superseded_ids | {
        "tax.us.2025.obligation.acquisition",
        "tax.us.2025.obligation.accrued-interest-paid",
        "tax.us.2025.obligation.acquisition.vocabulary",
        "tax.us.2025.closure-mapping.obligation-acquisition",
        "tax.us.2025.closure-mapping.obligation-accrued-interest-paid",
        "tax.us.2025.rule.obligation-accrued-interest-subtotal",
    }
    for entry_id in sorted(new_entrypoint_ids):
        entrypoints.append({"id": entry_id, "version": members_by_id[entry_id]["version"]})
    package["entrypoints"] = [
        {"id": eid, "version": ver}
        for eid, ver in sorted({(e["id"], e["version"]) for e in entrypoints})
    ]

    package["package_checksum"] = _checksum(package)
    return package


def build_registry(package: dict[str, Any]) -> dict[str, Any]:
    registry = _load("published-packages.v28.json")
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _NEW_MEMBER_FILES:
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
        "version": "v27",
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
        "act_id": "demo.act.adopt.core.v34",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-28T12:00:00Z",
        "committed_against": 0,
        "payload": {
            "package": {
                "id": package["id"],
                "version": package["version"],
                "checksum": package_entry["checksum"],
            },
            "release": {
                "id": release["id"],
                "version": release["version"],
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 34,
            "audit": {
                "note": "synthetic Document and Ordinary-Fact Translation Vertical adoption; non-authoritative"
            },
        },
    }


def render_all() -> dict[Path, bytes]:
    package = build_package()
    registry = build_registry(package)

    out: dict[Path, bytes] = {
        CONTENT / "package.core-calculations.v34.json": _bytes(package),
        CONTENT / "published-packages.v29.json": _bytes(registry),
    }

    registry_bytes = out[CONTENT / "published-packages.v29.json"]
    release = build_release(registry_bytes)
    release_bytes = _bytes(release)
    adoption = build_adoption(package, registry, release, release_bytes)

    out[FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v27.json"] = release_bytes
    out[FIXTURES / "adoptions" / "adopt-core-v34-current.json"] = _bytes(adoption)
    return out


def main() -> None:
    for path, body in render_all().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
