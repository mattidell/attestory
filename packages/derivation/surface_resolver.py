"""Surface artifact resolver: opaque UI bytes, the same authority chain (ADR-0033).

The artifact package (`production_resolver.py`) carries typed declarative rule
citizens whose whole member graph hard-validates. UI source and a vendored
dependency tree cannot be members of that: there is no way to "validate" a
`.svelte` file or a third-party npm package for meaning, and pretending
otherwise would just be a validator that always passes. So this is a second,
separate container, opened by its own owner adoption, carrying entries that
are never parsed or typed — only fingerprinted.

The authority chain is the same one Decisions 1 and 2 of ADR-0033 already
established, reused rather than reimplemented: a release-rooted, current-user
adoption; release bytes verified before registry entries authenticate supply.
This module calls into `production_resolver.py` for both. What differs is
Decision 3's shape: instead of a closed member graph validated by
`package_validation.validate_package`, a surface artifact is one manifest
citizen (itself verified the same way an `artifact-package.v4` instance is —
`package_instance_checksum` / `verify_published_package` against the
published registry) whose `entries` list is checked one raw file at a time by
SHA-256, never opened for meaning.

The owner adoption is a distinct act kind, `surface-adoption`, so a surface
artifact and a rule package sharing a scope can never tie or supersede one
another in `select_current_adoption`'s candidate pool. Its payload reuses
`act-package-adoption.v1` unchanged: that schema is already just an exact
`{id, version, checksum}` pin on a "package" and a "release", generic enough
for either kind of adopted thing, so a second schema would have recorded
nothing a `kind` value doesn't already say.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    PackageIntegrityError,
    load_published_package_checksums,
    package_instance_checksum,
    verify_published_package,
)
from packages.derivation.production_resolver import (
    PublicationSurface,
    Refusal,
    _json_candidates,
    _sha256_bytes,
    _verify_release_and_registry,
    select_current_adoption,
)
from packages.kernel.schema_registry import SchemaValidationError

SURFACE_ADOPTION_KIND = "surface-adoption"
SURFACE_SCHEMA = "surface-artifact.v1"


@dataclass(frozen=True)
class ResolvedSurface:
    """A verified surface manifest whose every entry's bytes are confirmed on disk."""

    manifest: dict[str, Any]
    content_dir: Path
    adoption_act_id: str
    release_id: str
    entry_count: int
    total_bytes: int

    @property
    def ok(self) -> bool:
        return True


def _within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def resolve_surface_artifact(
    adoption_acts: Sequence[Mapping[str, Any]],
    *,
    run_scope: Mapping[str, str],
    scope_user: str,
    workspace_revision: int,
    surface: PublicationSurface,
    content_dir: Path,
    schemas: DerivationSchemas | None = None,
) -> ResolvedSurface | Refusal:
    """Resolve the adopted surface artifact to verified entries, or refuse.

    Mirrors `production_resolver.resolve_production_package`'s shape through
    adoption and release/registry verification, then diverges at member
    resolution: a surface artifact has one manifest citizen (verified as an
    immutable published instance, the same primitive `artifact-package.v4`
    instances are verified by) whose `entries` are raw files checked by
    SHA-256 against `content_dir`, never schema-validated or interpreted.
    """
    schemas = schemas or DerivationSchemas()

    selected = select_current_adoption(
        adoption_acts,
        run_scope=run_scope,
        scope_user=scope_user,
        workspace_revision=workspace_revision,
        schemas=schemas,
        expected_kind=SURFACE_ADOPTION_KIND,
    )
    if isinstance(selected, Refusal):
        return selected
    payload = selected["payload"]

    verified = _verify_release_and_registry(payload, surface, schemas)
    if isinstance(verified, Refusal):
        return verified

    try:
        package_checksums = load_published_package_checksums(surface.package_registry_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, PackageIntegrityError) as exc:
        return Refusal("REGISTRY_INVALID", str(exc))

    pkg_pin = payload["package"]
    matching: dict[str, dict[str, Any]] = {}
    for body in _json_candidates(surface.member_dir):
        if body.get("schema") != SURFACE_SCHEMA:
            continue
        if body.get("id") != pkg_pin["id"] or str(body.get("version", "")) != pkg_pin["version"]:
            continue
        try:
            digest = package_instance_checksum(body)
        except (TypeError, ValueError):
            continue
        if body.get("package_checksum") == digest:
            matching[digest] = body
    manifest = matching.get(str(pkg_pin["checksum"]))
    if manifest is None:
        return Refusal(
            "SURFACE_ABSENT_OR_MISMATCH", f"no verified surface artifact {pkg_pin['id']}@{pkg_pin['version']} on surface"
        )
    if len(matching) > 1:
        return Refusal("SURFACE_AMBIGUOUS", "multiple distinct surface manifest bodies share the pinned identity")

    try:
        verify_published_package(manifest, package_checksums)
    except PackageIntegrityError as exc:
        return Refusal("SURFACE_INTEGRITY", str(exc))

    try:
        schemas.validate_declared(manifest)
    except SchemaValidationError as exc:
        return Refusal("SURFACE_SCHEMA_INVALID", str(exc))

    try:
        root = content_dir.resolve(strict=True)
    except OSError:
        return Refusal("SURFACE_CONTENT_ROOT_UNREADABLE", f"content root does not exist: {content_dir}")

    total_bytes = 0
    entries = manifest["entries"]
    for entry in entries:
        rel = str(entry["path"])
        candidate = content_dir / rel
        resolved = candidate.resolve(strict=False)
        if not _within(root, resolved):
            # A symlink resolving inside the root (npm's ordinary
            # node_modules/.bin layout) is fine — its bytes are read and
            # digested like any other entry. Only a target that resolves
            # outside the confined root is refused.
            return Refusal("SURFACE_ENTRY_NOT_CONFINED", f"entry path escapes the content root: {rel!r}")
        try:
            data = candidate.read_bytes()
        except OSError:
            return Refusal("SURFACE_ENTRY_ABSENT", f"entry not present on the content root: {rel!r}")
        if len(data) != int(entry["bytes"]) or _sha256_bytes(data) != entry["sha256"]:
            return Refusal("SURFACE_ENTRY_CHECKSUM_MISMATCH", f"entry bytes do not match the manifest digest: {rel!r}")
        total_bytes += len(data)

    return ResolvedSurface(
        manifest=manifest,
        content_dir=content_dir,
        adoption_act_id=str(selected["act_id"]),
        release_id=str(payload["release"]["id"]),
        entry_count=len(entries),
        total_bytes=total_bytes,
    )


__all__ = [
    "ResolvedSurface",
    "SURFACE_ADOPTION_KIND",
    "SURFACE_SCHEMA",
    "resolve_surface_artifact",
]
