<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, REPAIR CONFIRMATION CHARTERED.** Repair 1 returned at `e6747fd`, claiming CA-02 resolved (P2-S5A: box-2a must be closed, not closed-empty, for this bounded class; a closed-nonempty amount contributes once via Schedule D line 13) and CA-04 resolved (P3-S8: an exact TAX16 pin contract keyed to which producer — direct or Schedule-D — currently backs the route-neutral `P` symbol, requiring no first-class route tag). A focused, author-independent Confirmation Reviewer is chartered to falsify these claims and check regression of the already-settled P1/P2/P3 boundaries, without reopening topology selection or CA-05/CA-06. NEXT ACTION: launch the Confirmation Reviewer; on return, the foreman proceeds to contract synthesis if READY, or reports a spent repair pass to the owner if NOT READY.",
  "current_role": "Confirmation Reviewer — falsify CA-02/CA-04 repair, check regression",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/charter-repair1-confirmation.md"
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
Gains through Schedule D line 8a, is planned; the owner-authorized repair has
returned and now needs independent confirmation before contract synthesis.
No production implementation has started.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned; Track 0 repair confirmation in flight.**
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
* **Repair result:** the rival Builder's repair (`e6747fd`) claims:
  - **CA-02 resolved:** P2-S5A is a standalone numbered successor sentence
    superseding the plan's "closed empty" boundary wording; closed-empty
    still contributes zero, closed-nonempty contributes once via Schedule D
    line 13.
  - **CA-04 resolved:** P3-S8 gives an exact `TAX16` pin contract per `P`
    producer signature (`P-direct` keeps ADR-0050 Decision 7's original
    branch pins; `P-schedule-d` adds none of them), with no route tag needed
    because the producer signature is recoverable from direct pin lineage.
    CA-06 (generic exactly-one-producer representation) remains separately
    tracked, not resolved here.
* **Next:** owner-launch the Confirmation Reviewer against
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-repair1-confirmation.md`
  on branch `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing). On
  return, the foreman takes custody. `READY` moves to contract synthesis;
  `NOT READY` spends the plan's fixed repair cap and returns to the owner.
* **Branch line:** incumbent on
  `prototypes/schedule-d-covered-ltcg-8a/it1`; rival, both reviews, the
  triage record, the repair, and now the confirmation charter continuing on
  `prototypes/schedule-d-covered-ltcg-8a/it2`. Prototype code never merges to
  `main`; charters, designs, examinations, reviews, and the triage record
  merge with the eventual accepted ADR decision unit.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
