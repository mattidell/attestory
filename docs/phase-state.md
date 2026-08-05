<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-inbound-loss-carryovers",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH — INBOUND CAPITAL-LOSS CARRYOVERS CLOSED 2026-08-04.** Track 1 (with one findings-only repair) and Track 2 both independently reviewed `READY`. The bounded covered, basis-reported capital-transaction class is synthetic complete with a short-term or long-term capital-loss carryover derived from a bounded five-fact 2024 prior-return authority (ADR-0059, two-path completeness) via the Capital Loss Carryover Worksheet (ADR-0060), included on signed Schedule D lines 6/7/14/15/16/21 and Form 1040 line 7a/9. Rebased onto the merged Schedule B interest-adjustments milestone after an owner-directed unmerge/re-merge resolved a package-version collision on already-merged history; this milestone's own package.core-calculations/published-packages were renumbered to v16/v11 as an additive union, and a latent hardcoded package-version restriction in packages/derivation/package_validation.py was generalized. Closeout complete: coverage frontier, roadmap, deferral ledger, retrospective, and README are updated. The next breadth milestone is unselected.",
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
or Form 1099-OID box 5, the bounded three-class Schedule B interest-adjustment
path, and the bounded covered, basis-reported Form 1099-B class — short-term
or long-term, gain or loss — reported directly on Schedule D line 1a/8a
without Form 8949, including the current-year $3,000/$1,500 capital-loss
limitation and now a short-term or long-term capital-loss carryover derived
from a bounded 2024 prior-return authority, included on Schedule D lines 6
and 14. The next breadth slice is owner-selected from the refreshed coverage
frontier.

## Operational State: Engine Breadth

* **Active milestone:** none selected. Inbound Capital-Loss Carryovers into
  2025 Schedule D **closed 2026-08-04**, independently reviewed `READY`.
* **Result:** the bounded covered, basis-reported capital-transaction class
  is synthetic complete end to end with a short-term or long-term
  capital-loss carryover — a bounded five-fact 2024 prior-return authority
  (ADR-0059) with a two-path completeness gate (a cheap declared-absence
  path preserving the existing `no-inbound-capital-loss-carryovers`
  declaration, alongside the full authority path); the Capital Loss
  Carryover Worksheet as an auditable derived rule citizen and signed
  successor Schedule D lines 6/7/14/15/16/21 and Form 1040 line 7a/9
  (ADR-0060); a carryover-only routing case; and disposition-visibility
  parity for the missing-authority state. Form 8949, noncovered
  securities, digital assets, other Schedule D sources, and any amount
  carried into 2026 remain honestly outside it — see the deferral ledger.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-04-schedule-d-inbound-loss-carryovers.md`.
* **Deferral ledger:** `docs/phases/engine-breadth/milestones/schedule-d-inbound-loss-carryovers-deferral-ledger.md`.
* **Ratified in-scope:** ADR-0059 (prior-return capital-loss authority,
  two-path completeness) and ADR-0060 (worksheet arithmetic, sign,
  routing, 2026 bound) — both settled by a paper-first Track 0 before any
  implementation charter; ADR-0059 amended once before ratification (owner
  direction) to reinstate the declared-absence path rather than requiring
  the five-fact authority unconditionally. Both ratified as amended, with
  no further dissent.
* **Review history:** Track 1's independent review verified the arithmetic
  and routing correct by direct inspection and found four fixture-coverage
  findings, closed by one findings-only repair round (recheck `READY`,
  which also caught and fixed a real mypy defect). Track 2's independent
  review found no findings.
* **Cross-milestone incident:** the parallel Schedule B interest-
  adjustments milestone merged to `origin/main` with a
  `package.core-calculations` `v15` that silently dropped 45 members from
  the prior milestone's package within its own commits. The owner
  force-pushed `origin/main` back to the pre-collision merge point,
  confirmed the prior milestone needed no repair, and had Schedule B
  regenerated correctly on a separate branch before re-merging. This
  milestone rebased onto the repaired result and renumbered its own
  package to `v16`/`v11` as a validated additive union, keeping both
  already-merged files byte-immutable. A dry-run semantic-ledger check
  (temporary, never committed) preceded the real rebase and surfaced a
  generalized fix to a latent hardcoded-package-version defect in
  `packages/derivation/package_validation.py`, folded into this
  milestone's implementation commit and verified not to regress Schedule
  B's own packages. Full account in the retrospective.
* **Next:** owner-selects the next breadth milestone from
  `docs/phases/engine-breadth/coverage-frontier.md`. No milestone is
  currently active.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
