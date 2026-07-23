<!-- foreman-context-v1
{
  "version": 1,
  "topic": "foreman-context-loading",
  "status": "owner-approved role-capsule revision prepared; review and owner merge required",
  "next_permitted": "reconcile the role-capsule branch and obtain owner approval before dispatching the prepared Foreman Context Loading reviewer"
}
-->
# Foreman Handoff Note

A lightweight, living continuity note — **not a protocol and not a gate.** It
describes now. Durable history lives in milestone retrospectives, review
records, ADRs, and Git; this file links there rather than retelling it.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
.venv/bin/python3 tools/foreman_context.py --ref HEAD --format markdown
```

Reconcile its source commit and worktree report with Git, then read the
action-specific sources it names. If it refuses, inspect those committed sources
directly and resolve the disagreement before acting. The capsule does not
authorize a dispatch, change the data boundary, or replace accepted authority.

## Current state (2026-07-23)

- **Foreman Context Loading:** planning (`742e548`), ADR-0042/paper evidence
  (`9f115af`), renderer/tests (`1715626`), and the owner-approved
  builder/reviewer charter and clerk-task-capsule extension are on
  `track/foreman-context-loading-role-capsules`. The milestone is pending its
  required review and owner merge; it is not yet a `main` claim. Prepared
  review charter:
  `docs/reviews/charter-2026-07-23-foreman-context-loading-review.md`.
- **Live-Run Trust-Domain Definition:** remains selected but planning-only.
  Its plan and prototype records remain at
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md` and
  `docs/prototypes/live-run-trust-domains/`. No charter, builder, or reviewer
  dispatch is authorized for that topic.
- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Durable pointers

- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Binding process routing: `docs/adr/INDEX.md`; especially ADR-0005, ADR-0013,
  ADR-0030, ADR-0034, ADR-0039, and ADR-0042.
- Active process milestone: `docs/phases/real-return/milestones/foreman-context-loading.md`.
- Live-run prototype state: `docs/prototypes/live-run-trust-domains/SEAT.md`
  and `docs/prototypes/live-run-trust-domains/process-log.md`.
- Completed-milestone lessons: `docs/milestone-retrospectives/`.
