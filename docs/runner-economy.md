# Runner and Cache Economy

Audience: **the owner.** This is not an agent instruction — nothing here is a
rule an agent can follow, because every lever below is pulled from the owner's
side of the session. It lived in `AGENTS.md` until ADR-0045 moved it here.

## How the cache works

Claude Code reuses (caches) the unchanged prefix of each request; a change to
the system prompt or tool set forces a full, slow, uncached re-read. The TTL is
an *inactivity* timer, reset on every hit — continuous work stays warm
regardless of how long a task runs; a gap longer than the TTL goes cold. On a
Claude subscription the main conversation gets a 1-hour TTL; spawned sub-agents
get 5 minutes.

## Keeping it warm

- **Pick model and effort at session start; don't switch mid-task.** Each
  `/model` or `/effort` change re-reads the whole history. With `opusplan`,
  every plan-mode toggle is a model switch — expect a slow turn.
- **Prefer `/rewind` over `/compact`** when abandoning a path: rewind lands on
  an already-cached prefix, compact builds a new one. Run `/compact` at task
  breaks, not mid-task.
- **Avoid single tool calls that block longer than the TTL.** A >5-minute step
  (a slow test or build) cold-starts the next turn. This, not task length, is
  the cache risk — which is why the parallel `pytest` gate is kept at ~26s.
- **Each worktree has its own cache** (the working directory is in the system
  prompt). Create a new worktree only when you need isolation — e.g. a
  clean-room rival, or work that must not disturb another agent's live tree.
  Otherwise the same directory shares the warm cache.

## Measured baseline

See `docs/archive/2026-08-02-milestone-artifacts/prototypes/human-presentation-citation-walk/analysis/04-economy.md`
and the spawn ledger summary (`python3 tools/spawn_ledger.py summary`) for the
current measured numbers rather than estimates.
