"""SessionStart hook: push worktree branch + dirty state into agent context.

Rationale: transcripts showed ~219 re-orientation `git status`/`git branch`/`git
diff` calls concentrated in sessions that never loaded the foreman capsule. The
branch/dirty data already exists in `foreman_context.worktree_status()`; this hook
*pushes* it at session start so agents need no bash round-trip to orient. It is
intentionally compact (one summary line + a capped path list) so it costs fewer
context tokens than a single `git status` would.

Scope: this reports *state*, never policy. It is a snapshot taken once, at
session start — another agent may move the branch underneath it, which has
happened. When and how to re-check, and how to detect a superseded workspace,
is `AGENTS.md` ("Working rules"); an earlier version of this hook asserted that
no orientation `git status` was needed, which is false past the first turn.

Robustness: any failure prints nothing and exits 0, so a non-git directory or Git
error never blocks a session.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.foreman_context import ContextError, GitRepository

MAX_LISTED_PATHS = 12


def main() -> int:
    try:
        status = GitRepository(Path.cwd()).worktree_status()
    except (ContextError, Exception):  # never break a session over orientation data
        return 0

    branch = status["branch"] or "detached"
    paths = status["dirty_paths"]
    if not status["dirty"]:
        print(f"[worktree-state] branch: {branch} | clean  (snapshot at session start)")
        return 0

    shown = paths[:MAX_LISTED_PATHS]
    more = len(paths) - len(shown)
    print(f"[worktree-state] branch: {branch} | dirty: {len(paths)} path(s)"
          "  (snapshot at session start)")
    for path in shown:
        print(f"  M {path}")
    if more > 0:
        print(f"  … +{more} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
