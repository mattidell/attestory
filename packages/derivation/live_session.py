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
from hmac import compare_digest
from pathlib import Path
from secrets import token_urlsafe
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


PAGE_RELATIVE_PATH = Path("packages/presentation/pages/citation-walk.v1.html")
_MODEL_ASSIGNMENT = "const MODEL = Object.freeze(__MODEL_JSON__);"

# The evaluation fixture page under tools/presentation_harness/examples/ states
# in its title, its header, and its own comment that it carries synthetic
# demo-* data and never a real workspace. Serving it during a live session
# would put those claims on the screen the owner reads while forming the
# attestation. A page that declares a provenance it cannot verify is not
# servable here, so this refuses on the declaration rather than trusting
# PAGE_RELATIVE_PATH to keep pointing somewhere honest.
_PROVENANCE_CLAIM_MARKERS = ("synthetic demo-*", "synthetic <code>demo-*</code>")


class PresentationSessionError(RuntimeError):
    """A locator-free refusal of the one-act presentation session."""

    def __init__(self, reason: str, *, reason_codes: Sequence[str] = ()) -> None:
        self.reason = reason
        self.reason_codes = tuple(reason_codes)
        super().__init__(reason)


class _PresentationHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, page: bytes, route: str) -> None:
        self.page = page
        self.route = route
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
        if target.query or target.fragment or not compare_digest(target.path, self.server.route):
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
    """A loopback origin serving exactly one unguessable route.

    The served body carries the whole presentation model inline, so the socket
    is a live-data channel for as long as the session runs. Loopback binding
    alone does not confine it: every local account can reach ``127.0.0.1``, and
    an ephemeral port is not a secret — the whole range is scannable in well
    under a second. The route below is a 256-bit token, which is what actually
    keeps the model from being retrievable by an unrelated local process.

    This does not confine a process that can read this program's memory,
    arguments, or the workspace itself. Those remain the same-UID residuals
    ADR-0044 and ADR-0047 already name.
    """

    def __init__(self, page: bytes) -> None:
        route = f"/{token_urlsafe(32)}"
        self._http = _PresentationHTTPServer(page, route)
        self._thread = Thread(target=self._http.serve_forever, name="presentation-loopback", daemon=True)
        self._thread.start()
        port = self._http.server_address[1]
        self.url = f"http://127.0.0.1:{port}{route}"
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        # ``server_close`` releases the listening socket and must run even if
        # ``shutdown`` raises. Otherwise a failure in the first call leaves a
        # socket still serving the whole presentation model to any local
        # process, and leaves it silently, since the caller's teardown is
        # best-effort on a failing path.
        try:
            self._http.shutdown()
        finally:
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

    if any(marker in page for marker in _PROVENANCE_CLAIM_MARKERS):
        raise PresentationSessionError("presentation-page-declares-provenance")
    if page.count(_MODEL_ASSIGNMENT) != 1:
        raise PresentationSessionError("presentation-page-unavailable")
    return page.replace(
        _MODEL_ASSIGNMENT,
        f"const MODEL = Object.freeze({payload});",
        1,
    ).encode("utf-8")


def _release_quietly(viewing: LiveViewingSession | None, server: "_PresentationServer") -> None:
    """Release both owned resources on a failing exit path, best effort.

    Both are attempted regardless of the other failing: a browser left
    displaying the real return and a socket still serving the model are
    independent problems, so neither may be skipped because the other raised.
    This runs while another exception is already in flight and must not replace
    it, so a teardown failure here is invisible — a named residual.
    """

    if viewing is not None:
        try:
            viewing.close()
        except Exception:
            pass
    try:
        server.close()
    except Exception:
        pass


def _classified_viewing_failure(failure: BaseException) -> PresentationSessionError:
    """Convert any launch-time failure into a classified, locator-free refusal.

    ``LiveViewingError`` is a *sibling* of ``PresentationSessionError``, not a
    subclass, so before this wrapping a browser-, confinement-, or
    workspace-originated refusal escaped this function unchanged and reached the
    caller as a raw traceback. That matters beyond tidiness: the owner's
    non-descriptive failure vocabulary (``docs/runbooks/presentation-real-session.md``)
    rests on every failure arriving pre-classified as a stable reason code the
    owner may legally report. An unclassified traceback is precisely the text
    the vocabulary cannot describe, in the one session that cannot be repeated.

    The guarantee belongs here rather than in the runbook's copyable example: a
    widened ``except`` clause in an example silently no-ops the moment the owner
    adapts it.

    A ``LiveViewingError`` already carries a stable code, so it is forwarded as
    a sub-code. Anything else has no classification of its own and must not
    invent one from its message — an arbitrary exception's text is exactly the
    surface ADR-0047's locator-confinement decision keeps closed — so it
    collapses to one stable code and its detail is dropped.

    "Dropped" is meant literally, which takes more than ``raise ... from None``.
    That sets ``__suppress_context__``, which only stops the default traceback
    printer; the original exception stays reachable on ``__context__``, and an
    ``OSError`` there still carries the offending path in ``.filename``, which
    any debugger or reporting tool walking the chain can surface. Locator
    confinement is the whole point of this wrapping, so the chain is cleared
    rather than merely hidden.
    """

    if isinstance(failure, PresentationSessionError):
        return failure
    if isinstance(failure, LiveViewingError):
        classified = PresentationSessionError(
            "presentation-viewing-refused", reason_codes=(failure.reason.value,)
        )
    else:
        classified = PresentationSessionError("presentation-viewing-failed")
    classified.__context__ = None
    classified.__cause__ = None
    classified.__suppress_context__ = True
    return classified


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
        # Same guarantee as the launch path: teardown is a step the owner is
        # told to confirm, and "teardown did not complete" is a legal statement
        # only if a failure to complete arrives as this code rather than as
        # whatever the browser or socket layer happened to raise.
        try:
            self._browser.close()
        except Exception:
            teardown_failed = True
        try:
            self._server.close()
        except Exception:
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

    url = server.url
    viewing: LiveViewingSession | None = None
    try:
        viewing = (vehicle or LiveViewingVehicle()).launch(
            capability,
            chrome_executable=chrome_executable,
            launch_timeout_seconds=launch_timeout_seconds,
            initial_url=url,
        )
    except Exception as failure:
        _release_quietly(viewing, server)
        # Deliberately raised *after* this handler exits, not inside it. A
        # ``raise ... from None`` here would re-attach the original exception
        # to ``__context__`` no matter what the wrapper cleared, and an
        # ``OSError`` there still carries the offending path in ``.filename``.
        classified = _classified_viewing_failure(failure)
    except BaseException:
        # An interrupt is the owner's own act, not a session refusal, so it
        # travels as itself. It must still not leave a headed browser
        # displaying the real return, a session directory holding that
        # render's profile and disk cache, or a loopback socket still serving
        # the model. ``launch`` tears down its own partial state; this covers
        # the window between a successful launch and the return below.
        _release_quietly(viewing, server)
        raise
    else:
        classified = None
    if classified is not None:
        raise classified
    return LivePresentationSession(_outcome=outcome, url=url, _browser=viewing, _server=server)


__all__ = [
    "LivePresentationSession",
    "PresentationSessionError",
    "open_presentation_session",
]
