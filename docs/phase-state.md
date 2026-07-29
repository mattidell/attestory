<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
  "milestone_state": "track-2",
  "status": "Milestone 3 (The Entry Loop - synthetic) is open. Track 2e re-scored six rows: five Pass/Pass including criterion 2.3, and the accessibility row Fail/Fail on the amount input's focus indicator, so the cell verdict is FAIL and the W-2 cell stays at L1. Track 3 writes the entry-field contract, scoped by owner decision to the field contract only. A narrow focus-indicator repair is still outstanding. Synthetic W-2 only, no real data, no L3 claim. The standing owner directive is to model entry usability as schema and field contracts.",
  "current_role": "Builder — Track 3 entry-field contract",
  "current_prompt": "docs/reviews/charter-2026-07-29-entry-loop-synthetic-track3.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

Milestone 3 builds a synthetic W-2 entry loop. Two rounds of independent
evaluation are done, and the surface substantially works; one accessibility
defect keeps the cell from moving. Track 3 now writes the entry-field contract,
which is the durable deliverable this milestone was built to produce. The
milestone remains synthetic and does not make an L3 claim.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 3 — The Entry Loop (synthetic)
* **Current Track:** Track 3 — The entry-field contract
* **Maturity Status:** W-2 cell remains at L1 (evaluation returned FAIL)
* **Outstanding repair:** the amount input needs a focus indicator distinct from its resting boundary

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
.venv/bin/python3 tools/foreman_context.py --ref HEAD --format markdown
```
