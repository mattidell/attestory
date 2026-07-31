<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "improvised-milestone",
  "active_plan": "docs/phases/legible-entry/milestones/improvised-milestone.md",
  "milestone_state": "closed",
  "status": "**LEGIBLE ENTRY / IMPROVISED MILESTONE — CLOSED 2026-07-31.** No implementation began and no product behavior changed. The owner closed it so main and main-ui can begin their next milestones from a clean shared base. The unflattening prototype remains parked for later selection.",
  "current_role": "Foreman (select the next milestone; owner-held)",
  "current_prompt": "docs/phases/legible-entry/legible-entry-roadmap.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The entry surface can accept and correct one synthetic W-2 fact, run the
return, and show which lines changed. The proposed explanation prototype did
not begin. The owner closed it so `main` and `main-ui` can select separate
milestones after their histories are reconciled.

## Operational State: Legible Entry

* **Active Milestone:** none. The Improvised Milestone **closed without implementation 2026-07-31.**
* **Product change:** none.
* **Plan:** `docs/phases/legible-entry/milestones/improvised-milestone.md`.
* **Parked work:** the unflattening explanation prototype may be selected again later.
* **Next:** reconcile `main-ui` into `main`, then select separate milestones on the two branch lines.
* **Branch line:** UI work continues on `main-ui`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
