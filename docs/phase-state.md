<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "ssa1099-benefits-line6",
  "active_plan": "docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / 2025 SSA-1099 BENEFITS THROUGH THE SOCIAL SECURITY BENEFITS WORKSHEET AND FORM 1040 LINES 6A/6B — PLAN COMMITTED.** Track 0 is a foreman-owned paper-first scope checkpoint; Track 1 and Track 2 owner-launch charters are prepared.",
  "source_ref": "origin/main",
  "source_commit": "b0480bc2178ba7d2fd8baa59b1a6823e5aa5c4a0",
  "current_role": "Foreman (Track 0 paper-first scope contract; implementation charters prepared)",
  "current_prompt": "docs/reviews/charter-2026-08-04-ssa1099-line6-track1.md"
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
and 14. It also computes the bounded 2025 Form 1099-DIV box-12 to Form 1040
line-2a route, independent of the closed Schedule D carryover milestone.

## Operational State: Engine Breadth

* **Active milestone:** 2025 SSA-1099 Benefits through the Social Security Benefits Worksheet and Form 1040 Lines 6a/6b — plan committed 2026-08-04; Track 0 is foreman-owned and Track 1/2 are prepared for owner launch.
  Form 1099-DIV Box 12 to Form 1040 Line 2a **closed 2026-08-04**.
  Inbound Capital-Loss Carryovers into 2025 Schedule D **closed 2026-08-04**,
  independently reviewed `READY`, and remains preserved on the ratified line.
* **Previous result:** the bounded covered, basis-reported capital-transaction class
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
* **Current result:** the bounded box-12 family, residual successor, explicit
  line-2a completeness boundary, reported-only downstream semantics,
  explanation, presentation, package/release/adoption successors, and
  box-13 production-path companion enforcement are synthetic complete. The
  independent re-review returned `READY`. Other tax-exempt sources, nonzero
  box 13, excluded downstream consumers, and general tax-exempt-interest
  support remain outside the claim.
* **Current planning state:** the SSA-1099 milestone starts from `origin/main`
  at `b0480bc`. The base has no Form 1040 line-6a/6b citizens, no line-1z,
  line-4b, line-5b, or Form 1040 line-8 citizens, and no Schedule 1 adjustment
  families. Track 0 must close those worksheet inputs component by component;
  it must not use line 9 as a shortcut.
* **Plan:** `docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-04-form1099div-box12-line2a.md`.
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
  carryover milestone rebased onto the repaired result and renumbered its own
  package to `v16`/`v11` as a validated additive union, keeping both
  already-merged files byte-immutable. The current box-12 milestone then
  advanced its own additive package graph to v17/registry v12. A dry-run
  semantic-ledger check
  (temporary, never committed) preceded the real rebase and surfaced a
  generalized fix to a latent hardcoded-package-version defect in
  `packages/derivation/package_validation.py`, folded into this
  milestone's implementation commit and verified not to regress Schedule
  B's own packages. Full account is in the current retrospective.
* **Next:** complete the paper-first Track 0 scope contract, then owner-launch
  Track 1 only after Track 0 is ratified.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
