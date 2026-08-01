<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, EXPRESSIVENESS REVIEW CHARTERED.** The contract/adversary review returned NOT READY at `4fa6c10`: decision-blocking findings CA-01 (incumbent P1 admits a broader eligible class than the source-class charter permits), CA-02 (box-2a closed-nonempty is an unresolved scope contract in both designs; the rival's P2-S5 resolution is sound but needs explicit owner adoption), CA-03 (incumbent P3 omits a required QDCG input and full correction chain), and CA-04 (rival P3's route-neutral selected-base symbol hides route-sensitive ADR-0050 pins with no exact contract for where they live). CA-05/06/07 are separate-decision schema/substrate prerequisites, not blocking this charter. The second committee reviewer independently measures case-by-case recoverability, pinned to the same exact objects, without reading the first review. No repair is chartered. NEXT ACTION: launch the expressiveness Reviewer; on return, the foreman takes custody, compares both sealed reviews, and performs Gate-5 triage before recommending a disposition to the owner.",
  "current_role": "Expressiveness Reviewer — recover both Rung 1 designs case by case",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/charter-review-expressiveness.md"
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
Gains through Schedule D line 8a, is planned; its prototype Track 0 has both
rival designs and the first committee review in hand (NOT READY), and the
second review is entering. No production implementation has started.

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
* **Prototype progress:** both iterations complete; first committee review
  complete and **NOT READY**.
  - Incumbent (`it1`): decision-blocking on all three propositions (CA-01,
    part of CA-02, CA-03).
  - Rival (`it2`): P1 sufficient; P2 conditionally sufficient pending owner
    adoption of its box-2a boundary successor (CA-02); P3 decision-blocking
    on an unresolved pin contract (CA-04). Two schema/substrate gaps
    (CA-05, CA-06) are separately scored, not blocking.
  - Expressiveness review chartered next, pinned to the same exact objects
    (incumbent `d4e2203`, rival `bbecd3f`), independent of the first
    review's findings.
* **Next:** owner-launch the expressiveness Reviewer against
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-review-expressiveness.md`
  on branch `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing). On
  return, the foreman compares both sealed reviews and performs Gate-5
  triage before recommending a disposition (repair, partial ratification, or
  recharter) to the owner.
* **Branch line:** incumbent on
  `prototypes/schedule-d-covered-ltcg-8a/it1`; rival, both review charters,
  and the first review continuing on
  `prototypes/schedule-d-covered-ltcg-8a/it2`. Prototype code never merges to
  `main`; charters, designs, examinations, and reviews merge with the
  eventual accepted ADR decision unit.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
