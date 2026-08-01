<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "improvised-prototype",
  "active_plan": "docs/phases/legible-entry/milestones/improvised-prototype.md",
  "milestone_state": "closed",
  "status": "**LEGIBLE ENTRY / IMPROVISED PROTOTYPE — CLOSED 2026-08-01.** All nine evaluation lines now carry a walkable, dependency-aware explanation reusing the presentation model verbatim; a reachability predicate gates the correction action and annotates dependency chips before they're clicked; the trail no longer collapses on navigation. A holistic fresh-eyes review confirmed the walk holds together end to end, with one carried-forward defect (correction resets scroll position).",
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
return, and see the full record explained rather than flattened into status
rows. Every evaluation line -- the five that change with wages and the four
held for comparison -- can expand into a walkable explanation built entirely
from data the presentation model already computed: its governing rule, its
immediate dependencies or its cited evidence, and (for lines that trace back
to the entered fact) a scoped action returning to it. The explanation trail
does not collapse as a reader navigates deeper.

## Operational State: Legible Entry

* **Active Milestone:** none. The Improvised Prototype **closed 2026-08-01.**
* **Product change:** the synthetic W-2 entry surface now exposes a
  dependency-aware, walkable explanation across all nine evaluation lines
  (see `docs/milestone-retrospectives/2026-08-01-improvised-prototype.md`).
* **Plan:** `docs/phases/legible-entry/milestones/improvised-prototype.md`.
* **Carried forward:** a correction resets scroll position, silently
  relocating the reader away from open explanation panels (panels stay open
  and update correctly; only the reader's position is lost).
* **Next:** the owner selects the next milestone. Milestone 7, Real Entry,
  is the roadmap's standing proposal.
* **Branch line:** UI work continues on `main-ui`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
