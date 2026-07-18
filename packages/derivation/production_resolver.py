"""Production package resolver: one authority chain, or a typed refusal (ADR-0033).

The resolver never trusts a caller-provided package id, path, catalog, or fixture
``adoption_pin``. Authority flows one way (ADR-0033 Decisions 1-3):

    current user adoption -> verified release -> verified registry bytes
    -> verified package instance -> verified exclusive member graph
    -> hard ``validation.ok == True`` -> resolved graph

Any break refuses fail-closed with a typed :class:`Refusal` — refusals are return
values, never exceptions-as-control-flow. This module is import-fenced from the
raw evaluator (``runner.run`` / ``runners.derive``): it produces a resolved member
graph for the live entrypoint to marshal and run, and never hand-assembles an
``InputFinding``. It is a strict superset of the fixture path's guarantees: same
validator, more mandatory verification, and a hard gate the fixture path skips.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import (
    PackageIntegrityError,
    citizen_checksum,
    load_published_citizen_checksums,
    load_published_package_checksums,
    package_instance_checksum,
    validate_package,
    verify_published_package,
)
from packages.kernel.schema_registry import SchemaValidationError

ADOPTION_SCHEMA = "act-package-adoption.v1"
RELEASE_SCHEMA = "release-registry.v1"


@dataclass(frozen=True)
class Refusal:
    """A typed, fail-closed resolution refusal. Never an authorization."""

    reason: str
    detail: str
    issues: tuple[dict[str, str], ...] = ()

    @property
    def ok(self) -> bool:
        return False


@dataclass(frozen=True)
class ResolvedGraph:
    """An exclusive, verified member graph cleared by the hard gate."""

    package: dict[str, Any]
    resolved_members: tuple[dict[str, Any], ...]
    adoption_act_id: str
    release_id: str

    @property
    def ok(self) -> bool:
        return True


@dataclass(frozen=True)
class PublicationSurface:
    """The immutable publication surface the resolver reads bytes from.

    ``release_dir`` holds ``release-registry.v1`` documents named
    ``<id>.<version>.json``; ``package_registry_path`` is the exact registry
    document a release attests; ``member_dir`` holds candidate citizen and
    package bodies. Bytes are read and verified — never trusted by location.
    """

    release_dir: Path
    package_registry_path: Path
    member_dir: Path


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text("utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("JSON document must be an object")
    return loaded


def _json_candidates(directory: Path) -> tuple[dict[str, Any], ...]:
    """Return parseable object candidates in a deterministic order.

    A publication surface is allowed to have unrelated or malformed co-located
    files.  They cannot become authority merely by being present, so callers
    select only checksum-verified candidates from this neutral inventory.
    """
    try:
        paths = sorted(directory.rglob("*.json"))
    except OSError:
        return ()
    candidates: list[dict[str, Any]] = []
    for path in paths:
        try:
            candidates.append(_load_json(path))
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError):
            continue
    return tuple(candidates)


# --- Decision 1: release-rooted, current-user adoption ----------------------


def _well_formed_adoption(act: Mapping[str, Any], schemas: DerivationSchemas) -> bool:
    if act.get("schema") != "act.v1" or act.get("kind") != "package-adoption":
        return False
    payload = act.get("payload")
    if not isinstance(payload, Mapping):
        return False
    try:
        schemas.validate("act.v1", dict(act))
        schemas.validate(ADOPTION_SCHEMA, dict(payload))
    except Exception:
        return False
    return True


def select_current_adoption(
    adoption_acts: Sequence[Mapping[str, Any]],
    *,
    run_scope: Mapping[str, str],
    scope_user: str,
    workspace_revision: int,
    schemas: DerivationSchemas,
) -> Mapping[str, Any] | Refusal:
    """Select exactly one current adoption by the sole user in scope (Decision 1).

    Considers only well-formed ``act-package-adoption.v1`` acts by ``scope_user``
    whose payload scope equals ``run_scope`` and that were committed at or before
    the fixed ``workspace_revision``. Applies supersession, then requires a unique
    maximum ``revision``. Zero candidates or a tie refuses. A non-user act, a
    stale (superseded) act, or a caller argument never selects authority.
    """
    candidates: dict[str, Mapping[str, Any]] = {}
    for act in adoption_acts:
        if not _well_formed_adoption(act, schemas):
            continue
        if act.get("actor") != scope_user:
            continue  # a non-user act never selects authority
        committed = act.get("committed_against")
        if isinstance(committed, int) and committed > workspace_revision:
            continue  # not yet current at this fixed workspace revision
        payload = act["payload"]
        if dict(payload.get("scope", {})) != dict(run_scope):
            continue
        act_id = str(act.get("act_id"))
        prior = candidates.get(act_id)
        if prior is not None and prior != act:
            return Refusal("ADOPTION_AMBIGUOUS", f"conflicting bodies for adoption act {act_id}")
        candidates[act_id] = act

    superseded: set[str] = set()
    for act_id, act in candidates.items():
        ref = act["payload"].get("supersedes")
        if ref is None:
            continue
        if ref not in candidates:
            # A fixed-revision projection may contain only the current act;
            # its predecessor remains historical state outside this resolver's
            # candidate projection.  It cannot be made current by this absent
            # reference, but neither may absence erase an otherwise valid act.
            continue
        if int(act["payload"]["revision"]) <= int(candidates[ref]["payload"]["revision"]):
            return Refusal(
                "ADOPTION_SUPERSESSION_INVALID",
                f"adoption {act_id} does not advance superseded adoption {ref}",
            )
        superseded.add(ref)

    live = [act for act_id, act in candidates.items() if act_id not in superseded]
    if not live:
        return Refusal("ADOPTION_NONE_CURRENT", "no current user adoption in scope")

    max_revision = max(int(act["payload"]["revision"]) for act in live)
    top = [act for act in live if int(act["payload"]["revision"]) == max_revision]
    if len(top) != 1:
        return Refusal(
            "ADOPTION_AMBIGUOUS",
            f"{len(top)} current adoptions tie at revision {max_revision}",
        )
    return top[0]


# --- Decision 2: verify release bytes before registry authenticates supply ---


def _verify_release_and_registry(
    adoption_payload: Mapping[str, Any],
    surface: PublicationSurface,
    schemas: DerivationSchemas,
) -> tuple[dict[str, Any], Path] | Refusal:
    release_pin = adoption_payload["release"]
    # Never turn an adoption's id/version strings into a filesystem path.  The
    # release is selected from the immutable surface by its declared identity
    # and its adoption-pinned bytes, so a crafted id cannot escape that surface.
    matching: dict[str, dict[str, Any]] = {}
    try:
        release_paths = sorted(surface.release_dir.rglob("*.json"))
    except OSError:
        release_paths = []
    for path in release_paths:
        try:
            raw = path.read_bytes()
            candidate = json.loads(raw.decode("utf-8"))
            if not isinstance(candidate, dict):
                continue
            if candidate.get("id") != release_pin["id"] or candidate.get("version") != release_pin["version"]:
                continue
            schemas.validate(RELEASE_SCHEMA, candidate)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, SchemaValidationError, ValueError):
            continue
        matching[_sha256_bytes(raw)] = candidate
    release = matching.get(str(release_pin["checksum"]))
    if release is None:
        return Refusal(
            "RELEASE_ABSENT_OR_MISMATCH",
            f"no verified release {release_pin['id']}@{release_pin['version']} on surface",
        )
    if len(matching) > 1:
        return Refusal("RELEASE_AMBIGUOUS", "multiple distinct release bodies share the pinned identity")

    try:
        registry_bytes = surface.package_registry_path.read_bytes()
    except OSError as exc:
        return Refusal("REGISTRY_ABSENT", str(exc))
    if _sha256_bytes(registry_bytes) != release.get("package_registry_sha256"):
        # replaced registry bytes under an honest release
        return Refusal("REGISTRY_CHECKSUM_MISMATCH", "registry bytes do not match the release attestation")
    return release, surface.package_registry_path


# --- Decision 3: exclusive, verified member graph or refuse -----------------


def _resolve_member_corpus(
    package: Mapping[str, Any],
    surface: PublicationSurface,
    citizen_checksums: Mapping[tuple[str, str], str],
) -> dict[tuple[str, str], dict[str, Any]] | Refusal:
    """Walk exact member pins; admit only checksum-verified bodies (Decision 3).

    For each pinned (id, version) the resolver gathers every candidate body on
    the surface, computes its canonical checksum, and admits only a body whose
    checksum equals the registry-verified expected digest. Byte-identical
    duplicates collapse; two distinct bodies for one key refuse. Filesystem and
    glob order never affect admission (candidates are matched by digest, not
    order). Co-located unpinned files are never candidates for any key.
    """
    # Index candidate bodies by (id, version) -> set of distinct canonical checksums.
    by_key: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for body in _json_candidates(surface.member_dir):
        cid = body.get("id")
        if not isinstance(cid, str):
            continue
        key = (cid, str(body.get("version", "v1")))
        digest = citizen_checksum(body)
        by_key.setdefault(key, {})[digest] = body

    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for pin in package.get("members", []):
        key = (pin["id"], pin["version"])
        expected = citizen_checksums.get(key)
        if expected is None:
            return Refusal("MEMBER_UNPUBLISHED", f"member {key[0]}@{key[1]} not in verified registry")
        matches = [body for digest, body in by_key.get(key, {}).items() if digest == expected]
        if not matches:
            return Refusal("MEMBER_ABSENT_OR_MISMATCH", f"no verified body for member {key[0]}@{key[1]}")
        if len(matches) > 1:  # pragma: no cover - identical digests dedupe in the dict
            return Refusal("MEMBER_AMBIGUOUS", f"ambiguous verified bodies for member {key[0]}@{key[1]}")
        corpus[key] = matches[0]
    return corpus


def resolve_production_package(
    adoption_acts: Sequence[Mapping[str, Any]],
    *,
    run_scope: Mapping[str, str],
    scope_user: str,
    workspace_revision: int,
    surface: PublicationSurface,
    schemas: DerivationSchemas | None = None,
) -> ResolvedGraph | Refusal:
    """Resolve the adopted package to an exclusive verified graph, or refuse.

    The whole authority chain, fail-closed. Returns a :class:`ResolvedGraph`
    only when a current user adoption, a verified release, verified registry
    bytes, a verified package instance, an exclusive verified member graph, and
    a hard ``validation.ok == True`` all hold; otherwise a typed :class:`Refusal`.
    """
    schemas = schemas or DerivationSchemas()

    selected = select_current_adoption(
        adoption_acts,
        run_scope=run_scope,
        scope_user=scope_user,
        workspace_revision=workspace_revision,
        schemas=schemas,
    )
    if isinstance(selected, Refusal):
        return selected
    payload = selected["payload"]

    verified = _verify_release_and_registry(payload, surface, schemas)
    if isinstance(verified, Refusal):
        return verified

    try:
        package_checksums = load_published_package_checksums(surface.package_registry_path)
        citizen_checksums = load_published_citizen_checksums(surface.package_registry_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, PackageIntegrityError) as exc:
        return Refusal("REGISTRY_INVALID", str(exc))

    # Locate the adopted package body by pin and verify its instance checksum
    # against the adoption pin and the verified registry (no self-checksum evasion).
    pkg_pin = payload["package"]
    matching_packages: dict[str, dict[str, Any]] = {}
    for body in _json_candidates(surface.member_dir):
        if body.get("id") != pkg_pin["id"] or str(body.get("version", "")) != pkg_pin["version"]:
            continue
        try:
            digest = package_instance_checksum(body)
        except (TypeError, ValueError):
            continue
        if body.get("package_checksum") == digest:
            matching_packages[digest] = body
    package = matching_packages.get(str(pkg_pin["checksum"]))
    if package is None:
        return Refusal("PACKAGE_ABSENT_OR_MISMATCH", f"no verified package {pkg_pin['id']}@{pkg_pin['version']} on surface")
    if len(matching_packages) > 1:
        return Refusal("PACKAGE_AMBIGUOUS", "multiple distinct package bodies share the pinned identity")
    try:
        verify_published_package(package, package_checksums)
    except PackageIntegrityError as exc:
        return Refusal("PACKAGE_INTEGRITY", str(exc))

    corpus = _resolve_member_corpus(package, surface, citizen_checksums)
    if isinstance(corpus, Refusal):
        return corpus

    validation = validate_package(package, corpus, schemas, citizen_checksums)
    if not validation.ok:
        # Contained issues are reported in the refusal; they never authorize a
        # clean subset or an allowlist (ADR-0033 Decision 3 / Decision 5).
        issues = tuple(
            {"id": i.member_id, "version": i.version, "code": i.code, "detail": i.detail}
            for i in validation.issues
        )
        return Refusal("HARD_GATE_REFUSED", f"validation.ok is False ({len(issues)} contained issues)", issues)

    return ResolvedGraph(
        package=package,
        resolved_members=tuple(validation.resolved_members),
        adoption_act_id=str(selected["act_id"]),
        release_id=str(payload["release"]["id"]),
    )
