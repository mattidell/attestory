<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "capital-gain-distributions-line7a",
  "active_plan": "docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / CAPITAL-GAIN DISTRIBUTIONS LINE 7A — LINE 7B PREREQUISITE REPAIR.** The owner selected the targeted repair after the Track-3 clean stop. The Builder is chartered to add only immutable line-7b field/package/registry/release/adoption successors and production-shaped proof, preserving every ratified v1/v7 byte. Track 3 remains paused until this repair is independently reviewed, merged, and green.",
  "current_role": "Line 7b Prerequisite Repair Builder",
  "current_prompt": "docs/reviews/charter-2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

Milestone 3 built a synthetic W-2 entry loop. A person can now type W-2 facts
into a surface and get a computed return without opening a text editor. Two
rounds of independent evaluation ran against criteria written before the code;
the second failed on accessibility, and that failure stands as the reported
outcome. The durable deliverable is the entry-field contract, not the surface.
The milestone remains synthetic and makes no L3 claim.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 3 — The Entry Loop (synthetic), closing
* **Current Track:** none — all build units complete; the close PR is the last unit
* **Maturity Status:** W-2 cell remains at L1 (evaluation returned FAIL, no re-score)
* **Cut decision:** milestone closes at L1; the repair landed but nothing re-scored it, so the cell does not move
* **ADR ratification:** ADR-0049 and ADR-0051 ratified by the owner, 2026-07-29 (PR #112)
* **Owner's at the close:** the next milestone and the phase-boundary legibility audit

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
