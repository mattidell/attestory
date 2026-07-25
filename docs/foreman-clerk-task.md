# Foreman Clerk Task Capsule — Current Prompt

Status: **refreshed 2026-07-25 for Browser Evaluation Runner Completion after
owner merge of the planning unit.** This is a mechanical routing record; it
does not authorize dispatch before merge.

## Clerk Task Capsule

- **Source ref:** `main`; the Browser Evaluation Runner Completion planning
  unit is owner-merged in PR #69.
- **Resolution rule:** immediately when answering, resolve the applicable
  source ref once and include that commit in the response. The commit must
  contain this capsule and every allowed input.
- **One mechanical task:** when asked “what is the current prompt?”, return the
  fixed record below. Do not select work, dispatch a role, or infer a substitute
  prompt.
- **Allowed repository-relative inputs:** `docs/foreman-handoff.md`,
  `docs/phase-state.md`,
  `docs/phases/real-return/milestones/browser-evaluation-runner-completion.md`,
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`,
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair-review.md`,
  `docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md`,
  `docs/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`,
  `docs/prototypes/human-presentation-citation-walk/analysis/`,
  `docs/presentation-economy/`, `docs/roles/builder.md`, `docs/adr/INDEX.md`,
  and `AGENTS.md`, all at the resolved commit.
- **Required output:** chat only. Return the three labeled fields under
  “Current prompt record,” then the resolved source ref and commit.
- **Verification:** confirm the plan status says merge activates the repair
  Builder; confirm the handoff role and prompt match this record; confirm the
  charter requires adoption of the preserved implementation and forbids
  rebuilding; and confirm the plan scopes one repair and one focused delta
  review to the six known blockers and transferred measurements.
- **Stop rule:** before plan merge, report that the prompt is prepared but not
  launchable. After merge, stop if `main` lacks the plan/charter or any state
  field disagrees. Do not reconstruct a prompt.

## Current prompt record

- **Current prompt:** “You are the Browser Evaluation Runner repair Builder.
  Read
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`
  and its complete Context Capsule. After the milestone planning unit is
  owner-merged to `main`, resolve and echo the exact source/scope/evidence
  ceiling/stop conditions. Create the planned milestone branch, adopt and
  verify the preserved runner implementation named by the charter, then repair
  only the six known blockers and complete the transferred lifecycle/output
  measurements. Do not rebuild the runner or run a presentation-economy,
  product-prototype, or adversarial-novelty experiment.”
- **Current role:** Browser Evaluation Runner repair Builder.
- **Prompt/charter path:**
  `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`.
