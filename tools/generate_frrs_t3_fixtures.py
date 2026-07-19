"""Regenerate the synthetic Track 3 publication surface (release + adoption acts).

Wholly synthetic and deterministic. The release attests the *existing* committed
package registry (`packages/content/tax/2025/published-packages.json`) by its exact
SHA-256; the adoption acts pin that release and a committed package by checksum. No
package or member bytes are copied — the member surface is the committed tax content
the resolver already verifies. No live workspace or personal data is read.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = _ROOT / "packages" / "content" / "tax" / "2025"
PACKAGE_REGISTRY = CONTENT_DIR / "published-packages.json"
OUT = _ROOT / "packages" / "sample_data" / "frrs_t3"

SCOPE_USER = "demo.user.filer-1"
RUN_SCOPE = {"jurisdiction": "us", "year": "2025"}

RELEASE_ID = "demo.release.2025"
RELEASE_VERSION = "v1"


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _package_checksum(package_id: str, version: str = "v1") -> str:
    registry = json.loads(PACKAGE_REGISTRY.read_text("utf-8"))
    for entry in registry["packages"]:
        if entry["id"] == package_id and entry["version"] == version:
            return str(entry["checksum"])
    raise KeyError(package_id)


def _release_doc() -> dict[str, Any]:
    return {
        "schema": "release-registry.v1",
        "id": RELEASE_ID,
        "version": RELEASE_VERSION,
        "package_registry_sha256": _sha256(PACKAGE_REGISTRY.read_bytes()),
    }


def _adoption_act(
    act_id: str,
    *,
    actor: str,
    revision: int,
    package_id: str,
    package_version: str = "v1",
    release_checksum: str,
    supersedes: str | None = None,
    committed_against: int = 1,
    scope: dict[str, str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "package": {
            "id": package_id,
            "version": package_version,
            "checksum": _package_checksum(package_id, package_version),
        },
        "release": {
            "id": RELEASE_ID,
            "version": RELEASE_VERSION,
            "checksum": release_checksum,
        },
        "scope": dict(scope or RUN_SCOPE),
        "revision": revision,
        "audit": {"note": "synthetic adoption; non-authoritative"},
    }
    if supersedes is not None:
        payload["supersedes"] = supersedes
    return {
        "schema": "act.v1",
        "act_id": act_id,
        "kind": "package-adoption",
        "actor": actor,
        "at": "2026-07-18T00:00:00Z",
        "committed_against": committed_against,
        "payload": payload,
    }


def render_fixture_files() -> dict[str, bytes]:
    release = _release_doc()
    release_checksum = _sha256(_document(release))
    interest = "tax.us.2025.package.interest-slice"
    core = "tax.us.2025.package.core-calculations"

    acts: dict[str, dict[str, Any]] = {
        # Current user adoption of the clean interest-slice package: v2 supersedes v1.
        "adoptions/adopt-interest-v1.json": _adoption_act(
            "act.adopt.interest.v1", actor=SCOPE_USER, revision=1,
            package_id=interest, release_checksum=release_checksum,
        ),
        "adoptions/adopt-interest-v2-current.json": _adoption_act(
            "act.adopt.interest.v2", actor=SCOPE_USER, revision=2,
            package_id=interest, release_checksum=release_checksum,
            supersedes="act.adopt.interest.v1",
        ),
        # A non-user (automation) act at a higher revision — must never select.
        "adoptions/adopt-automation.json": _adoption_act(
            "act.adopt.automation", actor="automation.bot", revision=9,
            package_id=interest, release_checksum=release_checksum,
        ),
        # Two same-user same-scope acts tie at the maximum revision — must refuse.
        "adoptions/adopt-tie-a.json": _adoption_act(
            "act.adopt.tie.a", actor=SCOPE_USER, revision=5,
            package_id=interest, release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2099"},
        ),
        "adoptions/adopt-tie-b.json": _adoption_act(
            "act.adopt.tie.b", actor=SCOPE_USER, revision=5,
            package_id=interest, release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2099"},
        ),
        # Current adoption of the un-repaired core package (RG-1 hard-gate refusal).
        "adoptions/adopt-core-current.json": _adoption_act(
            "act.adopt.core", actor=SCOPE_USER, revision=1,
            package_id=core, release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2050"},
        ),
        # v1 remains a historical hard-gate refusal.  The repaired immutable
        # v2 package is separately adopted for the synthetic live analogue.
        "adoptions/adopt-core-v2-current.json": _adoption_act(
            "act.adopt.core.v2", actor=SCOPE_USER, revision=2,
            package_id=core, package_version="v2", release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2051"},
        ),
        # The live-path repair's immutable successor package.  It has a
        # distinct synthetic scope so v2 remains independently exercisable.
        "adoptions/adopt-core-v3-current.json": _adoption_act(
            "act.adopt.core.v3", actor=SCOPE_USER, revision=3,
            package_id=core, package_version="v3", release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2052"},
        ),
        # DSBS Track 2's core-calculations v4: adds 1099-DIV lines 3a/3b and
        # the line-9 dividend fold-in. Distinct synthetic scope so v3 stays
        # independently exercisable.
        "adoptions/adopt-core-v4-current.json": _adoption_act(
            "act.adopt.core.v4", actor=SCOPE_USER, revision=4,
            package_id=core, package_version="v4", release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2053"},
        ),
    }

    rendered: dict[str, bytes] = {
        f"publication_surface/releases/{RELEASE_ID}.{RELEASE_VERSION}.json": _document(release),
    }
    for path, act in acts.items():
        rendered[path] = _document(act)
    return rendered


def main() -> None:
    for relative, contents in render_fixture_files().items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)


if __name__ == "__main__":
    main()
