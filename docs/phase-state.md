<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "test-and-ci-efficiency",
  "active_plan": "docs/phases/engineering-health/milestones/test-and-ci-efficiency.md",
  "milestone_state": "closed",
  "status": "Closed. Draft pushes get the cheap checks and the fast lane in about a minute; verify fails on drafts and runs in full on ready PRs. Schema-check and historical-lattice reuse cut suite CPU (3,601s against 5,329s at P0, single runs). No test was moved. The next milestone is unselected.",
  "current_role": "Foreman — select next milestone",
  "current_prompt": "docs/phases/engineering-health/engineering-health-roadmap.md"
}
-->

# Phase State

## Current direction

**Faster CI, Cheaper Suites, the Same Defects Caught is closed**
([plan](phases/engineering-health/milestones/test-and-ci-efficiency.md),
[retrospective](milestone-retrospectives/2026-10-21-test-and-ci-efficiency.md)).
A draft push gets the cheap checks and the fast lane in about a minute; the
required `verify` fails on a draft and runs in full when the PR is marked ready.
Reusing successful fact-type schema checks and the historical lattice for an
exact fact state cut the sampled Form 1098 test's CPU by 48%; the local suite
used 3,601s of CPU against 5,329s at P0. No test was moved: moving cases below
the coordinator would recover under 1% of suite time.

The next milestone is unselected. The retrospective's leading follow-up is
re-projection: fold incrementally within one save, share one projection per
recording or review operation, and only then consider a prefix memo, chosen
from a P0 of the recorder and save paths.

## Previous milestone

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

- [Closed milestone plan](phases/engineering-health/milestones/test-and-ci-efficiency.md):
  ranking, tracks, outcome and remaining cost.
- [Retrospective](milestone-retrospectives/2026-10-21-test-and-ci-efficiency.md):
  lessons and the re-projection follow-up order.
- [ADR 0079](adr/0079-family-version-handover-and-containment.md).
- [Engineering Health roadmap](phases/engineering-health/engineering-health-roadmap.md).
- README, “Personal-item sale on Form 1099-K”.

## Parked

- Gain and break-even reporting on Form 8949 and Schedule D.
- Additional seller-paid shipping under platform pass-through.
- The adopted preferential-rate base taxes short-term covered gains at
  preferential rates. It is recorded and awaits owner disposition.
- Phase-state validation in `governance_lint`: an engineering-health
  candidate. Broad test redesign remains a later scope choice.
- A v1 Form 1099-K workspace re-answers its completeness question under the
  successor package; recovery for a log with two current family versions; a
  full pre-save fold for every act kind.
- Browser observation of the mortgage and sale pages.
- Multiple Form 1098 support, interest allocation above the debt limit,
  second-home extension, mixed-use amounts, refinancing and the mortgage credit.
- The configured standard deduction, which is not the verified 2025 amount.
- Use of the circumstance routes on the correction session, which still
  resolves an older registry.
- A general assumption framework, free-text intake and institutional
  verification.
