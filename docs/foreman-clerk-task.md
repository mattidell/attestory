# Foreman Clerk Task Capsule — Current Prompt

Status: **prepared 2026-07-24 at Track 0 builder-cycle completion.** This is a
mechanical routing record, not dispatch authority. It does not authorize the
clerk or the next execution role.

## Clerk Task Capsule

- **Source ref:** `track/presentation-economy-t0-measurement-substrate`.
- **Resolution rule:** immediately when answering, resolve the source ref to
  one commit and include that commit in the response. The resolved commit must
  contain this capsule and every allowed input. The committed capsule does not
  predict its own containing commit.
- **One mechanical task:** when asked “what is the current prompt?”, return the
  fixed current-prompt record below. Do not select, infer, or authorize work.
- **Allowed repository-relative inputs:**
  `docs/foreman-handoff.md`, `docs/phase-state.md`,
  `docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`,
  and
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-measurement-substrate.md`,
  all at the query-resolved source commit.
- **Required output shape and paths:** chat output only; make no repository
  write. Return the five labeled fields under “Current prompt record” exactly,
  followed by the source ref and resolved commit.
- **Verification:** resolve the source ref once; confirm that commit contains
  this capsule and every allowed input; confirm its handoff `status` and
  `next_permitted` fields agree with the fixed record; and confirm the Track 0
  charter says builder implementation complete and independent review not
  authorized.
- **Stop rule:** if the ref cannot be resolved, the resolved commit does not
  contain this capsule or an allowed input, the status fields disagree, or a
  later foreman-cycle record supersedes this capsule, stop and report the exact
  mismatch. Do not fall back to another ref or reconstruct a replacement prompt
  from other repository state.

## Current prompt record

- **Current prompt:** no dispatch prompt is staged.
- **Next role:** Track 0 independent Reviewer.
- **Authorization:** not authorized; explicit owner authorization is required.
- **Prompt/charter path:** none yet. The foreman must stage the reviewer charter
  before dispatch.
- **Next permitted action:** owner authorizes the Track 0 independent Reviewer;
  the foreman then stages and resolves its charter before dispatch.
