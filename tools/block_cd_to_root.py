"""PreToolUse hook: block a redundant `cd` to the directory you are already in.

AGENTS.md forbids `cd`-ing to the repo root because the Bash cwd already persists
there — but a doc rule alone doesn't hold (measured: ~606 redundant `cd`-to-root
calls, and the rule was violated repeatedly even by an agent who had just read
it). This hook enforces it deterministically.

Precise by design: it blocks only when the leading `cd` target resolves to the
current working directory (the truly redundant case). `cd` into a subdirectory or
a different path is untouched. Reads the PreToolUse JSON on stdin; exit code 2
blocks the call and feeds the message back to the model. Any parsing failure
exits 0 (fail open) so the hook can never wedge a session.
"""

from __future__ import annotations

import json
import os
import shlex
import sys


def _first_segment(command: str) -> str:
    # the part before the first &&, ; or | — where a `cd` prefix would live
    for sep in ("&&", ";", "|"):
        command = command.split(sep, 1)[0]
    return command.strip()


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    cwd = payload.get("cwd") or os.getcwd()

    seg = _first_segment(command)
    try:
        tokens = shlex.split(seg)
    except ValueError:
        return 0
    if len(tokens) < 2 or tokens[0] != "cd":
        return 0

    target = os.path.expanduser(tokens[1])
    if not os.path.isabs(target):
        target = os.path.join(cwd, target)
    if os.path.realpath(target) == os.path.realpath(cwd):
        sys.stderr.write(
            "Blocked: redundant `cd` to the current directory. The Bash cwd "
            "persists between calls and already sits here — drop the `cd ... &&` "
            "prefix and run the command directly (AGENTS.md Tool Preamble). Use "
            "absolute paths only to reach a *different* directory.\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
