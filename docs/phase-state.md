<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form1099r-ira-distributions-line4b",
  "active_plan": "docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / FULLY TAXABLE IRA DISTRIBUTIONS TO FORM 1040 LINE 4b — INDEPENDENT REVIEW IN FLIGHT.** Track 1 is committed as `efe0992` and Track 2 as `3274044`; the independent Reviewer is measuring the complete candidate, including package successors core v22 / published v17 / release v15 / adopt v22.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md",
  "current_role": "Reviewer (independent full-candidate review)",
  "current_prompt": "docs/reviews/charter-2026-08-04-form1099r-ira-line4b-review.md"
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
  Form 1040 Line 4b — Track 2 in flight after the ratified tip that includes Form 8949
  (PR #161), Form 1099-INT box 8 (PR #164), Form 1099-G (PR #166), and Form
  1099-DIV box 7 (PR #167).
  Concurrent work remains isolated: the wash-sale work is merged as PR #161,
  and the owner-launched SSA/Form 1040 line-6 work remains on its separate
  branch and draft PR #163; neither is part of this milestone.
* **Current result:** Track 1 is committed at `efe0992`, adding the bounded
  source-to-line-4b boundary. Track 2 is committed at `3274044`, adding the
  line-9/downstream/package/explanation/presentation integration. The package
  graph is now core **v22**, published **v17**, release **v15**, adoption
  **v22**; the independent review is in flight.
* **Plan:** `docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md`.
* **Owner-launch charters:** `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-track1.md`,
  `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-track2.md`,
  `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-review.md`, and
  `docs/reviews/charter-2026-08-04-form1099r-ira-line4b-repair.md`.
* **Prior closed (selected pointers):** Form 1099-G plan/retrospective remain
  on the ratified line; this phase-state points at the just-closed box-7 plan.
* **Contracts:** plan B7-C1–C10; no new ADR.
* **Next:** receive the independent review verdict; triage any findings before
  preparing the bounded repair cycle or milestone closeout.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
