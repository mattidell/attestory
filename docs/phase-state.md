<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "improvised-prototype",
  "active_plan": "docs/phases/legible-entry/milestones/improvised-prototype.md",
  "milestone_state": "planned",
  "status": "**LEGIBLE ENTRY / IMPROVISED PROTOTYPE — OPEN ON MAIN-UI.** Prototype one unflattened, navigable explanation in the existing synthetic W-2 entry surface. The owner directs the work and decides what to try and when the milestone is done.",
  "current_role": "Foreman (owner-directed prototype; awaiting the owner's next instruction)",
  "current_prompt": "docs/phases/legible-entry/milestones/improvised-prototype.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The entry surface can accept and correct one synthetic W-2 fact, run the
return, and show which lines changed. The new prototype starts from the richer
presentation and lineage data the UI already receives and asks how to make
that record understandable and navigable instead of flattening it into status
rows.

## Operational State: Legible Entry

* **Active Milestone:** Improvised Prototype.
* **Starting point:** the existing synthetic W-2 loop accepts and corrects a contribution and reports changed return lines.
* **Plan:** `docs/phases/legible-entry/milestones/improvised-prototype.md`.
* **First card:** render a walkable explanation for Form 1040 line 1a without deriving tax meaning again.
* **Next:** the owner chooses the first implementation move.
* **Branch line:** UI work continues on `main-ui`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
