<!-- foreman-context-v1
{
  "version": 1,
  "topic": "browser-evaluation-runner-completion",
  "status": "Presentation Economy closed in merged PR #68; Browser Evaluation Runner Completion plan prepared; existing-runner repair Builder is next after plan merge.",
  "current_role": "Browser Evaluation Runner repair Builder",
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
- **Presentation Evaluation Process Economy:** closed early by owner direction
  2026-07-25. Track 0 merged in PR #66 (`870c8ed`) and is the accepted
  foundation: strict presentation workload/observation/comparison contracts,
  the source-faithful historical baseline, participating-role completeness,
  and quality-before-cost comparison. Track 1's independent review returned
  `NOT READY` on tuple storage leakage, false-pass malformed injection,
  launch-time cleanup leakage, path/provenance traversal, incomplete strict
  validation, and rejected-input echo. Its implementation was not merged; the
  prepared repair/re-review and Tracks 2–3 were retired. The review trace
  reported 42 turns, 41 tool calls, 12 harness invocations, 11 Chrome launches,
  batched browser execution, several very large context reads, and unknown
  total token use. The retrospective records the owner disposition and the
  promoted foreman discipline: give known adversarial classes to both Builder
  and Reviewer as executable coverage, and spend independent review on an
  explicit novel boundary.
- **Browser Evaluation Runner Completion:** owner-directed plan prepared
  2026-07-25. It resumes the existing, reviewed implementation preserved on
  `track/presentation-economy-t1-harness-core`; the Builder must transplant the
  commit whose subject is `implement Track 1 instrumented harness core and
  fail-closed lifecycle`, verify the adopted files, and repair rather than
  reconstruct. Scope is the six known blockers (storage isolation, injection
  acknowledgement, cancellation-safe cleanup, canonical path/provenance
  confinement, strict non-vacuous validation, and redacted external failures)
  plus the transferred lifecycle/output measurements. One focused delta review
  checks those changes and adjacent invariants. No runner rebuild, product
  prototype, economy experiment, novelty catalog, or broad creative re-review
  belongs in this milestone. Merge of the planning unit activates the prepared
  repair Builder charter.
- **Later direction:** the actual human-surface Presentation frontier remains
  selected but deferred until the runner is trustworthy. The accepted economy
  contracts remain available, but no economical improvement or novelty-review
  practice has yet been demonstrated.
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
- Reactivated existing-runner repair Builder charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`.
- Prepared focused post-repair delta-review charter:
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair-review.md`.
- Foreman posture and verification floor: `docs/roles/foreman.md`.
- Binding process routing: `docs/adr/INDEX.md`; especially ADR-0005, ADR-0013,
  ADR-0030, ADR-0039, ADR-0042, and ADR-0043.
- Closed milestone plan:
  `docs/phases/real-return/milestones/presentation-evaluation-process-economy.md`.
- Milestone retrospective:
  `docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md`.
- Prepared Browser Evaluation Runner Completion plan:
  `docs/phases/real-return/milestones/browser-evaluation-runner-completion.md`.
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
