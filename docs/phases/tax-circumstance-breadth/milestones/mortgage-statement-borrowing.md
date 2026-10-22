<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-statement-borrowing",
  "status": "Rebased onto core v50 / registry v48 / release v48 after PR #217. Earlier dynamic positive is historical; verify the candidate on the new base, then finish six boundary cases and four-outcome integration. Owner deferred clear-account; production not begun.",
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

### Current base after PR #217

This branch is rebased onto the merged 2025 tax-calculation milestone. The
adopted base is now core calculations **v50**, package registry **v48** and
release **v48**, not core v49 / registry v47 / release v47. Its 26 input
bindings are unchanged. The mortgage rules, family and ordinary-answer
contracts are unchanged; three other rule pins advance: standard deduction
v2, line16 v6 and selected preferential base v5. Verified tax parameters and
the capital-gains worksheet replace the older demo tax content.

The remaining disposable checks and eventual production successor must
extend that v50 package, preserving its newer pins, rather than clone v49
and silently revert the tax repair. In particular, a single-filer control
whose standard deduction wins now shows $15,750, not the earlier $15,000.
Schedule A requirement checks must use the adopted standard deduction too.
Validate the new package/release/checksum chain and inspect the actual saved
return result on the changed base before reusing the earlier consumer claim.

P2/P3 and the first T0 runtime result remain historical evidence at their
recorded package hashes. Their synthetic v50–v55 package numbers describe
disposable content, **not** the now-published core v50 or reservations of
future production versions. Do not rewrite those observations or overwrite
published content. Preserve historical helper defaults; make the current T0
candidate explicitly choose its v50 base. Production takes the next unused
package and registry versions when its unit is actually chartered.

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
  distinct from a nonempty account whose support is unresolved. P3's actual
  v49 control clarifies the incumbent implementation: line8a is inapplicable,
  the separate closed-empty Schedule A total publishes zero, and line12e
  follows its existing no-statement path. Family authorization of a zero must
  not be mistaken for an existing numeric line8a publication.
- Raw Box 3 dates stay report-local, but their agreed origination date supplies
  the borrowing-wide debt category. Disagreement is a conflict, never a date
  selection. Retain the incumbent conservative $750,000/$375,000 limit and
  exclusion for origination on or before 1987-10-13; the higher pre-2017
  acquisition-debt limit is not modeled.
  The saved explanation must disclose that coverage limit.
- P1 incorporates the outside findings and the
  [independent Sol review](../../../reviews/mortgage-statement-borrowing/p1-independent-review.md)
  in one connected repair: correct empty-family handling, a real report-local
  rival, Box 3/category reconciliation, and explicit exit limitations. The
  independent paper verdict was REPAIR REQUIRED; the combined repair is not
  experiment evidence or a new production verdict.

### Selected ordinary-answer scope

The owner selected **A: report-local ordinary answers**. Retain all nine
existing ordinary answers on each report; add only the continuing-borrowing
claim, exact report links, annual ceiling and other-debt answer at their stated
scopes. The candidate successor line8a rule reads the common account once.
A grouped interaction may gather each report's confirmations together; equal
answers remain separate assertions with their own evidence and history.

This reuses established meanings and scopes rather than introducing shared
ordinary assertions now. Its person cost is confirmation for each report.
B remains a possible later extension: genuinely borrowing-wide ordinary
assertions propagated through link-dependent derived findings. It is not
promised work in this milestone, and existing report-local history must never
be reinterpreted as such a shared assertion. The
[P1 comparison](mortgage-statement-borrowing-evidence/p1-connected-account.md)
retains the cost and provenance distinction.

### Open evidence and next action

- P2 tested the existing student-loan `rule.sli-answer-status-*.json` pattern:
  declared `joined` and `direction: joined_contains_subject` already cause
  keyed source admission. Its own-report dependency chains are independently
  verified; a new Form-1099-K-style admission allowlist is not needed for
  the tested inputs.
- The owner deferred the clear-account action for this milestone. This is an
  accepted delivery limit, not a permanent product policy. Corrections and
  withdrawals remain supported; they must not silently resume a favorable
  legacy route. An explicit exit can be designed in later work.
- Sol accepted the [executed P2 experiment](mortgage-statement-borrowing-evidence/p2-option-a-results.md)
  under the existing P1 review unit, for production-design consolidation only.
  Its baseline derived $11,000 through a
  readiness selection plus one ordinary family-authorized collector, but the
  singleton mortgage projector rejected the multi-report result; no durable
  baseline report/model exists. All five isolated mutations withheld the
  amount and completed durable output. The source assertions were supplied;
  recorder, lifecycle and group-reader delivery remain unproved. Box 3
  disagreement currently blocks on an absent common scalar, not a saved
  conflict-specific explanation.
- Sol accepted the [P3 contract/evidence](mortgage-statement-borrowing-evidence/p3-saved-model-results.md)
  for Track 0 consolidation, not production readiness. Its bounded repairs
  clarify connected-singleton support, the current integration artifact and
  successful evidence locators. Finish the exact dynamic borrowing admission,
  current route/lifecycle and six closure artifacts under the
  [consolidation charter](../../../reviews/mortgage-statement-borrowing/charter-t0-connected-closure.md).
  The owner accepted deferral of a clear-account action; that scope choice
  no longer blocks consolidation. The returned contract draft still requires
  Foreman review and bounded repair: numeric link coverage cannot consume a
  category result, and per-borrowing publications need an explicit fan-in
  before the sole ordinary line8a collector can use them. The corrected
  design must preserve a subject when its ceiling is missing, ignore a
  dormant unrelated ceiling, and gate the actual empty-family consumers on
  an affirmative orphan without making a withdrawn old link an orphan.
  These are unexecuted declaration obligations, not a demonstrated engine
  gap or a change to the product goal. Complete Track 0 before production.
  The paper return repeated a `link_count` node that package validation
  permits only once, and left the multi-outcome report status unvalidated.
  Settle that composition in one bounded disposable package/coordinator
  check under the same charter, using existing intermediate rules if needed.
  Test dynamic borrowing collisions and the connected-singleton, withdrawn,
  true-empty and affirmative-orphan boundaries. Reuse reviewed P2/P3 evidence;
  supplied relationship claims are still not production recorder proof.
  The first dynamic-account candidate now resolves and publishes the supported
  pair through line8a, Schedule A total and line12e. Its final candidate and
  saved model are retained in [T0 results](mortgage-statement-borrowing-evidence/t0-dynamic-binding-results.md).
  This does not yet combine the separately validated four-outcome report
  status, nor establish the remaining six missing-support/transition cases.
  Do not commission further rounds merely to
  refine paper. A demonstrated need for allocation, refinancing, general
  identity or broader engine work returns as an owner scope choice.

P3 saves and reloads a two-report model. Its initial $11,000 case exposed an
early line12e attempt and did not require Schedule A. Two explicit disposable
content successors address those consumer boundaries: line12e waits for the
existing Schedule A total, and the attachment removes only an obsolete
legacy liability/payment presence check while retaining its seven boundary
value checks. The later $21,000 case publishes line12e and required Schedule A
with saved tie-out text and both source pins; removing one boundary answer
still blocks the attachment. Changed-content empty/singleton controls preserve
their actual calculation paths. These are prototype findings, not adopted
production changes. HTML serialization is not visible group-reader delivery.
Borrowing-reference admission, exact common-account selection, connected
one-report transitions and correction/withdrawal remain production-design
obligations. The clear-account exit is deferred by owner decision. The new
evidence refines the same goal rather than changing its scope.

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
