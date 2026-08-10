"""Generate the Form 1098 mortgage-interest Track 2 package/publication set.

Deterministic, additive over the immutable v28 core-calculations package: v29
wires in Track 1's already-committed Form 1098/Schedule A citizens (never
before an actual package member) plus Track 2's own new citizens - the
line-12e/13a/13b/14 succession, the line-15 v2 successor, the Schedule A
composition-total/excess-over-standard helpers, and the Schedule A attachment
disposition. No existing citizen bytes are rewritten in place; the historical
rule.form1040-line12.json, rule.form1040-line15.json (v1), and
form1040.line-12.form-field.json remain untouched on disk and simply stop
being v29 package members, exactly mirroring this corpus's established
line-16 v1->v5 successor-version precedent.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "f1098_mortgage_interest_line12e"


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


# Track 1 citizens: already committed on disk, never before a real package
# member (Track 1's own tests injected them via a resolve_production_package
# monkeypatch). Wired in for real here, by pin only - never re-rendered.
_TRACK1_MEMBER_FILES = (
    "f1098.bundle.json",
    "family.f1098.json",
    "closure-mapping.f1098.json",
    "parameter.mortgage-interest-debt-limit.json",
    "schedule-a-boundary.bundle.json",
    "citation.schedule-a-boundary.json",
    "rule.schedule-a-line8a.json",
    "rule.schedule-a-boundary-no-medical.json",
    "rule.schedule-a-boundary-no-salt.json",
    "rule.schedule-a-boundary-no-other-interest.json",
    "rule.schedule-a-boundary-no-investment-interest.json",
    "rule.schedule-a-boundary-no-charitable.json",
    "rule.schedule-a-boundary-no-casualty-theft.json",
    "rule.schedule-a-boundary-no-gambling-other.json",
)

# Track 2's own new citizens.
_TRACK2_MEMBER_FILES = (
    "rule.form1040-line12e.json",
    "form1040.line-12e.form-field.json",
    "citation.form1040.line-12e.json",
    "rule.form1040-line13a.json",
    "form1040.line-13a.form-field.json",
    "citation.form1040.line-13a.json",
    "rule.form1040-line13b.json",
    "form1040.line-13b.form-field.json",
    "citation.form1040.line-13b.json",
    "rule.form1040-line14.json",
    "form1040.line-14.form-field.json",
    "citation.form1040.line-14.json",
    "rule.form1040-line15.v2.json",
    "rule.schedule-a-total.json",
    "rule.schedule-a-total-closed-empty.json",
    "rule.schedule-a-excess-over-standard.json",
    "attachment.schedule-a.json",
    "citation.attachment.schedule-a.json",
)

# Track 2 review finding 1 repair round 2: rule.form1040-line12e.json's own
# value branches on this scope flag, but round 1's optional_default/
# default-true design let a real, fully-authorized Form 1098 return silently
# fall through to the raw itemized assertion whenever a preparer simply never
# asserted the new flag - a worse bypass than the original defect. The flag
# is now a mandatory pin (no optional_default, no default parameter), exactly
# like every other "no-X" scope-declaration token in this corpus: its absence
# blocks DEPENDENCY_ABSENT rather than silently defaulting.
_FINDING1_REPAIR_MEMBER_FILES = ("f1098-scope.bundle.json",)

# Repair round 3 finding 2: the seven Schedule A boundary rules and
# rule.form1040-line13a/13b.json previously published/zeroed unconditionally
# with no taxpayer declaration behind them and no downstream consumer - a
# citation trail wrapped around a hardcoded true/zero. schedule-a-boundary.
# bundle.json (already a Track 1 member, edited in place to add its seven new
# -declared fact types) and rule.schedule-a-boundary-no-*.json/rule.
# form1040-line13a.json/rule.form1040-line13b.json (already members) now gate
# on those new mandatory facts. qbi-schedule1a-scope.bundle.json is new -
# it needs its own package member entry.
_FINDING2_REPAIR_MEMBER_FILES = ("qbi-schedule1a-scope.bundle.json",)

# Historical citizens dropped from v29 membership (bytes untouched on disk;
# remain reachable through package versions v1-v28). Their role is fully
# superseded: rule.form1040-line12e replaces rule.form1040-line12,
# form1040.line-12e replaces form1040.line-12, rule.form1040-line15 v2
# replaces v1. Keeping the historical producer alongside its successor would
# either silently reopen the itemized-assertion bypass this milestone exists
# to close, or create an unresolved duplicate-producer conflict.
_DROPPED_MEMBER_IDS = (
    "tax.us.2025.rule.form1040-line12",
    "tax.us.2025.form1040.line-12",
    # citation.form1040.line-12 was only ever pinned by form1040.line-12's
    # form-field.citation; once that form-field is dropped, nothing else in
    # v29 references this citation, so it would otherwise become an
    # unreachable package member (Track 2 charter deliverable 7a).
    "tax.us.2025.citation.form1040.line-12",
)


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
    package = _load("package.core-calculations.v28.json")
    package["schema"] = "artifact-package.v22"
    package["version"] = "v29"

    members = [dict(member) for member in package["members"] if member["id"] not in _DROPPED_MEMBER_IDS]
    # Drop the v1 line-15 member; the v2 successor is added below.
    members = [m for m in members if not (m["id"] == "tax.us.2025.rule.form1040-line15")]

    added_ids: set[str] = set()
    for name in _TRACK1_MEMBER_FILES + _TRACK2_MEMBER_FILES + _FINDING1_REPAIR_MEMBER_FILES + _FINDING2_REPAIR_MEMBER_FILES:
        citizen = _load(name)
        members.append(_member_pin(citizen))
        added_ids.add(citizen["id"])

    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))
    package["admitted_schemas"] = sorted(
        set(package["admitted_schemas"])
        | {"rule-artifact.v4", "attachment-rule.v1", "form-field.v3"}
    )

    # tax.us.2025.schedule-a.total has two producers with provably mutually
    # exclusive guards (count == 0 XOR count > 0 over the closed f1098
    # family), so exactly one ever reaches publish for a given return - this
    # is the intended use of the package-level conflict_semantics allowlist
    # (first use in this corpus; the schema has carried the field since
    # artifact-package.v2 but no prior milestone needed a same-symbol
    # multi-producer route). selected_producer names the ordinary/expected
    # case for documentation; the runner's own first-publisher-wins /
    # inapplicable-conflict-loser semantics apply regardless at runtime, and
    # the guards' mutual exclusivity means the "loser" path is never
    # actually reached.
    package["conflict_semantics"] = list(package.get("conflict_semantics", [])) + [
        {
            "symbol": "tax.us.2025.schedule-a.total",
            "selected_producer": {"id": "tax.us.2025.rule.schedule-a-total", "version": "v1"},
        }
    ]

    # Track 2 review finding 1 repair round 2: tax.us.2025.deductions.line-12e
    # stays single-producer (a real second rule-artifact citizen for the same
    # form-field-bound symbol was tried and rejected: presentation_projection's
    # _one_row join requires exactly one disposition row per symbol for a
    # form-field-bound symbol, which the two-disjoint-producer pattern used
    # above for tax.us.2025.schedule-a.total - never form-field-bound - does
    # not have to satisfy). tax.us.2025.f1098-scope.no-mortgage-statement is a
    # mandatory pin on rule.form1040-line12e.json (requires/pins), not an
    # optional_default input binding, so - exactly like this corpus's other
    # "no-X" scope-declaration tokens (ss-benefits-scope, line2a-scope,
    # schedule-a-boundary) - it needs no package-level input_bindings entry at
    # all; it is referenced directly by its full fact-type id and its absence
    # blocks DEPENDENCY_ABSENT.

    entrypoints = [dict(e) for e in package["entrypoints"] if e["id"] not in _DROPPED_MEMBER_IDS]
    entrypoints = [e for e in entrypoints if not (e["id"] == "tax.us.2025.rule.form1040-line15")]
    new_entrypoint_ids = (
        "tax.us.2025.rule.form1040-line12e",
        "tax.us.2025.rule.form1040-line13a",
        "tax.us.2025.rule.form1040-line13b",
        "tax.us.2025.rule.form1040-line14",
        "tax.us.2025.rule.form1040-line15",
        "tax.us.2025.schedule-a.line8a.rule",
        "tax.us.2025.rule.schedule-a-total",
        "tax.us.2025.rule.schedule-a-total-closed-empty",
        "tax.us.2025.rule.schedule-a-excess-over-standard",
        "tax.us.2025.rule.schedule-a-boundary-no-medical",
        "tax.us.2025.rule.schedule-a-boundary-no-salt",
        "tax.us.2025.rule.schedule-a-boundary-no-other-interest",
        "tax.us.2025.rule.schedule-a-boundary-no-investment-interest",
        "tax.us.2025.rule.schedule-a-boundary-no-charitable",
        "tax.us.2025.rule.schedule-a-boundary-no-casualty-theft",
        "tax.us.2025.rule.schedule-a-boundary-no-gambling-other",
        "tax.us.2025.rule.attachment.schedule-a",
        "tax.us.2025.citation.attachment.schedule-a",
        "tax.us.2025.parameter.default-zero",
        # The 7 boundary rules publish "value: true" with no fact reads, so
        # nothing creates an adjacency edge to their own vocabulary bundle
        # (Track 2 charter deliverable 7b) - root it explicitly.
        "tax.us.2025.schedule-a-boundary.vocabulary",
        # Round 2 repair: tax.us.2025.f1098-scope.no-mortgage-statement is now
        # a mandatory pin referenced directly by full fact-type id (no
        # package-level input_bindings entry), so nothing creates an
        # adjacency edge to its own vocabulary bundle either - root it
        # explicitly, exactly like the boundary vocabulary above.
        "tax.us.2025.f1098-scope.vocabulary",
        # Repair round 3 finding 2: the seven schedule-a-boundary -declared
        # facts and the two new QBI/Schedule-1-A facts are all referenced
        # directly by full fact-type id (no package-level input_bindings
        # entry), so - exactly like f1098-scope.vocabulary above - nothing
        # creates an adjacency edge to qbi-schedule1a-scope.vocabulary; root
        # it explicitly. schedule-a-boundary.vocabulary is already rooted
        # above and needs no further change.
        "tax.us.2025.qbi-schedule1a-scope.vocabulary",
    )
    members_by_id = {m["id"]: m for m in package["members"]}
    for entry_id in new_entrypoint_ids:
        member = members_by_id[entry_id]
        entrypoints.append({"id": entry_id, "version": member["version"]})
    package["entrypoints"] = sorted(
        {(e["id"], e["version"]) for e in entrypoints}
    )
    package["entrypoints"] = [{"id": eid, "version": ver} for eid, ver in package["entrypoints"]]

    package["package_checksum"] = _checksum(package)
    return package


def build_registry(package: dict[str, Any]) -> dict[str, Any]:
    registry = _load("published-packages.v23.json")
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _TRACK1_MEMBER_FILES + _TRACK2_MEMBER_FILES + _FINDING1_REPAIR_MEMBER_FILES + _FINDING2_REPAIR_MEMBER_FILES:
        citizen = _load(name)
        key = (citizen["id"], citizen["version"])
        citizen_entries = [e for e in citizen_entries if (e["id"], e["version"]) != key]
        citizen_entries.append({"id": citizen["id"], "version": citizen["version"], "checksum": _citizen_checksum(citizen)})
    registry["citizens"] = sorted(citizen_entries, key=lambda e: (e["id"], e["version"]))

    package_entries = [dict(entry) for entry in registry["packages"]]
    package_entries.append({"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]})
    registry["packages"] = sorted(package_entries, key=lambda e: (e["id"], e["version"]))
    return registry


def build_release(registry_bytes: bytes) -> dict[str, Any]:
    return {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v22",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }


def build_adoption(
    package: dict[str, Any], registry: dict[str, Any], release: dict[str, Any], release_bytes: bytes
) -> dict[str, Any]:
    package_entry = next(
        e for e in registry["packages"]
        if e["id"] == package["id"] and e["version"] == package["version"]
    )
    return {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v29",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-08T12:00:00Z",
        "committed_against": 0,
        "payload": {
            "package": {"id": package["id"], "version": package["version"], "checksum": package_entry["checksum"]},
            "release": {"id": release["id"], "version": release["version"], "checksum": hashlib.sha256(release_bytes).hexdigest()},
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 29,
            "audit": {"note": "synthetic Form 1098 mortgage-interest line-12e Track 2 adoption; non-authoritative"},
        },
    }


def render_all() -> dict[Path, bytes]:
    package = build_package()
    registry = build_registry(package)

    out: dict[Path, bytes] = {
        CONTENT / "package.core-calculations.v29.json": _bytes(package),
        CONTENT / "published-packages.v24.json": _bytes(registry),
    }

    registry_bytes = out[CONTENT / "published-packages.v24.json"]
    release = build_release(registry_bytes)
    release_bytes = _bytes(release)
    adoption = build_adoption(package, registry, release, release_bytes)

    out[FIXTURES / "publication_surface" / "releases" / "demo.release.2025.v22.json"] = release_bytes
    out[FIXTURES / "adoptions" / "adopt-core-v29-current.json"] = _bytes(adoption)
    return out


def main() -> None:
    for path, body in render_all().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
