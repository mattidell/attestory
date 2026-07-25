# Foreman Clerk Task Capsule — Current Prompt

Status: **refreshed 2026-07-25 after the Track 1 technical-adversary review was
owner-halted with provisional findings and no gate verdict; review completion
prompt prepared.** This is a mechanical routing record.

## Clerk Task Capsule

- **Source ref:** `track/presentation-economy-t1-harness-core`.
- **Resolution rule:** immediately when answering, resolve the source ref to
  one commit and include that commit in the response. The resolved commit must
  contain this capsule and every allowed input. The committed capsule does not
  predict its own containing commit.
- **One mechanical task:** when asked “what is the current prompt?”, return the
  fixed current-prompt record below. Do not select or infer work.
- **Allowed repository-relative inputs:**
  `docs/foreman-handoff.md`, `docs/phase-state.md`,
  `docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`,
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-measurement-substrate.md`,
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-measurement-review.md`,
  `docs/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`,
  and
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair.md`,
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair-review.md`,
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core.md`,
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core-review.md`,
  `docs/reviews/2026-07-25-presentation-economy-t1-harness-core-review-progress.md`,
  all at the query-resolved source commit.
- **Required output shape and paths:** chat output only; make no repository
  write. Return the three labeled fields under “Current prompt record” exactly,
  followed by the source ref and resolved commit.
- **Verification:** resolve the source ref once; confirm that commit contains
  this capsule and every allowed input; confirm its handoff `status`,
  `current_role`, and `current_prompt` fields agree with the fixed record; and
  confirm the Track 1 Builder charter says implementation complete, confirm
  the interrupted progress record has no gate verdict, and confirm the Track 1
  review charter is the current prompt.
- **Stop rule:** if the ref cannot be resolved, the resolved commit does not
  contain this capsule or an allowed input, the status fields disagree, or a
  later foreman-cycle record supersedes this capsule, stop and report the exact
  mismatch. Do not fall back to another ref or reconstruct a replacement prompt
  from other repository state.

## Current prompt record

- **Current prompt:** “You are the High/high technical-adversary Reviewer
  completing the interrupted Presentation Economy Track 1 harness-core review.
  Read
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core-review.md`
  and its complete Context Capsule plus
  `docs/reviews/2026-07-25-presentation-economy-t1-harness-core-review-progress.md`;
  verify the source ref, echo the exact object/scope/evidence ceiling/stop
  conditions, reproduce rather than assume the provisional findings, finish
  every required measurement, and return the required verdict.”
- **Current role:** Track 1 harness lifecycle technical-adversary review
  completion.
- **Prompt/charter path:**
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core-review.md`.
