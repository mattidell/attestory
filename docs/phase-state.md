<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "capital-gain-distributions-line7a",
  "active_plan": "docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md",
  "milestone_state": "track-3",
  "status": "**ENGINE BREADTH / CAPITAL-GAIN DISTRIBUTIONS LINE 7A — TRACK 3 FINDINGS-ONLY REPAIR CHARTERED.** Independent review commit 22f281e8094fa126a5424949e01478e15504d11c returned NOT READY on three bounded fail-closed projector defects. The single allowed repair is limited to generic categorical-value and exact field-citation validation plus focused tests; valid goldens and browser artifacts remain frozen.",
  "current_role": "Track 3 Presentation Repair Builder",
  "current_prompt": "docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3-repair.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The active Engine Breadth milestone adds one bounded valid-return class:
Form 1099-DIV box 2a capital-gain distributions reported directly on Form 1040
line 7a when contributed authority says Schedule D is not required. The
contract, source family, declared computation, and line-7b prerequisite are on
`main`. Track 3 now carries the two new fields through the existing synthetic
presentation surface before completion records are prepared.

## Operational State: Capital-Gain Distributions and Line 7a

* **Active Milestone:** Capital-Gain Distributions and Form 1040 Line 7a
* **Current Track:** Track 3 — independent presentation review
* **Ratified contract:** ADR-0050
* **Merged prerequisite:** PR #125, with CI `verify` green
* **Remaining sequence:** independent Track-3 review, then Track 4 completion records

### Standing Directives

* **Synthetic boundary:** No real-data run, real browser/workspace session, or
  maturity claim belongs in this milestone.
* **Breadth boundary:** The direct line-7a class does not add Schedule D,
  Form 8949, Form 1099-B, or general capital-gains support.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
