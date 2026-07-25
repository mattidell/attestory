# Foreman Clerk Task Capsule — Current Prompt

Status: **refreshed 2026-07-25 after owner-directed early close of Presentation
Evaluation Process Economy.** This is a mechanical routing record.

## Clerk Task Capsule

- **Source ref:** `closeout/presentation-evaluation-process-economy`.
- **Resolution rule:** immediately when answering, resolve the source ref to
  one commit and include that commit in the response. The resolved commit must
  contain this capsule and every allowed input. The committed capsule does not
  predict its own containing commit.
- **One mechanical task:** when asked “what is the current prompt?”, return the
  fixed current-prompt record below. Do not select or infer work.
- **Allowed repository-relative inputs:** `docs/foreman-handoff.md`,
  `docs/phase-state.md`,
  `docs/phases/real-return/real-return-roadmap.md`,
  `docs/phases/real-return/maturity-matrix.md`,
  `docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`,
  `docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md`,
  `docs/prototypes/human-presentation-citation-walk/analysis/`,
  `docs/presentation-economy/`, `docs/roles/foreman.md`,
  `docs/roles/craft-notes.md`, `PROJECT_PLANNING.md`, and `docs/adr/INDEX.md`,
  all at the query-resolved source commit.
- **Required output shape and paths:** chat output only; make no repository
  write. Return the three labeled fields under “Current prompt record” exactly,
  followed by the source ref and resolved commit.
- **Verification:** resolve the source ref once; confirm that commit contains
  this capsule and every allowed input; confirm the handoff `status`,
  `current_role`, and `current_prompt` agree with the fixed record; confirm the
  economy plan and retrospective say Track 0 is accepted, Track 1 was not
  merged, and repair/Tracks 2–3 were retired; and confirm the roadmap names
  Presentation toward a human surface as selected for planning but not active.
- **Stop rule:** if the ref cannot be resolved, an allowed input is absent, the
  status fields disagree, or a later foreman-cycle record supersedes this
  capsule, stop and report the exact mismatch. Do not fall back to another ref
  or reconstruct a replacement prompt.

## Current prompt record

- **Current prompt:** “Resume as foreman. Prepare the first actual
  Presentation-frontier milestone plan toward a human surface. Start from the
  maturity matrix, the citation-walk evaluation analysis, the accepted
  Presentation Economy Track 0 contracts, and the five most recent milestone
  retrospectives. Identify any Tier 3 user-visible meaning that requires a
  prototype/ADR before implementation. Declare the comparable workload,
  quality floor, and observable cost fields in the plan. Map known adversarial
  classes into pre-build executable coverage shared by Builder and Reviewer,
  and charter independent review only around the genuinely novel boundary.
  Do not revive the rejected general harness as a prerequisite.”
- **Current role:** Foreman planning the first actual Presentation milestone.
- **Prompt/charter path:** `docs/foreman-clerk-task.md`.
