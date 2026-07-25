---
description: Self-orient to the current task from git (role auto-detected; no foreman, no paste)
argument-hint: "[clean-room]"
---

Pick up the current role task using the runner-agnostic protocol in `AGENTS.md`
("Picking up the current role task"). Do not ask the owner to paste context. The
role is auto-detected from the handoff — you do not need to be told it.

1. From the repo root, run (add `--clean-room` only if `$1` is "clean-room"):
   `python3 tools/build_orientation_block.py --ref main`
2. Verify the printed commit SHA against Git.
3. Read the block's detected `Role` and `Current role (per handoff)`; adopt that
   role's seat charter (`docs/roles/<role>.md`).
4. Echo back your understood scope, evidence-rung ceiling, and stop conditions.
5. Then act within scope.

Clean-room (`/pickup clean-room`): for an independent rival builder. Deep reads
come as a manifest only, not inlined; reimplement from the charter and scope and
do not read any other builder's implementation or thread.
