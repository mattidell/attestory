<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "schedule-d-form8949-covered-wash-sale",
  "active_plan": "docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md",
  "milestone_state": "closed",
  "status": "**ENGINE BREADTH — COVERED CODE-W WASH-SALE / FORM 8949 CLOSED 2026-08-05.** Track 1 (three repair/re-review rounds) and Track 2 both independently reviewed READY. The bounded covered, basis-reported capital-transaction class admits a Form 1099-B transaction routed to Form 8949 solely by a broker-reported box-1g wash-sale loss (code W), through Schedule D lines 1b/8b. ADR-0061 was amended pre-merge after review found the originally-proposed transaction-identity mechanism unsafe given a real source-family.v1 schema constraint; resolved with a separate wash-sale fact type and an identity-key collision kill-test wired into the live run path. Rebased onto the merged Form 1099-DIV Box 12 milestone; a second package/schema version collision was caught before either PR merged and resolved as an additive union (package v18, registry v13, quantity-vocabulary v7, artifact-package v15). Closeout complete: coverage frontier, roadmap, deferral ledger, retrospective, and README are updated. The next breadth milestone is unselected.",
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
path, the bounded covered, basis-reported Form 1099-B class — short-term
or long-term, gain or loss — reported directly on Schedule D line 1a/8a
without Form 8949, a short-term or long-term capital-loss carryover derived
from a bounded 2024 prior-return authority, included on Schedule D lines 6
and 14, and the bounded 2025 Form 1099-DIV box-12 to Form 1040 line-2a
route. A covered Form 1099-B transaction routed to Form 8949 solely by a
broker-reported box-1g wash-sale loss (code W) is now also computed,
through Schedule D lines 1b/8b. The next breadth slice is owner-selected
from the refreshed coverage frontier.

## Operational State: Engine Breadth

* **Active milestone:** none selected. Covered Form 1099-B Wash-Sale
  Adjustments through Form 8949 and Schedule D Lines 1b/8b **closed
  2026-08-05**, independently reviewed `READY`.
* **Result:** the bounded covered, basis-reported capital-transaction class
  admits a Form 1099-B transaction routed to Form 8949 solely by a
  broker-reported box-1g wash-sale loss (code W) — short-term through
  Form 8949 Part I/box A/Schedule D line 1b, long-term through Part
  II/box D/line 8b. Form 8949 columns (a)-(h), code W in column (f), and
  row arithmetic `h = d − e + g` are production-shaped with per-transaction
  validation guards for code W on a gain and an adjustment exceeding the
  otherwise-deductible loss. Successor Schedule D lines 1b/7/8b/15/16/21
  and Form 1040 line 7a/9 recompute over the new lines alongside the
  existing 1a/8a, box-2a, and carryover lines. Every other Form 8949
  adjustment code, noncovered securities, and taxpayer-side wash-sale
  determination remain honestly outside it — see the deferral ledger.
* **Plan:** `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md`.
* **Retrospective:** `docs/milestone-retrospectives/2026-08-05-schedule-d-form8949-covered-wash-sale.md`.
* **Deferral ledger:** `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale-deferral-ledger.md`.
* **Ratified in-scope:** ADR-0061 (transaction authority, family topology,
  completeness successor) and ADR-0062 (Form 8949 attachment, arithmetic,
  Schedule D 1b/8b composition) — both settled by a paper-first Track 0
  before any implementation charter; ADR-0061 amended once, pre-merge,
  after independent review found the originally-proposed transaction-
  identity mechanisms structurally unsafe (a `source-family.v1` schema
  constraint would have forced automatic dual family membership for every
  direct-reporting transaction). Amended to name the mechanism actually
  built (a separate `covered-w-st-txn`/`covered-w-lt-txn` fact type) and
  add an identity-key collision kill-test as the real non-double-count
  enforcement.
* **Review history:** Track 1's first independent review returned NOT
  READY with four findings — a critical arithmetic-masking defect
  (validation guards checked on aggregated box subtotals instead of per
  transaction), the transaction-identity deviation above, an unimplemented
  flag/amount guard plus five missing required fixtures, and one
  low-severity structural-enforcement gap. A first repair fixed two
  findings outright and stopped correctly on the identity-mechanism
  finding per its own charter; a continuation repair (after the ADR
  amendment) implemented the collision kill-test and the remaining
  fixtures. A second independent review found that kill-test correct in
  isolation but never wired into the live run path; a third repair round
  wired it into `runner.py` alongside the existing per-transaction
  arithmetic guard. A third independent review returned `READY`. Track 2's
  independent review found that Track 1's own repair rounds had already
  substantively delivered the presentation/citation-walk requirements, and
  confirmed that claim by direct inspection — no findings.
* **Cross-milestone incident:** the parallel Form 1099-DIV Box 12
  milestone (PR #158) merged to `origin/main` first. Both milestones
  independently minted the same next core-package version (`v17`) and
  registry version (`v12`), and independently minted colliding schema
  successors (`quantity-vocabulary.v6` for two different additive reasons;
  `artifact-package.v13` likewise). Caught before either PR merged, via
  the same disposable dry-run semantic-ledger technique used in the
  inbound-carryovers milestone, run proactively on explicit owner
  instruction before the real rebase. Resolved as a validated additive
  union: `package.core-calculations.v18`, `published-packages.v13`,
  `quantity-vocabulary.v7`, `artifact-package.v15` — keeping every
  already-merged file byte-immutable. A separate, unrelated mid-rebase
  worktree-registry incident (a concurrent session's operation orphaned
  this session's working directory) was reported, confirmed
  unintentional, and recreated cleanly with no work lost. Full account in
  the retrospective.
* **Next:** owner-selects the next breadth milestone from
  `docs/phases/engine-breadth/coverage-frontier.md`. No milestone is
  currently active.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
