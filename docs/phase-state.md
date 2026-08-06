<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098-mortgage-interest-line12e",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / FORM 1098 HOME-MORTGAGE INTEREST THROUGH SCHEDULE A AND FORM 1040 LINE 12E — PLANNED.** Owner-chartered 2026-08-05 on branch milestone/f1098-mortgage-interest-line12e, base core-calculations v21 / published v16 / release v14 / adoption v21 (tip of origin/main, immediately after box-7 direct FTC). Foreman completed paper-first Track 0 in-doc and chartered Track 1 (Form 1098 family + Schedule A line 8a/completeness); Track 2 (selection guard, attachment disposition, line-12e/13a/13b/14 succession, package/explanation/presentation) not yet chartered pending Track 1. A Track 1 builder correctly stopped on stop condition (a) (singleton-cardinality bound needs a new evaluator primitive, not existing closure content); foreman resolved it in-doc under 'Stop condition (a) resolution' (new additive rule-artifact.v4 'count' op; single family with box-2/3/etc as companions, not a per-box family split). No dispatch this session per owner instruction; Track 1 is owner-launch only. Two unrelated concurrent milestones remain open elsewhere and were not touched: PR #162 (Form 1099-R IRA distributions line 4b) and PR #163 (SSA-1099 benefits lines 6a/6b).",
  "retrospective": null,
  "current_role": "Builder (Track 1, owner-launch)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md"
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
line 1/8 and Form 1040 line 20. The active Engine Breadth milestone is Form
1098 home-mortgage interest through Schedule A and Form 1040 line 12e,
planned (Track 0 settled, Track 1 chartered, not yet built).

## Operational State: Engine Breadth

* **Active milestone:** Form 1098 Home-Mortgage Interest through Schedule A
  and Form 1040 Line 12e, **planned 2026-08-05** on branch
  `milestone/f1098-mortgage-interest-line12e`, base core-calculations
  **v21** / published **v16** / release **v14** / adoption **v21** (tip of
  `origin/main`, immediately after Form 1099-DIV box-7 direct FTC).
* **Current result:** paper-first Track 0 settled in-doc (supported class,
  Form 1098 box/authority inventory, mechanical debt-limit proof, Schedule A
  completeness boundary, generic-itemized-assertion guard, 2025
  deduction-spine bounded-additive-successor decision, attachment-selection
  contract). Track 1 (Form 1098 family, taxpayer-authority facts, Schedule A
  line 8a and completeness) chartered, not yet built. Track 2 (selection
  guard, attachment disposition, line-12e/13a/13b/14 succession, package,
  explanation, presentation) not yet chartered.
* **Plan:** `docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md`.
* **Retrospective:** none yet (milestone not closed).
* **Concurrent milestones (untouched, on their own branches/worktrees):**
  PR #162 `milestone/form1099r-ira-distributions-line4b` (OPEN), PR #163
  `milestone/form1040-ssa1099-line6` (DRAFT).
* **Contracts:** no new ADR yet; Track 0 concluded existing ADR-0015/0016/0017
  (identity/closure), ADR-0036 (attachment ontology), ADR-0020/0027/0029/0033/0046
  (explanation/package/citation/presentation) are sufficient by content-level
  reuse — no governance escalation needed.
* **Next:** owner-launch Track 1 (prompt in the milestone doc), or hand
  further direction to the foreman.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
