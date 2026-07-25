# Foreman Clerk Task Capsule — Current Prompt

Status: **prepared 2026-07-24 at Track 0 builder-cycle completion.** This is a
mechanical routing record, not dispatch authority. It does not authorize the
clerk or the next execution role.

## Clerk Task Capsule

- **Source ref and resolved commit:**
  `track/presentation-economy-t0-measurement-substrate` at
  `e0ccfad06e70a8ad61a38d8d3ea22fd1b42f3953`.
- **One mechanical task:** when asked “what is the current prompt?”, return the
  fixed current-prompt record below. Do not select, infer, or authorize work.
- **Allowed repository-relative inputs:**
  `docs/foreman-handoff.md`, `docs/phase-state.md`,
  `docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`,
  and
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-measurement-substrate.md`,
  all at the resolved source commit.
- **Required output shape and paths:** chat output only; make no repository
  write. Return the five labeled fields under “Current prompt record” exactly,
  followed by the source ref and resolved commit.
- **Verification:** confirm the resolved source commit exists; confirm its
  handoff `status` and `next_permitted` fields agree with the fixed record; and
  confirm the Track 0 charter says builder implementation complete and
  independent review not authorized.
- **Stop rule:** if the commit is unavailable, an allowed input is missing, the
  status fields disagree, or a later foreman-cycle record supersedes this
  capsule, stop and report the exact mismatch. Do not reconstruct a replacement
  prompt from other repository state.

## Current prompt record

- **Current prompt:** no dispatch prompt is staged.
- **Next role:** Track 0 independent Reviewer.
- **Authorization:** not authorized; explicit owner authorization is required.
- **Prompt/charter path:** none yet. The foreman must stage the reviewer charter
  before dispatch.
- **Next permitted action:** owner authorizes the Track 0 independent Reviewer;
  the foreman then stages and resolves its charter before dispatch.
