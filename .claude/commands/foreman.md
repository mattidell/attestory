---
description: Take the foreman seat and re-enter from the git-backed capsule (ADR-0042)
---

Re-enter as the **foreman** using the protocol in `AGENTS.md` ("Which seat are
you") and your seat file `docs/roles/foreman.md`. Those govern; this command
only invokes them.

```sh
python3 tools/foreman_context.py --ref main --format markdown
```

The capsule is advisory — reconcile its resolved commit and worktree report
against Git. If it refuses, read the committed sources it names directly.

Then report the current phase, milestone, role, and the next action, and
continue the loop. Remember that you may not dispatch without the owner's
literal authorization string (`AGENTS.md`, "Dispatch authorization").

Do not ask the owner to paste context.
