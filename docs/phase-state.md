<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — TRACK 0, CONTRACT SYNTHESIS CHARTERED.** Repair 1 is independently confirmed READY at `b6dabec` (CA-02 and CA-04 both confirmed against the exact repaired sentences, not the self-report; the P1/P2/P3 regression boundary is intact; CA-05/CA-06 correctly left as separately tracked production conditions). Track 0's evidence chain is complete: incumbent it1, rival it2, both committee reviews, repair1, and its confirmation. Contract synthesis is chartered on a fresh `decisions/schedule-d-covered-ltcg-8a` branch to draft proposed ADR-0052 from the full evidence chain. NEXT ACTION: launch the Contract Synthesis Builder; on return, the foreman prepares the ADR for owner review and ratification, then closes Track 0 and hands off to the milestone's production Tracks 1-4.",
  "current_role": "Contract Synthesis Builder — draft proposed ADR-0052",
  "current_prompt": "docs/prototypes/schedule-d-covered-ltcg-8a/charter-contract-synthesis.md"
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
Gains through Schedule D line 8a, is planned; its prototype evidence chain is
complete and a proposed successor ADR is being drafted for owner
ratification. No production implementation has started.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned; Track 0 contract synthesis in flight.**
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
* **Prototype evidence chain (complete):** incumbent (`it1`, rejected) →
  rival (`it2`, selected) → contract/adversary review (`NOT READY`) →
  expressiveness review (`READY` for rival, one recorded dissent on CA-04) →
  owner disposition (rival topology, CA-02/P2-S5 adopted, CA-04 repair
  authorized) → repair 1 → confirmation review (**READY**). Full record:
  `docs/prototypes/schedule-d-covered-ltcg-8a/round-1-triage.md` and
  `reviews/repair1-confirmation.md`.
* **Next:** owner-launch the Contract Synthesis Builder against
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-contract-synthesis.md`
  on branch `decisions/schedule-d-covered-ltcg-8a`. On return, the foreman
  prepares proposed ADR-0052 for owner review and ratification (merge to
  `main` is the ratification record), then closes Track 0 and hands off to
  production Tracks 1-4.
* **Branch line:** prototype evidence on
  `prototypes/schedule-d-covered-ltcg-8a/it1` and `.../it2`; contract
  synthesis on the new `decisions/schedule-d-covered-ltcg-8a` branch, cut
  from `origin/main`. Prototype code never merges to `main`; the plan,
  charters, designs, examinations, reviews, the triage record, and the
  proposed ADR merge together as one decision unit once ratified.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
