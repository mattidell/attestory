<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — PLANNED.** The milestone plan and its prototype plan are committed on `milestone/schedule-d-covered-ltcg-8a`, proposing the plan PR. No track has started. The prototype plan needs owner approval before Track 0 (paper-first incumbent/rival evidence for transaction identity and the completeness boundary, plus a paper spike for the Schedule D content/QDCG binding) may charter.",
  "current_role": "Foreman (prototype plan awaiting owner approval; no track chartered)",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/plan.md"
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
Gains through Schedule D line 8a, is selected and planned; no implementation
has started.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned.**
* **Product change (target):** covered, long-term, gain-only Form 1099-B
  transactions become a closed source family that reaches Schedule D line 8a,
  Part II line 15, Part III line 16, Form 1040 line 7a, and the correct
  QDCG-computed line-16 tax, with a real Schedule D attachment disposition,
  explanation walk, and presentation section.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  — **planned, not yet merged.** Prototype plan:
  `docs/prototypes/schedule-d-covered-ltcg-8a/plan.md` — **proposed, awaiting
  owner approval.**
* **Scope:** covered, long-term, gain-only, no-adjustment 1099-B transactions
  reported directly on Schedule D line 8a without Form 8949; short-term
  transactions, losses, carryovers, Form 8949, noncovered securities, digital
  assets, and other Schedule D sources remain outside it.
* **Next:** owner reviews and approves the plan PR (milestone plan +
  prototype plan). Once merged, the foreman charters Track 0's paper-first
  incumbent/rival evidence for transaction identity (P1) and the
  completeness-boundary declaration shape (P2), plus a paper spike for the
  Schedule D content/QDCG binding (P3).
* **Branch line:** proposed on `milestone/schedule-d-covered-ltcg-8a`, branched
  from `origin/main` at `0a744b5`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
