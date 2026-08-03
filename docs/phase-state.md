<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-current-year-losses",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH — CURRENT-YEAR CAPITAL LOSSES AND SCHEDULE D LINE 21 CLOSED 2026-08-03.** Track 1 (with one findings-only repair) and Track 2 both independently reviewed `READY`. The bounded covered, basis-reported, short-term-or-long-term, gain-or-loss 2025 Form 1099-B class is synthetic complete: signed Schedule D lines 1a/7/8a/15/16, the §1211 current-year loss cap (line 21), Form 1040 line 7a/9, the Schedule D-bound QDCG line-16 path at any sign of Schedule D's result, package resolution, explanation, and presentation, including honest visibility for the new SOURCE_SET_UNCLOSED and COMPLETENESS_VALUE_VIOLATION states. Closeout complete: coverage frontier, roadmap, deferral ledger, retrospective, and README are updated; the milestone's own working charters are distilled into the retrospective and this record, not retained. Entire milestone stayed local (no push, no PR) until this closeout, per explicit owner instruction. The next breadth milestone is unselected.",
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
or Form 1099-OID box 5, and now the bounded covered, basis-reported Form
1099-B class — short-term or long-term, gain or loss — reported directly on
Schedule D line 1a/8a without Form 8949, including the current-year
$3,000/$1,500 capital-loss limitation, the Schedule D-bound QDCG line-16 path
at any sign of Schedule D's result, and an honest attachment
disposition/explanation walk. The next breadth slice is owner-selected from
the refreshed coverage frontier.

## Operational State: Engine Breadth

* **Active milestone:** none selected. Current-Year Capital Losses and the
  Schedule D Line 21 Limitation **closed 2026-08-03**, independently
  reviewed `READY`.
* **Result:** the bounded covered, basis-reported, short-term-or-long-term,
  gain-or-loss 2025 Form 1099-B class is synthetic complete end to end —
  an additive successor long-term family and a new short-term family
  (ADR-0057), each preserving the original ADR-0052 gain-only family
  unedited and package-exclusive against it; a `selected-preferential-base`
  successor with a multi-family discriminator, an exact pin table, and a
  producer-side floor to nonnegative; signed Schedule D lines 1a/7/8a/15/16
  and the §1211 current-year loss cap (line 21, ADR-0058); a completeness
  successor retiring two of the seven boundary declarations; package
  resolution, explanation, and presentation, including honest visibility
  for the new `SOURCE_SET_UNCLOSED` and `COMPLETENESS_VALUE_VIOLATION`
  states. Inbound capital-loss carryovers, Form 8949, noncovered
  securities, digital assets, other Schedule D sources, and QOF flow
  remain honestly outside it — see the deferral ledger.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-03-schedule-d-current-year-losses.md`.
* **Deferral ledger:** `docs/phases/engine-breadth/milestones/schedule-d-current-year-losses-deferral-ledger.md`.
* **Ratified in-scope:** ADR-0057 (source families and multi-family route
  selection) and ADR-0058 (signed downstream, line-21 limitation,
  completeness successor, 2025-only bound) — both settled by a paper-first
  Track 0 before any implementation charter, per explicit owner
  instruction; both ratified as proposed, with no amendment. Track 0's
  decision record and all working charters were distilled into the two
  ADRs and this milestone's retrospective and are not retained in the
  repository.
* **Review history:** Track 1's independent review verified the
  arithmetic and routing correct by direct inspection and found four
  fixture-coverage/disclosure findings, closed by one findings-only
  repair round with substantive fixtures (recheck `READY`). Track 2's
  independent review found no findings.
* **Branch history:** the entire milestone — plan, Track 0, ADR
  ratification, Track 1, its repair, Track 2, and this closeout — stayed
  local on `milestone/schedule-d-current-year-losses` with no push and no
  PR until this closeout, per explicit owner instruction.
* **Next:** owner-selects the next breadth milestone from
  `docs/phases/engine-breadth/coverage-frontier.md`. No milestone is
  currently active.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
