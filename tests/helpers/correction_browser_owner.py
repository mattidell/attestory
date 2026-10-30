"""Lazy browser owner scoped to a pytest worker; endpoints stay in process memory."""
from __future__ import annotations

import json
import os
import shutil
import signal
import tempfile
import select
import subprocess
from pathlib import Path
from typing import Any

_owner: subprocess.Popen[str] | None = None
_endpoint: str | None = None
_profile_root: str | None = None
_browser_pid: int | None = None


# This is a closed diagnostic vocabulary, never arbitrary child output.
_CATEGORIES = frozenset({
    "devtools-active-port-write-error", "devtools-http-server-start-error",
    "pthread-create-resource-unavailable", "thread-start-resource-unavailable",
    "cannot-allocate-memory", "out-of-memory", "too-many-open-files",
    "no-usable-sandbox", "running-as-root-without-no-sandbox",
    "failed-to-move-to-new-namespace", "user-namespace-operation-not-permitted",
    "profile-in-use", "singleton-lock-failed", "devtools-bind-address-in-use",
    "missing-x-server", "crashpad-handler-failed", "zygote-fork-failed",
})
_OUTCOMES = frozenset({"unknown", "resolve_failure", "spawn_failure", "queue_failed",
    "cancelled", "exit_before_ready", "exit_after_deadline", "ready_after_deadline",
    "not_ready_after_grace"})


def _owner_failure(value: Any) -> str:
    def choice(item: Any, allowed: frozenset[str]) -> str:
        return item if isinstance(item, str) and item in allowed else "unknown"

    def count(item: Any, maximum: int) -> int | None:
        return item if type(item) is int and 0 <= item <= maximum else None

    data = value if isinstance(value, dict) else {}
    obs = data.get("observation")
    obs = obs if isinstance(obs, dict) else {}
    raw_categories = obs.get("categories")
    categories = sorted({x for x in raw_categories if isinstance(x, str) and x in _CATEGORIES}) if isinstance(raw_categories, list) else []
    safe = {
        "reason": choice(data.get("reason"), frozenset({"chrome-not-found", "chrome-launch-failed"})),
        "outcome": choice(obs.get("outcome"), _OUTCOMES),
        "exit_kind": choice(obs.get("exit_kind"), frozenset({"alive", "exited", "spawn_error", "resolve_error", "queue_error"})),
        "exit_code": count(obs.get("exit_code"), 255),
        "exit_signal": choice(obs.get("exit_signal"), frozenset({"SIGTERM", "SIGKILL", "SIGABRT", "SIGSEGV", "SIGTRAP", "SIGILL", "SIGBUS"})),
        "spawn_code": choice(obs.get("spawn_code"), frozenset({"ENOENT", "EACCES", "ENOEXEC", "ENOMEM", "EMFILE", "ENFILE", "EAGAIN"})),
        "stderr_bytes": count(obs.get("stderr_bytes"), 10**9),
        "queue_ms": count(obs.get("queue_ms"), 10**9),
        "categories": categories,
    }
    return "correction browser owner startup failed: " + json.dumps(safe, sort_keys=True)


def acquire() -> str:
    global _owner, _endpoint, _profile_root, _browser_pid
    if _owner is not None and _owner.poll() is not None:
        close()
    if _owner is None:
        path = Path(__file__).with_name("correction_browser_owner.mjs")
        _profile_root = tempfile.mkdtemp(prefix="demo-correction-browser-owner-")
        env = os.environ.copy()
        env["TMPDIR"] = _profile_root
        try:
            _owner = subprocess.Popen(["node", str(path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.DEVNULL, text=True, env=env, start_new_session=True)
        except BaseException:
            shutil.rmtree(_profile_root, ignore_errors=True)
            _profile_root = None
            raise
        assert _owner.stdout is not None
        ready, _, _ = select.select([_owner.stdout], [], [], 210)
        if not ready:
            close()
            raise RuntimeError("correction browser owner startup timed out")
        try:
            value: Any = json.loads(_owner.stdout.readline(8193))
            if isinstance(value, dict) and value.get("status") == "error":
                message = _owner_failure(value)
                close()
                raise RuntimeError(message)
            _endpoint = value["wsUrl"]
            _browser_pid = value["pid"]
            if not isinstance(_browser_pid, int) or _browser_pid <= 0:
                raise ValueError("invalid browser pid")
            if not isinstance(_endpoint, str) or not _endpoint.startswith("ws://127.0.0.1:"):
                raise ValueError("invalid endpoint")
        except (ValueError, KeyError, TypeError):
            close()
            raise RuntimeError("correction browser owner startup failed") from None
    assert _endpoint is not None
    return _endpoint


def close() -> None:
    global _owner, _endpoint, _profile_root, _browser_pid
    owner, _owner, _endpoint = _owner, None, None
    profile_root, _profile_root, _browser_pid = _profile_root, None, None
    if owner is None:
        return
    if owner.poll() is None:
        if owner.stdin is not None:
            try:
                owner.stdin.write("close\n")
                owner.stdin.flush()
            except BrokenPipeError:
                pass
        try:
            owner.wait(timeout=10)
        except subprocess.TimeoutExpired:
            owner.terminate()
            try:
                owner.wait(timeout=5)
            except subprocess.TimeoutExpired:
                owner.kill()
                owner.wait()
    if owner.stdin is not None:
        owner.stdin.close()
    if owner.stdout is not None:
        owner.stdout.close()
    # A killed owner cannot run its Node finally block. Its browser is in this
    # private process group and its temporary profiles are under our root.
    if profile_root is not None:
        if os.path.isdir(profile_root) and os.listdir(profile_root):
            try:
                os.killpg(owner.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        shutil.rmtree(profile_root, ignore_errors=False)
