"""Seed a workspace whose opening calculation is honestly refused.

Product code has no failure switch. This process patches
``correction_session.live_coordinate_run`` in its own interpreter so
``CorrectionRuntime.initialize``'s own opening call returns a typed
refusal -- the same ``LiveCoordinatorOutcome`` shape a real resolver
refusal returns, before any run record is ever written. The seed acts are
already durably committed by the time ``initialize`` makes that call (the
seed loop runs first), so the workspace this leaves behind holds an
account and no run record at all. Does not print the workspace directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import packages.derivation.correction_session as correction_session  # noqa: E402
from packages.derivation.correction_session import (  # noqa: E402
    CorrectionRuntime,
    CorrectionSessionError,
)
from packages.derivation.live import LiveCoordinatorOutcome  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import Refusal  # noqa: E402


def _refuse(*_args: object, **_kwargs: object) -> LiveCoordinatorOutcome:
    return LiveCoordinatorOutcome(
        refusal=Refusal(reason="SYNTHETIC_OPENING_REFUSAL", detail="test-only refusal"),
        output_path=None, run_id=None, presentation_path=None,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("NOT-READY", flush=True)
        return 1
    workspace = Path(argv[1])
    setattr(correction_session, "live_coordinate_run", _refuse)
    try:
        CorrectionRuntime.initialize(WorkspaceCapability(workspace), repo_root=_REPO)
    except CorrectionSessionError:
        pass
    else:
        print("NOT-READY no-refusal", flush=True)
        return 1
    print("READY", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
