---
description: Self-orient to the current task from git (role auto-detected; no foreman, no paste)
---

Pick up the current role task using the runner-agnostic protocol in `AGENTS.md`
("Picking up the current role task"). Do not ask the owner to paste context. The
role is auto-detected from the handoff — you do not need to be told it.

1. From the repo root, run:
   `python3 tools/build_orientation_block.py --ref main`
2. Verify the printed commit SHA against Git.
3. Read the block's detected `Role` and `Current role (per handoff)`; adopt that
   role's seat charter (`docs/roles/<role>.md`).
4. Echo back your understood scope, evidence-rung ceiling, and stop conditions.
5. Then act within scope.

If the handoff marks this as a clean-room / rival round, the block auto-switches
to clean-room mode (charter + scope, deep reads as a manifest only) and tells you
not to read any other builder's implementation or thread. You don't pass a flag —
it's detected from the role.
