<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-covered-ltcg-8a",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH — COVERED LONG-TERM GAINS, SCHEDULE D LINE 8a CLOSED 2026-08-02.** Track 2/3 independent review returned `READY` on the first pass. The bounded covered, long-term, gain-only, no-adjustment Form 1099-B class is synthetic complete: Schedule D line 8a/13/15/16, Form 1040 line 7a/9, and the Schedule D-bound QDCG line-16 path, with two additive architecture repairs ratified in-scope (ADR-0055 completeness value-check, ADR-0056 attachment disposition visibility). Closeout complete: coverage frontier, roadmap, deferral ledger, retrospective, and README are updated; the milestone's own working charters are distilled into the retrospective and this record, not retained. The next breadth milestone is unselected.",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/engine-breadth/coverage-frontier.md"
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
taxable-interest path through line 2b and Schedule B Part I, the bounded 2025
payer-reported current-inclusion market-discount class in Form 1099-INT box 10
or Form 1099-OID box 5, and now the bounded covered, long-term, gain-only Form
1099-B class reported directly on Schedule D line 8a without Form 8949,
including the Schedule D-bound QDCG line-16 path and an honest attachment
disposition/explanation walk. The next breadth slice is owner-selected from
the refreshed coverage frontier.

## Operational State: Engine Breadth

* **Active milestone:** none selected. Covered Long-Term Gains, Schedule D
  Line 8a **closed 2026-08-02**, independently reviewed `READY`.
* **Result:** the bounded covered, long-term, gain-only, no-adjustment 2025
  Form 1099-B class is synthetic complete end to end — Schedule D (line
  8a columns (d)/(e)/(h), Part II line 15, Part III line 16), Form 1040
  line 7a/9, the Schedule D-bound QDCG line-16 path, package resolution,
  explanation, and presentation (including honest visibility for
  blocked/not-required attachment states, ADR-0056). Short-term
  transactions, capital losses/carryovers, Form 8949, noncovered
  securities, digital assets, other Schedule D sources, and QOF flow
  remain honestly outside it — see the deferral ledger.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-02-schedule-d-covered-ltcg-8a.md`.
* **Deferral ledger:** `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a-deferral-ledger.md`.
* **Contract evidence:** `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/`
  preserves the P1-P3 prototype evidence behind ADR-0052/0053/0054,
  unchanged by this milestone's later tracks. ADR-0055 and ADR-0056's
  paper spikes and working charters were distilled into their accepted
  ADR text and this retrospective and are not retained in the repository.
* **Ratified in-scope:** ADR-0055 (attachment completeness value-check)
  and ADR-0056 (attachment disposition visibility) — both narrow,
  additive, Tier 2, surfaced by their own builders as named charter-stop
  findings and resolved via a paper-spike-plus-ADR-draft decision unit
  each, per the retrospective.
* **Next:** owner-selects the next breadth milestone from
  `docs/phases/engine-breadth/coverage-frontier.md`. No milestone is
  currently active.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
