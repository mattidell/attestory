<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "workspace-prototype",
  "active_plan": "docs/phases/legible-entry/milestones/workspace-prototype.md",
  "milestone_state": "open",
  "status": "**LEGIBLE ENTRY / WORKSPACE PROTOTYPE — OPEN on `main-ui` 2026-08-01.** Owner-directed prototype of the workspace: the home, map, and inbox for the record. Broader than the Improvised Prototype's per-line explanation walk -- the question here is orientation (what is this workspace, what does it contain, where do I stand, what should I do next), with the existing explanation walk reused as the drill-down rather than rebuilt.",
  "current_role": "Foreman (owner-directed prototype; experiments, no fixed tracks)",
  "current_prompt": "docs/phases/legible-entry/milestones/workspace-prototype.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The entry surface can accept and correct one synthetic W-2 fact, run the
return, and see the full record explained rather than flattened into status
rows. Every evaluation line -- the five that change with wages and the four
held for comparison -- can expand into a walkable explanation built entirely
from data the presentation model already computed: its governing rule, its
immediate dependencies or its cited evidence, and (for lines that trace back
to the entered fact) a scoped action returning to it. The explanation trail
does not collapse as a reader navigates deeper.

The open Workspace Prototype milestone asks a broader question on top of
that: not what produced one value, but what the workspace is, what it
contains, where the person stands in it, and what to do next. It is
orientation and navigation, using the explanation walk above as its
drill-down rather than duplicating it.

## Operational State: Legible Entry

* **Active Milestone:** Workspace Prototype, open on `main-ui` 2026-08-01,
  owner-directed.
* **Product change so far:** none yet -- milestone just opened.
* **Plan:** `docs/phases/legible-entry/milestones/workspace-prototype.md`.
* **Carried forward from Improvised Prototype:** a correction resets scroll
  position, silently relocating the reader away from open explanation panels
  (panels stay open and update correctly; only the reader's position is
  lost). Not in scope for this milestone unless the workspace view surfaces
  it again.
* **Next:** run the first card (a workspace landing view over the synthetic
  W-2 workspace) and let the result determine the next experiment.
* **Branch line:** UI work continues on `main-ui`; this milestone opened on
  `milestone/workspace-prototype`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
