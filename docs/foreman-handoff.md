<!-- foreman-context-v1
{
  "version": 1,
  "topic": "live-run-trust-domains",
  "status": "prototype plan prepared; owner approval required before the first current charter and dispatch",
  "next_permitted": "obtain owner approval of the prototype plan and the exact first charter/seat before dispatch"
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

- **Foreman Context Loading:** complete in merged PR #56 (`962c1ac`). ADR-0042,
  the provenance-bound renderer, role charter capsules, and clerk task capsules
  are now `main` records. The initial independent review found M3 only; the
  authorized delta review returned READY. Durable records are the
  retrospective and review reports under `docs/milestone-retrospectives/` and
  `docs/reviews/`.
- **Live-Run Trust-Domain Definition:** is now the active planning-only topic.
  Its plan and prototype records are at
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md` and
  `docs/prototypes/live-run-trust-domains/`. The owner must approve the
  prototype plan and the exact first current charter/seat before any builder or
  reviewer dispatch. No real workspace, credential, remote, output, or
  location may be accessed or recorded.
- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Durable pointers

- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Binding process routing: `docs/adr/INDEX.md`; especially ADR-0005, ADR-0013,
  ADR-0030, ADR-0034, ADR-0039, and ADR-0042.
- Active milestone: `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.
- Live-run prototype state: `docs/prototypes/live-run-trust-domains/SEAT.md`
  and `docs/prototypes/live-run-trust-domains/process-log.md`.
- Completed-milestone lessons: `docs/milestone-retrospectives/`.
