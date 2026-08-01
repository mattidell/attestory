<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, CONTRACT/ADVERSARY REVIEW CHARTERED.** The clean-room independent-family/direct-multi-read rival returned at `bbecd3f` (after self-correcting a P3 line7a-P circularity). The first committee reviewer measures both exact Builder outputs against accepted contracts and the same eleven Rung-1 cases, independently of the foreman's custody notes and the later expressiveness review. No repair is chartered. NEXT ACTION: launch the contract/adversary Reviewer; on return, the foreman takes custody and charters the isolated expressiveness review.",
  "current_role": "Contract/adversary Reviewer — compare both Rung 1 designs",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/charter-review-contract-adversary.md"
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
rival designs in hand and is entering committee review. No production
implementation has started.

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
* **Prototype progress:** both iterations complete.
  - Incumbent (`it1`, nested-identity/synthesized-conclusion): P1 and P2
    settled at Rung 1; P3 surfaced a real `attachment-rule.v2`
    threshold-only requirement-block gap plus two named design forks.
  - Rival (`it2`, independent-family/direct-multi-read): all three
    propositions settled at Rung 1; caught and resolved a box-2a-nonzero/
    Schedule-D-both-gain interaction the plan's completeness wording left
    ambiguous (P2-S5), and self-corrected a circular dependency in its
    original P3 selected-preferential-base definition before this review
    was chartered.
  - Committee review is entering its first pass: contract/adversary
    fidelity, chartered now; expressiveness review follows sequentially
    after it returns.
* **Next:** owner-launch the contract/adversary Reviewer against
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-review-contract-adversary.md`
  on branch `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing). On
  return, the foreman charters the isolated expressiveness review.
* **Branch line:** incumbent on
  `prototypes/schedule-d-covered-ltcg-8a/it1`; rival and now the review
  charter continuing on `prototypes/schedule-d-covered-ltcg-8a/it2`.
  Prototype code never merges to `main`; charters, designs, examinations, and
  reviews merge with the eventual accepted ADR decision unit.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
