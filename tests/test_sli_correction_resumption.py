"""Stop and return for one saved synthetic correction account.

The module is live: it starts the correction runner in another process,
drives it over HTTP, and SIGKILLs that process. The deciding checks read
the act log and the output files. Workspace directories stay outside the
repository and are removed afterwards.
"""

from __future__ import annotations

import json
import os
import queue
import shutil
import signal
import subprocess
import sys
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from packages.derivation.correction_session import (
    LOAN_COST_FACT_TYPE,
    CorrectionRuntime,
    CorrectionSessionError,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession

REPO = Path(__file__).resolve().parent.parent
_RUNNER = [sys.executable, "-m", "packages.derivation.runners.sli_correction_evaluation"]
_WORKER = REPO / "tests" / "helpers" / "sli_resumption_unfinished_worker.py"
_BROWSER_CLIENT = REPO / "tests" / "helpers" / "correction_browser_client.mjs"
_HTTP_SECONDS = 600
_READY_SECONDS = 600
# resume-completed: initial load, opened state, calculate, choice, confirmation,
# calculated outcome, reload, undetermined sentence.
_RESUME_STEPS = 8
_STEP_BUDGET_SECONDS = 600
_BROWSER_MARGIN_SECONDS = 120
_OPENING_RUN_ID = "demo.correction.run.initial"
_UNKNOWN = {
    "outcome": "unknown",
    "reason": "The outcome cannot be determined in this session.",
}
_ENV = {
    "PATH": os.environ.get("PATH", ""),
    "HOME": os.environ.get("HOME", ""),
    "LANG": os.environ.get("LANG", "C"),
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONUNBUFFERED": "1",
}
_NODE = shutil.which("node")
_BROWSER = next(
    (
        str(path)
        for path in (
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/google-chrome-stable"),
            Path("/usr/bin/chromium"),
            Path("/usr/bin/chromium-browser"),
        )
        if path.is_file()
    ),
    None,
)


def _outside_repository() -> TemporaryDirectory[str]:
    directory = TemporaryDirectory(prefix="demo-sli-resumption-")
    location = Path(directory.name).resolve()
    repo = REPO.resolve()
    if location == repo or repo in location.parents or location in repo.parents:
        directory.cleanup()
        raise AssertionError("temporary workspace was created inside the repository")
    return directory


def _tree(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _kill_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        return


class _Child:
    """One runner or worker. The workspace directory is never echoed."""

    def __init__(self, args: list[str], workspace: Path) -> None:
        self.workspace = workspace
        self.process = subprocess.Popen(
            args,
            cwd=str(REPO),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            start_new_session=True,
            env=_ENV,
        )
        self._lines: queue.Queue[str | None] = queue.Queue()
        self._thread = threading.Thread(target=self._read, daemon=True)
        self._thread.start()

    def _read(self) -> None:
        stdout = self.process.stdout
        if stdout is None:
            self._lines.put(None)
            return
        for line in stdout:
            self._lines.put(line)
        self._lines.put(None)

    def _line(self, timeout: float) -> str | None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                line = self._lines.get(timeout=1)
            except queue.Empty:
                if self.process.poll() is not None:
                    return None
                continue
            if line is None:
                return None
            if str(self.workspace) in line:
                raise AssertionError("child output contained the workspace directory")
            return line
        raise AssertionError("child did not become ready")

    def url(self, timeout: float = _READY_SECONDS) -> str:
        while True:
            line = self._line(timeout)
            if line is None:
                raise AssertionError("runner exited before it was ready")
            if line.startswith("URL: "):
                return line.split("URL: ", 1)[1].strip()

    def ready(self, timeout: float = _READY_SECONDS) -> None:
        line = self._line(timeout)
        if line is None or line.startswith("NOT-READY"):
            raise AssertionError("unfinished worker did not save the correction")
        if not line.startswith("READY"):
            raise AssertionError("unfinished worker did not become ready")

    def close(self) -> None:
        if self.process.poll() is None:
            _kill_group(self.process.pid)
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=10)


def _root(url: str) -> str:
    return url.rsplit("/", 1)[0]


def _api(root: str, route: str, body: Mapping[str, Any] | None = None) -> Any:
    url = f"{root}/api/{route}"
    if body is None:
        with urllib.request.urlopen(url, timeout=_HTTP_SECONDS) as response:
            return json.loads(response.read())
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=_HTTP_SECONDS) as response:
        return json.loads(response.read())


def _api_status(root: str, route: str, body: Mapping[str, Any]) -> tuple[int, Any]:
    request = urllib.request.Request(
        f"{root}/api/{route}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=_HTTP_SECONDS) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def _schemas() -> DerivationSchemas:
    schemas = DerivationSchemas()
    install_domain_scoped_supersession(schemas.registry)
    return schemas


def _log_bytes(workspace: Path) -> bytes:
    return (workspace / "acts.jsonl").read_bytes()


def _evidence_predecessor(state: Any, finding: Mapping[str, Any]) -> str | None:
    evidence_ids = finding.get("evidence_ids")
    if not isinstance(evidence_ids, list):
        return None
    found: str | None = None
    for evidence_id in evidence_ids:
        if not isinstance(evidence_id, str):
            return None
        lifecycle = state.evidence.get(evidence_id)
        evidence = getattr(lifecycle, "evidence", None)
        content = evidence.get("content") if isinstance(evidence, Mapping) else None
        if not isinstance(content, Mapping):
            continue
        value = content.get("correction_of_finding_id")
        if not isinstance(value, str) or not value:
            continue
        if found is not None and found != value:
            return None
        found = value
    return found


def _currency_predecessor(state: Any, currency: Any, fact_id: str, current_id: str) -> str | None:
    matches: list[str] = []
    for finding_id, row in state.findings.items():
        if not isinstance(row, Mapping) or row.get("fact_id") != fact_id:
            continue
        if finding_id not in currency.displaced_finding_ids:
            continue
        reasons = currency.reasons.get(finding_id, ())
        if any(
            getattr(reason, "kind", None) == "correction" and getattr(reason, "by", None) == current_id
            for reason in reasons
        ):
            matches.append(str(finding_id))
    if len(matches) != 1:
        return None
    return matches[0]


def _loans(workspace: Path) -> dict[str, dict[str, Any]]:
    """Current loan-cost answers, keyed by the borrowing's label."""
    schemas = _schemas()
    contents = ActLog(workspace, schemas.registry, read_only=True).read()
    state = project(tuple(dict(act) for act in contents.acts), schemas.registry)
    currency = compute_currency(state)
    lattice = facts_of(state.fact_state, include_displaced=True)
    found: dict[str, dict[str, Any]] = {}
    for finding_id in sorted(currency.current_finding_ids):
        finding = state.findings.get(finding_id)
        if not isinstance(finding, Mapping):
            continue
        fact = lattice.get(str(finding.get("fact_id", "")))
        if fact is None or fact.fact_type_id != LOAN_COST_FACT_TYPE:
            continue
        fact_id = str(finding.get("fact_id", ""))
        evidence_predecessor = _evidence_predecessor(state, finding)
        currency_predecessor = _currency_predecessor(state, currency, fact_id, str(finding_id))
        if evidence_predecessor is not None and evidence_predecessor == currency_predecessor:
            predecessor: str | None = evidence_predecessor
        elif evidence_predecessor is None and currency_predecessor is None:
            predecessor = None
        else:
            predecessor = "<not-established>"
        borrowing = dict(fact.keys).get("borrowing")
        label = None
        if isinstance(borrowing, str):
            lifecycle = state.fact_state.entities.get(borrowing)
            if lifecycle is not None:
                value = lifecycle.entity.get("label")
                label = value if isinstance(value, str) else None
        if not isinstance(label, str):
            raise AssertionError("a current loan-cost answer has no label")
        response = finding.get("value")
        found[label] = {
            "finding_id": str(finding_id),
            "value": response if isinstance(response, str) else None,
            "predecessor_id": predecessor,
        }
    return found


def _run_ids(workspace: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    outputs = workspace / "outputs"
    if not outputs.is_dir():
        return found
    for path in sorted(outputs.glob("*.presentation.json")):
        model = json.loads(path.read_text("utf-8"))
        if isinstance(model, dict) and isinstance(model.get("runId"), str):
            found[path.name] = model["runId"]
    return found


def _record_summary(workspace: Path) -> tuple[list[str], bool]:
    schemas = _schemas()
    stream = RecordStream(workspace / "records", schemas)
    recorded = stream.read()
    completed = [
        str(row["run_id"]) for row in recorded.records if row.get("phase") == "completed"
    ]
    return completed, bool(stream.open_runs())


def _choice(choices: Mapping[str, Any], statement_prefix: str) -> dict[str, Any]:
    matches = [
        choice for choice in choices.values()
        if isinstance(choice, dict) and any(
            isinstance(form, dict) and str(form.get("statement", "")).startswith(statement_prefix)
            for form in choice.get("forms") or []
        )
    ]
    if len(matches) != 1:
        raise AssertionError("expected one matching choice")
    return matches[0]


def _opened(answers: list[Any], label: str) -> dict[str, Any]:
    matches = [
        row for row in answers
        if isinstance(row, dict) and row.get("borrowing_label") == label
    ]
    if len(matches) != 1:
        raise AssertionError("expected one opened answer")
    return matches[0]


def _new_acts(before: bytes, after: bytes) -> list[dict[str, Any]]:
    if not after.startswith(before):
        raise AssertionError("earlier acts were not a byte prefix of the log")
    acts: list[dict[str, Any]] = []
    for line in after[len(before):].splitlines():
        if not line:
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise AssertionError("a new log line was not an act")
        acts.append(value)
    return acts


def _assert_same_files(before: dict[str, bytes], root: Path) -> None:
    after = _tree(root)
    for name, payload in before.items():
        if after.get(name) != payload:
            raise AssertionError(f"earlier output changed: {name}")


def _reject_path(payload: object, workspace: Path) -> None:
    if str(workspace) in json.dumps(payload):
        raise AssertionError("a response contained the workspace directory")


class SavedAccountResumption(unittest.TestCase):
    def test_init_on_an_existing_log_and_open_on_a_missing_log_write_nothing(self) -> None:
        held = _outside_repository()
        try:
            workspace = Path(held.name)
            (workspace / "acts.jsonl").write_bytes(b"")
            before = _tree(workspace)
            with self.assertRaises(CorrectionSessionError) as caught:
                CorrectionRuntime.initialize(WorkspaceCapability(workspace), repo_root=REPO)
            self.assertEqual(str(caught.exception), "correction-workspace-not-empty")
            self.assertEqual(_tree(workspace), before)
        finally:
            held.cleanup()

        missing = _outside_repository()
        try:
            workspace = Path(missing.name)
            before = _tree(workspace)
            with self.assertRaises(CorrectionSessionError) as caught:
                CorrectionRuntime.open(WorkspaceCapability(workspace), repo_root=REPO)
            self.assertEqual(str(caught.exception), "correction-workspace-missing")
            self.assertEqual(_tree(workspace), before)

            (workspace / "acts.jsonl").write_bytes(b"")
            before_blank = _tree(workspace)
            with self.assertRaises(CorrectionSessionError) as blank:
                CorrectionRuntime.open(WorkspaceCapability(workspace), repo_root=REPO)
            self.assertEqual(str(blank.exception), "correction-workspace-empty")
            self.assertEqual(_tree(workspace), before_blank)
        finally:
            missing.cleanup()

    def test_completed_correction_survives_process_kill(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            _reject_path(state, workspace)
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            birch = _choice(state["choices"], "2025 Form 1098-E from Birch")
            birch_id = birch["finding_id"]
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            self.assertEqual(chosen["status"], "current")
            self.assertEqual(chosen["confirmation"]["current_answer"], "yes")
            saved = _api(root, "confirm", {"token": chosen["token"], "response": "no"})
            self.assertEqual(saved["outcome"], "saved-and-calculated")
            predecessor = saved["predecessor_finding_id"]
            successor = saved["successor_finding_id"]
            self.assertEqual(predecessor, cedar["finding_id"])
            self.assertNotEqual(successor, predecessor)
            acts_after_save = _log_bytes(workspace)
            outputs_after_save = _tree(workspace / "outputs")
            save_run = f"demo.correction.run.{successor}"
            self.assertEqual(_run_ids(workspace).get(f"{save_run}.presentation.json"), save_run)
        finally:
            starter.close()
            if starter.process.poll() is None:
                self.fail("the first process was still running")

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts_after_save)
            self.assertEqual(_tree(workspace / "outputs"), outputs_after_save)
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            self.assertTrue(opened["opened"])
            self.assertFalse(opened["historical"])
            self.assertFalse(opened["did_not_finish"])
            self.assertTrue(opened["calculate"])
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            birch_answer = _opened(opened["answers"], "Spring study loan")
            self.assertEqual(cedar_answer["response"], "no")
            self.assertEqual(cedar_answer["finding_id"], successor)
            self.assertEqual(cedar_answer["predecessor"]["finding_id"], predecessor)
            self.assertEqual(cedar_answer["predecessor"]["response"], "yes")
            self.assertEqual(birch_answer["response"], "yes")
            self.assertEqual(birch_answer["finding_id"], birch_id)
            self.assertIsNone(birch_answer["predecessor"])
            earlier = opened["earlier_result"]
            self.assertEqual(earlier["status"], "earlier")
            self.assertEqual(earlier["run_id"], save_run)
            self.assertEqual(earlier["line21_disposition"], "blocked")
            run_ids = _run_ids(workspace)
            self.assertEqual(run_ids.get("initial.presentation.json"), _OPENING_RUN_ID)
            self.assertEqual(
                [name for name, run_id in run_ids.items() if run_id == save_run],
                [f"{save_run}.presentation.json"],
            )
            loans = _loans(workspace)
            self.assertEqual(loans["Autumn study loan"]["finding_id"], successor)
            self.assertEqual(loans["Autumn study loan"]["value"], "no")
            self.assertEqual(loans["Autumn study loan"]["predecessor_id"], predecessor)
            self.assertEqual(loans["Spring study loan"]["finding_id"], birch_id)
            self.assertEqual(loans["Spring study loan"]["value"], "yes")
            self.assertIsNone(loans["Spring study loan"]["predecessor_id"])

            calculated = _api(root, "calculate", {})
            self.assertEqual(calculated, {"calculated": True})
            self.assertEqual(_log_bytes(workspace), acts_after_save)
            _assert_same_files(outputs_after_save, workspace / "outputs")
            working = _api(root, "state")
            self.assertNotIn("opened", working)
            self.assertEqual(working["saved_run_id"], "demo.correction.run.s1")
            self.assertEqual(working["line21_disposition"], "blocked")
            self.assertEqual(
                _run_ids(workspace).get("demo.correction.run.s1.presentation.json"),
                "demo.correction.run.s1",
            )

            acts_before_next = _log_bytes(workspace)
            outputs_before_next = _tree(workspace / "outputs")
            again = _choice(working["choices"], "2025 Form 1098-E from Cedar")
            self.assertEqual(again["finding_id"], successor)
            review = _api(root, "choose", {"finding_id": again["finding_id"]})
            self.assertEqual(review["confirmation"]["current_answer"], "no")
            corrected = _api(root, "confirm", {"token": review["token"], "response": "yes"})
            self.assertEqual(corrected["outcome"], "saved-and-calculated")
            self.assertEqual(corrected["predecessor_finding_id"], successor)
            added = _new_acts(acts_before_next, _log_bytes(workspace))
            self.assertEqual([act.get("kind") for act in added].count("assertion"), 1)
            self.assertEqual([act.get("kind") for act in added].count("evidence-submitted"), 1)
            self.assertLessEqual(len(added), 4)
            evidence = next(act for act in added if act.get("kind") == "evidence-submitted")
            assertion = next(act for act in added if act.get("kind") == "assertion")
            self.assertEqual(
                evidence["payload"]["evidence"]["content"]["correction_of_finding_id"],
                successor,
            )
            new_successor = assertion["payload"]["finding"]["id"]
            self.assertEqual(corrected["successor_finding_id"], new_successor)
            loans = _loans(workspace)
            self.assertEqual(loans["Autumn study loan"]["finding_id"], new_successor)
            self.assertEqual(loans["Autumn study loan"]["value"], "yes")
            self.assertEqual(loans["Autumn study loan"]["predecessor_id"], successor)
            self.assertEqual(loans["Spring study loan"]["finding_id"], birch_id)
            self.assertEqual(loans["Spring study loan"]["value"], "yes")
            _assert_same_files(outputs_before_next, workspace / "outputs")
            _assert_same_files(outputs_after_save, workspace / "outputs")
        finally:
            opener.close()
            held.cleanup()

    def test_unfinished_save_reopens_on_the_opening_result(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        worker = _Child([sys.executable, str(_WORKER), str(workspace)], workspace)
        try:
            worker.ready()
        finally:
            worker.close()

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            self.assertFalse(opened["did_not_finish"])
            self.assertFalse(opened["records_not_established"])
            earlier = opened["earlier_result"]
            self.assertEqual(earlier["status"], "earlier")
            self.assertEqual(earlier["run_id"], _OPENING_RUN_ID)
            self.assertEqual(earlier["line21_value"], 2300)
            completed, still_open = _record_summary(workspace)
            self.assertEqual(completed, [_OPENING_RUN_ID])
            self.assertFalse(still_open)
            self.assertEqual(set(_run_ids(workspace)), {"initial.presentation.json"})
            cedar = _opened(opened["answers"], "Autumn study loan")
            birch = _opened(opened["answers"], "Spring study loan")
            loans = _loans(workspace)
            self.assertEqual(cedar["response"], "no")
            self.assertEqual(cedar["predecessor"]["response"], "yes")
            self.assertEqual(cedar["finding_id"], loans["Autumn study loan"]["finding_id"])
            self.assertEqual(
                cedar["predecessor"]["finding_id"],
                loans["Autumn study loan"]["predecessor_id"],
            )
            self.assertEqual(birch["response"], "yes")
            self.assertIsNone(birch["predecessor"])
            self.assertEqual(birch["finding_id"], loans["Spring study loan"]["finding_id"])
            self.assertIsNone(loans["Spring study loan"]["predecessor_id"])

            acts = _log_bytes(workspace)
            opening_output = _tree(workspace / "outputs")
            calculated = _api(root, "calculate", {})
            self.assertEqual(calculated, {"calculated": True})
            self.assertEqual(_log_bytes(workspace), acts)
            _assert_same_files(opening_output, workspace / "outputs")
            working = _api(root, "state")
            self.assertNotIn("opened", working)
            self.assertEqual(working["saved_run_id"], "demo.correction.run.s1")
            self.assertIn("demo.correction.run.s1.presentation.json", _run_ids(workspace))
        finally:
            opener.close()
            held.cleanup()

    def test_old_token_is_refused_by_the_next_process(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            token = chosen["token"]
            self.assertIsInstance(token, str)
            self.assertIn(".", token)
            acts = _log_bytes(workspace)
        finally:
            starter.close()

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts)
            status, body = _api_status(root, "confirm", {"token": token, "response": "no"})
            self.assertEqual(status, 422)
            self.assertNotIn(token, json.dumps(body))
            self.assertEqual(_log_bytes(workspace), acts)
            outcome = _api(root, "outcome", {"token": token})
            self.assertEqual(outcome, _UNKNOWN)
            self.assertNotIn(token, json.dumps(outcome))
            status, body = _api_status(root, "retry", {"token": token})
            self.assertEqual(status, 422)
            self.assertNotIn(token, json.dumps(body))
            self.assertEqual(_log_bytes(workspace), acts)
            self.assertEqual(_loans(workspace)["Autumn study loan"]["value"], "yes")
            self.assertIsNone(_loans(workspace)["Autumn study loan"]["predecessor_id"])
        finally:
            opener.close()
            held.cleanup()

    @unittest.skipUnless(_NODE and _BROWSER, "needs Node and a local Chrome/Chromium")
    def test_reopened_page_shows_the_correction_and_drops_an_old_token(self) -> None:
        # The new process binds a new port, so it is a new origin. This test
        # places the previous process's token into that origin's storage.
        # The page did not carry it.
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            token = chosen["token"]
            saved = _api(root, "confirm", {"token": token, "response": "no"})
            self.assertEqual(saved["outcome"], "saved-and-calculated")
        finally:
            starter.close()

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            url = opener.url()
            with urllib.request.urlopen(url, timeout=_HTTP_SECONDS) as response:
                page = response.read().decode("utf-8")
            if str(workspace) in page:
                raise AssertionError("the page contained the workspace directory")
            observed = _drive_resume(url, token, workspace)
            for key in (
                "showsCedarCorrected",
                "showsBirchUnchanged",
                "earlierResultNamed",
                "earlierResultBlocked",
                "noDidNotFinishClaim",
                "bannerHidden",
                "calculateShowsLine21",
                "correctionConfirmed",
                "undetermined",
                "notShownAsNotSaved",
                "tokenDropped",
                "noLeakedCodePatterns",
            ):
                self.assertTrue(observed[key], key)
            self.assertEqual(observed["leakedCodePatterns"], [])
        finally:
            opener.close()
            held.cleanup()


def _drive_resume(url: str, token: str, workspace: Path) -> dict[str, Any]:
    assert _NODE is not None
    proc = subprocess.Popen(
        [_NODE, str(_BROWSER_CLIENT), url, "resume-completed", token],
        cwd=str(REPO),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(
            timeout=_RESUME_STEPS * _STEP_BUDGET_SECONDS + _BROWSER_MARGIN_SECONDS)
    except subprocess.TimeoutExpired:
        _kill_group(proc.pid)
        proc.wait(timeout=10)
        raise AssertionError("browser client timed out") from None
    finally:
        if proc.poll() is None:
            _kill_group(proc.pid)
            proc.wait(timeout=10)
    if proc.returncode != 0:
        detail = stderr.replace(str(workspace), "<workspace>")
        raise AssertionError(detail or "browser client failed")
    observed = json.loads(stdout)
    if not isinstance(observed, dict):
        raise AssertionError("browser client returned an unexpected payload")
    return observed
