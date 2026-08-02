<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "track-0",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0 COMPLETE, RATIFIED.** ADR-0052 (independent anchor-keyed transaction family; nine-part direct-read completeness boundary with the adopted box-2a-closed successor; Schedule D content as an ADR-0036 instantiation; a shared selected-preferential-base symbol with an exact confirmed pin contract; named CA-05/CA-06 production conditions carried forward, not resolved) is accepted and on `main` (PR #137, owner ratification 2026-08-02). NEXT ACTION: charter production Track 1 (transaction source, identity, and versioned citizens).",
  "current_role": "Foreman (Track 0 ratified; production Track 1 not yet chartered)",
  "current_prompt": "docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md"
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
Gains through Schedule D line 8a, has an owner-ratified successor contract
(ADR-0052) on `main`; production has not started.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned; Track 0 complete and ratified.**
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
* **Accepted contract (ADR-0052, `main`):**
  - independent, anchor-keyed transaction identity one level below the
    existing statement-identity pattern;
  - a nine-part completeness boundary read directly (two closures plus
    seven categorical absence declarations), with box-2a required to be
    closed (not closed-empty) as an explicit adopted successor;
  - Schedule D line 8a/13/15/16 as content on the existing attachment
    ontology (ADR-0036) — no new mechanism;
  - a shared `selected-preferential-base` symbol with an exact,
    independently confirmed per-producer pin contract, resolving the one
    recorded committee dissent (CA-04);
  - two named production conditions carried forward, not resolved by this
    ADR: a categorical attachment-requirement schema successor (CA-05) and
    generic exactly-one-producer enforcement (CA-06).
* **Next:** charter production Track 1 (transaction source, identity, and
  versioned citizens, per the milestone plan's Tracks section).
* **Branch line:** the accepted decision unit (evidence chain, ADR-0052,
  index row) is on `main` via PR #137. Prototype code never merged; the
  ephemeral `prototypes/schedule-d-covered-ltcg-8a/it1` and `.../it2`
  branches remain for now and may be deleted per `PROJECT_PLANNING.md`
  ("Milestone Start") once no longer needed for re-derivation.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
