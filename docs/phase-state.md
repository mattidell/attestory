<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
  "milestone_state": "track-2",
  "status": "Milestone 3 (The Entry Loop - synthetic) is open. Track 2d is active. The work remains limited to a synthetic W-2 entry loop, with no real data or L3 claim. The standing owner directive is to model entry usability as schema and field contracts.",
  "current_role": "Reviewer — Track 2d declaration-driven validation repair re-review",
  "current_prompt": "docs/reviews/charter-2026-07-29-entry-loop-synthetic-track2d-repair-review.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

Milestone 3 builds a synthetic W-2 entry loop. Track 2d is the active repair
unit, focused on making the field's declared format govern both guidance and
runtime behavior. The milestone remains synthetic and does not make an L3
claim.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 3 — The Entry Loop (synthetic)
* **Current Track:** Track 2d — Make format declaration govern behavior
* **Maturity Status:** W-2 cell remains at L1 (Track 2 evaluation failed; pending Track 2d completion and evaluator re-run)

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
.venv/bin/python3 tools/foreman_context.py --ref HEAD --format markdown
```
