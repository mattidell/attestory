"""Save one correction whose calculation fails, then wait to be killed.

Product code has no failure switch. This process patches the coordinate
run so the opening calculation runs and the save-time calculation raises,
after the recorder has appended. The parent kills this process; it does
not print the workspace directory.
"""

from __future__ import annotations

import signal
import sys
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import packages.derivation.correction_session as correction_session  # noqa: E402
from packages.derivation.correction_session import CorrectionRuntime  # noqa: E402
from packages.derivation.live import live_coordinate_run  # noqa: E402
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


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("NOT-READY", flush=True)
        return 1
    workspace = Path(argv[1])
    try:
        calls = {"n": 0}

        def fail_after_opening(*args: Any, **kwargs: Any) -> Any:
            calls["n"] += 1
            if calls["n"] == 1:
                return live_coordinate_run(*args, **kwargs)
            raise RuntimeError("synthetic recalculation failure")

        setattr(correction_session, "live_coordinate_run", fail_after_opening)
        runtime = CorrectionRuntime.initialize(
            WorkspaceCapability(workspace), repo_root=_REPO)
        finding_id = _cedar_finding_id(runtime.state())
        chosen = runtime.choose(finding_id)
        token = chosen.get("token")
        if not isinstance(token, str) or not token:
            raise RuntimeError("worker-token-missing")
        outcome = runtime.confirm(token, "no")
        if outcome.get("outcome") != "saved-not-calculated":
            raise RuntimeError("worker-outcome-unexpected")
    except Exception as exc:
        print(f"NOT-READY {type(exc).__name__}", flush=True)
        return 1
    print("READY", flush=True)
    signal.pause()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
