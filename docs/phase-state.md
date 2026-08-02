<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a — PLANNED.** The milestone plan has been reconstructed on one milestone branch from the preserved pre-curation snapshot. Contract evidence and completed Track 1 will be restored as separate commits before Track 2 resumes.",
  "current_role": "Foreman (curate recovered contract evidence before production resumes)",
  "current_prompt": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The engine computes the bounded direct-reporting path for Form 1099-DIV box 2a
through Form 1040 line 7a, the bounded 2025 Schedule K-1 (Form 1065) box-5
taxable-interest path through line 2b and Schedule B Part I, and the bounded
2025 payer-reported current-inclusion market-discount class in Form 1099-INT
box 10 or Form 1099-OID box 5. The selected next slice is covered,
long-term, gain-only Form 1099-B transactions reported directly on Schedule D
line 8a without Form 8949; its plan is reconstructed, but none of its product
changes are yet claimed on this branch state.

## Operational State: Engine Breadth

* **Active milestone:** Covered Long-Term Gains, Schedule D Line 8a — **planned.**
* **Product change (target):** covered, long-term, gain-only Form 1099-B
  transactions become a closed source family that reaches Schedule D line 8a,
  Part II line 15, Part III line 16, Form 1040 line 7a, and the correct QDCG
  line-16 computation with an attachment disposition and explanation walk.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`
  — committed on the draft milestone branch.
* **Scope:** covered, long-term, gain-only, no-adjustment 2025 Form 1099-B
  transactions reported directly on Schedule D line 8a without Form 8949.
  Short-term transactions, losses, carryovers, Form 8949, noncovered
  securities, digital assets, and other Schedule D sources remain outside it.
* **Reconstruction source:** the complete discarded state is preserved at
  `snapshot/2026-08-02-schedule-d-covered-ltcg-pre-curation` (`4af36ca`).
  Its old PR, charter, and repair chronology is evidence, not current process.
* **Next:** commit the accepted Schedule D contract and its bounded evidence
  archive, then restore the completed Track 1 implementation as one commit.
* **Branch line:** `milestone/schedule-d-covered-ltcg-8a-v2`, one draft-to-final
  milestone PR based on the current `main`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
