<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-neutral-schedule1",
  "active_plan": "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md",
  "milestone_state": "closed",
  "status": "Closed on this branch (PR #177). Milestone 2 of the Form 1098-E prerequisite. No new tax route. Thirteen Schedule 1 absence facts succeed onto Schedule-1-native ids via an adopted migration-artifact.v1 (ADR-0063). Worksheet v3 retargets the nonempty CDS; Milestone 1 empty-route contract unchanged. Publication: core v31 / published-packages v26 / release v24. Track 0 STOP FOR ADVISOR on F1; owner disposition; Track 1 APPROVE. Next milestone unselected.",
  "retrospective": "docs/milestone-retrospectives/2026-08-14-fact-type-succession-neutral-schedule1.md",
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
The SSA no-activity applicability repair closed a defect on that last SSA
route: a return with no Social Security source can now reach total income
without answering 33 Social Security declarations. The thirteen shared
Schedule 1 absence declarations that used to live on that worksheet
vocabulary now have Schedule-1-native successor ids and an adopted
migration artifact that retires the old ones. **This milestone adds no
new tax route.**

## Operational State: Engine Breadth

* **Just-closed milestone (this branch):** Fact-type succession with
  neutral Schedule 1 vocabulary — **closed on this branch (PR #177)**.
  Milestone 2 of the owner-approved two-milestone prerequisite between
  the engine and Form 1098-E. They do not share a PR.
* **Objective, met:** the thirteen shared Schedule 1 absence
  declarations have a declared lifecycle relationship to their
  successors. Old answers do not stand silently. A no-Schedule-1
  return is not asked additional questions. Displacement is a named
  migration-artifact supersession root (ADR-0063), not an
  individuation edge and not a package filter.
* **What shipped:** ADR-0063; `migration-artifact.v1` /
  `act-migration-adoption.v1` / `artifact-package.v23`; thirteen
  `schedule1-adjustments-scope` successors; one succession citizen;
  worksheet v3 CDS retarget; package **v31** / published-packages
  **v26** / release **v24**.
* **What did not ship:** Form 1098-E; Schedule 1 line 21 as a real
  form; Form 1040 line 10; AGI 11a/11b; any change to
  `no-rrb-or-foreign-social-benefit`. Those remain Part 3,
  **unselected**.
* **Independent review:** Track 0 STOP FOR ADVISOR on F1 only; Track 1
  APPROVE, no findings. Material dissent (F1) is decided by ADR-0063.
* **Plan:** `docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-14-fact-type-succession-neutral-schedule1.md`.
* **Prior milestone:** SSA no-activity applicability repair — closed
  2026-08-14 (PR #173). Plan:
  `docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
