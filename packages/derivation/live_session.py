"""One-act live presentation session wiring.

The session path keeps the two content authorities separate: the renderer page
is fixed repository content, while the presentation model is read from the
live workspace produced by ``live_coordinate_run``.  This module deliberately
does not observe workstation state, add confinement, or reuse the browser
evaluation harness.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

from packages.derivation.live import LiveCoordinatorOutcome, live_coordinate_run
from packages.derivation.live_viewing import (
    LiveViewingError,
    LiveViewingSession,
    LiveViewingVehicle,
    PreflightProbes,
    run_viewing_preflight,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import PresentationModelError, validate_presentation_model
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.loader import DerivationSchemas


PAGE_RELATIVE_PATH = Path("tools/presentation_harness/examples/pages/citation-walk.v1.html")
_FIXTURE_ASSIGNMENT = "const FIXTURE = Object.freeze(__FIXTURE_JSON__);"


class PresentationSessionError(RuntimeError):
    """A locator-free refusal of the one-act presentation session."""

    def __init__(self, reason: str, *, reason_codes: Sequence[str] = ()) -> None:
        self.reason = reason
        self.reason_codes = tuple(reason_codes)
        super().__init__(reason)


class _PresentationHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, page: bytes) -> None:
        self.page = page
        super().__init__(("127.0.0.1", 0), _PresentationRequestHandler)


class _PresentationRequestHandler(BaseHTTPRequestHandler):
    server: _PresentationHTTPServer

    def log_message(self, _format: str, *_args: object) -> None:
        # Request paths are not diagnostics.  The session has no server log
        # surface that could accidentally retain a locator or query string.
        return

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler hook
        try:
            target = urlsplit(self.path)
        except ValueError:
            self.send_error(404)
            return
        if target.path != "/" or target.query or target.fragment:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.server.page)))
        self.end_headers()
        self.wfile.write(self.server.page)

    def do_HEAD(self) -> None:  # noqa: N802 - stdlib handler hook
        self.send_error(405)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler hook
        self.send_error(405)


class _PresentationServer:
    def __init__(self, page: bytes) -> None:
        self._http = _PresentationHTTPServer(page)
        self._thread = Thread(target=self._http.serve_forever, name="presentation-loopback", daemon=True)
        self._thread.start()
        port = self._http.server_address[1]
        self.origin = f"http://127.0.0.1:{port}"
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._http.shutdown()
        self._http.server_close()
        self._thread.join(timeout=3)
        if self._thread.is_alive():
            raise PresentationSessionError("presentation-server-teardown-failed")


def _confined_path(path: Path, root: Path, *, reason: str) -> Path:
    try:
        resolved_root = root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_root)
    except (OSError, RuntimeError, ValueError):
        raise PresentationSessionError(reason) from None
    return resolved_path


def _render_page(repo_root: Path, capability: WorkspaceCapability, model_path: Path) -> bytes:
    root = _confined_path(repo_root, repo_root, reason="presentation-page-unavailable")
    page_path = _confined_path(root / PAGE_RELATIVE_PATH, root, reason="presentation-page-unavailable")
    model_path = _confined_path(model_path, capability.location, reason="presentation-model-unavailable")
    try:
        page = page_path.read_text(encoding="utf-8")
        model = json.loads(model_path.read_text(encoding="utf-8"))
        if not isinstance(model, dict):
            raise ValueError("presentation model must be an object")
        validate_presentation_model(model)
        payload = json.dumps(model, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    except PresentationSessionError:
        raise
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, PresentationModelError):
        raise PresentationSessionError("presentation-model-unavailable") from None

    if page.count(_FIXTURE_ASSIGNMENT) != 1:
        raise PresentationSessionError("presentation-page-unavailable")
    return page.replace(
        _FIXTURE_ASSIGNMENT,
        f"const FIXTURE = Object.freeze({payload});",
        1,
    ).encode("utf-8")


@dataclass(repr=False)
class LivePresentationSession:
    """The owned browser and server resources for one viewing session."""

    _outcome: LiveCoordinatorOutcome
    url: str
    _browser: LiveViewingSession
    _server: _PresentationServer
    _closed: bool = False

    @property
    def run_id(self) -> str | None:
        return self._outcome.run_id

    def __repr__(self) -> str:
        return "<LivePresentationSession>"

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        teardown_failed = False
        try:
            self._browser.close()
        except (LiveViewingError, OSError):
            teardown_failed = True
        try:
            self._server.close()
        except (PresentationSessionError, OSError):
            teardown_failed = True
        if teardown_failed:
            raise PresentationSessionError("presentation-session-teardown-failed")

    def __enter__(self) -> "LivePresentationSession":
        return self

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()


def open_presentation_session(
    capability: WorkspaceCapability,
    *,
    probes: PreflightProbes,
    repo_root: Path,
    authoritative_acts: Sequence[Mapping[str, Any]],
    workspace_revision: int,
    run_scope: Mapping[str, str],
    scope_user: str,
    request: Mapping[str, Any],
    run_id: str,
    governance_pins: Sequence[Mapping[str, Any]],
    surface: PublicationSurface,
    output_name: str,
    schemas: DerivationSchemas | None = None,
    chrome_executable: str | Path | None = None,
    launch_timeout_seconds: float = 10.0,
    vehicle: LiveViewingVehicle | None = None,
) -> LivePresentationSession:
    """Run capability → preflight → model → loopback → browser → teardown.

    The caller supplies all preflight values.  A returned session owns the
    browser and loopback server and must be used as a context manager or closed
    explicitly.  All refusal surfaces use stable codes and never include paths.
    """

    verdict = run_viewing_preflight(capability, probes)
    if not verdict.allowed:
        raise PresentationSessionError("presentation-preflight-refused", reason_codes=verdict.reason_codes)

    try:
        outcome = live_coordinate_run(
            capability,
            repo_root=repo_root,
            authoritative_acts=authoritative_acts,
            workspace_revision=workspace_revision,
            run_scope=run_scope,
            scope_user=scope_user,
            request=request,
            run_id=run_id,
            governance_pins=governance_pins,
            surface=surface,
            output_name=output_name,
            schemas=schemas,
        )
    except Exception:
        raise PresentationSessionError("presentation-live-run-failed") from None
    if outcome.refusal is not None:
        raise PresentationSessionError("presentation-live-run-refused", reason_codes=(outcome.refusal.reason,))
    if outcome.presentation_path is None:
        raise PresentationSessionError("presentation-model-unavailable")

    try:
        page = _render_page(repo_root, capability, outcome.presentation_path)
        server = _PresentationServer(page)
    except PresentationSessionError:
        raise
    except (OSError, RuntimeError):
        raise PresentationSessionError("presentation-server-start-failed") from None

    url = f"{server.origin}/"
    try:
        viewing = (vehicle or LiveViewingVehicle()).launch(
            capability,
            chrome_executable=chrome_executable,
            launch_timeout_seconds=launch_timeout_seconds,
            initial_url=url,
        )
    except Exception:
        try:
            server.close()
        except Exception:
            pass
        raise
    return LivePresentationSession(_outcome=outcome, url=url, _browser=viewing, _server=server)


__all__ = [
    "LivePresentationSession",
    "PresentationSessionError",
    "open_presentation_session",
]
