---
description: Self-orient to the current task from git (role auto-detected; no foreman, no paste)
---

Pick up the current role task using the protocol in `AGENTS.md` ("Which seat
are you"). That section governs; this command only invokes it.

```sh
python3 tools/build_orientation_block.py --ref main
```

Verify the printed commit SHA against Git, adopt the detected role's seat file
(`docs/roles/<role>.md`), echo back your understood scope / evidence-rung
ceiling / stop conditions, then act within scope.

Do not ask the owner to paste context.
