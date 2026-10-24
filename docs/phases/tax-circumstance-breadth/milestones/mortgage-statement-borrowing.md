<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-statement-borrowing",
  "status": "Shared-answer scheduling and explicit-exit prototypes are measured. Finish uncertainty and the six connected-design artifacts for Sol review. No production built.",
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

The owner has now brought two previously deferred capabilities into this
milestone: explicitly leaving a connected account, and giving suitable
ordinary answers about the borrowing once rather than separately for each
report. This is a deliberate scope expansion, not new evidence that the
report-local design failed. Establish the report-local foundation first,
then add shared answers without changing the meaning of existing history.

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

### Current base after PR #219

The branch now includes core calculations **v52**, registry **v50**, release
**v50** (refund or amount owed). It retains the 26 input bindings. Mortgage,
standard-deduction and line12e members are unchanged from v51; the two changed
existing pins are IRA vocabulary v3 and direct foreign-tax-credit rule v2,
alongside the new withholding/payment/refund members. Preserve that complete
adopted surface; do not downgrade it to simplify the mortgage fixture.

Use the first repaired shared-answer case as the new-base consumer check,
not an extra rerun of the unchanged historical set. Validate its full package,
registry and release chain. Unrelated refund inputs may remain unresolved:
this milestone does not claim that its mortgage fixtures are complete returns.
Select unused temporary package versions explicitly: the previous intermediate
v52 now collides with adopted core v52. Earlier v59 observations and hashes
stay historical, not rewritten as current-base proof or version reservations.

### Retained v51 base and fixture inputs

The branch now includes the merged senior/dependent-deduction milestone:
core calculations **v51**, registry **v49**, release **v49**. Mortgage
contracts and the 26 input bindings are unchanged. Preserve every adopted
member, including standard deduction v3 and line13b v2, when extending this
base. The newer dependent worksheet needs an explicit synthetic answer to
`standard-deduction.can-be-claimed-as-dependent`; the older student-loan
"is claimed" answer is not interchangeable. Supply the separate
`schedule1a.no-parts-ii-iv-deductions-declared` answer where needed. These are
labelled fixture assertions, not new defaults or a selected intake policy.
Inspect conditional SSN dependencies if reached; do not change the case to
evade a missing dependency.

Before continuing the remaining cases, validate one supported pair on this
changed consumer base and inspect its saved outcomes and exact pins. Keep
the previous observations below as historical evidence, not current-base
proof. The old P2 helper's temporary v51 now collides with an adopted package:
the T0 caller must explicitly select unused intermediate and final temporary
versions, without replacing published bytes or reserving production versions.
Historical helper defaults and results stay intact.

### Retained evidence on the preceding base

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

That current-base positive is now recorded in the T0 results: a disposable
v56 successor resolves with 494 members and its one run publishes line8a
$11,000, Schedule A total and line12e $15,750. The standard-deduction rule
v2 and verified base parameter are pinned. Foreman inspection of the retained
candidate confirms that only the four intended mortgage/consumer member pins
change from core v50; its other member pins and retained source package and
registry are unchanged. Line16 v6 and preferential-base v5 are retained, but
this fixture lacks unrelated line16 inputs and does not demonstrate tax
computation. Remaining display/lifecycle proof is listed below.

The two A/B ceiling calculations have since executed: absent A cannot borrow
B's otherwise-favorable ceiling, and valid A still publishes with dormant B's
unfavorable ceiling present. The retained derivation lineage identifies A.
The original P3 adapter scanned current claims without borrowing scope,
displaying B as A's support or rejecting two ceilings. A T0-only adapter
repair now saves both models using the current root's structured account
keys: absent A's ceiling is omitted, and dormant B's ceiling is never shown
as A support. Applicable raw claims are not automatically consumed inputs;
actual derivation pins establish consumption. These are experimental saved
models, not production projection or visible reader delivery.

The core-v51-derived v58 candidate now executes the four outcome counts and
their per-report status fan-in. Its corrected saved cases show remaining A
at $8,000 line8a and $15,750 line12e; withdrawal withholds both amounts;
true-empty preserves inapplicable line8a, Schedule A total zero and published
line12e; an affirmed orphan blocks line12e through a separate exact-link
integrity result. The ordinary line12e keeps its lazy arithmetic and ordering
dependency rather than requiring line8a on empty. The T0-only adapter handles
connected singleton and withdrawn states without invented answer pins. The
[T0 results](mortgage-statement-borrowing-evidence/t0-dynamic-binding-results.md)
retain the earlier failures, corrected same-borrowing inputs and actual saved
records. These are supplied after-states, not recorder lifecycle or production
acceptance. The restored scope below and connected independent review remain.

P2/P3 and the first T0 runtime result remain historical evidence at their
recorded package hashes. Their synthetic v50–v55 package numbers describe
disposable content, **not** the now-published core v50 or reservations of
future production versions. Do not rewrite those observations or overwrite
published content. Preserve historical helper defaults; make the current T0
candidate explicitly choose the current adopted base. Production takes the next unused
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
ordinary assertions in the foundation. Its person cost is confirmation for
each report. The owner's latest direction brings **B after A** into scope:
explicit borrowing-wide ordinary assertions, connected to reports through
derived support. First identify which propositions genuinely have that scope;
do not widen a payment-period answer merely to avoid asking it twice.
Existing report-local history must never be reinterpreted as a shared assertion. The
[P1 comparison](mortgage-statement-borrowing-evidence/p1-connected-account.md)
retains the cost and provenance distinction.

### Restored work and its next decisions

After the four remaining foundation cases, refine the connected contract in
one small design increment before another experiment or production charter:

1. Describe the explicit action that ends use of a connected account. Say
   what it ends, which independent answers survive, and how a remaining
   report can use the incumbent route. Clearing an account is not deleting
   source reports, erasing history, declaring all debt absent or silently
   turning a withdrawal into a favorable answer. Two independent reports do
   not become a supported singleton when the account is cleared.
2. Compare each of the nine existing propositions with an explicitly shared
   version. Specify its subject and period, how it reaches each linked
   report, and what happens when a report-local answer differs or a link or
   shared answer changes. Prefer actual existing declared joins and pinned
   intermediates to copied assertions or a domain-specific admission list.
3. State the smallest discriminating cases and implementation cost, then
   execute only the new mechanism questions. Keep supplied relationships
   separate from demonstrated recording, calculation and saved display.
   Review this together with the foundation as one connected design.

The intended outcome includes both capabilities. The representation and exact
coexistence rules are not selected by this scope change; derive them from
the propositions and evidence. Refinancing, independent-loan aggregation,
allocation and the higher grandfathered debt limit remain excluded, not
silently restored as "deferred work".

The first proceeds-use composition now has five saved coordinator cases:
shared-only with local absent, agreeing answers, disagreement in both assertion
orders, and shared retraction with independent local support retained. The
three supported cases publish line8a $11,000 and line12e $15,750; both
disagreements block. Their current explanation is generic `DEPENDENCY_INVALID`,
not a specific disagreement account. All five shared types are admitted, but
only proceeds-use is consumed in this experiment. See the current
[T0 results](mortgage-statement-borrowing-evidence/t0-dynamic-binding-results.md).
The raw states are supplied; no production recorder or shared-answer lifecycle
is claimed. Later evidence below addresses completion, cross-account isolation
and explicit exit. Uncertainty and the late-member/changed-support contract
remain in the final consolidation. A linked-only effective-answer producer
cannot silently become a prerequisite of the old unlinked singleton's reason.

The independent checkpoint verified those saved observations and actual pins,
but found that the derived-marker counts do not declare a completion barrier
before counting marker publications. The observed run order is not a general
guarantee. ADR 0076 does not promise an implicit producer edge for
`link_count.links`; this is a candidate composition gap, not an established
engine-contract violation. Close that property before the exit experiment.
First investigate counts of the actual recorded answers at their natural
report/borrowing subjects, with explicit predecessor references for consuming
their results; this may remove the unguaranteed derived-row count. Do not
replace unresolved production with zero, or require publication of a marker
whose correct outcome is absence. Preserve the accepted historical evidence
ceiling and return any necessary contract change explicitly.

The repaired core-v52-derived candidate now counts recorded local answers per
report and recorded shared answers per borrowing/year. Its effective-answer
consumer explicitly requires those two numeric results. With that consumer
declared first, three saved coordinator cases support shared-only A, block
contradictory local/shared answers, and refuse to use unrelated B support for
A. The candidate preserves all 545 adopted member IDs, with four intended
successors and no removed IDs. The results and exact pins are retained in the
T0 account. This is a measured proceeds-use repair, not runtime proof for the
other four shared propositions, a reference-runner execution, or production
recording. Sol's focused recheck closed the completion finding and accepted
the exact consumed lineage. The exit increment now preserves a qualified
singleton's $8,000, yields zero for a no-payment singleton, and blocks two
unconnected reports. A changed connected case also works when its reason is
declared before the effective producer. These are supplied-state coordinator
and saved-model observations, not production recording. The latest T0 account
retains the rejected shortcuts as failures. Finish the uncertainty case and
late-member contract/acceptance trace, then obtain the connected Sol verdict.

### Open evidence and next action

- P2 tested the existing student-loan `rule.sli-answer-status-*.json` pattern:
  declared `joined` and `direction: joined_contains_subject` already cause
  keyed source admission. Its own-report dependency chains are independently
  verified; a new Form-1099-K-style admission allowlist is not needed for
  the tested inputs.
- The owner restored the clear-account action and borrowing-wide answers.
  Design them as set out above; correction or withdrawal alone must still
  not silently resume a favorable legacy route.
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
  The restored work above must join that contract before closure. The dynamic
  account collisions and four foundation lifecycle cases are now measured at
  their stated prototype ceiling; numeric coverage and per-report status use
  actual declared intermediates. Next refine the explicit exit/shared-answer
  contract, test its genuinely new mechanism questions, and obtain the planned
  connected independent review. Reuse prior evidence; supplied relationship
  claims are still not production recorder proof. Complete Track 0 before
  production. Allocation, refinancing, general identity and broader engine work
  remain outside this scope.

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
obligations. The owner-restored exit and shared-answer work expands the
delivery boundary; earlier experiments establish only the foundation.

### Completion boundary

Track 0 adversarial closure is PENDING. Completion remains a recordable,
calculable and saved-explainable bounded same-borrowing case with exact report
provenance and demonstrated correction/withdrawal behavior. Existing
single-report behavior and saved history stay compatible. If the evidence
defeats that boundary, return a specific partial result and owner choice.
The restored scope also requires an explicit connected-account exit and
truthfully scoped borrowing-wide answers with inspectable per-report support.
Their contracts and new mechanism evidence must settle before dependent
production tracks; the foundation's earlier evidence alone does not close them.

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
