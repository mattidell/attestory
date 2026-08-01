<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, CLEAN-ROOM RIVAL CHARTERED.** The incumbent (`it1`, nested-identity/synthesized-conclusion) returned: P1 and P2 settled at Rung 1; P3's paper spike named a genuine `attachment-rule.v2` requirement-block schema gap and two design forks (D1-vs-box-2a precedence, QDCG unconditional-eligibility) for committee scrutiny. The clean-room rival (`it2`, independent-family/direct-multi-read) is chartered on a branch cut from `main`, with no incumbent exposure. NEXT ACTION: owner-launch the rival Builder; on return, the foreman prepares the two independent committee review charters.",
  "current_role": "Rival Builder — Rung 1 independent-family, direct-multi-read design",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/charter-it2.md"
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
Gains through Schedule D line 8a, is planned and its prototype Track 0's
incumbent iteration is complete; the clean-room rival is chartered. No
production implementation has started.

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
* **Prototype progress:** incumbent iteration (`it1`) complete on
  `prototypes/schedule-d-covered-ltcg-8a/it1`. P1 (transaction identity) and
  P2 (completeness boundary) settled at Rung 1 with only non-blocking
  future-slice questions named. P3's paper spike (Schedule D content/QDCG
  binding) surfaced a real generality gap in `attachment-rule.v2` (threshold-
  only requirement block cannot express a categorical Schedule D
  disposition) plus two named design forks flagged for committee/owner
  scrutiny rather than asserted as settled.
* **Next:** owner-launch the clean-room Rival Builder against
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-it2.md` on branch
  `prototypes/schedule-d-covered-ltcg-8a/it2`. On return, the foreman
  prepares the independent contract/adversary and expressiveness review
  charters without exposing either reviewer to the other's work.
* **Branch line:** incumbent charter and outputs on
  `prototypes/schedule-d-covered-ltcg-8a/it1`; rival charter on
  `prototypes/schedule-d-covered-ltcg-8a/it2`, cut clean from `origin/main`
  at `a05d637`. Prototype code never merges to `main`; charters, designs,
  examinations, and reviews merge with the eventual accepted ADR decision
  unit.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
