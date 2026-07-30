<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-rescore",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-rescore.md",
  "milestone_state": "planned",
  "status": "**LEGIBLE ENTRY / RE-SCORE THE ENTRY LOOP — TRACK 1 CHARTERED.** The plan merged 2026-07-30 through PR #115 at `5add975`. Milestone 3 closed with the W-2 cell at L1: its evaluation returned FAIL on the accessibility row and nothing re-scored the surface after Track 4's repair. Owner decisions, 2026-07-29: close the harness gap that left keyboard operability unmeasured in both prior rounds before re-scoring; run one full twenty-row re-score with two fresh evaluators; amending the criteria document is forbidden. A second FAIL is a legitimate outcome. Track 1 makes Tab/Shift+Tab reachability and Enter/Space operability mechanically measurable, extending the existing CDP focus probe; it has a review gate and lands before any evaluator is briefed. Track 1 built at `b261aae`: a new CDP keyboard-operability probe checking reverse traversal, activation by observed effect, and a zero-mouse-event path, with two shipped defect-injection tests. The build reports every control passing and no surface defect. NEXT ACTION: the Track 1 review is chartered and awaiting launch. GOVERNANCE GAP, owner's to decide: the `verify` workflow triggers only on `main`, so no CI has run on this branch or on PRs #112 and #115 -- the UI line has been merging without the gate of record. The phase-boundary legibility audit is still due and is owner-spawned — the foreman must not launch it.",
  "current_role": "Track 1 Reviewer",
  "current_prompt": "docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-review.md"
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
* **Current Track:** Track 1 — built at `b261aae`, awaiting review. Build charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1.md`. Review charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-review.md`. Branch `track/entry-loop-rescore-track1`.
* **Open governance gap:** the `verify` workflow triggers only on `main`, so no CI runs on `main-ui` PRs. PRs #112 and #115 merged with zero checks. Charters on this line currently require a green `verify` that cannot run. Owner's to decide.
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

