"""Regenerate the synthetic Track 3 publication surface and line-7b successor.

Wholly synthetic and deterministic. Each release attests its matching committed
package registry by exact SHA-256: v1 preserves the historical packages through
core v6, v2 carries the core-v7 successor, and v3 carries the narrowly additive
core-v8 / line-7b-field-v2 successor. Adoption acts pin the release and package
checksum from the same route explicitly. Historical v1/v6 and v2/v7 bytes are
read as immutable generation inputs and are never rewritten. No live workspace
or personal data is read.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = _ROOT / "packages" / "content" / "tax" / "2025"
PACKAGE_REGISTRIES = {
    "v1": CONTENT_DIR / "published-packages.json",
    "v2": CONTENT_DIR / "published-packages.v2.json",
    "v3": CONTENT_DIR / "published-packages.v3.json",
}
OUT = _ROOT / "packages" / "sample_data" / "frrs_t3"

SCOPE_USER = "demo.user.filer-1"
RUN_SCOPE = {"jurisdiction": "us", "year": "2025"}

RELEASE_ID = "demo.release.2025"
LINE7B_FIELD_ID = "tax.us.2025.form1040.line-7b"
LINE7B_SYMBOL = "tax.us.2025.form1040.line7b-schedule-d-not-required"
CORE_PACKAGE_ID = "tax.us.2025.package.core-calculations"


def _document(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_checksum(value: dict[str, Any]) -> str:
    return _sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _package_instance_checksum(value: dict[str, Any]) -> str:
    return _canonical_checksum(
        {key: item for key, item in value.items() if key != "package_checksum"}
    )


def render_line7b_prerequisite_content_files() -> dict[str, bytes]:
    """Render the immutable field-v2, core-v8, and registry-v3 successors."""
    field_v1 = json.loads(
        (CONTENT_DIR / "form1040.line-7b.form-field.json").read_text("utf-8")
    )
    field_v2 = copy.deepcopy(field_v1)
    field_v2["version"] = "v2"
    field_v2["binds_symbol"] = LINE7B_SYMBOL

    package_v7 = json.loads(
        (CONTENT_DIR / "package.core-calculations.v7.json").read_text("utf-8")
    )
    package_v8 = copy.deepcopy(package_v7)
    package_v8["version"] = "v8"
    package_v8["members"].append({
        "id": LINE7B_FIELD_ID,
        "role": "form-field",
        "schema": "form-field.v3",
        "version": "v2",
    })
    package_v8["members"].sort(key=lambda member: (member["id"], member["version"]))
    package_v8["package_checksum"] = _package_instance_checksum(package_v8)

    registry_v2 = json.loads(
        (CONTENT_DIR / "published-packages.v2.json").read_text("utf-8")
    )
    registry_v3 = copy.deepcopy(registry_v2)
    registry_v3["citizens"].append({
        "id": LINE7B_FIELD_ID,
        "version": "v2",
        "checksum": _canonical_checksum(field_v2),
    })
    registry_v3["citizens"].sort(key=lambda entry: (entry["id"], entry["version"]))
    registry_v3["packages"].append({
        "id": CORE_PACKAGE_ID,
        "version": "v8",
        "checksum": package_v8["package_checksum"],
    })
    registry_v3["packages"].sort(key=lambda entry: (entry["id"], entry["version"]))

    return {
        "form1040.line-7b.form-field.v2.json": _document(field_v2),
        "package.core-calculations.v8.json": _document(package_v8),
        "published-packages.v3.json": _document(registry_v3),
    }


def _package_checksum(package_id: str, version: str, *, release_version: str) -> str:
    registry = json.loads(PACKAGE_REGISTRIES[release_version].read_text("utf-8"))
    for entry in registry["packages"]:
        if entry["id"] == package_id and entry["version"] == version:
            return str(entry["checksum"])
    raise KeyError((release_version, package_id, version))


def _release_doc(version: str) -> dict[str, Any]:
    return {
        "schema": "release-registry.v1",
        "id": RELEASE_ID,
        "version": version,
        "package_registry_sha256": _sha256(PACKAGE_REGISTRIES[version].read_bytes()),
    }


def _adoption_act(
    act_id: str,
    *,
    actor: str,
    revision: int,
    package_id: str,
    package_version: str = "v1",
    release_version: str = "v1",
    release_checksum: str,
    supersedes: str | None = None,
    committed_against: int = 1,
    scope: dict[str, str] | None = None,
    at: str = "2026-07-18T00:00:00Z",
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "package": {
            "id": package_id,
            "version": package_version,
            "checksum": _package_checksum(
                package_id, package_version, release_version=release_version
            ),
        },
        "release": {
            "id": RELEASE_ID,
            "version": release_version,
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
        "at": at,
        "committed_against": committed_against,
        "payload": payload,
    }


def render_fixture_files() -> dict[str, bytes]:
    releases = {version: _release_doc(version) for version in sorted(PACKAGE_REGISTRIES)}
    release_checksums = {
        version: _sha256(_document(release))
        for version, release in releases.items()
    }
    release_checksum = release_checksums["v1"]
    interest = "tax.us.2025.package.interest-slice"
    core = CORE_PACKAGE_ID

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
        # DSBS Track 2 deliverables 5-8: adds the Schedule B attachment
        # citizen (existence conditional, itemization, tie-out, Part III
        # completeness). Distinct synthetic scope so v4 stays independently
        # exercisable.
        "adoptions/adopt-core-v5-current.json": _adoption_act(
            "act.adopt.core.v5", actor=SCOPE_USER, revision=5,
            package_id=core, package_version="v5", release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2054"},
        ),
        # DSBS Track 3: the line-16 QDCG worksheet production build (ADR-0038)
        # - the rule-artifact.v3 line-16 successor and the two declared-
        # absence fact types. Distinct synthetic scope so v5 stays
        # independently exercisable.
        "adoptions/adopt-core-v6-current.json": _adoption_act(
            "act.adopt.core.v6", actor=SCOPE_USER, revision=6,
            package_id=core, package_version="v6", release_checksum=release_checksum,
            scope={"jurisdiction": "us", "year": "2055"},
        ),
        # Engine Breadth Track 2: the direct line-7a successor package has its
        # own registry/release route. The historical v1 route remains pinned
        # to the byte-identical registry through core v6.
        "adoptions/adopt-core-v7-current.json": _adoption_act(
            "act.adopt.core.v7", actor=SCOPE_USER, revision=7,
            package_id=core, package_version="v7", release_version="v2",
            release_checksum=release_checksums["v2"],
            scope={"jurisdiction": "us", "year": "2056"},
            at="2026-07-30T00:00:00Z",
        ),
        # Line-7b prerequisite repair: a package-only successor that adds the
        # versioned form-field whose symbol joins the unchanged line-7b rule.
        "adoptions/adopt-core-v8-current.json": _adoption_act(
            "act.adopt.core.v8", actor=SCOPE_USER, revision=8,
            package_id=core, package_version="v8", release_version="v3",
            release_checksum=release_checksums["v3"],
            scope={"jurisdiction": "us", "year": "2057"},
            at="2026-07-31T00:00:00Z",
        ),
    }

    rendered: dict[str, bytes] = {
        f"publication_surface/releases/{RELEASE_ID}.{version}.json": _document(release)
        for version, release in releases.items()
    }
    for path, act in acts.items():
        rendered[path] = _document(act)
    return rendered


def main() -> None:
    for relative, contents in render_line7b_prerequisite_content_files().items():
        target = CONTENT_DIR / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    for relative, contents in render_fixture_files().items():
        target = OUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)


if __name__ == "__main__":
    main()
