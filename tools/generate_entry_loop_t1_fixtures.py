"""Regenerate the synthetic W-2 entry-loop workspace and surface fixtures.

The workspace starts from the production-shaped presentation fixture with the
W-2 evidence retained but its contribution, member finding, and closure
removed.  Every other source family and declaration remains seeded.  The
surface publication is an independent ADR-0049 container so the earlier
``surface_t1`` publication remains byte-for-byte historical.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from packages.derivation.package_validation import package_instance_checksum
from tools.generate_presentation_l2_golden import canonical_acts


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "packages" / "sample_data" / "entry_loop_t1"
CONTENT = OUT / "surface" / "content" / "app"

MANIFEST_ID = "demo.surface.entry-loop"
MANIFEST_VERSION = "v1"
RELEASE_ID = "demo.surface-release.entry-loop.2025"
RELEASE_VERSION = "v1"
ACT_ID = "demo.act.adopt.surface.entry-loop.v1"


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seed_acts() -> list[dict[str, Any]]:
    """Return the deterministic seed with W-2 and 1099-DIV box 1b open."""

    result: list[dict[str, Any]] = []
    for raw in canonical_acts():
        act = json.loads(json.dumps(raw))
        payload = act.get("payload", {})
        contribution = payload.get("contribution")
        finding = payload.get("finding")
        member = payload.get("member")
        member_finding = member.get("finding") if isinstance(member, dict) else None
        if (
            isinstance(contribution, dict)
            and contribution.get("id") == "demo.presentation-l2.contribution.w2"
        ):
            continue
        if (
            isinstance(member_finding, dict)
            and member_finding.get("fact_id")
            == (
                "tax.us.2025.w2.box1-wages|"
                "employer=demo.presentation-l2.employer,"
                "w2-slip=demo.presentation-l2.w2,tax-year=2025"
            )
        ):
            continue
        if (
            isinstance(finding, dict)
            and str(finding.get("fact_id", "")).startswith(
                "tax.us.2025.w2.source-closure|"
            )
        ):
            continue
        if (
            isinstance(contribution, dict)
            and contribution.get("id") == "demo.presentation-l2.contribution.div1b"
        ):
            continue
        if (
            isinstance(member_finding, dict)
            and member_finding.get("fact_id")
            == (
                "tax.us.2025.f1099div.box1b-qualified|"
                "payer=demo.presentation-l2.payer,"
                "statement=demo.presentation-l2.divstmt,tax-year=2025"
            )
        ):
            continue
        if (
            isinstance(finding, dict)
            and str(finding.get("fact_id", "")).startswith(
                "tax.us.2025.f1099div.1b.source-closure|"
            )
        ):
            continue
        result.append(act)

    for revision, act in enumerate(result):
        act["committed_against"] = revision
    return result


def _seed_log() -> bytes:
    return b"".join(
        json.dumps(act, sort_keys=True, separators=(",", ":")).encode("utf-8")
        + b"\n"
        for act in seed_acts()
    )


def _content_entries() -> list[dict[str, Any]]:
    if (CONTENT / "dist").exists():
        raise RuntimeError(
            "generated dist/ is local output, not a surface-artifact input"
        )
    entries: list[dict[str, Any]] = []
    for path in sorted(CONTENT.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(CONTENT).as_posix(),
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
            {
                "id": MANIFEST_ID,
                "version": MANIFEST_VERSION,
                "checksum": manifest_checksum,
            }
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
        "actor": "demo.user.filer-1",
        "at": "2026-07-29T00:00:00Z",
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
                "note": "synthetic W-2 entry-loop surface; non-authoritative"
            },
        },
    }
    evaluation = {
        "schema": "demo.entry-loop-evaluation.v1",
        "document": "Synthetic Form W-2 from Demo Workshop",
        "entries": {
            "initial": {"box1": 90000},
            "correction": {"box1": 91000},
        },
        "expected_impact_lines": ["1a", "9", "11", "15", "16"],
        "untouched_comparison_lines": ["2b", "3a", "3b", "12"],
    }

    return {
        "workspace/acts.jsonl": _seed_log(),
        "evaluation-w2.json": _document(evaluation),
        "surface/manifest/surface-artifact.entry-loop.v1.json": _document(
            manifest
        ),
        "surface/registry/published-surface-artifacts.json": registry_bytes,
        f"surface/publication_surface/releases/{RELEASE_ID}.{RELEASE_VERSION}.json": release_bytes,
        "surface/adoptions/adopt-entry-loop-v1.json": _document(adoption),
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
    print(f"entry_loop_t1 content: {count} entries, {total} bytes")


if __name__ == "__main__":
    main()
