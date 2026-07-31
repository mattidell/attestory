<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "capital-gain-distributions-line7a",
  "active_plan": "docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md",
  "milestone_state": "track-4",
  "status": "**ENGINE BREADTH / CAPITAL-GAIN DISTRIBUTIONS LINE 7A — TRACK 4 ONE-RECORD F1 REPAIR RETURNED; FOCUSED RECHECK CHARTERED.** The repair adds the omitted Schedule B Part I multi-family interest obligation and trigger to the new deferral ledger. The original Completion Reviewer now rechecks only F1; all other completion-review measurements remain credited.",
  "current_role": "Track 4 Completion Repair Recheck Reviewer",
  "current_prompt": "docs/reviews/charter-2026-07-31-capital-gain-distributions-line7a-track4-completion-repair-recheck.md"
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
`main`. Track 3's reviewed branch evidence carries the two new fields through
the existing synthetic presentation surface and its focused repair recheck is
`READY`. Track 4 completion records are now prepared for a fresh independent
review; they are not yet merged or closed.

## Operational State: Capital-Gain Distributions and Line 7a

* **Active Milestone:** Capital-Gain Distributions and Form 1040 Line 7a
* **Current Track:** Track 4 — completion records prepared for review
* **Ratified contract:** ADR-0050
* **Merged prerequisite:** PR #125, with CI `verify` green
* **Remaining sequence:** fresh completion review, closing PR and CI, owner
  merge, mechanical post-merge closeout

### Standing Directives

* **Synthetic boundary:** No real-data run, real browser/workspace session, or
  maturity claim belongs in this milestone.
* **Breadth boundary:** The direct line-7a class does not add Schedule D,
  Form 8949, Form 1099-B, or general capital-gains support.
* **Evidence boundary:** Synthetic completion is bounded to the selected
  direct-reporting class and is not a real-data, filing-readiness, or maturity
  claim.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
