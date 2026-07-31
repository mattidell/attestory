<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "improvised-milestone",
  "active_plan": "docs/phases/legible-entry/milestones/improvised-milestone.md",
  "milestone_state": "planning",
  "status": "**LEGIBLE ENTRY / IMPROVISED MILESTONE — PLANNING 2026-07-31.** The owner selected a flexible, goal-oriented milestone under owner-directed mode. It starts with a small prototype that lets the entry surface use existing presentation lineage instead of flattening it into disconnected status rows. There are no fixed tracks, charters, up-front scoring sheet, maturity claim, or predetermined exit criteria. The owner chooses the next useful question as the work develops and decides what completion means after inspecting the result.",
  "current_role": "foreman — owner-directed mode",
  "current_prompt": "docs/phases/legible-entry/milestones/improvised-milestone.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The entry surface can accept and correct one synthetic W-2 fact, run the
return, and show which lines changed. The next milestone turns from proving
that narrow loop toward making the record behind it understandable and
navigable. It begins by preserving explanation data the runner already has
instead of reducing it to entry-specific status rows.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 5 — Improvised Milestone, **planning 2026-07-31.**
* **Goal:** move the entry surface toward a walkable record, starting with an unflattened explanation for Form 1040 line 1a.
* **Working mode:** owner-directed. No charters, fixed tracks, up-front scoring sheet, maturity claim, or predetermined definition of done. The owner chooses direction and decides completion from the result.
* **Starting point:** the synthetic W-2 surface already makes contributions, recomputes the return, and receives the existing presentation model. The prototype should reuse that model and its lineage rather than derive tax meaning again.
* **Plan:** `docs/phases/legible-entry/milestones/improvised-milestone.md`.
* **Prior milestone:** Re-score the Entry Loop closed 2026-07-30 through PR #126; both evaluators scored all twenty rows Pass.
* **Branch line:** UI work continues on `main-ui`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
