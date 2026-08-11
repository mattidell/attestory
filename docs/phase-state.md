<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-ssa-applicability",
  "active_plan": "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md",
  "milestone_state": "planned",
  "status": "SPLIT RECORD. The owner approved splitting the prerequisite into two milestones, applicability repair first: (1) ssa-no-activity-applicability, chartered on its own branch and PR; (2) fact-type-succession-neutral-schedule1, chartered only after (1) merges. They do not share a PR. This document charters nothing; it is the split record and Milestone 2's inherited Track 0 input. Two owner corrections govern: docs/archive/ is NEVER product authority, so the governing text is the ratified docs/governance/ontology.md (fact types and facts at §2, migration artifact at §5, two-edge invariant and correction-versus-succession at §7), and INTAKE_ONTOLOGY.md is historical corroboration only, cited nowhere; and the applicability repair does NOT reduce how many literal-keyed facts a workspace instantiates (§2: such facts 'arrive with the territory, instantiated when a body of fact types is adopted'), it reduces unnecessary questions users must answer and prospectively the number of predecessor findings created, so Milestone 2 must still handle predecessor facts that are OPEN as well as answered and preserve the full upgrade matrix. Verified substrate carried forward: all 23 ss-benefits-scope fact types keyed on a single literal {tax-year: 2025} with no entity citizen, contributed so no derivation pins — nothing reaches them under §7's two edges; thirteen are the shared Schedule 1 absences and no-schedule1-line24z-writein already exists in the predecessor bundle; fact-type.v3 allocated but unused and carries no succession field; no migration schema family exists. Owner governance reading for Milestone 2: superseding an adoption MAY authorize the transition but adoption currency may NOT become an undeclared third displacement channel — the contract must expose the predecessor fact type or its adoption as an explicit individuation root, or map every displacement through one of the two recognized edges; reject any design that merely removes types from a flat runtime dictionary or filters by current adoption without declaring the dependency responsible for their standing. Presume Milestone 2 needs an ADR that narrows and instantiates the Ontology rather than amending it. Adoption-currency is a HYPOTHESIS TO TEST, not an accepted design; prototype only after the paper rung identifies the smallest remaining empirical question.",
  "current_role": "Foreman (split record complete; Milestone 1 chartered on its own branch)",
  "current_prompt": "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Mechanism inventory (preserved for Milestone 2's Track 0)"
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

This branch opens no new tax route. It is a **prerequisite engine milestone** —
the first work whose subject is the shape of the question-space itself rather
than a form. It exists because the next tax route, Form 1098-E student-loan
interest through Schedule 1 line 21, cannot be built honestly until a fact
question can be succeeded by a differently identified fact question.

## Operational State: Engine Breadth

* **This branch is a split record.** The owner approved splitting the
  prerequisite into two ordered milestones that **do not share a PR**:
  1. **`ssa-no-activity-applicability`** — the SSA no-activity applicability
     repair, chartered on its own branch and PR.
  2. **`fact-type-succession-neutral-schedule1`** — fact-type succession with the
     thirteen neutral Schedule 1 propositions as its proving case, chartered
     only **after** Milestone 1 merges.

  The fresh Form 1098-E implementation milestone begins after both merge. This
  branch charters nothing; it carries the split record and Milestone 2's
  inherited Track 0 input.
* **Governing text is `docs/governance/ontology.md`** — fact types and facts at
  **§2**, the migration artifact at **§5**, the two-edge invariant and
  correction-versus-succession at **§7**. `docs/archive/` is **never** product
  authority; `INTAKE_ONTOLOGY.md` is historical corroboration only and is cited
  nowhere.
* **Ordering rationale, corrected.** The repair does **not** reduce how many
  literal-keyed facts a workspace instantiates — §2 states such facts "arrive
  with the territory, instantiated when a body of fact types is adopted." It
  reduces the **questions a user must answer** and, prospectively, the
  **predecessor findings users create**. Milestone 2 must still handle
  predecessor facts that are **open** as well as answered, and preserve the full
  upgrade matrix.
* **Verified substrate:** all 23 `ss-benefits-scope` fact types are keyed on a
  single **literal** `{tax-year: 2025}` with no entity citizen, and are
  contributed, so they carry no derivation pins — under §7's two edges **nothing
  reaches them**. Thirteen are the shared Schedule 1 absences;
  `no-schedule1-line24z-writein` **already exists** in the predecessor bundle.
  `fact-type.v3` is allocated, unused, and declares no succession field. No
  migration schema family exists.
* **Milestone 2 posture:** adoption-currency is a **hypothesis to test**, not an
  accepted design. The contract must expose the predecessor fact type or its
  adoption as an explicit **individuation root**, or map every displacement
  through one of the two recognized edges; a design that merely filters a flat
  runtime dictionary by current adoption **without declaring the dependency
  responsible for standing** is an undeclared third edge and is rejected.
  Presume an ADR that **narrows and instantiates** the Ontology, never amends it.
* **Authority boundary:** no seat reads tax-instruction PDFs. Inadequate
  authority is a **stop** requiring a bounded authority review.
* **Branch / worktree:** `milestone/fact-type-succession-ssa-applicability-design`
  in `engine-worktree-3`, cut from `origin/main` (`f60e7d1`). **PR #172.**
* **Split record:** `docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md`.
* **Next:** Milestone 1 Track 0 on its own branch. Dispatch is not authorized;
  charters are prepared for owner launch.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
