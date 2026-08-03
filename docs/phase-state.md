<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "workspace-prototype",
  "active_plan": "docs/phases/legible-entry/milestones/workspace-prototype.md",
  "milestone_state": "closed",
  "status": "**LEGIBLE ENTRY / WORKSPACE PROTOTYPE — CLOSED on `main-ui` 2026-08-02.** The owner-directed prototype established a separate workspace landing surface over the synthetic entry loop, then exercised it with a genuinely second fact family. The workspace is field-keyed and reuses the existing entry and explanation surfaces.",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/legible-entry/legible-entry-roadmap.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The entry surface can accept and correct synthetic W-2 and 1099-DIV facts,
run the return, and see the full record explained rather than flattened into
status rows. Every evaluation line can expand into a walkable explanation
built entirely from data the presentation model already computed, and the
explanation trail does not collapse as a reader navigates deeper.

The Workspace Prototype added a separate landing surface for orientation:
fact families, entered versus missing facts, current state, and attention
reasons are sourced from the existing model. Selecting a record item opens
the existing entry or explanation surface, and the field-keyed UI now holds
up when a second fact family is present.

## Operational State: Legible Entry

* **Active Milestone:** none. Workspace Prototype closed on `main-ui`
  2026-08-02.
* **Product change:** the workspace is a separate, field-keyed orientation
  surface over the synthetic entry loop, with links into the existing entry
  and explanation surfaces.
* **Plan:** `docs/phases/legible-entry/milestones/workspace-prototype.md`.
* **Carried forward:** correction still resets scroll position, silently
  relocating the reader away from open explanation panels. The workspace
  prototype did not change that behavior.
* **Next:** select the next Legible Entry milestone from the roadmap.
* **Branch line:** UI work continues on `main-ui`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
