---
description: Take the foreman seat and re-enter from the git-backed capsule
---

Re-enter as the **foreman** using the protocol in `AGENTS.md` ("Which seat are
you") and your seat file `docs/roles/foreman.md`. Those govern; this command
only invokes them.

```sh
python3 tools/foreman_context.py --ref main --format markdown
```

First run the staleness check in `AGENTS.md` ("Working rules") — fetch, compare
against `origin/main`, and look for a merged PR on this branch. Report a stale
or superseded workspace before doing anything else.

The capsule is advisory — reconcile its resolved commit and worktree report
against Git. If it refuses, read the committed sources it names directly.

Then report the current phase, milestone, role, and the next action, and
continue the loop. Chartering and running the loop need no permission; only
**spawning** sub-agents does (`AGENTS.md`, "Spawning sub-agents").

Do not ask the owner to paste context.
