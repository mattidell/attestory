<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098e-student-loan-interest-line21",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / 2025 FORM 1098-E STUDENT-LOAN INTEREST THROUGH SCHEDULE 1 LINE 21 AND FORM 1040 AGI — PLANNED.** New bounded, independent milestone chartered 2026-08-09 on a clean worktree (`engine-1098e`) and branch `milestone/f1098e-student-loan-interest-line21`, cut from `b25562f` (tip of `milestone/f1098-mortgage-interest-line12e`) at owner direction so version allocation sees the true highest allocated numbers (core v29 / published v24 / rule-artifact.v4 / attachment-rule.v6 / form-field.v3 / fact-type.v3 / line-9 v7). This base carries two unratified milestones — SSA-1099 (PR #163) and Form 1098 mortgage interest (PR #168) — and this milestone depends on both landing; integration order is merge #163 and #168, rebase, rebuild every successor and generated publication, then verify the rebased semantic delta before implementation review or publication. **No version numbers are allocated by the plan.** Track 0 is a paper-first scope contract settling ten items: Form 1098-E field authority; component-level taxpayer eligibility (no collapsed qualified=yes); the box-1 reported-interest boundary; the ordinary Student Loan Interest Deduction Worksheet; MAGI completeness; Schedule 1 Part II completeness; attachment disposition; Form 1040 line 10/11a/11b succession; SSA non-interaction; and contract novelty. Foreman findings already grounded in the base and in the 2025 forms: Form 1040 line 10 is entirely absent and rule.form1040-line11 publishes AGI as a bare passthrough of total income on a line number ('11') the 2025 form does not have — the printed form has 11a and 11b; the deduction spine (12e/13a/13b/14, line-15 v2) is already correct at the base, so only the income side needs repair; the evaluator has no multiply and no divide, both required by worksheet lines 7 and 8, so an ADR-0025-line expression extension is the one expected new contract; and ss-benefits-scope already carries the twelve Schedule 1 lines 11–20/23/25 absence facts the worksheet's MAGI base needs, making reuse-versus-mint the highest-leverage Track 0 decision. No dispatch authorization given or requested — owner-launch only.",
  "retrospective": null,
  "current_role": "Builder (Track 0: paper-first scope contract, owner-launch)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Track 0 charter"
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
foreign tax credit, the merged IRA line-4b route, the bounded SSA-1099 Benefits
Worksheet route through Form 1040 lines 6a/6b, and Form 1098 home-mortgage
interest through Schedule A and Form 1040 line 12e.

Every one of those is an **income** or **deduction** route. This branch opens
the first **adjustment to income**: Form 1098-E student-loan interest through
Schedule 1 line 21. It is therefore the first work that ever puts a value on
Form 1040 line 10 and makes adjusted gross income differ from total income.

## Operational State: Engine Breadth

* **Active milestone (this branch):** 2025 Form 1098-E Student-Loan Interest
  through Schedule 1 Line 21 and Form 1040 Adjusted Gross Income — **planned**.
  Track 0 (paper-first scope contract) is chartered and not yet performed.
* **Branch / worktree:** `milestone/f1098e-student-loan-interest-line21` in
  `engine-1098e`, cut clean from `b25562f`.
* **Base:** `b25562f`, tip of `milestone/f1098-mortgage-interest-line12e`.
  Selected by the owner so version allocation sees the true highest allocated
  numbers: core-calculations **v29**, published **v24**, `rule-artifact.v4`,
  `attachment-rule.v6`, `form-field.v3`, `fact-type.v3`, line-9 rule **v7**.
* **Dependencies:** this base carries two unratified milestones. **PR #163**
  (SSA-1099 lines 6a/6b) supplies the Social Security Benefits Worksheet, the
  `ss-benefits-scope` vocabulary, and line-9 v5–v7. **PR #168** (Form 1098
  mortgage interest) supplies `form1040.line-12e`, lines 13a/13b/14, line-15
  v2, the Schedule A attachment, `rule-artifact.v4`, and the `count`/`block`
  operators. Both must merge before this milestone rebases and allocates
  version numbers.
* **Integration order:** merge #163 → merge #168 → rebase this branch onto the
  resulting ratified line → rebuild every successor and generated publication
  from that base → run the ephemeral three-way semantic-ledger diagnostic and
  verify the rebased semantic delta → only then implementation review or
  publication.
* **Plan:** `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md`.
* **Retrospective:** none yet (milestone not closed).
* **Concurrent milestones (untouched, on their own branches/worktrees):**
  PR #163 `milestone/form1040-ssa1099-line6` and PR #168
  `milestone/f1098-mortgage-interest-line12e`. Neither worktree was altered,
  cleaned, staged, switched, or reused by this milestone's planning.
* **Contracts:** SLI-C1–C10 proposed in the plan; Track 0 owns them. At most
  one new ADR is expected — an ADR-0025-line expression extension adding the
  `multiply` and `divide` operators the worksheet phaseout requires.
* **Next:** owner-launch the Track 0 paper unit; ratify its settlement before
  Track 1 begins.

## Re-entry


Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
