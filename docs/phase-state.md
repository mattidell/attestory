<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "declarative-validation-substrate-f8949",
  "active_plan": "docs/phases/engine-breadth/milestones/declarative-validation-substrate.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / DECLARATIVE STRUCTURED VALIDATION AND CONSUMER DEPENDENCIES — CLOSED 2026-08-17.** Tax policy for the bounded 2025 covered-W Form 8949/Schedule D subsystem moved out of generic Python into versioned content (ADR-0066): a closed predicate grammar for member constraints, declared cross-family identity exclusivity, and reachability-derived consumer prerequisites. runner.py's domain references went from 24 to 0. The superseded hard-coded Form 8949 row guards and Form 1099-B identity-collision matrix are deleted, not bypassed. Both schedulers are proven byte-identical on the migrated content, including attachment-bearing citizens. An independent owner-advisor product review returned ACCEPT after repairing a failing type gate and a stale cross-milestone test; Track 3's independent review is reconfirmed ACCEPTED. Final package is the additive union core v32 / published v27 / release v25 / adopt v32. Retrospective: docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md. Next milestone unselected.",
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
validation and consumer dependency substrate — the prerequisite that moved
Form 8949's per-member validation and cross-family identity checks out of
generic runner code into versioned content — is now closed. **Neither
prerequisite adds a new tax route.**

## Operational State: Engine Breadth

* **Active milestone:** none selected.
* **Current product behavior:** registry-valid but unsupported semantic
  package members and unknown presentation-bound successors fail loudly. The
  declarative-validation substrate (ADR-0066) is production, not prototype:
  Form 8949's member constraints and identity exclusivity are versioned
  content, reachability-derived consumer prerequisites are mechanically
  required, and both schedulers agree on the result. The ratified package is
  core **v32**, published **v27**, release **v25**, adoption **v32**.
* **Paused dependency:** `milestone/f8949-noncovered-basis-lines2-9`; its
  proposed decisions are not authority and no implementation is chartered.
* **Prior milestone:** Declarative Structured Validation and Consumer
  Dependency Substrate — closed 2026-08-17; Candidate B P1-P3 ratified into
  ADR-0066; final package core v32/published v27/release v25/adopt v32.
  Plan: `docs/phases/engine-breadth/milestones/declarative-validation-substrate.md`;
  deferral ledger:
  `docs/phases/engine-breadth/milestones/declarative-validation-substrate-deferral-ledger.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-17-declarative-validation-substrate.md`.
* **Next:** owner selects the next milestone from
  `docs/phases/engine-breadth/coverage-frontier.md`. The Form 1098-E vertical
  slice (Schedule 1 lines 21/26, Form 1040 line 10, AGI 11a/11b) remains the
  next unselected breadth candidate. The scoped-not-built
  rule-artifact/attachment-rule capability-table consolidation
  (`milestones/rule-artifact-capability-table-consolidation.md`) is a
  hardening candidate, not breadth.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
