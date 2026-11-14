"""Focused, non-browser checks for bounded sale-page failure diagnostics."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
from types import SimpleNamespace
from typing import Any, cast

import pytest

from tools import sale_page_observation


ROOT = Path(__file__).resolve().parents[1]


def test_explicit_core_selection_restores_v79_after_v80() -> None:
    probe = SimpleNamespace()

    sale_page_observation._select_core_surface(probe, "v80")
    assert probe.PACKAGE_VERSION == "v80"
    assert probe.REGISTRY == "published-packages.v78.json"

    sale_page_observation._select_core_surface(probe, "v79")
    assert probe.PACKAGE_VERSION == "v79"
    assert probe.PACKAGE == "package.core-calculations.v79.json"
    assert probe.REGISTRY == "published-packages.v77.json"
    assert probe.RELEASE_VERSION == "v77"

    selected = sale_page_observation._select_core_surface(probe, "v89")
    assert selected == {
        "package": "package.core-calculations.v89.json",
        "package_version": "v89",
        "registry": "published-packages.v87.json",
        "release": "demo.release.sli-worksheet-integration.2025.v87.json",
        "release_version": "v87",
    }
    assert probe.PACKAGE_VERSION == "v89"
    assert probe.REGISTRY == "published-packages.v87.json"
    assert probe.RELEASE_VERSION == "v87"


@pytest.mark.parametrize("source_case", ["covered_flag_yes", "covered_flag_corrected_to_no"])
def test_v89_covered_sale_carry_rekeys_companions_without_changing_values(
    source_case: str,
) -> None:
    from copy import deepcopy

    from tests.test_noncovered_sales_v79 import world

    world_factory = getattr(world, "__wrapped__", None)
    assert callable(world_factory)
    source = cast(list[dict[str, Any]], world_factory().cases[source_case])
    original = deepcopy(source)
    adapted = sale_page_observation._prepare_v89_covered_sale_companions(source)
    expected_identity = (
        "broker=demo.ns.corr.broker,statement=demo.ns.corr.statement,"
        "transaction=demo.ns.corr.transaction,tax-year=2025"
    )

    def fact_rows(acts: list[dict[str, object]]) -> dict[str, object]:
        rows: dict[str, object] = {}
        for act in acts:
            payload = act.get("payload")
            if not isinstance(payload, dict):
                continue
            finding = payload.get("finding")
            if isinstance(finding, dict) and isinstance(finding.get("fact_id"), str):
                rows[finding["fact_id"]] = finding.get("value")
            member = payload.get("member")
            if isinstance(member, dict):
                member_finding = member.get("finding")
                if isinstance(member_finding, dict) and isinstance(member_finding.get("fact_id"), str):
                    rows[member_finding["fact_id"]] = member_finding.get("value")
        return rows

    original_rows = fact_rows(original)
    adapted_rows = fact_rows(adapted)
    child_types = (
        "tax.us.2025.f1099b.covered-lt-txn.proceeds",
        "tax.us.2025.f1099b.covered-lt-txn.basis",
    )
    closure_types = (
        "tax.us.2025.f1099b.covered-lt.source-closure",
        "tax.us.2025.f1099b.covered-lt-proceeds.source-closure",
        "tax.us.2025.f1099b.covered-lt-basis.source-closure",
    )

    assert source == original
    assert sorted(original_rows.values(), key=repr) == sorted(adapted_rows.values(), key=repr)
    for fact_type in child_types:
        assert f"{fact_type}|{expected_identity}" in adapted_rows
    assert {
        fact_id for fact_id in original_rows
        if any(fact_id.startswith(f"{fact_type}|") for fact_type in closure_types)
    } == {
        fact_id for fact_id in adapted_rows
        if any(fact_id.startswith(f"{fact_type}|") for fact_type in closure_types)
    }
    assert f"{closure_types[0]}|family-horizon=demo.ns.corr.h1,tax-year=2025" in adapted_rows
    assert f"{closure_types[1]}|family-horizon=demo.ns.corrp.h1,tax-year=2025" in adapted_rows
    assert f"{closure_types[2]}|family-horizon=demo.ns.corrb.h1,tax-year=2025" in adapted_rows
    assert adapted_rows[f"{child_types[0]}|{expected_identity}"] == 6000.0
    assert adapted_rows[f"{child_types[1]}|{expected_identity}"] == 2000.0


def test_owned_chrome_tmpdir_ignores_long_inherited_tmpdir_and_cleans_up(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    inherited_tmpdir = tmp_path / ("long-temp-component-" * 8)
    inherited_tmpdir.mkdir()
    monkeypatch.setenv("TMPDIR", str(inherited_tmpdir))
    profile_root = sale_page_observation._new_owned_chrome_tempdir()

    try:
        assert not profile_root.is_relative_to(inherited_tmpdir)
        assert profile_root.name.startswith("spo-")
        socket_path = profile_root / "presentation-harness-profile-XXXXXX" / "SingletonSocket"
        if os.name == "posix":
            assert len(os.fsencode(socket_path)) < 108
    finally:
        shutil.rmtree(profile_root, ignore_errors=False)

    assert not profile_root.exists()


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

        def communicate(self, timeout: float) -> tuple[bytes, bytes]:
            timeouts.append(timeout)
            if len(timeouts) < 3:
                raise subprocess.TimeoutExpired("node", timeout, output=b"private stdout", stderr=b"private stderr")
            return b"private stdout", b"private stderr"

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


def test_bounded_process_timeout_preserves_safe_node_failure_record(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    record = json.dumps(
        {
            "error": True,
            "reason": "browser-cleanup-failed",
            "category": "cleanup",
            "stage": "cleanup",
        },
        separators=(",", ":"),
    ) + "\n"
    record_bytes = record.encode("utf-8")
    assert len(record_bytes) == 88
    timeouts: list[float] = []
    signals: list[int] = []

    class Child:
        pid = 12345
        returncode = -signal.SIGKILL

        def communicate(self, timeout: float) -> tuple[bytes, bytes]:
            timeouts.append(timeout)
            if len(timeouts) < 3:
                raise subprocess.TimeoutExpired(
                    "node", timeout, output=b"", stderr=record_bytes
                )
            return b"", record_bytes

    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: Child())
    monkeypatch.setattr(
        os,
        "killpg",
        lambda pid, requested_signal: signals.append(requested_signal),
    )

    with pytest.raises(sale_page_observation._BoundedBrowserFailure) as caught:
        sale_page_observation._run_bounded_subprocess(
            ["node"], cwd=tmp_path, env={}, timeout_seconds=0.1
        )

    assert timeouts == [0.1, 5, 5]
    assert signals == [signal.SIGTERM, signal.SIGKILL]
    assert caught.value.reason == "browser-observation-timeout"
    assert caught.value.stderr_bytes == 88
    assert caught.value.node_failure == {
        "reason": "browser-cleanup-failed",
        "category": "cleanup",
        "stage": "cleanup",
    }
    assert record.rstrip() not in str(caught.value)

    message = sale_page_observation._format_browser_failure(
        reason=caught.value.reason,
        category="timeout",
        stage="python-subprocess",
        node_exit_code=None,
        stdout_bytes=caught.value.stdout_bytes,
        stderr_bytes=caught.value.stderr_bytes,
        launch=None,
        node_failure=caught.value.node_failure,
        node_progress=caught.value.node_progress,
    )
    assert "stage=python-subprocess" in message
    assert "node_failure_reason=browser-cleanup-failed" in message
    assert "node_failure_category=cleanup" in message
    assert "node_failure_stage=cleanup" in message


def test_progress_projection_keeps_last_safe_record_only() -> None:
    rows = [
        {"kind": "progress", "stage": "cdp-connect-ready", "elapsed_ms": 17, "case_index": 0},
        {"kind": "progress", "stage": "dom-read-complete", "elapsed_ms": 845, "case_index": 4},
        {"kind": "progress", "stage": "private-stage", "elapsed_ms": 900, "case_index": 4},
        {"kind": "progress", "stage": "cleanup-complete", "elapsed_ms": True, "case_index": 0},
    ]
    stdout = b"\xff\n" + b"".join(
        (json.dumps(row, separators=(",", ":")) + "\n").encode("utf-8") for row in rows
    )

    assert sale_page_observation._safe_progress_record_if_present(stdout) == {
        "stage": "dom-read-complete",
        "elapsed_ms": 845,
        "case_index": 4,
    }
    assert sale_page_observation._safe_progress_record_if_present(
        json.dumps({"kind": "progress", "stage": "dom-read-complete", "elapsed_ms": 1, "case_index": 1, "path": "SECRET"})
    ) is None


def test_real_timed_child_invalid_utf8_preserves_byte_counts_and_safe_records(tmp_path: Path) -> None:
    failure = json.dumps(
        {
            "error": True,
            "reason": "browser-cleanup-failed",
            "category": "cleanup",
            "stage": "cleanup",
        },
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    assert len(failure) == 88
    progress = json.dumps(
        {"kind": "progress", "stage": "cdp-connect-start", "elapsed_ms": 12, "case_index": 0},
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    stdout = b"\xff\n" + progress
    stderr = b"\xff\n" + failure
    child_script = (
        "import os, signal, sys, time\n"
        f"os.write(1, {stdout!r})\n"
        f"os.write(2, {stderr!r})\n"
        "signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))\n"
        "while True: time.sleep(0.05)\n"
    )

    with pytest.raises(sale_page_observation._BoundedBrowserFailure) as caught:
        sale_page_observation._run_bounded_subprocess(
            [sys.executable, "-c", child_script], cwd=tmp_path, env=os.environ.copy(), timeout_seconds=1
        )

    assert caught.value.reason == "browser-observation-timeout"
    assert caught.value.stdout_bytes == len(stdout)
    assert caught.value.stderr_bytes == len(stderr)
    assert caught.value.node_failure == {
        "reason": "browser-cleanup-failed",
        "category": "cleanup",
        "stage": "cleanup",
    }
    assert caught.value.node_progress == {
        "stage": "cdp-connect-start",
        "elapsed_ms": 12,
        "case_index": 0,
    }
    assert "UnicodeDecodeError" not in str(caught.value)


def test_successful_binary_subprocess_output_is_preserved(tmp_path: Path) -> None:
    run = sale_page_observation._run_bounded_subprocess(
        [sys.executable, "-c", "import os; os.write(1, b'valid\\xffoutput')"],
        cwd=tmp_path,
        env=os.environ.copy(),
        timeout_seconds=5,
    )

    assert run.returncode == 0
    assert run.stdout.encode("utf-8", errors="surrogateescape") == b"valid\xffoutput"
    assert run.stderr == ""


def test_timeout_parsing_waits_for_term_and_kill_and_skips_deep_json(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    record = json.dumps(
        {"error": True, "reason": "browser-cleanup-failed", "category": "cleanup", "stage": "cleanup"},
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    deep_line = b"{" + b"\"x\":[" * 100 + b"0" + b"]" * 100 + b"}\n"
    signals: list[int] = []
    parser_calls: list[int] = []
    original_parser = sale_page_observation._safe_failure_record_if_present

    class Child:
        pid = 12345
        returncode = -signal.SIGKILL

        def __init__(self) -> None:
            self.calls = 0

        def communicate(self, timeout: float) -> tuple[bytes, bytes]:
            self.calls += 1
            if self.calls < 3:
                raise subprocess.TimeoutExpired("node", timeout, output=b"", stderr=deep_line + record)
            return b"", deep_line + record

    def observe_parser(
        stderr: str | bytes | None,
    ) -> sale_page_observation._SafeFailureRecord | None:
        parser_calls.append(len(signals))
        assert signals == [signal.SIGTERM, signal.SIGKILL]
        return original_parser(stderr)

    child = Child()
    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: child)
    monkeypatch.setattr(os, "killpg", lambda pid, requested_signal: signals.append(requested_signal))
    monkeypatch.setattr(sale_page_observation, "_safe_failure_record_if_present", observe_parser)

    with pytest.raises(sale_page_observation._BoundedBrowserFailure) as caught:
        sale_page_observation._run_bounded_subprocess(
            ["node"], cwd=tmp_path, env={}, timeout_seconds=0.1
        )

    assert signals == [signal.SIGTERM, signal.SIGKILL]
    assert parser_calls == [2]
    assert caught.value.node_failure == {
        "reason": "browser-cleanup-failed",
        "category": "cleanup",
        "stage": "cleanup",
    }
