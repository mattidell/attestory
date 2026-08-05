<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-b-interest-adjustments",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-b-interest-adjustments.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH / SCHEDULE B INTEREST ADJUSTMENTS — CLOSED 2026-08-03.** The bounded 2025 three-class Schedule B interest-adjustment path is synthetic complete; the post-close CI type-only test repair and final exact-range review are complete. Ratified package history is preserved and Schedule D remains outside scope.",
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
disposition/explanation walk, and the bounded three-class Schedule B
interest-adjustment path. The next breadth slice is owner-selected from the
refreshed coverage frontier.

## Operational State: Engine Breadth

* **Active milestone:** Schedule B Interest Adjustments — **closed
  2026-08-03**. The preceding Current-Year Capital Losses and Schedule D
  Line 21 Limitation also closed 2026-08-03, independently reviewed `READY`.
* **Result:** the bounded 2025 nominee-distribution, accrued-interest-paid-to-a-
  seller, and taxable-amortizable-bond-premium adjustment classes are synthetic
  complete end to end. Each class has explicit authority and closure; the
  resulting subtraction flows through Form 1040 line 2b and named Schedule B
  Part I rows, with package/release/adoption resolution, explanation, and a
  production-shaped presentation golden. Underlying investment calculations,
  other Schedule B adjustments, and Schedule D remain outside scope.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-b-interest-adjustments.md` — **closed**.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-03-schedule-b-interest-adjustments.md`.
* **Schedule B result:** the explicit closed nominee-distribution, accrued-interest-paid-to-a-seller, and taxable-ABP adjustment classes subtract from positive interest and render as named Schedule B Part I rows tied to line 2b. The final graph uses artifact-package.v12, package v15, published registry v10, release v8, and adoption v15; Schedule D remains outside scope.
* **Ratified in-scope:** ADR-0057 (source families and multi-family route
  selection) and ADR-0058 (signed downstream, line-21 limitation,
  completeness successor, 2025-only bound) — both settled by a paper-first
  Track 0 before any implementation charter, per explicit owner
  instruction; both ratified as proposed, with no amendment. Track 0's
  decision record and all working charters were distilled into the two
  ADRs and this milestone's retrospective and are not retained in the
  repository.
* **Review history:** The integrated independent review returned READY after
  one bounded package-history repair. The follow-up review confirmed the
  ratified package files were restored byte-for-byte and the Schedule B
  successor graph remained additive. The immutable v6 EOF formatting warning
  remains deferred in the retrospective.
* **Branch history:** The milestone plan, implementation tracks, repairs,
  review disposition, retrospective, and closeout remain on the single
  milestone PR branch until the owner merges it.
* **Next:** select a new Engine Breadth milestone from the coverage frontier.
  No next milestone is selected.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
