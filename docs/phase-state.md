<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form1099r-ira-distributions-line4b",
  "active_plan": "docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md",
  "milestone_state": "track-1",
  "status": "**ENGINE BREADTH / FULLY TAXABLE IRA DISTRIBUTIONS TO FORM 1040 LINE 4b — TRACK 1 IN FLIGHT.** The Track 1 Builder is implementing the bounded source-to-line-4b boundary from ratified core v21 / published v16 / release v14 / adopt v21. No IRA successor package, schema, registry, or rule version is allocated yet.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md",
  "current_role": "Builder (Track 1 source-to-line-4b boundary)",
  "current_prompt": "docs/reviews/charter-2026-08-04-form1099r-ira-line4b-track1.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Milestone Briefing

The engine computes the closed Engine Breadth synthetic routes through Form
1099-DIV box 2a and box 12, Schedule K-1 box-5 interest, market-discount
interest, Schedule B adjustments, covered Form 1099-B capital paths including
inbound carryovers and Form 8949 wash-sale (code W) lines 1b/8b, Form 1099-INT
box 8 tax-exempt interest on line 2a, Form 1099-G box-1 unemployment
compensation through Schedule 1 into Form 1040 line 8, and the bounded Form
1099-DIV box-7 direct foreign tax credit without Form 1116 through Schedule 3
line 1/8 and Form 1040 line 20. The selected next milestone is the bounded
fully taxable IRA-family distribution route from Form 1099-R to Form 1040 line
4b; line 4a remains blank/absent for this class and basis, rollovers, and
special distribution treatment remain outside the claim.

## Operational State: Engine Breadth

* **Active milestone:** Fully Taxable IRA Distributions from Form 1099-R to
  Form 1040 Line 4b — Track 1 in flight from the ratified tip that includes Form 8949
  (PR #161), Form 1099-INT box 8 (PR #164), Form 1099-G (PR #166), and Form
  1099-DIV box 7 (PR #167).
  Concurrent work remains isolated: the wash-sale work is merged as PR #161,
  and the owner-launched SSA/Form 1040 line-6 work remains on its separate
  branch and draft PR #163; neither is part of this milestone.
* **Current result:** Track 1 Builder dispatched against the committed
  source-to-line-4b charter. The package graph remains the ratified core
  **v21**, published **v16**, release **v14**, adoption **v21**; future IRA
  versions are intentionally unassigned.
* **Plan:** `docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md`.
* **Owner-launch charters:** `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-track1.md`,
  `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-track2.md`,
  `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-review.md`, and
  `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-repair.md`.
* **Prior closed (selected pointers):** Form 1099-G plan/retrospective remain
  on the ratified line; this phase-state points at the just-closed box-7 plan.
* **Contracts:** plan B7-C1–C10; no new ADR.
* **Next:** receive and review the clean Track 1 handoff, then advance the
  pointer to the committed Track 2 charter.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
