<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-statement-borrowing",
  "active_plan": "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md",
  "milestone_state": "track-0",
  "status": "P0 READY. Sol P1 review returned REPAIR REQUIRED; Luna combines it with the outside review. Owner choice between report-local ordinary answers and shared-answer intermediates is pending. No experiment, production or schema successor started.",
  "current_role": "Builder — Luna P1 connected repair",
  "current_prompt": "docs/reviews/mortgage-statement-borrowing/charter-p1-connected-account.md"
}
-->

# Phase State

## Current direction

**One Home Loan, More Than One Interest Statement** is the new opening
milestone ([plan](phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md)).
The owner directed a return to tax concepts and ordinary-circumstance recording.
Start with two reports concerning one continuing borrowing and one main home,
such as a change in who collects payments. Preserve the two reports and
establish what the person can affirm about their shared borrowing, without
counting the reports as separate debts or selecting a principal formula now.

P0's real-path investigation is independently reviewed READY after the
source-authority correction. The current two-report calculation can attach
the first report's evidence to the second report's result; matching values
do not repair that provenance problem.

P1's connected design now has outside and independent Sol findings. Luna
repairs them together: compare all nine report-local ordinary answers against
loan-wide assertions with per-report intermediates; use the existing
student-loan scoped-answer pattern before considering an admission allowlist;
reconcile linked Box 3 dates; remove the contradictory empty-family instruction;
and make the connected-route exit limit visible. The owner must select answer
scope before the intermediate-specific experiment. The numeric annual ceiling
and separate other-debt account remain provisional, not observed user inputs.
No production path or schema successor is selected.

The existing full-deduction premise remains distinct from a general limited-debt
calculation. No new balance treatment is selected. Refinancing, multiple independent borrowings,
second homes and allocation remain contrast cases or excluded work, not hidden
implementation promises. Tax Circumstance Breadth's earlier endpoint remains
met; this is a bounded extension.

This branch opened after merged PR #214 in a new managed primary worktree
and is now rebased onto merged PR #215. Its fold-once projection reuse is
included as ratified code, not concurrent milestone WIP.

## Latest completed return-calculation milestone

**The 2025 Earned Income Credit is closed**
([plan](phases/engine-breadth/milestones/earned-income-credit.md),
[retrospective](milestone-retrospectives/2026-10-23-earned-income-credit.md)).
On core v53 a filer with no qualifying child gets the credit on line 27a,
from EIC Worksheet A and the printed EIC Table. Investment income over
$11,950 asks only the unsupported-situations answer. AGI at or above $68,675
asks no EIC question. W-2 box 1 at or above $68,675 while AGI is below it
asks that answer. Otherwise the qualifying-child answer is asked; married
filing separately and head of household with no qualifying child are $0.
AGI at or above the 0-child completed amount ($19,104 other, including
qualifying surviving spouse; $26,214 joint) then asks no further EIC
question, because Step 1 tests line 11b. Box 1 at or above that amount while
AGI is below it asks the unsupported-situations answer, except where filing
status alone stops the credit. The remaining
questions are asked only for single, married filing jointly, or qualifying
surviving spouse when both box 1 and AGI are below that amount. Qualifying
children are the next slice. The next milestone is unselected.

## Previous return-calculation milestone

**Refund or Amount Owed: Finishing the 2025 Return is closed**
([plan](phases/engine-breadth/milestones/refund-or-amount-owed.md),
[retrospective](milestone-retrospectives/2026-10-22-refund-or-amount-owed.md)).
On core calculations v52 every computed return continues from tax after
credits to total tax, withholding (W-2 box 2; Forms 1099-INT, 1099-DIV and
1099-R box 4), estimated payments and the refund or amount owed. A return
without foreign tax no longer answers the direct foreign tax credit's
questions.

## Earlier return-calculation milestones

- **The 2025 Senior Deduction and a Dependent's Standard Deduction**
  ([plan](phases/engine-breadth/milestones/senior-and-dependent-deductions.md),
  [retrospective](milestone-retrospectives/2026-10-22-senior-and-dependent-deductions.md)):
  on core v51, Schedule 1-A Part V reaches line 13b and the dependents'
  worksheet computes line 12e.
- **The 2025 Tax on Taxable Income**
  ([plan](phases/engine-breadth/milestones/tax-on-taxable-income.md),
  [retrospective](milestone-retrospectives/2026-10-22-tax-on-taxable-income.md)):
  on core v50, line 16 and the standard deduction follow verified 2025 law,
  with the Tax Table, the Tax Computation Worksheet and the capital gains
  worksheet published line by line.

The mortgage same-borrowing milestone (PR #216) continues in parallel and
takes the next free package versions when it needs them.

## Earlier engineering-health result

**Fold Once: Less Replaying of the Same History closed** through PR #215
([plan](phases/engineering-health/milestones/projection-reuse.md),
[retrospective](milestone-retrospectives/2026-10-22-projection-reuse.md)).
Recording, review and correction reuse one projection per call instead of
re-projecting the same history in their helpers: save, correct and withdraw
fold the log once instead of three or four times, with 60–72% less CPU on a long
synthetic history. A per-worker warm-up in test setup returned 19 tests to the
fast lane, which runs about 1,528 tests in 23s on the CI runner. The save-path
incremental fold was skipped as the smallest share.

That retrospective lists the remaining re-projection sites, the save-path
fold and current-lattice rebuilds; none is selected.

## Previous milestone

**Faster CI, Cheaper Suites, the Same Defects Caught** closed through PR #214
([retrospective](milestone-retrospectives/2026-10-21-test-and-ci-efficiency.md)).
Draft pushes get the cheap checks and the fast lane in about a minute; `verify`
fails on drafts and runs in full on ready PRs. Schema-check and
historical-lattice reuse lowered suite CPU; no test was moved.

## Earlier engineering-health milestone

**Less Repeated Work, the Same Defects Caught** closed through PR #213. A live
return reuses its own current projection for claim applicability; cold and
historical reads stay fresh. The fixed story's ordinary CPU observation was
7.2% lower; no tests were removed. See the
[closed plan](phases/engineering-health/milestones/test-cost-and-coverage.md).

## Completed performance improvement

The Engineering Health opening milestone, **Faster Feedback, Cheaper
Workspace Replay**, is closed on this branch. The selected fold-local reuse
reduced CPU on the unchanged synthetic correction story by 62.3%; the fixed
80% full-construction target missed by 22 builds. The neighboring control
improved. The result and its limits are in the
[milestone plan](phases/engineering-health/milestones/test-replay-performance.md)
and [measurement note](phases/engineering-health/milestones/test-replay-performance-evidence/measured-performance.md).

Full `verify` succeeded in run
[39551011772](https://github.com/mattidell/attestory/actions/runs/39551011772)
on the repaired implementation: 3,150 passed and 20 skipped; the test step took 2,814.97s
(46m54s). The job ran 05:41:52–06:29:08 UTC; the test step itself ran
05:42:10–06:29:06 UTC (46m56s). These are whole-suite observations, not a
controlled speed comparison. The milestone PR carries the curated candidate's
publication review and CI posture separately from this implementation run.

PR #212 merged after exact-head CI and independent final review. Its branch
is spent; the current milestone starts from the merge. Further implementation
will be selected from the investigation, not inferred from the earlier speedup.

## Inherited product result

**More Than One Statement: Keeping Each Account With Its Form is closed.**
On a synthetic account, a person can record any number of Forms 1099-K, or
that none was received, and answer the ordinary sale questions for each
statement. They can correct, withdraw or remove one statement's account
without changing another's. When the family is closed and every current
statement is a supported personal loss, the Box 1a amounts are added and
entered once at the top of 2025 Schedule 1. Income and tax do not change.
Any other reason, a blocked statement or an unclosed family blocks the entry,
and each statement's saved explanation keeps its own reason and figures.

ADR 0079 adds a recorded family-version handover. A workspace recorded on the
earlier Form 1099-K family hands over to the successor in the same save as its
next write, and completeness is asked again. One Form 1098 remains the
mortgage limit. Accounts are synthetic only.

## Earlier product results

**Personal-Item Sales** closed 2026-10-17 (one Form 1099-K, one sale at a
loss). **Mortgage Interest and What the Loan Paid For** closed 2026-10-15
(one Form 1098).

## Begin here

- [Active mortgage plan](phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md).
- [Tax Circumstance Breadth roadmap](phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md).

- [Latest milestone plan](phases/engine-breadth/milestones/earned-income-credit.md):
  P0, contract, tracks and outcome; and its
  [retrospective](milestone-retrospectives/2026-10-23-earned-income-credit.md).
- [Previous return-calculation plan](phases/engine-breadth/milestones/refund-or-amount-owed.md).
- [Coverage frontier](phases/engine-breadth/coverage-frontier.md): routes,
  their status and the candidates for the next milestone.
- [Earlier return-calculation plan](phases/engine-breadth/milestones/tax-on-taxable-income.md).
- [Previous milestone plan](phases/engineering-health/milestones/projection-reuse.md):
  fold attribution, tracks, outcome and remaining work.
- [Retrospective](milestone-retrospectives/2026-10-22-projection-reuse.md):
  lessons and follow-ups.
- [ADR 0079](adr/0079-family-version-handover-and-containment.md).
- [Engineering Health roadmap](phases/engineering-health/engineering-health-roadmap.md).
- README, “Personal-item sale on Form 1099-K”.

## Parked

- Gain and break-even reporting on Form 8949 and Schedule D.
- Additional seller-paid shipping under platform pass-through.
- Phase-state validation in `governance_lint`: an engineering-health
  candidate. Broad test redesign remains a later scope choice.
- A v1 Form 1099-K workspace re-answers its completeness question under the
  successor package; recovery for a log with two current family versions; a
  full pre-save fold for every act kind.
- Browser observation of the mortgage and sale pages.
- General multiple-Form-1098 support beyond this same-borrowing milestone,
  interest allocation above the debt limit,
  second-home extension, mixed-use amounts, refinancing and the mortgage credit.
- Form 1099-K, 1099-G and SSA-1099 withholding on line 25b; a 1099-INT,
  1099-DIV or 1099-R statement recorded without its box 4 answer; Form W-2G.
- The earned income credit with qualifying children (per-child facts, the
  separated-spouse rule, a refusal when another person can claim the same
  child); Worksheet B, Form 8862, combat pay, the Medicaid waiver exclusion
  and Worksheet 1.
- `explain()` re-expands shared inputs at each use: the line 27a walk is
  9,885 tree nodes over 218 findings.
- Lines 28-31 refundable credits, Schedule 2 Part II taxes and the estimated
  tax penalty, each declared absent.
- Worksheet lines as presentation rows; `demo.*` ids on the correct
  capital-loss and Social Security amounts.
- The age questions' wording (born before January 2, 1961; a death in 2025
  before age 65), and the SLI dependent answer ("is claimed", filer only)
  beside the new "can be claimed" answer.
- Use of the circumstance routes on the correction session, which still
  resolves an older registry.
- A general assumption framework, free-text intake and institutional
  verification.
