<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, GATE-5 TRIAGE COMPLETE, OWNER DISPOSITION NEEDED.** Both prototype iterations and both committee reviews are complete. Both reviews converge on the rival topology (independent-family P1, direct-multi-read P2, selected-preferential-base P3) and independently corroborate the incumbent's defects (narrow P1 eligibility predicate, dropped box-2a gain in the both-gain case, missing QDCG input). They dissent on the rival's P3: the contract/adversary review calls the route-neutral `P` symbol's missing ADR-0050 pin-attachment sentence decision-blocking (CA-04); the expressiveness review reaches READY without addressing that specific question. Full record: `docs/prototypes/schedule-d-covered-ltcg-8a/round-1-triage.md`. NEXT ACTION: owner disposition on (1) rival topology selection, (2) CA-02/P2-S5 completeness-boundary adoption, (3) CA-04 repair authorization. No repair is chartered yet.",
  "current_role": "Foreman (Gate-5 triage complete; owner disposition needed before repair charter)",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/round-1-triage.md"
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
rival designs and both committee reviews in hand, and now needs an owner
disposition before a repair pass and contract synthesis. No production
implementation has started.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned; Track 0 in flight, awaiting owner disposition.**
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
* **Prototype progress:** both iterations and both reviews complete. Gate-5
  triage recorded in `round-1-triage.md`:
  - Both reviews converge on the rival topology; incumbent is not
    recommended to carry forward.
  - CA-02: rival's box-2a boundary successor (P2-S5) needs explicit owner
    adoption — it changes the plan's stated "closed empty" wording to
    "closed," with a nonzero amount contributing once via Schedule D
    line 13.
  - CA-04 (dissent): whether the rival's shared `P` symbol has a settled
    home for ADR-0050's route-specific pins. Contract/adversary review says
    no (decision-blocking); expressiveness review's READY doesn't test the
    question. Not resolved here — recorded as open dissent per project
    protocol.
* **Next:** owner reviews `round-1-triage.md` and dispositions topology
  selection, CA-02 adoption, and CA-04 repair authorization. Only then does
  the foreman charter the bounded repair pass (the plan's single authorized
  pass), assigned to the rival Builder for design continuity.
* **Branch line:** incumbent on
  `prototypes/schedule-d-covered-ltcg-8a/it1`; rival, both review charters,
  both reviews, and the triage record continuing on
  `prototypes/schedule-d-covered-ltcg-8a/it2`. Prototype code never merges to
  `main`; charters, designs, examinations, reviews, and the triage record
  merge with the eventual accepted ADR decision unit.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
