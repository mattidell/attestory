<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "form-1099-withholding",
  "active_plan": "docs/phases/engine-breadth/milestones/form-1099-withholding.md",
  "milestone_state": "closed",
  "status": "Closed. On core v59 withholding on Forms 1099-G box 4 and SSA-1099 box 6 reaches line 25b; earlier packages still refuse it (ADR-0082). Form 1099-K stays outside the class.",
  "current_role": "Foreman \u2014 select next milestone",
  "current_prompt": "docs/phases/engine-breadth/coverage-frontier.md"
}
-->

# Phase State

## Current direction

The next milestone is unselected. The leading candidate: the
form-1099-withholding final review found that an unresolved Form 1099-K is
left out of line 8 and total income while the bottom line publishes, on v58
as on v59. ADR-0082 (package-scoped companion admission) and ADR-0081
(per-subject conditional dependencies) are accepted.

Engineering Health's [Remaining Test and CI Cost](phases/engineering-health/milestones/test-cost-remaining.md)
is closed and merged
([retrospective](milestone-retrospectives/2026-10-28-test-cost-remaining.md)).
Mortgage recording and review reuse one projection inside the operation. A
checked save folds its prefix incrementally and refuses as before; the fold
follows the package in force (ADR-0082). Full verify runs as four shards under
the same `verify` job. Its historical baseline guard fails closed; at main-ui
convergence it refuses restoring a divergent historical file to main's bytes
without an independent prior-main witness. The profiled mortgage case fell
from 123.89s to 98.03s of CPU. The profiled form-save folds are a one-case
result.

## Latest Tax Circumstance Breadth milestone

The [mortgage result](phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md)
has been reconstructed on the milestone branch against the merged
credit-for-other-dependents work below. Main's core v56 / registry v54 /
release v54 are retained unchanged; the mortgage core v57 / registry v55 /
release v55 chain is regenerated and its focused package, adoption and
credit-preservation checks pass.
One or two
exact Forms 1098 can describe one
continuing original borrowing for one main home, retaining local and shared
answer scope, supported calculation, fresh-source restoration and saved
explanation. The existing dependency guard now records helper prerequisites so
their old findings become stale when support is withdrawn.

Question meaning, one offered shared scope and actionable saved conflicts are
repaired, as are stale production rule notes. The duplicate-payment calculation
repair is built. The owner approved preserving confirmations for unchanged
A/B after temporarily adding and removing C; a third current form still blocks,
and changed source/link support needs fresh confirmation. The active charter
retains the bounded applicability and declared payment-readiness contract.
The result was independently reviewed. General mortgage allocation,
refinancing, more homes/borrowings, higher grandfathered debt limits and
observed browser interaction remain outside this result. The earlier phase
endpoint remains met; another vertical is not automatically selected.

## Latest milestone

**Federal Tax Withheld on Forms 1099 is closed**
([plan](phases/engine-breadth/milestones/form-1099-withholding.md),
[retrospective](milestone-retrospectives/2026-10-28-form-1099-withholding.md)).
On core v59 federal income tax withheld on Forms 1099-G box 4 and SSA-1099
box 6 reaches line 25b and the refund or amount owed. Companion admission
now belongs to the package being run (ADR-0082), so v58 and earlier
still refuse that withholding. An existing return is asked two new closures
and, after its Social Security family is handed over to v2, to re-confirm
its SSA-1099s.

## Previous milestone

**A Child More Than One Person Could Claim is closed**
([plan](phases/engine-breadth/milestones/dependent-tie-breaker.md),
[retrospective](milestone-retrospectives/2026-10-27-dependent-tie-breaker.md)).
On core v58 a per-child tie-breaker decides whether a contested child counts
for the earned income credit, child tax credit and credit for other
dependents; Form 8332 releases, more than one other claimant and unsettled
equal-AGI ties are outside the class by answer.

## Earlier return-calculation milestone (child tax credit)

**The 2025 Child Tax Credit is closed**
([plan](phases/engine-breadth/milestones/child-tax-credit.md),
[retrospective](milestone-retrospectives/2026-10-24-child-tax-credit.md)).
On core v55 lines 19 and 28 come from Schedule 8812 for qualifying children
on a credit roster, including Part II-B for three or more children. The
credit for other dependents stays outside the class.

## Earlier engineering-health milestones

**Every Required Answer Is Read is closed**
([plan](phases/engineering-health/milestones/required-versus-read.md),
[retrospective](milestone-retrospectives/2026-10-24-required-versus-read.md)).
A static check in CI keeps a rule from requiring an input it never
references; `tools/required_versus_read.py path` reports path-dependent cases
on demand. The rows examined in shipped content had no misleading question
or correction hazard.

**A Per-Subject Rule Reads Only Its Own Subject is closed**
([plan](phases/engineering-health/milestones/per-subject-binding.md),
[retrospective](milestone-retrospectives/2026-10-24-per-subject-binding.md)).
A per-subject rule now binds only its own subject's answers or a return-level
value. The shipped Form 1098 reason rule no longer reads another statement's
answers; no content or golden changed.

## Earlier return-calculation milestone

**The 2025 Earned Income Credit is closed**
([plan](phases/engine-breadth/milestones/earned-income-credit.md),
[retrospective](milestone-retrospectives/2026-10-23-earned-income-credit.md)).
On core v53 a filer with no qualifying child gets the credit on line 27a,
from EIC Worksheet A and the printed EIC Table. Each EIC question is asked
only where it can change line 27a; the plan and README give each stop.

## Earlier return-calculation milestones

- **The 2025 Earned Income Credit with Qualifying Children**
  ([plan](phases/engine-breadth/milestones/eic-qualifying-children.md),
  [retrospective](milestone-retrospectives/2026-10-24-eic-qualifying-children.md)):
  on core v54 the credit uses the column for the number of qualifying
  children, each counted from six answers on a closed child roster.
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

The mortgage publication candidate above preserves these return selections.

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
fold and current-lattice rebuilds. Remaining Test and CI Cost, in the current
direction above, took the mortgage recording and review repeats and the
save-path fold. Current-lattice rebuilds stay unselected.

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

- [Current mortgage plan](phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md)
  and [lessons](milestone-retrospectives/2026-10-25-mortgage-statement-borrowing.md).
- [Tax Circumstance Breadth roadmap](phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md):
  the attained endpoint and separately selectable remaining work.
- [Earlier return-calculation plan](phases/engine-breadth/milestones/eic-qualifying-children.md):
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
- An unresolved Form 1099-K (nonzero box 4, or unanswered circumstance
  questions) is left out of line 8 and total income while lines 24-37
  publish, on v58 and v59. Form 1099-K box 4 on line 25b (SC-R1); routing the
  1098, 1099-K and nominee recorders through the package overlay first
  (ADR-0082 production condition 2).
- A recorded withholding amount counts while its family is unclosed, in
  every withholding family; missing-box-4 tests for 1099-DIV and 1099-R;
  Form W-2G (line 25c); package companion declarations in package content;
  a generator for the core package, registry and release chain; an
  in-product route for the Social Security handover.
- Form 8332 and decree releases, more than one other claimant and unsettled
  equal-AGI ties (outside the class by answer); asking the tie-breaker only
  of a child some credit can count, which needs derived per-subject results
  as conditional members; Worksheet B, Form 8862, combat pay, the Medicaid waiver exclusion
  and Worksheet 1.
- `explain()` re-expands shared inputs at each use: the line 27a walk is
  9,885 tree nodes over 218 findings.
- Disabled-over-limit relatives and multiple support agreements for the
  credit for other dependents; lines 29-31
  refundable credits, Schedule 2 Part II taxes and the estimated tax
  penalty, each declared absent.
- Lines 19 and 28's form-field explanations read as the earned income
  credit (copied from line 27a on core v55), and no presentation line names
  the tie-breaker step that decided a child.
- Worksheet lines as presentation rows; `demo.*` ids on the correct
  capital-loss and Social Security amounts.
- The age questions' wording (born before January 2, 1961; a death in 2025
  before age 65), and the SLI dependent answer ("is claimed", filer only)
  beside the new "can be claimed" answer.
- Use of the circumstance routes on the correction session, which still
  resolves an older registry.
- A general assumption framework, free-text intake and institutional
  verification.
