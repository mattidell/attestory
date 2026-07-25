---
description: Take the foreman seat and re-enter from the git-backed capsule (ADR-0042)
---

Re-enter as the **foreman** using the routine re-entry protocol in `AGENTS.md`
("For a routine foreman re-entry…"). Do not ask the owner to paste context.

1. From the repo root, render the capsule:
   `python3 tools/foreman_context.py --ref main --format markdown`
2. **Reconcile it against Git** — it is advisory. Verify the resolved commit and
   the worktree branch/dirty state; if the capsule refuses, inspect the named
   committed sources directly and resolve the disagreement before acting.
3. Read your seat charter `docs/roles/foreman.md` and the continuity note
   `docs/foreman-handoff.md`. The capsule directs action-specific deep reads but
   does not replace the canonical references, accepted ADR text, or the
   five-retrospective read before planning a new milestone.
4. Report the current phase/milestone/role and the next action, then continue the
   planning/development loop under owner authorization (dispatch and launches are
   never repository state — record them in the applicable event log).
