"""Synthetic contract tests for the ADR-0047 Track 2 viewing vehicle."""

from __future__ import annotations

import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from typing import Any

from packages.derivation.live_viewing import (
    LiveViewingError,
    LiveViewingVehicle,
    PreflightProbes,
    ProbeState,
    ViewingReason,
    run_viewing_preflight,
    validate_loopback_navigation,
)
from packages.derivation.live_workspace import WorkspaceCapability


class _SyntheticProcess:
    next_pid = 7000

    def __init__(self, args: list[str], **_kwargs: Any) -> None:
        self.args = args
        self.pid = self.next_pid
        type(self).next_pid += 1
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


def _capability(root: Path) -> WorkspaceCapability:
    return WorkspaceCapability(root)


class PreflightTests(unittest.TestCase):
    def test_always_decidable_preconditions_are_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw:
            root = Path(raw)
            for field, reason in (
                ("backup_inclusion", ViewingReason.BACKUP_INDETERMINATE),
                ("content_indexing", ViewingReason.INDEX_INDETERMINATE),
            ):
                probes = PreflightProbes(backup_inclusion=False, content_indexing=False)
                probes = replace(probes, **{field: ProbeState.UNKNOWN})
                verdict = run_viewing_preflight(_capability(root), probes)
                self.assertFalse(verdict.allowed)
                self.assertIn(reason.value, verdict.reason_codes)

    def test_unreadable_observer_is_a_refusal(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw:
            root = Path(raw)

            def unreadable() -> object:
                raise OSError("synthetic probe unavailable")

            verdict = run_viewing_preflight(
                _capability(root),
                PreflightProbes(backup_inclusion=unreadable, content_indexing=False),
            )
            self.assertFalse(verdict.allowed)
            self.assertEqual(verdict.reason_codes, (ViewingReason.BACKUP_INDETERMINATE.value,))

    def test_present_preconditions_refuse_without_locator(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw:
            root = Path(raw)
            verdict = run_viewing_preflight(
                _capability(root),
                PreflightProbes(backup_inclusion=True, content_indexing=True),
            )
            self.assertFalse(verdict.allowed)
            self.assertEqual(
                verdict.reason_codes,
                (ViewingReason.BACKUP_PRESENT.value, ViewingReason.INDEX_PRESENT.value),
            )
            self.assertNotIn(str(root), repr(verdict))

    def test_clipboard_result_is_partial_and_detectable_presence_refuses(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw:
            root = Path(raw)
            unknown = run_viewing_preflight(
                _capability(root),
                PreflightProbes(False, False, ProbeState.UNKNOWN),
            )
            self.assertTrue(unknown.allowed)
            self.assertEqual(
                unknown.owner_responsibilities,
                (ViewingReason.CLIPBOARD_HISTORY_UNDETECTABLE.value,),
            )
            detected = run_viewing_preflight(
                _capability(root),
                PreflightProbes(False, False, True),
            )
            self.assertFalse(detected.allowed)
            self.assertEqual(detected.reason_codes, (ViewingReason.CLIPBOARD_HISTORY_PRESENT.value,))

    def test_confirmed_absent_clipboard_is_still_not_a_clearance(self) -> None:
        # A scan that finds no known clipboard manager rules out only the
        # managers it knows to look for.  ADR-0047 forbids reading that as a
        # completeness claim, so the owner-responsibility code must survive the
        # confirmed-absent case exactly as it survives an undecidable one.
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw:
            absent = run_viewing_preflight(
                _capability(Path(raw)),
                PreflightProbes(False, False, False),
            )
            self.assertTrue(absent.allowed)
            self.assertEqual(
                absent.owner_responsibilities,
                (ViewingReason.CLIPBOARD_HISTORY_UNDETECTABLE.value,),
            )

    def test_missing_capability_refuses(self) -> None:
        verdict = run_viewing_preflight(None, PreflightProbes(False, False, False))
        self.assertFalse(verdict.allowed)
        self.assertEqual(verdict.reason_codes, (ViewingReason.CAPABILITY_UNAVAILABLE.value,))


class VehicleTests(unittest.TestCase):
    def _browser(self, root: Path) -> Path:
        browser = root / "demo-browser"
        browser.write_text("#!/bin/sh\n", encoding="utf-8")
        browser.chmod(browser.stat().st_mode | os.X_OK)
        return browser

    def test_launch_refuses_a_missing_capability_and_spawns_nothing(self) -> None:
        def factory(args: list[str], **kwargs: Any) -> _SyntheticProcess:
            raise AssertionError("no process may be spawned without a capability")

        vehicle = LiveViewingVehicle(process_factory=factory)
        with self.assertRaises(LiveViewingError) as caught:
            vehicle.launch(None, chrome_executable="/nonexistent", launch_timeout_seconds=0.2)
        self.assertEqual(caught.exception.args, (ViewingReason.CAPABILITY_UNAVAILABLE.value,))

    def test_destinations_are_inside_capability_and_browser_is_headed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw:
            root = Path(raw)
            browser = self._browser(root)
            factory_calls: list[_SyntheticProcess] = []

            def factory(args: list[str], **kwargs: Any) -> _SyntheticProcess:
                del kwargs
                process = _SyntheticProcess(args)
                factory_calls.append(process)
                return process

            vehicle = LiveViewingVehicle(process_factory=factory)
            session = vehicle.launch(_capability(root), chrome_executable=browser, launch_timeout_seconds=0.2)
            try:
                self.assertEqual(len(factory_calls), 1)
                args = factory_calls[0].args
                self.assertNotIn("--headless=new", args)
                for prefix in (
                    "--user-data-dir=",
                    "--disk-cache-dir=",
                    "--download-default-directory=",
                    "--print-to-pdf=",
                ):
                    path = Path(next(value for value in args if value.startswith(prefix)).split("=", 1)[1])
                    self.assertIn(root.resolve(), path.resolve().parents)
                self.assertIsNone(factory_calls[0].poll())
            finally:
                session.close()
            self.assertIsNotNone(factory_calls[0].poll())
            self.assertFalse((root / ".live-view").exists())

    def test_symlink_escape_refuses_without_diagnostic_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw, tempfile.TemporaryDirectory(prefix="demo-outside-") as outside_raw:
            root = Path(raw)
            outside = Path(outside_raw)
            (root / ".live-view").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(LiveViewingError) as raised:
                LiveViewingVehicle().launch(_capability(root), chrome_executable=outside / "missing")
            self.assertEqual(raised.exception.reason, ViewingReason.PATH_NOT_CONFINED)
            self.assertNotIn(str(outside), str(raised.exception))

    def test_navigation_refuses_non_loopback_without_claiming_more(self) -> None:
        with self.assertRaises(LiveViewingError) as raised:
            validate_loopback_navigation("https://demo.invalid/view")
        self.assertEqual(raised.exception.reason, ViewingReason.NON_LOOPBACK_NAVIGATION)
        validate_loopback_navigation("http://127.0.0.1:8080/demo")
        validate_loopback_navigation("http://localhost:8080/demo")

    def test_launch_failure_tears_down_owned_session(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-viewing-") as raw:
            root = Path(raw)
            browser = self._browser(root)

            class FailingProcess(_SyntheticProcess):
                def __init__(self, args: list[str], **kwargs: Any) -> None:
                    super().__init__(args, **kwargs)
                    (Path(next(value for value in args if value.startswith("--user-data-dir=")).split("=", 1)[1]) / "DevToolsActivePort").unlink()
                    self._running = False

            with self.assertRaises(LiveViewingError) as raised:
                LiveViewingVehicle(process_factory=FailingProcess).launch(
                    _capability(root), chrome_executable=browser, launch_timeout_seconds=0.05
                )
            self.assertEqual(raised.exception.reason, ViewingReason.BROWSER_EXITED_DURING_LAUNCH)
            self.assertFalse((root / ".live-view").exists())


if __name__ == "__main__":
    unittest.main()
