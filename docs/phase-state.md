<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
  "milestone_state": "closed",
  "status": "**LEGIBLE ENTRY / THE ENTRY LOOP (SYNTHETIC) — CLOSED 2026-07-29 (PR #112).** The W-2 cell stays at L1: the second evaluation returned FAIL on the accessibility row and nothing re-scored the surface after the repair, so the failed evaluation stands as the reported outcome. ADR-0049 and ADR-0051 are ratified by the owner. No track is chartered and no build is in flight. The owner selected the next milestone on 2026-07-29: re-score the repaired W-2 loop against the unchanged criteria to settle the L2 claim. NEXT ACTION: the foreman drafts that milestone plan for owner approval; no charter may be filed before it is approved. The phase-boundary legibility audit is still due and is owner-spawned — the foreman must not launch it.",
  "current_role": "Foreman — drafting the Milestone 4 plan",
  "current_prompt": "docs/phases/legible-entry/legible-entry-roadmap.md"
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

* **Active Milestone:** none — Milestone 3, The Entry Loop (synthetic), closed 2026-07-29 (PR #112)
* **Current Track:** none — no charter is filed and no build is in flight
* **Maturity Status:** W-2 cell remains at L1 (evaluation returned FAIL, no re-score)
* **Cut decision:** the milestone closed at L1; the repair landed but nothing re-scored it, so the cell did not move
* **ADR ratification:** ADR-0049 and ADR-0051 ratified by the owner, 2026-07-29 (PR #112)
* **Next milestone:** selected by the owner 2026-07-29 — re-score the repaired W-2 loop to settle the L2 claim. The plan is being drafted and must be owner-approved before any charter.
* **Still due:** the phase-boundary legibility audit. Owner-spawned by design; the foreman must not launch it.
* **Branch line:** the UI line continues on `main-ui`. PR #113 was a one-off sync of `main-ui` upstream into `main` and does not move the base; UI PRs still target `main-ui`.

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```

