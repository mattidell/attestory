"""Generate the synthetic correction-guidance surface successor metadata.

The successor starts from the existing reviewed W-2 page, with a focused
reader change in its own content directory. Its dependencies remain local,
ignored build inputs; the successor manifest pins their bytes when present,
and reuses its own published dependency hashes when they are absent.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from packages.derivation.package_validation import package_instance_checksum

OUT = ROOT / "packages" / "sample_data" / "entry_loop_t1" / "surface-successor"
CONTENT = OUT / "content" / "app"
LEGACY = ROOT / "packages" / "sample_data" / "entry_loop_t1" / "surface"
LEGACY_MANIFEST = LEGACY / "manifest" / "surface-artifact.entry-loop.v1.json"

MANIFEST_ID = "demo.surface.entry-loop"
MANIFEST_VERSION = "v2"
RELEASE_ID = "demo.surface-release.entry-loop.2025"
RELEASE_VERSION = "v2"
ACT_ID = "demo.act.adopt.surface.entry-loop.v2"


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _published_dependency_entries() -> list[dict[str, Any]]:
    for manifest_path in (
        OUT / "manifest" / "surface-artifact.entry-loop.v2.json",
        LEGACY_MANIFEST,
    ):
        try:
            manifest = json.loads(manifest_path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        entries = manifest.get("entries") if isinstance(manifest, dict) else None
        if isinstance(entries, list):
            dependencies = [
                dict(entry)
                for entry in entries
                if isinstance(entry, dict)
                and isinstance(entry.get("path"), str)
                and entry["path"].startswith("node_modules/")
            ]
            if dependencies:
                return dependencies
    raise RuntimeError("published surface dependency hashes are unavailable")


def _content_entries() -> list[dict[str, Any]]:
    if (CONTENT / "dist").exists():
        raise RuntimeError("generated dist/ is local output, not a surface input")
    source_entries: list[dict[str, Any]] = []
    for path in sorted(CONTENT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(CONTENT).as_posix()
        if relative.startswith("node_modules/"):
            continue
        data = path.read_bytes()
        source_entries.append(
            {"path": relative, "sha256": _sha256(data), "bytes": len(data)}
        )

    dependency_root = CONTENT / "node_modules"
    if dependency_root.is_dir():
        installed_dependencies: list[dict[str, Any]] = []
        for path in sorted(dependency_root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(CONTENT).as_posix()
            data = path.read_bytes()
            installed_dependencies.append(
                {"path": relative, "sha256": _sha256(data), "bytes": len(data)}
            )
        dependency_entries = installed_dependencies
    else:
        dependency_entries = _published_dependency_entries()

    return sorted(source_entries + dependency_entries, key=lambda entry: entry["path"])


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

    registry_bytes = _document(
        {
            "packages": [
                {
                    "id": MANIFEST_ID,
                    "version": MANIFEST_VERSION,
                    "checksum": manifest_checksum,
                }
            ]
        }
    )
    release_bytes = _document(
        {
            "schema": "release-registry.v1",
            "id": RELEASE_ID,
            "version": RELEASE_VERSION,
            "package_registry_sha256": _sha256(registry_bytes),
        }
    )
    adoption = {
        "schema": "act.v1",
        "act_id": ACT_ID,
        "kind": "surface-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-11-01T00:00:00Z",
        "committed_against": 1,
        "payload": {
            "package": {
                "id": MANIFEST_ID,
                "version": MANIFEST_VERSION,
                "checksum": manifest_checksum,
            },
            "release": {
                "id": RELEASE_ID,
                "version": RELEASE_VERSION,
                "checksum": _sha256(release_bytes),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 1,
            "audit": {
                "note": "synthetic W-2 correction-guidance surface; non-authoritative"
            },
        },
    }
    return {
        "surface-successor/manifest/surface-artifact.entry-loop.v2.json": _document(
            manifest
        ),
        "surface-successor/registry/published-surface-artifacts.json": registry_bytes,
        f"surface-successor/publication_surface/releases/{RELEASE_ID}.{RELEASE_VERSION}.json": release_bytes,
        "surface-successor/adoptions/adopt-entry-loop-v2.json": _document(adoption),
    }


def content_stats() -> tuple[int, int]:
    entries = _content_entries()
    return len(entries), sum(int(entry["bytes"]) for entry in entries)


def main() -> None:
    for relative, contents in render_fixture_files().items():
        target = ROOT / "packages" / "sample_data" / "entry_loop_t1" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    count, total = content_stats()
    print(f"entry_loop surface successor: {count} entries, {total} bytes")


if __name__ == "__main__":
    main()
