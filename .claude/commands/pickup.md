---
description: Self-orient to the current builder/reviewer task from git (no foreman, no paste)
argument-hint: builder | reviewer
---

Pick up the current role task using the runner-agnostic protocol in `AGENTS.md`
("Picking up the current role task"). Do not ask the owner to paste context.

1. From the repo root, run:
   `python3 tools/build_orientation_block.py --ref main --role $1`
2. Verify the printed commit SHA against Git.
3. Confirm the block's `current role` matches "$1". If it does not, STOP and
   report the mismatch — do not proceed on a different role's task.
4. Echo back your understood scope, evidence-rung ceiling, and stop conditions
   per your seat charter (`docs/roles/$1.md`).
5. Then act within scope.
