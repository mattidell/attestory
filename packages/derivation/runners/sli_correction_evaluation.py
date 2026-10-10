"""Launch the synthetic SLI correction-session evaluation.

This runner composes the existing correction runtime, adopted surface build,
and loopback server. It owns no correction or serving behavior of its own.
It seeds a temporary synthetic workspace, runs the starting (saved) result,
builds the one adopted surface page, serves the correction session over
loopback, and prints the URL.
"""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event
from typing import Sequence

from packages.derivation.correction_session import (
    RUN_SCOPE,
    SCOPE_USER,
    CorrectionRuntime,
    CorrectionSessionServer,
    build_correction_surface,
    core_calculations_surface,
    load_seed_acts,
)
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability

REPO = Path(__file__).resolve().parents[3]


def main(_argv: Sequence[str] | None = None) -> int:
    try:
        with TemporaryDirectory(prefix="demo-correction-saved-") as saved_dir, \
                TemporaryDirectory(prefix="demo-correction-session-") as session_dir:
            acts = load_seed_acts(REPO)
            surface = core_calculations_surface(REPO)

            saved_capability = WorkspaceCapability(Path(saved_dir) / "L")
            saved_outcome = live_coordinate_run(
                saved_capability, repo_root=REPO, authoritative_acts=acts,
                workspace_revision=len(acts), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                request={"schema": "run-request.v1"}, run_id="demo.correction.run.initial",
                governance_pins=[], surface=surface, output_name="initial.json",
            )
            if saved_outcome.refusal is not None or saved_outcome.presentation_path is None:
                print(f"Starting result refused: {saved_outcome.refusal!r}", file=sys.stderr)
                return 1

            session_capability = WorkspaceCapability(Path(session_dir) / "L")
            runtime = CorrectionRuntime(
                session_capability, repo_root=REPO, surface=surface, run_scope=RUN_SCOPE,
                scope_user=SCOPE_USER, saved_presentation_path=saved_outcome.presentation_path,
                saved_run_id="demo.correction.run.initial", seed_acts=acts,
            )
            dist = build_correction_surface(session_capability, repo_root=REPO)

            with CorrectionSessionServer(runtime, dist) as server:
                print("Synthetic SLI correction-session evaluation")
                print(f"URL: {server.url}")
                print("Two forms are seeded: Cedar (lender Cedar Servicing, borrowing "
                      "\"Autumn study loan\") and Birch (lender Birch Servicing, borrowing "
                      "\"Spring study loan\"). Both answer the loan-cost question \"yes\".")
                print("Stop: press Ctrl-C in this terminal.")
                print("Clean restart: stop this command, then run the same command again.")
                sys.stdout.flush()
                Event().wait()
    except KeyboardInterrupt:
        print("\nStopped. Run the command again for a clean starting state.")
        return 130
    except Exception:
        print("Evaluation launch failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
