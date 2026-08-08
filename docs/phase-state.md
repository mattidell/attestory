<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form1099r-ira-distributions-line4b",
  "active_plan": "docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / FULLY TAXABLE IRA DISTRIBUTIONS TO FORM 1040 LINE 4b — CURATED CANDIDATE.** Track 1 and Track 2 are complete; final independent review and CI must bind the exact pushed head.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md",
  "current_role": "Reviewer (curated final range)",
  "current_prompt": "docs/reviews/2026-08-08-form1099r-ira-line4b-curated-final-review-charter.md"
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
  Form 1040 Line 4b — curated candidate after Track 1 and Track 2 completion,
  awaiting final independent review and CI.
  Concurrent work remains isolated: the wash-sale work is merged as PR #161,
  and the owner-launched SSA/Form 1040 line-6 work remains on its separate
  branch and draft PR #163; neither is part of this milestone.
* **Current result:** the bounded IRA-family route is implemented through line
  4b, line 9, AGI, taxable income, regular tax, package resolution,
  explanation, citations, and production-shaped presentation. The current
  package graph is core **v26**, published **v21**, release **v19**, adoption
  **v26**, with exact entrypoints gated by artifact-package **v20**.
* **Plan:** `docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md`.
* **Final review charter:**
  `docs/reviews/2026-08-08-form1099r-ira-line4b-curated-final-review-charter.md`.
* **Prior closed (selected pointers):** Form 1099-G plan/retrospective remain
  on the ratified line; this phase-state points at the just-closed box-7 plan.
* **Contracts:** plan IRA-C1–C4; no new ADR.
* **Next:** obtain an independent verdict on the exact curated head, then run
  the repository verify check before marking PR #162 ready.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
