<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "ssa1099-benefits-line6",
  "active_plan": "docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / 2025 SSA-1099 BENEFITS TO FORM 1040 LINES 6a/6b — CLOSED OUT, PR OPEN.** The bounded SSA-1099 route is implemented through lines 6a/6b, line 9, AGI, taxable income, regular tax, package resolution, explanation, citations, and production-shaped presentation. Box 8 claim-based identity minting is deferred by owner ruling and recorded in the plan as a named obligation for the first real-entry milestone.",
  "retrospective": "docs/milestone-retrospectives/2026-08-05-form1099div-box7-direct-ftc.md",
  "current_role": "Foreman (milestone closed out, PR open)",
  "current_prompt": "docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md"
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
foreign tax credit, the merged IRA line-4b route, and the bounded SSA-1099
Benefits Worksheet route through Form 1040 lines 6a/6b.

## Operational State: Engine Breadth

* **Active milestone:** 2025 SSA-1099 Benefits through the Social Security
  Benefits Worksheet and Form 1040 lines 6a/6b — complete and closed out to
  three durable commits plus closeout, open as a PR.
* **Current result:** the bounded SSA-1099 route is implemented through lines
  6a/6b, line 9, AGI, taxable income, regular tax, package resolution,
  explanation, citations, and production-shaped presentation. The current
  package graph is core **v28**, published **v23**, release **v21**, adoption
  **v28**, with the artifact-package successor and quantity-vocabulary schema
  admitted additively.
* **Plan:** `docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md`.
* **Prior closed (selected pointers):** the merged IRA line-4b route is an
  integration prerequisite for this SSA candidate; unrelated active work stays
  isolated on its own branch.
* **Contracts:** SSA Track 0 paper boundary and the reused source-family,
  closure, composition, resolver, citation, explanation, and presentation
  contracts; no new ADR. Statement identity is **logical statement + tax year**
  by owner decision of 2026-08-09 — milestone-scoped, and explicitly not a
  generalization of ADR-0015 beyond Form 1099-INT.
* **Next:** merge the PR, then select the next Engine Breadth milestone.
* **Deferred obligation:** deterministic claim-based statement-identity minting
  is not implemented. Statement sameness is enforced by the kernel's
  duplicate-entity guard but its derivation is delegated to whatever mints
  entity ids, and no artifact specifies that policy. Owner deferred Box 8
  claim-number authority on 2026-08-09; carry to the first real-entry
  milestone.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
