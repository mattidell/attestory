<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
  "milestone_state": "closing",
  "status": "Milestone 3 (The Entry Loop - synthetic) is closing. All build units are done: Track 4 repaired the focus indicator and reproduced on foreman inspection. The W-2 cell stays at L1 -- the second evaluation returned FAIL and nothing re-scored the surface afterwards, so the failed evaluation stands as the reported outcome. The remaining unit is the close PR against main-ui: milestone outcome, retrospective, carried findings, and ADR-0049 and ADR-0051 brought to the owner for ratification. The next milestone is the owner's to pick, and a phase-boundary legibility audit is due and is owner-spawned.",
  "current_role": "Builder — milestone close (PR is the gate)",
  "current_prompt": "docs/reviews/charter-2026-07-29-entry-loop-synthetic-close.md"
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
* **Owner's at the close:** ADR-0049 and ADR-0051 ratification, the next milestone, and the phase-boundary legibility audit

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
