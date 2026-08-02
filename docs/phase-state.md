<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, REPAIR CHARTERED.** Owner disposition (2026-08-01): rival topology selected (independent-family P1, direct-multi-read P2, selected-preferential-base P3); incumbent not carried forward. CA-02/P2-S5 adopted as the completeness-boundary successor (box-2a must be closed, not closed-empty; a closed-nonempty amount contributes once via Schedule D line 13). CA-04 repair authorized, spending the plan's single fixed repair pass. The Repair Builder (rival continuity) must state P2-S5 as an explicit successor sentence and supply an exact pin contract for how ADR-0050's route-specific direct pins attach to the route-neutral `P` symbol. NEXT ACTION: launch the Repair Builder; on return, the foreman charters one focused confirmation reviewer.",
  "current_role": "Repair Builder — CA-02 explicit successor sentence and CA-04 exact pin contract",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/charter-repair1.md"
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
Gains through Schedule D line 8a, is planned; the owner has selected the
rival prototype topology and authorized one bounded repair before contract
synthesis. No production implementation has started.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned; Track 0 repair in flight.**
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
* **Prototype progress:** owner disposition recorded in `round-1-triage.md`
  (2026-08-01):
  - Rival topology selected; incumbent not carried forward.
  - Completeness boundary successor adopted (CA-02/P2-S5): box-2a must be
    closed, not closed-empty, for this bounded class; a nonzero closed
    amount contributes once via Schedule D line 13.
  - CA-04 repair authorized (spends the plan's single fixed repair pass):
    the rival Builder must state P2-S5 as an explicit numbered successor
    sentence and supply an exact pin contract for how ADR-0050's
    route-specific direct pins attach to the shared, route-neutral `P`
    symbol.
* **Next:** owner-launch the Repair Builder against
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-repair1.md` on branch
  `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing). On return, the
  foreman charters one focused confirmation reviewer covering only CA-02,
  CA-04, and regression of the already-settled P1/P2/P3 boundaries.
* **Branch line:** incumbent on
  `prototypes/schedule-d-covered-ltcg-8a/it1`; rival, both reviews, the
  triage record, and now the repair charter continuing on
  `prototypes/schedule-d-covered-ltcg-8a/it2`. Prototype code never merges to
  `main`; charters, designs, examinations, reviews, and the triage record
  merge with the eventual accepted ADR decision unit.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
