"""Generate the Document/Ordinary-Fact Translation package-membership successors.

Two additive successors over the published v33 core-calculations package
(v28 registry, v26 release), matching the genuine two-stage migration
design ``rule.form1040-line2b`` itself already carries (a coexistence
successor, then a migrated successor reached only through a real
migration-adoption act):

- **v34 (coexistence)**: wires every seam citizen Integration mints --
  Seam 2 association, Seam 3 per-pairing and aggregate accrued-interest
  supportability, Seam 5's two consequence rules, the pairing-scoped
  current-year-adjustment subtotal -- and admits the coexistence
  ``rule.form1040-line2b`` v5, which still subtracts the incumbent
  form-row accrued-interest subtotal *and* the new pairing-scoped
  subtotal. The legacy Schedule B accrued-interest source-family,
  fact-type-bundle vocabulary, source-closure-mapping, and form-row
  subtotal rule all remain package members, unedited, exactly as on v33:
  a workspace that has adopted the new seams but has not yet run a
  migration-adoption act still resolves and computes through them. Only
  the real ``rule.form1040-line2b`` v4 stops being a v34 member (mirroring
  this corpus's successor-version precedent, rule.form1040-line11
  v1 -> v2 at v33). The package schema moves to artifact-package.v26
  (already published) so the exclusive graph can pin rule-artifact.v7
  computation members.

- **v35 (migrated)**: additive over v34. Admits the migrated
  ``rule.form1040-line2b`` v6 (a single accrued-interest-shaped
  subtractand: only the pairing-scoped subtotal) and
  ``rule.attachment.schedule-b`` v5 in place of the coexistence v5 and the
  real v4 respectively, together with the migration-succession artifact
  and its migrated-claim vocabulary. The legacy Schedule B accrued-interest
  source-family, its fact-type-bundle vocabulary, its source-closure-
  mapping, and its form-row subtotal rule all stop being members here --
  the legacy input surface is retired for new obligations. A workspace
  reaches v6 only by also committing the
  ``scheduleb-accrued-interest.succession`` migration-adoption sequence
  (see ``tests/test_legacy_pairing_coexistence_migration.py``).

No existing citizen bytes are rewritten in place at either step: real v4,
the coexistence v5, the real schedule-b v4, and the legacy Schedule B
accrued-interest family/bundle/closure-mapping/subtotal rule all remain on
disk unedited, immutable history for whichever package generation a
workspace is actually pinned to.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "package_membership_wiring"

# --- v34 (coexistence) ---

_V34_NEW_MEMBER_FILES = (
    "obligation-acquisition.bundle.json",
    "pairing-scoped-consequences.bundle.json",
    "citation.basis-adjustment.accrued-interest.json",
    "rule.relationship.accrued-supported.json",
    "rule.interest.current-year-adjustment.pairing-scoped.json",
    "rule.basis.item-level-consequence.pairing-scoped.json",
    "rule.interest.current-year-adjustment-subtotal.json",
    "rule.interest.current-year-adjustment.aggregate-supportability.json",
    "rule.form1040-line2b.v5.json",
)
# Kept for backward-compatible import (test fixtures enumerate this set).
_NEW_MEMBER_FILES = _V34_NEW_MEMBER_FILES

_V34_DROPPED_MEMBERS = (
    ("tax.us.2025.rule.form1040-line2b", "v4"),
)

_V34_NEW_ENTRYPOINT_IDS = (
    "tax.us.obligation-acquisition.vocabulary",
    "tax.us.2025.pairing-scoped-consequences.vocabulary",
    "tax.us.2025.citation.basis-adjustment.accrued-interest",
    "tax.us.2025.rule.relationship.accrued-supported",
    "tax.us.2025.rule.interest.current-year-adjustment.pairing-scoped",
    "tax.us.2025.rule.basis.item-level-consequence.pairing-scoped",
    "tax.us.2025.rule.interest.current-year-adjustment-subtotal",
    "tax.us.2025.rule.interest.current-year-adjustment.aggregate-supportability",
    "tax.us.2025.rule.form1040-line2b",
)

# --- v35 (migrated), additive over v34 ---

_V35_NEW_MEMBER_FILES = (
    "rule.form1040-line2b.v6.json",
    "rule.attachment.schedule-b.v5.json",
    "scheduleb-accrued-interest.succession.json",
    "scheduleb-accrued-interest-migrated.bundle.json",
)

_V35_DROPPED_MEMBERS = (
    ("tax.us.2025.rule.form1040-line2b", "v5"),
    ("tax.us.2025.rule.attachment.schedule-b", "v4"),
    ("tax.us.2025.rule.scheduleb-adjustment.accrued-interest-subtotal", "v1"),
    ("tax.us.2025.scheduleb.adjustment.accrued-interest.vocabulary", "v1"),
    ("tax.us.2025.scheduleb.adjustment.accrued-interest", "v1"),
    ("tax.us.2025.closure-mapping.scheduleb-adjustment.accrued-interest", "v1"),
)

_V35_NEW_ENTRYPOINT_IDS = (
    "tax.us.2025.rule.form1040-line2b",
    "tax.us.2025.rule.attachment.schedule-b",
    "tax.us.2025.scheduleb-accrued-interest.succession",
    "tax.us.2025.interest.accrued-interest-migrated.vocabulary",
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
    elif schema == "migration-artifact.v1":
        role = "migration-artifact"
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


def _apply_step(
    package: dict[str, Any],
    *,
    version: str,
    new_member_files: tuple[str, ...],
    dropped_members: tuple[tuple[str, str], ...],
    new_entrypoint_ids: tuple[str, ...],
    admitted_schema_additions: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    package = dict(package)
    package["schema"] = "artifact-package.v26"
    package["version"] = version

    members = [
        dict(member)
        for member in package["members"]
        if (member["id"], member["version"]) not in dropped_members
    ]
    for name in new_member_files:
        citizen = _load(name)
        key = (citizen["id"], citizen["version"])
        members = [m for m in members if (m["id"], m["version"]) != key]
        members.append(_member_pin(citizen))
    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))
    package["admitted_schemas"] = sorted(set(package["admitted_schemas"]) | admitted_schema_additions)

    entrypoints = [
        dict(e)
        for e in package["entrypoints"]
        if (e["id"], e["version"]) not in dropped_members
    ]
    members_latest = {m["id"]: m for m in package["members"]}
    seen_entrypoints = {(e["id"], e["version"]) for e in entrypoints}
    for entry_id in new_entrypoint_ids:
        member = members_latest[entry_id]
        key = (entry_id, member["version"])
        if key not in seen_entrypoints:
            entrypoints.append({"id": entry_id, "version": member["version"]})
            seen_entrypoints.add(key)
    package["entrypoints"] = sorted({(e["id"], e["version"]) for e in entrypoints})
    package["entrypoints"] = [{"id": eid, "version": ver} for eid, ver in package["entrypoints"]]

    package["package_checksum"] = _checksum(package)
    return package


def build_package() -> dict[str, Any]:
    """v34, the coexistence successor. Kept as the default ``build_package``
    for backward-compatible callers/tests that only need one generation."""
    base = _load("package.core-calculations.v33.json")
    return _apply_step(
        base,
        version="v34",
        new_member_files=_V34_NEW_MEMBER_FILES,
        dropped_members=_V34_DROPPED_MEMBERS,
        new_entrypoint_ids=_V34_NEW_ENTRYPOINT_IDS,
        admitted_schema_additions=frozenset({"rule-artifact.v7"}),
    )


def build_migrated_package(coexistence_package: dict[str, Any]) -> dict[str, Any]:
    """v35, additive over v34: the migrated successor."""
    return _apply_step(
        coexistence_package,
        version="v35",
        new_member_files=_V35_NEW_MEMBER_FILES,
        dropped_members=_V35_DROPPED_MEMBERS,
        new_entrypoint_ids=_V35_NEW_ENTRYPOINT_IDS,
    )


def build_registry(package: dict[str, Any], *, base_registry: dict[str, Any] | str = "published-packages.v28.json") -> dict[str, Any]:
    registry = _load(base_registry) if isinstance(base_registry, str) else dict(base_registry)
    new_member_files = _V34_NEW_MEMBER_FILES if package["version"] == "v34" else _V35_NEW_MEMBER_FILES
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in new_member_files:
        citizen = _load(name)
        key = (citizen["id"], citizen["version"])
        citizen_entries = [e for e in citizen_entries if (e["id"], e["version"]) != key]
        citizen_entries.append(
            {"id": citizen["id"], "version": citizen["version"], "checksum": _citizen_checksum(citizen)}
        )
    registry["citizens"] = sorted(citizen_entries, key=lambda e: (e["id"], e["version"]))

    package_entries = [dict(entry) for entry in registry["packages"]]
    package_entries = [
        e for e in package_entries if not (e["id"] == package["id"] and e["version"] == package["version"])
    ]
    package_entries.append(
        {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]}
    )
    registry["packages"] = sorted(package_entries, key=lambda e: (e["id"], e["version"]))
    return registry


def build_release(registry_bytes: bytes, *, version: str = "v27") -> dict[str, Any]:
    return {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": version,
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }


def build_adoption(
    package: dict[str, Any],
    registry: dict[str, Any],
    release: dict[str, Any],
    release_bytes: bytes,
    *,
    at: str = "2026-08-29T12:00:00Z",
) -> dict[str, Any]:
    package_entry = next(
        e for e in registry["packages"] if e["id"] == package["id"] and e["version"] == package["version"]
    )
    revision = int(package["version"].lstrip("v"))
    return {
        "schema": "act.v1",
        "act_id": f"demo.act.adopt.core.{package['version']}",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": at,
        "committed_against": 0,
        "payload": {
            "package": {"id": package["id"], "version": package["version"], "checksum": package_entry["checksum"]},
            "release": {
                "id": release["id"],
                "version": release["version"],
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": revision,
            "audit": {
                "note": "synthetic package-membership wiring of document/ordinary-fact translation seams; non-authoritative"
            },
        },
    }


def render_all() -> dict[Path, bytes]:
    coexistence_package = build_package()
    coexistence_registry = build_registry(coexistence_package, base_registry="published-packages.v28.json")

    out: dict[Path, bytes] = {
        CONTENT / "package.core-calculations.v34.json": _bytes(coexistence_package),
        CONTENT / "published-packages.v29.json": _bytes(coexistence_registry),
    }

    coexistence_registry_bytes = out[CONTENT / "published-packages.v29.json"]
    coexistence_release = build_release(coexistence_registry_bytes, version="v27")
    coexistence_release_bytes = _bytes(coexistence_release)
    coexistence_adoption = build_adoption(
        coexistence_package, coexistence_registry, coexistence_release, coexistence_release_bytes,
        at="2026-08-29T12:00:00Z",
    )

    out[FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v27.json"] = coexistence_release_bytes
    out[FIXTURES / "adoptions" / "adopt-core-v34-current.json"] = _bytes(coexistence_adoption)

    migrated_package = build_migrated_package(coexistence_package)
    migrated_registry = build_registry(migrated_package, base_registry=coexistence_registry)
    out[CONTENT / "package.core-calculations.v35.json"] = _bytes(migrated_package)
    out[CONTENT / "published-packages.v30.json"] = _bytes(migrated_registry)

    migrated_registry_bytes = out[CONTENT / "published-packages.v30.json"]
    migrated_release = build_release(migrated_registry_bytes, version="v28")
    migrated_release_bytes = _bytes(migrated_release)
    migrated_adoption = build_adoption(
        migrated_package, migrated_registry, migrated_release, migrated_release_bytes,
        at="2026-08-29T13:00:00Z",
    )

    out[FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v28.json"] = migrated_release_bytes
    out[FIXTURES / "adoptions" / "adopt-core-v35-current.json"] = _bytes(migrated_adoption)
    return out


def main() -> None:
    for path, body in render_all().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
