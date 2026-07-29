"""Regenerate the synthetic Track 1 surface-artifact publication surface.

Wholly synthetic and deterministic. The committed content tree
(`packages/sample_data/surface_t1/content/app/`) is real, ordinary `npm
install` output for one deliberately boring Svelte page — nobody's data, just
a public dependency tree pinned by an exact version and its lockfile. This
script never touches that tree; it only *describes* it: a manifest citizen
listing every file's path, byte count, and SHA-256, a registry pinning that
manifest's own instance checksum, a release attesting the registry, and one
`surface-adoption` act pinning both. All four are generated fixtures, the
same relationship `generate_frrs_t3_fixtures.py` has to the tax content it
describes, just in the other direction: there the script writes acts against
already-committed rule content; here it writes the manifest itself, computed
from already-committed program bytes.

Nothing here is fetched, installed, or executed. Re-run after touching the
content tree (adding, removing, or upgrading a dependency) and commit the
diff; the regeneration test proves the checked-in fixtures still match.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from packages.derivation.package_validation import package_instance_checksum

_ROOT = Path(__file__).resolve().parent.parent
OUT = _ROOT / "packages" / "sample_data" / "surface_t1"
CONTENT_DIR = OUT / "content" / "app"

MANIFEST_ID = "demo.surface.entry-page"
MANIFEST_VERSION = "v1"
RELEASE_ID = "demo.surface-release.2025"
RELEASE_VERSION = "v1"
ACT_ID = "act.adopt.surface.entry-page.v1"
SCOPE_USER = "demo.user.filer-1"
RUN_SCOPE = {"jurisdiction": "us", "year": "2025"}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _content_entries() -> list[dict[str, Any]]:
    entries = []
    for path in sorted(CONTENT_DIR.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(CONTENT_DIR).as_posix(),
                "sha256": _sha256(data),
                "bytes": len(data),
            }
        )
    return entries


def render_fixture_files() -> dict[str, bytes]:
    entries = _content_entries()

    manifest_body = {
        "schema": "surface-artifact.v1",
        "id": MANIFEST_ID,
        "version": MANIFEST_VERSION,
        "build_command": "node build.mjs",
        "entrypoint_html": "dist/index.html",
        "entries": entries,
    }
    manifest_checksum = package_instance_checksum(manifest_body)
    manifest = dict(manifest_body, package_checksum=manifest_checksum)

    registry = {
        "packages": [
            {"id": MANIFEST_ID, "version": MANIFEST_VERSION, "checksum": manifest_checksum},
        ]
    }
    registry_bytes = _document(registry)

    release = {
        "schema": "release-registry.v1",
        "id": RELEASE_ID,
        "version": RELEASE_VERSION,
        "package_registry_sha256": _sha256(registry_bytes),
    }
    release_bytes = _document(release)

    adoption = {
        "schema": "act.v1",
        "act_id": ACT_ID,
        "kind": "surface-adoption",
        "actor": SCOPE_USER,
        "at": "2026-07-28T00:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {"id": MANIFEST_ID, "version": MANIFEST_VERSION, "checksum": manifest_checksum},
            "release": {"id": RELEASE_ID, "version": RELEASE_VERSION, "checksum": _sha256(release_bytes)},
            "scope": dict(RUN_SCOPE),
            "revision": 1,
            "audit": {"note": "synthetic surface adoption; non-authoritative"},
        },
    }

    return {
        "manifest/surface-artifact.entry-page.v1.json": _document(manifest),
        "registry/published-surface-artifacts.json": registry_bytes,
        f"publication_surface/releases/{RELEASE_ID}.{RELEASE_VERSION}.json": release_bytes,
        "adoptions/adopt-surface-entry-page-v1.json": _document(adoption),
    }


def content_stats() -> tuple[int, int]:
    """Return (entry_count, total_bytes) for the vendored content tree."""
    entries = _content_entries()
    return len(entries), sum(e["bytes"] for e in entries)


def main() -> None:
    for relative, contents in render_fixture_files().items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    count, total = content_stats()
    print(f"surface_t1 content: {count} entries, {total} bytes ({total / 1_000_000:.2f} MB)")


if __name__ == "__main__":
    main()
