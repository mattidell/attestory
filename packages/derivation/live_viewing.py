"""Confined headed viewing support for a runtime live-workspace capability.

This module implements the controllable filesystem part of ADR-0047.  It does
not create a trust boundary for a same-authority browser process: the browser
flags only reduce accidental background traffic, while navigation policy is a
separate cooperative check.  The module has no publication credential or
publication path.

All externally observable failures use closed reason codes.  In particular,
none of the exception or verdict surfaces contain the capability location.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from packages.derivation.live_workspace import WorkspaceCapability


class ViewingReason(str, Enum):
    """Stable diagnostics for a viewing vehicle or preflight refusal."""

    CAPABILITY_UNAVAILABLE = "viewing-capability-unavailable"
    WORKSPACE_UNREADABLE = "viewing-workspace-unreadable"
    PATH_NOT_CONFINED = "viewing-path-not-confined"
    BROWSER_NOT_FOUND = "viewing-browser-not-found"
    BROWSER_LAUNCH_FAILED = "viewing-browser-launch-failed"
    BROWSER_START_TIMEOUT = "viewing-browser-start-timeout"
    BROWSER_EXITED_DURING_LAUNCH = "viewing-browser-exited-during-launch"
    BROWSER_TEARDOWN_FAILED = "viewing-browser-teardown-failed"
    NON_LOOPBACK_NAVIGATION = "viewing-navigation-non-loopback"
    BACKUP_PRESENT = "viewing-residency-backup-present"
    BACKUP_INDETERMINATE = "viewing-residency-backup-indeterminate"
    INDEX_PRESENT = "viewing-residency-index-present"
    INDEX_INDETERMINATE = "viewing-residency-index-indeterminate"
    CLIPBOARD_HISTORY_PRESENT = "viewing-clipboard-history-present"
    CLIPBOARD_HISTORY_UNDETECTABLE = "viewing-clipboard-history-undetectable-remainder"


class LiveViewingError(RuntimeError):
    """A fail-closed viewing refusal with no locator-bearing detail."""

    def __init__(self, reason: ViewingReason) -> None:
        self.reason = reason
        super().__init__(reason.value)


class ProbeState(str, Enum):
    """The only probe states admitted by the preflight."""

    PRESENT = "present"
    ABSENT = "absent"
    UNKNOWN = "unknown"
    UNREADABLE = "unreadable"


@dataclass(frozen=True)
class PreflightProbes:
    """Probe results or zero-argument observers supplied by live-run code.

    ``backup_inclusion`` and ``content_indexing`` are always-decidable inputs:
    only ``False``/``ABSENT`` is a pass.  Clipboard history is intentionally
    partial; an unknown result is carried as an owner responsibility rather
    than being represented as a complete clearance.  Observer exceptions are
    converted to ``UNREADABLE`` by the preflight.
    """

    backup_inclusion: object = ProbeState.UNKNOWN
    content_indexing: object = ProbeState.UNKNOWN
    clipboard_history: object = ProbeState.UNKNOWN


@dataclass(frozen=True)
class PreflightVerdict:
    """Locator-free preflight result."""

    allowed: bool
    reason_codes: tuple[str, ...] = ()
    owner_responsibilities: tuple[str, ...] = ()


def _state(value: object) -> ProbeState:
    if isinstance(value, ProbeState):
        return value
    if isinstance(value, bool):
        return ProbeState.PRESENT if value else ProbeState.ABSENT
    if isinstance(value, str):
        try:
            return ProbeState(value)
        except ValueError:
            return ProbeState.UNKNOWN
    return ProbeState.UNKNOWN


def _observe(value: object) -> object:
    if not callable(value):
        return value
    try:
        return value()
    except Exception:
        return ProbeState.UNREADABLE


def _capability_ready(capability: WorkspaceCapability | None) -> bool:
    if not isinstance(capability, WorkspaceCapability):
        return False
    try:
        return capability.location.is_dir()
    except (OSError, RuntimeError, TypeError):
        return False


def run_viewing_preflight(
    capability: WorkspaceCapability | None,
    probes: PreflightProbes | None,
) -> PreflightVerdict:
    """Return a fail-closed verdict for the observable workstation state.

    The first two checks are total: an indeterminate result refuses.  The
    clipboard check is deliberately partial, so an undetectable result does
    not block mechanically but records an owner-responsibility code.  That
    code is not a completeness claim.
    """

    if not _capability_ready(capability):
        return PreflightVerdict(False, (ViewingReason.CAPABILITY_UNAVAILABLE.value,))
    if not isinstance(probes, PreflightProbes):
        probes = PreflightProbes()

    refusals: list[str] = []

    backup = _state(_observe(probes.backup_inclusion))
    if backup is ProbeState.PRESENT:
        refusals.append(ViewingReason.BACKUP_PRESENT.value)
    elif backup is not ProbeState.ABSENT:
        refusals.append(ViewingReason.BACKUP_INDETERMINATE.value)

    indexing = _state(_observe(probes.content_indexing))
    if indexing is ProbeState.PRESENT:
        refusals.append(ViewingReason.INDEX_PRESENT.value)
    elif indexing is not ProbeState.ABSENT:
        refusals.append(ViewingReason.INDEX_INDETERMINATE.value)

    clipboard = _state(_observe(probes.clipboard_history))
    if clipboard is ProbeState.PRESENT:
        refusals.append(ViewingReason.CLIPBOARD_HISTORY_PRESENT.value)

    if refusals:
        return PreflightVerdict(False, tuple(refusals))

    # The false/absent result only reports what this probe observed.  It never
    # upgrades a partially decidable clipboard check into a clearance claim.
    return PreflightVerdict(
        True,
        owner_responsibilities=(ViewingReason.CLIPBOARD_HISTORY_UNDETECTABLE.value,),
    )


@dataclass(frozen=True)
class _ConfinedDestinations:
    session_root: Path
    profile: Path
    cache: Path
    downloads: Path
    print_to_file: Path


def _within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return candidate != root


def _confined_destinations(capability: WorkspaceCapability | None) -> _ConfinedDestinations:
    if capability is None or not isinstance(capability, WorkspaceCapability):
        raise LiveViewingError(ViewingReason.CAPABILITY_UNAVAILABLE)
    if not _capability_ready(capability):
        raise LiveViewingError(ViewingReason.CAPABILITY_UNAVAILABLE)

    try:
        root = capability.location.resolve(strict=True)
        if not root.is_dir():
            raise LiveViewingError(ViewingReason.WORKSPACE_UNREADABLE)
        container = root / ".live-view"
        session = container / f"session-{uuid.uuid4().hex}"
        destinations = _ConfinedDestinations(
            session_root=session,
            profile=session / "profile",
            cache=session / "cache",
            downloads=session / "downloads",
            print_to_file=session / "print" / "view.pdf",
        )
        for candidate in (
            container,
            destinations.session_root,
            destinations.profile,
            destinations.cache,
            destinations.downloads,
            destinations.print_to_file,
        ):
            resolved = candidate.resolve(strict=False)
            if not _within(root, resolved):
                raise LiveViewingError(ViewingReason.PATH_NOT_CONFINED)
            # Refuse symlinked destinations even when they happen to point back
            # inside.  This keeps teardown from ever following a link.
            if candidate.exists() and candidate.is_symlink():
                raise LiveViewingError(ViewingReason.PATH_NOT_CONFINED)
    except LiveViewingError:
        raise
    except (OSError, RuntimeError, ValueError, TypeError):
        raise LiveViewingError(ViewingReason.WORKSPACE_UNREADABLE) from None
    return destinations


def _make_destinations(destinations: _ConfinedDestinations) -> None:
    try:
        destinations.session_root.mkdir(parents=True, exist_ok=False)
        destinations.profile.mkdir()
        destinations.cache.mkdir()
        destinations.downloads.mkdir()
        destinations.print_to_file.parent.mkdir()
        # Recheck after creation, closing the obvious symlink/race window before
        # the browser receives any of these paths.
        root = destinations.session_root.parents[1].resolve(strict=True)
        for candidate in (
            destinations.session_root,
            destinations.profile,
            destinations.cache,
            destinations.downloads,
            destinations.print_to_file,
        ):
            if not _within(root, candidate.resolve(strict=False)):
                raise LiveViewingError(ViewingReason.PATH_NOT_CONFINED)
    except LiveViewingError:
        raise
    except (OSError, RuntimeError, ValueError):
        raise LiveViewingError(ViewingReason.PATH_NOT_CONFINED) from None


def _remove_session(destinations: _ConfinedDestinations) -> None:
    try:
        root = destinations.session_root.parents[1].resolve(strict=True)
        session = destinations.session_root.resolve(strict=False)
        if not _within(root, session) or destinations.session_root.is_symlink():
            raise LiveViewingError(ViewingReason.PATH_NOT_CONFINED)
        shutil.rmtree(destinations.session_root)
        container = destinations.session_root.parent
        if (
            not container.is_symlink()
            and _within(root, container.resolve(strict=False))
        ):
            # Remove only our empty container; a pre-existing sibling session
            # or other live-workspace content remains untouched.
            try:
                container.rmdir()
            except OSError:
                pass
    except LiveViewingError:
        raise
    except (OSError, RuntimeError, ValueError):
        raise LiveViewingError(ViewingReason.BROWSER_TEARDOWN_FAILED) from None


def _executable(path: Path) -> bool:
    try:
        return path.is_file() and os.access(path, os.X_OK)
    except OSError:
        return False


_BROWSER_CANDIDATES = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/google-chrome-stable"),
    Path("/usr/bin/chromium"),
    Path("/usr/bin/chromium-browser"),
)


def _resolve_browser(explicit: str | os.PathLike[str] | None) -> Path:
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(Path(explicit))
    candidates.extend(_BROWSER_CANDIDATES)
    for candidate in candidates:
        if _executable(candidate):
            return candidate
    raise LiveViewingError(ViewingReason.BROWSER_NOT_FOUND)


def _wait_for_devtools(profile: Path, process: Any, timeout: float) -> str:
    active_port = profile / "DevToolsActivePort"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            lines = active_port.read_text(encoding="utf-8").splitlines()
            port = int(lines[0])
            if port > 0:
                suffix = lines[1].strip() if len(lines) > 1 else ""
                return f"ws://127.0.0.1:{port}{suffix}"
        except (OSError, ValueError, IndexError):
            pass
        try:
            if process.poll() is not None:
                raise LiveViewingError(ViewingReason.BROWSER_EXITED_DURING_LAUNCH)
        except AttributeError:
            pass
        time.sleep(0.01)
    raise LiveViewingError(ViewingReason.BROWSER_START_TIMEOUT)


def _stop_process(process: Any) -> bool:
    """Stop and reap an owned process, making a final kill attempt on errors."""

    try:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
        return process.poll() is not None
    except (OSError, subprocess.SubprocessError, AttributeError):
        try:
            process.kill()
            process.wait(timeout=3)
        except (OSError, subprocess.SubprocessError, AttributeError):
            return False
        return process.poll() is not None


class LiveViewingSession:
    """Owned headed-browser session; construction is internal to the vehicle."""

    def __init__(self, process: Any, destinations: _ConfinedDestinations, websocket_url: str) -> None:
        self._process = process
        self._destinations = destinations
        self.websocket_url = websocket_url
        self._closed = False

    def navigate(self, url: str) -> str:
        """Validate a navigation target before any browser operation."""

        _validate_navigation_url(url)
        return url

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        teardown_error = False
        if not _stop_process(self._process):
            teardown_error = True
        try:
            _remove_session(self._destinations)
        except LiveViewingError:
            teardown_error = True
        if teardown_error:
            raise LiveViewingError(ViewingReason.BROWSER_TEARDOWN_FAILED)

    def __enter__(self) -> "LiveViewingSession":
        return self

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()


class LiveViewingVehicle:
    """Launch a headed browser with all product-controlled destinations confined."""

    def __init__(self, *, process_factory: Callable[..., Any] = subprocess.Popen) -> None:
        self._process_factory = process_factory

    def launch(
        self,
        capability: WorkspaceCapability | None,
        *,
        chrome_executable: str | os.PathLike[str] | None = None,
        launch_timeout_seconds: float = 10.0,
    ) -> LiveViewingSession:
        """Launch from capability state only; destination paths have no caller input."""

        destinations = _confined_destinations(capability)
        process = None
        try:
            _make_destinations(destinations)
            executable = _resolve_browser(chrome_executable)
            args = [
                str(executable),
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-sync",
                "--disable-translate",
                "--mute-audio",
                "--disable-gpu",
                f"--user-data-dir={destinations.profile}",
                f"--disk-cache-dir={destinations.cache}",
                f"--download-default-directory={destinations.downloads}",
                f"--print-to-pdf={destinations.print_to_file}",
                "--remote-debugging-port=0",
                "about:blank",
            ]
            if hasattr(os, "getuid") and os.getuid() == 0:
                args.insert(1, "--no-sandbox")
            process = self._process_factory(
                args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            websocket_url = _wait_for_devtools(destinations.profile, process, launch_timeout_seconds)
            if process.poll() is not None:
                raise LiveViewingError(ViewingReason.BROWSER_EXITED_DURING_LAUNCH)
            return LiveViewingSession(process, destinations, websocket_url)
        except LiveViewingError:
            if process is not None:
                _stop_process(process)
            try:
                _remove_session(destinations)
            except LiveViewingError:
                pass
            raise
        except (OSError, subprocess.SubprocessError, TypeError):
            if process is not None:
                _stop_process(process)
            try:
                _remove_session(destinations)
            except LiveViewingError:
                pass
            raise LiveViewingError(ViewingReason.BROWSER_LAUNCH_FAILED) from None


def validate_loopback_navigation(url: str) -> None:
    """Raise the stable refusal code for a non-loopback navigation target."""

    _validate_navigation_url(url)


def _validate_navigation_url(url: str) -> None:
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
    except (AttributeError, TypeError, ValueError):
        raise LiveViewingError(ViewingReason.NON_LOOPBACK_NAVIGATION) from None
    if parsed.scheme not in {"http", "https"} or host not in {"127.0.0.1", "localhost", "::1"}:
        raise LiveViewingError(ViewingReason.NON_LOOPBACK_NAVIGATION)


__all__ = [
    "LiveViewingError",
    "LiveViewingSession",
    "LiveViewingVehicle",
    "PreflightProbes",
    "PreflightVerdict",
    "ProbeState",
    "ViewingReason",
    "run_viewing_preflight",
    "validate_loopback_navigation",
]
