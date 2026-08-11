<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-noncovered-basis",
  "active_plan": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / BROKER-FURNISHED NONCOVERED BASIS THROUGH FORM 8949 BOXES B/E AND SCHEDULE D LINES 2/9 — PLANNED.** Owner selected the milestone; the complete plan is committed as this branch's first milestone commit and awaits owner approval in the draft PR. Track 0 runs at the paper rung and is settled inside the plan, including the mandatory adversarial-closure declaration; one closure item (cross-term identity collisions) is returned to the owner for disposition with plan approval. No implementation charter is filed and no package version numbers are allocated or reserved. Base: origin/main f60e7d1, core-calculations v29 / published v24 / release v22 / adopt v29. Concurrent milestone `f1098e-student-loan-interest-line21` (PR #169) competes for the same version numbers; the plan carries a Parallel Work Manifest and an additive-union-at-publication rule.",
  "retrospective": null,
  "current_role": "Foreman (milestone plan awaiting owner approval)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md"
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
The selected next milestone extends the Form 1099-B capital path to
transactions whose basis the broker shows to the recipient but does not report
to the IRS, routing them through Form 8949 boxes B and E into Schedule D
lines 2 and 9.

## Operational State: Engine Breadth

* **Active milestone:** Broker-Furnished Noncovered Basis through Form 8949
  Boxes B/E and Schedule D Lines 2/9 — **planned**, awaiting owner approval of
  this branch's committed plan and draft PR. No implementation charter is
  filed.
* **Plan:** `docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`.
  Track 0 is settled at the paper rung inside the plan, including the
  adversarial-closure declaration.
* **Proposed contracts:** ADR-0063 (noncovered transaction authority, family
  topology, generalized identity-collision kill-test, Path C completeness
  successor) and ADR-0064 (Form 8949 boxes B/E, Schedule D lines 2/9
  composition). Neither is drafted yet; both are Track 0 outputs pending
  approval.
* **Open owner decision:** whether the generalized identity-collision
  kill-test also covers cross-term pairs (the same transaction identity
  asserted into both a short-term and a long-term family). Not detected today
  and not detected after this milestone unless the owner extends it.
* **Base:** origin/main `f60e7d1`; core-calculations **v29**, published
  **v24**, release **v22**, adoption **v29**. No successor version is
  reserved — `milestone/f1098e-student-loan-interest-line21` (PR #169) is
  concurrent and competes for the same numbers.
* **Just closed:** Form 1098 Home-Mortgage Interest through Schedule A and
  Form 1040 Line 12e, closed 2026-08-10. Plan:
  `docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md`.
* **Prior closed (record defect, not repaired here):** the SSA-1099 and IRA
  line-4b routes are merged on the ratified line (PR #163 `48d46f9`, PR #162
  `9cecf30`) and their plans remain committed, but neither has a file under
  `docs/milestone-retrospectives/` and both plan capsules still read
  `track-2`. The coverage frontier's status rows were reconciled to the
  committed source in this milestone's planning commit; the missing
  retrospectives are recorded here rather than backfilled, because writing
  them is not this milestone's work.
* **Next:** owner approval of the plan and draft PR, then the Track 0
  contract charters.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
