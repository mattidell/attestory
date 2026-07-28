"""Synthetic Track 2 tests for the one-act live presentation session."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen
from typing import Any

from packages.derivation.live_session import PresentationSessionError, open_presentation_session
from packages.derivation.live_viewing import LiveViewingVehicle, PreflightProbes
from packages.derivation.live_workspace import WorkspaceCapability
from tools import generate_presentation_l2_golden as golden


REPO = Path(__file__).resolve().parent.parent


class _SyntheticProcess:
    def __init__(self, args: list[str], **_kwargs: Any) -> None:
        self.args = args
        profile_arg = next(value for value in args if value.startswith("--user-data-dir="))
        profile = Path(profile_arg.split("=", 1)[1])
        (profile / "DevToolsActivePort").write_text("9222\n/devtools/browser/demo\n", encoding="utf-8")
        self._running = True

    def poll(self) -> int | None:
        return None if self._running else 0

    def terminate(self) -> None:
        self._running = False

    def kill(self) -> None:
        self._running = False

    def wait(self, timeout: float | None = None) -> int:
        del timeout
        self._running = False
        return 0


def _browser(root: Path) -> Path:
    browser = root / "demo-browser"
    browser.write_text("#!/bin/sh\n", encoding="utf-8")
    browser.chmod(browser.stat().st_mode | os.X_OK)
    return browser


def _open(root: Path, *, probes: PreflightProbes, vehicle: Any) -> Any:
    (root / "L").mkdir()
    return open_presentation_session(
        WorkspaceCapability(root / "L"),
        probes=probes,
        repo_root=REPO,
        authoritative_acts=golden.canonical_acts(),
        workspace_revision=len(golden.canonical_acts()),
        run_scope=golden.SCOPE,
        scope_user=golden.USER,
        request={"schema": "run-request.v1"},
        run_id="demo.presentation-live-session",
        governance_pins=[],
        surface=golden._surface(),
        output_name="demo.presentation-live-session.json",
        chrome_executable=_browser(root),
        launch_timeout_seconds=0.2,
        vehicle=vehicle,
    )


class SessionTests(unittest.TestCase):
    def test_preflight_refusal_happens_before_derivation_or_browser(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            calls: list[object] = []

            class NoLaunchVehicle:
                def launch(self, *_args: object, **_kwargs: object) -> Any:
                    calls.append("launch")
                    raise AssertionError("preflight refusal must happen before browser launch")

            with self.assertRaises(PresentationSessionError) as caught:
                _open(root, probes=PreflightProbes(), vehicle=NoLaunchVehicle())
            self.assertEqual(caught.exception.reason, "presentation-preflight-refused")
            self.assertIn("viewing-residency-backup-indeterminate", caught.exception.reason_codes)
            self.assertEqual(calls, [])

    def test_page_is_repository_content_and_model_is_workspace_content(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            vehicle = LiveViewingVehicle(process_factory=_SyntheticProcess)
            with _open(root, probes=PreflightProbes(False, False, False), vehicle=vehicle) as session:
                with urlopen(session.url, timeout=2) as response:
                    body = response.read().decode("utf-8")
                self.assertIn("Form 1040 — Citation Walk", body)
                self.assertIn('"schema":"presentation-model.v1"', body)
                self.assertIn('"runId":"demo.presentation-live-session"', body)
                self.assertTrue(session.url.startswith("http://127.0.0.1:"))
                self.assertNotIn(str(root), body)
                self.assertNotIn(str(root), repr(session))
                model_path = root / "L" / "outputs" / "demo.presentation-live-session.presentation.json"
                model = json.loads(model_path.read_text(encoding="utf-8"))
                self.assertIn("presentation-model.v1", model["schema"])
                self.assertIn(root.resolve(), model_path.resolve().parents)
                try:
                    urlopen(f"{session.url}not-allowed", timeout=2)
                except HTTPError as missing:
                    with missing:
                        self.assertEqual(missing.code, 404)
                else:
                    self.fail("unexpected route returned successfully")
            self.assertFalse((root / "L" / ".live-view").exists())

    def test_browser_launch_failure_closes_server_and_workspace_session(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)

            class FailingProcess(_SyntheticProcess):
                def __init__(self, args: list[str], **kwargs: Any) -> None:
                    super().__init__(args, **kwargs)
                    profile_arg = next(value for value in args if value.startswith("--user-data-dir="))
                    (Path(profile_arg.split("=", 1)[1]) / "DevToolsActivePort").unlink()
                    self._running = False

            with self.assertRaises(Exception):
                _open(root, probes=PreflightProbes(False, False, False), vehicle=LiveViewingVehicle(process_factory=FailingProcess))
            self.assertFalse((root / "L" / ".live-view").exists())


if __name__ == "__main__":
    unittest.main()
