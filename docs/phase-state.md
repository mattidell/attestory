<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "per-subject-binding",
  "active_plan": "docs/phases/engineering-health/milestones/per-subject-binding.md",
  "milestone_state": "planned",
  "status": "Planned. P0 reproduces how a per-subject rule can read another subject's answer, and finds which shipped rules are exposed.",
  "current_role": "Builder — P0 reproduce and inventory",
  "current_prompt": "docs/reviews/per-subject-binding/charter-p0-reproduce-and-inventory.md"
}
-->

# Phase State

## Latest milestone

**A Per-Subject Rule Reads Only Its Own Subject is planned**
([plan](phases/engineering-health/milestones/per-subject-binding.md)). The EIC
child probe showed a per-subject rule in the Form 1098 shape can be evaluated
with another subject's answer. P0 reproduces the smallest failing case, names
the code path, and checks every shipped per-subject rule for a wrong result.

## Previous milestone

**The 2025 Earned Income Credit with Qualifying Children is closed**
([plan](phases/engine-breadth/milestones/eic-qualifying-children.md),
[retrospective](milestone-retrospectives/2026-10-24-eic-qualifying-children.md)).
On core v54 the credit uses the column for the number of children who meet
every test and have a valid SSN, each counted from six answers on a closed
child roster. A child another person may also claim blocks.

## Earlier return-calculation milestone

**The 2025 Earned Income Credit is closed**
([plan](phases/engine-breadth/milestones/earned-income-credit.md),
[retrospective](milestone-retrospectives/2026-10-23-earned-income-credit.md)).
On core v53 a filer with no qualifying child gets the credit on line 27a,
from EIC Worksheet A and the printed EIC Table. Each EIC question is asked
only where it can change line 27a; the plan and README give each stop.

## Earlier return-calculation milestones

- **Refund or Amount Owed: Finishing the 2025 Return**
  ([plan](phases/engine-breadth/milestones/refund-or-amount-owed.md),
  [retrospective](milestone-retrospectives/2026-10-22-refund-or-amount-owed.md)):
  on core v52 every computed return ends in a refund or an amount owed.
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

- [Latest milestone plan](phases/engine-breadth/milestones/eic-qualifying-children.md):
  P0, contract, tracks and outcome; and its
  [retrospective](milestone-retrospectives/2026-10-24-eic-qualifying-children.md).
- [Previous return-calculation plan](phases/engine-breadth/milestones/earned-income-credit.md).
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
- Multiple Form 1098 support, interest allocation above the debt limit,
  second-home extension, mixed-use amounts, refinancing and the mortgage credit.
- Form 1099-K, 1099-G and SSA-1099 withholding on line 25b; a 1099-INT,
  1099-DIV or 1099-R statement recorded without its box 4 answer; Form W-2G.
- The EIC tie-breaker rules (a child another person may also claim is
  outside the class); Worksheet B, Form 8862, combat pay, the Medicaid waiver exclusion
  and Worksheet 1.
- The Form 1098 flat per-subject rule shape can bind another subject's
  answer (seen in the EIC child probe); the mortgage rules use it.
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
