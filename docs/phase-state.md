<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098e-student-loan-interest-agi",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md",
  "status": "Closed 2026-08-18. All eight tracks (plus repairs at Tracks 4b and 6b, and one Track-7 repair round) built and foreman-reviewed. Rebased and rebuilt onto origin/main after the concurrent declarative-validation-substrate-f8949 milestone (PR #174) merged: the package this milestone built collided ADD/ADD with that milestone's own same-numbered package; rebuilt on top of its ratified content as core v33 / published v28 / release v26 / adopt v33, with artifact-package.v25 regenerated as v24's true additive successor rather than v23's, as a genuinely bisectable rebase. An independent review of PR #178 (curated object 64c540ce) returned CHANGES REQUESTED on two curation-introduced defects (runner.py's run_and_record use_v2 set regressing a closed rule-artifact.v6 divergence, and three stale v6-capability comments); both fixed at 29971813, gate re-verified green. Full suite green: 1488 passed, 20 skipped, zero regressions against an independent origin/main baseline run. Deferral ledger: docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi-deferral-ledger.md.",
  "current_role": "Foreman — between-milestones selection",
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
The SSA no-activity applicability repair closed a defect on that last SSA
route: a return with no Social Security source can now reach total income
without answering 33 Social Security declarations. The thirteen shared
Schedule 1 absence declarations that used to live on that worksheet
vocabulary now have Schedule-1-native successor ids and an adopted
migration artifact that retires the old ones. The declarative structured
validation and consumer dependency substrate that moved Form 8949's
per-member validation and cross-family identity checks out of generic
runner code into versioned content is closed. **The engine now also covers
the first Engine Breadth route on the income-adjustment side of the
return**: 2025 Form 1098-E student-loan interest through Schedule 1 lines
21/26, Form 1040 line 10, and AGI 11a/11b.

## Operational State: Engine Breadth

* **Active milestone:** none selected.
* **Prior milestone:** 2025 Form 1098-E student-loan interest through
  Schedule 1 lines 21/26, Form 1040 line 10, and AGI — closed 2026-08-18.
  The bounded class: a single 2025 Form 1098-E statement's deductible
  interest, capped at $2,500 and reduced by the MAGI phaseout, computed on
  the Student Loan Interest Deduction Worksheet as rule content and carried
  through Schedule 1 lines 21/26 into Form 1040 line 10 and AGI (lines
  11a/11b). Twelve eligibility components gate the route; MFS filing status
  and any genuine Schedule 1 Part II adjustment this milestone does not
  compute honestly block rather than silently underweighting MAGI. Final
  package is the additive union core **v33** / published **v28** / release
  **v26** / adopt **v33**, over the merged `declarative-validation-substrate-f8949`
  base. Plan:
  `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md`;
  deferral ledger:
  `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi-deferral-ledger.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-18-f1098e-student-loan-interest-agi.md`.
* **Earlier prior milestone:** Declarative Structured Validation and
  Consumer Dependency Substrate — closed 2026-08-17 (PR #174); Candidate B
  P1-P3 ratified into ADR-0066; final package core v32/published v27/release
  v25/adopt v32. Plan:
  `docs/phases/engine-breadth/milestones/declarative-validation-substrate.md`;
  deferral ledger:
  `docs/phases/engine-breadth/milestones/declarative-validation-substrate-deferral-ledger.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md`.
* **Next:** owner selects the next milestone from
  `docs/phases/engine-breadth/coverage-frontier.md`. The scoped-not-built
  rule-artifact/attachment-rule capability-table consolidation
  (`milestones/rule-artifact-capability-table-consolidation.md`) is a
  hardening candidate, not breadth — confirmed a fourth time by this
  milestone's own rebase.
* **Concurrent milestones (separate worktrees, do not collide on schema
  versions):** `f8949-noncovered-basis-lines2-9`. Coordinate through
  `origin/milestone-schema-ledger` — see
  `docs/process/concurrent-work.md`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
