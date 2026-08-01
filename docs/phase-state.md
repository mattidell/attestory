<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "k1-interest-breadth",
  "active_plan": "docs/phases/engine-breadth/milestones/k1-interest-breadth.md",
  "milestone_state": "track-1",
  "status": "**ENGINE BREADTH / SCHEDULE K-1 BOX-5 INTEREST — BUILT, AWAITING REVIEW.** The integrated Builder completed the K1-C1–C5 implementation and committed a clean handoff. The exact-range independent review is chartered next.",
  "current_role": "Reviewer (integrated K-1 interest breadth independent review)",
  "current_prompt": "docs/reviews/charter-2026-07-31-k1-interest-breadth-review.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a. The selected breadth slice for 2025 Schedule K-1
(Form 1065) box-5 taxable interest has been built through line 2b, Schedule B,
package resolution, and presentation; its independent review is next.

## Operational State: Engine Breadth

* **Active Milestone:** Schedule K-1 Box-5 Interest Breadth — **built, awaiting review.**
* **Product change:** integrated implementation committed; not yet independently reviewed or merged.
* **Plan:** `docs/phases/engine-breadth/milestones/k1-interest-breadth.md`.
* **Scope:** Form 1065 K-1 box 5 only; market discount, adjustments, other K-1s, and Schedule D remain outside it.
* **Next:** run the exact-range independent integrated review; one bounded repair cycle is available if findings require it.
* **Branch line:** engine work continues on `main` through `milestone/k1-interest-breadth`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
