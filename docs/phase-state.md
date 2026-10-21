<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "test-cost-and-coverage",
  "active_plan": "docs/phases/engineering-health/milestones/test-cost-and-coverage.md",
  "milestone_state": "closed",
  "status": "Closed on this branch. Live applicability reuses the return's current projection; cold and historical reads stay fresh. Eight fewer full-history folds in the fixed story; single-case CPU observation 7.2% lower. No test removal or broader cache. PR #213 carries publication review and exact-head CI; next milestone unselected.",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/engineering-health/engineering-health-roadmap.md"
}
-->

# Phase State

## Current direction

**Less Repeated Work, the Same Defects Caught is closed on this branch.**
A live return uses its own current projection for claim applicability instead
of replaying the full history again. Cold callers still read freshly and
historical correction checks still read their actual earlier states. No tests,
parity checks or saved-output assertions were removed. See the
[closed plan](phases/engineering-health/milestones/test-cost-and-coverage.md).

The unchanged story profile contains 191 rather than 199 full-history folds,
with all 11 coordinator, forward and reference runs retained. Its ordinary
CPU observation was 49.08s versus the earlier 52.87s (7.2% lower); the control
was 27.12s versus 27.50s. These are bounded single-run historical comparisons,
not a whole-suite speedup. The [measurement note](phases/engineering-health/milestones/test-cost-and-coverage-evidence/measured-applicability-reuse.md)
records raw-output retention and limits. Independent implementation review was
READY with no material findings. PR #213 records the curated candidate's
publication review and exact-head CI separately.

The next milestone remains unselected. Package-validation cost, historical
lattice construction, defensible test replacements and useful local component
commands remain candidates. No broader cache, partial catalog, test cull or
application split is selected.

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

- [Closed milestone plan](phases/engineering-health/milestones/test-cost-and-coverage.md):
  result, preservation evidence and remaining choices.
- [Retrospective](milestone-retrospectives/2026-10-21-test-cost-and-coverage.md):
  reusable lessons and open questions.
- [ADR 0079](adr/0079-family-version-handover-and-containment.md).
- [Engineering Health roadmap](phases/engineering-health/engineering-health-roadmap.md).
- README, “Personal-item sale on Form 1099-K”.

## Parked

- Gain and break-even reporting on Form 8949 and Schedule D.
- Additional seller-paid shipping under platform pass-through.
- The adopted preferential-rate base taxes short-term covered gains at
  preferential rates. It is recorded and awaits owner disposition.
- The 22 fast-lane budget failures and phase-state validation in
  `governance_lint`: separate engineering-health candidates. Broad test
  redesign remains a later scope choice.
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
