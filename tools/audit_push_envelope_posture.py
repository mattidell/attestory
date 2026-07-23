"""Audit the installed push-envelope gate's honest local posture.

The audit builds a fresh Git clone backed by a local bare remote.  It proves
the installed hook bytes, observes a seeded marker refusal on an ordinary
push, and then observes that ``git push --no-verify`` reaches that synthetic
remote.  It does not inspect credentials or contact a network remote.

Its JSON record deliberately reports credential confinement as unestablished:
this audit describes the hook boundary that exists, not a guarded transport
boundary that does not.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


TOOLS_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable


@dataclass(frozen=True)
class Posture:
    """The stable, intentionally narrow push-envelope posture record."""

    hooks_verified: bool
    hooked_marker_refused: bool
    no_verify_bypass_reachable: bool
    credential_confinement: str = "unestablished"

    @property
    def verified(self) -> bool:
        return (
            self.hooks_verified
            and self.hooked_marker_refused
            and self.no_verify_bypass_reachable
            and self.credential_confinement == "unestablished"
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)


def _git(arguments: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        [
            "git",
            "-c",
            "user.name=push-envelope-audit",
            "-c",
            "user.email=push-envelope-audit@example.invalid",
            *arguments,
        ],
        cwd,
    )


def _succeeded(completed: subprocess.CompletedProcess[str]) -> bool:
    return completed.returncode == 0


def _copy_gate_tools(workspace: Path) -> None:
    destination = workspace / "tools"
    destination.mkdir()
    for name in ("__init__.py", "envelope_scan.py", "install_envelope_hooks.py"):
        shutil.copyfile(TOOLS_DIR / name, destination / name)


def make_audit_workspace(root: Path) -> tuple[Path, Path]:
    """Make a fresh clone and a local-only remote for the authoritative probe."""
    remote = root / "synthetic-remote.git"
    workspace = root / "synthetic-workspace"
    if not _succeeded(_git(["init", "--bare", str(remote)], root)):
        raise RuntimeError("could not initialize the synthetic remote")
    if not _succeeded(_git(["clone", str(remote), str(workspace)], root)):
        raise RuntimeError("could not clone the synthetic remote")
    _copy_gate_tools(workspace)
    if not _succeeded(_run([PYTHON, "tools/install_envelope_hooks.py"], workspace)):
        raise RuntimeError("could not install the synthetic workspace hooks")
    return workspace, remote


def _remote_ref(remote: Path, ref: str) -> str | None:
    completed = _run(["git", f"--git-dir={remote}", "rev-parse", "--verify", ref], remote)
    return completed.stdout.strip() if _succeeded(completed) else None


def _hook_bytes_verify(workspace: Path) -> bool:
    return _succeeded(_run([PYTHON, "tools/envelope_scan.py", "--verify"], workspace))


def audit_workspace(workspace: Path, remote: Path) -> Posture:
    """Exercise the installed gate against one prepared synthetic workspace."""
    hooks_verified = _hook_bytes_verify(workspace)
    if not hooks_verified:
        return Posture(False, False, False)

    clean_file = workspace / "clean.txt"
    clean_file.write_text("synthetic clean commit\n", encoding="utf-8")
    if not _succeeded(_git(["add", clean_file.name], workspace)):
        return Posture(True, False, False)
    if not _succeeded(_git(["commit", "-m", "synthetic clean"], workspace)):
        return Posture(True, False, False)
    if not _succeeded(_git(["push", "origin", "HEAD:refs/heads/main"], workspace)):
        return Posture(True, False, False)
    clean_head = _git(["rev-parse", "HEAD"], workspace).stdout.strip()
    if _remote_ref(remote, "refs/heads/main") != clean_head:
        return Posture(True, False, False)

    marker_file = workspace / "marker.txt"
    marker = "/Us" + "ers/" + "synthetic-owner/return.pdf"
    marker_file.write_text(marker + "\n", encoding="utf-8")
    if not _succeeded(_git(["add", marker_file.name], workspace)):
        return Posture(True, False, False)
    if not _succeeded(_git(["commit", "--no-verify", "-m", "synthetic marker"], workspace)):
        return Posture(True, False, False)

    refused = _git(["push", "origin", "HEAD:refs/heads/main"], workspace)
    refusal_text = refused.stdout + refused.stderr
    hooked_marker_refused = (
        not _succeeded(refused)
        and "envelope gate: push refused" in refusal_text
        and _remote_ref(remote, "refs/heads/main") == clean_head
    )

    bypass = _git(["push", "--no-verify", "origin", "HEAD:refs/heads/main"], workspace)
    marker_head = _git(["rev-parse", "HEAD"], workspace).stdout.strip()
    no_verify_bypass_reachable = (
        _succeeded(bypass) and _remote_ref(remote, "refs/heads/main") == marker_head
    )
    return Posture(hooks_verified, hooked_marker_refused, no_verify_bypass_reachable)


def audit() -> Posture:
    """Run the fully local synthetic audit, converting setup failures to a failed posture."""
    try:
        with TemporaryDirectory(prefix="push-envelope-posture-") as temporary:
            workspace, remote = make_audit_workspace(Path(temporary))
            return audit_workspace(workspace, remote)
    except RuntimeError:
        return Posture(False, False, False)


def main() -> int:
    posture = audit()
    print(posture.to_json())
    return 0 if posture.verified else 1


if __name__ == "__main__":
    sys.exit(main())
