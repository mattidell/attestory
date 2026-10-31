"""Integrated correction-browser resource controls."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import pytest

from tests.helpers import correction_browser_owner as owner
import tests.test_sli_correction_session as correction


@pytest.mark.skipif(not (correction._BROWSER and correction._NODE), reason="needs Node and a local Chrome/Chromium")
def test_two_real_correction_scenarios_share_one_browser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    owner.close()
    trace = tmp_path / "launches.jsonl"
    monkeypatch.setenv("DEMO_CHROME_TRACE", str(trace))
    try:
        started = time.monotonic()
        correction.BrowserIntegration("test_choose_confirm_calculated_shows_before_and_after_explanation").test_choose_confirm_calculated_shows_before_and_after_explanation()
        first = time.monotonic()
        correction.BrowserIntegration("test_indistinguishable_choice_is_refused_with_nothing_saved").test_indistinguishable_choice_is_refused_with_nothing_saved()
        second = time.monotonic()
        records = [json.loads(line) for line in trace.read_text().splitlines()]
        assert len(records) == 1
        assert records[0]["outcome"] == "ready_accepted"
        print(f"demo browser launches=1 startup_ms={records[0]['readiness_ms']} first_ms={round((first-started)*1000)} second_ms={round((second-first)*1000)}")
    finally:
        owner.close()


def test_python_and_node_share_startup_slot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import os
    import select
    import subprocess
    from tests.helpers.chrome_startup_slot import browser_startup_slot

    node = correction._NODE
    if not node:
        pytest.skip("Node is unavailable")
    monkeypatch.setenv("DEMO_CHROME_STARTUP_DIR", str(tmp_path))
    module = (Path(__file__).resolve().parents[1] / "tools/presentation_harness/lib/startup-coordinator.mjs").as_uri()
    script = f"import {{acquireStartupSlot}} from {json.dumps(module)}; const s=await acquireStartupSlot(process.env.DEMO_CHROME_STARTUP_DIR); process.stdout.write('ready\\n'); await new Promise(r=>setTimeout(r,500)); await s.release();"
    with browser_startup_slot():
        proc = subprocess.Popen([node, "--input-type=module", "-e", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=os.environ.copy())
        assert proc.stdout is not None
        assert not select.select([proc.stdout], [], [], 0.3)[0]
    try:
        assert select.select([proc.stdout], [], [], 10)[0]
        assert proc.stdout.readline().strip() == "ready"
        with pytest.raises(RuntimeError, match="queue timed out"):
            with browser_startup_slot(timeout=0.15):
                pytest.fail("live Node owner was stolen")
        assert proc.wait(timeout=10) == 0
        with browser_startup_slot(timeout=1):
            pass
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        if proc.stdout is not None:
            proc.stdout.close()
        if proc.stderr is not None:
            proc.stderr.close()


def test_node_browser_resource_controls() -> None:
    import subprocess

    if not correction._NODE:
        pytest.skip("Node is unavailable")
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [correction._NODE, "--test",
         "tools/presentation_harness/tests/startup-coordinator.test.mjs",
         "tools/presentation_harness/tests/shared-browser-context.test.mjs",
         "tools/presentation_harness/tests/correction-owner.test.mjs"],
        cwd=root, capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, f"browser resource controls failed\n{result.stdout[-16000:]}\n{result.stderr[-4000:]}"


@pytest.mark.skipif(not correction._NODE, reason="needs Node")
def test_hard_owner_death_reaps_browser_and_profile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import os
    import signal
    import time

    owner.close()
    trace = tmp_path / "hard-owner.jsonl"
    fake = tmp_path / "demo-chrome"
    fake.write_text("#!/usr/bin/env node\nimport {writeFileSync} from 'node:fs';\nconst p=process.argv.find(x=>x.startsWith('--user-data-dir=')).slice(16);\nwriteFileSync(p+'/DevToolsActivePort','12345\\n/demo');\nsetInterval(()=>{},1000);\n")
    fake.chmod(0o755)
    monkeypatch.setenv("PRESENTATION_HARNESS_CHROME", str(fake))
    monkeypatch.setenv("DEMO_CHROME_TRACE", str(trace))
    try:
        owner.acquire()
        process, pid, profile_root = owner._owner, owner._browser_pid, owner._profile_root
        assert process is not None and pid is not None and profile_root is not None
        os.kill(process.pid, signal.SIGKILL)
        process.wait(timeout=10)
        owner.close()
        for _ in range(100):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.02)
        else:
            pytest.fail("browser survived hard owner cleanup")
        assert not Path(profile_root).exists()
        owner.acquire()  # Explicit later acquisition creates a fresh generation.
        assert len(trace.read_text().splitlines()) == 2
    finally:
        owner.close()


@pytest.mark.parametrize("known", [True, False])
def test_owner_failure_preserves_safe_structured_evidence(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, known: bool) -> None:
    if not correction._NODE:
        pytest.skip("needs Node")
    owner.close()
    fake = tmp_path / "demo-failing-chrome"
    text = ("cannot allocate memory " if known else "unrecognized startup text ") + "demo-private-value /demo/private-path https://demo.invalid"
    fake.write_text(f"#!/usr/bin/env node\nprocess.stderr.write({json.dumps(text)}); process.exit(9);\n")
    fake.chmod(0o755)
    monkeypatch.setenv("PRESENTATION_HARNESS_CHROME", str(fake))
    monkeypatch.delenv("DEMO_CHROME_TRACE", raising=False)
    try:
        with pytest.raises(RuntimeError) as captured:
            owner.acquire()
        message = str(captured.value)
        assert message.startswith("correction browser owner startup failed: ")
        details = json.loads(message.split(": ", 1)[1])
        assert details["reason"] == "chrome-launch-failed"
        assert details["outcome"] == "exit_before_ready"
        assert details["exit_kind"] == "exited" and details["exit_code"] == 9
        assert details["stderr_bytes"] > 0
        assert details["categories"] == (["cannot-allocate-memory"] if known else [])
        assert "demo-private-value" not in message and "private-path" not in message and "demo.invalid" not in message
        assert owner._owner is None and owner._profile_root is None
    finally:
        owner.close()


def test_unknown_owner_protocol_values_are_normalized() -> None:
    details = json.loads(owner._owner_failure({"reason": "demo-private", "observation": {
        "outcome": "https://demo.invalid", "exit_kind": "demo-private", "exit_code": -9,
        "stderr_bytes": "demo-private", "categories": ["demo-private", "cannot-allocate-memory"],
    }}).split(": ", 1)[1])
    assert details["reason"] == details["outcome"] == details["exit_kind"] == "unknown"
    assert details["exit_code"] is None and details["stderr_bytes"] is None
    assert details["categories"] == ["cannot-allocate-memory"]
    assert "demo-private" not in json.dumps(details) and "demo.invalid" not in json.dumps(details)


def test_owner_without_trace_fails_at_injected_allowance(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    if not correction._NODE:
        pytest.skip("needs Node")
    owner.close()
    fake = tmp_path / "demo-never-ready"
    fake.write_text("#!/usr/bin/env node\nsetInterval(()=>{},1000);\n")
    fake.chmod(0o755)
    monkeypatch.setenv("PRESENTATION_HARNESS_CHROME", str(fake))
    monkeypatch.setenv("DEMO_CHROME_STARTUP_DIR", str(tmp_path))
    monkeypatch.delenv("DEMO_CHROME_TRACE", raising=False)
    monkeypatch.setenv("DEMO_CHROME_LAUNCH_TIMEOUT_MS", "2000")
    started = time.monotonic()
    try:
        with pytest.raises(RuntimeError) as captured:
            owner.acquire()
        elapsed = time.monotonic() - started
        details = json.loads(str(captured.value).split(": ", 1)[1])
        assert details["outcome"] == "not_ready_after_grace"
        assert 1.5 <= elapsed < 20
        assert owner._owner is None and owner._profile_root is None
    finally:
        owner.close()


def test_owner_wait_covers_worst_case_startup() -> None:
    assert owner.LAUNCH_ALLOWANCE_S == 45
    assert owner.OWNER_STARTUP_WAIT_S > (
        owner.SLOT_QUEUE_TIMEOUT_S + owner.LAUNCH_ALLOWANCE_S + owner.OBSERVER_GRACE_S)


def _js_const(path: str, name: str) -> int:
    text = (Path(__file__).resolve().parents[1] / path).read_text()
    match = re.search(rf"export const {name} = (\d+);", text)
    assert match, name
    return int(match.group(1))


def test_python_and_js_timing_constants_agree() -> None:
    harness = "tools/presentation_harness/lib/"
    assert _js_const(harness + "chrome.mjs", "CHROME_LAUNCH_TIMEOUT_MS") == owner.LAUNCH_ALLOWANCE_S * 1000
    assert _js_const(harness + "chrome.mjs", "SLOT_QUEUE_TIMEOUT_MS") == owner.SLOT_QUEUE_TIMEOUT_S * 1000
    assert _js_const(harness + "chrome-observation.mjs", "OBSERVER_GRACE_MS") == owner.OBSERVER_GRACE_S * 1000
