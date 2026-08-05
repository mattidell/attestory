<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form1099div-box7-direct-ftc",
  "active_plan": "docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / FORM 1099-DIV BOX 7 DIRECT FOREIGN TAX CREDIT (NO FORM 1116) — CLOSED.** An owner-commissioned external independent review (2026-08-05) found the original in-branch READY verdict was made in error; one bounded findings-only repair cycle fixed all five findings (destructive/non-reproducible generator, crashing MFS claim narrowed rather than backfilled, stale presentation golden, thin lifecycle evidence, red mypy gate) and a fresh independent re-review confirmed READY. Package graph unchanged by the repair: core v21 / published v16 / release v14 / adopt v21. Next milestone owner-unselected.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md",
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
line 1/8 and Form 1040 line 20. The next Engine Breadth milestone is
owner-unselected.

## Operational State: Engine Breadth

* **Active milestone:** none. Form 1099-DIV Box 7 Direct Foreign Tax Credit
  (No Form 1116) **closed 2026-08-05** after one findings-only repair cycle
  and a fresh independent re-review confirmed READY, following an external
  review that found the original in-branch READY verdict was made in error.
  Prior state: rebased onto the ratified tip that includes Form 8949 (PR
  #161), Form 1099-INT box 8 (PR #164), and Form 1099-G (PR #166).
* **Current result:** bounded synthetic-complete direct-election box-7 path
  with independent family, residual succession (boxes 3 and 5 only), box-8
  companion, creditability and election authorities, threshold gate, regular-tax
  cap against line 16, Schedule 3 line 1/8, Form 1040 line 20, and
  tax-after-credit. Package graph is the validated additive union of the
  ratified tip plus this milestone’s members: core **v21**, published **v16**,
  release **v14**, adoption **v21** (see retrospective).
* **Plan:** `docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md`.
* **Prior closed (selected pointers):** Form 1099-G plan/retrospective remain
  on the ratified line; this phase-state points at the just-closed box-7 plan.
* **Contracts:** plan B7-C1–C10; no new ADR.
* **Next:** select a new milestone from the coverage frontier.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
