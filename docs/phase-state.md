<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "declarative-validation-substrate-f8949",
  "active_plan": "docs/phases/engine-breadth/milestones/declarative-validation-substrate.md",
  "milestone_state": "track-2",
  "status": "**ENGINE BREADTH / DECLARATIVE STRUCTURED VALIDATION AND CONSUMER DEPENDENCIES — TRACK 2 REPAIR 7 CHARTERED.** Repair 6 closes single-entry self and mutual projection cycles, but independent review found multi-entry convergence on one cycle remains hash-seed-dependent and can silently drop one required origin. Repair 7 is confined to deterministic complete multi-entry cycle closure.",
  "current_role": "Track 2 Deterministic Multi-Entry Cycle Closure Repair Builder 7",
  "current_prompt": "docs/prototypes/declarative-validation-substrate/charter-track-2-repair-7.md"
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
migration artifact that retires the old ones. The active milestone is the
owner-selected prerequisite that makes structured validation, cross-family
identity constraints, and their consumer dependencies declarative. It begins
with a paper/static Track 0 and stops for owner contract ratification before
production implementation. **Neither prerequisite adds a new tax route.**

## Operational State: Engine Breadth

* **Active milestone:** Declarative Structured Validation and Consumer
  Dependency Substrate; Candidate B P1-P3 is owner-ratified and distilled in
  accepted ADR-0066. Track 1 is accepted. Track 2 repair 7 is chartered after
  Repair 6 review found hash-seed-dependent multi-entry convergence on a
  shared projection cycle; every single-entry and noncycle case passed.
* **Current product behavior:** registry-valid but unsupported semantic package
  members and unknown presentation-bound successors fail loudly. The generic
  declarative-validation substrate is implemented on the milestone branch but
  projected scalar-family reachability is not yet safe for 2025 adoption. The
  ratified package remains core **v31**, published **v26**, release **v24**,
  adoption **v31**.
* **Defect in scope:** Form 8949 row guards and Form 1099-B identity collision
  policy are hard-coded in generic runner/package-validator paths and repeated
  by known consumers; Schedule D attachment can omit the same validation.
* **Plan:** `docs/phases/engine-breadth/milestones/declarative-validation-substrate.md`.
* **Paused dependency:** `milestone/f8949-noncovered-basis-lines2-9`; its
  proposed decisions are not authority and no implementation is chartered.
* **Prior milestone:** Fact-type succession with neutral Schedule 1 vocabulary
  — closed 2026-08-14 (PR #177); ADR-0063 and package **v31** shipped.
* **Next:** launch the Track 2 Repair Builder 7 from
  `docs/prototypes/declarative-validation-substrate/charter-track-2-repair-7.md`.
  Numerical iteration caps are suspended by live owner direction; evidence
  and safety boundaries remain.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
