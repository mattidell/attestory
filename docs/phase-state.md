<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-neutral-schedule1",
  "active_plan": "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md",
  "milestone_state": "track-0",
  "status": "CHARTERED, NOT YET BUILT. Milestone 2 of the two-milestone Form 1098-E prerequisite; chartered after Milestone 1 (ssa-no-activity-applicability, closed 2026-08-14, PR #173) merged. Predecessor population re-verified against this base: thirteen tax.us.2025.ss-benefits-scope fact types (v1), all keyed on a bare {tax-year: 2025} literal, contributed, no derivation pins, no declared individuation edge -- the shared Schedule 1 absence declarations. no-rrb-or-foreign-social-benefit is explicitly excluded from that population and dispositioned on its own terms (Milestone 1's fourteenth candidate, a source-existence proposition, not a Schedule 1 absence). Seven Track 0 settlement questions chartered; rival prototypes only if more than one lifecycle shape survives the paper rung; stop for Advisor/owner if the design turns on the Ontology rather than composing its existing derivation/individuation edges. No implementation yet -- Track 0 must settle on paper first.",
  "current_role": "Foreman (present the Track 0 charter for owner-launch; no dispatch without literal authorization)",
  "current_prompt": "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Track 0 charter — seven settlement questions"
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
without answering 33 Social Security declarations. This branch charters
Milestone 2 of the same Form 1098-E prerequisite: making the shared Schedule
1 absence declarations safe to evolve before Form 1098-E introduces real
Schedule 1 activity. **This branch opens no new tax route and implements
nothing yet** — it is a Track 0 paper charter.

## Operational State: Engine Breadth

* **Active milestone (this branch):** Fact-type succession with neutral
  Schedule 1 vocabulary — **Track 0 chartered, not built.** Milestone 2 of
  the owner-approved two-milestone prerequisite between the engine and Form
  1098-E student-loan interest. Milestone 1 (SSA no-activity applicability
  repair) closed 2026-08-14 (PR #173). **They do not share a PR.**
* **Objective:** the thirteen shared Schedule 1 absence declarations gain a
  declared lifecycle relationship to any successor — no silently standing
  old answers, no repeated irrelevant questions, no undeclared third
  displacement mechanism beside the Ontology's two edges (§7).
* **The predecessor population, verified against this base:** thirteen
  `tax.us.2025.ss-benefits-scope` fact types (`v1`), all keyed on a bare
  `{tax-year: 2025}` literal, contributed, carrying no derivation pins and
  reachable by no individuation edge under the two edges §7 recognizes. Full
  table in the plan's `## The predecessor population`.
* **`no-rrb-or-foreign-social-benefit` is explicitly excluded** from that
  population. Milestone 1's T0-1 found it load-bearing for the SSA
  no-activity zero and recorded it as a **fourteenth** migration candidate —
  a source-existence proposition, not a Schedule 1 absence. This milestone
  must disposition it on its own terms, not by analogy to the thirteen.
* **Seven Track 0 settlement questions chartered** (predecessor population;
  `no-rrb-or-foreign-social-benefit` disposition; what a successor changes;
  fate of every predecessor state; the displacing edge; schema/ADR
  citizenship; the Part 3 integration surface). Full text in the plan's
  `## Track 0 charter — seven settlement questions`.
* **Rival prototypes** only if more than one lifecycle shape survives the
  paper rung; never one Builder designing both. **Stop for an Advisor/owner
  decision** if the design turns on interpreting the Ontology itself rather
  than composing its existing derivation/individuation edges.
* **Non-goals:** Form 1098-E, Schedule 1 line 21, Form 1040 line 10, and AGI
  lines 11a/11b are **Part 3**, chartered only after this milestone closes.
* **Plan:** `docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md`.
* **Prior milestone:** SSA no-activity applicability repair — closed
  2026-08-14 (PR #173, `05ddd777`). Plan:
  `docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md`.
* **Split record:** `docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md` (PR #172, closed — historical input, not authority; this milestone re-verified its inventory against current `main` rather than inheriting it by reference).

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
