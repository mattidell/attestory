<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098-mortgage-interest-line12e",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / FORM 1098 HOME-MORTGAGE INTEREST THROUGH SCHEDULE A AND FORM 1040 LINE 12E — CLOSED.** Bounded singleton-closed Form 1098 statement class: deductible interest derived through Schedule A line 8a from taxpayer-authority component facts (never an unexplained contributed conclusion), a composition-complete Schedule A for this class with every unimplemented category genuinely taxpayer-declared absent, deterministic standard-vs-itemized selection at Form 1040 line 12e (guarding the generic itemized assertion off whenever a Form 1098 statement is genuinely on record, including the contradictory-declaration case), and the correct 2025 line-13a/13b/14 deduction-spine succession into taxable income. Rebased onto the merged SSA-1099 milestone (origin/main 48d46f9, PR #163); final package is the additive union core **v29** / published **v24** / release **v22** / adopt **v29**. Independent review passed; CI green on the exact pushed head (PR #168). Next milestone owner-unselected.",
  "retrospective": "docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md",
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
box 8 tax-exempt interest on line 2a, Form 1099-G box-1 unemployment through
Schedule 1 into Form 1040 line 8, the bounded Form 1099-DIV box-7 direct
foreign tax credit, the merged IRA line-4b route, the bounded SSA-1099
Benefits Worksheet route through Form 1040 lines 6a/6b, and the bounded Form
1098 home-mortgage interest route through Schedule A and Form 1040 line 12e.
The next Engine Breadth milestone is owner-unselected.

## Operational State: Engine Breadth

* **Active milestone:** none. Form 1098 Home-Mortgage Interest through
  Schedule A and Form 1040 Line 12e **closed 2026-08-10** after independent
  review returned READY and CI bound the exact curated head.
* **Current result:** bounded synthetic-complete route from a singleton
  Form 1098 statement through Schedule A line 8a, the full Schedule A
  completeness boundary (nine mandatory taxpayer-declaration facts wired
  into the ADR-0036 attachment completeness gate), Form 1040 line 12e (with
  a guard against both the omitted-declaration and contradictory-declaration
  bypass shapes), line-13a/13b/14 deduction-spine succession, and taxable
  income. Package graph is the additive union of the ratified tip plus this
  milestone's members: core **v29**, published **v24**, release **v22**,
  adoption **v29** (see retrospective).
* **Plan:** `docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md`.
* **Prior closed (selected pointers):** SSA-1099 and IRA line-4b plans/
  retrospectives remain on the ratified line; this phase-state points at the
  just-closed Form 1098 plan.
* **Contracts:** Track 0 paper-first scope contract; no new ADR — existing
  identity/closure (ADR-0015/0016/0017), attachment ontology (ADR-0036), and
  explanation/package/citation/presentation (ADR-0020/0027/0029/0033/0046)
  contracts were sufficient by content-level reuse.
* **Next:** select a new milestone from the coverage frontier.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
