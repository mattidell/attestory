"""Real Chrome proof that sale-page profiles use a short owned temp root."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any

import pytest

from tests.helpers.sale_page_observation import collect
from tools import sale_page_observation


@pytest.mark.live
def test_real_v80_chrome_launch_ignores_long_inherited_tmpdir_and_cleans_owned_root(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    inherited_tmpdir = tmp_path / ("long-temp-component-" * 8)
    inherited_tmpdir.mkdir()
    monkeypatch.setenv("TMPDIR", str(inherited_tmpdir))
    monkeypatch.setattr(tempfile, "tempdir", None)
    assert Path(tempfile.gettempdir()) == inherited_tmpdir
    assert len(os.fsencode(inherited_tmpdir)) > 107

    observed: dict[str, Any] = {}
    run_bounded_subprocess = sale_page_observation._run_bounded_subprocess

    def capture_owned_tempdir(
        command: list[str], *, cwd: Path, env: dict[str, str], timeout_seconds: float
    ) -> subprocess.CompletedProcess[str]:
        chrome_tempdir = Path(env["TMPDIR"])
        observed["chrome_tempdir"] = chrome_tempdir
        observed["outside_inherited"] = not chrome_tempdir.is_relative_to(inherited_tmpdir)
        observed["socket_path_bytes"] = len(
            os.fsencode(chrome_tempdir / "presentation-harness-profile-XXXXXX" / "SingletonSocket")
        )
        observed["exists_during_launch"] = chrome_tempdir.is_dir()
        return run_bounded_subprocess(command, cwd=cwd, env=env, timeout_seconds=timeout_seconds)

    monkeypatch.setattr(sale_page_observation, "_run_bounded_subprocess", capture_owned_tempdir)
    result = collect(core_version="v80", case_id="covered-long-term-sale")

    chrome_tempdir = observed["chrome_tempdir"]
    assert isinstance(chrome_tempdir, Path)
    assert observed["outside_inherited"] is True
    assert observed["exists_during_launch"] is True
    if os.name == "posix":
        assert observed["socket_path_bytes"] < 108
    assert not chrome_tempdir.exists()
    assert result["browser"]["browser_version"].startswith("Chrome/")
    assert result["browser"]["cleanup_completed"] is True
    assert len(result["cases"]) == 1
    case = result["cases"][0]
    assert case["spec"]["id"] == "covered-long-term-sale"
    assert case["metadata"]["selected_adoption"] == {
        "package": "core-calculations@v80",
        "registry": "published-packages.v78.json",
        "release": "demo.release.sli-worksheet-integration.2025@v78",
        "coordinator_saved_page": True,
    }
    assert case["dom"]["context_cleanup"] == {
        "target_closed": True,
        "browser_context_disposed": True,
    }
