"""Save one correction whose recalculation self-kills mid-run, leaving a
started record with no closing record.

Product code has no failure switch. This process patches
``production_executor.execute_marshaled`` -- the one call that sits between
``start_run``'s own append of the started record and
``execute_and_record_marshaled``'s own append of the closing record -- in
its own interpreter. The started record is already durable by the time the
patched function runs. This process then kills itself with ``SIGKILL``
before returning, so the closing record is never appended and no hand-
written record stands in for one. The opening calculation (``initialize``)
runs unpatched first, so this leaves an earlier *completed* run alongside
the open one. Does not print the workspace directory.
"""

from __future__ import annotations

import os
import signal
import sys
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import packages.derivation.production_executor as production_executor  # noqa: E402
from packages.derivation.correction_session import CorrectionRuntime  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402


def _cedar_finding_id(state: dict[str, Any]) -> str:
    choices = state.get("choices")
    if not isinstance(choices, dict):
        raise RuntimeError("worker-state-invalid")
    matches: list[str] = []
    for choice in choices.values():
        if not isinstance(choice, dict):
            continue
        forms = choice.get("forms")
        if not isinstance(forms, list):
            continue
        for form in forms:
            statement = form.get("statement") if isinstance(form, dict) else None
            if isinstance(statement, str) and statement.startswith("2025 Form 1098-E from Cedar"):
                finding_id = choice.get("finding_id")
                if isinstance(finding_id, str) and finding_id:
                    matches.append(finding_id)
                break
    if len(matches) != 1:
        raise RuntimeError("worker-cedar-not-found")
    return matches[0]


def _die_after_started_record(*_args: Any, **_kwargs: Any) -> Any:
    # ``execute_and_record_marshaled`` already called ``start_run`` (which
    # appends and fsyncs the started record) before calling this function.
    # Say so, then die before the closing record can ever be appended.
    print("READY", flush=True)
    os.kill(os.getpid(), signal.SIGKILL)
    raise AssertionError("unreachable: SIGKILL does not return")  # pragma: no cover


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("NOT-READY", flush=True)
        return 1
    workspace = Path(argv[1])
    try:
        runtime = CorrectionRuntime.initialize(WorkspaceCapability(workspace), repo_root=_REPO)
        finding_id = _cedar_finding_id(runtime.state())
        chosen = runtime.choose(finding_id)
        token = chosen.get("token")
        if not isinstance(token, str) or not token:
            raise RuntimeError("worker-token-missing")
    except Exception as exc:
        print(f"NOT-READY {type(exc).__name__}", flush=True)
        return 1
    setattr(production_executor, "execute_marshaled", _die_after_started_record)
    try:
        runtime.confirm(token, "no")
    except Exception as exc:
        # The patched call kills this process before returning; reaching
        # here at all means the kill did not happen as designed.
        print(f"NOT-READY {type(exc).__name__}", flush=True)
        return 1
    print("NOT-READY no-kill", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
