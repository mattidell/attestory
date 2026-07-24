<!-- foreman-context-v1
{
  "version": 1,
  "topic": "frontier-selection",
  "status": "Live-Run System Definition complete (ADR-0044, PR #61 merged); Presentation UI/UX process experiment complete and preserved (PR #63, abbe1f3); next milestone unselected",
  "next_permitted": "owner selects the next maturity-matrix frontier milestone (a Presentation decision prototype is now well-formed) or directs further exploratory cycles"
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
authorize a foreman dispatch, change the data boundary, or replace accepted
authority.

## Current state (2026-07-24)

- **Live-Run System Definition and Trust Domains:** complete; ADR-0044 accepted
  as a positioning contract; closure PR #61 **merged**. It selects and schedules
  no enforcement mechanism, makes no L4 claim.
- **Presentation UI/UX process experiment:** complete and preserved (PR #63,
  merged `abbe1f3`). An **exploratory process experiment, not a milestone and not
  an ADR** — it studied whether UI/UX is developable under this project's
  constraints (agent-authored, agent-reviewed, owner rarely looking), using the
  citation-walk surface as substrate. Five 2-builder/2-reviewer cycles. Finding:
  yes, via a demonstrated loop (surface a criterion via execution-based review →
  write it into the next brief → the next generation satisfies it, mechanically
  verifiable); ~65–80% of UI quality is agent-mechanizable. Full record + a
  reusable method recipe: `docs/prototypes/human-presentation-citation-walk/plan.md`.
  Raising the Presentation matrix aspect for real is now a well-formed but
  **unselected** ADR-0013 decision prototype.
- **Next:** owner-directed milestone selection from the maturity-matrix frontier
  (Tier 3); no milestone is active.
- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Durable pointers

- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Binding process routing: `docs/adr/INDEX.md`; especially ADR-0005, ADR-0013,
  ADR-0030, ADR-0039, ADR-0042, and ADR-0043.
- Active milestone: `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.
- Accepted decision: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`.
- Live-run system-definition plan:
  `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.
- Review:
  `docs/reviews/2026-07-23-live-run-system-trust-domains-adr-review.md`.
- Retrospective:
  `docs/milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md`.
- Completed-milestone lessons: `docs/milestone-retrospectives/`.
- Presentation UI/UX process experiment (preserved findings + reusable
  agent-driven-UI method recipe): `docs/prototypes/human-presentation-citation-walk/plan.md`.
