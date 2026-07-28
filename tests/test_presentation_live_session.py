"""Synthetic Track 2 tests for the one-act live presentation session."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from typing import Any

from packages.derivation import live_session, live_viewing
from packages.derivation.live_session import PresentationSessionError, open_presentation_session
from packages.derivation.live_viewing import (
    LiveViewingError,
    LiveViewingVehicle,
    PreflightProbes,
    ViewingReason,
)
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
                # The served page must not tell the owner what it is rendering.
                # Its comment explains why it stays silent; the title and the
                # visible header carry no provenance claim at all.
                for marker in live_session._PROVENANCE_CLAIM_MARKERS:
                    self.assertNotIn(marker, body)
                self.assertIn("<title>Form 1040 — Citation Walk</title>", body)
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

    def test_the_model_is_not_retrievable_without_the_session_route(self) -> None:
        # The served body carries the whole presentation model inline, and every
        # local account can reach 127.0.0.1. An ephemeral port is scannable in
        # well under a second, so the route token is what actually keeps the
        # model from an unrelated local process.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            vehicle = LiveViewingVehicle(process_factory=_SyntheticProcess)
            with _open(root, probes=PreflightProbes(False, False, False), vehicle=vehicle) as session:
                origin = session.url.rsplit("/", 1)[0]
                route = session.url[len(origin) :]
                self.assertGreater(len(route), 32)
                for guess in (f"{origin}/", f"{origin}/index.html", f"{origin}{route}x", f"{origin}{route[:-1]}"):
                    with self.assertRaises(HTTPError, msg=guess) as refused:
                        urlopen(guess, timeout=2)
                    with refused.exception:
                        self.assertEqual(refused.exception.code, 404)

    def test_a_page_declaring_synthetic_provenance_is_refused(self) -> None:
        # Serving the evaluation fixture page would put "synthetic demo-* data
        # only" in the title and header of the screen the owner reads while
        # forming the attestation. The refusal is on the declaration, so
        # re-pointing PAGE_RELATIVE_PATH at the fixture cannot quietly succeed.
        fixture_page = (REPO / "tools/presentation_harness/examples/pages/citation-walk.v1.html").read_text(
            encoding="utf-8"
        )
        self.assertTrue(any(marker in fixture_page for marker in live_session._PROVENANCE_CLAIM_MARKERS))
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            with mock.patch.object(
                live_session,
                "PAGE_RELATIVE_PATH",
                Path("tools/presentation_harness/examples/pages/citation-walk.v1.html"),
            ):
                with self.assertRaises(PresentationSessionError) as caught:
                    _open(
                        root,
                        probes=PreflightProbes(False, False, False),
                        vehicle=LiveViewingVehicle(process_factory=_SyntheticProcess),
                    )
            self.assertEqual(caught.exception.reason, "presentation-page-declares-provenance")

    def test_the_product_page_carries_no_provenance_claim(self) -> None:
        page = (REPO / live_session.PAGE_RELATIVE_PATH).read_text(encoding="utf-8")
        self.assertNotIn("synthetic demo-*", page)
        self.assertNotIn("synthetic <code>demo-*</code>", page)
        self.assertEqual(page.count(live_session._MODEL_ASSIGNMENT), 1)

    def test_closing_the_session_stops_the_listening_socket(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            vehicle = LiveViewingVehicle(process_factory=_SyntheticProcess)
            session = _open(root, probes=PreflightProbes(False, False, False), vehicle=vehicle)
            url = session.url
            with urlopen(url, timeout=2) as response:
                self.assertEqual(response.status, 200)
            session.close()
            with self.assertRaises(URLError):
                urlopen(url, timeout=2)

    def test_browser_launch_failure_closes_server_and_workspace_session(self) -> None:
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)

            class FailingProcess(_SyntheticProcess):
                def __init__(self, args: list[str], **kwargs: Any) -> None:
                    super().__init__(args, **kwargs)
                    profile_arg = next(value for value in args if value.startswith("--user-data-dir="))
                    (Path(profile_arg.split("=", 1)[1]) / "DevToolsActivePort").unlink()
                    self._running = False

            with self.assertRaises(PresentationSessionError) as caught:
                _open(root, probes=PreflightProbes(False, False, False), vehicle=LiveViewingVehicle(process_factory=FailingProcess))
            self.assertEqual(caught.exception.reason, "presentation-viewing-refused")
            self.assertEqual(caught.exception.reason_codes, ("viewing-browser-exited-during-launch",))
            self.assertFalse((root / "L" / ".live-view").exists())

    def test_a_viewing_refusal_reaches_the_caller_classified_not_as_a_traceback(self) -> None:
        # LiveViewingError is a sibling of PresentationSessionError, not a
        # subclass. The owner's failure vocabulary rests on every failure
        # arriving as a stable reason code they may legally report, so a
        # viewing-originated refusal must not escape this function unwrapped.
        for reason in (
            ViewingReason.BROWSER_NOT_FOUND,
            ViewingReason.WORKSPACE_UNREADABLE,
            ViewingReason.PATH_NOT_CONFINED,
            ViewingReason.NON_LOOPBACK_NAVIGATION,
        ):
            with self.subTest(reason=reason):
                with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
                    root = Path(raw)

                    class RefusingVehicle:
                        def launch(self, *_args: object, **_kwargs: object) -> Any:
                            raise LiveViewingError(reason)

                    with self.assertRaises(PresentationSessionError) as caught:
                        _open(root, probes=PreflightProbes(False, False, False), vehicle=RefusingVehicle())
                    self.assertEqual(caught.exception.reason, "presentation-viewing-refused")
                    self.assertEqual(caught.exception.reason_codes, (reason.value,))
                    self.assertNotIn(str(root), str(caught.exception))

    def test_an_unclassified_launch_failure_collapses_to_one_stable_code(self) -> None:
        # An arbitrary exception carries no stable classification, and its
        # message is exactly the surface ADR-0047's locator confinement keeps
        # closed. It must collapse to a fixed code and drop its detail.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            secret = "a-string-standing-in-for-locator-bearing-detail"

            class ExplodingVehicle:
                def launch(self, *_args: object, **_kwargs: object) -> Any:
                    raise ValueError(secret)

            with self.assertRaises(PresentationSessionError) as caught:
                _open(root, probes=PreflightProbes(False, False, False), vehicle=ExplodingVehicle())
            self.assertEqual(caught.exception.reason, "presentation-viewing-failed")
            self.assertEqual(caught.exception.reason_codes, ())
            self.assertNotIn(secret, str(caught.exception))
            self.assertNotIn(str(root), str(caught.exception))

    def test_a_launch_failure_does_not_leave_the_socket_listening(self) -> None:
        # The classified refusal must not come at the cost of the teardown the
        # previous re-raise performed.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            captured: list[str] = []

            class UrlCapturingVehicle:
                def launch(self, *_args: object, **kwargs: object) -> Any:
                    captured.append(str(kwargs["initial_url"]))
                    raise LiveViewingError(ViewingReason.BROWSER_LAUNCH_FAILED)

            with self.assertRaises(PresentationSessionError):
                _open(root, probes=PreflightProbes(False, False, False), vehicle=UrlCapturingVehicle())
            self.assertEqual(len(captured), 1)
            with self.assertRaises(URLError):
                urlopen(captured[0], timeout=2)

    def test_an_interrupt_during_launch_leaves_no_browser_socket_or_session_directory(self) -> None:
        # Ctrl-C stays a KeyboardInterrupt -- relabelling the owner's own act
        # as a session refusal would be a lie inside the failure vocabulary.
        # But it must not leave a headed browser displaying the real return, a
        # session directory holding that render's profile and disk cache, or a
        # socket still serving the model. The preflight refuses on backup and
        # indexing at session *start*; residue that outlives the session
        # outlives that guarantee.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            captured: list[str] = []
            processes: list[Any] = []

            class InterruptedProcess(_SyntheticProcess):
                def __init__(self, args: list[str], **kwargs: Any) -> None:
                    super().__init__(args, **kwargs)
                    processes.append(self)

            class InterruptingVehicle(LiveViewingVehicle):
                def launch(self, *args: Any, **kwargs: Any) -> Any:
                    captured.append(str(kwargs["initial_url"]))
                    original = live_viewing._wait_for_devtools

                    def interrupt(*inner: Any, **inner_kwargs: Any) -> str:
                        original(*inner, **inner_kwargs)
                        raise KeyboardInterrupt

                    with mock.patch.object(live_viewing, "_wait_for_devtools", interrupt):
                        return super().launch(*args, **kwargs)

            with self.assertRaises(KeyboardInterrupt):
                _open(
                    root,
                    probes=PreflightProbes(False, False, False),
                    vehicle=InterruptingVehicle(process_factory=InterruptedProcess),
                )

            self.assertEqual(len(processes), 1)
            self.assertIsNotNone(processes[0].poll())              # browser stopped
            self.assertFalse((root / "L" / ".live-view").exists())  # session dir gone
            with self.assertRaises(URLError):                      # socket released
                urlopen(captured[0], timeout=2)

    def test_an_interrupt_inside_a_with_block_tears_the_session_down(self) -> None:
        # The context-manager form is what the runbook template uses, so that
        # an owner who adapts the template still gets teardown on every exit
        # path without having had to copy a `finally`.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            url = ""
            with self.assertRaises(KeyboardInterrupt):
                with _open(
                    root,
                    probes=PreflightProbes(False, False, False),
                    vehicle=LiveViewingVehicle(process_factory=_SyntheticProcess),
                ) as session:
                    url = session.url
                    with urlopen(url, timeout=2) as response:
                        self.assertEqual(response.status, 200)
                    raise KeyboardInterrupt  # the owner pressing Ctrl-C at the prompt
            self.assertFalse((root / "L" / ".live-view").exists())
            with self.assertRaises(URLError):
                urlopen(url, timeout=2)

    def test_a_classified_failure_retains_no_reference_to_the_original_exception(self) -> None:
        # `raise ... from None` only sets __suppress_context__, which stops the
        # default traceback printer. The original exception stays reachable on
        # __context__, and an OSError there still carries the offending path in
        # .filename -- reachable by any tool that walks the chain. Locator
        # confinement is the point of the wrapping, so the chain is cleared.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)

            class PathBearingVehicle:
                def launch(self, *_args: object, **_kwargs: object) -> Any:
                    raise OSError(2, "No such file", "a-string-standing-in-for-a-locator")

            with self.assertRaises(PresentationSessionError) as caught:
                _open(root, probes=PreflightProbes(False, False, False), vehicle=PathBearingVehicle())
            failure = caught.exception
            self.assertEqual(failure.reason, "presentation-viewing-failed")
            self.assertIsNone(failure.__context__)
            self.assertIsNone(failure.__cause__)
            self.assertTrue(failure.__suppress_context__)

    def test_the_socket_is_released_even_when_shutdown_raises(self) -> None:
        # If shutdown() raises and server_close() is skipped, a socket serving
        # the whole presentation model survives -- and survives silently, since
        # teardown on a failing path is best effort.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            session = _open(
                root,
                probes=PreflightProbes(False, False, False),
                vehicle=LiveViewingVehicle(process_factory=_SyntheticProcess),
            )
            url = session.url
            server = session._server._http

            def explode() -> None:
                raise RuntimeError("shutdown failed")

            with mock.patch.object(server, "shutdown", explode):
                # PresentationSessionError subclasses RuntimeError, so assert
                # the classified teardown code rather than the base class.
                with self.assertRaises(PresentationSessionError) as caught:
                    session.close()
            self.assertEqual(caught.exception.reason, "presentation-session-teardown-failed")
            # OSError rather than URLError, unlike the orderly-teardown cases
            # above. Here shutdown() was made to explode, so the serving thread
            # is still running when server_close() closes the listening socket
            # underneath it, and what a client sees is platform-dependent:
            # ECONNREFUSED wrapped as URLError on macOS, ECONNRESET raised bare
            # on Linux, because urlopen only wraps failures from the request
            # phase and not from reading the response. URLError subclasses
            # OSError, so this still asserts the thing that matters -- no page
            # comes back -- across both.
            with self.assertRaises(OSError):
                urlopen(url, timeout=2)

    def test_teardown_failure_is_reported_as_a_classified_refusal(self) -> None:
        # "Teardown did not complete" is a legal statement in the owner's
        # vocabulary only if an incomplete teardown actually arrives as this
        # code rather than as whatever the browser layer raised.
        with tempfile.TemporaryDirectory(prefix="demo-live-session-") as raw:
            root = Path(raw)
            session = _open(
                root,
                probes=PreflightProbes(False, False, False),
                vehicle=LiveViewingVehicle(process_factory=_SyntheticProcess),
            )

            def explode() -> None:
                raise ValueError("an unclassified teardown failure")

            with mock.patch.object(session._browser, "close", explode):
                with self.assertRaises(PresentationSessionError) as caught:
                    session.close()
            self.assertEqual(caught.exception.reason, "presentation-session-teardown-failed")


if __name__ == "__main__":
    unittest.main()
