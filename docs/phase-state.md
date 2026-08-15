<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-neutral-schedule1",
  "active_plan": "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md",
  "milestone_state": "track-1",
  "status": "TRACK 0 COMPLETE AND DISPOSITIONED. All seven questions settled on paper and independently reviewed; verdict STOP FOR ADVISOR fired on exactly one finding (F1, T0-5's displacing-edge mechanism) -- T0-1, T0-2, T0-3, T0-6, T0-7, and all four rejected mechanism alternatives held on independent re-derivation. Owner disposition on F1: adoption of an explicit migration artifact is a direct supersession root, not an individuation edge and not a new third cascade edge -- this corrects (not merely approves) the paper's original individuation-root framing. '## Amended Track 1 charter' in the plan supersedes the paper's original Track 1 proposal with that correction; nothing else is reopened. No governance version change; no Ontology amendment. Two non-blocking review hygiene items (F2, a stale parent-SHA citation) remain for Track 1 to clean up incidentally, not to re-litigate.",
  "current_role": "Foreman (present the Track 1 charter for owner-launch; no dispatch without literal authorization)",
  "current_prompt": "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Amended Track 1 charter"
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
  Schedule 1 vocabulary — **Track 0 complete and dispositioned; Track 1
  chartered, not built.** Milestone 2 of the owner-approved two-milestone
  prerequisite between the engine and Form 1098-E student-loan interest.
  Milestone 1 (SSA no-activity applicability repair) closed 2026-08-14
  (PR #173). **They do not share a PR.**
* **Objective:** the thirteen shared Schedule 1 absence declarations gain a
  declared lifecycle relationship to any successor — no silently standing
  old answers, no repeated irrelevant questions, no undeclared third
  displacement mechanism beside the Ontology's recognized roots and edges.
* **The predecessor population, independently re-verified twice:** thirteen
  `tax.us.2025.ss-benefits-scope` fact types (`v1`), all keyed on a bare
  `{tax-year: 2025}` literal, contributed, carrying no derivation pins.
  `no-rrb-or-foreign-social-benefit` is excluded — a fourteenth, separately
  dispositioned, source-existence proposition. Full table in the plan's
  `## The predecessor population`.
* **T0-5 dispositioned by the owner.** The paper's original argument —
  displacement via an individuation edge with the predecessor fact type as
  the "keyed-on citizen" — was independently reviewed and held to be a live
  but non-unique Ontology reading (STOP FOR ADVISOR). Owner ruling: adoption
  of an explicit migration artifact is a **direct supersession root**, not an
  individuation edge and not a new third cascade edge. No Ontology amendment.
  See the plan's `## Owner disposition (binding on Track 1)`.
* **`## Amended Track 1 charter`** supersedes the paper's original Track 1
  proposal with that correction. T0-1 through T0-4, T0-6, T0-7, and the
  required-evidence list are unaffected and are not reopened.
* **Independent review:** `docs/reviews/2026-08-14-fact-type-succession-track0-review.md`.
  Every claim except F1 held on independent re-derivation against the kernel
  (`packages/kernel/facts.py`, `packages/kernel/currency.py`) and the
  committed bundle/rule, not merely against the builder's prose.
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
