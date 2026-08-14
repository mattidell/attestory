<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "ssa-no-activity-applicability",
  "active_plan": "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md",
  "milestone_state": "closed",
  "status": "Closed 2026-08-14 (PR #173, merged at 05ddd777). Independent review returned APPROVE WITH FINDINGS (both findings closed) and CI (verify) is green on the exact merged head. Shipped: rule.ss-benefits-worksheet v2, the sole producer of tax.us.2025.social-security.line6b, publishing the canonical zero on a closed-empty SSA source family without reading or pinning the 22 worksheet-only scope declarations. no-rrb-or-foreign-social-benefit is retained (load-bearing, T0-1 answered 33 -> 1) and recorded as a fourteenth migration candidate for Milestone 2. Publication generation: package.core-calculations.v30 / published-packages.v25 / demo.release.2025.v23 / adopt-core-v30-current. Full arc distilled in the retrospective, not carried here.",
  "retrospective": "docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md",
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
The SSA no-activity applicability repair closes a defect on that last SSA
route: a return with no Social Security source can now reach total income
without answering 33 Social Security declarations.

## Operational State: Engine Breadth

* **Just-closed milestone:** SSA no-activity applicability repair — **closed
  2026-08-14** (PR #173, `05ddd777`). Milestone 1 of the owner-approved
  two-milestone prerequisite standing between the engine and Form 1098-E
  student-loan interest.
* **Objective, met:** a return with no applicable Social Security source
  publishes the legally authorized line-6 zero and proceeds through line 9
  without satisfying worksheet-only scope declarations.
* **The defect, repaired:** `rule.ss-benefits-worksheet` was the **only**
  producer of `tax.us.2025.social-security.line6b` corpus-wide and carried
  **33** `requires`, while `rule.form1040-line9.v7` requires line 6b
  **unconditionally** — so every return in the engine had to satisfy 33
  Social Security declarations to reach total income.
* **The shipped contract:** `rule.ss-benefits-worksheet` **v2** under
  `rule-artifact.v4`, the **sole** producer of line 6b. Eleven unconditional
  `requires` (the retained declaration, the seven derived numeric inputs,
  `social-security.line6a`, `filing_status`, `rounding.convention`); an
  ADR-0037 `conditional_dependency_set` of **22** worksheet-only declarations
  gated on `count > 0`; unconditional `require_closed` on **both** routes; a
  value-level `choose` selecting canonical `0` or the **unchanged** v1
  worksheet expression.
* **T0-1 answered 33 → 1:** `no-rrb-or-foreign-social-benefit` is load-bearing
  and is retained, active on both routes. It is recorded as a **fourteenth**
  migration candidate for Milestone 2 and was **not acted on** in Milestone 1.
* **Publication generation:** `package.core-calculations.v30` /
  `published-packages.v25` / `demo.release.2025.v23` / `adopt-core-v30-current`.
  `ss-benefits-scope` stays at its base **v1** everywhere: no vocabulary
  successor exists. A withdrawn `bundle.v2` and the `package_validation`
  check-10a root cause it exposed are repaired and fully distilled into the
  retrospective.
* **Coordination item for Milestone 2 is retracted.** Its predecessor
  population is `ss-benefits-scope` **v1**, as it always was on the ratified
  line — not v2.
* **Posture:** content-level for the worksheet contract itself. No new schema
  family, no ledger entry, **no ADR owed**.
* **Independent review:** APPROVE WITH FINDINGS, both findings closed. CI
  `verify` green on the exact merged head.
* **Plan:** `docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md`.
* **Split record:** `docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md` (PR #172, closed — historical input, not authority).

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
