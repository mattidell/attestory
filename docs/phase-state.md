<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "k1-interest-breadth",
  "active_plan": "docs/phases/engine-breadth/milestones/k1-interest-breadth.md",
  "milestone_state": "track-1",
  "status": "**ENGINE BREADTH / SCHEDULE K-1 BOX-5 INTEREST — CLOSING CI REPAIR CHARTERED.** The independent review returned READY, but closing PR #133 exposed one stale historical test expectation: the current line-2b field is v3 while the test still expects v2. A one-file Builder repair is next.",
  "current_role": "Builder (K-1 closing CI stale expectation repair)",
  "current_prompt": "docs/reviews/charter-2026-07-31-k1-interest-breadth-ci-repair.md"
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
taxable-interest path through line 2b and Schedule B Part I. Its integrated
review is READY; the closing CI gate found one stale test expectation before
the milestone could merge.

## Operational State: Engine Breadth

* **Active Milestone:** Schedule K-1 Box-5 Interest Breadth — **closing CI repair.**
* **Product change:** independently reviewed `READY`; not yet merged because one historical test still expects the superseded current field version.
* **Plan:** `docs/phases/engine-breadth/milestones/k1-interest-breadth.md`.
* **Scope:** Form 1065 K-1 box 5 only; market discount, adjustments, other K-1s, and Schedule D remain outside it.
* **Evidence:** PR #133 CI completed 781 tests and failed only `tests/test_dsbs_t1_schema_citizens.py:227` (`v3` actual versus stale `v2` expected).
* **Next:** apply the chartered one-file test repair, restore closed records, and rerun PR #133 `verify`.
* **Branch line:** engine work continues on `main` through `milestone/k1-interest-breadth`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
