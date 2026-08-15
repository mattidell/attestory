<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1098e-student-loan-interest-agi",
  "active_plan": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md",
  "milestone_state": "track-4",
  "status": "Re-cut of the Form 1098-E design-exploration branch (milestone/f1098e-student-loan-interest-line21, PR #169, ruled completed design exploration at owner stop). Cut fresh from origin/main at 85b6a0f1. Track 0 settled (ten settlement questions; five of six adversarial closure artifacts PASS, integration surface PENDING by design pending Track 1-6 build evidence, per the ssa-no-activity-applicability precedent). Foreman review corrected a version collision (rule-artifact v5 -> v6) and a substrate bug in build_orientation_block.py (current_prompt's #anchor was ignored). Version claims on the local-only milestone-schema-ledger branch: attachment-rule v9, artifact-package v25, rule-artifact v6. Track 1 (multiply/divide), Track 2 (Form 1098-E family + twelve eligibility facts), and Track 3 (SLI worksheet rule, publishes Schedule 1 line 21) built, foreman-reviewed (added a missing SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE block test on review), full suite green. Commits f91fb600, 3f201845, plus Track 3's commit and the review addition. Known limitation carried to Track 6: multi-statement per-statement-witness disagreement is unmarshalled first-wins, untested. Track 4 dispatched.",
  "retrospective": null,
  "current_role": "Builder (Track 4 — Schedule 1 line-26 composition and attachment succession)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md#Tracks"
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
migration artifact that retires the old ones. **The active milestone opens
the first Engine Breadth route on the income-adjustment side of the
return** — 2025 Form 1098-E student-loan interest through Schedule 1 lines
21/26, Form 1040 line 10, and AGI 11a/11b.

## Operational State: Engine Breadth

* **Active milestone:** `f1098e-student-loan-interest-agi` — Track 0
  charter drafted on branch `milestone/f1098e-student-loan-interest-agi`,
  cut from `origin/main` at `85b6a0f1`. Not yet performed; no dispatch
  without literal owner authorization in the live thread. Plan:
  `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md`.
* **Re-cut, not a resumption**, of `milestone/f1098e-student-loan-interest-line21`
  (PR #169, still open) — the owner ruled that branch **completed design
  exploration** after its Track 0c found the substrate it depended on
  (cross-fact-type succession) did not yet exist. This milestone inherits
  only that branch's Durable findings register, re-verified against current
  `main`, not its track narrative or prior settlement answers.
* **What re-verification changed:** cross-fact-type succession now exists
  (ADR-0063, `migration-artifact.v1`); the thirteen Schedule 1 absence facts
  have Schedule-1-native ids; but Schedule 1 lines 21/22/26 have **no**
  completeness declaration today — this milestone is not a fourteenth entry
  in an existing pattern, it is the first Part II total. The SSA burden is
  repaired (33 → 1 declaration) but by retaining
  `no-rrb-or-foreign-social-benefit` as load-bearing, not by migrating it —
  that remains the deferred fourteenth migration candidate, out of this
  milestone's scope.
* **Prior milestone:** Fact-type succession with neutral Schedule 1
  vocabulary — closed (PR #177, merged `85b6a0f1`). Milestone 2 of the
  two-milestone Form 1098-E prerequisite; shipped ADR-0063,
  `migration-artifact.v1` / `act-migration-adoption.v1` /
  `artifact-package.v23`, package **v31** / published-packages **v26** /
  release **v24**. Plan:
  `docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-14-fact-type-succession-neutral-schedule1.md`.
* **Earlier prior milestone:** SSA no-activity applicability repair — closed
  2026-08-14 (PR #173). Plan:
  `docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md`.
* **Concurrent milestones (separate worktrees, do not collide on schema
  versions):** `declarative-validation-substrate-f8949` and
  `f8949-noncovered-basis-lines2-9`. Coordinate through
  `origin/milestone-schema-ledger` — see
  `docs/process/concurrent-work.md`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
