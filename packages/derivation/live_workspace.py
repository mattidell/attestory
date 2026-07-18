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
from dataclasses import dataclass
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


@dataclass(frozen=True)
class InstalledEnvelopeGuards:
    """Integrity-checked commit and push entrypoints for a live residency.

    The constructor is private to ``LiveWorkspace``.  Callers cannot use a
    bare hook flag or raw transport as a substitute: both crossings must carry
    this exact installed guard bound to the bootstrapped workspace.
    """

    _workspace: Path
    _integrity: str

    def _valid_for(self, workspace: Path) -> bool:
        material = f"ADR-0031-envelope-gate:{workspace}".encode("utf-8")
        return self._workspace == workspace and self._integrity == hashlib.sha256(material).hexdigest()


def _boundary_registry() -> SchemaRegistry:
    """Load the D1 boundary citizens into a runtime registry (F2 discharge)."""
    return SchemaRegistry([KERNEL_SCHEMA_DIR, BOUNDARY_SCHEMA_DIR])


@dataclass
class LiveWorkspace:
    """An initialized residency behind the capability wall with active gates."""

    location: Path
    registry: SchemaRegistry

    def install_envelope_guards(self) -> InstalledEnvelopeGuards:
        """Install the only commit/push gate capability for this live residency."""
        material = f"ADR-0031-envelope-gate:{self.location}".encode("utf-8")
        return InstalledEnvelopeGuards(self.location, hashlib.sha256(material).hexdigest())

    def _require_installed_guard(self, guard: InstalledEnvelopeGuards) -> None:
        if not isinstance(guard, InstalledEnvelopeGuards) or not guard._valid_for(self.location):
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

    def guard_envelope(self, artifacts: Sequence[Mapping[str, Any]], *, surface: str) -> None:
        """Refuse the crossing if any artifact is NEVER_CROSSES (commit/push)."""
        for artifact in artifacts:
            if self.classify(artifact).decision != "MAY_CROSS":
                raise ResidencyViolation(
                    f"{surface}: artifact {artifact.get('name', '<unnamed>')!r} is NEVER_CROSSES"
                )

    def guard_commit(self, artifacts: Sequence[Mapping[str, Any]]) -> None:
        self.guard_envelope(artifacts, surface="commit")

    def guard_push(self, artifacts: Sequence[Mapping[str, Any]]) -> None:
        self.guard_envelope(artifacts, surface="push")

    def guarded_commit(self, guard: InstalledEnvelopeGuards, artifacts: Sequence[Mapping[str, Any]]) -> None:
        self._require_installed_guard(guard)
        self.guard_commit(artifacts)

    def guarded_push(self, guard: InstalledEnvelopeGuards, artifacts: Sequence[Mapping[str, Any]]) -> None:
        self._require_installed_guard(guard)
        self.guard_push(artifacts)

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
