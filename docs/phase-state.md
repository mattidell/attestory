<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form1099g-box1-schedule1-line7",
  "active_plan": "docs/phases/engine-breadth/milestones/form1099g-box1-schedule1-line7.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / FORM 1099-G BOX 1 → SCHEDULE 1 LINE 7 / FORM 1040 LINE 8 — CLOSED.** Rebased onto origin/main after Form 8949 and Form 1099-INT box-8 merges. Bounded unemployment route synthetic complete on package v20 (union of ratified v19). Next milestone owner-unselected.",
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
box 8 tax-exempt interest on line 2a, and now Form 1099-G box-1 unemployment
compensation through Schedule 1 lines 7 and 10 into Form 1040 line 8 and line
9. The next Engine Breadth milestone is owner-unselected.

## Operational State: Engine Breadth

* **Active milestone:** none. Form 1099-G Box 1 → Schedule 1 Line 7 / Form
  1040 Line 8 **closed** on this branch after rebase onto the ratified tip
  that includes Form 8949 (PR #161) and Form 1099-INT box 8 (PR #164).
* **Current result:** bounded synthetic-complete unemployment path with
  package **v20** / registry **v15** / release **v13** / adoption **v20**,
  `artifact-package.v17`, `quantity-vocabulary.v9`, line-9 **v5**. Package is
  the validated union of ratified **v19** plus this milestone’s members.
* **Plan:** `docs/phases/engine-breadth/milestones/form1099g-box1-schedule1-line7.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-05-form1099g-box1-schedule1-line7.md`.
* **Next:** select a new milestone from the coverage frontier.

## Re-entry

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
