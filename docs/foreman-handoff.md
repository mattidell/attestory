<!-- foreman-context-v1
{
  "version": 1,
  "topic": "live-run-trust-domains",
  "status": "approved records-and-ADR milestone; no new prototype or dispatch",
  "next_permitted": "prepare the evidence-synthesis record; obtain explicit owner approval before any later independent-review dispatch"
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
- **Live-Run System Definition and Trust Domains:** is the active
  records-and-ADR milestone. Its plan is at
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.
  It synthesizes existing boundary evidence; no new prototype or seat dispatch
  is planned. No real workspace, credential, remote, output, or location may
  be accessed or recorded.
- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Durable pointers

- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Binding process routing: `docs/adr/INDEX.md`; especially ADR-0005, ADR-0013,
  ADR-0030, ADR-0034, ADR-0039, and ADR-0042.
- Active milestone: `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.
- Live-run system-definition plan:
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.
- Completed-milestone lessons: `docs/milestone-retrospectives/`.
