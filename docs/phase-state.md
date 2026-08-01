<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, INCUMBENT ITERATION CHARTERED.** PR #136 merged as `a05d637`, approving the milestone and prototype plans. The nested-identity, synthesized-conclusion incumbent must answer P1-P3 against all eleven shared paper cases at Rung 1 only. Its branch, charter, outputs, and stop conditions are recorded in the topic SEAT file. No rival or reviewer is chartered. NEXT ACTION: owner-launch the incumbent Builder; on return, the foreman takes custody and charters the clean-room rival without exposing incumbent output.",
  "current_role": "Incumbent Builder — Rung 1 nested-identity, synthesized-conclusion design",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/charter-it1.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a, the bounded 2025 Schedule K-1 (Form 1065) box-5
taxable-interest path through line 2b and Schedule B Part I, and the bounded
2025 payer-reported current-inclusion market-discount class in Form 1099-INT
box 10 or Form 1099-OID box 5. The next breadth slice, Covered Long-Term
Gains through Schedule D line 8a, is planned and its prototype Track 0 is
chartered; no production implementation has started.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned; Track 0 in flight.**
* **Product change (target):** covered, long-term, gain-only Form 1099-B
  transactions become a closed source family that reaches Schedule D line 8a,
  Part II line 15, Part III line 16, Form 1040 line 7a, and the correct
  QDCG-computed line-16 tax, with a real Schedule D attachment disposition,
  explanation walk, and presentation section.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  — merged on `main` in PR #136. Prototype plan:
  `docs/prototypes/schedule-d-covered-ltcg-8a/plan.md` — owner-approved,
  merged in the same PR.
* **Scope:** covered, long-term, gain-only, no-adjustment 1099-B transactions
  reported directly on Schedule D line 8a without Form 8949; short-term
  transactions, losses, carryovers, Form 8949, noncovered securities, digital
  assets, and other Schedule D sources remain outside it.
* **Next:** owner-launch the incumbent prototype Builder against
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-it1.md` on branch
  `prototypes/schedule-d-covered-ltcg-8a/it1`. On return, the foreman charters
  the clean-room rival without exposing incumbent output.
* **Branch line:** Track 0 charter committed on
  `prototypes/schedule-d-covered-ltcg-8a/it1`, branched from `origin/main` at
  `a05d637`. Prototype code never merges to `main`; charters, designs,
  examinations, and reviews merge with the eventual accepted ADR decision
  unit.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
