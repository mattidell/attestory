"""Focused, non-browser checks for bounded sale-page failure diagnostics."""
from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import subprocess

import pytest

from tools import sale_page_observation


ROOT = Path(__file__).resolve().parents[1]


def test_node_observer_emits_safe_manifest_stage_without_starting_chrome() -> None:
    result = subprocess.run(
        [
            "node",
            "tools/presentation_harness/sale-page-observation.mjs",
            "temp/sale-page-observation/diagnostic-test-missing/cases.json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    assert result.returncode == 2
    assert result.stdout == ""
    payload = json.loads(result.stderr)
    assert payload == {
        "error": True,
        "reason": "case-manifest-unavailable",
        "category": "manifest",
        "stage": "case-manifest",
    }
    formatted = sale_page_observation._format_browser_failure(
        **sale_page_observation._safe_failure_record(result.stderr),
        node_exit_code=result.returncode,
        stdout_bytes=sale_page_observation._captured_byte_count(result.stdout),
        stderr_bytes=sale_page_observation._captured_byte_count(result.stderr),
        launch=None,
    )
    assert "stage=case-manifest" in formatted
    assert "category=manifest" in formatted


def test_failure_projection_keeps_stage_and_launch_evidence_but_not_raw_output(tmp_path: Path) -> None:
    trace_path = tmp_path / "observer.jsonl"
    trace_path.write_text(
        json.dumps(
            {
                "label": "other",
                "outcome": "exit_before_ready",
                "queue_ms": 17,
                "elapsed_ms": 2403,
                "readiness_ms": None,
                "stderr_bytes": 120,
                "exit_kind": "exited",
                "exit_code": 1,
                "exit_signal": None,
                "spawn_code": None,
                "stderr_categories": ["pthread-create-resource-unavailable", "PATH_SENTINEL"],
                "environment": {"SECRET": "do-not-include"},
                "dom": "do-not-include",
                "report_path": "PATH_SENTINEL/report.json",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    run = subprocess.CompletedProcess(
        ["node"],
        2,
        "stdout URL_SENTINEL",
        "unstructured PATH_SENTINEL raw stderr\n"
        + json.dumps(
            {
                "error": True,
                "reason": "target-attach-timeout",
                "category": "timeout",
                "stage": "page-observation",
            }
        ),
    )

    failure = sale_page_observation._safe_failure_record(run.stderr)
    message = sale_page_observation._format_browser_failure(
        **failure,
        node_exit_code=run.returncode,
        stdout_bytes=sale_page_observation._captured_byte_count(run.stdout),
        stderr_bytes=sale_page_observation._captured_byte_count(run.stderr),
        launch=sale_page_observation._safe_launch_record(trace_path),
    )

    assert "reason=target-attach-timeout" in message
    assert "category=timeout" in message
    assert "stage=page-observation" in message
    assert "outcome:exit_before_ready" in message
    assert "queue_ms:17" in message
    assert "stderr_categories:['pthread-create-resource-unavailable']" in message
    for private_fragment in (
        "URL_SENTINEL", "PATH_SENTINEL", "SECRET", "do-not-include", "raw stderr",
    ):
        assert private_fragment not in message

    assert sale_page_observation._safe_failure_record(
        json.dumps(
            {
                "error": True,
                "reason": "anything PATH_SENTINEL",
                "category": "unknown-category",
                "stage": "unsafe-stage",
            }
        )
    ) == {
        "reason": "browser-observation-failed",
        "category": "unclassified",
        "stage": "unknown",
    }


def test_invalid_utf8_launch_trace_does_not_mask_primary_failure(tmp_path: Path) -> None:
    trace_path = tmp_path / "invalid-trace.jsonl"
    trace_path.write_bytes(b"\xff\n")
    child_error = json.dumps(
        {
            "error": True,
            "reason": "target-attach-timeout",
            "category": "timeout",
            "stage": "page-observation",
        }
    )

    message = sale_page_observation._format_browser_failure(
        **sale_page_observation._safe_failure_record(child_error),
        node_exit_code=2,
        stdout_bytes=0,
        stderr_bytes=len(child_error),
        launch=sale_page_observation._safe_launch_record(trace_path),
    )

    assert "reason=target-attach-timeout" in message
    assert "category=timeout" in message
    assert "stage=page-observation" in message
    assert "chrome_launch=unavailable" in message
    assert "UnicodeDecodeError" not in message


def test_bounded_process_timeout_uses_term_then_kill_without_retaining_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    timeouts: list[float] = []
    signals: list[int] = []

    class Child:
        pid = 12345
        returncode = -signal.SIGKILL

        def communicate(self, timeout: float) -> tuple[str, str]:
            timeouts.append(timeout)
            if len(timeouts) < 3:
                raise subprocess.TimeoutExpired("node", timeout, output=b"private stdout", stderr=b"private stderr")
            return "private stdout", "private stderr"

    child = Child()
    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: child)
    monkeypatch.setattr(
        os,
        "killpg",
        lambda pid, requested_signal: signals.append(requested_signal),
    )

    with pytest.raises(sale_page_observation._BoundedBrowserFailure) as caught:
        sale_page_observation._run_bounded_subprocess(
            ["node"], cwd=tmp_path, env={}, timeout_seconds=240
        )

    assert timeouts == [240, 5, 5]
    assert signals == [signal.SIGTERM, signal.SIGKILL]
    assert caught.value.reason == "browser-observation-timeout"
    assert caught.value.stdout_bytes == len("private stdout")
    assert caught.value.stderr_bytes == len("private stderr")
    assert "private stdout" not in str(caught.value)
    assert "private stderr" not in str(caught.value)
