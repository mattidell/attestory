#!/usr/bin/env python3
"""Run the sale-page P0 returns and retain real saved-page observations.

All source returns are the committed synthetic cases in
``tests/test_noncovered_sales_v79.py``. Full run output is written only below
the ignored ``temp/`` tree; this command writes a concise evidence report in
the assigned sale-page-observation evidence directory.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, TypedDict


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs/phases/engine-breadth/milestones/sale-page-observation-evidence"
QUESTION_TEXT = "Did you sell any securities whose basis was not reported to the IRS?"
CASES: tuple[dict[str, Any], ...] = (
    {
        "id": "mortgage-1098",
        "source_case": "one_mortgage",
        "principal_field": "tax.us.2025.schedule-a.line8a",
        "inputs": (
            "Base: single filer, W-2 wages $50,000 and withholding $4,500. One Form 1098; "
            "box 1 interest $4,000, box 2 principal $200,000, origination 2020-06-01, "
            "one property. The case records the existing mortgage-use and payment answers."
        ),
        "answered_noncovered_question": "no",
    },
    {
        "id": "covered-long-term-sale",
        "source_case": "covered_flag_yes",
        "principal_field": "tax.us.2025.schedule-d.line-8a",
        "inputs": (
            "Base wages $50,000. One covered long-term sale: proceeds $6,000, basis $2,000, "
            "basis reported to the IRS; noncovered-sale answer no."
        ),
        "answered_noncovered_question": "no",
    },
    {
        "id": "noncovered-box-e-sale",
        "source_case": "lt_gain",
        "principal_field": "tax.us.2025.schedule-d.line-9",
        "inputs": (
            "Base wages $50,000. One long-term noncovered box E sale: proceeds $6,000, "
            "supplied basis $2,000; the return records the noncovered-sale answer yes."
        ),
        "answered_noncovered_question": "yes",
    },
    {
        "id": "wash-sale-code-w",
        "source_case": "wash",
        "principal_field": "tax.us.2025.schedule-d.line-9",
        "inputs": (
            "Base wages $50,000. One long-term sale on the existing code W route: proceeds "
            "$4,000, basis $7,000, box 1g adjustment $1,000; the return records the "
            "noncovered-sale answer yes."
        ),
        "answered_noncovered_question": "yes",
    },
    {
        "id": "covered-basis-not-reported",
        "source_case": "covered_flag_corrected_to_no",
        "principal_field": "tax.us.2025.schedule-d.line-8a",
        "inputs": (
            "Base wages $50,000. One covered long-term sale: proceeds $6,000, basis $2,000, "
            "covered-security flag yes; a correction changes basis-reported-to-IRS from yes "
            "to no. The noncovered-sale answer is no."
        ),
        "answered_noncovered_question": "no",
    },
    {
        "id": "wage-single-noncovered-no",
        "source_case": "one_wage",
        "principal_field": "tax.us.2025.schedule-d.line-9",
        "inputs": (
            "Single filer, W-2 wages $50,000 and withholding $4,500; no sales; one no answer "
            "to the shared noncovered-sale question."
        ),
        "answered_noncovered_question": "no",
    },
    {
        "id": "wage-unanswered-question",
        "source_case": "wage_unclosed",
        "principal_field": "tax.us.2025.schedule-d.line-9",
        "inputs": (
            "Blocked variant of the wage-only return: single filer, wages $50,000 and "
            "withholding $4,500; no noncovered-sale answer is recorded."
        ),
        "answered_noncovered_question": "unanswered",
    },
    {
        "id": "sale-answer-needs-reconfirmation",
        "source_case": "late_member_unclosed",
        "principal_field": "tax.us.2025.schedule-d.line-9",
        "inputs": (
            "Blocked variant: a long-term sale is added after the shared noncovered-sale "
            "answer no, without recording a confirming answer after the sale."
        ),
        "answered_noncovered_question": "stale-no",
    },
)

MORTGAGE_ITEMIZATION_CASE: dict[str, Any] = {
    "id": "mortgage-itemized-missing-boundaries",
    "source_case": "current_core_returns.add_mortgage_itemizer(20000)",
    "principal_field": "tax.us.2025.schedule-a.line8a",
    "inputs": (
        "Base: single filer, W-2 wages $50,000 and withholding $4,500. One Form 1098; "
        "box 1 interest $20,000, box 2 principal $200,000, origination 2020-06-01, "
        "one property, existing mortgage-use and payment answers, and shared "
        "noncovered-sale answer no. This uses the existing mortgage builder with a "
        "higher interest amount so the itemized result exceeds the $15,750 standard deduction observed in the baseline. "
        "The seven non-mortgage Schedule A boundaries, no-QBI, and no-Schedule-1-A answers "
        "are explicitly recorded; no-other-line16 is intentionally unanswered. The exact "
        "missing Schedule A input is reported from the coordinator below."
    ),
    "answered_noncovered_question": "no",
}

MORTGAGE_ITEMIZATION_DECLARATIONS_CASE: dict[str, Any] = {
    **MORTGAGE_ITEMIZATION_CASE,
    "id": "mortgage-itemized-declared-boundaries",
    "source_case": "current_core_returns.add_mortgage_itemizer(20000) plus explicit boundary declarations",
    "inputs": (
        MORTGAGE_ITEMIZATION_CASE["inputs"]
        + " The synthetic return also declares no medical, SALT, other-interest, investment-interest, "
        "charitable, casualty/theft, or gambling/other Schedule A deductions, and declares no QBI or "
        "Schedule 1-A deduction."
    ),
}

MORTGAGE_ITEMIZATION_COMPLETE_SCOPE_CASE: dict[str, Any] = {
    **MORTGAGE_ITEMIZATION_DECLARATIONS_CASE,
    "id": "mortgage-itemized-complete-scope",
    "source_case": "current_core_returns.add_mortgage_itemizer(20000), explicit boundary declarations, and no-other-line16 declaration",
    "inputs": MORTGAGE_ITEMIZATION_DECLARATIONS_CASE["inputs"].replace(
        "no-other-line16 is intentionally unanswered. The exact missing Schedule A input is reported from the coordinator below.",
        "the no-other-line16 declaration is explicitly recorded for this complete-scope variant.",
    ),
}

REGRESSION_CASES: tuple[dict[str, Any], ...] = (
    *CASES,
    MORTGAGE_ITEMIZATION_DECLARATIONS_CASE,
    MORTGAGE_ITEMIZATION_COMPLETE_SCOPE_CASE,
)

CORE_SURFACES: dict[str, dict[str, str]] = {
    "v79": {
        "package": "package.core-calculations.v79.json",
        "package_version": "v79",
        "registry": "published-packages.v77.json",
        "release": "demo.release.sli-worksheet-integration.2025.v77.json",
        "release_version": "v77",
    },
    "v80": {
        "package": "package.core-calculations.v80.json",
        "package_version": "v80",
        "registry": "published-packages.v78.json",
        "release": "demo.release.sli-worksheet-integration.2025.v78.json",
        "release_version": "v78",
    },
    "v82": {
        "package": "package.core-calculations.v82.json",
        "package_version": "v82",
        "registry": "published-packages.v80.json",
        "release": "demo.release.sli-worksheet-integration.2025.v80.json",
        "release_version": "v80",
    },
    "v89": {
        "package": "package.core-calculations.v89.json",
        "package_version": "v89",
        "registry": "published-packages.v87.json",
        "release": "demo.release.sli-worksheet-integration.2025.v87.json",
        "release_version": "v87",
    },
}


def _select_core_surface(probe: Any, core_version: str) -> dict[str, str]:
    """Pin every surface field for each run, even when a previous run used another core."""
    selected = CORE_SURFACES[core_version]
    expected_pins = {
        "PACKAGE": selected["package"],
        "PACKAGE_VERSION": selected["package_version"],
        "REGISTRY": selected["registry"],
        "RELEASE": selected["release"],
        "RELEASE_VERSION": selected["release_version"],
    }
    for key, value in expected_pins.items():
        setattr(probe, key, value)
    actual_pins = {key: getattr(probe, key) for key in expected_pins}
    if actual_pins != expected_pins:
        raise SystemExit("The synthetic case builder did not select the explicitly requested package surface.")
    return selected


_BROWSER_FAILURE_REASONS = frozenset("""
    invalid-case-manifest case-manifest-unavailable case-manifest-invalid
    browser-version-timeout browser-context-timeout target-create-timeout target-attach-timeout
    page-enable-timeout runtime-enable-timeout fetch-enable-timeout page-navigation-timeout
    page-navigation-failed page-load-timeout page-load-failed page-requested-non-loopback-resource
    dom-evaluation-timeout dom-evaluation-failed target-close-timeout context-dispose-timeout
    browser-context-cleanup-failed observation-output-unavailable browser-cleanup-failed
    chrome-not-found chrome-launch-failed server-start-failed browser-observation-failed
""".split())
_BROWSER_FAILURE_STAGES = frozenset(
    "case-manifest loopback-server chrome-startup cdp-connect browser-version "
    "page-observation observation-output cleanup unknown python-subprocess".split()
)
_BROWSER_FAILURE_CATEGORIES = frozenset("timeout chrome-launch manifest cleanup unclassified observation".split())
_BROWSER_PROGRESS_STAGES = frozenset("""
    loopback-start loopback-ready chrome-launch-start chrome-launch-ready
    cdp-connect-start cdp-connect-ready browser-version-start browser-version-ready
    case-start case-context-ready page-load-start page-load-complete dom-read-start dom-read-complete
    case-cleanup-start case-cleanup-complete cleanup-start client-close-complete
    chrome-dispose-start chrome-dispose-complete server-close-start server-close-complete
    observer-flush-start observer-flush-complete cleanup-complete
""".split())
_BROWSER_PROGRESS_MAX_BYTES = 65_536
_BROWSER_PROGRESS_MAX_LINE_BYTES = 512
_BROWSER_PROGRESS_MAX_RECORDS = 96


class _SafeFailureRecord(TypedDict):
    reason: str
    category: str
    stage: str


class _SafeProgressRecord(TypedDict):
    stage: str
    elapsed_ms: int
    case_index: int
_CHROME_LAUNCH_OUTCOMES = frozenset(
    "resolve_failure spawn_failure exit_before_ready exit_after_deadline ready_accepted "
    "ready_after_deadline not_ready_after_grace cancelled queue_failed".split()
)
_CHROME_STDERR_CATEGORIES = frozenset("""
    devtools-active-port-write-error devtools-http-server-start-error pthread-create-resource-unavailable
    thread-start-resource-unavailable cannot-allocate-memory out-of-memory too-many-open-files
    no-usable-sandbox running-as-root-without-no-sandbox failed-to-move-to-new-namespace
    user-namespace-operation-not-permitted profile-in-use singleton-lock-failed
    devtools-bind-address-in-use missing-x-server crashpad-handler-failed zygote-fork-failed
""".split())


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _system_temp_parent() -> Path:
    candidates = (
        [Path("/tmp"), Path("/var/tmp"), Path(tempfile.gettempdir())]
        if os.name == "posix"
        else [Path(tempfile.gettempdir())]
    )
    for candidate in candidates:
        if candidate.is_dir() and os.access(candidate, os.W_OK | os.X_OK):
            return candidate
    raise RuntimeError("no writable system temporary directory is available")


def _new_owned_chrome_tempdir() -> Path:
    """Create a private short root, independent of inherited TMPDIR."""
    for base in dict.fromkeys((Path("/tmp"), Path("/var/tmp"), _system_temp_parent())):
        if not base.is_dir() or not os.access(base, os.W_OK | os.X_OK):
            continue
        try:
            root = Path(tempfile.mkdtemp(prefix="spo-", dir=base))
        except OSError:
            continue
        # Reserve room for Node's profile prefix, its six random characters,
        # and Chrome's Unix-domain singleton socket filename.
        socket_path = root / "presentation-harness-profile-XXXXXX" / "SingletonSocket"
        if not sys.platform.startswith("linux") or len(os.fsencode(socket_path)) <= 107:
            return root
        shutil.rmtree(root, ignore_errors=True)
    raise RuntimeError("no short system temporary directory fits Chrome's Linux socket path")


def _matching_fact_rows(acts: Iterable[Mapping[str, object]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "fact_id": str(finding.get("fact_id")),
            "value": finding.get("value"),
        }
        for act in acts
        if isinstance(act, dict)
        for finding in [_safe_dict(_safe_dict(act.get("payload")).get("finding"))]
        if isinstance(finding.get("fact_id"), str) and finding["fact_id"].startswith(prefix)
    ]


def _prepare_v89_covered_sale_companions(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Carry the covered-sale case on v89's same-identity scalar contract.

    The historical v79 fixture recorded a covered transaction object and its
    proceeds/basis scalar members under separate synthetic transaction ids.
    Core v82 and later require those scalar members to share the transaction
    object's identity. Re-key only those existing fixture members; their
    family-horizon closure witnesses and all values stay unchanged.
    """
    out = copy.deepcopy(acts)
    parent_type = "tax.us.2025.f1099b.covered-lt-txn"
    parent_rows: list[tuple[str, dict[str, Any], str]] = []
    for act in out:
        if act.get("kind") != "member-transition":
            continue
        payload = _safe_dict(act.get("payload"))
        member = _safe_dict(payload.get("member"))
        finding = _safe_dict(member.get("finding"))
        fact_id = finding.get("fact_id")
        value = finding.get("value")
        if isinstance(fact_id, str) and fact_id.startswith(parent_type + "|") and isinstance(value, dict):
            parent_rows.append((fact_id.split("|", 1)[1], value, str(member.get("action") or "")))
    if not parent_rows:
        return out

    target_identity, target_value, target_action = parent_rows[-1]
    if target_action != "assert":
        raise ValueError("v89 covered-sale carry has no current transaction object")
    identities = {identity for identity, _value, action in parent_rows if action == "assert"}
    if identities != {target_identity}:
        raise ValueError("v89 covered-sale carry has ambiguous transaction identities")
    identity_fields = dict(
        part.split("=", 1) for part in target_identity.split(",") if "=" in part
    )
    transaction_id = identity_fields.get("transaction")
    if not isinstance(transaction_id, str) or not transaction_id.endswith(".transaction"):
        raise ValueError("v89 covered-sale carry has no transaction identity")
    target_horizon = transaction_id.removesuffix(".transaction") + ".h1"
    target_closure = f"tax.us.2025.f1099b.covered-lt.source-closure|family-horizon={target_horizon},"
    if not any(
        isinstance(_safe_dict(_safe_dict(act.get("payload")).get("finding")).get("fact_id"), str)
        and str(_safe_dict(_safe_dict(act.get("payload")).get("finding")).get("fact_id")).startswith(target_closure)
        for act in out
    ):
        raise ValueError("v89 covered-sale carry lacks its matching closure witness")

    child_families = {
        f"{parent_type}.proceeds": ("proceeds", "tax.us.2025.f1099b.covered-lt-proceeds"),
        f"{parent_type}.basis": ("basis", "tax.us.2025.f1099b.covered-lt-basis"),
    }
    expected_closure_prefixes: set[str] = set()
    for act in out:
        if act.get("kind") != "member-transition":
            continue
        payload = _safe_dict(act.get("payload"))
        member = _safe_dict(payload.get("member"))
        finding = _safe_dict(member.get("finding"))
        fact_id = finding.get("fact_id")
        if not isinstance(fact_id, str):
            continue
        for child_type, (field, closure_type) in child_families.items():
            if not fact_id.startswith(child_type + "|"):
                continue
            if finding.get("value") != target_value.get(field):
                raise ValueError("v89 covered-sale scalar does not match its transaction object")
            old_identity = fact_id.split("|", 1)[1]
            old_fields = dict(
                part.split("=", 1) for part in old_identity.split(",") if "=" in part
            )
            old_transaction = old_fields.get("transaction")
            if not isinstance(old_transaction, str) or not old_transaction.endswith(".transaction"):
                raise ValueError("v89 covered-sale scalar has no transaction identity")
            old_horizon = old_transaction.removesuffix(".transaction") + ".h1"
            expected_closure_prefixes.add(
                f"{closure_type}.source-closure|family-horizon={old_horizon},"
            )
            finding["fact_id"] = child_type + "|" + target_identity

    if not expected_closure_prefixes:
        return out
    closure_fact_ids = {
        finding.get("fact_id")
        for act in out
        for finding in [_safe_dict(_safe_dict(act.get("payload")).get("finding"))]
        if isinstance(finding.get("fact_id"), str)
    }
    if any(
        not any(
            isinstance(fact_id, str) and fact_id.startswith(prefix)
            for fact_id in closure_fact_ids
        )
        for prefix in expected_closure_prefixes
    ):
        raise ValueError("v89 covered-sale scalar lacks its matching closure witness")
    return out


class _BoundedBrowserFailure(RuntimeError):
    """Safe timeout summary; retains only counts and validated Node fields."""

    def __init__(
        self,
        reason: str,
        stdout_bytes: int,
        stderr_bytes: int,
        node_failure: _SafeFailureRecord | None = None,
        node_progress: _SafeProgressRecord | None = None,
    ) -> None:
        super().__init__(reason)
        self.reason = reason
        self.stdout_bytes = stdout_bytes
        self.stderr_bytes = stderr_bytes
        self.node_failure = node_failure
        self.node_progress = node_progress


def _captured_byte_count(value: str | bytes | None) -> int:
    if isinstance(value, bytes):
        return len(value)
    if isinstance(value, str):
        return len(value.encode("utf-8", errors="surrogateescape"))
    return 0


def _safe_failure_record_if_present(
    stderr: str | bytes | None,
) -> _SafeFailureRecord | None:
    """Decode the first bounded, closed-vocabulary Node error record."""
    if isinstance(stderr, bytes):
        text = stderr[:_BROWSER_PROGRESS_MAX_BYTES].decode("utf-8", errors="replace")
    elif isinstance(stderr, str):
        text = stderr[:_BROWSER_PROGRESS_MAX_BYTES]
    else:
        return None
    for raw_line in text.splitlines()[:_BROWSER_PROGRESS_MAX_RECORDS]:
        if len(raw_line.encode("utf-8", errors="surrogateescape")) > _BROWSER_PROGRESS_MAX_LINE_BYTES:
            continue
        try:
            payload = json.loads(raw_line)
        except (ValueError, RecursionError):
            continue
        if (
            not isinstance(payload, dict)
            or set(payload) != {"error", "reason", "category", "stage"}
            or payload.get("error") is not True
        ):
            continue
        reason = payload.get("reason")
        category = payload.get("category")
        stage = payload.get("stage")
        if (
            isinstance(reason, str)
            and reason in _BROWSER_FAILURE_REASONS
            and isinstance(category, str)
            and category in _BROWSER_FAILURE_CATEGORIES
            and isinstance(stage, str)
            and stage in _BROWSER_FAILURE_STAGES
        ):
            return {"reason": reason, "category": category, "stage": stage}
    return None


def _safe_progress_record_if_present(stdout: str | bytes | None) -> _SafeProgressRecord | None:
    """Project only the last bounded, allowlisted Node progress record."""
    if isinstance(stdout, bytes):
        text = stdout[-_BROWSER_PROGRESS_MAX_BYTES:].decode("utf-8", errors="replace")
    elif isinstance(stdout, str):
        text = stdout[-_BROWSER_PROGRESS_MAX_BYTES:]
    else:
        return None
    selected: _SafeProgressRecord | None = None
    for raw_line in text.splitlines()[-_BROWSER_PROGRESS_MAX_RECORDS:]:
        if len(raw_line.encode("utf-8", errors="surrogateescape")) > _BROWSER_PROGRESS_MAX_LINE_BYTES:
            continue
        try:
            payload = json.loads(raw_line)
        except (ValueError, RecursionError):
            continue
        if (
            not isinstance(payload, dict)
            or set(payload) != {"kind", "stage", "elapsed_ms", "case_index"}
            or payload.get("kind") != "progress"
        ):
            continue
        stage = payload.get("stage")
        elapsed_ms = payload.get("elapsed_ms")
        case_index = payload.get("case_index")
        if (
            isinstance(stage, str)
            and stage in _BROWSER_PROGRESS_STAGES
            and type(elapsed_ms) is int
            and 0 <= elapsed_ms <= 600_000
            and type(case_index) is int
            and 0 <= case_index <= 10
        ):
            selected = {
                "stage": stage,
                "elapsed_ms": elapsed_ms,
                "case_index": case_index,
            }
    return selected


def _captured_bytes(value: str | bytes | None) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8", errors="surrogateescape")
    return b""


def _largest_capture(captures: list[bytes]) -> bytes:
    return max(captures, key=len, default=b"")


def _run_bounded_subprocess(
    command: list[str], *, cwd: Path, env: dict[str, str], timeout_seconds: float
) -> subprocess.CompletedProcess[str]:
    """Run one owned process group and reap it on success or bounded timeout."""
    child = subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = child.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired as first_timeout:
        stdout_captures = [_captured_bytes(first_timeout.output)]
        stderr_captures = [_captured_bytes(first_timeout.stderr)]
        try:
            os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            stdout, stderr = child.communicate(timeout=5)
            stdout_captures.append(_captured_bytes(stdout))
            stderr_captures.append(_captured_bytes(stderr))
        except subprocess.TimeoutExpired as second_timeout:
            stdout_captures.append(_captured_bytes(second_timeout.output))
            stderr_captures.append(_captured_bytes(second_timeout.stderr))
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                stdout, stderr = child.communicate(timeout=5)
                stdout_captures.append(_captured_bytes(stdout))
                stderr_captures.append(_captured_bytes(stderr))
            except subprocess.TimeoutExpired as final_timeout:
                stdout_captures.append(_captured_bytes(final_timeout.output))
                stderr_captures.append(_captured_bytes(final_timeout.stderr))
                stdout_data = _largest_capture(stdout_captures)
                stderr_data = _largest_capture(stderr_captures)
                raise _BoundedBrowserFailure(
                    "owned-browser-process-cleanup-timeout",
                    len(stdout_data),
                    len(stderr_data),
                    _safe_failure_record_if_present(stderr_data),
                    _safe_progress_record_if_present(stdout_data),
                ) from None
        stdout_data = _largest_capture(stdout_captures)
        stderr_data = _largest_capture(stderr_captures)
        raise _BoundedBrowserFailure(
            "browser-observation-timeout",
            len(stdout_data),
            len(stderr_data),
            _safe_failure_record_if_present(stderr_data),
            _safe_progress_record_if_present(stdout_data),
        ) from None
    # Decode only after process completion. `surrogateescape` keeps invalid
    # bytes round-trippable and preserves exact byte counts at the boundary.
    return subprocess.CompletedProcess(
        command,
        child.returncode,
        stdout.decode("utf-8", errors="surrogateescape"),
        stderr.decode("utf-8", errors="surrogateescape"),
    )


def _safe_failure_record(stderr: str | bytes) -> _SafeFailureRecord:
    """Read only the Node tool's closed-vocabulary diagnostic, never raw logs."""
    return _safe_failure_record_if_present(stderr) or {
        "reason": "browser-observation-failed",
        "category": "unclassified",
        "stage": "unknown",
    }


def _safe_launch_record(path: Path) -> dict[str, Any] | None:
    """Project the existing Chrome observer record to bounded safe fields."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()[-16:]
    except (OSError, UnicodeError):
        return None
    for line in reversed(lines):
        if len(line) > 65_536:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict) or payload.get("label") != "other":
            continue
        outcome = payload.get("outcome")
        if not isinstance(outcome, str) or outcome not in _CHROME_LAUNCH_OUTCOMES:
            continue
        projected: dict[str, Any] = {"outcome": outcome}
        for key in ("queue_ms", "elapsed_ms", "readiness_ms", "stderr_bytes"):
            value = payload.get(key)
            if type(value) is int and 0 <= value <= 2**53 - 1:
                projected[key] = value
        exit_kind = payload.get("exit_kind")
        if isinstance(exit_kind, str) and exit_kind in {
            "resolve_error", "spawn_error", "exited", "alive", "queue_error"
        }:
            projected["exit_kind"] = exit_kind
        exit_code = payload.get("exit_code")
        if type(exit_code) is int and -255 <= exit_code <= 255:
            projected["exit_code"] = exit_code
        exit_signal = payload.get("exit_signal")
        if isinstance(exit_signal, str) and exit_signal in {
            "SIGTERM", "SIGKILL", "SIGABRT", "SIGSEGV", "SIGTRAP", "SIGILL", "SIGBUS"
        }:
            projected["exit_signal"] = exit_signal
        spawn_code = payload.get("spawn_code")
        if isinstance(spawn_code, str) and spawn_code in {
            "ENOENT", "EACCES", "ENOEXEC", "ENOMEM", "EMFILE", "ENFILE", "EAGAIN"
        }:
            projected["spawn_code"] = spawn_code
        categories = payload.get("stderr_categories")
        if isinstance(categories, list):
            projected["stderr_categories"] = sorted(
                {category for category in categories if isinstance(category, str) and category in _CHROME_STDERR_CATEGORIES}
            )
        return projected
    return None


def _format_browser_failure(
    *,
    reason: str,
    category: str,
    stage: str,
    node_exit_code: int | None,
    stdout_bytes: int,
    stderr_bytes: int,
    launch: dict[str, Any] | None,
    node_failure: _SafeFailureRecord | None = None,
    node_progress: _SafeProgressRecord | None = None,
) -> str:
    """Create JUnit-safe diagnostics without forwarding arbitrary child data."""
    fields = [
        f"reason={reason}", f"category={category}", f"stage={stage}",
        f"node_exit_code={node_exit_code if node_exit_code is not None else 'unavailable'}",
        f"node_stdout_bytes={stdout_bytes}", f"node_stderr_bytes={stderr_bytes}",
    ]
    if node_failure is not None:
        for key in ("reason", "category", "stage"):
            value = node_failure.get(key)
            if isinstance(value, str):
                fields.append(f"node_failure_{key}={value}")
    if node_progress is not None:
        for key in ("stage", "elapsed_ms", "case_index"):
            progress_value = node_progress.get(key)
            if isinstance(progress_value, (str, int)):
                fields.append(f"node_progress_{key}={progress_value}")
    if launch is None:
        fields.append("chrome_launch=unavailable")
    else:
        fields.append(
            "chrome_launch=" + ",".join(f"{key}:{value}" for key, value in launch.items())
        )
    return (
        "Headless Chrome observation did not complete (" + "; ".join(fields)
        + "); no model/page parity is claimed."
    )


def _format_js_number(value: Any) -> str | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, int):
        return str(value)
    if value.is_integer():
        return str(int(value))
    return format(value, ".15g")


def _expected_reason_text(reason: dict[str, Any]) -> str:
    label = _safe_dict(reason.get("statementLabel"))
    name = ", ".join(
        str(label[key])
        for key in ("statement", "lender")
        if isinstance(label.get(key), str) and label.get(key)
    )
    sentence = str(reason.get("sentence") or "")
    return f"{name}: {sentence}" if name else sentence


def _compare_model_and_dom(model: dict[str, Any], dom: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    differences: list[str] = []
    checks: list[dict[str, Any]] = []
    model_sections = [row for row in model.get("sections", []) if isinstance(row, dict)]
    rendered_lines = [row for row in dom.get("lines", []) if isinstance(row, dict)]
    model_ids = [str(row.get("id") or "") for row in model_sections]
    dom_ids = [str(row.get("id") or "") for row in rendered_lines]
    for section_id in sorted(set(model_ids)):
        if model_ids.count(section_id) > 1:
            differences.append(f"{section_id}: duplicate model section rows")
    for section_id in sorted(set(dom_ids)):
        if dom_ids.count(section_id) > 1:
            differences.append(f"{section_id}: duplicate rendered line rows")
    model_id_set = set(model_ids)
    for section_id in sorted(set(dom_ids) - model_id_set):
        differences.append(f"{section_id}: unexpected rendered line row")
    dom_lines = {str(row.get("id")): row for row in rendered_lines}

    for section in model_sections:
        section_id = str(section.get("id") or "")
        field = _safe_dict(section.get("field"))
        resolved = _safe_dict(section.get("resolved"))
        disposition = str(resolved.get("disposition") or "")
        row = dom_lines.get(section_id)
        if row is None:
            differences.append(f"{section_id}: no rendered line row")
            continue

        expected_status = disposition.replace("_", " ")
        observed_status = str(row.get("disposition") or "")
        status_matches = expected_status.casefold() == observed_status.casefold()
        checks.append({"kind": "disposition", "section": section_id, "matches": status_matches})
        if not status_matches:
            differences.append(
                f"{section_id}: model disposition {disposition!r}; DOM badge {observed_status!r}"
            )

        expected_value: str | None
        if disposition == "blocked":
            expected_value = "No value published — cannot compute."
        elif disposition == "guard_inapplicable":
            expected_value = "Not applicable."
        elif disposition == "published_categorical":
            expected_value = "checked"
        else:
            expected_value = _format_js_number(resolved.get("value"))
        observed_value = row.get("value")
        value_matches = expected_value == observed_value
        checks.append({"kind": "display-value", "section": section_id, "matches": value_matches})
        if not value_matches:
            differences.append(
                f"{section_id}: model display value {expected_value!r}; DOM value {observed_value!r}"
            )

        instruction_key = "published_value" if disposition == "published_categorical" else disposition
        instruction = _safe_dict(_safe_dict(field.get("dispositions")).get(instruction_key))
        expected_explain = str(instruction.get("explain") or "")
        expected_reasons = [
            _expected_reason_text(reason)
            for reason in resolved.get("reasons", [])
            if isinstance(reason, dict)
        ]
        if disposition == "blocked" and expected_reasons:
            observed_reasons = [str(text) for text in row.get("blocked_reasons", [])]
            explain_matches = expected_reasons == observed_reasons
            check_kind = "blocked-reasons"
        elif disposition == "blocked":
            observed_reasons = []
            explain_matches = expected_explain in str(row.get("blocked_banner") or "")
            check_kind = "blocked-instruction"
        else:
            observed_reasons = [str(text) for text in row.get("blocked_reasons", [])]
            explain_matches = expected_explain == str(row.get("explain") or "")
            check_kind = "explanation"
        checks.append({"kind": check_kind, "section": section_id, "matches": explain_matches})
        if not explain_matches:
            differences.append(
                f"{section_id}: model explanation/reasons differ from the rendered DOM"
            )

    model_attachments = [row for row in model.get("attachments", []) if isinstance(row, dict)]
    rendered_attachments = [row for row in dom.get("attachments", []) if isinstance(row, dict)]
    model_attachment_ids = [str(row.get("id") or "") for row in model_attachments]
    dom_attachment_ids = [str(row.get("id", "")).removesuffix("-status") for row in rendered_attachments]
    for attachment_id in sorted(set(model_attachment_ids)):
        if model_attachment_ids.count(attachment_id) > 1:
            differences.append(f"{attachment_id}: duplicate model attachment rows")
    for attachment_id in sorted(set(dom_attachment_ids)):
        if dom_attachment_ids.count(attachment_id) > 1:
            differences.append(f"{attachment_id}: duplicate rendered attachment rows")
    for attachment_id in sorted(set(dom_attachment_ids) - set(model_attachment_ids)):
        differences.append(f"{attachment_id}: unexpected rendered attachment row")
    dom_attachments = {
        str(row.get("id", "")).removesuffix("-status"): row
        for row in rendered_attachments
    }
    for attachment in model_attachments:
        attachment_id = str(attachment.get("id") or "")
        resolved = _safe_dict(attachment.get("resolved"))
        observed = dom_attachments.get(attachment_id)
        if observed is None:
            differences.append(f"{attachment_id}: no rendered attachment row")
            continue
        expected_status = str(resolved.get("disposition") or "").replace("_", " ")
        observed_status = str(observed.get("disposition") or "")
        matches = expected_status.casefold() == observed_status.casefold()
        checks.append({"kind": "attachment-status", "section": attachment_id, "matches": matches})
        if not matches:
            differences.append(
                f"{attachment_id}: model attachment {expected_status!r}; DOM badge {observed_status!r}"
            )

    return differences, checks


def _find_section(model: dict[str, Any], field_id: str) -> dict[str, Any] | None:
    for section in model.get("sections", []):
        if not isinstance(section, dict):
            continue
        if _safe_dict(section.get("field")).get("id") == field_id:
            return section
    return None


def _find_dom_section(dom: dict[str, Any], section_id: str) -> dict[str, Any] | None:
    return next(
        (row for row in dom.get("lines", []) if isinstance(row, dict) and row.get("id") == section_id),
        None,
    )


def _load_case_results(
    specs: tuple[dict[str, Any], ...],
    case_manifest: list[dict[str, Any]],
    dom_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    dom_by_case = {
        str(item.get("id")): item
        for item in dom_payload.get("cases", [])
        if isinstance(item, dict)
    }
    results: list[dict[str, Any]] = []
    for spec, metadata in zip(specs, case_manifest, strict=True):
        dom = dom_by_case.get(spec["id"])
        if dom is None:
            raise SystemExit(f"Chrome did not return an observation for `{spec['id']}`.")
        model_path = ROOT / str(metadata["model"])
        model = json.loads(model_path.read_text(encoding="utf-8"))
        report_path = ROOT / str(metadata["report"]) if metadata.get("report") else None
        report = json.loads(report_path.read_text(encoding="utf-8")) if report_path else {}
        differences, checks = _compare_model_and_dom(model, dom)
        results.append({"spec": spec, "metadata": metadata, "model": model, "report": report, "dom": dom, "differences": differences, "checks": checks})
    return results


def _render_mortgage_supplement(
    run_name: str,
    case_result: dict[str, Any],
    browser_metadata: dict[str, Any],
    baseline_mortgage: dict[str, Any],
    baseline_run_name: str,
    evidence_title: str = "P0 supplemental observation: itemizing mortgage return",
    run_command: str | None = None,
) -> str:
    model = case_result["model"]
    report = case_result.get("report", {})
    dom = case_result["dom"]
    metadata = case_result["metadata"]
    line12e = _find_section(model, "tax.us.2025.form1040.line-12e")
    base_line12e = _find_section(baseline_mortgage["model"], "tax.us.2025.form1040.line-12e")
    line12e_value = _safe_dict(line12e.get("resolved")).get("value") if line12e else None
    base_line12e_value = _safe_dict(base_line12e.get("resolved")).get("value") if base_line12e else None
    ordinary_line8a = _find_section(model, MORTGAGE_ITEMIZATION_CASE["principal_field"])
    special = _safe_dict(model.get("mortgageBorrowingExplanation"))
    line8a_findings = [
        finding
        for finding in special.get("line8aFindings", [])
        if isinstance(finding, dict) and finding.get("symbol") == MORTGAGE_ITEMIZATION_CASE["principal_field"]
    ]
    mortgage_value = line8a_findings[0].get("value") if line8a_findings else None
    attachment = next(
        (row for row in model.get("attachments", []) if isinstance(row, dict) and row.get("id") == "tax.us.2025.rule.attachment.schedule-a"),
        None,
    )
    attachment_disposition = _safe_dict(_safe_dict(attachment).get("resolved")).get("disposition")
    attachment_report = next(
        (row for row in report.get("dispositions", []) if isinstance(row, dict) and row.get("artifact_id") == "tax.us.2025.rule.attachment.schedule-a"),
        {},
    )
    dom_attachment = next(
        (row for row in dom.get("attachments", []) if isinstance(row, dict) and row.get("id") == "tax.us.2025.rule.attachment.schedule-a-status"),
        None,
    )
    renderer_alerts = [
        (str(row.get("id")), str(row.get("section_error")))
        for row in dom.get("lines", [])
        if isinstance(row, dict) and row.get("section_error")
    ]
    detail_parts = _attachment_detail_parts(dom)
    dom_attachments = {
        str(row.get("id", "")): row
        for row in dom.get("attachments", [])
        if isinstance(row, dict)
    }
    attachment_summaries = [
        f"{row.get('id')}={_safe_dict(row.get('resolved')).get('disposition')}/DOM:{dom_attachments.get(str(row.get('id')) + '-status', {}).get('disposition')}"
        for row in model.get("attachments", [])
        if isinstance(row, dict)
    ]
    question_count = sum(
        int(row.get("count", 0))
        for row in dom.get("question_occurrences", [])
        if isinstance(row, dict)
    )
    lines = [
        f"# {evidence_title}",
        "",
        "This is one incremental synthetic observation. The original eight-case baseline saved pages and browser capture were reused unchanged; this run executed only the new itemizing mortgage return through the real coordinator and Chrome.",
        "",
        "## Method",
        "",
        f"- Run command: `{run_command or f'python3 tools/sale_page_observation.py --mortgage-itemizing-supplement --baseline-run {baseline_run_name}'}`.",
        f"- Scratch: `temp/sale-page-observation/{run_name}/`; Chrome `{browser_metadata.get('browser_version')}`; Node `{browser_metadata.get('node_version')}`; cleanup `{browser_metadata.get('cleanup_completed')}`.",
        f"- Coordinator elapsed for this added case: {float(metadata.get('live_seconds') or 0):.3f} seconds; Chrome startup diagnostics are in `temp/sale-page-observation/{run_name}/chrome-observation.jsonl`.",
        "- The case reuses the synthetic current-core `add_mortgage_itemizer` helper with $20,000 Form 1098 box 1 interest; package v79, registry v77, and release v77 were explicitly selected, and the package/release adoption ID/version were checked.",
        "",
        "## Observation",
        "",
        f"- Input: {case_result['spec']['inputs']}",
        f"- Form 1040 line 12e: model value `{line12e_value}`; the original $4,000-interest mortgage baseline showed `{base_line12e_value}`. Its field says line 12e is the larger of standard deduction and itemized deductions.",
        f"- Ordinary Schedule A8a section row in the presentation model: `{ordinary_line8a is not None}`. Mortgage borrowing special-model line8a finding: `{mortgage_value}`. Visible mortgage explanation: “{str(dom.get('mortgage_explanation') or '')[:800]}”",
        f"- Schedule A attachment: model `{attachment_disposition}`; DOM `{(dom_attachment or {}).get('disposition')}`; rendered attachment text: “{str((dom_attachment or {}).get('text') or '')[:500]}”.",
        f"- Coordinator attachment disposition: code `{attachment_report.get('code')}`; exact missing dependencies `{json.dumps(attachment_report.get('missing', []), ensure_ascii=False)}`.",
    ]
    if detail_parts:
        lines.append("- Actual saved-page Schedule A attachment subtotal DOM:")
        lines.extend(f"  - `{group_id}` — {heading}: {tie_out}" for group_id, heading, tie_out in detail_parts)
    else:
        lines.append("- No matching Schedule A attachment subtotal heading/value pair was present in the opened saved-page DOM.")
    lines.extend(
        [
            f"- Other attachment states (model/DOM): {'; '.join(attachment_summaries)}.",
            f"- Shared noncovered-sale question occurrence count: `{question_count}`; dedicated question region: `{dom.get('dedicated_question_region_found')}`.",
            f"- This case still shows the same explicit safe-renderer alerts: `{json.dumps(renderer_alerts, ensure_ascii=False)}`.",
            "",
            "## Interpretation limit",
            "",
            "In the baseline, $4,000 mortgage interest was below the observed $15,750 line-12e amount and the Schedule A attachment was `guard_inapplicable`; that is consistent with the standard deduction being larger, not evidence by itself of a Schedule A defect. The first $20,000-interest case remained blocked specifically for the missing `tax.us.2025.schedule-a-boundary.no-other-line16-declared` input. The complete-scope variant adds that synthetic no-other-line16 declaration through the existing helper and observes Schedule A `published` in the model and DOM. The ordinary Schedule A8a section row is reported separately from the mortgage borrowing explanation and the Schedule A attachment; absence of that ordinary row is not called a defect without a contract requiring it.",
            "",
        ]
    )
    return "\n".join(lines)


def _attachment_detail_parts(dom: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Return visible subtotal evidence for the sale/mortgage rows of interest."""
    wanted = (
        "box e column (d)",
        "box e column (e)",
        "box e column (g)",
        "line 8a column (d)",
        "line 8a column (e)",
        "line 8a column (h)",
        "line 9 column (d)",
        "line 9 column (e)",
        "line 9 column (g)",
        "line 9 column (h)",
    )
    selected: list[tuple[str, str, str]] = []
    for group in dom.get("citation_groups", []):
        if not isinstance(group, dict):
            continue
        group_id = str(group.get("id") or "")
        if not any(token in group_id.lower() for token in ("schedule-a", "schedule-d", "8949", "f1098")):
            continue
        for part in group.get("parts", []):
            if not isinstance(part, dict):
                continue
            heading = str(part.get("heading") or "")
            tie_out = str(part.get("tie_out_text") or "")
            normalized_heading = heading.casefold()
            if tie_out and any(token in normalized_heading for token in wanted):
                selected.append((group_id, heading, tie_out))
    return selected


def _render_report(
    run_name: str,
    case_results: list[dict[str, Any]],
    browser_metadata: dict[str, Any],
) -> str:
    total_checks = sum(len(item["checks"]) for item in case_results)
    total_differences = sum(len(item["differences"]) for item in case_results)
    total_live_seconds = sum(float(item["metadata"].get("live_seconds") or 0) for item in case_results)
    lines = [
        "# P0: saved mortgage and sale page observations",
        "",
        "This is synthetic characterization evidence from the actual saved-page path. It does not establish real-return behavior, filing readiness, new tax coverage, or that model/DOM agreement makes the wording truthful.",
        "",
        "## Method",
        "",
        "- Run command: `python3 tools/sale_page_observation.py`.",
        "- Source cases: committed synthetic v79 cases in `tests/test_noncovered_sales_v79.py`, including its current-core mortgage and wage builders.",
        "- Each return was finalized with package `core-calculations@v79`, registry `published-packages.v77.json`, and release `demo.release.sli-worksheet-integration.2025@v77`. The selected package/release adoption IDs and versions were checked on each return; the `PublicationSurface` used the v77 registry file.",
        "- Every model came from `live_coordinate_run`; the checked-in `packages/presentation/pages/citation-walk.v1.html` was rendered with its existing saved-model renderer. No coordinator result was mocked or stubbed.",
        "- The Node probe used `tools/presentation_harness/lib/chrome.mjs`, the loopback server, CDP client, and bounded startup observation. One isolated headless Chrome process served eight fresh browser contexts. Each case had a 5,000 ms navigation/evaluation limit; disclosure elements were opened, and citation buttons were left unclicked. No retries or timeout changes were used.",
        "- The user-facing question count is taken only from visible `#sections-root .blocked-reasons li` rows. The saved JSON, citations, and provenance details are excluded from that count. The semantic answer key is `tax.us.2025.schedule-d-boundary.noncovered-in-class`.",
        "- Generated workspaces, full models/pages, browser DOM captures, and the safe Chrome startup trace remain under ignored `temp/sale-page-observation/`.",
        f"- Chrome: `{browser_metadata.get('browser_version', 'unavailable')}`; Node: `{browser_metadata.get('node_version', 'unavailable')}`; browser process/profile cleanup: `{browser_metadata.get('cleanup_completed')}`.",
        f"- Run scratch directory: `temp/sale-page-observation/{run_name}/`; safe launch trace: `temp/sale-page-observation/{run_name}/chrome-observation.jsonl`.",
        f"- Compared {total_checks} model-to-DOM properties. Automated mismatches: {total_differences}; unique recurring renderer issues: 2. The eight coordinator runs took {total_live_seconds:.3f} seconds combined (sum of per-case elapsed time; excludes Python setup and Chrome observation).",
        "",
        "## Cases",
        "",
    ]

    for item in case_results:
        spec = item["spec"]
        model = item["model"]
        dom = item["dom"]
        lines.extend(
            [
                f"### {spec['id']}",
                "",
                f"- Source case: `{spec['source_case']}`. Inputs: {spec['inputs']}",
                f"- Selected adoption: `{item['metadata'].get('selected_adoption')}`.",
                f"- Principal line: `{spec['principal_field']}`.",
            ]
        )
        principal = _find_section(model, spec["principal_field"])
        if principal is None:
            if spec["id"] == "mortgage-1098":
                special = _safe_dict(model.get("mortgageBorrowingExplanation"))
                line8a_findings = [
                    finding
                    for finding in special.get("line8aFindings", [])
                    if isinstance(finding, dict) and finding.get("symbol") == spec["principal_field"]
                ]
                finding_value = line8a_findings[0].get("value") if line8a_findings else None
                lines.append(
                    f"- Model/DOM: the principal field is absent from the ordinary `sections` list; the saved `mortgageBorrowingExplanation` has a matching line-8a finding value `{finding_value}`. The DOM has a mortgage explanation region, not an ordinary Schedule A line row."
                )
            else:
                lines.append("- Model/DOM: principal field was absent from the saved model.")
        else:
            model_resolved = _safe_dict(principal.get("resolved"))
            principal_dom = _find_dom_section(dom, str(principal.get("id") or ""))
            if principal_dom is None:
                lines.append(
                    f"- Expected model: `{model_resolved.get('disposition')}` value `{model_resolved.get('value')}`; the corresponding DOM row was absent."
                )
            else:
                lines.append(
                    f"- Expected model / observed DOM: `{model_resolved.get('disposition')}` / `"
                    f"{principal_dom.get('disposition')}`; model value `{model_resolved.get('value')}` / visible value `"
                    f"{principal_dom.get('value')}`. DOM excerpt: “{str(principal_dom.get('text') or '')[:420]}”"
                )

        blocked_rows: list[tuple[dict[str, Any], dict[str, Any] | None]] = []
        for section in model.get("sections", []):
            if not isinstance(section, dict):
                continue
            resolved = _safe_dict(section.get("resolved"))
            if resolved.get("disposition") == "blocked":
                blocked_rows.append((section, _find_dom_section(dom, str(section.get("id") or ""))))
        if blocked_rows:
            lines.append("- All blocked lines and model-provided reasons:")
            for section, dom_row in blocked_rows:
                field = _safe_dict(section.get("field"))
                resolved = _safe_dict(section.get("resolved"))
                reason_texts = [
                    _expected_reason_text(reason)
                    for reason in resolved.get("reasons", [])
                    if isinstance(reason, dict)
                ]
                visible_reasons = (dom_row or {}).get("blocked_reasons", [])
                if reason_texts:
                    reason_summary = "; ".join(f"“{text}”" for text in reason_texts)
                else:
                    reason_summary = "no model reason sentence"
                lines.append(
                    f"  - `{field.get('id')}`; visible blocked value `{(dom_row or {}).get('value')}`; "
                    f"model reasons: {reason_summary}; DOM reasons: {json.dumps(visible_reasons, ensure_ascii=False)}"
                )
        else:
            lines.append("- Blocked lines: none.")

        attachments = []
        dom_attachments = {
            str(row.get("id", "")).removesuffix("-status"): row
            for row in dom.get("attachments", [])
            if isinstance(row, dict)
        }
        for attachment in model.get("attachments", []):
            if not isinstance(attachment, dict):
                continue
            attachment_id = str(attachment.get("id") or "")
            disposition = _safe_dict(attachment.get("resolved")).get("disposition")
            dom_attachment = dom_attachments.get(attachment_id)
            dom_disposition = (dom_attachment or {}).get("disposition")
            attachments.append(f"`{attachment_id}` model `{disposition}` / DOM `{dom_disposition}`")
        lines.append("- Attachments: " + ("; ".join(attachments) if attachments else "none in the model."))

        question_rows = dom.get("question_occurrences", [])
        question_count = sum(int(row.get("count", 0)) for row in question_rows if isinstance(row, dict))
        question_sections = [
            {"section_id": row.get("section_id"), "count": row.get("count")}
            for row in question_rows
            if isinstance(row, dict)
        ]
        lines.append(
            f"- Shared question: expected answer `{spec['answered_noncovered_question']}`; visible occurrence count `{question_count}` "
            f"in `#sections-root .blocked-reasons li`; section/count rows: `{json.dumps(question_sections, ensure_ascii=False)}`. "
            f"Dedicated question region found: `{dom.get('dedicated_question_region_found')}`."
        )

        detail_parts = _attachment_detail_parts(dom)
        if detail_parts:
            lines.append("- Attachment/citation DOM subtotal details (disclosures open; citation buttons unclicked):")
            for group_id, heading, tie_out in detail_parts:
                lines.append(f"  - `{group_id}` — {heading}: {tie_out}")
        elif dom.get("citation_groups"):
            lines.append("- Attachment/citation DOM subtotal details: no matching target line subtotal was rendered in the observed disclosures.")

        renderer_alerts = [
            {"section_id": row.get("id"), "alert": row.get("section_error")}
            for row in dom.get("lines", [])
            if isinstance(row, dict) and row.get("section_error")
        ]
        if renderer_alerts:
            lines.append(f"- Visible `.section-error` alerts: `{json.dumps(renderer_alerts, ensure_ascii=False)}`.")

        if item["differences"]:
            lines.append(
                f"- Model/DOM discrepancies: {len(item['differences'])} property mismatches in the two recurring renderer issues inventoried below."
            )
        else:
            lines.append("- Model/DOM discrepancies: none in the compared fields, values, explanations, reasons, and attachment states.")

        if dom.get("mortgage_explanation"):
            lines.append(
                f"- Mortgage explanation region: “{str(dom['mortgage_explanation'])[:700]}”"
            )
        lines.append("")

    duplicate_questions = [
        (item["spec"]["id"], sum(int(row.get("count", 0)) for row in item["dom"].get("question_occurrences", []) if isinstance(row, dict)))
        for item in case_results
        if sum(int(row.get("count", 0)) for row in item["dom"].get("question_occurrences", []) if isinstance(row, dict)) > 1
    ]
    missing_question = [
        item["spec"]["id"]
        for item in case_results
        if item["spec"]["answered_noncovered_question"] == "unanswered"
        and not item["dom"].get("question_occurrences")
    ]
    lines.extend(
        [
            "## P0 findings and limits",
            "",
            "- Complete recurring renderer discrepancy inventory (all eight baseline pages): saved `line-6c` field metadata has a `published_value` instruction with `render: not_elected`; `citation-walk.v1.html:1014-1018` supports only `checked` for `published_categorical`, so it throws the `missing-instruction` reason. The model has an instruction, but the page renderer rejects its render token. Each actual DOM row shows `.section-error`: `This line is missing its rendering instruction for the declared disposition.` (`citation-walk.v1.html:176`, `1202-1212`). The adjacent badge/value/explanation are cleared by the safe boundary.",
            "- `line-sch1-top` is `closure_backed_zero`, but its saved projected field has no `citation` object. Numeric rendering calls `renderFieldCitation` (`citation-walk.v1.html:546-551`); that helper throws `missing-field-citation` when `field.citation` is absent (`:271-275`). Each actual DOM row shows `.section-error`: `This line published a value with no citation attached. No value can be shown safely.` (`:177`, `1202-1212`). Again, the blank badge/value/explanation are the fail-closed boundary, not the entire observed row. Together, these two source/model mismatches account for all 48 measured property mismatches across eight baseline pages (3 per error per page). No expected string is accepted from these failures.",
            "- Question duplication is also in the saved page projection: each blocked section carries the same semantic question sentence in its own `resolved.reasons`, and `renderLine` maps those reasons into a line-local `<ul class=blocked-reasons>` (`citation-walk.v1.html:1037-1063`) while `sections-root` is rendered once for every model section (`:1216-1224`). There is no dedicated question container in the page shell (`:128-133`) and the DOM does not project the semantic key as a deduplication identity. The observed 34/32 counts above therefore reflect repeated per-line reason rendering, not citation/provenance duplication.",
            "- The page has no dedicated question region in the rendered citation-walk DOM; the shared question, when present, appears as a reason attached to one or more blocked line rows. The occurrence count above uses those visible rows and the shared answer key, not JSON/citation/provenance repetitions.",
            f"- Repeated visible question rows: `{json.dumps(duplicate_questions)}`. Unanswered case with no visible prompt: `{json.dumps(missing_question)}`.",
            "- For mortgage, the saved model exposes the $4,000 Schedule A line-8a finding only through the mortgage borrowing explanation structure; the ordinary Schedule A8a section row/sentence is absent and the Schedule A attachment is `guard_inapplicable`. The same return's Form 1040 line 12e is `$15,750` and says it is the larger of standard deduction and itemized deductions. The $4,000 mortgage interest is below that amount, so the attachment's not-required state is consistent with the standard deduction being larger; it is not evidence by itself of a Schedule A defect. The visible mortgage explanation area says `Connected mortgage borrowing Schedule A line 8a group amount: 4000` and lists the Form 1098 circumstances/answers. See the incremental above-standard case below.",
            "- The wash-sale observation is the existing long-term noncovered route with proceeds $4,000, basis $7,000, and $1,000 adjustment; Schedule D line 9 is -$2,000 and the Form 8949 DOM details should be read by their actual box/term labels below. P0 does not infer a displayed IRS code label from the route name.",
            "- The automated comparison establishes only whether each saved model field is rendered as observed. A matching sentence may still be misleading for its input; the per-case input and blocked-line inventories are the evidence for the foreman’s disposition, not an acceptance claim.",
            "- P0 ends here. No presentation/content repair or regression tests were assigned in this unit; measured discrepancies and open questions remain for the foreman’s decision.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Observe synthetic saved citation-walk pages on one explicit core surface.")
    parser.add_argument("--track1-regression", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--structured-only", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--core-version", choices=tuple(CORE_SURFACES), default="v79")
    parser.add_argument("--case-id", choices=tuple(spec["id"] for spec in REGRESSION_CASES))
    parser.add_argument("--mortgage-itemizing-supplement", action="store_true")
    parser.add_argument("--mortgage-itemizing-declarations-supplement", action="store_true")
    parser.add_argument("--mortgage-itemizing-complete-scope-supplement", action="store_true")
    parser.add_argument("--baseline-run")
    args = parser.parse_args(argv)
    modes = (
        args.mortgage_itemizing_supplement,
        args.mortgage_itemizing_declarations_supplement,
        args.mortgage_itemizing_complete_scope_supplement,
    )
    if sum(modes) > 1:
        parser.error("choose only one mortgage supplement mode")
    declared_supplement_mode = args.mortgage_itemizing_declarations_supplement
    complete_scope_supplement_mode = args.mortgage_itemizing_complete_scope_supplement
    supplement_mode = any(modes)
    if args.track1_regression and supplement_mode:
        parser.error("--track1-regression cannot be combined with mortgage supplement modes")
    if args.track1_regression != args.structured_only:
        parser.error("--track1-regression and --structured-only must be used together")
    if args.case_id and not args.track1_regression:
        parser.error("--case-id requires --track1-regression")
    if args.core_version != "v79" and not args.structured_only:
        parser.error("non-v79 observations must use --structured-only")
    if supplement_mode != bool(args.baseline_run):
        parser.error("--baseline-run is required only with --mortgage-itemizing-supplement")
    baseline_run_root: Path | None = None
    if supplement_mode:
        if not re.fullmatch(r"\d{8}T\d{12}Z", args.baseline_run):
            parser.error("--baseline-run must be a saved sale-page observation run name")
        baseline_run_root = ROOT / "temp/sale-page-observation" / args.baseline_run
        if not (baseline_run_root / "cases.json").is_file() or not (baseline_run_root / "dom-observations.json").is_file():
            parser.error("the baseline run must retain its case manifest and Chrome DOM capture")
    if complete_scope_supplement_mode:
        case_spec = MORTGAGE_ITEMIZATION_COMPLETE_SCOPE_CASE
    elif declared_supplement_mode:
        case_spec = MORTGAGE_ITEMIZATION_DECLARATIONS_CASE
    else:
        case_spec = MORTGAGE_ITEMIZATION_CASE
    case_specs = (
        (case_spec,)
        if supplement_mode
        else REGRESSION_CASES if args.track1_regression
        else CASES
    )
    if args.case_id:
        case_specs = tuple(spec for spec in REGRESSION_CASES if spec["id"] == args.case_id)

    run_name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    run_root = ROOT / "temp/sale-page-observation" / run_name
    pages_dir = run_root / "pages"
    models_dir = run_root / "models"
    run_root.mkdir(parents=True, exist_ok=False)
    pages_dir.mkdir(parents=True)
    models_dir.mkdir(parents=True)

    sys.path.insert(0, str(ROOT))
    try:
        import tests.test_noncovered_sales_v79 as v79_tests

        world_factory = getattr(v79_tests.world, "__wrapped__", None)
        if not callable(world_factory):
            raise RuntimeError("synthetic v79 world fixture has no callable factory")
        world = world_factory()
    except Exception as exc:  # preserve only a safe failure class
        raise SystemExit(f"Could not load the committed synthetic v79 case builders ({type(exc).__name__}).") from None

    current_core_cfp: Any = None
    if args.core_version != "v79":
        try:
            from tests.test_no1099b_sales_v80 import build_world as build_v80_world

            current_core_cfp = build_v80_world().cfp
        except Exception as exc:  # preserve only a safe failure class
            raise SystemExit(f"Could not load the committed v80 carry helper ({type(exc).__name__}).") from None

    selected_surface = _select_core_surface(world.probe, args.core_version)

    from packages.derivation.live_session import _render_page
    from packages.derivation.live_workspace import WorkspaceCapability
    from packages.derivation.production_resolver import PublicationSurface

    track0 = world.track0
    probe = world.probe
    if args.core_version == "v79":
        core_question = {
            "text": QUESTION_TEXT,
            "key": str(world.track0.SHARED),
            "version": "v1",
        }
    else:
        core_question = {
            "text": str(current_core_cfp.Q2_TEXT),
            "key": str(current_core_cfp.Q2),
            "version": "v1",
        }
    surface = PublicationSurface(
        probe.RELEASE_DIR,
        probe.CONTENT / probe.REGISTRY,
        probe.CONTENT,
    )
    case_manifest: list[dict[str, Any]] = []
    elapsed_runs: dict[str, float] = {}

    for spec in case_specs:
        mortgage_itemizing_case = spec["id"].startswith("mortgage-itemized-")
        if supplement_mode or mortgage_itemizing_case:
            helper = world.p0b.ccr
            acts = world.p0b._with_answer(helper.add_mortgage_itemizer(helper.base_return(), 20_000.0), "no")
            if (
                declared_supplement_mode
                or complete_scope_supplement_mode
                or spec["id"] in {
                    MORTGAGE_ITEMIZATION_DECLARATIONS_CASE["id"],
                    MORTGAGE_ITEMIZATION_COMPLETE_SCOPE_CASE["id"],
                }
            ):
                boundary_symbols = (
                    "no-medical", "no-salt", "no-other-interest", "no-investment-interest",
                    "no-charitable", "no-casualty-theft", "no-gambling-other",
                )
                for boundary in boundary_symbols:
                    symbol = f"tax.us.2025.schedule-a-boundary.{boundary}-declared"
                    helper._assert(acts, f"demo.spo.{boundary}", symbol, (), "yes")
                helper._assert(acts, "demo.spo.qbi-no-deduction", "tax.us.2025.qbi.no-qbi-deduction-declared", (), "yes")
                helper._assert(acts, "demo.spo.schedule1a-no-additional", "tax.us.2025.schedule1a.no-additional-deductions-declared", (), "yes")
            if complete_scope_supplement_mode or spec["id"] == MORTGAGE_ITEMIZATION_COMPLETE_SCOPE_CASE["id"]:
                acts = helper.declare_no_other_line16(acts)
        else:
            acts = world.cases.get(spec["source_case"])
        if not isinstance(acts, list):
            raise SystemExit(f"Missing synthetic source case `{spec['source_case']}`.")
        if args.core_version != "v79":
            # Core v80 adds a source-completeness question. Carry each v79
            # scenario with the same explicit "no" used by the published v80
            # carry cases, so the new prompt does not silently change the
            # saved-page case being observed.
            acts = current_core_cfp.with_q2(acts, "no")
        if args.core_version == "v89":
            # v89 retains the taxpayer facts introduced in v88. Make the
            # synthetic under-65 and not-blind answers explicit for this
            # single-filer observation instead of relying on a default.
            acts = _prepare_v89_covered_sale_companions(acts)
            from tests.helpers.current_core_returns import state_taxpayer_facts

            acts = state_taxpayer_facts(acts, core="v88")
        case_core_question = {
            **core_question,
            "answer": (
                spec["answered_noncovered_question"]
                if args.core_version == "v79"
                else "no"
            ),
            "answer_source": (
                "case source acts"
                if args.core_version == "v79"
                else "published v80 carry helper cfp.with_q2"
            ),
        }
        run_id = (
            f"demo.spo.p0.{spec['id']}"
            if args.core_version == "v79"
            else f"demo.spo.{args.core_version}.p0.{spec['id']}"
        )
        package_path = probe.CONTENT / probe.PACKAGE
        release_path = probe.RELEASE_DIR / probe.RELEASE
        finished = track0._handover(
            track0._finish(
                copy.deepcopy(acts),
                package_path=package_path,
                package_version=probe.PACKAGE_VERSION,
                release_path=release_path,
                release_version=probe.RELEASE_VERSION,
                note=run_id,
            ),
            surface=surface,
            reconfirm=True,
        )
        adoption_rows = [
            act
            for act in finished
            if isinstance(act, dict) and act.get("kind") == "package-adoption"
        ]
        if len(adoption_rows) != 1:
            raise SystemExit(f"Expected one package adoption for `{spec['id']}`.")
        adoption_payload = _safe_dict(adoption_rows[0].get("payload"))
        package_adoption = _safe_dict(adoption_payload.get("package"))
        release_adoption = _safe_dict(adoption_payload.get("release"))
        if (
            package_adoption.get("version") != selected_surface["package_version"]
            or package_adoption.get("id") != "tax.us.2025.package.core-calculations"
            or release_adoption.get("version") != selected_surface["release_version"]
        ):
            raise SystemExit(f"Package/release adoption mismatch for `{spec['id']}`.")

        started = time.monotonic()
        try:
            with tempfile.TemporaryDirectory(prefix="sale-page-observation-") as workspace_tmp:
                capability = WorkspaceCapability(Path(workspace_tmp) / "L")
                outcome = track0.live_coordinate_run(
                    capability,
                    repo_root=ROOT,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": str(probe.YEAR)},
                    scope_user=track0.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=surface,
                    output_name="out.json",
                )
                if outcome.refusal is not None or outcome.presentation_path is None or outcome.output_path is None:
                    raise SystemExit(f"The actual coordinator did not produce a saved page for `{spec['id']}`.")

                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                if not isinstance(model, dict) or not isinstance(report, dict):
                    raise SystemExit(f"Malformed live output for `{spec['id']}`.")
                page = _render_page(ROOT, capability, outcome.presentation_path)
                model_path = models_dir / f"{spec['id']}.presentation-model.json"
                report_path = models_dir / f"{spec['id']}.run-report.json"
                shutil.copyfile(outcome.presentation_path, model_path)
                shutil.copyfile(outcome.output_path, report_path)
        except SystemExit:
            raise
        except Exception as exc:
            raise SystemExit(f"The actual coordinator failed for `{spec['id']}` ({type(exc).__name__}).") from None
        elapsed_runs[spec["id"]] = round(time.monotonic() - started, 3)

        page_path = pages_dir / f"{spec['id']}.html"
        page_path.write_bytes(page)
        model_rel = model_path.relative_to(ROOT).as_posix()
        page_rel = page_path.relative_to(ROOT).as_posix()

        case_manifest.append(
            {
                "id": spec["id"],
                "source_case": spec["source_case"],
                "page": page_rel,
                "model": model_rel,
                "report": report_path.relative_to(ROOT).as_posix(),
                "question_text": case_core_question["text"],
                "question_key": case_core_question["key"],
                "core_question": case_core_question,
                "source_question": {
                    "text": QUESTION_TEXT,
                    "key": str(world.track0.SHARED),
                    "version": "v1",
                    "answer": spec["answered_noncovered_question"],
                },
                "selected_adoption": {
                    "package": f"core-calculations@{args.core_version}",
                    "registry": probe.REGISTRY,
                    "release": f"{release_adoption.get('id')}@{release_adoption.get('version')}",
                    "coordinator_saved_page": True,
                },
                "inputs": spec["inputs"] + (
                    " The synthetic taxpayer was born in 1980 and was not blind on December 31, 2025; "
                    "the taxpayer age and blindness questions are explicitly answered no. Covered-sale "
                    "proceeds and basis share the transaction identity required by v89."
                    if args.core_version == "v89"
                    else ""
                ),
                "age_blindness_answers": (
                    [
                        *_matching_fact_rows(finished, "tax.us.2025.taxpayer-over-65|"),
                        *_matching_fact_rows(finished, "tax.us.2025.taxpayer-blind|"),
                    ]
                    if args.core_version == "v89"
                    else []
                ),
                "answered_noncovered_question": spec["answered_noncovered_question"],
                "noncovered_in_class_answers": _matching_fact_rows(
                    finished, f"{world.proto.NONCOVERED}|"
                ),
                "noncovered_source_closures": _matching_fact_rows(
                    finished, "tax.us.2025.f1099b.noncovered-sold.source-closure|"
                ),
                "source_scope_declarations": [
                    *_matching_fact_rows(finished, "tax.us.2025.schedule-a-boundary."),
                    *_matching_fact_rows(finished, "tax.us.2025.qbi.no-qbi-deduction-declared|"),
                    *_matching_fact_rows(finished, "tax.us.2025.schedule1a.no-additional-deductions-declared|"),
                ],
                "principal_field": spec["principal_field"],
                "live_seconds": elapsed_runs[spec["id"]],
                "stop_reason": report.get("stop_reason"),
            }
        )

    config_path = run_root / "cases.json"
    config_path.write_text(
        json.dumps({"timeout_ms": 5000, "cases": case_manifest}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    # Pytest installs a worker-shared root in conftest; standalone runs use a
    # stable machine-wide temp root rather than creating a private per-run slot.
    if not env.get("DEMO_CHROME_STARTUP_DIR"):
        env["DEMO_CHROME_STARTUP_DIR"] = str(_system_temp_parent() / "demo-chrome-startup-coordinator")
    Path(env["DEMO_CHROME_STARTUP_DIR"]).mkdir(parents=True, exist_ok=True)
    node_command = [
        "node",
        "tools/presentation_harness/sale-page-observation.mjs",
        config_path.relative_to(ROOT).as_posix(),
    ]
    trace_path = run_root / "chrome-observation.jsonl"
    profile_root = _new_owned_chrome_tempdir()
    try:
        env["TMPDIR"] = str(profile_root)
        browser_run = _run_bounded_subprocess(
            node_command, cwd=ROOT, env=env, timeout_seconds=240
        )
    except _BoundedBrowserFailure as exc:
        category = "timeout" if exc.reason == "browser-observation-timeout" else "cleanup"
        raise SystemExit(
            _format_browser_failure(
                reason=exc.reason,
                category=category,
                stage="python-subprocess",
                node_exit_code=None,
                stdout_bytes=exc.stdout_bytes,
                stderr_bytes=exc.stderr_bytes,
                launch=_safe_launch_record(trace_path),
                node_failure=exc.node_failure,
                node_progress=exc.node_progress,
            )
        ) from None
    except OSError:
        raise SystemExit(
            _format_browser_failure(
                reason="browser-subprocess-start-failed",
                category="chrome-launch",
                stage="python-subprocess",
                node_exit_code=None,
                stdout_bytes=0,
                stderr_bytes=0,
                launch=_safe_launch_record(trace_path),
            )
        ) from None
    finally:
        # This directory is exclusive to this run. Normal Node cleanup empties
        # it; this final owner boundary also removes an interrupted child profile.
        shutil.rmtree(profile_root, ignore_errors=True)
    if browser_run.returncode != 0:
        safe_failure = _safe_failure_record(browser_run.stderr)
        raise SystemExit(
            _format_browser_failure(
                **safe_failure,
                node_exit_code=browser_run.returncode,
                stdout_bytes=_captured_byte_count(browser_run.stdout),
                stderr_bytes=_captured_byte_count(browser_run.stderr),
                launch=_safe_launch_record(trace_path),
            )
        )

    dom_path = run_root / "dom-observations.json"
    dom_payload = json.loads(dom_path.read_text(encoding="utf-8"))
    case_results = _load_case_results(case_specs, case_manifest, dom_payload)
    browser_metadata = {
        "browser_version": dom_payload.get("browser_version"),
        "node_version": dom_payload.get("node_version"),
        "cleanup_completed": dom_payload.get("cleanup_completed"),
    }

    if args.structured_only:
        structured_path = run_root / "regression-observations.json"
        structured_path.write_text(
            json.dumps(
                {
                    "run_name": run_root.name,
                    "browser": browser_metadata,
                    "cases": [
                        {
                            "spec": item["spec"],
                            "metadata": item["metadata"],
                            "model_path": item["metadata"]["model"],
                            "report_path": item["metadata"]["report"],
                            "dom": item["dom"],
                            "differences": item["differences"],
                            "checks": item["checks"],
                        }
                        for item in case_results
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        elapsed = sum(float(item["metadata"].get("live_seconds") or 0) for item in case_results)
        print(
            f"Captured {len(case_results)} structured saved-page cases through core {args.core_version} in real headless Chrome; "
            f"coordinator elapsed sum={elapsed:.3f}s; scratch=temp/sale-page-observation/{run_root.name}/"
        )
        return 0

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    if supplement_mode:
        assert baseline_run_root is not None
        baseline_case_manifest = json.loads((baseline_run_root / "cases.json").read_text(encoding="utf-8")).get("cases", [])
        baseline_dom_payload = json.loads((baseline_run_root / "dom-observations.json").read_text(encoding="utf-8"))
        if not isinstance(baseline_case_manifest, list) or {row.get("id") for row in baseline_case_manifest if isinstance(row, dict)} != {spec["id"] for spec in CASES}:
            raise SystemExit("The baseline run does not contain exactly the original eight P0 cases.")
        baseline_results = _load_case_results(CASES, baseline_case_manifest, baseline_dom_payload)
        baseline_mortgage = next(item for item in baseline_results if item["spec"]["id"] == "mortgage-1098")
        baseline_report = _render_report(args.baseline_run, baseline_results, {
            "browser_version": baseline_dom_payload.get("browser_version"),
            "node_version": baseline_dom_payload.get("node_version"),
            "cleanup_completed": baseline_dom_payload.get("cleanup_completed"),
        })
        if complete_scope_supplement_mode:
            supplement_mode_flag = "--mortgage-itemizing-complete-scope-supplement"
            supplement_name = "P0 supplemental observation: itemizing mortgage with complete scope declarations"
            supplement_filename = "p0-mortgage-itemized-complete-supplement.md"
        elif declared_supplement_mode:
            supplement_mode_flag = "--mortgage-itemizing-declarations-supplement"
            supplement_name = "P0 supplemental observation: itemizing mortgage with boundaries declared"
            supplement_filename = "p0-mortgage-itemized-declared-supplement.md"
        else:
            supplement_mode_flag = "--mortgage-itemizing-supplement"
            supplement_name = "P0 supplemental observation: itemizing mortgage return with boundaries undeclared"
            supplement_filename = "p0-mortgage-itemized-supplement.md"
        supplement_command = f"python3 tools/sale_page_observation.py {supplement_mode_flag} --baseline-run {args.baseline_run}"
        supplement_report = _render_mortgage_supplement(
            run_root.name,
            case_results[0],
            browser_metadata,
            baseline_mortgage,
            args.baseline_run,
            evidence_title=supplement_name,
            run_command=supplement_command,
        )
        supplement_path = EVIDENCE_DIR / supplement_filename
        supplement_path.write_text(supplement_report, encoding="utf-8")

        supplement_model = case_results[0]["model"]
        supplement_dom = case_results[0]["dom"]
        supplement_line12e = _find_section(supplement_model, "tax.us.2025.form1040.line-12e")
        supplement_line12e_value = _safe_dict(supplement_line12e.get("resolved")).get("value") if supplement_line12e else None
        supplement_attachment = next(
            (row for row in supplement_model.get("attachments", []) if isinstance(row, dict) and row.get("id") == "tax.us.2025.rule.attachment.schedule-a"),
            None,
        )
        supplement_attachment_disposition = _safe_dict(_safe_dict(supplement_attachment).get("resolved")).get("disposition")
        supplement_dom_attachment = next(
            (row for row in supplement_dom.get("attachments", []) if isinstance(row, dict) and row.get("id") == "tax.us.2025.rule.attachment.schedule-a-status"),
            None,
        )
        prior_supplement = EVIDENCE_DIR / "p0-mortgage-itemized-supplement.md"
        declared_supplement = EVIDENCE_DIR / "p0-mortgage-itemized-declared-supplement.md"
        complete_supplement = EVIDENCE_DIR / "p0-mortgage-itemized-complete-supplement.md"
        additions: list[str] = []
        for path, label in (
            (prior_supplement, "20,000-interest case with other boundaries undeclared"),
            (declared_supplement, "20,000-interest case with explicit boundary declarations, missing no-other-line16"),
            (complete_supplement, "20,000-interest case with explicit boundary declarations and no-other-line16"),
        ):
            if path.is_file():
                additions.append(f"- {label}: [saved evidence]({path.name}).")
        baseline_report += (
            "\n\n## Incremental mortgage itemization captures\n\n"
            f"These are separate real coordinator/Chrome runs; the original eight-case baseline remains unchanged in `{args.baseline_run}`.\n\n"
            + "\n".join(additions)
        )
        (EVIDENCE_DIR / "p0-observation.md").write_text(baseline_report + "\n", encoding="utf-8")
        print(
            f"Observed one supplemental saved mortgage page through core v79 in real headless Chrome; "
            f"line12e={supplement_line12e_value}; Schedule A model/DOM={supplement_attachment_disposition}/"
            f"{(supplement_dom_attachment or {}).get('disposition')}; evidence=docs/phases/engine-breadth/milestones/"
            f"sale-page-observation-evidence/{supplement_filename}; scratch=temp/sale-page-observation/{run_root.name}/"
        )
    else:
        report = _render_report(run_root.name, case_results, browser_metadata)
        (EVIDENCE_DIR / "p0-observation.md").write_text(report, encoding="utf-8")
        total_differences = sum(len(item["differences"]) for item in case_results)
        print(
            f"Observed {len(case_results)} saved pages through core v79 in real headless Chrome; "
            f"model/DOM differences={total_differences}; evidence=docs/phases/engine-breadth/milestones/"
            f"sale-page-observation-evidence/p0-observation.md; scratch=temp/sale-page-observation/{run_root.name}/"
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit("P0 observation interrupted; scratch output remains under ignored temp/.") from None
