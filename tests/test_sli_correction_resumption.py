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
import re
import shutil
import signal
import socket
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
from unittest import mock

import packages.derivation.correction_session as correction_session_mod
from packages.derivation.correction_session import (
    LOAN_COST_FACT_TYPE,
    CorrectionRuntime,
    CorrectionSessionError,
    CorrectionSessionServer,
    build_correction_surface,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.records import RECORD_STREAM_FILENAME, RecordStream
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.loader import install_domain_scoped_supersession

REPO = Path(__file__).resolve().parent.parent
_RUNNER = [sys.executable, "-m", "packages.derivation.runners.sli_correction_evaluation"]
_WORKER = REPO / "tests" / "helpers" / "sli_resumption_unfinished_worker.py"
_OPEN_RUN_WORKER = REPO / "tests" / "helpers" / "sli_resumption_open_run_worker.py"
_REFUSED_OPENING_WORKER = REPO / "tests" / "helpers" / "sli_resumption_refused_opening_worker.py"
_BROWSER_CLIENT = REPO / "tests" / "helpers" / "correction_browser_client.mjs"
_HTTP_SECONDS = 600
_READY_SECONDS = 600
# Sequential browser steps per scenario, including the initial load.
# resume-completed: opened state, calculate, choice, confirmation, calculated
# outcome, reload, undetermined sentence. The others are counted beside their
# scenarios in correction_browser_client.mjs.
_SCENARIO_STEPS = {
    "resume-completed": 8,
    "calculate-dropped": 3,
    "calculate-refused": 3,
    "opened-uninterpretable": 2,
}
_STEP_BUDGET_SECONDS = 600
_BROWSER_MARGIN_SECONDS = 120
_OPENING_RUN_ID = "demo.correction.run.initial"
# A calculation's run id carries its runtime's own nonce (R4 finding 1), so
# no two processes on one workspace can produce the same run id.
_SESSION_RUN = re.compile(r"demo\.correction\.run\.c[0-9a-f]{12}\.s1")
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
    except (ProcessLookupError, PermissionError):
        # A self-killing worker races this call: its own SIGKILL to
        # itself can already have ended the process group leader by the
        # time this runs, which this platform sometimes reports as EPERM
        # rather than ESRCH.
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
        raw = path.read_bytes()
        if not raw:
            continue
        model = json.loads(raw)
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


def _presentation_path(workspace: Path, run_id: str) -> Path:
    matches = [
        path for path, found_run_id in _run_ids(workspace).items() if found_run_id == run_id
    ]
    if len(matches) != 1:
        raise AssertionError("expected exactly one presentation file for this run id")
    return workspace / "outputs" / matches[0]


def _records_path(workspace: Path) -> Path:
    return workspace / "records" / RECORD_STREAM_FILENAME


def _corrupt_first_record_line(workspace: Path) -> None:
    """Replace the record stream's first committed line with malformed JSON,
    directly on disk -- a file mutation, never a product-code failure
    switch. ``RecordStream.read()`` raises ``RecordStreamCorruption`` on it."""
    path = _records_path(workspace)
    lines = path.read_bytes().split(b"\n")
    if not lines or not lines[0]:
        raise AssertionError("expected at least one committed record line")
    lines[0] = b"{not valid json"
    path.write_bytes(b"\n".join(lines))


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

    def test_calculating_in_successive_runtimes_never_reuses_a_run_id(self) -> None:
        # R4 finding 1: every runtime's serial starts again at 1, so the run
        # id and output name must also carry the runtime's own nonce. Before
        # the repair, the second runtime's calculation collided with the
        # first one's reserved output and was reported as not calculated.
        held = _outside_repository()
        workspace = Path(held.name) / "L"
        try:
            CorrectionRuntime.initialize(WorkspaceCapability(workspace), repo_root=REPO)
            acts = _log_bytes(workspace)
            run_ids = []
            for _ in range(2):
                runtime = CorrectionRuntime.open(WorkspaceCapability(workspace), repo_root=REPO)
                self.assertEqual(runtime.calculate(), {"calculated": True})
                run_ids.append(runtime.state()["saved_run_id"])
                self.assertEqual(_log_bytes(workspace), acts)
            self.assertNotEqual(run_ids[0], run_ids[1])
            for run_id in run_ids:
                self.assertRegex(run_id, _SESSION_RUN)
            completed = [
                record["run_id"] for record in RecordStream(workspace / "records", _schemas()).read().records
                if record["phase"] == "completed"
            ]
            self.assertEqual(completed[-2:], run_ids)
            reopened = CorrectionRuntime.open(WorkspaceCapability(workspace), repo_root=REPO).state()
            self.assertEqual(reopened["earlier_result"]["status"], "earlier")
            self.assertEqual(reopened["earlier_result"]["run_id"], run_ids[1])
        finally:
            held.cleanup()

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
            self.assertRegex(working["saved_run_id"], _SESSION_RUN)
            self.assertEqual(working["line21_disposition"], "blocked")
            self.assertEqual(
                _run_ids(workspace).get(f"{working['saved_run_id']}.presentation.json"),
                working["saved_run_id"],
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
            self.assertRegex(working["saved_run_id"], _SESSION_RUN)
            self.assertIn(f"{working['saved_run_id']}.presentation.json", _run_ids(workspace))
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

    def test_missing_result_file_is_unavailable_not_lost(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            saved = _api(root, "confirm", {"token": chosen["token"], "response": "no"})
            self.assertEqual(saved["outcome"], "saved-and-calculated")
            successor = saved["successor_finding_id"]
            predecessor = saved["predecessor_finding_id"]
            save_run = f"demo.correction.run.{successor}"
        finally:
            starter.close()

        # The completed record's own presentation is removed -- a file
        # mutation, never a product-code failure switch. The completed
        # record itself stays in the stream.
        _presentation_path(workspace, save_run).unlink()
        acts_before_reopen = _log_bytes(workspace)

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            self.assertEqual(cedar_answer["response"], "no")
            self.assertEqual(cedar_answer["finding_id"], successor)
            self.assertEqual(cedar_answer["predecessor"]["finding_id"], predecessor)
            earlier = opened["earlier_result"]
            self.assertEqual(earlier["status"], "unavailable")
            self.assertEqual(earlier["run_id"], save_run)
            self.assertFalse(opened["did_not_finish"])

            calculated = _api(root, "calculate", {})
            self.assertEqual(calculated, {"calculated": True})
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
        finally:
            opener.close()
            held.cleanup()

    def test_duplicate_presentation_is_not_established(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            saved = _api(root, "confirm", {"token": chosen["token"], "response": "no"})
            self.assertEqual(saved["outcome"], "saved-and-calculated")
            successor = saved["successor_finding_id"]
            predecessor = saved["predecessor_finding_id"]
            save_run = f"demo.correction.run.{successor}"
        finally:
            starter.close()

        original = _presentation_path(workspace, save_run)
        duplicate = original.with_name("duplicate." + original.name)
        duplicate.write_bytes(original.read_bytes())
        acts_before_reopen = _log_bytes(workspace)

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            self.assertEqual(cedar_answer["response"], "no")
            self.assertEqual(cedar_answer["predecessor"]["finding_id"], predecessor)
            earlier = opened["earlier_result"]
            self.assertEqual(earlier["status"], "not-established")
            self.assertEqual(earlier["run_id"], save_run)
            self.assertFalse(opened["did_not_finish"])
        finally:
            opener.close()
            held.cleanup()

    def test_damaged_file_beside_a_match_is_its_own_status(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            saved = _api(root, "confirm", {"token": chosen["token"], "response": "no"})
            self.assertEqual(saved["outcome"], "saved-and-calculated")
            successor = saved["successor_finding_id"]
            predecessor = saved["predecessor_finding_id"]
            save_run = f"demo.correction.run.{successor}"
            expected_line21 = saved["line21_value"]
            expected_disposition = saved["line21_disposition"]
        finally:
            starter.close()

        original = _presentation_path(workspace, save_run)
        damaged = original.with_name("damaged." + original.name)
        damaged.write_bytes(b"{not valid json")
        acts_before_reopen = _log_bytes(workspace)

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            self.assertEqual(cedar_answer["response"], "no")
            self.assertEqual(cedar_answer["predecessor"]["finding_id"], predecessor)
            earlier = opened["earlier_result"]
            # R3 finding 1: a single match beside a damaged neighbor is its
            # own status, never "not-established" (two real matches).
            self.assertEqual(earlier["status"], "damaged")
            self.assertEqual(earlier["run_id"], save_run)
            self.assertEqual(earlier["line21_value"], expected_line21)
            self.assertEqual(earlier["line21_disposition"], expected_disposition)
            self.assertFalse(opened["did_not_finish"])
        finally:
            opener.close()
            held.cleanup()

    def test_unreadable_record_stream_leaves_answers_visible(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            saved = _api(root, "confirm", {"token": chosen["token"], "response": "no"})
            self.assertEqual(saved["outcome"], "saved-and-calculated")
            successor = saved["successor_finding_id"]
            predecessor = saved["predecessor_finding_id"]
        finally:
            starter.close()

        _corrupt_first_record_line(workspace)
        acts_before_reopen = _log_bytes(workspace)

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            self.assertTrue(opened["records_not_established"])
            self.assertEqual(opened["earlier_result"], {"status": "records-not-established"})
            self.assertFalse(opened["did_not_finish"])
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            self.assertEqual(cedar_answer["response"], "no")
            self.assertEqual(cedar_answer["finding_id"], successor)
            self.assertEqual(cedar_answer["predecessor"]["finding_id"], predecessor)
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
        finally:
            opener.close()
            held.cleanup()

    def test_open_run_with_no_close_is_did_not_finish(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        worker = _Child(
            [sys.executable, str(_OPEN_RUN_WORKER), str(workspace)], workspace)
        try:
            worker.ready()
        finally:
            worker.close()

        completed, still_open = _record_summary(workspace)
        self.assertEqual(completed, [_OPENING_RUN_ID])
        self.assertTrue(still_open)
        acts_before_reopen = _log_bytes(workspace)

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            self.assertTrue(opened["did_not_finish"])
            self.assertFalse(opened["records_not_established"])
            earlier = opened["earlier_result"]
            # The kill happens after this run's own output path is reserved
            # (an empty file) but before anything is written to it. An empty
            # reservation carries no runId and is not a damaged copy of any
            # result (R4 finding 2), so the opening result stays "earlier".
            self.assertEqual(earlier["status"], "earlier")
            self.assertEqual(earlier["run_id"], _OPENING_RUN_ID)
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            self.assertEqual(cedar_answer["response"], "no")
            self.assertIsNotNone(cedar_answer["predecessor"])
            self.assertEqual(cedar_answer["predecessor"]["response"], "yes")

            calculated = _api(root, "calculate", {})
            self.assertEqual(calculated, {"calculated": True})
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            working = _api(root, "state")
            self.assertNotIn("opened", working)
            self.assertRegex(working["saved_run_id"], _SESSION_RUN)
        finally:
            opener.close()
            held.cleanup()

    def test_later_change_keeps_the_older_result_historical(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        # Both corrections happen in the one process that holds the
        # opening calculation already (``--init``), so a second session
        # never needs its own first ``calculate`` call before reopening --
        # that is exercised by other cases, and reusing this session's
        # own calculate serial twice would collide with itself.
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            saved1 = _api(root, "confirm", {"token": chosen["token"], "response": "no"})
            self.assertEqual(saved1["outcome"], "saved-and-calculated")
            successor1 = saved1["successor_finding_id"]
            older_run = f"demo.correction.run.{successor1}"

            working = _api(root, "state")
            cedar_working = _choice(working["choices"], "2025 Form 1098-E from Cedar")
            # ``choices`` is still keyed from the opening presentation --
            # this long-lived session never recalculated -- so the
            # displayed id is stale and is reported "superseded". Choosing
            # it still resolves against the current log, proven below by
            # the confirmation naming the just-saved "no" as current.
            self.assertIn(cedar_working["status"], {"current", "superseded"})
            review = _api(root, "choose", {"finding_id": cedar_working["finding_id"]})
            self.assertEqual(review["confirmation"]["current_answer"], "no")
            saved2 = _api(root, "confirm", {"token": review["token"], "response": "yes"})
            self.assertEqual(saved2["outcome"], "saved-and-calculated")
            successor2 = saved2["successor_finding_id"]
            self.assertEqual(saved2["predecessor_finding_id"], successor1)
            later_run = f"demo.correction.run.{successor2}"
        finally:
            starter.close()

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            earlier = opened["earlier_result"]
            # The latest completed run is the later change's own run, never
            # the result that predates it.
            self.assertEqual(earlier["status"], "earlier")
            self.assertEqual(earlier["run_id"], later_run)
            self.assertNotEqual(earlier["run_id"], older_run)
            self.assertNotEqual(earlier.get("line21_disposition"), "blocked")
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            self.assertEqual(cedar_answer["response"], "yes")
            self.assertEqual(cedar_answer["finding_id"], successor2)
            self.assertEqual(cedar_answer["predecessor"]["finding_id"], successor1)

            calculated = _api(root, "calculate", {})
            self.assertEqual(calculated, {"calculated": True})
            working = _api(root, "state")
            choice_now = _choice(working["choices"], "2025 Form 1098-E from Cedar")
            self.assertEqual(choice_now["finding_id"], successor2)
        finally:
            opener.close()
            held.cleanup()

    def test_workspace_with_no_completed_calculation_offers_calculate(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        worker = _Child(
            [sys.executable, str(_REFUSED_OPENING_WORKER), str(workspace)], workspace)
        try:
            worker.ready()
        finally:
            worker.close()

        completed, still_open = _record_summary(workspace)
        self.assertEqual(completed, [])
        self.assertFalse(still_open)
        acts_before_reopen = _log_bytes(workspace)
        self.assertNotEqual(acts_before_reopen, b"")

        opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
        try:
            root = _root(opener.url())
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            opened = _api(root, "state")
            _reject_path(opened, workspace)
            self.assertFalse(opened["did_not_finish"])
            self.assertFalse(opened["records_not_established"])
            self.assertEqual(opened["earlier_result"], {"status": "none"})
            self.assertTrue(opened["calculate"])
            cedar_answer = _opened(opened["answers"], "Autumn study loan")
            self.assertEqual(cedar_answer["response"], "yes")
            self.assertIsNone(cedar_answer["predecessor"])

            calculated = _api(root, "calculate", {})
            self.assertEqual(calculated, {"calculated": True})
            self.assertEqual(_log_bytes(workspace), acts_before_reopen)
            working = _api(root, "state")
            self.assertNotIn("opened", working)
            self.assertRegex(working["saved_run_id"], _SESSION_RUN)
        finally:
            opener.close()
            held.cleanup()

    def test_reopen_twice_without_editing_appends_nothing(self) -> None:
        held = _outside_repository()
        workspace = Path(held.name)
        try:
            starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
            try:
                starter.url()
            finally:
                starter.close()
            tree_after_init = _tree(workspace)
            acts_after_init = _log_bytes(workspace)

            first_opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
            try:
                first_opener.url()
                self.assertEqual(_log_bytes(workspace), acts_after_init)
            finally:
                first_opener.close()
            tree_after_first_open = _tree(workspace)

            second_opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
            try:
                second_opener.url()
                self.assertEqual(_log_bytes(workspace), acts_after_init)
            finally:
                second_opener.close()
            tree_after_second_open = _tree(workspace)

            _assert_same_files(tree_after_init, workspace)
            _assert_same_files(tree_after_first_open, workspace)

            new_after_first = set(tree_after_first_open) - set(tree_after_init)
            new_after_second = set(tree_after_second_open) - set(tree_after_first_open)
            self.assertTrue(new_after_first, "expected a new build target on the first reopen")
            self.assertTrue(new_after_second, "expected a new build target on the second reopen")
            for name in (*new_after_first, *new_after_second):
                self.assertTrue(
                    name.startswith(".correction-surface/"),
                    f"unexpected new file outside the surface build target: {name}",
                )
        finally:
            held.cleanup()

    def test_uninterpretable_earlier_explanation_keeps_the_account(self) -> None:
        # The saved presentation parses as JSON but its explanation cannot be
        # interpreted. The actual reader, in a new process, keeps the account,
        # its predecessor and the calculate action, and shows no part of the
        # explanation as if it were whole.
        held = _outside_repository()
        workspace = Path(held.name)
        starter = _Child([*_RUNNER, "--workspace", str(workspace), "--init"], workspace)
        try:
            root = _root(starter.url())
            state = _api(root, "state")
            cedar = _choice(state["choices"], "2025 Form 1098-E from Cedar")
            chosen = _api(root, "choose", {"finding_id": cedar["finding_id"]})
            saved = _api(root, "confirm", {"token": chosen["token"], "response": "no"})
            self.assertEqual(saved["outcome"], "saved-and-calculated")
            successor = saved["successor_finding_id"]
            predecessor = saved["predecessor_finding_id"]
            save_run = f"demo.correction.run.{successor}"
        finally:
            starter.close()

        presentation = _presentation_path(workspace, save_run)
        intact = json.loads(presentation.read_text("utf-8"))
        try:
            for name, damage in (("reason index", _damage_reason_index),
                                 ("rows", _damage_rows)):
                with self.subTest(damage=name):
                    presentation.write_text(json.dumps(damage(intact)), encoding="utf-8")
                    acts_before = _log_bytes(workspace)
                    opener = _Child([*_RUNNER, "--workspace", str(workspace)], workspace)
                    try:
                        url = opener.url()
                        root = _root(url)
                        opened = _api(root, "state")
                        _reject_path(opened, workspace)
                        self.assertTrue(opened["opened"])
                        self.assertTrue(opened["calculate"])
                        self.assertEqual(
                            opened["earlier_result"], {"status": "uninterpretable", "run_id": save_run})
                        cedar_answer = _opened(opened["answers"], "Autumn study loan")
                        self.assertEqual(cedar_answer["finding_id"], successor)
                        self.assertEqual(cedar_answer["response"], "no")
                        self.assertEqual(cedar_answer["predecessor"]["finding_id"], predecessor)
                        self.assertEqual(cedar_answer["predecessor"]["response"], "yes")
                        birch_answer = _opened(opened["answers"], "Spring study loan")
                        self.assertEqual(birch_answer["response"], "yes")
                        self.assertIsNone(birch_answer["predecessor"])
                        if _NODE and _BROWSER and name == "reason index":
                            observed = _drive_scenario(url, "opened-uninterpretable", workspace)
                            self.assertEqual(observed, {
                                "complete": True,
                                "explanationUnavailable": True,
                                "noPartialExplanation": True,
                                "showsCedarCorrected": True,
                                "showsBirchUnchanged": True,
                                "calculateOffered": True,
                                "noLeakedCodePatterns": True,
                                "leakedCodePatterns": [],
                            })
                        self.assertEqual(_log_bytes(workspace), acts_before)
                    finally:
                        opener.close()
        finally:
            held.cleanup()

    @unittest.skipUnless(_NODE and _BROWSER, "needs Node and a local Chrome/Chromium")
    def test_page_recovers_a_calculation_whose_response_was_lost(self) -> None:
        # The session calculates and saves its presentation; the response is
        # then dropped. The page reads the session's state once, shows the
        # calculated result, claims no failure and sends no second
        # calculation. No answer act is appended.
        held = _outside_repository()
        workspace = Path(held.name) / "L"
        try:
            CorrectionRuntime.initialize(WorkspaceCapability(workspace), repo_root=REPO)
            acts = _log_bytes(workspace)
            completed_before = _completed_run_ids(workspace)
            runtime = CorrectionRuntime.open(WorkspaceCapability(workspace), repo_root=REPO)
            dist = build_correction_surface(
                WorkspaceCapability(workspace), repo_root=REPO, opening_id="demo-dropped-calculate")
            with mock.patch.object(correction_session_mod._CorrectionRequestHandler, "do_POST",
                                   _do_post_dropping_first_calculate_response):
                with CorrectionSessionServer(runtime, dist) as server:
                    observed = _drive_scenario(server.url, "calculate-dropped", workspace)
            self.assertEqual(observed, {
                "complete": True,
                "recoveredHeading": True,
                "noFailureClaim": True,
                "noLeakedCodePatterns": True,
                "leakedCodePatterns": [],
            })
            self.assertEqual(_log_bytes(workspace), acts)
            completed_after = _completed_run_ids(workspace)
            self.assertEqual(completed_after[:len(completed_before)], completed_before)
            self.assertEqual(len(completed_after), len(completed_before) + 1)
            self.assertRegex(completed_after[-1], _SESSION_RUN)
            working = runtime.state()
            self.assertTrue(working["calculated_in_session"])
            self.assertEqual(working["saved_run_id"], completed_after[-1])
        finally:
            held.cleanup()

    @unittest.skipUnless(_NODE and _BROWSER, "needs Node and a local Chrome/Chromium")
    def test_page_states_an_explicit_calculation_refusal(self) -> None:
        # The session answers that it did not calculate. The page says so,
        # keeps the opened account, and offers calculating again.
        held = _outside_repository()
        workspace = Path(held.name) / "L"
        try:
            CorrectionRuntime.initialize(WorkspaceCapability(workspace), repo_root=REPO)
            acts = _log_bytes(workspace)
            completed_before = _completed_run_ids(workspace)
            runtime = CorrectionRuntime.open(WorkspaceCapability(workspace), repo_root=REPO)
            dist = build_correction_surface(
                WorkspaceCapability(workspace), repo_root=REPO, opening_id="demo-refused-calculate")
            with mock.patch.object(correction_session_mod, "live_coordinate_run",
                                   side_effect=RuntimeError("demo refusal")):
                with CorrectionSessionServer(runtime, dist) as server:
                    observed = _drive_scenario(server.url, "calculate-refused", workspace)
            self.assertEqual(observed, {
                "complete": True,
                "saysDidNotCalculate": True,
                "openedAccountShown": True,
                "calculateStillOffered": True,
                "noLeakedCodePatterns": True,
                "leakedCodePatterns": [],
            })
            self.assertEqual(_log_bytes(workspace), acts)
            self.assertEqual(_completed_run_ids(workspace), completed_before)
            self.assertTrue(runtime.state()["opened"])
        finally:
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


def _drive_scenario(url: str, scenario: str, workspace: Path, token: str = "") -> dict[str, Any]:
    assert _NODE is not None
    proc = subprocess.Popen(
        [_NODE, str(_BROWSER_CLIENT), url, scenario, token],
        cwd=str(REPO),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(
            timeout=_SCENARIO_STEPS[scenario] * _STEP_BUDGET_SECONDS + _BROWSER_MARGIN_SECONDS)
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


def _drive_resume(url: str, token: str, workspace: Path) -> dict[str, Any]:
    return _drive_scenario(url, "resume-completed", workspace, token)


_ORIGINAL_DO_POST = correction_session_mod._CorrectionRequestHandler.do_POST


def _do_post_dropping_first_calculate_response(self: Any) -> None:
    """Test-only: let the real ``calculate()`` run to completion server-side,
    then drop the TCP connection before any response byte is written. The
    page's fetch() rejects -- a transport failure, not an HTTP status. Only
    the first ``/api/calculate`` is dropped; a second one, if the page sent
    it, would be served and counted."""
    target = self._target()
    if (target is not None and target[1] == "api/calculate"
            and not getattr(self.server, "_calculate_response_dropped", False)):
        self.server._calculate_response_dropped = True
        self._read_body()
        self.server.runtime.calculate()
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.close_connection = True
        return
    _ORIGINAL_DO_POST(self)


def _completed_run_ids(workspace: Path) -> list[str]:
    return [
        record["run_id"] for record in RecordStream(workspace / "records", _schemas()).read().records
        if record["phase"] == "completed"
    ]


def _damage_reason_index(model: dict[str, Any]) -> dict[str, Any]:
    """A valid JSON presentation whose named-by-reason row names a reason
    index the line 21 section does not have."""
    damaged: dict[str, Any] = json.loads(json.dumps(model))
    for row in damaged["line21Explanation"]["rows"]:
        status = row.get("status")
        if isinstance(status, dict) and status.get("kind") == "named-by-reason":
            status["reasonIndices"] = [999]
            return damaged
    raise AssertionError("no named-by-reason row to damage")


def _damage_rows(model: dict[str, Any]) -> dict[str, Any]:
    """A valid JSON presentation whose explanation rows are not objects."""
    damaged: dict[str, Any] = json.loads(json.dumps(model))
    damaged["line21Explanation"]["rows"] = ["not a row"]
    return damaged
