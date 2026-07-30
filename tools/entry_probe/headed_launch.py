#!/usr/bin/env python3
"""Throwaway bridge for Entry Boundary Track 1b. Not product code.

Launches ``packages/derivation/live_viewing.py``'s ``LiveViewingVehicle``
against a synthetic workspace directory supplied by the caller (a bare temp
directory, never a real workspace), prints the resulting session's
``websocket_url`` as one line of JSON to stdout, and then blocks reading
stdin until told to stop.

It deliberately never calls ``session.close()`` itself. That method's own
last act is to delete the confined ``.live-view/session-<uuid>`` directory,
which would erase the evidence ``tools/entry_probe/probe.mjs`` needs to
inspect before deletion. Instead, the Node-side probe finds the Chrome
process by external ``ps`` inspection (the same method Track 1 used against
``tools/presentation_harness/lib/chrome.mjs``) and signals it directly,
bypassing this module's own teardown, then removes the workspace directory
itself only after inspecting it.

This script imports ``packages/derivation/live_viewing.py`` and
``packages/derivation/live_workspace.py`` unmodified. It does not read or
write any attribute of ``LiveViewingSession`` beyond the one public
``websocket_url`` field.

Not wired into CI or verify. Run only by ``tools/entry_probe/probe.mjs``.

    python3 tools/entry_probe/headed_launch.py <synthetic-workspace-dir>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from packages.derivation.live_viewing import LiveViewingVehicle  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: headed_launch.py <synthetic-workspace-dir>", file=sys.stderr)
        raise SystemExit(2)

    workspace_dir = Path(sys.argv[1])
    capability = WorkspaceCapability(location=workspace_dir)
    session = LiveViewingVehicle().launch(capability, launch_timeout_seconds=10.0)

    print(json.dumps({"websocket_url": session.websocket_url}), flush=True)

    # Block until the Node-side probe is done with this session. It signals
    # the Chrome process directly and then terminates this process; it does
    # not write anything meaningful to our stdin. EOF (pipe closed) or any
    # line ends the wait.
    sys.stdin.readline()


if __name__ == "__main__":
    main()
