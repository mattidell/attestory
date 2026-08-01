<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "k1-interest-breadth",
  "active_plan": "docs/phases/engine-breadth/milestones/k1-interest-breadth.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / SCHEDULE K-1 BOX-5 INTEREST — PLANNED.** The owner selected the bounded 2025 Form-1065 K-1 box-5 interest slice and a streamlined integrated build/review. The plan and Builder work packet are prepared; implementation has not begun.",
  "current_role": "Builder (integrated K-1 interest breadth implementation)",
  "current_prompt": "docs/reviews/charter-2026-07-31-k1-interest-breadth-builder.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a. The next selected breadth slice adds 2025 Schedule
K-1 (Form 1065) box-5 taxable interest to line 2b and Schedule B. Its plan and
integrated Builder work packet are ready; implementation has not begun.

## Operational State: Engine Breadth

* **Active Milestone:** Schedule K-1 Box-5 Interest Breadth — **planned.**
* **Product change:** none.
* **Plan:** `docs/phases/engine-breadth/milestones/k1-interest-breadth.md`.
* **Scope:** Form 1065 K-1 box 5 only; market discount, adjustments, other K-1s, and Schedule D remain outside it.
* **Next:** run the integrated Builder charter, then one independent integrated review.
* **Branch line:** engine work continues on `main` through `milestone/k1-interest-breadth`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
