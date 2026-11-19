"""Keep the browser launcher lifecycle regressions in the pytest gate."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.skipif(shutil.which("node") is None, reason="Node is unavailable")
def test_chrome_launch_lifecycle() -> None:
    root = Path(__file__).resolve().parents[1]
    # These controls exercise the standalone launcher; gate controls run separately.
    env = os.environ.copy()
    env.pop("DEMO_CHROME_STARTUP_DIR", None)
    result = subprocess.run(
        ["node", "--test", "tools/presentation_harness/tests/chrome-lifecycle.test.mjs",
         "tools/presentation_harness/tests/chrome-observation.test.mjs"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=30, env=env,
    )
    assert result.returncode == 0, (
        f"Node lifecycle tests failed (exit {result.returncode})\n"
        f"stdout (last 16000 characters):\n{result.stdout[-16000:]}\n"
        f"stderr (last 4000 characters):\n{result.stderr[-4000:]}"
    )


@pytest.mark.skipif(shutil.which("node") is None, reason="Node is unavailable")
def test_chrome_process_group_cleanup() -> None:
    """A helper that outlives Chrome's main process is ended and cannot hang the observer."""
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env.pop("DEMO_CHROME_STARTUP_DIR", None)
    result = subprocess.run(
        ["node", "--test", "tools/presentation_harness/tests/chrome-group-cleanup.test.mjs"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=120, env=env,
    )
    assert result.returncode == 0, (
        f"Node process-group tests failed (exit {result.returncode})\n"
        f"stdout (last 16000 characters):\n{result.stdout[-16000:]}\n"
        f"stderr (last 4000 characters):\n{result.stderr[-4000:]}"
    )
