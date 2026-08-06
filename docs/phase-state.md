<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form1099r-ira-distributions-line4b",
  "active_plan": "docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / FULLY TAXABLE IRA DISTRIBUTIONS TO FORM 1040 LINE 4b — CLOSED.** The bounded 2025 ordinary, fully taxable IRA-family Form 1099-R class is synthetic complete through line 4b, line 9, AGI, taxable income, regular tax, package resolution, explanation, citations, and production-shaped presentation; independent re-review returned READY after one findings-only repair. Next milestone owner-unselected.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099r-ira-distributions-line4b.md",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/engine-breadth/coverage-frontier.md"
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
4b, now closed; line 4a remains blank/absent for this class and basis,
rollovers, and special distribution treatment remain outside the claim. The
next Engine Breadth milestone is owner-unselected.

## Operational State: Engine Breadth

* **Active milestone:** Fully Taxable IRA Distributions from Form 1099-R to
  Form 1040 Line 4b **closed 2026-08-05** after one findings-only repair and
  independent re-review READY, from the ratified tip that includes Form 8949
  (PR #161), Form 1099-INT box 8 (PR #164), Form 1099-G (PR #166), and Form
  1099-DIV box 7 (PR #167).
  Concurrent work remains isolated: the wash-sale work is merged as PR #161,
  and the owner-launched SSA/Form 1040 line-6 work remains on its separate
  branch and draft PR #163; neither is part of this milestone.
* **Current result:** bounded ordinary, fully taxable IRA-family distributions
  publish on line 4b with line 4a blank, enter line 9 exactly once, and use the
  existing AGI, taxable-income, and regular-tax path. Package graph is core
  **v22**, published **v17**, release **v15**, adoption **v22**, with
  `artifact-package.v19` and `quantity-vocabulary.v11`.
* **Plan:** `docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-05-form1099r-ira-distributions-line4b.md`.
* **Final review:** `docs/reviews/2026-08-05-form1099r-ira-distributions-line4b-final-review.md`.
* **Prior closed (selected pointers):** Form 1099-G and Form 1099-DIV box-7
  plans/retrospectives remain on the ratified line.
* **Contracts:** plan IRA-C1–C4; no new ADR.
* **Next:** select a new milestone from the coverage frontier.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
