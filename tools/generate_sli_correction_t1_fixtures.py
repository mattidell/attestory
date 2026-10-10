"""Regenerate the synthetic SLI correction-session workspace and surface
fixtures (Track 1, ``account-review-correction`` milestone).

The seed workspace is two forms, each supported, on different borrowings:
Cedar (lender "Cedar Servicing") carries the "autumn" borrowing, Birch
(lender "Birch Servicing") carries "spring". Both are built only through the
real recorder and review flow (``tests.test_sli_track5_worksheet_integration.Return``),
then v42 is adopted (``tests.test_sli_track1_combined_standing.adopt_v42``) --
the same already-adopted production surface the existing SLI tests run
against. No new package, release, or registry version is produced here.

The surface publication is its own ADR-0049 container (H4, settled by the
plan's Track 0 review): one manifest entry (the one static page), a no-op
``build_command``, and a ``surface-adoption`` act. All identities are
synthetic ``demo.*``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from packages.derivation.package_validation import package_instance_checksum

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "packages" / "sample_data" / "sli_correction_t1"
CONTENT = OUT / "surface" / "content" / "app"

MANIFEST_ID = "demo.surface.sli-correction"
MANIFEST_VERSION = "v1"
RELEASE_ID = "demo.surface-release.sli-correction.2025"
RELEASE_VERSION = "v1"
ACT_ID = "demo.act.adopt.surface.sli-correction.v1"


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seed_acts() -> list[dict[str, Any]]:
    """Two supported forms, on different borrowings, with v42 adopted."""

    import tests.test_sli_track1_combined_standing as T1
    import tests.test_sli_track5_worksheet_integration as T5

    ws = T5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
    with ws.raw:
        ws.link("financing", "autumn", "autumn")
        ws.link("statement-inclusion", "autumn", "cedar")
        ws.answer("loan", "autumn", "yes")
        ws.answer("enroll", "autumn", "yes")
        ws.common_answers("cedar")
        ws.link("financing", "spring", "spring")
        ws.link("statement-inclusion", "spring", "birch")
        ws.answer("loan", "spring", "yes")
        ws.answer("enroll", "spring", "yes")
        ws.common_answers("birch")
        T1.adopt_v42(ws)
        acts = [json.loads(json.dumps(act)) for act in ws.acts()]
    for revision, act in enumerate(acts):
        if act.get("committed_against") != revision:
            raise RuntimeError("seed acts are not sequentially committed from zero")
    return acts


def _seed_log() -> bytes:
    return b"".join(
        json.dumps(act, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        for act in seed_acts()
    )


def _content_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(CONTENT.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": path.relative_to(CONTENT).as_posix(),
            "sha256": _sha256(data),
            "bytes": len(data),
        })
    return entries


def render_fixture_files() -> dict[str, bytes]:
    entries = _content_entries()
    manifest_body = {
        "schema": "surface-artifact.v1",
        "id": MANIFEST_ID,
        "version": MANIFEST_VERSION,
        # H4 (plan, Track 0 — readiness for implementation): resolution and
        # build never require Node; the one entry is already a built page.
        "build_command": "true",
        "entrypoint_html": "index.html",
        "entries": entries,
    }
    manifest_checksum = package_instance_checksum(manifest_body)
    manifest = dict(manifest_body, package_checksum=manifest_checksum)

    registry = {"packages": [
        {"id": MANIFEST_ID, "version": MANIFEST_VERSION, "checksum": manifest_checksum},
    ]}
    registry_bytes = _document(registry)
    release = {
        "schema": "release-registry.v1", "id": RELEASE_ID, "version": RELEASE_VERSION,
        "package_registry_sha256": _sha256(registry_bytes),
    }
    release_bytes = _document(release)
    adoption = {
        "schema": "act.v1", "act_id": ACT_ID, "kind": "surface-adoption",
        # Must match ``correction_session.SCOPE_USER``, since
        # ``select_current_adoption`` selects only that user's own adoption acts.
        "actor": "demo.user.filer", "at": "2026-10-08T00:00:00Z", "committed_against": 1,
        "payload": {
            "package": {"id": MANIFEST_ID, "version": MANIFEST_VERSION, "checksum": manifest_checksum},
            "release": {"id": RELEASE_ID, "version": RELEASE_VERSION,
                       "checksum": _sha256(release_bytes)},
            "scope": {"jurisdiction": "us", "year": "2025"}, "revision": 1,
            "audit": {"note": "synthetic SLI correction-session surface; non-authoritative"},
        },
    }

    return {
        "workspace/acts.jsonl": _seed_log(),
        "surface/manifest/surface-artifact.sli-correction.v1.json": _document(manifest),
        "surface/registry/published-surface-artifacts.json": registry_bytes,
        f"surface/publication_surface/releases/{RELEASE_ID}.{RELEASE_VERSION}.json": release_bytes,
        "surface/adoptions/adopt-sli-correction-v1.json": _document(adoption),
    }


def content_stats() -> tuple[int, int]:
    entries = _content_entries()
    return len(entries), sum(int(entry["bytes"]) for entry in entries)


def main() -> None:
    for relative, contents in render_fixture_files().items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    count, total = content_stats()
    print(f"sli_correction_t1 content: {count} entries, {total} bytes")


if __name__ == "__main__":
    main()
