<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-statement-borrowing",
  "status": "P0 independently reviewed READY. P1 connected design awaits combined outside/Sol review repair and the owner's report-local versus shared-answer choice before the experiment. No production or schema successor selected.",
  "scope": [
    "extend the existing ordinary mortgage account to a bounded same-borrowing multiple-report case",
    "preserve report amounts, loan-level circumstances and their separate correction lifecycles",
    "establish a supported Schedule A result and saved explanation only after tax and production-path evidence"
  ],
  "non_goals": [
    "no refinancing, second-home, mixed-use, partial-payment or above-limit allocation calculator",
    "no automatic loan matching from names, account strings, amounts or property address",
    "no general assumption framework, free-text intake or broad engine redesign",
    "no changes to the separate projection-reuse performance milestone"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-overview.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md",
      "docs/milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md",
      "docs/milestone-retrospectives/2026-10-19-multiple-statement-circumstances.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md"
    ]
  }
}
-->

# One Home Loan, More Than One Interest Statement

Milestone key: mortgage-statement-borrowing.
Branch: milestone/mortgage-statement-borrowing-same-loan.
Opening base: origin/main after merged PR #214. New primary managed worktree;
rebased onto PR #215's merged fold-once projection-reuse result. See its
[retrospective](../../../milestone-retrospectives/2026-10-22-projection-reuse.md).

## What we are trying to accomplish

A person can receive two mortgage-interest statements even though they still
have one home loan—for example, after the company collecting payments changes.
The application should help the person describe that relationship, keep what
each form reports, and use the loan's circumstances to calculate and explain
the supported interest treatment. Two reports must not silently become two
borrowings, and saying they concern one borrowing must not erase either report.

The existing mortgage route obtains ordinary answers and saves an inspectable,
correctable result, but supports only one Form 1098. The opening case is one
continuing borrowing for one main home with two distinct reports in 2025.
Whether this case can stay within the existing calculation boundary is an
investigation question. No favorable result follows just from calling the
reports a pair.

This extends the earlier phase's completed breadth result; it does not retract
that result or imply that its original endpoint required more work. The useful
new distinction is a continuing borrowing versus the documents describing it.
Additional independent loans remain a contrast case, not promised coverage.

## What makes this uncertain

Interest reported for different periods may compose differently from a
reported outstanding balance. Naming one loan does not tell us which balance
or period the tax calculation needs. Counting the borrowing once is not a
license to choose the smaller balance, pick whichever form passes a limit,
or treat Box 2 as an annual average.

We must distinguish what the person recognizes and affirms, what a document
reports, what the application assumes, and what a tax rule establishes. A
complete set of recorded Forms 1098 is not automatically a complete account
of all home debt. The question and authority for each must be examined on its
own meaning. No new completeness claim or blanket favorable default is selected.

The current recorder, input transport, rule cardinality, debt-limit check,
closure and saved display may have different restrictions. Their names are not
evidence that two reports can reach the right loan and result. Existing sale
and student-loan mechanisms are candidates for reuse, not a selected loan model.

## Actions the team will take

1. **Review this opening account.** Independently examine whether the same-loan
   scope is useful and sufficiently bounded, what facts could defeat it, and
   whether the proposed investigation will expose those facts. Refine the plan
   before P0; do not demand a full implementation specification yet.
2. **Describe the case and verify current behavior (P0).** Explain in ordinary
   language what the person knows about the loan and reports. Verify the 2025
   reporting and deduction rules from primary sources, including balance dates,
   reporting periods, loan acquisition versus origination, and relevant limits.
   Trace the current adopted package through real recording, current support,
   marshalling, rule execution, Schedule A and saved explanation. Reproduce the
   actual second-statement stop through the offered path. Identify supplied,
   assumed, derived and unresolved information separately. Have P0 independently
   reviewed before selecting a representation.
3. **Establish the relationships and correction boundaries.** Separate the
   report, continuing borrowing, home, reported interest and balance observations.
   Identify a finite set of ordinary questions that can establish a material
   relationship without asking the person for a tax verdict. Work through
   correcting one form, correcting the shared account, withdrawing a link and
   adding a new report. Decide what remains supported and what needs renewed
   confirmation. Keep uncertainty different from a negative answer.
4. **Compare existing-first mechanisms and test decisive assumptions.** Inspect
   the adopted multi-statement subtotal/subject-result pattern and explicit
   relationship recording before proposing a schema or coordinator. Determine
   what belongs in content, recording or the engine. Use paper instances first;
   charter rival prototypes only for a consequential choice paper cannot settle.
   Specify the question, cheapest discriminating cases and evidence ceiling
   before running a probe. A supplied relationship or test-only declaration is
   not evidence that production obtained it. Review one connected design rather
   than commissioning a new full review for each prose refinement.
5. **Select and build the bounded path.** Return material scope choices to the
   owner. Establish any required contract and Track 0 closure before production.
   Charter small implementation units from the settled design, keeping existing
   single-statement behavior and saved history compatible. Refine track divisions
   only after the integration cost is known; no new schema version is allocated
   by this opening plan.
6. **Demonstrate, review and close.** Use the actual recorder, durable recovery,
   coordinator and reloaded saved presentation. Show which two reports contributed,
   what borrowing account was used, why the result follows and how one correction
   changes it. Keep focused regression and typing evidence; full ready-PR CI is
   the gate. Curate the result and assess this bounded extension, rather than
   automatically adding another mortgage scenario.

Each stage changes the plan only as evidence increases specificity. Keep the
high-level goal current. If it changes, record the reason; do not rename an
unresolved prerequisite as completed breadth. Record consequential product
decisions with their grounds and implications, not a transcript of every check.

## Cases that will shape the design

- Two genuine reports for one continuing borrowing, with different interest
  amounts and balance observations. Determine the required treatment; do not
  predeclare a principal formula.
- Identical-looking reports that instead concern two different borrowings;
  a duplicate or corrected report; and a person unable to establish the link.
  Similar amounts, labels or addresses do not decide the relationship.
- A deliberately over-limit debt and balances that would cross a limit if
  incorrectly added. A fixture whose principal never reaches the comparison
  is not a useful limit test.
- Correct one reported amount without changing the borrowing; change or
  withdraw the report-to-borrowing account; remove and re-record a report;
  preserve unrelated statements and saved history.
- No reports, one report and two reports; late entry after closure; missing
  or contrary ordinary answers. Do not let an omitted report produce a
  favorable partial sum, or a withdrawn answer silently resume a default.
- Preserve the incumbent single-statement mortgage route and neighboring
  sale/student-loan behavior. Scope of each shared change determines regressions.

These are investigation classes, not an exhaustive list of human statements.
Only questions material to the relationship, tax treatment or actionable
coverage limit belong in the supported interaction.

## Design state

The high-level goal is unchanged: keep two reports about one continuing home
borrowing separate while calculating and explaining their supported interest
treatment. No production path or schema successor has been selected.

### Settled understanding and its grounds

- P0 is independently reviewed READY for connected design. The
  [current-path account](mortgage-statement-borrowing-evidence/p0-current-account.md)
  and [review/recheck](../../../reviews/mortgage-statement-borrowing/p0-independent-review.md)
  distinguish the actual v49/v47 route from manually supplied diagnostic
  answers. Two-report review/save remains unsupported; the calculation loses
  report-local authority even when equal values permit publication.
- Each report's amounts, dates and ordinary-answer history remain separate.
  Filing status remains return-wide. A continuing-borrowing claim and exact
  report links do not by themselves establish deductibility or debt coverage.
- The provisional balance source is a person-confirmed numeric annual ceiling,
  not a selected Box 2 snapshot. A bound within the applicable limit can
  support that condition; a loose bound above it does not prove actual excess.
  The separate other-debt answer covers secured borrowing on either home;
  known additional debt is unsupported here and unknown coverage is unresolved.
- The existing F1098 family authorizes exactly Schedule A line8a. A successor
  must retain that symbol and the actual closure scope, not publish an
  unauthorized generic subtotal. Genuine closed-empty authority remains
  distinct from a nonempty account whose support is unresolved.
- Raw Box 3 dates stay report-local, but their agreed origination date supplies
  the borrowing-wide debt category. Disagreement is a conflict, never a date
  selection. Retain the incumbent conservative $750,000/$375,000 limit and
  pre-1987 exclusion; the higher pre-2017 acquisition-debt limit is not modeled.
  The saved explanation must disclose that coverage limit.

### Owner decision before the intermediate-join experiment

Choose the ordinary-answer scope for this bounded delivery:

- **Report-local rival:** keep all nine existing ordinary answers keyed to
  each report; add only the continuing-borrowing claim, exact report links,
  annual ceiling and other-debt answer at their stated scopes. The successor
  line8a rule reads the common account once.
- **Shared-answer candidate:** allow genuinely borrowing-wide ordinary
  assertions to cover both linked reports through actual derived per-report
  intermediates that pin the assertion and each report's link.

The shared candidate was a Foreman preference, not an owner selection. Compare
the additional person effort against recording/content/lifecycle and provenance
cost before choosing it. Do not run its intermediate-join experiment before
the owner answers. Neither option permits A's report-local evidence to stand
in for B's. The
[P1 connected account](mortgage-statement-borrowing-evidence/p1-connected-account.md)
must carry both options and the resulting disposition.

### Open evidence and next action

- Combine the outside review with the
  [independent Sol P1 review](../../../reviews/mortgage-statement-borrowing/p1-independent-review.md)
  as one Luna repair. Its verdict is REPAIR REQUIRED for the empty-family
  contradiction, omitted report-local rival and unspecified Box 3/limit source.
- Test the existing student-loan `rule.sli-answer-status-*.json` pattern:
  declared `joined` and `direction: joined_contains_subject` already cause
  keyed source admission. Prefer that real content path to a new
  Form-1099-K-style allowlist unless it demonstrably fails for these inputs.
- Make connected-route exit explicit, or identify the lack of exit as a
  deliberate product limit. Withdrawal must not silently resume a favorable
  legacy route.
- Once the owner chooses and the connected repair is ready, run the bounded
  real-coordinator experiment, including unequal report answers, missing
  membership, principal/ceiling conflict, loose ceiling and conflicting Box 3
  dates. Include the intermediate-producer removal only if the shared route
  is selected. Raw synthetic inputs are supplied; derived results must
  actually execute. No ordinary-recorder or saved-reader delivery is proved
  by this feasibility check.
- Then settle the integration cost and complete Track 0 adversarial closure
  before any production charter. Do not commission further rounds merely to
  refine paper. A demonstrated need for allocation, refinancing, general
  identity or broader engine work returns as an owner scope choice.

### Completion boundary

Track 0 adversarial closure is PENDING. Completion remains a recordable,
calculable and saved-explainable bounded same-borrowing case with exact report
provenance and demonstrated correction/withdrawal behavior. Existing
single-report behavior and saved history stay compatible. If the evidence
defeats that boundary, return a specific partial result and owner choice.

Only synthetic demo accounts enter committed evidence. No schema version is
allocated; existing published schemas and contracts remain in force. Broad
verification remains CI's gate, not a repeated full suite for paper changes.

## Planning sources

- The prior mortgage and multiple-statement plans and their retrospectives
  named in this plan's planning reads. Their one-Form-1098 boundary remains
  the starting point, not evidence of a multi-report calculation.
- [2025 Publication 936](https://www.irs.gov/pub/irs-prior/p936--2025.pdf):
  general deductibility, debt limits and average-balance methods. P0 must
  establish which provisions the selected class actually needs.
- [Form 1098 instructions, April 2025](https://www.irs.gov/pub/irs-prior/i1098--2025.pdf),
  Boxes 1, 2, 3 and 11: reported interest and dated principal/origination/acquisition
  observations. Opening inspection confirms those distinctions, not a complete
  same-loan deduction method. P0 must reconcile any stale tax-summary language
  against the actual 2025 rules rather than extending it to later years.
