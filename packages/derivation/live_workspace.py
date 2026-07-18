"""Live workspace bootstrap behind the ADR-0031 capability wall (Track 3).

The out-of-repo residency ``L`` is initialized from a runtime **capability**, not
from repository content: no locator is committed, and the location is supplied by
the capability the live-run environment holds. The bootstrap installs the D1
residency gates — a total, fail-closed classification (ADR-0031 Decision 2) and a
commit/push envelope guard — so they are *active over live artifacts*, not merely
validated in a test. This discharges the Track-1 review's F2 (the boundary schema
citizens are loaded into a runtime registry here, not only in-test) and consumes
ADR-0031's installed-residency conditions for this track.

Still synthetic: the workspace is bootstrapped and exercised with synthetic
artifacts. No personal data ever enters the repository; the classification gate is
the structural reason a personal artifact cannot cross the envelope.
"""

from __future__ import annotations

import os
import hashlib
import json
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from packages.kernel.schema_registry import SchemaRegistry

BOUNDARY_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas" / "boundary"
KERNEL_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas" / "kernel"

CLASSIFICATION_SCHEMA = "classification.v1"

_MAY_CROSS_KINDS = frozenset(
    {
        "public-origin code",
        "public-origin contract",
        "independently-constructed synthetic fixture",
    }
)


class ResidencyViolation(Exception):
    """A live artifact classified NEVER_CROSSES was presented at the envelope."""


class WorkspaceBootstrapError(Exception):
    """The declared residency location fails the ADR-0031 topology rule."""


class GuardIntegrityError(ResidencyViolation):
    """A commit/push gate was replaced or a raw transport was attempted."""


@dataclass(frozen=True)
class WorkspaceCapability:
    """The runtime authority to reach ``L``. Never committed to the repository."""

    location: Path
    repository_read_only: bool = True
    repository_write_allowed: bool = False
    publication_allowed: bool = False
    network_allowed: bool = False


@dataclass(frozen=True)
class Classification:
    decision: str
    kind: str | None = None
    reason: str | None = None

    def to_citizen(self) -> dict[str, Any]:
        body: dict[str, Any] = {"schema": CLASSIFICATION_SCHEMA, "decision": self.decision}
        if self.decision == "MAY_CROSS":
            body["kind"] = self.kind
        else:
            body["reason"] = self.reason
        return body


@dataclass(frozen=True, init=False)
class InstalledEnvelopeGuards:
    """An opaque capability minted only by installed live-workspace gates.

    It deliberately has no public constructor.  A path plus a reproducible
    digest is not authority: the capability is bound to one ``LiveWorkspace``
    instance and to the random installation recorded beneath its quarantine.
    """

    _workspace: Path
    _installation_id: str
    _authority: object

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        raise TypeError("InstalledEnvelopeGuards may only be minted by an installed LiveWorkspace gate")

    @classmethod
    def _mint(cls, workspace: Path, installation_id: str, authority: object) -> "InstalledEnvelopeGuards":
        guard = object.__new__(cls)
        object.__setattr__(guard, "_workspace", workspace)
        object.__setattr__(guard, "_installation_id", installation_id)
        object.__setattr__(guard, "_authority", authority)
        return guard


def _boundary_registry() -> SchemaRegistry:
    """Load the D1 boundary citizens into a runtime registry (F2 discharge)."""
    return SchemaRegistry([KERNEL_SCHEMA_DIR, BOUNDARY_SCHEMA_DIR])


@dataclass
class LiveWorkspace:
    """An initialized residency behind the capability wall with active gates."""

    location: Path
    registry: SchemaRegistry
    _guard_authority: object = field(default_factory=object, init=False, repr=False)
    _installation_id: str | None = field(default=None, init=False, repr=False)
    _installed_digests: dict[str, str] = field(default_factory=dict, init=False, repr=False)

    _GATE_DIR = ".residency-envelope-gates"
    _MANIFEST = "manifest.json"
    _SURFACES = ("commit", "push")

    def _gate_root(self) -> Path:
        return self.location / self._GATE_DIR

    @staticmethod
    def _gate_bytes(surface: str, installation_id: str) -> bytes:
        """Stable local hook body; the random installation id binds its files."""
        return (
            "attestory ADR-0031 envelope gate\n"
            f"surface={surface}\n"
            f"installation={installation_id}\n"
            "scan=complete-declared-envelope\n"
        ).encode("utf-8")

    def _read_installed_manifest(self) -> dict[str, object]:
        root = self._gate_root()
        manifest_path = root / self._MANIFEST
        try:
            body = json.loads(manifest_path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GuardIntegrityError("installed commit/push gates are missing or unreadable") from exc
        if not isinstance(body, dict):
            raise GuardIntegrityError("installed commit/push gate manifest is invalid")
        return body

    def _verify_installed_gates(self) -> str:
        """Verify two separately-installed local gate files before crossing."""
        manifest = self._read_installed_manifest()
        installation_id = manifest.get("installation_id")
        digests = manifest.get("digests")
        if (
            not isinstance(installation_id, str)
            or not isinstance(digests, dict)
            or installation_id != self._installation_id
            or digests != self._installed_digests
        ):
            raise GuardIntegrityError("installed commit/push gate manifest is incomplete")
        for surface in self._SURFACES:
            expected = self._installed_digests.get(surface)
            if not isinstance(expected, str):
                raise GuardIntegrityError(f"installed {surface} gate manifest entry is missing")
            try:
                actual = hashlib.sha256((self._gate_root() / f"{surface}.gate").read_bytes()).hexdigest()
            except OSError as exc:
                raise GuardIntegrityError(f"installed {surface} gate is missing") from exc
            if not secrets.compare_digest(expected, actual):
                raise GuardIntegrityError(f"installed {surface} gate was tampered")
        return installation_id

    def install_envelope_guards(self) -> InstalledEnvelopeGuards:
        """Install distinct commit/push gates and mint their opaque authority.

        Gate state lives only under the runtime residency.  No repository file,
        locator, or deterministic path-derived token participates in authority.
        Every bootstrap refreshes the local gate pair and mints a fresh
        in-process capability that callers cannot fabricate.
        """
        root = self._gate_root()
        if root.is_symlink():
            raise GuardIntegrityError("installed gate directory may not be a symlink")
        root.mkdir(mode=0o700, exist_ok=True)
        # A bootstrap gets fresh installation material.  It never treats a
        # pre-existing local manifest as authority; the in-process expected
        # digests below are the authority that detects a manifest+hook rewrite.
        installation_id = secrets.token_urlsafe(32)
        digests: dict[str, str] = {}
        for surface in self._SURFACES:
            gate_path = root / f"{surface}.gate"
            if gate_path.is_symlink():
                raise GuardIntegrityError(f"installed {surface} gate may not be a symlink")
            gate_bytes = self._gate_bytes(surface, installation_id)
            gate_path.write_bytes(gate_bytes)
            gate_path.chmod(0o600)
            digests[surface] = hashlib.sha256(gate_bytes).hexdigest()
        manifest_path = root / self._MANIFEST
        if manifest_path.is_symlink():
            raise GuardIntegrityError("installed gate manifest may not be a symlink")
        manifest_path.write_text(
            json.dumps({"installation_id": installation_id, "digests": digests}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        manifest_path.chmod(0o600)
        self._installation_id = installation_id
        self._installed_digests = digests
        return InstalledEnvelopeGuards._mint(self.location, installation_id, self._guard_authority)

    def _require_installed_guard(self, guard: InstalledEnvelopeGuards) -> None:
        if (
            type(guard) is not InstalledEnvelopeGuards
            or guard._workspace != self.location
            or guard._authority is not self._guard_authority
            or guard._installation_id != self._verify_installed_gates()
        ):
            raise GuardIntegrityError("commit/push requires the integrity-checked installed envelope guard")

    def classify(self, artifact: Mapping[str, Any]) -> Classification:
        """Total, fail-closed classification (ADR-0031 Decision 2).

        MAY_CROSS requires exactly one proven public kind. Personal provenance,
        personal description, or missing/unknown proof is deterministically
        NEVER_CROSSES — there is no undecided outcome. The result is validated
        against the runtime boundary schema, so the gate is enforced by the
        published citizen, not a private notion.
        """
        classification = self._classify(artifact)
        # Enforced by the runtime boundary schema, not a private predicate.
        self.registry.validate_declared(classification.to_citizen())
        return classification

    def _classify(self, artifact: Mapping[str, Any]) -> Classification:
        if _has_sensitive_lineage(artifact):
            return Classification("NEVER_CROSSES", reason="personal provenance or description")
        kind = artifact.get("kind")
        if kind in _MAY_CROSS_KINDS and artifact.get("public_origin_proof"):
            return Classification("MAY_CROSS", kind=kind)
        return Classification("NEVER_CROSSES", reason="no public-origin proof")

    def _scan_declared_envelope(self, artifacts: Sequence[Mapping[str, Any]], *, surface: str) -> None:
        """Classify every declared artifact before its commit or push crossing."""
        for artifact in artifacts:
            if self.classify(artifact).decision != "MAY_CROSS":
                raise ResidencyViolation(
                    f"{surface}: artifact {artifact.get('name', '<unnamed>')!r} is NEVER_CROSSES"
                )

    def guarded_commit(
        self, guard: InstalledEnvelopeGuards, artifacts: Sequence[Mapping[str, Any]], *, no_verify: bool = False
    ) -> None:
        """The only modeled commit crossing; ``--no-verify`` is a hard refusal."""
        if no_verify:
            raise GuardIntegrityError("--no-verify cannot bypass the installed commit gate")
        self._require_installed_guard(guard)
        self._scan_declared_envelope(artifacts, surface="commit")

    def guarded_push(
        self, guard: InstalledEnvelopeGuards, artifacts: Sequence[Mapping[str, Any]], *, raw_transport: bool = False
    ) -> None:
        """The only modeled push crossing; raw transport is a hard refusal."""
        if raw_transport:
            raise GuardIntegrityError("raw transport cannot bypass the installed push gate")
        self._require_installed_guard(guard)
        self._scan_declared_envelope(artifacts, surface="push")

    def live_output_path(self, relative_path: Path) -> Path:
        """Return a quarantine-contained output path or refuse the write.

        Process records, caches, reports, and failures from a live run may only
        be written under ``L``.  A relative path is required so an output cannot
        use an absolute path or ``..`` to escape the capability root.
        """
        if relative_path.is_absolute():
            raise ResidencyViolation("live output path must be relative to the workspace")
        target = (self.location / relative_path).resolve()
        if target != self.location and self.location not in target.parents:
            raise ResidencyViolation("live output path escapes the workspace")
        return target

    def reserve_live_output_path(self, relative_path: Path) -> Path:
        """Atomically reserve a validated output slot before a run begins."""
        target = self.live_output_path(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise ResidencyViolation("declared live output path is already reserved") from exc
        os.close(descriptor)
        return target


def _has_sensitive_lineage(artifact: Mapping[str, Any]) -> bool:
    """Apply ADR-0031's monotone description/provenance rule recursively."""
    if artifact.get("personal_provenance") or artifact.get("describes_personal"):
        return True
    nested = artifact.get("inputs", ())
    if not isinstance(nested, Sequence) or isinstance(nested, (str, bytes)):
        return bool(artifact.get("unknown_or_unreadable_proof"))
    return bool(artifact.get("unknown_or_unreadable_proof")) or any(
        isinstance(item, Mapping) and _has_sensitive_lineage(item) for item in nested
    )


def _assert_topology(capability: WorkspaceCapability, repo_root: Path) -> Path:
    """Audit the local, observable portion of the D1 capability wall."""
    if (
        not capability.repository_read_only
        or capability.repository_write_allowed
        or capability.publication_allowed
        or capability.network_allowed
    ):
        raise WorkspaceBootstrapError("live capability grants repository write or publication/network access")

    declared = capability.location.absolute()
    if declared.is_symlink():
        raise WorkspaceBootstrapError("residency location may not be a symlink")
    location = declared.resolve()
    if location == repo_root or repo_root in location.parents:
        raise WorkspaceBootstrapError(
            f"residency location {location} is inside the repository {repo_root}"
        )
    if location.exists() and (location / ".git").exists():
        raise WorkspaceBootstrapError("residency location may not contain a Git administrative directory")
    # A same inode would be a hard-link bridge even when two path spellings look
    # disjoint.  The roots are enough at bootstrap; subsequent live outputs are
    # constrained by ``live_output_path`` and never placed in the repository.
    try:
        if location.exists() and os.path.samestat(location.stat(), repo_root.stat()):
            raise WorkspaceBootstrapError("residency and repository share an inode")
    except OSError as exc:
        raise WorkspaceBootstrapError(f"cannot audit residency topology: {exc}") from exc
    return location


def bootstrap_workspace(
    capability: WorkspaceCapability, *, repo_root: Path
) -> LiveWorkspace:
    """Initialize ``L`` from the capability, behind the residency topology wall.

    The location must be outside the repository working tree and its git store
    (ADR-0031 Decision 1); a location inside the repo is a bootstrap error, not a
    silent fallback. No locator is read from repository content — it arrives only
    through ``capability``.
    """
    repo_root = repo_root.resolve()
    location = _assert_topology(capability, repo_root)
    if not location.exists():
        location.mkdir(parents=True, exist_ok=True)
    return LiveWorkspace(location=location, registry=_boundary_registry())
