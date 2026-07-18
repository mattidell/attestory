"""Install the ADR-0031 repo envelope gates as pre-commit/pre-push hooks.

Writes the byte-exact shims `tools/envelope_scan.py` declares into this
clone's git hooks directory (worktree-aware via `git rev-parse
--git-path hooks`) and verifies them. Run once per clone from anywhere
inside the repository:

    python3 tools/install_envelope_hooks.py

The focused suite fails in any clone where this has not been run or the
shims have been edited, so the gate cannot silently be absent.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.envelope_scan import SURFACES, expected_hook_bytes, hooks_dir, verify_hooks


def main() -> int:
    directory = hooks_dir()
    directory.mkdir(parents=True, exist_ok=True)
    for surface in SURFACES:
        hook = directory / surface
        if hook.is_symlink():
            print(f"refusing to install over a symlinked hook: {surface}")
            return 1
        hook.write_bytes(expected_hook_bytes(surface))
        hook.chmod(0o755)
    problems = verify_hooks()
    if problems:
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"envelope gates installed and verified in {directory}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
