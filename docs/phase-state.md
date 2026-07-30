<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-rescore",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-rescore.md",
  "milestone_state": "planned",
  "status": "**LEGIBLE ENTRY / RE-SCORE THE ENTRY LOOP — PLANNED.** Milestone 3 closed 2026-07-29 (PR #112) with the W-2 cell at L1: its evaluation returned FAIL on the accessibility row and nothing re-scored the surface after Track 4's repair. Milestone 4 settles that claim. Owner decisions, 2026-07-29: close the harness gap that left keyboard operability unmeasured in both prior rounds before re-scoring; run one full twenty-row re-score with two fresh evaluators; amending the criteria document is forbidden. A second FAIL is a legitimate outcome. NEXT ACTION: charter the Track 1 Builder to make keyboard reachability and operability mechanically measurable, on a fresh branch from the plan merge. The phase-boundary legibility audit is still due and is owner-spawned — the foreman must not launch it.",
  "current_role": "Track 1 Builder",
  "current_prompt": "docs/phases/legible-entry/milestones/entry-loop-rescore.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

Milestone 3 built a synthetic W-2 entry loop and then failed its own
evaluation on accessibility, so the surface scored worse than it probably is:
the defect was repaired afterwards but nothing re-ran the evaluation, and a
repair does not retroactively pass a score. Milestone 4 settles that. It first
fixes the measuring instrument — keyboard operability was never actually
measurable — and then re-scores the whole sheet with two evaluators who have
not seen this surface before. Failing again is an acceptable result.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 4 — Re-score the Entry Loop, planned
* **Current Track:** Track 1 — make keyboard reachability and operability mechanically measurable
* **Maturity Status:** W-2 cell at L1. No cell in this phase has reached L2.
* **Prior close:** Milestone 3 closed 2026-07-29 (PR #112) at L1; ADR-0049 and ADR-0051 ratified there
* **Owner decisions, 2026-07-29:** close the harness gap before re-scoring; one full twenty-row re-score with two fresh evaluators; **the criteria document may not be amended**
* **Still due:** the phase-boundary legibility audit. Owner-spawned by design; the foreman must not launch it.
* **Branch line:** the UI line continues on `main-ui`. PR #113 was a one-off sync of `main-ui` upstream into `main` and does not move the base; UI PRs still target `main-ui`.

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.
* **Prove the check bites:** any assertion added to an evaluation harness must be demonstrated to fail when the behaviour it guards is removed. Milestone 3 rejected three builds for machinery that asserted something untrue.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```

