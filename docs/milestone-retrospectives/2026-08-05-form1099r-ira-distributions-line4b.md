# Retrospective — Fully Taxable IRA Distributions from Form 1099-R to Form 1040 Line 4b

## What differed from the plan

- The bounded source class settled on IRA/SEP/SIMPLE-family Form 1099-R
  statements with distribution code 7, box 1 equal to box 2a, an explicit
  false box-2b-not-determined state, and no line-4a publication. Basis,
  rollovers, Roth qualification, withholding, and special distribution
  treatment remain outside the class.
- Track 1 added logical statement identity, same-statement correction,
  distinct-statement aggregation, affirmative current-horizon closure,
  source-family mapping, line 4b, citations, and lifecycle fixtures. Track 2
  added the additive line-9 successor, downstream proof through AGI, taxable
  income, and regular tax, package/release/adoption successors, explanation
  pins, and production-shaped presentation.
- Final package successors were allocated only after inventory and ledger
  reconciliation: core **v22**, published registry **v17**, release **v15**,
  adoption **v22**, `artifact-package.v19`, and
  `quantity-vocabulary.v11`. Existing package, schema, registry, release,
  and adoption history remained byte-immutable; the manifests changed only by
  additive rows.
- The first independent review returned **BLOCKED** with one decision-blocking
  production defect: the standalone validator knew the IRA indicator, code 7,
  and box-2a equality requirements, but the authoritative loader/subtotal
  route collected box 1 without requiring those witnesses. One findings-only
  repair wired the existing witnesses into the live route and added focused
  negative coverage. No second finding, new decision, or scope expansion
  resulted.

## Result

The engine now has a bounded, production-shaped synthetic path for 2025 returns
with one or more ordinary, fully taxable IRA-family distributions reported on
Form 1099-R. The authoritative taxable amount appears on Form 1040 line 4b,
line 4a remains blank, line 4b enters line 9 exactly once, and the existing
line-11 AGI, line-15 taxable-income, and line-16 regular-tax path remains in
use. Explanation, exact citation identity, package resolution, and
presentation are included.

The engine does not calculate IRA basis, Form 8606, rollover eligibility,
Roth qualification, qualified charitable distributions, early/death/disaster
exceptions, withholding, Form 5329, Form 5498, Form 1098-Q, state treatment,
or non-IRA pension, annuity, qualified-plan, or insurance distributions.

## Evidence and review disposition

- Plan and contracts: `docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md`.
- Focused source, downstream, schema-registry, and compatibility checks passed;
  the independent re-review recorded 33 focused IRA/schema checks and 123
  compatibility checks, plus clean `git diff --check` and envelope scan.
- The repair re-review verified valid line 4b/line 9 output, blocking for
  mismatched or missing box 2a, missing or invalid IRA indicator, and missing
  or invalid code 7, with line 4a absent and line 4b entering line 9 once.
- The re-review also verified the three-way semantic ledger and negative
  control: no upstream members, producer selections, schema admissions,
  input bindings, or composition obligations were lost.
- Durable final review: `docs/reviews/2026-08-05-form1099r-ira-distributions-line4b-final-review.md`.
- CI remains the gate of record for the final pushed PR head; the foreman did
  not substitute local full-suite output for CI.

## What it cost

- One paper-first Track 0, two dependent Builders, one independent Reviewer,
  one findings-only repair by the original Builder, and one independent repair
  re-review. No rival prototype and no new ADR.
- Operational dispatch metrics remain in the ignored spawn ledger; no personal
  or real tax data entered the branch, fixtures, review, or output.

## Follow-ups

- Keep other Form 1099-R distribution treatments, basis/rollover machinery,
  Form 8606, and non-IRA distributions as separate future frontier work.
- Preserve append-only package/schema/registry/release/adoption history. Any
  concurrent base change before merge requires a fresh three-way semantic-ledger
  diagnostic and additive union rebuild.
- Leave the next frontier row unselected until the owner chooses it.

## Closeout lesson

Source-boundary validators are not sufficient evidence unless the authoritative
live route requires the same witnesses. Every new admission companion needs a
load-bearing mutation test through the production-shaped runner, not only a
standalone validator test. Version numbers remain inventory facts rather than
reservations, and additive ledger checks must cover both the package graph and
published schema history.
