<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-evaluation-process-economy",
  "status": "Presentation Evaluation Process Economy Track 0 merged in PR #66; Track 1 harness-core review completed NOT READY with six blockers; focused repair Builder is the current role.",
  "current_role": "Track 1 harness failure-integrity repair Builder",
  "current_prompt": "docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md"
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

## Current state (2026-07-25)

- **Live-Run System Definition and Trust Domains:** complete; ADR-0044 accepted
  as a positioning contract; closure PR #61 **merged**. It selects and schedules
  no enforcement mechanism, makes no L4 claim.
- **Presentation Exploratory Milestone:** complete 2026-07-24. An **exploratory
  milestone (no ADR, no matrix cell raised)** — studied developing/evaluating UI
  under agent-authored, agent-reviewed, owner-light constraints, using a synthetic
  citation-walk surface. Five 2-builder/2-reviewer cycles. Finding: developable
  via a demonstrated loop; ~65–80% of UI quality is agent-mechanizable. Main
  artifact = seven evaluation-analysis documents at
  `docs/prototypes/human-presentation-citation-walk/analysis/` (cycle log +
  process in the sibling `plan.md`; reference prototypes/fixtures/harness-seed
  under `reference/`; retrospective pointer
  `docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md`).
  Raising the Presentation matrix aspect for real remains a well-formed but
  **unselected** ADR-0013 decision prototype.
- **Presentation Evaluation Process Economy:** plan prepared and owner-approved
  2026-07-24, then merged in PR #65 (`1fd3d4c`). It makes economy
  learning—not just one optimization—the durable capability, scoped
  exclusively to UI/UX
  presentation iteration, development, and review. It adds
  presentation-specific workload, observation, and comparison data; a
  source-faithful historical baseline; and a quality-adjusted paired pilot. The
  offline batch harness, standing synthetic corpus, reusable examples, and
  tier-matched review allocation are the first measured intervention. It is not
  evaluating non-presentation workflows and makes no economic claim about them.
  It raises no matrix cell and proposes no ADR. Track 0 builder implementation
  is complete on `track/presentation-economy-t0-measurement-substrate`. The
  owner-launched independent measurement-integrity review returned `NOT READY`
  on one blocker: omitting a workload-declared participant can let a partial
  cost total appear economically promising. The focused participant-cost
  repair landed in `4f8a07c` and the independent delta review returned `READY`;
  Track 0 then merged in PR #66 (`870c8ed`). Track 1's harness-core Builder
  implementation is complete on `track/presentation-economy-t1-harness-core`.
  The independent technical-adversary review completed `NOT READY` with six
  blockers: tuple storage leakage, false-pass malformed injection, launch-time
  signal cleanup leakage, CLI manifest traversal/invalid provenance, incomplete
  manifest strictness, and rejected-input echo on stderr. The exact Reviewer
  also reported 42 turns, 41 tool calls, 12 harness invocations, 11 Chrome
  launches, and unknown token usage; browser execution itself was batched.
  The focused repair Builder is the current role. A post-repair delta-review
  charter is already prepared for the owner's independently launched Reviewer.
  Its five bounded packets measured
  foreman-observed dispatch-to-handoff times of 289, 182, 135, 169, and 480
  seconds. Cache status was never exposed and remains unknown. The resulting
  presentation observation contract records direct task-duration,
  dispatch-batch, foreman-idle-gap, and cache-status telemetry while requiring
  unavailable cache state to stay missing, never inferred.
- **Data boundary:** all committed evidence remains synthetic. Do not access or
  record a real workspace, credential, remote, output, or location. The
  owner-held live-run helpers remain untracked.

## Durable pointers

- Current-prompt Clerk Task Capsule: `docs/foreman-clerk-task.md`.
- Track 0 independent review:
  `docs/reviews/2026-07-24-presentation-economy-t0-measurement-review.md`.
- Track 0 participant-cost repair charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair.md`.
- Track 0 participant-cost repair delta-review charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t0-participant-cost-repair-review.md`.
- Track 1 instrumented harness core charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core.md`.
- Track 1 harness-core review charter:
  `docs/reviews/charter-2026-07-24-presentation-economy-t1-harness-core-review.md`.
- Completed Track 1 harness-core review (`NOT READY`):
  `docs/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`.
- Interrupted Track 1 review progress:
  `docs/reviews/2026-07-25-presentation-economy-t1-harness-core-review-progress.md`.
- Track 1 repair Builder charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`.
- Prepared post-repair delta-review charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair-review.md`.
- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Binding process routing: `docs/adr/INDEX.md`; especially ADR-0005, ADR-0013,
  ADR-0030, ADR-0039, ADR-0042, and ADR-0043.
- Active milestone plan:
  `docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`.
- Grounding economy analysis:
  `docs/prototypes/human-presentation-citation-walk/analysis/04-economy.md`.
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
