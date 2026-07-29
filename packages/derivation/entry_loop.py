"""Synthetic W-2 entry loop over the existing contribution and live-run paths.

The browser owns no fact-writing authority.  It submits an ``act.v1`` whose
kind is ``contribution``; this module admits that event with its ordinary
successor carriers, appends only acts to the workspace log, and recomputes the
return through ``live_coordinate_run``.

This first product slice is intentionally narrow: one committed synthetic
fixture, one W-2 Box 1 fact, and loopback serving.  Nothing here accepts a
caller-supplied workspace locator through HTTP or exposes one in a response.
"""

from __future__ import annotations

import json
import mimetypes
import shutil
import subprocess
from contextlib import AbstractContextManager
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from hmac import compare_digest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from secrets import token_urlsafe
from threading import Lock, Thread
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import (
    WorkspaceCapability,
    bootstrap_workspace,
)
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface, Refusal
from packages.derivation.surface_resolver import (
    ResolvedSurface,
    resolve_surface_artifact,
)
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project


ENTRY_FIXTURE = Path("packages/sample_data/entry_loop_t1")
SEED_LOG = ENTRY_FIXTURE / "workspace" / "acts.jsonl"
SURFACE_CONTENT = ENTRY_FIXTURE / "surface" / "content" / "app"
SURFACE_MANIFESTS = ENTRY_FIXTURE / "surface" / "manifest"
SURFACE_REGISTRY = (
    ENTRY_FIXTURE / "surface" / "registry" / "published-surface-artifacts.json"
)
SURFACE_RELEASES = ENTRY_FIXTURE / "surface" / "publication_surface" / "releases"
SURFACE_ADOPTION = (
    ENTRY_FIXTURE / "surface" / "adoptions" / "adopt-entry-loop-v1.json"
)

SCOPE_USER = "demo.user.filer-1"
RUN_SCOPE = {"jurisdiction": "us", "year": "2055"}
W2_FAMILY = {"id": "tax.us.2025.w2", "version": "v2"}
W2_SCOPE = {"tax-year": "2025", "subject": "demo.primary"}
W2_PREDECESSOR = "demo.presentation-l2.w2.h0"
W2_SUCCESSOR = "demo.entry-loop.w2.h1"
W2_EVIDENCE_ID = "demo.presentation-l2.evidence.w2"
W2_FACT_ID = (
    "tax.us.2025.w2.box1-wages|"
    "employer=demo.presentation-l2.employer,"
    "w2-slip=demo.presentation-l2.w2,tax-year=2025"
)
W2_CLOSURE_FACT_ID = (
    "tax.us.2025.w2.source-closure|"
    f"family-horizon={W2_SUCCESSOR},tax-year=2025"
)

EXPECTED_IMPACT_LINES = ("1a", "9", "11", "15", "16")
COMPARISON_LINES = ("2b", "3a", "3b", "12")
EVALUATION_LINES = EXPECTED_IMPACT_LINES + COMPARISON_LINES

_MAX_REQUEST_BYTES = 16_384
_LINE_TITLES = {
    "1a": "Wages, salaries, tips",
    "2b": "Taxable interest",
    "3a": "Qualified dividends",
    "3b": "Ordinary dividends",
    "9": "Total income",
    "11": "Adjusted gross income",
    "12": "Standard deduction",
    "15": "Taxable income",
    "16": "Tax",
}


class EntryLoopError(RuntimeError):
    """A locator-free refusal suitable for the synthetic entry surface."""


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text("utf-8"))
    if not isinstance(value, dict):
        raise EntryLoopError("entry-loop-fixture-invalid")
    return value


def load_seed_acts(repo_root: Path) -> list[dict[str, Any]]:
    """Read and validate the committed, newline-terminated seed act log."""

    path = repo_root / SEED_LOG
    try:
        raw = path.read_bytes()
    except OSError:
        raise EntryLoopError("entry-loop-fixture-unavailable") from None
    if not raw.endswith(b"\n"):
        raise EntryLoopError("entry-loop-fixture-invalid")
    acts: list[dict[str, Any]] = []
    try:
        for line in raw.splitlines():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError
            acts.append(value)
    except (json.JSONDecodeError, UnicodeError, ValueError):
        raise EntryLoopError("entry-loop-fixture-invalid") from None
    return acts


def _surface_publication(repo_root: Path) -> PublicationSurface:
    root = repo_root / ENTRY_FIXTURE / "surface"
    return PublicationSurface(
        release_dir=root / "publication_surface" / "releases",
        package_registry_path=root / "registry" / "published-surface-artifacts.json",
        member_dir=root / "manifest",
    )


def resolve_entry_surface(repo_root: Path) -> ResolvedSurface:
    """Resolve the entry program through the ADR-0049 surface artifact route."""

    adoption = _load_json(repo_root / SURFACE_ADOPTION)
    resolved = resolve_surface_artifact(
        [adoption],
        run_scope={"jurisdiction": "us", "year": "2025"},
        scope_user=SCOPE_USER,
        workspace_revision=1,
        surface=_surface_publication(repo_root),
        content_dir=repo_root / SURFACE_CONTENT,
    )
    if isinstance(resolved, Refusal):
        raise EntryLoopError(f"entry-surface-refused:{resolved.reason}")
    return resolved


def build_entry_surface(
    capability: WorkspaceCapability,
    *,
    repo_root: Path,
    timeout_seconds: float = 60.0,
) -> Path:
    """Verify, copy, and build the adopted surface inside the workspace."""

    workspace = bootstrap_workspace(capability, repo_root=repo_root)
    resolved = resolve_entry_surface(repo_root)
    build_root = workspace.live_output_path(
        Path(".entry-surface") / resolved.manifest["id"]
    )
    if build_root.exists():
        raise EntryLoopError("entry-surface-build-target-exists")
    shutil.copytree(resolved.content_dir, build_root)
    command = str(resolved.manifest["build_command"]).split()
    try:
        result = subprocess.run(
            command,
            cwd=build_root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        raise EntryLoopError("entry-surface-build-failed") from None
    if result.returncode != 0:
        raise EntryLoopError("entry-surface-build-failed")
    entrypoint = build_root / str(resolved.manifest["entrypoint_html"])
    if not entrypoint.is_file():
        raise EntryLoopError("entry-surface-build-failed")
    return entrypoint.parent


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _derived_id(prefix: str, value: Any) -> str:
    return f"{prefix}{sha256(_canonical_bytes(value)).hexdigest()[:24]}"


def _line_values(model: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    sections = model.get("sections")
    if not isinstance(sections, list):
        raise EntryLoopError("entry-state-unavailable")
    for section in sections:
        if not isinstance(section, dict):
            continue
        field = section.get("field")
        resolved = section.get("resolved")
        if not isinstance(field, dict) or not isinstance(resolved, dict):
            continue
        line = str(field.get("line", ""))
        if line not in EVALUATION_LINES:
            continue
        disposition = str(resolved.get("disposition", ""))
        if disposition in {
            "published_value",
            "computed_zero",
            "closure_backed_zero",
        }:
            values[line] = {
                "line": line,
                "title": _LINE_TITLES[line],
                "computed": True,
                "value": resolved.get("value"),
            }
        else:
            values[line] = {
                "line": line,
                "title": _LINE_TITLES[line],
                "computed": False,
                "value": None,
            }
    if set(values) != set(EVALUATION_LINES):
        raise EntryLoopError("entry-state-unavailable")
    return values


def _parse_box1(value: object) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise EntryLoopError("entry-value-invalid")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise EntryLoopError("entry-value-invalid") from None
    exponent = amount.as_tuple().exponent
    if (
        not amount.is_finite()
        or amount <= 0
        or not isinstance(exponent, int)
        or exponent < -2
    ):
        raise EntryLoopError("entry-value-invalid")
    if amount > Decimal("999999999.99"):
        raise EntryLoopError("entry-value-invalid")
    return int(amount) if amount == amount.to_integral_value() else float(amount)


@dataclass(frozen=True)
class EntrySnapshot:
    revision: int
    payload: dict[str, Any]


class SyntheticW2EntryRuntime:
    """One synthetic workspace, serialized contribution admission, live recompute."""

    def __init__(
        self,
        capability: WorkspaceCapability,
        *,
        repo_root: Path,
        seed_acts: Sequence[Mapping[str, Any]] | None = None,
    ) -> None:
        self._capability = capability
        self._repo_root = repo_root
        self._schemas = DerivationSchemas()
        self._lock = Lock()
        self._workspace = bootstrap_workspace(capability, repo_root=repo_root)
        self._log = ActLog(self._workspace.location, self._schemas.registry)
        self._surface = PublicationSurface(
            repo_root / "packages" / "sample_data" / "frrs_t3" / "publication_surface" / "releases",
            repo_root / "packages" / "content" / "tax" / "2025" / "published-packages.json",
            repo_root / "packages" / "content" / "tax" / "2025",
        )
        self._previous_lines: dict[str, dict[str, Any]] | None = None
        self._last_accepted = False
        self._last_action = ""
        self._seed(seed_acts or load_seed_acts(repo_root))
        self._snapshot = self._compute_snapshot()

    def _seed(self, seed_acts: Sequence[Mapping[str, Any]]) -> None:
        if self._log.read().revision:
            raise EntryLoopError("entry-workspace-not-empty")
        for expected, act in enumerate(seed_acts):
            body = dict(act)
            if body.get("committed_against") != expected:
                raise EntryLoopError("entry-loop-fixture-invalid")
            self._log.append(body, expected_revision=expected)

    def _current_w2(self, acts: Sequence[Mapping[str, Any]]) -> dict[str, Any] | None:
        state = project(tuple(dict(act) for act in acts), self._schemas.registry)
        currency = compute_currency(state)
        matches = [
            state.findings[finding_id]
            for finding_id in sorted(currency.current_finding_ids)
            if finding_id in state.findings
            and state.findings[finding_id].get("fact_id") == W2_FACT_ID
        ]
        if len(matches) > 1:
            raise EntryLoopError("entry-state-unavailable")
        return matches[0] if matches else None

    def _contribution_template(self, revision: int) -> dict[str, Any]:
        nonce = token_urlsafe(18)
        contribution_id = f"demo.entry-loop.contribution.{nonce}"
        payload = {
            "contribution": {
                "schema": "contribution.v1",
                "id": contribution_id,
                "evidence_id": W2_EVIDENCE_ID,
                "content": {
                    "mode": "manual-entry",
                    "synthetic": True,
                },
            }
        }
        return {
            "schema": "act.v1",
            "act_id": f"demo.entry-loop.act.contribution.{nonce}",
            "kind": "contribution",
            "actor": SCOPE_USER,
            "at": "2026-07-29T00:00:00Z",
            "committed_against": revision,
            "payload": payload,
        }

    def _compute_snapshot(self) -> EntrySnapshot:
        contents = self._log.read()
        revision = contents.revision
        output_name = f"entry-state-{revision}.json"
        outcome = live_coordinate_run(
            self._capability,
            repo_root=self._repo_root,
            authoritative_acts=contents.acts,
            workspace_revision=revision,
            run_scope=RUN_SCOPE,
            scope_user=SCOPE_USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo.entry-loop.run.{revision}",
            governance_pins=[],
            surface=self._surface,
            output_name=output_name,
            schemas=self._schemas,
        )
        if outcome.refusal is not None or outcome.output_path is None:
            reason = outcome.refusal.reason if outcome.refusal is not None else "unknown"
            raise EntryLoopError(f"entry-run-refused:{reason}")
        if outcome.presentation_path is None:
            raise EntryLoopError("entry-state-unavailable")
        try:
            report = json.loads(outcome.output_path.read_text("utf-8"))
            model = json.loads(outcome.presentation_path.read_text("utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            raise EntryLoopError("entry-state-unavailable") from None

        lines_by_id = _line_values(model)
        current = self._current_w2(contents.acts)
        missing = current is None
        blocked = [
            row
            for row in report.get("dispositions", [])
            if isinstance(row, dict) and row.get("disposition") == "blocked"
        ]
        fully_computed = not missing and not blocked and all(
            line["computed"] for line in lines_by_id.values()
        )
        lines: list[dict[str, Any]] = []
        for line_id in EVALUATION_LINES:
            line = dict(lines_by_id[line_id])
            line["group"] = (
                "expected-impact"
                if line_id in EXPECTED_IMPACT_LINES
                else "untouched-comparison"
            )
            before = (
                self._previous_lines.get(line_id)
                if self._previous_lines is not None
                else None
            )
            if before is None:
                line["change"] = "blocked" if not line["computed"] else "baseline"
            elif (
                before["computed"] == line["computed"]
                and before["value"] == line["value"]
            ):
                line["change"] = "unchanged"
            else:
                line["change"] = "changed"
            lines.append(line)

        payload = {
            "revision": revision,
            "missing": (
                [
                    {
                        "id": "w2-box1",
                        "label": "W-2 from Demo Workshop — Box 1 wages",
                        "document": "Form W-2",
                        "box": "Box 1",
                        "target": "w2-box1",
                    }
                ]
                if missing
                else []
            ),
            "answered": (
                []
                if current is None
                else [
                    {
                        "id": "w2-box1",
                        "label": "W-2 Box 1",
                        "value": current["value"],
                        "target": "w2-box1",
                    }
                ]
            ),
            "lines": lines,
            "accepted": self._last_accepted,
            "last_action": self._last_action,
            "complete": fully_computed,
            "computed": fully_computed,
            "contribution": self._contribution_template(revision),
        }
        self._previous_lines = lines_by_id
        return EntrySnapshot(revision=revision, payload=payload)

    def snapshot(self) -> EntrySnapshot:
        with self._lock:
            return self._snapshot

    @staticmethod
    def _validate_template(
        submitted: Mapping[str, Any],
        expected: Mapping[str, Any],
    ) -> None:
        if set(submitted) != set(expected):
            raise EntryLoopError("entry-event-invalid")
        for key in ("schema", "act_id", "kind", "actor", "at", "committed_against"):
            if submitted.get(key) != expected.get(key):
                raise EntryLoopError("entry-event-invalid")
        submitted_payload = submitted.get("payload")
        expected_payload = expected.get("payload")
        if not isinstance(submitted_payload, dict) or not isinstance(expected_payload, dict):
            raise EntryLoopError("entry-event-invalid")
        submitted_contribution = submitted_payload.get("contribution")
        expected_contribution = expected_payload.get("contribution")
        if not isinstance(submitted_contribution, dict) or not isinstance(
            expected_contribution, dict
        ):
            raise EntryLoopError("entry-event-invalid")
        for key in ("schema", "id", "evidence_id"):
            if submitted_contribution.get(key) != expected_contribution.get(key):
                raise EntryLoopError("entry-event-invalid")
        content = submitted_contribution.get("content")
        if not isinstance(content, dict) or set(content) != {
            "mode",
            "synthetic",
            "w2_box1",
        }:
            raise EntryLoopError("entry-event-invalid")
        if content.get("mode") != "manual-entry" or content.get("synthetic") is not True:
            raise EntryLoopError("entry-event-invalid")

    def contribute(self, submitted: Mapping[str, Any]) -> EntrySnapshot:
        """Admit one browser-originated contribution and recompute the return."""

        with self._lock:
            expected = self._snapshot.payload["contribution"]
            if not isinstance(expected, dict):
                raise EntryLoopError("entry-state-unavailable")
            self._validate_template(submitted, expected)
            contribution_act = json.loads(json.dumps(submitted))
            contribution = contribution_act["payload"]["contribution"]
            amount = _parse_box1(contribution["content"]["w2_box1"])
            contribution["content"]["w2_box1"] = amount

            contents = self._log.read()
            if contribution_act["committed_against"] != contents.revision:
                raise EntryLoopError("entry-event-stale")
            current = self._current_w2(contents.acts)
            contribution_id = contribution["id"]
            finding_body = {
                "schema": "finding.v2",
                "id": _derived_id(
                    "demo.entry-loop.finding.",
                    {"contribution": contribution_id, "value": amount},
                ),
                "fact_id": W2_FACT_ID,
                "value": amount,
                "basis": "documentary",
                "evidence_ids": [W2_EVIDENCE_ID],
                "contribution_id": contribution_id,
            }
            successor_index = contents.revision + 1
            successor_base = {
                "schema": "act.v1",
                "actor": SCOPE_USER,
                "at": "2026-07-29T00:00:01Z",
                "committed_against": successor_index,
            }
            successor_acts: list[dict[str, Any]] = []
            if current is None:
                payload = {
                    "family": dict(W2_FAMILY),
                    "scope": dict(W2_SCOPE),
                    "member": {"action": "assert", "finding": finding_body},
                    "successor": {
                        "id": W2_SUCCESSOR,
                        "predecessor": W2_PREDECESSOR,
                    },
                }
                successor_acts.append(
                    {
                        **successor_base,
                        "act_id": _derived_id(
                            "demo.entry-loop.act.member.", payload
                        ),
                        "kind": "member-transition",
                        "payload": payload,
                    }
                )
                closure_finding = {
                    "schema": "finding.v2",
                    "id": _derived_id(
                        "demo.entry-loop.closure.",
                        {"contribution": contribution_id, "horizon": W2_SUCCESSOR},
                    ),
                    "fact_id": W2_CLOSURE_FACT_ID,
                    "value": True,
                    "basis": "documentary",
                    "evidence_ids": [W2_EVIDENCE_ID],
                    "contribution_id": contribution_id,
                }
                closure_payload = {"finding": closure_finding}
                successor_acts.append(
                    {
                        **successor_base,
                        "act_id": _derived_id(
                            "demo.entry-loop.act.closure.", closure_payload
                        ),
                        "kind": "assertion",
                        "at": "2026-07-29T00:00:02Z",
                        "committed_against": successor_index + 1,
                        "payload": closure_payload,
                    }
                )
                action = "entered"
            else:
                payload = {"finding": finding_body}
                successor_acts.append(
                    {
                        **successor_base,
                        "act_id": _derived_id(
                            "demo.entry-loop.act.correction.", payload
                        ),
                        "kind": "assertion",
                        "payload": payload,
                    }
                )
                action = "corrected"

            state = project(tuple(contents.acts), self._schemas.registry)
            try:
                admitted = apply_contribution_batch(
                    state,
                    contribution_act=contribution_act,
                    successor_acts=successor_acts,
                    registry=self._schemas.registry,
                    record_id=_derived_id(
                        "demo.entry-loop.record.", contribution_id
                    ),
                    workspace_revision=contents.revision,
                )
            except (ContributionError, KeyError, TypeError):
                raise EntryLoopError("entry-event-rejected") from None
            if admitted.terminal_record["phase"] != "completed":
                raise EntryLoopError("entry-event-rejected")

            revision = self._log.append(
                contribution_act, expected_revision=contents.revision
            )
            for act in successor_acts:
                revision = self._log.append(act, expected_revision=revision)

            self._last_accepted = True
            self._last_action = action
            self._snapshot = self._compute_snapshot()
            return self._snapshot


class _EntryHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(
        self,
        runtime: SyntheticW2EntryRuntime,
        static_root: Path,
        route: str,
    ) -> None:
        self.runtime = runtime
        self.static_root = static_root.resolve(strict=True)
        self.route = route.rstrip("/")
        super().__init__(("127.0.0.1", 0), _EntryRequestHandler)


class _EntryRequestHandler(BaseHTTPRequestHandler):
    server: _EntryHTTPServer

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def _json(self, status: int, body: Mapping[str, Any]) -> None:
        encoded = _canonical_bytes(body)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def _target(self) -> tuple[str, str] | None:
        try:
            parsed = urlsplit(self.path)
        except ValueError:
            return None
        if parsed.query or parsed.fragment:
            return None
        prefix = f"{self.server.route}/"
        if not parsed.path.startswith(prefix):
            return None
        return parsed.path, parsed.path[len(prefix) :]

    def _serve_static(self, relative: str) -> None:
        relative = relative or "index.html"
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            self.send_error(404)
            return
        candidate = (self.server.static_root / Path(*pure.parts)).resolve(
            strict=False
        )
        try:
            candidate.relative_to(self.server.static_root)
        except ValueError:
            self.send_error(404)
            return
        if not candidate.is_file():
            self.send_error(404)
            return
        try:
            body = candidate.read_bytes()
        except OSError:
            self.send_error(404)
            return
        mime = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; connect-src 'self'; "
            "img-src 'self' data:; object-src 'none'; base-uri 'none'",
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        target = self._target()
        if target is None:
            self.send_error(404)
            return
        _, relative = target
        if compare_digest(relative, "api/state"):
            self._json(200, self.server.runtime.snapshot().payload)
            return
        self._serve_static(relative)

    def do_POST(self) -> None:  # noqa: N802
        target = self._target()
        if target is None or not compare_digest(target[1], "api/contributions"):
            self.send_error(404)
            return
        if self.headers.get_content_type() != "application/json":
            self._json(415, {"error": "Contribution request must be JSON."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        if size <= 0 or size > _MAX_REQUEST_BYTES:
            self._json(400, {"error": "Contribution request is invalid."})
            return
        try:
            submitted = json.loads(self.rfile.read(size))
            if not isinstance(submitted, dict):
                raise ValueError
            snapshot = self.server.runtime.contribute(submitted)
        except EntryLoopError as exc:
            if str(exc) == "entry-value-invalid":
                message = (
                    "Enter W-2 Box 1 as a positive dollar amount with no more "
                    "than two decimal places."
                )
            elif str(exc) == "entry-event-stale":
                message = "The entry session changed. Reload the current entry."
            else:
                message = "The contribution was not accepted. No entry was changed."
            self._json(422, {"error": message})
            return
        except (json.JSONDecodeError, UnicodeError, ValueError):
            self._json(400, {"error": "Contribution request is invalid."})
            return
        self._json(200, snapshot.payload)

    def do_HEAD(self) -> None:  # noqa: N802
        self.send_error(405)


class EntryLoopServer(AbstractContextManager["EntryLoopServer"]):
    """Owned loopback server for one synthetic entry runtime."""

    def __init__(
        self,
        runtime: SyntheticW2EntryRuntime,
        static_root: Path,
    ) -> None:
        route = f"/entry/{token_urlsafe(32)}"
        self._http = _EntryHTTPServer(runtime, static_root, route)
        self._thread = Thread(
            target=self._http.serve_forever,
            name="synthetic-entry-loopback",
            daemon=True,
        )
        self._thread.start()
        self.url = (
            f"http://127.0.0.1:{self._http.server_address[1]}"
            f"{route}/index.html"
        )
        self._closed = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._http.shutdown()
        finally:
            self._http.server_close()
        self._thread.join(timeout=3)
        if self._thread.is_alive():
            raise EntryLoopError("entry-server-teardown-failed")

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()


__all__ = [
    "COMPARISON_LINES",
    "ENTRY_FIXTURE",
    "EVALUATION_LINES",
    "EXPECTED_IMPACT_LINES",
    "EntryLoopError",
    "EntryLoopServer",
    "EntrySnapshot",
    "SyntheticW2EntryRuntime",
    "build_entry_surface",
    "load_seed_acts",
    "resolve_entry_surface",
]
