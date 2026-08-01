<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "k1-interest-breadth",
  "active_plan": "docs/phases/engine-breadth/milestones/k1-interest-breadth.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / SCHEDULE K-1 BOX-5 INTEREST — CLOSED.** The engine computes the bounded 2025 Form-1065 K-1 box-5 taxable-interest path through Form 1040 line 2b, composition-complete Schedule B Part I, downstream results, package resolution, explanation, and presentation on production-shaped synthetic evidence. The independent review returned READY.",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/engine-breadth/coverage-frontier.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a and the bounded 2025 Schedule K-1 (Form 1065) box-5
taxable-interest path through line 2b and Schedule B Part I. Both paths are
synthetic complete; no next breadth slice has been selected.

## Operational State: Engine Breadth

* **Completed Milestone:** Schedule K-1 Box-5 Interest Breadth — **closed.**
* **Product change:** Form-1065 K-1 box-5 taxable interest is a closed fifth positive-interest family, and Schedule B Part I now itemizes the complete adopted interest composition.
* **Plan:** `docs/phases/engine-breadth/milestones/k1-interest-breadth.md`.
* **Scope:** Form 1065 K-1 box 5 only; market discount, adjustments, other K-1s, and Schedule D remain outside it.
* **Evidence:** production-shaped synthetic coordinator, lifecycle, package, explanation, and presentation cases; independent review `READY`.
* **Next:** select the next bounded engine-breadth slice from `docs/phases/engine-breadth/coverage-frontier.md`.
* **Branch line:** engine work continues on `main`; no successor milestone branch is selected.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
